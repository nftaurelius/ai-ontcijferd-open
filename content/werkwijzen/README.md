# Werkwijzen: prompts, skills en agents

Elke werkwijze is een bestand `<slug>.md` hier, met frontmatter (de bijsluiter) en een uitleg in Markdown.
De site maakt er `/werkwijzen` en `/werkwijzen/<slug>` van.

- **prompt**: de prompt staat in de uitleg, in een codeblok onder de kop `## De prompt`. De site zet er een kopieerknop bij.
- **skill**: een map `<slug>/` naast het bestand, met minstens `SKILL.md`. De site maakt er een zip van (`/werkwijzen/<slug>.zip`), met de map erin, klaar om op te laden in Claude.
- **agent**: zoals een skill, plus in de uitleg een lijst van wat de agent wel en niet mag aanraken.

Frontmatter: `titel`, `soort` (prompt | skill | agent), `samenvatting`, `voor` (labels zoals op /voor), `niveau`,
`versie`, `bijgewerkt`, `getest` (eerlijk: met welk model en wanneer, of "Nog niet getest"), `licentie`,
`status` (beschikbaar | in-voorbereiding). Volg de huisstijl: bijsluiter, bron, datum.
