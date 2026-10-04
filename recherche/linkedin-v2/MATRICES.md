# LinkedIn Skills v2 : matrices de capacités

État : **à valider par Aleksander** avant toute rédaction (étape 5 du processus,
voir `CLAUDE.md`). Rédigé le 2 octobre 2026.

## Sources analysées en entier

| Code | Source | Taille | Licence |
|---|---|---|---|
| J | Jake Schincariol, linkedin-agent-skill (base de la v1) | 22 fichiers | MIT |
| JD | JoshuaDIWork, Linkedin_SKILL (Jake adapté à une entreprise) | 26 fichiers | MIT |
| S | Serge Bulaev, linkedin-skills (12 Skills, 131 commits) | 104 fichiers uniques | MIT |
| A | alirezarezvani, claude-skills/marketing/linkedin (17 scripts) | 64 fichiers | MIT |
| T | Taplio, taplio-linkedin-claude-skills (26 Skills, liés à l'outil) | 30 fichiers | MIT |
| M | Marian Kamenistak, linkedin-post-writing-skill | 9 fichiers | MIT |
| B | Boileau (humaniseur français) | 4 fichiers | MIT |
| H | blader/humanizer v3.1 (CHANGELOG compris) | 14 fichiers | MIT |
| W | Wikipédia EN « Signs of AI writing » et FR « Identifier l'usage d'une IA générative » (texte source complet) | 230 Ko | CC BY-SA |
| C | Corey Haines, marketingskills (social, copywriting, relecture, prospection, contexte produit) | 12 Skills lus | MIT |
| AN | Anthropic, skill-creator (méthode officielle d'écriture et d'évaluation) | 15 fichiers | Apache 2.0 |
| V1 | Notre pack LinkedIn actuel | 12 Skills | MIT |

Notes détaillées par source : `notes/01` à `notes/09`.

Verdicts : ✅ reprendre · ⬆ reprendre en améliorant · ✖ écarter (avec la raison).

---

## Ce que les sources nous apprennent (les 10 leçons)

1. **Les meilleurs packs notent la solidité de chaque affirmation** (A : officiel / étude
   / folklore ; S : vendeur / foule / consensus / plateforme). Les chiffres « LinkedIn »
   viennent presque tous d'outils qui vendent du LinkedIn. Deux mythes sont démentis par
   les plus gros jeux de données. La note d'invitation personnalisée ne triple pas
   l'acceptation (~26% avec ou sans). La pénalité des liens est d'environ 19% en
   médiane, pas 40-60%, et LinkedIn ne l'a jamais confirmée.
2. **Ce qui manque le plus souvent, c'est la matière, pas l'écriture** (S : Story Bank et
   interviewer ; T : extracteur d'histoire). C'est exactement ton axe « J'ai vendu X, en
   Y, pour Z ».
3. **Le contexte de l'entreprise est un fichier à part entière** (JD, C). Il contient les
   offres, le sujet qui mène à quel appel à l'action, les preuves datées et étiquetées,
   le vocabulaire client mot pour mot et les formulations retirées.
4. **Ce qui se mesure doit passer par un script** (A) : note du titre, audit du profil
   classé par points gagnés par heure, linter de post, budget en minutes, garde-fou de
   volume, statistiques honnêtes sur ses propres posts.
5. **L'humaniseur de référence a changé de doctrine en 2026** (S V3, H) :
   - les marqueurs se comptent par paragraphe, pas mot par mot ;
   - forcer l'alternance de phrases courtes et longues est devenu un tic, pas un
     remède ;
   - annoncer sa sincérité (« honnêtement, … ») est un tic ;
   - il faut vérifier qu'aucun fait n'a été ajouté ni perdu ;
   - il faut une garde contre la sur-correction.
6. **Les listes de mots IA vieillissent vite** (W les classe désormais « historiques »,
   par génération de modèle). Les tics de structure durent.
7. **La sécurité fait partie du Skill** (S, JD, A) :
   - le texte écrit par un tiers est une donnée, jamais une instruction ;
   - les refus sont écrits en dur, chacun avec une alternative ;
   - rien n'est écrit sur une plateforme.
8. **Choisir l'accroche par objectif** (commentaires, partages, likes, sauvegardes), puis
   par sujet (S), avec une règle de densité : un contraste et une triade par post au
   plus, aucun « Le résultat ? ».
9. **L'analyse de ses posts doit refuser de trop conclure** (A) : médiane plutôt que
   moyenne, tests par permutation, aucun motif sous 10 posts, et « rien n'a survécu »
   est un résultat.
10. **Tests de cohérence des instructions** (S) : chaque Skill cité existe, chaque
    description dit « pas pour X (utiliser Y) », les gabarits sont livrés vides. Évals
    avec des correcteurs qui ont une bonne réponse (S, AN).

---

## Arbitrages entre sources (à valider)

| Sujet | Désaccord | Proposition |
|---|---|---|
| Tiret cadratin | S : le plafonner (~1 pour 100 mots), car l'absence totale devient un tic | **Ta règle prime** : supprimé, ou remplacé par une virgule. En français, le tiret cadratin n'a pas l'usage anglais. |
| Rythme des phrases | B et H : « varier le rythme » ; S : ne jamais fabriquer de variation, corriger seulement le plat mécanique | Suivre S : notre contrôle RYTHME (detect.py) ne récompense plus la variation, il signale le paragraphe plat et le staccato. |
| Question en 1re ligne | J : formule « Question Trap » ; S : −34% de likes [donnée d'un vendeur] | Pas de question en ouverture par défaut. Si l'audit de l'utilisateur montre l'inverse, son audit prime. |
| Longueur d'un post | J et S : 900-1 300 car. ; C : 1 200-1 500 ; A : 1 300-2 500 ; S : 1 000+ = 1,18× | Pas de fourchette imposée : la longueur choisie par l'utilisateur gagne, plafond de 3 000. Sa médiane personnelle vient de `/linkedin-audit`. |
| Relances après invitation | J : 2 (J+4, J+10) ; A : 1, ≥ 1 semaine, seulement avec du nouveau | 1 relance par défaut, une 2e seulement avec du nouveau, jamais « je me permets de relancer ». |
| Note d'invitation | T : 300 car. ; J et A : 200 | 200 en compte gratuit, 300 en Premium ; nombre de notes personnalisées limité par mois en gratuit [à vérifier au moment d'écrire]. |
| Lien dans le post | S : −40 à −60% ; A : ~19% en médiane, non confirmé | Lien en premier commentaire par défaut, présenté comme une précaution [étude tierce], pas comme une règle. |
| Hashtags | J : 3 max ; JD : 3-5 ; S : 0-2 | 0 à 3, en fin de post. |
| « Comment X pour recevoir Y », commentaires de « seeding » sous son propre post, pods | T et S les proposent en partie | ✖ Écartés : les règles de LinkedIn interdisent d'« augmenter artificiellement l'engagement » [officiel]. |
| Publication automatique, lecture de LinkedIn par Apify, Taplio ou navigateur | S et T | ✖ Écartées : contraire aux conditions d'utilisation (§8.2) et à ta règle « rien n'est publié ». |

---

## Les Skills prévus (v2)

13 Skills au lieu de 12 : 9 approfondis, 2 fusionnés ou recentrés, 3 nouveaux.

| Skill | Statut | Ce qu'il fait de plus que la v1 |
|---|---|---|
| `/linkedin-strategie` | **nouveau** | Positionnement (questions qui forcent, anti-positionnement), piliers, objectif à 90 jours, budget en minutes, newsletter oui ou non. Écrit le fichier contexte. |
| `/linkedin-interview` | **nouveau** | Banque d'histoires : réussites chiffrées, tournants, cicatrices, positions. Alimente le profil et les posts. |
| `/linkedin-profile` | approfondi | Objectif (clients, emploi, autorité), 3 lecteurs, 3 scripts (titre, audit par points/heure, section Infos), demande de recommandation, chiffres via l'interview. |
| `/linkedin-entreprise` | **nouveau** | Page entreprise notée sur 100 (n/a si la donnée manque) et programme d'ambassadeurs salariés (lancement 14 jours, ce qu'on relit et ce qu'on ne relit pas, ROI). |
| `/linkedin-post` | approfondi | Objectif d'abord, formules fusionnées (J + S, dédoublonnées, avec piège et niveau de preuve), règle de densité, choix du format, linter, reçu enrichi, appel à l'action choisi par sujet, analyse d'un post qui a marché. |
| `/linkedin-carrousel` | approfondi | 5 structures (C), règles d'accessibilité, script qui construit le PDF à partir des textes validés. |
| `/linkedin-human` | refondu | 4 passes (S V3), 3 niveaux, 38 marqueurs français (B), densité par paragraphe, vérification de fidélité des faits (H), garde anti-sur-correction, listes de mots datées. |
| `/linkedin-comment` | approfondi | Choisir quels posts commenter (grille de priorité), 9 types + modèles, structure en 4 temps, contrôle « un angle que le post n'a pas ». |
| `/linkedin-reply` | approfondi | Tri, rapport de filtrage chiffré, repérage des leads chauds dans les commentaires (note /10), passage au message privé. |
| `/linkedin-dm` | approfondi | Ligne spécifique à la personne vérifiée par script, garde-fou de volume, ordre qui marche (commenter avant d'inviter), cadre CNIL et RGPD vérifié. |
| `/linkedin-inbox` | approfondi | 6 catégories, détection de séquence automatisée, leads notés pour le CRM. |
| `/linkedin-plan` | recentré | La semaine seulement (la stratégie part dans `/linkedin-strategie`) : équilibre des objectifs, routine de 15 min par jour, boucle avec l'audit. |
| `/linkedin-audit` | approfondi | Script statistique : médiane, bandes, motifs testés par permutation, plan d'expérience, page et profil séparés. |
| `/linkedin-repurpose` | approfondi | Registre de réutilisation (script), règles par source. |
| `/linkedin-job` | approfondi | Requêtes booléennes et URL de la dernière heure (déjà là), profil en mode « emploi », message au recruteur, suivi des candidatures. |

Fichiers communs, lus par tous les Skills :

- `contexte.md` : la personne (voix) et l'entreprise (offres, sujet → appel à l'action,
  preuves datées et étiquetées, vocabulaire client, hors-limites, formulations retirées) ;
- `reserve.md` : la banque d'histoires ;
- `journal.md` et `apprentissages.md` : existent déjà ;
- `references/preuves.md` : chaque affirmation sur LinkedIn avec son niveau de preuve et
  sa date.

---

## Matrices par Skill

### `/linkedin-strategie` (nouveau)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| 5 questions qui forcent, une à la fois, avec réponse recommandée ; relancer une fois puis noter la réponse faible | A | ✅ | Exemples français et Assurly |
| Objectif à 90 jours vérifiable par un tiers, pas un nombre d'abonnés | A | ✅ | |
| Niche : 7 questions, reformulation, anti-positionnement, « J'aide X à Y grâce à Z » + 3 variantes | T | ✅ | Filtre pour chaque post, repris par `/linkedin-post` |
| Piliers en pourcentage, mix par persona (dirigeant, commercial, marketing, fondateur, freelance) | S, C, M | ⬆ | Persona « freelance » et « marketeur en interne » |
| Funnel notoriété / éducation / conversion (conversion ≤ 1 post sur 5) | M | ✅ | |
| Budget en minutes mesuré sur une mauvaise semaine ; sous 90 min, semaine « commentaires seulement » | A | ✅ | Script `budget.py` (refait en français) |
| Étape selon l'audience (0-1 000 : commenter avant de publier) | S, A | ✅ | [étude tierce] |
| Newsletter : éligibilité (plus de 150 abonnés, critère officiel), soutenabilité sur 6 mois, règle d'arrêt écrite avant le n°1 | A | ✅ | |
| Angles « fondateur » (10) | S | ⬆ | Gardés en `references/`, plus des angles freelance et salarié |
| Écrit `contexte.md` (personne et entreprise) | JD, C | ⬆ | Faits étiquetés LIVE / À CONFIRMER / RETIRÉ, datés |
| Garde-fou de politique (automatisation, pods, messages en masse, preuve inventée) avec alternative | A | ⬆ | Script commun `garde_fou.py`, utilisé par tous les Skills |

### `/linkedin-interview` (nouveau)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Banque d'histoires en 9 sections : parcours daté, réussites chiffrées avec référent, réalisations, tournants, cicatrices, positions qui coûtent, histoires déjà racontées, noms citables / à demander / interdits, hors-limites | S | ✅ | Format « J'ai vendu X, en Y, pour Z » en sortie directe vers le profil |
| Une question à la fois ; relancer une fois chaque réponse molle (« de combien, mesuré comment, quel mois ? ») | S | ✅ | |
| Questions qui marchent et questions qui gâchent la séance | S | ✅ | Traduites et adaptées |
| Mode post : la scène, le chiffre, la date, l'erreur, qui n'est pas d'accord, quoi faire, ossature relue en 5 lignes | S | ✅ | |
| Arc : situation, tension, tournant, résultat, leçon (« pas d'histoire sans tension ») | T | ✅ | |
| Questions par poste pour faire sortir les chiffres (volume, temps, argent, avant/après, classement, périmètre ; ordre de grandeur si confidentiel) | V1 | ✅ | Déjà dans notre profil, déplacé ici et partagé |
| Avertissement : le fichier contient des données personnelles, ne pas le pousser dans un dépôt public | S | ✅ | Rappel RGPD sur les tiers cités |

### `/linkedin-profile` (approfondi)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Objectif d'abord (clients / emploi / autorité), qui change la Sélection et l'appel à l'action | S | ✅ | |
| 3 lecteurs : celui qui survole (3 s), celui qui évalue (40 s), celui qui décide | A | ✅ | |
| Grille sur 100 (12-14 critères) | J, A, V1 | ⬆ | Fusion de nos critères et de ceux d'A, avec « Open To / Services » |
| Note du titre sur 5 dimensions, plafond de 220 car., 60 premiers caractères (aperçu dans la recherche et les invitations) | A | ✅ | Script `titre.py` en français |
| Audit du profil classé par **points gagnés par heure** + plan de la première heure | A | ✅ | Script `audit_profil.py` |
| Section Infos : pli à ~265 car., refuse un pli coupé en pleine phrase, structure en 7 temps | S, A | ✅ | Script `infos.py` |
| Expériences « verbe + chiffre » avec tableau avant/après, verbes forts et faibles | S, V1 | ✅ | Chiffres tirés de `reserve.md` |
| Sélection : 3 éléments selon l'objectif, vignettes 1200×627 | S | ✅ | |
| Bannière 1584×396 (texte dans les 2/3 droits, test mobile), photo 400×400 | S | ✅ | [à vérifier] sur l'aide LinkedIn |
| Modèle de demande de recommandation précise (proposer de rédiger, écrire la sienne d'abord) | S | ✅ | |
| URL personnalisée, compétences (3 épinglées, miroir des offres visées) | S | ✅ | |
| Re-noter à la fin, honnêtement, et dire ce qu'une réécriture ne crée pas | J | ✅ | |
| Ne jamais noter une section non montrée ; demander un copier-coller, pas une URL | S | ✅ | |
| Chiffres annoncés par S (3,9× plus de vues, 71% d'entretiens…) | S | ✖ | Données d'un vendeur, non vérifiables |

### `/linkedin-entreprise` (nouveau)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Page notée sur 100, 12 critères, chacun avec sa source ; critère sans source = n/a, score « sur les points notables » | JD | ✅ | Généralisé (JD est propre à une entreprise) |
| Deux voix : dirigeant « je » et page « nous », jamais mélangées | JD | ✅ | |
| Coordination page / dirigeant : jamais le même jour, la page repartage le meilleur post 2 jours après | JD | ✅ | |
| Programme d'ambassadeurs : lancement en 14 jours, ce que le marketing relit (faits, confidentialité, conformité) et ne relit pas (voix, style), délai de relecture < 4 h, 5 min par post | S | ✅ | |
| ROI en 3 niveaux (personne, équipe, business) et anti-modèles (même post copié sur plusieurs comptes) | S | ✅ | |
| Alignement de l'équipe (titres des salariés qui reprennent les formulations maison) | JD | ✅ | |
| Convention UTM (organique / payant) | JD | ✅ | |

### `/linkedin-post` (approfondi)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Lire `contexte.md`, `reserve.md`, `journal.md` ; idée mince → une question groupée | J, S | ✅ | |
| Choisir l'objectif d'abord (commentaires, partages, likes, sauvegardes), puis la formule | S | ✅ | |
| Formules d'accroche avec squelette complet, « pourquoi », **piège**, niveau de preuve et note 2026 | J (21), S (20) | ⬆ | Fusion dédoublonnée, environ 25 formules en français, exemples Assurly |
| Formules structurelles (A/B contrôlé, faux dilemme, anecdote + preuves, courbes divergentes) | S | ✅ | |
| Règle de densité : un contraste, une triade, aucun « Le résultat ? », aucune question avant la fin | S | ✅ | Vérifiée par le linter |
| Micro-règles : chiffre d'abord, « Comment j'ai » plutôt que « Comment », échec daté dans les 3 premières lignes | S | ⬆ | Présentées avec leur niveau de preuve |
| Choix du format : texte, carrousel, sondage (seulement s'il y a une vraie décision derrière), vidéo (seulement avec caméra ou images), article, newsletter | A | ✅ | Script `format.py` |
| Linter : 3 000 car., pli à 140 car. avec phrase complète, **pseudo-gras Unicode bloquant** (accessibilité), hashtags, liens, appâts, densité | A | ✅ | Script `lint_post.py`, règles françaises |
| Reçu : formule, objectif, longueur, score de l'humaniseur, **texte du premier commentaire**, visuel utile ou non, **potentiel de sauvegarde** | J, M | ✅ | |
| Un seul appel à l'action, une phrase, choisi par sujet dans `contexte.md` | JD | ✅ | |
| Nommer ses méthodes (« la méthode des 3 questions ») quand il y a un processus répétable | M | ✅ | |
| Partir d'un post qui a marché (5 à 10× la moyenne de son auteur) : classer la formule, structure, modèle vierge, ce qui serait pénalisé aujourd'hui | S, M | ✅ | Mode « analyser » |
| Séries numérotées (« Histoire de client n°12 ») | M | ✅ | |
| Pas de lien dans le corps, 0 à 3 hashtags, aucune invention | J | ✅ | Niveaux de preuve affichés |
| « Commente X pour recevoir Y », pods, seeding | T, S | ✖ | Règles officielles de LinkedIn |
| Publication via Publora | S | ✖ | « Rien n'est publié » |

### `/linkedin-carrousel` (approfondi)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Quand en faire un (idée avec une suite d'étapes) ; sinon renvoyer vers `/linkedin-post` | J | ✅ | |
| 5 structures : liste de valeur (nombre exact promis), problème-preuve (boucle ouverte puis fermée par la preuve), liste de techniques nommées, coup de gueule avec pivot d'équité, démo (vue d'ensemble avant le détail) | C | ✅ | Exemples français |
| Slide 1 = vignette autonome, un seul gabarit visuel, police ≥ 28 pt, un seul appel à l'action, numérotation, signature sur chaque slide | C, J | ✅ | |
| PDF avec texte sélectionnable (accessibilité), 1080×1350 | A, J | ⬆ | Script `carrousel.py` : textes validés → HTML → PDF (Chromium si disponible, sinon impression depuis le navigateur) ; gabarit v1 repris |
| Mesurer sauvegardes et taux de complétion, pas les likes | C | ✅ | Repris dans `/linkedin-audit` |

### `/linkedin-human` (refondu)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Caractères invisibles, texte caché, typographie française, tes règles (« 15% », tiret cadratin supprimé ou virgule) | V1, J | ✅ | Garde la v1 |
| 4 passes : nettoyer → rythme (corriger le plat, ne jamais fabriquer de variation) → ajouter (chiffre avec référent, entité nommée, fait daté énoncé à plat ; jamais d'annonce de sincérité ni de précaution inventée) → contrôle anti-sur-correction | S V3 | ✅ | Adaptées au français |
| 3 niveaux : forensique (fuites de modèle), strict (par défaut), esthétique (sur demande) | S | ✅ | |
| Densité par paragraphe (3+ marqueurs = réécrire le paragraphe ; jamais un synonyme de la même liste) | S | ✅ | Nouvelle logique dans `detect.py` |
| 38 marqueurs français en 7 familles, avec avant/après | B | ⬆ | Fusion avec notre `tics-ia.json` ; on comble ce qui manque (faux registre familier, fausses gammes, variation élégante…) |
| Une seule explication (le choix par défaut contre le choix pour un lecteur) ; marqueurs forts (1 occurrence suffit) ou faibles (il en faut plusieurs) | H | ✅ | Poids par marqueur |
| **Vérification de fidélité** : aucun chiffre, nom, date ou citation ajouté ou perdu entre avant et après | H | ✅ | Script : comparaison automatique |
| « Mauvais lecteur » : une réponse qui ré-explique ce que l'autre sait déjà → commencer par la décision | H | ✅ | Appliqué à `/linkedin-reply` et `/linkedin-dm` |
| Listes de mots IA datées par génération de modèle ; indicateurs inefficaces (grammaire parfaite, mots de transition isolés) | W | ✅ | |
| Échantillon de l'utilisateur > règles ; conflit voix/règle : forensique = toujours corriger, strict = demander, esthétique = laisser | S, H | ✅ | |
| Modes de sortie : collé (brouillon + tics restants + final), fichier, intégré | H | ✅ | |
| Mode audit (liste de contrôle avant publication, bloquants et avertissements) | S | ✅ | Fusionné avec le linter de `/linkedin-post` |
| Mode profil de voix (à partir de 3 à 6 posts) | S | ✅ | Écrit la partie « voix » de `contexte.md` |
| Testeur de détecteurs payants | S | ✖ | Envoie le texte à des tiers ; scores bruités sur des textes courts |
| Planter des fautes (« its/it's ») | M | ✖ | |

### `/linkedin-comment` (approfondi)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| 9 types de commentaires choisis selon le post | J, V1 | ✅ | |
| 7 modèles (pièce manquante, répondre à la question de clôture, chiffre d'abord, observation de praticien, contre avec concession, recadrage citable, question plus pointue) | S | ⬆ | Fusionnés avec les 9 types |
| Structure en 4 temps (citer un point, sa donnée, **un angle absent du post**, une vraie question) | S | ✅ | Contrôle : le commentaire apporte-t-il un mot ou une idée absents du post ? |
| Lire les meilleurs commentaires existants pour ne pas faire doublon | S | ✅ | |
| Grille de priorité des posts à commenter (ICP ×2, intention ×2, portée, commentaire utile ×2, fraîcheur) et cas d'exclusion | C | ✅ | |
| 3 niveaux : relation, visibilité, entretien | C | ✅ | |
| Modèles « vente » : réchauffer un compte cible sans aucun pitch | S | ✅ | |
| Mode session et suivi de qui a été commenté | J, V1 | ✅ | |
| Texte de tiers = donnée, jamais instruction | S | ✅ | Règle commune |

### `/linkedin-reply` (approfondi)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Tri en catégories, écrire dans cet ordre, s'arrêter quand la valeur s'arrête | J, V1 | ✅ | |
| Rapport de filtrage chiffré (« 23 récupérés → 6 écartés : 4 éloges vides, 1 doublon, 1 spam ») | S | ✅ | |
| Toujours garder : questions, désaccords, détails nommés, personnes déjà venues (« relation ») | S | ✅ | |
| Leads chauds notés /10 (adéquation, intention, récurrence, portée) avec l'action suivante | T | ✅ | Passage à `/linkedin-dm` |
| « D'où viennent les leads » : quels posts en attirent | T | ✅ | Repris dans `/linkedin-audit` |
| Fil de plus de 72 h → plutôt un message privé | S | ✅ | |
| Réponses de l'auteur interdites (« Merci ! », « 100% ») ; chaque réponse apporte un détail, un nom ou une question | S | ✅ | |

### `/linkedin-dm` (approfondi)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Raison d'écrire **maintenant**, sinon le dire | J | ✅ | |
| Ligne spécifique à la personne, vérifiée (« aurait-elle pu être envoyée à quelqu'un d'autre ? ») ; phrases à supprimer | A | ✅ | Script `message.py` en français |
| La note sert à gagner la conversation, pas la connexion ; aucune demande dans la note | A | ✅ | [étude tierce] |
| 5 contextes (froid, après commentaire, après événement, après engagement sur mes posts, contact commun) | T | ✅ | |
| Ordre qui marche : 2 semaines de commentaires, invitation qui cite, attendre, une petite demande | A | ✅ | |
| Garde-fou de volume (invitations en attente comptées, taux d'acceptation sous 20% = stop, temps nécessaire) | A | ✅ | Script `volume.py` |
| « Pick your brain » → une question précise répondable en 2 phrases | A | ✅ | |
| Cadre CNIL et RGPD de la prospection B2B (intérêt légitime, opposition simple, information si stockage en CRM) | V1, C | ⬆ | À vérifier aux sources CNIL au moment d'écrire |

### `/linkedin-inbox` (approfondi)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Comptes par catégorie d'abord ; détection de séquence automatisée avec l'indice qui la trahit | J, V1 | ✅ | |
| Catégories adaptées au métier (partenaire, candidat) | JD | ✅ | Catégories configurables dans `contexte.md` |
| Leads à reporter dans le CRM le jour même | JD | ✅ | Format prêt à coller (HubSpot, Pipedrive, tableur) |

### `/linkedin-plan` (recentré)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Ne demander que ce qui change chaque semaine (« qu'est-ce qui s'est passé ? ») | JD | ✅ | |
| Équilibre des objectifs dans la semaine, aucune formule répétée en 7 jours, aucun pilier au-delà de 60% | S | ✅ | |
| Ne pas reprogrammer une formule qui a échoué dans l'audit | JD | ✅ | |
| Liste de 10 personnes à suivre (5 portée, 3 pairs, 2 acheteurs) ; 70% pairs, 20% aspirationnels, 10% prospects | J, S | ⬆ | |
| Routine quotidienne de 15 min (répondre sous ses posts, puis 5 commentaires) | T | ✅ | |
| Créneau de réponse bloqué après publication ; visuel à demander en début de semaine | JD, A | ✅ | |
| Export du plan pour Notion ou un tableur | S | ✅ | |
| « Giants strategy » (commenter avant la publication) | S | ✖ | Incohérent |

### `/linkedin-audit` (approfondi)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Lire l'export LinkedIn de l'utilisateur, sans rien aller chercher sur LinkedIn | A, J | ✅ | Chemin d'export en français |
| Médiane et MAD, bandes (exceptionnel, fort, typique, faible), définition explicite du taux d'engagement | A | ✅ | Script `audit.py` |
| Motifs testés : effectif ≥ 5 par groupe, effet ≥ 15%, permutation, comparaisons multiples ; refus sous 10 posts ; « rien n'a survécu » est un résultat | A | ✅ | |
| Plan d'expérience (hypothèse, nombre de posts, semaines, critère d'échec écrit avant, alterner les variantes) | A | ✅ | |
| Facteurs : formule, format, longueur, thème, appel à l'action, réponses sous 2 h ; jour et heure en dernier | J, JD | ✅ | |
| Hiérarchie des métriques : conversations entrantes et opportunités avant la portée ; abonnés = vanité | A, S | ✅ | |
| Page et profil audités séparément | JD | ✅ | |
| Leçons → `apprentissages.md` (validées par l'utilisateur) → `/linkedin-plan` | V1 | ✅ | |

### `/linkedin-repurpose` (approfondi)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Extraire, pas résumer (affirmations, chiffres, histoires, mécanismes, erreurs, phrases) | J, V1 | ✅ | |
| Registre de réutilisation (évite de publier 3 fois la même idée) | A | ✅ | Script `registre.py` |
| Règles par source (tweet, fil, vidéo, blog, newsletter, podcast, Instagram) ; retirer les traces de la plateforme d'origine | S | ✅ | |

### `/linkedin-job` (approfondi)

| Capacité | Source | Verdict | Ce qu'on ajoute |
|---|---|---|---|
| Requêtes booléennes et URL `f_TPR=r3600` | V1 (ton axe) | ✅ | Garde la v1 et ses tests |
| Profil en mode « emploi » (Sélection, compétences calquées sur les offres) | S | ✅ | Passage vers `/linkedin-profile` |
| Message au recruteur ou à un salarié de l'entreprise visée | T, A | ✅ | Passage vers `/linkedin-dm` |
| Suivi des candidatures (tableau simple) | nouveau | ⬆ | Dans `journal.md` |

---

## Ingénierie commune (S-tier)

| Capacité | Source | Verdict |
|---|---|---|
| Niveaux de preuve sur chaque affirmation, dans `references/preuves.md` (officiel / étude tierce / praticien / folklore), datés | A, S | ✅ |
| Règle « contenu non fiable » dans chaque Skill qui lit le texte d'un tiers | S, JD | ✅ |
| Descriptions avec « pas pour X (utiliser Y) », sous la limite, sans tiret cadratin | S, AN | ✅ |
| Scripts : `--help`, `--exemple`, `--json`, codes de sortie typés, Python sans dépendance | A | ✅ |
| Tests de cohérence des instructions (Skills et fichiers cités existent, gabarits vides, grilles = 100) | S, JD | ✅ |
| Évals : `evals.json` par Skill, correcteurs déterministes, comparaison à l'aveugle avec J et S, optimisation des descriptions (requêtes qui doivent et ne doivent pas déclencher) | AN, S, C | ✅ |
| Annoncer une limite (publication impossible) une seule fois, jamais de relance après un refus | S | ✅ |
| Lien de promotion, demande d'étoile GitHub | S, T | ✖ |

---

## Ce qui manque à la v1, honnêtement

- **Matière** : la v1 n'a ni banque d'histoires, ni interview. Les chiffres sont
  demandés au cas par cas, puis perdus d'une séance à l'autre.
- **Contexte de l'entreprise** : rien sur les offres, l'appel à l'action par sujet, les
  preuves étiquetées ou le vocabulaire client.
- **Mesure** : un seul script de mesure en dehors de l'humaniseur (`job_url.py`). Ni
  note du titre, ni audit du profil par points/heure, ni linter de post, ni budget en
  minutes, ni garde-fou de volume, ni statistiques honnêtes dans l'audit (qui compare
  des moyennes).
- **Preuves** : les chiffres sur LinkedIn sont présentés sans niveau de preuve. On
  reprend notamment la règle « 900-1 300 caractères » comme une vérité.
- **Humaniseur** : il compte les marqueurs mot par mot et récompense la variation de
  rythme. Il ne vérifie pas que les faits sont conservés et n'a pas de garde
  anti-sur-correction. Environ 10 marqueurs de Boileau manquent.
- **Page entreprise et ambassadeurs salariés** : absents, alors que c'est une demande
  fréquente chez des marketeurs en interne.
- **Sécurité** : pas de règle explicite « contenu non fiable ».
- **Tests et évals** : bonne base (humaniseur, job, 8 cas comparés à J). Mais pas de
  tests de cohérence des instructions, ni d'évals par Skill, ni d'optimisation des
  descriptions.

---

## Questions à trancher avant d'écrire

1. Valides-tu la liste des Skills : 3 nouveaux (`strategie`, `interview`,
   `entreprise`), `plan` recentré sur la semaine, et `carousel` renommé `carrousel` ?
2. Valides-tu les arbitrages du tableau ci-dessus, en particulier ta règle sur le tiret
   cadratin, maintenue contre l'avis de S ?
3. Les fichiers communs `contexte.md` (personne et entreprise) et `reserve.md` (banque
   d'histoires) te conviennent-ils ?
4. Par quel Skill modèle veux-tu commencer ? Je propose `/linkedin-profile`, avec
   `/linkedin-interview`, parce que c'est ton axe principal et qu'il exerce tout le
   gabarit : scripts, références, preuves et évals.
