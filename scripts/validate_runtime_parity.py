#!/usr/bin/env python3
from pathlib import Path
import json, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
errors=[]
cfg=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
parity=yaml.safe_load((ROOT/"runtime-parity.yaml").read_text(encoding="utf-8"))
expected={"chatgpt_chat","chatgpt_custom","claude_project","opencode","openai_plugin"}
if set(parity.get("registered_runtimes",[]))!=expected: errors.append("all five runtimes must be registered")
if set(parity.get("compared_categories",[]))!={"behavior","capability","artifact","workspace_state","tool"}: errors.append("parity categories differ")
candidates={x["runtime_id"]:x for x in cfg["analysis"]["runtime"]["candidates"]}
for rid in {"chatgpt_chat","chatgpt_custom","claude_project","opencode"}:
    if candidates[rid].get("suitability")!="ready" or candidates[rid].get("activate_by_default") is not True: errors.append(rid+" not ready/active")
for rid in {"openai_plugin"}:
    if candidates[rid].get("suitability")!="reduced" or candidates[rid].get("activate_by_default") is not False: errors.append(rid+" not reduced/inactive")
contracts={"chatgpt_chat":"runtime-contracts/chatgpt-chat.json","chatgpt_custom":"runtime-contracts/chatgpt-custom.json","claude_project":"runtime-contracts/claude-project.json","opencode":"runtime-contracts/opencode.json"}
for rid,path in contracts.items():
    d=json.loads((ROOT/path).read_text(encoding="utf-8"))
    if d.get("runtime_id")!=rid: errors.append(rid+" runtime_id mismatch")
    if d.get("behavior",{}).get("canonical")!="gpt-configuration/gpt-instructions.txt": errors.append(rid+" canonical drift")
    if d.get("behavior",{}).get("persistent_state_required") is not False: errors.append(rid+" state drift")
if errors:
    print("RUNTIME PARITY: FAIL"); [print("-",e) for e in errors]; sys.exit(1)
print("RUNTIME PARITY: PASS")
