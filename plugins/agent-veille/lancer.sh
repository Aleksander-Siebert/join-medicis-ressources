#!/usr/bin/env bash
# Lance la veille sans ouvrir Claude : à programmer avec cron (macOS, Linux).
# Exemple, chaque lundi à 8 h :  0 8 * * 1  /chemin/vers/agent-veille/lancer.sh
# Prérequis : Claude Code installé et connecté (commande « claude »), Python 3,
# et un fichier .env avec les réglages d'envoi (copie .env.exemple).
# Sous Windows : lancer.ps1.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p sortie
exec >>sortie/journal.log 2>&1
echo "=== Veille du $(date '+%Y-%m-%d %H:%M') ==="

if [ -f .env ]; then set -a; . ./.env; set +a; fi
PY=$(command -v python3 || command -v python) || { echo "Python introuvable : voir references/installation.md"; exit 1; }

"$PY" scripts/collecte.py

claude -p "Mode automatique. Suis AGENT.md, étapes 2 bis à 6 : sortie/a-traiter.json est prêt. \
La commande Python est « $PY ». Fais les recherches web demandées et intègre-les, \
écris sortie/resume.json, lance scripts/mail.py et corrige jusqu'à ce qu'il réussisse. \
N'envoie rien et ne lance pas --valider : le script lancer.sh s'en charge." \
  --allowedTools "Read,Write,Edit,WebSearch,WebFetch,Bash($PY scripts/mail.py:*),Bash($PY scripts/collecte.py --integrer:*)"

"$PY" scripts/mail.py --envoyer
"$PY" scripts/collecte.py --valider
echo "Terminé."
