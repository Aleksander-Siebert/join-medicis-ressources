# Avant de dépenser : prudence, réglages hors fichier, relecture

Le Skill prépare un fichier ; l'argent se dépense dans Ads Manager. Cette
page dit quoi vérifier entre les deux. Les seuls repères chiffrés sont ceux
qu'OpenAI publie ; le reste se décide avec les données de l'annonceur.

## 1. Avant de dépenser

À reprendre dans la réponse, adapté à la campagne :

1. **Éligibilité confirmée.** Catégorie et pays vérifiés
   (`references/politiques.md`), règles publicitaires relues à la date du
   lancement.
2. **Commencer petit.** Un budget de test que l'annonceur accepte de perdre
   pour apprendre, sur quelques groupes, avant d'élargir.
3. **Budget quotidien plutôt que total.** Le modèle d'import le conseille
   (le budget total n'a pas encore de lissage), les stratégies « Maximize
   Results » l'exigent, et un budget total ne se rebascule pas en quotidien
   (`commun/faits.md` § 2). Le script signale un budget `Lifetime`.
4. **Plafonner l'enchère** (`max_bid`) sur chaque groupe. Au clic, OpenAI
   conseille de commencer entre 3 et 5 USD, à convertir dans la devise du
   compte ; en conversion, c'est un coût par conversion visé, facturé au
   clic. Ads Manager signale une enchère trop faible, pas dans les 24 heures
   qui suivent une modification.
5. **Un groupe, une intention.** C'est ce qui permet de lire les résultats :
   un groupe qui mélange deux intentions ne dit rien sur aucune.
6. **Mesurer avant d'augmenter.** Pixel, API Conversions (plus fiable que le
   pixel seul) ou balise image, testés : une conversion de test remonte dans
   les événements récents. Pour une campagne `Conversions`, un seul
   événement standard, choisi pour de bon (il ne change plus après
   création) : `order_created` pour un achat, `lead_created` pour une
   demande de contact, `appointment_scheduled` pour une démonstration,
   `trial_started` pour un essai.
7. **Laisser tourner avant de juger.** La dépense peut s'afficher avec 7 à
   8 heures de retard ; pas de conclusion sur quelques dizaines
   d'affichages ; le seuil se fixe avec l'annonceur
   **{{à compléter : seuil de décision}}**. Un réglage changé à la fois.
8. **Pays ouverts.** Un code ISO valide n'est pas forcément ouvert à la
   publicité pour le compte : vérifier dans Ads Manager.
9. **Tester l'import.** Importer d'abord un petit fichier (une campagne en
   pause, un groupe, une annonce) pour vérifier qu'Ads Manager accepte le
   modèle utilisé.

## 2. Ce que le fichier d'import ne règle pas

À régler dans Ads Manager, si le compte y a accès :

- zones plus fines que le pays (identifiants de lieux) et exclusions de
  zones ;
- plateformes : application iOS, application Android, web ;
- audiences personnalisées (25 000 personnes reconnues au moins pour une
  inclusion) et multiplicateurs d'enchère ;
- stratégie « Maximize Results » (sans enchère maximale) ;
- hints d'exclusion et « Negative Phrases » ;
- paramètres de suivi au niveau du compte ou de la campagne.

Le Skill les mentionne quand ils servent la campagne, il ne les invente
pas.

## 3. Secteurs sensibles

Voir `references/politiques.md` : santé, finance, assurance et juridique
sont réservés aux États-Unis, au cas par cas, et généralement interdits
ailleurs ; d'autres catégories sont interdites partout. Même admis, un
secteur réglementé garde ses règles nationales (en France : assurance,
crédit, santé, jeux) en plus de celles de la plateforme ; le Skill ne
remplace pas la relecture par la conformité de l'annonceur.

## 4. Checklist de relecture humaine

À cocher par une personne qualifiée de l'équipe de l'annonceur, avant
import :

- [ ] Catégorie et pays éligibles, règles publicitaires relues le
      {{à compléter : date}}.
- [ ] Chaque annonce relue en entier, à voix haute.
- [ ] Chaque allégation retrouvée sur sa page source, avec ses conditions.
- [ ] Aucune annonce qui imite ChatGPT ou suggère une affiliation.
- [ ] Chaque lien ouvert : bonne page, pas d'erreur, accessible sans
      connexion, UTM corrects.
- [ ] Chaque image ouverte : carrée, entre 640 et 1 200 pixels de côté, PNG
      ou JPG, lisible en petit, droits d'usage acquis.
- [ ] Chaque groupe : les hints décrivent bien l'intention, aucun ne vise
      une conversation sensible ni une zone géographique.
- [ ] Noms de campagne et d'ad groups identiques dans les 3 onglets.
- [ ] Budget, type de budget, dates, objectif, pays, enchères maximales
      conformes à la décision de l'annonceur.
- [ ] Mesure des conversions testée (campagne `Conversions` ou hausse de
      budget prévue), événement standard choisi.
- [ ] Import d'essai réussi dans Ads Manager.
- [ ] Le rapport du script est à 0 bloquant, et chaque point « attention »
      gardé a une raison.
