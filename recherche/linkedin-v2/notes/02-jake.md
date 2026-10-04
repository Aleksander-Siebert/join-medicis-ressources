# Jake Schincariol · linkedin-agent-skill (MIT, 22 fichiers, 1 commit)

Philosophie : gratuit, sans API, rien n'est publié (« These skills write. You post. »), honnêteté (pas de promesse « indétectable »), zéro invention ({{your number}}), voice.md lu par tous, log.md (historique des posts avec hook utilisé) → li-audit. Fichiers partagés ~/.claude/linkedin/{voice,log,plan}.md.

## li-post
- Avant : lire voice.md (sinon demander 3 posts et l'écrire) ; lire hooks.json ; idée mince → 1 question groupée (quoi, à qui, coût/gain).
- Forme : ligne 1 seule (~140 car. mobile / 210 desktop), ligne 2 = payoff (pas mise en place), paragraphes 1-3 lignes, « the turn » (recadrage), clôture = 1 question spécifique OU 1 instruction. 900-1 300 car. ; <400 = pensée ; >2 000 doit tout mériter.
- Boucle : 3 hooks de formules différentes + lequel et pourquoi ; brouillon ; humanisé ; bloc prêt à coller + reçu (hook, longueur, humaniseur, score, horaire du plan) ; « yes » → log.md.
- Règles : une idée/post ; chiffres > adjectifs ; pas d'appât (« Thoughts? ») ; 3 hashtags max ; pas de lien dans le corps (1er commentaire) ; jamais inventer.
- hooks.json : 21 formules {template, example, best_for, trap} + 5 règles (une idée par hook ; ligne 2 = payoff ; pas de ? en ligne 1 sauf question unique ; chiffres ; « si le hook marche avec le nom de quelqu'un d'autre, ce n'est pas ton hook »). Les « trap » sont la partie la plus précieuse.

## li-comment
- Pourquoi : un commentaire sous un post à 400 réactions vu par plus de monde que ses propres posts.
- Entrée : texte collé (pas de scraping, pas deviner une URL).
- 9 types (datum, cas manquant, désaccord respectueux, prolonger une ligne, la vraie question, le reçu, la correction, le recadrage, le one-liner <12 mots).
- Règles : 2-4 phrases ; ouvertures interdites listées ; pas d'émoji en tête ; ne pas reformuler le post ; une idée ; spécifique ; désaccord OK après accord réel.
- Sortie : 2 options de types différents + celle à poster et pourquoi ; humanisées.
- Mode lot : 5-10 posts, suivi de qui a été commenté (éviter les 3 mêmes personnes).

## li-reply
- Tri en 5 seaux avec comptes (LEAD, SUBSTANCE, PEER, SUPPORT, NOISE) puis écrire dans cet ordre, s'arrêter quand la valeur s'arrête.
- Règles : répondre à la vraie question publiquement (pas « en DM ») ; prénom une fois sans « ! » ; longueur miroir ; critique = concéder le vrai puis tenir ; lead = réponse complète + 1 phrase de porte ouverte ; pitch = ignorer.
- Première heure de réponses = portée.

## li-profile + rubric.json
- « Un profil n'est pas un CV » : répond à « dois-je contacter cette personne » en 4 s.
- Entrée : titre, about, rôle actuel + 2 expériences, bannière/sélection oui/non ; capture OK ; jamais se connecter.
- Rubrique 12 items /100 : headline 12, about_open 10, about_body 10, featured 8, banner 6, photo 6, current_role 10, experience_depth 8, skills 6, recommendations 8, activity 10, contact 6 ; chaque item a « full_marks ». Honnêteté : la plupart des profils 30-40.
- Réécriture par points perdus : titre 220 car. ({quoi pour qui} | {preuve} | {comment commencer}, 3 options, pas « Helping X do Y ») ; about 2 premières lignes ; corps à la 2e personne <1 400 car. ; sélection 3 éléments ; expériences = 1 ligne de périmètre + 2-3 résultats chiffrés, >10 ans compressés ; bannière.
- Re-score honnête à la fin + ce qu'une réécriture ne peut pas créer (recos, bannière, historique).

## li-plan
- 1 fois/semaine. Lit voice.md + log.md (ne pas répéter un thème de 15 jours). Sinon 4 questions (offre/cible, 3-4 thèmes, ce qui s'est passé cette semaine, 10-20 personnes).
- 4 posts/sem > 7. Mix : Proof, Opinion, Teach (1/sem chacun), Story, Offer (1/15 j). Chaque créneau : thème + angle tiré de la semaine + n° de hook.
- Horaires : B2B mar-jeu 7h30-9h30 heure du public ; « l'heure compte bien moins que la 1re ligne ».
- Liste d'engagement 10 : 5 reach (commenter avant 20 commentaires), 3 pairs, 2 acheteurs (commenter des semaines avant tout DM). 20 min/jour AVANT de publier.
- Écrit plan.md. « Say "write Tuesday" ».

## li-carousel
- Quand : idée avec séquence ; sinon renvoyer à li-post.
- 8-12 slides : couverture (≤6 mots + 1 ligne promesse), enjeu, 1 idée/slide (titre 3-7 mots, ≤25 mots), récap (capture), CTA unique. Numéroter (3/10), handle sur chaque slide.
- PDF 1080x1350 (4:5), <100 Mo, <300 pages ; HTML une <section> par slide, police ≥28px, 1 couleur d'accent, utiliser la charte si présente. Texte du post au-dessus (2-3 lignes). PDF seulement après validation du texte.

## li-repurpose
- Extraire, pas résumer : claims, numbers, stories, mechanisms, mistakes, lines (avec comptes). <4 éléments = source mince, le dire.
- Chaque post autonome (jamais « comme dans ma vidéo ») ; hooks variés ; ordre : claim le plus fort d'abord, story milieu de semaine, mécanisme en dernier. Rédiger un par un (pas 4 d'un coup).

## li-dm
- Questions groupées : qui, la raison d'écrire MAINTENANT (pas « ICP »), ce que l'utilisateur veut. Pas de raison → le dire.
- Note d'invitation ≤200 car. (compteur affiché) : référence précise + qui je suis + aucune demande.
- Message 1 après J+1 : 2-4 phrases, continuité avec la note, donner avant de demander, 1 petite demande, pas de lien calendrier.
- Relances : 2 seulement (J+4 avec du nouveau ; J+10 clôture). Jamais d'automatisation, jamais inventer un point commun, max 20 invitations/jour.

## li-inbox
- 5 seaux (LEAD, RECRUITER, PEER, ASK, SPAM) + comptes d'abord.
- Détection de séquence automatisée (note vide, message <minutes après acceptation, « quick question », lien calendrier msg 1, relance J+4) → dire quel indice.
- Réponses par seau (recruteur : demander salaire, niveau, présentiel ; « pick your brain » : décliner chaleureusement en donnant la réponse).

## li-audit
- Entrée : export Analytics CSV, captures, ou posts + réactions ; lit log.md (hook par post).
- Métriques : taux d'engagement, ratio commentaires/réactions, multiple de portée (impressions/abonnés), sauvegardes/envois. Classer par taux et multiple, pas impressions.
- Top 5 vs bottom 5 : hook, format, longueur, thème, jour/heure EN DERNIER, réponses 1re heure. Confiance selon n (6 posts → pas de conclusion). Sortie STOP / DO MORE → li-plan.

## li-human (+ humanize.py 257 l., detect.py 235 l., slop.json)
- slop.json : 17 invisibles, 11 typographiques, 81 mots, 32 phrases (familles), 11 structures (regex + fix).
- Corrige auto : invisibles, typographie (cadratin→virgule, guillemets droits…), lexique (casse préservée, URL intactes). Signale : structures (not just, triades, question d'un mot, émojis 🚀🔥💡✨🎯, murs de hashtags, appâts, longueurs uniformes).
- 5 contrôles 0-100 : BURSTINESS, SPECIFICITY, SLOP DENSITY, FINGERPRINT, VOICE. Verdict = 0,6 moyenne + 0,4 min ; PASS ≥70 et aucun <55 ; REVIEW ≥50 ; sinon FLAGGED. Code retour ≠0 si pas PASS. Comparaison avant/après.
- Ordre : humanize → réécrire les structures signalées → detect avant/après → corriger le contrôle le plus faible ; 2 tours normaux, 5 = changer de brouillon. Toujours montrer texte + score.

## Forces / faiblesses
+ Formats de sortie très précis (reçus, comptes par seau), « trap » des hooks, honnêteté, scripts réels.
+ Écosystème de fichiers partagés (voice/log/plan) qui relie les Skills.
- Pas de tests, pas d'évals, pas d'exemples d'entrée/sortie complets en références.
- Anglais/US (ET, $, contractions), heuristiques VOICE fausses en français.
- Profil : pas d'aide à extraire les chiffres (axe utilisateur), pas de page entreprise.
- Pas de recherche d'emploi, pas de stratégie/positionnement, pas d'analyse de concurrents/créateurs, pas de newsletter LinkedIn, pas de vidéo/sondage, pas de RGPD.
- Carrousel : pas de script PDF fourni (juste la consigne).
