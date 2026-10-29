# Résultats des évaluations : pack Tone of Voice

## Tests automatiques

`python3 evals/tout_tester.py` : **49 tests** au 27 octobre 2026.

- 37 tests des scripts (`evals/tone-of-voice/test_scripts.py`) :
  - `texte.py` : découpage, mesures sans objet laissées vides, tutoiement et
    vouvoiement, négation sans « ne », classes de ponctuation, liens et emails
    ignorés, émojis, marques d'écriture IA, bloc de mesures ;
  - `voix.py` : corpus Assurly, règles justifiées par le corpus seulement,
    alerte texte IA, alerte autre auteur, textes presque identiques, fichier
    unique séparé par `---`, niveaux de confiance, codes de sortie, bloc de
    l'exemple égal à la sortie du script ;
  - `ecart.py` : expressions interdites lues en tête de ligne seulement, texte
    hors voix, texte dans la voix, adresse et réglage de canal, « vous »
    ambigu, phrases trop longues, « cela » contre « ça », fichier sans bloc,
    codes de sortie ;
  - `profil.py` : exemple complet, modèle vide signalé, péremption et
    typographie, section manquante, fichier vide, nom de Skill, anonymisation,
    Skill « ma-voix » et son ZIP (un seul SKILL.md, nom égal au dossier,
    description de 1 024 caractères au plus, `ecart.py` embarqué qui marche).
- 12 tests d'intégrité : frontmatter, taille du SKILL.md, fichiers cités,
  références citées, typographie, scripts (`--help`, bibliothèque standard),
  modèle et exemple alignés, exemples fictifs, cas d'éval, manifeste et
  marketplace, ZIP claude.ai, captures du README.

Un bug trouvé par les tests et corrigé avant publication : `ecart.py`
prenait les citations explicatives de « Ce que je n'écris jamais » pour des
expressions interdites (« on ne vend pas une solution… »). Seule
l'expression en tête de ligne est désormais contrôlée.

## Mesures sur les cas de test

| Cas | Sortie |
|---|---|
| 5 textes de Camille (405 mots) | confiance faible, vouvoiement 5 sur 5, 9 règles justifiées, 1 alerte (corpus court) |
| + 1 texte écrit par IA + 1 lettre administrative | le texte IA signalé (6 familles de marques), la lettre classée « à part » (3 raisons) |
| texte écrit par IA (`assurly-ia.txt`) contre la voix | HORS VOIX, 0/100, 12 écarts dont 8 forts |
| post écrit dans la voix (`test_texte_dans_la_voix`) | DANS LA VOIX, aucun écart |

## Éval à l'aveugle : à faire

Protocole prévu, sur le modèle des autres packs :

- trois configurations sur les mêmes textes et les mêmes réponses
  d'utilisateur : `/tone-of-voice`, `voice-extractor` (brianrwagner, la
  référence la plus proche pour une personne seule) et Claude sans Skill ;
- tâches : créer la voix, réécrire 3 textes génériques, vérifier 2 textes ;
- un juge reçoit les sorties sous des lettres tirées au hasard et note :
  fidélité à la personne (elle choisit à l'aveugle le texte qui lui
  ressemble), précision des traits, respect des faits, utilité du fichier,
  honnêteté sur les limites ;
- textes : ceux d'une vraie personne volontaire, anonymisés, plutôt que
  l'exemple fictif. Les résultats seront publiés ici, défaites comprises.
