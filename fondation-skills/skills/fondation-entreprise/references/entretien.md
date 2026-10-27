# L'entretien

Un entretien de contexte échoue quand il recueille ce que les gens disent au
lieu de ce qui est vrai. Les dirigeants et les marketeurs ont une version
« plaquette » de leur entreprise. Le but est d'obtenir la version du
quotidien, sans transformer l'échange en interrogatoire.

## 1. Le cadre, en une phrase

> « Je te pose quelques questions, une à la fois, pour que tout ce que
> j'écrirai ensuite parte de ton entreprise et pas d'une entreprise en
> général. Il n'y a pas de bonne réponse ; “je ne sais pas” est une réponse
> utile. »

Puis une question, et on attend.

## 2. Les questions, dans l'ordre

Saute celles que le site ou un fichier existant ont déjà résolues.
Reformule à partir de ce que tu as lu (« J'ai vu trois offres sur le site :
laquelle se vend le plus ? »).

| # | Question | Remplit | Bonne réponse | Relance si vague |
|---|---|---|---|---|
| 1 | Qu'est-ce qui se vend le plus, à qui, et comment (abonnement, devis, vente) ? | §2 | une offre, un client type, un format | « Le dernier contrat signé, c'était quoi ? » |
| 2 | Qui sont vos clients aujourd'hui, pas ceux que vous visez ? | §3 | un type, une taille, un secteur, une proportion si connue | « Si je regarde les 10 derniers clients, qu'ont-ils en commun ? » |
| 3 | Si vous n'existiez pas, que ferait ce client ? | §4 | au moins le statu quo et une alternative nommée | « Avant de vous trouver, il faisait comment ? » |
| 4 | Pourquoi ceux qui vous choisissent vous choisissent-ils ? Qu'est-ce qui le prouve ? | §5 | un attribut et une preuve | « Qu'a dit le dernier client qui a signé, mot pour mot ? » |
| 5 | Quel est l'objectif de ce trimestre, et quel chiffre dira qu'il est atteint ? | §6 | un objectif vérifiable par un tiers | « À la fin du trimestre, qu'est-ce qui vous ferait dire “c'est réussi” ? » |
| 6 | Qu'est-ce qui a cassé ou ralenti ce trimestre ? Quelle décision repoussez-vous ? | §7 | un fait, une décision | « Si quelque chose devait mal tourner dans les 90 jours, ce serait quoi ? » |
| 7 | Y a-t-il des choses que vous ne devez jamais affirmer, des mentions obligatoires ? Vos clients sont-ils des particuliers, des professionnels ? Faites-vous de la prospection par email ? Confiez-vous des données clients à une IA ? | §8 | oui/non par question, les textes ou la personne qui les connaît | « Qui valide vos publicités aujourd'hui ? » |
| 8 | Quels outils utilisez-vous pour le site, le suivi clients, les emails, les chiffres ? | §9 | une catégorie, un outil | aucune : « aucun » est une réponse |

**Version courte (pressé)** : 1, 2 et 5. Le reste en `{{à compléter}}`, et la
fin de tâche liste les questions à poser la prochaine fois.

**Pas de recommandation d'outil.** On demande la catégorie, on note ce que
la personne utilise. Si elle demande « lequel prendre ? », c'est une autre
conversation, hors de ce Skill (règle de neutralité reprise du plugin
small-business d'Anthropic).

## 3. Les relances

Une seule relance par question. Après, on note `À CONFIRMER` et on avance :
un entretien qui insiste perd la personne.

### La réponse est vague

- « Tu peux me donner un exemple précis ? »
- « Ça ressemble à quoi, un mardi matin ? »
- « Comment saurais-tu que c'est vrai ? »

### La réponse est trop lisse

- « Ça, c'est la version du site. Et la version que tu donnerais à un
  collègue ? »
- « Si c'est vrai, comment expliquer [le fait contraire lu sur le site ou
  dit plus tôt] ? »
- « Que dirait un client qui est parti ? »

### Le sujet est évité

- « Tu es passé vite sur [sujet] : c'est parce que ce n'est pas un problème,
  ou parce que c'est trop gros pour maintenant ? »
- « Tu n'es pas obligé de donner un chiffre : une fourchette suffit. »

### La personne est pressée ou réservée

Ralentis plutôt que d'insister. Propose de laisser la question en
`{{à compléter}}`. Pose d'abord les questions faciles (offre, outils) et
reviens aux sensibles (ce qui coince) quand la confiance est là.

## 4. Les signaux d'alerte

| Ce qu'on entend | Ce que ça cache souvent | Relance |
|---|---|---|
| « Nous n'avons pas de concurrent. » | la concurrence est définie trop étroitement | « Que ferait ce client si vous n'existiez pas ? Qui gagne si vous échouez ? » |
| « Nos valeurs sont X, Y, Z » (dit sans hésiter) | recopié du site | « Racontez-moi une fois où tenir cette valeur vous a coûté quelque chose. » |
| « Ça marche bien, on grandit. » | « bien » n'est pas un chiffre | « Une fourchette ? Elle ne sort pas d'ici. » |
| « Il nous faut juste plus de clients. » | rarement la vraie cause | « Qu'est-ce qui amène les clients que vous avez ? Pourquoi les autres ne vous trouvent pas, ou ne signent pas ? » |
| « Notre cible, c'est tout le monde. » | pas de cible | « Si vous ne pouviez garder qu'un type de client, lequel ? » |
| « Nous sommes les meilleurs / les moins chers. » | superlatif invérifiable | « Comparé à quoi, mesuré comment ? » |
| Détaillé sur les concurrents, flou sur la différence | posture défensive | revenir à la question 4 avec un client précis |

Grille d'origine : guide d'entretien de `cs-onboard` (dépôt
alirezarezvani/claude-skills, MIT), réécrit pour un marketeur. Nous n'en
gardons pas le profil personnel du fondateur (angles morts, conflits,
sortie) : hors sujet pour un fichier partagé, et trop intime.

## 5. Ce qui se note en plus des réponses

- **Ce qui vient en premier**, sans qu'on le demande : souvent la vraie
  priorité.
- **Les contradictions** entre deux réponses, ou entre une réponse et le
  site : les deux valeurs vont en `À CONFIRMER`.
- **Les mots exacts** que la personne emploie pour son offre et ses clients :
  ils servent à `/tone-of-voice` et `/fondation-preuves`, pas ici.

## 6. La clôture

1. Relis tes notes : les 3 à 5 faits les plus importants doivent être dans
   le fichier.
2. Montre le fichier entier, avec les `À CONFIRMER` et les trous visibles.
3. « J'enregistre ? » et attends « oui ».
4. La date de relecture : 3 mois plus tard.
