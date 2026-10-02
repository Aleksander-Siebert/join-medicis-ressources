---
name: geo-schema
description: >-
  Données structurées JSON-LD pour le SEO et les moteurs génératifs : lit les
  types présents sur une page, repère ce qui manque (Organization, Person,
  Article, FAQPage, Product, LocalBusiness, BreadcrumbList…) et produit le
  bloc JSON-LD à coller, rempli seulement avec des informations vraies et
  visibles sur la page. Utilise-le pour « schema », « JSON-LD », « données
  structurées », « balisage », « entité de marque ».
---

# geo-schema

Les données structurées disent aux moteurs **qui** parle (organisation,
auteur), **de quoi** (article, produit, service) et **où** (adresse, zone).
Pour le GEO, l'enjeu principal est l'entité : relier le site, la marque et
les auteurs à leurs profils ailleurs (`sameAs`) pour que les modèles les
reconnaissent.

## Ce qui sert vraiment

| Page | Types | Pourquoi |
|---|---|---|
| Toutes | `Organization` (ou `LocalBusiness`), `WebSite`, `BreadcrumbList` | identité de la marque, `sameAs` vers LinkedIn, Wikidata, YouTube… |
| Article | `Article` ou `BlogPosting` + `Person` (auteur) | attribution, date de mise à jour, expertise de l'auteur |
| Page produit / offre | `Product` + `Offer`, `AggregateRating` si avis réels | prix, disponibilité, note |
| Service | `Service` + `areaServed` | ce que vous faites, et où |
| Commerce local | `LocalBusiness` (sous-type précis) | adresse, horaires, zone (voir `/seo-local` du pack SEO) |
| Questions-réponses visibles | `FAQPage` | structure question → réponse lisible par les machines |

À savoir **[à vérifier sur Google Search Central]** : Google n'affiche plus
les résultats enrichis FAQ que pour quelques sites officiels et de santé, et
a retiré ceux de HowTo. Le balisage `FAQPage` reste lisible par les moteurs ;
il ne garantit plus d'affichage spécial.

## Méthode

1. **Lire l'existant** : blocs `<script type="application/ld+json">` de la
   page (ou `geo_audit.py`, qui liste les types utiles trouvés). Repérer les
   doublons (le thème et un plugin SEO qui balisent chacun l'organisation).
2. **Choisir les types** avec le tableau ci-dessus. Pas de type sans contenu
   visible correspondant : baliser une FAQ absente de la page est contraire
   aux règles de Google.
3. **Remplir** avec `references/jsonld.md`. Chaque valeur vient de la page,
   de `site-context.md` ou de l'utilisateur ; sinon `{{à compléter}}`.
   Jamais de note, d'avis, de prix ou de date inventés.
4. **Valider** : test des résultats enrichis de Google
   (search.google.com/test/rich-results) et validateur schema.org
   (validator.schema.org). Donne les deux liens.

## Sortie

```
SCHEMA · /blog/cfe-ou-premier-euro/
PRÉSENT : Organization (doublon : thème + plugin, à fusionner)
MANQUE : BlogPosting + Person (auteur), BreadcrumbList
SAMEAS : aucun → LinkedIn de l'entreprise, page Wikidata si elle existe

(bloc JSON-LD prêt à coller)
```

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : chaque propriété correspond à une information vraie et
  visible ; `{{à compléter}}` sinon.
- Texte simple dans la conversation, sans créer de document ; seul le bloc
  JSON-LD va dans un bloc de code.
- Rien n'est modifié sur le site par le Skill.
