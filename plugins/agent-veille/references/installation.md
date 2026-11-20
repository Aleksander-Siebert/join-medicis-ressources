# Installer l'agent : trois façons

Choisis selon ta situation. `CONFIGURE-MOI.md` pose la question et suit la
bonne partie de ce guide.

| | Cloud | Local, sans rien installer | Local, version complète |
|---|---|---|---|
| Tourne ordinateur éteint | oui | non | non |
| À installer | rien | rien | Python (l'agent s'en charge) |
| Il faut | un compte GitHub gratuit | l'application Claude | l'application Claude |
| Mac et PC | identique | identique | identique |
| Dates et doublons | vérifiés par script | vérifiés à la main | vérifiés par script |
| Pages suivies, appels d'offres, emplois | oui | pages seulement | oui |

Dans tous les cas : une offre Claude payante (les tâches planifiées n'existent
pas dans l'offre gratuite) et, pour recevoir un mail, le connecteur Gmail ou
Outlook activé dans Claude (Paramètres → Connecteurs).

Les noms de menus viennent de la documentation de Claude Code lue le
12 novembre 2026. Les tâches planifiées cloud y sont en « research
preview » : leur fonctionnement peut changer.

## 1. Cloud : la veille tourne ordinateur éteint

1. **Copie le modèle.** Sur la page GitHub de l'agent, clique sur « Use this
   template », puis « Create a new repository ». Choisis « Private » et un
   nom, par exemple `ma-veille`.
2. **Donne l'accès à Claude.** Sur claude.ai/code, connecte GitHub et
   installe l'application GitHub de Claude sur ce dépôt.
3. **Ouvre le réseau.** L'environnement « Default » n'atteint que des sites
   techniques : les sites d'actualité sont bloqués. Sous la zone de saisie
   de claude.ai/code, ouvre le sélecteur d'environnement, crée un
   environnement « veille » et règle « Network access » sur « Full ». Plus
   strict : garde « Limited » et liste les sites à lire dans « Allowed
   domains ».
4. **Configure.** Démarre une session sur ton dépôt, dans cet environnement,
   et colle le texte de `CONFIGURE-MOI.md`. À la fin, demande à l'agent
   d'enregistrer la configuration dans le dépôt (« commit et pousse sur la
   branche principale »).
5. **Programme.** Sur claude.ai/code/routines, crée une tâche planifiée :
   ton dépôt, l'environnement « veille », le rythme voulu, et dans
   « Connectors » uniquement ceux qui servent (Gmail, par exemple). Colle
   comme instructions le texte « cloud » de `LANCER.md`.
6. **Teste.** Clique sur « Run now » et vérifie trois choses : le mail est
   arrivé, le dossier `memoire/` du dépôt a changé, un second « Run now »
   ne renvoie pas les mêmes infos.

À savoir :

- Chaque lancement repart d'une copie neuve du dépôt. La mémoire doit donc y
  être enregistrée à chaque veille : c'est ce que demande le texte de
  `LANCER.md`. Par défaut, Claude pousse sur une branche `claude/…` : le
  texte lui demande la branche principale. **À tester sur ton compte**, et
  à adapter si ton dépôt protège cette branche.
- Un lancement compte dans l'usage de ton offre Claude.
- Autre voie cloud, sans tâche planifiée Claude : GitHub Actions, avec le
  fichier `cloud/github-actions-veille.yml` (clé API ou jeton, envoi par
  SMTP). Plus technique, expliqué en tête du fichier.

## 2. Local, sans rien installer

1. Télécharge le dossier de l'agent (bouton « Code » → « Download ZIP » sur
   GitHub) et décompresse-le.
2. Dans l'application Claude, onglet Code, ouvre ce dossier.
3. Colle le texte de `CONFIGURE-MOI.md`. Quand l'agent constate que Python
   manque, réponds « continue sans Python ».
4. Programme : onglet Code → « Scheduled » (ou « Routines ») → « New
   task », dossier de l'agent, ton rythme, instructions de `LANCER.md`.

La tâche locale ne tourne que si l'application est ouverte et l'ordinateur
allumé. Une veille manquée est rattrapée une fois, au réveil.

## 3. Local, version complète

Comme la partie 2. À l'étape 3, l'agent vérifie Python :

- **Mac** : `python3 --version`. S'il manque, macOS propose d'installer les
  outils de développement d'Apple : accepte, puis relance. Autre voie :
  l'installateur de python.org.
- **Windows** : `python --version`, puis `py --version`. S'il manque,
  l'agent propose `winget install -e --id Python.Python.3.12` **[à vérifier
  sur ton PC]**, ou l'installateur de python.org en cochant « Add python.exe
  to PATH ». Ferme et rouvre l'application Claude après l'installation.
- Puis `python3 scripts/collecte.py --diagnostic` (ou `python`, `py`) : tout
  doit être « OK ».

Si l'installation échoue, l'agent continue sans Python (partie 2) et tu
pourras y revenir : rien n'est perdu.

Sans l'application Claude, avec le terminal seul : `lancer.sh` (Mac, Linux)
et `lancer.ps1` (Windows) lancent la veille et l'envoient par SMTP. Ils se
programment avec cron ou le Planificateur de tâches. Réglages dans
`.env.exemple`.

## Ce qui a été testé, et ce qui ne l'a pas été

- Testé automatiquement sur Linux, macOS et Windows : les scripts (tests
  dans `tests/`).
- Testé sur de vraies sources, sous Linux : collecte standard et étendue,
  appels d'offres, emplois, mise en forme.
- **Pas encore testé en conditions réelles** : la tâche planifiée cloud,
  la tâche locale sous Windows, l'envoi par les connecteurs Outlook, Slack
  et Notion, `lancer.ps1`. Signale ce que tu constates.
