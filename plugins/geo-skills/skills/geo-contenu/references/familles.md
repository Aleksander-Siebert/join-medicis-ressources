# Familles de faits par type de question

Une question appelle des faits précis. Un moteur de réponse qui compose sa
réponse cherche ces faits dans plusieurs pages ; une page qui les réunit,
sourcés, sert le lecteur et reste une bonne candidate. Ces listes sont
**déduites** des questions, pas observées dans les moteurs.

`contenu.py` repère le type de question par ses mots :

| Type | Mots repérés | Exemple |
|---|---|---|
| prix | combien, prix, tarif, coût, coûte, cher | « Combien coûte une mutuelle pour indépendant ? » |
| comparaison | ou, vs, versus, entre, différence, comparatif | « CFE ou premier euro ? » |
| procédure | comment, démarche, étapes, procédure | « Comment résilier sa mutuelle ? » |
| définition | qu'est-ce, c'est quoi, définition, signifie | « Qu'est-ce que la CFE ? » |
| choix | tout le reste | « Quelle mutuelle pour un freelance ? » |

« Où acheter… » est un choix (le « où » de lieu n'est pas le « ou » de
l'alternative).

## Les familles

| Type | Familles | Repérée par |
|---|---|---|
| prix | montant chiffré ; période ; ce qui fait varier ; inclus ou exclu ; date du tarif | montant en €, « par mois », « selon l'âge », « inclus », mois et année |
| comparaison | critères nommés ; tableau ou liste ; verdict par profil ; limites de chaque option | mots de critère, tableau ou 3 puces, « si vous », « en revanche » |
| procédure | étapes numérotées ; prérequis ou documents ; durée ; coût ; erreurs fréquentes | liste numérotée, « justificatif », durée, montant ou « gratuit », « attention » |
| définition | définition en une phrase ; exemple ; différence avec un terme voisin ; cadre légal ou source | réponse en tête, « par exemple », « à ne pas confondre », source nommée |
| choix | options nommées ; critères ; pour qui ; prix ; limites ou avis négatifs | 3 noms propres ou plus, « choisir », « si vous », montant, « inconvénient » |

## Confirmer avec les moteurs

1. Dans `/geo-visibilite`, prends les réponses à la question visée.
2. Note les faits qu'elles donnent (un prix, un délai, un critère) et les
   pages qu'elles citent.
3. Un fait présent dans la plupart des réponses et absent de la page est
   une famille manquante **observée** : écris-le comme tel.
4. Une famille déduite qu'aucune réponse ne donne passe en dernier.

## Limites

- La détection est lexicale : « présente » veut dire qu'un indice est là,
  pas que le fait est juste ni complet.
- Une page peut couvrir toutes les familles et rester générique : la
  première main ne se détecte qu'en partie (`reecrire.md` §3).
