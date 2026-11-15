import fs from "node:fs";
import path from "node:path";

export type Term = { term: string; uitleg_leek: string; voorbeeld?: string; verdieping?: string; slug: string };

export const slugify = (t: string) =>
  t.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");

let cache: Term[] | null = null;

export function alleTermen(): Term[] {
  if (cache) return cache;
  const pad = path.resolve(process.cwd(), "../content/jargon.json");
  const ruw: Omit<Term, "slug">[] = fs.existsSync(pad) ? JSON.parse(fs.readFileSync(pad, "utf-8")) : [];
  const gezien = new Set<string>();
  cache = ruw
    .map((t) => ({ ...t, slug: slugify(t.term) }))
    .filter((t) => t.slug && !gezien.has(t.slug) && gezien.add(t.slug))
    .sort((a, b) => a.term.localeCompare(b.term, "nl"));
  return cache;
}
