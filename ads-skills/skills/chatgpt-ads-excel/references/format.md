# Le classeur d'annonces, colonne par colonne

Format : le schéma d'annonces fourni le 20 oct. 2026 comme format
compatible avec l'import d'Ads Manager. Ce qui n'y est pas écrit est marqué
**[à vérifier]** et se confirme par un import d'essai.

## Structure

- **Un seul onglet.** L'exemplaire fourni le nomme `Feuil1` (nom par
  défaut d'un Excel français) ; aucun effet connu du nom sur l'import
  **[à vérifier]**.
- **Ligne 1 : les 10 en-têtes**, en minuscules, dans cet ordre :
  `ad_id`, `ad_group_id`, `adgroup_name`, `ad_name`, `status`, `title`,
  `copy`, `link`, `image_url`, `image_file_id`. Attention aux variantes :
  `adgroup_name` s'écrit sans tiret bas entre « ad » et « group », alors que
  `ad_group_id` en a un.
- **Lignes suivantes : une annonce par ligne**, sans ligne vide entre deux
  annonces, sans cellule fusionnée, sans formule, sans mise en forme
  particulière.
- Notes, sources, scores, numéros de lot : **jamais dans le classeur**. Un
  onglet de travail ou une colonne en plus peut faire échouer l'import.

## Colonnes

| Colonne | Obligatoire ? | Contrôle du script | Erreur fréquente |
|---|---|---|---|
| `ad_id` | non pour une création **[à vérifier]** | unique ; préfixe `ad_` attendu (documentation) | coller un identifiant d'annonce dans une ligne de création : l'import modifierait l'annonce existante |
| `ad_group_id` | probablement, pour relier l'annonce **[à vérifier]** | préfixe `adgrp_` ; un identifiant = un nom de groupe | identifiant tapé à la main, ou transformé en nombre par Excel |
| `adgroup_name` | à remplir pour la relecture | un nom = un identifiant | même groupe écrit de deux façons (« expat-01 » et « Expat-01 ») |
| `ad_name` | **[à vérifier]** | 3 à 1 000 caractères ; unique dans le groupe | laissé vide (`reparer` le remplit) |
| `status` | **[à vérifier]** | `active` ou `paused`, en minuscules | « Active », « Paused », « en pause » |
| `title` | oui | 3 à 24 caractères | dépassement d'un ou deux caractères à cause d'une espace typographique ou d'un « ’ » |
| `copy` | oui | 1 à 48 caractères | texte de 90 caractères repris d'une annonce Google |
| `link` | oui | http(s) complet, sans espace, 2 048 caractères au plus | adresse sans `https://`, page d'accueil au lieu de la page de l'offre |
| `image_url` | une des deux colonnes d'image | http(s), finit par .png, .jpg, .jpeg ou .webp | lien vers une page qui contient l'image, ou lien de partage Google Drive |
| `image_file_id` | une des deux colonnes d'image | préfixe `file_` | identifiant d'une image d'un autre compte |

## Comptage des caractères

- Le script compte les caractères affichés : une lettre accentuée vaut 1,
  une espace insécable vaut 1, un caractère invisible (espace de largeur
  nulle, trait d'union conditionnel) vaut 0 et est retiré par `reparer`.
- La typographie française ajoute des espaces avant `: ; ! ?` : elles
  comptent. « Pourquoi attendre ? » fait 19 caractères, espace insécable
  comprise.

## Excel abîme les identifiants

Un identifiant uniquement numérique collé dans une cellule « Standard »
devient un nombre : les zéros de tête disparaissent, et au-delà de
15 chiffres il s'affiche en `1,23E+15` et perd ses derniers chiffres.

- **Prévenir** : mettre les colonnes `ad_id`, `ad_group_id` et
  `image_file_id` au format Texte **avant** de coller.
- **Constater** : le script signale « enregistré comme nombre ».
- **Réparer** : recoller l'identifiant depuis sa source. `reparer` écrit
  tout en texte, mais ne peut pas retrouver des chiffres déjà perdus.

## Selon le tableur

| Tableur | Pour obtenir un .xlsx propre |
|---|---|
| Excel | Fichier → Enregistrer sous → « Classeur Excel (.xlsx) » |
| Google Sheets | Fichier → Télécharger → « Microsoft Excel (.xlsx) » ; les identifiants restent du texte si la colonne est en format « Texte brut » |
| Numbers | Fichier → Exporter vers → Excel |
| CSV | `verifier` lit le CSV (séparateur virgule, point-virgule ou tabulation) ; `reparer` écrit un .xlsx |

## Liste de contrôle manuel (sans script)

1. Un seul onglet, 10 en-têtes exacts dans l'ordre.
2. Pas de ligne vide, de cellule fusionnée, de formule ni d'italique.
3. Chaque titre ≤ 24, chaque copie ≤ 48 caractères (compter les espaces).
4. Chaque ligne a un lien https et une image (lien direct ou `file_…`).
5. `status` en minuscules : `paused` pour relire avant de lancer.
6. Même `adgroup_name` partout pour un même `ad_group_id`.
7. Identifiants en texte, recopiés de leur source.
8. Chaque lien et chaque image ouverts dans un navigateur.
