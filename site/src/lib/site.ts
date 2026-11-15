// Algemene instellingen van de site.
export const CONTACT_EMAIL = "redactie@aiontcijferd.be"; // stel doorsturing in bij Combell
export const LINKEDIN = ""; // url van de LinkedIn-pagina van AI Ontcijferd, als die er is

// Hoofdmenu: zes ingangen. `ook` = paden die onder dezelfde ingang vallen (voor de markering).
export const MENU = [
  { href: "/edities", tekst: "Weekeditie", uitleg: "Elke vrijdag: de week in AI in vijf minuten, met hype-meter.", ook: [] as string[] },
  { href: "/plus", tekst: "Plus", uitleg: "Elke dag een korte dagbrief, en dossiers die één onderwerp grondig uitleggen.", ook: [] },
  { href: "/voor", tekst: "Voor jou", uitleg: "Alleen wat jouw sector raakt: onderwijs, werk, gemeenten, zelfstandigen, bibliotheken, burgers.", ook: [] },
  { href: "/wat-kan-ai", tekst: "Wat kan AI al?", uitleg: "Demo's en praktijkvoorbeelden, met wat ze niet tonen.", ook: [] },
  { href: "/gratis", tekst: "Gratis", uitleg: "Gratis tools zoals de Plakcheck, en open lespakketten en een AI-cursus om zelf te geven.", ook: ["/plakcheck", "/materiaal"] },
  { href: "/naslag", tekst: "Naslag", uitleg: "AI Act-kompas, jargonfilter, fiches en terugblik.", ook: ["/ai-act", "/jargon", "/fiches", "/terugblik"] },
];

// Wat onder "Naslag" valt (pagina /naslag en de startpagina).
export const NASLAG = [
  { href: "/ai-act", tekst: "AI Act-kompas", uitleg: "Wat de Europese AI-wet betekent voor jou, en wat wanneer geldt." },
  { href: "/jargon", tekst: "Jargonfilter", uitleg: "AI-termen in gewoon Nederlands." },
  { href: "/fiches", tekst: "Fiches", uitleg: "Praktische checklists om morgen mee aan de slag te gaan." },
  { href: "/terugblik", tekst: "Terugblik", uitleg: "Klopte onze hype-meter achteraf? Elk kwartaal kijken we terug." },
];
