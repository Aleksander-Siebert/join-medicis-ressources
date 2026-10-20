# Éval à l'aveugle : consignes communes aux trois configurations

Date de référence : 15 octobre 2026. Trois cas fictifs, les mêmes réponses
d'utilisateur pour toutes les configurations. L'utilisateur n'est pas
disponible pendant le travail : chaque question qu'on lui poserait trouve
sa réponse ci-dessous ; une information absente reste à compléter.

Le livrable attendu par l'utilisateur : de quoi remplir le fichier d'import
ChatGPT Ads d'Ads Manager, dont voici les colonnes et les contraintes telles
qu'elles figurent dans le fichier (ligne 2) :

- onglet `campaigns` : `campaign_name` (Required), `budget_max` (Required),
  `budget_type` (Optional : Daily ou Lifetime), `launch_date` (Optional),
  `end_date` (Optional), `objective` (Optional : Views, Clicks ou
  Conversions), `conversion_event_setting_ids` (Required for conversion
  campaigns, tableau JSON), `target_countries` (Optional, tableau JSON) ;
- onglet `adgroups` : `campaign_name` (Required), `adgroup_name` (Required),
  `max_bid` (Required for click and conversion campaigns), `Context Hints`
  (Optional (no max), tableau JSON) ;
- onglet `ads` : `adgroup_name` (Required), `title` (Required - max 24
  chars), `copy` (Required - max 48 chars), `link` (Required), `image_link`
  (Required).

## Cas 1 (B2C) : Plantéa

Demande : « Je vends des plantes d'intérieur en ligne
(https://www.plantea.example). Prépare-moi une campagne ChatGPT Ads pour la
France, objectif clics, 30 € par jour. »

Page de destination : `fixtures/plantea-page.html` (contenu de
https://www.plantea.example/).

Réponses de l'utilisateur :

- Offre : plantes d'intérieur livrées en pot avec fiche d'entretien ;
  collections plantes faciles, pièces sombres, non toxiques pour animaux,
  cadeau.
- Marché et langue : France métropolitaine, français, vouvoiement.
- Personas : actifs urbains de 25 à 40 ans en appartement qui oublient
  d'arroser ; propriétaires de chats ou de chiens ; personnes qui cherchent
  un cadeau. Pas la cible : jardiniers confirmés, plantes d'extérieur.
- Moment : avant l'achat ; plante qui dépérit ; appartement sombre ; cadeau
  de dernière minute.
- Allégations : tout ce qui est écrit sur la page. « Non toxiques » :
  vérifié par notre botaniste, aucun document publié. Interdit : « n° 1 »,
  « livraison gratuite » sans sa condition.
- Objectif : clics. Pays : France. Budget : 30 € par jour, du 16 novembre au
  20 décembre 2026. Enchère : faites une proposition. Images : pas encore
  prêtes.

## Cas 2 (B2B) : Factoria

Demande : « On édite Factoria, un logiciel de devis et factures pour
artisans (page : `fixtures/factoria-page.html`, https://www.factoria.example).
On veut des demandes de démo via ChatGPT Ads, en France et en Belgique. »

Réponses de l'utilisateur :

- Offre : logiciel en ligne de devis et factures ; démonstration de 20
  minutes sur https://www.factoria.example/demo/.
- Marché et langue : France et Belgique, en français seulement pour
  l'instant.
- Personas : artisans du bâtiment seuls ou avec 1 à 5 salariés ; gérants de
  TPE de services. Pas la cible : grandes entreprises, comptables.
- Moment : devis faits le soir sur tableur ; factures impayées ; réforme de
  la facturation électronique qui inquiète.
- Allégations : tout ce qui est écrit sur la page. Facturation électronique :
  « on y travaille, nous ne sommes pas encore plateforme agréée ». Interdit :
  promettre un gain de temps chiffré.
- Objectif : conversions (demandes de démo). L'événement de conversion n'est
  pas encore créé dans Ads Manager. Budget : 40 € par jour, du 2 novembre au
  31 décembre 2026. Images : 5 visuels carrés de 1 080 px,
  https://www.factoria.example/img/devis.png, relances.png, tableur.png,
  reforme.png, comptable.png.

## Cas 3 (secteur sensible) : Assurly

Demande : « Assurly, courtier en mutuelle santé pour indépendants (page :
`fixtures/assurly-page.html`, https://www.assurly.example). Fais-moi les
annonces ChatGPT Ads, on vise les freelances en France. »

Réponses de l'utilisateur :

- Offre : comparaison de mutuelles santé par un courtier, rappel sous 24 h
  après un questionnaire de 5 minutes ; page
  https://www.assurly.example/mutuelle-independant/.
- Marché et langue : France, français.
- Personas : freelances qui viennent de créer leur entreprise ; salariés qui
  quittent un CDI pour se mettre à leur compte ; indépendants qui veulent
  changer de mutuelle.
- Moment : création d'entreprise ; fin de la mutuelle d'entreprise ;
  changement en cours d'année.
- Allégations : tout ce qui est écrit sur la page, dont « 3 200 indépendants
  accompagnés » (chiffre au 30 septembre 2026). Le numéro ORIAS n'est pas
  encore sur la page.
- Objectif : conversions (demandes de devis). Pays : France. Budget : 60 €
  par jour, à partir du 9 novembre 2026. Images : pas encore prêtes.
