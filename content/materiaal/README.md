# Open lesmateriaal

Elke map hier is één pakket op https://aiontcijferd.be/materiaal. De site bouwt er zelf de pagina's,
de losse downloads en een zip met LEESMIJ van. Je hoeft geen code aan te raken.

## Een pakket toevoegen

```
content/materiaal/<slug>/
  pakket.md            frontmatter + uitleg (verplicht)
  bestanden/           alles wat bezoekers downloaden
    01-draaiboek.docx
    02-presentatie.pptx
    03-werkblad.pdf
```

Submappen in `bestanden/` mogen (zoals bij de AI-proeverij: `01-draaiboek/`, `02-presentatie/`); ze blijven submappen in de zip.
Staat hetzelfde document er in meer formaten (zelfde naam, andere extensie: `.pdf`, `.docx`, `.md`), dan toont de
pagina één regel met een link per formaat. In `bestanden:` in de frontmatter mag je dan de naam zonder extensie
gebruiken (bijvoorbeeld `01-draaiboek/AO-01-draaiboek`).

De `<slug>` wordt het adres: `/materiaal/<slug>`. Kleine letters en koppeltekens, geen spaties.

### pakket.md

```yaml
---
titel: "AI-proeverij"
samenvatting: "Eén of twee zinnen: wat deelnemers na afloop kunnen of weten."
soort: workshop            # cursus | workshop | lezing | gesprek | fiches
status: beschikbaar        # in-voorbereiding | beschikbaar
volgorde: 20               # lager staat hoger in de lijst
voor: ["Bibliotheken", "Onderwijs", "Werk"]   # waar je het kunt geven (labels zoals op /voor)
deelnemers: "Volwassenen zonder voorkennis"
niveau: "Instap"
duur: "2 uur"
versie: "1.0"              # verhogen bij elke wijziging; staat in de naam van de zip
bijgewerkt: 2027-01-15
licentie: "CC BY 4.0"      # of "CC BY-SA 4.0"
maker: "Duncan Panis"      # standaard
bestanden:                 # optioneel: volgorde en uitleg per bestand
  - bestand: 01-draaiboek.docx
    omschrijving: "Wat je doet en zegt, minuut per minuut, met antwoorden op vragen die vaak komen."
  - bestand: 02-presentatie.pptx
    omschrijving: "De dia's, met sprekersnotities."
personaliseren: |          # optioneel: extra regels voor de prompt om het pakket aan te passen
  - Vervang de oefening met de bibliotheekcatalogus door een voorbeeld uit de eigen organisatie.
---

Hier komt de uitleg op de pagina van het pakket, in Markdown: wat erin zit, hoe je de sessie opbouwt,
wat je vooraf regelt (zaal, wifi, accounts), wat kan mislopen.
```

Een pakket verschijnt pas als downloadbaar als `status: beschikbaar` er staat **én** er minstens één bestand
in `bestanden/` zit. Anders staat het onder "In voorbereiding" (alleen titel, soort en samenvatting).

### Wat een pakket bevat

Zodat iemand anders de sessie kan geven zonder ons te bellen:

- een **draaiboek**: wat je doet en zegt, de timing, antwoorden op vragen die vaak komen, en wat je doet als iets misloopt (geen wifi, een tool die niet meer bestaat, een deelnemer zonder account);
- de **presentatie**, met sprekersnotities;
- **werkbladen** of oefeningen voor deelnemers;
- wat je **vooraf regelt** (accounts, toestellen, zaal).

Gebruik bewerkbare formaten (Word, PowerPoint, of OpenDocument), want organisaties moeten het kunnen aanpassen.
Een pdf erbij voor wie meteen wil afdrukken, mag.

### Regels

- **Geen persoonsgegevens** in het materiaal: geen namen van echte deelnemers, geen foto's van herkenbare mensen zonder toestemming.
- **Geen merken en logo's van een organisatie** in de algemene versie. Een versie voor één organisatie wordt hiervan afgeleid en hoort hier niet.
- **Feiten met een datum** (prijzen, regels, namen van knoppen in tools) krijgen een datum in het draaiboek, zodat wie het later gebruikt weet wat na te kijken.
- **Grootte:** houd een bestand onder 25 MB. Video's niet hier, maar op een videoplatform; zet de link in het draaiboek.
- **Versie:** verhoog `versie` en `bijgewerkt` bij elke wijziging. Een fout verbeteren is een kleine stap (1.0 → 1.1), een nieuwe opbouw een grote (1.1 → 2.0).
- **Licentie:** standaard CC BY 4.0, zoals de rest van de site. Kies CC BY-SA 4.0 als aangepaste versies ook open moeten blijven.

## Publiceren

Zoals alles op de site: via een pull request. Samenvoegen in `main` is publiceren. Vercel bouwt opnieuw omdat er iets in `content/` verandert.

Lokaal nakijken: `cd site && npm run build`, daarna `npm run preview` en open `/materiaal`.

## Wat de site zelf maakt

- `/materiaal`: overzicht met filters, beschikbare pakketten en wat in voorbereiding is.
- `/materiaal/<slug>`: pagina met downloads, uitleg, de prompt om het met AI aan te passen en de naamsvermelding.
- `/materiaal/<slug>.zip`: alle bestanden plus een LEESMIJ.txt (licentie, naamsvermelding, prompt).
- `/gegeven/<slug>`: "Gaf je dit pakket?", zes vragen en een kant-en-klare mail naar de redactie. De pakketpagina, de LEESMIJ, de laatste dia (QR-code) en de bijsluiter verwijzen ernaar.
- `/materiaal/<slug>/bestanden/<bestand>`: elk bestand apart.
- `/materiaal/gebruiken`: de algemene handleiding voor organisaties.

De prompt en de LEESMIJ staan in `site/src/lib/materiaal.ts`.
