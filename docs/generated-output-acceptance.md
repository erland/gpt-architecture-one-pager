# Acceptanstest av genererade one-pagers

Det finns nu tre separata kontrollnivåer:

1. **Kanoniskt kontrakt:** \`scripts/validate_runtime_regressions.py\` granskar instruktionernas markörer och byggd Chat-distribution, inte en modellutdata.
2. **Deterministiskt resultatprov:** \`scripts/validate_generated_one_pager.py\` kontrollerar en sparad rapport i Markdown eller ren text. \`tests/test_generated_one_pager.py\` innehåller både positiva och negativa fixture-tester. Dessa körs i CI utan externa modell-API:er.
3. **Funktionellt live-acceptanstest:** Genomför testprompten mot faktiskt installerad \`@architecture-one-pager\`, spara hela svaret och kör resultatprovet. Granska källornas identitet och innehåll separat innan resultatet markeras funktionellt godkänt.

## Köra testet på en faktisk modellutdata

Spara det fullständiga svaret (inklusive källförteckning) som UTF-8 i \`/tmp/one-pager.md\` och kör:

\`\`\`bash
python3 scripts/validate_generated_one_pager.py /tmp/one-pager.md --language sv --max-words 750
\`\`\`

Utfall: \`PASS\` eller \`FAIL\` med konkreta avvikelser. Underkänn bland annat om rubriker saknas eller kommer i fel ordning, rekommendationsavsnittet inte har ett entydigt val, ofullständiga \`+1\`-markörer finns kvar, källförteckningen saknar URL eller texten överstiger ordgränsen.

## Vad testet inte påstår sig göra

- Det utför **inga** live-modellanrop; en CI-PASS garanterar därför inte att installerad Plugin följer instruktionen.
- Det verifierar URL:ers **syntax och förekomst**, inte att länkarna verkligen går att öppna eller att citerad information stödjer ett påstående.
- Det kan inte säkert avgöra om ett källpåstående ligger tillräckligt nära en hänvisning. Kräver manuell granskning eller mer avancerad verifiering.
- Ordräkningen är en mätbar redaktionell gräns, inte en garanti för 1–2 faktiska PDF-sidor.
- Det befintliga testet av en agentrapport i november 2026 kan inte retroaktivt klassas som godkänt utan att köras mot valideraren och källorna granskas.

## Manuell acceptans – förslag på testprompt

\`\`\`text
Använd @architecture-one-pager för att skapa en beslutsorienterad one-pager om AI-agenter i stora myndigheters IT-arkitektur 2027–2030. Använd aktuella verifierbara källor, följ det ordinarie åttastegsflödet och välj exakt en rekommendation.
\`\`\`

Spara testdatum, versionsnummer, fullständig rapport och validerarens resultat. Kontrollera att varje väsentlig aktuell/regulatorisk uppgift har en riktig, relevant och öppningsbar källa, att källor är verkligt kontrollerade och att inga ofullständiga källmarkörer förekommer. Det är först då ett funktionellt acceptansbeslut kan motiveras.

## Release-gate

Fixture-testets PASS är obligatoriskt i GitHub Actions. Live-testet är en separat manuell release-gate som måste dokumenteras innan man påstår fullständigt funktionellt godkännande. Projektets åtta arbetssteg ändras inte av detta testarbete.
