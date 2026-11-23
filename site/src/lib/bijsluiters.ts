// Bijsluiters van AI-tools: wat een aanbieder met je invoer doet en wat het kost.
// Alle gegevens komen uit het configuratieblok van de Plakcheck (public/plakcheck/app/index.html),
// zodat ze maar op één plek nagekeken en bijgewerkt worden. Hier staat alleen de indeling per tool.
import { leesConfig } from "./tools";

export type Gegeven = {
  id: string;
  naam: string;
  tekst: string;
  opmerking?: string;
  bron: string;
  bronUrl: string;
  laatstGecontroleerd: string;
  status: string;
  gecontroleerdDoor: string;
  verouderd: boolean;
};

export type Prijs = Gegeven & { soort: string; bedrag: number; munt: string; btw: string };

export type Bijsluiter = {
  slug: string;
  naam: string;
  maker: string;
  wat: string;
  invoer: Gegeven[];
  prijzen: Prijs[];
  teControleren: number;
  verouderd: number;
  laatstGecontroleerd: string;
};

const INDELING = [
  { slug: "chatgpt", naam: "ChatGPT", maker: "OpenAI (Verenigde Staten)", wat: "Chatbot en assistent voor tekst, beeld, spraak en bestanden.", aanbieders: ["openai-"], prijzen: ["chatgpt-"] },
  { slug: "claude", naam: "Claude", maker: "Anthropic (Verenigde Staten)", wat: "Chatbot en assistent voor tekst, code en bestanden.", aanbieders: ["anthropic-"], prijzen: ["claude-"] },
  { slug: "gemini", naam: "Gemini", maker: "Google (Verenigde Staten)", wat: "Chatbot en assistent, ook ingebouwd in Gmail, Docs en de rest van Google Workspace.", aanbieders: ["google-"], prijzen: ["google-"] },
  { slug: "copilot", naam: "Copilot", maker: "Microsoft (Verenigde Staten)", wat: "Chatbot en assistent, ook ingebouwd in Word, Outlook, Teams en de rest van Microsoft 365.", aanbieders: ["microsoft-"], prijzen: ["m365-"] },
  { slug: "le-chat", naam: "Le Chat", maker: "Mistral AI (Frankrijk)", wat: "Chatbot en assistent van een Europese aanbieder.", aanbieders: ["mistral"], prijzen: ["mistral-"] },
];

const DAG = 24 * 60 * 60 * 1000;

function isVerouderd(datum: string, dagen: number, nu: Date): boolean {
  const d = new Date(datum);
  return Number.isNaN(d.getTime()) || nu.getTime() - d.getTime() > dagen * DAG;
}

let cache: { bijsluiters: Bijsluiter[]; versie: string; bijgewerkt: string; nagekekenOp: string | null } | null = null;

export function bijsluiters() {
  if (cache) return cache;
  const cfg = leesConfig("plakcheck") ?? {};
  const houdbaar = cfg.meta?.houdbaarheidDagen ?? { prijzen: 60, aanbieders: 90 };
  const nu = new Date();
  const lijst = INDELING.map((f) => {
    const invoer: Gegeven[] = (cfg.aanbieders ?? [])
      .filter((a: any) => f.aanbieders.some((p) => a.id.startsWith(p)))
      .map((a: any) => ({ ...a, tekst: a.bewering, verouderd: isVerouderd(a.laatstGecontroleerd, houdbaar.aanbieders, nu) }));
    const prijzen: Prijs[] = (cfg.prijzen ?? [])
      .filter((p: any) => f.prijzen.some((v) => p.id.startsWith(v)))
      .map((p: any) => ({ ...p, tekst: "", verouderd: isVerouderd(p.laatstGecontroleerd, houdbaar.prijzen, nu) }));
    const alles = [...invoer, ...prijzen];
    return {
      slug: f.slug,
      naam: f.naam,
      maker: f.maker,
      wat: f.wat,
      invoer,
      prijzen,
      teControleren: alles.filter((g) => g.status === "TE CONTROLEREN").length,
      verouderd: alles.filter((g) => g.verouderd).length,
      laatstGecontroleerd: alles.map((g) => g.laatstGecontroleerd).sort().at(-1) ?? "",
    };
  });
  cache = {
    bijsluiters: lijst,
    versie: String(cfg.meta?.versie ?? ""),
    bijgewerkt: String(cfg.meta?.configBijgewerktOp ?? ""),
    nagekekenOp: cfg.redactie?.nagekekenDoorEindredacteurOp ?? null,
  };
  return cache;
}

export function bedrag(p: Prijs): string {
  const getal = p.bedrag.toLocaleString("nl-BE", { minimumFractionDigits: Number.isInteger(p.bedrag) ? 0 : 2, maximumFractionDigits: 2 });
  return p.munt === "EUR" ? `€ ${getal}` : p.munt === "USD" ? `$ ${getal}` : `${getal} ${p.munt}`;
}
