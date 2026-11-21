---
name: seo-human
description: >-
  Humaniseur français pour les articles et pages SEO, en 4 passes : nettoie
  les marques d'écriture IA (tirets cadratins, invisibles, « Dans cet
  article », « Ce n'est pas X, c'est Y », sections « Conclusion », staccato,
  sincérité annoncée, lexique compté par paragraphe) sans casser le Markdown,
  le code ni la typographie française ; applique les règles du site (style
  affirmatif, remplacements, mots interdits) ; vérifie qu'aucun fait n'a été
  ajouté ni perdu et garde contre la sur-correction. 3 niveaux, note sur 6
  signaux calculée sur la prose seule. Utilise-le pour « humanise cet
  article », « ça fait IA ? », après chaque rédaction de /seo-write et avant
  de publier. Pas pour rédiger un article (/seo-write), ni pour promettre
  qu'un texte passera un détecteur.
---

# seo-human

Le filtre par lequel passe tout ce que le pack écrit. Il fait trois choses :
nettoyer ce qu'une machine peut nettoyer sans risque, montrer précisément ce
qu'un humain doit réécrire, et vérifier que la réécriture n'a rien inventé.

C'est le **même moteur** que `/linkedin-human` (version 2 des packs,
octobre 2026), avec un profil `article` par défaut : `references/article.md`.

**À lire avant de commencer :** `commun/regles.md` (règles du pack) et
`site-context.md` s'il existe (règles maison : entité, remplacements, mots
interdits, style affirmatif).

## La doctrine, en une phrase

Un modèle fait le choix qui convient au plus grand nombre ; un humain choisit
pour **un** lecteur et **un** sujet. On corrige les choix par défaut (mots
passe-partout, mises en scène, structures toutes faites), pas les signes
isolés, et on n'ajoute jamais de faux humain.

| Version 1 du Skill | Version 2 | Pourquoi |
|---|---|---|
| marqueurs comptés mot par mot | comptés **par paragraphe** : 3 = réécrire, 2 = remplacer le plus faible, 1 faible = laisser | les lecteurs repèrent les grappes |
| récompenser la variation de longueur | signaler le paragraphe plat **et** la variation fabriquée (staccato) | l'alternance forcée est le premier tic des textes « humanisés » |
| rien sur les faits | **vérification de fidélité** (`fidelite.py`) | une réécriture qui ajoute un chiffre invente |
| aucune garde | **garde anti-sur-correction** | un texte trop « nettoyé » a sa propre empreinte |
| titres et gras comptés dans la note | note calculée sur la **prose seule** | un article structuré n'est pas un texte d'IA |

## Les trois niveaux

