# Des mesures aux traits

`voix.py` mesure ; le Skill juge. Cette page dit comment passer de l'un à
l'autre sans rien inventer.

## 1. Lire la sortie de voix.py

| Mesure | Ce qu'elle dit | Comment l'écrire dans le fichier |
|---|---|---|
| Phrase médiane, écart-type | rythme : court et sec, posé, mêlé | « Phrases courtes, 8 mots en médiane ; une plus longue pour raconter. » |
| Part de phrases de 8 mots ou moins, de 25 ou plus | phrases sèches, phrases longues | nuance la consigne de rythme |
| Paragraphes d'une phrase | mise en page aérée (LinkedIn) ou en blocs | section 4, « Paragraphes » |
| Ponctuation classée jamais / rare / habituelle | ce qui fait partie de la voix ; « jamais » vaut règle | section 4 et 6 ; un « jamais » de `voix.py` est une règle justifiée |
| Adresse par texte | tu ou vous, et s'il varie selon le canal | section 4 et 8 |
| je / on / nous pour 1000 mots | qui parle : la personne, l'équipe, l'institution | section 4 |
| « ça » ou « cela », négation sans « ne » | registre parlé ou écrit | curseur formel / décontracté |
| Chiffres pour 100 mots | goût du concret | trait « concret » s'il dépasse 2 [heuristique maison] |
| Marques d'oral, anglicismes | tics à garder, mots du métier | section 5 |
| Mots et expressions présents dans plusieurs textes | vocabulaire et phrases signatures | section 5 ; une expression d'un seul texte n'est pas une signature |
| Ouvertures et fins | entrée en matière, chute | section 4 |
| Espace avant « : ; ! ? », pourcentage espacé ou collé | habitude typographique | à noter ; la règle du fichier reste la typographie française, sauf choix contraire |

Une mesure absente (`n.d.`) n'a pas de sens sur ce corpus (trop peu de
phrases) : ne pas la remplacer par une estimation.

**Sans exécution de code.** Relever à la main, sur 3 textes au moins : nombre
de mots de 10 phrases prises au hasard (médiane), présence ou absence de
chaque ponctuation du tableau, tu ou vous, « ça » ou « cela ». Écrire dans
le fichier « mesures estimées à la main » et laisser le bloc de la section 12
vide, à remplir dès qu'un outil le permet.

## 2. Comparer avec l'IA par défaut

C'est l'étape qui trouve les traits (méthode comparative d'athola, scribe,
MIT, réécrite).

1. Prends le sujet de 2 textes différents (par exemple « un sinistre traité
   vite », « une erreur de l'équipe »).
2. Écris pour chacun 3 à 5 lignes comme une IA les écrirait sans consigne.
3. Mets-les à côté des textes réels, sans dire lequel est lequel dans ta tête :
   lis seulement les différences.
4. Liste ce que la personne fait autrement, en 6 familles :
   - **structure** : par quoi elle commence, comment elle finit, où arrive
     le fait important ;
   - **arguments** : chiffre, anecdote, comparaison, aveu ;
   - **engagement** : où elle tranche, où elle nuance, comment elle dit
     une erreur ;
   - **phrase** : longueur, fragments, questions, incises ;
   - **mots** : concrets ou abstraits, métier ou grand public, mots
     qu'elle aime ;
   - **négations** : ce qu'elle ne fait jamais alors que l'IA le fait
     (exclamations, « n'hésitez pas », triades d'adjectifs).

Les négations sont souvent les plus utiles : une IA reproduit mal ce qu'on
lui dit de faire, mais respecte bien ce qu'on lui interdit.

## 3. Écrire des traits qui servent

Format : **Je suis X, pas Y** + consigne + citation exacte.

- **X** : le trait ; **Y** : l'excès du même trait (concrète, pas
  technique ; franche, pas dure). Le « pas » dit où s'arrêter.
- **Consigne** : ce qu'on fait, pas ce qu'on observe. « Donne l'heure, le
  délai, le nombre » plutôt que « tend à utiliser des chiffres ».
- **Citation** : recopiée mot pour mot d'un texte. Pas de citation, pas de
  trait.

**Test de spécificité** (d'après athola et rampstack, MIT). Refuse un trait
s'il pourrait décrire la moitié des gens qui écrivent. Formules refusées
d'office :

- « professionnel mais accessible », « bienveillant », « authentique » ;
- « ton conversationnel », « engageant », « dynamique » ;
- « varie la longueur des phrases », « équilibre formel et informel » ;
- « tend à », « utilise souvent », « crée un sentiment de ».

Remplace par ce que la personne fait précisément : « commence par l'heure ou
le jour », « dit l'erreur dans la première phrase ».

**Test de résistance** (facultatif, d'après rampstack). Note un texte d'une
autre personne du même métier avec les traits. S'il obtient la même note,
les traits ne distinguent rien : resserre-les.

## 4. Zones où l'on tranche

D'après brianrwagner/voice-extractor (licence MIT annoncée), réécrit.

| Zone | Ce qu'on y lit | Exemple Assurly |
|---|---|---|
| Je tranche | aucune précaution, phrases affirmatives | délais de l'équipe, erreurs d'Assurly |
| Je parle d'expérience | « chez nous », « ce qu'on voit » | ce que vivent les artisans |
| J'explore | « on teste », « je vous redis » | les changements en cours |

Une IA met des précautions partout ou nulle part ; ce tableau lui dit où.

## 5. Confiance

| Niveau | Corpus | Ce qu'on fait |
|---|---|---|
| faible | moins de 500 mots, ou 1 seul texte | profil provisoire, plus de questions, recalcul demandé dans « Questions ouvertes » |
| moyenne | 500 à 1 500 mots, ou 2 textes | profil utilisable, rythme indicatif |
| bonne | plus de 1 500 mots et 3 textes au moins | profil fiable |

Seuils maison, tirés des minimums des références (500 mots chez athola et
brianrwagner) et adaptés à des posts courts. La confiance est écrite en tête
du fichier : tout Skill qui lit la voix sait ce qu'elle vaut.

## 6. Ce qui n'entre pas dans le fichier

- Ce qui tient au sujet et pas à la voix (le vocabulaire de l'assurance
  n'est pas un trait, la façon d'en parler en est un).
- Les tics de plateforme subis (hashtags imposés, sauts de ligne de
  LinkedIn) : ils vont dans la ligne du canal, pas dans les traits.
- Les fautes de frappe.
- Ce que la personne voudrait être sans le faire : voir « Vers où je veux
  aller » dans `references/format.md`.
