# Méthode : décrire, tester, expérimenter

D'après `evidence_thresholds.md`, `linkedin_metrics_canon.md` et les scripts
de `linkedin-analytics` (alirezarezvani, claude-skills, MIT), réécrits en
français et complétés (lecture de l'export .xlsx et de `journal.md`, motifs
confondus, séparation page / profil).

## 1. Pourquoi la médiane

Les résultats LinkedIn ont une queue lourde : un post sur vingt fait dix fois
la médiane. La moyenne se laisse tirer par ce post, l'écart-type explose, et la
« moyenne » décrit un post qui n'existe pas. La médiane et l'écart absolu
médian (MAD) restent stables (Tukey, *Exploratory Data Analysis*, 1977 ;
Taleb, *Statistical Consequences of Fat Tails*, 2020).

CV robuste = 1,4826 × MAD / médiane. Le facteur 1,4826 rend le MAD
comparable à un écart-type pour une loi normale.

## 2. Les 4 filtres d'un motif

| Filtre | Seuil | Pourquoi |
|---|---|---|
| Taille | 5 posts dedans, 5 dehors | sous 5, la médiane tient à un ou deux posts |
| Effet | 15% d'écart relatif entre médianes | un écart de 3%, même réel, ne change aucune décision |
| Hasard | plus grand que 90% de 2 000 permutations (graine fixe) | test sans hypothèse de loi normale (Good, *Permutation, Parametric and Bootstrap Tests*) |
| Nombre de tests | faux positifs attendus = tests × 0,10 | 20 motifs testés, 2 passent par hasard (Benjamini et Hochberg, 1995) |

Un attribut à deux valeurs (« texte » contre « carrousel ») n'est testé qu'une
fois : l'autre sens est la même comparaison.

Le seuil de 0,10 est volontairement permissif : un motif qui passe est une
**hypothèse à tester**, pas une conclusion.

## 3. Les motifs confondus

Quand deux motifs soutenus désignent presque les mêmes posts (70% ou plus de
recouvrement, dans un sens ou dans l'autre), le script les regroupe : « format
texte », « réponse sous 2 h » et « jeudi » ne sont alors qu'un seul signal.
Aucune statistique sur ces données ne dit lequel est la cause. Seule une
expérience qui fait varier l'un en gardant les autres le peut.

## 4. Le jardin des chemins qui bifurquent

Même sans tester vingt motifs, l'analyste qui aurait choisi un autre
découpage si les données avaient été différentes multiplie les tests sans le
savoir (Gelman et Loken, « The Garden of Forking Paths », 2013). Défense : la
liste des attributs est fixée à l'avance (`--attributs`), et le jour est testé
en dernier.

## 5. L'arithmétique des expériences

Posts par variante = 2 × (z_α + z_β)² × CV² / effet² (Cohen, *Statistical
Power Analysis*, 2e éd.). Avec α = 0,10 et une puissance de 0,80 :

| CV | effet visé | posts par variante | à 2 posts par semaine (A et B) |
|---|---|---|---|
| 0,35 | 30% | 17 | 17 semaines |
| 0,45 | 30% | 28 | 28 semaines |
| 0,45 | 50% | 11 | 11 semaines |
| 0,60 | 30% | 50 | 50 semaines |

(Valeurs calculées par `audit.py experience`.)

La plupart des tests A/B racontés sur LinkedIn ne sont pas faisables au
rythme réel de leur auteur. Réponses honnêtes : tester une variable à gros
effet, accepter un effet minimal détectable plus haut et le dire, ou arrêter
de tester et écrire ce qu'on préfère écrire.

## 6. Les métriques

| Métrique | Ce qu'elle est | Ce qu'elle n'est pas |
|---|---|---|
| Impressions | nombre d'affichages dans un fil | des personnes uniques ; la règle de comptage a changé plusieurs fois, comparer des posts de la même période |
| Taux d'engagement | (réactions + commentaires + republications) / impressions, la définition de ce pack | une valeur comparable aux « benchmarks » publiés, calculés sur d'autres dénominateurs |
| Abonnés gagnés | un effet secondaire | un objectif |
| Conversations entrantes | le résultat qu'on cherche | une métrique de l'export : elle se compte à la main dans `journal.md` |

## 7. Sources

1. Good, P., *Permutation, Parametric, and Bootstrap Tests of Hypotheses*, 3e éd.
2. Gelman, A. et Loken, E., « The Garden of Forking Paths », 2013.
3. Cohen, J., *Statistical Power Analysis for the Behavioral Sciences*, 2e éd.
4. Tukey, J., *Exploratory Data Analysis*, 1977.
5. Benjamini, Y. et Hochberg, Y., « Controlling the False Discovery Rate », *JRSS-B*, 1995.
6. Taleb, N. N., *Statistical Consequences of Fat Tails*, 2020.
7. Aide LinkedIn a704175 (statistiques du créateur, export .xlsx) et a551206 (export des statistiques d'une page).
