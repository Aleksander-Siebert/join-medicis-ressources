# Agent SEO « du mot-clé à l'article » : collecte et matrice de capacités

Date de la collecte : 16 novembre 2026.
Statut : **en attente de validation**, rien n'est écrit.

Mission choisie par l'utilisateur : du mot-clé à l'article, données gratuites
d'abord, en trois versions (Claude, Dust, Grok Bot).

## 1. Ce qui a été lu

Dépôts clonés le 16 novembre 2026 (`git clone --depth 1`) :

| Dépôt | Licence | Lu | Ce que c'est |
|---|---|---|---|
| AgriciDaniel/claude-blog (2 765 étoiles) | MIT | Skills d'écriture, de brief et de vérification des faits, contrat de livraison | 33 Skills de blog, 5 sous-agents, portes de livraison |
| kevinbadi/seo-agent-kit | MIT | en entier (Skill, 6 scripts, schéma) | Agent qui trouve les sujets, écrit, vérifie et publie sur WordPress, puis apprend des inscriptions |
| samynym/groundskeeper | MIT | README, conception de la garde | Mise à jour de contenus en « monde clos » : aucune affirmation sans source déjà connue |
| iannuttall/seo (seoskill.dev) | Apache 2.0 | README, confidentialité, Skill | Serveur MCP Search Console, GA4, Bing, dates des mises à jour Google, crawl |
| nowork-studio/notfair-plugin (4 213 étoiles) | MIT | workflow de rédaction, structure | 45 Skills SEO, GEO, publicité, WordPress |
| Ryze-AI-Adgent/open-seo-mcp-skills (10 089 étoiles) | MIT | en entier (8 Skills courts, installation) | Skills courts branchés sur le connecteur hébergé de Ryze |
| avansaber/seo-monster, squirrelscan, geo-aeo-tracker | MIT | descriptions seulement | Hors mission (MCP local Search Console, audit technique, suivi de visibilité IA) |

En ligne : l'article d'Ahrefs (Louise Linehan) sur Letaido, l'article de
Dust (Davis Christenhuis, 17 juin 2026) sur ses 4 agents SEO, les
documentations de Dust et la page de lancement de Grok Bot.

Déjà analysés pour nos packs SEO et GEO : claude-seo, geo-seo-claude,
seomachine, superseo-skills, marketingskills.

## 2. Le point de départ : ce que nous avons déjà

`/seo-article` (pack SEO) mène déjà un article du mot-clé à la livraison, en
8 étapes validées une à une :

1. cadrage ;
2. mots-clés ;
3. SERP ;
4. plan ;
5. rédaction ;
6. contrôles ;
7. maillage ;
8. livraison.

Il comprend aussi :
- `pipeline.py`, qui tient l'état et la reprise ;
- un portail qualité par portes : une affirmation sans source en YMYL bloque ;
- un mode autonome.

L'agent n'est donc pas un nouveau rédacteur. C'est **`/seo-article` plus une
couche agent** :
- trouver les sujets seul ;
- tourner à heure fixe ;
- se souvenir ;
- livrer un brouillon ;
- apprendre des résultats.

S'y ajoute la déclinaison sur trois plateformes.

## 3. Matrice de capacités

Verdict : **R** reprendre, **A** améliorer, **E** écarter.

### Trouver les sujets

| Capacité | Source | Verdict | Ce que nous faisons |
|---|---|---|---|
| Requêtes avec impressions en page 2 ou 3 dans Search Console : sujets où le site est presque visible | seo-agent-kit (`scout.mjs`), open-seo-mcp-skills, seoskill | R | Source n°1, gratuite, à partir de l'export Search Console ou d'un connecteur |
| Veille de mots-clés autour d'un thème, nouvelles idées ajoutées à un tableau avec la date de détection | Dust, agent SEOMonitor | A | Un fichier `sujets.csv` (ou Google Sheet) tenu par l'agent : volume si disponible, SERP, idée de titre, date |
| Volumes gratuits par le planificateur de mots-clés Google Ads | open-seo-mcp-skills | A | Option : il faut un compte Google Ads. Sinon, pas de volume inventé : l'agent classe par impressions Search Console |
| Semrush ou Ahrefs pour les volumes et la difficulté | Dust, Ahrefs | A | Option pour ceux qui ont l'abonnement, jamais requise |
| Sujets tirés des actualités et des sorties produit | seo-agent-kit | A | Option : réutiliser la collecte du Guetteur (flux RSS) |
| Déclinaison des articles gagnants en 6 intentions distinctes | seo-agent-kit (`scout.mjs`) | A | Proposée au rapport mensuel, jamais lancée seule |
| Une intention par sujet : dédoublonnage par mots et par sens, refus au-delà de 0,8 de similarité de titre | seo-agent-kit | R | Contre la cannibalisation : comparé aussi aux articles déjà publiés (sitemap) |
| Vérifier que le sujet colle à la marque avant d'écrire | Dust, agent SERPScout (lit Notion) | R | Étape « pertinence » lue dans `site-context.md`, existant dans le pack |

### Écrire et contrôler

