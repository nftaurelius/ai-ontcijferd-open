// Het hele pakket als één zip, met een LEESMIJ.txt (licentie, naamsvermelding en de prompt om het aan te passen).
import fs from "node:fs";
import type { APIRoute } from "astro";
import { zipSync, strToU8, type Zippable } from "fflate";
import { beschikbarePakketten, leesmij, type Pakket } from "../../lib/materiaal";

export function getStaticPaths() {
  return beschikbarePakketten().map((p) => ({ params: { slug: p.slug }, props: { p } }));
}

export const GET: APIRoute = ({ props }) => {
  const { p } = props as { p: Pakket };
  // Vaste datum: dezelfde inhoud geeft dezelfde zip.
  const mtime = new Date((p.bijgewerkt || "2026-01-01") + "T12:00:00Z");
  const map: Zippable = { "LEESMIJ.txt": [strToU8(leesmij(p)), { mtime }] };
  for (const b of p.bestanden) {
    // Submappen (bv. 01-draaiboek/) blijven submappen in de zip.
    const delen = b.naam.split("/");
    let doel = map;
    for (const d of delen.slice(0, -1)) doel = (doel[d] ??= {}) as Zippable;
    doel[delen[delen.length - 1]] = [new Uint8Array(fs.readFileSync(b.pad)), { mtime }];
  }
  const zip = zipSync({ [`${p.slug}-v${p.versie}`]: map }, { level: 6 });
  return new Response(zip, { headers: { "Content-Type": "application/zip" } });
};
