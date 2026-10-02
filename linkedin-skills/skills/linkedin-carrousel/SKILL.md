---
name: linkedin-carrousel
description: >-
  Crée un carrousel LinkedIn (post document en PDF) de bout en bout : vérifie
  que l'idée mérite un carrousel, choisit une des 5 structures (liste de
  valeur, problème-preuve, techniques nommées, coup de gueule avec pivot
  d'équité, démonstration), écrit les slides (couverture-vignette, une idée
  par slide, récapitulatif, un seul appel à l'action), le texte du post et le
  titre du document, puis fabrique le PDF avec un script (texte
  sélectionnable, accessible, 1080 × 1350). Fait aussi la bannière de profil
  (1584 × 396, PNG). Utilise-le pour « fais un carrousel », « post
  document », « slides LinkedIn », « transforme cette méthode en étapes
  visuelles », « fais ma bannière ». Pas pour un post texte (utiliser
  /linkedin-post) ni pour découper un contenu long en plusieurs posts
  (/linkedin-repurpose). Ne publie rien.
---

# linkedin-carrousel

Un carrousel n'est pas un article coupé en carrés. Chaque slide a deux
travaux : livrer une idée, et donner envie de passer à la suivante.

**À lire avant de commencer :** `commun/regles.md` et `commun/preuves.md`
(formats officiels : PDF, 100 Mo et 300 pages au plus).

## 1. Est-ce vraiment un carrousel ?

Un carrousel quand l'idée a une **suite** : des étapes, une liste vérifiable,
une méthode en parties, une démonstration. Sinon, un post texte.

Test : **la slide 1 et le texte du post suffisent-ils à donner la valeur ?**
Si oui, c'est un post texte, et les autres slides sont du coût. Dis-le et passe
à `/linkedin-post`.

Le carrousel coûte environ 90 minutes, contre 25 pour un post texte
[praticien]. Vérifie que le budget de la semaine le permet
(`/linkedin-strategie`, `budget.py`).

## 2. Lire le contexte et trouver la matière

