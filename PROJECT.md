# PROJECT – Architecture One Pager

Architecture One Pager skapar korta, beslutsorienterade one-pagers för teknologier, ramverk, plattformar, produkter, metoder, arkitekturpraktiker och IT-trender.

## Canonical källa

- Instruktion: `gpt-configuration/gpt-instructions.txt`
- Knowledge: `knowledge/`
- Golden examples: `examples/`
- Portable Chat preamble: `portable/START-HERE-PREAMBLE.md`

## GPT Byggaren 1.5-konvertering

Projektet konverteras från en äldre, handbyggd GPT-struktur till GPT Byggaren 1.5.0 utan att ändra det etablerade one-pager-beteendet.

Robusthetsnivå: **guided**.

Skäl:
- tydligt åttastegsflöde,
- deterministiska semantiska validatorer,
- regressioner för enklare modeller,
- ingen persistent state machine krävs.

Runtime-mål:
- ChatGPT Chat – ready / active
- Custom GPT – ready / active
- Claude Projects – ready / planned
- OpenCode – ready / planned
- OpenAI Plugin – reduced / inactive

Migreringsplan: `docs/gpt-builder-1.5-migration-plan.md`.
