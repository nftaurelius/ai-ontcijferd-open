// Kleine hulpjes voor tekst op de site.

/** "1 onderwerp", "3 onderwerpen". */
export function aantal(n: number, enkelvoud: string, meervoud: string): string {
  return `${n} ${n === 1 ? enkelvoud : meervoud}`;
}

/**
 * Kort een tekst in zonder midden in een woord te stoppen.
 * Eindigt er binnen de limiet een zin (en is die niet te kort), dan stopt de tekst daar.
 * Anders breekt hij af op de laatste spatie, met een beletselteken.
 */
export function inkorten(tekst: string, max: number): string {
  const schoon = tekst.trim();
  if (schoon.length <= max) return schoon;
  const stuk = schoon.slice(0, max + 1);
  const zinseinde = Math.max(stuk.lastIndexOf(". "), stuk.lastIndexOf("? "), stuk.lastIndexOf("! "));
  if (zinseinde >= max * 0.5) return stuk.slice(0, zinseinde + 1);
  const spatie = stuk.lastIndexOf(" ");
  return `${stuk.slice(0, spatie > 0 ? spatie : max).replace(/[\s,;:–-]+$/, "")}…`;
}
