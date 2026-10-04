# Exemple : l'audit de 14 posts

> Les faits de cet exemple sont fictifs (Assurly, Camille et leurs chiffres) : ils
> montrent la méthode. Ne les reprends jamais dans une réponse à l'utilisateur.

Utilisatrice fictive : Camille D., acquisition chez Assurly
(assurly.example). 14 posts de mai et juin 2026, recopiés de ses statistiques
dans le modèle (`evals/linkedin-audit/posts-exemple.csv`) ; formules et
piliers notés au fil de l'eau. Son `journal.md` liste 3 contacts sur la
période.

Elle pense : « les carrousels ne marchent pas chez moi, et il faut publier
le mardi ».

## Décrire (sortie réelle)

```
AUDIT  ANALYSÉ · 14 posts · 2026-05-05 au 2026-06-18 · métrique : engagement
  RÉSULTATS QUI COMPTENT : 3 conversation(s) ou prospect(s) dans journal.md sur la période (1 commentaire, 1 message, 1 événement)
  taux d'engagement = (réactions + commentaires + republications) / impressions
  médiane 2,3% · écart absolu médian 0,7% · CV robuste 0,447 · exceptionnel au-delà de 4,8%
  bandes : 0 exceptionnel, 4 fort, 6 typique, 4 faible, 0 très faible

TOP 5
     3,4%  2026-06-02  erreur-datee       texte        4100 imp.  [fort]
     3,3%  2026-05-19  chiffre-d-abord    texte        3300 imp.  [fort]
     3,1%  2026-05-12  erreur-datee       texte        2900 imp.  [fort]
     3,0%  2026-06-16  chiffre-d-abord    texte        2800 imp.  [fort]
     2,8%  2026-05-26  cas-a-trancher     texte        2500 imp.  [typique]
FLOP 5
     1,3%  2026-05-28  liste-promise      carrousel    1200 imp.  [faible]
     1,5%  2026-05-07  liste-promise      carrousel    1650 imp.  [faible]
     1,6%  2026-06-11  releve             carrousel    1350 imp.  [faible]
     1,6%  2026-05-14  liste-promise      texte        1400 imp.  [faible]
     1,8%  2026-06-18  liste-promise      texte        1600 imp.  [typique]
```

## Tester les motifs (sortie réelle, lignes « non testé » abrégées)

```
MOTIFS  MOTIFS TROUVÉS · 14 posts · écart de médianes, test de permutation (2000 tirages, graine 20261002), seuil 0,1, effet minimal 15%, 5 posts par groupe
  ✔ format = texte : écart de +77%, plus grand que 98% des 2000 tirages au hasard (n = 9 contre 5)
  ✔ pilier = Acquisition : écart de -39%, plus grand que 93% des 2000 tirages au hasard (n = 7 contre 7)
  ✔ pilier = Rétention : écart de +73%, plus grand que 99% des 2000 tirages au hasard (n = 5 contre 9)
  ✔ longueur = court (<800) : écart de -45%, plus grand que 99% des 2000 tirages au hasard (n = 6 contre 8)
  ✔ reponse = non : écart de -47%, plus grand que 98% des 2000 tirages au hasard (n = 7 contre 7)
  ✔ jour = jeudi : écart de -47%, plus grand que 99% des 2000 tirages au hasard (n = 7 contre 7)
  · longueur : seul « court (<800) » est testé, « moyen (800-1500) » est la même comparaison inversée
  · reponse : seul « non » est testé, « oui » est la même comparaison inversée
  · jour : seul « jeudi » est testé, « mardi » est la même comparaison inversée
  ! Confondus : format = texte, pilier = Acquisition, pilier = Rétention, longueur = court (<800), reponse = non, jour = jeudi désignent presque les mêmes posts. C'est un seul signal ; la cause ne se sépare qu'avec une expérience.
  6 motif(s) testé(s) au seuil de 0,1 : le hasard seul en ferait passer environ 0,6. 6 passe(nt). C'est plus que le hasard : un indice, à confirmer par une expérience.
  Un motif trouvé dans des posts passés est une hypothèse : tu as fait des carrousels quand tu avais de la matière structurée, sur des sujets que tu connaissais, des semaines où tu avais du temps.
  · (13 motifs non testés : moins de 5 posts dedans, dont toutes les formules)
```

