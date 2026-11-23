// Kopieerknoppen: <button data-kopieer="id-van-element">. Kopieert de tekst (of de waarde van een tekstveld).
export function koppelKopieerknoppen() {
  // Mag meer dan eens per pagina worden opgeroepen: een knop wordt maar één keer gekoppeld.
  document.querySelectorAll<HTMLButtonElement>("[data-kopieer]:not([data-gekoppeld])").forEach((knop) => {
    knop.dataset.gekoppeld = "1";
    knop.addEventListener("click", async () => {
      const bron = document.getElementById(knop.dataset.kopieer ?? "");
      if (!bron) return;
      const tekst = bron instanceof HTMLTextAreaElement || bron instanceof HTMLInputElement ? bron.value : (bron.textContent ?? "");
      const oud = knop.textContent;
      try {
        await navigator.clipboard.writeText(tekst);
        knop.textContent = "Gekopieerd";
      } catch {
        if (bron instanceof HTMLTextAreaElement || bron instanceof HTMLInputElement) {
          bron.focus();
          bron.select();
        } else {
          const r = document.createRange();
          r.selectNodeContents(bron);
          getSelection()?.removeAllRanges();
          getSelection()?.addRange(r);
        }
        knop.textContent = "Geselecteerd: kopieer met Ctrl+C";
      }
      setTimeout(() => (knop.textContent = oud), 2500);
    });
  });
}
