---
name: chatgpt-ads-ids
description: >-
  Retrouve les identifiants ChatGPT Ads (OpenAI Ads) que demande le classeur
  d'import : ad_group_id, ad_id, image_file_id, campaign_id et
  conversion_event_setting_ids. Deux voies : l'API officielle d'OpenAI en
  lecture seule (clé du compte dans une variable d'environnement, jamais
  dans la conversation), ou un fichier exporté d'Ads Manager où les
  identifiants sont repérés par leur préfixe. Le script liste campagnes,
  ad groups et annonces, cherche par nom, puis reporte les identifiants
  dans le classeur ou le JSON de campagne en signalant les noms ambigus.
  Il donne aussi le modèle d'UTM avec les macros de campagne et d'annonce
  et, sur confirmation, téléverse une image pour obtenir son
  image_file_id. Utilise-le pour « où trouver l'ad_group_id », « ID des ad
  groups », « image_file_id », « remplir les identifiants du fichier
  d'import ». Pas pour créer, modifier, activer ou mettre en pause une
  campagne, ni pour rédiger des annonces (/chatgpt-ads-skills).
---

# chatgpt-ads-ids

Le classeur d'annonces relie chaque annonce à un ad group **qui existe
déjà** par son `ad_group_id`. Ce Skill retrouve ces identifiants sans les
recopier à la main un par un, et les reporte au bon endroit.

**À lire avant de commencer :** `commun/regles.md` (l'API ne sert qu'en
lecture ; la seule écriture possible, le téléversement d'une image, demande
l'accord de l'annonceur) et `commun/faits.md` § 1 (identifiants
documentés). Guide pas à pas, sans et avec API :
`references/trouver-les-ids.md`.

## Quel identifiant, pour quoi

| Identifiant | Préfixe (docs) | Sert à | Où le trouver |
|---|---|---|---|
| `ad_group_id` | `adgrp_` | relier une annonce du classeur à son ad group | API `lister`, export d'Ads Manager |
| `ad_id` | `ad_` | **modifier** une annonce existante (vide pour en créer une) | API `lister --annonces` |
| `image_file_id` | `file_` | réutiliser une image déjà téléversée | API `lister --annonces`, ou `televerser` |
| `campaign_id` | `cmpn_` | filtrer, suivre (UTM `{campaign_id}`) | API `lister` |
| `conversion_event_setting_ids` | `ces_` | campagne de conversion (un seul) | API `evenements`, onglet des conversions d'Ads Manager |

Les préfixes sont ceux des exemples de la documentation : un identifiant
réel peut différer, le script le signale sans bloquer.

## Méthode

1. **Choisir la voie.** L'annonceur a-t-il une clé d'API (Ads Manager >
   Settings) et un terminal ? Sinon, voie B (fichier) ou recopie guidée.
2. **Voie A, API en lecture.** L'annonceur définit la clé **lui-même**, dans
   son terminal : `export OPENAI_ADS_API_KEY=…`. Ne demande jamais la clé
   dans la conversation ; si elle y est collée, dis-lui de la révoquer et
   d'en créer une autre.
   ```bash
   python3 scripts/ids.py compte                         # bon compte ? devise ?
   python3 scripts/ids.py lister -o ids.csv              # campagnes et ad groups
   python3 scripts/ids.py lister --annonces -o ids.csv   # + annonces et image_file_id
   python3 scripts/ids.py chercher "expat-preparer"      # un ad group par son nom
   python3 scripts/ids.py evenements                     # ces_… pour la conversion
   ```
3. **Voie B, sans API.** Exporter depuis Ads Manager le tableau des ad
   groups ou des annonces avec ses identifiants, puis :
   ```bash
   python3 scripts/ids.py depuis-fichier export.csv -o ids.csv
   ```
4. **Reporter les identifiants** dans le classeur ou le JSON de campagne :
   ```bash
   python3 scripts/ids.py fusionner import.xlsx --ids ids.csv -o import-ids.xlsx
   python3 scripts/ids.py fusionner campagne.json --ids ids.csv -o campagne-ids.json
   ```
   La correspondance se fait par nom d'ad group (sans casse ni accents). Un
   nom porté par deux groupes n'est **pas** rempli : il est signalé.
   `--ad-id` reporte aussi les `ad_id` : chaque ligne **modifiera** alors
   l'annonce existante au lieu d'en créer une ; ne l'utilise que pour une
   mise à jour voulue.
5. **Contrôler** le résultat avec `/chatgpt-ads-excel`.

Autres commandes : `utm` (paramètres de suivi avec `{campaign_id}`,
`{ad_id}`, `{oppref}` : les identifiants arrivent aussi dans l'outil
d'analyse), `televerser IMAGE --confirmer` (écrit une image dans le compte,
rend son `image_file_id`, ne crée aucune annonce).

## Format de sortie

1. Le compte interrogé (nom, devise) ou le fichier lu.
2. Le tableau des identifiants trouvés (campagne, groupe, annonce).
3. Ce qui a été reporté, ce qui reste ambigu ou introuvable, et pourquoi.
4. Le fichier mis à jour, à contrôler avec `/chatgpt-ads-excel`.

## Erreurs et limites

| Situation | Conduite |
|---|---|
| Pas de terminal (claude.ai, ChatGPT) | voie B si l'annonceur peut exporter ; sinon recopie guidée de `references/trouver-les-ids.md`, puis contrôle du classeur |
| HTTP 401 | clé refusée : en recréer une dans Ads Manager > Settings |
| HTTP 403 | la clé appartient à un autre compte, ou la fonction n'est pas ouverte au compte |
| HTTP 429 | le script attend et réessaie 3 fois, puis s'arrête |
| Deux ad groups du même nom | rien n'est rempli : renommer un groupe dans Ads Manager ou choisir l'identifiant à la main |
| Ad group absent | il n'est pas encore créé : fiche de paramétrage de `/chatgpt-ads-skills` |
| Clé collée dans la conversation | la faire révoquer ; ne jamais la recopier dans un fichier ou un message |
