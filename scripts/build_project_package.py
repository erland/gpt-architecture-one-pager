#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, tempfile, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIXED=(2020,1,1,0,0,0)

def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()

def zipdir(src:Path,out:Path):
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists(): out.unlink()
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in src.rglob("*") if x.is_file()):
            info=zipfile.ZipInfo(p.relative_to(src).as_posix(),FIXED)
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--version"); ap.add_argument("--output-dir",default=str(ROOT/"dist"))
    a=ap.parse_args(); version=(a.version or (ROOT/"VERSION").read_text(encoding="utf-8")).strip()
    out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    include_dirs=["gpt-configuration","knowledge","examples","portable","setup","scripts","tests","schemas","runtime-contracts","docs",".github/workflows"]
    include_files=["README.md","VERSION","gpt-project.yaml","PROJECT.md","STATUS.md","project-status.yaml","runtime-parity.yaml",".gitignore"]
    with tempfile.TemporaryDirectory() as td:
        stage=Path(td)/"project"; stage.mkdir()
        for rel in include_dirs:
            src=ROOT/rel
            if src.exists(): shutil.copytree(src,stage/rel,ignore=shutil.ignore_patterns("__pycache__",".pytest_cache","*.pyc"))
        for rel in include_files:
            src=ROOT/rel
            if src.exists():
                dst=stage/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
        (stage/"VERSION").write_text(version+"\n",encoding="utf-8")
        files={}
        for p in sorted(x for x in stage.rglob("*") if x.is_file() and x.name!="MANIFEST.json"):
            files[p.relative_to(stage).as_posix()]={"sha256":sha(p),"bytes":p.stat().st_size}
        (stage/"MANIFEST.json").write_text(json.dumps({"schema_version":1,"runtime_id":"project","version":version,"entrypoint":"gpt-project.yaml","files":files},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        target=out/f"architecture-one-pager-project-v{version}.zip"; zipdir(stage,target); print(target)

if __name__=="__main__": main()
