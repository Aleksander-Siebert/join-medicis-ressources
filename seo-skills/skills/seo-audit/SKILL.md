---
name: seo-audit
description: >-
  Audit SEO d'une page ou d'un site, par ordre de priorité : exploration et
  indexation, technique (vitesse, mobile, HTTPS, URL), on-page (title, H1,
  plan, liens, images, schema), qualité du contenu et E-E-A-T, autorité.
  Mesure avec un script on-page, puis classe les corrections en critique,
  haute, moyenne, basse. Utilise-le pour « audit SEO », « pourquoi je ne me
  positionne pas », « mon trafic a baissé », « vérifie cette page ».
---

# seo-audit

Un audit utile tient en une liste de corrections classées, pas en 40 pages
de constats. On mesure, puis on priorise.

## Périmètre

- **Une page** (URL) : on-page complet + contenu + intention.
- **Un site** : échantillon (accueil, 3 pages produit, 3 articles, 1 page
  catégorie), sitemap, robots.txt, et `/seo-maillage` pour la structure.
- **Une baisse de trafic** : commence par les dates (mise à jour Google ?
  refonte ? migration ?), puis les pages qui ont le plus perdu
  (`/seo-veille rapport` avec deux exports Search Console).

## Ordre d'analyse (on ne passe à l'étape suivante que si la précédente tient)

1. **Exploration et indexation** : robots.txt (rien d'important bloqué),
   meta robots `noindex` involontaires, canonical, sitemap (URL en erreur,
   URL non canoniques), codes 3xx/4xx/5xx, pages importantes indexées
   (`site:` ou rapport d'indexation Search Console).
2. **Technique** : HTTPS, mobile, Core Web Vitals (PageSpeed Insights ou
   Search Console ; ne les invente pas depuis le HTML), rendu JavaScript du
   contenu principal, structure des URL, redirections en chaîne.
3. **On-page** : title, meta description, H1 unique, plan des titres sans
   saut, mot-clé aux bons endroits, images (alt, poids, format), liens
   internes et ancres, données structurées, hreflang si plusieurs langues.
4. **Contenu** : la page répond-elle à l'intention que montre la SERP
   (`/seo-serp`) ? Grille qualité Google (`/seo-write`,
   `references/qualite-google.md`), E-E-A-T (auteur, sources, expérience),
   contenu daté ou mince, cannibalisation.
5. **Autorité** : liens entrants et mentions (avec un connecteur Semrush ou
   Ahrefs), en dernier : c'est rarement ce qui bloque en premier.

## Le script on-page

Avec exécution de code :

```bash
python3 onpage.py https://www.site.fr/page/ --mot-cle "mot clé principal"
python3 onpage.py page.html --url https://www.site.fr/page/ --json
```

Il mesure 15 points (title, description, H1, plan des titres, mots, images
sans alt, canonical, robots, lang, viewport, Open Graph, JSON-LD, liens
internes et ancres génériques, hreflang, place du mot-clé). Sans exécution
de code, fais les mêmes contrôles à la lecture du code source de la page.

Les longueurs de title (50-60) et de description (140-160) sont des repères :
Google tronque en pixels et réécrit souvent la description.

## Sortie

```
AUDIT · https://www.site.fr/assurance-expatrie/ · mot-clé « assurance santé expatrié »

CRITIQUE (à corriger maintenant)
  - 2 H1 sur la page (l'un dans l'en-tête mobile) → n'en garder qu'un
HAUTE (cette semaine)
  - Meta description de 246 caractères → 150-160, voix active
  - La SERP montre des comparatifs ; la page n'a aucun tableau
MOYENNE (ce mois-ci)
  - Saut H2 → H4 dans « Garanties »
BASSE
  - 1 image sans alt

À MESURER (données non disponibles ici) : Core Web Vitals, indexation réelle
```

Chaque point : le constat, pourquoi il compte, la correction précise. Pas de
note globale inventée ; si un score est demandé, dis comment il est calculé.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : ne déclare jamais une mesure que tu n'as pas faite (vitesse,
  indexation, liens entrants). Écris « à mesurer » et dis avec quel outil.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est modifié sur le site par le Skill.
