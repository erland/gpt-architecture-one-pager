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

runtime=cfg.get("runtime",{})
claude=runtime.get("claude",{})
opencode=runtime.get("opencode",{})
check(claude.get("enabled") is True,"Claude peer runtime must be enabled")
check(claude.get("mode")=="claude_project","Claude runtime mode must be claude_project")
check(claude.get("project",{}).get("instructions")=="project/instructions.md","Claude instructions path drift")
check(opencode.get("enabled") is True,"OpenCode peer runtime must be enabled")
check(opencode.get("mode")=="opencode_workspace","OpenCode runtime mode must be opencode_workspace")
check(opencode.get("runtime_root")==".opencode/architecture-one-pager","OpenCode runtime root drift")
check(runtime.get("openai_plugin",{}).get("enabled") is False,"OpenAI Plugin must remain inactive")
check(runtime.get("openai_plugin",{}).get("role")=="assessed_reduced","OpenAI Plugin assessment must remain reduced")

parity=cfg.get("runtime_parity",{})
check(parity.get("model")=="runtime-parity.yaml","runtime parity model not registered")
check(set(parity.get("registered_runtimes",[]))==expected,"runtime parity must register all five runtimes")
check(set(parity.get("compared_categories",[]))=={"behavior","capability","artifact","workspace_state","tool"},"runtime parity categories differ")

testing=cfg.get("testing",{})
check(testing.get("manifest")=="tests/test-manifest.yaml","GPT Builder test manifest not registered")
check(testing.get("manifest_schema")=="schemas/test-manifest.schema.json","test manifest schema not registered")
check(testing.get("runtime_cases")=="tests/runtime-regression-cases.json","runtime regression catalog not registered")
check(testing.get("contract_validator")=="scripts/validate_gpt_builder_tests.py","test contract validator not registered")
check(testing.get("deterministic_contracts_block_release") is True,"deterministic test contracts must block")
check(testing.get("live_model_runtime_evals_are_separate") is True,"live model runtime evals must be separate")

for rel in [
    "schemas/test-manifest.schema.json",
    "tests/test-manifest.yaml",
    "scripts/validate_gpt_builder_tests.py",
    "scripts/build_peer_distributions.py",
    "scripts/validate_peer_distributions.py",
    "runtime-parity.yaml",
    "runtime-contracts/chatgpt-chat.json",
    "runtime-contracts/chatgpt-custom.json",
    "runtime-contracts/claude-project.json",
    "runtime-contracts/opencode.json",
    "scripts/build_project_package.py",
    "scripts/build_delivery_metadata.py",
    "scripts/validate_runtime_parity.py",
    "scripts/validate_release_readiness.py",
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
