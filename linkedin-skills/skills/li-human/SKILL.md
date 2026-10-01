---
name: li-human
description: >-
  Humaniseur français : retire d'un brouillon les marques d'écriture IA (tirets
  cadratins, caractères invisibles, guillemets anglais, tics du type « Il est
  important de noter », « Le résultat ? », « Ce n'est pas X, c'est Y ») et le
  note sur cinq signaux avant que l'utilisateur le voie. Utilise-le dès qu'un
  texte doit sonner humain : « humanise », « ça fait IA ? », « enlève les
  tirets », « dé-IA-ise ce post », et avant de montrer tout post, commentaire,
  réponse ou message LinkedIn produit par les autres Skills du pack.
---

# li-human

Le filtre par lequel passe tout ce que le pack écrit. Il fait deux choses :
nettoyer ce qu'une machine peut nettoyer sans risque, et montrer précisément ce
qu'un humain doit réécrire.

Les marqueurs viennent de la page d'aide de Wikipédia « Identifier l'usage
d'une IA générative » et de ses déclinaisons francophones. Ils sont détaillés,
avec des exemples avant/après, dans `references/marqueurs-ia-fr.md`.

## Avec exécution de code (Claude Code, claude.ai avec l'option activée)

Deux scripts sans dépendance, qui tournent en local. Rien n'est envoyé.

```bash
python3 humanize.py brouillon.txt -o propre.txt --rapport   # nettoie + liste ce qui reste à réécrire
python3 detect.py brouillon.txt propre.txt                  # note avant / après, cinq contrôles
```

Les deux lisent `tics-ia.json` : 25 remplacements sûrs, 66 tics signalés,
13 structures. Le fichier est fait pour être modifié : si un mot fait partie
de la voix de l'utilisateur, retire-le du fichier plutôt que de le combattre.

## Sans exécution de code (ChatGPT, Gemini, Mistral, claude.ai sans l'option)

Applique la même chose à la main : lis `references/marqueurs-ia-fr.md`,
passe le texte au crible famille par famille, puis donne une note sur 100
pour chacun des cinq contrôles ci-dessous en expliquant d'où elle vient.
Dis clairement que la note est une estimation, pas un calcul.

## Ce qui est corrigé automatiquement

**1. Caractères invisibles.** Espaces sans chasse, joints, traits d'union
conditionnels, BOM, marques de direction, caractères d'étiquette Unicode. Les
espaces insécables et fines deviennent des espaces normales **sans être
supprimées** : en français, l'espace avant `; : ! ?` reste. Avec
`--insecables`, le script pose au contraire de vraies insécables, pour une
typographie soignée.

**2. Typographie française.**

