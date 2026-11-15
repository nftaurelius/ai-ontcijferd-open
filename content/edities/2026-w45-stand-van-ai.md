---
titel: "Stand van AI — week 45, 2026"
week: 2026-w45
datum: 2026-11-06
status: klaar
labels: ["Burgers", "Lokale overheden", "Onderwijs", "Werk", "Zelfstandigen"]
---

## De week in één alinea
Een studie in de zorg vindt dat klassieke automatisering (een script met vaste stappen) bij een stabiele interface sneller, goedkoper en iets nauwkeuriger is dan een AI-agent (een systeem dat taken met meerdere stappen uitvoert). Dat helpt bij de keuze tussen die twee. Mistral zet zijn nieuwe topmodel Large 4 aan het werk in Studio, een platform voor bedrijfsagenten dat volgens de maker ook op eigen servers draait. Google verlaagt volgens eigen zeggen de prijs van zijn videomodel. Een onderzoeksraamwerk laat AI studenten over hun eigen werk ondervragen. En VRT NWS toont hoe partijdige 'pink slime'-sites in chatbotantwoorden belanden.

## Klassieke automatisering klopt AI-agent in zorgtest
**Labels:** Werk
**Hype-meter:** Terecht — de studie toetst één vaste portaaltaak en haar conclusie (bij een stabiele interface wint het script) past bij die beperkte reikwijdte.

