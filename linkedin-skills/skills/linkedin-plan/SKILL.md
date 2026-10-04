---
name: linkedin-plan
description: >-
  Planifie la semaine LinkedIn à partir de la stratégie et de ce qui s'est
  passé : ne demande que ce qui change chaque semaine, choisit pour chaque
  créneau un angle précis (pas un sujet), une formule de /linkedin-post, un
  objectif, un pilier et un format ; contrôle par script (aucune formule
  répétée en 7 jours, aucun pilier au-delà de 60% sur 4 semaines, objectifs
  variés, formule écartée par l'audit jamais reprogrammée, jours fériés et
  ponts français, temps nécessaire contre budget), bloque le créneau de
  réponse, liste de 10 personnes (6 pairs, 2 de portée, 2 acheteurs),
  routine de 15 minutes, semaine minimale et reprise après une pause, export
  CSV ou JSON pour Notion ou un tableur. Utilise-le pour « quoi poster cette
  semaine ? », « mon plan LinkedIn », « calendrier de la semaine ». Pas pour
  la stratégie à 90 jours (/linkedin-strategie), ni pour écrire les posts
  (/linkedin-post). Ne programme rien.
---

# linkedin-plan

La stratégie dit où aller sur 90 jours ; le plan dit quoi faire cette
semaine. À lancer une fois par semaine, le même jour. Il tient en un écran,
part de ce qui s'est vraiment passé, et se contrôle par script pour ne pas
répéter ce qui vient d'être fait ou ce qui a déjà échoué.

**À lire avant de commencer :** `commun/regles.md`.

## 1. Lire, puis demander une seule chose

Lis :

- `contexte.md` : objectif à 90 jours, piliers et leurs parts, rythme et
  budget en minutes (écrits par `/linkedin-strategie`), offres ;
- `journal.md` : les posts des 4 dernières semaines (formule, objectif,
  pilier), les idées déjà utilisées ;
- `apprentissages.md` : ce qui marche, ce qui ne marche pas, l'expérience en
  cours ;
- `reserve.md` : la matière (chiffres, histoires, avis).

**Sans stratégie** (pas de piliers, pas de rythme) : propose
`/linkedin-strategie` d'abord. Si l'utilisateur veut un plan tout de suite,
pars sur la semaine minimale (section 5) et dis-le.

Puis **une seule question** (d'après Joshua, di-li-plan, MIT) :

> Qu'est-ce qui s'est passé cette semaine ? Un appel client, un chiffre, une
> erreur, un désaccord, quelque chose de construit ou de lu.

Le reste, tu l'as déjà. Si la réponse est maigre, puise dans `reserve.md`
(éléments pas encore utilisés d'après `journal.md`) ou propose
`/linkedin-interview` en mode « post ».

## 2. Construire la semaine

**Nombre de posts** : celui de `contexte.md`. À défaut, 2 à 3 pour une
personne, et jamais plus que ce que le budget permet (section 4). La
régularité est un plancher, pas un objectif : le post de trop est presque
toujours le faible.

Pour chaque créneau :

| Champ | Règle |
|---|---|
| **angle** | ce qui s'est passé, le chiffre, la scène. « L'IA » n'est pas un angle ; « le devis perdu à cause d'un tiret cadratin » en est un |
| **objectif** | commentaires, partages, réactions ou sauvegardes ; **au moins 3 objectifs différents** pour 3 posts ou plus |
| **formule** | un `id` de `linkedin-post/formules.json` qui sert cet objectif ; **jamais deux fois en 7 jours** ; jamais une formule de « Ce qui ne marche pas pour moi » |
| **pilier** | selon les parts de la stratégie ; **aucun au-delà de 60%** sur 4 semaines |
| **format** | texte, image, carrousel (`/linkedin-carrousel`), vidéo, sondage ; le visuel se demande dès le lundi |
| **jour et heure** | voir « Quand » ; deux posts jamais le même jour |
| **créneau de réponse** | 20 minutes bloquées après la publication (`/linkedin-reply`) |

**Expérience en cours** (`apprentissages.md`) : programme la variante prévue
cette semaine, en alternant A et B, sans changer d'autre variable. C'est elle
qui fait avancer `/linkedin-audit`.

**Offre** : un post qui parle de l'offre au plus toutes les deux semaines,
seulement si `contexte.md` en a une marquée LIVE.

**Prêt à recevoir des demandes ?** (d'après le « Weekly Inbound-Readiness
Check » de Serge Bulaev, MIT, ramené sur deux semaines) : au moins un post de
preuve (un chiffre, un relevé), un post de vécu (une erreur, une scène), et
un post avec un appel à l'action vers l'offre. Les variantes « commente X
pour recevoir » de la source sont écartées (`commun/garde_fou.py`, E2).

## 3. Quand publier

**Le jour et l'heure comptent bien moins que la première ligne.** Les études
d'éditeurs se contredisent (matin en semaine pour les unes, fin d'après-midi
pour les autres) **[étude tierce, contradictoire]**. Ordre de décision :

1. le meilleur créneau mesuré par `/linkedin-audit` sur le compte, s'il
   existe (au moins 10 posts) ;
2. sinon, les heures de bureau de l'audience, dans **son** fuseau (Québec,
   Belgique, Afrique francophone) ;
