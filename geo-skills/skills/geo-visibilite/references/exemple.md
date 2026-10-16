# Exemple de bout en bout (Assurly, fictif)

Données de test du pack (`evals/geo-visibilite/`), **réponses fictives** :
elles montrent la mécanique, pas ce que disent vraiment les IA.

## 1. La demande

« Est-ce que les IA recommandent Assurly quand une famille cherche une
assurance santé pour partir à l'étranger ? »

Décision visée : savoir si Assurly est dans la liste courte des familles
qui s'expatrient, face à April International, Allianz Care et Cigna (jeu
figé, tiré de `site-context.md`).

## 2. Le portefeuille

9 questions : 6 dans le cœur (5 sans la marque, soit 83%), 1 exploratoire,
2 témoins (`portefeuille-assurly.csv`).

```
$ python3 scripts/visibilite.py portefeuille portefeuille-assurly.csv --marque Assurly
PORTEFEUILLE · 9 questions · cœur version 68ecb76c
  cohortes : coeur 6, exploratoire 1, temoin 2
  cœur sans la marque : 83% (visé : 70 à 85%)
  intentions du cœur : decouverte 2, comparaison 1, alternative 1, usage 1, marque 1
  aucune alerte
```

## 3. La mesure (ChatGPT 8 réponses, Perplexity 4)

```
$ python3 scripts/visibilite.py mesurer reponses-septembre.txt --marque Assurly --domaine assurly.example \
    --concurrent "April International" --concurrent "Allianz Care" --concurrent Cigna --portefeuille portefeuille-assurly.csv

VISIBILITÉ IA · Assurly · mesuré (réponses collées) · 12 réponses · 6 questions · 2 moteur(s)

MOTEUR        MENTIONNÉE            CITÉE (lien)        RECOMMANDÉE         DÉCONSEILLÉE  PART DE VOIX
ChatGPT       50% (4/8, 22-78%)     13% (1/8, 2-47%)    13% (1/8, 2-47%)    1/8           31% (4/13, 13-58%)
Perplexity    50% (2/4, 15-85%)     0% (0/4, 0-49%)     0% (0/4, 0-49%)     0/4           50% (2/4, 15-85%)
TOTAL         50% (6/12, 25-75%)    8% (1/12, 1-35%)    8% (1/12, 1-35%)    1/12          35% (6/17, 17-59%)

Exploratoire : moins de 5 passages par question pour ChatGPT, Perplexity.

TÉMOINS
  T01   attendu present  mentionnée 2/2  OK
  T02   attendu absent   mentionnée 0/2  OK

QUESTIONS PERDUES (un concurrent cité, la marque jamais)
  P01   ChatGPT       Je pars travailler à Dubaï avec deux enfants, quelle assurance s…
        concurrents : Allianz Care 2, April International 2, Cigna 1 · sources : lelynx.fr, quechoisir.org
  P02   Perplexity    Quelle est la meilleure assurance santé pour un expatrié françai…
        concurrents : Cigna 1 · sources : reddit.com

SOURCES CITÉES PAR CLASSE
  comparateur 1 · consommateurs 1 · propre site 1 · autre 1 · institution 1 · reference 1 · communaute 1
```

## 4. La réponse rendue à l'utilisateur

```
VISIBILITÉ IA · Assurly · mesuré (réponses collées) · 12 réponses · 6 questions · ChatGPT, Perplexity
Cœur version 68ecb76c · série de septembre 2026 · 1 à 2 passages par question (exploratoire)

ChatGPT : mentionnée dans 50% des réponses (4/8, entre 22 et 78%), recommandée 1 fois sur 8, déconseillée 1 fois.
Perplexity : mentionnée dans 50% des réponses (2/4, entre 15 et 85%), jamais recommandée ni liée.
Témoins : OK.

CE QUE ÇA VEUT DIRE
1. Trop peu de passages pour conclure : les marges vont de ±25 à ±35 points. Il faut 5 passages par question
   sur le cœur (30 réponses par moteur) pour une première tendance.
2. La question la plus précieuse (famille à Dubaï) est perdue sur ChatGPT au profit d'April International,
   Allianz Care et Cigna, avec pour sources un comparateur (lelynx.fr) et Que Choisir → /geo-mentions.
3. Une réponse de ChatGPT dit qu'Assurly est « à éviter selon certains avis » (P03) → /geo-exactitude,
   pour retrouver la source de cette phrase.

À VÉRIFIER
- Le site est-il inclus dans le réglage « IA générative » de Search Console ? (/geo-acces)

Skill suivant proposé : /geo-exactitude sur la mise en garde de P03.
```

## 5. Un mois plus tard

```
$ python3 scripts/visibilite.py comparer reponses-septembre.txt reponses-octobre.txt --marque Assurly \
    --domaine assurly.example --portefeuille portefeuille-assurly.csv

COMPARAISON · Assurly · 2 paires moteur et question communes (9 écartées, absentes d'une période)

ChatGPT
  mentionnée  50% (2/4, 15-85%)  → 100% (4/4, 51-100%)  +50 pts (-10 à +85) · PAS DE CHANGEMENT DÉTECTABLE
```

Même +50 points ne suffisent pas avec 4 réponses par période : on ne
l'annonce pas comme une hausse. La série d'octobre ne couvrait ni
Perplexity ni la plupart des questions : la comparaison le dit (9 paires
écartées) au lieu de les mélanger.
