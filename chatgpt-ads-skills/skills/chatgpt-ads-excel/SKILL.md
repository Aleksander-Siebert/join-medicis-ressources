---
name: chatgpt-ads-excel
description: >-
  Contrôle et répare le fichier d'import CSV ChatGPT Ads (OpenAI Ads) avant
  l'import dans Ads Manager, au format du schéma d'annonces en CSV :
  10 colonnes (ad_id, ad_group_id, adgroup_name, ad_name, status, title,
  copy, link, image_url, image_file_id). Le script vérifie séparateur et
  encodage, en-têtes, ordre des colonnes, formules, italique,
  identifiants enregistrés comme nombres, invisibles, statuts, longueurs
  (titre 24, copie 48), liens, images (en ligne : taille et format carré),
  doublons ; il liste les cases vides colonne par colonne. Il écrit ensuite
  un CSV propre, sans ajouter d'identifiant ni raccourcir un texte. Utilise-le pour
  « vérifie mon fichier ChatGPT Ads », « l'import Ads Manager échoue »,
  « nettoie le fichier d'import », « convertis en format d'import ». Pas pour
  rédiger des annonces (/chatgpt-ads-skills, /chatgpt-ads-bulk), ni pour
  trouver les identifiants (/chatgpt-ads-ids).
---

# chatgpt-ads-excel

Un import qui échoue fait perdre une demi-journée : une colonne renommée, un
identifiant transformé en `1,23E+15` par Excel, une ligne en italique copiée
d'un modèle, un titre de 26 caractères. Ce Skill contrôle le fichier d'import
**avant** l'import et en écrit une copie propre. Il ne rédige pas et ne
change jamais le sens d'une annonce.

**À lire avant de commencer :** `commun/regles.md` et `commun/faits.md` § 1
(le schéma, ce qui est documenté et ce qui reste à vérifier).

## Le format attendu

Un **CSV** (UTF-8 sans BOM, virgule), une ligne d'en-tête, une annonce par
ligne. Un XLSX à un onglet se lit aussi, et se convertit avec `reparer`.

Règles d'usage (retours du 20 oct. 2026) :

- `status` = `active` par défaut : l'import lance directement les annonces
  (après l'examen d'OpenAI) ;
- `ad_group_id`, `ad_id`, `image_file_id` : **jamais ajoutés** s'ils ne sont
  pas fournis, laissés vides ;
- une case vide (`adgroup_name`, `title`, `copy`, `link`, `image_url`) est
  listée avec ses lignes pour vérification ; le fichier s'écrit quand même.

| Colonne | Contenu | Règle du pack |
|---|---|---|
| `ad_id` | identifiant d'une annonce existante | vide pour une nouvelle annonce ; rempli = modification **[à vérifier]** |
| `ad_group_id` | identifiant de l'ad group existant | vide s'il n'est pas fourni ; /chatgpt-ads-ids pour le retrouver |
| `adgroup_name` | nom de l'ad group | le même pour un même `ad_group_id` |
| `ad_name` | nom de l'annonce | 3 caractères au moins, unique dans le groupe |
| `status` | `active` ou `paused` | `active` par défaut |
| `title` | titre | 24 caractères au plus (3 au moins) |
| `copy` | texte | 48 caractères au plus |
| `link` | page de destination | adresse https complète, UTM permis, 2 048 caractères au plus |
| `image_url` | lien direct vers l'image | PNG, JPG (WebP selon l'API), carrée, 640 × 640 au moins |
| `image_file_id` | identifiant d'une image déjà téléversée | seulement s'il est fourni ; sinon `image_url` |

Détails, erreurs fréquentes et corrections dans Excel, Google Sheets et
Numbers : `references/format.md`.

## Méthode

1. **Contrôle.**
   ```bash
   python3 scripts/classeur_ads.py verifier import.csv            # format et annonces
   python3 scripts/classeur_ads.py verifier import.csv --en-ligne # + liens et images ouverts
   ```
   Un XLSX se contrôle de la même façon. Sans exécution de code, applique à
   la main la liste de `references/format.md` et écris en tête « Contrôle
   manuel, non vérifié par script. »
2. **Lecture du rapport.** Commence par les cases vides (colonne et
   lignes) pour que l'utilisateur les vérifie. Regroupe les points par cause (« 12 titres trop
   longs », « identifiants abîmés par Excel »), pas ligne par ligne, et
   donne la correction pour chaque cause.
3. **Réparation automatique** de ce qui ne change pas le sens :
   ```bash
   python3 scripts/classeur_ads.py reparer import.xlsx -o import.csv
   ```
   Onglets en trop retirés, colonnes remises dans l'ordre, valeurs en
   texte, formules et italique retirés, espaces nettoyés, `status` vide →
   `active`, `ad_name` vide → `groupe-01` (numéro libre), doublons exacts
   retirés, CSV sans BOM à virgules. Aucun identifiant ajouté.
4. **Ce qui reste à une personne** : textes trop longs (propose une
   réécriture par ligne, avec sa longueur, sans changer l'allégation),
   identifiants manquants (/chatgpt-ads-ids), liens ou images en erreur,
   noms de groupe incohérents.
5. **Import d'essai** : recommande d'importer d'abord 2 ou 3 lignes, puis
   le reste. Ce qui n'est pas documenté (colonnes obligatoires, limites de
   ce format) se confirme ainsi.

Autres commandes : `schema -o vierge.csv` (fichier vierge au format),
`depuis-json campagne.json -o import.csv` (depuis le JSON des autres Skills
du pack), `tableau import.csv` (lignes à coller en A1).

## Limites : 24 et 48 par défaut

Le modèle d'import d'Ads Manager fixe 24 et 48 caractères ; l'API accepte
50 et 100. Le schéma ne dit pas lesquelles s'appliquent : le pack écrit pour
la plus stricte, qui passe partout. `--limites api` applique 50 et 100 si
l'annonceur a constaté que son import les accepte ; dis-le dans le rapport.

## Format de sortie

1. Verdict en une phrase : bloquant, importable après relecture, ou
   conforme.
2. Les points regroupés par cause, avec la correction.
3. Le fichier d'import réparé (ou les lignes à coller) et la liste de ce qui reste
   à corriger à la main.
4. « À vérifier » : ce que seul un import d'essai confirme.

## Erreurs et limites

| Situation | Conduite |
|---|---|
| Fichier .xls, .numbers ou Google Sheets | demander un export .xlsx ou .csv |
| Fichier illisible (ZIP abîmé, mot de passe) | le dire, demander un nouvel export |
| Colonnes de l'ancien modèle à 3 onglets (campaigns, adgroups, ads) | expliquer la différence ; reconstruire au schéma avec /chatgpt-ads-skills (`exporter`) |
| Plusieurs onglets dont un seul d'annonces | `reparer` garde l'onglet aux en-têtes du schéma et retire les autres |
| Liens injoignables depuis le script (pare-feu, robots bloqués) | le signaler : la page doit aussi être lisible par les robots d'OpenAI |
| Plus de 5 000 annonces | limite par compte (docs) : découper ou archiver |
| Texte trop long | ne pas couper : proposer une réécriture, la faire valider |
