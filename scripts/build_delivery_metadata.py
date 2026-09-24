#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, sys

ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--version"); ap.add_argument("--dist",default=str(ROOT/"dist"))
    a=ap.parse_args(); version=(a.version or (ROOT/"VERSION").read_text(encoding="utf-8")).strip(); dist=Path(a.dist)
    files=[
      ("project_zip",dist/f"architecture-one-pager-project-v{version}.zip"),
      ("custom_gpt_zip",dist/f"architecture-one-pager-custom-gpt-v{version}.zip"),
      ("chat_zip",dist/f"architecture-one-pager-chat-v{version}.zip"),
      ("claude_zip",dist/f"architecture-one-pager-claude-v{version}.zip"),
      ("opencode_zip",dist/f"architecture-one-pager-opencode-v{version}.zip"),
    ]
    missing=[p.name for _,p in files if not p.exists()]
    if missing: print("Missing: "+", ".join(missing),file=sys.stderr); return 1
    rows=[{"type":t,"file":p.name,"sha256":sha(p),"bytes":p.stat().st_size} for t,p in files]
    (dist/"DELIVERY-MANIFEST.json").write_text(json.dumps({"schema_version":1,"version":version,"artifacts":rows,"runtime_status":{"chatgpt_chat":"ready_active","chatgpt_custom":"ready_active","claude_project":"ready_active","opencode":"ready_active","openai_plugin":"reduced_inactive"}},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (dist/"SHA256SUMS.txt").write_text("".join(f"{r['sha256']}  {r['file']}\n" for r in rows),encoding="utf-8")
    print(dist/"DELIVERY-MANIFEST.json"); print(dist/"SHA256SUMS.txt"); return 0
if __name__=="__main__": raise SystemExit(main())
