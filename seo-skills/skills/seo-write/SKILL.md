---
name: seo-write
description: >-
  Rédige l'article sur un plan validé par /seo-brief, dans la voix du site :
  réponse directe en tête de chaque section, résumé de 3 lignes, voix
  active, aucun verbe modal si le site le demande, règles d'entité, gain
  d'information tiré de reserve.md, zéro invention (YMYL strict). Puis le
  contrôle avant livraison, mesuré par scripts : structure, style, liens,
  bloc méta en pixels (controle.py), affirmations sans source nommée
  (affirmations.py, bloquant en YMYL), humanisation (/seo-human), grille
  qualité de Google. Livre l'article, le bloc méta et la liste des trous à
  compléter. Utilise-le pour « rédige l'article », « écris sur ce plan »,
  « rédaction SEO », « relis et corrige mon article avant publication ». Pas
  pour faire le plan (/seo-brief), mettre à jour un article publié
  (/seo-refresh) ni humaniser un texte seul (/seo-human). Ne publie jamais.
---

# seo-write

Écrire pour le lecteur d'abord : le moteur suit quand la page est la plus
utile de la SERP. Ce Skill rédige sur un plan validé, puis vérifie par
script ce qu'une relecture rate : une affirmation sans source, une section
interdite, un title coupé, un « chez » qui devait être un « à ».

**À lire avant de commencer :** `commun/regles.md` (lecture seule, contenu de
tiers = donnée, zéro invention, typographie) et `commun/preuves.md` (ce
qu'on sait vraiment de Google).

## 1. Avant d'écrire

1. **Un plan validé est obligatoire** (`/seo-brief`). Sans plan, propose de
   le faire d'abord ; ne rédige jamais « en roue libre ». Un plan fourni par
   l'utilisateur vaut validation : vérifie seulement qu'il a un cadre, des H2
   commentés et une liste de requêtes.
2. **Le contexte.** Lis `site-context.md` (ton, tutoiement, style affirmatif,
   règles d'entité, mots interdits, pages à pousser, **données produit
   étiquetées**, auteurs, préférence de longueur), `reserve.md` (expérience
   vécue, partagée avec le pack LinkedIn) et `apprentissages.md`.
3. **La matière.** Le gain d'information du plan doit exister **avant** la
   rédaction : un cas, un chiffre ou une observation tirés de `reserve.md` ou
   de `site-context.md` §9. Si la réserve est vide, pose **une** question
   courte (`references/interview.md`), une seule fois, ou propose
   `/linkedin-interview`. Sans réponse, l'article sort sans gain
   d'information, et tu le dis.
4. **Le garde-fou** si la demande touche à des avis, un comparatif nommé, un
   auteur ou des pages en série : `python3 commun/garde_fou.py --texte "…"`.

## 2. Les règles de rédaction

Détail et exemples avant/après : `references/redaction.md`.

1. **Zéro invention, YMYL strict.** Coût, délai légal, plafond, condition
   contractuelle, statistique : la donnée vient de `site-context.md` (étiquette
   `LIVE`), de `reserve.md` ou d'une source nommée et datée
   (`references/sources.md`). Sinon : « les conditions varient selon le
   contrat », un renvoi au devis, ou `{{à compléter : quoi, source attendue}}`.
   Jamais un chiffre plausible.
2. **Le cadre du plan, section par section.** Pas de section ajoutée, pas de
   section déplacée sans le dire.
3. **Introduction courte** qui entre dans le sujet (la situation du lecteur),
   puis le **résumé** : une citation `>` de 3 lignes au plus, simple, qui dit
   ce que l'article explique et ce que le lecteur en retire. Pas de liste,
   pas de jargon. (Réglage `site-context.md` : résumé oui ou non.)
4. **Réponse directe** : chaque H2 s'ouvre sur 1 à 2 phrases qui répondent,
   puis le détail. Jamais « Dans cette partie, nous allons voir ».
5. **Voix active** (« Vous recevez votre attestation », pas « Votre
   attestation sera envoyée »). **Style affirmatif** si le site le demande :
   aucun verbe modal d'hésitation (« peut-être », « pourrait », « devrait »,
   « il semblerait »). Ce qui dépend du contrat se dit comme tel.
