#!/usr/bin/env bash
# Copie dans .claude/skills/ les Skills du pack SEO dont l'agent a besoin.
# Dans une session claude.ai/code, Claude charge les Skills du dossier
# .claude/skills du dépôt : l'agent marche donc sans rien installer.
#
# La source reste plugins/seo-skills/ : ne modifie pas les copies, modifie le
# pack puis relance ce script. Les tests vérifient que les copies sont à jour.
set -euo pipefail
ICI="$(cd "$(dirname "$0")/.." && pwd)"
PACK="$ICI/../seo-skills/skills"
DEST="$ICI/.claude/skills"
SKILLS=(seo-article seo-keywords seo-serp seo-brief seo-write seo-human seo-maillage seo-context seo-refresh)
[ -d "$PACK" ] || { echo "Pack SEO introuvable : $PACK" >&2; exit 1; }
rm -rf "$DEST"
mkdir -p "$DEST"
for s in "${SKILLS[@]}"; do
  cp -r "$PACK/$s" "$DEST/$s"
  find "$DEST/$s" -name __pycache__ -type d -prune -exec rm -rf {} +
done
echo "${#SKILLS[@]} Skills copiés dans .claude/skills/ depuis plugins/seo-skills/."
