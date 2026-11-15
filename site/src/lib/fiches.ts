import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { marked } from "marked";

export type Fiche = { slug: string; titel: string; samenvatting: string; voor: string[]; bijgewerkt: string; html: string };

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
      const bijgewerkt = data.bijgewerkt instanceof Date ? data.bijgewerkt.toISOString().slice(0, 10) : String(data.bijgewerkt ?? "");
      return {
        slug: f.replace(/\.md$/, ""),
        titel: String(data.titel ?? f),
        samenvatting: String(data.samenvatting ?? ""),
        voor: Array.isArray(data.voor) ? data.voor : [],
        bijgewerkt,
        // checkboxes uit markdown worden gewone, aanvinkbare vakjes
        html: (marked.parse(content, { async: false, gfm: true }) as string).replace(/disabled=""\s*/g, ""),
      };
    })
    .sort((a, b) => a.titel.localeCompare(b.titel, "nl"));
  return cache;
}
