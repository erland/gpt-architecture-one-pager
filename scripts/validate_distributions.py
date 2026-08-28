#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
CANONICAL_INSTRUCTIONS = ROOT / "gpt-configuration/gpt-instructions.txt"
CHAT_PREAMBLE = ROOT / "portable/START-HERE-PREAMBLE.md"
KNOWLEDGE = sorted((ROOT / "knowledge").glob("*.md"))
EXAMPLES = sorted((ROOT / "examples").glob("*.md"))
CUSTOM_SOURCE_FILES = [
    ROOT / "README.md",
    ROOT / "gpt-configuration/gpt-name-and-description.md",
    CANONICAL_INSTRUCTIONS,
    ROOT / "gpt-configuration/conversation-starters.md",
    ROOT / "gpt-configuration/recommended-capabilities.md",
    ROOT / "setup/how-to-configure-the-gpt.md",
] + KNOWLEDGE + EXAMPLES

# These are intentionally plain-text semantic guardrails rather than a full parser.
# They catch accidental deletion or drift of behavior that lightweight models rely on.
REQUIRED_RUNTIME_MARKERS = [
    "1. LANGUAGE",
    "2. TOPIC CHECK",
    "3. CLASSIFICATION",
    "4. CURRENT-INFORMATION CHECK",
    "5. ASSESSMENT",
    "6. RECOMMENDATION",
    "7. OUTPUT",
    "8. EXPORT",
    "ask exactly one concise question",
    "Choose exactly one recommendation",
    "Never combine recommendation labels",
    "Executive summary",
    "Sammanfattning",
    "Adopt / Inför",
    "Trial / Testa",
    "Assess / Utvärdera",
    "Hold / Avvakta",
    "medium-to-large organization",
    "core behavior must not depend on locating a particular knowledge file",
    "FINAL SELF-CHECK BEFORE SENDING A ONE-PAGER",
    "the available export formats are offered after it",
]

