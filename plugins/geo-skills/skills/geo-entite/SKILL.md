---
name: geo-entite
description: >-
  Vérifie que la marque est une seule entité, nommée pareil partout, pour
  que les moteurs et les modèles ne la confondent ni avec un homonyme ni
  avec un concurrent : nom dans le title (coupé au bon séparateur),
  og:site_name, H1, JSON-LD (Organization et tous ses sous-types, @graph)
  et mention ©, un seul bloc Organization avec @id, logo et sameAs, profils
  sameAs classés et appelés, valeurs du JSON-LD visibles sur la page (une
  note ou un prix balisé mais invisible est critique), candidats Wikidata à
  confirmer. Produit le bloc JSON-LD à coller, rempli seulement avec du
  vrai. Utilise-le pour « schema », « JSON-LD », « données structurées »,
  « entité de marque », « sameAs », « Wikidata », « l'IA nous confond avec
  une autre société ». Pas pour les erreurs factuelles des IA
  (/geo-exactitude) ni la présence sur les sites tiers (/geo-mentions).
  Aucun balisage « pour l'IA ».
---

# geo-entite

Un modèle ne connaît pas un site, il connaît des **entités** : une marque,
ses produits, ses dirigeants, reliés entre eux. Si la marque s'appelle
« Assurly » dans le title, « Assur.ly » dans og:title et « Assurly
Courtage » dans le JSON-LD, si son `sameAs` pointe vers le profil personnel
d'une salariée, les moteurs ont plusieurs entités floues au lieu d'une. Ce
Skill aligne les noms et les profils, et ne balise que ce qui est vrai et
visible.

Google le dit : aucune donnée structurée n'est requise pour les Aperçus IA
et aucune n'est propre à l'IA. Elles servent à décrire l'entité et aux
résultats enrichis encore actifs. Pas de promesse de citation.

**À lire avant de commencer :** `commun/regles.md` et `commun/preuves.md`
(§2 Google). `site-context.md` donne le nom officiel, la raison sociale et
les profils.

## 1. Lancer le contrôle

```bash
python3 scripts/entite.py https://www.site.fr/ --marque "Assurly"
python3 scripts/entite.py accueil.html --marque "Assurly" --verifier --wikidata
python3 scripts/entite.py accueil.html --marque "Assurly" --bloc
```

Sur la page d'accueil d'abord, puis la page « à propos » et une page
produit. `--verifier` appelle chaque lien `sameAs` ; `--wikidata` cherche la
marque sur Wikidata (API publique, sans clé).

## 2. Ce que le script contrôle

| Bloc | Contrôle | Pourquoi |
|---|---|---|
| Noms | title, og:site_name, og:title, H1, JSON-LD, mention © : la marque, une variante ou rien | un nom déclaré (JSON-LD, og:site_name, ©) doit être la marque, forme juridique mise à part ; un title ou un H1 peut la contenir |
| Séparateurs | le title se coupe à chaque `\|`, `–`, `—`, `-`, `·`, `:` entourés d'espaces | « Guide \| Assurly » et « Assurly – Guide » donnent la marque ; « Coca-Cola » reste entier |
| Organisation | un seul bloc, ou des blocs reliés par le même `@id` ; `@id`, `url`, `logo`, `sameAs` présents | deux blocs aux noms différents (thème et extension) font deux entités |
| Sous-types | `InsuranceAgency`, `Restaurant`, `Dentist`, `@type` en liste… comptent comme Organization | un commerce local est une organisation |
| sameAs | plateformes reconnues, doublons, lien non https, profil LinkedIn personnel | l'organisation pointe vers ses propres profils |
| Visible | téléphone, e-mail, adresse, prix, note, nombre d'avis retrouvés dans le texte | un avis ou un prix balisé sans être affiché est contraire aux règles de Google sur les données structurées |
| FAQ, HowTo | signalés | plus de résultat enrichi FAQ depuis le 7 mai 2026 ; HowTo retiré |

Sans exécution de code : relève les mêmes noms à la main (code source de la
page, `Ctrl+U`) et applique le tableau.

## 3. Corriger

Dans l'ordre :

1. **Un nom.** Choisis la forme officielle (celle du logo et de
   `site-context.md`) et aligne title, og:site_name, JSON-LD et ©. La
   raison sociale va dans `legalName`, les autres écritures dans
   `alternateName`.
