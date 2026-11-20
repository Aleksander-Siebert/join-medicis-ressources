# Guetteur v2 : collecte et matrice de capacités

Date de la collecte et des vérifications : 12 novembre 2026.
Statut : **en attente de validation**, rien n'est écrit dans l'agent.

## 1. Ce qui a été lu

20 dépôts clonés (`git clone --depth 1`), environ 3 700 fichiers.

Lus en entier (SKILL.md, scripts, workflows, configuration) :

| Dépôt | Licence | Ce que c'est |
|---|---|---|
| muguang1224/competitor-watch | MIT | Skill de veille par instantanés et diff, Python sans dépendance, le plus proche du Guetteur |
| gpavan1992/Vigil-Agent | aucune | Agent hebdomadaire Claude Managed Agents, Supabase, Telegram |
| unifapi-agent/agents (2 Skills de veille) | MIT | Skills branchés sur une API payante de données sociales |
| ferdinandobons/startup-skill (startup-competitors) | MIT | Analyse concurrentielle ponctuelle en 3 vagues |
| charlie947/agent-harness-starter | MIT | Installation Claude Code et Cowork pour non-développeurs |
| Nassiraouzzine/Veille-Concurrentielle-n8n | aucune | Workflow n8n francophone, Perplexity |
| aryamankd/competitor-intel-agent | aucune | Script unique, API Claude |

Lus en partie (README, architecture, modules de collecte et de détection) :

| Dépôt | Licence | Ce que c'est |
|---|---|---|
| yassnemo/compete | MIT | Plateforme complète : collecte, DuckDB, tableau de bord |
| dgtlmoon/changedetection.io (35 770 étoiles) | Apache 2.0 | Référence de la surveillance de pages |
| valuationgeek/daybrief | MIT | Résumé d'actualités local, robuste sans surveillance |
| andgineer/news-recap | MIT | Résumé RSS avec regroupement et reprise sur erreur |
| daijro/camoufox | MPL 2.0 | Navigateur Firefox modifié pour ne pas être détecté |
| redf0x1/camofox-mcp | MIT | Serveur MCP tiers au-dessus de Camoufox |
| firecrawl/firecrawl-observer | aucune | Surveillance de sites, API Firecrawl payante |

Clonés mais non analysés, faute d'apport au sujet : kevinho/clawfeed,
yinan-c/RSSbrew, Johell1NS/browser-search, grcx-dev/grcx,
samshanmukh/Competitor-Intelligence-Agent, emotixco/claude-skills-founder.

Un dépôt sans licence n'est pas copié : on s'en inspire et on réécrit.

## 2. Matrice de capacités

Verdict : **R** reprendre, **A** améliorer, **E** écarter.

### Collecte

| Capacité | Source | Verdict | Ce que nous faisons |
|---|---|---|---|
| Types de source `github_releases` et `json` (diff par clé) | competitor-watch, `scripts/watch.py` | R | Deux nouveaux types dans `sources.json`, utiles pour les concurrents logiciels |
| Respect de `robots.txt`, du `Crawl-delay`, agent utilisateur honnête, pause par site | compete, `pipeline/collect/base.py` | R | Aujourd'hui absent du Guetteur : à ajouter, activé par défaut |
| Offres d'emploi par les API publiques des outils de recrutement (Greenhouse, Lever, Ashby) | compete, `pipeline/collect/jobs.py` | A | Signal « recrutement » fiable. À compléter pour la France : Welcome to the Jungle bloque les robots (403 constaté) |
| Ciblage d'une partie de page (sélecteur CSS), texte à ignorer, déclenchement sur un mot | changedetection.io, README « Filters » | A | Version simple : `ignorer` et `seulement_si` par page |
| Règle en langage courant par page (« préviens-moi seulement si le prix change ») | changedetection.io, section IA | R | Un champ `intention` par page, lu par l'agent à l'étape 4 |
| Surveillance de fichiers PDF | changedetection.io | E pour l'instant | Demande une bibliothèque : contraire à l'installation sans dépendance |
| Navigateur réel pour les pages en JavaScript | compete (`dynamic.py`), changedetection.io | A | Voir l'option « étendue », partie 4 |
| Avis clients (G2, Capterra) et discussions (Reddit, Hacker News) | Vigil, unifapi, startup-skill | A | Hacker News a une API gratuite (testée, 200). G2 et Reddit passent par la recherche web de l'agent, donnée moins fiable : à signaler dans le mail |
| LinkedIn des concurrents | Vigil, unifapi | E | Pas d'accès propre sans API payante ni contournement |

