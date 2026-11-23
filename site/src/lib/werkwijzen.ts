// Werkwijzen: prompts, skills en agents (content/werkwijzen/). Zie content/werkwijzen/README.md.
import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { html } from "./edities";
import { personalisatiePrompt } from "./materiaal";

const MAP = path.resolve(process.cwd(), "..", "content", "werkwijzen");

export type Soort = "prompt" | "skill" | "agent";
export const SOORT_NAAM: Record<Soort, string> = { prompt: "Prompt", skill: "Skill", agent: "Assistent of agent" };

export type Werkwijze = {
  slug: string;
  titel: string;
  soort: Soort;
  samenvatting: string;
  voor: string[];
  niveau: string;
  versie: string;
  bijgewerkt: string;
  getest: string;
  licentie: string;
  status: "beschikbaar" | "in-voorbereiding";
  html: string;
  bestanden: { naam: string; inhoud: Buffer }[]; // voor skills en agents: de map naast het .md-bestand
};

const datum = (d: unknown) => (d instanceof Date ? d.toISOString().slice(0, 10) : String(d ?? ""));

function leesMap(map: string, basis = ""): { naam: string; inhoud: Buffer }[] {
  if (!fs.existsSync(map)) return [];
  return fs.readdirSync(map, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory()
      ? leesMap(path.join(map, e.name), path.join(basis, e.name))
      : [{ naam: path.join(basis, e.name), inhoud: fs.readFileSync(path.join(map, e.name)) }],
  );
}

let cache: Werkwijze[] | null = null;

export function alleWerkwijzen(): Werkwijze[] {
  if (cache) return cache;
  if (!fs.existsSync(MAP)) return (cache = []);
  cache = fs
    .readdirSync(MAP)
    .filter((f) => f.endsWith(".md") && f !== "README.md")
    .map((f) => {
      const slug = f.replace(/\.md$/, "");
      const { data, content } = matter(fs.readFileSync(path.join(MAP, f), "utf-8"));
      const md = content.replace("PERSONALISATIEPROMPT", personalisatiePrompt());
      const soort = (["prompt", "skill", "agent"].includes(data.soort) ? data.soort : "prompt") as Soort;
      return {
        slug,
        titel: String(data.titel ?? slug),
        soort,
        samenvatting: String(data.samenvatting ?? ""),
        voor: Array.isArray(data.voor) ? data.voor : [],
        niveau: String(data.niveau ?? ""),
        versie: String(data.versie ?? "1.0"),
        bijgewerkt: datum(data.bijgewerkt),
        getest: String(data.getest ?? "Nog niet getest."),
        licentie: String(data.licentie ?? "CC BY 4.0"),
        status: data.status === "in-voorbereiding" ? "in-voorbereiding" : "beschikbaar",
        html: html(md),
        bestanden: soort === "prompt" ? [] : leesMap(path.join(MAP, slug)),
      } as Werkwijze;
    })
    .sort((a, b) => a.titel.localeCompare(b.titel, "nl"));
  return cache;
}

export const beschikbareWerkwijzen = () => alleWerkwijzen().filter((w) => w.status === "beschikbaar");
