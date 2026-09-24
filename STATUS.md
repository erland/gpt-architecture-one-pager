# Status – Architecture One Pager

**Produktversion:** 1.0.0  
**Migration:** GPT Byggaren 1.5.0  
**Tillstånd:** Konvertering pågår

## Migrationssteg

- [x] Steg 1 – Guided 1.5-projektmodell och plattformsneutrala kontrakt
- [x] Steg 2 – Registrera befintliga regressioner i GPT Builder-testmodellen
- [x] Steg 3 – Claude/OpenCode peer-distributioner och runtime-bedömning
- [ ] Steg 4 – Runtime parity och modern releaseleverans
- [ ] Steg 5 – Slutregression, hygiene och reproducerbar release

## Runtime-bedömning

- ChatGPT Chat: ready / active
- Custom GPT: ready / active
- Claude Projects: ready / active
- OpenCode: ready / active
- OpenAI Plugin: reduced / inactive

## Robusthetsprofil

Projektet är `guided`, inte `stateful`.

- det obligatoriska åttastegsflödet ska följas i ordning,
- core behavior får inte bero på Knowledge retrieval,
- exakt en rekommendation ska väljas,
- persistent state är inte nödvändigt,
- current-information-check styr när webb/färska källor behövs.

## Verifiering av steg 1

CI passerade den nya GPT Builder 1.5-linten tillsammans med befintliga reproducerbara Chat/Custom-byggen, semantisk distributionsvalidering, small-model runtime-regressioner och artifact upload. Canonical åttastegsflöde och befintligt one-pager-beteende är oförändrade.

## Verifiering av steg 2

CI passerade GPT Builder-testmanifestet och kontraktsvalidatorn tillsammans med den befintliga distributionsvalidatorn och alla 12 small-model runtime-regressioner. De deterministiska kontraktssviterna är blockerande. Live Luna/Sol eller andra runtime-körningar hålls separat som manuella runtime-evals och blandas inte ihop med statisk kontraktsvalidering.

## Verifiering av steg 3

CI passerade Claude Projects- och OpenCode-distributionerna tillsammans med befintliga Chat/Custom-paket, GPT Builder-testkontraktet och alla 12 runtime-regressioner. Båda peer-runtimes använder samma canonical åttastegsinstruktion. Knowledge och examples är supporting references och persistent state krävs inte. OpenAI Plugin är slutligt bedömd som reduced/inactive eftersom den inte tillför en meningsfull peer-runtime för den här huvudsakligen instruktionsdrivna produkten.

## Aktuellt steg

**Steg 4 – Runtime parity och modern releaseleverans.**
