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


def meting() -> str:
    kop = f"## Meter, {nu():%Y-%m-%d}"
    if not os.environ.get("BREVO_API_KEY"):
        return f"{kop}\n\n- BREVO_API_KEY ontbreekt in de secrets van deze repo; geen cijfers van Brevo.\n"
    regels = [kop, "", "| Lijst | Inschrijvingen | Uitgeschreven of geblokkeerd |", "| --- | --- | --- |"]
    for lijst in sorted(brevo("/contacts/lists", limit=50).get("lists", []), key=lambda l: l["id"]):
        regels.append(f"| {lijst['name']} (#{lijst['id']}) | {lijst.get('uniqueSubscribers', lijst.get('totalSubscribers', 0))} | {lijst.get('totalBlacklisted', 0)} |")
    campagnes = brevo("/emailCampaigns", status="sent", limit=5, sort="desc", statistics="globalStats").get("campaigns", [])
    if campagnes:
        regels += ["", "| Campagne | Verstuurd op | Afgeleverd | Geopend | Geklikt |", "| --- | --- | --- | --- | --- |"]
        for c in campagnes:
            s = (c.get("statistics") or {}).get("globalStats") or {}
            af = int(s.get("delivered", 0))
            regels.append(f"| {c.get('name', '')} | {str(c.get('sentDate', ''))[:10]} | {af} | "
                          f"{procent(int(s.get('uniqueViews', 0)), af)} | {procent(int(s.get('uniqueClicks', 0)), af)} |")
    regels += ["", "Bezoeken en verwijzers: Vercel Web Analytics (dashboard, met de hand). Bron van de tabellen: Brevo-API, opgehaald door de Meter."]
    return "\n".join(regels) + "\n"


def main() -> None:
    try:
        blok = meting()
    except requests.HTTPError as fout:  # schrijf de reden op in plaats van stil te falen (bevat geen sleutel)
        r = fout.response
        uitleg = ""
        try:
            uitleg = str(r.json().get("message", ""))[:300]
        except ValueError:
            uitleg = r.text[:300]
        blok = f"## Meter, {nu():%Y-%m-%d}\n\n- Brevo weigerde de vraag (HTTP {r.status_code}): {uitleg}\n"
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
