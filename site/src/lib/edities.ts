// Leest de edities uit content/edities (gemaakt door de pijplijn) en zet ze om
// naar onderdelen die de site kan tonen. Alleen edities met `status: klaar`
// én een ingevulde "Mijn inschatting" worden gepubliceerd.

import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { marked } from "marked";

marked.setOptions({ gfm: true });

const MAP = path.resolve(process.cwd(), process.env.EDITIES_MAP ?? "../content/edities");
const TOON_CONCEPTEN = process.env.TOON_CONCEPTEN === "1";

export const HYPE_STANDEN = [
  "Sterk overroepen",
  "Overroepen",
  "Terecht",
  "Onderschat",
  "Sterk onderschat",
] as const;

export type Hype = { stand: string; index: number; uitleg: string };

export type Onderwerp = {
  slug: string;
  titel: string;
  labels: string[];
  hype: Hype | null;
  html: string;
};

export type Editie = {
  week: string; // bv. 2026-w44
  bestand: string; // pad in de repo, bv. content/edities/2026-w44-stand-van-ai.md
  titel: string;
  datum: string;
  labels: string[];
  status: string;
  kern: string; // "De week in één alinea", als HTML
  kernTekst: string; // idem, platte tekst (voor RSS en beschrijving)
  onderwerpen: Onderwerp[];
  ruis: string;
  woord: string;
  inschatting: string;
  gemaakt: string;
  bronnen: string;
  lezersvraag: string;
  lezersvraagTitel: string;
};

const VASTE_SECTIES = {
  lezersvraag: "Lezersvraag",
  kern: "De week in één alinea",
  ruis: "Ruis van de week",
  woord: "Woord van de week",
  inschatting: "Mijn inschatting",
  gemaakt: "Zo is dit gemaakt",
  bronnen: "Bronnen",
};

export function slugify(tekst: string): string {
  return tekst
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "")
    .slice(0, 60);
}

export function leesHype(regel: string): Hype | null {
  // "Terecht — omdat ..." of "Sterk overroepen - omdat ..."
  const [standRuw, ...rest] = regel.split(/\s[—–-]\s/);
  // "Terecht (voorlopig)" of "Terecht." telt ook als "Terecht"
  const stand = standRuw.trim().replace(/\s*\(.*\)\s*$/, "").replace(/\.$/, "");
  const index = HYPE_STANDEN.findIndex((s) => s.toLowerCase() === stand.toLowerCase());
  if (index === -1) return null;
  const uitleg = rest.join(" — ").trim();
  return { stand: HYPE_STANDEN[index], index, uitleg: uitleg.charAt(0).toUpperCase() + uitleg.slice(1) };
}

export function splitsSecties(md: string): { titel: string; body: string }[] {
  const delen = md.split(/^## /m);
  return delen.slice(1).map((deel) => {
    const [kop, ...rest] = deel.split("\n");
    return { titel: kop.trim(), body: rest.join("\n").trim() };
  });
}

export function haalRegel(body: string, label: string): [string | null, string] {
  const re = new RegExp(`^\\*\\*${label}:\\*\\*\\s*(.+)$`, "mi");
  const m = body.match(re);
  if (!m) return [null, body];
  return [m[1].trim(), body.replace(m[0], "").trim()];
}

export const html = (md: string) => marked.parse(md, { async: false }) as string;
export const platteTekst = (md: string) =>
  md.replace(/\[([^\]]+)\]\([^)]+\)/g, "$1").replace(/[*_`#>]/g, "").replace(/\s+/g, " ").trim();

function isGepubliceerd(status: string, inschatting: string): boolean {
  if (TOON_CONCEPTEN) return true;
  const ingevuld = inschatting.replace(/<!--[\s\S]*?-->/g, "").trim().length > 0;
  return status === "klaar" && ingevuld;
}

function leesEditie(bestand: string): Editie | null {
  const bron = fs.readFileSync(path.join(MAP, bestand), "utf-8");
  const { data, content } = matter(bron);
  const secties = splitsSecties(content);
  const vind = (naam: string) => secties.find((s) => s.titel === naam)?.body ?? "";

  const inschattingMd = vind(VASTE_SECTIES.inschatting);
  const status = String(data.status ?? "concept");
  if (!isGepubliceerd(status, inschattingMd)) return null;

  const vast = new Set(Object.values(VASTE_SECTIES));
  const onderwerpen: Onderwerp[] = secties
    .filter((s) => !vast.has(s.titel))
    .map((s) => {
      let [labelsRuw, body] = haalRegel(s.body, "Labels");
      let hypeRuw: string | null;
      [hypeRuw, body] = haalRegel(body, "Hype-meter");
      return {
        slug: slugify(s.titel),
        titel: s.titel,
        labels: labelsRuw ? labelsRuw.split(",").map((l) => l.trim()).filter(Boolean) : [],
        hype: hypeRuw ? leesHype(hypeRuw) : null,
        html: html(body),
      };
    });

  const kernMd = vind(VASTE_SECTIES.kern);
  return {
    week: String(data.week ?? bestand.replace(/-stand-van-ai\.md$/, "")),
    bestand: `content/edities/${bestand}`,
    titel: String(data.titel ?? "Stand van AI"),
    datum: data.datum instanceof Date ? data.datum.toISOString().slice(0, 10) : String(data.datum ?? ""),
    labels: Array.isArray(data.labels) ? data.labels : [],
    status,
    kern: html(kernMd),
    kernTekst: platteTekst(kernMd),
    onderwerpen,
    ruis: html(vind(VASTE_SECTIES.ruis)),
    woord: html(vind(VASTE_SECTIES.woord)),
    inschatting: html(inschattingMd.replace(/<!--[\s\S]*?-->/g, "")),
    gemaakt: html(vind(VASTE_SECTIES.gemaakt)),
    bronnen: html(vind(VASTE_SECTIES.bronnen)),
    lezersvraag: html(vind(VASTE_SECTIES.lezersvraag)),
    lezersvraagTitel: (vind(VASTE_SECTIES.lezersvraag).match(/^\*\*(.+?)\*\*/) ?? [])[1] ?? "",
  };
}

let cache: Editie[] | null = null;

export function alleEdities(): Editie[] {
  if (cache) return cache;
  if (!fs.existsSync(MAP)) return (cache = []);
  cache = fs
    .readdirSync(MAP)
    .filter((f) => f.endsWith(".md"))
    .map(leesEditie)
    .filter((e): e is Editie => e !== null)
    .sort((a, b) => b.week.localeCompare(a.week));
  return cache;
}

export function weekNummer(week: string): string {
  const m = week.match(/^(\d{4})-w(\d{2})$/);
  return m ? `week ${Number(m[2])}, ${m[1]}` : week;
}

export function datumLeesbaar(iso: string): string {
  if (!iso) return "";
  return new Date(iso + "T12:00:00").toLocaleDateString("nl-BE", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}
