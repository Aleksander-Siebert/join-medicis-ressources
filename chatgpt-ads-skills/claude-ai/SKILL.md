---
name: chatgpt-ads-skills
description: >-
  Pack ChatGPT Ads (OpenAI Ads) en français, spécialisé France, en un seul
  Skill de 5 modules : préparer une campagne de 40 à 50 annonces (entretien,
  alerte datée si le secteur est restreint par OpenAI puis campagne quand
  même, allégations étayées, intentions, context hints, titre 24 et copie
  48), passer à 120 annonces ou plus sans doublons, réécrire des exports
  Google Ads, Meta Ads ou Microsoft Ads, retrouver les identifiants
  (ad_group_id, ad_id, image_file_id), contrôler et réparer le fichier
  d'import CSV au schéma d'annonces à 10 colonnes. Utilise-le pour « campagne
  ChatGPT Ads », « annonces ChatGPT », « context hints », « fichier d'import
  ChatGPT », « ChatGPT ads campaign ». Pas pour lancer, piloter ou optimiser
  une campagne, ni pour un avis juridique.
---

# ChatGPT Ads (Join Médicis)

Ce Skill regroupe les modules du pack ChatGPT Ads. Chaque module est un mode
d'emploi complet rangé dans `modules/<nom>/<nom>.md`, avec ses fichiers
(références, scripts, socle `commun/`) dans le même dossier.

## Choisir le module

| Module | Quand l'utiliser |
|---|---|
| `chatgpt-ads-skills` | préparer une campagne : intentions, ad groups, context hints, 40 à 50 annonces, fichier d'import CSV au schéma d'annonces et fiche de paramétrage |
| `chatgpt-ads-bulk` | passer de 40 à 50 annonces à 120 ou plus, par lots, sans doublons |
| `chatgpt-ads-exports` | partir d'exports Google Ads, Meta Ads ou Microsoft Ads |
| `chatgpt-ads-ids` | retrouver `ad_group_id`, `ad_id`, `image_file_id`, `conversion_event_setting_ids` |
| `chatgpt-ads-excel` | contrôler ou réparer le fichier d'import avant l'import dans Ads Manager |

## Comment travailler

1. Lis le module en entier, puis son `commun/regles.md` et son
   `commun/faits.md` ; les règles d'OpenAI sont dans
   `commun/politiques-openai.md`, le droit français dans
   `commun/droit-francais.md`.
2. Les scripts (Python, sans dépendance) se lancent depuis le dossier du
   module. Sans exécution de code, applique leurs règles à la main et écris
   « Contrôle manuel, non vérifié par script ».
3. Secteur restreint par OpenAI (finance, assurance, santé, juridique) :
   alerte datée, pistes conformes, puis le travail demandé, avec des
   annonces véridiques.
4. **Le fichier d'import est toujours un .csv** (UTF-8, virgule), jamais un
   .xlsx : n'utilise pas d'outil ou de Skill de tableur pour le produire.
   Un .xlsx seulement si l'utilisateur le demande en toutes lettres.
5. Rien n'est importé ni lancé : le fichier produit est un brouillon à
   relire par une personne qualifiée.
