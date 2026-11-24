// Mail "Nieuw gratis materiaal": één mail per nieuw lespakket, voor de lijst van lesgevers.
// De site bouwt hem op /mail/materiaal/<slug>.html; die HTML gaat als conceptcampagne naar Brevo.
// Volgt de huisstijl (versie 1.0): geel alleen voor het blokje "AI" en de ene knop.
import { groepen, type Pakket } from "./materiaal";
import { datumLeesbaar } from "./edities";
import { SITE_URL } from "./seo";

const K = { buiten: "#e8eae4", papier: "#ffffff", vlak: "#f2f3ef", inkt: "#20262b", grijs: "#5c6368", lijn: "#cfd3cc", geel: "#ffd400" };
const TEKST = "Georgia,'Times New Roman',serif";
const UI = "Arial,Helvetica,sans-serif";

export function materiaalOnderwerp(p: Pakket): string {
  return `Nieuw en gratis: ${p.titel}`;
}

export function materiaalMail(p: Pakket): string {
  const url = `${SITE_URL}/materiaal/${p.slug}`;
  const rij = (k: string, v: string) =>
    v ? `<tr><td style="padding:6px 16px 6px 0;font-family:${UI};font-size:13px;color:${K.grijs};vertical-align:top;white-space:nowrap;">${k}</td><td style="padding:6px 0;font-family:${UI};font-size:14px;color:${K.inkt};">${v}</td></tr>` : "";
  const bestanden = groepen(p)
    .map((g) => `<li style="margin:0 0 6px 0;font-family:${UI};font-size:14px;line-height:1.5;color:${K.inkt};"><strong>${g.bestanden.length === 1 ? g.bestanden[0].naam : g.stam}</strong>${g.omschrijving ? `: ${g.omschrijving}` : ""}</li>`)
    .join("");
  return `<!doctype html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<meta name="onderwerp" content="${materiaalOnderwerp(p).replace(/"/g, "&quot;")}"><title>${p.titel}</title></head>
<body style="margin:0;padding:0;background:${K.buiten};">
<div style="display:none;max-height:0;overflow:hidden;">${p.samenvatting}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${K.buiten};"><tr><td align="center" style="padding:20px 8px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:${K.papier};">
<tr><td style="padding:28px 32px 0 32px;">
<p style="margin:0;font-family:Georgia,serif;font-size:22px;font-weight:bold;color:${K.inkt};"><span style="background:${K.geel};font-family:${UI};padding:0 5px;">AI</span> Ontcijferd</p>
<p style="margin:6px 0 0 0;font-family:${UI};font-size:13px;color:${K.grijs};">Nieuw gratis materiaal</p>
</td></tr>
<tr><td style="padding:22px 32px 0 32px;">
<h1 style="margin:0 0 10px 0;font-family:${TEKST};font-size:26px;line-height:1.25;color:${K.inkt};">${p.titel}</h1>
<p style="margin:0 0 16px 0;font-family:${UI};font-size:17px;line-height:1.6;color:${K.inkt};">${p.samenvatting}</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${K.vlak};"><tr><td style="padding:12px 16px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
${rij("Voor wie", p.deelnemers)}${rij("Niveau", p.niveau)}${rij("Duur", p.duur)}${rij("Versie", `${p.versie}, bijgewerkt op ${datumLeesbaar(p.bijgewerkt)}`)}${rij("Licentie", `${p.licentie}: gratis, en je mag het aanpassen`)}
</table></td></tr></table>
</td></tr>
<tr><td style="padding:20px 32px 0 32px;">
<p style="margin:0 0 8px 0;font-family:${UI};font-size:13px;font-weight:bold;color:${K.inkt};">In het pakket</p>
<ul style="margin:0;padding:0 0 0 18px;">${bestanden}</ul>
</td></tr>
<tr><td style="padding:24px 32px 0 32px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="background:${K.geel};padding:14px 26px;"><a href="${url}" style="font-family:${UI};font-size:16px;font-weight:bold;color:${K.inkt};text-decoration:none;">Bekijk en download het pakket</a></td></tr></table>
<p style="margin:14px 0 0 0;font-family:${UI};font-size:14px;line-height:1.5;color:${K.inkt};">Gaf je de sessie? Antwoord gewoon op deze mail: wanneer, waar, voor hoeveel mensen en wat werkte.</p>
</td></tr>
<tr><td style="padding:24px 32px 26px 32px;">
<p style="margin:0;padding:14px 0 0 0;border-top:1px solid ${K.lijn};font-family:${UI};font-size:12px;line-height:1.55;color:${K.grijs};">AI Ontcijferd: AI zonder hype, door Duncan Panis. Je krijgt deze mail omdat je je inschreef voor nieuw gratis materiaal op <a href="${SITE_URL}" style="color:${K.grijs};">aiontcijferd.be</a>. <a href="{{ unsubscribe }}" style="color:${K.grijs};">Uitschrijven</a> kan met één klik.</p>
</td></tr>
</table></td></tr></table>
</body></html>`;
}
