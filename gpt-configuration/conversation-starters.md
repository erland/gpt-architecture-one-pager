# Conversation Starters

Use generic conversation starters. These are intentionally incomplete so the GPT asks the user which concrete topic they want.

## English starters

- Create a one pager for a technology
- Create a one pager for a framework
- Create a one pager for a platform
- Create a one pager for a product
- Create a one pager for a method
- Create a one pager for an IT trend
- Create a one pager for an architecture practice
- Help me assess something for our technology radar

## Swedish starters

- Skapa en one pager för en teknologi
- Skapa en one pager för ett ramverk
- Skapa en one pager för en plattform
- Skapa en one pager för en produkt
- Skapa en one pager för en metod
- Skapa en one pager för en IT-trend
- Skapa en one pager för en arkitekturpraktik
- Hjälp mig bedöma något för vår teknikradar

## Expected behavior

When the user clicks:

```text
Skapa en one pager för en produkt
```

The GPT should ask:

```text
Vilken produkt vill du skapa en one pager för?
```

When the user clicks:

```text
Create a one pager for a method
```

The GPT should ask:

```text
Which method should I create the one pager for?
```

Then, after the user answers with a concrete topic, the GPT should create the one-pager directly.
