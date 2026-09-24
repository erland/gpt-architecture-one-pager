#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def check(cond,msg):
    if not cond: errors.append(msg)

cfg=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))

check(cfg.get("schema_version")==1,"schema_version must be 1")
check(cfg.get("project",{}).get("id")=="architecture-one-pager","wrong project id")

rob=cfg.get("model_robustness",{})
check(rob.get("level")=="guided","model robustness must be guided")
for key in ["operational_core","explicit_workflow","deterministic_gates","instruction_adherence_evals"]:
    check(rob.get(key) is True,f"guided robustness flag must be true: {key}")

candidates={x.get("runtime_id"):x for x in cfg.get("analysis",{}).get("runtime",{}).get("candidates",[]) if isinstance(x,dict)}
expected={"chatgpt_chat","chatgpt_custom","claude_project","opencode","openai_plugin"}
check(set(candidates)==expected,"all five peer runtimes must be assessed")

check(candidates.get("chatgpt_chat",{}).get("suitability")=="ready","Chat must be ready")
check(candidates.get("chatgpt_custom",{}).get("suitability")=="ready","Custom GPT must be ready")
check(candidates.get("claude_project",{}).get("suitability")=="ready","Claude must be assessed ready")
check(candidates.get("opencode",{}).get("suitability")=="ready","OpenCode must be assessed ready")
check(candidates.get("openai_plugin",{}).get("suitability")=="reduced","Plugin must be assessed reduced")

ws=cfg.get("workspace_state",{})
check(ws.get("state",{}).get("requirement")=="not_required","persistent state must remain not_required")
check(ws.get("state",{}).get("authority")=="conversation","state authority must remain conversation")

instr=cfg.get("instructions",{})
check(instr.get("canonical")=="gpt-configuration/gpt-instructions.txt","canonical instruction path drift")
core=instr.get("core_contract",{})
check(core.get("knowledge_may_not_be_required_for_core_behavior") is True,"core behavior must remain Knowledge-independent")

canonical=(ROOT/"gpt-configuration/gpt-instructions.txt").read_text(encoding="utf-8")
for marker in core.get("required_markers",[]):
    check(marker in canonical,f"canonical instruction missing marker: {marker}")

for rel in [
    "schemas/capability-contract.schema.json",
    "schemas/artifact-contract.schema.json",
    "schemas/workspace-state-contract.schema.json",
    "schemas/tool-contract.schema.json",
    "docs/gpt-builder-1.5-migration-plan.md",
    "PROJECT.md",
    "STATUS.md",
    "project-status.yaml",
]:
    check((ROOT/rel).exists(),f"missing GPT Builder file: {rel}")

if errors:
    print("GPT BUILDER PROJECT LINT: FAIL")
    for e in errors: print("-",e)
    sys.exit(1)

print("GPT BUILDER PROJECT LINT: PASS")
print("robustness=guided runtimes=5 persistent_state=not_required")