### Analyse

| Capacité | Source | Verdict | Ce que nous faisons |
|---|---|---|---|
| Note chiffrée par signal (base + mots surveillés + concurrent direct + tendance confirmée) | Vigil, `vigil.yaml` | A | Notre échelle 1 à 3 reste, mais calculée par une règle écrite, donc stable d'une semaine à l'autre |
| Mémoire des tendances sur plusieurs semaines (« 3e baisse de prix en 2 mois ») | Vigil, table `trend_memory` | R | Fichier `memoire/tendances.json`, une ligne « ce que ça confirme » dans le mail |
| Détection des sujets qui montent (fréquence du jour comparée à l'habitude) | daybrief, `decision.py` | R | Base de la veille « tendances du marché » |
| Étiquettes confirmé / déduit / estimation | unifapi, startup-skill (`honesty-protocol.md`) | R | « Déduit » obligatoire quand l'agent interprète (ex. recrutements) |
| Fiche de départ par concurrent (offre, prix, positionnement) | startup-skill, vague 1 | A | Faite une fois à la configuration, sert de point de comparaison |
| « À surveiller dans 2 à 4 semaines » | Vigil | R | Existe déjà (`a_surveiller`), à dater |
| Sous-agents spécialisés par type de signal | Vigil | E | Coût et lenteur, sans gain démontré sur nos essais |
| Alerte immédiate hors du rythme hebdomadaire | Vigil, daybrief | A | Option : passage quotidien léger, mail seulement si importance 3 |

### Fiabilité sans surveillance

| Capacité | Source | Verdict | Ce que nous faisons |
|---|---|---|---|
| Un mail n'est jamais envoyé deux fois | daybrief, README « Built to run unattended » | R | Verrou dans `memoire/` |
| Refus des adresses du réseau local, taille et durée de téléchargement plafonnées | daybrief | R | À ajouter à `collecte.py` |
| Diagnostic étape par étape | daybrief, `quick_test.py` | R | `collecte.py --diagnostic`, lisible par un non-développeur |
| Reprise après interruption | news-recap, startup-skill (`PROGRESS.md`) | E | Une veille dure quelques minutes, on relance |
| Recettes de planification cron, launchd, Planificateur de tâches Windows | daybrief, `docs/scheduling.md` | A | Remplacées par les tâches planifiées de Claude, plus simples. Recette Windows gardée en annexe |

### Installation et personnalisation

| Capacité | Source | Verdict | Ce que nous faisons |
|---|---|---|---|
| Un seul texte à coller pour tout installer | unifapi, README « Paste one prompt » | R | Déjà notre fiche participant : à généraliser |
| Parcours Cowork sans terminal | agent-harness-starter, `cowork-setup.md` | A | Un parcours par situation, choisi par l'assistant |
| Exécution cloud sur dépôt GitHub avec mémoire commitée | competitor-watch, `.github/workflows/watch.yml` | A | Modèle de dépôt à copier en un clic, plus tâche planifiée cloud de Claude |
| Exemples de configuration par secteur | Vigil, `docs/example-configs.md` | R | 4 exemples français (SaaS, assurance, e-commerce, agence) |
| Sections et seuils réglables par fichier | daybrief, `feeds.yaml` | A | Réglables par la conversation, pas en éditant du YAML |
| Tableau de bord web | compete, firecrawl-observer | E | Hors sujet : le livrable est un mail |
| Base de données (Supabase, DuckDB, SQLite) | Vigil, compete, daybrief | E | Des fichiers JSON suffisent et s'installent sans rien |

## 3. Sources officielles gratuites, testées en direct

Test du 12 novembre 2026 depuis un serveur cloud, sans clé.

| Domaine | Source | Résultat |
|---|---|---|
| Appels d'offres France | API BOAMP (`boamp-datadila.opendatasoft.com`, API Explore v2.1) | 200, recherche par mot dans l'objet |
| Appels d'offres Europe | API TED v3 (`api.ted.europa.eu/v3/notices/search`, POST) | 200, filtre par pays et mot du titre |
| Réglementation | Flux RSS CNIL | 200 |
| Réglementation | Flux RSS EUR-Lex | 200 |
| Réglementation | Flux RSS DGCCRF | 200 |
| Réglementation | Légifrance et Journal officiel | **403, protection anti-robot**. Voie officielle : API PISTE avec compte gratuit **[à vérifier]** |
| Vie des sociétés | API Recherche d'entreprises (`recherche-entreprises.api.gouv.fr`) | 200 |
| Vie des sociétés | API BODACC | 200 |
| Brevets | Office européen des brevets (OPS) | **403 sans clé**. Clé gratuite sur inscription **[à vérifier]** |
| Brevets et marques | data.inpi.fr | **403, protection anti-robot**. API avec compte gratuit **[à vérifier]** |
| Actualités | Google Actualités RSS | 200. Conditions : usage personnel et non commercial, version actuelle des conditions **[à vérifier]** |
| Actualités | Bing Actualités RSS | 200. Conditions **[à vérifier]** |
| Actualités | GDELT | pas de réponse pendant le test |
| Discussions | Hacker News (API Algolia) | 200 |

## 4. Les deux options de collecte

**Option standard, sans zone grise.** Flux RSS des médias et des concurrents,
pages publiques dans le respect de `robots.txt`, API officielles de la partie
3, et recherche web intégrée de l'agent. Aucun agrégateur d'actualités.

**Option étendue, à activer par l'utilisateur.** En plus : Google Actualités
et Bing Actualités en RSS (comportement actuel du Guetteur), et un navigateur
réel pour les pages qui ne s'affichent qu'en JavaScript. Un avertissement
rappelle les conditions d'usage personnel.

**Camoufox : analysé, écarté (recommandation).**

- Il sert à masquer qu'un robot visite la page. Les recommandations de la
  CNIL sur le moissonnage (19 juin 2025, lues par des résumés de cabinets,
  texte officiel **[à vérifier]**) demandent d'exclure les sites qui
  s'opposent par `robots.txt` ou CAPTCHA.
- Le MCP n'est pas dans le dépôt officiel : c'est un projet tiers
  (redf0x1/camofox-mcp) qui demande Node.js et deux serveurs lancés en
  permanence. C'est l'inverse d'une installation facile, et il ne tourne
  pas dans une tâche cloud.
- Une partie des blocages constatés vient de l'adresse du serveur cloud. Sur
  l'ordinateur de l'utilisateur, le mode local lit souvent ces pages sans
  rien contourner.

## 5. Installation : les trois modes

| Mode | Pour qui | Ce qu'il faut | Limites vérifiées dans la documentation Claude |
|---|---|---|---|
| Cloud | Qui veut que ça tourne ordinateur éteint | Compte GitHub gratuit, offre Claude payante | Python est déjà installé dans le cloud. Aperçu de recherche. L'environnement par défaut a un réseau « Limited » qui bloque les sites d'actualité : il faut un environnement en accès « Full » ou une liste de domaines. Le connecteur Gmail passe sans réglage. Les modifications partent par défaut sur une branche `claude/` : la mémoire doit être poussée ailleurs, à tester |
| Local sans script | Qui ne veut rien installer, Mac ou PC | L'application Claude | L'agent collecte avec sa recherche web. Dates et doublons moins fiables, dit dans le mail |
| Local avec scripts | Qui veut la meilleure fiabilité en local | Python, installé par l'agent | Tâche planifiée locale : ne tourne que si l'application est ouverte et l'ordinateur allumé. Un seul rattrapage au réveil, sur 7 jours |

Windows : les scripts Python sont à tester sur Windows et macOS par GitHub
Actions (`windows-latest`, `macos-latest`). `lancer.sh` n'existe qu'en bash :
à doubler en PowerShell ou à retirer au profit des tâches planifiées de
Claude. L'expérience dans l'application sur PC reste à tester par
l'utilisateur.

## 6. Comparaison honnête avec le Guetteur actuel

Ce que le Guetteur fait mieux que les dépôts lus : contrôle bloquant des
sources avant l'envoi, lecture de l'article d'origine, mémoire sur 90 jours,
regroupement des doublons, mail HTML, typographie française, zéro
dépendance.

Ce qui lui manque : respect de `robots.txt`, veille stratégique, mémoire des
tendances, note stable, sources officielles, offres d'emploi, garde-fous
réseau, diagnostic, Windows, installation sans Python, mode cloud testé,
éval à l'aveugle.
