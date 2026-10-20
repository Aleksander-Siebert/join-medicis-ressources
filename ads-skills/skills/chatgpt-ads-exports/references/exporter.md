# Exporter ses annonces depuis Google Ads, Meta Ads et Microsoft Ads

Les libellés des menus changent souvent : ces chemins sont des repères
**[à vérifier dans l'interface du jour]**. Ce qui compte, ce sont les
colonnes.

## Colonnes à inclure

| Plateforme | Annonces | Statistiques (si possible) | Termes |
|---|---|---|---|
| Google Ads | campagne, groupe d'annonces, état, titres 1 à 15, descriptions 1 à 4, URL finale, chemins | impressions, clics, conversions, coût | rapport des termes de recherche : terme, groupe, clics, conversions |
| Meta Ads | campagne, ensemble de publicités, nom de la publicité, titre, texte principal, description du lien, URL du site web, statut | impressions, clics sur un lien, résultats | sans objet |
| Microsoft Ads | fichier en masse ou rapport d'annonces : type, statut, campagne, groupe, titres, textes, URL finale | impressions, clics, conversions | rapport des termes de recherche |

Exporter les annonces **actives** et celles qui ont bien marché
récemment ; les annonces refusées ou expirées seulement si elles sont
marquées comme contre-exemples.

## Repères par plateforme

- **Google Ads** : Campagnes > Annonces > icône de téléchargement, format
  CSV ou Excel **[à vérifier]** ; Google Ads Editor exporte aussi un CSV
  (souvent en UTF-16 avec tabulations : le script le lit).
- **Meta Ads Manager** : sélectionner les publicités > Exporter > Excel ou
  CSV **[à vérifier]**.
- **Microsoft Advertising** : Outils > Importations et exportations en
  masse, ou Rapports > Annonces **[à vérifier]** ; les lignes de structure
  (version de format, campagne, groupe) sont ignorées.

## Avant de partager un export

- Retirer ce qui est personnel ou confidentiel (noms de clients, adresses
  e-mail dans les audiences, coûts si l'annonceur ne veut pas les
  partager) : l'analyse n'en a pas besoin.
- Garder les en-têtes d'origine : le script reconnaît l'anglais et le
  français.