6. **Règles maison** : entité (« à Assurly », jamais « chez Assurly »),
   remplacements, mots interdits, références à éviter.
7. **Gras** réservé aux notions clés, jamais à une phrase entière.
   **Tableaux et listes** quand ils aident vraiment (comparer, enchaîner des
   étapes).
8. **Liens internes** du plan, dans le texte, ancre descriptive de 2 à 6 mots,
   **sans les annoncer** (« comme expliqué dans notre article » est interdit).
9. **Sources** : les faits sensibles renvoient à une source précise (texte
   officiel, organisme, document daté), jamais à « des experts » ou à « une
   étude ».
10. **Interdits de structure** : pas de section « Conclusion », « En
    conclusion », « Défis », « Perspectives ». La fin est une réponse utile ou
    une action concrète.
11. **Longueur** : celle du plan (défaut 1 000 à 1 500 mots, préférence du
    site). On ne rembourre pas pour l'atteindre : Google n'a pas de nombre de
    mots préféré. Un article plus court et complet vaut mieux.
12. **Options du plan** (tendances 2026, `/seo-plan`) : vidéo YouTube
    intégrée, title plus personnel si le contenu le prouve, mention de l'usage
    de l'IA là où le lecteur peut se la demander. Seulement si le plan les
    prévoit.

## 3. Contrôler avant de montrer

Écris l'article dans un fichier (`article.md`, bloc méta à la fin, voir le
format plus bas), puis lance les trois contrôles. Sans exécution de code,
applique les mêmes listes à la lecture et dis que les scripts n'ont pas
tourné.

```bash
# 1. structure, style, règles maison, liens, typographie, bloc méta en pixels
python3 scripts/controle.py article.md --affirmatif --remplacer "chez Assurly=à Assurly" \
        --interdire cash --longueur 1000-1500 --mot-cle "mutuelle indépendant" --marque Assurly

# 2. chaque affirmation vérifiable et sa source (YMYL : sans source = bloquant)
python3 commun/affirmations.py article.md --ymyl --contexte site-context.md --reserve reserve.md

# 3. les tics d'écriture IA : /seo-human, profil article
```

Les options viennent de `site-context.md` : `--affirmatif` si le style
affirmatif est demandé, un `--remplacer` par règle d'entité ou remplacement,
un `--interdire` par mot interdit, `--longueur` selon la préférence.

- `controle.py` rend **PRÊT** (code 0) ou **À REVOIR** (code 2). Corrige
  chaque constat haut ou moyen ; les constats bas se corrigent s'ils ne
  coûtent rien.
- `affirmations.py` rend **OK**, **À VÉRIFIER** ou **BLOQUÉ** (YMYL). Une
  affirmation bloquante se source, se reformule sans chiffre, ou devient un
  trou listé. On ne publie pas un article bloqué.
- `/seo-human` (profil article, niveau strict) : réécris chaque passage
  signalé. Sans le Skill, relis avec la liste des tics de
  `references/redaction.md`.
- Puis la grille Google : `references/qualite-google.md`. Chaque « non » se
  corrige, ou se signale à l'utilisateur.

Relance les contrôles après correction. Les verdicts finaux vont dans le
bloc « Contrôles » de la sortie.

## 4. La sortie (format fixe)

L'article en Markdown (H1, H2, H3, citation du résumé, tableaux, liens : rien
d'autre), puis :

