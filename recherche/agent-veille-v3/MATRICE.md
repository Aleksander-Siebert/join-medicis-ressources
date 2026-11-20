# Agent de veille v3 : last30days + Guetteur, matrice à valider

Statut : **proposition**, rien n'est écrit dans `plugins/agent-veille/` avant
la validation de l'utilisateur (19 novembre 2026).

## Décisions déjà prises (19 novembre 2026)

- Moteur : **last30days** pour les conversations (Reddit, Hacker News, X,
  YouTube, GitHub, Polymarket…) + **sources françaises du Guetteur** (CNIL,
  DGCCRF, EUR-Lex, BOAMP, TED, flux métier, offres d'emploi).
- Mémoire : **watchlist + briefing de last30days** (pas de mémoire maison
  en double).
- Lancement : **au choix**, tâche planifiée Claude Code dans le cloud
  (défaut) ou planificateur de l'ordinateur (cron, Planificateur de tâches).
- Livraison : **mail à soi-même** par le connecteur Gmail de claude.ai ;
  **brouillon au premier passage**, envoi ensuite. Jamais d'envoi à des tiers.
- Distribution : **dépôt modèle** `agent-veille` (« Use this template ») +
  marketplace `join-medicis` déjà en place pour les Skills.
- Dust et les autres IA : **pages séparées**, plus tard.

## Sources lues

- `mvanhorn/last30days-skill`, commit `2623916` (v4.3.2, 17 novembre 2026),
  licence MIT : `CHANGELOG.md`, `CONFIGURATION.md` (trend monitoring,
  backends, agent-hosted runs), `SECURITY.md`, `skills/last30days/SKILL.md`,
  `references/agent-mode.md`, `scripts/watchlist.py`, `scripts/briefing.py`,
  `scripts/store.py`, hôtes appelés par `scripts/lib/`.
- Guetteur v2 (`plugins/agent-veille/`, PR #23 en brouillon) : `collecte.py`,
  `mail.py`, `modeles/`, `sources.json`, `AGENT.md`, 67 tests.

## Matrice

| # | Fonction | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|---|
| 1 | Sujets suivis, quotidiens ou hebdo | last30days `watchlist.py add [--weekly]` | reprendre | sujets réglés dans `CONFIGURE-MOI.md`, en français |
| 2 | Recherche dans les conversations | last30days, sources sans clé (Reddit, HN, Polymarket, GitHub) | reprendre | YouTube, Bluesky, Brave en option ; X et LinkedIn **écartés par défaut** (cookies impossibles en cloud, clés payantes) |
| 3 | Mode non surveillé | last30days `LAST30DAYS_SCHEDULED_RUN=1` (posé par watchlist) | reprendre | aucun cookie de navigateur lu en tâche planifiée |
| 4 | Mémoire, anti-doublons par URL | last30days `store.py` (SQLite, URL unique) | reprendre | la base vit dans `~/.local/share/last30days/` : copiée depuis `memoire/research.db` avant le passage et recopiée après, puis enregistrée dans le dépôt (sinon perdue entre deux tâches cloud) |
| 5 | Budget quotidien | last30days `config budget` (5 $ par défaut, arrêt si coût inconnu) | reprendre | budget à **0** par défaut : sources gratuites seulement |
| 6 | Résumé quotidien / hebdo | last30days `briefing.py generate [--weekly]` (données, la rédaction est faite par l'IA) | reprendre | rédaction en français par l'agent, avec nos modèles de mail |
| 7 | Livraison par webhook | last30days (Slack ou HTTPS, seulement s'il y a du nouveau) | garder en option | Slack direct possible ; défaut = Gmail |
| 8 | Sources officielles françaises | Guetteur `collecte.py` (CNIL, DGCCRF, EUR-Lex en RSS ; BOAMP ; TED) | reprendre | ce que last30days n'a pas : marché et réglementation français |
| 9 | Offres d'emploi des concurrents | Guetteur (Greenhouse, Lever, Ashby) ; last30days a aussi une voie « jobs » | comparer au test | garder la plus fiable, pas les deux |
| 10 | Pages surveillées (diff) | Guetteur `decrire_page` / diff JSON | reprendre | prix et pages produit des concurrents |
| 11 | `robots.txt`, pause par site, refus du réseau local | Guetteur `Robots`, `verifier_adresse` | reprendre | last30days passe par des API, le Guetteur lit des pages : ses garde-fous restent |
| 12 | Modèles de mail (thèmes, récap, flash) | Guetteur `mail.py`, `modeles/*.html` | reprendre | rendu pour Gmail (HTML simple + texte) |
| 13 | Envoi Gmail | connecteur Gmail de claude.ai | ajout | brouillon au 1er passage, puis envoi à l'adresse de l'utilisateur seulement |
| 14 | Mémoire maison du Guetteur (`historique.json`, `termes.json`, verrou `dernier-envoi.json`) | Guetteur | **remplacer** par la mémoire last30days pour les conversations ; garder le verrou d'envoi (pas deux mails le même jour) | une seule mémoire par type de source |
| 15 | Sujets qui montent | Guetteur `sujets_qui_montent` ; last30days `--discover` (protocole en 3 commandes) | comparer au test | `--discover` demande un jugement de l'IA en 3 étapes : plus coûteux |
| 16 | Tâche planifiée cloud | Claude Code (claude.ai/code, routines) | ajout | prompt prêt à coller ; réseau de l'environnement à ouvrir (point bloquant ci-dessous) |
| 17 | Planificateur local | last30days « cron / Task Scheduler / GitHub Actions » ; Guetteur `lancer.sh`, `lancer.ps1` | reprendre | Mac, Linux, Windows |
| 18 | Diagnostic des sources | last30days `doctor`, `--diagnose` ; Guetteur `--diagnostic` | reprendre | une commande « vérifier ma veille » qui lance les deux |
| 19 | Hosted backend / proxy payant de last30days | last30days `LAST30DAYS_API_BASE` | **écarter** | pas de service payant tiers par défaut ; incompatible avec la watchlist |
| 20 | Lecture des cookies X et Reddit | last30days (avec accord) | **écarter** | impossible en cloud, et recherches au nom du compte de l'utilisateur |
| 21 | Version sans Claude Code | — | **écarter ici** | pages séparées par IA, plus tard |

## Points bloquants à tester avant d'écrire le code

1. **Python 3.12.** last30days exige Python 3.12 ou plus (`pyproject.toml`).
   Dans ce conteneur cloud, `python3` est en 3.11 mais `python3.13` est
   présent. À vérifier dans l'environnement par défaut des tâches cloud, et
   à écrire dans le script d'installation de l'environnement.
2. **Réseau du cloud.** Environnement « Limited » par défaut. Hôtes appelés
   par les sources gratuites : `www.reddit.com`, `reddit.com`,
   `arctic-shift.photon-reddit.com`, `hn.algolia.com`,
   `news.ycombinator.com`, `api.github.com`, `github.com`,
   `gamma-api.polymarket.com`, `polymarket.com`, plus les sources du
   Guetteur (cnil.fr, boamp.fr, ted.europa.eu…). Liste exacte à confirmer en
   lançant `doctor` dans une vraie tâche.
3. **Enregistrer la mémoire.** La tâche planifiée doit pousser
   `memoire/research.db` dans le dépôt après chaque passage (comme l'agent
   SEO).
4. **Gmail dans une tâche planifiée.** Le connecteur doit être disponible
   dans la tâche, pas seulement dans une session ouverte : à vérifier.
5. **Sources anglophones.** last30days trouvera peu sur un sujet très
   français : c'est le rôle des sources du Guetteur, à démontrer sur un cas
   réel.

## Ce que la v3 apporte, honnêtement

- Face à last30days seul : sources françaises officielles, mail mis en
  forme, mise en place guidée pour le cloud, budget à zéro par défaut.
- Face au Guetteur v2 seul : les conversations (Reddit, HN, GitHub,
  Polymarket), et une mémoire et un budget déjà testés par la communauté
  de last30days.
- Risque : last30days change vite (4 versions entre le 16 et le 17 novembre).
  Il est figé à un commit et mis à jour volontairement.
