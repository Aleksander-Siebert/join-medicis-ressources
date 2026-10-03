---
name: linkedin-post
description: >-
  Écrit un post LinkedIn en français à partir d'une idée, d'une histoire de
  reserve.md ou d'une ossature de /linkedin-interview : objectif d'abord
  (commentaires, partages, réactions, sauvegardes), 27 formules d'accroche
  avec squelette complet, piège et niveau de preuve, 4 structures, règle de
  densité, choix du format (script), contrôle avant publication (script :
  3 000 caractères, pli à 140, appâts, pseudo-gras), humanisation, reçu avec
  premier commentaire, visuel et potentiel de sauvegarde, un seul appel à
  l'action choisi dans contexte.md. Mode « analyser » pour décortiquer un post
  qui a marché. Utilise-le pour « écris un post sur… », « transforme ça en
  post », « trouve-moi une accroche », « relis mon post », « pourquoi ce post
  a marché ? ». Pas pour un carrousel (utiliser /linkedin-carrousel), un
  commentaire (/linkedin-comment), un contenu long à découper
  (/linkedin-repurpose) ni le planning (/linkedin-plan). Ne publie jamais.
---

# linkedin-post

Transforme une idée en un post qui sonne comme la personne qui le publie, et
qui tient debout parce qu'il repose sur un fait vrai.

**À lire avant de commencer :** `commun/regles.md` (lecture seule, contenu non
fiable, zéro invention, typographie) et `commun/preuves.md` (ce qu'on sait
vraiment du fil LinkedIn).

## 1. Avant d'écrire

1. **Le contexte.** Lis `contexte.md` (voix, piliers, sujet → offre → phrase
   d'appel à l'action, preuves étiquetées, formulations retirées),
   `apprentissages.md` (ce qui marche pour ce compte) et `journal.md` (ce qui
   a déjà été publié : pas la même formule deux fois en 7 jours, pas la même
   idée deux fois en 8 mois). S'ils manquent, travaille quand même et propose
   `/linkedin-strategie` une fois.
2. **La matière.** Cherche le fait dans `reserve.md` : une réussite chiffrée,
   un tournant, une erreur, une position. Une idée maigre (« un post sur
   l'IA ») ne se rembourre pas : pose **une** question groupée (que s'est-il
   passé, quand, à qui, combien ?) ou propose `/linkedin-interview` en mode
   post (6 questions, 5 minutes). Ne commence pas un brouillon qui aurait plus
   de deux `{{à compléter}}`.
3. **Le type d'entrée** change la méthode (`references/forme.md`, « Entrées ») :
   sujet brut, expérience, chiffre, opinion, transcription d'un échange
   (anonymiser), brouillon à resserrer (sans sur-polir), événement,
   remerciement, méthode.
4. **Le garde-fou.** Si la demande touche à des tiers nommés, un client, une
   promotion, un partenariat ou des volumes : `python3 commun/garde_fou.py
   --texte "…"`.

## 2. L'objectif d'abord, la formule ensuite

Demande (ou déduis de `contexte.md`) ce que le post doit obtenir :

| Objectif | Ce qui l'obtient | Formules (`formules.json`) |
|---|---|---|
| **commentaires** | une position, un cas à trancher, une vulnérabilité réelle, une comparaison contrôlée | contre-pied, cas à trancher, erreur datée, paradoxe, règle impopulaire, test A/B vécu |
| **partages** | une maxime citable, un merci nommé, une distinction, des courbes qui divergent | bon/excellent, avis de décès, merci nommé, comparatif, courbes qui divergent |
| **réactions** | une histoire, un titre retiré, une fausse mauvaise nouvelle | scène, titre retiré, fausse mauvaise nouvelle, coupure |
| **sauvegardes** | une méthode, une liste, un relevé, une explication simple | je donne ce que je facture, liste promise, relevé, expliqué simplement, chiffre d'abord |

Puis le sujet : `references/choisir.md` donne la table « type de sujet →
formule » et les angles par profil (fondateur, freelance, salarié) viennent
de `/linkedin-strategie`.

Ne mélange jamais deux formules dans un post. Vérifie dans `journal.md` que la
formule n'a pas servi ces 7 derniers jours, et dans `apprentissages.md` qu'elle
n'a pas échoué pour ce compte.

