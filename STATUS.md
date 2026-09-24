# Status – Architecture One Pager

**Produktversion:** 1.0.0  
**Migration:** GPT Byggaren 1.5.0  
**Tillstånd:** Konvertering pågår

## Migrationssteg

- [ ] Steg 1 – Guided 1.5-projektmodell och plattformsneutrala kontrakt
- [ ] Steg 2 – Registrera befintliga regressioner i GPT Builder-testmodellen
- [ ] Steg 3 – Claude/OpenCode peer-distributioner och runtime-bedömning
- [ ] Steg 4 – Runtime parity och modern releaseleverans
- [ ] Steg 5 – Slutregression, hygiene och reproducerbar release

## Runtime-bedömning

- ChatGPT Chat: ready / active
- Custom GPT: ready / active
- Claude Projects: ready / planned
- OpenCode: ready / planned
- OpenAI Plugin: reduced / inactive

## Robusthetsprofil

Projektet är `guided`, inte `stateful`.

- det obligatoriska åttastegsflödet ska följas i ordning,
- core behavior får inte bero på Knowledge retrieval,
- exakt en rekommendation ska väljas,
- persistent state är inte nödvändigt,
- current-information-check styr när webb/färska källor behövs.

## Aktuellt steg

**Steg 1 – Guided 1.5-projektmodell och plattformsneutrala kontrakt.**

Steget markeras klart först när ny projektlint och hela befintliga build/validation/regression-kedjan passerar.
