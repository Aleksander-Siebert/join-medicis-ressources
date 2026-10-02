---
name: seo-plan
description: >-
  Stratégie SEO sur 12 mois pour un site nouveau ou existant : état des
  lieux, concurrents, architecture et piliers de contenu, plan éditorial,
  socle technique, feuille de route en 4 phases, indicateurs partant des
  vraies données. Modèles français : services réglementés (YMYL), SaaS B2B,
  entreprise locale ou multi-agences, média, conseil et freelance.
  Utilise-le pour « stratégie SEO », « plan SEO », « feuille de route SEO »,
  « par où commencer », « lancer un site ».
---

# seo-plan

Les autres Skills du pack exécutent. Celui-ci décide quoi faire, dans quel
ordre, et comment savoir si ça marche. Un bon plan tient en une page : une
feuille de route de 40 pages ne sera jamais suivie.

## 1. État des lieux (questions courtes, une à la fois)

À partir de `site-context.md` (sinon lance `/seo-context`) :

- **Objectif business** : leads, ventes, notoriété, recrutement ? Une page
  qui convertit vaut plus que dix pages de trafic.
- **Point de départ** : site nouveau ou existant ? Avec Search Console
  (connecteur ou export) : clics, impressions, pages qui ramènent du trafic,
  requêtes en positions 5 à 20 (les gains rapides).
- **Moyens** : qui écrit, combien de contenus par mois, qui touche au site,
  budget outils.
- **Délai** : le SEO se mesure en mois. Un objectif à 4 semaines relève de la
  publicité.

## 2. Concurrents et terrain

3 à 5 concurrents qui se classent vraiment sur les requêtes cibles (pas
seulement les concurrents commerciaux). Pour chacun : types de pages qui
ramènent du trafic, piliers de contenu, ce qu'ils couvrent et pas vous
(`/seo-serp`, `/seo-keywords`, `/seo-veille`).

## 3. Architecture

- 3 à 6 **piliers** (un sujet central par pilier, une page pilier, des pages
  satellites), tirés des intentions de `/seo-keywords`.
- Structure d'URL courte et stable, profondeur de 3 clics au plus pour les
  pages qui comptent.
- Maillage entre piliers et pages qui convertissent (`/seo-maillage`).

## 4. Plan éditorial

- Ordre de priorité : pages qui convertissent, puis requêtes en positions 5 à
  20 (mise à jour avec `/seo-refresh`), puis nouveaux contenus des piliers.
- Cadence réaliste selon les moyens déclarés. Mieux vaut 4 bons articles par
  mois tenus 12 mois que 20 le premier mois.
- E-E-A-T : auteurs nommés avec page auteur, sources, expérience de terrain,
  données propres.

## 5. Socle technique

Indexation propre, Core Web Vitals, données structurées par type de page
(`/geo-schema` du pack GEO), robots d'IA (`/geo-crawlers`), photo de
référence `/seo-drift` avant toute refonte.

## 6. Feuille de route en 4 phases

| Phase | Période | Contenu | Skills |
|---|---|---|---|
| 1. Fondations | semaines 1-4 | indexation, technique bloquante, pages clés, suivi | `/seo-audit`, `/seo-drift`, `/seo-context` |
| 2. Gains rapides | semaines 5-12 | mise à jour des pages en positions 5-20, maillage, premiers contenus des piliers | `/seo-refresh`, `/seo-maillage`, `/seo-article` |
| 3. Expansion | mois 4-6 | piliers complets, SEO local ou programmatique si pertinent, GEO | `/seo-article`, `/seo-local`, `/seo-programmatic`, `/geo-optimize` |
| 4. Autorité | mois 7-12 | données propres, relations presse, mentions, réseaux sociaux | `/geo-mentions`, `/seo-social`, `/seo-veille` |

Adapte les phases avec le modèle du secteur : `references/modeles.md`.

## 7. Indicateurs

| Indicateur | Point de départ | 3 mois | 6 mois | 12 mois |
|---|---|---|---|---|
| Clics organiques / mois | mesuré | `{{à fixer}}` | | |
| Requêtes dans le top 10 | mesuré | | | |
| Conversions issues du SEO | mesuré | | | |
| Présence dans les réponses d'IA (`/geo-visibility`) | mesuré | | | |

Le point de départ vient des données (Search Console, analytics, test de
visibilité). Les cibles sont fixées **avec** l'utilisateur à partir de ce
point de départ et des moyens : le Skill ne promet jamais un chiffre de
trafic. Sans données, la colonne reste `{{à mesurer}}`.

Adapté de seo-plan (claude-seo, MIT), relié aux Skills du pack.

## Sortie

Le plan en une page dans la conversation : objectif, 3 à 6 piliers, les
5 premières actions avec leur Skill, la feuille de route, les indicateurs.
Puis propose de commencer la phase 1.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : aucun volume de recherche, trafic concurrent ou objectif
  chiffré sans source ; `{{à compléter}}` sinon.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
