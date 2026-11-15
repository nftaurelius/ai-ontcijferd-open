"""WEEKEDITIE — maakt het concept van de wekelijkse Stand van AI.

Keten: kandidaten kiezen -> bronteksten ophalen -> ANALIST -> VERTALER
       -> TEGENSPREKER (andere leverancier) -> REVISIE door de analist.
Resultaat: content/edities/JJJJ-wWW-stand-van-ai.md (status: concept)
           data/weken/JJJJ-wWW/ (kandidaten, bevindingen, verantwoording, logboek)
Gebruik:  python -m pipeline.weekeditie
          AIO_DATUM=2026-10-23 python -m pipeline.weekeditie   (editie voor een vroegere vrijdag)
"""

from __future__ import annotations

import datetime as dt
import json
import os
from email.utils import parsedate_to_datetime
from urllib.parse import urlsplit

from pipeline.common import (CONTENT, DATA, DROOG, config, haal_json, lees_json, log, nu, prompt,
                             schrijf_json, systeemprompt, vraag)

import yaml

BRONGEWICHT = {"primair": 1.0, "beleid": 1.0, "meting": 0.8, "vlaams": 0.8, "duiding": 0.5, "radar": 0.6,
               "x": 0.5, "video": 0.4}
# Radar-items die naar een post of video zelf wijzen, zijn geen bron voor de weekeditie
GEEN_BRON = ("youtube.com", "youtu.be", "x.com", "twitter.com")


def peildatum() -> dt.date:
    """De vrijdag waarvoor de editie gemaakt wordt: vandaag, of AIO_DATUM (JJJJ-MM-DD)."""
    waarde = os.environ.get("AIO_DATUM", "").strip()
    return dt.date.fromisoformat(waarde) if waarde else nu().date()


