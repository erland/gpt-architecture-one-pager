# Modulär källmigration och källspårbarhet

## Beslut
Behåll **en sammanhållen Skill** `architecture-one-pager` eftersom åttastegsflödet inte har fristående delprocesser, men använd GPT Byggaren 1.6.33:s `instructions.mode: modular_skills` för en gemensam kärna och separat Skill-beteende.

## Kanoniska källor
- `canonical/core.md`: identitet, syfte och runtimeövergripande obligatoriska regler.
- `canonical/skills/architecture-one-pager/behavior.md`: åttastegsmetodik, informationsaktualitet, bedömning, en rekommendation, rubriker, export och slutkontroll.
- `gpt-configuration/gpt-instructions.txt`: ursprunglig baslinje för migreringsspårbarhet; **inte** längre auktoritativ runtimekälla.
- `gpt-project.yaml`: aktiverar `modular_skills` och resursisolering `explicit` med tomma listor för resurser som inte används.

## Beteendekorrigering
Det funktionella testet av version 1.3.1 gav ofullständiga källmarkörer, exempelvis `OWASP ... +1`. Den nya Skill-instruktionen kräver slutkontroll av det **renderade användarsvaret**, inte bara källverktygets interna referenser. Om presentationskomponenter inte bevarar länkar vid kopiering eller export ska vanliga Markdown-länkar med faktiska käll-URL:er användas. Det är inte tillåtet att uppfinna URL:er, påstå obefintlig verifiering eller lämna platshållare. Texten ska vara kortfattad utan att någon av de 14 rubrikerna stryks.

## Verifiering
- Kör projektlint, bygg och runtime-/leveransvalidering med oförändrad kanonisk GPT Byggaren-motor.
- Kontrollera att kompilerad Chat-instruktion innehåller hela `core.md` och Skill-beteendet.
- Verifiera att tidigare 12 regressionsfall fortfarande omfattas.
- Kör ett nytt live-test i installerad Plugin efter release. Den deterministiska byggkedjan kan inte garantera faktiskt modellbeteende.

## Spårbarhet
Den tidigare monolitiska texten är bevarad. Behåll samtliga befintliga 14 rubriker, sex beslutsområden och åttastegsordningen. Det enda avsedda beteendetillägget är tydligare källrendering och kortare text.
