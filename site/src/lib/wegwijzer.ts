// Wegwijzer: wat anderen in Vlaanderen al goed aanbieden over AI (content/wegwijzer.yaml).
// "Zelf maken wat ontbreekt, verwijzen naar wat goed is" (data/visie.md). Alleen gecontroleerde items komen op de site.
import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";
import { DOELGROEPEN } from "./doelgroepen";

export type Ingang = "volgen" | "leren" | "doen" | "lesgeven";

export type Wegwijs = {
  slug: string;
  naam: string;
  aanbieder: string;
  url: string;
  soort: string;
  wat: string;
  doelgroepen: string[];
  doelgroepSlugs: string[];
  ingang: Ingang;
  niveau: string;
  prijs: "gratis" | "betalend" | "gemengd" | "onbekend";
  prijsTekst?: string;
  licentie: string;
  taal: string;
  verwijsAls: string;
  bijOns?: { tekst: string; href: string };
  laatstGecontroleerd: string;
  status: string;
};

export const INGANG_LABELS: Record<Ingang, { titel: string; vraag: string }> = {
  leren: { titel: "Leren", vraag: "Begrijpen hoe het werkt" },
  doen: { titel: "Doen", vraag: "Ermee aan de slag" },
  lesgeven: { titel: "Lesgeven", vraag: "Het doorgeven aan anderen" },
  volgen: { titel: "Volgen", vraag: "Op de hoogte blijven en anderen ontmoeten" },
};
export const INGANG_VOLGORDE: Ingang[] = ["leren", "doen", "lesgeven", "volgen"];

export const SOORT_LABELS: Record<string, string> = {
  lesmateriaal: "Lesmateriaal",
  opleiding: "Opleiding",
  richtlijn: "Richtlijn",
  kader: "Kader",
  tool: "Hulpmiddel",
  overzicht: "Overzicht",
  netwerk: "Netwerk",
  onderzoek: "Onderzoek",
  evenement: "Evenement",
  hulp: "Hulplijn",
};

export const TAAL_LABELS: Record<string, string> = { nl: "Nederlands", en: "Engels", "nl en en": "Nederlands en Engels" };

function datumTekst(d: unknown): string {
  return d instanceof Date ? d.toISOString().slice(0, 10) : String(d ?? "");
}

let cache: Wegwijs[] | null = null;

/** Alle gecontroleerde items, in de volgorde van het bestand. */
export function alleWegwijzers(): Wegwijs[] {
  if (cache) return cache;
  const bestand = path.resolve(process.cwd(), "../content/wegwijzer.yaml");
  if (!fs.existsSync(bestand)) return (cache = []);
  const data = yaml.load(fs.readFileSync(bestand, "utf-8")) as { wegwijzer?: Record<string, any>[] } | null;
  const slugs = new Set<string>();
  cache = (data?.wegwijzer ?? [])
    .filter((w) => String(w.status) === "gecontroleerd")
    .map((w) => {
      const slug = String(w.slug);
      if (slugs.has(slug)) throw new Error(`wegwijzer.yaml: dubbele slug ${slug}`);
      slugs.add(slug);
      const doelgroepen = (w.doelgroepen ?? []) as string[];
      const doelgroepSlugs = doelgroepen.map((d) => {
        const g = DOELGROEPEN.find((x) => x.label.toLowerCase() === d.toLowerCase());
        if (!g) throw new Error(`wegwijzer.yaml: onbekende doelgroep "${d}" bij ${slug}`);
        return g.slug;
      });
      if (!INGANG_LABELS[w.ingang as Ingang]) throw new Error(`wegwijzer.yaml: onbekende ingang "${w.ingang}" bij ${slug}`);
      return {
        slug,
        naam: String(w.naam),
        aanbieder: String(w.aanbieder),
        url: String(w.url),
        soort: String(w.soort),
        wat: String(w.wat).trim(),
        doelgroepen,
        doelgroepSlugs,
        ingang: w.ingang as Ingang,
        niveau: String(w.niveau ?? ""),
        prijs: w.prijs,
        prijsTekst: w.prijs_tekst ? String(w.prijs_tekst) : undefined,
        licentie: String(w.licentie ?? "niet vermeld"),
        taal: String(w.taal ?? "nl"),
        verwijsAls: String(w.verwijs_als ?? ""),
        bijOns: w.bij_ons ? { tekst: String(w.bij_ons.tekst), href: String(w.bij_ons.href) } : undefined,
        laatstGecontroleerd: datumTekst(w.laatstGecontroleerd),
        status: String(w.status),
      } as Wegwijs;
    });
  return cache;
}

export function wegwijzersVoor(doelgroepSlug: string): Wegwijs[] {
  // Wat in de eerste plaats voor deze doelgroep is, komt eerst (de eerste doelgroep in het bestand is de belangrijkste).
  return alleWegwijzers()
    .filter((w) => w.doelgroepSlugs.includes(doelgroepSlug))
    .map((w, i) => ({ w, i, rang: w.doelgroepSlugs.indexOf(doelgroepSlug) }))
    .sort((a, b) => a.rang - b.rang || a.i - b.i)
    .map((x) => x.w);
}

/** Leesbare prijs: de precieze tekst als die er is, anders het soort. */
export function prijsLeesbaar(w: Wegwijs): string {
  if (w.prijsTekst) return w.prijsTekst.charAt(0).toUpperCase() + w.prijsTekst.slice(1);
  return { gratis: "Gratis", betalend: "Betalend", gemengd: "Deels gratis", onbekend: "Prijs: zie de aanbieder" }[w.prijs] ?? w.prijs;
}

/** Mag je het overnemen? Alleen bij een open licentie; anders verwijzen we alleen. */
export function licentieLeesbaar(w: Wegwijs): string {
  if (/^cc /i.test(w.licentie)) return `${w.licentie}: je mag het overnemen en aanpassen, met naamsvermelding`;
  if (w.licentie === "niet vermeld") return "Geen licentie vermeld: gebruik het, maar neem het niet zomaar over";
  if (w.licentie === "niet van toepassing") return "";
  return w.licentie.charAt(0).toUpperCase() + w.licentie.slice(1);
}

export function laatsteControle(): string {
  return alleWegwijzers().map((w) => w.laatstGecontroleerd).sort().at(-1) ?? "";
}
