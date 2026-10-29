# Photo avant / après : les règles

Les pires chutes de trafic viennent souvent du site lui-même : un `noindex`
oublié après la recette, un canonical cassé par un plugin, un H1 supprimé par
un nouveau thème, un contenu passé en JavaScript. Personne ne le voit avant
la courbe de Search Console, trois semaines plus tard.

## Le réflexe

1. **Avant** une mise en ligne, une refonte, un changement de thème ou de
   plugin SEO : une photo des pages qui comptent (`audit photo`).
2. **Juste après** : une comparaison (`audit compare`).
3. **Chaque mois** : une comparaison des mêmes pages, avec le rapport de
   `/seo-veille`.

Quelles pages ? Celles qui ramènent le plus de clics (Search Console), les
pages à pousser de `site-context.md`, l'accueil et un modèle de chaque type
(article, catégorie, produit, page locale).

## Les commandes

```bash
python3 scripts/drift.py photo https://www.site.fr/ https://www.site.fr/guide/
python3 scripts/drift.py photo --sitemap https://www.site.fr/sitemap.xml --max 50
python3 scripts/drift.py comparer --tout
python3 scripts/drift.py historique https://www.site.fr/guide/
```

Les photos sont des fichiers JSON dans `~/.claude/seo/drift/`, sur la machine
de l'utilisateur (20 photos gardées par page). Le script renvoie le code 1
s'il trouve un changement critique : il peut tourner dans une CI après chaque
déploiement. Sans exécution de code : le code source des pages avant et après
(ou l'URL de préproduction), comparé à la lecture avec les règles ci-dessous.

## Les règles

| Gravité | Changement | Pourquoi |
|---|---|---|
| CRITIQUE | erreur 4xx/5xx, nouvelle redirection | la page sort de l'index ou perd ses signaux |
| CRITIQUE | `noindex` ajouté | la page disparaît de Google |
| CRITIQUE | `nosnippet` ou `max-snippet:0` ajouté | plus d'extrait, plus d'AI Overviews ni d'AI Mode |
| CRITIQUE | canonical vers une autre URL | la page est retirée de l'index au profit de l'autre |
| CRITIQUE | title ou H1 supprimé, contenu divisé par deux | souvent un gabarit cassé ou un rendu JavaScript |
| À SURVEILLER | title, meta, H1 modifiés | voulu ou pas ? suivre les clics |
| À SURVEILLER | données structurées retirées ou invalides | plugin ou thème changé |
| À SURVEILLER | contenu −20%, liens internes −30%, hreflang ou langue modifiés | |
| INFO | plan H2, Open Graph, images sans alt, texte modifié | à relire |

Adapté de seo-drift (claude-seo, MIT ; auteur d'origine Dan Colta).

## Sortie

```
DRIFT · 12 pages comparées · 2 CRITIQUES · 3 À SURVEILLER

CRITIQUE  /assurance-sante-expatrie/ : noindex ajouté
          -> retirer le noindex (resté de la préproduction ?)
CRITIQUE  /blog/cfe/ : canonical « /blog/cfe/ » → « /blog/ »
          -> le nouveau thème pointe tous les articles vers le blog
À SURVEILLER  /devis/ : title modifié, « Devis assurance expatrié en 24 h » → « Devis »
RIEN À SIGNALER : 9 pages
```

Exemple fictif. Un changement n'est signalé que s'il est mesuré entre deux
photos réelles.
