"""X-RADAR — wat er op X rondgaat over AI, via Grok (xAI) met de tool x_search.

Een radar, geen bron: elk item wijst waar mogelijk naar het oorspronkelijke artikel of
de blog waarnaar de post linkt. Alleen als er geen link is, blijft de post zelf de url.
Resultaat: nieuwe items in data/items/JJJJ-MM-DD.json (type "x"), daarna gewone triage.

Zonder XAI_API_KEY slaat dit script zichzelf over, zodat de dagelijkse run niet faalt.
Gebruik:  python -m pipeline.xradar
"""

from __future__ import annotations

import datetime as dt
import json
import os

from pipeline.common import (DATA, DROOG, _log_kosten, config, haal_json, lees_json, log, nu,
                             rapporteer_fouten, schrijf_json)
from pipeline.verkenner import item_id, schone_url

OPDRACHT = """Je bent de X-radar van AI Ontcijferd, een Vlaamse analysesite over AI.
Zoek op X naar de belangrijkste berichten over AI van {van} tot {tot}{wie}.
{extra}
Kies hoogstens {max} berichten die echt nieuws bevatten: een nieuw model of product, onderzoek,
een meting, beleid, een incident, een opvallende uitspraak van een betrokkene. Sla promotie,
memes, vacatures en herhalingen over.

Per bericht geef je:
- post_url: de url van de post op x.com
- auteur: de @handle
- datum: JJJJ-MM-DD
- samenvatting: één of twee zinnen in het Nederlands, wat de post zegt (niet wat je denkt)
- bron_url: de url van het artikel, de blog of het rapport waarnaar de post linkt, of "" als er geen is
- titel: een korte, feitelijke titel in het Nederlands

Verzin niets. Geen link in de post? Dan bron_url "". Antwoord UITSLUITEND met een JSON-array:
[{{"post_url": "...", "auteur": "...", "datum": "...", "samenvatting": "...", "bron_url": "...", "titel": "..."}}]
"""


def _zoek(m: dict, tekst: str, handles: list[str] | None, van: str, tot: str):
    if DROOG:
        return json.dumps([{
            "post_url": "https://x.com/voorbeeld/status/1", "auteur": "@voorbeeld", "datum": tot,
            "samenvatting": "Proefdraai: nepbericht van de X-radar.", "bron_url": "https://example.com/artikel",
            "titel": "Proefdraai X-radar"}]), 0, 0
    import openai

    client = openai.OpenAI(api_key=os.environ["XAI_API_KEY"], base_url="https://api.x.ai/v1")
    tool = {"type": "x_search", "from_date": van, "to_date": tot}
    if handles:
        tool["allowed_x_handles"] = handles[:20]  # x_search aanvaardt er hoogstens 20
    r = client.responses.create(model=m["model"], input=tekst, tools=[tool],
                                max_output_tokens=m["max_tokens"])
    gebruik = getattr(r, "usage", None)
    return r.output_text, getattr(gebruik, "input_tokens", 0), getattr(gebruik, "output_tokens", 0)


def main() -> None:
    if not DROOG and not os.environ.get("XAI_API_KEY"):
        log("X-radar overgeslagen: geen XAI_API_KEY ingesteld")
        return
    cfg = config()
    m = cfg["modellen"]["xradar"]
    xc = cfg.get("xradar", {})
    vandaag = nu().date()
    van, tot = (vandaag - dt.timedelta(days=1)).isoformat(), vandaag.isoformat()

    opdrachten = []
    for g in xc.get("groepen", []):
        wie = " van deze accounts: " + ", ".join("@" + h for h in g["handles"])
        opdrachten.append((g["naam"], g["handles"], wie, ""))
    for v in xc.get("vrij", []):
        opdrachten.append((v["naam"], None, "", v["vraag"]))

    gezien_pad = DATA / "gezien.json"
    gezien: dict[str, str] = lees_json(gezien_pad, {})
    dag_pad = DATA / "items" / f"{vandaag.isoformat()}.json"
    dag_items: list[dict] = lees_json(dag_pad, [])
    nieuw, fouten = 0, []

    for naam, handles, wie, extra in opdrachten:
        tekst = OPDRACHT.format(van=van, tot=tot, wie=wie, extra=extra, max=xc.get("max_posts", 25))
        try:
            antwoord, tin, tuit = _zoek(m, tekst, handles, van, tot)
            _log_kosten("xradar", m, tin, tuit)
            berichten = haal_json(antwoord)
        except Exception as fout:
            fouten.append(f"{naam}: {fout.__class__.__name__}: {str(fout)[:300]}")
            continue
        for b in berichten if isinstance(berichten, list) else []:
            post = str(b.get("post_url", "")).strip()
            bron = str(b.get("bron_url", "")).strip()
            if not post.startswith("http"):
                continue
            url = schone_url(bron if bron.startswith("http") else post)
            i = {
                "url": url,
                "titel": str(b.get("titel") or b.get("samenvatting", ""))[:300],
                "samenvatting": str(b.get("samenvatting", ""))[:600],
                "gepubliceerd": str(b.get("datum", "")),
                "id": item_id(url),
                "bron_id": f"x-{naam.replace(' ', '-')}",
                "bron_naam": f"X: {b.get('auteur', '?')}",
                "type": "x",
                "alleen_koppen": False,
                "post_url": post,
                "opgehaald": nu().isoformat(timespec="seconds"),
            }
            if i["id"] in gezien:
                continue
            gezien[i["id"]] = vandaag.isoformat()
            dag_items.append(i)
            nieuw += 1

    schrijf_json(dag_pad, dag_items)
    schrijf_json(gezien_pad, gezien)
    log(f"X-radar: {nieuw} nieuwe items uit {len(opdrachten)} zoekopdrachten")
    if fouten:
        rapporteer_fouten(f"xradar-{vandaag.isoformat()}", fouten)


if __name__ == "__main__":
    main()
