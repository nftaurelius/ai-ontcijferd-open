"""BRONNENCHECK — test elke bron en verzamelt diagnose voor wie niets oplevert.

Gebruik:  python -m pipeline.bronnencheck          (actieve bronnen)
          python -m pipeline.bronnencheck --alle   (ook inactieve bronnen)
Schrijft een overzicht naar data/bronnencheck.md (en naar de GitHub-samenvatting).
"""

from __future__ import annotations

import os
import re
import sys
from urllib.parse import urljoin, urlsplit

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup

from pipeline.common import DATA, ROOT, bronnen, nu
from pipeline.verkenner import HEADERS, TIMEOUT, haal_bron


def diagnose(b: dict) -> list[str]:
    """Wat staat er werkelijk op de pagina? Helpt om url of link_patroon te verbeteren."""
    if b["methode"] == "youtube":
        from pipeline.common import lees_json
        gekend = lees_json(DATA / "youtube-kanalen.json", {}).get(b["kanaal"], "nog niet opgezocht")
        return [f"kanaal-id: {gekend} (https://www.youtube.com/channel/{gekend})",
                f"YouTube-kanaal {b['kanaal']}: controleer of de @handle klopt; "
                "verwijder het kanaal uit data/youtube-kanalen.json om het id opnieuw op te zoeken"]
    try:
        r = requests.get(b["url"], headers=HEADERS, timeout=TIMEOUT)
    except Exception as fout:
        return [f"verbinding mislukt: {fout.__class__.__name__}"]
    regels = [f"HTTP {r.status_code}, eind-url {r.url}, type {r.headers.get('content-type', '?')}"]
    if r.status_code >= 400:
        return regels
    if b["methode"] == "rss":
        feed = feedparser.parse(r.content)
        regels.append(f"{len(feed.entries)} items in de feed vóór het trefwoordfilter")
        regels += [f"voorbeeldtitel: {e.get('title', '')[:100]}" for e in feed.entries[:5]]
        return regels
    soup = BeautifulSoup(r.text, "html.parser")
    feeds = [urljoin(r.url, l["href"]) for l in soup.find_all("link", href=True)
             if "rss" in (l.get("type") or "") or "atom" in (l.get("type") or "")]
    if feeds:
        regels.append("feeds op de pagina: " + ", ".join(feeds[:5]))
    host = urlsplit(r.url).netloc
    links = []
    for a in soup.find_all("a", href=True):
        url = urljoin(r.url, a["href"])
        tekst = " ".join(a.get_text(" ", strip=True).split())
        if urlsplit(url).netloc == host and len(tekst) >= 12:
            links.append((url, tekst[:70]))
    patroon = re.compile(b.get("link_patroon", "$^"))
    regels.append(f"{len(links)} links met tekst op hetzelfde domein, "
                  f"{sum(1 for u, _ in links if patroon.search(u))} passen bij het patroon")
    if not links:
        regels.append(f"pagina is mogelijk JavaScript-gestuurd ({len(r.text)} tekens HTML)")
    regels += [f"voorbeeldlink: {u} — {t}" for u, t in links[:12]]
    return regels


def wegwijzer_check() -> tuple[list[str], int]:
    """Werkt elke link in de wegwijzer nog, en is elk adres het voorbije kwartaal nagekeken?"""
    import datetime as dt
    pad = ROOT / "content" / "wegwijzer.yaml"
    if not pad.exists():
        return [], 0
    items = (yaml.safe_load(pad.read_text(encoding="utf-8")) or {}).get("wegwijzer", [])
    regels = ["", "## Wegwijzer (content/wegwijzer.yaml)", "",
              "| Adres | Status | Nagekeken | Opmerking |", "| --- | --- | --- | --- |"]
    vandaag, problemen = dt.date.today(), 0
    for w in items:
        opm = []
        try:
            r = requests.get(w["url"], headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
            code = str(r.status_code)
            if r.status_code >= 400:
                opm.append(f"link geeft {r.status_code}")
            elif urlsplit(r.url).netloc != urlsplit(w["url"]).netloc:
                opm.append(f"stuurt door naar {urlsplit(r.url).netloc}")
        except Exception as fout:
            code = "geen verbinding"
            opm.append(fout.__class__.__name__)
        gezien = w.get("laatstGecontroleerd")
        gezien = gezien if isinstance(gezien, dt.date) else dt.date.fromisoformat(str(gezien)) if gezien else None
        if not gezien or (vandaag - gezien).days > 100:
            opm.append("langer dan een kwartaal niet nagekeken")
        if w.get("status") != "gecontroleerd":
            opm.append("status TE CONTROLEREN (niet op de site)")
        if opm:
            problemen += 1
        regels.append(f"| {w.get('naam')} | {code} | {gezien or '?'} | {'; '.join(opm) or 'OK'} |")
    regels += ["", f"{problemen} adres(sen) in de wegwijzer vragen aandacht. Een 403 kan een site zijn die bots weert: open de link zelf."]
    return regels, problemen


def main() -> None:
    alle = "--alle" in sys.argv
    lijst = (yaml.safe_load((ROOT / "sources.yaml").read_text(encoding="utf-8"))["bronnen"]
             if alle else bronnen())
    regels = [f"# Bronnencheck {nu():%Y-%m-%d %H:%M}", "",
              "| Bron | Methode | Items | Status |", "| --- | --- | --- | --- |"]
    details, problemen = [], 0
    for b in lijst:
        try:
            items = haal_bron(b)
            aantal = len(items)
            if items:
                status = "OK"
            elif b.get("trefwoorden") and haal_bron(b, filteren=False):
                status = "OK (vandaag geen AI-titels)"
            else:
                status = "LEEG"
        except Exception as fout:
            status, aantal = f"FOUT: {fout.__class__.__name__} {str(fout)[:80]}", 0
        if not b.get("actief", True):
            status = f"UIT (bewust) — {status}"
        elif not status.startswith("OK"):
            problemen += 1
        if not status.startswith(("OK", "UIT")):
            details += [f"### {b['naam']} ({b['id']})", f"`{b.get('url') or b.get('kanaal')}`", ""]
            details += [f"- {d}" for d in diagnose(b)] + [""]
        regels.append(f"| {b['naam']} | {b['methode']} | {aantal} | {status} |")
        # inactieve bronnen krijgen geen diagnose, tenzij je ze zelf onderzoekt met Probe
    regels += ["", f"{problemen} bron(nen) vragen aandacht."]
    if details:
        regels += ["", "## Diagnose", ""] + details
    try:
        regels += wegwijzer_check()[0]
    except Exception as fout:  # de wegwijzer mag de bronnencheck nooit doen falen
        regels += ["", f"Wegwijzer niet nagekeken: {fout.__class__.__name__} {str(fout)[:80]}"]
    tekst = "\n".join(regels) + "\n"
    (DATA / "bronnencheck.md").write_text(tekst, encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(tekst)
    print(tekst)


if __name__ == "__main__":
    main()
