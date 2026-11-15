// AI Ontcijferd Plus: dagbrieven (content/plus/dag) en dossiers (content/plus/dossiers).
// Een dagbrief verschijnt met `status: klaar` (de pijplijn zet dat; samenvoegen van de PR is de
// goedkeuring). Een dossier verschijnt pas met `status: klaar` én een ingevulde "Mijn inschatting".

import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { haalRegel, html, leesHype, platteTekst, slugify, splitsSecties, type Hype } from "./edities";

const MAP = path.resolve(process.cwd(), process.env.PLUS_MAP ?? "../content/plus");
const TOON_CONCEPTEN = process.env.TOON_CONCEPTEN === "1";

export const STATUSSEN = ["Bevestigd", "Volgens de maker", "Eén bron"] as const;

export type PlusItem = { slug: string; titel: string; labels: string[]; status: string; html: string };

export type Dagbrief = {
  datum: string;
  titel: string;
  labels: string[];
  kort: string;
  kortTekst: string;
  items: PlusItem[];
  proberen: string;
  radar: string;
  oordeel: string; // optioneel: "## Kort oordeel" van Duncan
  gemaakt: string;
  bronnen: string;
};

export type Dossier = {
  slug: string;
  titel: string;
  datum: string;
  labels: string[];
  samenvatting: string;
  kort: string;
  hype: Hype | null;
  secties: { slug: string; titel: string; html: string }[];
  inschatting: string;
  gemaakt: string;
  bronnen: string;
};

const datumTekst = (d: unknown) => (d instanceof Date ? d.toISOString().slice(0, 10) : String(d ?? ""));
const zonderCommentaar = (md: string) => md.replace(/<!--[\s\S]*?-->/g, "").trim();

function lees(sub: string) {
  const map = path.join(MAP, sub);
  if (!fs.existsSync(map)) return [];
  return fs
    .readdirSync(map)
    .filter((f) => f.endsWith(".md"))
    .map((f) => ({ bestand: f, ...matter(fs.readFileSync(path.join(map, f), "utf-8")) }));
}

let dagCache: Dagbrief[] | null = null;

export function alleDagbrieven(): Dagbrief[] {
  if (dagCache) return dagCache;
  const vast = ["Vandaag in het kort", "Om te proberen", "Uit de radar", "Kort oordeel", "Zo is dit gemaakt", "Bronnen"];
  dagCache = lees("dag")
    .filter(({ data }) => TOON_CONCEPTEN || data.status === "klaar")
    .map(({ bestand, data, content }) => {
      // NAKIJKEN-notities voor de eindredactie horen niet in de gepubliceerde pagina, ook niet in de broncode
      const secties = splitsSecties(zonderCommentaar(content));
      const vind = (naam: string) => secties.find((s) => s.titel === naam)?.body ?? "";
      const items = secties
        .filter((s) => !vast.includes(s.titel))
        .map((s) => {
          let [labelsRuw, body] = haalRegel(s.body, "Labels");
          let statusRuw: string | null;
          [statusRuw, body] = haalRegel(body, "Status");
          return {
            slug: slugify(s.titel),
            titel: s.titel,
            labels: labelsRuw ? labelsRuw.split(",").map((l) => l.trim()).filter(Boolean) : [],
            status: statusRuw ?? "",
            html: html(body),
          };
        });
      const kortMd = vind("Vandaag in het kort");
      return {
        datum: datumTekst(data.datum) || bestand.replace(/\.md$/, ""),
        titel: String(data.titel ?? "Plus"),
        labels: Array.isArray(data.labels) ? data.labels : [],
        kort: html(kortMd),
        kortTekst: platteTekst(kortMd),
        items,
        proberen: html(vind("Om te proberen")),
        radar: html(vind("Uit de radar")),
        oordeel: html(zonderCommentaar(vind("Kort oordeel"))),
        gemaakt: html(vind("Zo is dit gemaakt")),
        bronnen: html(vind("Bronnen")),
      };
    })
    .sort((a, b) => b.datum.localeCompare(a.datum));
  return dagCache;
}

let dossierCache: Dossier[] | null = null;

export function alleDossiers(): Dossier[] {
  if (dossierCache) return dossierCache;
  const vast = ["In het kort", "Mijn inschatting", "Zo is dit gemaakt", "Bronnen"];
  dossierCache = lees("dossiers")
    .map(({ bestand, data, content }) => {
      const secties = splitsSecties(content);
      const vind = (naam: string) => secties.find((s) => s.titel === naam)?.body ?? "";
      const inschattingMd = zonderCommentaar(vind("Mijn inschatting"));
      if (!TOON_CONCEPTEN && !(data.status === "klaar" && inschattingMd.length > 0)) return null;
      const [hypeRuw, kortMd] = haalRegel(vind("In het kort"), "Hype-meter");
      return {
        slug: bestand.replace(/\.md$/, ""),
        titel: String(data.titel ?? bestand),
        datum: datumTekst(data.datum),
        labels: Array.isArray(data.labels) ? data.labels : [],
        samenvatting: String(data.samenvatting ?? "") || platteTekst(kortMd).slice(0, 200),
        kort: html(zonderCommentaar(kortMd)),
        hype: hypeRuw ? leesHype(hypeRuw) : null,
        secties: secties
          .filter((s) => !vast.includes(s.titel))
          .map((s) => ({ slug: slugify(s.titel), titel: s.titel, html: html(zonderCommentaar(s.body)) })),
        inschatting: html(inschattingMd),
        gemaakt: html(vind("Zo is dit gemaakt")),
        bronnen: html(vind("Bronnen")),
      };
    })
    .filter((d): d is Dossier => d !== null)
    .sort((a, b) => b.datum.localeCompare(a.datum));
  return dossierCache;
}

/** Plus-onderwerpen voor één doelgroep, nieuwste eerst (voor /voor/<doelgroep> en de RSS). */
export function plusVoor(label: string): { dag: Dagbrief; item: PlusItem }[] {
  const uit: { dag: Dagbrief; item: PlusItem }[] = [];
  for (const dag of alleDagbrieven()) {
    for (const item of dag.items) {
      if (item.labels.some((l) => l.toLowerCase() === label.toLowerCase())) uit.push({ dag, item });
    }
  }
  return uit;
}
