// Maakt het woordmerk en het monogram van AI Ontcijferd (huisstijl 1.0) als SVG en PNG.
// Tekst wordt omgezet in vormen, zodat de bestanden overal hetzelfde ogen zonder lettertypen.
// Gebruik: node scripts/merk.mjs   (vanuit de map site/)
import fs from "node:fs";
import path from "node:path";
import satori from "satori";
import sharp from "sharp";

const NM = path.resolve("node_modules/@fontsource");
const fonts = [
  { name: "Atkinson", data: fs.readFileSync(path.join(NM, "atkinson-hyperlegible-next/files/atkinson-hyperlegible-next-latin-700-normal.woff")), weight: 700, style: "normal" },
  { name: "Literata", data: fs.readFileSync(path.join(NM, "literata/files/literata-latin-600-normal.woff")), weight: 600, style: "normal" },
];
const K = { inkt: "#20262b", papier: "#f2f3ef", geel: "#ffd400" };
const UIT = path.resolve("public/merk");
fs.mkdirSync(UIT, { recursive: true });

const el = (type, style, children) => ({ type, props: { style, children } });

// Maten volgens de gids: blok = 1,2 x hoofdlettershoogte van "Ontcijferd",
// "AI" krijgt links en rechts een kwart van de blokhoogte, tussenruimte een vijfde.
const F = 100; // lettergrootte in px; hoofdletterhoogte Literata ~ 0,7 F
const blok = Math.round(0.7 * F * 1.2);
const woordmerk = (achtergrond, tekst) =>
  el("div", { display: "flex", alignItems: "center", width: 760, height: blok + 72, padding: "0 28px", background: achtergrond }, [
    el("div", { display: "flex", alignItems: "center", justifyContent: "center", height: blok, padding: `0 ${Math.round(blok * 0.25)}px`, background: K.geel, color: K.inkt, fontFamily: "Atkinson", fontWeight: 700, fontSize: Math.round(F * 0.78) }, "AI"),
    el("div", { display: "flex", marginLeft: Math.round(blok * 0.2), color: tekst, fontFamily: "Literata", fontWeight: 600, fontSize: F, lineHeight: 1 }, "Ontcijferd"),
  ]);
const monogram = (maat) =>
  el("div", { display: "flex", alignItems: "center", justifyContent: "center", width: maat, height: maat, background: K.geel, color: K.inkt, fontFamily: "Atkinson", fontWeight: 700, fontSize: Math.round(maat * 0.5) }, "AI");

async function maak(naam, boom, breedte, hoogte, png = []) {
  const svg = await satori(boom, { width: breedte, height: hoogte, fonts });
  fs.writeFileSync(path.join(UIT, `${naam}.svg`), svg);
  for (const b of png) {
    await sharp(Buffer.from(svg), { density: 72 * (b / breedte) * 4 }).resize({ width: b }).png({ compressionLevel: 9 }).toFile(path.join(UIT, `${naam}-${b}.png`));
  }
  return svg;
}

const B = 760, H = blok + 72;
await maak("woordmerk", woordmerk("transparent", K.inkt), B, H, [600, 1200]);
await maak("woordmerk-donker", woordmerk(K.inkt, K.papier), B, H, [600, 1200]);
const mono = await maak("monogram", monogram(512), 512, 512, [180, 512]);
// Standaard deelafbeelding voor pagina's zonder eigen beeld
const og = el("div", { display: "flex", flexDirection: "column", justifyContent: "space-between", width: 1056, height: 502, background: K.papier, padding: "64px 72px", color: K.inkt, fontFamily: "Atkinson" }, [
  el("div", { display: "flex", alignItems: "center", fontSize: 34 }, [
    el("span", { background: K.geel, fontWeight: 700, padding: "0 7px", marginRight: 9 }, "AI"),
    el("span", { fontFamily: "Literata", fontWeight: 600 }, "Ontcijferd"),
  ]),
  el("div", { display: "flex", fontFamily: "Literata", fontWeight: 600, fontSize: 96 }, "AI zonder hype."),
  el("div", { display: "flex", justifyContent: "space-between", fontSize: 26, color: "#5c6368" }, [
    el("div", {}, "Wat er in AI gebeurt, en wat het betekent voor Vlaanderen"),
    el("div", { fontWeight: 700, color: K.inkt }, "aiontcijferd.be"),
  ]),
]);
fs.writeFileSync(path.resolve("public/og.png"), await sharp(Buffer.from(await satori(og, { width: 1200, height: 630, fonts }))).png({ compressionLevel: 9 }).toBuffer());
fs.copyFileSync(path.join(UIT, "monogram.svg"), path.resolve("public/favicon.svg"));
fs.copyFileSync(path.join(UIT, "monogram-512.png"), path.resolve("public/logo.png"));
console.log("klaar:", fs.readdirSync(UIT).join(", "), mono.length);
