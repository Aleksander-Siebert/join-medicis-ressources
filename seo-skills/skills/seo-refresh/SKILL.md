---
name: seo-refresh
description: >-
  Met à jour un article déjà publié : repère les affirmations datées et les
  chiffres périmés, les sujets que la SERP actuelle couvre et pas l'article,
  les nouvelles sources à citer et les liens internes à ajouter, puis propose
  chaque modification séparément, à accepter ou refuser. Utilise-le pour
  « mets à jour cet article », « rafraîchis ce contenu », « l'article a perdu
  des positions », ou pour un article de plus de 12 mois.
---

# seo-refresh

Mettre à jour un article qui a déjà une histoire vaut souvent mieux qu'en
écrire un nouveau. On garde ce qui marche, on corrige ce qui a vieilli.
Inspiré du pipeline de mise à jour d'Ahrefs (Agent A).

## Entrée

L'URL de l'article (ou son texte collé), et si possible ses données Search
Console (requêtes, clics, position) sur 3 à 6 mois.

## Quatre analyses

1. **Affirmations datées** : chaque statistique, étude, prix, loi, règle,
   année ou outil cité. Pour chacune : encore vraie ? plus récente
   disponible ? Propose la source de remplacement précise, ou marque
   « à vérifier ». Ne remplace jamais un chiffre par un chiffre non sourcé.
2. **Écarts avec la SERP actuelle** : ce que les 5 premiers résultats
   d'aujourd'hui couvrent et que l'article ne couvre pas (`/seo-serp` en
   version courte). Format attendu changé ? (ex. la SERP montre désormais
   des tableaux).
3. **Requêtes perdues ou proches** : avec la Search Console, les requêtes en
   positions 5 à 20 où une section ajoutée ou un H2 mieux formulé ferait
   gagner.
4. **Maillage et offre** : nouvelles pages du site à lier (`/seo-maillage
   --cible`), nouveau produit ou service à mentionner (`site-context.md`).

## Sortie : des modifications, pas un article réécrit

Pour économiser les tokens et garder la main, une liste numérotée :

```
MISE À JOUR · /blog/cfe-ou-premier-euro/ · publié en mars 2025

1. [CHIFFRE DATÉ] §2 « La cotisation CFE démarre à X € par mois » (chiffre de 2025)
   → à vérifier sur cfe.fr (barème 2026) · proposition : citer le barème sans montant
2. [MANQUE SERP] 4/5 concurrents traitent « CFE et retraite » ; l'article non
   → ajouter un H3 sous « Qui peut adhérer » (3 phrases, source cfe.fr)
3. [TITRE] « CFE ou assurance privée » → « CFE ou assurance au premier euro : que choisir en 2026 »
4. [LIEN] ajouter vers /assurance-retraite-etranger/ dans §4, ancre « assurance retraité à l'étranger »

Lesquelles j'applique ? (ex. « 1, 2, 4 »)
```

Puis réécris **seulement** les passages acceptés, humanisés avec `/seo-human`
(profil article). Rappelle de changer la date de mise à jour seulement si le
contenu a vraiment changé.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : un chiffre périmé sans remplaçant sourcé devient une
  formulation sans chiffre, jamais un nouveau chiffre inventé.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
