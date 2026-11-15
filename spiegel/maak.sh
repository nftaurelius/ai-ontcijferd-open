#!/usr/bin/env bash
# Bouwt de publieke spiegel van deze repo in de map die je meegeeft.
#
#   bash spiegel/maak.sh /pad/naar/lege/map
#
# De spiegel bevat alleen wat in git staat (de laatste commit), zonder geschiedenis,
# zonder de paden uit spiegel/uitsluiten.txt, en met de workflows in een map waar
# GitHub ze niet uitvoert. Vindt de controle onderaan toch iets dat niet publiek mag,
# dan stopt het script met een fout en wordt er niets gepubliceerd.
set -euo pipefail

doel="${1:?Geef de doelmap mee}"
hier="$(git rev-parse --show-toplevel)"
mkdir -p "$doel"
if [ -n "$(ls -A "$doel")" ]; then
  echo "De doelmap is niet leeg: $doel" >&2
  exit 1
fi

git -C "$hier" archive HEAD | tar -x -C "$doel"

# Uitsluitingen toepassen.
while IFS= read -r regel; do
  regel="${regel%%#*}"
  regel="$(echo "$regel" | xargs)"
  [ -z "$regel" ] && continue
  # shellcheck disable=SC2086
  ( cd "$doel" && rm -rf -- $regel )
done < "$hier/spiegel/uitsluiten.txt"

# Workflows meegeven als voorbeeld, zonder dat GitHub ze in de publieke repo uitvoert.
if [ -d "$doel/.github/workflows" ]; then
  mv "$doel/.github/workflows" "$doel/.github/workflows-voorbeeld"
  cat > "$doel/.github/workflows-voorbeeld/LEESMIJ.md" <<'UITLEG'
# Workflows (voorbeeld)

Dit zijn de workflows van de redactie. Ze staan hier in een map die GitHub niet uitvoert.
Wil je de keten zelf draaien, verplaats ze dan naar `.github/workflows/` in je eigen repo
en voeg je eigen sleutels toe (zie de LEESMIJ in de hoofdmap).
UITLEG
fi

# Controle: niets wat privé moet blijven.
fout=0
if grep -rIlE "[A-Za-z0-9._%+-]+@(gmail|hotmail|outlook|telenet|skynet|proximus|yahoo|icloud)\.[a-z.]+" "$doel" >/tmp/spiegel-adressen.txt 2>/dev/null; then
  if [ -s /tmp/spiegel-adressen.txt ]; then
    echo "Persoonlijke e-mailadressen gevonden in:" >&2
    cat /tmp/spiegel-adressen.txt >&2
    fout=1
  fi
fi
if grep -rIlE "sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|xai-[A-Za-z0-9]{30,}|xkeysib-[a-f0-9]{30,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY" "$doel" >/tmp/spiegel-sleutels.txt 2>/dev/null; then
  if [ -s /tmp/spiegel-sleutels.txt ]; then
    echo "Iets dat op een sleutel lijkt, gevonden in:" >&2
    cat /tmp/spiegel-sleutels.txt >&2
    fout=1
  fi
fi
for pad in data/items data/triage data/fouten; do
  if [ -e "$doel/$pad" ]; then
    echo "Niet uitgesloten: $pad" >&2
    fout=1
  fi
done
if [ -n "$(find "$doel" -name bronmateriaal.md -o -name kandidaten.json | head -1)" ]; then
  echo "Er staat nog bronmateriaal of een kandidatenlijst in de spiegel." >&2
  fout=1
fi
[ "$fout" -eq 0 ] || exit 1

echo "Spiegel klaar in $doel: $(find "$doel" -type f | wc -l) bestanden, $(du -sh "$doel" | cut -f1)."
