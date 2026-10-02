#!/usr/bin/env bash
# Construit le ZIP « tout-en-un » importable sur claude.ai (Personnaliser → Skills) :
# un seul SKILL.md (l'aiguilleur de ce dossier), les modules dans modules/<nom>/
# (leur SKILL.md renommé <nom>.md), les modèles dans templates/, la licence.
# claude.ai refuse un ZIP avec plusieurs SKILL.md ou un manifeste de plugin.
#
# Usage : <pack>/claude-ai/build.sh <chemin du zip à écrire>
set -euo pipefail

OUT="$(realpath -m "${1:?Chemin du ZIP à écrire}")"
PACK="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
NAME="$(basename "$PACK")"
ROOT="$TMP/$NAME"

mkdir -p "$ROOT/modules" "$ROOT/templates"
cp "$PACK/claude-ai/SKILL.md" "$ROOT/SKILL.md"
cp "$PACK/LICENSE" "$PACK/CREDITS.md" "$ROOT/"
cp "$PACK"/templates/*.md "$ROOT/templates/"
for dir in "$PACK"/skills/*/; do
  name="$(basename "$dir")"
  cp -r "$dir" "$ROOT/modules/$name"
  mv "$ROOT/modules/$name/SKILL.md" "$ROOT/modules/$name/$name.md"
done
find "$ROOT" \( -name '__pycache__' -o -name '.DS_Store' \) -prune -exec rm -rf {} +

count="$(find "$ROOT" -name SKILL.md | wc -l)"
[ "$count" -eq 1 ] || { echo "Erreur : $count SKILL.md dans le ZIP (1 attendu)" >&2; exit 1; }
[ -z "$(find "$ROOT" -path '*.claude-plugin*')" ] || { echo "Erreur : manifeste de plugin dans le ZIP" >&2; exit 1; }

rm -f "$OUT"
(cd "$TMP" && zip -qrX "$OUT" "$NAME")
echo "ZIP claude.ai : $OUT"
