"""TRIAGE — scoort nieuwe items op relevantie voor Vlaanderen en hype-gehalte.

Goedkoop model, dagelijks. Resultaat: data/triage/JJJJ-MM-DD.json
Gebruik:  python -m pipeline.triage            (vandaag)
          python -m pipeline.triage 2026-10-26 (een andere dag)
"""

from __future__ import annotations

import json
import sys

from pipeline.common import DATA, Noodrem, config, rapporteer_fouten, haal_json, lees_json, log, nu, schrijf_json, systeemprompt, vraag

LABELS = {"Onderwijs", "Werk", "Lokale overheden", "Zelfstandigen", "Bibliotheken", "Burgers"}


def _schoon(score: dict) -> dict:
    """Houd modeluitvoer binnen de afgesproken vorm."""
    def getal(x):
        try:
            return max(0, min(5, int(x)))
        except (TypeError, ValueError):
            return 0
    return {
        "relevantie": getal(score.get("relevantie")),
        "hype": getal(score.get("hype")),
        "labels": [l for l in score.get("labels", []) if l in LABELS],
        "onderwerp": str(score.get("onderwerp", ""))[:80],
        "waarom": str(score.get("waarom", ""))[:300],
    }


def main(dag: str | None = None) -> None:
    cfg = config()
    dag = dag or nu().date().isoformat()
    items = lees_json(DATA / "items" / f"{dag}.json", [])
    uit_pad = DATA / "triage" / f"{dag}.json"
    scores: dict[str, dict] = lees_json(uit_pad, {})

    te_doen = [i for i in items if i["id"] not in scores]
    if not te_doen:
        log(f"Triage {dag}: niets nieuw")
        return

    systeem = systeemprompt("triage")
    stap = cfg["limieten"]["triage_batch"]
    fouten = []
    for start in range(0, len(te_doen), stap):
        partij = te_doen[start : start + stap]
        invoer = [{"id": i["id"], "titel": i["titel"], "bron": i["bron_naam"],
                   "brontype": i["type"], "samenvatting": i["samenvatting"][:600],
                   **({"rol": i["rol"]} if i.get("rol") else {})} for i in partij]
        try:
            antwoord = vraag("triage", systeem, json.dumps(invoer, ensure_ascii=False, indent=1))
            geldige_ids = {i["id"] for i in partij}
            for s in haal_json(antwoord):
                if isinstance(s, dict) and s.get("id") in geldige_ids:
                    scores[s["id"]] = _schoon(s)
        except Noodrem:
            raise
        except Exception as fout:  # één mislukte partij mag de rest niet tegenhouden
            fouten.append(f"partij {start // stap + 1}: {fout.__class__.__name__}: {str(fout)[:500]}")
            log(f"Triage-fout in {fouten[-1]}")
        schrijf_json(uit_pad, scores)  # tussentijds bewaren

    gescoord = sum(1 for i in te_doen if i["id"] in scores)
    behouden = sum(1 for s in scores.values() if s["relevantie"] >= cfg["triage"]["min_relevantie"])
    log(f"Triage {dag}: {gescoord}/{len(te_doen)} items gescoord, {behouden} boven de drempel")
    if fouten:
        rapporteer_fouten(f"triage-{dag}", fouten)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
