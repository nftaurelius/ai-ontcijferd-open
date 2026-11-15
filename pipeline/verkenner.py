"""VERKENNER — haalt dagelijks nieuwe items op uit de bronnenlijst.

Geen taalmodel nodig. Resultaat: data/items/JJJJ-MM-DD.json
Gebruik:  python -m pipeline.verkenner
"""

from __future__ import annotations

import datetime as dt
import hashlib
import re
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import feedparser
import requests
from bs4 import BeautifulSoup

from pipeline.common import DATA, bronnen, config, lees_json, log, nu, schrijf_json

UA = "AI-Ontcijferd-verkenner/1.0 (+https://aiontcijferd.be/zo-werken-we)"
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "nl-BE,nl;q=0.9,en;q=0.8",
}
TIMEOUT = 20


def schone_url(url: str) -> str:
    """Verwijder trackingparameters en ankers, zodat dubbels herkenbaar zijn."""
    d = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(d.query) if not k.lower().startswith(("utm_", "ref"))]
    return urlunsplit((d.scheme, d.netloc, d.path, urlencode(query), ""))


def item_id(url: str) -> str:
    return hashlib.sha1(url.encode()).hexdigest()[:12]


def trefwoordfilter(termen: list[str] | None):
    if not termen:
        return lambda titel: True
    delen = []
    for t in termen:
        kern = t.strip()
        # "AI" alleen als los woord in hoofdletters, anders vang je "mail", "trail" enz.
        delen.append(r"(?-i:\bAI\b)" if kern == "AI" else re.escape(kern))
    patroon = re.compile("|".join(delen), re.IGNORECASE)
    return lambda titel: bool(patroon.search(titel))


LINK_RE = re.compile(r"https?://[^\s<>\"')\]]+")
# Links in videobeschrijvingen die zelden een nieuwsbron zijn
RUIS_DOMEINEN = ("youtube.com", "youtu.be", "instagram.com", "tiktok.com", "facebook.com", "discord.gg",
                 "patreon.com", "skool.com", "linktr.ee", "gumroad.com", "calendly.com", "bit.ly", "amzn.to")


def _tekst(html: str, max_tekens: int = 400) -> str:
    tekst = BeautifulSoup(html or "", "html.parser").get_text(" ", strip=True)
    return tekst[:max_tekens]


def lees_rss(inhoud: bytes, bron: dict) -> list[dict]:
    feed = feedparser.parse(inhoud)
    items = []
    for e in feed.entries:
        if not e.get("link") or not e.get("title"):
            continue
        items.append({
            "url": schone_url(e.link),
            "titel": e.title.strip(),
            "samenvatting": _tekst(e.get("summary", "")),
            "gepubliceerd": e.get("published", e.get("updated", "")),
        })
    return items


def lees_pagina(html: str, bron: dict) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    patroon = re.compile(bron["link_patroon"])
    items, gezien = [], set()
    for a in soup.find_all("a", href=True):
        url = urljoin(bron["url"], a["href"])
        if not patroon.search(url):
            continue
        url = schone_url(url)
        titel = " ".join(a.get_text(" ", strip=True).split()) or a.get("title", "")
        if url in gezien or len(titel) < 12:
            continue
        gezien.add(url)
        items.append({"url": url, "titel": titel[:300], "samenvatting": "", "gepubliceerd": ""})
    return items


