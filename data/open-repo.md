# De repo openzetten: stand van zaken

Doel: de code even open maken als de inhoud (zie `data/visie.md`). Bijwerken na elke stap.

## Beslist op 13 november 2026

- **Licentie voor de code: MIT** (`LICENSE`). De inhoud blijft CC BY 4.0 (`content/LICENTIE.md`).
- **Deze repo blijft privé; er komt een publieke spiegel.** Een workflow zet na elke wijziging een gefilterde kopie
  in een aparte publieke repo. Dat lost twee dingen tegelijk op, zonder iets aan de werkende keten te veranderen:
  - het persoonlijke e-mailadres in de geschiedenis (16 commits) komt nooit in de publieke repo, want de spiegel
    heeft een eigen, nieuwe geschiedenis met alleen commits van `ai-ontcijferd-bot`;
  - de teksten van anderen in `data/` gaan niet mee (lijst in `spiegel/uitsluiten.txt`).

  Waarom niet de geschiedenis herschrijven: dan veranderen alle commit-id's, moeten Vercel, de workflows en elke
  werkmap opnieuw, en blijven de oude commits bij GitHub bereikbaar via de bestaande pull requests. Het adres zou
  dus niet eens zeker weg zijn.

## Hoe de spiegel werkt

- `spiegel/maak.sh` bouwt de kopie uit de laatste commit: alleen bestanden die in git staan, zonder geschiedenis,
  zonder de paden uit `spiegel/uitsluiten.txt`. De workflows gaan mee als voorbeeld in `.github/workflows-voorbeeld/`,
  een map die GitHub niet uitvoert.
- Het script controleert zelf of er geen persoonlijke e-mailadressen, sleutels of uitgesloten mappen in de kopie
  zitten. Vindt het iets, dan stopt het en wordt er niets gepubliceerd.
- `.github/workflows/spiegel.yml` draait bij elke wijziging op `main`, elke dag om 15.40 u. UTC, en met de hand.
  Zolang de variabele `SPIEGEL_REPO` niet bestaat, doet de workflow niets.
- Getest op 13 november: de kopie bevat geen persoonlijke adressen, en de site bouwt eruit (69 pagina's).
- Werknotities (beslist op 15/11, volgens de visie: open waar het kan). Publiek: `data/open-repo.md`,
  `data/verspreidingsplan.md`, `data/bronnencheck.md` en `content/materiaal/README.md`. Privé: `CLAUDE.md`,
  `data/ideeen.md` en `data/plan-plus.md`, omdat ze elke sessie worden bijgewerkt met de stand van accounts en
  lopend werk, en omdat ze aan Duncans andere werk raken. Wat in een publiek bestand staat, is na de volgende
  spiegel publiek en blijft dat: zet er geen persoonlijke gegevens in.
- Ook publiek: de code, de inhoud, de prompts met het redactiestatuut, `data/visie.md`, en de verantwoording,
  bevindingen, logboeken en kosten per editie.

## Stand op 15 november 2026: de spiegel is live

- Publieke repo: https://github.com/nftaurelius/ai-ontcijferd-open, met beschrijving, homepage aiontcijferd.be en
  onderwerpen (ai, vlaanderen, nederlands, ai-geletterdheid, open-educational-resources, astro).
- In deze repo staan de variabele `SPIEGEL_REPO` en het secret `SPIEGEL_TOKEN` (door Duncan gezet; de sleutel geldt
  alleen voor de publieke repo, *Contents* lezen en schrijven, en **vervalt op 15/11/2027**: tegen dan vernieuwen).
- Eerste spiegel gepubliceerd op 15/11: 208 bestanden, één commit van `ai-ontcijferd-bot`. Nagekeken in een verse
  kopie van de publieke repo: geen uitgesloten paden, geen werknotities, geen persoonlijke e-mailadressen, geen
  sleutels, workflows alleen als voorbeeld in `.github/workflows-voorbeeld/`.
- De workflow draait voortaan vanzelf bij elke wijziging op `main` en elke dag om 15.40 u. UTC. Zonder secret geeft
  hij een waarschuwing en publiceert hij niets.
- Homepage en beschrijving van deze repo bijgewerkt; de samengevoegde tak `claude/visie-eerste-stappen` is weg.
- Wat een agent hier niet mag: sleutels of wachtwoorden in een veld zetten. Al de rest (repo aanmaken, variabelen,
  instellingen) lukt via de browser in Duncans account.

## Afspraken zolang de spiegel bestaat

- Wijzigingen gebeuren hier, in de privé-repo. Een wijziging rechtstreeks in de publieke repo wordt bij de volgende
  spiegel overschreven.
- Meldingen en voorstellen van buiten komen binnen in de publieke repo (issues, pull requests). Een goed voorstel
  nemen we hier over, met vermelding van de indiener.
- Nieuw bestand met tekst van anderen of met toestand van de pijplijn? Zet het pad in `spiegel/uitsluiten.txt`.

## Nagekeken op 13 november 2026

- Sleutels in de geschiedenis: geen gevonden in de 101 commits op `main` (eigen zoekopdracht met patronen, geen
  gespecialiseerd hulpmiddel). Voor de spiegel maakt dit niet meer uit: die bevat geen geschiedenis.
- In `data/items/` staan publieke contactadressen van YouTube-kanalen. Die map gaat niet mee.

## Daarna

- [ ] LEESMIJ aanvullen voor buitenstaanders die de keten zelf willen draaien.
- [ ] `CONTRIBUTING.md` en sjablonen voor meldingen; pagina "Meedoen" op de site.
- [ ] Link "Verbeter deze pagina" onder elke pagina, naar het bronbestand in de publieke repo.
- [x] Beslist welke werknotities publiek zijn (15/11, zie hierboven).
