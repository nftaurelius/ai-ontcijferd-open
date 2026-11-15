import { alleEdities, type Editie, type Onderwerp } from "./edities";

export const DOELGROEPEN = [
  { label: "Onderwijs", slug: "onderwijs", wie: "leraren, directies en ouders", vraag: "Wat verandert er in de klas, voor leerlingen en leraren?" },
  { label: "Werk", slug: "werk", wie: "werknemers, werkgevers en HR", vraag: "Welke taken en jobs verschuiven, en hoe snel?" },
  { label: "Lokale overheden", slug: "lokale-overheden", wie: "steden, gemeenten en OCMW's", vraag: "Wat moet een stad of gemeente nu weten of beslissen?" },
  { label: "Zelfstandigen", slug: "zelfstandigen", wie: "zelfstandigen en kmo's", vraag: "Wat kun je er morgen mee, en waar moet je op letten?" },
  { label: "Bibliotheken", slug: "bibliotheken", wie: "bibliotheken en cultuurwerkers", vraag: "Wat betekent dit voor informatie, lezen en digitale geletterdheid?" },
  { label: "Burgers", slug: "burgers", wie: "iedereen", vraag: "Wat merk jij ervan in je dagelijks leven, en wat zijn je rechten?" },
] as const;

export type Doelgroep = (typeof DOELGROEPEN)[number];

export function onderwerpenVoor(label: string): { editie: Editie; onderwerp: Onderwerp }[] {
  const uit: { editie: Editie; onderwerp: Onderwerp }[] = [];
  for (const editie of alleEdities()) {
    for (const onderwerp of editie.onderwerpen) {
      if (onderwerp.labels.some((l) => l.toLowerCase() === label.toLowerCase())) uit.push({ editie, onderwerp });
    }
  }
  return uit;
}
