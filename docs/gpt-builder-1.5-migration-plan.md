# Konverteringsplan – GPT Byggaren 1.5.0

**Projekt:** Architecture One Pager  
**Konverteringstyp:** existing-project-conversion  
**Modellrobusthet:** `guided`

Den befintliga canonical instruktionen, Knowledge-filerna, golden examples, Chat/Custom-distributionerna och regressionkatalogen ska bevaras så länge de uppfyller 1.5-kontrakten.

## Steg 1 – Guided 1.5-projektmodell och plattformsneutrala kontrakt

Inför:

- `gpt-project.yaml`,
- `PROJECT.md`,
- `STATUS.md`,
- `project-status.yaml`,
- capability-, artifact-, workspace/state- och tool-kontrakt,
- explicit bedömning av alla fem runtimes,
- lint som verifierar guided-profilen och canonical åttastegsflödet.

Kärnbeteendet i `gpt-configuration/gpt-instructions.txt` ska inte ändras.

## Steg 2 – GPT Builder-testmodell

Registrera de befintliga 12 runtime-regressionerna och distributionsvalidatorerna i ett 1.5-testmanifest. Komplettera endast där instruktionsefterlevnad inte redan täcks.

## Steg 3 – Peer-distributioner

Bygg Claude Projects och OpenCode från samma canonical instruktion och supporting references. Bekräfta slutlig bedömning av OpenAI Plugin.

## Steg 4 – Runtime parity och modern releaseleverans

Inför runtime contracts, fem-runtime parity, Project ZIP, gemensamma checksummor, delivery manifest och release readiness.

## Steg 5 – Slutregression, hygiene och reproducerbar release

Verifiera full regression, workflow parity, runtime parity, project hygiene och reproducerbar leverans.

## Aktuellt steg

Alla konverteringssteg 1–5 är klara och verifierade. Projektet är i maintenance-läge efter konverteringen till GPT Byggaren 1.5.0.
