#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests/runtime-regression-cases.json"
INSTRUCTIONS_PATH = ROOT / "gpt-configuration/gpt-instructions.txt"
PREAMBLE_PATH = ROOT / "portable/START-HERE-PREAMBLE.md"
BUILD_PATH = ROOT / "scripts/build_distributions.py"

REQUIRED_CASE_IDS = {
    "missing-topic-sv",
    "missing-topic-en",
    "technology-sv",
    "product-current-info-sv",
    "method-timeless-sv",
    "trend-en",
    "neutral-org-baseline-sv",
    "public-sector-context-sv",
    "mixed-language-latest-request",
    "single-recommendation-guardrail",
    "chat-no-knowledge-dependency",
    "fixed-section-order-sv",
}

REQUIRED_RUNTIME_RULES = {
    "missing-topic": [
        "ask exactly one concise question for the missing topic and stop",
        "Do not create a generic one-pager about the category unless explicitly requested",
    ],
    "language": [
        "Use the same language as the user's latest substantive request",
        "Use that language throughout headings, tables, recommendation labels, explanatory text and next steps",
    ],
    "classification": [
        "Classify the topic as exactly one primary category",
        "Technology",
        "Platform",
        "Product",
        "Method",
        "IT trend",
    ],
    "freshness": [
        "CURRENT-INFORMATION CHECK",
        "If uncertain whether freshness matters, prefer current sources",
    ],
    "recommendation": [
        "Choose exactly one recommendation",
        "Never combine recommendation labels",
        "Adopt / Inför",
        "Trial / Testa",
        "Assess / Utvärdera",
        "Hold / Avvakta",
    ],
    "organization": [
        "medium-to-large organization",
        "do not invent an industry, regulatory regime, architecture, product estate, cloud strategy or maturity level",
    ],
    "public-sector": [
        "When the known context is public-sector or government",
        "procurement, security, compliance, data-governance and exit considerations",
    ],
    "knowledge-independence": [
        "core behavior must not depend on locating a particular knowledge file",
    ],
    "export": [
        "After the completed one-pager, offer a downloadable version in PDF, Confluence wiki markup, Markdown or Microsoft Word/DOCX",
        "Do not discuss export before the one-pager is complete",
        "the available export formats are offered after it",
    ],
}

SWEDISH_HEADINGS = [
    "Sammanfattning",
    "Klassificering",
    "Vad det är",
    "Varför det är relevant",
    "Typiska användningsfall",
    "Arkitekturpåverkan",
    "Styrkor",
    "Begränsningar och risker",
    "Säkerhet, regelefterlevnad och styrning",
    "Mognad och ekosystem",
    "Passform för myndighets- och enterprise-kontext",
    "Rekommendation",
    "Föreslagna nästa steg",
    "Källor och tillförlitlighet, när relevant",
]

ENGLISH_HEADINGS = [
    "Executive summary",
    "Classification",
    "What it is",
    "Why it matters",
    "Typical use cases",
    "Architecture impact",
    "Strengths",
    "Limitations and risks",
    "Security, compliance and governance",
    "Maturity and ecosystem",
    "Fit for public-sector / enterprise context",
    "Recommendation",
    "Suggested next steps",
    "Sources and confidence, when applicable",
]


def fail(message: str) -> None:
    raise RuntimeError(message)


def assert_in_order(text: str, markers: list[str], label: str) -> None:
    cursor = 0
    for marker in markers:
        pos = text.find(marker, cursor)
        if pos < 0:
            fail(f"Missing or reordered {label} marker: {marker}")
        cursor = pos + len(marker)


def extract_heading_block(text: str, start_marker: str, end_marker: str) -> str:
    start = text.find(start_marker)
    if start < 0:
        fail(f"Missing heading block start: {start_marker}")
    end = text.find(end_marker, start + len(start_marker))
    if end < 0:
        fail(f"Missing heading block end: {end_marker}")
    return text[start:end]


def validate_cases(data: dict) -> None:
    if data.get("suite") != "architecture-one-pager-small-model-runtime":
        fail("Unexpected regression suite name")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        fail("Regression suite must contain cases")

    ids = [case.get("id") for case in cases]
    if len(ids) != len(set(ids)):
        fail("Regression case ids must be unique")
    missing = REQUIRED_CASE_IDS - set(ids)
    if missing:
        fail(f"Missing required regression cases: {sorted(missing)}")

    for case in cases:
        cid = case.get("id")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            fail(f"Regression case {cid} has no prompt")
        expected = case.get("expected")
        if not isinstance(expected, dict) or not expected:
            fail(f"Regression case {cid} has no expected contract")
        if expected.get("action") not in {"ask_for_topic_and_stop", "produce_one_pager"}:
            fail(f"Regression case {cid} has unsupported expected action")
        if expected.get("action") == "produce_one_pager" and expected.get("recommendation_count") != 1:
            fail(f"One-pager case {cid} must require exactly one recommendation")


def validate_runtime_contract(instructions: str) -> None:
    for group, markers in REQUIRED_RUNTIME_RULES.items():
        for marker in markers:
            if marker not in instructions:
                fail(f"Runtime contract no longer supports regression group {group}: missing {marker!r}")

    english_block = extract_heading_block(instructions, "English headings:", "Swedish headings:")
    swedish_block = extract_heading_block(instructions, "Swedish headings:", "Keep the output compact")
    assert_in_order(english_block, ENGLISH_HEADINGS, "English output heading")
    assert_in_order(swedish_block, SWEDISH_HEADINGS, "Swedish output heading")

    steps = re.findall(r"(?m)^([1-8])\. ([A-Z-]+(?: [A-Z-]+)*)$", instructions)
    if [n for n, _ in steps[:8]] != list("12345678"):
        fail("The canonical eight-step runtime sequence is missing or reordered")


def validate_chat_compilation() -> None:
    build = BUILD_PATH.read_text(encoding="utf-8")
    preamble = PREAMBLE_PATH.read_text(encoding="utf-8")
    if "build_chat_entrypoint" not in build:
        fail("Build script no longer compiles the portable Chat entrypoint")
    if "CANONICAL_INSTRUCTIONS" not in build or "CHAT_PREAMBLE" not in build:
        fail("Portable Chat build no longer derives from canonical instructions + preamble")
    if "portable ChatGPT distribution" not in preamble:
        fail("Portable Chat preamble lost its runtime identity marker")


def main() -> int:
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    instructions = INSTRUCTIONS_PATH.read_text(encoding="utf-8")
    validate_cases(data)
    validate_runtime_contract(instructions)
    validate_chat_compilation()
    print(f"Runtime regression contract OK: {len(data['cases'])} cases")
    print("Small-model gates covered: topic, language, classification, freshness, recommendation, org context, public sector, structure, export, chat independence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
