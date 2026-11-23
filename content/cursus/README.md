# De AI-cursus

Geschreven door Duncan Panis. Licentie: CC BY 4.0 (zoals de rest van de inhoud).

- `src/`: de bron, één tekstbestand per deel, in een lichte eigen opmaak (koppen met `#`, blokken met `:::soort`, figuren met `:::fig`).
- `bouw/build.py`: maakt de PDF's in de huisstijl (`python3 build.py all`). Ze komen in `content/materiaal/ai-cursus/bestanden/`, samen met de volledige band.
- `bouw/web.py`: zet de bron om in JSON voor de website (`content/cursus/web/`). De site toont de cursus op `/cursus`.
- `bouw/assets/`: de stijl van de PDF (`cursus.css`), de schema's (`diagrams.py`) en de lettertypen Literata en Atkinson Hyperlegible Next (SIL Open Font License).

Na een wijziging in `src/`: draai beide scripts (nodig: Python 3, `weasyprint`, `pypdf`) en commit de bron, de JSON en de PDF's samen.
