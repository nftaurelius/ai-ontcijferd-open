# AI Ontcijferd

AI zonder hype. Door Duncan Panis.

Dit is de code en de inhoud achter [aiontcijferd.be](https://aiontcijferd.be): een Vlaamse site die AI begrijpelijk,
bruikbaar en doorgeefbaar maakt. Elke week de Stand van AI, elke dag een dagbrief, en daarrond lespakketten, tools,
fiches en een AI Act-kompas. Alles is gratis en open: de inhoud onder CC BY 4.0, de code onder MIT.

Het grootste deel van het werk doen AI-agents. Een mens, de eindredacteur, leest alles na en beslist wat online gaat.
Het redactiestatuut dat elke agent volgt, staat in [`prompts/statuut.md`](prompts/statuut.md). Waarom en hoe we zo
werken, en wat het kost, staat op [Zo werken we](https://aiontcijferd.be/zo-werken-we).

## Wat je hiermee kunt

- **Inhoud overnemen.** Teksten, fiches, het AI Act-kompas en de lespakketten mag je overnemen en aanpassen, met
  vermelding van AI Ontcijferd en een link. Zie [Neem het over](https://aiontcijferd.be/overnemen).
- **Een fout melden of iets voorstellen.** Open een issue in deze repo, of mail naar redactie@aiontcijferd.be. Zie
  [CONTRIBUTING.md](CONTRIBUTING.md) en [Meedoen](https://aiontcijferd.be/meedoen).
- **De site lokaal draaien.** Zie "De site" hieronder.
- **De agentketen zelf draaien,** voor je eigen regio, sector of taal. Je kunt ze eerst gratis testen met een nepmodel.

## Waar je dit leest

De redactie werkt in een privé-repo. Een workflow zet na elke wijziging een kopie in de publieke repo
[nftaurelius/ai-ontcijferd-open](https://github.com/nftaurelius/ai-ontcijferd-open): zonder geschiedenis, zonder de
opgehaalde berichten en bronteksten van anderen, en zonder een paar werknotities (lijst in `spiegel/uitsluiten.txt`).
In de publieke repo staan de workflows daarom in `.github/workflows-voorbeeld/`, waar GitHub ze niet uitvoert.

Een wijziging rechtstreeks in de publieke repo wordt bij de volgende kopie overschreven. Een goed voorstel nemen we
over in de werkrepo, met vermelding van wie het indiende.

## Hoe de keten werkt

| Wanneer | Workflow | Wat gebeurt er |
| --- | --- | --- |
| Elke ochtend | Dagelijks | **Verkenner** haalt nieuwe items op uit `sources.yaml`, ook YouTube-kanalen. **X-radar** zoekt op X via Grok (als er een xAI-sleutel is). **Triage** (goedkoop model) scoort ze op relevantie voor Vlaanderen en hype. |
| Na Dagelijks | Plus — dagbrief | **Dagbrief** schrijft het nieuws van het etmaal, **dagcontrole** (model van een andere leverancier) toetst het aan de bronnen. Zijn er geen open problemen, dan verschijnt de dagbrief meteen; anders komt er een pull request. |
| Vrijdag | Wekelijks | **Analist** schrijft het concept, **vertaler** maakt het leesbaar, **tegenspreker** (andere leverancier) controleert, **analist** verwerkt de bevindingen. Er komt een pull request; de eindredacteur schrijft "Mijn inschatting" en publiceert. |
| Met de hand | Plus — dossier | Een uitgebreid stuk over één onderwerp, met dezelfde controle als de weekeditie. |
| Maandag | Bronnencheck | Test elke bron en zet in `data/bronnencheck.md` welke niets opleveren. |
| Bij elke wijziging en dagelijks | Publieke spiegel | Zet de gefilterde kopie in de publieke repo. |

Elke editie houdt bij wat de agents deden: de kandidaten, de bevindingen van de tegenspreker en wat ermee gebeurde, en
de kosten per modeloproep (`data/weken/<week>/`).

## Zelf testen, zonder kosten

```bash
pip install -r requirements.txt
AIO_DROOG=1 python -m pipeline.triage
AIO_DROOG=1 python -m pipeline.weekeditie
```

Met `AIO_DROOG=1` antwoordt een nepmodel, zodat je de hele keten kunt doorlopen zonder API-sleutels.

## Zelf draaien, met echte modellen

1. **Bronnen.** Pas `sources.yaml` aan voor jouw regio of sector. In `config.yaml` staan de modellen, de limieten en
   de drempels van de triage.
2. **API-sleutels.** Maak een aparte sleutel bij Anthropic en bij OpenAI, en stel in beide consoles een maandelijkse
   uitgavenlimiet in. Voor de X-radar ook een sleutel bij xAI; zonder die sleutel slaat de keten X over.
3. **Secrets in GitHub.** *Settings* → *Secrets and variables* → *Actions*: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`
   en eventueel `XAI_API_KEY`.
4. **Workflows.** Zet de bestanden uit `.github/workflows-voorbeeld/` in `.github/workflows/`. Geef de workflows
   schrijfrechten: *Settings* → *Actions* → *General* → *Workflow permissions* → *Read and write permissions*, en vink
   *Allow GitHub Actions to create and approve pull requests* aan.
5. **Bronnen testen.** *Actions* → *Bronnencheck* → *Run workflow*.

**Kosten in de hand:** het dure model draait één keer per week, het goedkope doet het dagelijkse sorteerwerk.
`config.yaml` bevat harde plafonds (`limieten`), met een noodrem op het aantal modeloproepen per run. Elke oproep wordt
gelogd met het aantal tokens in `data/kosten.csv`, `data/plus/kosten.csv` en `data/weken/<week>/kosten.csv`.

## De site

De site staat in `site/` (Astro) en leest alles uit `content/`. Een editie of dossier verschijnt pas online als
`status: klaar` staat én "Mijn inschatting" ingevuld is.

```bash
cd site
npm install
TOON_CONCEPTEN=1 npm run dev   # toont ook concepten
npm run build                  # bouwt de statische site in site/dist
```

- **Hosting:** Vercel, met `site` als *Root Directory*. Een wijziging in `site/` of `content/` bouwt de site opnieuw.
- **Nieuwsbrief:** de site maakt per editie een mail op `/mail/<week>.html` (sjabloon `site/src/lib/mail.ts`). De
  eindredacteur verstuurt ze zelf via Brevo.
- **Tools** zoals de Plakcheck zijn één zelfstandig HTML-bestand in `site/public/<slug>/app/`, zonder netwerkverkeer.
- **Lespakketten:** een map per pakket in `content/materiaal/`; zie `content/materiaal/README.md`.

## Mappen

```
config.yaml            modellen, limieten, drempels
sources.yaml           bronnenlijst
prompts/               redactiestatuut en instructies per rol
pipeline/              verkenner, xradar, triage, weekeditie, dagbrief, dossier, bronnencheck
content/edities/       weekedities (Markdown)
content/plus/          dagbrieven en dossiers
content/materiaal/     open lespakketten
content/fiches/        fiches
content/jargon.json    jargonfilter
data/weken/<week>/     bevindingen, logboek en kosten per editie
data/visie.md          visie en routekaart
site/                  de website (Astro)
spiegel/               hoe de publieke kopie gemaakt wordt
```

## Licentie

- **Code** (alles buiten `content/`): MIT, zie [`LICENSE`](LICENSE).
- **Inhoud** (`content/`): CC BY 4.0, zie [`content/LICENTIE.md`](content/LICENTIE.md). Overnemen en aanpassen mag,
  met vermelding van AI Ontcijferd en een link. Citaten en cijfers van anderen in onze stukken blijven van hun makers.