2. **Un bloc Organization** par site, avec un `@id` stable
   (`https://www.site.fr/#organization`) que les autres blocs référencent.
   Deux extensions qui balisent chacune : en désactiver une.
3. **sameAs** : page entreprise LinkedIn (pas un profil personnel),
   chaîne YouTube, Wikidata et Wikipédia s'ils existent, fiche Google, et
   les annuaires officiels (annuaire des entreprises). Les personnes ont
   leur propre bloc `Person`.
4. **Visible ou retiré** : une note, un nombre d'avis ou un prix balisé
   doit être affiché sur la même page. Sinon, on retire le balisage.
5. **Le bloc à coller** (`--bloc`) : il reprend les valeurs vraies du
   site, retire profils personnels et doublons, et met `{{à compléter}}`
   ailleurs. Modèles pour article, auteur, produit, service et commerce
   local : `references/jsonld.md`.
6. **Valider** : test des résultats enrichis de Google
   (search.google.com/test/rich-results) et validator.schema.org. Donne les
   deux liens ; l'utilisateur publie.

## 4. Wikidata et homonymes

Wikidata relie une entité à ses identifiants (site, SIREN, profils). Le
script liste des **candidats** ; seul l'utilisateur confirme qu'un élément
est bien sa marque. Créer un élément, gérer un homonyme, aligner les
profils tiers : `references/entite.md`.

## 5. La sortie (format fixe)

```
ENTITÉ · accueil-assurly.html · marque lue : « Assurly »

NOMS (JSON-LD, og:site_name et © doivent être la marque ; title et H1 peuvent la contenir)
  ok       title                                        « Assurly »
  VARIANTE og:title                                     « Assur.ly, la mutuelle des indépendants »
  VARIANTE JSON-LD Organization.name                    « Assurly Courtage »
ORGANISATION · 2 bloc(s) · types JSON-LD : FAQPage, InsuranceAgency, LocalBusiness, Organization, WebSite
  manque : logo
  ! 2 blocs Organization aux noms différents
  ! sameAs vers un profil LinkedIn personnel
SAMEAS · 3 profil(s)
JSON-LD VISIBLE · 4/6 valeurs vérifiables retrouvées sur la page
  CRITIQUE InsuranceAgency/LocalBusiness.aggregateRating.ratingValue = 4.8 : note balisé mais absent du texte visible
```

Exemple fictif (`evals/geo-entite/`). Sous la sortie : 3 corrections au
plus, puis le bloc si l'utilisateur le demande.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Page en 403 ou non lue | Demander le HTML enregistré depuis le navigateur ; relancer sur le fichier. |
| JSON-LD injecté en JavaScript | Absent du HTML serveur : le dire, et demander le code de la page rendue (outil d'inspection) ; Google le lit souvent, d'autres robots non **[à vérifier par moteur]**. |
| JSON-LD invalide | Le script ignore le bloc et le signale (« bloc JSON-LD illisible ») ; le corriger d'abord. |
| Wikidata en 429 ou non lu | « NON LU » : chercher la marque sur wikidata.org à la main. |
| Marque au nom commun (« Orange », « Alan ») | `alternateName` et `sameAs` complets ; `/geo-exactitude` avec les homonymes en `--concurrent`. |
| Plusieurs marques sur un site | Un bloc Organization pour la société, des blocs `Brand` pour les marques produits. |
| Coordonnées absentes de l'accueil | Normal si elles figurent sur la page contact : ligne « info », pas une erreur. |

## Ressources

- `scripts/entite.py` · `commun/page.py`
- `references/jsonld.md` : modèles Organization, WebSite, article et
  auteur, produit, service, commerce local.
- `references/entite.md` : Wikidata, homonymes, profils tiers à aligner.

## Skills liés

`/geo-exactitude` (ce que les IA disent de la marque), `/geo-mentions`
(profils tiers et sources), `/geo-contenu` (la page « à propos »),
`/seo-local` (fiche Google et commerce local, pack SEO).

## Règles du pack

- Zéro invention : pas de note, d'avis, de prix, de date ni de profil
  ajouté au balisage sans être vrai et visible.
- Rien n'est publié : le bloc est proposé, l'utilisateur l'installe.
- Texte simple dans la conversation ; seul le bloc JSON-LD va dans un bloc
  de code.
