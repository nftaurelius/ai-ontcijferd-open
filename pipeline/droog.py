"""Nepmodel voor proefdraaien (AIO_DROOG=1): test de keten zonder API-kosten."""

from __future__ import annotations

import json
import re

CONCEPT = """## De week in één alinea
Proefdraai: dit is geen echte editie.

## Proefonderwerp
**Labels:** Burgers
**Hype-meter:** Terecht — proefdraai.

**Wat gebeurde er?** Een voorbeeld, [bron](https://example.org/a).

**Waarom doet het ertoe voor Vlaanderen?** Om de keten te testen.

<details><summary>Verdieping</summary>

Geen.

</details>

## Ruis van de week
Geen deze week.

## Woord van de week
Proefdraai: een test zonder echte kosten.

## Bronnen
1. [Voorbeeld](https://example.org/a), Example
"""


DAGBRIEF = """## Vandaag in het kort
Proefdraai: dit is geen echte dagbrief.

## Proefonderwerp
**Labels:** Burgers, Werk
**Status:** Eén bron

Een voorbeeld, [bron](https://example.org/a). Context bij het voorbeeld.

**Voor wie:**
- **Burgers:** om de keten te testen.

## Uit de radar
- Een signaal op X, [post](https://x.com/voorbeeld/status/1) (nog niet bevestigd)

## Bronnen
1. [Voorbeeld](https://example.org/a), Example
"""


def nepantwoord(rol: str, invoer: str) -> str:
    if rol == "dagbrief":
        if "BEVINDINGEN:" in invoer:
            return DAGBRIEF + '\n---VERANTWOORDING---\n[{"passage": "Een voorbeeld", "beslissing": "verwerkt", "toelichting": "ok"}]'
        return DAGBRIEF
    if rol == "dagcontrole":
        return '[{"ernst": "kritiek", "passage": "Een voorbeeld", "probleem": "proef", "voorstel": "proef"}]'
    if rol == "dossier" and "BEVINDINGEN:" in invoer:
        return CONCEPT + '\n---VERANTWOORDING---\n[]'
    if rol == "dossier":
        return CONCEPT
    if rol == "triage":
        try:
            items = json.loads(invoer)
        except json.JSONDecodeError:
            return "Proefdraai: concept voor een LinkedIn-post."
        return json.dumps([{"id": i["id"], "relevantie": 4 if n % 2 == 0 else 2, "hype": 1,
                            "labels": ["Burgers", "Werk"], "onderwerp": f"onderwerp {n}",
                            "waarom": "proefdraai"} for n, i in enumerate(items)])
    if rol == "vertaler":
        return CONCEPT + '\n---JARGON---\n[{"term": "proefdraai", "uitleg_leek": "Een test.", "voorbeeld": "Deze run."}]'
    if rol == "tegenspreker":
        return '[{"ernst": "klein", "passage": "Een voorbeeld", "probleem": "vaag", "voorstel": "concreter"}]'
    if rol == "analist" and "BEVINDINGEN:" in invoer:
        return CONCEPT + '\n---VERANTWOORDING---\n[{"passage": "Een voorbeeld", "beslissing": "verwerkt", "toelichting": "ok"}]'
    return CONCEPT
