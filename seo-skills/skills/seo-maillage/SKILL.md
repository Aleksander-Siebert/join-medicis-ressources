---
name: seo-maillage
description: >-
  Lit le sitemap du site, regroupe les pages en clusters thématiques (pilier
  et pages satellites), repère les pages orphelines, isolées, en erreur ou qui
  se cannibalisent, et propose des liens internes avec ancre et phrase
  d'insertion, à valider un par un. Trouve aussi les pages qui doivent faire
  un lien vers un nouvel article. Utilise-le pour « maillage interne »,
  « topic cluster », « pages orphelines », « analyse mon sitemap »,
  « cannibalisation ».
---

# seo-maillage

Le maillage interne, c'est dire à Google quelles pages comptent et comment
elles se tiennent. Ce Skill construit les clusters à partir de ce qui existe
vraiment sur le site, puis propose des liens qu'un humain valide.

## Entrées

- le **sitemap** (URL ou fichier ; les index de sitemaps sont suivis) ;
- ou un **export de crawl** (Screaming Frog, Sitebulb : colonnes Address,
  Title, H1, Meta Description) ;
- en option, un **export Search Console « Pages »** (clics) : les pages
  visitées deviennent des hôtes prioritaires ;
- en option, un **brouillon d'article** : on cherche ses pages hôtes.

## Avec exécution de code

```bash
python3 maillage.py --sitemap https://www.site.fr/sitemap.xml --lire --max 300
python3 maillage.py --sitemap … --lire --filtre /blog/ --trafic pages-gsc.csv
python3 maillage.py --crawl export-screaming-frog.csv --trafic pages-gsc.csv
python3 maillage.py --sitemap … --lire --cible brouillon.md      # nouvel article
```

`--lire` ouvre chaque page (titre, H1, texte, liens déjà présents ; mis en
cache) : c'est ce qui permet de trouver les orphelines et d'exclure les liens
existants. Le script calcule la proximité des pages (TF-IDF, sans API) et
note chaque lien possible : **0,7 × proximité + 0,3 × trafic de la page
hôte**.

Sans exécution de code : demande la liste des URL et titres (ou l'export de
crawl) et fais le regroupement à la lecture. Au-delà de ~200 pages, propose
Claude Code.

## Ce que tu fais du résultat (le travail du Skill)

Le script propose, **tu relis** :

1. **URL en erreur** (404, 5xx dans le sitemap) : à corriger ou retirer du
   sitemap en premier.
2. **Clusters** : vérifie que chaque cluster a un vrai sujet commun ; nomme
   le pilier (page la plus complète sur le sujet large). Un cluster sans page
   pilier = une page pilier à créer (`/seo-brief`).
3. **Cannibalisation** : pour chaque paire, regarde l'intention réelle (et la
   SERP). Décision : fusionner (redirection 301), différencier l'angle, ou
   garder si les intentions diffèrent vraiment.
4. **Pages orphelines et isolées** : rattache-les à un cluster ou assume
   qu'elles vivent seules (pages légales).
5. **Liens** : écarte ceux qui n'ont pas de sens réel pour le lecteur. Pour
   chaque lien gardé : l'**ancre** (2 à 6 mots, descriptive, variée, jamais
   « cliquez ici ») et la **phrase réécrite** de la page hôte qui l'accueille.

## Les règles d'un cluster sain

| Lien | Règle |
|---|---|
| Satellite → pilier | obligatoire, dans le texte |
| Pilier → chaque satellite | obligatoire |
| Satellite ↔ satellite du même cluster | 2 à 3 liens par page |
| Entre clusters | 0 à 1, seulement si le lecteur en a besoin |
| Toute page importante | au moins 3 liens entrants, à 3 clics max de l'accueil |

Les pages à pousser de `site-context.md` reçoivent des liens depuis les
articles du cluster correspondant.

## Sortie

```
MAILLAGE · 97 pages · 7 clusters · 33 URL en erreur dans le sitemap

À CORRIGER D'ABORD : 33 URL du sitemap en 404 (fiches /ecosysteme/… vides)
CLUSTER « Assurance santé expatrié » · pilier /assurance-sante-expatrie/
  liens à ajouter (3 sur 7 validés) :
  /blog/choisir-assurance-sante-expatrie/ → /assurance-sante-expatrie/
     ancre « assurance santé expatrié »
     phrase : « Une fois vos critères posés, comparez les formules d'assurance santé expatrié… »
CANNIBALISATION : /assurance-sante-expatrie/ et /blog/assurance-sante-expatrie-prix/ → garder, angles différents (offre / prix)
```

Valide les liens avec l'utilisateur ; rien n'est modifié sur le site.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : ne cite que des URL qui existent (sitemap ou crawl).
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
