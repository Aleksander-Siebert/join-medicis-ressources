# localseoskills (Garrett Smith, GMB Gorilla) · dissection

MIT. Dernier commit le 15 août 2026. 39 Skills (8 708 lignes), dont
14 Skills « outil » (connecteurs payants : LocalSEOData, Local Falcon,
BrightLocal, Whitespark, DataForSEO, SerpApi, Semrush, Ahrefs, Screaming
Frog, Search Console, GA4), 15 tâches récurrentes (`tasks/` : brouillons
de posts de fiche, réponses aux avis, audit de citations, suivi des
classements et de la vitesse des avis, rapports hebdo et mensuels), des
spécifications de sortie et d'approbation, un glossaire, un document
« comment marche la recherche locale ». Aucun script de mesure : les
mesures viennent des connecteurs payants.

Lu : `local-seo-audit`, `review-management`, `local-landing-pages`,
`bing-places`, `apple-business-connect`, `ai-local-search` (extraits),
`docs/how-local-search-works.md`, `meta/lessons.md`,
`specs/approval-workflow.md`, structure des autres Skills. Les Skills
publicitaires (LSA, PPC) et d'agence (livrables clients, prospection) sont
hors périmètre.

## Ce qui vaut d'être repris

- **Ordre d'audit local** : fiche Google, signaux du site, citations et
  NAP, avis, liens locaux, contenu local, technique.
- **Fiches en double ou liées** (le meilleur passage) : chercher par nom,
  variantes, nom du praticien, **numéro de téléphone**, adresse, ancienne
  adresse ; cataloguer chaque fiche (avis, catégories, revendiquée ou non,
  relation) ; décider **fusionner / garder séparé / consolider** avec les
  cas (praticien qui exerce aussi seul, ancienne adresse, entité distincte
  au même endroit) ; procédure selon que la fiche est revendiquée ou non ;
  captures « avant » ; surveiller 3 mois (les agrégateurs recréent les
  doublons). « Google ne transfère pas les avis d'une fiche à l'autre »
  **[à vérifier]**.
- **Pages locales** : test « valeur propre par page », stratégie selon le
  volume (5-20 pages faites à la main, 20-100 gabarit + sections uniques
  obligatoires), liste des signes de page satellite.
- **Approbation en 3 niveaux** : autonome (rapports, alertes), file
  d'attente (posts de fiche, réponses aux avis, pages : brouillon, aperçu,
  destination, puis validation humaine), jamais automatique pour ce qui
  touche un client. Même logique que notre règle « rien n'est publié à ta
  place ».
- **`meta/lessons.md`** : l'agent propose une leçon quand il observe un
  écart avec les consignes, l'humain approuve, avec catégorie, confiance,
  portée et **date de revérification**. Même mécanique que notre
  `apprentissages.md` LinkedIn : à étendre au pack SEO.
- Les trois piliers locaux de Google (pertinence, distance, proéminence)
  expliqués avec leurs conséquences : la distance ne s'optimise pas, une
  zone de service déclarée plus grande ne rapproche pas l'entreprise.

## Ce qui est faux ou non sourcé

- « Les signaux sociaux sont désormais un facteur de classement confirmé et
  mesurable » : aucune source ; à écarter.
- « Les mots-clés dans le nom de l'entreprise pèsent » : observation de
  praticiens, et contraire aux règles de Google (nom réel uniquement).
  Notre Skill rappelle la règle et le risque de suspension.
- Horaires d'ouverture « 5e facteur du pack local », « âge de la fiche »,
  « Apple Plans tire ses avis de Yelp » (vrai aux États-Unis, à vérifier en
  France), « 300 mots uniques minimum par page locale » : à marquer ou
  écarter.
- Tout l'écosystème est américain : Yelp, BBB, Angi, LSA, HIPAA.

## Ce que nous ajoutons pour la France

- Écosystème : Google Business Profile, PagesJaunes (Solocal), Apple
  Business Connect, Bing Places, Waze, annuaires professionnels et
  sectoriels (Doctolib pour la santé, ordres professionnels, annuaires de
  CCI et de chambres de métiers) **[à vérifier : liste et pertinence par
  secteur]**.
- Avis en ligne : obligations d'information sur la vérification des avis
  (Code de la consommation), norme NF sur les avis **[à vérifier : textes
  et références exactes]**, interdiction des faux avis et des avis
  achetés, contrôle DGCCRF.
- Données personnelles : photos de clients et réponses aux avis sans
  donnée sensible (RGPD), secret professionnel pour la santé et le droit.
- Mode gratuit par défaut : recherches manuelles notées (requête, lieu,
  date, appareil) plutôt que géo-grille payante, comme le recommande
  marketingskills.

## Verdict

Source la plus complète sur **les opérations locales** (doublons, avis,
pages, approbation, leçons), mais américaine, dépendante d'outils payants
et peu sourcée sur les facteurs de classement. À combiner avec la rigueur
de marketingskills (`local-seo*.md`) et les contrôles de claude-seo
(NAP HTML / JSON-LD / fiche, sous-type schema, test du remplacement).
