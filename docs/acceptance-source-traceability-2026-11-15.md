# Acceptanstest: källspårbarhet och rapportlängd

## Bakgrund

Funktionellt test av installerad Architecture One Pager 1.3.0 (15 november 2026) på ämnet AI-agenter i stora myndigheters IT-arkitektur 2027–2030 visade korrekt svenskt åttastegsflöde, rubriker och en rekommendation, men bristfälliga källmarkörer (exempelvis `Consilium +1`) och alltför omfattande text för en one-pager.

## Korrigering

- Kanonisk instruktion kräver klickbara, specifika källor när stöd finns: utgivare, dokumenttitel och tillgängligt datum.
- Källor som verifierats ska skiljas från dokument som enbart identifierats; inga påståenden om utförd kontroll utan faktisk källtillgång.
- Ofullständiga citatmarkörer (t.ex. `+1`) får inte förekomma i färdig rapport.
- Normalt mål för huvudtexten: cirka 500–750 ord, utan att ta bort obligatoriska rubriker, risker eller rekommendationen.
- Testet `scripts/validate_runtime_regressions.py` har utökats med deterministiska kontrollmarkörer för källspårbarhet och kompakthet.

## Oförändrade kontrakt

Åtta sekventiella steg, två språks rubriker, exakt en rekommendation, organisationsanpassning, exportformat och fem aktiva distributioner.

## Verifiering och begränsning

GitHub Actions verifierar instruktionskontrakt, regressioner och distributionsbygge. Det är **inte** ett funktionellt språkmodellstest. Efter release ska en ny separat chatt med installerad Plugin genomföra motsvarande AI-agent-test och visa verkliga klickbara källor och ett kortare resultat. PDF-export behöver testas separat för faktisk sidlängd.

## Acceptanskriterier för manuell kontroll

1. Rätt språk, alla 14 rubriker i ordning och exakt en rekommendation.
2. Faktiska klickbara hänvisningar nära viktiga uppdateringskänsliga påståenden samt källförteckning med titel och utgivare.
3. Inga ospecificerade `+1`-markörer eller ogrundade påståenden om källverifiering.
4. Kort huvudtext i normalfallet; tydlig motivering om längre text krävs.
5. Export erbjuds först efter avslutad one-pager.
