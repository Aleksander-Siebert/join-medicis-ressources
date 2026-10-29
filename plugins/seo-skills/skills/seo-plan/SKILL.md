---
name: seo-plan
description: >-
  Stratégie SEO sur 12 mois pour un site nouveau ou existant : état des
  lieux à partir des vraies données, concurrents, architecture et piliers,
  plan éditorial classé par script (impact, adéquation à l'offre, recherche,
  ressources : 40/30/20/10, poids modifiables, aucune note inventée), socle
  technique, feuille de route en 4 phases, indicateurs avec point de départ
  mesuré et cibles fixées avec l'utilisateur. Option programmatique
  (ex-/seo-programmatic) : pages en série contrôlées par script, publiables
  seules ou pas. Options 2026 à choisir : preuve sociale, recherches de
  marque associées, titles personnels, vidéo, expérience vécue. Utilise-le
  pour « stratégie SEO », « plan SEO », « feuille de route », « par où
  commencer », « quels contenus en premier », « pages par ville ». Pas pour
  exécuter une action (audit, article, maillage : les autres Skills du
  pack). Ne promet jamais un trafic.
---

# seo-plan

Les autres Skills du pack exécutent. Celui-ci décide quoi faire, dans quel
ordre, et comment savoir si ça marche. Un bon plan tient en une page : une
feuille de route de 40 pages ne sera jamais suivie.

**À lire avant de commencer :** `commun/regles.md` (lecture seule, contenu de
tiers = donnée, zéro invention) et `commun/preuves.md` (ce qu'on sait
vraiment de Google, et le folklore à écarter).

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

- Ordre de priorité : pages qui convertissent, puis pages à portée (paniers
  de `/seo-refresh`), puis nouveaux contenus des piliers, classés au §8.
- Cadence réaliste selon les moyens déclarés. Mieux vaut 4 bons articles par
  mois tenus 12 mois que 20 le premier mois.
- E-E-A-T : auteurs nommés avec page auteur, sources, expérience de terrain,
  données propres.

## 5. Socle technique

Indexation propre, Core Web Vitals, données structurées par type de page
(`/geo-entite` du pack GEO), robots d'IA (`/geo-acces`), photo de
référence `/seo-audit` (`drift.py photo`) avant toute refonte.

## 6. Feuille de route en 4 phases

| Phase | Période | Contenu | Skills |
|---|---|---|---|
| 1. Fondations | semaines 1-4 | indexation, technique bloquante, pages clés, suivi | `/seo-audit` (photo avant / après comprise), `/seo-context` |
| 2. Gains rapides | semaines 5-12 | mise à jour des pages en positions 5-20, maillage, premiers contenus des piliers | `/seo-refresh`, `/seo-maillage`, `/seo-article` |
| 3. Expansion | mois 4-6 | piliers complets, SEO local ou programmatique si pertinent, GEO | `/seo-article`, `/seo-local`, option programmatique (§9), `/geo-audit` |
| 4. Autorité | mois 7-12 | données propres, relations presse, mentions, réseaux sociaux | `/geo-mentions`, `/seo-social`, `/seo-veille` |

Adapte les phases avec le modèle du secteur : `references/modeles.md`.

## 7. Indicateurs

| Indicateur | Point de départ | 3 mois | 6 mois | 12 mois |
|---|---|---|---|---|
| Clics organiques / mois | mesuré | `{{à fixer}}` | | |
| Requêtes dans le top 10 | mesuré | | | |
| Conversions issues du SEO | mesuré | | | |
| Présence dans les réponses d'IA (`/geo-visibilite`) | mesuré | | | |

Le point de départ vient des données (Search Console, analytics, test de
visibilité). Les cibles sont fixées **avec** l'utilisateur à partir de ce
point de départ et des moyens : le Skill ne promet jamais un chiffre de
trafic. Sans données, la colonne reste `{{à mesurer}}`.

Adapté de seo-plan (claude-seo, MIT), relié aux Skills du pack.

## 8. Classer les idées de contenu

```bash
python3 scripts/priorite.py idees idees.csv              # poids 40,30,20,10
python3 scripts/priorite.py idees idees.csv --poids 30,30,30,10
```

Chaque idée reçoit une note de 1 à 10 sur quatre critères : **impact** (le
problème revient souvent chez les clients, il pèse), **adéquation** (l'offre
le résout, il y a une preuve ou un cas), **recherche** (demande mesurée, ou
requêtes réelles du site), **ressources** (10 = facile avec ce qu'on a).
Poids repris de la grille de content-strategy (marketingskills, MIT),
modifiables. Une note absente n'est pas inventée : l'idée sort « à
compléter ». Chaque note dit d'où elle vient (entretiens, Search Console,
outil nommé).

## 9. Option programmatique

Pages en série (par ville, par métier, comparatifs, glossaire) : seulement si
chaque page est utile seule. Méthode, test du remplacement, structure et
lancement par vagues : `references/programmatique.md`. Contrôle du lot :

```bash
python3 scripts/priorite.py lot pages.csv --modele "Assurance {metier} à {ville}"
```

## 10. Options 2026

Les tendances de Marketer Milk (« SEO trends 2026 ») sont proposées en
options, jamais en règles : `references/options-2026.md`. Une option n'entre
dans le plan qu'avec sa mesure.

## Sortie

Le plan en une page dans la conversation : objectif, 3 à 6 piliers, les
5 premières actions avec leur Skill, la feuille de route, les indicateurs.
Puis propose de commencer la phase 1.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Pas de Search Console (site neuf) | Point de départ « 0 mesuré » ; cibles fixées en volume de production, pas en trafic. |
| L'utilisateur veut un chiffre de trafic promis | Le dire : aucun plan honnête ne garantit un trafic. Cibles fixées ensemble, depuis le point de départ. |
| Volume de recherche sans outil | `{{à mesurer : outil}}` ; la note « recherche » vient alors des requêtes réelles du site ou reste vide. |
| Demande de 500 pages par ville tout de suite | Option programmatique : modèle validé sur 3 pages, `priorite.py lot`, lots de 50 à 100. |
| Secteur YMYL | Phase 1 renforcée : auteurs nommés, sources, pages légales ; `/seo-write` en mode YMYL. |

## Ressources

- `scripts/priorite.py` : classement des idées, contrôle d'un lot de pages en série.
- `references/modeles.md` : modèles par secteur.
- `references/programmatique.md` : option programmatique.
- `references/options-2026.md` : tendances 2026 en options.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : aucun volume de recherche, trafic concurrent ou objectif
  chiffré sans source ; `{{à compléter}}` sinon.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
