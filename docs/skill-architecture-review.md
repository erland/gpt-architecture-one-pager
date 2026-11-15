# Skill-arkitekturgranskning – Architecture One Pager

Datum: 2026-11-15  
Underlag: `gpt-configuration/gpt-instructions.txt`, `gpt-project.yaml`, GPT Byggaren 1.6.33:s kriterier för Skill-uppdelning.

## Beslut

**Behåll en enda Skill, `architecture-one-pager`, och aktivera inte `instructions.mode: modular_skills` i detta steg.**

Projektet har en sammanhållen uppgift: framställa en kort, beslutsorienterad one-pager med exakt en rekommendation. De åtta numrerade stegen är en sekvens, inte självständigt aktiverbara förmågor. Separata Skills per steg skulle skapa ökad koppling, flera aktiveringsvillkor och en risk för att det obligatoriska flödet bryts utan att ge självständiga användningsfall.

## Analyserade ansvarsområden

| Område | Aktiveringsvillkor | Rekommenderad hemvist | Skäl |
| --- | --- | --- | --- |
| Språk och ämneskontroll | Varje one-pager-begäran | Gemensamt kontrakt | Måste gälla före övriga steg |
| Klassificering | Ett konkret ämne är känt | One-pager-Skill | Styr analysens betoning |
| Aktualitetskontroll | Ämnet kräver aktuella uppgifter | One-pager-Skill | Del av bedömningens evidens, inte separat leverans |
| Bedömning | Ämne och evidens är kända | One-pager-Skill | Samtliga obligatoriska bedömningsperspektiv hör ihop |
| En rekommendation | Efter bedömning | One-pager-Skill | Huvudsakligt beslutsresultat |
| Fast utdataformat | Efter rekommendation | One-pager-Skill | Måste bevara 14 rubriker på respektive språk |
| Export (MD, Confluence, PDF, DOCX) | Användaren väljer format efter färdig rapport | One-pager-Skill tills vidare | Framtida utbrytning om egen funktionalitet, formatlogik eller verktyg tillkommer |

## Resurser och beroenden

- En Skill: `architecture-one-pager`.
- Gemensamt beteende kommer från `gpt-configuration/gpt-instructions.txt` och får inte förloras.
- `knowledge/` och `examples/` är valfria stödresurser; de får inte ersätta instruktionens kärnregler.
- Ingen obligatorisk extern runtime-exekvering, persistent state eller MCP-server.
- Alla fem aktiva distributioner ska även fortsättningsvis byggas ur samma kanoniska beteendekälla.

## Prövade alternativ

1. **Åtta Skills, en per steg – avvisat.** Stegen saknar självständiga användningsfall och är tätt sekventiellt beroende.
2. **Tre Skills (research, one-pager, export) – avvisat tills vidare.** Research är integrerad evidensgranskning; export är endast ett efterföljande alternativ. Flera källor skulle skapa överlapp och extra aktiveringsgränser.
3. **En Skill – valt.** Sammanhållen ansvarsyta och enklast att säkerställa full beteendeparitet.

## Modulärt källformat

GPT Byggaren 1.6.33 stödjer `instructions.mode: modular_skills` med `canonical/core.md` och `canonical/skills/<id>/behavior.md`, även med en Skill. En sådan omstrukturering är tekniskt möjlig men har i nuläget inget påvisat behov av flera självständiga Skills. Nuvarande `skills.mode: inferred` och monolitiska kanoniska instruktion behålls för att undvika en beteenderisk utan tydlig nytta.

**Ny prövning:** om export blir ett separat återkommande arbetsflöde, om one-pagern får andra självständiga analys-/leveranstyper eller om separata resurser/verktyg får egna utlösande användningsfall.

## Granskningskriterier inför framtida uppdelning

- Tydligt separat aktiveringsvillkor och resultat för varje Skill.
- Ingen dubblerad kanonisk regeltext.
- Spårbarhet från varje ursprungligt instruktionsavsnitt till kärna/Skill.
- Explicit deklarerade, befintliga referenser, assets och scripts per Skill.
- Samma obligatoriska åttastegsflöde, språk, rubrikordning och exakt en rekommendation i alla fem distributioner.
- Godkända deterministiska validatorer och runtime-regressioner före merge.

## Status

Arkitekturbedömning dokumenterad. **Ingen aktivering av modulärt läge genomförd och ingen ändring av originalbeteendet.** Befintlig CI-verifiering av PR #5 kvarstår som separat kontroll.
