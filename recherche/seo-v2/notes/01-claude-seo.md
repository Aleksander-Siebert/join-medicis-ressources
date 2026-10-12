# claude-seo (AgriciDaniel), v2.4.2 · dissection

19k étoiles, MIT. 26 Skills, 19 agents, 61 scripts Python, 9 extensions,
71 tests, CHANGELOG de 1 511 lignes. Dépôt public de publication ; le
développement se fait dans un dépôt privé (`aimh`).

## Architecture

- **3 couches** : directive (SKILL.md), orchestration (agents), exécution
  (scripts Python avec sortie JSON). Règles internes : SKILL.md de 500 lignes
  au plus, références de 200 lignes au plus, chaque script a une docstring,
  une CLI et une sortie JSON.
- **Lanceur unique** : `scripts/claude-seo run <script.py>`, environnement
  Python isolé (`/seo setup`, `/seo doctor`), jamais de `pip install`
  improvisé.
- **Sécurité** : `url_safety.py` (blocage IP privées, loopback, métadonnées
  cloud, DNS rebinding) imposé à tout script qui suit une URL ; allowlist
  explicite `CLAUDE_SEO_LOCAL_TARGETS` pour auditer un site local.
- **Publication** : manifeste SHA-256 signé (`release_sign.py`,
  `verify_release.py`), contrôle de cohérence du graphe de références
  (`consistency_check.py` : liens morts, routage, orphelins), lint de
  portabilité des SKILL.md.
- **Rapports** : un seul générateur PDF (`google_report.py`, WeasyPrint +
  matplotlib), charte imposée, relecture automatique du PDF avant
  présentation (`_review_pdf()` : images vides, sections minces, doublons).
- **Publicité** : pied de page « Built by agricidaniel… Skool » après chaque
  livrable majeur. À écarter.

## Orchestrateur `/seo`

- Routage vers 25 sous-Skills ; « utilise ce hub seulement quand le domaine
  est clair et le workflow non ».
- **Audit complet** : détection du type d'activité (SaaS, local, e-commerce,
  éditeur, agence), puis jusqu'à 17 agents en parallèle, dont certains
  conditionnels (local si adresse détectée, google si identifiants, drift si
  une base existe, cluster si blog, e-commerce si boutique). Agents toujours
  présents : technique, contenu, schema, sitemap, performance, visuel, GEO,
  agentique, SXO.
- **Note SEO Health sur 100** : technique 22%, contenu 23%, on-page 20%,
  schema 10%, CWV 10%, préparation IA 10%, images 5%.
