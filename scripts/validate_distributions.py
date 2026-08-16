#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
KNOWLEDGE = sorted((ROOT / "knowledge").glob("*.md"))
EXAMPLES = sorted((ROOT / "examples").glob("*.md"))
CUSTOM_SOURCE_FILES = [
    ROOT / "README.md",
    ROOT / "gpt-configuration/gpt-name-and-description.md",
    ROOT / "gpt-configuration/gpt-instructions.txt",
    ROOT / "gpt-configuration/conversation-starters.md",
    ROOT / "gpt-configuration/recommended-capabilities.md",
    ROOT / "setup/how-to-configure-the-gpt.md",
] + KNOWLEDGE + EXAMPLES


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assert_same(zf: zipfile.ZipFile, member: str, src: Path) -> None:
    actual = zf.read(member)
    expected = src.read_bytes()
    if actual != expected:
        raise RuntimeError(f"Content differs: {member} != {src.relative_to(ROOT)}")


def validate(version: str, dist: Path) -> None:
    if not SEMVER.fullmatch(version):
        raise RuntimeError(f"Invalid version: {version}")
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

    with zipfile.ZipFile(chat_path) as zf:
        assert_same(zf, "assistant/instructions.txt", ROOT / "gpt-configuration/gpt-instructions.txt")
        assert_same(zf, "assistant/conversation-starters.md", ROOT / "gpt-configuration/conversation-starters.md")
        for src in KNOWLEDGE + EXAMPLES:
            assert_same(zf, src.relative_to(ROOT).as_posix(), src)
        if zf.read("VERSION").decode().strip() != version:
            raise RuntimeError("Wrong VERSION in portable package")
        manifest = json.loads(zf.read("MANIFEST.json"))
        if manifest.get("version") != version:
            raise RuntimeError("Wrong version in MANIFEST.json")
        if manifest.get("instructions") != "assistant/instructions.txt":
            raise RuntimeError("Wrong instructions path in MANIFEST.json")
        for member, expected_hash in manifest.get("sha256", {}).items():
            if digest(zf.read(member)) != expected_hash:
                raise RuntimeError(f"SHA-256 mismatch for {member}")

    print(f"Validation OK for Architecture One Pager v{version}")


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
