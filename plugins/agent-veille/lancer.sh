#!/usr/bin/env bash
# Lance la veille sans ouvrir Claude : à programmer avec cron (macOS, Linux).
# Exemple, chaque lundi à 8 h :  0 8 * * 1  /chemin/vers/agent-veille/lancer.sh
# Prérequis : Claude Code installé et connecté (commande « claude »), Python 3,
# et un fichier .env avec les réglages d'envoi (copie .env.exemple).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p sortie
exec >>sortie/journal.log 2>&1
echo "=== Veille du $(date '+%Y-%m-%d %H:%M') ==="

if [ -f .env ]; then set -a; . ./.env; set +a; fi

python3 scripts/collecte.py

claude -p "Mode automatique. Suis AGENT.md, étapes 3 à 6 seulement (dont 3 bis) : sortie/a-traiter.json est prêt. \
Écris sortie/resume.json, lance python3 scripts/mail.py et corrige jusqu'à ce qu'il réussisse. \
N'envoie rien et ne lance pas --valider : le script lancer.sh s'en charge." \
  --allowedTools "Read,Write,Edit,WebSearch,WebFetch,Bash(python3 scripts/mail.py:*)"

python3 scripts/mail.py --envoyer
python3 scripts/collecte.py --valider
echo "Terminé."
