---
name: fondation-skills
description: >-
  Pack Fondation en français, en un seul Skill : construire et tenir à jour
  le contexte qu'une IA doit lire avant d'écrire pour une entreprise. Fiche
  entreprise (identité vérifiée par les mentions légales, SIREN et TVA
  contrôlés, offre, alternatives, différence prouvée, positionnement,
  objectifs, contraintes de secteur et de données selon la CNIL). Chaque fait
  est étiqueté LIVE, À CONFIRMER ou RETIRÉ, daté et sourcé ; rien n'est écrit
  sans accord. Utilise-le pour « présente mon entreprise », « fiche
  entreprise », « positionnement », « mets à jour mon contexte ». Pas pour un
  avis juridique.
---

# Fondation Skills (Join Médicis)

Ce Skill regroupe les modules du pack Fondation. Chaque module est un mode
d'emploi complet rangé dans `modules/<nom>/<nom>.md`, avec ses fichiers
(références, scripts, socle `commun/`) dans le même dossier.

## Choisir le module

| Module | Quand l'utiliser |
|---|---|
| `fondation-entreprise` | premier usage, « voici mon site », fiche entreprise, positionnement, contraintes, mise à jour du contexte |

Les modules `fondation-clients` (clients idéaux, personas étayés) et
`fondation-preuves` (mots des clients, promesses vérifiées) arrivent dans les
prochaines versions. La voix a son propre pack : `/tone-of-voice`.

## Comment travailler

1. Lis le module choisi en entier, puis son `commun/regles.md`.
2. Les scripts Python (sans dépendance) se lancent depuis le dossier du
   module. Sans exécution de code, applique leurs règles à la main et dis-le.
3. Les fichiers de contexte vivent dans les connaissances du Projet :
   montre le fichier complet et laisse l'utilisateur l'ajouter.
