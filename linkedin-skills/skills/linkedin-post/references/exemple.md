# Exemple complet : de la matière au reçu

Personne fictive : Camille, responsable acquisition chez Assurly
(assurly.example). Sorties des scripts recopiées telles quelles.

## La demande

> /linkedin-post un post sur la fidélisation

## Avant d'écrire

- `contexte.md` : objectif clients ; piliers « Acquisition en assurance » (45%)
  et « Ce que disent les clients qui partent » (25%, expérimental) ; tutoiement
  dans les posts ; jamais d'assureur nommé.
- `reserve.md`, section Tournants : « Janvier 2026 : 60 résiliations
  rappelées ; je croyais que c'était le prix ; la moitié parlait du délai de
  remboursement ». Section Réussites : « Réduit le délai de remboursement de
  21 à 9 jours en 3 mois ».
- `journal.md` : la formule « chiffre d'abord » a servi mardi dernier.
- Objectif choisi avec Camille : **commentaires**.

Une question posée, une seule : « Les résiliations ont baissé de combien
après ? » Réponse : « Je ne peux pas donner le chiffre. » La phrase reste
qualitative, sans chiffre inventé.

## Trois accroches

```
1. Erreur datée     J'ai cru pendant deux ans que nos clients partaient pour le prix.
2. Contre-pied      Tout le monde dit qu'on fidélise par le prix. 60 appels de résiliation m'ont dit autre chose.
3. Scène            « Je pars parce que j'ai attendu trois semaines mon remboursement. » Janvier, appel n°14 sur 60.

Je publierais la 1 : elle porte un revirement daté, c'est le pilier
expérimental, et le contre-pied ajouterait un contraste dont le post n'a pas besoin.
```

## Le post

```
J'ai cru pendant deux ans que nos clients partaient pour le prix.

En janvier, on a rappelé 60 assurés qui venaient de résilier. La moitié parlait du délai de remboursement. Le prix venait loin derrière.

La direction commerciale voulait baisser nos tarifs. On a d'abord raccourci le délai de remboursement : de 21 à 9 jours, en 3 mois.

On n'a pas touché aux tarifs. Les résiliations du trimestre ont baissé, et le comité a arrêté de parler de prix.

Ce que je vérifie maintenant avant toute réunion sur la fidélisation : les appels de résiliation de la semaine.

Vous écoutez vos clients qui partent, ou seulement ceux qui restent ?
```

## Contrôles

```
lint_post.py --mediane 900
POST  99/100  PRÊT
634/3000 caractères · 0 hashtag(s) · 0 lien(s) · 0 contraste(s) · 0 triade(s) · 0 appel(s) à l'action
[INFO] accroche : Pas de chiffre en première ligne.

detect.py
SCORE HUMAIN  79.1   OK (se lit humain)
```

L'info est assumée : la formule « chiffre d'abord » a servi la semaine
dernière, et « deux ans » porte la durée.

## Le reçu

```
POST PRÊT · 2026-10-06
formule :          L'erreur datée (erreur-datee)        objectif : commentaires
format :           texte                                pilier : Ce que disent les clients qui partent · étape : notoriété
longueur :         634 caractères (ta médiane : 900)
contrôle :         lint 99 PRÊT · humaniseur 79.1 OK · fidélité : tous les faits viennent de reserve.md
appel à l'action : aucun (post de notoriété ; l'offre de diagnostic attendra un post d'éducation)
premier commentaire : « Pour ceux qui veulent essayer : on a gardé une grille de 6 questions pour ces appels. Je la mets ici si ça intéresse. »
visuel :           inutile (le texte porte le revirement)
potentiel de sauvegarde : moyen, parce que la dernière ligne donne une habitude applicable
à publier :        jeudi 8 h 15 (créneau du plan)
à vérifier :       nom d'Assurly : citable (contexte.md) ; « la direction commerciale » : la mention convient-elle à ta direction ?

Réponds « ok » pour l'ajouter au journal, ou dis-moi ce qu'il faut changer.
```

Le premier commentaire ne demande rien en échange : la grille sera donnée à
tous, pas contre un mot-clé.

## Ce que le Skill n'a pas fait

- Inventer « −23% de résiliations » pour rendre la 4e phrase plus forte, ou
  un pourcentage de baisse de tarifs que Camille n'a pas donné.
- Ouvrir par « Pourquoi vos clients partent-ils ? ».
- Ajouter « Le résultat ? » avant le délai de remboursement.
- Nommer un assureur partenaire.
- Publier.
