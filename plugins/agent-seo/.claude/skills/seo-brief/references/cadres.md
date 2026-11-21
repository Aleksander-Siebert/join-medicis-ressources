# Les 4 cadres de structure

Un cadre par page, choisi selon le type de page et l'objectif. On ne mélange
pas deux structures. Méthode tirée du workflow de rédaction de l'utilisateur
et d'une carte des frameworks de formation (Empirik, SEO Edition), réécrite.

## Choisir

```
L'objectif principal est la conversion ?
├─ oui → PAS
└─ non
   ├─ c'est une actualité, une annonce, une réponse directe ? → pyramide inversée
   └─ non
      ├─ la page doit aussi convertir (comparatif, avis, « meilleurs X ») ? → AIDA
      └─ non → MECE (guide complet, page pilier, sujet concurrentiel)
```

| Cadre | Pages | Objectif | À éviter pour |
|---|---|---|---|
| PAS | page produit, page de conversion, page catégorie orientée achat | conversion | guides informationnels, actualités |
| AIDA | comparatif, avis, « meilleurs X », page de campagne | information + conversion | guide pilier très informatif, actualité (trop lourd) |
| MECE | guide complet, page pilier, sujet très concurrentiel | couvrir toutes les intentions d'un sujet | format court, page de conversion pure |
| Pyramide inversée | actualité, annonce, réponse directe à une question | l'essentiel tout de suite | page produit, guide long |

Annonce le cadre avec une phrase de justification : « Guide MECE : la
requête est informationnelle et les 7 premiers résultats sont des guides. »

## PAS : Problème, Agiter, Solution

- **Problème** : la douleur exacte, dès la première phrase, avec les mots
  que le lecteur tape dans Google.
- **Agiter** : les conséquences (temps, argent, risque), **crédibles et
  sourcées**. Pas de dramatisation : elle détruit la confiance, surtout en
  YMYL. Un chiffre d'agitation sans source devient une formulation sans
  chiffre.
- **Solution** : l'offre nommée, le bénéfice principal (pas la liste des
  fonctions), une preuve (`site-context.md` §9 ou `reserve.md`), un seul
  appel à l'action.

Contrôle : problème dit avec les mots du lecteur · agitation crédible et
sourcée · solution nommée avec son bénéfice · une preuve réelle · un seul
appel à l'action.

## AIDA : Attention, Intérêt, Désir, Action

- **Attention** : un fait, un chiffre sourcé ou une affirmation forte, liés
  au sujet. Jamais « Dans cet article, nous allons voir ».
- **Intérêt** : les bénéfices pour le lecteur, les questions qu'il se pose.
- **Désir** : preuves vérifiables (avis datés, résultats, cas réels),
  comparaison avec l'alternative, sans dénigrer. Un comparatif nommé suit
  `comparatif.md`.
- **Action** : verbe + bénéfice immédiat, friction réduite. Une
  « garantie » ou un « sans engagement » seulement si le contrat le dit.

Contrôle : accroche factuelle · bénéfices distincts des fonctions · au moins
une preuve vérifiable · appel à l'action sans friction. Sur un format court,
PAS est plus efficace.

## MECE : sans recouvrement, sans manque

*Mutually Exclusive, Collectively Exhaustive.*

- **Sans recouvrement (ME)** : chaque H2 a son périmètre. Test : « si je
  supprime cette section, une autre l'absorbe-t-elle ? » Si oui, c'est un
  doublon. `couverture.py couvrir` signale les sections qui répondent aux
  mêmes requêtes et celles dont le vocabulaire est trop proche.
- **Sans manque (CE)** : chaque requête du champ sémantique (20 à 30
  requêtes réelles) est rattachée à une section. Une requête orpheline est
  une section à créer, ou une requête qui appartient à une autre page.
  `couverture.py couvrir` le mesure.
- **Réponse directe** en 1 à 2 phrases en tête de chaque H2, puis le
  détail : c'est ce que le lecteur pressé lit, et ce que les extraits et les
  réponses génératives reprennent.
- Chaque H2 a assez de matière pour exister : une section de deux lignes se
  fusionne ou devient un H3. (Pas de minimum de mots : c'est le sujet qui
  décide.)

Contrôle : test de non-recouvrement fait · toutes les requêtes couvertes ou
renvoyées vers une autre page · réponse directe en tête de section · aucune
section creuse.

## Pyramide inversée

- **L'essentiel** : qui, quoi, quand, où, dans les 2 premières phrases, avec
  la requête.
- **Le contexte** : pourquoi, origine, conséquences, sources.
- **Les détails** : textes officiels, tableaux, liens, pour les plus
  impliqués.

Contrôle : l'information principale tient dans les 2 premières phrases ·
contexte sourcé et daté · détails en fin de page. On ne « construit pas
vers » l'information.

## Ce que les cadres ne disent pas

- Ils structurent, ils ne remplissent pas : le gain d'information vient de
  `reserve.md`, `site-context.md` ou d'une source lue, jamais du cadre.
- Les exemples chiffrés qu'on trouve dans les fiches de cadres (« 78% des
  utilisateurs abandonnent… ») sont des illustrations sans source : ne les
  reprends jamais dans un plan ou un article.
