# Réécrire une section

Une section se réécrit quand elle manque un contrôle **et** qu'elle porte
sur la question visée. Les autres attendent.

## 1. Avant, après (exemples fictifs, Assurly)

### Préambule

Avant :
> Dans cet article, nous allons voir pourquoi la mutuelle est un sujet
> important pour tous les indépendants.

Après :
> Un indépendant n'a pas de mutuelle d'entreprise : il la choisit et la
> paie seul, et la loi Madelin permet d'en déduire les cotisations sous
> conditions {{à compléter : plafond et source, BOFiP}}.

Le préambule disparaît ; la première phrase dit ce que le lecteur venait
chercher. Le plafond n'est pas écrit de mémoire.

### Pronom en tête et renvoi

Avant :
> Elle couvre l'hospitalisation, les soins courants et l'optique. Comme vu
> plus haut, le prix varie selon ces garanties.

Après :
> La formule Confort d'Assurly couvre l'hospitalisation, les soins courants
> et l'optique. Son prix varie selon le niveau de remboursement choisi pour
> chacune de ces garanties.

### Statistique sans source

Avant :
> Les tarifs ont augmenté de 8% en un an.

Après, deux issues seulement :
> Les tarifs des complémentaires santé individuelles ont augmenté de
> {{à compléter}}% en 2026, selon {{source : DREES, Mutualité française,
> rapport daté}}.

ou la phrase sort du texte. Jamais un chiffre « plausible ».

### Promesse

Avant :
> Assurly est le meilleur courtier du marché, n°1 de la mutuelle en ligne.

Après :
> Assurly compare {{à compléter : nombre}} assureurs partenaires ; ses
> clients lui donnent {{à compléter : note}} sur {{nombre}} avis
> {{plateforme, date}}.

Un classement « n°1 » n'est gardé que si une source indépendante et datée
le dit, avec son périmètre (« n°1 des ventes en ligne en 2025 selon X »).

## 2. Le format suit la question

| Question | Format | Piège |
|---|---|---|
| Qu'est-ce que… | définition en une phrase, puis exemple, puis différence avec le terme voisin | définir par un synonyme |
| Comment… | étapes numérotées, chacune avec son verbe ; prérequis avant ; durée et coût | étapes noyées dans un paragraphe |
| X ou Y | tableau de critères, puis verdict par profil (« si vous… ») | verdict unique pour tout le monde |
| Combien… | fourchette chiffrée, période, ce qui fait varier, inclus et exclus, date du tarif | « ça dépend » sans dire de quoi |
| Quel… choisir | options nommées, critères, pour qui chacune, limites | liste sans critères |

## 3. Première main

Ce qui distingue une page des cent autres sur la même question, et que
Google nomme contenu original :

- un cas réel, anonymisé (« une graphiste de 34 ans à Lyon… ») ;
- une donnée maison, avec sa méthode (« sur 1 200 dossiers traités en
  2025 ») ;
- une expérience de terrain (« ce que les assureurs refusent le plus
  souvent ») ;
- une citation attribuée à une personne nommée, avec sa fonction.

Demande-les à l'utilisateur. Sans eux, écris `{{à compléter : un cas réel}}`
à l'endroit où il servirait, et dis-le dans la synthèse.

## 4. Ce qu'on ne fait pas

| Pratique | Pourquoi |
|---|---|
| Découper en blocs de 40-60 ou 134-167 mots | aucune source primaire ; Google : pas de longueur idéale (`commun/preuves.md` §7) |
| Ajouter « TL;DR pour les IA », texte caché, consignes aux IA | inutile pour Google ; texte caché détecté par `/geo-agentic` comme instruction dissimulée |
| Ajouter une FAQ pour le balisage | résultats enrichis FAQ arrêtés le 7 mai 2026 ; une FAQ reste utile si les questions sont vraies |
| Bourrer la page de statistiques | une statistique sans source fait perdre la confiance du lecteur |
| Réécrire tout le site d'un coup | impossible de savoir ce qui a joué ; une page, un journal, une remesure |

## 5. Journal

Après publication par l'utilisateur, note dans `apprentissages.md` : page,
date, sections changées, question visée. Remesure avec `/geo-visibilite`
sur la même question 4 à 6 semaines après **[repère praticien]**, et
compare avec `stats.py comparer` : sans écart détectable, on ne conclut
rien.
