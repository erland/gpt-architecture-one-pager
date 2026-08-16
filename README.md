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
architecture-one-pager-gpt-production-v2/
├── README.md
├── gpt-configuration/
│   ├── gpt-name-and-description.md
│   ├── gpt-instructions.txt
│   ├── conversation-starters.md
│   └── recommended-capabilities.md
├── knowledge/
│   ├── architecture-one-pager-method.md
│   ├── classification-guide.md
│   ├── one-pager-template.md
│   ├── one-pager-template-sv.md
│   ├── assessment-criteria.md
│   ├── radar-recommendation-model.md
│   ├── public-sector-context.md
│   ├── source-guidance.md
│   ├── export-format-guide.md
│   └── language-and-style-guide.md
├── examples/
│   ├── example-prompts.md
│   ├── example-technology-one-pager.md
│   ├── example-method-one-pager.md
│   ├── example-trend-one-pager.md
│   └── example-swedish-one-pager.md
└── setup/
    └── how-to-configure-the-gpt.md
```

## Recommended GPT setup

1. Create a new custom GPT.
2. Name it **Architecture One Pager**.
3. Use `gpt-configuration/gpt-instructions.txt` as the GPT instructions.
4. Upload all files in the `knowledge/` folder as knowledge files.
5. Optionally upload the `examples/` files as additional knowledge.
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
