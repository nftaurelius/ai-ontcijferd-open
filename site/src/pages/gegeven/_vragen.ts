// De vragen van "Gaf je dit pakket?" en de kant-en-klare mail. Gedeeld door /gegeven en /gegeven/<slug>.
export const VRAGEN = [
  ["Waar gaf je het?", "Soort organisatie en gemeente volstaan: een school in Aalst, een bibliotheek, een vereniging."],
  ["Voor wie, en met hoeveel?", "Bijvoorbeeld: twaalf senioren, een lerarenteam van twintig, de gemeenteraad."],
  ["Wat werkte?", "Een oefening, een voorbeeld, een vraag die het gesprek opende."],
  ["Wat liep mis of duurde te lang?", "Ook kleine dingen: een dia die niet klopte, een oefening die niemand begreep."],
  ["Wat paste je aan?", "Wat je schrapte, toevoegde of anders deed. Daar leren we het meest van."],
  ["Mogen we het vermelden?", "Bijvoorbeeld als 'gegeven in een bibliotheek in Oost-Vlaanderen'. Zonder jouw akkoord vermelden we niets."],
] as const;

export function mailto(titel: string, versie?: string): string {
  const onderwerp = `Ik gaf ${titel}${versie ? ` (versie ${versie})` : ""}`;
  const romp = VRAGEN.map(([v]) => `${v}\n\n`).join("\n");
  return `mailto:redactie@aiontcijferd.be?subject=${encodeURIComponent(onderwerp)}&body=${encodeURIComponent(romp)}`;
}
