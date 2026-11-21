# Lancer l'agent

Colle l'un de ces textes dans une session claude.ai/code ouverte sur ton
dépôt, ou dans le champ « Instructions » de la tâche planifiée.

## Proposer des sujets

---

Propose-moi des sujets d'articles : suis `AGENT.md`, étapes 1 à 3, et
montre-moi les 5 premiers.

---

## Écrire le prochain article (à la demande)

---

Écris le prochain article : suis `AGENT.md` de bout en bout, en mode
autonome, sur le premier sujet gardé de `sujets.md` (ou sur « {{mot-clé}} »
si je le précise). Livre l'article en `.md` et `.docx`, enregistre tout dans
le dépôt, puis fais le bilan en 5 lignes.

---

## Tous les lundis (tâche planifiée)

---

Lance l'agent SEO de ce dépôt en suivant `AGENT.md` de bout en bout, en mode
autonome : récupère les données Search Console avec le connecteur, propose
les sujets, écris le premier sujet gardé en brouillon, contrôle-le, livre-le
en `.md` et `.docx` dans `articles/`. Ne publie rien et n'envoie rien.

Enregistre ensuite dans le dépôt le dossier de l'article, `sujets.md` et
`memoire/` : commit, puis push sur la branche principale du dépôt (`main`),
pas sur une branche `claude/` : la tâche suivante repart de la branche
principale et doit retrouver la mémoire. Si le push est refusé, dis-le
clairement dans ta réponse.

Le premier lundi du mois, ajoute le bilan des articles livrés (`AGENT.md`,
étape 8).

Termine par le bilan en 5 lignes.

---

## Sur ton ordinateur, sans le cloud

L'agent tourne aussi sur ton ordinateur, seul, chaque lundi à 8 h. Il lit
la même consigne que la tâche cloud : `local/prompt.md`. Les journaux de
chaque passage vont dans `journaux/` (ignoré par Git).

### Avant de commencer (une seule fois)

1. Installe Claude Code (version 2.1.259 ou plus récente) et connecte-toi
   avec ton compte claude.ai : lance `claude` dans ce dossier, puis `/login`.
   Les connecteurs de claude.ai (Search Console) ne sont disponibles qu'avec
   cette connexion : pas avec une clé API ni avec un jeton `setup-token`.
   N'exporte pas `ANTHROPIC_API_KEY` : elle passerait avant ton abonnement
   et serait facturée à part.
2. Fais un premier passage à la main, dans ce dossier : `claude`, puis colle
   le contenu de `local/prompt.md`. Quand Claude demande d'utiliser le
   connecteur Search Console, choisis « toujours autoriser pour ce projet ».
   Ce choix est enregistré dans `.claude/settings.local.json` et servira aux
   passages sans surveillance.
3. Vérifie l'installation sans lancer Claude :
   `bash local/lancer.sh --essai` (Mac, Linux) ou
   `powershell -NoProfile -ExecutionPolicy Bypass -File local\lancer.ps1 -Essai`
   (Windows).

Sans surveillance, Claude Code tourne en mode `dontAsk` : il n'a droit qu'aux
outils listés dans le lanceur et dans `.claude/settings.json` (lire et
modifier les fichiers du dossier, chercher sur le web, lancer les scripts de
l'agent, `git add`, `commit`, `push`) ; tout le reste est refusé sans
question. Le force push, `git reset --hard`, `rm -rf` et la lecture de
`.env` sont interdits même s'ils sont demandés.

### Option 1 : l'application Claude (le plus simple)

L'application Claude pour ordinateur sait lancer une tâche planifiée sur ton
ordinateur : onglet Code, tâche planifiée, « Only on this computer »,
hebdomadaire le lundi, consigne = contenu de `local/prompt.md`, dossier = ce
dossier. Limite : la tâche ne tourne que si l'application est ouverte et
l'ordinateur allumé ; un passage manqué est rattrapé une fois dans les
7 jours. Documentation :
https://code.claude.com/docs/en/desktop-scheduled-tasks (lue le
20 novembre 2026).

### Option 2 : Mac (launchd)

1. Ouvre `local/fr.joinmedicis.agent-seo.plist` et remplace les deux
   `CHEMIN_DU_DOSSIER` par le chemin de ce dossier (exemple :
   `/Users/toi/agent-seo`).
2. Copie-le et active-le :
   ```
   cp local/fr.joinmedicis.agent-seo.plist ~/Library/LaunchAgents/
   launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/fr.joinmedicis.agent-seo.plist
   ```
3. Lance un passage tout de suite pour vérifier :
   `launchctl kickstart -k gui/$(id -u)/fr.joinmedicis.agent-seo`, puis lis
   le dernier fichier de `journaux/`. Si le journal dit que la connexion
   manque, launchd n'a pas accès au trousseau : la documentation de Claude
   Code ne traite pas ce cas **[à vérifier sur ton Mac]** ; utilise alors
   l'option 1.

Si le Mac dort à 8 h, launchd lance le passage au réveil. Pour arrêter :
`launchctl bootout gui/$(id -u)/fr.joinmedicis.agent-seo`.

### Option 3 : Windows (Planificateur de tâches)

Dans PowerShell, remplace `C:\chemin\agent-seo` par le chemin de ce dossier :

```
schtasks /Create /TN "Agent SEO Join Medicis" /SC WEEKLY /D MON /ST 08:00 /TR "powershell -NoProfile -ExecutionPolicy Bypass -File C:\chemin\agent-seo\local\lancer.ps1"
```

Pour vérifier tout de suite : `schtasks /Run /TN "Agent SEO Join Medicis"`,
puis lis le dernier fichier de `journaux\`. Pour arrêter :
`schtasks /Delete /TN "Agent SEO Join Medicis"`. Le lanceur Windows n'a pas
encore été testé sur un vrai PC : seule sa syntaxe est vérifiée
automatiquement **[à vérifier]**.

### Option 4 : Linux ou serveur (cron)

`crontab -e`, puis ajoute (remplace le chemin) :

```
0 8 * * 1 /bin/bash /home/toi/agent-seo/local/lancer.sh
```

cron ne rattrape pas un passage manqué si la machine était éteinte.

### Dans tous les cas

- Un seul passage à la fois : si un passage plante, supprime
  `journaux/.en-cours`.
- Si Claude Code n'est pas trouvé, indique son chemin dans la variable
  `CLAUDE_BIN`.
- La tâche cloud crée en principe ses changements sur des branches
  `claude/` ; la documentation ne dit pas si elle peut pousser sur la
  branche principale. Si le push est refusé, la tâche le dit dans son bilan :
  fusionne la branche, sinon la tâche suivante ne retrouvera pas la mémoire.
