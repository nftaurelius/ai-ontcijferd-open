---
titel: "Een AI-nieuwsbericht nuchter lezen"
soort: skill
samenvatting: "Een skill voor Claude die een artikel, persbericht of post over AI leest zoals wij dat doen: wat gebeurde er, wie zegt het, wat ontbreekt er, en hoeveel aandacht verdient het, met een hype-meter."
voor: ["Burgers", "Onderwijs", "Werk", "Bibliotheken", "Lokale overheden", "Zelfstandigen"]
niveau: "Instap"
versie: "1.0"
bijgewerkt: 2026-11-23
getest: "Nog niet getest. Probeer je het? Laat weten wat het gaf."
licentie: "CC BY 4.0"
status: beschikbaar
---

## Wat is een skill?

Een skill is een map met instructies die een AI-assistent laadt wanneer een taak erom vraagt. Je zet hem één keer klaar; daarna gebruikt de assistent hem vanzelf als je een nieuwsbericht over AI deelt. Deze skill is gemaakt voor Claude (Anthropic). De instructies in `SKILL.md` kun je ook als gewone prompt gebruiken in een andere assistent.

## Wat hij doet

Je deelt een bericht over AI en vraagt "wat betekent dit?". De skill geeft:

1. Wat er gebeurde, in twee zinnen.
2. Wie het zegt: de maker zelf, een onafhankelijke bron, of één bron.
3. De vakwoorden, uitgelegd.
4. Wat het bericht niet zegt: de vragen die je moet stellen.
5. Een hype-meter in vijf standen, met één zin uitleg.
6. Wat het betekent voor jou, als je zegt wie je bent (leraar, ondernemer, gemeente).

Hij verzint geen bronnen en zegt het als hij iets niet weet. Dit is dezelfde werkwijze als in onze [weekeditie](/edities), in het klein.

## Installeren

1. Download de zip bovenaan deze pagina. Pak hem niet uit.
2. In Claude: kijk bij *Settings* > *Capabilities* of *Code execution and file creation* aanstaat.
3. Ga naar *Customize* > *Skills*, klik op "+", kies *Create skill* en dan *Upload a skill*, en kies de zip ([uitleg van Anthropic](https://support.claude.com/en/articles/12512180-use-skills-in-claude), nagekeken op 23 november 2026; namen van menu's kunnen veranderen).
4. Deel een AI-nieuwsbericht en vraag: "Lees dit nuchter."

## Wat je nakijkt

- Lees de oorspronkelijke bron zelf als je het bericht wilt doorgeven.
- De hype-meter is een inschatting, geen feit. Vind je hem te streng of te mild, zeg het en vraag waarom.
