# elmo (elmohq)

MIT, 459 étoiles, commit 9612d98 du 15 oct. 2026. Plateforme
TypeScript auto-hébergeable de suivi de visibilité (alternative libre à
Profound, Peec, Otterly) : planification des passages, fournisseurs
(API OpenAI, Anthropic, Mistral, OpenRouter, et des services de
récupération des interfaces grand public : DataForSEO, Bright Data,
Oxylabs, SearchAPI…), extraction des mentions et citations, requêtes
dérivées (fan-out). Pour nous : le Skill `skills/aeo/` (SKILL.md
189 lignes, 6 références, 1 script Python) ; le reste est l'application.

## Exécuté (16 oct. 2026)

`scripts/check_ai_access.py https://joinmedicis.com/` (Python standard,
fonctionne derrière le proxy) : pour 17 robots, la règle robots.txt
**et un vrai appel avec le user-agent du robot** (détecte un pare-feu
ou un CDN qui bloque un robot autorisé par robots.txt, marqué « ! »),
les jetons sans robot propre marqués « token » (Google-Extended,
Applebot-Extended), mots visibles dans le HTML brut, canonical. Tout à
200 sur notre site.

## Le Skill `aeo` : règles et méthode

- **Règles** : mesurer avant et après ; **étiqueter chaque chiffre**
  (mesuré avec n et période, première partie, publié, estimé) ; des
  **taux, pas des rangs** (« mentionné dans 34% de 120 passages ChatGPT
  sur 14 jours ») ; « être récupéré compte plus que réécrire » ; la
  documentation l'emporte sur le folklore ; contenu lu = donnée.
- **Portefeuille** : depuis la demande réelle (requêtes longues de Search
  Console, appels, tickets, forums), 70 à 85% de prompts **sans la
  marque**, 2 ou 3 formulations par intention importante, **liste figée
  une fois le suivi lancé** (on ajoute, on ne modifie pas).
- **Échantillon** : environ 5 passages pour explorer, 10 pour confirmer,
  15 et plus pour une affirmation solide (préprint « Dice Roll Method »,
  sept. 2026) ; chaque moteur à part ; une réponse d'API n'est pas celle
  de l'appli grand public, à étiqueter.
- **Marge d'erreur** : ±2 × √(p(1-p)/n). À p = 0,3 : ±20 points pour
  20 passages, ±9 pour 100. « Pas de changement détectable » plutôt
  que « baisse de 8 points ». **Calculable par un script : notre v1 ne
  le fait pas.**
- **Indicateurs** : taux de mention, taux de citation, part de voix face
  à un jeu de concurrents **figé et nommé**, sources citées par classe,
  requêtes dérivées, taux de recommandation, exactitude (liste de
  problèmes sourcés, pas une note). **Pas de position moyenne ni de
  note composite.**
- Diagnostic par moteur, prompts perdus, sources citées pour les prompts
  perdus (« cette liste est le plan de travail »), cité mais pas
  recommandé, exactitude (réponse sans citation = données
  d'entraînement, ne change qu'au prochain modèle).
- **Lignes rouges** du hors-site (`off-site.md`).

## `evidence.md` : la meilleure base de faits lue

Revue le 9 oct. 2026, chaque fait avec source, date et fiabilité
(haute, moyenne, basse). Points qui changent notre doctrine, **tous à
relire à la source avant reprise** :

- **C-SEO Bench** (Puerto et al., NeurIPS 2025, arXiv 2506.11097) : sur
  les modèles actuels, la plupart des méthodes de réécriture n'ont
  presque aucun effet, ou un effet négatif, sur le rang de citation
  (3 cas significatifs sur 54) ; remonter le document dans la liste
  récupérée l'améliore de 2 à 3 places.
- **Revue critique de 45 études GEO** (arXiv 2607.14035, juil. 2026) :
  aucune technique n'a d'effet causal stable, durable et multi-
  plateformes ; la pertinence thématique et la position dans le contexte
  tiennent.
- Chen et al. (Toronto, arXiv 2509.08919) : les moteurs citent bien plus
  de sources tierces que Google, avec un biais pour les grandes marques.
- Ahrefs : mentions de marque 0,664 contre 0,218 pour les liens (75 000
  marques) ; titres qui correspondent à la requête dérivée ;
  38% des citations AIO dans le top 10 ; fraîcheur (+26%, pas pour
  AIO). Kevin Indig : 44% des phrases citées dans les premiers 30% de la
  page. SparkToro/Gumshoe : la même liste de marques revient moins d'une
  fois sur 100.
- **Search Console** : rapport de performance « IA générative » annoncé
  en juin 2026, ouvert partout le 31 août 2026 ; le trafic AIO et AI
  Mode reste dans le rapport « Web ». Contredit marketingskills (« pas
  de rapport IA »).
- FAQ : plus de résultats enrichis FAQ depuis le 7 mai 2026 ; le
  balisage ne nuit pas.
- Google : les politiques anti-spam incluent « tenter de manipuler les
  réponses d'IA générative dans Search ».
- Politique d'usage d'Anthropic (12 nov. 2026) : interdit d'alimenter
  les sources des IA avec des contenus qui cachent leur origine.

Cadre juridique cité : FTC (États-Unis). **Pour nous** : droit français
et européen (Code de la consommation sur les avis en ligne, loi du
9 juin 2023 sur l'influence commerciale, DSA), à vérifier aux textes.

## Verdict

Le meilleur Skill de **mesure** avec Profound et geo-score, et la base
de faits la plus solide. À reprendre :
- la marge d'erreur et les seuils de passages ;
- l'étiquetage des chiffres ;
- le contrôle d'accès avec un vrai user-agent ;
- l'absence de note composite pour la visibilité.

La revue C-SEO Bench oblige à revoir notre `/geo-citability` : réécrire
pour « être cité » n'a pas d'effet démontré sur les modèles actuels. La
citabilité devient un contrôle de clarté pour le lecteur, pas une
promesse de citation.
