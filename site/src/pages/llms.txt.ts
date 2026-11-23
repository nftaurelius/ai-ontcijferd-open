// llms.txt: een overzicht van de site voor AI-assistenten (zie llmstxt.org).
import { alleEdities } from "../lib/edities";
import { alleDossiers } from "../lib/plus";
import { alleTermen } from "../lib/jargon";
import { alleToepassingen } from "../lib/toepassingen";
import { alleTools } from "../lib/tools";
import { beschikbarePakketten } from "../lib/materiaal";

export function GET() {
  const edities = alleEdities();
  const regels = [
    "# AI Ontcijferd",
    "",
    "> Wekelijkse analyse van wat er in AI gebeurt en wat het betekent voor Vlaanderen (België): onderwijs, werk, lokale overheden, zelfstandigen, bibliotheken en burgers. AI zonder hype. Door Duncan Panis. Nederlandstalig.",
    "",
    "Elke editie geeft per onderwerp wat er gebeurde, waarom het ertoe doet voor Vlaanderen en een hype-meter (sterk overroepen, overroepen, terecht, onderschat, sterk onderschat). Claims van bedrijven over hun eigen producten krijgen het label 'volgens de maker'. De site wordt grotendeels gemaakt door AI-agents en nagelezen door een menselijke eindredacteur. Alle inhoud valt onder CC BY 4.0: hergebruik mag met vermelding van AI Ontcijferd en een link.",
    "",
    "## Kernpagina's",
    "",
    "- [Edities](https://aiontcijferd.be/edities): alle weekedities van de Stand van AI",
    "- [Plus](https://aiontcijferd.be/plus): dagelijkse dagbrief met het AI-nieuws per doelgroep, en uitgebreide dossiers",
    "- [AI Act-kompas](https://aiontcijferd.be/ai-act): wat de Europese AI-verordening betekent voor scholen, gemeenten, kmo's en burgers in Vlaanderen",
    "- [Wat kan AI al?](https://aiontcijferd.be/wat-kan-ai): demo's en praktijkvoorbeelden van AI, met bron en kanttekening, per doelgroep",
    "- [Jargonfilter](https://aiontcijferd.be/jargon): AI-termen in gewoon Nederlands",
    "- [Fiches](https://aiontcijferd.be/fiches): praktische checklists",
    "- [Voor jou](https://aiontcijferd.be/voor): onderwerpen per doelgroep",
    "- [Terugblik](https://aiontcijferd.be/terugblik): alle hype-meter-oordelen, met terugblik op wie gelijk had",
    "- [Gratis](https://aiontcijferd.be/gratis): gratis tools en open lesmateriaal (Creative Commons) over AI",
    "- [Open lesmateriaal](https://aiontcijferd.be/materiaal): lespakketten, lezingen en een AI-cursus om te downloaden en met AI aan te passen; handleiding op /materiaal/gebruiken",
    "- [Zo werken we](https://aiontcijferd.be/zo-werken-we): werkwijze, bronregels en redactiestatuut",
    "- [De AI-cursus](https://aiontcijferd.be/cursus): een volledige, tool-onafhankelijke cursus om met AI te leren werken, online en als PDF",
    "- [Werkwijzen](https://aiontcijferd.be/werkwijzen): prompts, skills en agents om AI verstandig te gebruiken, met bijsluiter",
    "- [Begin hier](https://aiontcijferd.be/begin-hier): AI in tien minuten, voor wie nieuw is",
    "- [Bijsluiters van AI-tools](https://aiontcijferd.be/bijsluiters): wat ChatGPT, Claude, Gemini, Copilot en Le Chat met je invoer doen en wat ze kosten, met bron en datum",
    "- [Neem het over](https://aiontcijferd.be/overnemen): alles staat onder CC BY 4.0; zo vermeld je de bron, met kant-en-klare teksten",
    "- [Meedoen](https://aiontcijferd.be/meedoen): fouten melden, bronnen voorstellen, de open code (MIT) verbeteren",
    "",
    "## Gratis tools",
    "",
    ...alleTools().map((t) => `- [${t.naam}](https://aiontcijferd.be/${t.slug}): ${t.vraag} ${t.uitleg}`),
    "",
    ...(beschikbarePakketten().length
      ? ["## Open lesmateriaal", "", ...beschikbarePakketten().map((p) => `- [${p.titel}](https://aiontcijferd.be/materiaal/${p.slug}) (${p.soort}, ${p.licentie}): ${p.samenvatting}`), ""]
      : []),
    "## Edities",
    "",
    ...edities.map((e) => `- [${e.titel}](https://aiontcijferd.be/edities/${e.week}): ${e.kernTekst.slice(0, 200)}`),
    "",
    "## Dossiers",
    "",
    ...alleDossiers().map((d) => `- [${d.titel}](https://aiontcijferd.be/plus/dossiers/${d.slug}): ${d.samenvatting.slice(0, 200)}`),
    "",
    "## Wat kan AI al?",
    "",
    ...alleToepassingen().map((t) => `- [${t.titel}](https://aiontcijferd.be/wat-kan-ai#${t.slug}) (${t.soort === "demo" ? "demo" : "praktijk"}, ${t.wie}, ${t.datum}): ${t.wat.slice(0, 200)}`),
    "",
    "## Jargon",
    "",
    ...alleTermen().map((t) => `- [${t.term}](https://aiontcijferd.be/jargon/${t.slug}): ${t.uitleg_leek}`),
    "",
  ];
  return new Response(regels.join("\n"), { headers: { "Content-Type": "text/plain; charset=utf-8" } });
}
