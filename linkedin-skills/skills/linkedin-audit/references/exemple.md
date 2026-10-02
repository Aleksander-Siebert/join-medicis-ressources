# Exemple : l'audit de 14 posts

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
  ! Confondus : format = texte, reponse = non, jour = jeudi désignent presque les mêmes posts. C'est un seul signal ; la cause ne se sépare qu'avec une expérience.
  ! Confondus : pilier = Acquisition, pilier = Rétention désignent presque les mêmes posts. C'est un seul signal ; la cause ne se sépare qu'avec une expérience.
  6 motif(s) testé(s) au seuil de 0,1 : le hasard seul en ferait passer environ 0,6. 6 passe(nt). C'est plus que le hasard : un indice, à confirmer par une expérience.
  Un motif trouvé dans des posts passés est une hypothèse : tu as fait des carrousels quand tu avais de la matière structurée, sur des sujets que tu connaissais, des semaines où tu avais du temps.
  · (13 motifs non testés : moins de 5 posts dedans, dont toutes les formules)
```

## Ce que le Skill en dit

```
AUDIT · 14 posts · 5 mai au 18 juin 2026 · profil

RÉSULTATS QUI COMPTENT
  3 conversations ou prospects sur la période : 1 venu d'un commentaire,
  1 d'un message après le post du 2 juin, 1 d'un événement.

DESCRIPTION
  médiane 2,3% · écart absolu médian 0,7% · CV 0,447
  les 4 posts « forts » sont des textes sur la rétention, avec réponse rapide.

CE QUE DISENT LES DONNÉES
  1. Un seul signal, pas six : texte, réponse rapide et mardi désignent les
     mêmes posts (confondus). Les posts de ce groupe font environ +77% de
     taux d'engagement (n = 9 contre 5). On ne sait pas lequel des trois
     joue : le jour est le moins probable, et le plus facile à croire.
  2. Rétention contre acquisition : +73% pour la rétention (n = 5 contre 9),
     confondu avec l'autre axe des piliers. À relire avec le point 1 : les
     posts sur la rétention sont aussi des textes.
  3. Formules : aucune n'a 5 posts. Rien à conclure sur « liste-promise »
     malgré 4 posts dans le bas du classement : c'est une piste, pas une
     preuve.
  Hypothèses, pas conclusions : les carrousels ont été faits avec des listes,
  sur l'acquisition, sans réponse rapide.

À TESTER
  Le format, à pilier égal : texte contre carrousel sur la rétention,
  alternés, 10 posts par variante, environ 7 semaines à 3 posts par semaine.
  Critère d'échec écrit avant.

ARRÊTER : rien sur ces données.   FAIRE PLUS : répondre dans les 2 heures
(peu coûteux, et dans le groupe qui marche).   NE PLUS OPTIMISER : le jour.

Proposition pour apprentissages.md :
  Expériences en cours : la ligne ci-dessous.
  Rien en « Ce qui marche » : aucun motif ne sépare une cause.
```

## L'expérience (sortie réelle)

```
EXPÉRIENCE  FAISABLE · 10 posts par variante, 20 au total, environ 7 semaines · effet minimal détectable en 12 semaines : 37%
  - Une seule variable change ; formule, pilier, format, longueur et créneau restent comparables.
  - Alterner A et B (A, B, A, B…), jamais un bloc de A puis un bloc de B.
  - Le critère d'échec est écrit avant le premier post, dans apprentissages.md.
  - Ne pas regarder le résultat avant la fin : on arrête toujours au moment où ça arrange.
  Critère d'échec : Si, après 10 posts par variante, la médiane de la variante B ne dépasse pas celle de A d'au moins 50%, l'hypothèse est abandonnée.
  Ligne pour apprentissages.md (Expériences en cours) :
  | 2026-10-02 | Les posts texte font plus réagir que les carrousels, à pilier égal | format : A | format : B | 10 | Si, après 10 posts par variante, la médiane de la variante B ne dépasse pas celle de A d'au moins 50%, l'hypothèse est abandonnée. | dans 7 semaines |
```
