# Les quatre passes, en détail

D'après le humanizer V3 de Serge Bulaev (MIT) et blader/humanizer v3.1
(MIT), adaptés au français et aux règles de l'utilisateur.

## Passe 1 · NETTOYER

### Automatique (humanize.py)

Rien de ce qui suit ne peut changer le sens :

| Avant | Après |
|---|---|
| `morte — elle a changé` | `morte, elle a changé` (jamais de point-virgule) |
| `— Premier point` · `une idée —` | `Premier point` · `une idée` |
| `15 %` | `15%` |
| `“on signe”` | `« on signe »` |
| `Résultat: 212 rendez-vous!` | `Résultat : 212 rendez-vous !` |
| `Etat des lieux` · `A propos` | `État des lieux` · `À propos` |
| `**Important**` | `Important` (LinkedIn n'affiche pas le Markdown) |
| `Il est important de noter que les chiffres montent.` | `Les chiffres montent.` |
| `afin de` · `au sein de l'équipe` | `pour` · `dans l'équipe` |
| espaces sans chasse, BOM, balises Unicode, sélecteurs isolés | supprimés (procédés pour cacher du texte) |

Gardés : heures (`14:30`), URL, émojis composés (👨‍💻), espaces insécables
légitimes (remplacées par des espaces normales, pas supprimées ; `--insecables`
pose de vraies insécables).

Les filigranes statistiques (type SynthID) sont dans le choix des mots, pas
dans les caractères : aucun outil ne les retire de façon fiable, et le Skill
ne le promet pas.

### À la main, par paragraphe

Lis le rapport de `humanize.py --rapport` ou la section « Paragraphes à
reprendre » de `detect.py`.

| Marqueurs dans le paragraphe | Action |
|---|---|
| 3 ou plus | **réécris le paragraphe entier**, pas mot par mot, dans le registre de l'auteur |
| un marqueur fort (révélation, parallélisme, staccato, sincérité, appât, anaphore, formulation retirée) | corrige-le, même seul |
| 2 marqueurs faibles | remplace celui qui travaille le moins, laisse l'autre |
| 1 marqueur faible | laisse-le |

Exemple (3 marqueurs : « stratégique », « levier », « crucial ») :

> Avant : Cette approche stratégique constitue un levier crucial pour notre croissance.
> Après : Cette approche nous a apporté 40% de nos rendez-vous du trimestre.

Le chiffre de l'« après » doit venir de l'utilisateur. Sinon :

> Après : Cette approche nous a apporté {{à compléter : part des rendez-vous du trimestre}}.

Règles :

- jamais un synonyme de la même liste (« levier » → « catalyseur ») ;
- réécris dans le registre de l'auteur, pas dans un « neutre » uniforme : la
  platitude à température constante est elle-même une empreinte ;
- parallélisme négatif (« Ce n'est pas X, c'est Y ») : réécris en affirmations
  côte à côte, ou dis seulement Y.

> Avant : Ce n'est pas une question de volume, c'est une question de pertinence.
> Après : On a envoyé 7 fois moins de messages et obtenu plus de réponses.

## Passe 2 · RYTHME

On ne fabrique jamais de variation. On corrige deux choses.

**Le plat mécanique.** Un paragraphe de 4 phrases ou plus, toutes de même
longueur (à 3 mots près), sans subordonnée. Relie **une** phrase, celle qui
porte le plus de sens, à sa voisine par une subordonnée qui travaille :

> Avant : Nous avons lancé la campagne en mars. Les premiers résultats sont arrivés vite. L'équipe a suivi les chiffres chaque matin. Le budget est resté stable.
> Après : Nous avons lancé la campagne en mars, quand le budget a enfin été validé. Les premiers résultats sont arrivés vite. L'équipe a suivi les chiffres chaque matin, et le budget n'a pas bougé.

Deux ou trois phrases moyennes à la suite, c'est normal. Une longue et une
courte, aussi.

**La variation fabriquée.** À réécrire en phrases complètes :

| Tic | Exemple | Réécriture |
|---|---|---|
| rafale d'adjectifs | « Simple. Rapide. Efficace. » | « L'outil se prend en main en 5 minutes. » |
| « Pas de X. Pas de Y. Juste Z. » | « Pas de réunion. Pas de slides. Juste du terrain. » | « On a passé la semaine chez trois clients au lieu de préparer la présentation. » |
| paragraphe d'un mot | « Vraiment. » | supprimer, ou rattacher à la phrase d'avant |
| question-réponse | « Pourquoi ? Parce que personne ne lit. » | « Personne ne lit ces messages. » |
| chute sèche | « C'est tout. » | supprimer |
| plus de 2 fragments | « Résultat. Énorme. Merci. » | garder 2 fragments au plus dans tout le post |
| bascule long/court/long/court | | fusionner une phrase courte avec sa voisine |

**Ce n'est pas un tic** : une phrase par paragraphe séparée par une ligne
vide. C'est la mise en page normale de LinkedIn sur mobile.

## Passe 3 · AJOUTER (seulement du vrai)

Un texte propre mais vide sonne encore machine. Il lui faut, s'il ne les a
pas déjà :

- **un chiffre avec son référent** : « 412 messages envoyés au 1er trimestre
  2025 », pas « 400 messages » ni « beaucoup de messages ». Un nombre nu ne
  suffit pas : c'est le référent qui fait le signal ;
- **une entité nommée** : une personne (avec accord), une entreprise, un
  outil, une ville, une date ;
- si le sujet s'y prête, **un fait daté, inconfortable, énoncé à plat**, sans
  phrase pour l'annoncer :

> Mise en scène : Je vais être honnête avec vous, ça a été dur : on a perdu ce client.
> À plat : On a perdu le client Assurly le 14 février.

D'où viennent ces faits : `reserve.md`, `contexte.md`, la conversation. Rien
d'autre. Sinon : `{{à compléter : …}}` ou une question à l'utilisateur.

**Interdit dans cette passe** :

- les annonces de sincérité : « Honnêtement, », « Pour être transparent »,
  « Je vais être cash », « Petite confession », « La vérité, c'est que » ;
- les précautions que l'auteur n'a pas écrites : « peut-être que je me trompe,
  mais », « à mon humble avis » ;
- un détail sensoriel ou une anecdote inventés « pour faire humain » ;
- des fautes volontaires.

## Passe 4 · CONTRÔLER

Relis une fois et réponds à trois questions. Les scripts aident pour les deux
premières.

1. **Ai-je créé ce que je devais retirer ?** Staccato, révélation,
   parallélisme, alternance long/court ? (`detect.py avant après` : garde
   anti-sur-correction.)
2. **Ai-je ajouté ou perdu un fait ?** (`fidelite.py avant après`.) Un ajout
   est bloquant sauf s'il vient de l'utilisateur ; une perte est une erreur
   sauf si une règle l'impose (chiffre interdit, doublon).
3. **Ai-je aplati la voix ?** Plus aucune réaction, plus aucun détail concret,
   tous les « je » partis, toutes les phrases longues coupées ? Rends ce que
   l'auteur avait.

Si l'une des réponses est oui : dose à la baisse, ne nettoie pas plus fort.
Dans le doute sur un tic qui pourrait être la voix de l'auteur, laisse-le et
signale-le.

## Quand ne pas toucher

- citations, titres, noms propres, noms de produits (termes protégés de
  `contexte.md`) ;
- textes écrits avant fin 2022, ou dont l'utilisateur dit qu'ils sont de sa
  main et qu'il veut juste la typographie (niveau forensique seulement) ;
- formules de politesse d'un message privé ;
- détails insolites, sentiments mêlés, apartés, auto-corrections de l'auteur :
  ce sont des signes humains, ils restent.
