# Lance la veille sans ouvrir Claude, sous Windows. À programmer avec le Planificateur de tâches :
#   schtasks /create /tn "Veille" /sc weekly /d MON /st 08:00 /tr "powershell -ExecutionPolicy Bypass -File C:\chemin\vers\agent-veille\lancer.ps1"
# Prérequis : Claude Code installé et connecté (commande « claude »), Python 3,
# et un fichier .env avec les réglages d'envoi (copie .env.exemple).
# Pas encore testé en conditions réelles : signale ce que tu constates.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force -Path sortie | Out-Null
Start-Transcript -Path sortie\journal.log -Append | Out-Null
Write-Output "=== Veille du $(Get-Date -Format 'yyyy-MM-dd HH:mm') ==="

if (Test-Path .env) {
    Get-Content .env | Where-Object { $_ -match '^\s*[^#\s][^=]*=' } | ForEach-Object {
        $nom, $valeur = $_ -split '=', 2
        [Environment]::SetEnvironmentVariable($nom.Trim(), $valeur.Trim(), "Process")
    }
}
$env:PYTHONUTF8 = "1"
$py = @("python", "py", "python3") | Where-Object { Get-Command $_ -ErrorAction SilentlyContinue } | Select-Object -First 1
if (-not $py) { Write-Output "Python introuvable : voir references\installation.md"; Stop-Transcript | Out-Null; exit 1 }

function Lancer { & $args[0] $args[1..($args.Length - 1)]; if ($LASTEXITCODE -ne 0) { Stop-Transcript | Out-Null; exit $LASTEXITCODE } }

Lancer $py scripts/collecte.py
Lancer claude -p "Mode automatique. Suis AGENT.md, étapes 2 bis à 6 : sortie/a-traiter.json est prêt. La commande Python est « $py ». Fais les recherches web demandées et intègre-les, écris sortie/resume.json, lance scripts/mail.py et corrige jusqu'à ce qu'il réussisse. N'envoie rien et ne lance pas --valider : le script lancer.ps1 s'en charge." --allowedTools "Read,Write,Edit,WebSearch,WebFetch,Bash($py scripts/mail.py:*),Bash($py scripts/collecte.py --integrer:*)"
Lancer $py scripts/mail.py --envoyer
Lancer $py scripts/collecte.py --valider
Write-Output "Terminé."
Stop-Transcript | Out-Null
