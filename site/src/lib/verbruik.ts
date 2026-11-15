// Wat de redactieketen verbruikt: het aantal modeloproepen en tokens per rol.
// Leest de kostenbestanden die de pijplijn zelf bijhoudt (data/kosten.csv, data/plus/kosten.csv
// en data/weken/<week>/kosten.csv). Proefdraaien tellen niet mee.
// Bedragen in euro staan hier bewust niet: die hangen af van de prijs per model en van de facturen.
import fs from "node:fs";
import path from "node:path";

export type VerbruikRij = { rol: string; modellen: string[]; oproepen: number; tokensIn: number; tokensUit: number };
export type Verbruik = { rijen: VerbruikRij[]; totaal: VerbruikRij; van: string | null; tot: string | null };

const ROLNAMEN: Record<string, string> = {
  triage: "Triage",
  xradar: "X-radar",
  analist: "Analist",
  vertaler: "Vertaler",
  tegenspreker: "Tegenspreker",
  dagbrief: "Dagbrief (schrijven en revisie)",
  dagcontrole: "Dagbrief (controle)",
  dossier: "Dossier",
};

function bestanden(): string[] {
  const data = path.resolve(process.cwd(), "../data");
  const lijst = [path.join(data, "kosten.csv"), path.join(data, "plus", "kosten.csv")];
  const weken = path.join(data, "weken");
  if (fs.existsSync(weken)) {
    for (const week of fs.readdirSync(weken).sort()) lijst.push(path.join(weken, week, "kosten.csv"));
  }
  return lijst.filter((f) => fs.existsSync(f));
}

export function verbruik(): Verbruik {
  const perRol = new Map<string, VerbruikRij>();
  let van: string | null = null;
  let tot: string | null = null;
  for (const bestand of bestanden()) {
    const regels = fs.readFileSync(bestand, "utf-8").trim().split(/\r?\n/);
    const kop = regels.shift()?.split(",") ?? [];
    const kolom = (naam: string) => kop.indexOf(naam);
    for (const regel of regels) {
      const v = regel.split(",");
      if (v.length < kop.length || v[kolom("proefdraai")] === "ja") continue;
      const tokensIn = Number(v[kolom("tokens_in")]);
      const tokensUit = Number(v[kolom("tokens_uit")]);
      if (!Number.isFinite(tokensIn) || !Number.isFinite(tokensUit)) continue;
      const dag = v[kolom("tijd")].slice(0, 10);
      if (!van || dag < van) van = dag;
      if (!tot || dag > tot) tot = dag;
      const sleutel = v[kolom("rol")];
      const rij = perRol.get(sleutel) ?? { rol: ROLNAMEN[sleutel] ?? sleutel, modellen: [], oproepen: 0, tokensIn: 0, tokensUit: 0 };
      rij.oproepen += 1;
      rij.tokensIn += tokensIn;
      rij.tokensUit += tokensUit;
      const model = v[kolom("model")];
      if (model && !rij.modellen.includes(model)) rij.modellen.push(model);
      perRol.set(sleutel, rij);
    }
  }
  const rijen = [...perRol.values()].sort((a, b) => b.tokensIn + b.tokensUit - (a.tokensIn + a.tokensUit));
  const totaal = rijen.reduce(
    (t, r) => ({ ...t, oproepen: t.oproepen + r.oproepen, tokensIn: t.tokensIn + r.tokensIn, tokensUit: t.tokensUit + r.tokensUit }),
    { rol: "Totaal", modellen: [] as string[], oproepen: 0, tokensIn: 0, tokensUit: 0 },
  );
  return { rijen, totaal, van, tot };
}

/** 17.912.345 → "17,9 miljoen"; 345.000 → "345.000". */
export function leesbaarGetal(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toLocaleString("nl-BE", { maximumFractionDigits: 1 })} miljoen`;
  return n.toLocaleString("nl-BE");
}
