"""DAGBRIEF — de dagelijkse update van AI Ontcijferd Plus.

Keten: items van het laatste etmaal (verkenner, YouTube- en X-radar, triage)
       -> bronteksten ophalen -> SCHRIJVER (dagbrief) -> CONTROLE (andere leverancier)
       -> REVISIE alleen als er kritieke bevindingen zijn.
Resultaat: content/plus/dag/JJJJ-MM-DD.md  (status: klaar; de workflow publiceert automatisch
           als data/plus/JJJJ-MM-DD/vrijgeven.txt "ja" zegt, anders maakt hij een pull request)
           data/plus/JJJJ-MM-DD/           (kandidaten, bronmateriaal, bevindingen, pr.md)
           data/plus/gebruikt.json         (items die al in een dagbrief stonden)
Gebruik:  python -m pipeline.dagbrief
"""

from __future__ import annotations

import datetime as dt
import json
import os
from urllib.parse import urlsplit

from pipeline import common
from pipeline.common import (CONTENT, DATA, config, haal_json, lees_json, log, nu, prompt,
                             schrijf_json, systeemprompt, vraag)
from pipeline.weekeditie import BRONGEWICHT, brontekst, splits

RADAR_DOMEINEN = ("youtube.com", "youtu.be", "x.com", "twitter.com")
# Links in videobeschrijvingen zijn vaak sponsors of affiliates. Alleen deze domeinen gelden als bron;
# aangevuld met elk domein uit sources.yaml.
BETROUWBAAR = ("openai.com", "anthropic.com", "deepmind.google", "blog.google", "ai.google.dev", "x.ai",
               "mistral.ai", "ai.meta.com", "about.fb.com", "microsoft.com", "nvidia.com", "apple.com",
               "deepseek.com", "qwenlm.github.io", "moonshot.ai", "huggingface.co", "arxiv.org", "github.com",
               "epoch.ai", "artificialanalysis.ai", "metr.org", "reuters.com", "apnews.com", "bloomberg.com",
               "ft.com", "axios.com", "theverge.com", "techcrunch.com", "wired.com", "arstechnica.com",
               "thenextweb.com", "theinformation.com", "nytimes.com", "washingtonpost.com", "bbc.co.uk",
               "bbc.com", "theguardian.com", "cnbc.com", "europa.eu", "vrt.be", "standaard.be", "tijd.be")


def betrouwbaar(url: str) -> bool:
    from pipeline.common import bronnen
    host = urlsplit(url).netloc.lower().removeprefix("www.")
    eigen = {urlsplit(b["url"]).netloc.lower().removeprefix("www.") for b in bronnen() if b.get("url")}
    return any(host == d or host.endswith("." + d) for d in (*BETROUWBAAR, *eigen))


def is_radar(url: str) -> bool:
    return any(d in urlsplit(url).netloc for d in RADAR_DOMEINEN)


def opgehaald(item: dict) -> dt.datetime | None:
    try:
        return dt.datetime.fromisoformat(item.get("opgehaald", ""))
    except ValueError:
        return None


def kandidaten(cfg: dict) -> tuple[list[dict], list[dict], list[dict]]:
    """Geeft (bronnen, techniek, radar) terug, elk gesorteerd van belangrijk naar minder."""
    pc = cfg["plus"]
    grens = nu() - dt.timedelta(hours=pc["uren_terug"])
    gebruikt = set(lees_json(DATA / "plus" / "gebruikt.json", {}).keys())
    alle = []
    for d in (nu().date() - dt.timedelta(days=1), nu().date()):
        scores = lees_json(DATA / "triage" / f"{d.isoformat()}.json", {})
        for item in lees_json(DATA / "items" / f"{d.isoformat()}.json", []):
            s = scores.get(item["id"])
            tijd = opgehaald(item)
            if not s or s["relevantie"] < pc["min_relevantie"] or item["id"] in gebruikt:
                continue
            if tijd and tijd < grens:
                continue
            alle.append({**item, **s})

    def score(i):
        return i["relevantie"] * BRONGEWICHT.get(i["type"], 0.5) - 0.3 * i["hype"]

    alle.sort(key=score, reverse=True)
    bronnen, techniek, radar = [], [], []
    per_onderwerp: dict[str, dict] = {}
    for i in alle:
        # Een video die naar een artikel linkt: dat artikel is de bron, de video het signaal
        if i["type"] == "video" and i.get("rol") != "techniek":
            bron = next((l for l in i.get("links", []) if betrouwbaar(l)), None)
            if bron:  # anders blijft de video een signaal onder "Uit de radar"
                i = {**i, "url": bron, "gevonden_via": f"{i['bron_naam']}: {i['url']}"}
        if i["type"] == "video" and i.get("rol") == "techniek":
            techniek.append(i)
            continue
        if is_radar(i["url"]):
            radar.append(i)
            continue
        sleutel = i["onderwerp"].lower().strip() or i["id"]
        if sleutel in per_onderwerp:
            per_onderwerp[sleutel].setdefault("verwant", []).append(
                {"titel": i["titel"], "url": i["url"], "bron": i["bron_naam"]})
        else:
            per_onderwerp[sleutel] = i
            bronnen.append(i)
    # iets ruimer dan nodig: de schrijver kiest, en sommige bronnen leveren geen tekst op
    return bronnen[: pc["dagbrief_items"] + 4], techniek[:3], radar[: pc["radar_items"] * 2]


