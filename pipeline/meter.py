"""Meter: elke maandag de cijfers van de verspreiding in data/verspreiding/cijfers.md (privé, niet in de spiegel).

Nu: inschrijvingen per Brevo-lijst en de laatste verstuurde campagnes (afgeleverd, geopend, geklikt).
Bezoeken en verwijzers staan alleen in het dashboard van Vercel Web Analytics; die vult Duncan of Claude met de hand
aan bij de nulmeting op 4 januari 2027.

Nodig: secret BREVO_API_KEY in de repo waar deze workflow draait. Zonder sleutel schrijft de Meter alleen dat ze
ontbreekt.
"""

from __future__ import annotations

import os

import requests

from pipeline.common import DATA, log, nu

API = "https://api.brevo.com/v3"
PAD = DATA / "verspreiding" / "cijfers.md"


def brevo(pad: str, **params) -> dict:
    r = requests.get(f"{API}{pad}", params=params, timeout=30,
                     headers={"api-key": os.environ["BREVO_API_KEY"], "accept": "application/json"})
    r.raise_for_status()
    return r.json()


def procent(deel: int, geheel: int) -> str:
    return f"{100 * deel / geheel:.0f} %" if geheel else "–"


def waarom(fout: requests.HTTPError) -> str:
    r = fout.response
    try:
        uitleg = str(r.json().get("message", ""))[:200]
    except ValueError:
        uitleg = r.text[:200]
    return f"HTTP {r.status_code} op {r.request.path_url.split('?')[0]}" + (f": {uitleg}" if uitleg else "")


def meting() -> str:
    kop = f"## Meter, {nu():%Y-%m-%d}"
    if not os.environ.get("BREVO_API_KEY"):
        return f"{kop}\n\n- BREVO_API_KEY ontbreekt in de secrets van deze repo; geen cijfers van Brevo.\n"
    regels = [kop, ""]
    try:
        lijsten = brevo("/contacts/lists", limit=50, offset=0).get("lists", [])
        regels += ["| Lijst | Inschrijvingen | Uitgeschreven of geblokkeerd |", "| --- | --- | --- |"]
        for lijst in sorted(lijsten, key=lambda l: l["id"]):
            regels.append(f"| {lijst['name']} (#{lijst['id']}) | {lijst.get('uniqueSubscribers', lijst.get('totalSubscribers', 0))} | {lijst.get('totalBlacklisted', 0)} |")
    except requests.HTTPError as fout:
        regels += [f"- Lijsten niet opgehaald ({waarom(fout)})."]
    try:
        campagnes = brevo("/emailCampaigns", type="classic", status="sent", limit=5, offset=0, sort="desc",
                          statistics="globalStats", excludeHtmlContent="true").get("campaigns", [])
        if campagnes:
            regels += ["", "| Campagne | Verstuurd op | Afgeleverd | Geopend | Geklikt |", "| --- | --- | --- | --- | --- |"]
            for c in campagnes:
                s = (c.get("statistics") or {}).get("globalStats") or {}
                af = int(s.get("delivered", 0))
                regels.append(f"| {c.get('name', '')} | {str(c.get('sentDate', ''))[:10]} | {af} | "
                              f"{procent(int(s.get('uniqueViews', 0)), af)} | {procent(int(s.get('uniqueClicks', 0)), af)} |")
    except requests.HTTPError as fout:
        regels += ["", f"- Campagnes niet opgehaald ({waarom(fout)})."]
    regels += ["", "Bezoeken en verwijzers: Vercel Web Analytics (dashboard, met de hand). Bron van de tabellen: Brevo-API, opgehaald door de Meter."]
    return "\n".join(regels) + "\n"


def main() -> None:
    blok = meting()
    PAD.parent.mkdir(parents=True, exist_ok=True)
    tekst = PAD.read_text(encoding="utf-8") if PAD.exists() else "# Cijfers verspreiding\n"
    kop = blok.splitlines()[0]
    if kop in tekst:  # vandaag al gemeten: vervang die meting
        voor, _, na = tekst.partition(kop)
        rest = na.split("\n## ", 1)
        tekst = voor.rstrip() + "\n\n" + blok + ("\n## " + rest[1] if len(rest) > 1 else "")
    else:
        tekst = tekst.rstrip() + "\n\n" + blok
    PAD.write_text(tekst, encoding="utf-8")
    log(f"Meting geschreven in {PAD.relative_to(DATA.parent)}")


if __name__ == "__main__":
    main()
