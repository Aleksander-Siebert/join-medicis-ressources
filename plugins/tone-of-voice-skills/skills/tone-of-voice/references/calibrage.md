# Calibrage : trois variantes, puis « c'est moi »

Les mesures et les questions donnent une voix plausible. Le calibrage la rend
juste : la personne ne décrit pas sa voix, elle la reconnaît.

## 1. Choisir le message

Un texte court que la personne a **vraiment** à écrire cette semaine : un
post, une réponse à un client, un message à l'équipe. 60 à 120 mots. Les faits
viennent d'elle (demande-les en une question) ; s'il en manque, écris
`{{à compléter}}` plutôt que d'en inventer.

## 2. Écrire trois variantes

Les trois respectent les traits et les « jamais ». Elles diffèrent sur **un
seul curseur à la fois**, celui sur lequel les textes et les réponses
hésitent le plus :

| Si l'hésitation porte sur… | Variante A | Variante B | Variante C |
|---|---|---|---|
| formel ↔ décontracté | phrases complètes, « cela », pas de tournure parlée | intermédiaire | « ça », négation sans « ne », une tournure parlée |
| factuel ↔ enthousiaste | faits seuls | un mot de sentiment | une phrase d'émotion assumée |
| court ↔ développé | 40 mots | 80 mots | 120 mots |
| direct ↔ amené | le fait en première phrase | une phrase de contexte d'abord | une anecdote d'abord |

Présente-les sans commentaire, étiquetées A, B, C. Question unique : « Laquelle
est la plus toi ? Et qu'est-ce qui cloche dans les autres ? »

## 3. Traduire les retours en réglages

| La personne dit | Réglage à écrire dans le fichier |
|---|---|
| « plus direct » | fait principal dans la première phrase ; supprimer les phrases de contexte ; curseur factuel −1 |
| « moins formel » | « ça » au lieu de « cela » ; une tournure parlée par texte ; curseur décontracté +1 |
| « trop familier » | négation complète (« ne… pas ») ; pas de tournure parlée dans les emails |
| « trop sec » | une phrase de lien ou de ressenti par paragraphe ; curseur enthousiaste +1 |
| « trop long » | longueur du canal réduite d'un tiers, dans la section 8 |
| « je ne dirais jamais ça » | l'expression va en section 6, entre « » en tête de ligne |
| « ça, c'est moi » sur une phrase | la phrase va en section 9 (après) ; si elle vient d'un vrai texte, en section 10 |

Applique, réécris la variante choisie, montre-la. **3 tours au plus** : au
quatrième, le problème vient d'ailleurs (traits mal posés, ou textes qui ne
reflètent pas la personne). Dis-le et reviens à l'analyse.

## 4. Test final « dans la voix / hors voix »

D'après la validation de brianrwagner et l'A/B de notque (MIT), réécrits.

Écris le même message deux fois : une version dans la voix, une version
générique (celle d'une IA sans consigne). Présente-les dans un ordre tiré au
hasard, sans les nommer. Question : « Lequel est toi, sans réfléchir ? »

- La personne choisit la bonne : la voix est prête.
- Elle hésite : demande ce qui la gêne dans chacune, retour à la section 3.
- Elle choisit la générique : la voix décrite n'est pas la sienne. Reviens aux
  textes : souvent, ils ont été retouchés par une IA ou par quelqu'un d'autre.

Après rédaction du fichier, vérifie la version dans la voix avec
`scripts/ecart.py` : elle doit sortir « DANS LA VOIX ». Sinon, c'est le
fichier qui contredit les textes : corrige le fichier, pas le texte.
