// Kopieerknoppen: <button data-kopieer="id-van-element">. Kopieert de tekst (of de waarde van een tekstveld).
export function koppelKopieerknoppen() {
  document.querySelectorAll<HTMLButtonElement>("[data-kopieer]").forEach((knop) =>
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
    }),
  );
}
