// Open lesmateriaal: cursus, lespakketten en lezingen onder Creative Commons.
// Elk pakket is een map in content/materiaal/<slug>/ met een pakket.md (frontmatter + uitleg)
// en een map bestanden/ met wat bezoekers downloaden. De site maakt er zelf een zip van.
// Zie content/materiaal/README.md voor hoe je een pakket toevoegt.
import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { marked } from "marked";
import { SITE_URL } from "./seo";

export const SOORTEN = {
  cursus: "Cursus",
  workshop: "Workshop",
  lezing: "Lezing",
  gesprek: "Gespreksformat",
  fiches: "Fiches",
  fundament: "Fundament",
} as const;
export type Soort = keyof typeof SOORTEN;

export const LICENTIES: Record<string, { naam: string; url: string; kort: string }> = {
  "CC BY 4.0": {
    naam: "Creative Commons Naamsvermelding 4.0",
    url: "https://creativecommons.org/licenses/by/4.0/deed.nl",
    kort: "Je mag het gebruiken, aanpassen en delen, ook als je er geld voor vraagt, zolang je AI Ontcijferd vermeldt en aangeeft dat je het aanpaste.",
  },
  "CC BY-SA 4.0": {
    naam: "Creative Commons Naamsvermelding-GelijkDelen 4.0",
    url: "https://creativecommons.org/licenses/by-sa/4.0/deed.nl",
    kort: "Je mag het gebruiken, aanpassen en delen, ook als je er geld voor vraagt, zolang je AI Ontcijferd vermeldt, aangeeft dat je het aanpaste en je eigen versie onder dezelfde licentie deelt.",
  },
};

export type Bestand = {
  naam: string; // bestandsnaam zoals hij gedownload wordt
  omschrijving: string;
  formaat: string; // "PDF", "Word", ...
  bytes: number;
  pad: string; // absoluut pad op schijf (alleen bij het bouwen)
  url: string;
};

export type Pakket = {
  slug: string;
  titel: string;
  samenvatting: string;
  soort: Soort;
  status: "beschikbaar" | "in-voorbereiding";
  voor: string[];
  deelnemers: string;
  niveau: string;
  /** De niveaus uit de niveaucheck waarbij het pakket past, bv. ["N0", "N1", "N2"]; leeg als onbekend. */
  niveaus: string[];
  duur: string;
  versie: string;
  bijgewerkt: string;
  licentie: string;
  maker: string;
  volgorde: number;
  personaliseren: string;
  html: string;
  bestanden: Bestand[];
  zipUrl: string;
  zipNaam: string;
};

const FORMATEN: Record<string, string> = {
  pdf: "PDF",
  docx: "Word",
  doc: "Word",
  odt: "OpenDocument-tekst",
  pptx: "PowerPoint",
  odp: "OpenDocument-presentatie",
  xlsx: "Excel",
  ods: "OpenDocument-rekenblad",
  md: "Tekst (Markdown)",
  txt: "Tekst",
  html: "Webpagina",
  png: "Afbeelding",
  jpg: "Afbeelding",
  jpeg: "Afbeelding",
  svg: "Afbeelding",
  mp4: "Video",
  mp3: "Audio",
  csv: "Tabel (CSV)",
};

function datum(x: unknown): string {
  if (x instanceof Date) return x.toISOString().slice(0, 10);
  return x ? String(x) : "";
}

/** Bestandsnaam zonder extensie: "01-draaiboek/AO-01-draaiboek.pdf" -> "01-draaiboek/AO-01-draaiboek". */
export function stam(naam: string): string {
  return naam.replace(/\.[^./]+$/, "");
}

// Volgorde van de formaten binnen één document: eerst om te printen, dan om aan te passen, dan de bron.
const FORMAAT_VOLGORDE = ["pdf", "pptx", "docx", "xlsx", "odt", "odp", "ods", "md", "txt"];

export type Groep = { stam: string; titel: string; omschrijving: string; bestanden: Bestand[] };

/** Dezelfde tekst in meer formaten (pdf, docx, md) wordt één regel met een link per formaat. */
export function groepen(p: Pakket): Groep[] {
  const uit: Groep[] = [];
  for (const b of p.bestanden) {
    const s = stam(b.naam);
    let g = uit.find((x) => x.stam === s);
    if (!g) {
      g = { stam: s, titel: s.split("/").pop() ?? s, omschrijving: "", bestanden: [] };
      uit.push(g);
    }
    g.bestanden.push(b);
    if (!g.omschrijving && b.omschrijving) g.omschrijving = b.omschrijving;
  }
  const ext = (b: Bestand) => b.naam.split(".").pop()?.toLowerCase() ?? "";
  const rang = (b: Bestand) => {
    const i = FORMAAT_VOLGORDE.indexOf(ext(b));
    return i === -1 ? 99 : i;
  };
  for (const g of uit) g.bestanden.sort((a, b) => rang(a) - rang(b));
  return uit;
}

