// Gratis tools op de site. Elke tool is één zelfstandig HTML-bestand in public/<slug>/app/
// met een eigen configuratieblok (<script type="application/json" id="ao-config">).
// De site leest dat blok bij het bouwen, zodat versie en "bijgewerkt op" maar op één plek staan.
import fs from "node:fs";
import path from "node:path";

export type Tool = {
  slug: string;
  naam: string;
  korteNaam: string;
  knop: string;
  vraag: string;
  uitleg: string;
  voor: string[];
  versie: string;
  bijgewerkt: string;
  teControleren: number;
  totaalGegevens: number;
  nagekekenOp: string | null;
};

type Basis = Omit<Tool, "versie" | "bijgewerkt" | "teControleren" | "totaalGegevens" | "nagekekenOp">;

const TOOLS: Basis[] = [
  {
    slug: "plakcheck",
    naam: "Plakcheck en Urenrekening",
    korteNaam: "Plakcheck",
    knop: "Doe de Plakcheck",
    vraag: "Mag dit in een chatbot? En loont het dan nog?",
    uitleg:
      "Vier vragen zeggen of je gegevens in een AI-tool horen. Daarna reken je na of het je nog tijd en geld oplevert als je het veilig doet. Alles draait in je browser.",
    voor: ["Werk", "Lokale overheden", "Zelfstandigen", "Onderwijs", "Bibliotheken", "Burgers"],
  },
  {
    slug: "afsprakenkaart",
    naam: "Afsprakenkaart",
    korteNaam: "Afsprakenkaart",
    knop: "Maak je afsprakenkaart",
    vraag: "Welke afspraken over AI maken we?",
    uitleg:
      "Kies klas, werk, gemeente, vereniging of thuis, loop acht vragen door en druk één pagina met jullie afspraken af. Alles draait in je browser.",
    voor: ["Onderwijs", "Werk", "Lokale overheden", "Zelfstandigen", "Bibliotheken", "Burgers"],
  },
];

export function leesConfig(slug: string): Record<string, any> | null {
  const bestand = path.resolve(process.cwd(), "public", slug, "app", "index.html");
  if (!fs.existsSync(bestand)) return null;
  const html = fs.readFileSync(bestand, "utf-8");
  const m = /<script type="application\/json" id="ao-config">([\s\S]*?)<\/script>/.exec(html);
  if (!m) return null;
  try {
    return JSON.parse(m[1]);
  } catch {
    return null;
  }
}

let cache: Tool[] | null = null;

export function alleTools(): Tool[] {
  if (cache) return cache;
  cache = TOOLS.map((t) => {
    const cfg = leesConfig(t.slug);
    const items = cfg ? [...(cfg.prijzen ?? []), ...(cfg.aanbieders ?? []), ...(cfg.feiten ?? []), ...(cfg.wisselkoers ? [cfg.wisselkoers] : [])] : [];
    return {
      ...t,
      versie: String(cfg?.meta?.versie ?? ""),
      bijgewerkt: String(cfg?.meta?.configBijgewerktOp ?? ""),
      teControleren: items.filter((i: any) => i.status === "TE CONTROLEREN").length,
      totaalGegevens: items.length,
      nagekekenOp: cfg?.redactie?.nagekekenDoorEindredacteurOp ?? null,
    };
  });
  return cache;
}

export function tool(slug: string): Tool {
  const t = alleTools().find((x) => x.slug === slug);
  if (!t) throw new Error(`Onbekende tool: ${slug}`);
  return t;
}
