# Lance l'agent SEO sans surveillance, depuis le Planificateur de tâches (Windows).
# Usage : powershell -NoProfile -ExecutionPolicy Bypass -File local\lancer.ps1 [-Essai]
# Ne publie rien et n'envoie rien : voir local\prompt.md.
param([switch]$Essai)

$Dossier = Split-Path -Parent $PSScriptRoot
Set-Location $Dossier

$Claude = $env:CLAUDE_BIN
if (-not $Claude) {
  $Trouve = Get-Command claude -ErrorAction SilentlyContinue
  if ($Trouve) { $Claude = $Trouve.Source }
}

New-Item -ItemType Directory -Force -Path journaux | Out-Null
$Journal = Join-Path "journaux" ((Get-Date -Format "yyyy-MM-dd_HHmmss") + ".log")
function Note($Texte) { Add-Content -Path $Journal -Value ("[" + (Get-Date -Format "HH:mm:ss") + "] " + $Texte) -Encoding UTF8 }

if (-not $Claude -or -not (Test-Path $Claude)) {
  Note "Claude Code introuvable. Installe-le, ou indique son chemin dans CLAUDE_BIN."
  Write-Error "Claude Code introuvable (voir $Journal)"
  exit 2
}

# Un seul passage à la fois.
$Verrou = "journaux\.en-cours"
if (Test-Path $Verrou) {
  Note "Un passage est déjà en cours (supprime $Verrou s'il reste après un plantage)."
  exit 3
}
New-Item -ItemType Directory -Path $Verrou | Out-Null

try {
  Note ("Début, Claude Code " + (& $Claude --version 2>$null | Select-Object -First 1))
  if ($Essai) {
    Note "Essai : installation correcte, Claude Code n'est pas lancé."
    Write-Output "Essai réussi : $Journal"
    exit 0
  }

  git remote get-url origin *> $null
  if ($LASTEXITCODE -eq 0) {
    git pull --ff-only *>> $Journal
    if ($LASTEXITCODE -ne 0) { Note "git pull impossible : on continue avec la copie locale." }
  }

  # Outils permis sans question. Les scripts Python permis sont listés dans
  # .claude\settings.json ; tout le reste est refusé (mode dontAsk).
  $Outils = "Read,Edit,Write,Glob,Grep,WebSearch,WebFetch,Bash(git status *),Bash(git add *),Bash(git commit *),Bash(git push *)"

  Get-Content -Raw -Encoding UTF8 local\prompt.md |
    & $Claude -p "Suis les consignes reçues ci-dessous." --permission-mode dontAsk --permission-prompts none --allowedTools $Outils --output-format text *>> $Journal
  $Code = $LASTEXITCODE
  Note "Fin, code $Code"
  exit $Code
}
finally {
  Remove-Item -Recurse -Force $Verrou -ErrorAction SilentlyContinue
}
