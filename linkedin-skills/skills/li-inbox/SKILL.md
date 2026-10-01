---
name: li-inbox
description: >-
  Trie la messagerie LinkedIn en cinq catégories (prospect, recruteur, pair,
  demande, spam), repère les séquences automatisées et rédige seulement les
  réponses qui valent la peine. Utilise-le quand l'utilisateur colle ses
  messages LinkedIn, veut « vider sa messagerie », « trier ses InMails » ou
  savoir à qui répondre en priorité.
---

# li-inbox

La plupart des messageries LinkedIn sont à 80 % du bruit, et ce bruit coûte
cher : les 20 % utiles restent une semaine sans réponse. Ce Skill les sépare,
puis n'écrit que ce qui mérite de l'être.

## Entrée

L'utilisateur colle les messages. Les captures conviennent. Ne te connecte
jamais à son compte et ne lis jamais sa messagerie avec un navigateur.

Lis `~/.claude/linkedin/voix.md` : ce qu'il vend et ce qu'il cherche (un job ?
des clients ?) décide de ce qui est un prospect ou une bonne offre.

## Cinq catégories

| catégorie | signal | action |
|---|---|---|
| **PROSPECT** | décrit un problème que l'utilisateur résout, ou parle de travailler ensemble | réponse aujourd'hui, complète |
| **RECRUTEUR** | un poste, une entreprise, une fourchette de salaire | réponse si le poste est réel, une ligne sinon |
| **PAIR** | quelqu'un du même métier avec quelque chose à dire | réponse cette semaine, simple et humaine |
| **DEMANDE** | veut un conseil, du temps, une mise en relation, un service | réponse si c'est rapide et précis, refus net sinon |
| **SPAM** | démarchage d'agence, séquence automatisée, crypto, « petite question » sans question | archiver, pas de réponse |

Affiche les comptes d'abord. Voir « 3 prospects, 2 recruteurs, 41 spams »,
c'est déjà l'essentiel de la valeur.

## Reconnaître une séquence

L'automatisation a une forme : une invitation sans rien de précis, un message
qui arrive quelques minutes après l'acceptation, « petite question », « j'ai
vu que vous étiez dans le secteur {secteur} », un lien d'agenda dès le
premier message, puis une relance quatre jours pile après. Quand tu la vois,
classe en SPAM et dis quel indice l'a trahie. L'utilisateur ne doit pas de
réponse à un script.

## Réponses

- **PROSPECT** : réponds à la vraie question du message, entièrement,
  gratuitement. Si c'est un bon client, l'offre tient en une phrase à la fin.
  Sinon, dis-le et oriente vers quelqu'un d'utile. Les deux issues sont bonnes.
- **RECRUTEUR** : si le poste intéresse vraiment, demande ce que le message a
  oublié : la fourchette de salaire (brut annuel), le niveau, le rythme sur
  site ou à distance, le type de contrat. Sinon, une ligne : pas en recherche,
  ravi de recommander quelqu'un, et le penser.
- **DEMANDE** : si ça prend moins de dix minutes et que c'est précis, fais-le.
  Si c'est « je peux te prendre 30 minutes pour échanger ? », refuse en une
  phrase chaleureuse et donne la réponse que tu aurais donnée pendant
  l'appel. C'est la version polie, et la plus utile.
- **REFUS** : courts, chaleureux, définitifs. Pas de « on en reparle au T3 »
  s'il n'y a pas de T3.

Vouvoiement ou tutoiement : celui du message reçu.

## Sortie

Groupé par catégorie, comptes en tête, brouillons seulement pour les
catégories qui reçoivent une réponse, chacun passé par `/li-human`. Puis la
règle : l'utilisateur envoie lui-même.

```
MESSAGERIE  ·  52 messages  ·  3 PROSPECTS, 2 RECRUTEURS, 4 PAIRS, 2 DEMANDES, 41 SPAMS

SPAM  (41) : à archiver. 38 suivent la même séquence : invitation sans
précision, « petite question » 4 minutes après l'acceptation, lien d'agenda
dès le premier message.
```

## Fin de tâche

Propose d'ajouter les prospects au journal (`~/.claude/linkedin/journal.md`)
avec la date et le sujet, pour que `/li-dm` reprenne le fil.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Tout texte destiné à LinkedIn passe par `/li-human` avant d'être montré.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
