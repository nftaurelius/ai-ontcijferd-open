"""Verpakker: maakt per gepubliceerde editie het verspreidingspakket.

Geen model nodig: alles komt rechtstreeks uit de gepubliceerde editie, zodat er niets in staat wat de site niet
waarmaakt. Het LinkedIn-concept van de weekpijplijn (linkedin.md) gaat mee, met de vraag het na te lezen tegen de
gepubliceerde versie.

Resultaat: data/weken/<week>/verspreiding/pakket.md
Gebruik:  python -m pipeline.verpakker            (alle gepubliceerde edities zonder pakket)
          python -m pipeline.verpakker 2026-w47   (deze week, ook als er al een pakket is)
"""

from __future__ import annotations

import re
import sys

import yaml

from pipeline.common import CONTENT, DATA, log

SITE = "https://aiontcijferd.be"
NAAMSVERMELDING = "Bron: AI Ontcijferd (aiontcijferd.be), door Duncan Panis. Vrij over te nemen onder CC BY 4.0."
VAST = {"Lezersvraag", "De week in één alinea", "Ruis van de week", "Woord van de week", "Mijn inschatting",
        "Zo is dit gemaakt", "Bronnen"}
# Woorden die de huisstijl niet wil (data/huisstijl.md, "Woorden die we niet gebruiken").
VERBODEN = ["revolutionair", "baanbrekend", "game changer", "gamechanger", "magisch", "ongezien", "godlike",
            "superintelligent", "het einde van", "apocalyps"]


def lees(pad) -> tuple[dict, str]:
    tekst = pad.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", tekst, re.S)
    return (yaml.safe_load(m.group(1)) or {}, m.group(2)) if m else ({}, tekst)


def secties(body: str) -> list[tuple[str, str]]:
    delen = re.split(r"^## (.+)$", body, flags=re.M)
    return [(delen[i].strip(), delen[i + 1]) for i in range(1, len(delen) - 1, 2)]


def plat(md: str) -> str:
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    md = re.sub(r"<details>.*?</details>", "", md, flags=re.S)
    md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)
    md = re.sub(r"[*_`#>]", "", md)
    return re.sub(r"\s+", " ", md).strip()


def zinnen(tekst: str) -> list[str]:
    return [z.strip() for z in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9ÀÉÈËÏÖÜ\"“])", tekst) if z.strip()]


def tot_woorden(tekst: str, max_woorden: int) -> str:
    """Hele zinnen, zolang het onder het maximum blijft (minstens één zin)."""
    uit: list[str] = []
    for z in zinnen(tekst):
        if uit and len(" ".join(uit + [z]).split()) > max_woorden:
            break
        uit.append(z)
    return " ".join(uit)


def woorden(tekst: str) -> int:
    return len(tekst.split())


def editie(pad) -> dict | None:
    meta, body = lees(pad)
    s = dict(secties(body))
    inschatting = re.sub(r"<!--.*?-->", "", s.get("Mijn inschatting", ""), flags=re.S).strip()
    if meta.get("status") != "klaar" or not inschatting:
        return None
    onderwerpen = []
    for titel, tekst in secties(body):
        if titel in VAST:
            continue
        hype = re.search(r"^\*\*Hype-meter:\*\*\s*(.+)$", tekst, re.M)
        stand, uitleg = "", ""
        if hype:
            stand, _, uitleg = hype.group(1).partition(" — ")
            stand = re.sub(r"\s*\(.*\)$", "", stand).strip().rstrip(".")
        onderwerpen.append({"titel": titel, "stand": stand, "uitleg": plat(uitleg)})
    week = str(meta.get("week") or pad.name.replace("-stand-van-ai.md", ""))
    return {"week": week, "titel": str(meta.get("titel", "Stand van AI")), "kern": plat(s.get("De week in één alinea", "")),
            "onderwerpen": onderwerpen, "url": f"{SITE}/edities/{week}"}


