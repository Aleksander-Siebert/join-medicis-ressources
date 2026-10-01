---
name: li-plan
description: >-
  Planifie la semaine LinkedIn : quoi publier (et sous quel angle), quand, et
  les dix personnes avec qui interagir. Écrit ~/.claude/linkedin/plan.md, que
  les autres Skills du pack relisent. Utilise-le quand l'utilisateur demande un
  calendrier éditorial, « quoi poster cette semaine », un plan de contenu
  LinkedIn, ou veut organiser sa routine.
---

# li-plan

La salle de contrôle. Les autres Skills exécutent ; celui-ci décide quoi
exécuter. À lancer une fois par semaine, toujours le même jour.

## Entrée

Lis `~/.claude/linkedin/voix.md`, `journal.md` et, s'il existe, le dernier
rapport de `/li-audit` : le plan ne doit pas répéter un thème des quinze
derniers jours, et il s'appuie d'abord sur ce qui a marché pour ce compte.

S'il manque quelque chose, demande en une fois :

1. Ce que l'utilisateur vend, et à qui.
2. Les trois ou quatre thèmes pour lesquels il veut être reconnu.
3. **Ce qui s'est vraiment passé cette semaine** : un appel client, un
   chiffre, une erreur, un truc construit, un désaccord. C'est de là que
   viennent les posts.
4. Dix à vingt personnes ou entreprises auprès desquelles il veut être
   visible.

Si la semaine demandée est déjà passée, ou sans date précise, signale-le et
propose la prochaine semaine qui correspond.

## Quoi publier

Quatre posts par semaine valent mieux que sept. La régularité est un plancher,
pas un objectif, et le cinquième post de la semaine est presque toujours le
faible qui fait baisser la moyenne.

Varie dans la semaine, jamais deux fois le même type d'affilée :

| type | fréquence | rôle |
|---|---|---|
| **Preuve** | 1 par semaine | quelque chose qui s'est passé, avec un chiffre |
| **Opinion** | 1 par semaine | une position qui peut faire perdre des abonnés |
| **Leçon** | 1 par semaine | une chose que le lecteur peut faire aujourd'hui |
| **Histoire** | 1 tous les 15 jours | une scène, une réplique, un coût |
| **Offre** | 1 tous les 15 jours | ce que l'utilisateur vend, dit simplement, sans s'excuser |

Pour chaque créneau : le thème, **l'angle précis tiré de ce qui s'est passé
cette semaine**, le numéro de formule de `li-post/accroches.json` et le
format (texte, carrousel via `/li-carousel`, image). Pas un sujet, un angle.
« L'IA » n'est pas un plan. « Le devis qu'on a perdu parce que notre
brouillon IA avait un tiret cadratin » est un post.

## Quand publier

Publie quand l'audience est à son bureau. Pour une audience B2B en France,
**mardi à jeudi, 7 h 30 - 9 h 30 heure de Paris**, est la base de travail, avec
le lundi après-midi et le vendredi matin en second choix. Le week-end, des
histoires personnelles ou rien. **[données à grande échelle, éditeurs,
contradictoires : d'autres études donnent 17 h - 18 h]**

Spécificités françaises : l'audience B2B fond en **août** (15 août férié),
entre Noël et le Nouvel An, et pendant les **ponts de mai**. Allège ces semaines-là ou passe en
mode engagement seul.

Mais dis-le clairement : **le jour et l'heure comptent bien moins que la
première ligne.** Si l'utilisateur optimise ses horaires avant que ses
accroches fonctionnent, il polit la mauvaise pièce. Dis-le-lui.

Cale les horaires sur le fuseau de l'audience, pas sur celui de
l'utilisateur, s'ils diffèrent (Québec, Belgique, Afrique francophone).

## Avec qui interagir

Une liste de 10, en trois groupes :

- **5 de portée** : des personnes dont l'audience intéresse l'utilisateur, et
  sous les posts desquelles il peut vraiment apporter quelque chose. Commenter
  avant qu'il y ait 20 commentaires, sinon personne ne voit.
- **3 pairs** : même niveau, même métier. Le groupe qui rend la pareille.
- **2 acheteurs** : des personnes qui pourraient vraiment acheter. Commenter
  leurs posts pendant des semaines avant tout message privé, et ne jamais
  vendre en commentaire.

Vingt minutes par jour, **avant** de publier, pas après. Ce sont les
commentaires sous les posts des autres qui font porter ceux de l'utilisateur.
`/li-comment` les écrit.

## Sortie

```
SEMAINE DU 8 SEPTEMBRE

LUN  engagement seul  (20 min, liste ci-dessous)
MAR  8 h 15  PREUVE    #17 Le gain de temps   le devis passé de 5 h à 20 min
MER  engagement seul
JEU  8 h 00  OPINION   #1  Le contre-pied     pourquoi on a supprimé l'appel découverte
VEN  8 h 30  LEÇON     #21 Le cadeau          le mail de relance en 4 lignes, offert
SAM  -
DIM  16 h 00 HISTOIRE  #9  La réplique        le mail « on part sur moins cher »

ENGAGEMENT  (5 portée / 3 pairs / 2 acheteurs)
  ...

Dis « écris mardi » et je rédige le post.
```

Écris le plan dans `~/.claude/linkedin/plan.md` pour que les autres Skills le
lisent. Sans accès aux fichiers, donne le bloc à garder dans le Projet. Rien
n'est programmé ni publié nulle part : c'est un plan, l'utilisateur le suit.

## Fin de tâche

Si l'utilisateur raye un type de post ou un horaire (« je ne publie jamais le
dimanche »), propose de le noter dans `apprentissages.md`, avec son accord.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Tout texte destiné à LinkedIn passe par `/li-human` avant d'être montré.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
