# Exemple : un pipeline réel, de `init` à la revue

Assurly est une entreprise fictive (courtier en santé et prévoyance pour
indépendants). Le contexte est `commun/modeles/exemple-site-context.md`,
l'article celui de l'exemple de `/seo-write` (son `references/exemple.md`). Les
sorties ci-dessous sont celles du script, copiées telles quelles le
16 octobre 2026. Les fichiers sont dans `evals/seo-article/` du dépôt.

## 1. Ouvrir, et l'ordre qui tient

```
$ python3 scripts/pipeline.py init "mutuelle indépendant" --dossier art/ --ymyl
ARTICLE · mutuelle indépendant · YMYL · validé étape par étape
  Cadrage    à faire
  Mots-clés  à faire
  SERP       à faire
  Plan       à faire
  Rédaction  à faire
  Contrôles  à faire
  Maillage   à faire
  Livraison  à faire
SUITE · Cadrage : faire · les réponses aux questions, ou les hypothèses écrites
```

Le cadrage est fait (6 questions, une à la fois) et validé. L'utilisateur a
donné le mot-clé et l'intention : l'étape se passe.

```
$ python3 scripts/pipeline.py passer mots-cles --dossier art/ --raison "mot-clé et intention donnés par l'utilisateur"
```

Après la SERP validée, on tente d'écrire avant le plan :

```
$ python3 scripts/pipeline.py fait redaction --dossier art/ --fichier art/article.md
Erreur : « redaction » attend la validation de : plan. On ne rédige pas sans plan validé, on ne contrôle pas sans article.
[code 1]
```

Le plan est fait par `/seo-brief`, montré, validé ; puis la rédaction par
`/seo-write`, montrée, validée.

## 2. Le portail qualité, tour 1

```
$ python3 scripts/pipeline.py controler art/article.md --dossier art/ --contexte site-context.md --affirmatif --remplacer "chez Assurly=à Assurly" --longueur 1000-1500 --mot-cle "mutuelle indépendant" --marque Assurly
PORTAIL QUALITÉ · tour 1 sur 2 · YMYL
  Rédaction     OK          PRÊT · 763 mots · 4 liens internes · title 490 px · description 852 px
  Affirmations  OK          OK en mode YMYL · 0 bloquante(s), 0 à vérifier, 4 trou(s) assumé(s)
  Humaniseur    À CORRIGER  67.6 À REVOIR (profil article, niveau strict, seuil 70)
VERDICT · À CORRIGER
À CORRIGER (dans l'ordre : bloquants d'abord)
  Humaniseur · paragraphe 9 (ligne 32) : REMPLACER LE PLUS FAIBLE, indépendants s'appellent Essentielle, Confort et Intégrale, Essentielle
  Humaniseur · paragraphe 17 (ligne 58) : RÉÉCRIRE LE PARAGRAPHE, **Listez vos besoins réels**, **Comparez les garanties**, **Vérifiez le délai de carence**, **Regardez les conditions de résiliation**
AVIS (non bloquant : à améliorer si un passage s'y prête)
  Humaniseur · DENSITÉ 62 : 9 marqueur(s) sur 22 paragraphe(s) : 1 à réécrire, 0 avec un marqueur fort, 1 à 2 marqueurs
  Humaniseur · CONCRET 53.4 : 26 éléments concrets, 3.4 pour 100 mots (viser 4+)
  Humaniseur · VOIX 62.1 : 5.4 pronoms et 0.0 marques d'oral pour 100 mots, 0 structure(s) type
TROUS ASSUMÉS (4)
  {{à compléter : page service-public.fr sur la complémentaire santé des travailleurs indépendants}}
  {{à compléter : niveaux de remboursement par formule, conditions générales 2026}}
  {{à compléter : plafond Madelin 2026, source impots.gouv.fr}}
  {{à compléter : page impots.gouv.fr sur la déduction Madelin}}
SUITE · Corrige seulement les passages listés, puis relance le contrôle.
[code 2]
```

Ce que le Skill fait de ce verdict :

