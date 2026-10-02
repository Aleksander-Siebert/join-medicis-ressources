# Résultats de l'évaluation v1.0 (2 octobre 2026)

## 1. Sur des sites réels

- **Maillage de joinmedicis.com.** `maillage.py` a lu le sitemap et formé 7
  clusters. Il a aussi listé à part 33 URL du sitemap en erreur 404 : des
  fiches d'écosystème vides, que le site déclarait sans les servir. Elles
  faussaient l'analyse avant la correction du script.
- **Fiches Skills de joinmedicis.com.** `onpage.py` a trouvé 4 défauts communs
  à toutes les fiches :
  - title de 10 caractères sans la marque (le layout coupait le modèle de title) ;
  - meta description de 246 à 255 caractères ;
  - deux H1, le README rendu ajoutant le sien ;
  - saut H2 → H4 dans le pied de page.

  Les quatre sont corrigés sur le site. L'audit a aussi remonté un faux
  positif du script : un avatar décoratif avec `alt=""` était compté comme
  « image sans alt ». Le script est corrigé : seul l'attribut absent est
  signalé.

## 2. Humaniseur, profil article

La fixture [`seo-human/article-ia.md`](seo-human/article-ia.md) concentre les
tics d'un article généré :

- une intro méta (« Dans cet article, nous allons voir ») ;
- « dans un monde en constante évolution » ;
- une section « Défis et perspectives » ;
- des gras partout ;
- « chez Assurly » ;
- une voix passive avec agent.

`detect.py` la note 28,7 sur 100 (SIGNALÉ). `humanize.py` fait 4 corrections
automatiques sans toucher aux titres ni aux listes. Il laisse 21 passages à
réécrire, avec la raison de chacun. Le score ne bouge presque pas (28,3) :
c'est voulu. Le script ne réécrit pas les phrases. Il les montre à Claude, qui
les réécrit en suivant le rapport.

## 3. Tests automatiques

| Suite | Résultat |
|---|---|
| `seo-human/test_humaniseur.py` | 21 sur 21 |
| `seo-human/test_article.py` | 9 sur 9 |
| `scripts/test_scripts.py` (maillage, on-page, images, Core Web Vitals, veille, drift) | 11 sur 11 |

## Limites

Cette version ne contient pas encore de comparaison à l'aveugle des textes
produits face à claude-seo ou aux Skills de Corey Haines (même brief, deux
packs, notation sans savoir lequel a écrit quoi). Pour le pack LinkedIn,
l'exercice avait montré des écarts surtout sur le français. C'est la
prochaine série.
