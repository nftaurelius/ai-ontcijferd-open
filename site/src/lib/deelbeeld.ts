// Deelafbeeldingen (1200 x 630) per editie, dossier, dagbrief, pakket en vaste pagina.
// Gemaakt bij het bouwen met satori (tekst wordt vorm, dus geen lettertypen nodig op de server) en sharp.
import fs from "node:fs";
import path from "node:path";
import satori from "satori";
import sharp from "sharp";
import { alleEdities, datumLeesbaar, weekNummer } from "./edities";
import { alleDagbrieven, alleDossiers } from "./plus";
import { beschikbarePakketten } from "./materiaal";
import { INGANGEN } from "./site";

export type Deelbeeld = { pad: string; soort: string; titel: string; onder: string };

const VAST: Deelbeeld[] = [
  { pad: "/plakcheck", soort: "Gratis tool", titel: "Mag dit in een chatbot? En loont het dan nog?", onder: "Plakcheck en Urenrekening · draait in je browser" },
  { pad: "/bijsluiters", soort: "Bijsluiters", titel: "Wat doen AI-tools met wat je intypt, en wat kosten ze?", onder: "ChatGPT · Claude · Gemini · Copilot · Le Chat" },
  { pad: "/begin-hier", soort: "Begin hier", titel: "AI in tien minuten", onder: "Wat het is, waar je op let, waar je verder kunt" },
  { pad: "/ai-act", soort: "AI Act-kompas", titel: "Wat geldt wanneer, en wat betekent het voor jou?", onder: "Voor scholen, gemeenten, kmo's en burgers" },
  { pad: "/materiaal", soort: "Open lesmateriaal", titel: "Lespakketten om zelf over AI les te geven", onder: "Gratis, onder Creative Commons" },
  { pad: "/overnemen", soort: "Neem het over", titel: "Alles mag je overnemen en aanpassen", onder: "CC BY 4.0 · kant-en-klare teksten" },
  { pad: "/meedoen", soort: "Meedoen", titel: "Open inhoud, open code, samen beter maken", onder: "Fouten melden, bronnen voorstellen, code verbeteren" },
  ...Object.entries(INGANGEN).map(([k, i]) => ({ pad: `/${k}`, soort: i.titel, titel: i.vraag, onder: i.lead })),
];

let cache: Deelbeeld[] | null = null;

export function alleDeelbeelden(): Deelbeeld[] {
  if (cache) return cache;
  cache = [
    ...alleEdities().map((e) => ({ pad: `/edities/${e.week}`, soort: `Weekeditie · ${datumLeesbaar(e.datum)}`, titel: e.titel, onder: e.onderwerpen.slice(0, 3).map((o) => o.titel).join(" · ") })),
    ...alleDossiers().map((d) => ({ pad: `/plus/dossiers/${d.slug}`, soort: `Dossier · ${datumLeesbaar(d.datum)}`, titel: d.titel, onder: d.samenvatting })),
    ...alleDagbrieven().map((d) => ({ pad: `/plus/dag/${d.datum}`, soort: `Dagbrief · ${datumLeesbaar(d.datum)}`, titel: d.items.length ? d.items.slice(0, 3).map((i) => i.titel).join(" · ") : d.titel, onder: "AI Ontcijferd Plus" })),
    ...beschikbarePakketten().map((p) => ({ pad: `/materiaal/${p.slug}`, soort: `Open lespakket · versie ${p.versie}`, titel: p.titel, onder: `${p.duur ?? ""}${p.duur ? " · " : ""}${p.licentie} · gratis te downloaden` })),
    ...VAST,
  ];
  return cache;
}

export function deelbeeldVoor(pad: string): string | null {
  const schoon = pad.replace(/\/$/, "") || "/";
  return alleDeelbeelden().some((d) => d.pad === schoon) ? `/deel${schoon}.png` : null;
}

const kort = (t: string, n: number) => (t.length <= n ? t : `${t.slice(0, n).replace(/\s+\S*$/, "")}…`);

let fonts: { name: string; data: Buffer; weight: 400 | 700; style: "normal" }[] | null = null;
function lettertypen() {
  if (fonts) return fonts;
  const map = path.resolve(process.cwd(), "node_modules/@fontsource/atkinson-hyperlegible-next/files");
  fonts = [
    { name: "Atkinson", data: fs.readFileSync(path.join(map, "atkinson-hyperlegible-next-latin-400-normal.woff")), weight: 400, style: "normal" },
    { name: "Atkinson", data: fs.readFileSync(path.join(map, "atkinson-hyperlegible-next-latin-700-normal.woff")), weight: 700, style: "normal" },
  ];
  return fonts;
}

const el = (type: string, style: Record<string, unknown>, children: unknown) => ({ type, props: { style, children } });

export async function maakDeelbeeld(d: Deelbeeld): Promise<Buffer> {
  const titel = kort(d.titel, 110);
  const grootte = titel.length > 70 ? 54 : titel.length > 40 ? 64 : 76;
  const boom = el("div", { width: 1056, height: 502, display: "flex", flexDirection: "column", justifyContent: "space-between", background: "#f2f3ef", padding: "64px 72px", fontFamily: "Atkinson", color: "#20262b" }, [
    el("div", { display: "flex", alignItems: "center", fontSize: 34, fontWeight: 700 }, [
      el("span", { background: "#ffd400", padding: "0 6px", marginRight: 6 }, "AI"),
      el("span", {}, "Ontcijferd"),
    ]),
    el("div", { display: "flex", flexDirection: "column", width: 1056 }, [
      el("div", { fontSize: 24, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", color: "#5c6368", marginBottom: 20 }, d.soort),
      el("div", { display: "flex", width: 1056, fontSize: grootte, fontWeight: 700, lineHeight: 1.15 }, titel),
    ]),
    el("div", { display: "flex", width: 1056, justifyContent: "space-between", alignItems: "flex-end", fontSize: 24, color: "#5c6368" }, [
      el("div", { display: "flex", width: 800 }, kort(d.onder, 110)),
      el("div", { fontWeight: 700, color: "#20262b" }, "aiontcijferd.be"),
    ]),
  ]);
  const svg = await satori(boom as any, { width: 1200, height: 630, fonts: lettertypen() });
  return sharp(Buffer.from(svg)).png({ compressionLevel: 9 }).toBuffer();
}
