// De niveaucheck (AO-00) van Duncan is de enige bron: de pagina /niveaucheck leest de niveaus, de vijf vragen en
// de uitslagteksten rechtstreeks uit content/materiaal/niveaucheck/bestanden/AO-00-niveaucheck.md.
// Pas je daar iets aan, dan volgt de pagina bij de volgende bouw. Blijft de opbouw van dat bestand gelijk
// (tabel in deel 1, vragen als "**1. ...**", uitslagen als "### N0 · Naam"), dan werkt de lezer.
import fs from "node:fs";
import path from "node:path";
import { marked } from "marked";

const BESTAND = path.resolve(process.cwd(), "../content/materiaal/niveaucheck/bestanden/AO-00-niveaucheck.md");

export type Niveau = {
  code: string; // "N0"
  naam: string; // "Nieuwsgierig"
  kanAl: string;
  leertHierna: string;
  inDeCursus: string;
  uitslagHtml: string;
};
export type Vraag = { nr: number; tekst: string; uitlegHtml: string; neeGeeft: string; jaGeeft?: string };

// Waar je verder kunt per niveau: de delen van de cursus op deze site en één ander stuk. Redactionele keuze;
// de cursuskolom in AO-00 is de basis.
export const VERDER: Record<string, { href: string; tekst: string }[]> = {
  N0: [
    { href: "/begin-hier", tekst: "Begin hier: AI in tien minuten" },
    { href: "/cursus/m-omjeheen", tekst: "Cursus: AI om je heen" },
    { href: "/cursus/deel1", tekst: "Cursus, deel 1: Aan de slag met AI" },
  ],
  N1: [
    { href: "/cursus/deel1", tekst: "Cursus, deel 1: Aan de slag met AI" },
    { href: "/plakcheck", tekst: "Plakcheck: mag dit in een chatbot?" },
  ],
  N2: [
    { href: "/cursus/deel2", tekst: "Cursus, deel 2: Je persoonlijke assistent" },
    { href: "/werkwijzen", tekst: "Werkwijzen: prompts om te hergebruiken" },
  ],
  N3: [
    { href: "/cursus/deel3", tekst: "Cursus, deel 3: AI als hefboom" },
    { href: "/werkwijzen", tekst: "Werkwijzen: prompts, skills en agents" },
  ],
  N4: [
    { href: "/cursus/deel4", tekst: "Cursus, deel 4: Geïntegreerde systemen" },
    { href: "/bijsluiters", tekst: "Bijsluiters: wat AI-tools met je gegevens doen" },
  ],
};

const md = (s: string) => marked.parse(s.trim(), { async: false }) as string;
const zonderMd = (s: string) => s.replace(/\*\*?([^*]+)\*\*?/g, "$1").trim();

function deel(tekst: string, kop: RegExp): string {
  const start = tekst.search(kop);
  if (start === -1) throw new Error(`Niveaucheck: deel ${kop} niet gevonden in ${BESTAND}`);
  const rest = tekst.slice(start);
  const volgende = rest.slice(3).search(/\n## /);
  return volgende === -1 ? rest : rest.slice(0, volgende + 3);
}

let cache: { niveaus: Niveau[]; vragen: Vraag[]; onderElke: string; versie: string; nagekeken: string; inleiding: string; chatbot: string } | null = null;

export function niveaucheck() {
  if (cache) return cache;
  const ruw = fs.readFileSync(BESTAND, "utf-8").replace(/\r\n/g, "\n");
  const versie = ruw.match(/^versie:\s*(.+)$/m)?.[1].trim() ?? "";
  const nagekeken = ruw.match(/^nagekeken:\s*(.+)$/m)?.[1].trim() ?? "";
  const tekst = ruw.replace(/^---\n[\s\S]*?\n---\n/, "");

  // Deel 1: de tabel met niveaus
  const rijen = deel(tekst, /\n## 1\. /).split("\n").filter((r) => /^\|\s*N\d\s*\|/.test(r));
  const basis = rijen.map((r) => {
    const c = r.split("|").slice(1, -1).map((x) => x.trim());
    return { code: c[0], naam: c[1], kanAl: c[2], leertHierna: c[3], inDeCursus: c[4] };
  });

  // Deel 2: de vragen
  const d2 = deel(tekst, /\n## 2\. /);
  const chatbot = d2.match(/\n(Een \*\*chatbot\*\*[^\n]+)/)?.[1] ?? "";
  const inleiding = d2.match(/\*\*Op welk niveau sta je met AI\?\*\*\n\n([^\n]+)/)?.[1] ?? "";
  const vragen: Vraag[] = [];
  const blokken = d2.split(/\n(?=\*\*\d\. )/).slice(1);
  for (const b of blokken) {
    const m = b.match(/^\*\*(\d)\. (.+?)\*\*\n([\s\S]*?)☐ ja/);
    if (!m) continue;
    const uitleg = m[3].trim().replace(/^\*(.+)\*$/s, "$1");
    const nee = b.match(/☐ nee → je bent \*\*(N\d)\*\*/)?.[1] ?? "";
    const ja = b.match(/☐ ja → je bent \*\*(N\d)\*\*/)?.[1];
    vragen.push({ nr: Number(m[1]), tekst: m[2].trim(), uitlegHtml: uitleg ? md(uitleg) : "", neeGeeft: nee, jaGeeft: ja });
  }

  // Deel 3: de uitslagen
  const d3 = deel(tekst, /\n## 3\. /);
  const uitslagen: Record<string, string> = {};
  for (const b of d3.split(/\n### /).slice(1)) {
    const kop = b.split("\n")[0];
    const code = kop.match(/^(N\d)/)?.[1];
    const romp = b.slice(kop.length);
    if (code) uitslagen[code] = md(romp);
  }
  const onderElke = md((d3.split(/\n### Onder elke uitslag\n/)[1] ?? "").trim());

  const niveaus = basis.map((n) => ({ ...n, uitslagHtml: uitslagen[n.code] ?? "" }));
  if (niveaus.length !== 5 || vragen.length !== 5 || niveaus.some((n) => !n.uitslagHtml))
    throw new Error(`Niveaucheck: verwacht 5 niveaus, 5 vragen en 5 uitslagen, kreeg ${niveaus.length}, ${vragen.length}, ${Object.keys(uitslagen).length}`);
  cache = { niveaus, vragen, onderElke, versie, nagekeken, inleiding: zonderMd(inleiding), chatbot: md(chatbot) };
  return cache;
}
