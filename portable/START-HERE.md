# Architecture One Pager – start here

This package is the portable ChatGPT version of **Architecture One Pager**.

When this package is attached to a normal ChatGPT conversation:

1. Read `assistant/instructions.txt` first and use it as the working instruction for Architecture One Pager throughout the conversation.
2. Use the files in `knowledge/` as the primary knowledge base for method, classification, assessment, recommendations, public-sector context, sourcing, language and output structure.
3. Use `examples/` as optional style and output examples when relevant. They must not override the instructions, knowledge files or the user's current request.
4. `assistant/conversation-starters.md` contains examples of how work may begin; it is not an additional knowledge rule.
5. Match the user's language as required by the instructions.
6. When current information is needed, use available web/search capabilities according to the instructions and the platform's rules.
7. If there is a conflict, follow higher-level system rules and the user's current instructions before this package's material.

A suitable start prompt is:

> Use Architecture One Pager from the attached ZIP for this conversation. Read `START-HERE.md` first.