| Capacité | Source | Verdict | Ce que nous faisons |
|---|---|---|---|
| Analyse SERP, plan, rédaction, contrôles, maillage | `/seo-article` | R | Inchangé |
| Fiche « vérité produit » : prix, fonctionnalités, limites, interdits ; l'agent n'affirme rien d'autre sur la marque | seo-agent-kit (`facts.json`) | R | `faits.md` à côté de `site-context.md`, contrôlé par script : un prix absent de la fiche bloque |
| Monde clos : un chiffre de l'article doit figurer mot pour mot dans une source citée | groundskeeper | A | Renforce `affirmations.py`, qui demande déjà une source : il vérifiera aussi la présence du chiffre |
| Vérifier la citation en ouvrant la source (correspondance exacte, paraphrase, absente) | claude-blog (`blog-factcheck`) | R | Étape de contrôle ajoutée au portail, limitée aux chiffres et aux citations |
| Table « affirmation, source » livrée avec l'article | groundskeeper | R | Bloc en fin de brouillon : la relecture se fait sur la table, pas dans le texte |
| Ciblage des surfaces (Google, AI Overviews, assistants IA) avant d'écrire | claude-blog (FLOW) | A | Déjà couvert par le pack GEO ; une ligne dans le cadrage |
| Image principale générée gratuitement, crédits obligatoires | claude-blog (`generate_hero.py`) | E pour l'instant | Demande des bibliothèques et un service d'images : hors du « sans installation » |
| Sous-agents rédacteur, relecteur, SEO | claude-blog, Dust | E | Coût et lenteur sans gain mesuré, comme pour le Guetteur |

### Livrer et apprendre

| Capacité | Source | Verdict | Ce que nous faisons |
|---|---|---|---|
| Publication automatique sur WordPress | seo-agent-kit (par défaut) | E | Contraire à notre règle : rien n'est publié à la place de l'utilisateur |
| Brouillon dans le CMS ou un document, validation humaine | notfair (« jamais sans oui explicite »), Dust, Ahrefs | R | Brouillon Google Docs, Notion, fichier, ou brouillon WordPress si le connecteur existe |
| Une seule publication par lancement, file d'attente de sujets | seo-agent-kit | R | Un article par passage, pour que chacun soit relu |
| Apprendre des résultats : poids des thèmes selon les clics Search Console (0,5 à 3 fois) | seo-agent-kit (`measure.mjs`, inscriptions PostHog) | A | Avec les clics et les impressions Search Console à 28 jours, gratuits ; les inscriptions en option |
| Fichier mémoire des leçons | Ahrefs (memory.md), `/seo-article` (apprentissages.md) | R | Existe : alimenté à chaque relecture |
| Tableau de bord des résultats | Dust (Frames) | A | Rapport mensuel en page HTML, sur le modèle des mails du Guetteur |

### Données gratuites, sans compte tiers

| Source | Accès | Verdict |
|---|---|---|
| Export CSV de Search Console | aucun tiers | **par défaut** : marche partout, même sans connecteur |
| seoskill.dev (MCP hébergé) | gratuit, connexion Google ; le serveur garde les jetons chiffrés | option, avec mention de ce qu'il stocke |
| seo-monster (MCP local) | tes propres identifiants Google | option pour Claude Code |
| Connecteur Ryze | hébergé par un éditeur commercial ; coût des données non précisé | écarté par défaut |
| Sitemap et pages publiques | aucun | pour le maillage et la cannibalisation |

## 4. Les trois plateformes, telles que vérifiées

| | Claude (Code, Cowork) | Dust | Grok Bot |
|---|---|---|---|
| Skills | SKILL.md natifs | « Skills » maison, import de fichiers par API ([doc](https://docs.dust.tt/api-reference/skills/import-skills-from-uploaded-files.md)) | aucun import de SKILL.md décrit ; on lui montre la tâche une fois |
| Scripts de contrôle | oui | outil « Computer » : capacité à lancer Python **[à vérifier]** | non décrit |
| Tâche planifiée | oui, cloud ou locale | oui (Triggers, Schedules) | routines, sans planificateur décrit |
| Connecteurs | MCP, Google Drive, Notion, Gmail | MCP distants ajoutés par un admin, Notion, Google Drive | pas de MCP : il se connecte aux sites et applications comme un humain |
| Coût | offre Claude payante | abonnement Dust **[à vérifier]** | inclus dans SuperGrok et Cursor, usage facturé à part, sans prix publié |
| Statut | stable, tâches cloud en aperçu | stable | bêta depuis le 11 août 2026, Android absent, Europe non précisée |

Conséquence : **seule la version Claude garde les contrôles par script**, qui
font la fiabilité du pack. Sur Dust et Grok Bot, la même méthode tourne en
instructions, avec une liste de contrôle relue par l'agent. C'est moins sûr,
et chaque version doit le dire.

## 5. Ce qui manque aux Skills existants, honnêtement

- Rien ne trouve les sujets tout seul : `/seo-article` attend un mot-clé.
- Pas de file d'attente ni de règle « une intention par article » face aux
  articles publiés.
- Pas de fiche « vérité produit » contrôlée par script.
- `affirmations.py` vérifie qu'une source existe, pas que le chiffre y figure.
- Pas de boucle d'apprentissage à partir des clics.
- Aucune version Dust ni Grok Bot.
