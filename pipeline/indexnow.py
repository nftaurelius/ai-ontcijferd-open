"""IndexNow: meldt nieuwe pagina's aan Bing (en Yandex, Seznam, Naver) zonder login.

Leest de sitemap van de live site, vergelijkt met wat al gemeld is (data/indexnow-gemeld.txt) en meldt
nieuwe adressen plus een paar pagina's die vaak veranderen. Eerste run: alles. Sleutel: site/public/<sleutel>.txt.
"""
import pathlib, sys, time, xml.etree.ElementTree as ET
import requests

SITE = "https://aiontcijferd.be"
SLEUTEL = "6d0167db741635bd458d6d7c76f094ca"
GEMELD = pathlib.Path("data/indexnow-gemeld.txt")
ALTIJD = [f"{SITE}/", f"{SITE}/edities/", f"{SITE}/plus/", f"{SITE}/materiaal/", f"{SITE}/ai-act/"]  # zoals in de sitemap
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def haal(url: str) -> str:
    r = requests.get(url, timeout=30, headers={"User-Agent": "ai-ontcijferd-indexnow"})
    r.raise_for_status()
    return r.text


def sitemap_urls() -> list[str]:
    urls = []
    index = ET.fromstring(haal(f"{SITE}/sitemap-index.xml"))
    for loc in index.findall("s:sitemap/s:loc", NS):
        deel = ET.fromstring(haal(loc.text.strip()))
        urls += [u.text.strip() for u in deel.findall("s:url/s:loc", NS)]
    return urls


def wacht_op_sleutel() -> None:
    # Vercel bouwt na een push nog even: wacht tot de sleutel live staat (max. 10 minuten).
    for _ in range(20):
        try:
            if haal(f"{SITE}/{SLEUTEL}.txt").strip() == SLEUTEL:
                return
        except requests.RequestException:
            pass
        time.sleep(30)
    sys.exit("Sleutelbestand niet bereikbaar; niets gemeld.")


def main() -> None:
    wacht_op_sleutel()
    if "--wacht" in sys.argv:
        time.sleep(240)  # na een push: laat Vercel de nieuwe pagina's eerst uitrollen
    alle = sitemap_urls()
    gemeld = set(GEMELD.read_text().split()) if GEMELD.exists() else set()
    nieuw = [u for u in alle if u not in gemeld]
    melden = sorted(set(nieuw) | (set(ALTIJD) if gemeld else set()))
    if not melden:
        print("Niets nieuws.")
        return
    r = requests.post("https://api.indexnow.org/indexnow", timeout=60, json={
        "host": "aiontcijferd.be", "key": SLEUTEL, "keyLocation": f"{SITE}/{SLEUTEL}.txt", "urlList": melden[:10000]})
    print(f"IndexNow: {len(melden)} adressen gemeld, antwoord {r.status_code} {r.text[:200]}")
    if r.status_code not in (200, 202):
        sys.exit(1)
    GEMELD.write_text("\n".join(sorted(gemeld | set(alle))) + "\n")


if __name__ == "__main__":
    main()
