import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { marked } from "marked";

export type Bron = { naam: string; url: string };
// Bijsluitervelden (huisstijl 1.0) zijn optioneel: oudere fiches hebben alleen voor en bijgewerkt.
export type Fiche = {
  slug: string;
  titel: string;
  samenvatting: string;
  voor: string[];
  bijgewerkt: string;
  niveau: string;
  duur: string;
  versie: string;
  nagekeken: string;
  getest: string;
  bronnen: Bron[];
  html: string;
};

const datum = (d: unknown) => (d instanceof Date ? d.toISOString().slice(0, 10) : String(d ?? ""));

let cache: Fiche[] | null = null;

export function alleFiches(): Fiche[] {
  if (cache) return cache;
  const map = path.resolve(process.cwd(), "../content/fiches");
  if (!fs.existsSync(map)) return (cache = []);
  cache = fs
    .readdirSync(map)
    .filter((f) => f.endsWith(".md"))
    .map((f) => {
      const { data, content } = matter(fs.readFileSync(path.join(map, f), "utf-8"));
      const bijgewerkt = datum(data.bijgewerkt);
      return {
        slug: f.replace(/\.md$/, ""),
        titel: String(data.titel ?? f),
        samenvatting: String(data.samenvatting ?? ""),
        voor: Array.isArray(data.voor) ? data.voor : [],
        bijgewerkt,
        niveau: String(data.niveau ?? ""),
        duur: String(data.duur ?? ""),
        versie: String(data.versie ?? ""),
        nagekeken: data.nagekeken ? datum(data.nagekeken) : "",
        getest: String(data.getest ?? ""),
        bronnen: Array.isArray(data.bronnen)
          ? data.bronnen.filter((b: any) => b?.naam && b?.url).map((b: any) => ({ naam: String(b.naam), url: String(b.url) }))
          : [],
        // checkboxes uit markdown worden gewone, aanvinkbare vakjes
        html: (marked.parse(content, { async: false, gfm: true }) as string).replace(/disabled=""\s*/g, ""),
      };
    })
    .sort((a, b) => a.titel.localeCompare(b.titel, "nl"));
  return cache;
}
