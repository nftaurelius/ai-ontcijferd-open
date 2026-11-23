// "Verder denken": essays over AI van Duncan Panis op duncanpanis.be (content/verder-denken.yaml).
import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";

export type Essay = { titel: string; url: string; datum: string; samenvatting: string };

export function essays(): Essay[] {
  const pad = path.resolve(process.cwd(), "..", "content", "verder-denken.yaml");
  if (!fs.existsSync(pad)) return [];
  const ruw = (yaml.load(fs.readFileSync(pad, "utf-8")) as any[]) ?? [];
  return ruw
    .map((e) => ({ ...e, datum: e.datum instanceof Date ? e.datum.toISOString().slice(0, 10) : String(e.datum ?? "") }))
    .sort((a, b) => b.datum.localeCompare(a.datum));
}