def youtube_kanaal_id(handle: str) -> str:
    """Zoek het kanaal-id (UC...) bij een @handle; bewaard in data/youtube-kanalen.json."""
    pad = DATA / "youtube-kanalen.json"
    kanalen: dict[str, str] = lees_json(pad, {})
    if handle in kanalen:
        return kanalen[handle]
    r = requests.get(f"https://www.youtube.com/{handle}", headers=HEADERS, timeout=TIMEOUT,
                     cookies={"CONSENT": "YES+1"})  # sla de toestemmingspagina over
    r.raise_for_status()
    # Eerst wat zeker over dit kanaal zelf gaat (canonieke link, metadata), pas dan losse vermeldingen:
    # een kanaalpagina noemt ook andere kanalen (aanbevolen, samenwerkingen).
    m = (re.search(r'<link rel="canonical" href="https://www\.youtube\.com/channel/(UC[\w-]{22})"', r.text)
         or re.search(r'<meta itemprop="(?:identifier|channelId)" content="(UC[\w-]{22})"', r.text)
         or re.search(r'"externalId":"(UC[\w-]{22})"', r.text)
         or re.search(r"channel_id=(UC[\w-]{22})", r.text))
    if not m:
        raise ValueError(f"kanaal-id niet gevonden voor {handle}")
    kanalen[handle] = m.group(1)
    schrijf_json(pad, kanalen)
    return m.group(1)


def lees_youtube(inhoud: bytes, bron: dict) -> list[dict]:
    """Openbare kanaalfeed: titel, link en de (langere) beschrijving met de links erin."""
    feed = feedparser.parse(inhoud)
    items = []
    for e in feed.entries:
        if not e.get("link") or not e.get("title"):
            continue
        beschrijving = e.get("media_description") or e.get("summary", "")
        links = []
        for url in LINK_RE.findall(beschrijving):
            url = schone_url(url.rstrip(".,;"))
            if not any(d in urlsplit(url).netloc for d in RUIS_DOMEINEN) and url not in links:
                links.append(url)
        items.append({
            "url": schone_url(e.link),
            "titel": e.title.strip(),
            "samenvatting": _tekst(beschrijving, 1500),
            "gepubliceerd": e.get("published", ""),
            "links": links[:15],
            "rol": bron.get("rol", "nieuws"),
        })
    return items


def haal_bron(bron: dict, filteren: bool = True) -> list[dict]:
    if bron["methode"] == "youtube":
        kanaal = youtube_kanaal_id(bron["kanaal"])
        r = requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={kanaal}",
                         headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        items = lees_youtube(r.content, bron)
    else:
        r = requests.get(bron["url"], headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        items = lees_rss(r.content, bron) if bron["methode"] == "rss" else lees_pagina(r.text, bron)
    filter_ = trefwoordfilter(bron.get("trefwoorden"))
    if filteren:
        items = [i for i in items if filter_(i["titel"])]
    for i in items:
        i.update({
            "id": item_id(i["url"]),
            "bron_id": bron["id"],
            "bron_naam": bron["naam"],
            "type": bron["type"],
            "alleen_koppen": bool(bron.get("alleen_koppen")),
        })
    return items[: bron.get("max_per_run", config()["limieten"].get("max_per_bron", 12))]


def main() -> None:
    cfg = config()
    vandaag = nu().date().isoformat()
    gezien_pad = DATA / "gezien.json"
    gezien: dict[str, str] = lees_json(gezien_pad, {})
    dag_pad = DATA / "items" / f"{vandaag}.json"
    dag_items: list[dict] = lees_json(dag_pad, [])

    nieuw, fouten = 0, []
    for bron in bronnen():
        try:
            items = haal_bron(bron)
        except Exception as fout:
            fouten.append(f"{bron['id']}: {fout.__class__.__name__}: {fout}")
            continue
        for i in items:
            if i["id"] in gezien or len(dag_items) >= cfg["limieten"]["max_items_per_dag"]:
                continue
            i["opgehaald"] = nu().isoformat(timespec="seconds")
            gezien[i["id"]] = vandaag
            dag_items.append(i)
            nieuw += 1

    # vergeet items ouder dan 90 dagen, zodat het bestand klein blijft
    grens = nu().date() - dt.timedelta(days=90)
    gezien = {k: v for k, v in gezien.items() if dt.date.fromisoformat(v) >= grens}

    schrijf_json(dag_pad, dag_items)
    schrijf_json(gezien_pad, gezien)
    log(f"Verkenner: {nieuw} nieuwe items, {len(fouten)} bronnen met fouten")
    for f in fouten:
        log(f"  fout bij {f}")


if __name__ == "__main__":
    main()
