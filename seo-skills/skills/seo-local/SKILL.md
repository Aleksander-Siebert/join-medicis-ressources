---
name: seo-local
description: >-
  SEO local pour la France : audit et optimisation de la fiche
  d'établissement Google, avis (dans le respect du droit français), pages
  locales et pages service, cohérence nom-adresse-téléphone, annuaires
  français, Apple Plans et Bing Places, données structurées LocalBusiness,
  sites multi-établissements. Utilise-le pour « SEO local », « fiche Google »,
  « Google Business Profile », « apparaître sur Maps », « avis clients »,
  « pages par ville », pour un commerce, un cabinet, une agence ou un artisan.
---

# seo-local

Pour une entreprise qui sert une zone, le pack local de Google (la carte et
les 3 fiches) compte souvent plus que les liens bleus.

## 1. Le type d'entreprise

- **Établissement physique** (commerce, cabinet, restaurant) : adresse
  visible.
- **Zone desservie** (artisan, dépannage, services à domicile) : adresse
  masquée, zone définie.
- **Hybride** et **multi-établissements** : une fiche et une page par lieu.

## 2. Les six axes

| Axe | Ce qu'on vérifie |
|---|---|
| **Fiche d'établissement Google** | catégorie principale exacte (le facteur n°1), catégories secondaires, horaires (y compris jours fériés), description, services, photos récentes, posts, lien vers une page pertinente du site, réponses aux questions courantes reprises sur le site |
| **Avis** | volume, note, **régularité** des nouveaux avis, réponses du propriétaire, présence sur d'autres plateformes |
| **Pages du site** | une page par service, une page par lieu ; ville et service dans title et H1 ; NAP visible ; carte ; bouton d'appel `tel:` ; avis et photos locales |
| **NAP et annuaires** | nom, adresse, téléphone identiques partout : site, fiche Google, schema, annuaires |
| **Données structurées** | `LocalBusiness` avec le bon sous-type (Dentist, LegalService, Restaurant, HomeAndConstructionBusiness…), `address`, `geo`, `openingHoursSpecification`, `telephone`, `@id` par établissement |
| **Autorité locale** | liens et mentions de la presse locale, des partenaires, des associations, de la mairie, des événements |

## 3. Les annuaires qui comptent en France

Fiche d'établissement Google · Apple Plans (Apple Business Connect) · Bing
Places (alimente aussi des assistants IA) · PagesJaunes · Waze · Facebook ·
annuaires du secteur (Doctolib pour la santé, Avocats.fr, TheFork,
Tripadvisor, Houzz, annuaires des chambres de métiers et CCI). Les données
cohérentes comptent plus que le nombre d'annuaires.

## 4. Les avis et le droit français

- **Interdit** : acheter des avis, écrire de faux avis, filtrer les clients
  avant de les orienter vers Google (« vous êtes satisfait ? laissez un avis,
  sinon écrivez-nous »). Pratiques commerciales trompeuses (Code de la
  consommation) et contraires aux règles de Google.
- **Autorisé** : demander un avis à tous les clients, au bon moment, avec un
  lien direct ; répondre à tous les avis, y compris négatifs, sans données
  personnelles ni secret professionnel (santé, avocats).
- Le site qui affiche des avis doit dire s'ils sont vérifiés et comment
  (obligation d'information sur les avis en ligne). **[à vérifier pour le
  secteur]**

## 5. Pages locales : éviter les pages satellites

Une page par ville avec le même texte = page satellite. **Test du
remplacement** : remplace le nom de la ville ; si le texte reste vrai, la page
doit être réécrite avec des éléments locaux réels (équipe, chantiers, avis
locaux, contraintes du quartier, photos). Voir `/seo-programmatic` au-delà de
10 villes.

## Sortie

```
SEO LOCAL · Cabinet dentaire, Lyon 6e · établissement physique

FICHE GOOGLE      catégorie « Dentiste » ok · horaires fériés absents · 4 photos de 2023
AVIS              38 avis, 4,7 · dernier avis il y a 3 mois → relancer la demande
PAGES DU SITE     pas de page « implant dentaire Lyon » alors que c'est le service n°1
NAP               téléphone différent entre le site (04…) et PagesJaunes (06…)
SCHEMA            LocalBusiness générique → Dentist, ajouter geo et horaires
PRIORITÉS         1. corriger le téléphone  2. page service  3. demande d'avis  4. photos
```

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : pas de note, nombre d'avis ou classement local sans les
  avoir vus. Dis d'où vient chaque constat.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié ni modifié sur la fiche par le Skill.
