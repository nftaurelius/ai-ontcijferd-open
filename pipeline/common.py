"""Gedeelde hulpmiddelen: paden, instellingen, modeloproepen en kostenlog."""

from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys
import time
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PROMPTS = ROOT / "prompts"
CONTENT = ROOT / "content"

DROOG = os.environ.get("AIO_DROOG") == "1"  # proefdraai zonder echte modellen


def config() -> dict:
    return yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))


def bronnen() -> list[dict]:
    data = yaml.safe_load((ROOT / "sources.yaml").read_text(encoding="utf-8"))
    return [b for b in data["bronnen"] if b.get("actief", True)]


def nu() -> dt.datetime:
    return dt.datetime.now(ZoneInfo(config().get("tijdzone", "Europe/Brussels")))


def prompt(naam: str, **velden) -> str:
    tekst = (PROMPTS / f"{naam}.md").read_text(encoding="utf-8")
    for sleutel, waarde in velden.items():
        tekst = tekst.replace("{" + sleutel + "}", str(waarde))
    return tekst


def systeemprompt(rol: str, **velden) -> str:
    return prompt("statuut") + "\n\n" + prompt(rol, **velden)


def log(bericht: str) -> None:
    print(f"[{nu():%H:%M:%S}] {bericht}", flush=True)


def lees_json(pad: Path, standaard):
    return json.loads(pad.read_text(encoding="utf-8")) if pad.exists() else standaard


def schrijf_json(pad: Path, data) -> None:
    pad.parent.mkdir(parents=True, exist_ok=True)
    pad.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def haal_json(tekst: str):
    """Haal de eerste geldige JSON-array of -object uit een modelantwoord."""
    tekst = re.sub(r"```(?:json)?", "", tekst)
    decoder = json.JSONDecoder()
    for pos, teken in enumerate(tekst):
        if teken in "[{":
            try:
                waarde, _ = decoder.raw_decode(tekst, pos)
                return waarde
            except json.JSONDecodeError:
                continue
    raise ValueError("Geen geldige JSON in modelantwoord (begin: " + tekst[:300].replace("\n", " ") + ")")


def rapporteer_fouten(naam: str, fouten: list[str]) -> None:
    """Bewaar fouten in data/fouten/, zodat ze terug te lezen zijn zonder de Actions-logs."""
    pad = DATA / "fouten" / f"{naam}.txt"
    pad.parent.mkdir(parents=True, exist_ok=True)
    with pad.open("a", encoding="utf-8") as f:
        f.write(f"# {nu().isoformat(timespec='seconds')}\n" + "\n".join(fouten) + "\n\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(f"### Fouten ({naam})\n" + "\n".join(f"- {x}" for x in fouten) + "\n")


# ---------------------------------------------------------------- modellen

class Noodrem(RuntimeError):
    """Te veel modeloproepen in één run: stop voor het geld kost."""


class ModelFout(RuntimeError):
    """Het model gaf geen bruikbaar antwoord (afgekapt, leeg of geweigerd)."""


_oproepen = 0


def vraag(rol: str, systeem: str, gebruiker: str) -> str:
    """Stuur één bericht naar het model dat in config.yaml bij deze rol hoort."""
    global _oproepen
    cfg = config()
    _oproepen += 1
    if _oproepen > cfg["limieten"]["max_oproepen_per_run"]:
        raise Noodrem(f"Meer dan {cfg['limieten']['max_oproepen_per_run']} oproepen in één run.")

    m = cfg["modellen"][rol]
    if DROOG:
        from pipeline.droog import nepantwoord
        antwoord, tin, tuit = nepantwoord(rol, gebruiker), len(gebruiker) // 4, 500
    elif m["leverancier"] == "anthropic":
        antwoord, tin, tuit = _anthropic(m, systeem, gebruiker)
    elif m["leverancier"] == "openai":
        antwoord, tin, tuit = _openai(m, systeem, gebruiker)
    else:
        raise ValueError(f"Onbekende leverancier: {m['leverancier']}")

    _log_kosten(rol, m, tin, tuit)
    return antwoord


def _opnieuw(functie, pogingen: int = 3):
    for poging in range(1, pogingen + 1):
        try:
            return functie()
        except Exception as fout:  # netwerk, overbelasting, tijdslimiet
            if poging == pogingen:
                raise
            wacht = 10 * poging
            log(f"Oproep mislukt ({fout.__class__.__name__}), nieuwe poging over {wacht}s")
            time.sleep(wacht)


def _anthropic(m: dict, systeem: str, gebruiker: str):
    import anthropic

    client = anthropic.Anthropic()  # leest ANTHROPIC_API_KEY
    extra = {}
    if m.get("effort"):
        extra["output_config"] = {"effort": m["effort"]}
    if m.get("thinking"):
        extra["thinking"] = {"type": m["thinking"]}

    def oproep():
        # Streamen: nodig bij grote max_tokens, en denktijd telt mee in max_tokens
        with client.messages.stream(
            model=m["model"], max_tokens=m["max_tokens"], system=systeem,
            messages=[{"role": "user", "content": gebruiker}], **extra,
        ) as stroom:
            return stroom.get_final_message()

    r = _opnieuw(oproep)
    tekst = "".join(b.text for b in r.content if b.type == "text")
    if r.stop_reason == "refusal":
        raise ModelFout(f"model weigerde (stop_reason refusal)")
    if r.stop_reason == "max_tokens":
        raise ModelFout(f"antwoord afgekapt op max_tokens={m['max_tokens']} "
                        f"(tekst: {len(tekst)} tekens); verhoog max_tokens of verlaag effort")
    if not tekst.strip():
        raise ModelFout(f"leeg antwoord (stop_reason {r.stop_reason})")
    return tekst, r.usage.input_tokens, r.usage.output_tokens


def _openai(m: dict, systeem: str, gebruiker: str):
    if m["model"] in ("", "VUL_IN"):
        sys.exit("Vul in config.yaml het OpenAI-model voor de tegenspreker in.")
    import openai

    client = openai.OpenAI()  # leest OPENAI_API_KEY
    try:
        r = _opnieuw(lambda: client.responses.create(
            model=m["model"], instructions=systeem, input=gebruiker,
            max_output_tokens=m["max_tokens"],
        ))
        return r.output_text, r.usage.input_tokens, r.usage.output_tokens
    except (openai.BadRequestError, openai.NotFoundError) as fout:
        # Sommige modellen zijn enkel via Chat Completions beschikbaar
        log(f"Responses API weigerde ({fout.__class__.__name__}); probeer Chat Completions")
        r = _opnieuw(lambda: client.chat.completions.create(
            model=m["model"], max_completion_tokens=m["max_tokens"],
            messages=[{"role": "system", "content": systeem}, {"role": "user", "content": gebruiker}],
        ))
        return r.choices[0].message.content or "", r.usage.prompt_tokens, r.usage.completion_tokens


def _log_kosten(rol: str, m: dict, tin: int, tuit: int) -> None:
    pad = ROOT / os.environ.get("AIO_KOSTEN_PAD", "data/kosten.csv")
    nieuw = not pad.exists()
    pad.parent.mkdir(parents=True, exist_ok=True)
    with pad.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nieuw:
            w.writerow(["tijd", "rol", "leverancier", "model", "tokens_in", "tokens_uit", "proefdraai"])
        w.writerow([nu().isoformat(timespec="seconds"), rol, m["leverancier"], m["model"],
                    tin, tuit, "ja" if DROOG else "nee"])
