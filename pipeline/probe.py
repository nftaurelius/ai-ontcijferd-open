"""PROBE — test losse adressen (kandidaat-bronnen) vanaf GitHub.

Gebruik:  python -m pipeline.probe URL [URL ...]
Schrijft per adres: HTTP-status, gevonden feeds, feeditems of alle links met tekst,
naar data/probe.md. Handig om nieuwe bronnen of link-patronen te kiezen.
"""

from __future__ import annotations

import sys
from urllib.parse import urljoin, urlsplit

import feedparser
import requests
from bs4 import BeautifulSoup

from pipeline.common import DATA, nu
from pipeline.verkenner import HEADERS, TIMEOUT


def probe(url: str) -> list[str]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except Exception as fout:
        return [f"verbinding mislukt: {fout.__class__.__name__}"]
    uit = [f"HTTP {r.status_code}, eind-url {r.url}, type {r.headers.get('content-type', '?')}"]
    if r.status_code >= 400:
        return uit
    feed = feedparser.parse(r.content)
    if feed.entries:
        uit.append(f"FEED met {len(feed.entries)} items")
        uit += [f"item: {e.get('title', '')[:90]} — {e.get('link', '')}" for e in feed.entries[:8]]
        return uit
    soup = BeautifulSoup(r.text, "html.parser")
    for l in soup.find_all("link", href=True):
        if any(t in (l.get("type") or "") for t in ("rss", "atom")):
            uit.append(f"feed: {urljoin(r.url, l['href'])}")
    host = urlsplit(r.url).netloc
    gezien = set()
    for a in soup.find_all("a", href=True):
        doel = urljoin(r.url, a["href"]).split("#")[0]
        tekst = " ".join(a.get_text(" ", strip=True).split())
        if urlsplit(doel).netloc == host and len(tekst) >= 15 and doel not in gezien:
            gezien.add(doel)
            uit.append(f"link: {doel} — {tekst[:70]}")
    uit.append(f"({len(gezien)} unieke links met tekst; {len(r.text)} tekens HTML)")
    return uit


def main(urls: list[str]) -> None:
    regels = [f"# Probe {nu():%Y-%m-%d %H:%M}", ""]
    for url in urls:
        regels += [f"## {url}", ""] + [f"- {x}" for x in probe(url)[:90]] + [""]
    tekst = "\n".join(regels) + "\n"
    (DATA / "probe.md").write_text(tekst, encoding="utf-8")
    print(tekst)


if __name__ == "__main__":
    main(sys.argv[1:])
