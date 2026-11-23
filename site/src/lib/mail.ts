// De nieuwsbriefmail van een weekeditie, in de huisstijl van de site.
// De site bouwt hem per editie op /mail/<week>.html; die HTML gaat als campagne naar Brevo.
// Mailprogramma's kennen geen gewone CSS: alles staat in tabellen met inline stijlen.

import { HYPE_STANDEN, datumLeesbaar, weekNummer, type Editie } from "./edities";
import { SITE_URL } from "./seo";

const K = {
  buiten: "#e8eae4",
  papier: "#ffffff",
  vlak: "#f2f3ef",
  inkt: "#20262b",
  grijs: "#5c6368",
  lijn: "#cfd3cc",
  geel: "#ffd400",
  markeer: "#ffe773",
  link: "#20262b",
};
// Huisstijl 1.0: koppen in Georgia, tekst in Arial (webfonts werken niet betrouwbaar in mail).
const KOP = "Literata,Georgia,'Times New Roman',serif";
const UI = "'Atkinson Hyperlegible Next',Arial,Helvetica,sans-serif";
const TEKST = UI;

/** Voegt inline stijlen toe aan de eenvoudige HTML die marked maakt. */
function inline(html: string, grootte = 16): string {
  return html
    .replace(/<p>/g, `<p style="margin:0 0 14px 0;font-family:${TEKST};font-size:${grootte}px;line-height:1.6;color:${K.inkt};">`)
    .replace(/<ul>/g, `<ul style="margin:0 0 14px 0;padding:0 0 0 20px;">`)
    .replace(/<ol>/g, `<ol style="margin:0 0 14px 0;padding:0 0 0 20px;">`)
    .replace(/<li>/g, `<li style="margin:0 0 8px 0;font-family:${TEKST};font-size:${grootte}px;line-height:1.55;color:${K.inkt};">`)
    .replace(/<a href=/g, `<a style="color:${K.link};text-decoration:underline;" href=`)
    .replace(/<strong>/g, `<strong style="font-weight:bold;">`)
    .replace(/<blockquote>/g, `<blockquote style="margin:0 0 14px 0;padding:0 0 0 12px;border-left:3px solid ${K.lijn};color:${K.grijs};">`);
}

/**
 * Geen links in de lopende tekst. Veel links naar veel verschillende domeinen is voor
 * spamfilters (vooral Outlook) een sterk signaal; de mail met links naar acht domeinen
 * kwam in de ongewenste e-mail, de eerste mail met twee links naar de site niet.
 * De linktekst blijft staan; de bronnen staan bij elk onderwerp op de site.
 */
const zonderLinks = (html: string) => html.replace(/<a\b[^>]*>([\s\S]*?)<\/a>/g, "$1");

const eerstePara = (html: string) => html.match(/<p>[\s\S]*?<\/p>/)?.[0] ?? "";
const vlaamsBlok = (html: string) =>
  html.match(/<p><strong>Waarom doet het ertoe voor Vlaanderen\?<\/strong><\/p>\s*(<ul>[\s\S]*?<\/ul>)/)?.[1] ?? "";

function hypeMeter(index: number): string {
  const vakjes = HYPE_STANDEN.map(
    (_, i) =>
      `<td width="34" height="10" style="width:34px;height:10px;font-size:8px;line-height:8px;background:${i === index ? K.geel : K.papier};border:1px solid ${i === index ? K.geel : K.lijn};">&nbsp;</td><td width="3" style="width:3px;font-size:8px;line-height:8px;">&nbsp;</td>`,
  ).join("");
  return `<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>${vakjes}</tr></table>`;
}

function blok(inhoud: string, opties: { boven?: number; onder?: number } = {}): string {
  return `<tr><td style="padding:${opties.boven ?? 0}px 32px ${opties.onder ?? 0}px 32px;" class="rand">${inhoud}</td></tr>`;
}

function kader(kop: string, inhoud: string, rand: "links" | "boven" = "links"): string {
  void rand;
  return `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${K.vlak};"><tr><td style="padding:14px 18px 2px 18px;">
<p style="margin:0 0 8px 0;font-family:${UI};font-size:14px;font-weight:bold;color:${K.inkt};">${kop}</p>
${inhoud}</td></tr></table>`;
}