**Wat gebeurde er?** Onderzoekers vergeleken twee manieren om mammografie- en borstechografierapporten op te halen uit een laboratoriumportaal. Ze publiceerden hun werk op arXiv, een website waar onderzoekers studies delen ([studie op arXiv](https://arxiv.org/abs/2611.03853)).

RPA (Robotic Process Automation, een script dat vaste stappen volgt) haalde een nauwkeurigheid van 98,90%. De agent, die draait op een taalmodel (een AI die tekst begrijpt en schrijft), haalde 96,49%. De samenvatting legt niet uit hoe die nauwkeurigheid is berekend. RPA was ongeveer 13 keer sneller en kostte ongeveer zes keer minder per rapport.

**Waarom doet het ertoe voor Vlaanderen?** Werk: wie in een administratie elke week dezelfde gegevens uit een vast webportaal haalt, hoeft niet automatisch voor een agent te kiezen. Bij een stabiele interface was het script hier beter.

Volgens de auteurs belooft een agent aanpassingsvermogen, terwijl een script gevoelig is voor wijzigingen aan de interface. De samenvatting toont niet dat de interface tijdens de test wijzigde. Dat voordeel van de agent blijft hier dus onbewezen. Het gaat om één studie in de zorg. De cijfers zeggen niets over andere taken of andere modellen.

<details><summary>Verdieping</summary>

- **De cijfers:** F1-score (een maat die zowel volledigheid als juistheid meeweegt): 98,27% voor RPA tegenover 94,48% voor de agent. Tijd per patiënt: 16,07 s tegenover 207,21 s. Kosten per rapport: USD 0,030 tegenover USD 0,187.
- **De opstelling:** RPA bouwden ze met Playwright. De agent bestond uit browser-use, LangGraph en Gemini 2.5 Flash-lite. Ze meten in twee rondes, aangeduid als T en T+7. De samenvatting vermeldt geen tijdseenheid.
- **Wat de meting wel zegt:** nauwkeurigheid, snelheid en kost bij één taak, namelijk mammografie- en borstechografierapporten ophalen. Beide aanpakken slaagden in 100% van de stappen, maar de agent schommelde meer over de tijd.
- **Wat ze niet zegt:** hoeveel patiënten of rapporten getest zijn, staat niet in de samenvatting. Een ander model of een portaal dat verandert, kan een ander beeld geven. De rapporten zijn enkel als informatie behandeld.
- **Bronstatus:** het is één bron, een artikel op arXiv. Een onafhankelijke herhaling wordt niet vermeld.

</details>

<!-- NAGEKEKEN 8/11: volledig artikel niet bereikbaar; de tekst noemt steekproef, T+7 en de definitie van nauwkeurigheid uitdrukkelijk als onbekend. -->

## Mistral zet Large 4 aan het werk in Studio voor bedrijfsagenten
**Labels:** Werk, Lokale overheden
**Hype-meter:** Terecht — een Europese aanbieder die inzet op eigen servers is relevant, maar het bewijs komt van Mistral zelf.

**Wat gebeurde er?** Mistral breidde op 5 november zijn platform Studio uit, met zijn nieuwe topmodel Mistral Large 4 (bijnaam "Le Chonk") als motor ([Mistral](https://mistral.ai/news/build-with-studio/)). Large 4 zelf is niet nieuw: het verscheen begin oktober als voorversie, en sinds 29 oktober zijn de gewichten vrij te downloaden ([VentureBeat](https://venturebeat.com/ai/mistral-large-4-le-chonk-arrives-as-the-top-open-model-outside-china-with-improved-coding-performance-and-63-lower-cost-per-task)). Volgens Mistral bouwen bedrijven met Studio agents (AI-systemen die taken met meerdere stappen uitvoeren), workflows en apps. Die kunnen volgens het bedrijf draaien in de cloud, in een eigen VPC (een afgeschermd deel van een clouddienst) of on-premises (op eigen servers).

Volgens Mistral gebruiken onder meer BNP Paribas en ABANCA Studio al in productie.

**Waarom doet het ertoe voor Vlaanderen?** Lokale overheden: wie gevoelige dossiers beheert, wil vaak zelf bepalen waar model en data draaien. Mistral belooft die keuze. Een Europese leverancier is een extra optie om te vergelijken. Het bericht zegt niet of het ook past bij een Vlaamse gemeente of intercommunale.

Werk: de genoemde klanten zijn grote bedrijven. Voor kleinere organisaties zegt het bericht weinig.

<details><summary>Verdieping</summary>

- **Claims van de maker:** Mistral zegt dat Large 4 sterk is in coderen, defensieve cyberveiligheid en redeneren over complexe documenten. Onafhankelijke metingen staan niet in het bericht. Artificial Analysis geeft Large 4 26 punten op zijn intelligentie-index: het hoogste van alle open modellen die buiten China gemaakt zijn, maar onder de beste Chinese open modellen (32) en ver onder de gesloten topmodellen (57 tot 59).
- **Eigen voorbeelden:** volgens Mistral bespaart een agent die incidenten onderzoekt het eigen team honderden uren per maand. Een workflow die feedback sorteert, zou ongeveer 35 uur per week schelen. Dat zijn interne cijfers van Mistral zonder referentiepunt.
- **Beheersbaarheid:** in het incidentenvoorbeeld vraagt de agent volgens Mistral toestemming voor gevoelige acties. Mistral zegt dat Studio ook functies krijgt voor agent observability (kunnen nakijken wat een agent deed) en evaluaties.
- **Techniek:** via een nieuwe Mistral MCP server kunnen ontwikkelaars volgens Mistral met een coderingsagent bouwen en met één commando naar Studio uitrollen. Met connectors en MCP-servers (koppelstukken tussen agents en andere software) verbindt Studio zich volgens Mistral ook met bedrijfsdata en -systemen.
- **Open gewichten en licentie:** de gewichten zijn te downloaden. Intern gebruik is vrij; wie het model als betaalde dienst aanbiedt, heeft een aparte commerciële overeenkomst met Mistral nodig. Via de API kost het $0,70 per miljoen tokens invoer en $2,10 per miljoen tokens uitvoer.
- **Open vragen:** welke talen Mistral ondersteunt en hoe goed het model in het Nederlands werkt.
- **Bronstatus:** de kernclaims berusten op één bron, de maker zelf.

</details>


## Google brengt AI-video naar 15 seconden, tegen een lagere prijs
**Labels:** Zelfstandigen, Werk, Burgers
**Hype-meter:** Terecht — het is een stapsgewijze update (15 in plaats van 10 seconden, 30% goedkoper) met beperkte winst voor Vlaamse gebruikers, en de kwaliteitsbeloftes komen enkel van Google.

**Wat gebeurde er?** Google DeepMind zegt Gemini Omni 1.2 Flash algemeen beschikbaar te maken via de Gemini API (de technische koppeling voor ontwikkelaars) en Gemini for business ([Google DeepMind](https://deepmind.google/blog/gemini-omni-12-flash-fast-and-cost-effective-with-longer-clips/)). Volgens Google maakt het videomodel clips tot 15 seconden, tegenover 10 bij de vorige versie.

Volgens Google kun je een clip beurt na beurt bijsturen en blijven personages en producten consistenter. Google zegt dat de prijs met 30% daalt tot $0,07 per seconde bij 720p (een gewone HD-resolutie).

**Waarom doet het ertoe voor Vlaanderen?** Zelfstandigen en Werk: een webshop kan volgens Google bestaande productfoto's omzetten in advertentiespots. Op 720p kost een clip van 15 seconden ongeveer $1,05, op basis van de prijs per seconde.

Burgers: Google belooft ook natuurlijkere spraak en duidelijkere lipsynchronisatie. Als AI-clips goedkoper te maken zijn, kom je ze mogelijk vaker tegen. Google zegt een onzichtbaar SynthID-watermerk (een verborgen merkteken dat bedoeld is om AI-beeld te herkennen) op de uitvoer te zetten. Hoe makkelijk je dat zelf kunt controleren, staat niet in de bron.

<details><summary>Verdieping</summary>

- **Wat Google belooft:** minder "visuele drift" (personages of objecten die onderweg veranderen), vloeiendere dialoog, duidelijkere lipsynchronisatie en camerabewegingen met minder ongewenste sprongen.
- **Hoe de kosten werken:** volgens Google kun je snel schetsen op 360p of 720p, een detail via een vervolgopdracht aanpassen en het beste resultaat opschalen naar 1080p of 4K.
- **Wat de bron niet geeft:** geen benchmark en geen onafhankelijke test. De voorbeelden zijn door Google gekozen. Het tweede bericht ([Google AI-blog](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/)) heeft dezelfde titel en komt van hetzelfde bedrijf. Het bevestigt dus niets onafhankelijk.
- **Eigen beperkingen:** Google zegt zelf dat snelle sportactie, snelle scriptwissels en complexe fysica nog verbeteren.
- **Open vragen:** hoe goed spraak en lipsynchronisatie in het Nederlands werken, en hoe het model presteert bij andere dan reclamebeelden.
- **Bronstatus:** alle claims komen van de maker.

</details>

<!-- NAGEKEKEN 8/11: talen en EU-beschikbaarheid niet te vinden in de documentatie; staat als open vraag in de tekst. -->

## ProofPaths: AI die studenten over hun eigen werk ondervraagt
**Labels:** Onderwijs
**Hype-meter:** Terecht — het mikt op een echt probleem (een juiste oplossing bewijst geen begrip), maar het is een onderzoeksraamwerk zonder gemelde praktijkproef, dus de toepasbaarheid in het Vlaamse onderwijs blijft voorlopig beperkt.

**Wat gebeurde er?** Onderzoekers publiceerden op arXiv het raamwerk ProofPaths, dat inzendingen beoordeelt en studenten erover ondervraagt ([arXiv](https://arxiv.org/abs/2611.03882)). Meerdere beoordelingsagents scoren een inzending volgens de richtlijnen van de docent. Ze geven elkaar kritiek en passen hun oordeel aan.

Een interviewagent vraagt de student daarna stappen uit de eigen inzending te verantwoorden. De docent kan alles inzien en cijfers aanpassen.

**Waarom doet het ertoe voor Vlaanderen?** Onderwijs: volgens de auteurs kunnen studenten taalmodellen gebruiken om opdrachten af te werken. Een juiste oplossing bewijst dan niet dat de student de redenering begrijpt. Denk aan een lesgever in Vlaanderen die tientallen inzendingen nakijkt. Een individuele bevraging kan helpen om begrip te onderzoeken, maar vraagt volgens de auteurs telkens tijd van medewerkers. ProofPaths wil een deel van dat werk overnemen.

Voor welk onderwijsniveau het bedoeld is, melden de auteurs niet. Het blijft een onderzoeksraamwerk, geen product voor de klas.

<details><summary>Verdieping</summary>

- **Hoe het werkt:** elke vraag van de interviewagent is gekoppeld aan een opgehaald stuk uit de inzending. De docent kan zo het antwoord van de student naast de bewuste passage leggen. Het systeem bewaart beoordelingen en gespreksverslagen per inzending.
- **Wat getest is:** de auteurs noemen deterministische tests (tests met telkens hetzelfde verwachte resultaat) van de beoordelingscontrollers. Die tests controleren bronverwerking, scoreberekening en een limiet op correctiepogingen. Uitslagen geven de auteurs niet. Het is geen bewijs dat de AI correct beoordeelt of begrip herkent.
- **Wat niet getest lijkt:** of de AI eerlijk beoordeelt of echt begrip herkent. De samenvatting meldt geen vergelijking met menselijke beoordelaars en geen proef met studenten.
- **Open vragen:**
  - Hoe eerlijk is een AI-interview voor studenten die zich minder vlot uitdrukken?
  - Hoe lang blijven de opgeslagen gesprekken bewaard, en wie heeft er toegang toe?
  - Wie draagt de verantwoordelijkheid voor het cijfer? De docent kan overrulen, maar of dat in de praktijk gebeurt, is onbekend.
- **Bronstatus:** één bron, de samenvatting van de auteurs zelf.

</details>

## 'Pink slime': partijdige nieuwssites vullen ook chatbotantwoorden
**Labels:** Burgers, Lokale overheden
**Hype-meter:** Terecht — het gemeten verschijnsel is Amerikaans, maar het mechanisme (partijdige sites als chatbotbron) is ook voor Vlaamse lezers bruikbaar om bronnen kritisch te bekijken; of het hier speelt, is onbekend.

**Wat gebeurde er?** VRT NWS beschrijft hoe partijgebonden 'pink slime'-sites zich voor de Amerikaanse midterms voordoen als onafhankelijk lokaal nieuws ([VRT NWS](https://vrtnws.be/p.y318kdEd5)). De Amerikaanse organisatie NewsGuard telt 1.179 van die sites. Er verschijnen in de VS nog 937 dagbladen, volgens de Local News Initiative van Northwestern University ([AFP via Malay Mail](https://www.malaymail.com/news/world/2026/09/29/pseudo-journalism-researchers-warn-pink-slime-outlets-are-targeting-us-midterms-with-partisan-content/236872)).

NewsGuard stelde zeven chatbots samen 168 vragen over kandidaten en races. In 48% van de antwoorden zat zo'n site tussen de bronnen ([Politico, via Slashdot](https://tech.slashdot.org/story/26/09/26/2358224/)). Het gaat om een test van NewsGuard zelf; een onafhankelijke herhaling is er niet.

**Waarom doet het ertoe voor Vlaanderen?** Burgers: wie een chatbot om nieuws vraagt, krijgt mogelijk bronnen zonder te weten wie ze betaalt. Kijk dus na welke bronnen een antwoord noemt.

Lokale overheden: volgens VRT NWS misbruiken Russische netwerken bekende lokale nieuwsmerken voor nepvideo's. Dat is een signaal dat herkenbare lokale media misbruikt kunnen worden. Dat dit in Vlaanderen op dezelfde schaal speelt, staat niet in de bron.

<details><summary>Verdieping</summary>

- **De telling:** de 1.179 sites komen van NewsGuard, de 937 dagbladen van de Local News Initiative van Northwestern University. Het zijn dus twee verschillende bronnen. De term "pink slime" bestaat sinds 2012. AI maakt het volgens VRT NWS makkelijker om snel hele sites te vullen.
- **Beide kampen:** Ohio Pulse krijgt geld van SLF PAC, een Republikeinsgezinde actiegroep. The Ohio Independent is opgericht door een ngo die steun krijgt van een Democratische actiegroep. Beide brengen eenzijdig nieuws.
- **Bereik:** de sites zelf bereiken weinig mensen. Afzonderlijke artikels bereiken er wel veel, doordat actiegroepen ze als advertentie op sociale media duwen.
- **Wat de 48% meet:** hoe vaak een pink slime-site tussen de bronnen stond, naast andere bronnen. Getest zijn ChatGPT, Copilot, Perplexity, Claude, Gemini, Meta AI en Grok, met vragen op basis van twaalf sites (zes links, zes rechts). ChatGPT citeerde zo'n site het vaakst (70,8%), Grok het minst (29,2%). In 7,7% van de antwoorden was een pink slime-site de enige bron in de tekst. Slechts één van de 168 antwoorden wees op het partijdige karakter van de bron.
- **Russische campagnes:** eind oktober circuleerde op X een gemanipuleerde video met het merk van de zender WOIO Channel 19 en een verzonnen beschuldiging aan een senaatskandidaat. Volgens VRT NWS is dat een beproefde tactiek van netwerken als Storm-1516. AntiBot4Navalny identificeerde tientallen campagnes met bewerkte video's, vooral tegen Democratische kandidaten. NewsGuard meldde in maart 2025 al dat Russische netwerken chatbots bewust bespelen met massa's nepartikels.
- **Bronstatus:** de kernclaims berusten op één bron, VRT NWS. Die schrijft de telling en de chatbottest toe aan NewsGuard en Politico.

</details>


## Ruis van de week
Geen deze week.

## Woord van de week
**Pink slime** is een nieuwssite die zich voordoet als onafhankelijk lokaal medium, maar betaald wordt door een politieke actiegroep. De naam verwijst naar een goedkoop vleesproduct dat op echt vlees lijkt. Volgens VRT NWS maakt AI het makkelijker zulke sites snel te vullen, en belanden hun artikels ook als bron in chatbotantwoorden.

<!-- NAKIJKEN: niet opgenomen. K1 (tienerveiligheid OpenAI), K2 (GPT-6 Cyber), K5 (robots.txt OpenAI) en K10 (UCB/Cradle) hebben in de bron slechts één zin of een afgekapte tekst; OpenAI zou bovendien al snel drie keer voorkomen. K6 (Google en schoolsoftware, VS) en K12 (podcast over shopping-agents) bevatten te weinig om te duiden. K11 (De Standaard) zit achter een betaalmuur; enkel de kop is gebruikt als signaal. K2 is een kandidaat voor een volgende editie als er meer bronmateriaal is. -->

## Mijn inschatting

**Over scripts tegen agents.** Dat een script het vandaag nog beter doet dan een agent, verbaast me niet. De modellen zijn al ver, maar ze zitten nog niet aan hun plafond. In deze test was de agent minder nauwkeurig, trager en duurder per rapport. De vraag is alleen hoelang dat nog zo blijft. Gezien het tempo waarmee AI verbetert, verwacht ik dat agents ook zulke vaste taken, waar ze nu nog niet de beste in zijn, binnen afzienbare tijd overnemen.

**Over Mistral.** Europa wacht al te lang op een eigen model dat kan meedoen met OpenAI, Anthropic en Google, en met de open modellen uit China. Large 4 is een stap in die richting: volgens Artificial Analysis is het het sterkste open model dat buiten China gemaakt is. Aan de top staat het nog lang niet. Op hun intelligentie-index haalt het [26 punten](https://venturebeat.com/ai/mistral-large-4-le-chonk-arrives-as-the-top-open-model-outside-china-with-improved-coding-performance-and-63-lower-cost-per-task), tegenover 32 voor de beste Chinese open modellen en 57 tot 59 voor de topmodellen van Google, Anthropic en OpenAI.

Toch vind ik het een goede en nodige ontwikkeling, specifiek voor Europa. Bedrijven en overheden kunnen een model gebruiken dat in Europa gebouwd is, desnoods op hun eigen servers, en hoeven niet afhankelijk te blijven van de VS of China. De vraag is hoe goed het in de praktijk werkt naast de modellen die al veel verder staan.

**Over Gemini Omni.** Ik bekeek enkele demo's van het nieuwe videomodel van Google, en die maakten indruk, al zijn het wel voorbeelden die Google zelf koos. Opnieuw zakt de drempel om zelf video te maken, voor eender welk doel. De kwaliteit is hoog en de prijs laag: een clip van 15 seconden kost ongeveer een dollar. Daarmee komt dit binnen bereik van het grote publiek.

Tegelijk is het een volgende stap in deepfakes, juist omdat de beelden zo goed zijn geworden. Een van de grote vragen wordt hoe we als mens nog onderscheiden wat echt is en wat niet. Daarom vind ik het goed dat AI-bedrijven een watermerk aan hun beelden toevoegen, zodat andere platformen die kunnen herkennen en aanduiden. In Europa is dat ook geen vrije keuze meer: de AI Act verplicht aanbieders van generatieve AI om hun beeld, video, geluid en tekst [machineleesbaar te markeren](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-article-50-transparency-20260729/). Voor systemen die al op de markt waren, loopt de overgangstermijn tot 2 december.

**Over ProofPaths.** Ik studeer zelf met AI, als autodidact, en het is voor mij een grote meerwaarde. Mijn werk laten nalezen en beoordelen brengt veel terug in het leerproces. Een systeem dat studenten over hun eigen werk bevraagt, is dus een stap in de goede richting. In het gewone onderwijs mag het de menselijke rol in de didactiek wel niet wegnemen. Ik zie zo'n toepassing daarom vooral in het hoger onderwijs, en hooguit in de laatste graad van het secundair, bij feitelijke vakken.

**Over pink slime.** Dit is een echt risico. Informatie kunnen beoordelen wordt een vaardigheid die je nodig hebt om aan de samenleving deel te nemen. En het probleem is moeilijk op te lossen. Zelfs als de grote AI-bedrijven alles wat met hun modellen gemaakt wordt van een watermerk voorzien, zul je nooit alles kunnen herkennen. Met open modellen kan bijna iedereen zelf zulke sites vullen.

De Amerikaanse sites uit dit stuk worden betaald door binnenlandse actiegroepen, van beide partijen. Maar in een tijd van conflict zoals nu gebruiken ook andere landen zulke technieken om de informatie voor burgers elders verwarrend te maken. Rusland is het duidelijkste voorbeeld. Volgens NewsGuard publiceerde het Russische Pravda-netwerk in 2024 zo'n 3,6 miljoen artikels, en herhaalden tien geteste chatbots die [valse verhalen in een derde van de gevallen](https://the-decoder.com/russian-fake-news-network-floods-western-ai-chatbots-with-millions-of-propaganda-articles/). Chatbots zijn daar sindsdien beter in geworden: in een test van NPR en NewsGuard deze zomer [ontkrachtten ze zulke verhalen](https://www.wamc.org/2026-08-30/we-tested-how-ai-chatbots-would-handle-foreign-propaganda-they-did-surprisingly-well) gemiddeld in ongeveer drie op de vier gevallen. Waterdicht is dat niet. Ik verwacht dat dit probleem de komende jaren alleen maar groter wordt.

## Zo is dit gemaakt

- AI-agents verzamelden en selecteerden het nieuws, schreven het concept en controleerden het. Schrijver: claude-sonnet-5-5 (anthropic); controle: gpt-6-astra (openai).
- De tegenspreker maakte 16 opmerking(en), waarvan 6 kritiek; kritieke punten zijn opgelost of geschrapt.
- Duncan Panis las alles na, paste aan waar nodig en schreef zelf "Mijn inschatting".
- Meer over onze werkwijze: [Zo werken we](/zo-werken-we).

## Bronnen
1. [Performance, Scalability and Maintenance: An Experimental Study of RPA vs. Autonomous Agents in the Healthcare Domain](https://arxiv.org/abs/2611.03853), arXiv (cs.AI)
2. [Product Le Chonk brings the brains. Studio puts it to work.](https://mistral.ai/news/build-with-studio/), Mistral AI
3. [Gemini Omni 1.2 Flash: Fast and cost-effective with longer clips](https://deepmind.google/blog/gemini-omni-12-flash-fast-and-cost-effective-with-longer-clips/), Google DeepMind
4. [Gemini Omni 1.2 Flash: Fast and cost-effective with longer clips](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/), Google AI-blog
5. [ProofPaths: An AI Agent Framework for Assessing Student Reasoning](https://arxiv.org/abs/2611.03882), arXiv (cs.AI)
6. [Roze slijm en uiteraard AI: deze desinformatie krijgen Amerikanen voor de midterms te verwerken](https://vrtnws.be/p.y318kdEd5), VRT NWS
7. [Mistral Large 4 'Le Chonk' arrives as the top open model outside China](https://venturebeat.com/ai/mistral-large-4-le-chonk-arrives-as-the-top-open-model-outside-china-with-improved-coding-performance-and-63-lower-cost-per-task), VentureBeat
8. [Are AI Chatbots Spreading Misinformation to US Voters?](https://tech.slashdot.org/story/26/09/26/2358224/), Slashdot over Politico
9. [Pseudo-journalism: researchers warn pink slime outlets are targeting US midterms](https://www.malaymail.com/news/world/2026/09/29/pseudo-journalism-researchers-warn-pink-slime-outlets-are-targeting-us-midterms-with-partisan-content/236872), AFP via Malay Mail