| Niveau | Ce qu'il traite | Quand |
|---|---|---|
| **forensique** | fuites de modèle (« En tant qu'IA », `oaicite`, « Voici une version révisée »), gabarits non remplis, invisibles, typographie | toujours |
| **strict** (défaut) | forensique + lexique par densité, verbes vides, calques, révélations, parallélismes, staccato, sincérité annoncée, triades creuses, contrôles d'article | tout texte publié |
| **esthétique** | strict + copule évitée (« constitue », « représente »), voix passive sans agent, vocabulaire en déclin | sur demande |

Conflit entre la voix du site et une règle : forensique, on corrige
toujours ; strict, on **demande** ; esthétique, on laisse. Détail :
`references/niveaux.md`.

## Avec exécution de code

Scripts sans dépendance, dans `scripts/`. Rien n'est envoyé.

```bash
python3 scripts/humanize.py article.md -o propre.md --rapport \
  --affirmatif --remplacer "chez Assurly=>à Assurly" --interdire cash
python3 scripts/detect.py article.md propre.md --affirmatif     # 6 signaux, densité, garde anti-sur-correction
python3 scripts/fidelite.py article.md propre.md               # faits ajoutés (bloquant) ou perdus
```

Options : `--profil article|court` (court : texte sans Markdown, pour un
extrait ou une publication sociale), `--niveau forensique|strict|esthetique`,
`--json`. `tics-ia.json` est fait pour être modifié : si un mot fait partie
de la voix du site, retire-le du fichier plutôt que de le combattre.

## Sans exécution de code

Applique la même méthode à la main avec `references/marqueurs-ia-fr.md`,
`references/passes.md` et `references/article.md`. Donne la note de chaque
signal en expliquant d'où elle vient, et dis que c'est une estimation, pas
un calcul. Fais la vérification de fidélité en listant les chiffres, dates
et noms avant et après.

## Les quatre passes

Détail, exemples et cas limites : `references/passes.md`.

1. **NETTOYER.** `humanize.py` corrige seul ce qui ne peut pas casser le
   sens (invisibles, tirets cadratins supprimés ou remplacés par une
   virgule, « 15% », guillemets « », espaces avant `: ; ! ?`, majuscules
   accentuées, formules sûres, remplacements du site) et laisse intacts
   titres, gras, code et URL. Puis il **signale** le reste : réécris par
   paragraphe selon la densité. Un marqueur fort (révélation, parallélisme,
   staccato, sincérité, intro méta, section « Conclusion ») se corrige dès
   la première fois.
2. **RYTHME.** Corrige seulement ce qui est plat ou mis en scène : relie une
   phrase à sa voisine dans un paragraphe plat ; réécris le staccato en
   phrase. Jamais d'alternance long/court mécanique.
3. **AJOUTER (seulement du vrai).** Un passage vague reçoit un chiffre avec
   son référent, un nom, un exemple daté, **venant de `reserve.md`, de
   `site-context.md` ou de l'utilisateur**. Sinon `{{à compléter : …}}`
   dans la version enrichie.
4. **CONTRÔLER.** `detect.py avant après` (garde anti-sur-correction) puis
   `fidelite.py avant après` : un fait ajouté est bloquant, un fait perdu
   est une erreur sauf règle qui l'impose.

## Les six signaux (detect.py)

| Signal | Mesure | Ce qui fait « machine » |
|---|---|---|
| FORENSIQUE | fuites de modèle | une seule : verdict SIGNALÉ |
| DENSITÉ | marqueurs par paragraphe | un paragraphe à 3 marqueurs, un marqueur fort |
| RYTHME | paragraphes plats, staccato, fragments | du plat mécanique ou de la variation fabriquée |
| CONCRET | chiffres, noms, montants pour 100 mots | des abstractions |
| EMPREINTE | invisibles, tirets cadratins, guillemets anglais | une typographie de machine |
| VOIX | pronoms, oral, structures types | des mises en scène |

En profil article, titres, code et gras sortent du calcul. Verdict : moyenne
à 60% et signal le plus faible à 40%. **OK** : 70 et plus sans signal sous
55. **À REVOIR** : 50 et plus. **SIGNALÉ** sinon, ou dès une fuite
forensique. N'allonge jamais un texte pour faire monter la note.

## Modes de sortie

| Mode | Quand | Ce que tu rends |
|---|---|---|
| **collé** (défaut) | l'utilisateur colle un article | le texte final, puis la note avant/après, les tics laissés et pourquoi, la ligne de fidélité |
| **fichier** | un fichier `.md` à corriger | le fichier corrigé, Markdown, code, URL et noms intacts |
| **intégré** | appelé par `/seo-write` ou `/seo-article` | seulement le texte final ; l'autre Skill affiche la note |

```
{{texte final, publiable tel quel}}

HUMANISEUR · profil article · niveau strict · {{date}}
Avant {{note}} ({{verdict}}) → après {{note}} ({{verdict}})
Corrigé : {{n}} automatiques · {{n}} paragraphes réécrits
Laissé volontairement : {{tic et raison, ou « rien »}}
Fidélité : {{FIDÈLE | faits ajoutés ou perdus listés}}
```

## Dis-le honnêtement

Ce sont des heuristiques locales, construites sur les signaux que repèrent
les lecteurs et les contributeurs de Wikipédia. Ce ne sont ni GPTZero, ni
Pangram, ni Compilatio, et aucune réécriture ne garantit leur verdict. Ne dis
jamais qu'un texte est « indétectable ». Google ne pénalise pas un texte
parce qu'il est écrit avec une IA, mais parce qu'il n'apporte rien
(`commun/preuves.md`) : l'humaniseur corrige la forme, la valeur vient du
brief et des faits.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| « C'est mon texte, publie-le tel quel » | passe quand même le niveau forensique ; pour le reste, propose et laisse décider |
| Le site emploie lui-même un tic | `apprentissages.md` et `site-context.md` priment sur la règle de style, jamais sur le forensique ni sur la règle du tiret cadratin |
| Citation, nom de produit, titre d'œuvre, mot-clé validé dans le brief | ne pas toucher |
| Bloc de code, tableau de données | intact ; seul le texte autour est traité |
| Texte anglais | les scripts sont faits pour le français : signale-le et applique la méthode à la main |

## Fin de tâche

Si l'utilisateur a corrigé à la main un mot que le lexique laissait passer,
ou rétabli un mot que le lexique retirait, propose d'ajouter la règle à
`apprentissages.md` (ou à `tics-ia.json`). N'écris rien sans son accord.
