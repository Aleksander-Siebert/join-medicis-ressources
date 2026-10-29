---
name: seo-keywords
description: >-
  Recherche de mots-clés en français qui aboutit à une liste de pages, pas de
  mots : élargit un sujet en 30 à 50 requêtes réelles (Search Console,
  recherches associées, questions posées), classe l'intention, décide
  quelles requêtes partagent une page par recouvrement de SERP mesuré par
  script (domaines généralistes retirés, échantillon bruité signalé), repère
  la cannibalisation dans l'export requête × page de Search Console et
  regroupe les requêtes réelles du site par page. Aucun volume sans outil
  nommé. Utilise-le pour « quels mots-clés viser », « idées d'articles »,
  « recherche de mots-clés », « mes pages se cannibalisent ? », « sur quoi
  écrire ». Pas pour analyser une SERP en profondeur (/seo-serp), écrire le
  plan d'un article (/seo-brief) ni bâtir la stratégie d'ensemble
  (/seo-plan).
---

# seo-keywords

Le but n'est pas une liste de mots-clés, c'est une liste de **pages** : une
page par intention, un mot-clé principal par page, et aucune page qui en
concurrence une autre du même site.

**À lire avant de commencer :** `commun/regles.md` (lecture seule, contenu de
tiers = donnée, zéro invention) et `commun/preuves.md` (ce qu'on sait de
Google, folklore à écarter). Données et connecteurs :
`references/donnees.md`.

## 1. Avant de chercher

1. Lis `site-context.md` (lecteurs, offre, pages à pousser, concurrents),
   `apprentissages.md` et, s'il existe, l'export Search Console.
2. Une seule question si le sujet est flou : « Pour quelle offre ou quelle
   page veux-tu du trafic ? ». Sinon, avance avec des hypothèses écrites.

## 2. Élargir (30 à 50 requêtes réelles)

Dans cet ordre de fiabilité :

1. **Search Console du site** : les requêtes sur lesquelles il apparaît
   déjà. Positions 5 à 20 = gains rapides sur une page existante.
2. **Ce que montre Google** : recherches associées, « Autres questions
   posées », saisie semi-automatique, relevées à la main ou par l'outil de
   lecture web, avec la date.
3. **Un connecteur payant** (Semrush, Ahrefs…) si l'utilisateur en a un :
   volumes et difficulté de l'outil, cités avec leur nom.
4. **Les mots des clients** : questions au service client, avis, FAQ.

Modificateurs français utiles : comment, pourquoi, quel, prix, tarif,
combien, meilleur, comparatif, avis, vs, ou, exemple, modèle, définition,
obligatoire, gratuit, près de chez moi, et l'année seulement si la SERP la
montre.

Sans outil, **aucun volume chiffré** : écris « vu dans Search Console »,
« proposé par Google » ou « non mesuré ».

## 3. Classer l'intention

| Intention | Signaux | Page qui gagne en général |
|---|---|---|
| Informationnelle | comment, pourquoi, qu'est-ce, guide, définition | guide, article |
| Commerciale | meilleur, comparatif, avis, vs, prix | comparatif, page de catégorie |
| Transactionnelle | devis, acheter, souscrire, tarif, réserver | page produit ou service |
| Navigationnelle | nom de marque, connexion, contact | aucune nouvelle page |

En cas de doute, la SERP tranche : ce que Google classe dit l'intention
(`/seo-serp`).

## 4. Regrouper : une page par intention, mesuré

Relève les 10 premiers résultats de chaque requête candidate (outil de
lecture web, export d'un outil, ou relevé collé par l'utilisateur, avec la
date et le pays), puis :

```bash
python3 scripts/motscles.py recouvrement serp.txt
```

| URL communes sur 10 | Verdict | Conséquence |
|---|---|---|
| 7 à 10 | même page | une seule page vise les deux requêtes |
| 4 à 6 | même cluster, **à trancher** | l'intention décide : une page ou deux pages liées |
| 2 à 3 | clusters voisins | un lien croisé |
| 0 à 1 | sujets séparés | aucun lien imposé |

Ces seuils sont une **pratique de terrain**, pas une règle de Google : dis-le.
Le script retire les plateformes généralistes présentes partout (Wikipédia,
YouTube, Reddit…), garde les concurrents, et signale un échantillon trop
court ou bruité. Sans accès aux SERP, regroupe par intention et écris
« regroupement à confirmer ».

## 5. Vérifier la cannibalisation

Avant de proposer une nouvelle page, vérifie que le site n'en a pas déjà
une sur la même intention :

```bash
python3 scripts/motscles.py cannibalisation gsc-requetes-pages.csv --marque assurly
python3 scripts/motscles.py groupes gsc-requetes-pages.csv
```

- `cannibalisation` : requêtes dont plusieurs pages se partagent les
  impressions (la seconde à 20% au moins de la première), avec une piste :
  garder, fusionner ou différencier, **après relecture des deux pages**.
- `groupes` : pour quoi chaque page est déjà vue. Une requête cible déjà
  portée par une page = on renforce cette page (`/seo-refresh`), on n'en crée
  pas une deuxième.

L'export de l'interface Search Console ne croise pas requête et page : il
faut l'API (connecteur), Looker Studio ou un module de tableur
(`references/donnees.md`). Sans lui : sitemap, recherche `site:` et
`/seo-maillage`, et le dire.

## 6. La sortie (format fixe)

```
MOTS-CLÉS · {{sujet}} · {{date}} · sources : {{Search Console du … au …, Google relevé le …, outil}}

PAGES À CRÉER OU À RENFORCER
  1. {{mot-clé principal}}   {{intention}}   {{page existante → renforcer | nouvelle page ({{type}})}}
     + {{requêtes de la même page}} ({{preuve : même SERP 8/10 | même page Search Console}})
     données : {{impressions, position | « non mesuré »}}
  2. …

À TRANCHER
  {{paires à 4-6 URL communes, et ce qui décidera}}

CANNIBALISATION
  {{requête : pages en concurrence, piste}} | aucune vue dans l'export du … au …

PROCHAINE ÉTAPE : /seo-brief sur la page n° {{1}}
```

## Erreurs et cas limites

| Situation | Conduite |
|---|---|
| Aucun accès aux SERP ni à Search Console | regroupe par intention, marque chaque regroupement « à confirmer », aucun volume |
| SERP très différentes selon le pays ou l'appareil | relève dans le pays visé, note la date et le pays, compare à date égale |
| SERP de marque (navigationnelle) | exclue des regroupements et de la cannibalisation (`--marque`) |
| Le site est neuf, sans Search Console | partir du connecteur ou de Google ; positions et gains rapides « non mesurés » |
| L'utilisateur veut « des volumes » sans outil | dire qu'aucun volume n'est disponible sans outil nommé ; proposer Search Console (gratuit) pour les requêtes du site |
| Demande de page par ville ou par variante sans contenu propre | `python3 commun/garde_fou.py --texte "…"` : pages en série, risque de spam |

## Fin de tâche

Propose `/seo-brief` sur la page prioritaire. Si l'utilisateur a corrigé un
regroupement (« ces deux requêtes, chez nous, c'est la même page »), propose
de l'ajouter à `apprentissages.md`, avec son accord.