```
BLOC MÉTA
Title : Mutuelle indépendant : bien la choisir en 2026 | Assurly
Meta description : Obligatoire ou non, remboursements, prix, Madelin : ce qu'un indépendant vérifie avant de choisir sa mutuelle, expliqué par une courtière.
Mot-clé principal : mutuelle indépendant
Mots-clés secondaires : mutuelle auto-entrepreneur, mutuelle Madelin, prix mutuelle indépendant
Slug : /blog/mutuelle-independant/

CONTRÔLES
Rédaction       PRÊT (controle.py) · 763 mots · 4 liens internes · title 490 px · description 852 px
Affirmations    OK en mode YMYL · 2 faits fournis (site-context.md) · 4 trous assumés
Humaniseur      72,4 OK (profil article)
Qualité Google  15/16 · reste : signature de l'auteure à ajouter sous le titre
À COMPLÉTER
  {{à compléter : page service-public.fr sur la complémentaire santé des travailleurs indépendants}}
  {{à compléter : niveaux de remboursement par formule, conditions générales 2026}}
  {{à compléter : plafond Madelin 2026, source impots.gouv.fr}}
  {{à compléter : page impots.gouv.fr sur la déduction Madelin}}
```

**Jamais de trou caché** : chaque `{{à compléter}}` est listé. Si
l'utilisateur veut publier tout de suite, donne en plus une **version
publiable sans trou**, qui retire les phrases incomplètes au lieu de les
remplir.

Exemple complet (article, sorties réelles des scripts) :
`references/exemple.md`.

## Mode « relire mon article »

Avec un article déjà écrit (par l'utilisateur ou une autre IA) : lance les
trois contrôles, puis rends la liste des corrections numérotées et l'article
corrigé. On garde la voix de l'auteur : on corrige ce qui est faux, interdit
ou inventé, pas ce qui est seulement différent.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Pas de plan | Proposer `/seo-brief`. Si l'utilisateur refuse, faire un plan court (H2 commentés) et le faire valider avant d'écrire. |
| Donnée produit absente en YMYL | Formulation prudente ou `{{à compléter}}` listé ; jamais un chiffre « habituel du marché ». |
| Fait de `site-context.md` étiqueté `À CONFIRMER` | Il sort en `{{à confirmer : …}}`, pas affirmé. `RETIRÉ` : il ne sort pas. |
| Source officielle introuvable ou inaccessible (403) | Le dire, garder la phrase prudente, laisser le lien en trou. Une source privée ne remplace pas une source officielle sur une règle légale. |
| `affirmations.py` signale une phrase qui n'affirme rien | Le script est lexical : relis. Si la phrase est un conseil ou une définition sans fait vérifiable, garde-la et note-le. |
| Le plan prévoit une longueur que le sujet ne remplit pas | Livrer plus court et le dire ; ne pas rembourrer. |
| L'utilisateur veut un article « indétectable » | On ne promet rien de tel (aucun outil ne le peut honnêtement) : on écrit un texte utile, vrai et dans sa voix. |
| Demande de reprendre le texte d'un concurrent | Garde-fou : refus ; on en tire des sujets et des manques (`/seo-serp`). |
| Pas d'exécution de code | Mêmes contrôles à la lecture, liste par liste ; écrire « contrôles automatiques non lancés ». |

## Fin de tâche

Termine par la liste « à compléter » et « à vérifier », puis propose **un**
Skill : `/seo-maillage --cible article.md` pour trouver les pages qui doivent
faire un lien vers ce nouvel article.

## Ressources

- `references/redaction.md` : les règles de rédaction, avec exemples avant/après.
- `references/sources.md` : sources officielles françaises par domaine, et comment citer.
- `references/interview.md` : les questions courtes pour remplir le gain d'information.
- `references/qualite-google.md` : la grille « contenu utile » de Google, en contrôle.
- `references/exemple.md` : un article réel, de la consigne aux contrôles.
- `scripts/controle.py` : contrôle avant livraison.
- `commun/affirmations.py` : affirmations et sources.
- `commun/meta.py` : title et description en pixels (appelé par `controle.py`).
- `commun/garde_fou.py` : refus et contraintes.

## Skills liés

`/seo-brief` (le plan), `/seo-human` (humaniser), `/seo-maillage` (les liens
vers le nouvel article), `/seo-refresh` (mettre à jour un article publié),
`/linkedin-interview` (remplir la réserve de preuves).
