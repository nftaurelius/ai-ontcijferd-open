import rss from "@astrojs/rss";
import { alleDagbrieven, alleDossiers } from "../../lib/plus";

// Aparte feed voor Plus, zodat de nieuwsbrief van de weekeditie (/rss.xml) ongemoeid blijft.
export function GET(context) {
  const dagen = alleDagbrieven().slice(0, 30).map((d) => ({
    title: `Plus · ${d.datum}: ${d.items.map((i) => i.titel).slice(0, 2).join(" / ")}`,
    pubDate: new Date(d.datum + "T06:30:00Z"),
    description: d.kortTekst,
    link: `/plus/dag/${d.datum}/`,
    content: d.kort + d.items.map((i) => `<h2>${i.titel}</h2>${i.status ? `<p><strong>Status:</strong> ${i.status}</p>` : ""}${i.html}`).join(""),
  }));
  const dossiers = alleDossiers().map((d) => ({
    title: `Dossier: ${d.titel}`,
    pubDate: new Date(d.datum + "T08:00:00Z"),
    description: d.samenvatting,
    link: `/plus/dossiers/${d.slug}/`,
    content: d.kort + `<h2>Mijn inschatting</h2>${d.inschatting}`,
  }));
  return rss({
    title: "AI Ontcijferd Plus",
    description: "Elke dag het AI-nieuws en wat het betekent voor Vlaanderen, plus dossiers. Zonder hype.",
    site: context.site,
    customData: "<language>nl-be</language><copyright>CC BY 4.0, AI Ontcijferd</copyright>",
    items: [...dossiers, ...dagen].sort((a, b) => b.pubDate - a.pubDate),
  });
}
