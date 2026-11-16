# Exports Search Console

Dépose ici un export Search Console si tu n'utilises pas le connecteur.

Il faut un export qui **croise requête et page** : l'export de l'interface de
Search Console ne le fait pas. Trois façons de l'obtenir :

- Looker Studio : tableau avec les dimensions « Requête » et « Page de
  destination », puis export CSV ;
- le module « Search Analytics for Sheets » de Google Sheets, regroupé par
  requête et page, puis Fichier → Télécharger → CSV ;
- l'API Search Console.

Colonnes reconnues, en français ou en anglais : requête, page, clics,
impressions, position. 3 derniers mois complets de préférence.

Ce dossier va dans ton dépôt **privé** : ne le copie jamais dans un dépôt
public, ses données sont celles de ton site.
