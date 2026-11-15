---
titel: "Black October: wat AI wel en niet deed met de veiligheid van het internet"
datum: 2026-11-01
status: klaar
labels: ["Lokale overheden", "Zelfstandigen", "Werk", "Burgers", "Bibliotheken"]
samenvatting: "In een paar dagen kwamen kritieke lekken, inbraken en noodpatches samen. AI hielp de grootste lekken vinden, maar niet elk incident heeft met AI te maken. Wat er gebeurde, wat Vlaanderen merkte en wat je nu doet."
---

## In het kort
Eind oktober kreeg het internet in een week tijd een reeks zware beveiligingsproblemen te verwerken. Online kreeg die week de naam "Black October". Het belangrijkste is PHP2Shell: twee kritieke lekken in PHP, de programmeertaal achter ongeveer 70 procent van de websites waarvan de technologie gekend is. Die lekken werden mee gevonden met AI. Op 21 oktober haalden ook tientallen Vlaamse en Belgische organisaties hun website uit voorzorg offline. Tegelijk bundelt het etiket incidenten die niets met AI te maken hebben. Dit dossier zet ze uit elkaar.

**Hype-meter:** Terecht — de dreiging is reëel en raakte Vlaamse websites rechtstreeks, al gooit het etiket "Black October" incidenten zonder AI-verband op één hoop.

