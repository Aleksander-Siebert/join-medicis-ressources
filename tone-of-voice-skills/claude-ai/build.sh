#!/usr/bin/env bash
# Construit le ZIP importable sur claude.ai (Personnaliser → Skills).
# Ce pack n'a qu'un Skill : le ZIP contient son dossier tel quel (un seul
# SKILL.md), plus la licence et les crédits. claude.ai refuse un ZIP avec
# plusieurs SKILL.md ou un manifeste de plugin.
#
# Usage : <pack>/claude-ai/build.sh <chemin du zip à écrire>
set -euo pipefail

OUT="$(realpath -m "${1:?Chemin du ZIP à écrire}")"
PACK="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
ROOT="$TMP/tone-of-voice"

cp -r "$PACK/skills/tone-of-voice" "$ROOT"
cp "$PACK/LICENSE" "$PACK/CREDITS.md" "$ROOT/"
find "$ROOT" \( -name '__pycache__' -o -name '.DS_Store' \) -prune -exec rm -rf {} +

count="$(find "$ROOT" -name SKILL.md | wc -l)"
[ "$count" -eq 1 ] || { echo "Erreur : $count SKILL.md dans le ZIP (1 attendu)" >&2; exit 1; }
[ -z "$(find "$ROOT" -path '*.claude-plugin*')" ] || { echo "Erreur : manifeste de plugin dans le ZIP" >&2; exit 1; }

rm -f "$OUT"
(cd "$TMP" && zip -qrX "$OUT" "tone-of-voice")
echo "ZIP claude.ai : $OUT"
