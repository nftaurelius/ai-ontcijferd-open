// De AI-cursus online. De bron staat in content/cursus/src (tekstbestanden van Duncan);
// content/cursus/bouw/web.py zet ze om in JSON (content/cursus/web), build.py maakt de PDF's
// in content/materiaal/ai-cursus/bestanden. Na een wijziging in de bron: beide scripts draaien.
import fs from "node:fs";
import path from "node:path";

export type Hoofdstuk = { id: string; nr: number | null; kicker: string; titel: string; onder: string; html: string };
export type CursusDeel = {
  id: string; nr: number; groep: string; bestand: string; pdf: string; kicker: string; titel: string;
  ondertitel: string; tagline: string; versie: string; korteTitel: string; regel: string; intro: string;
  hoofdstukken: Hoofdstuk[];
};

const MAP = path.resolve(process.cwd(), "../content/cursus/web");
let cache: CursusDeel[] | null = null;

export function cursusDelen(): CursusDeel[] {
  if (cache) return cache;
  cache = fs.readdirSync(MAP)
    .filter((f) => /^\d\d-.+\.json$/.test(f))
    .sort()
    .map((f) => JSON.parse(fs.readFileSync(path.join(MAP, f), "utf-8")) as CursusDeel);
  return cache;
}

export const GROEP_UITLEG: Record<string, string> = {
  "Start": "Lees dit eerst.",
  "De ladder — lees deze in volgorde": "Vier delen die klimmen. Begin bij Deel 1.",
  "De modules — kies op behoefte": "Tien modules om te verbreden, in geen vaste volgorde.",
  "Naslag — hou erbij, print wat je nodig hebt": "De toolgids, de veiligheidskaart en een werkblad.",
};

export const groepNaam = (g: string) => g.split(" — ")[0];
export const VOLLEDIG_PDF = "/materiaal/ai-cursus/bestanden/AI-Cursus-volledig.pdf";