3. et rester constant quelques semaines : on ne mesure rien en changeant tout.

Calendrier français (le script le signale) : jours fériés, ponts, août, fin
décembre. Ces semaines-là, alléger ou passer en semaine d'engagement.

## 4. Contrôler (script)

```
python3 scripts/semaine.py --plan plan.json --journal ~/.claude/linkedin/journal.md \
  --apprentissages ~/.claude/linkedin/apprentissages.md --minutes {{budget de la semaine}}
```

| Niveau | Contrôle |
|---|---|
| BLOQUANT | formule écartée par l'audit ; même formule en 7 jours (journal compris) ; pilier au-delà de 60% sur 4 semaines ; formule inconnue ; temps au-delà du budget |
| ATTENTION | moins de 3 objectifs pour 3 posts ou plus ; objectif que la formule ne sert pas ; deux posts le même jour ; même objectif deux jours de suite ; angle vague ; jour férié, pont, août, fin décembre ; liste d'engagement incomplète ou sans acheteur |

Le temps se compte avec les coûts de `/linkedin-strategie` : rédaction selon
le format, plus 20 minutes de réponses par post, plus 15 minutes de routine
par jour ouvré.

Le format de `plan.json` est en tête du script ; un exemple complet est dans
`assets/plan-exemple.json`.

## 5. L'engagement de la semaine

Détail dans `references/routine.md`.

- **Routine de 15 minutes par jour ouvré** (d'après Taplio, MIT) : d'abord
  répondre sous ses propres posts (`/linkedin-reply`), puis 3 à 5
  commentaires utiles (`/linkedin-comment`).
- **Liste de 10 personnes**, revue chaque mois : **6 pairs** (même métier,
  même niveau), **2 de portée** (audience que l'utilisateur veut toucher),
  **2 acheteurs** (à commenter des semaines avant tout message). Arbitrage
  entre Jake Schincariol (5 de portée, 3 pairs, 2 acheteurs) et Serge Bulaev
  (70% pairs, 20% aspirationnels, 10% prospects) : les pairs d'abord, parce
  que ce sont eux qui répondent.
- « Commenter juste avant de publier pour chauffer l'algorithme » : écarté,
  aucune donnée ne le soutient **[folklore]**.

**Semaine minimale** (mauvaise semaine, moins de 90 minutes) : 1 post texte,
1 commentaire utile par jour ouvré, réponse à chaque commentaire sous 24 h.

**Reprise après 3 semaines ou plus sans rien** (pratique du pack) : une
semaine de commentaires seuls, puis 1 post la semaine suivante, puis le
rythme normal.

## Sortie (format fixe)

```
SEMAINE DU {{lundi}} · {{n}} posts · environ {{m}} min sur {{budget}} · contrôle {{PRÊT|À REVOIR}}

{{JOUR}}  {{heure}}  {{OBJECTIF}}  {{formule}}  [{{pilier}} · {{format}}]
      angle : {{angle}}
      réponses : {{heure + 20 min}}
…
ROUTINE  15 min par jour ouvré : répondre, puis 3 à 5 commentaires
LISTE    6 pairs · 2 de portée · 2 acheteurs  (inchangée | à revoir le {{date}})
À PRÉPARER LUNDI  {{visuels, chiffres à vérifier, éléments {{à compléter}}}}
EXPÉRIENCE  {{variante A/B de la semaine, ou aucune}}

Dis « écris mardi » et /linkedin-post rédige le post de mardi.
```

Rien n'est programmé ni publié. L'utilisateur peut programmer lui-même avec
le planificateur intégré de LinkedIn. Pour Notion ou un tableur :

```
python3 scripts/semaine.py --plan plan.json --export csv   # ou json
```

Sur « ok », rien n'est écrit : chaque post entre dans `journal.md` quand il
est publié (`/linkedin-post`). Si l'utilisateur raye une règle (« jamais le
vendredi »), propose une ligne dans `apprentissages.md`, avec son accord.

## Erreurs et cas limites

| Cas | Ce qu'on fait |
|---|---|
| Rien ne s'est passé cette semaine | puiser dans `reserve.md` ; sinon un post de leçon ou d'avis, ou une semaine d'engagement |
| `journal.md` vide | le contrôle des 7 jours et des piliers ne porte que sur la semaine ; le dire |
| Formule voulue déjà utilisée il y a 5 jours | une autre formule pour le même objectif (`formules.json`) |
| Semaine de 3 jours fériés | 1 post, ou engagement seul |
| Plusieurs voix (dirigeant, page, salariés) | un plan par voix ; la page et les ambassadeurs : `/linkedin-entreprise` |

## Ressources

- `scripts/semaine.py` : contrôle, calendrier français, export.
- `assets/plan-exemple.json` : un plan qui passe le contrôle.
- `references/routine.md` : routine, liste de 10, reprise, calendrier.
- `references/exemple.md` : une semaine complète.

## Skills liés

- `/linkedin-strategie` : piliers, rythme, budget (avant le premier plan).
- `/linkedin-post` : écrit chaque créneau.
- `/linkedin-comment`, `/linkedin-reply` : la routine.
- `/linkedin-audit` : ce qui marche, l'expérience en cours.