`contexte.md` (voix, couleurs de la charte, appel à l'action par sujet),
`reserve.md` (les étapes et chiffres vrais), `journal.md` (pas la même idée
deux fois). Chaque chiffre d'une slide vient de l'utilisateur ou de
`reserve.md` ; sinon `{{à compléter}}`, et le script refusera de fabriquer le
PDF tant qu'il en reste.

## 3. Choisir la structure

Détail, slide par slide, avec exemples français : `references/structures.md`.

| Ta matière est… | Structure | Ce qui fait passer à la slide suivante |
|---|---|---|
| une liste de ressources, d'outils, de vérifications | **A. Liste de valeur** (4 à 14 slides) | le nombre exact promis en couverture, payé slide après slide |
| un résultat personnel avec une méthode derrière | **B. Problème-preuve** (6 à 10) | la boucle ouverte en slide 1, fermée par la preuve en dernière slide |
| plusieurs techniques sur un même thème | **C. Techniques nommées** (6 à 10) | chaque technique a un nom et tient seule |
| une conviction forte sur une pratique courante | **D. Coup de gueule** (4 à 8) | l'escalade, puis le **pivot d'équité** (« je ne vise pas X ») |
| un outil ou un processus qu'on peut montrer | **E. Démonstration** (5 à 11) | le résultat d'abord, puis la **vue d'ensemble des étapes** avant le détail |

## 4. Écrire les slides

Règles communes (Corey Haines, Jake Schincariol, alirezarezvani) :

- **La slide 1 est une vignette** : elle se bat seule dans le fil, avant que
  quiconque sache qu'un carrousel suit. 8 mots au plus, gros.
- **Une idée par slide** : un titre de 3 à 7 mots, 25 mots au plus dessous.
  Plus long : deux slides.
- **Un seul gabarit visuel** : même mise en page, mêmes tailles, mêmes
  couleurs sur toutes les slides intérieures.
- **Un nombre promis est tenu exactement** : « 6 vérifications » = 6 slides
  d'étapes (le script le vérifie). Pas de remplissage pour faire un chiffre
  rond.
- **Une slide récapitulatif** quand il y a 4 étapes ou plus : c'est celle qu'on
  capture.
- **Un seul appel à l'action**, en dernière slide, pris dans `contexte.md`.
  Jamais « commente PDF pour recevoir » (appât, refusé par le script).
- **Numérotation** (3/10) et **signature** sur chaque slide : les captures
  voyagent sans le post.
- **Accessibilité** : corps 28 px au moins à 1080 px de large, contraste
  suffisant, texte réel (pas d'image de texte), pas de pseudo-gras Unicode.
- Typographie française, pas de tiret cadratin ; le texte passe par
  `/linkedin-human`.

Montre d'abord le texte, slide par slide, en liste numérotée lisible en dix
secondes. **Le PDF se fabrique seulement après validation du texte.**

## 5. Fabriquer le PDF (script)

Écris le JSON des slides (format en tête de `scripts/carrousel.py`, exemple
complet : `assets/exemple.json`), puis :

```
python3 scripts/carrousel.py --fichier carrousel.json --verifier          # contrôle seul
python3 scripts/carrousel.py --fichier carrousel.json --sortie carrousel.pdf
```

Le script contrôle (nombre de slides, mots, promesse tenue, appel unique,
appâts, tiret cadratin, pseudo-gras, champs `{{…}}`, signature), construit le
HTML à partir de `assets/gabarit.html`, imprime le PDF avec Chromium s'il est
installé (texte sélectionnable), puis vérifie le nombre de pages et le poids.

- Couleurs : `"couleurs": {"accent": "#…", "fond": "#…", "texte": "#…"}`, prises
  dans la charte de l'utilisateur ; n'invente pas de palette.
- Format : `portrait` (1080 × 1350, défaut) ou `carre` (1080 × 1080).
- Sans Chromium : le HTML est produit ; l'utilisateur l'ouvre dans Chrome,
  Imprimer, « Enregistrer au format PDF », marges « Aucune ».
- Sans exécution de code : donne le HTML complet du gabarit rempli, ou le
  texte slide par slide pour Canva.

**Bannière de profil** : `"format": "banniere"`, une seule slide ; le script
produit un PNG de 1 584 × 396 px (texte dans les deux tiers droits, la photo
couvre la gauche). Exemple : `assets/exemple-banniere.json`.

## 6. Le texte du post et le titre du document

- **Le texte du post** a sa propre accroche (pas une copie de la slide 1) :
  2 à 5 lignes, via `/linkedin-post` (formule au choix). Il reprend aussi
  l'essentiel du contenu pour qui ne fait pas défiler.
- **Le titre du document** (affiché par LinkedIn) : court et descriptif.
- **Texte alternatif** : LinkedIn ne lit pas les slides à voix haute de façon
  fiable ; le texte du post porte l'essentiel.

## Sortie (format fixe)

```
CARROUSEL · structure {{A-E}} · {{n}} slides · {{date}}

1. [couverture] {{titre}} · {{promesse}}
2. [enjeu] …
…
n. [appel] …

Texte du post : {{…}}
Titre du document : {{…}}
Contrôle : {{TEXTES OK | À REVOIR : …}}
PDF : {{chemin}} · {{pages}} pages · {{poids}} Mo   (après validation du texte)
À mesurer dans une semaine : sauvegardes, taux de complétion (statistiques du document), pas les likes
À vérifier : {{…}}
```

Rien n'est téléversé sur LinkedIn par ce Skill. Sur « ok », une ligne dans
`journal.md` (format : carrousel).

## Mesurer

Juger un carrousel sur les **sauvegardes** et la **complétion** (jusqu'à
quelle slide on va), pas sur les likes. `/linkedin-audit` les compare aux
posts texte du même compte.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Une seule idée étalée sur 8 slides | post texte (`/linkedin-post`) |
| Plus de 14 étapes | deux carrousels, ou garder les plus utiles ; jamais de remplissage |
| Captures d'écran (structure E) | réelles, recadrées sur l'action, noms et données masqués ; à insérer dans le HTML par l'utilisateur ou le graphiste |
| Charte graphique de l'entreprise | couleurs et police de la charte ; demander le code couleur exact plutôt que deviner |
| Chiffres confidentiels | ordre de grandeur, pourcentage, ou slide retirée |
| Coup de gueule sur un concurrent nommé | refuser de nommer ; viser la pratique, pas la personne (pivot d'équité) |
| PDF au-delà de 100 Mo | images trop lourdes : les compresser ; le texte, lui, ne pèse presque rien |

## Ressources

- `scripts/carrousel.py` : contrôle, HTML, PDF ou PNG, vérification.
- `assets/gabarit.html` : styles du carrousel (une `<section>` par slide).
- `assets/exemple.json`, `assets/exemple-banniere.json` : entrées complètes.
- `references/structures.md` : les 5 structures, slide par slide, avec
  exemples et pièges.

## Skills liés

- `/linkedin-post` : le texte qui accompagne le carrousel.
- `/linkedin-human` : passe sur tout le texte des slides.
- `/linkedin-profile` : la bannière.
- `/linkedin-audit` : sauvegardes et complétion.