REQUIRED_CHAT_MARKERS = [
    "portable ChatGPT distribution",
    "embedded canonical runtime instructions",
    "Core behavior must never depend on retrieving a particular knowledge file",
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assert_same(zf: zipfile.ZipFile, member: str, src: Path) -> None:
    actual = zf.read(member)
    expected = src.read_bytes()
    if actual != expected:
        raise RuntimeError(f"Content differs: {member} != {src.relative_to(ROOT)}")


def assert_contains(text: str, markers: list[str], label: str) -> None:
    missing = [m for m in markers if m not in text]
    if missing:
        raise RuntimeError(f"Semantic runtime validation failed for {label}; missing: {missing}")


def expected_chat_entrypoint() -> str:
    preamble = CHAT_PREAMBLE.read_text(encoding="utf-8").rstrip()
    instructions = CANONICAL_INSTRUCTIONS.read_text(encoding="utf-8").strip()
    return f"{preamble}\n\n{instructions}\n"


def validate_runtime_source() -> None:
    canonical = CANONICAL_INSTRUCTIONS.read_text(encoding="utf-8")
    assert_contains(canonical, REQUIRED_RUNTIME_MARKERS, "canonical Custom GPT instructions")

    if len(KNOWLEDGE) != 5:
        raise RuntimeError(f"Expected 5 knowledge files, found {len(KNOWLEDGE)}")
    if len(EXAMPLES) != 3:
        raise RuntimeError(f"Expected 3 golden examples, found {len(EXAMPLES)}")

    for path in KNOWLEDGE:
        text = path.read_text(encoding="utf-8").lower()
        if "runtime" not in text and "support" not in text and "reference" not in text:
            raise RuntimeError(f"Knowledge file does not clearly identify itself as supporting reference: {path.name}")

    for path in EXAMPLES:
        text = path.read_text(encoding="utf-8").lower()
        if "not a factual source" not in text and "inte en faktakälla" not in text:
            raise RuntimeError(f"Golden example lacks non-factual-source guardrail: {path.name}")


def validate_profile(profile: dict, target: str, version: str) -> None:
    if profile.get("package") != "architecture-one-pager":
        raise RuntimeError(f"Wrong package in {target} runtime profile")
    if profile.get("target") != target:
        raise RuntimeError(f"Wrong target in runtime profile: expected {target}")
    if profile.get("version") != version:
        raise RuntimeError(f"Wrong version in {target} runtime profile")
    if profile.get("core_behavior_requires_knowledge") is not False:
        raise RuntimeError(f"{target} profile must state that core behavior does not require knowledge retrieval")
    if profile.get("small_model_safe") is not True:
        raise RuntimeError(f"{target} profile must be marked small_model_safe")


def validate(version: str, dist: Path) -> None:
    if not SEMVER.fullmatch(version):
        raise RuntimeError(f"Invalid version: {version}")
    validate_runtime_source()

    custom_path = dist / f"architecture-one-pager-custom-gpt-v{version}.zip"
    chat_path = dist / f"architecture-one-pager-chat-v{version}.zip"
    for p in (custom_path, chat_path):
        if not p.is_file():
            raise RuntimeError(f"Missing distribution: {p}")
        with zipfile.ZipFile(p) as zf:
            bad = zf.testzip()
            if bad:
                raise RuntimeError(f"Corrupt ZIP member in {p.name}: {bad}")

    with zipfile.ZipFile(custom_path) as zf:
        for src in CUSTOM_SOURCE_FILES:
            assert_same(zf, src.relative_to(ROOT).as_posix(), src)
        if zf.read("VERSION").decode().strip() != version:
            raise RuntimeError("Wrong VERSION in Custom GPT package")
        canonical = zf.read("gpt-configuration/gpt-instructions.txt").decode("utf-8")
        assert_contains(canonical, REQUIRED_RUNTIME_MARKERS, "Custom GPT package instructions")
        profile = json.loads(zf.read("RUNTIME-PROFILE.json"))
        validate_profile(profile, "custom-gpt", version)
        if profile.get("entrypoint") != "gpt-configuration/gpt-instructions.txt":
            raise RuntimeError("Wrong Custom GPT runtime entrypoint")

    with zipfile.ZipFile(chat_path) as zf:
        assert_same(zf, "assistant/instructions.txt", CANONICAL_INSTRUCTIONS)
        assert_same(zf, "assistant/conversation-starters.md", ROOT / "gpt-configuration/conversation-starters.md")
        for src in KNOWLEDGE + EXAMPLES:
            assert_same(zf, src.relative_to(ROOT).as_posix(), src)
        if zf.read("VERSION").decode().strip() != version:
            raise RuntimeError("Wrong VERSION in portable package")

        start_here = zf.read("START-HERE.md").decode("utf-8")
        if start_here != expected_chat_entrypoint():
            raise RuntimeError("START-HERE.md was not compiled from the current preamble + canonical instructions")
        assert_contains(start_here, REQUIRED_CHAT_MARKERS + REQUIRED_RUNTIME_MARKERS, "portable chat START-HERE")

        profile = json.loads(zf.read("RUNTIME-PROFILE.json"))
        validate_profile(profile, "portable-chat", version)
        if profile.get("entrypoint") != "START-HERE.md":
            raise RuntimeError("Wrong portable chat runtime entrypoint")

        manifest = json.loads(zf.read("MANIFEST.json"))
        if manifest.get("version") != version:
            raise RuntimeError("Wrong version in MANIFEST.json")
        if manifest.get("entrypoint") != "START-HERE.md":
            raise RuntimeError("Wrong entrypoint in MANIFEST.json")
        if manifest.get("instructions") != "assistant/instructions.txt":
            raise RuntimeError("Wrong instructions path in MANIFEST.json")
        if manifest.get("runtime_profile") != "RUNTIME-PROFILE.json":
            raise RuntimeError("Wrong runtime profile path in MANIFEST.json")
        if manifest.get("knowledge") != [f"knowledge/{p.name}" for p in KNOWLEDGE]:
            raise RuntimeError("Knowledge list in MANIFEST.json differs from source")
        if manifest.get("examples") != [f"examples/{p.name}" for p in EXAMPLES]:
            raise RuntimeError("Example list in MANIFEST.json differs from source")

        hashed_members = manifest.get("sha256", {})
        expected_hashed = sorted(n for n in zf.namelist() if n != "MANIFEST.json")
        if sorted(hashed_members) != expected_hashed:
            raise RuntimeError("MANIFEST.json SHA-256 member list is incomplete or contains unexpected entries")
        for member, expected_hash in hashed_members.items():
            if digest(zf.read(member)) != expected_hash:
                raise RuntimeError(f"SHA-256 mismatch for {member}")

    print(f"Validation OK for Architecture One Pager v{version}")
    print("Semantic runtime checks OK: workflow, recommendation, language/output, small-model profile and compiled chat entrypoint")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(ROOT / "dist"))
    ap.add_argument("--version")
    args = ap.parse_args()
    version = args.version or (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    validate(version, Path(args.dist))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
