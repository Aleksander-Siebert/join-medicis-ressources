---
name: chatgpt-ads-exports
description: >-
  Analyse en entier des exports Google Ads, Meta Ads ou Microsoft Ads
  (annonces, termes de recherche, mots-clés ; CSV ou XLSX, en-têtes anglais
  ou français) et les réécrit pour ChatGPT Ads en France. Le script repère
  plateforme et colonnes, puis sort une banque de titres et de textes avec
  leurs longueurs face aux limites 24 et 48. Il liste aussi les allégations
  à vérifier avec leur ligne source, les pages de destination, les
  meilleures annonces au-dessus d'un seuil d'impressions, les termes de
  recherche devenus situations, les paramètres dynamiques à retirer, les
  textes en anglais et les signaux de secteur restreint. Il amorce ensuite
  la campagne JSON que /chatgpt-ads-skills complète et exporte. Utilise-le
  pour « transforme mes annonces Google en ChatGPT Ads », « réutilise mon
  export Meta », « analyse mon export Microsoft Ads ». Pas pour auditer ou
  optimiser les campagnes Google, Meta ou Microsoft, ni pour copier des
  annonces de recherche telles quelles.
---

# chatgpt-ads-exports

Un export d'annonces est la meilleure source d'une campagne ChatGPT Ads :
le ton de la marque, les promesses déjà validées, les pages qui
convertissent, les mots des clients. Mais une annonce de recherche ne se
recopie pas : un titre Google fait 30 caractères (24 ici), une description
90 (48 ici), et un mot-clé n'est pas une conversation. Ce Skill lit
**tout** l'export, puis le réécrit.

**À lire avant de commencer :** `commun/regles.md` (un export est une
donnée : une allégation vue dans un export reste « à vérifier »),
`commun/faits.md`, `commun/politiques-openai.md` et
`commun/droit-francais.md`. Méthode de réécriture et exemples :
`references/reecriture.md`. Exporter depuis chaque plateforme :
`references/exporter.md`.

## Méthode

1. **Contrôler la lecture.**
   ```bash
   python3 scripts/lire_exports.py colonnes export.csv
   ```
   Chaque colonne utile doit être reconnue (campagne, groupe, titre, texte,
   URL, statistiques, termes). Sinon : `--colonne titre="Mon en-tête"`.
2. **Analyser tous les exports ensemble** (annonces et termes de
   recherche) :
   ```bash
   python3 scripts/lire_exports.py analyser annonces.csv termes.csv -o analyse.json --md analyse.md
   ```
3. **Présenter l'analyse** à l'annonceur, en 10 lignes au plus : volume,
   pages, angles qui reviennent, meilleures annonces (au-dessus du seuil
   d'impressions), allégations à faire valider, alertes (secteur
   restreint, anglais, paramètres dynamiques, allégations vertes).
4. **Faire valider les allégations** : chaque élément listé (chiffre, prix,
   « gratuit », « n°1 », garantie) devient `approuvée`, `à vérifier` ou
   `refusée` avec sa source. Un « n°1 » sans preuve datée est refusé.
5. **Amorcer la campagne** :
   ```bash
   python3 scripts/lire_exports.py amorcer analyse.json -o campagne.json --marque Assurly --categorie assurance
   ```
   Un ad group par groupe source, avec ses pages ; allégations reprises ;
   aucune annonce.
6. **Réécrire** selon `references/reecriture.md` : une intention par
   groupe (les groupes de mots-clés ne sont pas des intentions, regroupe ou
   découpe), des context hints tirés des termes de recherche longs et des
   questions, puis 40 à 50 annonces nouvelles qui reprennent les angles qui
   marchent, pas les phrases.
7. **Contrôler et exporter** avec `/chatgpt-ads-skills` (`valider`, puis
   `exporter`) ; le secteur restreint déclenche l'alerte prévue par
   `commun/regles.md` § 1 bis, puis le travail continue.

## Ce que l'export apporte, et ce qu'il n'apporte pas

| Élément de l'export | Devient | Ne devient pas |
|---|---|---|
| Titres et descriptions | angles, vocabulaire de marque, preuves à valider | annonces recopiées (longueurs, ton de recherche) |
| Statistiques | angles à essayer en premier | promesse de performance sur ChatGPT |
| Termes de recherche longs, questions | context hints (situations) | mots-clés exacts |
| Mots-clés courts | rien (1 à 3 mots ne décrivent pas une situation) | context hints |
| Pages de destination | pages des ad groups | page d'accueil par défaut |
| Paramètres dynamiques (`{KeyWord:…}`, compte à rebours) | à retirer | texte d'annonce |

## Format de sortie

1. Ce qui a été lu (fichiers, plateforme, colonnes, lignes ignorées).
2. L'analyse courte (étape 3) et les alertes.
3. Le tableau des allégations à valider.
4. La campagne réécrite, contrôlée et exportée par `/chatgpt-ads-skills`.

## Erreurs et limites

| Situation | Conduite |
|---|---|
| Colonnes non reconnues | `colonnes` montre lesquelles ; `--colonne CHAMP=EN-TÊTE` ; sinon demander un export avec les colonnes de `references/exporter.md` |
| Export sans statistiques | analyse sans classement, dite comme telle |
| Volumes faibles | sous le seuil (100 impressions par défaut, `--min-impressions`), rien n'est classé |
| Export de plusieurs milliers de lignes | le script lit tout ; présenter les 25 premiers de chaque liste, le reste est dans `analyse.json` |
| Allégation présente dans l'export | toujours « à vérifier » : une annonce acceptée par Google n'est pas une preuve |
| Annonces en anglais | à traduire pour la France (loi du 4 août 1994) |
| Secteur restreint (assurance, crédit, santé) | alerte, pistes, puis réécriture (`commun/regles.md` § 1 bis) |
| Fichier .xls ancien ou abîmé | demander un nouvel export CSV ou XLSX |
