---
name: chatgpt-ads-bulk
description: >-
  Fait passer une campagne ChatGPT Ads (OpenAI Ads) de 40 à 50 annonces à
  120 ou plus, sans doublons ni reformulations minimales. Le script analyse
  la construction des annonces existantes : nombre par ad group, structures
  de titre (question, impératif, chiffre, situation, groupe nominal),
  facettes d'intention couvertes (problème, objectif, compromis,
  contrainte, comparaison, occasion, budget, question), angles, mots trop
  répétés, quasi-doublons, allégations. Il planifie ensuite des lots de
  50 au plus, en servant d'abord les groupes les moins garnis. Chaque
  nouvelle annonce est contrôlée contre toutes les autres, puis tout est
  noté (Conserver, Corriger, Supprimer) et exporté au schéma d'annonces.
  Utilise-le pour « passe à 120 annonces », « bulk ChatGPT Ads »,
  « décline mes annonces », « plus de variantes sans doublons ». Pas pour
  créer la campagne de départ (/chatgpt-ads-skills), ni pour inventer des
  allégations pour remplir le volume.
---

# chatgpt-ads-bulk

Monter en volume aide la diffusion seulement si chaque annonce vise une
façon **différente** de décrire le même besoin. Cent reformulations d'une
même phrase n'apportent rien et se relisent mal. Ce Skill part des 40 à 50
annonces de `/chatgpt-ads-skills`, regarde comment elles sont construites,
et ajoute des lots qui comblent ce qui manque.

**À lire avant de commencer :** `commun/regles.md` (zéro invention : le
volume ne justifie aucune allégation nouvelle), `commun/faits.md`.
Méthode des lots, banque d'angles et exemples : `references/lots.md`.

## Entrée

Le JSON de campagne de `/chatgpt-ads-skills` (avec allégations, groupes,
intentions et hints), contrôlé sans bloquant. Un fichier d'import CSV au schéma
d'annonces se lit aussi, mais sans liste d'allégations : chaque chiffre ou
promesse y est alors refusé jusqu'à validation.

## Méthode

1. **Analyser** la campagne et fixer la cible (120 par défaut) :
   ```bash
   python3 scripts/analyser_lot.py analyser campagne.json --cible 120 --md plan.md
   ```
   Corrige d'abord les quasi-doublons et titres partagés signalés.
2. **Écrire le lot** (50 annonces au plus) dans `lot-1.json`
   (`{"ads": [...]}`, même format que la campagne, avec `angle`), en
   suivant le plan : nombre par groupe, structures et facettes absentes,
   mots à éviter. Chaque annonce change **au moins une** chose réelle : la
   situation, la facette, l'angle ou la structure du titre
   (`references/lots.md`).
3. **Ajouter** le lot :
   ```bash
   python3 scripts/analyser_lot.py ajouter campagne.json lot-1.json -o campagne-2.json
   ```
   Les annonces refusées (doublon, quasi-doublon, titre déjà pris, longueur,
   allégation non approuvée, groupe inconnu) sont listées : réécris-les ou
   abandonne-les, sans les forcer.
4. **Recommencer** `analyser` sur `campagne-2.json` jusqu'à la cible.
   Arrête plus tôt si un groupe n'a plus d'angle réel à offrir : dis-le
   plutôt que de remplir.
5. **Noter** l'ensemble :
   ```bash
   python3 scripts/analyser_lot.py noter campagne-final.json --md notes.md
   ```
   Le script note longueur, caractère distinct et sources (1 à 5) et
   propose Conserver, Corriger ou Supprimer. Note toi-même page,
   intention et clarté (1 à 5), puis présente les trois listes. Rien n'est
   supprimé sans l'accord de l'annonceur.
6. **Contrôler et exporter** avec `/chatgpt-ads-skills` :
   `valider` puis `exporter` (fichier d'import CSV au schéma d'annonces).

## Volume et budget

Plus d'annonces ne veut pas dire plus de résultats si le budget ne permet
pas de les départager : `valider` de `/chatgpt-ads-skills` compare le
nombre d'annonces aux clics possibles par jour. Si l'écart est grand,
propose de lancer une partie des annonces (en pause pour les autres) et de
les faire tourner, au choix de l'annonceur.

## Format de sortie

1. Le plan du lot (tableau par groupe) et les corrections préalables.
2. Après chaque lot : acceptées, refusées avec leur raison, total.
3. À la fin : les notes, les listes Conserver, Corriger, Supprimer, puis
   le fichier d'import exporté et la liste « à vérifier ».

## Erreurs et limites

| Situation | Conduite |
|---|---|
| Campagne de départ non validée | la valider d'abord (`/chatgpt-ads-skills`) |
| Allégations trop peu nombreuses | des annonces sans chiffre ni promesse, sur la situation et le bénéfice d'usage ; jamais d'allégation nouvelle |
| Un groupe plafonne (tout est refusé) | il a atteint ses angles réels : le dire, rééquilibrer vers les autres groupes ou ajouter un groupe d'intention nouvelle |
| Fichier CSV au schéma sans JSON | lecture possible, chaque allégation y est refusée faute de liste |
| Plus de 5 000 annonces par compte | limite de la documentation : impossible |
| Conversation trop longue | un lot par message, le JSON fait foi entre deux lots |
