import rss from "@astrojs/rss";
import { DOELGROEPEN, onderwerpenVoor } from "../../../lib/doelgroepen";
import { plusVoor } from "../../../lib/plus";

export function getStaticPaths() {
  return DOELGROEPEN.map((d) => ({ params: { slug: d.slug }, props: { d } }));
}

export function GET(context) {
  const { d } = context.props;
  return rss({
    title: `AI Ontcijferd — ${d.label}`,
    description: `Wat AI betekent voor ${d.wie} in Vlaanderen. AI zonder hype.`,
    site: context.site,
    customData: "<language>nl-be</language><copyright>CC BY 4.0, AI Ontcijferd</copyright>",
    items: [
      ...onderwerpenVoor(d.label).map(({ editie, onderwerp }) => ({
        title: onderwerp.titel,
        pubDate: new Date(editie.datum + "T07:00:00Z"),
        link: `/edities/${editie.week}/#${onderwerp.slug}`,
        description: onderwerp.hype ? `Hype-meter: ${onderwerp.hype.stand}. ${onderwerp.hype.uitleg}` : editie.titel,
        content: onderwerp.html,
      })),
      // Dagelijkse updates uit Plus, zodat elke doelgroep een eigen dagelijkse feed heeft
      ...plusVoor(d.label).slice(0, 40).map(({ dag, item }) => ({
        title: `Plus: ${item.titel}`,
        pubDate: new Date(dag.datum + "T06:30:00Z"),
        link: `/plus/dag/${dag.datum}/#${item.slug}`,
        description: item.status ? `Status: ${item.status}` : "Dagbrief AI Ontcijferd Plus",
        content: item.html,
      })),
    ].sort((a, b) => b.pubDate - a.pubDate),
  });
}
