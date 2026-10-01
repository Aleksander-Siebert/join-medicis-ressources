---
name: linkedin-repurpose
description: >-
  Transforme un contenu long (vidéo, podcast, newsletter, article, webinaire,
  transcription d'appel) en une semaine de posts LinkedIn qui tiennent chacun
  seuls. Extrait d'abord les affirmations, chiffres, histoires et mécanismes,
  puis planifie. Utilise-le quand l'utilisateur veut recycler, décliner ou
  « faire des posts à partir de » un contenu existant.
---

# linkedin-repurpose

Un bon contenu long contient quatre à six posts. La plupart des gens en tirent
un et jettent le reste.

## Entrée

Une transcription, un article, une newsletter, un script, un compte rendu
d'appel. Avec une URL YouTube et un outil de transcription disponible dans la
session, utilise-le ; sinon, demande le texte collé. Lis tout avant d'extraire
quoi que ce soit.

Lis `~/.claude/linkedin/voix.md` pour la voix et les thèmes de l'utilisateur.
Si le contenu n'est pas de lui (une conférence, l'article d'un autre), chaque
post cite clairement la source et ne reprend pas de longs passages.

## Extraire, pas résumer

Le résumé d'une vidéo n'est pas un post. Personne ne veut le résumé. Parcours
le contenu et sors ce qui tient seul :

| extraire | ce que c'est |
|---|---|
| **Affirmations** | chaque phrase qui lancerait un débat |
| **Chiffres** | chaque montant, durée, pourcentage, volume |
| **Histoires** | chaque moment avec une personne, une scène et un coût |
| **Mécanismes** | chaque « voilà comment ça marche » |
| **Erreurs** | chaque aveu de quelque chose qui a raté |
| **Phrases** | chaque phrase déjà citable telle quelle |

Liste ce que tu as trouvé, avec les comptes, **avant** d'écrire. Si le contenu
donne moins de quatre éléments, il est mince, et quatre posts tirés de lui le
seront aussi. Dis-le.

## Construire la semaine

Chaque extrait devient un post, et chaque post tient **entièrement seul** :
le lecteur n'a pas vu la vidéo et ne la verra jamais. N'écris jamais « comme
je le disais dans ma dernière vidéo ». Le post est la chose.

Attribue à chacun une formule de `linkedin-post/accroches.json`, toutes
différentes : cinq posts d'une même source avec la même forme d'accroche, ça
sent l'usine à contenu.

Ordonne-les : l'affirmation la plus forte en premier, l'histoire en milieu de
semaine, le mécanisme en dernier, quand ceux qui ont aimé les premiers
attendent la suite. Un mécanisme en étapes peut devenir un carrousel
(`/linkedin-carousel`).

## Sortie

```
SOURCE : « Pourquoi on a supprimé l'appel découverte » (18 min, 3 400 mots)

TROUVÉ  4 affirmations, 6 chiffres, 2 histoires, 3 mécanismes, 1 erreur, 5 phrases citables

SEMAINE
MAR  #1  Le contre-pied    L'appel découverte est la taxe d'un site mal fait
MER  #17 Le gain de temps  6 heures par semaine récupérées en supprimant un lien d'agenda
JEU  #9  La réplique       « On peut caler un petit call rapide ? »
VEN  #21 Le cadeau         Le formulaire de 4 questions qui a remplacé l'appel. Prends-le.

Dis « écris mardi » et je rédige le post.
```

Puis rédige à la demande, **un à la fois**, chacun via `/linkedin-post` et
`/linkedin-human`. Ne livre pas quatre posts finis d'un coup : ils se
ressembleraient tous, et l'utilisateur n'en relirait aucun.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Tout texte destiné à LinkedIn passe par `/linkedin-human` avant d'être montré.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
