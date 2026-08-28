# Architecture One Pager – portable chat runtime

This ZIP is the portable ChatGPT distribution of **Architecture One Pager**.

Treat this file as the active entry point for the conversation. The mandatory runtime contract is embedded below during the build, so the assistant can execute the complete core workflow without opening any other file first.

## Portable package rules

- Follow platform/system instructions and the user's current request first.
- Then follow the embedded canonical runtime instructions in this file.
- `assistant/instructions.txt` is an identical copy of the canonical runtime instructions for inspection and compatibility; it does not add a second rule set.
- `knowledge/` contains optional supporting depth. Core behavior must never depend on retrieving a particular knowledge file.
- `examples/` contains optional golden examples for style and quality only. Never use them as factual sources for another topic.
- `assistant/conversation-starters.md` contains starter examples, not additional rules.

A suitable initial prompt when attaching the ZIP is:

> Use Architecture One Pager from the attached ZIP for this conversation. Read `START-HERE.md` first and follow its embedded runtime instructions.

---

## Embedded canonical runtime instructions