- **Priorités** : Critique (bloque l'indexation ou pénalise, tout de suite),
  Haute (1 semaine), Moyenne (1 mois), Basse.
- **Cadre de synthèse en 10 principes** (PERCEIVE, ANALYZE, VALIDATE, ACT) :
  chaque recommandation porte son principe premier, ses dépendances, **« comment
  saurait-on que ça a échoué ? »** et un indicateur avancé à suivre sans
  relancer l'audit. Pièges d'hypothèse listés (« la page d'accueil
  représente le site », « peu de trafic = peu de valeur »…). Règle : si une
  recommandation contredit la SERP pour la même intention, la SERP gagne.
- **Registre des mises à jour Google** (`seo_updates.py`) : toutes les
  entrées citent une URL Google ; signale s'il est périmé ; « une
  coïncidence de dates est une hypothèse, jamais une preuve ».

## Références communes (`skills/seo/references/`)

- `quality-gates.md` : minimums de mots par type de page (accueil 500,
  service 800, article 1 500…), **alerte à 30 pages locales, arrêt à 50**,
  pages programmatiques sûres ou risquées, titre 30 à 60 car., méta 120 à
  160, alt 10 à 125, liens internes par type de page, fraîcheur.
  **Contrôle des méta « gabarits »** (`metadata_template.py`) : une
  description qui recopie le titre et finit sur un appel à l'action générique.
  Fragilité : les minimums de mots contredisent ce que Google dit (le Skill
  contenu le reconnaît : « planchers de couverture, pas des cibles »).
- `eeat-framework.md` (QRG 11 septembre 2025, revérifié juin 2026) : « la
  confiance est le membre le plus important » ; pondération interne
  Expérience 20, Expertise 25, Autorité 25, Confiance 30 ; YMYL élargi
  (élections, processus démocratiques) ; politiques anti-spam au
  30 août 2026 (abus de réputation de site traité différemment dans l'EEE
  depuis le 30 août 2026, abus de contenu à grande échelle nommant l'IA
  générative, **détournement du bouton retour** sanctionné depuis le
  15 juin 2026) ; garde-fous anti-hallucination (« pas de récit de
  watershed », pas de pourcentages de chute par secteur).
- `cwv-thresholds.md` (23 sept. 2026) : LCP 2,5 s, INP 200 ms, CLS 0,1 au
  75e centile ; « pas de VSI, pas de CWV 2.0 » ; sous-parties du LCP ;
  Soft Navigations par défaut dans Chrome 151 sans effet de classement.
- `schema-types.md` (Schema.org 30.1, 16 sept. 2026) : types actifs ;
  **FAQPage : résultats enrichis retirés pour tous les sites le
  7 mai 2026** (ne pas recommander, ne pas faire retirer, QAPage pour de
  vraies questions d'utilisateurs) ; HowTo retiré (sept. 2023) ;
  VideoObject `creator` recommandé depuis le 24 sept. 2026.
- `thinking-framework*.md` : voir ci-dessus.
- Références locales (signaux, comportement, schémas, multi-sites) et
  « maps » (géo-grille, API) : hors périmètre demandé (« laisse de côté
  seo-maps »).

## `/seo audit`

- Rendu de la page d'accueil (`render_page.py`, brut et rendu, détection
  SPA), exploration jusqu'à 500 pages (robots.txt, 3 redirections, 30 s par
  page, 5 requêtes simultanées, 1 s de délai), délégation aux agents,
  note, artefacts persistés (`{domaine}-audit/` : rapport complet, plan
  d'action, `audit-data.json`, constats par catégorie, captures).
- Format `audit-data.json` normé (catégories, constats avec gravité,
  « ce qui marche », plan en 4 phases : semaine 1, semaines 2-3, mois 2,
  continu).
- Cas limites : site injoignable, robots qui bloque, 429, site de plus de
  500 pages, agent qui atteint son budget (chaque agent écrit un constat
  partiel dès sa première passe).

## `/seo page`

- On-page (titre 50-60, méta 150-160, H1 unique, hiérarchie, URL, liens),
  contenu (mots, Flesch, densité 1-3%, E-E-A-T, fraîcheur), technique
  (canonical, robots, Open Graph, Twitter, hreflang), schema, images
  (> 200 Ko attention, > 500 Ko critique, WebP/AVIF, dimensions, **détection
  des chargeurs paresseux JS pour éviter les faux positifs**), CWV estimés
  depuis le HTML. Carte de score par catégorie.
- Fragilité : densité de mots-clés 1-3% et Flesch (anglais) sont du folklore
  ou inadaptés au français.

## `/seo technical` (9 catégories)

Exploration (robots, sitemaps via `sitemap_discovery.py`, profondeur
3 clics, **limites de récupération de Googlebot : 2 Mo de HTML, 64 Mo de
PDF**, pas de réglage manuel du crawl depuis janv. 2024, doc déplacée sur
developers.google.com/crawling le 20 nov. 2025, AMP sans avantage et URL
éditeur directes depuis le 1er juillet 2026), **gestion des robots IA**
(tableau GPTBot / OAI-SearchBot / ChatGPT-User, ClaudeBot /
Claude-SearchBot, Google-Extended, Applebot-Extended… et ce que bloquer
chacun fait ou ne fait pas ; agents déclenchés par l'utilisateur qui
ignorent robots.txt ; Web Bot Auth), indexabilité (canonicals, doublons,
**jusqu'à deux semaines pour qu'une correction de canonical soit prise en
compte**, pagination sans rel=next), sécurité (HTTPS, en-têtes,
**détournement du bouton retour = Critique**), URL, mobile (parité
mobile/desktop comme contrôle principal, interstitiels, contenu caché
derrière des onglets), CWV, données structurées, **rendu JS** (canonical
injecté qui diffère, noindex retiré par JS toujours appliqué, pas de rendu
JS sur les codes non-200, données structurées JS traitées en différé),
IndexNow (hors Google). Note : « ne noter que ce qui a été mesuré ; une
catégorie non mesurée est “non mesurée”, jamais un chiffre ».

## `/seo content`

- **Test Qui / Comment / Pourquoi** de Google en premier.
- E-E-A-T 20/25/25/30, AI Citation Readiness sur 100.
- Planchers de mots « couverture, pas cibles » ; Flesch « pas un facteur ».
- **Google, 15 mai 2026 (maj 10 juillet 2026)** : « optimiser pour l'IA
  générative, c'est du SEO » : pas besoin de fichiers IA, de balisage, de
  Markdown, de découpage en morceaux ni de réécritures spéciales.
- **Google, 5 juin 2026** : aucun outil tiers n'a accès aux données de
  classement ; les scores sont des heuristiques, le dire.
- **Nettoyage** (`content_humanize.py`) : caractères invisibles (y compris
  les balises Unicode de texte caché), remplacements 1 pour 1 prudents ;
  honnêteté : les filigranes statistiques (type SynthID) ne se retirent pas ;
  refus de « blanchir » le contenu d'autrui.
- Corrélation avec les mises à jour Google (même registre).

## `/seo content-brief`

- **Deux modes** : améliorer une page existante (garder ce qui est fort,
  distinguer « garder ou renforcer » et « ajouter », jamais de réécriture
  complète si des retouches suffisent) ou créer une page.
- Contexte : page d'accueil + sitemap pour savoir ce que le site vend.
- SERP : top 5, **filtre des non-concurrents** (Wikipedia, Reddit,
  Pinterest, Amazon, YouTube, sites publics, outils SEO, annuaires…,
  `excluded-domains.md`), note de chaque concurrent sur 40 (profondeur,
  forme, SEO, UX), **3 types d'écart** (sujet absent, sujet traité en
  surface, qualité : périmé, sans expert, mal mis en forme), priorité
  `impact × avantage / effort`.