/** "N0–N2 · ..." -> ["N0","N1","N2"]; "N1 · Starter" -> ["N1"]; "N0 tot N4" -> alle vijf. */
export function niveausUit(tekst: string): string[] {
  const m = tekst.match(/N(\d)\s*(?:[–-]|tot)\s*N?(\d)/) ?? tekst.match(/N(\d)/);
  if (!m) return [];
  const van = Number(m[1]), tot = Number(m[2] ?? m[1]);
  return Array.from({ length: tot - van + 1 }, (_, i) => `N${van + i}`);
}

/** Korte weergave: "N0–N2" of "N1". */
export function niveauKort(p: { niveaus: string[] }): string {
  const n = p.niveaus;
  return n.length === 0 ? "" : n.length === 1 ? n[0] : `${n[0]}–${n[n.length - 1]}`;
}

let cache: Pakket[] | null = null;

export function allePakketten(): Pakket[] {
  if (cache) return cache;
  const map = path.resolve(process.cwd(), "../content/materiaal");
  if (!fs.existsSync(map)) return (cache = []);
  cache = fs
    .readdirSync(map, { withFileTypes: true })
    .filter((d) => d.isDirectory() && fs.existsSync(path.join(map, d.name, "pakket.md")))
    .map((d) => {
      const slug = d.name;
      const { data, content } = matter(fs.readFileSync(path.join(map, slug, "pakket.md"), "utf-8"));
      const meta: Record<string, string> = {};
      for (const b of Array.isArray(data.bestanden) ? data.bestanden : []) {
        if (b?.bestand) meta[String(b.bestand)] = String(b.omschrijving ?? "");
      }
      const bestandenMap = path.join(map, slug, "bestanden");
      // Submappen mogen (bv. 01-draaiboek/); de naam is dan het relatieve pad met "/".
      const lijst = (dir: string, voor = ""): string[] =>
        fs.readdirSync(dir, { withFileTypes: true }).filter((f) => !f.name.startsWith(".")).flatMap((f) =>
          f.isDirectory() ? lijst(path.join(dir, f.name), `${voor}${f.name}/`) : f.isFile() ? [`${voor}${f.name}`] : []);
      const volgorde = Object.keys(meta);
      const plaats = (naam: string) => {
        const i = volgorde.findIndex((k) => k === naam || k === stam(naam));
        return i === -1 ? 999 : i;
      };
      const bestanden: Bestand[] = fs.existsSync(bestandenMap)
        ? lijst(bestandenMap)
            .map((naam) => {
              const pad = path.join(bestandenMap, ...naam.split("/"));
              const ext = naam.split(".").pop()?.toLowerCase() ?? "";
              return {
                naam,
                omschrijving: meta[naam] ?? meta[stam(naam)] ?? "",
                formaat: FORMATEN[ext] ?? ext.toUpperCase(),
                bytes: fs.statSync(pad).size,
                pad,
                url: `/materiaal/${slug}/bestanden/${naam.split("/").map(encodeURIComponent).join("/")}`,
              };
            })
            // volgorde uit de frontmatter eerst, daarna alfabetisch
            .sort((a, b) => plaats(a.naam) - plaats(b.naam) || a.naam.localeCompare(b.naam, "nl"))
        : [];
      const soort = (String(data.soort ?? "workshop") as Soort) in SOORTEN ? (String(data.soort) as Soort) : "workshop";
      const versie = String(data.versie ?? "1.0");
      // Een pakket is pas beschikbaar als het dat zegt én er iets te downloaden valt.
      const status = data.status === "beschikbaar" && bestanden.length ? "beschikbaar" : "in-voorbereiding";
      return {
        slug,
        titel: String(data.titel ?? slug),
        samenvatting: String(data.samenvatting ?? ""),
        soort,
        status,
        voor: Array.isArray(data.voor) ? data.voor.map(String) : [],
        deelnemers: String(data.deelnemers ?? ""),
        niveau: String(data.niveau ?? ""),
        niveaus: niveausUit(String(data.niveau ?? "")),
        duur: String(data.duur ?? ""),
        versie,
        bijgewerkt: datum(data.bijgewerkt),
        licentie: LICENTIES[String(data.licentie)] ? String(data.licentie) : "CC BY 4.0",
        maker: String(data.maker ?? "Duncan Panis"),
        volgorde: Number(data.volgorde ?? 100),
        personaliseren: String(data.personaliseren ?? "").trim(),
        html: content.trim() ? (marked.parse(content, { async: false, gfm: true }) as string) : "",
        bestanden,
        zipUrl: `/materiaal/${slug}.zip`,
        zipNaam: `${slug}-v${versie}.zip`,
      } satisfies Pakket;
    })
    .sort((a, b) => a.volgorde - b.volgorde || a.titel.localeCompare(b.titel, "nl"));
  return cache;
}

export function beschikbarePakketten(): Pakket[] {
  return allePakketten().filter((p) => p.status === "beschikbaar");
}