function knop(href: string, tekst: string): string {
  return `<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="background:${K.geel};padding:14px 26px;"><a href="${href}" style="font-family:${UI};font-size:16px;font-weight:bold;color:${K.inkt};text-decoration:none;">${tekst}</a></td>
</tr></table>`;
}

export function onderwerpregel(e: Editie): string {
  return `${weekNummer(e.week).replace(/^week/, "Stand van AI, week").replace(/, \d{4}$/, "")}: ${e.onderwerpen.map((o) => o.titel.split(/[,:]/)[0]).join(" · ")}`;
}

export function nieuwsbriefMail(e: Editie): string {
  const url = `${SITE_URL}/edities/${e.week}`;
  const voorvertoning = e.kernTekst.split(/(?<=[.!?])\s/)[0];
  const eersteZin = voorvertoning;
  const rest = e.kernTekst.slice(eersteZin.length).trim();
  const n = e.onderwerpen.length;

  const inhoud = e.onderwerpen
    .map(
      (o, i) =>
        `<tr><td valign="top" style="padding:6px 10px 6px 0;font-family:${UI};font-size:14px;font-weight:bold;color:${K.inkt};">${i + 1}.</td><td style="padding:6px 0;font-family:${UI};font-size:14px;line-height:1.45;">${o.titel}${o.hype ? `<br><span style="color:${K.grijs};font-size:12px;">Hype-meter: ${o.hype.stand}</span>` : ""}</td></tr>`,
    )
    .join("");

  const onderwerpen = e.onderwerpen
    .map((o, i) => {
      const labels = o.labels.length ? `<p style="margin:0 0 12px 0;font-family:${UI};font-size:12px;color:${K.grijs};">Voor: ${o.labels.join(" · ")}</p>` : "";
      const hype = o.hype
        ? `<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 16px 0;"><tr><td style="padding:0 0 6px 0;font-family:${UI};font-size:13px;font-weight:bold;color:${K.inkt};">Hype-meter: ${o.hype.stand}</td></tr><tr><td>${hypeMeter(o.hype.index)}</td></tr>${o.hype.uitleg ? `<tr><td style="padding:8px 0 0 0;font-family:${UI};font-size:13px;line-height:1.5;color:${K.grijs};">${o.hype.uitleg}</td></tr>` : ""}</table>`
        : "";
      const vl = vlaamsBlok(o.html);
      return [
        blok(`<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td height="3" style="height:3px;background:${K.inkt};font-size:3px;line-height:3px;">&nbsp;</td></tr></table>`, { boven: 28 }),
        blok(
          `<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 10px 0;"><tr>
<td width="32" height="32" align="center" style="width:32px;height:32px;background:${K.geel};font-family:${UI};font-size:16px;font-weight:bold;color:${K.inkt};">${i + 1}</td>
<td style="padding:0 0 0 10px;font-family:${UI};font-size:13px;color:${K.grijs};">Onderwerp ${i + 1} van ${n}</td></tr></table>
<h2 style="margin:0 0 8px 0;font-family:${KOP};font-size:22px;line-height:1.3;color:${K.inkt};">${o.titel}</h2>
${labels}${hype}${inline(zonderLinks(eerstePara(o.html)))}`,
          { boven: 18 },
        ),
        vl ? blok(kader("Waarom het ertoe doet voor Vlaanderen", inline(zonderLinks(vl), 15)), { boven: 4 }) : "",
        blok(`<p style="margin:12px 0 0 0;font-family:${UI};font-size:14px;"><a href="${url}#${o.slug}" style="color:${K.link};font-weight:bold;">Lees verder, met verdieping en bronnen &rarr;</a></p>`),
      ].join("\n");
    })
    .join("\n");

  const rubriek = (kop: string, html: string) =>
    html ? blok(kader(kop, inline(zonderLinks(html), 15), "boven"), { boven: 24 }) : "";

  const inschattingEerste = eerstePara(e.inschatting);

  return `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<meta name="onderwerp" content="${onderwerpregel(e).replace(/"/g, "&quot;")}">
<title>${e.titel}</title>
<style>
body{margin:0;padding:0;background:${K.buiten};-webkit-text-size-adjust:100%}
@media (max-width:620px){.kader{width:100%!important}.rand{padding-left:18px!important;padding-right:18px!important}}
</style>
</head>
<body style="margin:0;padding:0;background:${K.buiten};">
<div style="display:none;max-height:0;overflow:hidden;">${voorvertoning}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${K.buiten};">
<tr><td align="center" style="padding:20px 8px;">
<table role="presentation" class="kader" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:${K.papier};">

${blok(
  `<p style="margin:0;font-family:${KOP};font-size:22px;font-weight:bold;color:${K.inkt};"><span style="background:${K.geel};font-family:${UI};padding:0 5px;">AI</span> Ontcijferd</p>
<p style="margin:4px 0 0 0;font-family:${UI};font-size:13px;color:${K.grijs};">Stand van AI &middot; ${weekNummer(e.week)} &middot; ${datumLeesbaar(e.datum)}</p>`,
  { boven: 26, onder: 6 },
)}

${blok(
  `<p style="margin:18px 0 8px 0;font-family:${UI};font-size:14px;font-weight:bold;color:${K.inkt};">De week in 30 seconden</p>
<p style="margin:0 0 6px 0;font-family:${TEKST};font-size:18px;line-height:1.6;color:${K.inkt};"><span style="background:${K.markeer};">${eersteZin}</span> ${rest}</p>`,
)}

${blok(
  `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid ${K.lijn};border-bottom:1px solid ${K.lijn};margin:14px 0 0 0;"><tr><td style="padding:12px 0 8px 0;">
<p style="margin:0 0 6px 0;font-family:${UI};font-size:14px;font-weight:bold;color:${K.grijs};">In deze editie</p>
<table role="presentation" cellpadding="0" cellspacing="0" border="0">${inhoud}</table>
</td></tr></table>`,
)}

${onderwerpen}

${rubriek("Ruis van de week", e.ruis)}
${rubriek("Woord van de week", e.woord)}

${blok(
  `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${K.vlak};border-left:4px solid ${K.inkt};"><tr><td style="padding:16px 18px 4px 18px;">
<p style="margin:0 0 8px 0;font-family:${UI};font-size:14px;font-weight:bold;color:${K.inkt};">Mijn inschatting</p>
${inline(zonderLinks(inschattingEerste))}
<p style="margin:0 0 14px 0;font-family:${UI};font-size:14px;"><a href="${url}#inschatting" style="color:${K.link};font-weight:bold;">Lees mijn volledige inschatting &rarr;</a></p>
<p style="margin:0 0 12px 0;font-family:${UI};font-size:13px;color:${K.grijs};">Duncan Panis, eindredacteur</p>
</td></tr></table>`,
  { boven: 28 },
)}

${blok(`<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center">${knop(url, "Lees de hele editie op de site")}</td></tr></table>`, { boven: 28, onder: 8 })}

${blok(
  `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${K.vlak};"><tr><td style="padding:14px 18px;font-family:${UI};font-size:14px;line-height:1.5;color:${K.inkt};">
<strong>Ken je iemand die dit moet lezen?</strong> Stuur deze mail gewoon door. Kreeg je hem doorgestuurd? <a href="${SITE_URL}/nieuwsbrief" style="color:${K.link};font-weight:bold;">Schrijf je zelf in</a>.
</td></tr></table>`,
  { boven: 22, onder: 6 },
)}

${blok(
  `<p style="margin:18px 0 0 0;padding:16px 0 0 0;border-top:1px solid ${K.lijn};font-family:${UI};font-size:12px;line-height:1.55;color:${K.grijs};">AI Ontcijferd: AI zonder hype, door Duncan Panis. AI-agents maken het concept, een mens leest alles na. <a href="${SITE_URL}/zo-werken-we" style="color:${K.grijs};">Zo werken we</a>.<br>Je krijgt deze mail omdat je je inschreef op <a href="${SITE_URL}" style="color:${K.grijs};">aiontcijferd.be</a>. Voeg redactie@aiontcijferd.be toe aan je contactpersonen, dan komt de mail niet bij je ongewenste e-mail terecht. <a href="{{ unsubscribe }}" style="color:${K.grijs};">Uitschrijven</a> kan met één klik.</p>`,
  { onder: 26 },
)}

</table>
</td></tr>
</table>
</body>
</html>`;
}