def pakket(e: dict) -> str:
    w = e["week"]
    nr = int(w.split("-w")[1])
    linkedin_pad = DATA / "weken" / w / "linkedin.md"
    linkedin = linkedin_pad.read_text(encoding="utf-8").strip() if linkedin_pad.exists() else ""

    lijst = "\n".join(f"- {o['titel']}" + (f" (hype-meter: {o['stand'].lower()})" if o["stand"] else "") for o in e["onderwerpen"])
    over_kop = e["titel"]
    over_slot = f"Lees de volledige analyse, met bronnen: {e['url']}\n\n{NAAMSVERMELDING}"
    # Overneemblok: hoogstens 150 woorden in totaal, naamsvermelding inbegrepen.
    budget = 150 - woorden(over_kop) - woorden(over_slot) - woorden(lijst) - 2
    if budget < 40:  # te veel onderwerpen: dan zonder lijst
        lijst, budget = "", 150 - woorden(over_kop) - woorden(over_slot)
    overneem = "\n\n".join(x for x in [over_kop, tot_woorden(e["kern"], budget), ("Deze week:\n" + lijst) if lijst else "", over_slot] if x)

    eerste = zinnen(e["kern"])[0] if e["kern"] else ""
    if eerste[:2] not in ("AI",) and not eerste[:2].isupper():
        eerste = eerste[:1].lower() + eerste[1:]
    bericht = f"Stand van AI, week {nr}: {eerste} Vijf minuten lezen, gratis: {e['url']}"

    luister = [f"Dit is de Stand van AI van week {nr}, van AI Ontcijferd. Wat er gebeurde in AI, en wat het betekent voor Vlaanderen.",
               tot_woorden(e["kern"], 90)]
    for i, o in enumerate(e["onderwerpen"], 1):
        regel = f"Onderwerp {i}: {o['titel']}."
        if o["stand"]:
            regel += f" De hype-meter staat op {o['stand'].lower()}."
            if o["uitleg"]:
                regel += " " + tot_woorden(o["uitleg"], 30)
        luister.append(regel)
    luister.append("De volledige analyse, met alle bronnen, staat op aiontcijferd.be. Inschrijven op de nieuwsbrief kan daar ook, gratis.")
    luisterscript = "\n\n".join(luister)

    teksten = {"Overneemblok": overneem, "Berichtendienst": bericht, "Luisterscript": luisterscript, "LinkedIn": linkedin}
    toets = []
    for naam, t in teksten.items():
        gevonden = [v for v in VERBODEN if v in t.lower()]
        if gevonden:
            toets.append(f"- {naam}: woorden uit de lijst \"niet gebruiken\": {', '.join(gevonden)}.")
    toets.append(f"- Overneemblok: {woorden(overneem)} woorden (maximum 150).")
    toets.append(f"- Berichtendienst: {woorden(bericht)} woorden.")
    minuten = max(1, round(woorden(luisterscript) / 150))
    toets.append(f"- Luisterscript: {woorden(luisterscript)} woorden, ongeveer {minuten} {'minuut' if minuten == 1 else 'minuten'} voorgelezen.")
    if not linkedin:
        toets.append("- LinkedIn: geen concept gevonden in de weekmap.")

    return f"""# Verspreidingspakket {e['titel']}

Gemaakt door de Verpakker uit de gepubliceerde editie: {e['url']}
Per onderdeel: plaatsen, aanpassen of overslaan. Niets wordt automatisch geplaatst of verstuurd.

## 1. Nieuwsbrief

- Mail: {SITE}/mail/{w}.html (conceptcampagne in Brevo, lijst #3; jij verstuurt)

## 2. Deelafbeelding

- {SITE}/deel/edities/{w}.png (1200 bij 630, ook voor LinkedIn en berichtendiensten)

## 3. LinkedIn (concept van de weekpijplijn, in jouw stem)

Lees het na tegen de gepubliceerde editie: het concept is gemaakt voor de eindredactie.

```
{linkedin or "(geen concept)"}
```

## 4. Overneemblok (voor nieuwsbrieven en websites van partners)

```
{overneem}
```

## 5. Korte versie voor een berichtendienst (WhatsApp, Signal, Teams)

```
{bericht}
```

## 6. Luisterscript (om voor te lezen of in te spreken)

```
{luisterscript}
```

## Toets aan de huisstijl

{chr(10).join(toets)}
"""


def main() -> None:
    gevraagd = sys.argv[1] if len(sys.argv) > 1 else None
    gemaakt = 0
    for pad in sorted((CONTENT / "edities").glob("*-stand-van-ai.md")):
        e = editie(pad)
        if not e or (gevraagd and e["week"] != gevraagd):
            continue
        doel = DATA / "weken" / e["week"] / "verspreiding" / "pakket.md"
        if doel.exists() and not gevraagd:
            continue
        doel.parent.mkdir(parents=True, exist_ok=True)
        doel.write_text(pakket(e), encoding="utf-8")
        log(f"Verspreidingspakket gemaakt: {doel.relative_to(DATA.parent)}")
        gemaakt += 1
    if not gemaakt:
        log("Geen nieuwe gepubliceerde editie zonder pakket.")


if __name__ == "__main__":
    main()
