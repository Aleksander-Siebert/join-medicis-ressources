---
name: geo-citability
description: >-
  Note chaque section d'une page sur sa capacité à être citée par un moteur
  génératif (réponse directe, autonomie du passage, structure, données,
  originalité), puis réécrit les passages faibles pour qu'une IA puisse les
  reprendre tels quels, sans rien inventer. Utilise-le pour « rends cette page
  citable », « optimise pour ChatGPT / Perplexity / AI Overviews »,
  « citabilité », ou après un audit GEO.
---

# geo-citability

Les moteurs génératifs ne citent pas des pages, ils citent des **passages**.
Un passage citable répond tout de suite, se comprend sans le reste de la
page, et contient un fait vérifiable.

Ce sont d'abord des règles de clarté pour le lecteur. Google précise qu'il
n'est pas nécessaire de découper ses contenus en petits morceaux ni de les
réécrire « pour l'IA » : ses systèmes comprennent les synonymes et trouvent
le bon passage dans une page longue. On ne hache donc pas un texte en blocs
artificiels ; on corrige les sections qui tournent autour du pot.

## Les cinq critères (par section)

| Critère | Poids | Un bon passage |
|---|---|---|
| Réponse directe | 30% | la 1re phrase répond : « La CFE est… », « Le délai de carence dure… » |
| Autonomie | 25% | nomme son sujet (pas « Il », « Cela », « Mais » en tête), ne renvoie pas à « plus haut » |
| Structure | 20% | titre (question pour l'informationnel), paragraphes courts, listes, tableaux |
| Données | 15% | chiffres, dates, unités, **source citée** |
| Originalité | 10% | donnée propre, cas réel, expérience, citation attribuée |

Rubrique adaptée de geo-seo-claude (MIT). Les études sur le GEO (dont
l'étude de Princeton, KDD 2024) vont dans le même sens : citer des sources,
ajouter des statistiques et des citations d'experts aident ; le bourrage de
mots-clés n'aide pas. **[étude académique, 2024]**

## Avec exécution de code

```bash
python3 citability.py https://www.site.fr/guide/
python3 citability.py article.md --top 5
```

Sans exécution de code : découpe la page par titres et note chaque section à
la lecture avec la même grille.

## Réécrire un passage faible

Pour chaque section sous 50 :

1. **Première phrase = la réponse.** Sujet nommé + verbe d'état ou d'action +
   fait : « Le délai de carence d'une assurance expatrié dure en général de 0
   à 12 mois selon la garantie. » (si le fait est sourcé, sinon formule sans
   chiffre ou `{{à compléter}}`).
2. **Le passage tient seul** : remplace « Il », « Cela » par le nom ; coupe
   les renvois (« comme vu plus haut »).
3. **La réponse en 2 ou 3 phrases**, puis le détail. Pas de section coupée
   en morceaux pour atteindre une longueur.
4. **Une source** par fait sensible, nommée (organisme, texte, étude datée).
5. **Le format qui correspond à la question** : définition pour « qu'est-ce
   que », étapes numérotées pour « comment », tableau pour « X ou Y »,
   liste pour « quels ».
6. **Ce que le site est seul à savoir** : un cas client, une donnée interne,
   une expérience de terrain, si l'utilisateur la fournit.

Montre l'avant/après **section par section**, pas la page entière, puis passe
le résultat par l'humaniseur (`/seo-human` du pack SEO, profil article, s'il
est installé).

## Sortie

```
CITABILITÉ · /blog/cfe-ou-premier-euro/ · 46/100

À RÉÉCRIRE
 26  « Format de sortie » : commence par une consigne, 18 mots, aucun fait
     après : « Le format de sortie est la partie du Skill qui fixe… (48 mots) »
 31  ...
DÉJÀ CITABLES : « Qu'est-ce que la CFE ? » (82), « Combien ça coûte ? » (74)
```

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : un passage plus citable ne doit jamais contenir un chiffre
  inventé. Pas de source ? Pas de chiffre.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
