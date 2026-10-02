---
name: seo-article
description: >-
  Pipeline complet de production d'un article SEO, avec une validation à
  chaque étape : questions de cadrage, mots-clés, analyse de SERP, plan selon
  le framework, rédaction, humanisation, contrôle qualité Google, maillage
  interne et sources. Utilise-le pour « écris un article SEO sur… », « produis
  un article complet », ou quand l'utilisateur veut aller du mot-clé à
  l'article publiable en une session.
---

# seo-article

Le chemin complet, étape par étape. Chaque étape s'arrête sur une validation :
on corrige l'étape fautive, on ne relance jamais tout.

Inspiré du pipeline d'article d'Ahrefs (Agent A) et d'un workflow de
rédaction éprouvé en secteur YMYL.

## Les étapes

| # | Étape | Skill | Ce qu'on valide |
|---|---|---|---|
| A | Cadrage | ce Skill | les 6 réponses (ci-dessous) |
| 1 | Mots-clés | `/seo-keywords` (version courte) | mot-clé principal, secondaires, intention |
| 2 | SERP et concurrents | `/seo-serp` | type de page, manques, gain d'information |
| 3 | Plan | `/seo-brief` | title, H1, H2/H3, framework, liens |
| 4 | Rédaction | `/seo-write` | l'article |
| 5 | Humanisation | `/seo-human` (profil article) | passages réécrits, score |
| 6 | Qualité Google | grille de `/seo-write` | 15 contrôles |
| 7 | Maillage | `/seo-maillage` (mode nouvel article) | liens entrants depuis les pages existantes |
| 8 | Sources | ce Skill | chaque fait sensible a sa source |

## A. Le cadrage (une question à la fois)

1. Mot-clé principal, langue, intention dominante.
2. Persona et zone géographique.
3. Produit ou service à mettre en avant, liens internes imposés.
4. Termes techniques, juridiques ou médicaux obligatoires.
5. Données produit disponibles. Sinon, aucun chiffre ne sera inventé.
6. Type de page (sinon : proposer le framework adapté et le justifier).

Ce que `site-context.md` contient déjà n'est pas redemandé.

## Les validations

À la fin de chaque étape, montre le résultat **court** et demande : « On
valide, ou je corrige ? ». Un retour de l'utilisateur relance **cette étape
seulement**. Pour économiser les tokens : ne réaffiche pas l'article entier
après une correction, montre seulement les passages modifiés.

## Étape 7 : les liens entrants

Un nouvel article sans lien entrant est une page orpheline. Avec le sitemap
du site : `maillage.py --sitemap … --cible article.md` (dans `/seo-maillage`)
donne les 3 pages hôtes les plus proches ; propose pour chacune l'ancre et la
phrase où placer le lien.

## Étape 8 : les sources

Liste chaque affirmation factuelle sensible avec sa source (organisme, texte
officiel, étude datée). Ce qui n'a pas de source est reformulé ou retiré.

## Sortie finale

L'article (texte simple, H2/H3 en Markdown), le bloc méta, puis :

```
CONTRÔLES · humaniseur 84 OK · qualité Google 15/15 · 3 liens entrants proposés · 6 sources
À VÉRIFIER AVANT PUBLICATION · {{à compléter}} x 1 · relecture d'un expert (YMYL)
```

## Fin de tâche

Propose d'ajouter ce qui a été appris (un angle qui a plu, une tournure
rejetée) à `apprentissages.md`, avec l'accord de l'utilisateur.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : aucun chiffre, prix, délai ou condition sans source.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
