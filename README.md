# AI Ontcijferd — pijplijn

AI zonder hype. Door Duncan Panis.

Deze repo draait de agentketen achter [aiontcijferd.be](https://aiontcijferd.be). Het redactiestatuut staat in `prompts/statuut.md` en geldt voor elke agent.

## Hoe het werkt

| Wanneer | Workflow | Wat gebeurt er |
| --- | --- | --- |
| Elke ochtend | Dagelijks | **Verkenner** haalt nieuwe items op uit `sources.yaml`. **Triage** (goedkoop model) scoort ze op relevantie voor Vlaanderen en hype. Alles wordt bewaard in `data/`. |
| Vrijdagochtend | Wekelijks | **Analist** schrijft het concept, **vertaler** maakt het leesbaar, **tegenspreker** (andere leverancier) controleert, **analist** verwerkt de bevindingen. Er komt een pull request met het concept. |
| Elke ochtend, na Dagelijks | Plus — dagbrief | **Dagbrief** (Sonnet) schrijft het nieuws van het etmaal, **dagcontrole** (andere leverancier) toetst het aan de bronnen. Pull request: samenvoegen = publiceren op `/plus`. |
| Met de hand | Plus — dossier | Uitgebreid stuk over één onderwerp: zelfde keten als de weekeditie, met Mijn inschatting. |
| Maandagochtend | Bronnencheck | Test elke bron en meldt in `data/bronnencheck.md` welke niets opleveren. |

**Jouw rol als eindredacteur:** open de pull request, lees het concept na, schrijf **Mijn inschatting**, zet `status: klaar` en voeg de pull request samen. Reken op één à twee uur per week.

## Eenmalige installatie

1. **API-sleutels.** Maak bij Anthropic en bij OpenAI een aparte sleutel voor dit project, en stel in beide consoles een maandelijkse uitgavenlimiet in.
2. **Secrets in GitHub.** Repo → *Settings* → *Secrets and variables* → *Actions* → voeg toe: `ANTHROPIC_API_KEY` en `OPENAI_API_KEY`. Voor de X-radar van Plus ook `XAI_API_KEY` (xAI-console, met uitgavenlimiet); zonder die sleutel slaat de pijplijn X gewoon over.
3. **Rechten voor de workflows.** Repo → *Settings* → *Actions* → *General* → *Workflow permissions*: kies *Read and write permissions* en vink *Allow GitHub Actions to create and approve pull requests* aan.
4. **Model van de tegenspreker.** Staat in `config.yaml` (nu `gpt-6-astra`). Wijzig het daar als je een ander model wilt.
5. **Bronnen testen.** Tabblad *Actions* → *Bronnencheck* → *Run workflow*. Pas in `sources.yaml` de bronnen aan die LEEG of FOUT geven.

## De site (aiontcijferd.be)

De site staat in `site/` (Astro) en leest de edities uit `content/edities/`. Een editie verschijnt pas online als `status: klaar` staat én **Mijn inschatting** ingevuld is. Termen voor de jargonfilter staan in `content/jargon.json`, correcties in `content/correcties.json`.

- **Hosting:** Vercel-project met als *Root Directory* `site`. Elke wijziging op `main` in `site/` of `content/` bouwt de site opnieuw; dagelijkse data-commits niet.
- **Lokaal bekijken:** `cd site && npm install && TOON_CONCEPTEN=1 npm run dev` (toont ook concepten).
- **Nieuwsbrief:** Brevo verstuurt automatisch (RSS-campagne) vanuit `https://aiontcijferd.be/rss.xml`. Het inschrijfformulier staat in `site/src/components/Inschrijven.astro`.

## Kosten in de hand

- Het dure model draait één keer per week; het goedkope doet het dagelijkse sorteerwerk.
- `config.yaml` bevat harde plafonds (`limieten`), met een noodrem op het aantal modeloproepen per run.
- Elke oproep wordt gelogd met het aantal tokens: `data/kosten.csv` (dagelijks) en `data/weken/<week>/kosten.csv` (weekeditie).

## Lokaal testen zonder kosten

```bash
pip install -r requirements.txt
AIO_DROOG=1 python -m pipeline.triage
AIO_DROOG=1 python -m pipeline.weekeditie
```

Met `AIO_DROOG=1` antwoordt een nepmodel, zodat je de hele keten kunt testen zonder API-sleutels.

## Mappen

```
config.yaml          modellen, limieten, drempels
sources.yaml         bronnenlijst (te verifiëren via Bronnencheck)
prompts/             redactiestatuut + instructies per rol
pipeline/            verkenner, triage, weekeditie, bronnencheck
data/items/          ruwe items per dag
data/triage/         scores per dag
data/weken/<week>/   kandidaten, bronmateriaal, bevindingen, logboek per editie
content/edities/     concepten en gepubliceerde edities (Markdown)
```

## Licentie

- **Code** (alles buiten `content/`): MIT, zie `LICENSE`.
- **Inhoud** (`content/`): CC BY 4.0, zie `content/LICENTIE.md`. Overnemen en aanpassen mag, met vermelding van AI Ontcijferd en een link.

## Publieke spiegel

De redactie werkt in een privé-repo. Een workflow zet na elke wijziging een kopie in de publieke repo: zonder
geschiedenis en zonder de opgehaalde berichten en bronteksten van anderen (`spiegel/uitsluiten.txt`). Lees je dit in
de publieke repo, dan staan de workflows in `.github/workflows-voorbeeld/` en kun je de keten zelf testen met
`AIO_DROOG=1` (zie hierboven). Een fout of een voorstel melden kan daar met een issue.
