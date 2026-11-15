import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";

export type Toepassing = {
  titel: string;
  slug: string;
  soort: "demo" | "praktijk";
  datum: string;
  wie: string;
  waar: string;
  dichtbij: boolean;
  doelgroepen: string[];
  wat: string;
  waarom: string;
  kanttekening: string;
  video?: string;
  bron: { titel: string; url: string; uitgever: string };
};

let cache: Toepassing[] | null = null;

function datumTekst(d: unknown): string {
  return d instanceof Date ? d.toISOString().slice(0, 10) : String(d ?? "");
}

export function alleToepassingen(): Toepassing[] {
  if (cache) return cache;
  const bestand = path.resolve(process.cwd(), "../content/toepassingen.yaml");
  if (!fs.existsSync(bestand)) return (cache = []);
  const data = yaml.load(fs.readFileSync(bestand, "utf-8")) as { toepassingen?: Record<string, unknown>[] } | null;
  cache = (data?.toepassingen ?? [])
    .map((t) => ({ ...(t as unknown as Toepassing), datum: datumTekst(t.datum), dichtbij: Boolean(t.dichtbij) }))
    .sort((a, b) => b.datum.localeCompare(a.datum));
  return cache;
}

export function toepassingenVoor(label: string): Toepassing[] {
  return alleToepassingen().filter((t) => t.doelgroepen.some((d) => d.toLowerCase() === label.toLowerCase()));
}

/** YouTube-id uit een link, zodat we de video privacyvriendelijk kunnen inbedden. */
export function youtubeId(url?: string): string | null {
  if (!url) return null;
  const m = url.match(/(?:youtube\.com\/(?:watch\?v=|shorts\/|embed\/)|youtu\.be\/)([\w-]{11})/);
  return m ? m[1] : null;
}

export function videoBron(url: string): string {
  const host = new URL(url).hostname.replace(/^www\./, "");
  if (host === "x.com" || host === "twitter.com") return "X";
  if (host.endsWith("linkedin.com")) return "LinkedIn";
  if (host.endsWith("vimeo.com")) return "Vimeo";
  return host;
}
