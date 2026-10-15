---
name: ads-skills
description: >-
  Pack ChatGPT Ads en français, en un seul Skill : préparer une campagne ChatGPT Ads
  (OpenAI Ads) prête à importer. Entretien d'une question à la fois,
  allégations étayées, carte des intentions, 5 ad groups ou plus, context
  hints écrits comme des situations et testés sur des prompts simulés, 40 à
  50 annonces aux limites du modèle d'import (titre 24, copie 48), idée de
  visuel par groupe, contrôle par script et fichier XLSX au format du
  modèle. Les pratiques non documentées sont données comme hypothèses.
  Utilise-le pour « campagne ChatGPT Ads », « annonces ChatGPT », « context
  hints », « ChatGPT ads campaign ». Pas pour lancer, piloter ou optimiser une
  campagne, ni pour Google Ads, Meta Ads ou LinkedIn Ads, ni pour un avis
  juridique.
---

# ChatGPT Ads (Join Médicis)

Ce Skill regroupe les modules du pack ChatGPT Ads. Chaque module est un mode
d'emploi complet rangé dans `modules/<nom>/<nom>.md`, avec ses fichiers
(références, scripts, modèle d'import, socle `commun/`) dans le même
dossier.

## Choisir le module

| Module | Quand l'utiliser |
|---|---|
| `chatgpt-ads-skills` | préparer une campagne ChatGPT Ads : intentions, ad groups, context hints, annonces, fichier d'import XLSX |

## Comment travailler

1. Lis le module en entier, puis son `commun/regles.md` et son
   `commun/faits.md`.
2. Le script `valider_exporter.py` (Python, sans dépendance) se lance
   depuis le dossier du module. Sans exécution de code, applique ses règles
   à la main, livre les tableaux à coller et écris « Contrôle manuel, non
   vérifié par script ».
3. Rien n'est importé ni lancé : le fichier produit est un brouillon à
   relire par une personne qualifiée.
