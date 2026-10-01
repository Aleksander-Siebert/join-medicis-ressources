---
name: linkedin-carousel
description: >-
  Crée un carrousel LinkedIn (post document en PDF) : le texte de chaque
  diapositive, la couverture qui donne envie de faire défiler, le texte du post
  qui l'accompagne, puis le PDF à téléverser. Utilise-le quand l'utilisateur
  veut un carrousel, un post document, des « slides LinkedIn », ou transformer
  une méthode en étapes visuelles.
---

# linkedin-carousel

Le carrousel (post « document ») est le format où l'on passe le plus de temps
sur LinkedIn : chaque diapositive tournée compte. **[données à grande échelle,
éditeurs]** Il récompense une idée découpée en étapes. Il punit un post texte
coupé en morceaux.

## Quand l'utiliser plutôt qu'un post texte

Un carrousel quand l'idée a une **suite** : des étapes, un compte à rebours,
une progression avant/après, une méthode en plusieurs parties. Un post texte
quand l'idée est une seule affirmation. Étaler une affirmation sur huit
diapositives est la première cause d'échec : si c'est ce que l'utilisateur a,
dis-le et passe la main à `/linkedin-post`.

## Structure

8 à 12 diapositives. En dessous de 8, c'est un post texte. Au-dessus de 12,
le taux de lecture jusqu'au bout s'effondre.

```
1        COUVERTURE  l'accroche, 6 mots maximum, + une ligne de promesse
2        L'ENJEU     pourquoi ça compte, en une phrase
3 à N    UNE IDÉE PAR DIAPO. Un titre de 3 à 7 mots, 25 mots maximum dessous.
                     Si une diapo a besoin d'un paragraphe, c'est deux diapos.
N+1      RÉCAP       tout le carrousel en liste : la diapo qu'on capture
DERNIÈRE APPEL       une seule action : s'abonner, commenter, ou le lien.
```

## Règles de texte

- **La diapo 1 fait 80% du résultat.** Six mots. En gros. Le reste ne
  rattrapera pas une couverture que personne ne fait défiler.
- **Numérote chaque diapo** (3/10) : on va plus loin quand on voit la fin.
- **Aucune diapo en paragraphe.** Plus de 25 mots : coupe en deux.
- **Le récap est la diapo qu'on capture.** Elle doit tenir seule.
- **Le nom ou l'@ de l'utilisateur sur chaque diapo**, petit, en bas : les
  captures voyagent sans lui.
- **Typographie française** : « », espace avant `: ; ! ?`. Passe tout le texte
  par `/linkedin-human`.
- **Accessibilité** : contraste suffisant, corps 28 px minimum, pas de texte
  en image seule sans le reprendre dans le post.

## Fabriquer le PDF

LinkedIn attend un PDF, idéalement **1080 × 1350 px** (format 4:5, le plus
de place dans le fil), moins de 100 Mo et 300 pages.

Pars de `gabarit.html` dans ce dossier : une `<section>` par diapo, déjà
dimensionnée, numérotée, avec l'@ en bas. Remplace les textes, la couleur
d'accent (`--accent`) et la police. Si l'utilisateur a une charte (ou un Skill
de marque dans le Projet), utilise-la et n'invente pas de palette.

Avec exécution de code :

```bash
chromium --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=carrousel.pdf gabarit.html
```

Sans exécution de code : donne le HTML complet ; l'utilisateur l'ouvre dans
Chrome, Imprimer, « Enregistrer au format PDF », marges « Aucune », format
personnalisé. Ou propose le texte diapo par diapo pour Canva.

## Sortie

1. Le texte diapo par diapo, en liste numérotée, lisible en dix secondes.
2. Le **texte du post** qui accompagne le carrousel : 2 à 3 lignes au-dessus,
   c'est la vraie accroche dans le fil (via `/linkedin-post`, formule au choix).
3. Le **titre du document** (il s'affiche sur LinkedIn) : court, descriptif.
4. Le PDF, seulement après validation du texte.

Rien n'est téléversé sur LinkedIn. L'utilisateur publie le PDF lui-même.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Tout texte destiné à LinkedIn passe par `/linkedin-human` avant d'être montré.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
