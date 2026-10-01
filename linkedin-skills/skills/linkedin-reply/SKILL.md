---
name: linkedin-reply
description: >-
  Répond aux commentaires sous les posts de l'utilisateur : trie chaque
  commentaire (prospect, fond, pair, soutien, bruit) avant d'écrire, puis
  rédige les réponses dans cet ordre. Utilise-le quand l'utilisateur colle les
  commentaires de son post, demande « que répondre », « aide-moi à gérer mes
  commentaires » ou veut traiter un fil après publication.
---

# linkedin-reply

Le fil sous un post de l'utilisateur, c'est là que se joue la diffusion.
Chaque réponse est un nouvel engagement sur le post, et les réponses de la
première heure font l'essentiel du travail. **[estimation de praticien]**
Mais tous les commentaires ne se valent pas : ce Skill trie avant d'écrire.

## Entrée

L'utilisateur colle les commentaires, idéalement avec noms et rôles. Les
captures d'écran conviennent. Ne parcours jamais le fil avec un navigateur.

Lis `~/.claude/linkedin/voix.md` pour le ton, l'offre et ce que l'utilisateur
vend : c'est ce qui permet de reconnaître un prospect.

## Trier d'abord

Range chaque commentaire dans une des cinq catégories et annonce les comptes :

| catégorie | ce que c'est | ce qu'il reçoit |
|---|---|---|
| **PROSPECT** | quelqu'un qui décrit le problème que l'utilisateur résout | une vraie réponse + une porte ouverte discrète |
| **FOND** | apporte une donnée, conteste, prolonge | la réponse la plus longue du fil |
| **PAIR** | un nom à côté duquel il est bon d'être vu | une réponse qui lui apporte quelque chose |
| **SOUTIEN** | « Super post », 🔥, une identification | un like, et 3 à 8 mots au plus |
| **BRUIT** | démarchage, spam, mauvaise foi | rien, ou une ligne et on sort |

Puis écris dans cet ordre, et arrête-toi quand la valeur s'arrête.

## Comment répondre

- **Répondre à la vraie question.** Si on demande comment, dis comment, dans
  la réponse. N'envoie pas en message privé une réponse qui tenait ici.
- **Le prénom une fois**, au début, jamais suivi d'un point d'exclamation.
- **Même longueur que le commentaire.** Deux lignes n'appellent pas six lignes.
- **À un critique** : concède d'abord ce qui est vrai, avec ses mots, puis
  tiens ta position sur le reste. Ne supprime pas, ne te défends pas, ne
  réponds jamais deux fois dans le même échange.
- **À un prospect** : réponds entièrement en public. La porte ouverte tient en
  une phrase, à la fin, et c'est une offre d'aide, pas un argumentaire. La
  valeur donnée en public fait venir le prochain en message privé.
- **À un démarchage dans tes commentaires** : ignore-le. Lui répondre lui
  donne de la portée.
- **Tutoiement ou vouvoiement** : celui du commentaire.

## Sortie

Un seul bloc, groupé par catégorie, chaque réponse prête à copier et déjà
passée par `/linkedin-human` :

```
RÉPONSES  ·  17 commentaires  ·  1 PROSPECT, 3 FOND, 4 PAIR, 8 SOUTIEN, 1 BRUIT

PROSPECT
@Sarah Martin, « on a le même problème avec nos devis »
> Ce qui a tout débloqué chez nous : sortir la grille tarifaire du document et
> l'envoyer comme une page à part. Un tour de relecture en moins. Je peux
> t'envoyer le modèle si ça t'aide.

FOND
@Marc Weber, conteste le rythme de publication
> Juste, et 4 posts par semaine n'ont marché que parce que j'avais 8 mois de
> posts derrière moi. En partant de zéro, je ferais comme tu dis.

SOUTIEN  (like à tous, réponse aux trois premiers)
@Dan, « Top » -> Merci Dan.
...

BRUIT  (1)
Ignoré : un démarchage d'agence. Y répondre lui donne de la portée.
```

Puis la règle : **rien n'est publié tant que l'utilisateur n'a pas dit oui.**
Il colle les réponses lui-même.

## Fin de tâche

Si un PROSPECT apparaît, propose `/linkedin-dm` pour la suite en privé, et propose
d'ajouter son nom au journal (`~/.claude/linkedin/journal.md`) pour ne pas le
perdre.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Tout texte destiné à LinkedIn passe par `/linkedin-human` avant d'être montré.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
