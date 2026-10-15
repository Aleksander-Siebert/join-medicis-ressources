# Résultats des évaluations : pack ChatGPT Ads

## Tests automatiques

`python3 evals/tout_tester.py` : **142 tests** au 15 octobre 2026.

- 121 tests du script `valider_exporter.py` : chaque règle, export vers le
  modèle du pack et vers un modèle à la manière d'Ads Manager (préfixe XML,
  ligne d'exemple en italique, lien hypertexte), aller-retour, absence
  d'italique, règles publicitaires.
- 21 tests d'intégrité.

Le fichier exporté a aussi été ouvert avec openpyxl : 3 onglets, en-têtes et
contrôles de saisie intacts, aucune cellule de données en italique, dates
lues comme des dates.

## Éval à l'aveugle (15 octobre 2026)

**Protocole** (décision d'Aleksander : « Les deux ») :

- trois configurations travaillent séparément sur les 3 cas fictifs
  principaux (`eval-aveugle/consignes.md`), avec les mêmes réponses
  d'utilisateur et les mêmes contraintes du fichier d'import :
  - **x1** : `/chatgpt-ads-skills` ;
  - **x2** : `chatgpt-ads-builder` (fseixas, MIT) ;
  - **x3** : Claude sans Skill ;
- aucune n'a accès au web ;
- un juge reçoit les 9 réponses, sous des lettres tirées au hasard pour
  chaque cas, avec un référentiel des faits officiels d'OpenAI ;
- il note 6 critères sur 10 (exactitude, conformité, ciblage, rédaction,
  utilité, honnêteté) ;
- le tirage n'a été révélé qu'après le verdict.

Les sorties, le verdict, le référentiel et les mesures sont dans
`chatgpt-ads-skills/eval-aveugle/`.

### Notes du juge (sur 60)

| Cas | /chatgpt-ads-skills | chatgpt-ads-builder | Claude sans Skill | Gagnant |
|---|---|---|---|---|
| 1 · Plantéa (B2C, clics) | **47** | 46 | 45 | /chatgpt-ads-skills |
| 2 · Factoria (B2B, conversions) | 44 | **46** | 42 | chatgpt-ads-builder |
| 3 · Assurly (assurance santé, France) | **51** | 29 | 41 | /chatgpt-ads-skills |

### Mesures objectives (`eval-aveugle/mesurer.py`)

| | /chatgpt-ads-skills | chatgpt-ads-builder | Claude sans Skill |
|---|---|---|---|
| Titres au-delà de 24 caractères, copies au-delà de 48 | 0 | 0 | 0 |
| Allégations absentes de la page ou des réponses | 0 | 0 | 0 |
| Campagne produite pour un secteur non éligible (cas 3) | non | **oui** | non |
| Annonces (cas 1 / 2) | 40 / 46 | 10 / 6 | 9 / 7 |
| Enchère proposée quand l'utilisateur la demandait (cas 1) | oui (3, dans la fourchette conseillée par OpenAI) | non | non |

### Ce que l'éval apprend

- **Victoire nette sur le cas sensible.** Seule notre configuration cite la
  règle exacte : assurance et santé admises aux États-Unis seulement,
  généralement interdites ailleurs (règles v1.6). Elle arrête sans
  chercher de contournement.
  - `chatgpt-ads-builder` livre une campagne d'assurance santé en France
    « prête à partir » : c'est la seule erreur grave de l'éval.
  - Claude sans Skill bloque le fichier par prudence, mais sous-estime
    l'interdiction.
- **Défaite sur le cas B2B (44 contre 46).** Le juge reproche :
  - 6 groupes et 46 annonces pour 40 € par jour : l'apprentissage est
    trop fragmenté ;
  - des groupes qui se recouvrent ;
  - deux petites inventions (« démo en ligne », « Voir l'appli ») ;
  - des hints formulés en négation.

  Il reconnaît en revanche le meilleur traitement de la mesure :
  - événement standard choisi ;
  - enchère oCPC bien définie ;
  - réforme traitée sans promesse.
- **Le volume ne paie pas sur un petit budget.** 40 annonces pour 30 € par
  jour (environ 10 clics) rendent le test illisible.
- **Un titre en double** entre deux groupes, alors que le rapport annonçait
  « ni doublon ».

### Corrections apportées après l'éval

- Le script signale un nombre d'annonces supérieur au double des clics
  possibles par jour (budget ÷ enchère), et un titre repris dans plusieurs
  groupes. 3 tests ajoutés.
- Le SKILL.md :
  - adapte le volume au budget (2 ou 3 annonces par groupe pour
    commencer, au choix de l'annonceur) ;
  - préfère moins de groupes bien distincts ;
  - interdit les reformulations qui changent le sens (« notre botaniste »,
    « en ligne »).
- `commun/faits.md` § 4 : le point « volume » cite l'éval.

Hints formulés en négation : ils restent permis, comme le demande le brief
d'Aleksander, et sont présentés comme une hypothèse. Le juge les a jugés
inutiles, parce que les hints ne sont pas booléens. Point ouvert.

## Limites connues

- L'éval porte sur 3 cas et un seul juge, lui-même un modèle. Les écarts
  des cas 1 et 2 (1 à 4 points) sont dans la marge d'un juge humain ;
  celui du cas 3 (22 points) ne l'est pas.
- Le contrôle des allégations est lexical (chiffres, prix, superlatifs,
  promesses connues) : « en ligne » ou « application » passent, d'où la
  relecture humaine.
- Le script contrôle l'URL et l'extension des images, pas leur taille ni
  leur format carré : c'est dans la checklist de relecture.
- L'acceptation du modèle d'import du pack par Ads Manager reste à
  confirmer par un import d'essai.
