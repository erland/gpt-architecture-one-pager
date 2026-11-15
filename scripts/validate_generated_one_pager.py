#!/usr/bin/env python3
"""Deterministic checks of an actual saved Architecture One Pager response.

This is an output artifact validator, NOT a live model test and NOT proof that
cited URLs were opened or that their claims are correct.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

SV = (
    "Sammanfattning", "Klassificering", "Vad det är", "Varför det är relevant",
    "Typiska användningsfall", "Arkitekturpåverkan", "Styrkor",
    "Begränsningar och risker", "Säkerhet, regelefterlevnad och styrning",
    "Mognad och ekosystem", "Passform för myndighets- och enterprise-kontext",
    "Rekommendation", "Föreslagna nästa steg", "Källor och tillförlitlighet",
)
EN = (
    "Executive summary", "Classification", "What it is", "Why it matters",
    "Typical use cases", "Architecture impact", "Strengths",
    "Limitations and risks", "Security, compliance and governance",
    "Maturity and ecosystem", "Fit for public-sector / enterprise context",
    "Recommendation", "Suggested next steps", "Sources and confidence",
)
HEADER = re.compile(r"(?m)^\s*(?:#{1,4}\s*)?(\d{1,2})\.\s+(.+?)\s*$")
LINK = re.compile(r"https?://[^\s<>)\]]+")
PLACEHOLDER = re.compile(r"(?m)(?:\b(?:OWASP|Digg|IMY|NIST|OECD|Consilium|AI Act Service Desk)\b[^\n]{0,90}?\s+\+\d+\b)|(?:\s+\+\d+\s*$)|(?:\[[^\]]+\]\(\s*\))")
RECOMMENDATIONS = {
    "sv": ("Inför", "Testa", "Utvärdera", "Avvakta"),
    "en": ("Adopt", "Trial", "Assess", "Hold"),
}


def check_report(text: str, language: str = "sv", max_words: int = 750) -> list[str]:
    problems: list[str] = []
    lines = [(int(m.group(1)), m.group(2).strip(), m.start(), m.end()) for m in HEADER.finditer(text)]
    expected = SV if language == "sv" else EN
    if len(lines) != 14 or [item[0] for item in lines] != list(range(1, 15)):
        problems.append("Expected exactly 14 consecutively numbered sections (1-14)")
    else:
        for (number, actual, _, _), heading in zip(lines, expected):
            if not actual.casefold().startswith(heading.casefold()):
                problems.append(f"Wrong heading/order at section {number}: {actual}")
    if PLACEHOLDER.search(text):
        problems.append("Unresolved citation placeholder (e.g. '+1')")

    # Do not mistake a title banner's recommendation for a second section.
    section12 = ""
    if len(lines) == 14 and [row[0] for row in lines] == list(range(1, 15)):
        section12 = text[lines[11][3]:lines[12][2]]
    allowed = RECOMMENDATIONS[language]
    matched = [name for name in allowed if re.search(rf"(?im)^\s*(?:\*\*|[*-]\s*)?{re.escape(name)}(?:\*\*)?\s*(?:$|[—:])", section12)]
    if len(matched) != 1:
        problems.append("Section 12 must declare exactly one recommendation")
    if re.search(r"(?i)\b(?:Testa|Trial|Inför|Adopt)\s*/\s*(?:Utvärdera|Assess|Avvakta|Hold)\b", section12):
        problems.append("Mixed recommendation labels are not allowed")

    if len(lines) == 14 and [row[0] for row in lines] == list(range(1, 15)):
        source_section = text[lines[13][3]:]
        urls = [url.rstrip(".,;") for url in LINK.findall(source_section)]
        valid_urls = [
            url for url in urls
            if urlsplit(url).scheme in ("https", "http") and "." in (urlsplit(url).hostname or "")
        ]
        if not valid_urls:
            problems.append("Source section must contain at least one valid source URL")
        if re.search(r"(?i)(?:källor|sources).*(?:kontrollerats|verified|opened)", source_section) and not valid_urls:
            problems.append("Source verification is claimed but no inspectable URLs are provided")
        # Count the main report only, excluding reference URLs and export offer.
        main = text[lines[0][2]:lines[13][2]]
        main = LINK.sub("", main)
        words = re.findall(r"\b[\wÅÄÖåäö]+(?:[-’'][\wÅÄÖåäö]+)*\b", main, flags=re.UNICODE)
        if len(words) > max_words:
            problems.append(f"Main report too long: {len(words)} words (limit {max_words})")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Saved model response as Markdown/plain text")
    parser.add_argument("--language", choices=("sv", "en"), default="sv")
    parser.add_argument("--max-words", type=int, default=750)
    args = parser.parse_args()
    if not args.report.is_file():
        parser.error(f"Report file not found: {args.report}")
    problems = check_report(args.report.read_text(encoding="utf-8"), args.language, args.max_words)
    if problems:
        print("GENERATED ONE-PAGER: FAIL")
        for problem in problems:
            print(" -", problem)
        return 1
    print("GENERATED ONE-PAGER: PASS (structural evidence only; sources not independently checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
