# Résultats des évaluations du pack SEO

## Éval à l'aveugle de la v2 (16 octobre 2026)

**Protocole.** Trois textes réels qui ont bien marché dans Google, écrits
sans Skill, fournis par Aleksander : un guide de blog e-commerce high-tech
(2024), une page catégorie e-commerce, un guide d'assureur santé pour
expatriés. Ils sont anonymisés (marques fictives Numerix et Assurly,
signature retirée) et ne sont pas publiés dans ce dépôt.

- Deux rédacteurs travaillent séparément, sur la même consigne
  ([`eval-aveugle/consignes.md`](eval-aveugle/consignes.md)), sans accès au
  web et sans voir les références :
  - **A** : le pack SEO v2 (`/seo-article` en mode autonome, scripts lancés) ;
  - **B** : Claude sans Skill.
- **C** : la référence humaine.
- Un juge (un modèle, sans web) reçoit les trois textes de chaque cas sous
  X, Y et Z, tirés au hasard pour chaque cas
  ([`eval-aveugle/tirage.json`](eval-aveugle/tirage.json)), et note six
  critères sur 10 ([`eval-aveugle/juge.md`](eval-aveugle/juge.md)). Le
  tirage n'a été révélé qu'après le verdict.

### Notes du juge (sur 60)

| Cas | A · pack SEO v2 | B · Claude sans Skill | C · référence humaine | Premier |
|---|---|---|---|---|
| 1 · guide PS5 verticale ou horizontale | **49** | 47 | 21 | A |
| 2 · page catégorie iPhone 16 | **49** | 48 | 26 | A |
| 3 · associations de Français à l'étranger | 49 | **50** | 27 | B |
| Total | **147** | 145 | 74 | |

Verdict complet : [`eval-aveugle/verdict-juge.md`](eval-aveugle/verdict-juge.md).
Textes A et B : [`eval-aveugle/sorties/`](eval-aveugle/sorties/).

### Mesures objectives (`eval-aveugle/mesurer.py`)

| Cas | Conf. | Mots | Trous | controle.py | Constats hauts ou moyens | Affirmations sans source | Humaniseur | Paragraphes à réécrire |
|---|---|---|---|---|---|---|---|---|
| PS5 | A | 1 020 | 2 | PRÊT | 0 | 0 | 69,3 | 0 |
| PS5 | B | 1 135 | 0 | À REVOIR | 11 | 1 | 42,2 SIGNALÉ | 12 |
| PS5 | C | 941 | 0 | À REVOIR | 4 | 1 | 36,1 SIGNALÉ | 11 |
| iPhone 16 | A | 520 | 2 | À REVOIR (sans `--h1-gabarit`) | 2 | 3 | 73,4 | 0 |
| iPhone 16 | B | 544 | 0 | À REVOIR | 8 | 3 | 70,9 | 0 |
| iPhone 16 | C | 482 | 0 | À REVOIR | 5 | 2 | 68,7 | 1 |
| Expatriés | A | 968 | 2 | PRÊT | 0 | 0 | 64,9 | 0 |
| Expatriés | B | 959 | 0 | À REVOIR | 9 | 0 | 37,1 SIGNALÉ | 8 |
| Expatriés | C | 839 | 0 | À REVOIR | 3 | 3 (YMYL : BLOQUÉ) | 67,4 | 0 |

Ces mesures sont celles du pack : A les passe parce qu'il a été écrit pour
elles. Elles ne prouvent pas seules la qualité ; elles montrent ce que le
pack corrige que les autres textes laissent passer (tics, affirmations sans
source, gabarit).

### Ce que l'éval apprend

- **A et B sont au coude à coude** (147 contre 145). A gagne deux cas sur
  trois, d'un ou deux points : c'est dans la marge d'un juge unique. Le pack
  ne rend pas Claude meilleur rédacteur ; il le rend plus sûr (aucune
  affirmation inventée, typographie et structure contrôlées).
- **Les trous coûtent des points.** Le juge préfère un texte publiable tout
  de suite à un texte qui laisse deux `{{à compléter}}`. Deux trous du pack
  étaient évitables avec un accès au web (la distance de sécurité du guide
  PS5, les modalités de reprise déjà présentes sur une page du site). Sans
  web, le pack choisit le trou plutôt que le chiffre de mémoire : c'est la
  règle zéro invention, on la garde.
- **Le résumé de 3 lignes est jugé comme une annonce du plan** dans deux
  textes du pack (« Ce guide vous aide à… »). Le format vient d'une décision
  d'Aleksander (2 octobre) : il n'est pas changé sans son accord. Piste
  proposée : une première ligne qui répond, au lieu d'annoncer.
- **Sans SERP lue, la couverture est plus étroite** (cas 3 : moins de
  réseaux cités que B). En mode autonome hors ligne, le pack le dit dans ses
  hypothèses ; avec le web, `/seo-serp` comble cet écart.
- **Défaut corrigé pendant l'éval.** Sur la page catégorie, le portail a
  envoyé le texte en relecture humaine parce qu'il n'avait pas de H1, alors
  que le gabarit de la page le porte déjà. `controle.py` et `pipeline.py`
  prennent désormais `--h1-gabarit` (3 tests).

### Limites, à lire avant de conclure sur C

- Les références C ont **bien marché dans Google** : c'est une mesure réelle
  que le juge ne voit pas. Il juge la qualité éditoriale, pas le classement.
- Le protocole désavantage C :
  - le guide PS5 date de juin 2024, avant la PS5 Pro, et il est jugé avec
    des connaissances de 2026 ;
  - la consigne disait « conditions de paiement non fournies », si bien que
    la condition affichée par le site (financement jusqu'à 36 mois) a été notée
    comme une invention ;
  - le juge, sans web, a noté « invérifiables » des chiffres récents et
    sourcés (un baromètre 2026).
- Un seul juge, lui-même un modèle ; trois cas. L'écart entre A et B
  (1 à 2 points par cas) n'est pas significatif ; l'écart avec C ne mesure
  pas la performance SEO réelle.
- La comparaison qui manque : publier un texte du pack et un texte témoin,
  puis lire Search Console après 6 à 8 semaines.

## Évaluation v1.0 (2 octobre 2026)

### 1. Sur des sites réels

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

### 2. Humaniseur, profil article

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

### 3. Tests automatiques

| Suite | Résultat |
|---|---|
| `seo-human/test_humaniseur.py` | 21 sur 21 |
| `seo-human/test_article.py` | 9 sur 9 |
| `scripts/test_scripts.py` (maillage, on-page, images, Core Web Vitals, veille, drift) | 11 sur 11 |

### Limites

Cette version ne contient pas encore de comparaison à l'aveugle des textes
produits face à claude-seo ou aux Skills de Corey Haines (même brief, deux
packs, notation sans savoir lequel a écrit quoi). Pour le pack LinkedIn,
l'exercice avait montré des écarts surtout sur le français. C'est la
prochaine série.
