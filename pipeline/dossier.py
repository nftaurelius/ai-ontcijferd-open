"""DOSSIER — een uitgebreid stuk over één onderwerp (AI Ontcijferd Plus).

Duncan start het met de workflow "Plus — dossier" en geeft een titel, bron-urls en
trefwoorden mee. Keten: bronteksten ophalen (zijn urls + verwante items van de laatste
30 dagen) -> SCHRIJVER -> TEGENSPREKER (andere leverancier) -> REVISIE.
Resultaat: content/plus/dossiers/JJJJ-MM-DD-<slug>.md (status: concept)
           data/plus/dossiers/<slug>/ (bronmateriaal, bevindingen, pr.md)
Gebruik:  AIO_TITEL="..." AIO_URLS="https://... https://..." AIO_TREFWOORDEN="php, cyber" \
          python -m pipeline.dossier
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import unicodedata

from pipeline.common import (CONTENT, DATA, config, haal_json, lees_json, log, nu, prompt,
                             schrijf_json, systeemprompt, vraag)
from pipeline.verkenner import item_id, schone_url
from pipeline.weekeditie import brontekst, splits

GEEN_BRON = ("youtube.com", "youtu.be", "x.com", "twitter.com")


def slug(tekst: str) -> str:
    tekst = unicodedata.normalize("NFKD", tekst).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", tekst).strip("-")[:60]


def verwante_items(trefwoorden: list[str], dagen: int = 30, maximum: int = 10) -> list[dict]:
    if not trefwoorden:
        return []
    patroon = re.compile("|".join(re.escape(t) for t in trefwoorden), re.IGNORECASE)
    grens = (nu().date() - dt.timedelta(days=dagen)).isoformat()
    uit = []
    for pad in sorted((DATA / "items").glob("*.json"), reverse=True):
        if pad.stem < grens:
            break
        scores = lees_json(DATA / "triage" / pad.name, {})
        for i in lees_json(pad, []):
            s = scores.get(i["id"], {})
            if any(d in i["url"] for d in GEEN_BRON) or s.get("relevantie", 0) < 2:
                continue
            if patroon.search(i["titel"] + " " + s.get("onderwerp", "")):
                uit.append({**i, **s})
    uit.sort(key=lambda i: i.get("relevantie", 0), reverse=True)
    return uit[:maximum]


def main() -> None:
    cfg = config()
    titel = os.environ.get("AIO_TITEL", "").strip()
    if not titel:
        raise SystemExit("Geef een titel mee (AIO_TITEL).")
    notitie = os.environ.get("AIO_NOTITIE", "").strip() or "geen"
    urls = [schone_url(u) for u in re.split(r"[\s,]+", os.environ.get("AIO_URLS", "")) if u.startswith("http")]
    trefwoorden = [t.strip() for t in os.environ.get("AIO_TREFWOORDEN", "").split(",") if t.strip()]
    datum = nu().date().isoformat()
    s = slug(titel)
    map_ = DATA / "plus" / "dossiers" / s

    items = [{"id": item_id(u), "url": u, "titel": u, "bron_naam": "Aangebracht door de eindredactie",
              "type": "tip", "alleen_koppen": False, "samenvatting": ""} for u in urls]
    gekend = {i["url"] for i in items}
    items += [i for i in verwante_items(trefwoorden) if i["url"] not in gekend]
    if not items:
        raise SystemExit("Geen bronnen: geef urls of trefwoorden mee.")

    blokken = []
    for n, i in enumerate(items, 1):
        tekst, d = brontekst(i, cfg["limieten"]["max_tekens_per_bron"])
        blokken.append(f"### B{n}: {i['titel']}\nBron: {i['bron_naam']}\nURL: {i['url']}\n"
                       f"Datum: {d or i.get('gepubliceerd') or 'onbekend'}\n\nBrontekst:\n{tekst}\n")
    mat = f"Vandaag is {datum}.\n\n" + "\n\n".join(blokken)
    map_.mkdir(parents=True, exist_ok=True)
    (map_ / "bronmateriaal.md").write_text(mat, encoding="utf-8")

    log(f"Dossier '{titel}': schrijven met {len(items)} bronnen")
    systeem = prompt("statuut") + "\n\n" + prompt("dossier", titel=titel, notitie=notitie)
    concept = vraag("dossier", systeem, f"BRONMATERIAAL:\n\n{mat}")

    log("Dossier: tegenspreker")
    bevindingen = haal_json(vraag("tegenspreker", systeemprompt("tegenspreker"),
                                  f"CONCEPT:\n\n{concept}\n\n=====\nBRONMATERIAAL:\n\n{mat}"))
    schrijf_json(map_ / "bevindingen.json", bevindingen)

    log("Dossier: revisie")
    tekst, verantwoording = splits(vraag(
        "dossier", systeemprompt("revisie"),
        f"CONCEPT:\n\n{concept}\n\n=====\nBEVINDINGEN:\n\n{json.dumps(bevindingen, ensure_ascii=False, indent=1)}"
        f"\n\n=====\nBRONMATERIAAL:\n\n{mat}"), "---VERANTWOORDING---")
    schrijf_json(map_ / "verantwoording.json", verantwoording)

    m = cfg["modellen"]
    kritiek = [b for b in bevindingen if b.get("ernst") == "kritiek"]
    extra = ("## Mijn inschatting\n\n"
             "<!-- DUNCAN: schrijf hier je oordeel. Zonder deze sectie gaat het dossier niet online. -->\n\n"
             "## Zo is dit gemaakt\n\n"
             f"- AI-agents verzamelden de bronnen, schreven dit dossier ({m['dossier']['model']}) en lieten het "
             f"controleren door {m['tegenspreker']['model']} ({m['tegenspreker']['leverancier']}): "
             f"{len(bevindingen)} opmerking(en), waarvan {len(kritiek)} kritiek.\n"
             "- Duncan Panis las alles na en schreef zelf \"Mijn inschatting\". Meer: [Zo werken we](/zo-werken-we).\n")
    if "## Bronnen" in tekst:
        kern, bronlijst = tekst.split("## Bronnen", 1)
        tekst = f"{kern.rstrip()}\n\n{extra}\n## Bronnen{bronlijst}"
    else:
        tekst = f"{tekst.rstrip()}\n\n{extra}"

    labels = sorted({l for i in items for l in i.get("labels", [])})
    voorkant = ("---\n"
                f"titel: {json.dumps(titel, ensure_ascii=False)}\n"
                f"datum: {datum}\n"
                "status: concept\n"
                f"labels: {json.dumps(labels, ensure_ascii=False)}\n"
                "samenvatting: \"\"\n"
                "---\n\n")
    uit = CONTENT / "plus" / "dossiers" / f"{datum}-{s}.md"
    uit.parent.mkdir(parents=True, exist_ok=True)
    uit.write_text(voorkant + tekst.strip() + "\n", encoding="utf-8")

    pr = [f"Concept-dossier: **{titel}**", "", "### Te doen voor publicatie",
          "- [ ] Tekst nalezen tegen de bronnen", "- [ ] `samenvatting` in de kop invullen (één zin)",
          "- [ ] Sectie **Mijn inschatting** schrijven", "- [ ] `status: concept` veranderen in `status: klaar`",
          "", f"Bronnen: {len(items)} ({len(urls)} van jou, {len(items) - len(urls)} uit de verkenner)."]
    if kritiek:
        pr += ["", "### Kritieke bevindingen van de tegenspreker"]
        pr += [f"- *{b.get('passage', '')[:120]}* — {b.get('probleem', '')}" for b in kritiek]
    (map_ / "pr.md").write_text("\n".join(pr) + "\n", encoding="utf-8")
    log(f"Dossier klaar: {uit.relative_to(CONTENT.parent)}")


if __name__ == "__main__":
    main()
