# How to Configure the GPT

## 1. Create the GPT

In ChatGPT:
1. Go to Explore GPTs / Create.
2. Create a new GPT.
3. Name it: **Architecture One Pager**.
4. Use the description from `gpt-configuration/gpt-name-and-description.md`.

## 2. Add instructions

Copy the full contents of:

```text
gpt-configuration/gpt-instructions.txt
```

into the GPT instruction field.

This v2 instruction file includes:
- generic conversation-starter behavior
- one follow-up question when the concrete topic is missing
- full language matching for headings and templates
- Swedish recommendation labels: Inför / Testa / Utvärdera / Avvakta

## 3. Add knowledge files

Upload all files from:

```text
knowledge/
```

Recommended knowledge files:
- architecture-one-pager-method.md
- classification-guide.md
- one-pager-template.md
- one-pager-template-sv.md
- assessment-criteria.md
- radar-recommendation-model.md
- public-sector-context.md
- source-guidance.md
- export-format-guide.md
- language-and-style-guide.md

Optional:
Upload the files in `examples/` if you want the GPT to have examples of the intended output style.

## 4. Enable capabilities

Recommended:
- Web browsing: enabled
- File uploads: enabled

Optional:
- Code interpreter / Advanced Data Analysis: enabled if you want batch generation or downloadable output

## 5. Add conversation starters

Use the generic starters from:

```text
gpt-configuration/conversation-starters.md
```

Recommended Swedish starters:
- Skapa en one pager för en teknologi
- Skapa en one pager för ett ramverk
- Skapa en one pager för en plattform
- Skapa en one pager för en produkt
- Skapa en one pager för en metod
- Skapa en one pager för en IT-trend
- Hjälp mig bedöma något för vår teknikradar

Recommended English starters:
- Create a one pager for a technology
- Create a one pager for a framework
- Create a one pager for a platform
- Create a one pager for a product
- Create a one pager for a method
- Create a one pager for an IT trend
- Help me assess something for our technology radar

## 6. Test the generic starter flow

Test:

```text
Skapa en one pager för en produkt
```

Expected response:

```text
Vilken produkt vill du skapa en one pager för?
```

Then answer:

```text
GitHub Copilot
```

Expected:
- The GPT creates a Swedish one-pager.
- Headings are Swedish.
- Recommendation labels are Swedish.

Test:

```text
Create a one pager for a method
```

Expected response:

```text
Which method should I create the one pager for?
```

Then answer:

```text
Event Storming
```

Expected:
- The GPT creates an English one-pager.
- Headings are English.

## 7. Optional adaptation

You can adapt the GPT for a specific organization by adding a knowledge file with:
- architecture principles
- technology radar categories
- security requirements
- preferred platforms
- procurement constraints
- current strategic initiatives

Do not hard-code confidential data unless the GPT is configured for the intended audience and information classification.
