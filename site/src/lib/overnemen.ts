// Kant-en-klare tekst om een stuk van AI Ontcijferd over te nemen (CC BY 4.0).
// Geen model nodig: de tekst komt rechtstreeks uit de editie of het dossier, met naamsvermelding.
import type { Editie } from "./edities";
import { weekNummer } from "./edities";
import type { Dossier } from "./plus";
import { SITE_URL } from "./seo";
import { inkorten } from "./tekst";

export type Overneemblok = { kort: string; lang: string; url: string };

export const NAAMSVERMELDING = "Bron: AI Ontcijferd (aiontcijferd.be), door Duncan Panis. Vrij over te nemen onder CC BY 4.0.";

export function overneemEditie(e: Editie): Overneemblok {
  const url = `${SITE_URL}/edities/${e.week}`;
  const onderwerpen = e.onderwerpen.map((o) => `- ${o.titel}${o.hype ? ` (hype-meter: ${o.hype.stand.toLowerCase()})` : ""}`);
  const kort = `${e.titel}: ${inkorten(e.kernTekst, 200)} Lees meer op ${url}`;
  const lang = [
    /week/i.test(e.titel) ? e.titel : `${e.titel} (${weekNummer(e.week)})`,
    "",
    inkorten(e.kernTekst, 600),
    "",
    onderwerpen.length ? "Deze week:" : "",
    ...onderwerpen,
    "",
    `Lees de volledige analyse, met bronnen: ${url}`,
    "",
    NAAMSVERMELDING,
  ]
    .join("\n")
    .replace(/\n{3,}/g, "\n\n");
  return { kort, lang, url };
}

/** HTML naar platte tekst, voor de korte inleiding van een dossier. */
function zonderHtml(html: string): string {
  return html
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&")
    .replace(/\s+/g, " ")
    .trim();
}

export function overneemDossier(d: Dossier): Overneemblok {
  const url = `${SITE_URL}/plus/dossiers/${d.slug}`;
  const kort = `${d.titel}. ${inkorten(d.samenvatting, 200)} Lees meer op ${url}`;
  const lang = [
    d.titel,
    "",
    inkorten(zonderHtml(d.kort) || d.samenvatting, 700),
    "",
    `Lees het volledige dossier, met bronnen: ${url}`,
    "",
    NAAMSVERMELDING,
  ].join("\n");
  return { kort, lang, url };
}
