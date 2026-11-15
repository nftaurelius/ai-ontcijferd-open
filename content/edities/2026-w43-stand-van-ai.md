---
titel: "Stand van AI — week 43, 2026"
week: 2026-w43
datum: 2026-10-23
status: klaar
labels: ["Burgers", "Lokale overheden", "Werk", "Zelfstandigen"]
---

## De week in één alinea
Twee lekken in PHP, volgens OpenAI met AI ontdekt, haalden deze week sites offline, ook van Nederlandse en Finse overheidsdiensten. Beheer je een WordPress- of Drupalsite, controleer dan of de update erop staat. Microsoft meldt dat zijn AI-systeem beter diagnosticeert dan artsen, maar alleen in een eigen test. Princeton-onderzoekers leggen uit waarom het testen van AI-agents moeilijker en duurder wordt. Uber rolt ChatGPT Work uit bij meer dan 30.000 medewerkers, volgens OpenAI zelf.

## Twee PHP-lekken, volgens OpenAI ontdekt met AI, halen sites offline
**Labels:** Lokale overheden, Zelfstandigen
**Hype-meter:** Terecht — De aanvalspogingen waren reëel en begonnen dagen vóór de patch, en overheidsdiensten schakelden hun sites uit.

**Wat gebeurde er?** Twee ernstige kwetsbaarheden (fouten in software die aanvallers kunnen misbruiken) haalden deze week sites offline. Ze zitten in PHP, de programmeertaal achter onder meer WordPress en Wikipedia. Volgens [The Verge](https://www.theverge.com/tech/1016574/php2shell-security-vulnerability-websites-down) zitten de fouten al ongeveer twintig jaar in alle PHP-versies en werden ze volgens OpenAI met AI gevonden. Amazon zag al op 17 oktober een aanvalspoging, dagen voor de patch (de update die de fout herstelt).

**Waarom doet het ertoe voor Vlaanderen?**
**Lokale overheden:** Nederlandse en Finse overheidsdiensten haalden hun sites preventief offline. De Amerikaanse NSA en het Britse NCSC raadden dat aan als een directe update niet kan. Draait jullie website op WordPress of Drupal, dan draait ze op PHP. Vraag je leverancier naar de versie en de patch.

**Zelfstandigen:** Heb je een website of webshop op WordPress, laat dan nagaan of de update erop staat. Sites op oude, niet meer ondersteunde PHP-versies hebben vaak weinig opties. Of Vlaamse sites getroffen zijn, vermeldt de bron niet.

<details><summary>Verdieping</summary>

- **Wat "70%" zegt:** Volgens sommige schattingen gebruikt tot 70% van de websites PHP, op wat voor manier dan ook. Dat gaat over gebruik, niet over hoeveel sites kwetsbaar of gehackt zijn. Een meetmethode ontbreekt.
- **Aanvalspogingen:** Cloudflare-topman Matthew Prince meldt duizenden pogingen in de tien uur vóór de bekendmaking. In de twee uur erna waren het er honderdduizenden, en later volgens hem miljoenen. Dat zijn Cloudflares eigen cijfers, niet onafhankelijk bevestigd.
- **Pogingen zijn geen succes:** De PHP Foundation kent naar eigen zeggen geen geslaagde uitvoering van code op afstand (een aanvaller laat op jouw server eigen code draaien). Ze noemt updaten wel noodzakelijk.
- **Rol van AI:** Wiz zegt dat misbruik een uiterst complexe stappenreeks vereiste, op de rand van wat menselijke onderzoekers aankonden. Krachtige AI-modellen maken dat gemakkelijker. Volgens OpenAI vond een onderzoeker van Calif de fouten met GPT-5.6 Sol, vóór aanvallers. Dat is niet onafhankelijk bevestigd.
- **Onderhoud:** Ondřej Surý, die de patch klaarmaakte, vreest dat winstgevende bedrijven open source uitbuiten. Hij hoopt dat dit een kantelpunt wordt.
- **Beperking:** Dit overzicht komt van één medium dat rapporten van Amazon, Cloudflare en Wiz samenbrengt.

</details>

<!-- NAKIJKEN: K4 kwam binnen via de Future Tools-radar; de brontekst is afgekapt (laatste item over GPT-5.6 Sol/Wiz/WSJ). De kernclaim rust op één medium (The Verge). Primaire bronnen zoeken en linken (Amazon Threat Intelligence, Wiz, PHP Foundation, Cloudflare/Matthew Prince, CVE-2026-109618/-109619) en de exacte Verge-titel controleren. Tijdstip van de "miljoenen"-melding van Cloudflare verifiëren (Verge: "by last night"). Is er een Belgische/Vlaamse impact of een advies van het Centrum voor Cybersecurity België? -->

## Microsoft: AI-systeem diagnosticeert beter dan artsen, binnen een eigen test
**Labels:** Burgers
**Hype-meter:** Overroepen — De cijfers komen van de maker en gelden binnen één testopzet, terwijl de test met echte patiënten nog moet beginnen.

**Wat gebeurde er?** Microsoft meldt dat zijn diagnosesysteem MAI-DxO in een eigen benchmark (een vaste testopzet waarmee je systemen vergelijkt) 83% van 304 moeilijke gevallen uit het tijdschrift NEJM juist diagnosticeert. Artsen haalden 22% zonder naslagwerk en 36% met. Op meer typische spoedgevallen uit MIMIC-IV-ED, een Amerikaanse gegevensverzameling over spoedzorg, is het 80% tegenover 47%, [volgens Microsoft](https://microsoft.ai/news/building-medical-superintelligence/). Dat is geen gemeten prestatie op een Vlaamse spoeddienst. Het bedrijf zegt dat het werk in Science is gepubliceerd.

**Waarom doet het ertoe voor Vlaanderen?** **Burgers:** Microsoft meldt geen toepassing of patiëntenstudie in Vlaanderen. De test gebruikt bestaande gevallen, geen echte patiënten. Microsoft plant wel een studie met patiënten samen met het Beth Israel Deaconess Medical Center in Boston. Kom je AI-diagnosehulp tegen, vraag dan op welke gevallen ze getest is en tegen welke artsen.

<details><summary>Verdieping</summary>

- **Wat de test meet:** SDBench laat AI en artsen starten met beperkte informatie. Ze kiezen zelf welke vragen en onderzoeken ze opvragen. Gemeten worden juistheid, opgevraagde onderzoeken en geschatte kosten.
- **Wat niet:** echte patiënten, behandeling en een drukke werkdag. De kosten zijn schattingen. Microsoft vermeldt niet hoeveel artsen meededen of welke specialisten.
- **Hoe het werkt:** MAI-DxO werkt als een panel van virtuele artsen die in meerdere rondes debatteren. Volgens Microsoft bleven de winsten bestaan met nieuwere modellen, waaronder GPT-5.5.
- **Kosten:** Microsoft meldt dat één configuratie op de NEJM-gevallen 81% haalde tegen minder dan de helft van de kosten van "vergelijkbare systemen". Elders spreekt het bedrijf van de helft of zelfs een derde van de kosten. Niet duidelijk is of artsen bij die vergelijkingssystemen horen. Dit is een claim van Microsoft, geen onafhankelijke vaststelling.
- **Controle:** Microsoft publiceert de testcode voor een selectie NEJM-gevallen, zodat anderen kunnen herhalen. Onafhankelijke bevestiging van de cijfers is er (nog) niet.
- **Term:** "Medical superintelligence" is Microsofts ambitie, geen gemeten resultaat.

</details>

<!-- NAKIJKEN: Alleen Microsoft als bron (via Future Tools-radar binnengekomen, primaire tekst is van microsoft.ai). Link naar het Science-artikel en een onafhankelijke reactie van artsen/onderzoekers toevoegen; brontekst is afgekapt. -->

## Hoe test je een AI-agent? Princeton zet de vragen op een rij
**Labels:** Lokale overheden
**Hype-meter:** Terecht — Het paper levert bruikbare vragen voor wie AI-agents wil beoordelen of aankopen, zonder meer te beloven dan het kan waarmaken.

**Wat gebeurde er?** Onderzoekers van Princeton publiceerden met collega's van Stanford, het UK AI Security Institute en Brookings het paper *Emerging Trends in AI Agent Evaluation*. Een AI-agent is een systeem dat zelfstandig stappen uitvoert met hulpmiddelen. Volgens de auteurs, in [hun eigen toelichting](https://www.normaltech.ai/p/new-paper-emerging-trends-in-ai-agent), wordt testen lastiger en duurder. Je moet namelijk het hele verloop bekijken, niet alleen het eindresultaat.

**Waarom doet het ertoe voor Vlaanderen?** **Lokale overheden:** Koop je een AI-agent aan, dan is een resultaat van de leverancier geen garantie voor jouw toepassing. De auteurs waarschuwen dat een resultaat op het ene niveau niet automatisch geldt op het andere. Test de agent dus in de toepassing die je voor ogen hebt. Vraag wie getest heeft, in welke omstandigheden en of ook gekeken is naar hoe de agent tot het resultaat kwam.

De auteurs maken nog een onderscheid. Testen of een agent een taak zelfstandig overneemt, is iets anders dan testen of medewerkers er beter mee werken. Stel dat een gemeente een agent wil inzetten om meldingen van inwoners te sorteren (een denkbeeldig voorbeeld). Dan beoordeel je zowel hoe goed de agent dat alleen doet als hoe een medewerker met de agent werkt.

<details><summary>Verdieping</summary>

- **Het hele traject:** Evaluatoren moeten nagaan of een agent sluiproutes nam, zeker omdat agents toegang hebben tot hulpmiddelen en omgevingen.
- **Kosten:** Meerdere agents op de ExploitBench-benchmark kostten tientallen duizenden dollars aan rekentegoed om te testen. Het opzetten van de testomgeving komt daar nog bij.
- **Testen met agents:** Bij het OpenAI-HuggingFace-incident gebruikten evaluatoren achteraf andere agents om schadelijke acties op te sporen. Ze erkenden zelf de beperkingen daarvan. De blog legt het incident hier niet uit.
- **Lab versus praktijk:** De auteurs wijzen op een gerandomiseerde proef van METR. Daarin verhoogde het gebruik van agent-tools bij softwareontwikkeling de totale doorlooptijd, tegen de verwachting in. Het is één studie; details staan niet in de blog.
- **Onafhankelijkheid:** Echte onafhankelijkheid vraagt meer dan geld en toegang tot modellen. Evaluatoren moeten ook zelf hun onderzoeksvragen en methoden kunnen kiezen. Ze moeten kunnen werken zonder vrees voor vergelding en hun bevindingen transparant kunnen delen. Labs geven bovendien samenvattingen van de redeneerstappen vrij, geen ruwe sporen.
- **Beperking:** Dit is de eigen samenvatting van de auteurs. Hun aanbevelingen staan in het volledige paper.

</details>

<!-- NAKIJKEN: Brontekst is afgekapt vóór de aanbevelingen. Link naar het volledige paper ontbreekt; toevoegen indien beschikbaar. -->

## Uber geeft 30.000 medewerkers ChatGPT Work
**Labels:** Werk
**Hype-meter:** Terecht — Een brede uitrol bij een groot bedrijf is een nuttig signaal voor Vlaamse werkgevers, al zegt het bericht niets over resultaat.

**Wat gebeurde er?** Volgens [OpenAI](https://openai.com/index/uber-chatgpt-work-rollout) rolt Uber ChatGPT Work uit bij meer dan 30.000 medewerkers. Teams gebruiken het voor onderzoek, data-analyse, presentaties en complexe werkprocessen. Het is een bericht van de leverancier; onafhankelijke bevestiging is er (nog) niet.

**Waarom doet het ertoe voor Vlaanderen?** **Werk:** OpenAI presenteert dit als een uitrol voor het hele personeel, niet als proef bij één team. Voor Vlaamse werkgevers is dat vooral een signaal over de richting. Wat het oplevert, blijft open. Vraag je als werkgever dus vooraf af wat je wilt meten en bij welke taken.

<details><summary>Verdieping</summary>

- **Wat we weten:** een aantal medewerkers en een lijst taken, beide volgens OpenAI.
- **Wat niet:** productiviteitswinst, kosten en echt gebruik. Toegang is niet hetzelfde als gebruik.
- **Tegenwicht:** Een uitrol zegt niet of werk sneller gaat. In de METR-proef die de Princeton-auteurs aanhalen, nam de doorlooptijd bij softwareontwikkeling toe. Dat is één studie, in één vakgebied.
- **Open vragen:** welke taken echt veranderen, wat het kost en hoe Uber de resultaten meet.

</details>

<!-- NAKIJKEN: Er lag slechts een korte samenvatting van het OpenAI-bericht voor; controleren of het volledige bericht resultaten, citaten van Uber of gebruikscijfers noemt. K1 (training environment) en K2 (consistent standards) niet opgenomen: maximaal twee onderwerpen per bedrijf en te weinig brontekst. -->

## Ruis van de week
**"AI overtreft artsen tegen de helft van de kosten."** Dat zijn twee claims in één. De nauwkeurigheid komt uit Microsofts eigen test met bestaande gevallen. De kostenclaim gaat over één configuratie met 81% nauwkeurigheid, vergeleken met "vergelijkbare systemen" waarvan niet duidelijk is of artsen erbij horen, en het zijn geschatte kosten van onderzoeken, geen ziekenhuisrekeningen. Een studie met echte patiënten moet nog beginnen, en onafhankelijke bevestiging ontbreekt (zie [Microsoft](https://microsoft.ai/news/building-medical-superintelligence/)).

## Woord van de week
**Benchmark.** Een benchmark is een vaste set opdrachten waarmee je AI-systemen vergelijkt, zoals een examen. De score zegt hoe goed een systeem is op die opdrachten, niet hoe het presteert in jouw school, gemeente of ziekenhuis. Vraag daarom bij elke score: wat werd gemeten, door wie, en wat bleef buiten de test?

## Mijn inschatting

**PHP is nog maar het begin.** Deze lekken passen in een patroon dat dit voorjaar zichtbaar werd. In april meldde Anthropic dat zijn model Claude Mythos Preview duizenden ernstige, nog onbekende kwetsbaarheden vond, in elk groot besturingssysteem en elke grote browser ([The Hacker News](https://thehackernews.com/2026/04/anthropics-claude-mythos-finds.html)). In juni liet de Amerikaanse overheid de toegang van buitenlanders tot Mythos 5 tijdelijk afsluiten, uit vrees dat de beveiliging rond cybertaken te omzeilen was ([Greenberg Traurig](https://www.gtlaw.com/es/insights/2026/6/ai-company-anthropic-suspends-access-to-claude-fable-5-claude-mythos-5-following-us-export-control-directive)). Onze samenleving draait op ontelbare systemen die al twintig jaar niet veranderd zijn. Ik verwacht dat er nog veel meer zulke lekken bovenkomen, en dat niet altijd de verdedigers ze als eerste vinden. Ook open modellen, die iedereen kan gebruiken, lopen volgens [Epoch AI](https://epoch.ai/data-insights/open-closed-cyber-eci-gap) maar zes à zeven maanden achter op de gesloten topmodellen in cybervaardigheden. Interne beveiligingsteams kunnen dat tempo alleen niet volgen. Overheden zouden daarom nu moeten investeren in eigen of Europese AI voor cyberverdediging, nog vóór AI die vooral efficiëntie oplevert, en zonder volledig te rekenen op een handvol grote techbedrijven.

**Diagnose: deze claim is overroepen, de richting niet.** De hype-meter staat op overroepen voor Microsofts eigen test, en dat blijft zo. Maar dat AI de diagnose verbetert, is voor mij geen hype. In de grote Zweedse MASAI-studie vond borstkankerscreening met AI-ondersteuning 29 procent meer kankers, met nauwelijks meer vals alarm en 44 procent minder werk voor radiologen ([Healthcare in Europe](https://healthcare-in-europe.com/en/news/ai-enhance-breast-cancer-screening-performance-masai.html)). Artsen zijn vaak heel goed. Artsen met AI worden beter.

**Testen wordt een vak.** Hoe meer verantwoordelijkheid we aan AI-agents geven, hoe dringender de vraag wordt wat ze echt kunnen. Dat weet je alleen door te testen, testen en nog eens testen. Ik verwacht dat onafhankelijk testen een eigen sector wordt: wie een agent verkoopt, laat hem door een derde controleren op wat hij belooft en op veiligheid.

**Geef mensen toegang.** Uber doet wat ik elke werkgever en overheid in Vlaanderen zou aanraden: geef medewerkers toegang tot AI en laat ze zelf ontdekken wat het in hun job kan. AI-geletterdheid leer je niet uit een folder. Kies daarvoor wel een zakelijk abonnement en geen persoonlijk account, zodat er duidelijke afspraken zijn over wat er met bedrijfsgegevens gebeurt. AI wordt een van de grootste technologische hefbomen uit onze geschiedenis. Wie er nu mee leert werken, bouwt een voorsprong op tegenover wie het blijft behandelen als een veredelde Google.

## Zo is dit gemaakt

- AI-agents verzamelden en selecteerden het nieuws, schreven het concept en controleerden het. Schrijver: claude-sonnet-5-5 (anthropic); controle: gpt-6-astra (openai).
- De tegenspreker maakte 11 opmerking(en), waarvan 3 kritiek; kritieke punten zijn opgelost of geschrapt.
- Duncan Panis las alles na, paste aan waar nodig en schreef zelf "Mijn inschatting".
- Meer over onze werkwijze: [Zo werken we](/zo-werken-we).

## Bronnen
1. [PHP vulnerabilities affect 70% of web, AI-discovered exploits hit Wikipedia, WordPress, governments](https://www.theverge.com/tech/1016574/php2shell-security-vulnerability-websites-down), The Verge
2. [Building Medical Superintelligence](https://microsoft.ai/news/building-medical-superintelligence/), Microsoft AI
3. [New paper: Emerging trends in AI agent evaluation](https://www.normaltech.ai/p/new-paper-emerging-trends-in-ai-agent), AI Snake Oil
4. [Uber brings ChatGPT Work to all employees with OpenAI](https://openai.com/index/uber-chatgpt-work-rollout), OpenAI
