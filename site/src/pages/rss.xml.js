import rss from "@astrojs/rss";
import { alleEdities } from "../lib/edities";

// Deze feed gebruikt MailerLite om elke nieuwe editie automatisch te versturen.
export function GET(context) {
  return rss({
    title: "AI Ontcijferd",
    description: "AI zonder hype. Wekelijkse analyse voor Vlaanderen, door Duncan Panis.",
    site: context.site,
    customData: "<language>nl-be</language>",
    items: alleEdities().map((e) => ({
      title: e.titel,
      pubDate: new Date(e.datum + "T07:00:00Z"),
      description: e.kernTekst,
      link: `/edities/${e.week}/`,
      content:
        e.kern +
        e.onderwerpen
          .map((o) => `<h2>${o.titel}</h2>${o.hype ? `<p><strong>Hype-meter:</strong> ${o.hype.stand}</p>` : ""}${o.html}`)
          .join("") +
        `<h2>Mijn inschatting</h2>${e.inschatting}`,
    })),
  });
}
