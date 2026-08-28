# Runtime regression tests

This directory defines the behavioral contract that both the portable Chat distribution and the Custom GPT distribution should satisfy, including on lightweight models such as Luna.

## What CI verifies automatically

Run:

```bash
python3 scripts/validate_runtime_regressions.py
```

The validator checks that:

- the regression suite covers the required small-model-sensitive behaviors;
- every case has a stable machine-readable expected outcome;
- the canonical runtime instructions contain the rules needed to satisfy those cases;
- the portable Chat entrypoint can be reconstructed from the same canonical runtime;
- both runtime profiles declare that core behavior does not require knowledge retrieval;
- the fixed Swedish and English one-pager structures remain intact;
- recommendation labels remain mutually exclusive;
- public-sector, freshness, language, missing-topic and export behavior remain represented.

These are contract tests, not claims that a particular hosted model produced a correct answer. CI does not call an external model API.

## Live Luna/Sol evaluation

`runtime-regression-cases.json` is also the canonical model-eval catalog. To compare models, run each `prompt` in a fresh conversation/runtime and evaluate the response against its `expected` object.

A live evaluator should record at least:

- model/runtime;
- test case id;
- pass/fail per expected field;
- overall pass/fail;
- short failure note;
- captured model response or a reference to it.

The most important small-model gates are:

1. missing topic → exactly one question and stop;
2. user language is retained consistently;
3. one primary classification is selected;
4. freshness is considered for products/platforms/trends;
5. exactly one recommendation is returned;
6. fixed section structure is retained;
7. export is offered only after the completed one-pager;
8. portable Chat core behavior works from `START-HERE.md` alone.