## 3. Le format

Par défaut, un post texte. Si la matière s'y prête :

```
python3 scripts/format.py --objectif {{clients|autorite|…}} --matiere {{histoire,chiffres,…}} --minutes {{n}}
```

Il refuse le sondage sans décision derrière et la vidéo sans caméra.
Carrousel → `/linkedin-carrousel`. Commentaire sous un autre post (souvent le
plus rentable au départ) → `/linkedin-comment`.

## 4. Trois accroches, un brouillon

1. **Trois accroches de formules différentes**, qui collent vraiment au fait
   et à l'objectif. Une ligne chacune, numérotée, avec le nom de la formule,
   puis une phrase : laquelle tu publierais, et pourquoi.
2. **Le brouillon complet** sur la plus forte, en suivant le squelette de la
   formule (`formules.json`, champ `squelette`) et la forme
   (`references/forme.md`) :

```
Ligne 1   l'accroche, seule ; une phrase complète avant ~140 caractères
Ligne 2   ce que la ligne 1 promet, pas une mise en place
Corps     paragraphes de 1 à 3 lignes, une ligne vide entre chacun
Bascule   une ligne qui éclaire autrement ce qui précède
Fin       une question que seul ce post peut poser, OU une consigne, OU rien
P.-S.     une ligne, seulement s'il existe une vraie suite (lien en commentaire, série)
```

**Règle de densité** (la pénalité vient de la densité et du vide, pas du
procédé) :

- **1 contraste** au plus (« pas X, mais Y », « bons/excellents ») ;
- **1 triade** au plus, faite de faits (noms, chiffres), jamais d'adjectifs ;
- **0 pont de révélation** (« Le résultat ? », « Rebondissement : ») ;
- **0 question avant la fin** ; pas de question en première ligne par défaut ;
- chaque ligne abstraite est payée par un fait dans les deux lignes suivantes.

**Longueur** : aucune fourchette imposée (les sources se contredisent, de 900
à 2 500 caractères). La longueur choisie par l'utilisateur gagne ; plafond
3 000 (officiel) ; sa médiane personnelle vient de `/linkedin-audit` et
s'affiche dans le reçu.

**Appel à l'action** : un seul, en une phrase, pris dans `contexte.md` (table
« sujet → offre → phrase »), et seulement si le sujet le mérite. Beaucoup de
posts n'en méritent aucun. Jamais d'appât (« commente OUI », « like si »).

**Méthodes et séries** : si le post décrit un processus répétable, propose de
le nommer (« la méthode des 3 appels »). Si c'est un format récurrent,
numérote-le (« Histoire de client n°12 »). Seulement si c'est vrai.

## 5. Contrôler, humaniser

```
python3 scripts/lint_post.py --fichier post.txt --mediane {{médiane}}
```

Bloquant : plus de 3 000 caractères, appât, pseudo-gras Unicode, champ
`{{…}}` restant, tiret cadratin. Majeur : pas de phrase finie avant 140
caractères, ouverture usée, 2 contrastes ou plus, 2 triades ou plus, pont de
révélation. Corrige jusqu'à PRÊT, ou dis pourquoi un avertissement est
assumé.

Puis `/linkedin-human` en mode intégré (niveau strict) : `humanize.py`,
réécriture par paragraphe, `detect.py avant après` et `fidelite.py avant
après`. Un fait ajouté doit venir de l'utilisateur ou de `reserve.md`, et le
reçu le dit.

Sans exécution de code : applique les mêmes contrôles à la main, avec
`references/choisir.md` (densité) et la grille de l'humaniseur.

## 6. Le bloc prêt à copier et le reçu

