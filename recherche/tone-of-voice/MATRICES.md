# `/tone-of-voice` : collecte, dissection et matrice de capacités

Collecte du 27 octobre 2026. Dix dépôts clonés en entier (`git clone --depth 1`),
fichiers de voix lus un par un, scripts lus. Le plan du Skill (trois modes,
parcours en six étapes, deux sorties) a été validé par l'utilisateur avant la
collecte ; la matrice dit ce que la collecte change.

## 1. Sources

| Dépôt | Commit | Licence | Ce qui a été lu |
|---|---|---|---|
| anthropics/knowledge-work-plugins, `partner-built/brand-voice` (Tribe AI) | c75fda0 | MIT (dossier), Apache 2.0 (dépôt) | README, 3 SKILL.md, 6 références, 5 agents |
| anthropics/knowledge-work-plugins, `small-business/shared/voice-profile.md` | c75fda0 | Apache 2.0 | fichier entier, exemple compris |
| athola/claude-night-market, plugin `scribe` (voice-extract, voice-learn, voice-generate, voice-review) | 2943226 | MIT | 4 SKILL.md, 9 modules, liste des tests |
| rhuss/cc-prose (voice-extractor, voice-architect) | 8fc38fc | MIT | voice-extractor (1 342 lignes) : mesures, valeurs aberrantes, cas limites ; plan de voice-architect |
| houtini-ai/voice-analyser-mcp | c088e29 | Apache 2.0 (projet archivé) | README, CHANGELOG, générateur de Skill, 6 analyseurs |
| notque/claude-code-toolkit (voice-calibrator, VOICE-SYSTEM, voice-stylometry.py) | 8d93f3e | MIT | doc du système, calibrateur, script de stylométrie |
| brianrwagner/ai-marketing-claude-code-skills, `voice-extractor` | f36b34f | MIT annoncé dans le README, sans fichier LICENSE | SKILL.md, modèle de guide |
| affaan-m/everything-claude-code, `brand-voice` | 25278e7 | MIT | SKILL.md, schéma du profil |
| rampstackco/claude-skills, `brand-voice` | 9b90db2 | MIT | SKILL.md, cadres, modèle de document |
| arnabbagxd/brand-building-skills, `brand-voice` | 4a0a8b5 | MIT | SKILL.md |
| luongnv89/claude-howto, `brand-voice` | cd3d4eb | MIT | SKILL.md (exemple de tutoriel, peu de matière) |
| Join Médicis, `linkedin-human/references/profil-voix.md` et `detect.py` | 00b02d9 | MIT | existant maison |

Source primaire vérifiée : Kate Moran, « The Four Dimensions of Tone of Voice »,
Nielsen Norman Group, 17 juillet 2016, revu le 16 août 2023 (formel/décontracté,
sérieux/drôle, respectueux/irrévérencieux, factuel/enthousiaste). Spécification
Agent Skills (agentskills.io/specification, lue le 27 octobre 2026) : `name`
64 caractères, minuscules, chiffres et tirets, égal au nom du dossier ;
`description` 1 024 caractères.

## 2. Ce que fait chaque référence, et ses faiblesses

- **Tribe AI / Anthropic (brand-voice).** Entreprise, pas personne. Cherche
  dans Notion, Drive, Gong… Forces : « la voix est constante, le ton varie »,
  tableau « Nous sommes / Nous ne sommes pas », matrice de ton par contexte,
  confiance par section, questions ouvertes toujours accompagnées d'une
  recommandation, archive de l'ancienne version. Faiblesses : lourd (5
  agents, 7 connecteurs), aucun script, aucune mesure, rien sur la personne
  qui écrit seule.
- **Anthropic small-business (voice-profile).** La meilleure idée de la
  collecte : un seul fichier de voix partagé par tous les Skills (« une
  correction ici corrige tout »), des traits exacts (formule d'appel,
  signature, moment où arrive la demande), les « jamais » comme partie la plus
  utile, un vrai texte recopié, un journal des mises à jour qui garde la
  raison. Faiblesse : centré sur l'email, aucune mesure outillée.
