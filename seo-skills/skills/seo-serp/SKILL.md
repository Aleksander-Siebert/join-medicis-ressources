---
name: seo-serp
description: >-
  Analyse la SERP et les concurrents d'une requête : type de page que Google
  récompense, structure et profondeur des 5 à 10 premiers résultats, éléments
  de SERP (extrait optimisé, questions, AI Overview, pack local, vidéos),
  angles et manques à exploiter, score des concurrents. Utilise-le pour
  « analyse la SERP », « qui se positionne sur », « que font les concurrents »,
  avant un brief ou quand une page ne se positionne pas.
---

# seo-serp

On ne bat pas une SERP qu'on n'a pas lue. Ce Skill la lit à l'envers : partir
de ce que Google classe pour savoir quelle page construire.

## 1. Relever la SERP

Pour la requête (et le pays, `google.fr` par défaut) :

- les 10 premiers résultats organiques : URL, type de page, format, longueur
  estimée, angle ;
- les éléments de SERP : extrait optimisé (paragraphe, liste, tableau),
  « Autres questions posées » (toutes les questions), AI Overview et les
  sources qu'il cite, pack local, vidéos, images, recherches associées,
  annonces (leurs arguments révèlent ce qui fait acheter).

Données : connecteur Semrush ou Ahrefs s'il est là, sinon recherche web.
Écarte des concurrents « réels » les sites qui ne sont pas comparables :
Wikipédia, forums, réseaux sociaux, annuaires, sites d'outils SEO, sites
publics (mais garde-les comme **sources** à citer).

## 2. Trouver le consensus

- **Type de page dominant** : guide, liste, comparatif, page produit, outil,
  page locale. Plus de 60% des résultats du même type = consensus fort.
  Viser un autre type = perdre d'avance, sauf si la SERP est fragmentée.
- **Profondeur attendue** : longueur moyenne, niveau de détail.
- **Ce que Google montre en premier** : si l'extrait optimisé est un tableau,
  la page doit contenir ce tableau.

## 3. Noter les concurrents

Pour les 3 à 5 vrais concurrents, une note sur 40 :

| Critère | /10 |
|---|---|
| Profondeur (couverture du sujet) | |
| Mise en forme (lisibilité, tableaux, résumé) | |
| SEO (title, H1, plan, liens, schema) | |
| Confiance (auteur, sources datées, expertise visible) | |

## 4. Les manques à exploiter

- **Sujets absents** de tous les concurrents ;
- **sujets survolés** ;
- **défauts de qualité** : chiffres périmés, aucun expert, aucune source ;
- **gain d'information** (obligatoire) : ce que **notre** page apportera
  qu'aucune ne donne : données propres, cas réel, expérience de terrain,
  méthode, outil. « Plus de détails » ne compte pas.

## 5. Les questions du lecteur

À partir des « Autres questions posées », des recherches associées et des
annonces, écris 3 user stories :
« En tant que [persona], je veux [objectif], parce que [motivation], mais je
bloque sur [frein]. »

## Sortie

```
SERP · « assurance santé expatrié » · google.fr

CONSENSUS     pages produit hybrides (6/10), 1 500-2 500 mots, tableau des garanties
ÉLÉMENTS      AI Overview (cite 3 courtiers + service-public.fr), 6 questions, pas de pack local
CONCURRENTS   1. concurrent-a.example  31/40  manque : aucun exemple chiffré
              2. ...
MANQUES       - personne n'explique la différence CFE / premier euro avec un cas réel
GAIN D'INFO   notre cas : famille de 4 à Singapour, ce que le contrat a remboursé
QUESTIONS     - Est-ce obligatoire ? - Combien ça coûte ? - ...
```

Puis propose `/seo-brief`.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : ne décris pas une page que tu n'as pas pu lire ; dis-le.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