def materiaal(bronnen: list[dict], techniek: list[dict], radar: list[dict], max_tekens: int) -> str:
    blokken = []
    for n, k in enumerate(bronnen, 1):
        tekst, _ = brontekst(k, max_tekens)
        k["brontekst_lengte"] = len(tekst)
        verwant = "\n".join(f"  - {v['titel']} ({v['bron']}): {v['url']}" for v in k.get("verwant", []))
        blokken.append(
            f"### BRON {n}: {k['titel']}\nBron: {k['bron_naam']} (type: {k['type']})\nURL: {k['url']}\n"
            + (f"Gevonden via: {k['gevonden_via']}\n" if k.get("gevonden_via") else "")
            + f"Triage: relevantie {k['relevantie']}/5, hype {k['hype']}/5, labels {', '.join(k['labels'])}\n"
            + (f"Verwante berichtgeving:\n{verwant}\n" if verwant else "")
            + f"\nBrontekst:\n{tekst}\n")
    for n, k in enumerate(techniek, 1):
        blokken.append(f"### TECHNIEK {n}: {k['titel']}\nKanaal: {k['bron_naam']}\nURL: {k['url']}\n"
                       f"Labels: {', '.join(k['labels'])}\nBeschrijving van de maker:\n{k['samenvatting']}\n")
    for n, k in enumerate(radar, 1):
        blokken.append(f"### RADAR {n}: {k['titel']}\nWaar: {k['bron_naam']}\nURL: {k.get('post_url') or k['url']}\n"
                       f"Samenvatting: {k['samenvatting']}\n")
    return "\n\n".join(blokken)