- **athola (scribe).** Méthode comparative : on fait écrire à l'IA un texte
  par défaut sur le même sujet, puis on décrit ce que l'auteur fait autrement.
  Échantillons anonymisés, variété plutôt que volume, écrits spontanés plus
  révélateurs, passe de « test de pression » qui rejette les traits valables
  pour la moitié des auteurs, négations, consignes applicables (« fais X
  quand Y ») au lieu d'observations. Apprentissage depuis les retouches de
  l'utilisateur avec seuil de preuve (3 occurrences) et péremption à 30 jours.
  Faiblesses : 4 Skills et des fichiers cachés dans `~/.claude`, chiffres
  d'articles cités sans lien vérifiable, pas de français.
- **cc-prose.** Le plus outillé côté mesures : longueur et écart-type des
  phrases, paragraphes d'une phrase, entropie de la ponctuation, densité de
  précautions. Détection des textes à part (valeur aberrante) et des corpus à
  plusieurs auteurs, confiance selon le volume, champs omis plutôt que zéro
  quand la mesure n'a pas de sens. Faiblesses : mesures calculées « à la main »
  par le modèle dans le SKILL.md (pas de script), 1 342 lignes, anglais.
- **houtini.** Le Skill généré apprend par l'exemple : il contient de vrais
  textes de l'auteur et demande d'en lire trois avant d'écrire ; les règles ne
  sont écrites que si le corpus les justifie (exemple : aucun tiret cadratin
  dans le corpus, donc règle « pas de cadratin »). Faiblesses : projet archivé,
  15 000 mots minimum, statistiques d'économies non vérifiables.
- **notque.** Validation chiffrée d'un brouillon contre le profil : bande
  d'écart-type des phrases (0,5 à 1,5 fois celui du corpus), ponctuation
  classée jamais / rare / habituelle, détecteurs d'antithèse « ce n'est pas X,
  c'est Y », profil qui se périme (90 jours). Faiblesses : la doc appelle
  `voice-analyzer.py` et `voice-validator.py`, absents du dépôt ; exige 50 à
  100 échantillons, hors de portée d'un marketeur.
- **brianrwagner.** Modes rapide / standard / complet, seuil de 500 mots,
  priorité aux écrits spontanés, exclusion des tics de plateforme, zones de
  confiance (sujets où l'auteur tranche, où il parle d'expérience, où il
  explore), test A/B « ça sonne comme toi ? », autocritique. Faiblesse :
  aucun script, emojis dans le modèle.
- **affaan-m (ECC).** Profil court et réutilisable, séparation voix publique
  / voix privée, interdiction de stocker une empreinte de voix dans un dépôt
  versionné sans accord. Faiblesse : défauts propres à son auteur.
- **rampstack.** Quatre couches (attributs, ton par contexte, vocabulaire et
  grammaire, exemples appariés), test de résistance (noter 1 à 5 par
  attribut, et noter un concurrent : s'il obtient la même note, les attributs
  ne distinguent rien), alerte sur la voix « aspirationnelle » qui n'existe
  pas. Faiblesse : marque, pas personne ; 15 paires d'exemples minimum.