## Ce que le Skill en dit

**AUDIT · 14 posts · 5 mai au 18 juin 2026 · profil**

**Ce qui compte d'abord.** 3 conversations ou prospects sur la période : un
venu d'un commentaire, un par message après le post du 2 juin, un après un
événement.

**Ton niveau habituel.** La moitié de tes posts font plus de 2,3% de taux
d'engagement (réactions, commentaires et republications, divisés par les
impressions). D'un post à l'autre, l'écart typique est de 0,7 point. Aucun
post ne sort vraiment du lot.

**Ce que disent les données : un seul signal, pas six.** Tes posts du mardi
et ceux du jeudi ne se ressemblent en rien :

| | les 7 posts du mardi | les 7 posts du jeudi |
|---|---|---|
| format | 7 textes | 2 textes, 3 carrousels, 2 images |
| pilier | 5 rétention, 1 acquisition, 1 équipe | 5 acquisition, 1 équipe, 1 rétention |
| longueur | 980 à 1 500 caractères | 600 à 820 caractères |
| réponse aux commentaires dans les 2 h | 7 sur 7 | 0 sur 7 |
| taux d'engagement (médiane) | 3,0% | 1,6% |

Le mardi fait mieux, mais il change cinq choses à la fois. Le jour est
l'explication la moins probable, et la plus facile à croire : tu as sans
doute publié tes meilleurs sujets le mardi, quand tu avais le temps de
répondre. Aucune statistique sur ces 14 posts ne dira laquelle des cinq
compte.

**Ce qu'on ne peut pas dire.** Les carrousels : 3 posts seulement, tous le
jeudi, tous sans réponse rapide. « Les carrousels ne marchent pas » n'est
pas testable ici. Les formules non plus : aucune n'a 5 posts.

**À tester.** Le format, tout le reste égal : texte et carrousel sur la
rétention, le mardi, avec réponse dans les 2 h, en alternant. 10 posts par
format, environ 7 semaines à 3 posts par semaine. Critère d'échec écrit
avant : si les textes ne font pas au moins 50% de mieux que les carrousels,
l'idée est abandonnée. (En 12 semaines, ton rythme ne permet pas de voir un
écart plus petit que 37%.)

**Arrêter :** rien sur ces données. **Faire plus :** répondre dans les 2 h,
c'est gratuit et c'est dans le groupe qui marche. **Ne plus optimiser :** le
jour.

**Pour apprentissages.md :** la ligne d'expérience ci-dessous, rien en « Ce
qui marche » tant que la cause n'est pas séparée.

## L'expérience (sortie réelle)

```
EXPÉRIENCE  FAISABLE · 10 posts par variante, 20 au total, environ 7 semaines · effet minimal détectable en 12 semaines : 37%
  - Une seule variable change ; formule, pilier, format, longueur et créneau restent comparables.
  - Alterner A et B (A, B, A, B…), jamais un bloc de A puis un bloc de B.
  - Le critère d'échec est écrit avant le premier post, dans apprentissages.md.
  - Ne pas regarder le résultat avant la fin : on arrête toujours au moment où ça arrange.
  Critère d'échec : Si, après 10 posts par variante, la médiane de la variante B ne dépasse pas celle de A d'au moins 50%, l'hypothèse est abandonnée.
  Ligne pour apprentissages.md (Expériences en cours) :
  | 2026-10-03 | Les posts texte font plus réagir que les carrousels, à pilier égal | format : carrousel | format : texte | 10 | Si, après 10 posts par variante, la médiane de la variante B ne dépasse pas celle de A d'au moins 50%, l'hypothèse est abandonnée. | dans 7 semaines |
```
