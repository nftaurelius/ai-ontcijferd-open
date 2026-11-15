// Kleine hulpjes voor de opmaak.

/**
 * Zet de markeerstift alleen op de eerste zin van een korte HTML-alinea.
 * Een hele gemarkeerde alinea leest als één gele muur; de markeerstift is er
 * voor wat er het meest toe doet. Lukt het splitsen niet veilig (bv. een zin
 * die binnen een link eindigt), dan blijft de alinea ongemarkeerd.
 */
export function markeerEerste(alineaHtml: string): string {
  const binnen = alineaHtml.trim().replace(/^<p>|<\/p>$/g, "").trim();
  const m = binnen.match(/^([\s\S]*?[.!?])(\s+)(?=[A-ZÀ-Ý"“‘'])/);
  if (!m) return `<span class="markeer">${binnen}</span>`;
  const eerste = m[1];
  const open = (eerste.match(/<[a-z]/gi) ?? []).length;
  const dicht = (eerste.match(/<\//g) ?? []).length;
  if (open !== dicht) return binnen;
  return `<span class="markeer">${eerste}</span>${m[2]}${binnen.slice(m[0].length)}`;
}

/** Een dagbrieftitel als "A / B / C" uit elkaar halen tot losse onderwerpen. */
export function splitsTitel(titel: string): string[] {
  return titel.split(/\s+\/\s+/).map((t) => t.trim()).filter(Boolean);
}

/**
 * Het blok "Waarom doet het ertoe voor Vlaanderen?" (weekeditie) of "Voor wie:" (dagbrief)
 * is het hart van elk onderwerp. Zet het in een kader zodat het er bij het scrollen uitspringt.
 */
export function kaderVlaanderen(html: string): string {
  return html.replace(
    /<p><strong>(Waarom doet het ertoe voor Vlaanderen\?|Voor wie:)<\/strong><\/p>\s*(<ul>[\s\S]*?<\/ul>)/g,
    (_, kop: string, lijst: string) => `<div class="vlaanderen"><p class="vlaanderen-kop">${kop.replace(/:$/, "")}</p>${lijst}</div>`,
  );
}
