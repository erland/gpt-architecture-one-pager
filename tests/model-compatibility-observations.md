# Model compatibility observations

This file records observed runtime behavior. It does not redefine the GPT workflow.

## Principle

Architecture One Pager uses one canonical behavior contract for Custom GPT and portable Chat distributions. Model-specific limitations are documented here rather than encoded as divergent runtime instructions.

## Observations

| Runtime | Model | Status | Observation |
|---|---|---|---|
| Portable Chat ZIP | GPT-5.5 | Partial | The model can read and activate the ZIP instructions, but repeated tests showed that the final export offer may be omitted after a completed one-pager and replaced by a model-generated follow-up suggestion. |
| Portable Chat ZIP | GPT-5.6 Luna | Not yet verified | Run the same regression prompts before assigning a compatibility status. |
| Portable Chat ZIP | GPT-5.6 Sol | Not yet verified in this compatibility pass | Run the same regression prompts before assigning a compatibility status. |
| Custom GPT | GPT-5.5 / 5.6 family | Not verified in this compatibility pass | Custom GPT Instructions should be evaluated separately from ZIP-as-context behavior. |

## Interpretation

A failed model behavior does not automatically justify changing the canonical specification. Runtime changes should be retained only when they improve clarity, maintainability or behavior across model classes.

The regression cases in `tests/runtime-regression-cases.json` describe the intended behavior. This document records where tested models do or do not meet that contract.
