// Mail "Nieuw gratis materiaal" per beschikbaar pakket, klaar om als campagne in Brevo te zetten.
import type { APIRoute } from "astro";
import { beschikbarePakketten, type Pakket } from "../../../lib/materiaal";
import { materiaalMail } from "../../../lib/mail-materiaal";

export function getStaticPaths() {
  return beschikbarePakketten().map((p) => ({ params: { slug: p.slug }, props: { p } }));
}

export const GET: APIRoute = ({ props }) =>
  new Response(materiaalMail((props as { p: Pakket }).p), { headers: { "Content-Type": "text/html; charset=utf-8" } });
