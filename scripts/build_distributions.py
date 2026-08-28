#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, shutil, tempfile, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
FIXED_DT = (2020, 1, 1, 0, 0, 0)

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


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_chat_entrypoint() -> str:
    preamble = CHAT_PREAMBLE.read_text(encoding="utf-8").rstrip()
    instructions = CANONICAL_INSTRUCTIONS.read_text(encoding="utf-8").strip()
    return f"{preamble}\n\n{instructions}\n"


def runtime_profile(target: str, version: str, entrypoint: str, instructions: str) -> dict:
    return {
        "package": "architecture-one-pager",
        "target": target,
        "version": version,
        "entrypoint": entrypoint,
        "canonical_instructions": instructions,
        "core_behavior_requires_knowledge": False,
        "knowledge_role": "optional-supporting-reference",
        "examples_role": "optional-style-quality-reference",
        "small_model_safe": True,
    }


def write_zip(src_dir: Path, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in sorted(x for x in src_dir.rglob("*") if x.is_file()):
            rel = p.relative_to(src_dir).as_posix()
            info = zipfile.ZipInfo(rel, FIXED_DT)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build_custom(stage: Path, version: str) -> None:
    for src in CUSTOM_SOURCE_FILES:
        copy_file(src, stage / src.relative_to(ROOT))
    write_text(stage / "VERSION", version + "\n")
    write_text(
        stage / "RUNTIME-PROFILE.json",
        json.dumps(runtime_profile("custom-gpt", version, "gpt-configuration/gpt-instructions.txt", "gpt-configuration/gpt-instructions.txt"), ensure_ascii=False, indent=2) + "\n",
    )


def build_chat(stage: Path, version: str) -> None:
    write_text(stage / "START-HERE.md", build_chat_entrypoint())
    copy_file(CANONICAL_INSTRUCTIONS, stage / "assistant/instructions.txt")
    copy_file(ROOT / "gpt-configuration/conversation-starters.md", stage / "assistant/conversation-starters.md")
    for src in KNOWLEDGE + EXAMPLES:
        copy_file(src, stage / src.relative_to(ROOT))
    write_text(stage / "VERSION", version + "\n")
    write_text(
        stage / "RUNTIME-PROFILE.json",
        json.dumps(runtime_profile("portable-chat", version, "START-HERE.md", "assistant/instructions.txt"), ensure_ascii=False, indent=2) + "\n",
    )

    files = {}
    for p in sorted(x for x in stage.rglob("*") if x.is_file() and x.name != "MANIFEST.json"):
        files[p.relative_to(stage).as_posix()] = sha256(p)
    manifest = {
        "package": "architecture-one-pager",
        "format": "portable-chat-assistant",
        "version": version,
        "entrypoint": "START-HERE.md",
        "instructions": "assistant/instructions.txt",
        "conversation_starters": "assistant/conversation-starters.md",
        "runtime_profile": "RUNTIME-PROFILE.json",
        "knowledge": [f"knowledge/{p.name}" for p in KNOWLEDGE],
        "examples": [f"examples/{p.name}" for p in EXAMPLES],
        "sha256": files,
    }
    write_text(stage / "MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", default=str(ROOT / "dist"))
    ap.add_argument("--version")
    args = ap.parse_args()
    version = args.version or (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise SystemExit(f"Invalid version: {version!r}. Expected SemVer without leading v.")
    if len(KNOWLEDGE) != 5:
        raise SystemExit(f"Expected 5 knowledge files, found {len(KNOWLEDGE)}")
    if len(EXAMPLES) != 3:
        raise SystemExit(f"Expected 3 example files, found {len(EXAMPLES)}")
    missing = [p for p in CUSTOM_SOURCE_FILES + [CHAT_PREAMBLE] if not p.is_file()]
    if missing:
        raise SystemExit("Missing required files: " + ", ".join(str(p.relative_to(ROOT)) for p in missing))

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        custom = base / "custom"
        chat = base / "chat"
        build_custom(custom, version)
        build_chat(chat, version)
        write_zip(custom, out / f"architecture-one-pager-custom-gpt-v{version}.zip")
        write_zip(chat, out / f"architecture-one-pager-chat-v{version}.zip")
    print(f"Built Architecture One Pager distributions v{version} in {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
