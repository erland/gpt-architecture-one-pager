# Architecture One Pager GPT

This package contains the material needed to configure a custom GPT named **Architecture One Pager**.

The GPT is designed to create concise, decision-oriented one-pagers for:
- technologies
- frameworks
- platforms
- products
- methods
- architecture practices
- IT trends

## Important v2 behavior

This version supports **generic conversation starters**.

Example:
- User clicks: "Create a one pager for a product"
- GPT asks: "Which product should I create the one pager for?"
- User answers: "GitHub Copilot"
- GPT creates the one pager.

It also enforces **full language matching**:
- If the user asks in Swedish, headings, tables, recommendation labels and template wording should be in Swedish.
- If the user asks in English, the full one-pager should be in English.

## Package contents

```text
architecture-one-pager-gpt/
├── README.md
├── gpt-configuration/
│   ├── gpt-name-and-description.md
│   ├── gpt-instructions.txt
│   ├── conversation-starters.md
│   └── recommended-capabilities.md
├── knowledge/
│   ├── 01-topic-classification-and-focus.md
│   ├── 02-assessment-reference.md
│   ├── 03-public-sector-and-enterprise-context.md
│   ├── 04-source-and-evidence-guidance.md
│   └── 05-output-language-and-export-reference.md
├── examples/
│   ├── golden-example-method-sv.md
│   ├── golden-example-technology-en.md
│   └── golden-example-trend-en.md
└── setup/
    └── how-to-configure-the-gpt.md
```

The five knowledge files are intentionally supporting references. The mandatory workflow, recommendation model and output structure live in the runtime instructions so core behavior does not depend on knowledge retrieval. The three examples are optional golden examples for style and quality only.

## Recommended GPT setup

1. Create a new custom GPT.
2. Name it **Architecture One Pager**.
3. Use `gpt-configuration/gpt-instructions.txt` as the GPT instructions.
4. Upload the five files in the `knowledge/` folder as supporting knowledge.
5. Optionally upload the three `examples/` files as golden style examples; they are not required for core behavior.
6. Enable web browsing if available, because one-pagers often need current maturity, product, market and regulatory information.
7. Use the generic conversation starters from `gpt-configuration/conversation-starters.md`.

## Intended use

Example conversation flow:

```text
User: Skapa en one pager för en produkt.
GPT: Vilken produkt vill du skapa en one pager för?
User: GitHub Copilot.
GPT: [Creates Swedish one pager for GitHub Copilot]
```

```text
User: Create a one pager for a method.
GPT: Which method should I create the one pager for?
User: Event Storming.
GPT: [Creates English one pager for Event Storming]
```

## Portable Chat distribution and releases

The repository can also build a portable ChatGPT package from the same source files used by the Custom GPT.

Build locally:

```bash
python3 scripts/build_distributions.py
python3 scripts/validate_distributions.py
```

This creates:

```text
dist/
├── architecture-one-pager-custom-gpt-vX.Y.Z.zip
└── architecture-one-pager-chat-vX.Y.Z.zip
```

For normal push, pull request and manual workflow runs, the version in `VERSION` is used.

For a published GitHub Release, the release tag is the version source. A release tagged `v1.1.0` therefore creates:

```text
architecture-one-pager-custom-gpt-v1.1.0.zip
architecture-one-pager-chat-v1.1.0.zip
```

The release workflow validates the packages and attaches both ZIP files to the GitHub Release for long-term storage.

To use the portable package in a normal ChatGPT conversation, attach `architecture-one-pager-chat-vX.Y.Z.zip` and ask ChatGPT to read `START-HERE.md` first.

### Runtime-aware build

The two distributions share one canonical runtime source: `gpt-configuration/gpt-instructions.txt`.

- **Custom GPT:** uses the canonical instruction file directly as its runtime entrypoint.
- **Portable chat:** builds `START-HERE.md` by combining `portable/START-HERE-PREAMBLE.md` with the complete canonical runtime instructions. This makes the entrypoint self-contained while preventing a separately maintained copy from drifting out of sync.
- Both packages contain `RUNTIME-PROFILE.json`, which documents their target runtime and states that core behavior must not depend on knowledge retrieval.

`validate_distributions.py` performs both package-integrity checks and semantic runtime checks. It verifies the mandatory eight-step workflow, recommendation rules, language/output markers, small-model profile, compiled chat entrypoint, manifest completeness and the supporting-reference guardrails in knowledge/examples.

### Small-model runtime regression suite

The repository includes a behavioral regression catalog in `tests/runtime-regression-cases.json`. It focuses on failures that are more likely in lightweight models: missing-topic handling, language retention, classification, freshness decisions, exactly one recommendation, neutral organization assumptions, public-sector context, fixed output structure, export timing and portable Chat operation without knowledge retrieval.

Run all local verification with:

```bash
python3 scripts/build_distributions.py
python3 scripts/validate_distributions.py
python3 scripts/validate_runtime_regressions.py
```

The regression validator is deterministic and does not call an external model API. The JSON catalog is also designed to be reused for live Luna/Sol comparison runs. See `tests/README.md`.


## Model compatibility

The Custom GPT and portable Chat distributions use the same canonical runtime contract. Model-specific behavior and known limitations are recorded in `tests/model-compatibility-observations.md`; the runtime is not forked solely to work around a limitation in one lightweight model.
