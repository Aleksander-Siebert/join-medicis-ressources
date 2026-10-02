---
name: seo-brief
description: >-
  Construit le plan validable d'une page SEO : framework de structure (PAS,
  AIDA, MECE ou pyramide inversée) choisi selon l'intention, title, H1, H2 et
  H3 commentés, couverture des requêtes, gain d'information, preuves E-E-A-T
  et liens internes. Attend la validation avant toute rédaction. Utilise-le
  pour « fais un brief », « propose un plan », « structure de l'article »,
  ou pour améliorer le plan d'une page existante.
---

# seo-brief

C'est la phase de validation stratégique : on investit dans le plan avant
d'écrire une ligne. Un bon plan fait 80% d'un bon article.

## 1. Les informations (une question à la fois, si elles manquent)

1. Mot-clé principal, langue, intention dominante.
2. Persona cible et zone géographique.
3. Produit ou service à mettre en avant, liens internes imposés.
4. Termes techniques, juridiques ou médicaux obligatoires (E-E-A-T).
5. Données produit fournies (garanties, plafonds, noms de formules). Si
   aucune : on n'invente aucun chiffre.
6. Type de page. Si l'utilisateur ne sait pas, propose le framework adapté
   à l'intention et justifie-le en une phrase.

`site-context.md` répond souvent à 2, 3 et 4 : ne repose pas ces questions.

## 2. La SERP

Si `/seo-serp` n'a pas été lancé, fais la même analyse en version courte :
type de page dominant, structure des 3 à 5 premiers concurrents, questions de
la SERP, manques, **gain d'information**.

## 3. Le framework

Lis `references/frameworks.md`. Le framework choisi impose l'architecture du
plan, et la rédaction s'y tiendra.

## 4. Le plan

- **Title** (50 à 60 caractères, mot-clé au début, marque à la fin) et **H1**
  (proche du title, mot-clé en tête).
- **H2 et H3**, chacun avec une ligne de description : ce que la section
  répond, le mot-clé ou la question qu'elle porte, son format (liste, tableau,
  définition, étapes), une cible « extrait optimisé » si pertinent.
- **Couverture** : chaque requête du champ sémantique rattachée à une
  section ; MECE : test de non-recouvrement fait.
- **Longueur** : celle de `site-context.md` (défaut 1 000 à 1 500 mots), ajustée
  à la SERP ; dis-le si la SERP demande plus.
- **Gain d'information** : précisément ce que la page apporte de neuf.
- **E-E-A-T** : auteur, preuves d'expérience, sources officielles à citer,
  date de mise à jour. Obligatoire en YMYL.
- **Maillage** : 3 à 5 liens internes vers les pages de `site-context.md`
  (ancre + section où le placer), et la position de la page dans son cluster
  (pilier ou satellite).
- **Règle de pertinence** : chaque section doit être une chose que **ce
  site** peut écrire avec crédibilité. On ne copie pas une section d'un
  concurrent sur un service que le site n'offre pas.

## 5. La validation

Termine par : « Je rédige sur ce plan, ou tu veux changer quelque chose ? »
Ne rédige pas avant le feu vert. Puis passe à `/seo-write`.

## Page existante

Avec une URL : lis la page, garde ce qui est solide, signale ce qui manque ou
a vieilli, et propose des ajouts ciblés plutôt qu'une réécriture complète.

## Sortie

```
BRIEF · « CFE ou assurance au premier euro » · intention informationnelle · MECE

Title   CFE ou assurance au premier euro : que choisir en 2026 ? (57 car.)
H1      CFE ou assurance santé au premier euro : comment choisir
Résumé  3 lignes en tête d'article (voir /seo-write)

H2 Ce que couvre la CFE (et ce qu'elle ne couvre pas)       → réponse directe + tableau
   H3 ...
H2 L'assurance au premier euro : le principe                  → définition (extrait optimisé)
...
Requêtes couvertes 24/24 · Gain d'info : cas d'un couple à Dubaï · Sources : cfe.fr, service-public.fr
Liens   /assurance-sante-expatrie/ (H2 3, ancre « assurance santé expatrié »)

Je rédige sur ce plan, ou tu veux changer quelque chose ?
```

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : aucun chiffre, prix, délai ou condition sans source fournie.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