- Intention en 4 classes + **format que la SERP récompense** (guide,
  liste, comparatif, page de conversion, vidéo, pack local).
- **Règle de pertinence** : chaque titre suggéré doit être quelque chose que
  le site peut réellement livrer ; ne pas recopier la structure d'un
  concurrent qui vend autre chose. Très bon garde-fou.
- **Règle de couverture** pour une page hub : chaque catégorie réelle du
  site a sa section et son lien, aucune inventée, aucune oubliée.
- **Règle de langage** : jamais de noms de méthodes ou d'outils dans le
  livrable (« pas de méthode X, de formule Frase »).
- **Information Gain non négociable** : dire exactement ce que la page
  apporte qu'aucune page classée n'a (données propres, cas réels, expert,
  synthèse originale), « jamais “plus de détails” ou “meilleure mise en
  forme” ». À reprendre tel quel.
- Placement du mot-clé (titre, H1, URL, méta, 100 premiers mots, un alt),
  « pas de densité cible » dans le SKILL, mais la référence garde des
  repères de densité : contradiction interne.
- Méta : titre 50-60 « jamais en dessous de 50 », description 130-150
  « jamais en dessous de 130 », « pas de guillemets, Google tronque aux
  guillemets » **[à vérifier, probablement faux]**. Contredit
  `quality-gates.md` (30-60 et 120-160) : trois jeux de chiffres dans le
  même dépôt. Nous écrirons une seule règle, fondée sur la largeur en
  pixels et la réécriture fréquente par Google.
- 3 à 5 liens internes avec ancre, statut hub ou rayon.
- Mode plan seul. Erreurs : URL injoignable, aucun concurrent après
  filtre (élargir et le dire), pas de sitemap (le dire), nombre de mots
  non fourni (moyenne des concurrents, à remplacer chez nous par « ce que
  le sujet demande »).

## `/seo schema`

- Détection JSON-LD, Microdata, RDFa ; validation ; génération à partir de
  modèles (Organization, LocalBusiness, Article…).
- **Tableau des types retirés avec dates** (`deprecated-types-2024-2026.md`) :
  Vehicle Listing, ClaimReview, Estimated Salary, Learning Video, Course Info
  (12 juin 2025), SpecialAnnouncement (31 juillet 2025), Practice Problem
  (annonce 5 nov. 2025, outils retirés janv. 2026), HowTo (sept. 2023),
  FAQPage (restreint août 2023, **retiré pour tous le 7 mai 2026**, docs
  retirées le 15 juin 2026). Book Actions **pas** retiré ; Dataset
  seulement pour Dataset Search.
- **Table de remplacement** (ClaimReview → aucun, EstimatedSalary →
  JobPosting.baseSalary, LearningVideo → VideoObject, Course Info → Course
  list).
- Bonne nuance : une FAQPage existante est signalée en « info », pas à
  retirer.
- À reprendre : le tableau daté, revérifié par nous aux sources Google.

## `/seo sitemap`

- **Découverte avant de déclarer absent** (`sitemap_discovery.py` : lignes
  `Sitemap:` du robots.txt, chemins courants, cible d'un autre hôte
  vérifiée). Bon cas limite : un robots.txt qui déclare un sitemap mort.
