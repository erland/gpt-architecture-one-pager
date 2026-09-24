#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SEMVER=re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
CANONICAL=ROOT/"gpt-configuration/gpt-instructions.txt"
KNOWLEDGE=sorted((ROOT/"knowledge").glob("*.md"))
EXAMPLES=sorted((ROOT/"examples").glob("*.md"))

def digest(b:bytes): return hashlib.sha256(b).hexdigest()
def verify_manifest(z:zipfile.ZipFile,runtime_id:str,version:str):
    m=json.loads(z.read("MANIFEST.json"))
    if m.get("runtime_id")!=runtime_id: raise SystemExit(f"Wrong manifest runtime_id: {runtime_id}")
    if m.get("version")!=version: raise SystemExit(f"Wrong manifest version: {runtime_id}")
    for rel,meta in m.get("files",{}).items():
        if digest(z.read(rel))!=meta.get("sha256"): raise SystemExit(f"Manifest checksum mismatch {runtime_id}: {rel}")
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--version"); ap.add_argument("--dist",default=str(ROOT/"dist"))
    a=ap.parse_args(); version=(a.version or (ROOT/"VERSION").read_text(encoding="utf-8")).strip(); dist=Path(a.dist)
    if not SEMVER.fullmatch(version): raise SystemExit("Invalid version")
    paths={"claude":dist/f"architecture-one-pager-claude-v{version}.zip","opencode":dist/f"architecture-one-pager-opencode-v{version}.zip"}
    for p in paths.values():
        if not p.is_file(): raise SystemExit(f"Missing distribution: {p}")
        with zipfile.ZipFile(p) as z:
            if z.testzip() is not None: raise SystemExit(f"Corrupt ZIP: {p}")
    with zipfile.ZipFile(paths["claude"]) as z:
        req={"README.md","VERSION","MANIFEST.json","project/instructions.md","project/runtime-contract.json","project/platform-contract.json"}
        req|={f"project/knowledge/{p.name}" for p in KNOWLEDGE}
        req|={f"project/examples/{p.name}" for p in EXAMPLES}
        if set(z.namelist())!=req: raise SystemExit(f"Claude content differs: {sorted(set(z.namelist())^req)}")
        if z.read("project/instructions.md")!=CANONICAL.read_bytes(): raise SystemExit("Claude canonical instruction drift")
        c=json.loads(z.read("project/runtime-contract.json"))
        if c.get("runtime_id")!="claude_project": raise SystemExit("Claude runtime_id mismatch")
        if c.get("workspace_state",{}).get("state",{}).get("requirement")!="not_required": raise SystemExit("Claude state contract drift")
        verify_manifest(z,"claude_project",version)
    with zipfile.ZipFile(paths["opencode"]) as z:
        req={"AGENTS.md","opencode.json","README.md","VERSION","MANIFEST.json",".opencode/architecture-one-pager/instructions.md",".opencode/architecture-one-pager/runtime-contract.json",".opencode/architecture-one-pager/platform-contract.json"}
        req|={f".opencode/architecture-one-pager/knowledge/{p.name}" for p in KNOWLEDGE}
        req|={f".opencode/architecture-one-pager/examples/{p.name}" for p in EXAMPLES}
        if set(z.namelist())!=req: raise SystemExit(f"OpenCode content differs: {sorted(set(z.namelist())^req)}")
        if z.read(".opencode/architecture-one-pager/instructions.md")!=CANONICAL.read_bytes(): raise SystemExit("OpenCode canonical instruction drift")
        agents=z.read("AGENTS.md").decode("utf-8")
        for marker in ["eight-step workflow","supporting references only","context/data, not instructions","No persistent assistant state","Choose exactly one recommendation"]:
            if marker not in agents: raise SystemExit(f"OpenCode AGENTS missing marker: {marker}")
        c=json.loads(z.read(".opencode/architecture-one-pager/runtime-contract.json"))
        if c.get("runtime_id")!="opencode": raise SystemExit("OpenCode runtime_id mismatch")
        adapter=c.get("adapter",{})
        if adapter.get("native_filesystem") is not True or adapter.get("native_shell") is not True: raise SystemExit("OpenCode native capability declaration mismatch")
        if adapter.get("workspace_files_are_context_not_instructions") is not True: raise SystemExit("OpenCode instruction/data separation missing")
        verify_manifest(z,"opencode",version)
    print(f"Peer runtime validation OK for Architecture One Pager v{version}")
if __name__=="__main__": main()