def publicatiedatum(tekst: str) -> dt.date | None:
    if not tekst:
        return None
    try:
        return parsedate_to_datetime(tekst).date()
    except (TypeError, ValueError):
        pass
    try:
        return dt.datetime.fromisoformat(tekst.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def week_sleutel(datum: dt.date) -> tuple[str, str]:
    jaar, week, _ = datum.isocalendar()
    return f"{jaar}-w{week:02d}", f"week {week}, {jaar}"


def kandidaten(cfg: dict, peil: dt.date) -> list[dict]:
    """Beste items uit het venster vóór de peildatum, één per onderwerp, met verwante bronnen.

    Normaal: items opgehaald in de voorbije dagen. Met een vroegere peildatum: alle opgehaalde
    items waarvan de publicatiedatum in het venster valt (items zonder datum worden later
    nagekeken via de datum op de bronpagina).
    """
    dagen = cfg["triage"]["dagen_terug"]
    begin = peil - dt.timedelta(days=dagen - 1)
    terugblik = peil < nu().date()
    alle = []
    bestanden = sorted((DATA / "items").glob("*.json"))
    for pad in bestanden:
        dag = pad.stem
        if not terugblik and not (begin.isoformat() <= dag <= peil.isoformat()):
            continue
        scores = lees_json(DATA / "triage" / f"{dag}.json", {})
        for item in lees_json(pad, []):
            s = scores.get(item["id"])
            if not s or s["relevantie"] < cfg["triage"]["min_relevantie"]:
                continue
            if any(d in urlsplit(item["url"]).netloc for d in GEEN_BRON):
                continue
            if terugblik:
                pub = publicatiedatum(item.get("gepubliceerd", ""))
                if pub and not (begin <= pub <= peil):
                    continue
                item = {**item, "datum_onbekend": pub is None}
            alle.append({**item, **s})

    def score(i):  # relevant, primair en weinig hype eerst
        return i["relevantie"] * BRONGEWICHT.get(i["type"], 0.5) - 0.3 * i["hype"]

    alle.sort(key=score, reverse=True)
    per_onderwerp: dict[str, dict] = {}
    gezien_urls = set()
    per_domein: dict[str, int] = {}
    max_per_domein = cfg["limieten"].get("max_kandidaten_per_bron", 3)
    for i in alle:
        if i["url"] in gezien_urls:
            continue
        gezien_urls.add(i["url"])
        # spreiding: tel per doeldomein, zodat ook radar-links naar openai.com meetellen voor OpenAI
        domein = urlsplit(i["url"]).netloc.removeprefix("www.")
        sleutel_k = i["onderwerp"].lower().strip() or i["id"]
        if sleutel_k not in per_onderwerp and per_domein.get(domein, 0) >= max_per_domein:
            continue
        if sleutel_k not in per_onderwerp:
            per_domein[domein] = per_domein.get(domein, 0) + 1
        sleutel = i["onderwerp"].lower().strip() or i["id"]
        if sleutel in per_onderwerp:
            per_onderwerp[sleutel].setdefault("verwant", []).append(
                {"titel": i["titel"], "url": i["url"], "bron": i["bron_naam"]})
        else:
            per_onderwerp[sleutel] = i
    # bij een terugblik ruimer selecteren: items buiten het venster vallen later nog af
    factor = 3 if terugblik else 1
    return list(per_onderwerp.values())[: cfg["limieten"]["kandidaten_per_week"] * factor]


def tips(peil: dt.date, dagen: int) -> list[dict]:
    """Tips van de eindredactie uit content/tips.yaml die bij deze week horen."""
    pad = CONTENT / "tips.yaml"
    if not pad.exists():
        return []
    data = yaml.safe_load(pad.read_text(encoding="utf-8")) or {}
    begin = peil - dt.timedelta(days=dagen - 1)
    uit = []
    for t in data.get("tips") or []:
        if not t.get("url") or t.get("gebruikt_in"):
            continue
        datum = t.get("datum")
        if isinstance(datum, str):
            datum = dt.date.fromisoformat(datum)
        if datum and not (begin <= datum <= peil):
            continue
        uit.append({
            "id": "tip-" + t["url"][-12:], "url": t["url"], "titel": t.get("titel") or t["url"],
            "samenvatting": "", "bron_id": "tip", "bron_naam": "Tip van de eindredactie",
            "type": "tip", "alleen_koppen": False, "relevantie": 5, "hype": 0,
            "labels": [], "onderwerp": "tip " + (t.get("titel") or t["url"]),
            "waarom": "Aangebracht door Duncan: " + (t.get("notitie") or ""),
            "gepubliceerd": datum.isoformat() if datum else "",
            "verwant": [{"titel": u, "url": u, "bron": "extra bron bij tip"} for u in t.get("extra_bronnen") or []],
        })
    return uit


def open_lezersvraag() -> dict | None:
    pad = CONTENT / "lezersvragen.yaml"
    if not pad.exists():
        return None
    data = yaml.safe_load(pad.read_text(encoding="utf-8")) or {}
    for v in data.get("vragen") or []:
        if v.get("vraag") and not v.get("beantwoord_in"):
            return v
    return None


def markeer_vraag_beantwoord(vraag: str, sleutel: str) -> None:
    pad = CONTENT / "lezersvragen.yaml"
    tekst = pad.read_text(encoding="utf-8")
    kop = "".join(r + "\n" for r in tekst.splitlines() if r.startswith("#"))
    data = yaml.safe_load(tekst) or {}
    for v in data.get("vragen") or []:
        if v.get("vraag") == vraag:
            v["beantwoord_in"] = sleutel
    pad.write_text(kop + yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def markeer_tips_gebruikt(urls: set[str], sleutel: str) -> None:
    pad = CONTENT / "tips.yaml"
    if not urls or not pad.exists():
        return
    tekst = pad.read_text(encoding="utf-8")
    kop = "".join(r + "\n" for r in tekst.splitlines() if r.startswith("#"))
    data = yaml.safe_load(tekst) or {}
    for t in data.get("tips") or []:
        if t.get("url") in urls:
            t["gebruikt_in"] = sleutel
    pad.write_text(kop + yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def brontekst(item: dict, max_tekens: int) -> tuple[str, dt.date | None]:
    """Haal de tekst van de bronpagina op, plus de datum die op de pagina staat (als die er is)."""
    if item.get("alleen_koppen"):
        return "(Betaalmuur of auteursrecht: alleen de kop is bruikbaar als signaal.)", None
    if DROOG:
        return item.get("samenvatting") or "(proefdraai: geen brontekst opgehaald)", None
    tekst, datum = None, None
    try:
        import trafilatura
        html = trafilatura.fetch_url(item["url"])
        if html:
            tekst = trafilatura.extract(html)
            meta = trafilatura.extract_metadata(html)
            if meta and meta.date:
                datum = dt.date.fromisoformat(meta.date[:10])
    except Exception as fout:
        log(f"  brontekst mislukt voor {item['url']}: {fout}")
    return (tekst or item.get("samenvatting") or "(geen tekst beschikbaar)")[:max_tekens], datum


def met_bronteksten(kand: list[dict], cfg: dict, peil: dt.date) -> list[dict]:
    """Haal bronteksten op; bij een terugblik vallen items buiten het venster alsnog af."""
    begin = peil - dt.timedelta(days=cfg["triage"]["dagen_terug"] - 1)
    terugblik = peil < nu().date()
    uit = []
    for k in kand:
        if len(uit) >= cfg["limieten"]["kandidaten_per_week"]:
            break
        tekst, datum = brontekst(k, cfg["limieten"]["max_tekens_per_bron"])
        datum = datum or publicatiedatum(k.get("gepubliceerd", ""))
        if terugblik and datum and not (begin <= datum <= peil):
            log(f"  buiten venster ({datum}): {k['titel'][:70]}")
            continue
        uit.append({**k, "brontekst": tekst, "datum": datum.isoformat() if datum else "onbekend"})
    return uit


def bronmateriaal(kand: list[dict]) -> str:
    blokken = []
    for n, k in enumerate(kand, 1):
        verwant = "\n".join(f"  - {v['titel']} ({v['bron']}): {v['url']}" for v in k.get("verwant", []))
        blokken.append(
            f"### K{n}: {k['titel']}\n"
            f"Bron: {k['bron_naam']} (type: {k['type']})\nURL: {k['url']}\nDatum: {k['datum']}\n"
            f"Triage: relevantie {k['relevantie']}/5, hype {k['hype']}/5, labels {', '.join(k['labels'])}"
            f" — {k['waarom']}\n"
            + (f"Verwante berichtgeving:\n{verwant}\n" if verwant else "")
            + f"\nBrontekst:\n{k['brontekst']}\n"
        )
    return "\n\n".join(blokken)


def vraag_model_post(editie: str, sleutel: str) -> str:
    opdracht = (
        "Schrijf een LinkedIn-post van hoogstens 120 woorden in de ik-vorm van Duncan Panis, "
        "eindredacteur van AI Ontcijferd. Kies het ene inzicht uit deze editie dat Vlaamse professionals het meest raakt, "
        "met de stand van de hype-meter. Droog en helder, geen hype, geen emoji, hoogstens drie hashtags. "
        f"Eindig met: Lees de hele Stand van AI: https://aiontcijferd.be/edities/{sleutel}\n\nEDITIE:\n\n{editie}"
    )
    return vraag("triage", prompt("statuut"), opdracht).strip()


def splits(antwoord: str, marker: str) -> tuple[str, list]:
    if marker in antwoord:
        tekst, rest = antwoord.split(marker, 1)
        try:
            return tekst.strip(), haal_json(rest)
        except ValueError:
            return tekst.strip(), []
    return antwoord.strip(), []


def main() -> None:
    cfg = config()
    peil = peildatum()
    sleutel, week_label = week_sleutel(peil)
    map_ = DATA / "weken" / sleutel
    logboek: list[str] = []

    getipt = tips(peil, cfg["triage"]["dagen_terug"])
    kand = met_bronteksten(getipt + kandidaten(cfg, peil), cfg, peil)
    if len(kand) < 3:
        log(f"Te weinig kandidaten ({len(kand)}) voor een editie; gestopt.")
        return
    schrijf_json(map_ / "kandidaten.json", [{k: v for k, v in c.items() if k != "brontekst"} for c in kand])
    begin = peil - dt.timedelta(days=cfg["triage"]["dagen_terug"] - 1)
    if getipt:
        logboek.append(f"Tips van de eindredactie meegenomen: {len(getipt)}.")
    markeer_tips_gebruikt({t["url"] for t in getipt}, sleutel)
    logboek.append(f"Verkenner en triage: {len(kand)} kandidaat-onderwerpen uit de periode "
                   f"{begin:%d/%m} tot {peil:%d/%m/%Y}.")

    lezersvraag = open_lezersvraag()
    lezers = ""
    if lezersvraag:
        lezers = ("LEZERSVRAAG (beantwoord in een sectie '## Lezersvraag', na de onderwerpen en vóór 'Ruis van de week'; "
                  f"begin met de vraag in vet; vermeld als afzender: {lezersvraag.get('van') or 'anoniem'}):\n"
                  f"{lezersvraag['vraag']}\n\n")
        logboek.append("Lezersvraag meegenomen.")
    materiaal = lezers + (f"Deze editie gaat over de periode {begin:%d/%m} tot en met {peil:%d/%m/%Y}. "
                 "Gebruik geen gebeurtenissen van na die periode.\n\n" + bronmateriaal(kand))
    (map_ / "bronmateriaal.md").write_text(materiaal, encoding="utf-8")

    log("Analist schrijft het concept")
    concept = vraag("analist", systeemprompt("analist", week_label=week_label),
                    f"Kandidaten en bronteksten voor {week_label}:\n\n{materiaal}")
    logboek.append("Analist: koos de onderwerpen en schreef het concept.")

    log("Vertaler maakt het leesbaar")
    leesbaar, jargon = splits(vraag("vertaler", systeemprompt("vertaler"), concept), "---JARGON---")
    schrijf_json(map_ / "jargon.json", jargon)
    # Nieuwe termen gaan mee in de pull request naar de jargonfilter, zodat Duncan ze nakijkt
    jargon_pad = CONTENT / "jargon.json"
    bestaand = lees_json(jargon_pad, [])
    gekend = {t["term"].lower().removeprefix("ai-") for t in bestaand}
    nieuw = [{"term": t["term"], "uitleg_leek": t.get("uitleg_leek", ""), "voorbeeld": t.get("voorbeeld", "")}
             for t in jargon if isinstance(t, dict) and t.get("term")
             and t["term"].lower().removeprefix("ai-") not in gekend][:8]
    if nieuw:
        schrijf_json(jargon_pad, bestaand + nieuw)
    logboek.append(f"Vertaler: maakte de tekst leesbaar voor leken (vaktermen uitgelegd: {len(jargon)}).")

    log("Tegenspreker controleert")
    bevindingen = haal_json(vraag(
        "tegenspreker", systeemprompt("tegenspreker"),
        f"CONCEPT:\n\n{leesbaar}\n\n=====\nBRONMATERIAAL:\n\n{materiaal}"))
    schrijf_json(map_ / "bevindingen.json", bevindingen)
    kritiek = sum(1 for b in bevindingen if b.get("ernst") == "kritiek")
    logboek.append(f"Tegenspreker: bevindingen {len(bevindingen)}, waarvan kritiek {kritiek}.")

    log("Analist verwerkt de bevindingen")
    definitief, verantwoording = splits(vraag(
        "analist", systeemprompt("revisie"),
        f"CONCEPT:\n\n{leesbaar}\n\n=====\nBEVINDINGEN:\n\n{json.dumps(bevindingen, ensure_ascii=False, indent=1)}"
        f"\n\n=====\nBRONMATERIAAL:\n\n{materiaal}"), "---VERANTWOORDING---")
    schrijf_json(map_ / "verantwoording.json", verantwoording)
    niet = [v for v in verantwoording if v.get("beslissing") == "niet verwerkt"]
    logboek.append(f"Revisie: {len(verantwoording) - len(niet)} bevindingen verwerkt, {len(niet)} gemotiveerd niet.")

    if lezersvraag and "## Lezersvraag" in definitief:
        markeer_vraag_beantwoord(lezersvraag["vraag"], sleutel)

    # Concept voor een LinkedIn-post (goedkoop model), mee in de pull request
    try:
        post = vraag_model_post(definitief, sleutel)
        (map_ / "linkedin.md").write_text(post + "\n", encoding="utf-8")
        logboek.append("Concept voor een LinkedIn-post klaargezet (data/weken/<week>/linkedin.md).")
    except Exception as fout:
        log(f"LinkedIn-concept mislukt: {fout}")

    m = cfg["modellen"]
    gemaakt = (
        "## Zo is dit gemaakt\n\n"
        f"- AI-agents verzamelden en selecteerden het nieuws, schreven het concept en controleerden het. "
        f"Schrijver: {m['analist']['model']} ({m['analist']['leverancier']}); "
        f"controle: {m['tegenspreker']['model']} ({m['tegenspreker']['leverancier']}).\n"
        f"- De tegenspreker maakte {len(bevindingen)} opmerking(en), waarvan {kritiek} kritiek; kritieke punten zijn opgelost of geschrapt.\n"
        "- Duncan Panis las alles na, paste aan waar nodig en schreef zelf \"Mijn inschatting\".\n"
        "- Meer over onze werkwijze: [Zo werken we](/zo-werken-we).\n"
    )
    inschatting = (
        "## Mijn inschatting\n\n"
        "<!-- DUNCAN: schrijf hier je oordeel. Zonder deze sectie gaat de editie niet online. -->\n"
    )
    # Bronnen achteraan houden: inschatting en werkwijze komen ervoor.
    if "## Bronnen" in definitief:
        kern, bronlijst = definitief.split("## Bronnen", 1)
        tekst = f"{kern.rstrip()}\n\n{inschatting}\n{gemaakt}\n## Bronnen{bronlijst}"
    else:
        tekst = f"{definitief}\n\n{inschatting}\n{gemaakt}"

    labels = sorted({l for k in kand for l in k["labels"]})
    voorkant = (
        "---\n"
        f"titel: \"Stand van AI — {week_label}\"\n"
        f"week: {sleutel}\n"
        f"datum: {peil.isoformat()}\n"
        "status: concept\n"
        f"labels: {json.dumps(labels, ensure_ascii=False)}\n"
        "---\n\n"
    )
    uit = CONTENT / "edities" / f"{sleutel}-stand-van-ai.md"
    uit.parent.mkdir(parents=True, exist_ok=True)
    uit.write_text(voorkant + tekst.strip() + "\n", encoding="utf-8")

    # Samenvatting voor de pull request: wat Duncan moet nakijken
    open_kritiek = [b for b in bevindingen if b.get("ernst") == "kritiek"]
    pr = [f"Concept van de Stand van AI, {week_label}.", "", "### Te doen voor publicatie",
          "- [ ] Tekst nalezen tegen de bronnen",
          "- [ ] Sectie **Mijn inschatting** schrijven",
          "- [ ] Nieuwe termen in `content/jargon.json` nakijken",
          "- [ ] `status: concept` veranderen in `status: klaar`", "", "### Logboek"]
    pr += [f"- {regel}" for regel in logboek]
    if open_kritiek:
        pr += ["", "### Kritieke bevindingen van de tegenspreker (check of ze opgelost zijn)"]
        pr += [f"- *{b.get('passage', '')[:120]}* — {b.get('probleem', '')}" for b in open_kritiek]
    if niet:
        pr += ["", "### Niet verwerkt, met motivering"]
        pr += [f"- *{v.get('passage', '')[:120]}* — {v.get('toelichting', '')}" for v in niet]
    (map_ / "pr.md").write_text("\n".join(pr) + "\n", encoding="utf-8")
    (map_ / "logboek.md").write_text("\n".join(f"- {r}" for r in logboek) + "\n", encoding="utf-8")

    log(f"Concept klaar: {uit.relative_to(CONTENT.parent)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as fout:
        import traceback
        from pipeline.common import rapporteer_fouten
        rapporteer_fouten(f"weekeditie-{week_sleutel(peildatum())[0]}",
                          [f"{fout.__class__.__name__}: {str(fout)[:800]}",
                           traceback.format_exc()[-1500:]])
        raise