- Contrôles : XML valide, 50 000 URL et 50 Mo non compressés, URL en 200,
  `lastmod` au format W3C et fidèle au dernier changement significatif
  (alerte si tous identiques ou plus récents que le contenu),
  `priority`/`changefreq` ignorés, référencé dans robots.txt, pages
  explorées absentes du sitemap, pas d'URL non canoniques, noindex ou
  redirigées.
- Sitemaps image (2 balises valides, 1 000 images par URL), vidéo, actualités
  (1 000 par fichier, 2 derniers jours).
- Mode génération : gabarits par secteur (`seo-plan/assets/`), alerte à 30
  pages locales, arrêt à 50, liste des pages programmatiques sûres ou
  risquées, `STRUCTURE.md`.
- Ce qui manque pour notre besoin « sitemap → maillage par clusters » : le
  Skill ne regroupe pas les URL par thème et ne propose aucun lien. À
  chercher dans `seo-cluster` et ailleurs.

## `/seo images`

- Alt, poids (seuils par type d'image), formats (`<picture>` AVIF > WebP >
  JPEG), `srcset`, dimensions (CLS), `loading="lazy"` sauf image LCP,
  `fetchpriority="high"` sur l'image LCP, noms de fichiers.
- Métadonnées IPTC : `DigitalSourceType: TrainedAlgorithmicMedia` exigé par
  Merchant Center pour les images produit générées par IA.
- Tableau honnête « ce qui compte pour Google Images » : alt et contexte
  forts, IPTC Creator affichage seul, EXIF et mots-clés IPTC nuls.
- Dépend d'exiftool, cwebp, ImageMagick (repli prévu). Pour nous : la grille,
  pas la chaîne de conversion.

## `/seo geo`

- **Cadre** : les constats GEO sont « les fondamentaux SEO appliqués aux
  surfaces IA » ; si la communauté contredit Google, Google gagne et la
  contradiction est écrite.