def main() -> None:
    cfg = config()
    pc = cfg["plus"]
    # eigen noodrem: de dagbrief mag nooit meer oproepen doen dan nodig
    cfg["limieten"]["max_oproepen_per_run"] = pc["max_oproepen_dagbrief"]
    common.config = lambda: cfg

    datum = os.environ.get("AIO_DATUM", "").strip() or nu().date().isoformat()
    map_ = DATA / "plus" / datum
    bronnen, techniek, radar = kandidaten(cfg)
    if len(bronnen) < 2:
        log(f"Dagbrief {datum}: te weinig bronnen ({len(bronnen)}); geen dagbrief vandaag.")
        return

    mat = (f"Deze dagbrief gaat over het nieuws van het etmaal vóór {datum}.\n\n"
           + materiaal(bronnen, techniek, radar, pc["max_tekens_per_bron"]))
    map_.mkdir(parents=True, exist_ok=True)
    (map_ / "bronmateriaal.md").write_text(mat, encoding="utf-8")
    schrijf_json(map_ / "kandidaten.json",
                 [{k: v for k, v in c.items() if k != "brontekst"} for c in bronnen + techniek + radar])

    log("Dagbrief: schrijven")
    systeem = common.prompt("statuut") + "\n\n" + prompt(
        "dagbrief", datum=datum, max_items=pc["dagbrief_items"], max_radar=pc["radar_items"])
    concept = vraag("dagbrief", systeem, f"MATERIAAL:\n\n{mat}")

    log("Dagbrief: controle door een tweede leverancier")
    controle_mislukt = False
    try:
        bevindingen = haal_json(vraag("dagcontrole", systeemprompt("tegenspreker"),
                                      f"CONCEPT:\n\n{concept}\n\n=====\nBRONMATERIAAL:\n\n{mat}"))
    except Exception as fout:  # controle mislukt: wel een brief, maar duidelijk gemarkeerd in de PR
        log(f"Controle mislukt: {fout}")
        controle_mislukt = True
        bevindingen = [{"ernst": "kritiek", "passage": "(hele dagbrief)",
                        "probleem": f"De controle liep niet: {fout.__class__.__name__}. Lees alles zelf na."}]
    schrijf_json(map_ / "bevindingen.json", bevindingen)
    kritiek = [b for b in bevindingen if b.get("ernst") == "kritiek"]

    tekst, verantwoording = concept, []
    if kritiek and kritiek[0].get("passage") != "(hele dagbrief)":
        log(f"Dagbrief: revisie ({len(kritiek)} kritieke bevindingen)")
        tekst, verantwoording = splits(vraag(
            "dagbrief", systeemprompt("revisie"),
            f"CONCEPT:\n\n{concept}\n\n=====\nBEVINDINGEN:\n\n{json.dumps(bevindingen, ensure_ascii=False, indent=1)}"
            f"\n\n=====\nBRONMATERIAAL:\n\n{mat}"), "---VERANTWOORDING---")
    schrijf_json(map_ / "verantwoording.json", verantwoording)

    # De dagbrief heeft geen hype-meter (die is voor de weekeditie); revisies voegen er soms een toe
    tekst = "\n".join(r for r in tekst.splitlines() if not r.startswith("**Hype-meter:**"))

    m = cfg["modellen"]
    gemaakt = (
        "## Zo is dit gemaakt\n\n"
        f"- AI-agents verzamelden het nieuws (websites, YouTube en X als radar), schreven deze dagbrief "
        f"({m['dagbrief']['model']}) en lieten hem controleren door een model van een andere leverancier "
        f"({m['dagcontrole']['model']}).\n"
        "- Video's en posts zijn nooit een bron: we vermelden ze alleen als signaal, of als demo onder \"Om te proberen\".\n"
        "- De dagbrief verschijnt automatisch als de controle geen open problemen meer ziet; anders leest "
        "eindredacteur Duncan Panis hem eerst na. Fout gezien? [Meld het](/correcties). "
        "Meer: [Zo werken we](/zo-werken-we).\n")
    if "## Bronnen" in tekst:
        kern, bronlijst = tekst.split("## Bronnen", 1)
        tekst = f"{kern.rstrip()}\n\n{gemaakt}\n## Bronnen{bronlijst}"
    else:
        tekst = f"{tekst.rstrip()}\n\n{gemaakt}"

    labels = sorted({l for k in bronnen for l in k["labels"]})
    voorkant = ("---\n"
                f"titel: \"Plus · {datum}\"\n"
                f"datum: {datum}\n"
                "status: klaar\n"
                f"labels: {json.dumps(labels, ensure_ascii=False)}\n"
                "---\n\n")
    uit = CONTENT / "plus" / "dag" / f"{datum}.md"
    uit.parent.mkdir(parents=True, exist_ok=True)
    uit.write_text(voorkant + tekst.strip() + "\n", encoding="utf-8")

    # Alles wat de schrijver te zien kreeg, telt als gebruikt; zo herhaalt morgen niets
    gebruikt_pad = DATA / "plus" / "gebruikt.json"
    gebruikt = lees_json(gebruikt_pad, {})
    for k in bronnen + techniek + radar:
        gebruikt[k["id"]] = datum
    grens = (nu().date() - dt.timedelta(days=30)).isoformat()
    schrijf_json(gebruikt_pad, {k: v for k, v in gebruikt.items() if v >= grens})

    # Automatisch publiceren, tenzij de controle niet liep of de revisie een kritiek punt liet liggen
    niet = [v for v in verantwoording if v.get("beslissing") == "niet verwerkt"]
    if controle_mislukt:
        vrijgeven, reden = False, "de controle door de tweede leverancier liep niet"
    elif kritiek and not verantwoording:
        vrijgeven, reden = False, "er waren kritieke bevindingen, maar de revisie verantwoordde ze niet"
    elif niet:
        vrijgeven, reden = False, f"de revisie liet {len(niet)} bevinding(en) bewust liggen"
    else:
        vrijgeven, reden = True, "controle gedaan, kritieke bevindingen verwerkt"
    (map_ / "vrijgeven.txt").write_text(("ja" if vrijgeven else "nee") + "\n", encoding="utf-8")
    log(f"Automatisch publiceren: {'ja' if vrijgeven else 'nee'} ({reden})")

    pr = [f"Dagbrief van AI Ontcijferd Plus, {datum}.", "",
          f"**Niet automatisch gepubliceerd: {reden}.**" if not vrijgeven else f"Vrijgegeven: {reden}.", "",
          "**Samenvoegen = publiceren.** Niet goed? Sluit de pull request, of pas het bestand eerst aan.", "",
          f"- Bronnen bekeken: {len(bronnen)}, techniek: {len(techniek)}, radar: {len(radar)}.",
          f"- Controle: {len(bevindingen)} bevinding(en), waarvan {len(kritiek)} kritiek."]
    if kritiek:
        pr += ["", "### Kritieke bevindingen (check of ze opgelost zijn)"]
        pr += [f"- *{b.get('passage', '')[:120]}* — {b.get('probleem', '')}" for b in kritiek]
    if niet:
        pr += ["", "### Niet verwerkt, met motivering"]
        pr += [f"- *{v.get('passage', '')[:120]}* — {v.get('toelichting', '')}" for v in niet]
    (map_ / "pr.md").write_text("\n".join(pr) + "\n", encoding="utf-8")
    log(f"Dagbrief klaar: {uit.relative_to(CONTENT.parent)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as fout:
        import traceback
        from pipeline.common import rapporteer_fouten
        rapporteer_fouten(f"dagbrief-{nu().date().isoformat()}",
                          [f"{fout.__class__.__name__}: {str(fout)[:800]}", traceback.format_exc()[-1500:]])
        raise