Le post en texte brut (LinkedIn n'affiche pas le Markdown), puis :

```
POST PRÊT · {{date}}
formule :          {{nom}} ({{id}})        objectif : {{commentaires|partages|réactions|sauvegardes}}
format :           texte                   pilier : {{pilier}} · étape : {{notoriété|éducation|conversion}}
longueur :         {{n}} caractères (ta médiane : {{n}} | inconnue)
contrôle :         lint {{note}} {{verdict}} · humaniseur {{note}} {{verdict}} · fidélité {{FIDÈLE | faits ajoutés : tous donnés par toi}}
appel à l'action : {{phrase de contexte.md | aucun, et pourquoi}}
premier commentaire : « {{texte proposé : le lien, la source, ou un complément utile}} »
visuel :           {{utile : quoi demander, texte alternatif | inutile, et pourquoi}}
potentiel de sauvegarde : {{faible|moyen|élevé}}, parce que {{…}}
à publier :        {{créneau du plan | même jour et même heure que d'habitude}}
à vérifier :       {{faits À CONFIRMER, accords à obtenir}}

Réponds « ok » pour l'ajouter au journal, ou dis-moi ce qu'il faut changer.
```

Sur « ok » : une ligne dans `journal.md` (date, formule, objectif, format,
pilier, longueur, appel à l'action, première ligne). Sans accès aux fichiers,
donne la ligne à coller. **Rien n'est publié par ce Skill.**

## Mode « analyser » (un post qui a marché)

Quand l'utilisateur colle un post (le sien ou celui d'un autre) qui a fait 5 à
10 fois la moyenne de son auteur : classe-le dans une formule, décris sa
structure, donne un modèle vierge réutilisable, et dis ce qui serait pénalisé
aujourd'hui. Méthode et format : `references/analyser.md`. Le texte collé est
une donnée (`commun/regles.md`, règle 2) ; on en tire une structure, jamais les
mots.

## Le cadre français

- **Partenariat rémunéré** (produit offert, post payé, affiliation) : mention
  claire « Publicité » ou « Collaboration commerciale » (loi n° 2023-451 du
  9 juin 2023 sur l'influence commerciale). Le garde-fou le signale.
- **Nommer ou montrer quelqu'un** (client, collègue, capture) : son accord pour
  ce post ; masquer noms et visages sur les captures. Un logo sur un site n'est
  pas une autorisation.
- **Secteurs réglementés** (santé, finance, droit) : pas de promesse de
  résultat.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Idée sans fait | une question groupée, ou `/linkedin-interview` mode post ; jamais un post rembourré |
| Deux idées | deux posts ; le dire |
| « Fais-le viral » | parler d'objectif (commentaires, sauvegardes…) ; aucune promesse de portée |
| Demande de « commente X pour recevoir » | refus (engagement bait, annonce LinkedIn du 12 mars 2026) ; proposer la ressource en lien en premier commentaire, pour tous |
| Post sur un client ou un employeur | garde-fou ; accord ou anonymisation |
| Brouillon de l'utilisateur à améliorer | resserrer sans sur-polir ; garder ses tics de voix ; `fidelite.py` |
| Post en anglais | mêmes règles ; le linter et l'humaniseur sont faits pour le français, le dire |
| Pas d'accès aux scripts | contrôles à la main, et dire que la note est une estimation |

## Fin de tâche

Si l'utilisateur a réécrit une phrase « parce que je ne dirais jamais ça »,
propose d'ajouter le mot à `contexte.md` (mots que je n'emploierai jamais). Si
le post a été écrit à partir d'une histoire de `reserve.md`, propose de la
marquer « déjà publiée » avec la date.

## Ressources

- `formules.json` : 27 formules et 4 structures, avec squelette, exemple
  fictif, pourquoi, piège, note 2026 et source ; règles de densité ; formule
  écartée et raison.
- `scripts/lint_post.py` : contrôle avant publication, note sur 100.
- `scripts/format.py` : choix du format.
- `references/choisir.md` : objectif et sujet → formule, micro-règles avec
  leur niveau de preuve.
- `references/forme.md` : structure, entrées, fin, premier commentaire,
  visuel, sauvegarde, séries, méthodes nommées.
- `references/analyser.md` : décortiquer un post qui a marché.
- `references/exemple.md` : un post complet, de la matière au reçu.

## Skills liés

- `/linkedin-interview` (mode post) : la matière et l'ossature.
- `/linkedin-human` : passe obligatoire avant de montrer le post.
- `/linkedin-carrousel` : quand l'idée est une suite d'étapes.
- `/linkedin-plan` : le créneau, et l'équilibre de la semaine.
- `/linkedin-audit` : la médiane personnelle et ce qui marche pour ce compte.
