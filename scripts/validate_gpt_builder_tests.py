#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def check(cond,msg):
    if not cond: errors.append(msg)

manifest_path=ROOT/"tests/test-manifest.yaml"
schema_path=ROOT/"schemas/test-manifest.schema.json"
cases_path=ROOT/"tests/runtime-regression-cases.json"

check(manifest_path.is_file(),"tests/test-manifest.yaml missing")
check(schema_path.is_file(),"schemas/test-manifest.schema.json missing")
check(cases_path.is_file(),"runtime regression catalog missing")

if not errors:
    m=yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    check(m.get("schema_version")==1,"test manifest schema_version must be 1")
    suites=m.get("suites",{})
    for sid in ["distribution_contract","runtime_behavior_contract","live_model_runtime"]:
        check(sid in suites,f"missing test suite: {sid}")
    check(suites.get("distribution_contract",{}).get("blocking") is True,"distribution contract must block")
    check(suites.get("runtime_behavior_contract",{}).get("blocking") is True,"behavior contract must block")
    check(suites.get("live_model_runtime",{}).get("blocking") is False,"live model runtime suite must be non-blocking in deterministic CI")

    data=json.loads(cases_path.read_text(encoding="utf-8"))
    cases=data.get("cases",[])
    check(len(cases)==12,f"expected 12 runtime regression cases, found {len(cases)}")
    ids=[c.get("id") for c in cases]
    check(len(ids)==len(set(ids)),"runtime regression ids must be unique")
    for c in cases:
        check(isinstance(c.get("prompt"),str) and c["prompt"].strip(),f"{c.get('id')}: prompt missing")
        expected=c.get("expected")
        check(isinstance(expected,dict) and expected,f"{c.get('id')}: expected contract missing")
        if isinstance(expected,dict) and expected.get("action")=="produce_one_pager":
            check(expected.get("recommendation_count")==1,f"{c.get('id')}: one-pager cases must require exactly one recommendation")

    workflow=(ROOT/".github/workflows/build-distributions.yml").read_text(encoding="utf-8")
    check("scripts/validate_gpt_builder_tests.py" in workflow,"CI must validate GPT Builder test contract")
    check("scripts/validate_distributions.py" in workflow,"CI must run distribution contract")
    check("scripts/validate_runtime_regressions.py" in workflow,"CI must run runtime behavior contract")

if errors:
    print("GPT BUILDER TEST CONTRACT: FAIL")
    for e in errors: print("-",e)
    sys.exit(1)

print("GPT BUILDER TEST CONTRACT: PASS")
print("suites=3 runtime_cases=12 deterministic_blocking=2 live_runtime_manual=1")
