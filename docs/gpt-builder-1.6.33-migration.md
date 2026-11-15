# Migration till GPT Byggaren 1.6.33

Migrationen utgår från oförändrad original-ZIP och den bifogade kanoniska engine 1.6.33.
Produktversionen är fortsatt 1.0.0. Historik från migreringen till 1.5 finns kvar i `docs/gpt-builder-1.5-migration-plan.md`.

## Sex migrationssteg

1. **Inventering – klar:** canonical instruktion i `gpt-configuration/gpt-instructions.txt`; fem Knowledge-filer; tre exempel; 12 statiska regressionsfall.
2. **Projektmodell – klar:** äldre `openai_plugin` mappad till modern `plugin`; historisk Custom GPT deaktiverad men dess konfiguration behållen; fem moderna peer-mål.
3. **Motor – klar:** oförändrad engine 1.6.33 genomförde originalets självtest, integritetskontroll och installation.
4. **Distributioner – klar:** Chat, Plugin, Claude Projects, Claude Skills, OpenCode samt projekt-ZIP byggda med originalbyggaren.
5. **Dokumentation/filhygien – klar för lokal leverans:** status och CI uppdaterade; äldre överlappande byggfiler finns arkiverade under `legacy-build-scripts/`, inte raderade.
6. **Slutverifiering – delvis klar:** lokal distributionsvalidering passerar. GitHub Actions, faktisk Plugin-import och funktionella regressioner hos värdarna återstår.

## Beteende och begränsningar

Den kanoniska instruktionen ändras inte. Guidat åttastegsflöde, språkmatchning, informationsaktualitet, ett enda rekommendationsval samt exportstöd består. Motorn verifierar distributionsstruktur men kan inte garantera webbsökning, dokumentexport eller funktionell runtimeparitet hos alla värdar.

## CI och migreringshygien

GitHub Actions hämtar den versionslåsta engine-filen för v1.6.33 och kontrollerar SHA-256 innan kanonisk installation och bygge. De äldre projektspecifika validatorerna bevaras för jämförelse och ska inte likställas med värdverifiering.
