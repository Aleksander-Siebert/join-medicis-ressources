# superseo-skills (InhouseSEO) · dissection

Apache 2.0 (NOTICE à conserver si l'on copie ; nous réécrivons). Dernier
commit le 3 sept. 2026. 11 Skills, **aucun script**, 16 313 lignes de
Markdown : 23 modèles de types de contenu, 16 modules de technique
d'écriture, 9 fiches de tactiques de liens. CHANGELOG court mais
instructif.

Skills : `page-audit`, `content-brief`, `write-content`,
`improve-content`, `expert-interview`, `keyword-deep-dive`,
`semantic-gap-analysis`, `topic-cluster-planning`,
`featured-snippet-optimizer`, `eeat-audit`, `linkbuilding`.

## Ce que le CHANGELOG apprend

- 0.2.1 (3 sept. 2026) : **règles d'ancrage ajoutées à chaque Skill** :
  une affirmation vient d'une page réellement lue ou d'une donnée de
  l'utilisateur, jamais déduite quand une récupération échoue ; les
  précisions d'un article (chiffres, noms, citations) viennent de la
  recherche, de l'interview ou du contexte. Même problème que claude-seo :
  les Skills de rédaction inventent tant qu'on ne l'interdit pas
  explicitement.
- « Échappatoires pour l'exécution autonome » : si l'utilisateur veut tout
  d'un coup ou n'est pas là, le Skill avance avec des hypothèses écrites
  au lieu de bloquer. Bonne règle, à reprendre.
- FAQPage « toujours recommandé pour les citations IA » : contraire à la
  position de Google (pas de balisage spécial pour l'IA). À écarter.

## `write-content` (le plus proche du flux de l'utilisateur)

- **Contexte d'entreprise persistant** : 5 questions au premier usage
  (activité et public, ton, langue, sujets interdits, 2-3 concurrents),
  sauvegarde dans un fichier dont l'emplacement est **confirmé avec
  l'utilisateur** (jamais dans son `CLAUDE.md` sans accord). À reprendre.
- 4 phases : recherche (top 5), **choix du type de contenu annoncé et
  confirmé** (« les premiers résultats sont tous des X, j'écris un X avec
  Y, ça te va ? »), **extraction de savoir** (2-3 questions, une à la
  fois), rédaction.
- **Pas de nombre de mots cible** : la profondeur suit la SERP et
  l'intention.
- **« Une précision inventée est pire qu'une phrase générique »** : pas de
  réelle disponible, on demande ou on coupe. C'est notre règle zéro
  invention, formulée pour la rédaction.
- **Règle des 30%** : au moins 30% de l'article doit contenir ce qu'aucune
  IA générique ne produirait (données, exemples, avis de l'utilisateur).
- Test « Et alors ? » par section ; contrôle final des mots interdits.
- Règles de structure par type (comment faire : réponse courte puis étapes
  avec « ce qui coince » ; comparatif : verdict d'abord ; définition :
  « X est… » en première phrase ; étude de cas : chiffre du résultat
  d'abord, PAS).
- Faiblesses : liste anti-IA anglaise ; interdiction mécanique des triades
  (« utilise 2 ou 4 ») ; densité « ~2% » ; scénarios « montrer plutôt que
  dire » qui affirment des choses invérifiables (« Google a mesuré chaque
  milliseconde ») ; références « navboost » et temps de séjour.

## `expert-interview` (rejoint notre `/linkedin-interview`)

- 4 questions noyau : ce que les gens comprennent mal, un exemple précis
  (client, projet, chiffre), ce qui a surpris, **à qui ce conseil ne
  s'applique pas**. Variantes par type (technique, comparatif, prise de
  position, étude de cas). Relances : « que s'est-il passé exactement ? »,
  « peux-tu mettre un chiffre ? ».
- Sortie : document de savoir (prise de position, exemples et chiffres,
  expérience, périmètre et limites) transmis à la rédaction.
- Notre `/linkedin-interview` et sa réserve de preuves font déjà ce
  travail : **le pack SEO doit lire la même réserve** (un seul endroit
  pour les preuves de l'utilisateur, LinkedIn et SEO).

## `topic-cluster-planning`

- Hub + 8-15 rayons tirés **seulement** des PAA et recherches associées
  réellement vus (« ne pas gonfler la liste avec des requêtes inventées »).
- **Ordre de publication** : 3-4 rayons d'abord, puis le hub qui les relie,
  puis le reste (le hub ne naît pas orphelin). Décision argumentée dans
  `publishing-sequence-decisions.md`.
- `first-link-weight-evidence.md` : **modèle de référence honnête** :
  l'origine de la « priorité au premier lien » (Fishkin 2008, Cutts 2014
  « peut-être plus vrai », Mueller « non défini », Shepard 2023 « priorité
  sélective »), ce qui tient (lien contextuel dans le corps > pied de page,
  tests SearchPilot) et la règle pratique qui reste vraie même si le mythe
  est faux. **Le SKILL.md, lui, affirme le mythe** (« le premier lien est
  ce que l'algorithme pèse le plus ») : décalage entre le Skill et sa
  propre référence.
- Indicateurs à 3, 6, 9, 12 mois présentés comme des repères
  (« top 50 à 3 mois ») sans source : à écarter ou marquer.

## `page-audit`

- Rôle : « pas ce que disent les documents officiels de Google » : posture
  contraire à la nôtre (Google d'abord, contradictions écrites).
- Utile : **identité du contenu** avant toute note (ce que la page cherche
  vraiment, type, étape du parcours, intention, décalage entre ce qu'elle
  dit faire et ce qu'elle est construite pour faire) ; top 3 lus en entier
  (« ne jamais déduire ce que couvre une page non récupérée ») ;
  **temps jusqu'à la valeur** (mots avant la première information utile,
  mesurable) ; **toutes les fautes avec leur emplacement exact**.
- Fragile : « Information Gain = facteur n°1 » (un brevet n'est pas une
  preuve d'usage) ; hiérarchie on-page tirée d'un outil commercial ;
  « méta sous 140 caractères » (quatrième jeu de chiffres) ; triplets
  entité-attribut-valeur et « graphe sémantique de BERT/MUM » présentés
  comme mécanisme connu.

## `keyword-deep-dive`

- **Difficulté lue dans la SERP**, pas dans un score d'outil (« les KD des
  outils divergent de 30 points ») : grille de 10 signaux (Wikipedia ou
  site public, éditeurs connus, longueur des 5 premiers, extrait optimisé
  tenu par une marque, AI Overview, auteurs identifiés, données
  originales, fraîcheur entretenue, site de niche dans le top 3, méta
  soignées) → facile / moyen / difficile, avec la mention « directionnel ».
  **Signaux « ne pas tenter »** (Wikipedia en top 3, Reddit domine, site
  officiel sur une question réglementaire, actualité chaude, pages
  produits de marques sur une requête générique). Utile en **mode
  gratuit** sans outil payant ; à adapter au français (Wikipédia,
  service-public.fr, sites des ordres et autorités).
- `ctr-benchmarks-by-position.md` : chaque chiffre sourcé et daté (First
  Page Sage 2026, Ahrefs déc. 2025 « -58% avec AI Overview », Seer sept.
  2025, AWR T3 2025), avec les cas où la table ne s'applique pas (marque,
  transactionnel, longue traîne). Une erreur de raisonnement : les CTR y
  sont présentés comme une part des clics plutôt que des impressions
  **[à vérifier dans la méthode First Page Sage]**. Chez nous : **le CTR
  attendu se calcule sur les données Search Console du site**, la table
  externe ne sert qu'en l'absence de données, avec sa source.

## `eeat-audit`

- Grille sur 40 et **grille YMYL** (santé ou sécurité, sécurité financière,
  vie civique) : expertise relevée de 10 à 12 et confiance de 8 à 10 ;
  « une seule erreur factuelle fait passer sous le seuil de
  publication » ; diplômes **vérifiables par un lien externe**
  (« Dr X sans lien est pire que pas de bio ») ; sources liées et pas
  seulement nommées ; avertissement obligatoire ; conflit d'intérêts
  visible.
- Ce que nous ajoutons pour la France : les registres vérifiables
  (ORIAS pour les intermédiaires en assurance, annuaires des ordres de
  santé, annuaire du barreau, registres de l'AMF) **[à vérifier : liens et
  intitulés exacts]**. Très pertinent pour l'exemple Assurly et pour le
  YMYL du flux de l'utilisateur.
- Modèles par type de page sensible (avis produit, études de cas, prise de
  position, pages services, tarifs, « à propos »).

## `featured-snippet-optimizer`, `semantic-gap-analysis`, `improve-content`, `content-brief`, `linkbuilding`

- Extrait optimisé : diagnostic de l'écart (mauvais format, réponse trop
  longue ou trop courte, enfouie, pas autonome, pas sous un titre qui
  reprend la question) puis bloc de réponse. Repères 40-60 mots, 3-8
  éléments de liste : pratiques courantes, non officielles.
- Écart sémantique : entités, prédicats (verbes du métier), classement des
  écarts. Utile en idée (le vocabulaire d'expert manquant), fragile en
  théorie.
- `improve-content` : même règles que la rédaction, interview de mise à
  jour, notation de qualité avant livraison.
- Liens : arbre de classement par phase du site, sécurité des ancres,
  signaux d'alerte de vitesse d'acquisition. Hors périmètre demandé, sauf
  la partie « citations et annuaires » pour le local.

## Verdict

Meilleure source sur **la méthode de rédaction humaine** (contexte
persistant, type confirmé, interview courte, 30% de première main, pas
d'invention, pas de nombre de mots) et sur **l'honnêteté des références**
(premier lien, CTR, difficulté). Plus faible sur les faits Google (FAQ,
posture « contre la doc officielle ») et sans aucune mesure automatisée.
