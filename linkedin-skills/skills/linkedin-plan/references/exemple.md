# Exemple : la semaine du 5 octobre 2026

> Les faits de cet exemple sont fictifs (Assurly, Camille et leurs chiffres) : ils
> montrent la méthode. Ne les reprends jamais dans une réponse à l'utilisateur.

Utilisatrice fictive : Camille D., acquisition chez Assurly
(assurly.example). Sa stratégie (`contexte.md`) : 3 posts par semaine,
budget de 300 minutes, piliers Rétention 40%, Acquisition 40%, Équipe 20%.
Son `journal.md` et son `apprentissages.md` sont dans `evals/linkedin-plan/`.

## La question, et la réponse

> Qu'est-ce qui s'est passé cette semaine ?

« On a fini l'analyse des 60 appels aux résiliés. Inès a tenu le téléphone
trois semaines. Le comité veut couper 30% du budget payant, je pense que
c'est le délai de remboursement qu'il faut traiter. »

## Premier jet, refusé par le contrôle

Le premier jet reprenait `chiffre-d-abord` mardi et jeudi, mettait les trois
posts sur la rétention et un angle « l'IA » vendredi :

```
python3 scripts/semaine.py --exemple --minutes 200
PLAN  BLOQUÉ  ·  3 posts · environ 275 min
  ✖ « chiffre-d-abord » le 2026-10-06 et le 2026-10-08 : pas deux fois la même formule en 7 jours.
  ✖ Pilier « Rétention » : 100% des 3 posts sur 4 semaines. Aucun pilier au-delà de 60%.
  ✖ Il faut environ 275 minutes (3 posts avec réponses + 15 min de routine par jour ouvré) pour 200 disponibles. […]
  ! 2026-10-09 : angle « l'IA » : un angle, pas un sujet […]
  ! Objectifs de la semaine : commentaires, sauvegardes. Avec 3 posts, vise au moins 3 objectifs différents […]
  ! 2026-10-08 et 2026-10-09 : même objectif deux jours de suite.
  ! Liste d'engagement de 8 personnes […]
  ! Aucun acheteur dans la liste […]
```

## Plan corrigé (sortie réelle du contrôle)

```
python3 scripts/semaine.py --plan assets/plan-exemple.json --journal journal-exemple.md \
  --apprentissages apprentissages-exemple.md --minutes 300
PLAN  PRÊT  ·  3 posts · environ 215 min
```

`interpellation` n'a pas été proposée : elle est dans « Ce qui ne marche pas
pour moi ». `cas-a-trancher`, utilisé le 1er octobre, revient le 8 : 7 jours
pile, c'est permis.

## Sortie

```
SEMAINE DU 5 OCTOBRE · 3 posts · environ 215 min sur 300 · contrôle PRÊT

MAR  08:15  SAUVEGARDES  chiffre-d-abord  [Rétention · texte]
      angle : les 60 appels aux résiliés, la moitié parlait du délai de remboursement, pas du prix
      réponses : 08:35
JEU  08:00  COMMENTAIRES  cas-a-trancher  [Acquisition · texte]
      angle : couper 30% du budget payant ou raccourcir le délai, ce que ferait le lecteur
      réponses : 08:20
VEN  08:30  PARTAGES  merci-nomme  [Équipe · image]
      angle : Inès, qui a passé 3 semaines au téléphone avec les résiliés
      réponses : 08:50

ROUTINE  15 min par jour ouvré : répondre, puis 3 à 5 commentaires
LISTE    6 pairs · 2 de portée · 2 acheteurs (inchangée)
À PRÉPARER LUNDI  la photo d'Inès et son accord pour être nommée ; le chiffre
                  « 30% » à confirmer avant publication (décision du comité)
EXPÉRIENCE  aucune cette semaine

Dis « écris mardi » et /linkedin-post rédige le post de mardi.
```

Prêt pour les demandes entrantes : preuve (mardi) et vécu (vendredi) cette
semaine ; l'appel à l'action vers l'offre viendra la semaine prochaine.
