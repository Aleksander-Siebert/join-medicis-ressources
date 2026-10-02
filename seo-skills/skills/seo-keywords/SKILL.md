---
name: seo-keywords
description: >-
  Recherche de mots-clés en français : élargit un sujet en 30 à 50 requêtes,
  classe l'intention (informationnelle, commerciale, transactionnelle,
  navigationnelle), regroupe les requêtes qui méritent la même page, repère
  la cannibalisation et choisit le mot-clé principal de chaque page.
  Utilise-le pour « quels mots-clés viser », « idées d'articles », « recherche
  de mots-clés », « sur quoi écrire » ou avant un brief.
---

# seo-keywords

Le but n'est pas une liste de mots-clés, c'est une liste de **pages** : une
page par intention, un mot-clé principal par page.

## 1. Élargir (30 à 50 requêtes)

À partir du sujet et des personas de `site-context.md` :

- recherches associées et questions « Autres questions posées » de Google ;
- modificateurs : comment, pourquoi, prix, meilleur, comparatif, avis, vs,
  exemple, modèle, définition, obligatoire, 2026 ;
- variantes du vocabulaire du lecteur (« mutuelle expatrié » et « assurance
  santé internationale » ne sont pas les mêmes mots, mais souvent la même
  intention) ;
- **avec un connecteur** (Semrush, Ahrefs, Search Console) : volumes,
  difficulté, requêtes sur lesquelles le site apparaît déjà (positions 5 à
  20 = gains rapides). Sans connecteur, ne donne **aucun volume chiffré** :
  indique « fort / moyen / faible » et dis que c'est une estimation.

## 2. Classer l'intention

| Intention | Signaux | Page qui gagne |
|---|---|---|
| Informationnelle | comment, pourquoi, qu'est-ce, guide | guide, article |
| Commerciale | meilleur, comparatif, avis, vs, prix | comparatif, page hybride |
| Transactionnelle | devis, acheter, souscrire, tarif | page produit ou service |
| Navigationnelle | nom de marque, connexion | aucune (exclue) |

En cas de doute, la SERP tranche : regarde ce que Google classe (voir
`/seo-serp`).

## 3. Regrouper : une page par intention

Méthode du recouvrement de SERP : compare les 10 premiers résultats de deux
requêtes.

| URL communes | Décision |
|---|---|
| 7 à 10 | même page : une seule page vise les deux |
| 4 à 6 | même cluster : pages différentes, liées entre elles |
| 2 à 3 | clusters voisins : un lien croisé |
| 0 à 1 | sujets séparés |

Sans accès aux SERP, regroupe par intention et signale que le regroupement
est à confirmer.

## 4. Vérifier la cannibalisation

Avant de proposer une nouvelle page, vérifie que le site n'a pas déjà une page
sur la même intention (sitemap, `site:` ou `/seo-maillage`). Si oui : on
améliore la page existante (`/seo-refresh`), on n'en crée pas une deuxième.

## Sortie

```
SUJET : assurance santé expatrié · persona : expatrié en famille

PAGES À CRÉER OU À RENFORCER
  1. assurance santé expatrié         transactionnelle  page existante → renforcer
     + assurance santé internationale, mutuelle expatrié (même SERP)
  2. assurance santé expatrié prix    commerciale       nouvelle page (comparatif)
  3. CFE ou assurance au premier euro informationnelle  nouvel article (guide MECE)
  ...
SOURCES DES DONNÉES : recherche web (volumes non disponibles)
```

Puis propose `/seo-brief` sur la page prioritaire.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : aucun volume, aucune difficulté sans source. Dis d'où vient
  chaque chiffre.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