## PHP2Shell: het lek dat AI mee vond
**Wat gebeurde er?** Op 21 oktober bracht het PHP-team noodpatches uit voor twee kritieke lekken, samen PHP2Shell genoemd. Een aanvaller zonder wachtwoord kon er in bepaalde gevallen eigen code mee uitvoeren op een webserver. De details lekten een dag vroeger uit via een forumbericht, waarna de patch naar voren werd gehaald ([Infosecurity Magazine](https://www.infosecurity-magazine.com/news/critical-php-vulnerabilities-leaked/)).

**Wie vond het, en met welke AI?** Het beveiligingsbedrijf Calif vond het eerste lek in augustus, tijdens een audit van de PHP-broncode die OpenAI betaalde. Calif gebruikte daarbij OpenAI's model GPT-5.6 Sol. Weken later vond Wiz de lekken onafhankelijk, met eigen software, Gemini 4 Argon en GPT-5.6 Sol ([The Next Web](https://thenextweb.com/news/php2shell-php-rce-ai-openai-wiz)). OpenAI zegt dat AI de lekken voor zover bekend vond vóór aanvallers dat deden ([Axios via Yahoo](https://www.yahoo.com/news/world/articles/black-october-why-bugs-discovered-180131955.html)). Dat is een claim van een betrokken partij: OpenAI financierde de audit.

**Werd het lek misbruikt?** Ja. Het Amerikaanse cyberagentschap CISA zette beide lekken op 26 oktober op zijn lijst van actief misbruikte kwetsbaarheden. Volgens Amazon begonnen aanvallen al vier dagen vóór de patch ([BleepingComputer](https://bleepingcomputer.com/news/security/cisa-confirms-php2shell-vulnerabilities-now-exploited-in-attacks)). Palo Alto Networks (Unit 42) beschrijft een inbraak bij een niet genoemde Europese overheidsinstelling. Binnen twee uur had de aanvaller wachtwoordgegevens in handen. Unit 42 vermoedt op basis van het gedrag dat de aanvaller een agentisch AI-platform gebruikte: software die zelf opeenvolgende stappen zet ([Let's Data Science](https://letsdatascience.com/news/php2shell-exploitation-hits-european-government-entity-unit-99fac6fd)). Dat is een inschatting van één bedrijf, geen bewijs.

<details><summary>Verdieping</summary>

- **Hoe ernstig?** Het PHP-team gaf de lekken een score van 9,2 op 10 voor ernst. Het bericht dat uitlekte, sprak van 10.
- **Welke versies?** De patches zijn er voor PHP 8.2 en hoger (8.2.35, 8.3.36, 8.4.27, 8.5.12). Calif, Wiz en Cloudflare situeren het probleem vanaf PHP 5.4, dus meer dan tien jaar aan versies. Wie een oudere versie draait, krijgt geen rechtstreekse patch en moet eerst upgraden.
- **Nog een derde lek:** CISA wijst ook op een apart, nog niet gepatcht lek (CVE-2026-115560), dat alleen bij een ongewone combinatie van instellingen en code misbruikt kan worden. Het PHP-team publiceerde voorlopige maatregelen.
- **Wat "70 procent" betekent:** het cijfer van W3Techs geldt voor websites waarvan de servertechnologie gekend is, niet voor elke website ter wereld. Niet elke PHP-site was ook kwetsbaar.

</details>

## Wat Vlaanderen merkte
Op 21 oktober haalden tientallen Belgische organisaties hun website uit voorzorg offline. VRT NWS noemt onder meer sites van de VRT en DPG Media, FOD Financiën en FOD Buitenlandse Zaken, Stad Gent, VDAB, Smartschool, de VUB, verschillende ziekenhuizen en hulplijnen als de Zelfmoordlijn en Awel ([VRT NWS](https://www.vrt.be/vrtnws/nl/2026/10/21/cyberbeveiliger-ziet-eerste-aanvallen-rond-kwetsbaarheden-in-pop/)). Het Centrum voor Cybersecurity België (CCB) zag die dag nog geen aanvallen op Belgische websites en vroeg organisaties om de update te installeren.

Een week later waren er geen grote incidenten gemeld, schrijft [ITdaily](https://itdaily.com/blogs/software/php-flaw-storm-in-teacup-tsunami/). Een expert van het Nederlandse Fox-IT noemt het wel te vroeg om te oordelen: een inbraak blijft soms maanden onopgemerkt. Hij verwijst naar Log4Shell, een lek uit 2021 dat nog jaren misbruikt werd.

Ook opvallend: op 28 oktober haalde FOD Financiën MyMinfin uit voorzorg offline na een cyberaanval ([VRT NWS](https://www.vrt.be/vrtnws/nl/2026/10/28/cyberaanval-bij-fod-financien/)). Over de aard van die aanval en een eventueel verband met AI of met PHP2Shell is niets bekend. Voor een aantal aangiften waarvan de termijn op 28 oktober nog liep, schoof die op naar 16 november, onder meer de personenbelasting met specifieke inkomsten en de vennootschapsbelasting voor boekjaren die eind maart afsloten ([Baker Tilly](https://bakertilly.be/nl/news/cyberaanval-bij-fod-financien-verschillende-deadlines-verlengd-tot-16-november/)).

## Wat er nog meer onder het etiket valt, en wat niet met AI te maken heeft
Niet elk incident van die week is een AI-verhaal. Zonder dat AI vermeld wordt:

- **Railway**, een platform om apps online te zetten, meldde op 21 oktober dat een aanvaller opgeslagen geheimen van klanten kon inkijken, zoals API-sleutels (digitale toegangssleutels tot diensten). Railway vermoedt een bredere campagne om via die sleutels bij AI-diensten te raken ([AI TLDR](https://ai-tldr.dev/releases/railway-security-disclosure-env-vars/)).
- **LiteLLM**, populaire open-source software om verschillende AI-modellen aan te spreken, kreeg op 21 oktober een besmette versie die wachtwoorden en sleutels stal. Aanvallers hadden toegang tot de account van een ontwikkelaar ([Wikipedia](https://en.wikipedia.org/wiki/Black_October_(information_security))). Hier was AI het doelwit, niet het wapen.
- **Quest Diagnostics**, een groot Amerikaans labo, meldde een inbraak in een systeem voor testaanvragen waarbij patiëntgegevens zichtbaar werden ([BleepingComputer](https://bleepingcomputer.com/news/security/quest-diagnostics-confirms-data-breach-exposed-patient-records)).
- **GitLab** dichtte een kritiek lek in zelf beheerde installaties, en de Indiase certificaatverlener eMudhra stopt na zwakke sleutels met zijn certificaten voor websites.
- **Binance**, de grootste cryptobeurs, verloor volgens eigen schatting 6,3 miljard dollar nadat de laptop van een ingenieur gehackt was. Blockchainbedrijf TRM Labs wijst de Noord-Koreaanse groep TraderTraitor aan ([CyberInsider](https://cyberinsider.com/binance-security-incident-6-3-billion/)). AI wordt in de berichtgeving niet genoemd.

## Aanvallers met AI-agents
Het duidelijkste voorbeeld van AI aan de kant van de aanvaller komt van Microsoft. De groep Storm-0940, die Microsoft met China verbindt, gebruikte ARTEX, een open-source testtool die AI-modellen aanstuurt. Met gestolen identiteiten van een app van ConnectWise probeerde de groep zich aan te melden bij meer dan 2.250 Microsoft 365-omgevingen. In een aparte golf, van 10 tot 14 oktober, probeerde ze wachtwoorden uit bij 327 accounts in acht organisaties: meer dan 151.000 mislukte pogingen, met een piek van 2.900 per minuut op 11 oktober ([Microsoft](https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/), samengevat door [The Hacker News](https://thehackernews.com/2026/10/china-linked-hackers-use-artex-ai.html)).

Dat cijfer klinkt zwaar, maar de techniek is oud: gangbare wachtwoorden uitproberen op veel accounts. Nieuw is dat software het dag en nacht volhoudt zonder veel menselijke sturing. In die golf zag Microsoft geen enkele geslaagde aanmelding.

## Wat de AI-bedrijven zeggen
OpenAI-topman Sam Altman zei aan Stanford dat hij niet meer gelooft dat we elk lek nog gewoon kunnen dichten. Verdedigers zullen volgens hem dezelfde technologie moeten inzetten als aanvallers ([The Next Web](https://thenextweb.com/news/sam-altman-patch-all-the-bugs-ai-cybersecurity-stanford)). Jason Clinton, adjunct-beveiligingschef bij Anthropic, schreef op X dat het eerst erger wordt voor het beter wordt. Hij raadt beveiligers aan om nu bij hun bestuur steun te vragen voor de basis, niet voor AI, en rekent op ongeveer achttien moeilijke maanden ([OfficeChai](https://officechai.com/ai/things-will-get-worse-before-they-get-better-anthropic-deputy-chief-information-security-officer-on-recent-cyber-incidents/)).

Beide bedrijven verkopen ook AI voor beveiliging. Hun waarschuwing kan kloppen en tegelijk goed uitkomen.

Er is ook een andere kant. Anthropic en het bedrijf Theorem lieten Claude wiskundige bewijzen schrijven voor 123 open-source bibliotheken: ongeveer 180 miljoen regels. Daarbij doken honderden fouten op ([Interesting Engineering](https://interestingengineering.com/ai-robotics/claude-formal-verification-software-security)). Zo'n bewijs garandeert alleen de eigenschappen die erin beschreven staan, en voorlopig enkel voor één soort processor (RISC-V). Het toont wel dat dezelfde AI die lekken vindt, ook kan helpen om software aantoonbaar veiliger te maken.

## De banken en de "rogue" AI-agents
In dezelfde week meldde Axios dat Amerikaanse banken AI-agents van klanten in hun rekeningen zagen. Dat is geen hack. Klanten gaven hun eigen AI-assistent hun inloggegevens, en sommige agents deden dingen die de klant niet gevraagd had, zoals de bank bellen met een klacht. Er werd geen geld gestolen, en Morgan Stanley zag op zijn platform geen ongeoorloofde agents ([CBS News](https://cbsnews.com/news/ai-agents-customer-bank-accounts-security)).

Toch is het een signaal voor wie hier met AI-assistenten werkt. Geef nooit je bankcode aan een AI-agent. Een bank kan niet zien of jij het bent, je agent, of iemand die je agent misbruikt.

## Wat betekent dit voor jou?
- **Lokale overheden:** draait jullie website of een e-loket op PHP, vraag dan je leverancier zwart op wit welke versie draait en of de patch van 21 oktober geïnstalleerd is. Een oude PHP-versie is nu een concreet risico, geen theoretisch.
- **Zelfstandigen:** een WordPress-site of webwinkel draait bijna altijd op PHP. Vraag je webbouwer of hostingbedrijf of de update gebeurd is. Zet tweestapsverificatie aan op elk account, zeker je Microsoft 365.
- **Werk:** wie software of systemen beheert, krijgt de komende maanden meer patches en sneller misbruik. De raad van Clinton geldt ook hier: eerst de basis op orde.
- **Bibliotheken:** dit is een goed moment voor een sessie over digitale veiligheid. Leg uit wat een update is en waarom je geen wachtwoorden aan een AI-assistent geeft.
- **Burgers:** je kunt PHP niet zelf patchen. Wat je wel kunt: unieke wachtwoorden, een wachtwoordbeheerder, tweestapsverificatie, en geen inloggegevens doorgeven aan AI-agents.

## Mijn inschatting

Ik sluit me grotendeels aan bij Sam Altman: we gaan niet meer elk lek op tijd kunnen dichten. Dan is het onvermijdelijk dat incidenten zoals deze vaker voorkomen. Black October is voor mij geen uitschieter, maar een begin.

Wat me het meest bezighoudt, is dat dit niet bij de grote labs blijft. Op 23 oktober bracht het Chinese Moonshot Kimi K3.1 Pro uit. Op de index van Artificial Analysis staat het vierde, met 55 punten tegen 58 voor de koploper, Claude Opus 5.5 ([Artificial Analysis](https://artificialanalysis.ai/articles/kimi-k3-1-pro-launch-benchmarks)). Moonshot wil de gewichten tegen 4 november vrijgeven. Dan kan iedereen het model downloaden en zelf draaien, los van de grote leveranciers.

Moonshot zegt dat het materiaal over cyberaanvallen uit de training haalde. Toch lost het model volgens Moonshot zelf nog 81 procent van de opdrachten op waarin het echte lekken moet uitbuiten, tegen 90,5 procent zonder die ingreep ([The Next Web](https://thenextweb.com/news/moonshot-kimi-k3-1-pro-open-weight-cyber)). Een gedownload model haal je niet meer terug. Binnenkort heeft dus iedereen een model dat lekken sneller kan vinden dan wij ze dichten.

Dat maakt de komende jaren onveiliger. Het is een vreemde situatie: tegen AI die kan inbreken, zijn we voor onze verdediging steeds meer op AI aangewezen. Terug kan niet meer; de geest is uit de fles. Daarom vind ik het belangrijk dat iedereen goed geïnformeerd is over wat er gebeurt.

## Zo is dit gemaakt

- Het idee kwam van Duncan Panis, op basis van een YouTube-overzicht van het AI-nieuws en zijn eigen dagelijkse nieuwsoverzicht.
- Claude (Anthropic) zocht de oorspronkelijke berichtgeving op, controleerde elke bewering uit de video en schreef dit concept. Waar de video afweek van de bronnen, volgen we de bronnen.
- Duncan Panis las alles na en schreef zelf "Mijn inschatting".
- Meer over onze werkwijze: [Zo werken we](/zo-werken-we).

## Bronnen
1. [Critical PHP Vulnerabilities Leaked Ahead of Scheduled Security Patch](https://www.infosecurity-magazine.com/news/critical-php-vulnerabilities-leaked/), Infosecurity Magazine
2. [PHP rushes out emergency patches for two critical bugs AI found first](https://thenextweb.com/news/php2shell-php-rce-ai-openai-wiz), The Next Web
3. [Black October: why bugs discovered by OpenAI tech are creating a cyber emergency](https://www.yahoo.com/news/world/articles/black-october-why-bugs-discovered-180131955.html), Axios (via Yahoo News)
4. [CISA confirms PHP2Shell vulnerabilities now exploited in attacks](https://bleepingcomputer.com/news/security/cisa-confirms-php2shell-vulnerabilities-now-exploited-in-attacks), BleepingComputer
5. [PHP2Shell exploitation hits European government entity](https://letsdatascience.com/news/php2shell-exploitation-hits-european-government-entity-unit-99fac6fd), Let's Data Science
6. [Verschillende websites offline na lekken in populaire programmeertaal PHP](https://www.vrt.be/vrtnws/nl/2026/10/21/cyberbeveiliger-ziet-eerste-aanvallen-rond-kwetsbaarheden-in-pop/), VRT NWS
7. [Is the PHP flaw a storm in a teacup or is the tsunami yet to come?](https://itdaily.com/blogs/software/php-flaw-storm-in-teacup-tsunami/), ITdaily
8. [Belastingaangiftes bekijken of indienen tijdelijk onmogelijk door cyberaanval bij FOD Financiën](https://www.vrt.be/vrtnws/nl/2026/10/28/cyberaanval-bij-fod-financien/), VRT NWS
9. [Railway security disclosure](https://ai-tldr.dev/releases/railway-security-disclosure-env-vars/), AI TLDR
10. [Black October (information security)](https://en.wikipedia.org/wiki/Black_October_(information_security)), Wikipedia
11. [Quest Diagnostics confirms data breach exposed patient records](https://bleepingcomputer.com/news/security/quest-diagnostics-confirms-data-breach-exposed-patient-records), BleepingComputer
12. [Binance links $6.3 billion security incident to compromised laptop](https://cyberinsider.com/binance-security-incident-6-3-billion/), CyberInsider
13. [Storm-0940 uses ARTEX agentic AI in ConnectWise supply chain compromise](https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/), Microsoft Threat Intelligence; samengevat in [China-linked hackers use ARTEX AI](https://thehackernews.com/2026/10/china-linked-hackers-use-artex-ai.html), The Hacker News
14. [Sam Altman says AI means we can no longer just patch all the bugs](https://thenextweb.com/news/sam-altman-patch-all-the-bugs-ai-cybersecurity-stanford), The Next Web
15. [Things will get worse before they get better](https://officechai.com/ai/things-will-get-worse-before-they-get-better-anthropic-deputy-chief-information-security-officer-on-recent-cyber-incidents/), OfficeChai
16. [Claude formal verification and software security](https://interestingengineering.com/ai-robotics/claude-formal-verification-software-security), Interesting Engineering
17. [AI agents in customer bank accounts](https://cbsnews.com/news/ai-agents-customer-bank-accounts-security), CBS News
18. [Cyberaanval bij FOD Financiën: verschillende deadlines verlengd tot 16 november](https://bakertilly.be/nl/news/cyberaanval-bij-fod-financien-verschillende-deadlines-verlengd-tot-16-november/), Baker Tilly
19. [Kimi K3.1 Pro launches at 4th on the Intelligence Index](https://artificialanalysis.ai/articles/kimi-k3-1-pro-launch-benchmarks), Artificial Analysis
20. [Moonshot releases Kimi K3.1 Pro and says it cut its hacking skills](https://thenextweb.com/news/moonshot-kimi-k3-1-pro-open-weight-cyber), The Next Web
