# Le fichier tone-of-voice.md

Un seul fichier, lu par toute IA et par tous les Skills Join Médicis qui
écrivent. Modèle vide : `modeles/tone-of-voice.md`. Exemple rempli :
`exemples/assurly/tone-of-voice.md`.

## 1. Les 13 sections

Toujours les mêmes, dans le même ordre, numérotées : deux versions se
comparent ligne à ligne, et `profil.py verifier` les retrouve.

| # | Section | Ce qu'on y met | Source |
|---|---|---|---|
| en-tête | version, date, volume, confiance | ce que vaut la voix | `voix.py` |
| 1 | En une phrase | qui parle, à qui, comment | analyse + question 12 |
| 2 | Ce que je suis, ce que je ne suis pas | 3 à 5 traits, consigne, citation | analyse |
| 3 | Curseurs | 5 curseurs notés 1 à 5, avec la preuve | mesures + calibrage |
| 4 | Règles d'écriture | adresse, phrases, paragraphes, ponctuation, chiffres, ouvertures, fins, typographie | mesures |
| 5 | Mes mots | vocabulaire, expressions, anglicismes, tics à garder | mesures |
| 6 | Ce que je n'écris jamais | une expression entre « » en tête de ligne, puis la raison | mesures + entretien |
| 7 | Où je tranche, où je nuance | sujets par zone | analyse + question 8 |
| 8 | Réglages par canal | adresse, longueur, ouverture, fin, formule d'appel, signature | textes + entretien |
| 9 | Avant / après | 1 à 3 paires | calibrage |
| 10 | Extraits de référence | 2 ou 3 extraits réels, sans retouche, tiers retirés | textes |
| 11 | Questions ouvertes | chaque incertitude, avec une proposition | tout le parcours |
| 12 | Mesures | bloc `voix.py --bloc`, jamais retouché à la main | `voix.py` |
| 13 | Journal | date, version, changement, pourquoi | chaque mise à jour |

Quand une section n'a pas de matière, elle garde son titre et dit pourquoi
(« Un seul canal pour l'instant »). Elle ne disparaît pas.

## 2. Règles d'écriture du fichier

- **150 lignes au plus.** Au-delà, une IA lit mal la fin. Les extraits sont
  courts (5 lignes chacun).
- **Chaque règle porte sa preuve** : « (5 textes sur 5) », « (entretien) »,
  « (calibrage) », ou une citation.
- **Consignes, pas observations.** « Commence par l'heure ou le jour », pas
  « elle a tendance à… ».
- **Les « jamais » sont contrôlables** : l'expression exacte entre « » en
  tête de ligne, la raison après. Une posture (« pas de critique des
  concurrents ») s'écrit sans guillemets : elle se juge, elle ne se cherche
  pas.
- **Typographie française** dans tout le fichier : `profil.py verifier`
  refuse le tiret cadratin et signale le pourcentage espacé et les guillemets droits.

## 3. Voix réelle et voix visée

Si la personne veut faire évoluer sa voix (« je voudrais être plus
direct »), ne mélange pas : la section 2 décrit la voix réelle, et une ligne
s'ajoute sous le tableau :

> **Vers où je veux aller** : plus direct sur les prix (aujourd'hui : prix
> donné en fin de message, dans 4 textes sur 5). Consigne : le prix dans les
> deux premières phrases.

Une voix entièrement « aspirationnelle » (aucun texte ne lui ressemble) est
une fiction : l'IA écrira quelque chose que personne ne reconnaît.

## 4. Versions et journal

- Version 1 à la création ; + 1 à chaque changement validé.
- La date d'en-tête change à chaque version.
- Une ligne de journal par changement, avec la raison dans les mots de la
  personne : « retiré “n'hésitez pas”, Camille : “ça fait standard
  téléphonique” ».
- `profil.py verifier` signale une voix de plus de 6 mois : la refaire avec
  des textes récents, une voix bouge.

## 5. Où le fichier vit

| Outil | Emplacement | Qui le lit |
|---|---|---|
| Claude Code | `~/.claude/fondation/tone-of-voice.md` | les packs Join Médicis (LinkedIn, SEO, Fondation) et toute conversation qui le cite |
| claude.ai | connaissances du Projet, ou Skill « ma-voix » | les conversations du Projet ; partout avec le Skill |
| ChatGPT | fichiers du Projet ou du GPT, ou Skill « ma-voix » | idem |
| Gemini, Mistral | fichier joint ou collé dans les instructions | la conversation |

Le fichier contient une empreinte d'écriture et parfois des informations
internes : jamais dans un dépôt public.

## 6. Ce que les autres Skills en font

- **Pack LinkedIn** : lit le fichier avant d'écrire ; l'humaniseur garde les
  « tics à garder » de la section 5.
- **Pack SEO** : `/seo-write` applique les sections 2, 4 et 6 aux articles,
  avec la ligne « Site » de la section 8 si elle existe.
- **Fondation** : `tone-of-voice.md` est le fichier de voix de la Fondation
  (il remplace le `voix.md` prévu).
