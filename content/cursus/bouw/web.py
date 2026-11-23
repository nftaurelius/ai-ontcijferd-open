#!/usr/bin/env python3
"""Zet de cursusbron om in JSON voor de website (content/cursus/web/<id>.json).
Gebruik: python3 web.py   (vanuit content/cursus/bouw; nodig na elke wijziging in src/)
De PDF's maak je met: python3 build.py all  (komen in content/materiaal/ai-cursus/bestanden/)."""
import os, json, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

UIT = os.path.join(B.ROOT, "..", "web")
os.makedirs(UIT, exist_ok=True)
S = B.sources()
volgorde = []
for groep, ids in B.GROUPS:
    for i in ids: volgorde.append((groep, i))
index = []
for nr, (groep, i) in enumerate(volgorde, 1):
    meta, lines = B.parse(S[i][0])
    intro, chapters = B.render_body(lines)
    ih = "".join(intro).replace("@@TOC@@", "")
    a = meta.get("anchor", "ladder:1"); ak, _, an = a.partition(":")
    doc = {
        "id": i, "nr": nr, "groep": groep, "bestand": meta["file"], "pdf": f"/materiaal/ai-cursus/bestanden/{meta['file']}.pdf",
        "kicker": meta.get("kicker", ""), "titel": meta["title"], "ondertitel": meta.get("subtitle", ""),
        "tagline": meta.get("tagline", ""), "versie": meta.get("version", ""), "korteTitel": meta.get("toctitle", meta["title"]),
        "regel": meta.get("tocline", ""), "intro": ih,
        "hoofdstukken": [{"id": c["id"], "nr": c["num"], "kicker": c["kicker"], "titel": c["title"], "onder": c["sub"], "html": "".join(c["parts"])} for c in chapters],
    }
    json.dump(doc, open(os.path.join(UIT, f"{nr:02d}-{i}.json"), "w", encoding="utf-8"), ensure_ascii=False)
    index.append({k: doc[k] for k in ("id", "nr", "groep", "titel", "ondertitel", "korteTitel", "regel", "versie", "pdf")})
    print(f"{nr:2d} {i:13s} {len(chapters):2d} hoofdstukken")
json.dump(index, open(os.path.join(UIT, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
