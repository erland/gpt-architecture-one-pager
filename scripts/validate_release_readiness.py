#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, subprocess, sys, zipfile
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--version"); ap.add_argument("--dist",default=str(ROOT/"dist"))
    a=ap.parse_args(); version=(a.version or (ROOT/"VERSION").read_text()).strip(); dist=Path(a.dist); errors=[]
    if subprocess.run([sys.executable,str(ROOT/"scripts/validate_runtime_parity.py")],cwd=ROOT).returncode: errors.append("runtime parity failed")
    arts=[
      dist/f"architecture-one-pager-project-v{version}.zip",
      dist/f"architecture-one-pager-custom-gpt-v{version}.zip",
      dist/f"architecture-one-pager-chat-v{version}.zip",
      dist/f"architecture-one-pager-claude-v{version}.zip",
      dist/f"architecture-one-pager-opencode-v{version}.zip",
    ]
    for p in arts:
        if not p.exists(): errors.append("missing "+p.name); continue
        try:
            with zipfile.ZipFile(p) as z:
                bad=z.testzip()
                if bad: errors.append(f"{p.name} CRC: {bad}")
        except zipfile.BadZipFile: errors.append("invalid zip "+p.name)
    dm=dist/"DELIVERY-MANIFEST.json"; sums=dist/"SHA256SUMS.txt"
    if not dm.exists(): errors.append("delivery manifest missing")
    else:
        types={x.get("type") for x in json.loads(dm.read_text(encoding="utf-8")).get("artifacts",[])}
        if types!={"project_zip","custom_gpt_zip","chat_zip","claude_zip","opencode_zip"}: errors.append("delivery types differ")
    if not sums.exists(): errors.append("checksums missing")
    else:
        got={}
        for line in sums.read_text(encoding="utf-8").splitlines():
            if line.strip():
                h,n=line.split(None,1); got[n.strip()]=h
        for p in arts:
            if p.exists() and got.get(p.name)!=hashlib.sha256(p.read_bytes()).hexdigest(): errors.append("checksum mismatch "+p.name)
    if errors:
        print("RELEASE READINESS: FAIL"); [print("-",e) for e in errors]; return 1
    print("RELEASE READINESS: PASS"); return 0
if __name__=="__main__": raise SystemExit(main())
