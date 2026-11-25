// Algemene instellingen van de site.
export const CONTACT_EMAIL = "redactie@aiontcijferd.be"; // stel doorsturing in bij Combell
export const LINKEDIN = ""; // url van de LinkedIn-pagina van AI Ontcijferd, als die er is

// Hoofdmenu: de vier ingangen uit de visie (Volgen, Leren, Doen, Lesgeven) en de doelgroepen dwars erdoor.
// `ook` = paden die onder dezelfde ingang vallen (voor de markering in het menu).
export const MENU = [
  { href: "/volgen", tekst: "Volgen", uitleg: "Wat gebeurt er? De Stand van AI, de dagbrief, dossiers en praktijkvoorbeelden.", ook: ["/edities", "/plus", "/wat-kan-ai", "/terugblik"] },
  { href: "/leren", tekst: "Leren", uitleg: "Hoe werkt het? Begin hier, het AI Act-kompas en de jargonfilter.", ook: ["/begin-hier", "/vragen", "/niveaucheck", "/ai-act", "/jargon", "/naslag", "/wegwijzer"] },
  { href: "/doen", tekst: "Doen", uitleg: "Wat kan ik ermee? De Plakcheck, bijsluiters van AI-tools, prompts en skills, en fiches.", ook: ["/plakcheck", "/bijsluiters", "/werkwijzen", "/fiches", "/gratis"] },
  { href: "/lesgeven", tekst: "Lesgeven", uitleg: "Hoe geef ik het door? Open lespakketten om zelf te geven, en alles om over te nemen.", ook: ["/materiaal", "/overnemen"] },
  { href: "/voor", tekst: "Voor jou", uitleg: "Alleen wat jouw sector raakt: onderwijs, werk, gemeenten, zelfstandigen, bibliotheken, burgers.", ook: [] as string[] },
];

// Wat onder elke ingang staat (de pagina's /volgen, /leren, /doen, /lesgeven en de startpagina).
export type IngangItem = { href: string; tekst: string; uitleg: string; ritme?: string };
export const INGANGEN: Record<string, { titel: string; vraag: string; lead: string; items: IngangItem[] }> = {
  volgen: {
    titel: "Volgen",
    vraag: "Wat gebeurt er?",
    lead: "Het nieuws over AI, zonder hype, met wat het betekent voor Vlaanderen.",
    items: [
      { href: "/edities", tekst: "Stand van AI", uitleg: "De week in AI in vijf minuten, met een hype-meter per onderwerp.", ritme: "Elke vrijdag" },
      { href: "/plus", tekst: "Dagbrief en dossiers", uitleg: "Elke dag een korte dagbrief met een status per onderwerp, en dossiers die één ontwikkeling grondig uitleggen.", ritme: "Elke dag" },
      { href: "/wat-kan-ai", tekst: "Wat kan AI al?", uitleg: "Demo's en praktijkvoorbeelden, met bron en wat ze niet tonen." },
      { href: "/terugblik", tekst: "Terugblik", uitleg: "Klopte onze hype-meter achteraf? Elk kwartaal kijken we terug." },
      { href: "/nieuwsbrief", tekst: "Nieuwsbrief", uitleg: "De Stand van AI elke vrijdag in je mailbox. Gratis." },
    ],
  },
  leren: {
    titel: "Leren",
    vraag: "Hoe werkt het?",
    lead: "Wat AI is, wat het kan en niet kan, en welke regels gelden. In gewoon Nederlands.",
    items: [
      { href: "/begin-hier", tekst: "Begin hier", uitleg: "Nieuw in AI? In tien minuten wat je moet weten, en waar je verder kunt." },
      { href: "/vragen", tekst: "Vragen over AI", uitleg: "Mag ik dit in een chatbot plakken? Is die video echt? Echte vragen met een nagekeken antwoord." },
      { href: "/niveaucheck", tekst: "Niveaucheck", uitleg: "Vijf vragen met ja of nee: op welk niveau sta je met AI, en wat leer je hierna?" },
      { href: "/ai-act", tekst: "AI Act-kompas", uitleg: "Wat de Europese AI-wet betekent voor jou, en wat wanneer geldt." },
      { href: "/jargon", tekst: "Jargonfilter", uitleg: "AI-termen in gewoon Nederlands." },
      { href: "/cursus", tekst: "AI-cursus", uitleg: "Leren werken met AI door het te doen: vier delen, tien modules, online of als PDF." },
      { href: "/wegwijzer", tekst: "Wegwijzer", uitleg: "Waar je elders in Vlaanderen terechtkunt: richtlijnen, lesmateriaal, opleidingen en hulp, nagekeken." },
    ],
  },
  doen: {
    titel: "Doen",
    vraag: "Wat kan ik ermee?",
    lead: "Gratis gereedschap om morgen verstandig met AI aan de slag te gaan.",
    items: [
      { href: "/plakcheck", tekst: "Plakcheck en Urenrekening", uitleg: "Mag dit in een chatbot? En loont het dan nog? Alles draait in je browser." },
      { href: "/bijsluiters", tekst: "Bijsluiters van AI-tools", uitleg: "Wat ChatGPT, Claude, Gemini, Copilot en Mistral met je invoer doen, en wat ze kosten." },
      { href: "/werkwijzen", tekst: "Werkwijzen", uitleg: "Prompts, skills en agents om AI verstandig te gebruiken, met wat je zelf nakijkt." },
      { href: "/fiches", tekst: "Fiches", uitleg: "Praktische checklists om af te drukken." },
    ],
  },
  lesgeven: {
    titel: "Lesgeven",
    vraag: "Hoe geef ik het door?",
    lead: "Alles om zelf een sessie over AI te geven, ook als je geen expert bent. Gratis en aan te passen.",
    items: [
      { href: "/materiaal", tekst: "Open lespakketten", uitleg: "Draaiboek, presentatie en werkbladen per sessie, onder Creative Commons." },
      { href: "/materiaal/ai-geletterdheid-in-een-doos", tekst: "AI-geletterdheid in een doos", uitleg: "In één uur afspraken maken over AI met je collega's of vrijwilligers. Voor artikel 4 van de AI Act." },
      { href: "/materiaal/gebruiken", tekst: "Zo pas je een pakket aan", uitleg: "Met AI op maat van je eigen organisatie en publiek, in zes stappen." },
      { href: "/overnemen", tekst: "Neem het over", uitleg: "Teksten, fiches en tools overnemen in je eigen nieuwsbrief, blad of intranet." },
    ],
  },
};

// Wat onder "Naslag" valt (pagina /naslag en de startpagina).
export const NASLAG = [
  { href: "/ai-act", tekst: "AI Act-kompas", uitleg: "Wat de Europese AI-wet betekent voor jou, en wat wanneer geldt." },
  { href: "/jargon", tekst: "Jargonfilter", uitleg: "AI-termen in gewoon Nederlands." },
  { href: "/fiches", tekst: "Fiches", uitleg: "Praktische checklists om morgen mee aan de slag te gaan." },
  { href: "/terugblik", tekst: "Terugblik", uitleg: "Klopte onze hype-meter achteraf? Elk kwartaal kijken we terug." },
];
