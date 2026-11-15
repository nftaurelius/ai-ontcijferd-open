// Nieuwsbriefmail per weekeditie, klaar om als campagne in Brevo te zetten.
// Niet bedoeld als leespagina: de mail verwijst naar de editie op de site.
import type { APIRoute } from "astro";
import { alleEdities, type Editie } from "../../lib/edities";
import { nieuwsbriefMail } from "../../lib/mail";

export function getStaticPaths() {
  return alleEdities().map((editie) => ({ params: { week: editie.week }, props: { editie } }));
}

export const GET: APIRoute = ({ props }) =>
  new Response(nieuwsbriefMail((props as { editie: Editie }).editie), {
    headers: { "Content-Type": "text/html; charset=utf-8" },
  });