- **arnabbagxd.** Version questionnaire pure (axes, marques admirées, ce
  qu'on ne doit jamais entendre). Faiblesse : aucun texte analysé.
- **luongnv89.** Exemple pédagogique figé. Rien à reprendre.
- **Join Médicis, profil-voix.** Déjà : 3 à 6 textes collés, mesures via
  `detect.py`, tics à garder, rien d'inventé. Manque : questions, calibrage,
  canaux, sortie autonome, mise à jour, vérification d'un texte.

## 3. Matrice de capacités

Verdict : **reprendre**, **améliorer** (repris et changé) ou **écarter**.

| # | Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|---|
| 1 | Trois entrées combinables : ses textes, un style à émuler, rien (questions) | plan validé ; arnabbagxd (questions seules) | reprendre | parcours unique, l'utilisateur ne choisit pas de « mode » |
| 2 | Volume minimal : 3 textes, 500 mots ; en dessous, plus de questions | athola, brianrwagner, cc-prose | améliorer | pas de blocage : on continue avec plus de questions et une confiance « faible » affichée |
| 3 | Priorité aux écrits spontanés (messages, emails) sur les textes polis | brianrwagner, athola | reprendre | liste française : WhatsApp, emails, posts, pages du site, en dernier |
| 4 | Variété de sujets plutôt que volume | athola | reprendre | `voix.py` signale des textes trop semblables |
| 5 | Repérage des textes écrits par IA | maison (`detect.py`) | améliorer | marqueurs embarqués dans `voix.py` (sans dépendre du pack LinkedIn) |
| 6 | Repérage des textes à part et du mélange d'auteurs | cc-prose | améliorer | règle simple sur 5 mesures, explication en clair, l'utilisateur tranche |
| 7 | Exclusion des tics de plateforme (sauts de ligne LinkedIn, hashtags) | brianrwagner | reprendre | réglage par canal plutôt qu'exclusion |
| 8 | Mesures chiffrées par script | cc-prose, notque, houtini | améliorer | `voix.py`, Python sans dépendance, mesures françaises (tu/vous, « ça »/« cela », négation sans « ne », anglicismes, espaces typographiques) |
| 9 | Champ omis plutôt que zéro quand la mesure n'a pas de sens | cc-prose | reprendre | dans `voix.py` et le bloc de mesures |
| 10 | Confiance selon le volume | cc-prose, Tribe AI | améliorer | 3 niveaux sur le nombre de mots, affichés dans le fichier |
| 11 | Ponctuation classée jamais / rare / habituelle | notque | reprendre | sert aussi de règle (« jamais » seulement si le corpus le montre, idée houtini) |
| 12 | Comparaison avec ce que l'IA écrirait par défaut | athola | reprendre | étape d'analyse : 1 texte « par défaut » sur le sujet d'un échantillon, différences listées |
| 13 | Test de spécificité (« valable pour la moitié des auteurs ? alors trop vague ») | athola, rampstack | reprendre | liste de formules vagues refusées, en français |
| 14 | Consignes applicables plutôt qu'observations | athola | reprendre | chaque trait = une consigne + un exemple tiré des textes |
| 15 | Les « jamais » comme partie la plus utile | Anthropic SMB, athola | reprendre | section dédiée, chaque entrée justifiée (absente des textes ou demandée) |
| 16 | « Nous sommes X, pas Y » | Tribe AI, rampstack | reprendre | 3 à 5 traits, pour une personne (« je suis ») ou une marque |
| 17 | Quatre curseurs NN/g | rampstack, arnabbagxd ; source NN/g 2016 | reprendre | notés 1 à 5, avec la mesure qui justifie la note quand elle existe |
| 18 | Archétypes de Jung | rampstack | écarter | peu utile pour une personne, risque de voix « aspirationnelle » |
| 19 | Voix constante, ton par canal | Tribe AI, rampstack, arnabbagxd | reprendre | canaux du marketeur français : LinkedIn, email, site, WhatsApp, newsletter |
| 20 | Traits exacts : formule d'appel, signature, moment de la demande | Anthropic SMB | reprendre | dans « Réglages par canal » |
| 21 | Zones de confiance (où l'auteur tranche, où il explore) | brianrwagner | reprendre | section courte, sujets nommés |
| 22 | Questions ciblées seulement sur ce que les textes ne disent pas | plan validé | reprendre | banque de 12 questions à choix, 7 posées au plus |
| 23 | Questions ouvertes avec recommandation | Tribe AI | reprendre | toute incertitude finit en question fermée avec une proposition |
| 24 | Calibrage par variantes | plan validé ; brianrwagner (A/B) ; notque (A/B) | améliorer | 3 variantes sur un même message, retours « plus direct » traduits en réglage |
| 25 | Validation « ça sonne comme toi ? » en fin de parcours | brianrwagner, athola | reprendre | un texte dans la voix + le même hors voix, pour voir l'écart |
| 26 | Test de résistance contre un concurrent | rampstack | améliorer | facultatif : si un texte d'une autre personne passe aussi bien, les traits sont trop vagues |
| 27 | Fichier de voix unique partagé par tous les Skills | Anthropic SMB | reprendre | `tone-of-voice.md` lu par les packs LinkedIn, SEO et Fondation |
| 28 | Vrais textes dans le livrable, « lis-en trois avant d'écrire » | houtini, notque (« les échantillons sont le Skill ») | reprendre | le Skill « ma-voix » embarque 3 à 6 extraits |
| 29 | Règles seulement si le corpus les justifie | houtini | reprendre | `voix.py` propose les règles de ponctuation à partir des classes |
| 30 | Génération d'un Skill de voix | houtini, notque | améliorer | `profil.py ma-voix` : dossier et ZIP valides (nom, description, un seul SKILL.md), importable sur claude.ai, ChatGPT, Gemini |
| 31 | Vérifier un texte contre le profil, en chiffres | notque | améliorer | `ecart.py` : écarts listés avec leur gravité ; le jugement reste à part |
| 32 | Détecteurs d'antithèse et d'ouvertures creuses | notque | reprendre | en français (« ce n'est pas X, c'est Y », « Dans un monde où ») |
| 33 | Apprendre des retouches de l'utilisateur | athola | améliorer | sans fichiers cachés : la personne colle sa version retouchée, on propose la règle, elle dit oui ; une retouche explicite (« jamais ce mot ») s'applique tout de suite |
| 34 | Seuil de preuve et péremption des motifs | athola | écarter | trop lourd pour l'usage visé ; remplacé par le journal et la question « on garde ? » |
| 35 | Profil qui se périme | notque (90 jours) | améliorer | date de mise à jour ; `profil.py verifier` signale un profil de plus de 6 mois |
| 36 | Journal des mises à jour avec la raison | Anthropic SMB, Tribe AI (archive) | reprendre | section « Journal », version incrémentée |
| 37 | Anonymiser les échantillons, retirer les données de tiers | athola, Tribe AI | reprendre | noms de clients et coordonnées retirés des extraits embarqués (RGPD) |
| 38 | Pas d'empreinte de voix dans un dépôt public | affaan-m | reprendre | rappel dans la sortie |
| 39 | Voix publique et voix privée | affaan-m | améliorer | devient « réglages par canal » |
| 40 | Recherche dans Notion, Drive, Gong | Tribe AI | écarter | v1 : textes collés ou fichiers ; un connecteur peut fournir les textes, sans recherche automatique |
| 41 | 15 paires d'exemples minimum | rampstack | écarter | trop long ; 2 à 3 avant / après suffisent pour une personne |
| 42 | 50 à 100 échantillons | notque | écarter | hors de portée ; la confiance affichée dit ce que vaut le profil |
| 43 | Émuler le style d'une personne réelle | plan validé | améliorer | on reprend des traits, pas les tournures signatures ; pas d'écriture « au nom de » quelqu'un d'autre |

## 4. Comparaison avec l'existant Join Médicis

`profil-voix.md` (pack LinkedIn) couvre les lignes 2, 5, 8 (en partie), 15 et
27 (pour LinkedIn seulement). Il lui manque : questions, calibrage, réglages
par canal, comparaison avec l'IA par défaut, test de spécificité, livrable
autonome, vérification chiffrée d'un texte, mise à jour. Décision : le pack
LinkedIn lit `tone-of-voice.md` s'il existe ; `/tone-of-voice` remplace le
`/fondation-voix` prévu (même rôle, un seul outil).

## 5. Ce que le Skill fera (rappel du plan validé, mis à jour)

1. **Créer** : textes (les siens, un style à émuler, ou rien) → mesures
   (`voix.py`) → comparaison avec l'IA par défaut → 3 à 5 traits « X, pas Y »
   → 5 à 7 questions ciblées → calibrage par 3 variantes → test « ça sonne
   comme toi ? » → `tone-of-voice.md`, et sur demande le Skill « ma-voix ».
2. **Appliquer** : réécrire un texte dans la voix, ou vérifier qu'il y est
   (`ecart.py` pour les chiffres, jugement à part).
3. **Mettre à jour** : retours, nouveaux textes ou version retouchée → règle
   proposée → nouvelle version et ligne de journal.
