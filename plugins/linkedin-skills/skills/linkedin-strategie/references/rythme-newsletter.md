# Rythme et newsletter

## Ce que coûte vraiment un post

Les estimations habituelles comptent le temps d'écriture. Le vrai coût inclut
la relecture et les réponses. Ordres de grandeur de praticien
(alirezarezvani, `cadence_planner.py`, MIT), à remplacer par les temps de
l'utilisateur :

| Activité | Minutes | Ce qu'il y a dedans |
|---|---|---|
| Post texte | 25 | écrire 15, relire et contrôler 10 |
| Post image | 30 | le texte, le visuel, le texte alternatif |
| Carrousel PDF | 90 | plan, 8 à 12 slides, export, couverture |
| Vidéo | 120 | script, tournage, montage, sous-titres |
| Sondage | 20 | seulement s'il y a une vraie décision derrière |
| Article | 180 | c'est un essai |
| Numéro de newsletter | 150 | un essai, avec une promesse de régularité |
| Commentaire utile | 6 | lire vraiment le post, écrire quelque chose qui mérite d'être lu |
| Réponses sous son post | 20 | par post publié, dans les heures qui suivent |
| Message de prospection | 5 | lire son travail, écrire la ligne qui lui est propre |

La ligne qu'on oublie : **répondre sous son post fait partie du post**. C'est
là que les lecteurs te rencontrent.

## Pourquoi la répartition change avec l'étape

| Étape | Part en commentaires | Raison |
|---|---|---|
| départ (moins d'environ 1 000 abonnés, ou reprise) | 60% | tes posts n'ont presque pas de diffusion ; un commentaire utile sous un post qui a déjà une audience est le seul levier qui marche à partir de zéro |
| reconstruction (audience endormie) | 45% | la portée revient avec la régularité |
| établi (tes posts touchent des non-relations) | 30% | la diffusion marche ; la contrainte est ce que tu publies |

Niveau de preuve : avis de praticiens, cohérent entre sources (A, S) ;
mécanisme plausible (un post sans audience n'est pas montré) ; aucune donnée
officielle.

## Le plancher de 90 minutes

Sous 90 minutes par semaine, `budget.py` refuse un plan de publication et
rend une semaine « commentaires seulement » :

- un rythme abandonné en 5e semaine est pire qu'un rythme jamais commencé :
  une rafale de posts suivie d'un silence se voit sur le profil ;
- commenter se dégrade en douceur : une semaine sans temps coûte une semaine,
  un créneau de publication manqué coûte le rythme.

## La semaine minimale

Chaque plan a sa version « mauvaise semaine » (environ 75 minutes) :

1. un post texte, le même jour chaque semaine ;
2. un commentaire utile par jour ouvré ;
3. une réponse à chaque commentaire sous 24 h.

C'est assez pour progresser. Tout ce qui dépasse accélère, et l'accélération
est facultative, la régularité non.

## Même jour, même heure

Deux raisons : un lecteur qui revient apprend quand tu publies ; et tes
propres données deviennent comparables (sinon l'heure brouille toutes les
comparaisons de `/linkedin-audit`). L'heure exacte compte bien moins que la
première ligne [praticien].

## Écrire en lot, et son vrai risque

Écrire quatre posts d'un coup protège le rythme. Le risque : des posts plus
abstraits, parce que le détail précis vient souvent de la journée vécue.
Compromis : écrire en lot, garder une note des détails au fil de la semaine
(`reserve.md`), et que chaque post en vole un.

## Une semaine manquée n'est pas un échec

Une semaine sautée, ce n'est rien. Un mois sauté remet à l'étape « départ ».
L'erreur à éviter : prendre la semaine manquée pour la preuve que tout a
échoué, et arrêter.

---

## La newsletter : une promesse chiffrée avant d'être faite

Une newsletter LinkedIn notifie chaque abonné à chaque numéro. C'est toute
sa valeur et tout son risque : une promesse de régularité et de sujet.

### Éligibilité (officiel, vérifié le 2 octobre 2026)

Aide LinkedIn a591266 : les membres et les pages qui ont **plus de 150
abonnés ou relations** peuvent être évalués ; il faut aussi du **contenu
original récent** et un **historique conforme** aux règles de la communauté.
150 est un seuil d'évaluation, pas une garantie. Personne hors de LinkedIn ne
connaît la liste complète des critères.

### Soutenabilité sur 6 mois

| Rythme | Numéros par mois | À 150 min le numéro |
|---|---|---|
| hebdomadaire | ~4,3 | ~645 min/mois |
| toutes les 2 semaines | ~2,2 | ~322 min/mois |
| mensuel | 1 | 150 min/mois |

Si le budget ne tient pas, on ne lance pas, ou on choisit le rythme qui tient.
Baisser le rythme avant le lancement ne coûte rien ; après, c'est une promesse
rompue envers des gens qui se sont abonnés à une fréquence.

Avec moins de 20% de marge, une seule mauvaise semaine casse le rythme. Les
deux parades qui marchent : **2 numéros d'avance** avant le lancement, et un
format léger en réserve (la sélection de lectures) pour un mois chargé.

### Douze numéros, pas douze essais

| Type | Ce que c'est | Coût |
|---|---|---|
| méthode | une façon reproductible de prendre une décision ; celui qu'on transfère | élevé |
| décorticage | un cas réel examiné en public, avec accord ou anonymisé | élevé |
| carnet de terrain | ce que tu as fait cette quinzaine, échecs compris | faible |
| contre-pied | l'idée reçue du métier, et là où elle casse | moyen |
| question de lecteur | une question reçue, traitée à fond | faible |
| sélection | ce que tu as lu et ce qui t'a fait changer d'avis | le plus faible |

Alterne les types sur les piliers pour que les mêmes paires ne reviennent pas
en boucle.

### Le nom

Nomme-la d'après le problème qu'elle résout. « La lettre de l'acquisition en
assurance » dit à un inconnu s'il doit s'abonner ; « La newsletter de Camille »
suppose qu'il te connaît déjà. Le sous-titre dit pour qui et à quel rythme.

### La règle d'arrêt, écrite avant le n°1

- 3 numéros d'affilée sous la moitié de l'engagement médian des posts : le
  format ne paie pas son coût, la matière retourne aux posts.
- 2 numéros manqués dans un trimestre : baisser le rythme d'un cran plutôt que
  rattraper.
- Finir volontairement, avec un dernier numéro qui le dit, ne coûte rien.
  Laisser mourir en silence, c'est ce que les gens retiennent.

### Newsletter et posts

Un numéro donne 2 ou 3 posts autonomes les deux semaines suivantes, chacun
avec le lien du numéro en premier commentaire (`/linkedin-repurpose`, avec le
registre pour ne pas publier deux fois la même idée). L'inverse (assembler de
vieux posts en numéro) ne marche que si le numéro apporte une synthèse que les
posts n'avaient pas.

Sous environ 500 abonnés : éligible peut-être, mais les retours sont trop
rares pour savoir si le sujet est le bon [praticien].

Sources : alirezarezvani, `cadence_and_consistency.md`,
`newsletter_playbook.md`, `cadence_planner.py` (MIT) ; Aide LinkedIn a591266.
