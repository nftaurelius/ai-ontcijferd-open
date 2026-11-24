// Elk bestand van een beschikbaar pakket, los te downloaden.
import fs from "node:fs";
import type { APIRoute } from "astro";
import { beschikbarePakketten, type Bestand } from "../../../../lib/materiaal";

export function getStaticPaths() {
  return beschikbarePakketten().flatMap((p) => p.bestanden.map((b) => ({ params: { slug: p.slug, bestand: b.naam }, props: { b } })));
}

export const GET: APIRoute = ({ props }) => {
  const { b } = props as { b: Bestand };
  return new Response(fs.readFileSync(b.pad));
};