| Avant | Après |
|---|---|
| `morte — elle a changé` | `morte, elle a changé` |
| `“on signe”` | `« on signe »` |
| `Résultat: 212 rendez-vous!` | `Résultat : 212 rendez-vous !` |
| `Etat des lieux` · `A propos` | `État des lieux` · `À propos` |
| `**Important**` | `Important` (LinkedIn n'affiche pas le Markdown) |
| `l'équipe` et `l’équipe` mélangés | une seule forme, la majoritaire |

Les heures (`14:30`), les URL et les émojis composés (👨‍💻) ne sont pas touchés.

**3. Formules sûres.** Seulement celles qui ne peuvent casser ni l'accord ni le
sens : « il est important de noter que » supprimé (et la phrase reprend sa
majuscule), « afin de » → « pour », « au sein de l'équipe » → « dans
l'équipe », « une véritable révolution » → « une révolution », « fait du
sens » → « a du sens »…

## Ce qui est signalé, jamais réécrit par le script

Changer la forme d'une phrase demande du jugement. Le rapport donne la ligne,
l'extrait et une piste :

- **Parallélismes** : « Ce n'est pas X, c'est Y », « Non seulement… mais »,
  « Bien plus qu'un simple… », « Le vrai sujet n'est pas… »
- **Ponts de révélation** : « Le résultat ? », « Le secret : », « Voici
  pourquoi 👇 »
- **Lexique IA** : crucial, essentiel, incontournable, levier, holistique,
  « plonger dans », « dans un monde en constante évolution »…
- **Verbes vides et faux soutenu** : permettre de, optimiser, mettre en place,
  effectuer, procéder à, s'avérer, constituer, représenter
- **Connecteurs en pluie** : Par ailleurs, De plus, En outre, Néanmoins…
- **Participes de fin de phrase** : « …, témoignant de notre engagement »
- **Anglicismes** : adresser un problème, impacter, en termes de
- **Artefacts de chatbot** : « Bien sûr ! », « N'hésitez pas à… »,
  « Excellente question »
- **Tics LinkedIn** : « Et si je vous disais », « Qu'en pensez-vous ? »,
  appâts à engagement, mur de hashtags, émojis en début de ligne, listes
  « Titre : texte »
- **Rythme** : anaphores, triades en série, phrases toutes de même longueur

C'est ton travail : réécris chaque passage signalé en gardant le sens, puis
relance `detect.py`. C'est cette étape qui fait passer de « À REVOIR » à
« OK », et aucun script ne peut la faire.

## Les cinq contrôles

| Contrôle | Ce qu'il mesure | Ce qui fait « machine » |
|---|---|---|
| RYTHME | variation de longueur des phrases | toutes les phrases de même longueur |
| PRÉCISION | chiffres, noms propres, montants pour 100 mots | des abstractions, aucun chiffre |
| TICS | densité du lexique pour 100 mots | vocabulaire de plaquette |
| EMPREINTE | invisibles, tirets cadratins, guillemets anglais, gras, pour 1 000 caractères | une typographie de machine |
| VOIX | pronoms, marques d'oral (« on », « ça », « j' »), structures types | pas de « je », des révélations mises en scène |

Le verdict pèse la moyenne à 60 % et le contrôle le plus faible à 40 %, parce
qu'un détecteur n'a besoin que d'un signal. **OK** : 70 et plus sans contrôle
sous 55. **À REVOIR** : 50 et plus. **SIGNALÉ** en dessous.

Sur un texte court (moins de 25 mots ou de 4 phrases : note d'invitation,
commentaire), RYTHME, PRÉCISION et VOIX sont marqués « n/a » et sortent du
verdict. N'allonge jamais un texte pour faire monter la note : on écrit pour
le lecteur, pas pour le script.

## Dis-le honnêtement

Ce sont cinq heuristiques locales, construites sur les signaux qu'utilisent
les détecteurs publics et les contributeurs de Wikipédia. Ce ne sont ni
GPTZero, ni Originality, ni Compilatio, et elles ne promettent pas leurs
verdicts. Corriger ce qu'elles mesurent fait en général bouger ces outils,
parce qu'ils regardent la même chose. C'est tout ce qu'on peut affirmer. Ne
dis jamais à l'utilisateur que son texte est « indétectable ».

Et rappelle la règle de Wikipédia elle-même : ces signes orientent, ils ne
prouvent rien. Un humain peut écrire « crucial ». Ce qui trahit l'IA, c'est
l'accumulation et le vide derrière.

## Ordre des opérations

1. `humanize.py brouillon.txt -o propre.txt --rapport`
2. Réécris chaque passage signalé, toi-même, en gardant le sens et la voix
   décrite dans `voix.md`.
3. `detect.py brouillon.txt propre.txt` pour montrer l'écart.
4. Si le verdict n'est pas OK, corrige le contrôle le plus faible et relance.
   Deux tours, c'est normal. Cinq tours veulent dire que le brouillon a été
   écrit par formule : il faut un autre brouillon, pas un sixième tour.
5. Montre le texte propre **et** la note. Jamais la note seule.

## Fin de tâche

Si l'utilisateur a corrigé à la main un mot que le lexique laissait passer,
ou rétabli un mot que le lexique retirait, propose d'ajouter la règle à
`~/.claude/linkedin/apprentissages.md` (ou à `tics-ia.json`). N'écris rien
sans son accord.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Ce Skill est le filtre des autres : il change la forme, jamais les faits. Il
  n'ajoute un fait que s'il vient de l'utilisateur (`voix.md`, « Preuves
  utilisables ») ; sinon il laisse `{{à compléter}}` à la place de la phrase
  générique.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
