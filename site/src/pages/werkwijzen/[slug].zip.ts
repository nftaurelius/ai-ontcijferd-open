// Een skill of agent als zip: de map met SKILL.md (en wat er nog bij hoort), plus een LEESMIJ.
import type { APIRoute } from "astro";
import { zipSync, strToU8, type Zippable } from "fflate";
import { beschikbareWerkwijzen, type Werkwijze } from "../../lib/werkwijzen";
import { SITE_URL } from "../../lib/seo";

export function getStaticPaths() {
  return beschikbareWerkwijzen()
    .filter((w) => w.bestanden.length > 0)
    .map((w) => ({ params: { slug: w.slug }, props: { w } }));
}

export const GET: APIRoute = ({ props }) => {
  const { w } = props as { w: Werkwijze };
  const mtime = new Date((w.bijgewerkt || "2026-01-01") + "T12:00:00Z");
  const map: Zippable = {};
  for (const b of w.bestanden) map[b.naam.split("\\").join("/")] = [new Uint8Array(b.inhoud), { mtime }];
  const leesmij = [
    w.titel,
    `Versie ${w.versie}, bijgewerkt op ${w.bijgewerkt}`,
    `Van AI Ontcijferd: ${SITE_URL}/werkwijzen/${w.slug}`,
    "",
    w.samenvatting,
    "",
    `Getest: ${w.getest}`,
    `Licentie: ${w.licentie}. Je mag dit gebruiken, aanpassen en delen, met vermelding van AI Ontcijferd en een link.`,
    "",
  ].join("\r\n");
  // Claude verwacht de map van de skill als enige bovenste map in de zip; de LEESMIJ gaat er dus in.
  map["LEESMIJ.txt"] = [strToU8(leesmij), { mtime }];
  const zip = zipSync({ [w.slug]: map }, { level: 6 });
  return new Response(zip, { headers: { "Content-Type": "application/zip" } });
};