export function grootte(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} kB`;
  return `${(bytes / 1024 / 1024).toFixed(1).replace(".", ",")} MB`;
}

export function totaleGrootte(p: Pakket): number {
  return p.bestanden.reduce((s, b) => s + b.bytes, 0);
}

/** De regel die wie het materiaal gebruikt, overneemt. */
export function naamsvermelding(p: Pakket, aangepastDoor = "[naam van je organisatie]"): string {
  return `Gebaseerd op "${p.titel}" (versie ${p.versie}) van AI Ontcijferd, ${SITE_URL.replace("https://", "")}/materiaal/${p.slug}, ${p.licentie}. Aangepast door ${aangepastDoor}.`;
}

/** Algemene prompt om een pakket met AI aan te passen. Werkt in elke chatbot die bestanden aanneemt. */
export function personalisatiePrompt(p?: Pakket): string {
  const wat = p ? `het pakket "${p.titel}" (versie ${p.versie}, ${p.licentie})` : "een open lespakket";
  const regels = [
    `Je helpt me ${wat} van AI Ontcijferd aan te passen voor mijn organisatie. De bestanden van het pakket zitten in de bijlage.`,
    "",
    "Over mijn organisatie en mijn publiek:",
    "- Organisatie: [naam en soort, bijvoorbeeld een bibliotheek, school, gemeente of bedrijf]",
    "- Deelnemers: [wie, hoeveel, leeftijd, voorkennis, taal]",
    "- Beschikbare tijd: [bijvoorbeeld 2 uur, of 3 sessies van 1 uur]",
    "- AI-tools die deelnemers mogen en kunnen gebruiken: [bijvoorbeeld alleen gratis tools, of het zakelijke account van de organisatie]",
    "- Voorbeelden en thema's uit onze eigen omgeving: [lokale voorbeelden, eigen diensten, actuele vragen]",
    "- Wat er zeker uit mag: [onderdelen die niet passen]",
    "",
    "Wat ik van je vraag:",
    "1. Geef me eerst een korte lijst van wat je wilt veranderen en waarom. Wacht op mijn akkoord voor je de bestanden aanpast.",
    "2. Houd de opbouw en de leerdoelen. Pas voorbeelden, oefeningen, woordkeuze en timing aan aan dit publiek.",
    "3. Verander geen feiten zonder het te melden. Zet [NAKIJKEN] bij alles wat afhangt van prijzen, regels of de versie van een AI-tool: dat verandert snel.",
    "4. Gebruik geen namen of gegevens van echte mensen in voorbeelden of oefeningen.",
    `5. Laat deze naamsvermelding staan, met onze naam ingevuld: ${p ? naamsvermelding(p) : "Gebaseerd op [titel] van AI Ontcijferd (aiontcijferd.be/materiaal), CC BY 4.0. Aangepast door [naam van je organisatie]."}`,
    "6. Zet geen logo of naam van AI Ontcijferd op de voorpagina alsof wij deze versie maakten.",
  ];
  if (p?.personaliseren) {
    regels.push("", "Specifiek voor dit pakket:", p.personaliseren);
  }
  return regels.join("\n");
}

export function leesmij(p: Pakket): string {
  const lic = LICENTIES[p.licentie];
  return [
    `${p.titel}`,
    `Versie ${p.versie}${p.bijgewerkt ? `, bijgewerkt op ${p.bijgewerkt}` : ""}`,
    `Van AI Ontcijferd: ${SITE_URL}/materiaal/${p.slug}`,
    "",
    p.samenvatting,
    "",
    "WAT ZIT ERIN",
    ...groepen(p).map((g) => `- ${g.bestanden.length === 1 ? g.bestanden[0].naam : `${g.stam} (${g.bestanden.map((b) => b.formaat).join(", ")})`}${g.omschrijving ? `: ${g.omschrijving}` : ""}`),
    "",
    "LICENTIE",
    `${lic.naam} (${p.licentie}): ${lic.url}`,
    lic.kort,
    "",
    "NAAMSVERMELDING (neem deze regel over in je eigen versie)",
    naamsvermelding(p),
    "",
    "AANPASSEN MET AI",
    `Uitleg in stappen: ${SITE_URL}/materiaal/gebruiken`,
    "Je kunt deze prompt in een chatbot plakken, samen met de bestanden uit dit pakket:",
    "",
    personalisatiePrompt(p),
    "",
    "Laat in de chatbot geen persoonsgegevens achter. Twijfel je? Doe eerst de Plakcheck:",
    `${SITE_URL}/plakcheck`,
    "",
    ...(p.soort === "fundament"
      ? ["GEBRUIK JE DIT? LAAT HET WETEN", "Waar en hoe gebruik je het, en wat zou je anders willen? Mail naar redactie@aiontcijferd.be.", ""]
      : ["GAF JE DIT PAKKET? LAAT HET WETEN", "Wat werkte, wat niet, wat paste je aan? Twee minuten van jou maken de volgende versie beter:", `${SITE_URL}/gegeven/${p.slug}`, ""]),
    "Fout gezien? Mail het naar redactie@aiontcijferd.be, met de naam van het pakket en het versienummer.",
    "",
  ].join("\r\n");
}
