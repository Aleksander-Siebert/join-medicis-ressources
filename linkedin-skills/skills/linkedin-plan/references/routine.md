# La routine, la liste de 10, le calendrier

## 1. La routine de 15 minutes (jours ouvrés)

D'après « Daily Engagement Routine » (Taplio, MIT), sans l'outil payant :

1. **Répondre sous ses propres posts** (5 min) : `/linkedin-reply`, en
   commençant par les prospects et les questions.
2. **3 à 5 commentaires utiles** (10 min) : `/linkedin-comment`, mode
   session, sur les posts de la liste de 10 d'abord.
3. Noter dans `journal.md` qui a été commenté (pour ne pas commenter les trois
   mêmes personnes tous les jours).

Les jours de publication, ajouter les **20 minutes bloquées** après le post
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
| Mercredi 15 h-16 h et jeudi 15 h-17 h, heure locale de l'audience ; pas le week-end | étude tierce : Sprout Social (31 mars 2026) et Buffer (9 sept. 2026) se recoupent là (`commun/preuves.md`) |
| Mardi à jeudi, 7 h 30-9 h 30 | **dépassé** : conseil par défaut de la v1 du pack, retiré le 14 oct. 2026 ; aucune étude de 2026 ne place le pic le matin |
| Le pic s'étend jusqu'à 20 h | une seule étude (Buffer 2026) ; Sprout s'arrête vers 17 h |
| Les 60 à 90 premières minutes sont corrélées à la portée finale | étude tierce, corrélation (`commun/preuves.md`) |
| « Golden hour » avec une coupure précise | folklore |
| Le meilleur créneau d'un compte se mesure sur ce compte | méthode du pack : heure notée dans `journal.md`, attribut `creneau` de `/linkedin-audit`, au moins 5 posts par créneau |

### Le test à deux créneaux

1. Choisis deux créneaux le même jour de la semaine (ex. jeudi 8 h 30 et
   jeudi 15 h) : seule l'heure change.
2. Calcule la durée avant de commencer :

   ```
   python3 ../linkedin-audit/scripts/audit.py experience --hypothese "15 h fait mieux que 8 h 30" \
     --variable "heure" --cv 0.45 --effet 0.30 --posts-semaine 2
   ```

   Résultat réel (14 oct. 2026) : `TROP LONG`, 28 posts par variante, environ
   28 semaines ; en 12 semaines, seul un écart d'au moins 46% se verrait. Le
   test ne vaut que pour un compte qui publie souvent, ou si l'écart attendu
   est gros (un créneau où personne ne lit).
3. Sinon : garde le point de départ, note l'heure réelle dans `journal.md`,
   et lance `audit.py motifs --journal …` tous les trimestres. Le créneau est
   testé en dernier, comme le jour.

## 6. Un post a floppé : avant d'accuser l'heure

Un post isolé ne prouve rien : sur LinkedIn, l'écart entre deux posts d'un
même compte dépasse souvent l'effet d'un créneau. Dans l'ordre :

| Vérification | Comment |
|---|---|
| Était-ce vraiment un flop ? | `audit.py decrire` : sous la bande « faible » de ses propres posts, pas sous les chiffres d'un autre compte |
| La première ligne | arrêtait-elle la lecture sans « voir plus » ? (`/linkedin-post`, mode « analyser ») |
| Un lien dans le corps du post | portée médiane plus basse selon une étude contestée (`commun/preuves.md`) : le lien va en commentaire |
| Les réponses dans la première heure | l'auteur était-il disponible pour répondre ? |
| L'heure, dans le fuseau de l'audience | publié tôt le matin, ou pendant les heures où l'audience ne lit pas ? |
| Le jour | férié, pont, veille de week-end prolongé, août ? (`semaine.py` le signale) |
| Le sujet | hors des piliers, ou trop loin de l'audience que le compte a construite ? |

Note la réponse dans `apprentissages.md` : un seul post ne change pas le
plan, trois posts du même type dans la bande « faible », si.
