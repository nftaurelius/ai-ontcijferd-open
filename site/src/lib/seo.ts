// Gestructureerde gegevens (schema.org) voor zoekmachines en AI-assistenten.

export const SITE_URL = "https://aiontcijferd.be";
export const LICENTIE_URL = "https://creativecommons.org/licenses/by/4.0/deed.nl";

export const uitgever = {
  "@type": "NewsMediaOrganization",
  "@id": `${SITE_URL}/#organisatie`,
  name: "AI Ontcijferd",
  url: SITE_URL,
  logo: { "@type": "ImageObject", url: `${SITE_URL}/logo.png`, width: 512, height: 512 },
  description: "Wekelijkse analyse van wat er in AI gebeurt en wat het betekent voor Vlaanderen. AI zonder hype.",
  inLanguage: "nl-BE",
  areaServed: { "@type": "Place", name: "Vlaanderen" },
  publishingPrinciples: `${SITE_URL}/zo-werken-we`,
  correctionsPolicy: `${SITE_URL}/correcties`,
  founder: { "@id": `${SITE_URL}/#duncan` },
};

export const auteur = {
  "@type": "Person",
  "@id": `${SITE_URL}/#duncan`,
  name: "Duncan Panis",
  jobTitle: "AI frontier analyst",
  url: `${SITE_URL}/over`,
  sameAs: ["https://duncanpanis.be"],
};

export function websiteSchema() {
  return {
    "@context": "https://schema.org",
    "@graph": [
      { "@type": "WebSite", "@id": `${SITE_URL}/#website`, url: SITE_URL, name: "AI Ontcijferd", inLanguage: "nl-BE", publisher: { "@id": uitgever["@id"] } },
      uitgever,
      auteur,
    ],
  };
}
