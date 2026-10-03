# Exemple complet : la stratégie de Camille

> Les faits de cet exemple sont fictifs (Assurly, Camille et leurs chiffres) : ils
> montrent la méthode. Ne les reprends jamais dans une réponse à l'utilisateur.

Personne fictive : Camille, responsable acquisition chez Assurly
(assurly.example), qui lance une activité de conseil le soir, avec l'accord de
son employeur. Fichier d'entrée : `brief.py --exemple`.

## Les cinq questions (extrait)

> **Q1.** Qu'est-ce qui doit être vrai dans 90 jours pour que ça ait valu le
> coup ? *Recommandé : un résultat qu'un tiers peut vérifier, pas un nombre
> d'abonnés.*
>
> **Camille** : Avoir 2 000 abonnés.
>
> **Relance** : Si tu avais 2 000 abonnés et aucun client, ce serait réussi ?
>
> **Camille** : Non. 6 rendez-vous avec des responsables marketing d'assureurs
> ou de courtiers.

> **Q3.** Combien de minutes par semaine, sur une mauvaise semaine ?
> *Recommandé : le chiffre honnête.*
>
> **Camille** : 5 heures.
>
> **Relance** : Et la semaine de clôture du trimestre chez Assurly ?
>
> **Camille** : Plutôt 4 heures.

> **Q5.** De quoi tu ne parleras pas ? *Recommandé : deux sujets, dont le
> sujet tendance sur lequel tu n'as aucun avantage.*
>
> **Camille** : L'IA en général, j'en sais autant que tout le monde. Et jamais
> d'assureur nommé : confidentialité.

## Le brief vérifié

```
python3 scripts/brief.py --exemple
BRIEF  VALIDE
Critères à 90 jours (vérifiables par un tiers, à chiffrer) :
  · {{n}} conversations entrantes de responsables marketing d'assureurs et de courtiers en ligne
    de 50 à 300 salariés dont le coût par lead monte, dont au moins une qui cite un post précis
  · {{n}} rendez-vous qualifiés obtenus après un échange sur LinkedIn
  · une personne de la cible sait dire en une phrase ce que tu fais (test de la phrase)
```

Chiffré avec Camille : 10 conversations entrantes, 6 rendez-vous.

Phrase de positionnement raccourcie avec elle : « J'aide les assureurs en
ligne à faire baisser leur coût par lead, en partant des appels clients. »

## Les piliers

| Pilier | Part | Étape | Pourquoi moi | Preuve |
|---|---|---|---|---|
| Acquisition en assurance, chiffres à l'appui | 45% | éducation | 3 ans à la tête de l'acquisition d'Assurly | coût par lead de 41 € à 23 € en 4 mois |
| Ce que disent les clients qui partent | 25% | notoriété | 60 appels de résiliation écoutés | (expérimental, à prouver) |
| Coulisses de l'activité de conseil | 15% | notoriété | je la lance | expérimental |
| Offre de diagnostic | 15% | conversion | c'est mon offre | à construire |

Conversion à 15% : moins d'un post sur cinq.

## Le budget

```
python3 scripts/budget.py --minutes 240 --etape depart --posts 2
BUDGET LINKEDIN  TIENT  ·  240 min/semaine
Posts : 2 (texte, texte), 90 min réponses comprises
Commentaires : 25 (5.0 par jour ouvré)
Semaine minimale (quand tout déraille, ~75 min) : 1 post texte le même jour chaque semaine,
1 commentaire utile par jour ouvré, réponse à chaque commentaire sous 24 h.
```

Camille voulait 4 posts par semaine : `budget.py --minutes 240 --etape depart
--posts 4` rend NE TIENT PAS : 4 posts × 45 min + 24 commentaires × 6 min =
324 min pour 240. Elle garde 2 posts.

## Newsletter

Pas maintenant : environ 400 relations (éligible peut-être), mais 2 posts par
semaine prennent tout le budget, et sous 500 abonnés les retours seraient trop
rares pour juger le sujet. Revue dans 3 mois.

## Ce qui est écrit dans contexte.md (extrait, après « oui »)

```
## Qui je suis
- Rôle : marketeuse en interne qui lance une activité de conseil (accord de l'employeur : À CONFIRMER par écrit)
- Objectif LinkedIn à 90 jours : 6 rendez-vous qualifiés avec des responsables marketing d'assureurs ou de courtiers en ligne
- Budget : 240 min par semaine (mesuré sur la semaine de clôture)

## Positionnement
- Phrase : J'aide les assureurs en ligne à faire baisser leur coût par lead, en partant des appels clients.
- Anti-positionnement : l'actualité générale de l'IA ; les comparatifs d'assureurs nommés

## Preuves
| Coût par lead de 41 € à 23 € en 4 mois, budget constant | LIVE | 2026-10-02 | reserve.md |
| 30% de non-renouvellement (comité de direction de juin) | À CONFIRMER | 2026-10-02 | interne, publiable ? |
```

Suite proposée : `/linkedin-interview` (reserve.md n'a qu'une réussite), puis
`/linkedin-profile` (le titre découle de la phrase de positionnement).
