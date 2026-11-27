# Bouwplan AI Ontcijferd

Stand: 25 november 2026. Dit is de prioriteitenlijst voor alles wat we nog bouwen. Ze vertrekt van drie dingen:

- **De visie** (`data/visie.md`): de open plek waar Vlaanderen AI leert begrijpen, gebruiken en doorgeven.
- **Het doelgroepenonderzoek** (25/11, samenvatting in `data/doelgroepenonderzoek.md`, volledig rapport:
  https://claude.ai/artifact/Gt2kxBra22Xz3j2ViAAG5Q): acht vragen die bij elke doelgroep terugkomen.
- **Het verspreidingsplan** (`data/verspreidingsplan.md`): start naar buiten op 4 januari 2027.

## Zo gebruik je dit plan

- Elk item heeft een nummer (B01, B02...). Zeg "bouw B04" en de agent weet wat te doen.
- Zonder andere opdracht neemt een bouwsessie **het eerste open item van de laagste fase** dat niet op Duncan wacht.
- Klaar = alles onder "Klaar als" staat online of in de repo. Vink af met datum en PR-nummer.
- Items met **wacht op Duncan** start een agent niet zelf; hij bereidt hoogstens voor.
- **We hangen niet af van anderen** (beslist door Duncan op 25/11). We bouwen, testen en verbeteren zelf zo ver het
  gaat; feedback van gebruikers stuurt bij (B26). Een tester, leraar of partner is welkom, maar nooit een voorwaarde
  om iets te bouwen of te publiceren. "Getest" zegt altijd eerlijk wie testte: de redactie, een gebruiker die
  feedback gaf, of iemand in de praktijk.
- **Poorten zijn meetpunten, geen voorwaarden.** Ze zeggen hoe ver we staan; ze houden het bouwen niet tegen.
- Elk nieuw stuk volgt de vaste regels: bijsluiter (voor wie, niveau, duur, laatst nagekeken, licentie, versie),
  bron en datum bij alles wat verandert, huisstijl 1.0, CC BY 4.0, en "getest" altijd eerlijk.
- Nieuwe inzichten of ideeën: bij `data/ideeen.md`, en pas in dit plan als Duncan ze een plaats geeft.

## Hoe we kiezen

Elk item scoort op vijf vragen. Hoe meer ja, hoe vroeger.

1. **Bereik:** bedient het meer dan één doelgroep, of een van de drie sterkste dwarsvragen (plakken, echt, afspraken)?
2. **Bewijs:** staat de nood er stevig in het onderzoek?
3. **Venster:** is er nu een moment dat later voorbij is (4 januari, eindtermen, Digitale Week, fraudeplan)?
4. **Hefboom:** kunnen anderen het overnemen of geven, zodat het zichzelf verspreidt?
5. **Haalbaar zonder Duncan:** kunnen agents het maken, zodat Duncans halfuur per week vrij blijft voor wat alleen hij kan?

## De kaart: acht vragen, wat we hebben, wat ontbreekt

| Dwarsvraag | Wat er al staat | Wat ontbreekt | Items |
| --- | --- | --- | --- |
| 1. Wat mag ik erin plakken? | Plakcheck, bijsluiters, pakket "Chatbot zonder risico" | Antwoorden per concrete vraag; versie voor het loket van een gemeente | B02, B06 |
| 2. Is dit echt? | Pakket "Echt of nep?", wegwijzer (Child Focus, EBA) | Papierversie in klare taal; oplichting gericht op zaken; aansluiting bij het fraudeplan | B05, B14 |
| 3. Welke afspraken maken we? | Doos artikel 4 (met afsprakenkaart), fiche en pakket voor scholen | Eén afsprakenkaart-maker met versies voor klas, werk, gemeente, vereniging en gezin | B03 |
| 4. Hoe leer ik het zonder tijd of expertise? | Proeverij, niveaucheck, cursus, Begin hier, draaiboeken | "Zo geef je dit" met de vragen die het publiek stelt; korte vormen | B02, B09 |
| 5. Denk ik nog zelf? | Pakket "Wanneer geen AI?", essays in "Verder denken" | Materiaal voor studenten en scholieren | B16 |
| 6. Wat heb ik eraan? | Wat kan AI al?, niveaucheck | Een uur AI per soort zaak; AI per job | B10, B12 |
| 7. Wat zegt de wet, wie houdt toezicht? | AI Act-kompas (Omnibus juist verwerkt), dossier 2 december | Duidelijk stuk over artikel 4 na de Omnibus; vragen voor raadsleden | B01, B06 |
| 8. Wat met mijn job? | Dagbrief en edities (Werk) | Stand per thema "werk"; AI per job | B12, B20 |

Leemtes waar niemand meet: verenigingen, bibliotheekmedewerkers, raadsleden en eenmanszaken (B11).

---

## Fase 1. Tot 4 januari 2027: de start versterken

Doel: wie op 4 januari komt, vindt antwoorden op de drie sterkste vragen. Alles hier kunnen agents maken; naar
buiten gaat niets voor 4 januari.

### B01 · Artikel 4 na de Omnibus: wat moet je nog? ✓ (26/11: fiche online, kompas, doos en vragenbank verwijzen ernaar)
- **Voor wie:** werkgevers, HR, directies, gemeenten, verenigingen met personeel. Dwarsvraag 7.
- **Waarom:** de Omnibus paste artikel 4 in juli 2026 aan; werkgevers krijgen tegenstrijdige uitleg ("de plicht viel
  weg" tegenover "de plicht blijft, zonder vast niveau"). Ons kompas heeft het juist. Snel stuk met gezag.
- **Vorm:** fiche "Artikel 4 na de Omnibus" (een pagina, afdrukbaar) plus een kader in het AI Act-kompas; verwijst
  naar de doos als praktische invulling. Optioneel later een dossier (dan met "Mijn inschatting").
- **Wie:** agents; tekst nakijken bij de Europese Commissie en in de Omnibus-tekst.
- **Klaar als:** fiche online, kompas verwijst ernaar, bron en datum erbij, opgenomen in de vragenbank (B02).

### B02 · De vragenbank: elke echte vraag een eigen pagina ✓ (25/11: eerste 24 vragen online)
- **Voor wie:** iedereen; de ingang voor wie geen AI-les wil maar een antwoord. Alle dwarsvragen.
- **Waarom:** het onderzoek levert ruim veertig echte vragen per doelgroep. Een pagina per vraag helpt mensen,
  zoekmachines en chatbots (motor 3 van het verspreidingsplan). De grootste groep wil een antwoord op een eigen vraag.
- **Vorm:** `content/vragen/<slug>.md` met vraag, kort antwoord (drie zinnen), uitleg, wat je doet, links naar tool,
  pakket en wegwijzer, doelgroepen, dwarsvraag, bron, nagekeken op, status. Pagina `/vragen` (filter per doelgroep en
  dwarsvraag) en `/vragen/<slug>`, met FAQ-gegevens voor zoekmachines. Lezersvragen komen er later ook in.
- **Eerste lading:** 24 vragen, drie per dwarsvraag, uit het rapport; daarna 40, dan alles.
- **Wie:** agents (elk antwoord nagekeken met bron).
- **Klaar als:** 24 pagina's online, `/vragen` in het menu onder Leren, elke doelgroeppagina toont haar vragen.

### B03 · De afsprakenkaart-maker ✓ (26/11: tool v1.0.1 online, regels per context goedgekeurd door Duncan)
- **Voor wie:** klas, werk, gemeente, vereniging, gezin. Dwarsvraag 3, de ruggengraat volgens het onderzoek.
- **Waarom:** vijf doelgroepen vragen hetzelfde: een korte regeling van wat wel en niet mag. Eén gereedschap bedient ze
  allemaal. 62% van de scholieren ziet regels per leraar verschillen; 35% van de bediendes werkt zonder kader.
- **Vorm:** gratis tool zoals de Plakcheck (één HTML-bestand, geen netwerkverkeer, `ao-config` met bron en datum):
  kies je context, beantwoord acht vragen, krijg een afsprakenkaart van één pagina om af te drukken of te delen
  (deellink `#p=`). Vertrekt van de afsprakenkaart uit de doos. Versie voor het gezin = basis voor "AI thuis" (B13).
- **Wie:** agents; Duncan kijkt de regels per context na (redactionele keuzes).
- **Klaar als:** tool op `/afsprakenkaart`, in `TOOLS`, op `/gratis` en `/doen`, testpaneel groen, doos en pakket
  "AI-afspraken op school" verwijzen ernaar.

### B04 · Waar AI Ontcijferd zelf van afhangt ✓ (26/11: blok op /zo-werken-we#afhankelijkheden)
- **Voor wie:** iedereen; eigen voorbeeld voor het thema digitale soevereiniteit (B17).
- **Waarom:** open en transparant zijn onze kernwaarden. We vragen organisaties hun afhankelijkheid te kennen; dan
  tonen we de onze.
- **Vorm:** blok op `/zo-werken-we`: Vercel, GitHub, Brevo, Combell, de modellen van Anthropic, OpenAI en xAI, wat
  elk doet, wat er gebeurt als het wegvalt, en de uitweg.
- **Wie:** agents. **Klaar als:** online, met datum.

### B05 · Echt of nep: van pakket naar gereedschap voor iedereen ✓ (26/11: twee fiches, drie vragen, pakket en wegwijzer gekoppeld)
- **Voor wie:** burgers, senioren, ouders, zelfstandigen. Dwarsvraag 2, het sterkste bewijs (85% vreest nepinformatie).
- **Waarom:** het federale fraudeplan (november 2026) legt volgens de berichtgeving niet uit hoe AI oplichting
  geloofwaardiger maakt. Wie het meest kwetsbaar is, leest liever op papier.
- **Vorm:** (a) een fiche "Is dit echt?" van één A4 in klare taal, om af te drukken in bibliotheek, OCMW of
  seniorenvereniging; (b) een fiche "AI-oplichting gericht op je zaak" (valse facturen, nagemaakte stem van een
  leverancier); (c) een vraag per vorm van oplichting in de vragenbank; (d) het pakket verwijst naar beide.
- **Wie:** agents; klare taal volgens de werkwijze "klare-taal".
- **Klaar als:** twee fiches online en afdrukbaar, gekoppeld aan het pakket en de wegwijzer.

### B06 · Twee fiches voor gemeenten ✓ (26/11: raad en loket, briefing en portaal verwijzen ernaar)
- **Voor wie:** raadsleden en medewerkers van lokale besturen. Dwarsvragen 1, 3 en 7.
- **Waarom:** over raadsleden bestaat geen enkele meting; wie beslist over een AI-project kreeg er meestal geen
  vorming over. Medewerkers van kleine gemeenten vallen buiten de door Vlaanderen betaalde Copilot-licenties en
  gebruiken vaak gratis publieke tools.
- **Vorm:** "Tien vragen bij een AI-voorstel in de raad" en "AI aan het loket" (wat mag, wat nooit, hoe help je een
  inwoner die een AI-brief of nepbericht niet vertrouwt). Gekoppeld aan de briefing voor raadsleden.
- **Wie:** agents. **Klaar als:** twee fiches online, briefing en portaal Lokale overheden verwijzen ernaar.

### B07 · Jaaroverzicht 2026
- Staat al gepland (geplande taken 21/12, 28/12, 30/12, 4/1). Duncan schrijft "Mijn inschatting" eind december
  (ingepland).

### B26 · Feedback van gebruikers op elk stuk ✓ (25/11: vragen, fiches, Plakcheck)
- **Voor wie:** iedereen die iets van ons gebruikt. Nodig omdat we niet afhangen van externe testers.
- **Waarom:** zo leren we wat werkt zonder dat iemand ons eerst moet testen. Elke reactie wordt een verbetering.
- **Vorm:** onder elke vraag, fiche, taakkaart, tool en pakket een klein blok "Werkte dit voor jou?" met twee knoppen
  en een mailto naar de redactie (onderwerp met de naam en versie van het stuk; geen formulier, geen opslag, privacy
  ongewijzigd). `/gegeven/<slug>` blijft voor pakketten. Een logboek `data/feedback.md` (privé, in
  `spiegel/uitsluiten.txt`): datum, stuk, wat de gebruiker zei (zonder naam), wat we aanpasten. Elke maand verwerken;
  een stuk met feedback krijgt bij "getest" ook "aangepast na feedback van gebruikers (datum)".
- **Wie:** agents. **Klaar als:** component `WerkteDit.astro` op vragen, fiches en tools; logboek en werkwijze in
  CLAUDE.md.

**Poort fase 1:** startlijst nagekeken op 28 december; B01 tot B06 en B26 online of bewust verschoven.

---

## Fase 2. Januari en februari 2027: naar buiten, en de portalen vullen

Doel: elk doelgroepportaal toont zijn vragen, een pakket, een tool, werkwijzen en de wegwijzer. De verspreiding
start (voorstellen, KlasCement, LinkedIn).

### B08 · Lespakket "AI in het zesde leerjaar"
- **Voor wie:** leraren lager onderwijs, ook zonder AI-ervaring. Dwarsvraag 4.
- **Waarom:** de nieuwe eindtermen gaan stapsgewijs in vanaf schooljaar 2026-2027; tegen het einde van het zesde
  leerjaar weten leerlingen wat AI is en schrijven ze een goede prompt in een tool van de school. Meer dan de helft
  van de leraren zonder AI voelt zich overweldigd. Een kant-en-klaar pakket is schaars. Het venster loopt nu.
- **Vorm:** twee lessen van 50 minuten met draaiboek in gewone woorden, dia's, werkblad, klasafsprakenkaart (B03),
  de vragen die kinderen stellen, en een versie zonder schermen. Eerst nakijken hoe de eindtermen precies ingevoerd
  worden per leerjaar.
- **Wie:** agents; de redactie test zelf (de les doorlopen als leraar en als leerling, elke prompt uitproberen in de
  tools die scholen aanbieden, nagaan tegen de eindtermen). Een klas via contacten van de bib kan later, maar is geen
  voorwaarde.
- **Klaar als:** pakket op `/materiaal` met "getest door de redactie" en feedbackblok (B26); op KlasCement vanaf
  4 januari.

### B09 · "Zo geef je dit" bij elk pakket
- **Voor wie:** lesgevers zonder AI-achtergrond. Dwarsvraag 4.
- **Waarom:** lesgevers hebben geen expertise nodig maar houvast: een draaiboek, de vragen van het publiek met een
  nagekeken antwoord, en een datum waarop het materiaal nagekeken is (LIBRA.I., Amai!).
- **Vorm:** per pakket een blok "Zo geef je dit": de tien vragen die je krijgt (uit de vragenbank), wat je doet als
  het misloopt, een werkvorm die toont in plaats van vertelt (zoals een deepfake van de lesgever, met toestemming).
- **Wie:** agents. **Klaar als:** alle beschikbare pakketten hebben het blok.

### B10 · Een uur AI voor je zaak
- **Voor wie:** zelfstandigen en kleine zaken. Dwarsvraag 6.
- **Waarom:** 72,5% van de Vlaamse bedrijven noemt een gebrek aan kennis als drempel; bouw, transport en horeca
  gebruiken het minst AI. UNIZO vraagt een aanspreekpunt, geen expertise.
- **Vorm:** één sjabloon voor een sessie van een uur, met een versie per sector (eerst bouw en winkel, daarna kapper,
  horeca, boekhouder): wat kan het in jouw zaak, wat plak je er niet in, oplichting gericht op je zaak (B05).
- **Wie:** agents. **Klaar als:** pakket met twee sectorversies online.

### B11 · Meten waar niemand meet
- **Voor wie:** verenigingen, bibliotheekmedewerkers, raadsleden, eenmanszaken.
- **Waarom:** vier groepen zonder enige meting. Een open bevraging levert materiaal, gezag en een reden om met een
  koepel te praten.
- **Vorm:** vier korte vragenlijsten (tien vragen, vijf minuten), zonder persoonsgegevens; de resultaten onder CC BY
  op de site, met de ruwe antwoorden. Vragenlijst in de eigen site (geen externe verwerker) of via een koepel.
- **Wie:** agents maken vragenlijst en privacytekst nu. Verspreiden vanaf 4 januari (akkoord Duncan 25/11), via
  De Federatie, Socius, VVBAD, VVSG, UNIZO; Duncan verstuurt, zoals elke mail naar een organisatie.
- **Klaar als:** eerste bevraging gesloten en resultaten gepubliceerd.

### B12 · AI per job: proef met drie jobs
- **Goedgekeurd door Duncan op 25/11.** Geen externe testers nodig: de redactie kiest de jobs en test elke taakkaart
  zelf; feedback van gebruikers (B26) stuurt bij.
- **Voor wie:** wie met een concrete taak komt. Dwarsvragen 6 en 8.
- **Vorm:** taakkaarten (één taak, wat AI wel en niet kan, werkwijze, wat je niet plakt, niveau, regels, "getest") en
  een jobpagina per job, onder het doelgroepportaal. Bronnen voor taken: de vragen per rol uit het onderzoek, de AI
  Radar van Digitaal Vlaanderen, de vragenbank.
- **Keuze van de eerste drie jobs:** waar het onderzoek de duidelijkste vragen per rol geeft en waar wij al materiaal
  hebben: medewerker van een gemeente (loket en communicatie), leraar secundair, zelfstandige met een kleine zaak.
- **Testen door de redactie:** elke taak echt uitvoeren met een verzonnen maar realistisch voorbeeld (nooit echte
  gegevens), in minstens twee gratis tools, en noteren wat werkte en wat niet. Dat staat bij "getest".
- **Klaar als:** drie jobpagina's met elk vijf taakkaarten, getest door de redactie, met feedbackblok (B26).

### B13 · AI thuis
- **Voor wie:** ouders. Geen enkel aanbod voor hen bij ons, en weinig elders.
- **Waarom:** kinderen gebruiken chatbots niet alleen voor huiswerk; sommigen praten er makkelijker mee over persoonlijke
  zaken dan met mensen. Ouders vragen wat hun kind ermee doet en welke afspraken ze thuis maken.
- **Vorm:** gesprekskaart voor ouder en kind, gezinsafsprakenkaart (uit B03), een pagina voor een ouderavond op school.
- **Wie:** agents. **Klaar als:** pakket online, Gezinsbond in het contactenboek met dit als aanbod.

### B14 · De doelgroepportalen afmaken
- **Voor wie:** alle zes doelgroepen.
- **Vorm:** elke `/voor/<doelgroep>` toont bovenaan "Wat mensen hier vragen" (uit B02), daarna het pakket, de tool en
  de werkwijzen die passen, dan het nieuws en de wegwijzer. Een zevende portaal voor verenigingen overwegen na B11.
- **Klaar als:** poort van fase "Naar buiten" uit de visie: elk portaal toont een pakket, een tool en werkwijzen.

### B15 · Verspreiding, stap 2 (uit het verspreidingsplan)
- De Speurder, de Voorsteller, de maandelijkse samenvatting per doelgroep, de chatbot-test bij de chatbots zelf.

**Poort fase 2:** iemand anders dan Duncan gaf de proeverij; elk portaal toont een pakket, een tool en werkwijzen;
de eerste bevraging (B11) loopt.

---

## Fase 3. Voorjaar 2027 (maart tot juni): dieper en breder

### B16 · Studeren en leren zonder je denken uit te besteden
- **Voor wie:** studenten en scholieren. Dwarsvraag 5 (53% van de 18- tot 24-jarige gebruikers denkt minder zelf;
  14% van de scholieren besteedt schoolwerk volledig uit).
- **Vorm:** het pakket "Studeren met AI" (staat in voorbereiding) afwerken, met de grens tussen hulp en fraude.

### B17 · Digitale soevereiniteit
- **Voor wie:** gemeenten, scholen, kmo's, verenigingen. Rol: wegwijzer en gereedschap, geen implementatiepartner.
- **Waarom:** 72% van de Belgische gemeenten draait e-mail op Microsoft; de VVSG vraagt collectieve regie.
  Koplopers (Schleswig-Holstein, LaSuite, openDesk) doen het samen, en het duurt jaren.
- **Vorm, in deze volgorde:** (a) dossier "Digitale soevereiniteit" met stand per thema; (b) afhankelijkheidsscan als
  tool (per functie: e-mail, documenten, identiteit, data, AI), met versie voor raadsleden; (c) bijsluiters voor open
  alternatieven (Nextcloud, LibreOffice, openDesk, lokale taalmodellen) in het bestaande formaat; (d) werkwijze
  "Zelf bouwen met AI: wanneer wel, wanneer niet"; (e) sessie van een uur voor besturen.
- **Grens:** geen uitvoering voor organisaties. Komt er ooit betaalde hulp, dan apart en vermeld op `/over`.

### B18 · AI in gewone taal
- **Voor wie:** laaggeletterden, senioren, wie digitaal kwetsbaar is (meer dan 70% van de laagopgeleiden).
- **Vorm:** "Echt of nep" in klare taal (uit B05), "AI als hulp bij een moeilijke brief" met wat je er nooit in zet,
  papier- en luisterversies van de belangrijkste fiches. Samen met basiseducatie of Ligo testen.

### B19 · Getest in de praktijk
- Elk pakket krijgt het label "Getest in de praktijk" (datum, plaats, aantal deelnemers) zodra iemand het gaf; opnames
  "Zo geef je dit"; de claimcheck; de proef van de AI-week.
- **Poort fase 3:** drie andere bibliotheken gaven een pakket.

### B20 · Stand per thema
- Blijvende pagina's die we bijwerken in plaats van nieuwe artikels: werk en jobs, onderwijs, de AI Act, digitale
  soevereiniteit. Voedt vraag 8 en de zoeklaag.

### B21 · AI voor je vereniging
- Pas na de bevraging (B11): pakket en afsprakenkaart voor verenigingsbesturen.

---

## Fase 4. Najaar 2027 en later

- **B22 · Vlaamse AI-week** in de bibliotheek, aansluitend bij de Digitale Week in oktober in plaats van een eigen
  datum; open draaiboek, met de koepels.
- **B23 · Sectorpakketten met partners** (zorg, bouw, cultuur), uit de proef "Een uur AI voor je zaak" en AI per job.
- **B24 · Redactie in een doos:** de pijplijn als open pakket voor wie zelf nuchter AI-nieuws wil maken.
- **B25 · Luisterversie en overneemblok** voor elke editie, als vaste onderdelen.

---

## Wat altijd doorloopt

| Ritme | Wat |
| --- | --- |
| Dagelijks | Dagbrief, verkenner, X-radar, IndexNow |
| Wekelijks | Stand van AI en nieuwsbrief (vrijdag), verpakker, meter en bronnencheck (maandag), wegwijzer-links |
| Maandelijks | Prijzen in de Plakcheck, chatbot-test (vanaf januari) |
| Elk kwartaal | Terugblik op de hype-meter, wegwijzer nakijken, regels van de Plakcheck nalezen |
| Bij AI Act-nieuws | AI Act-kompas en fiche artikel 4 (B01) nakijken |

## Wacht op Duncan

- "Mijn inschatting" voor het jaaroverzicht (B07): ingepland voor eind december.
- Versturen van de bevragingen (B11) en de voorstellen: vanaf 4 januari.

Beslist op 25/11: akkoord op AI per job (B12); geen externe testers als voorwaarde, wel feedback van gebruikers
(B26); een leraar via contacten van de bib kan later voor B08; bevragingen vanaf 4/1; ACV blijft in de wegwijzer.

## Volgorde voor de komende bouwsessies

1. ~~B02 · vragenbank, eerste 24 vragen, met B26~~ (klaar 25/11)
2. ~~B01 · fiche artikel 4 na de Omnibus~~ (klaar 26/11)
3. ~~B03 · afsprakenkaart-maker~~ (klaar 26/11)
4. ~~B05 · fiches "Is dit echt?" en "AI-oplichting gericht op je zaak"~~ (klaar 26/11)
5. ~~B06 · twee fiches voor gemeenten~~ (klaar 26/11)
6. ~~B04 · waar AI Ontcijferd van afhangt~~ (klaar 26/11)
7. B08 · pakket zesde leerjaar, getest door de redactie
8. B11 · vragenlijsten klaarzetten
9. B13 · AI thuis
10. B12 · AI per job, eerste drie jobs
11. B09, B10, B14 in januari

## Logboek

| Datum | Item | Wat | PR |
| --- | --- | --- | --- |
| 25/11/2026 | - | Bouwplan opgesteld uit visie, verspreidingsplan en doelgroepenonderzoek | #47 |
| 25/11/2026 | B12, B26 | Beslissingen Duncan: AI per job goedgekeurd, niet afhangen van anderen, B26 toegevoegd | #48 |
| 25/11/2026 | B02, B26 | Vragenbank: 24 vragen (drie per dwarsvraag) op /vragen, elk met eigen pagina, FAQ-gegevens en bronnen; blok op elke doelgroeppagina; feedbackblok op vragen, fiches en Plakcheck | #49 |
| 26/11/2026 | B01 | Fiche "Artikel 4 na de Omnibus" (één A4, bijsluiter, bronnen: Publicatieblad, Commissie 20/10, VRT); kader in het AI Act-kompas; doos en vraag artikel-4-werkgever verwijzen ernaar. Fiches tonen nu een bijsluiter en bronnen (huisstijl 1.0) | #50 |
| 26/11/2026 | B03 | Afsprakenkaart v1.0.1 op /afsprakenkaart: vijf contexten (klas, werk, gemeente, vereniging, thuis), acht vragen, kaart van één A4, deellink #p=, testpaneel 42 van 42; in TOOLS, /gratis, /doen, privacy; doos, schoolpakket, schoolfiche en drie vragen verwijzen ernaar. Regels per context nagekeken en goedgekeurd door Duncan (v1.0.1) | #50 |
| 26/11/2026 | B05 | Fiches "Is dit echt? Wat je doet bij twijfel" (klare taal, met invulregel voor een vertrouwenspersoon) en "AI-oplichting gericht op je zaak" (gewijzigd rekeningnummer, CEO-fraude, valse bankhelpdesk, phishing; naamcontrole van de bank), elk één A4. Drie nieuwe vragen (nieuw rekeningnummer, CEO-fraude, bank belt); twee vragen, het pakket "Echt of nep?" (v1.0.2) en de wegwijzer verwijzen naar de fiches. Het federale fraudeplan (12/11) noemt AI niet, de fiches vullen dat aan | #52 |
| 26/11/2026 | B06 | Fiches "Tien vragen bij een AI-voorstel in de raad" (de tien vragen uit de briefing, met wat vanaf 2 december 2027 geldt als AI meebeslist over mensen: artikel 26, 27 en 49) en "AI aan het loket" (wat mag, wat nooit, zes stappen voor een inwoner die een brief of bericht niet vertrouwt), elk één A4. De briefing voor raadsleden (v1.0.2) verwijst ernaar; het portaal Lokale overheden toont ze | #53 |
| 26/11/2026 | B04 | Blok "Waar AI Ontcijferd zelf van afhangt" op /zo-werken-we#afhankelijkheden: Vercel, GitHub, Combell, Brevo, Anthropic, OpenAI en xAI, met wat elk doet, wat er gebeurt als het wegvalt en de uitweg; open licenties en publieke kopie als sterkste uitweg; eerlijk over wat nog zwak is (vijf van de zeven diensten Amerikaans). Stand op 26/11 | #54 |
