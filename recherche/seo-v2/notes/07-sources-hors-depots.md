# Sources hors dépôts · dissection

## Agent A (Ahrefs) · Ryan Law, 20 mai 2026

Article lu le 12 oct. 2026 (https://ahrefs.com/fr/blog/agent-a-content-marketing/).
Agent A est un espace de travail avec un agent qui construit et entretient
des outils, branché sur les données Ahrefs et des connecteurs (WordPress,
Notion, HubSpot…). L'utilisateur a demandé de **s'inspirer de sa
structure**. Ce qui compte pour nous :

| brique Agent A | ce qu'elle fait | ce que nous en tirons |
|---|---|---|
| Pipeline d'article | 11 étapes visibles et modifiables une par une (mot-clé, SERP, instantané thématique, plan, mentions produit, rédaction, maillage, recherche de citations, images, export), relance d'une étape avec un retour | un pipeline `/seo-*` en étapes **nommées, montrées et validables** : brief → plan validé → rédaction → contrôles → maillage → méta ; chaque étape peut être rejouée seule |
| Mise à jour d'anciens articles | entrée = une URL ; diagnostics (audit des affirmations, écarts thématiques) ; **chaque modification acceptée ou refusée une par une** | `/seo-refresh` en diff section par section, Garder / Réviser / Nouveau, avec audit des affirmations datées |
| Rapport mensuel | Search Console + analytics ; tuiles, tendance 12 mois, anomalies, gagnants et perdants ; **l'IA propose 6-10 points, l'humain écrit l'analyse** | `/seo-veille` : le script calcule, Claude propose des pistes, l'utilisateur conclut ; aucune causalité affirmée |
| Audit d'autorité thématique | plongements des pages, centre du site, distance cosinus (cœur, proche, médian, lointain), croisé avec le trafic ; « les pages de cœur ont environ 2× plus de trafic que les lointaines » (sur leur site) | script sans dépendance : vecteurs TF-IDF des titres, H1-H2 et texte des pages (pas de modèle de plongement disponible hors ligne), centre du site, classes cœur à lointain ; croisement avec les clics Search Console si l'export est fourni. À présenter comme heuristique |
| Veille concurrentielle | sitemaps concurrents surveillés chaque jour, résumé, tri humain (garder, ignorer, rejeter), recherche de mots-clés sur ce qui est gardé | option : comparer deux relevés de sitemap d'un concurrent (nouvelles URL, URL disparues), sans robot permanent |
| Maillage interne | plongement de l'article, similarité, re-pondération par le trafic, **exclusion des pages qui font déjà le lien**, paragraphe cible et ancre de 2-6 mots | cœur de notre `/seo-maillage` v2 : similarité locale + trafic + liens existants exclus + paragraphe d'insertion + ancre ; validation humaine lien par lien |

Limites : outil interne d'un éditeur, chiffres sur ses propres données, pas
de section « limites ». Les données du rapport montré sont fictives.

## Workflow de rédaction de l'utilisateur (Project Claude), anonymisé

Fourni le 2 oct. 2026. Le nom de l'entreprise et du persona sont retirés à
la demande de l'utilisateur ; l'exemple devient Assurly.

- **Persona** : rédacteur web SEO senior, expert interne d'un courtier
  (ici : assurance), ton professionnel, empathique et rassurant, **secteur
  YMYL** ; contenu d'abord pour les internautes ; option « hors sujet »
  pour un article non lié à la marque.
- **Mission** : des articles qui surpassent la concurrence par la
  fiabilité et la profondeur utile, répondent à une intention précise et
  mènent naturellement à l'offre adaptée.
- **4 cadres de structure**, choisis selon le type de page :
  PAS (pages produit, pages de conversion), AIDA (comparatifs, avis,
  pages hybrides), MECE (guides piliers, forte concurrence, AI Overviews),
  pyramide inversée (actualités, blog d'entreprise, réponses rapides).
  Arbre de décision (conversion ? actualité ? comparatif ? sinon MECE) et
  liste de contrôle par cadre (fichier « Carte des frameworks » dérivé
  d'une formation tierce : on réécrit, on ne copie pas).
  - **MECE vérifiable** : test de non-chevauchement (« si je supprime cette
    section, une autre l'absorbe-t-elle ? ») et **test d'exhaustivité** :
    20-30 requêtes du champ sémantique, chacune rattachée à une section ;
    les requêtes sans section sont des trous. **Calculable par un script.**
  - À corriger : « aucune section sous 200 mots », « RRF » présenté comme
    mécanisme de classement, chiffres d'exemple non sourcés (« 78% des
    utilisateurs… ») ; dans nos modèles, les exemples chiffrés sont des
    `{{à compléter}}`.
- **Règles de style strictes** :
  1. YMYL, zéro hallucination : coût, délai légal, condition contractuelle
     inconnus → « les conditions varient selon le contrat » ou invitation
     au devis.
  2. Voix active ; **zéro verbe modal d'hésitation** (« peut-être »,
     « pourrait », « devrait », « il semblerait ») ; règles d'entité de la
     marque (formule imposée pour nommer l'entreprise) ; ne pas prendre le
     système de santé d'un seul pays comme référence quand le public est
     international ; pas de tiret cadratin (virgule ou reformulation).
  3. Ton professionnel et accessible, sans familiarité.
- **Éradication des signes d'IA** : lexique interdit (FR et EN),
  participes présents déductifs en fin de phrase, triade automatique,
  parallélisme « non seulement… mais aussi », sections « Défis »,
  « Perspectives d'avenir », « En conclusion », verbes d'état gonflés
  (« se positionne comme », « sert de »), transitions (« il convient de
  noter », « force est de constater »). Référence demandée : la page
  Wikipédia « Signs of AI writing ».
- **Processus en 3 phases** :
  A. 6 questions **une par une** (mot-clé, langue, intention ; persona et
     zone ; offre à mettre en avant et liens internes ; termes techniques,
     juridiques ou médicaux obligatoires ; **données produit** (sinon pas
     de chiffres) ; type de page, sinon cadre proposé avec une phrase de
     justification).
  B. Analyse des concurrents sur le mot-clé, **plan détaillé** (title, H1,
     H2, H3 avec une ligne par section) selon le cadre, maillage vers les
     pages produit, **attente de validation**.
  C. Rédaction : 1 000 à 1 500 mots ; après l'introduction, **résumé de
     3 lignes maximum, simple** (décision de l'utilisateur du 2 oct. 2026,
     remplace « L'essentiel en 5 points ») ; gras réservé aux notions
     clés ; liens internes dans le corps sans les annoncer ; bloc méta
     final (title 55-60 caractères, description 150-160, mot-clé, mots-clés
     secondaires, slug).
- Résultats déclarés par l'utilisateur : « très bons ». C'est la
  référence de qualité de l'éval à l'aveugle du Skill de rédaction.

Ce qui manque au workflow et que les dépôts apportent : contrôle
automatique des tics et de la typographie, vérification des affirmations
sans source, réserve de preuves de l'utilisateur (interview), choix du
type de page vérifié contre la SERP (SXO), bloc méta mesuré en pixels,
réutilisation d'un contexte persistant au lieu de 6 questions à chaque
article.

## Guide Google « Créer des contenus utiles, fiables et people-first »

PDF fourni (5 pages, version française créée le 11 févr. 2026, texte
identique à la page Search Central). Points utilisables tels quels comme
**grille de jugement** (pas de note numérique inventée) :

- Questions sur le contenu et la qualité (originalité, description
  substantielle, valeur ajoutée sur les sources, titre qui résume, fautes,
  soin, production à la chaîne), sur l'expertise (sources citées, preuve
  d'expertise, auteur, erreurs factuelles vérifiables).
- Questions people-first et **signaux de contenu pour les moteurs** :
  viser un nombre de mots (« ce qui n'est pas le cas »), entrer dans une
  niche sans compétence, répondre à une question sans réponse confirmée,
  **changer la date sans changement significatif**, ajouter ou supprimer
  en masse pour paraître « actuel » (« cette technique ne fonctionne
  pas »).
- E-E-A-T : la fiabilité est primordiale ; pas un facteur de classement
  en soi ; plus de poids pour le YMYL ; les évaluateurs n'agissent pas sur
  le classement.
- **Qui, Comment, Pourquoi** : signature et page auteur ; dire comment le
  contenu a été produit, y compris l'usage de l'IA quand le lecteur peut
  se le demander ; « pourquoi » = aider les gens ; l'automatisation pour
  manipuler le classement est du spam.

Conséquences pour le pack : aucun nombre de mots imposé (le 1 000-1 500 de
l'utilisateur devient **sa préférence par défaut**, modifiable dans le
contexte) ; `lastmod` et « mis à jour le » seulement après un vrai
changement ; mention de l'usage de l'IA proposée en option là où le lecteur
peut la chercher.

## Marketer Milk « SEO trends 2026 »

Déjà disséqué dans `recherche/seo-v2-tendances-marketermilk-2026.md`
(8 tendances, chacune en option avec son Skill d'accueil, chiffres et cas
marqués [à vérifier]). Rien à ajouter, sauf le croisement avec les dépôts :
seomachine impose déjà la vidéo YouTube intégrée (on la garde en
option) ; marketingskills apporte la méthode « couche texte » pour YouTube.

## Les deux comparatifs d'audit fournis (2 oct. 2026)

- Notre `seo-audit` v1 : ordre d'analyse, script on-page 15 points,
  sortie par gravité, « à mesurer » au lieu d'inventer, pas de note globale
  inventée.
- `seo-audit` de claude-seo : jusqu'à 500 pages, 15 agents, note sur 100
  pondérée, fichiers d'audit persistés, rapport PDF, corrélation avec les
  mises à jour Google, gestion du budget des agents.
- Lecture : notre v1 est plus sobre et plus honnête, claude-seo est bien
  plus profond (exploration, rendu JS, robots IA, données Google réelles,
  registre des mises à jour). La v2 doit garder la sobriété et prendre la
  profondeur mesurée.