- **Les affirmations passent** parce que le délai de 48 h et les 41% viennent
  de `site-context.md` (étiquettes LIVE et preuve d'entreprise). Sans
  `--contexte`, les deux phrases seraient bloquantes en YMYL.
- **Deux passages à réécrire, pas l'article.** La liste en gras « Listez,
  Comparez, Vérifiez, Regardez » est un tic de structure : les verbes restent,
  le gras sort. La phrase des trois formules est signalée comme énumération
  en trois ; elle est reformulée.
- **Les avis ne se corrigent pas un à un.** Le « concret » bas vient aussi
  des 4 trous : en YMYL, un `{{à compléter}}` remplace un chiffre qu'on ne
  peut pas sourcer.

Les deux passages, avant et après :

| Avant | Après |
|---|---|
| 1. **Listez vos besoins réels** : lunettes, soins dentaires prévus, enfants, médecine douce. | 1. Notez vos dépenses de l'année à venir : lunettes, soins dentaires prévus, enfants, médecine douce. |
| À Assurly, les trois formules pour indépendants s'appellent Essentielle, Confort et Intégrale. Leurs niveaux de remboursement figurent dans les conditions générales : … | À Assurly, le niveau de remboursement dépend de la formule choisie. Le détail poste par poste figure dans les conditions générales : … |

## 3. Tour 2

```
PORTAIL QUALITÉ · tour 2 sur 2 · YMYL
  Rédaction     OK          PRÊT · 768 mots · 4 liens internes · title 490 px · description 852 px
  Affirmations  OK          OK en mode YMYL · 0 bloquante(s), 0 à vérifier, 4 trou(s) assumé(s)
  Humaniseur    AVIS        67.6 À REVOIR (profil article, niveau strict, seuil 70)
VERDICT · LIVRABLE
AVIS (non bloquant : à améliorer si un passage s'y prête)
  Humaniseur · CONCRET 45.9 : 23 éléments concrets, 3.0 pour 100 mots (viser 4+)
  Humaniseur · VOIX 61.9 : 5.4 pronoms et 0.0 marques d'oral pour 100 mots, 0 structure(s) type
TROUS ASSUMÉS (4)
  …
SUITE · Montre l'article et le bloc « Contrôles » ; l'utilisateur valide l'étape.
[code 0]
```

Le « concret » a baissé (53,4 → 45,9) : la nouvelle phrase ne cite plus le
nom des formules. C'est un vrai recul, dit à l'utilisateur dans la
livraison ; il peut préférer garder les noms.

Si le tour 2 avait encore rendu À CORRIGER, le verdict aurait été
**RELECTURE HUMAINE** : pas de tour 3, la liste va à l'utilisateur.

## 4. Un retour après coup

Les contrôles sont validés, puis l'utilisateur demande une section de plus :

```
$ python3 scripts/pipeline.py refaire plan --dossier art/ --retour "ajouter une section sur la prévoyance"
ARTICLE · mutuelle indépendant · YMYL · validé étape par étape
  Cadrage    validé
  Mots-clés  passée
  SERP       validé     · art/serp.md
  Plan       à refaire  · art/plan.md
             retour : ajouter une section sur la prévoyance
  Rédaction  à revoir   · art/article.md
  Contrôles  à revoir   · art/article.md
  Maillage   à faire
  Livraison  à faire
SUITE · Plan : refaire, avec le retour · title, H1, H2/H3 commentés, cadre, liens (/seo-brief)
```

Le cadrage et la SERP restent validés : rien n'est refait en amont. La
rédaction « à revoir » ne veut pas dire tout réécrire : on ajoute la section,
on garde le reste, et on le dit. La nouvelle version a ses propres tours
(le compteur repart à 1).

```
$ python3 scripts/pipeline.py rapport --dossier art/
RAPPORT · mutuelle indépendant
  Cadrage    validé
  Mots-clés  passée
  SERP       validé
  Plan       à refaire
  Rédaction  à revoir
  Contrôles  à revoir
  Maillage   à faire
  Livraison  à faire
CONTRÔLES · 2 tour(s) : À CORRIGER → LIVRABLE
RESTE · Plan, Rédaction, Contrôles, Maillage, Livraison
```

## 5. Le même début en mode autonome

```
$ python3 scripts/pipeline.py init "mutuelle indépendant" --dossier art/ --ymyl --autonome
$ python3 scripts/pipeline.py hypothese cadrage --dossier art/ "persona : indépendant qui se lance, 25-40 ans (site-context.md §3, lecteur 1)"
$ python3 scripts/pipeline.py fait cadrage --dossier art/
$ python3 scripts/pipeline.py passer mots-cles --dossier art/ --raison "mot-clé donné dans la demande"
$ python3 scripts/pipeline.py hypothese serp --dossier art/ "comparatif : type le plus fréquent, 40% (consensus partagé, serp.py)"
$ python3 scripts/pipeline.py fait serp --dossier art/ --fichier art/serp.md
$ python3 scripts/pipeline.py hypothese plan --dossier art/ "1 000 à 1 500 mots, préférence du site"
$ python3 scripts/pipeline.py fait plan --dossier art/ --fichier art/plan.md
ARTICLE · mutuelle indépendant · YMYL · autonome
  Cadrage    validé
  Mots-clés  passée
  SERP       validé     · art/serp.md
  Plan       validé     · art/plan.md
  Rédaction  à faire
  Contrôles  à faire
  Maillage   à faire
  Livraison  à faire
SUITE · Rédaction : faire · l'article dans la voix du site (/seo-write)
HYPOTHÈSES · 3 (listées au rapport)

$ python3 scripts/pipeline.py rapport --dossier art/
…
HYPOTHÈSES À CONFIRMER
  Cadrage · persona : indépendant qui se lance, 25-40 ans (site-context.md §3, lecteur 1)
  SERP · comparatif : type le plus fréquent, 40% (consensus partagé, serp.py)
  Plan · 1 000 à 1 500 mots, préférence du site
RESTE · Rédaction, Contrôles, Maillage, Livraison
```

Le chiffre de 40% vient du relevé de SERP de test
(`evals/seo-serp/releve-mutuelle.csv`, `serp.py`) : une hypothèse cite sa
mesure. Le délai, le plafond Madelin et les niveaux de remboursement ne sont
jamais supposés, en autonome comme ailleurs.
