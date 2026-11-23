# Bijdragen aan AI Ontcijferd

Dank je om mee te helpen. AI Ontcijferd is een project van één eindredacteur, Duncan Panis, met AI-agents. Wat je
hieronder leest, maakt het voor jou en voor ons eenvoudig.

## Een fout melden

Een verkeerd cijfer, een verouderde regel, een bron die niet zegt wat wij schrijven, een kapotte link: open een issue
met het sjabloon **Fout melden**, of mail naar redactie@aiontcijferd.be. Zet erbij:

- de pagina (link);
- wat er staat en wat het volgens jou moet zijn;
- een bron, als je die hebt.

Een fout verbeteren we altijd. Elke verbetering komt op [Correcties](https://aiontcijferd.be/correcties).

## Een bron of een voorbeeld voorstellen

Een nieuwsbron die we missen, een onderzoek, of een Vlaams of Belgisch voorbeeld van AI in de praktijk: gebruik het
sjabloon **Bron of voorbeeld voorstellen**. Een video of een post op sociale media is voor ons een signaal, geen bron:
zet er de oorspronkelijke bron bij als je die vindt.

## Code of inhoud verbeteren

- Deze publieke repo is een kopie van onze werkrepo. Een pull request voegen we hier niet samen; we nemen een goed
  voorstel over in de werkrepo, met vermelding van wie het indiende (in de commit en, voor inhoud, in "Zo is dit
  gemaakt"). Daarna verschijnt het hier met de volgende kopie.
- Houd een pull request klein: één verbetering per keer.
- **Inhoud** volgt het redactiestatuut in [`prompts/statuut.md`](prompts/statuut.md): standaard Nederlands, droog en
  helder, geen superlatieven, elke bewering met een bron.
- **Code:** test de site met `cd site && npm run build` en de keten met `AIO_DROOG=1` (zie de LEESMIJ).
- **Tools** in `site/public/` maken geen netwerkverbindingen. Gegevens die veranderen (prijzen, regels) krijgen een bron,
  een datum en een status.

## Wat we niet overnemen

- Persoonlijke gegevens, ook niet in voorbeelden.
- Reclame, verdienlinks of gesponsorde inhoud.
- Materiaal met het merk of de gegevens van één organisatie: hier staat alleen de algemene versie.

## Licentie van je bijdrage

Door bij te dragen ga je ermee akkoord dat je bijdrage onder dezelfde licentie valt als de rest: MIT voor code,
CC BY 4.0 voor inhoud.

## Gedrag

Wees correct en to the point. Issues zijn openbaar: zet er geen persoonlijke gegevens in, ook niet van anderen.
