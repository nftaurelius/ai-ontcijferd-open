// Deelafbeelding per pagina: /deel/<pad>.png (zie src/lib/deelbeeld.ts).
import type { APIRoute } from "astro";
import { alleDeelbeelden, maakDeelbeeld, type Deelbeeld } from "../../lib/deelbeeld";

export function getStaticPaths() {
  return alleDeelbeelden().map((d) => ({ params: { pad: d.pad.replace(/^\//, "") }, props: { d } }));
}

export const GET: APIRoute = async ({ props }) => {
  const png = await maakDeelbeeld((props as { d: Deelbeeld }).d);
  return new Response(png, { headers: { "Content-Type": "image/png" } });
};
