#!/usr/bin/env bash
# Lance l'agent SEO sans surveillance, depuis cron (Linux) ou launchd (Mac).
# Usage : bash local/lancer.sh            (passage complet)
#         bash local/lancer.sh --essai    (vérifie l'installation, sans lancer Claude)
# Ne publie rien et n'envoie rien : voir local/prompt.md.
set -u

DOSSIER="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DOSSIER" || exit 1

# cron et launchd démarrent avec un PATH minimal : on ajoute les emplacements
# courants de Claude Code (installateur officiel, Homebrew, npm).
export PATH="$HOME/.local/bin:$HOME/.claude/local:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
CLAUDE="${CLAUDE_BIN:-$(command -v claude || true)}"

mkdir -p journaux
JOURNAL="journaux/$(date +%Y-%m-%d_%H%M%S).log"
note() { echo "[$(date +%H:%M:%S)] $*" >>"$JOURNAL"; }

if [ -z "$CLAUDE" ] || [ ! -x "$CLAUDE" ]; then
  note "Claude Code introuvable. Installe-le, ou indique son chemin dans CLAUDE_BIN."
  echo "Claude Code introuvable (voir $JOURNAL)" >&2
  exit 2
fi

# Un seul passage à la fois.
VERROU="journaux/.en-cours"
if ! mkdir "$VERROU" 2>/dev/null; then
  note "Un passage est déjà en cours (supprime $VERROU s'il reste après un plantage)."
  exit 3
fi
trap 'rmdir "$VERROU" 2>/dev/null' EXIT

note "Début, Claude Code $("$CLAUDE" --version 2>/dev/null | head -n 1)"

if [ "${1:-}" = "--essai" ]; then
  note "Essai : installation correcte, Claude Code n'est pas lancé."
  echo "Essai réussi : $JOURNAL"
  exit 0
fi

if git rev-parse --is-inside-work-tree >/dev/null 2>&1 && git remote get-url origin >/dev/null 2>&1; then
  git pull --ff-only >>"$JOURNAL" 2>&1 || note "git pull impossible : on continue avec la copie locale."
fi

# Outils permis sans question. Les scripts Python permis sont listés dans
# .claude/settings.json ; tout le reste est refusé (mode dontAsk).
OUTILS="Read,Edit,Write,Glob,Grep,WebSearch,WebFetch,Bash(git status *),Bash(git add *),Bash(git commit *),Bash(git push *)"

"$CLAUDE" -p "Suis les consignes reçues ci-dessous." \
  --permission-mode dontAsk \
  --permission-prompts none \
  --allowedTools "$OUTILS" \
  --output-format text \
  <local/prompt.md >>"$JOURNAL" 2>&1
CODE=$?

note "Fin, code $CODE"
exit "$CODE"
