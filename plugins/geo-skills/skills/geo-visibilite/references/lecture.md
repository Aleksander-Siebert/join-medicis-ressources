# Lire une mesure et décider

## 1. L'échelle de visibilité

Sources : marketingskills (Corey Haines), elmo, Profound (MIT), réécrit.

| Niveau | Ce que ça veut dire | Ce qui le gouverne | Où le voir |
|---|---|---|---|
| Récupéré | le moteur a lu une page du site | accès des robots, page indexée, pertinence | journaux du serveur, requêtes d'ancrage de Bing ; invisible dans une réponse |
| Cité | un lien vers le site dans la réponse | page utile à consulter : claire, à jour, sourcée | `citée` |
| Mentionné | la marque est nommée | ce que le web dit de la marque | `mentionnée` |
| Recommandé | la marque est conseillée pour le besoin | **consensus du web** : avis, comparatifs, presse, forums | `recommandée` |
| Déconseillé | la marque est citée comme à éviter | avis négatifs, faits périmés, comparaisons défavorables | `déconseillée` |

Être cité sans être recommandé est courant : le moteur consulte la page de
la marque pour décrire la catégorie, puis recommande d'après ce que disent
les autres.

Homonymes, réglés par le script :

- un concurrent dont le nom contient la marque (« Assurly Pro » pour
  « Assurly ») compte pour le concurrent, s'il est déclaré en
  `--concurrent` ;
- un domaine homonyme (« assurly.app » quand la marque est sur
  `assurly.example`) ne compte pas comme une mention : déclare les domaines
  de la marque avec `--domaine`.

## 2. Ordre de lecture

1. **Témoins.** Un témoin en dérive arrête la lecture : saisie, moteur ou
   outil a changé.
2. **Marges.** Une marge de ±30 points interdit les conclusions fines ;
   dis « exploratoire » et ce qu'il faudrait pour confirmer.
3. **Moteur par moteur**, jamais un total seul.
4. **Questions perdues** et leurs sources : c'est le plan de travail.
5. **Mentionnée contre recommandée**, puis les mises en garde.

## 3. Diagnostic

| Constat | Cause probable | Suite |
|---|---|---|
| Absente partout, témoin « présent » raté | robots bloqués, site non indexé, marque inconnue des modèles | `/geo-acces`, puis `/geo-audit` |
| Présente sur Perplexity, absente de ChatGPT | sources et robots différents (OAI-SearchBot, sources tierces différentes) | `/geo-acces` pour le robot, sources citées par ChatGPT sur les questions perdues |
| Mentionnée, rarement recommandée | consensus tiers faible ou défavorable | `/geo-mentions` (sources citées sur ces questions) |
| Citée, peu mentionnée | la page sert de source sur la catégorie, la marque n'est pas associée au besoin | `/geo-contenu` (dire clairement qui fait quoi pour qui) et `/geo-entite` |
| Déconseillée, ou faits faux | avis négatifs, page périmée, comparatif tiers | `/geo-exactitude` |
| Questions perdues dominées par un comparateur ou un média | ce site tiers façonne la liste | `/geo-mentions` : être présent et exact sur ce site, sans acheter d'avis |
| Questions perdues dominées par le site d'un concurrent | il a la page qui répond, pas le site | `/geo-contenu` : la page qui manque, avec un vrai gain d'information |
| Rien ne bouge après une action | délai de prise en compte, ou l'action ne touchait pas la bonne couche | garder la mesure, journal de `/geo-audit`, arrêter après deux tours sans effet |

## 4. Ce qu'on ne dit jamais

- « ChatGPT nous classe 2e » (pas de rang stable).
- « La visibilité a baissé de 12 points » sans verdict de `comparer`.
- « Notre article a fait remonter la marque » sans action datée ni groupe
  de comparaison : c'est une observation, pas une cause.
- Un pourcentage d'étude d'éditeur transformé en prévision pour le site.
