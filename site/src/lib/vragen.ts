// Vragenbank (bouwplan B02): echte vragen over AI, elk met een nagekeken antwoord en een eigen pagina.
// Bron: content/vragen/<slug>.md. Alleen status "gecontroleerd" komt op de site.
import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { marked } from "marked";
import { DOELGROEPEN } from "./doelgroepen";

// De acht dwarsvragen uit het doelgroepenonderzoek (data/doelgroepenonderzoek.md).
export const DWARSVRAGEN: Record<number, { titel: string; kort: string }> = {
  1: { titel: "Wat mag ik erin plakken?", kort: "Privacy en gegevens" },
  2: { titel: "Is dit echt?", kort: "Nepbeelden en oplichting" },
  3: { titel: "Welke afspraken maken we?", kort: "Afspraken" },
  4: { titel: "Hoe leer ik het zonder tijd of expertise?", kort: "Leren en lesgeven" },
  5: { titel: "Denk ik nog zelf?", kort: "Zelf denken" },
  6: { titel: "Wat heb ik eraan?", kort: "Nut" },
  7: { titel: "Wat zegt de wet, en wie houdt toezicht?", kort: "Wet en toezicht" },
  8: { titel: "Wat met mijn job?", kort: "Werk en jobs" },
};

export type Link = { tekst: string; href: string };
export type Bron = { naam: string; url: string };
export type Vraag = {
  slug: string;
  vraag: string;
  kort: string;
  doelgroepen: string[];
  doelgroepSlugs: string[];
  dwarsvraag: number;
  niveau: string;
  verder: Link[];
  bronnen: Bron[];
  nagekeken: string;
  versie: string;
  getest: string;
  html: string;
  tekst: string;
};

const datum = (d: unknown) => (d instanceof Date ? d.toISOString().slice(0, 10) : String(d ?? ""));
let cache: Vraag[] | null = null;

export function alleVragen(): Vraag[] {
  if (cache) return cache;
  const map = path.resolve(process.cwd(), "../content/vragen");
  if (!fs.existsSync(map)) return (cache = []);
  cache = fs
    .readdirSync(map)
    .filter((f) => f.endsWith(".md") && f !== "README.md")
    .map((f) => {
      const slug = f.replace(/\.md$/, "");
      const { data, content } = matter(fs.readFileSync(path.join(map, f), "utf-8"));
      if (String(data.status) !== "gecontroleerd") return null;
      const dv = Number(data.dwarsvraag);
      if (!DWARSVRAGEN[dv]) throw new Error(`vragen/${f}: onbekende dwarsvraag ${data.dwarsvraag}`);
      const doelgroepen = (data.doelgroepen ?? []) as string[];
      const doelgroepSlugs = doelgroepen.map((d) => {
        const g = DOELGROEPEN.find((x) => x.label.toLowerCase() === d.toLowerCase());
        if (!g) throw new Error(`vragen/${f}: onbekende doelgroep "${d}"`);
        return g.slug;
      });
      return {
        slug,
        vraag: String(data.vraag),
        kort: String(data.kort).trim(),
        doelgroepen,
        doelgroepSlugs,
        dwarsvraag: dv,
        niveau: String(data.niveau ?? ""),
        verder: (data.verder ?? []) as Link[],
        bronnen: (data.bronnen ?? []) as Bron[],
        nagekeken: datum(data.nagekeken),
        versie: String(data.versie ?? "1.0"),
        getest: String(data.getest ?? ""),
        html: marked.parse(content, { async: false, gfm: true }) as string,
        tekst: content.replace(/[#>*_`|-]/g, " ").replace(/\s+/g, " ").trim(),
      } as Vraag;
    })
    .filter((v): v is Vraag => v !== null)
    .sort((a, b) => a.dwarsvraag - b.dwarsvraag || a.vraag.localeCompare(b.vraag, "nl"));
  return cache;
}

export function vragenVoor(doelgroepSlug: string): Vraag[] {
  return alleVragen().filter((v) => v.doelgroepSlugs.includes(doelgroepSlug));
}