- **Mythes rejetés par Google** (guide IA, 15 mai 2026, maj 10 juillet
  2026) : llms.txt et fichiers IA, découpage en morceaux, réécriture pour
  l'IA, mentions artificielles, surinvestissement en données structurées.
  Ce qui compte : contenu unique, de première main (exemple Google :
  « 7 conseils » contre « pourquoi nous avons renoncé à l'inspection »).
- **Contrôle d'éligibilité** : page indexée et éligible à l'extrait, et
  réglage Search Console « Search generative AI » (inclure par défaut,
  exclure, hériter ; ouvert à tous le 31 août 2026, pas un signal de
  classement, pas un contrôle d'entraînement) **[à vérifier : postérieur à
  ma date de connaissance]**.
- **Tableau des robots IA** et règle « chaque affirmation se vérifie sur
  son propre robot » : GPTBot (entraînement) ≠ OAI-SearchBot (citation
  ChatGPT), ClaudeBot ≠ Claude-SearchBot, Google-Extended ≠ Googlebot (AI
  Overviews servis par l'index Googlebot), Applebot-Extended ≠ Applebot.
  Agents déclenchés par l'utilisateur qui ignorent robots.txt. C'est le
  meilleur contenu du Skill ; notre v1 `/geo-*` doit être comparée ligne à
  ligne.
- **Note GEO /100** : citabilité 25, structure 20, multimodal 15, autorité
  20, accès technique 20. Chiffres tiers en grand nombre (« mentions de
  marque 3× plus corrélées que les backlinks », Ahrefs ; « 44% des
  citations dans les 30% du haut de page », SE Ranking ; « contenu de moins
  de 3 mois 3× plus cité ») : ce sont des corrélations d'études
  d'éditeurs d'outils. Le Skill lui-même dit « non revérifié le
  23 sept. 2026 ». Chez nous : seulement avec source et date, en option.
- **Blocs de 130-170 mots** présentés comme heuristique tout en contredisant
  le « pas besoin de découper » de Google : à écarter comme règle.
- llms.txt : présence rapportée, poids nul (`llmstxt-evidence.md` : guide
  Google, Mueller, Illyes, SE Ranking 300 k domaines, OtterlyAI 0,1% des
  requêtes de robots IA). Utile seulement pour la documentation de
  développeurs. Notre v1 avait déjà corrigé ce point ; à revérifier.
- Surfaces : AI Overviews (corrélées au classement) et AI Mode (vivier plus
  large ; « 13,7% d'URL communes », Ahrefs) ; Preferred Sources (préférence
  par utilisateur, pas un signal général) ; contrôle d'apparition par
  `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`.
- Sortie `GEO-ANALYSIS.md` : note par plateforme **seulement si mesurée par
  un outil**, sinon « préparation qualitative, non mesurée ». Bonne règle.
- Fragilités : statistiques d'audience non pertinentes pour un audit
  (« 2,5 milliards d'utilisateurs »), recommandations Wikipedia (« créer
  une présence Wikipedia » = risque de violation des règles de Wikipedia).

## `/seo agentic`

- Cadre : « préparation des agents = accessibilité + performance + politique
  d'accès, avec une couche Markdown et découverte » ; WebMCP en option pour
  les sites à formulaires.
- Étapes : fraction Lighthouse « Agentic Browsing » `X/N` (jamais en
  pourcentage, N ≤ 6) **[à vérifier : catégorie postérieure à ma date de
  connaissance]**, `agentic_check.py` (rendu serveur, groupes robots.txt par
  agent, Content-Signal, llms.txt, Markdown, `/.well-known`, WebMCP),
  `agent_ux_check.py` (arbre d'accessibilité, heuristique locale sur 100),
  test du pare-feu avec des user-agents d'IA **seulement avec autorisation**.
- Priorités P0 à P3 avec l'identifiant du contrôle qui les prouve ; « ne pas
  recommander une P2 tant qu'une P0 mesurée échoue » ; une P0 non testée est
  « non testée ».
- Mode correction : brouillons sur la sortie standard, rien de déployé ;
  Content-Signal ajouté sans toucher Allow/Disallow ; **la politique
  d'entraînement est demandée à l'utilisateur, jamais décidée**.
- Règles d'honnêteté : aucune promesse de trafic ; pas de chiffres
  d'économie de jetons des éditeurs ; ne jamais dire qu'un agent nommé lit
  le Markdown ou llms.txt ; dater chaque fait fournisseur, alerte au-delà de
  60 jours (`vendor-matrix.md` avec procédure de rafraîchissement).
- Sécurité : contenu récupéré = donnée, un llms.txt qui s'adresse à l'agent
  est un constat, pas un ordre.
- Comparer ligne à ligne avec notre `/geo-agentic` v1.

## `/seo cluster`

- **Regroupement par recouvrement de SERP**, pas par similarité de texte :
  7-10 URL communes dans le top 10 = même page ; 4-6 = même cluster ; 2-3 =
  liens croisés ; 0-1 = séparés. Bris d'égalité pour 3-4 (domaines, intention,
  écart de volume). Optimisation : pré-groupes par intention, échantillon de
  20% des paires sautées vérifié. Anti-motifs : stemming seul, domaines
  omniprésents (Wikipedia, Reddit) à retirer avant le calcul.
- Expansion 30-50 variantes (recherches associées, PAA, modificateurs), puis
  intention, pilier, 2-5 clusters, 2-4 articles chacun.
- **Matrice de liens** : rayon → pilier et pilier → rayon obligatoires, 2-3
  liens entre rayons, 0-1 entre clusters, 3 liens entrants minimum, aucune
  orpheline, ancres variées (une ancre ≤ 40% des liens vers une page).
- Cannibalisation : un mot-clé principal par page ; fusion au-delà de 7.
- Sorties : `cluster-plan.json`, carte HTML interactive, briefs, tableau de
  bord après exécution (couverture, orphelines, liens au pilier…).
- **Fragilités** : (1) la recherche web de Claude ne rend pas un top 10
  organique stable, le Skill le reconnaît (« répéter et garder le plus
  fréquent ») mais le seuil 7/10 devient fragile sur un échantillon bruité ;
  (2) aucun script : le calcul de recouvrement est fait « à la main » par le
  modèle sur des centaines de paires ; (3) planifie **à partir d'un mot-clé**,
  jamais à partir des pages existantes d'un site. Notre besoin (« analyser le
  sitemap et construire le maillage par clusters ») n'est couvert par aucun
  Skill de claude-seo. Notre v1 le couvre déjà (`maillage.py` : sitemap,
  TF-IDF, liens existants exclus, trafic) : l'avantage est de notre côté,
  à approfondir.
- Nombre de mots pilier 2 500-4 000, rayon 1 200-1 800 : folklore, à écarter.

## `/seo sxo`

- **Idée centrale** : une page techniquement parfaite échoue si ce n'est pas
  le **bon type de page** pour la requête. Lecture de la SERP à rebours :
  type de chaque résultat parmi 8 (taxonomie), consensus (> 60% fort,
  40-60% mixte, < 40% fragmenté), fonctionnalités de la SERP, annonces,
  PAA, recherches associées, AI Overview.
- Tableau de gravité des décalages (article contre pages produit =
  critique…).
- **Récits utilisateurs** tirés des signaux de la SERP (« en tant que…, je
  veux…, parce que…, mais… »), 4 à 7 personas notés pertinence, clarté,
  confiance, action (25 chacun).
- Note d'écart SXO sur 100 (7 dimensions), séparée de la note SEO.
- Maquette actuelle / cible avec des consignes concrètes (« pas “ajoute un
  CTA”, mais “CTA tarif avec badge d'économie annuelle sous le
  bandeau” »).
- À reprendre : la détection du décalage de type de page (c'est la première
  cause de non-classement qu'un audit classique rate). Les personas déduits
  des annonces sont plus fragiles : option.

## `/seo drift`

- Instantané (titre, méta, canonical, robots, H1-H3, JSON-LD, Open Graph,
  CWV, statut HTTP, empreintes SHA-256 du HTML et du schema) en SQLite,
  comparaison par 17 règles en 3 gravités, historique, URL normalisée (UTM
  retirés, paramètres triés).
- Notre v1 a déjà `/seo-drift` (`drift.py`) : comparer les 17 règles avec
  les nôtres pendant la matrice.

## `/seo plan`

- Découverte, concurrents, architecture (gabarits par secteur : SaaS,
  local, e-commerce, éditeur, agence, générique), stratégie de contenu,
  fondations techniques, **feuille de route en 4 phases** (semaines 1-4,
  5-12, 13-24, mois 7-12), tableau d'indicateurs à 3/6/12 mois.
- Faible : générique, « Domain Authority » comme indicateur (métrique d'un
  outil tiers), aucune donnée réelle sans DataForSEO. Les gabarits de
  secteur contiennent des minimums de mots et de « % unique » non sourcés.
  Notre v1 a `/seo-plan` : à comparer, l'apport ici est surtout
  l'arborescence type par secteur.

## `/seo programmatic` (hors périmètre demandé, gardé pour référence)

- Portes de qualité (alerte à 100 pages non relues, arrêt à 500), test de
  valeur autonome (« publierait-on cette page si elle était seule ? »),
  déploiement par lots de 50-100, échantillon relu de 5-10%, contrôle des
  méta gabarits (`metadata_template.py`). Seuils de « % unique » sans
  source Google (le Skill local le dit : « pas de seuil confirmé »).

## `/seo competitor-pages`

- 4 types : « X vs Y », « alternatives à X », « meilleurs outils »,
  tableau comparatif. Exactitude : sources publiques, prix « au [date] »,
  revue trimestrielle, affiliation déclarée, forces du concurrent reconnues,
  pas de dénigrement.
- Schema Product + AggregateRating proposé sur ses propres produits :
  risque (avis auto-attribués) **[à vérifier aux règles Google sur les
  avis]**.
- **Ce que nous ajoutons** : le cadre français de la publicité comparative
  (Code de la consommation, comparaison objective de caractéristiques
  essentielles, pertinentes, vérifiables et représentatives)
  **[à vérifier : articles exacts]** ; formules de titre avec l'année, à
  n'utiliser que si la page est vraiment mise à jour.

## `/seo local`

- Détection du type (adresse physique, zone de service, hybride) qui change
  les contrôles ; détection du secteur (restaurant, santé, juridique,
  services à domicile, immobilier, automobile).
- 6 dimensions : fiche Google (25), avis (20), signaux on-page (20), NAP et
  citations (15), schema local (10), liens locaux (10).
- Bons contrôles : **test du remplacement** (« si on change le nom de la
  ville et que le texte tient, c'est une page satellite ») ; NAP comparé
  entre HTML, JSON-LD et fiche ; sous-type schema correct ; `@id` unique par
  établissement ; Q&A Google en voie de disparition ; filtrage des avis
  interdit ; limites déclarées (pas de géo-grille, pas de données de fiche).
- **Très américain** : BBB, Yelp, Data Axle, Neustar, FTC, HIPAA, Chambre de
  commerce. Statistiques tierces nombreuses (Whitespark, BrightLocal, Sterling
  Sky, Seer) dont certaines sans date ni lien.
- **Ce que nous ajoutons** : annuaires français (PagesJaunes, Apple Business
  Connect, Bing Places, Waze, annuaires sectoriels et professionnels),
  règles françaises sur les avis en ligne (obligation d'information du
  Code de la consommation, DGCCRF) **[à vérifier : textes exacts]**,
  zones de chalandise françaises. À croiser avec `localseoskills`.

## `/seo backlinks`

- Sources par niveau : Common Crawl (toujours), Moz, Bing Webmaster,
  Keywords Everywhere (inscriptions gratuites), DataForSEO (payant).
- **Règle forte** : moins de 4 facteurs mesurés = pas de note,
  « INSUFFICIENT DATA (X/7) » ; avec Common Crawl seul, **aucun chiffre** ;
  porte de validation qui fait échouer le rapport si une note n'a pas de
  source notable. Pondération par confiance de la source (1,0 / 0,85 /
  0,70). À reprendre : c'est exactement notre règle « non mesuré n'est
  pas noté ».
- Le suivi des liens gagnés et perdus demande un outil payant : le dire.
- Hors périmètre demandé, mais utile à l'audit (section « autorité »).

## `/seo google`

- Paliers d'identifiants (clé API : PageSpeed, CrUX, YouTube, NLP ;
  OAuth/compte de service : Search Console, inspection, sitemaps, Indexing ;
  GA4 ; Ads). Le palier détecté est annoncé avant tout.
- Search Console : 28 jours, `query,page`, gains rapides positions 4-10 à
  fortes impressions ; **totaux pris d'une requête sans dimension** car les
  lignes omettent les requêtes anonymisées ; inspection d'URL = vérité
  d'indexation.
- Faits datés à revérifier (postérieurs à ma date de connaissance) : rapport
  « Generative AI performance » (impressions seulement, AI Overviews + AI
  Mode, ouvert à tous le 31 août 2026) ; type de recherche « multimodal » ;
  clics AI Mode déjà dans le rapport Web ; **erreur de journalisation des
  impressions du 13 mai 2025 au 27 avril 2026** ; comptes TikTok,
  Instagram, X et YouTube vérifiables comme propriétés Search Console (utile
  pour notre « SEO social ») **[à vérifier]**.
- Indexing API réservée par Google aux offres d'emploi et diffusions en
  direct **[à vérifier : le Skill la présente-t-il comme générale ?]**.
- YouTube Data API : recherche (100 unités, 10 000 par jour gratuites).
- Rapport PDF : hors de notre règle « texte simple par défaut ».

## `/seo hreflang` (hors périmètre demandé)

- Auto-référence, liens retour, x-default, codes ISO, alignement canonical,
  méthodes (HTML, en-têtes, sitemap), audit de parité de contenu,
  adaptation culturelle. Utile pour les sites FR/BE/CH/CA : à proposer
  comme option si l'utilisateur le veut.

## `/seo flow`

- Bibliothèque de 41 prompts (CC BY 4.0, auteur du dépôt), 5 étapes
  (trouver, levier, optimiser, gagner, local). Choix de 2-3 prompts selon le
  contexte. Surtout un produit d'appel vers la communauté de l'auteur ;
  pas de mesure. À écarter, sauf idées ponctuelles (carte de score « double
  surface » Google + IA).

## Agents, hooks, extensions

- **19 agents** (1 615 lignes) : surtout des copies condensées des SKILL.md
  (`model: opus`, `maxTurns` jusqu'à 45). Ils servent à l'audit parallèle.
  Leçon du CHANGELOG : un agent qui atteint son budget doit écrire un
  constat partiel dès la première passe.
- **Hook** `validate-schema.py` après chaque écriture : JSON-LD avec
  placeholder ou type retiré = code 2 (Claude lit l'erreur), avertissements
  en contexte additionnel. Idée à reprendre pour nos modèles de schema
  (version script, pas hook, pour rester portable vers claude.ai).
- **9 extensions** payantes ou à clé (DataForSEO, Ahrefs, SE Ranking,
  Profound, Firecrawl, Bing Webmaster, Matomo, Unlighthouse, Banana) avec
  **contrôle de coût avant chaque appel** (`dataforseo_costs.py` :
  « needs_approval » au-delà d'un seuil, « blocked » au-delà du budget).
  À reprendre comme règle : annoncer le coût d'un connecteur payant avant
  de l'appeler.

## Scripts exécutés (12 oct. 2026)

Environnement isolé, textes de test Assurly en français et en anglais.

| script | résultat | verdict |
|---|---|---|
| `content_quality.py` | anglais : 3 remplissages, 5 tics IA, qualité 41/100. **Français : 0 détection**, qualité 78/100 sur un texte truffé de tics (« dans un monde en constante évolution », « plongeons dans le vif du sujet », « véritable pilier », « en somme ») | listes anglaises seulement ; inutilisable tel quel pour nous |
| `content_verify.py` | anglais : « 73% » compté **cité** parce que « According to a recent study » suit dans la fenêtre : une « étude récente » sans nom passe pour une source. **Français : 0 affirmation extraite** (« 73% des Français », « 12% en 2025 ») | idée excellente (affirmations sans source avant publication), exécution à refaire : FR, source nommée exigée |
| `content_humanize.py` | retire bien les caractères invisibles ; **casse la typographie française** (« maison\u202f! » devient « maison! ») ; réécritures anglaises qui cassent la grammaire (« Let's dive in! » → « Starting with! », phrase sans majuscule après « In essence, ») | notre humaniseur LinkedIn v2 fait déjà mieux en français |
| `metadata_template.py` | titre recopié en tête de description repéré ; titres courts ignorés à dessein ; CTA de fin en anglais seulement ; ne compare pas les descriptions **entre** pages (deux descriptions identiques au mot près sauf le produit ne sont pas signalées) | bonne idée, à refaire en FR avec comparaison entre pages |
| `seo_updates.py` | 58 entrées, chacune avec URL Google, vérifié le 28 sept. 2026, alerte de péremption | **à reprendre** (registre daté, sources primaires) |
| `sitemap_discovery.py`, `agentic_check.py` | **échec total derrière un proxy local** : le garde-fou SSRF refuse un proxy en 127.0.0.1, or c'est le cas des bacs à sable (Claude Code web, exécution de code claude.ai). Le CHANGELOG (#280) a corrigé le cas d'un proxy public seulement | cas limite à traiter chez nous : fonctionner derrière `HTTPS_PROXY`, et sinon accepter un fichier collé par l'utilisateur |

**Tests** : **1 020 réussis, 3 échecs, 3 ignorés** (les
3 échecs viennent du proxy de l'environnement qui fuit dans les tests). Suite
sérieuse : entrées hostiles, ReDoS, SSRF, encodages, cohérence des
manifestes, absence de tiret cadratin (`test_no_em_dash.py`).

## Ce que le CHANGELOG apprend

- **Les auteurs eux-mêmes ont publié des faits inventés**, puis les ont
  retirés : « watershed de décembre 2025 » avec des chutes de « 71, 67,
  52% », pondérations E-E-A-T présentées comme celles de Google, FID « dans
  Lighthouse », QAPage présentée comme « remplaçante de FAQ », ligne de
  robot `anthropic-ai` non vérifiée, modèle d'AI Mode changé trois fois.
  Conclusion pour nous : chaque fait daté porte sa source primaire et sa
  date de vérification, et un fait non revérifié porte [à vérifier].
- Bugs récurrents : encodage (UTF-8 sans charset lu en Latin-1), scripts
  enregistrés nulle part, chemins de références cassés entre Skills,
  commandes documentées qui n'existent pas, scripts qui sortent en code 1
  sur un résultat valide mais bas (`preload_check.py`), compteurs de coût
  qui perdent des écritures concurrentes. Nos tests d'intégrité LinkedIn
  (fichiers cités, sous-commandes `--help`) couvrent déjà la plupart.

## Synthèse claude-seo

**À reprendre** (avec réécriture, licence MIT) :
- note « non mesuré = non noté » (technique, backlinks, plateformes GEO) ;
- registre daté des mises à jour Google, « coïncidence de dates =
  hypothèse » ;
- tableau des robots IA et règle « chaque affirmation sur son robot » ;
- tableau daté des types de schema retirés et de leurs remplaçants ;
- découverte du sitemap avant de le déclarer absent, contrôles `lastmod` ;
- brief : filtre des non-concurrents, 3 types d'écart, règle de pertinence,
  règle de couverture du hub, Information Gain non négociable ;
- SXO : décalage de type de page en premier ;
- recouvrement de SERP pour regrouper (avec la réserve sur la qualité des
  données de recherche web) ;
- recommandation falsifiable (« comment saurait-on que ça a échoué ? ») ;
- contrôle de coût avant tout connecteur payant ;
- faits techniques datés (limites de Googlebot, rendu JS, canonical,
  détournement du bouton retour, contrôle « Search generative AI »), tous à
  revérifier par nous.

**À améliorer** :
- tout ce qui est texte (qualité, affirmations, humaniseur, méta) : anglais
  seulement, à refaire en français ;
- clusters : notre v1 part déjà des pages existantes ; ajouter le
  recouvrement de SERP pour les mots-clés à venir ;
- local : version française (annuaires, avis, règles) ;
- comparatifs : cadre français de la publicité comparative.

**À écarter** :
- minimums de mots, densité de mots-clés, Flesch, titres « jamais sous 50 »,
  « Google tronque aux guillemets » ;
- statistiques tierces en tête de Skill (audience, corrélations) ;
- rapports PDF, publicité de l'auteur, FLOW, génération d'images ;
- e-commerce, maps, programmatique, hreflang (hors périmètre, options
  possibles).

