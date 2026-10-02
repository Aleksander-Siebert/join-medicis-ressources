# La routine, la liste de 10, le calendrier

## 1. La routine de 15 minutes (jours ouvrés)

D'après « Daily Engagement Routine » (Taplio, MIT), sans l'outil payant :

1. **Répondre sous ses propres posts** (5 min) : `/linkedin-reply`, en
   commençant par les prospects et les questions.
2. **3 à 5 commentaires utiles** (10 min) : `/linkedin-comment`, mode
   session, sur les posts de la liste de 10 d'abord.
3. Noter dans `journal.md` qui a été commenté (pour ne pas commenter les trois
   mêmes personnes tous les jours).

Les jours de publication, ajouter les **30 minutes bloquées** après le post
pour répondre aux premiers commentaires.

## 2. La liste de 10

| Groupe | Combien | Qui | Ce qu'on y fait |
|---|---|---|---|
| **Pairs** | 6 | même métier, même niveau, publient régulièrement | commentaires de fond, échanges ; ce sont eux qui répondent |
| **Portée** | 2 | une audience que l'utilisateur veut toucher | commentaires tôt (les premiers sont plus lus), une idée nette |
| **Acheteurs** | 2 | des personnes qui pourraient acheter | commentaires de relation pendant des semaines, aucun pitch ; puis `/linkedin-dm` |

Sources et arbitrage :

- Jake Schincariol (li-plan, MIT) : 5 de portée, 3 pairs, 2 acheteurs.
- Serge Bulaev (linkedin-content-planner, MIT) : commentaires répartis 70%
  pairs, 20% aspirationnels, 10% prospects.
- Pack : 6, 2, 2. Les pairs d'abord, comme chez Serge, mais 2 acheteurs
  plutôt qu'1 pour que la liste serve l'objectif commercial.

Revoir la liste chaque mois : retirer qui ne publie plus, qui ne répond
jamais, qui n'est plus dans la cible.

Les « commentaires de premier arrivé » sous les gros comptes, chronométrés à
10 minutes, ne sont pas repris : coûteux, et aucune donnée publique ne mesure
leur effet **[praticien]**.

## 3. Semaine minimale et reprise

| Situation | Semaine |
|---|---|
| Moins de 90 minutes (mauvaise semaine) | 1 post texte, 1 commentaire par jour ouvré, réponses sous 24 h (`/linkedin-strategie`, `budget.py`) |
| Reprise après 3 semaines ou plus | semaine 1 : commentaires seuls ; semaine 2 : 1 post ; semaine 3 : rythme normal |
| Moins d'environ 1 000 abonnés | plus de temps à commenter qu'à publier (60% du budget, `budget.py`) |

## 4. Le calendrier français

`semaine.py` calcule les jours fériés (dont lundi de Pâques, Ascension,
lundi de Pentecôte) et les ponts (férié un jeudi : vendredi ; un mardi :
lundi). Il signale aussi août et la fin décembre. Ce sont des semaines où
l'audience B2B lit moins **[praticien]** : alléger, ou garder des posts qui
vieillissent bien.

Hors de France, l'utilisateur donne le calendrier de son audience (Belgique,
Suisse, Québec) : le script ne le connaît pas.

## 5. Quand publier, ce que disent les sources

| Affirmation | Niveau |
|---|---|
| Mardi à jeudi matin, heures de bureau | étude tierce (éditeurs), contredite par d'autres études qui placent le pic en fin d'après-midi |
| Les 60 à 90 premières minutes sont corrélées à la portée finale | étude tierce, corrélation (`commun/preuves.md`) |
| « Golden hour » avec une coupure précise | folklore |
| Le meilleur créneau d'un compte se mesure sur ce compte | méthode du pack (`/linkedin-audit`, au moins 10 posts) |
