# Notre méthodologie

Les skills Join Médicis sont une production 100% Join Médicis, conçue à la main.

Nous sommes partis d'un constat simple, la majorité des prompts et agents disponibles aujourd'hui sont pensés pour le marché américain, restent trop généralistes et se cassent souvent les dents sur les usages de LinkedIn en France (prospection encadrée par la CNIL, mention des partenariats, calendrier français) et produisent des textes qui sonnent IA.

Pour créer ce pack, nous n'avons pas fait de simple compilation. Notre processus repose sur la rétro-ingénierie :
- Analyse de l'écosystème : Nous décortiquons la logique des meilleurs skills mondiaux.
- Rétro-ingénierie : Nous isolons les mécaniques qui performent réellement (architecture des pipelines, boucles de qualité, logique de raisonnement, scripts, etc.).
- Reconstruction & expertise : Nous recréons entièrement le skill en y injectant notre expérience de terrain, nos propres workflows et notre contexte métier.
- Localisation experte : Nous calibrons chaque instruction pour les nuances de la langue française, les règles/réglementations locales et la rigueur de rédaction anti-hallucination indispensable aux différents secteurs.

Le résultat ? Ce que ce pack vous apporte en exclusivité : un LinkedIn pensé pour la France, une écriture qui ne sonne pas IA, des scripts testés pour tout ce qui se mesure, et une boucle d'apprentissage que vous validez vous-même.

# Transparence & inspirations
Bien que le code et les directives de chaque skill soient une création propre à Join Médicis, nous croyons en la culture open-source. Nos travaux de R&D s'appuient sur l'analyse et la compréhension d'excellents projets internationaux.

Nous tenons à remercier et créditer les auteurs des projets suivants, qui ont nourri notre réflexion :

- [linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill), Jake Schincariol (MIT) : l'architecture de la v1 (commandes, fichier de voix, journal), les types de commentaires, la structure des scripts de l'humaniseur, le tri de la messagerie
- [Linkedin_SKILL](https://github.com/JoshuaDIWork/Linkedin_SKILL), Joshua, Design Industries (MIT) : les faits marqués LIVE, À CONFIRMER, RETIRÉ ; la lecture seule stricte ; les 6 catégories de messagerie et le signalement CRM ; « ne demander que ce qui change chaque semaine »
- [linkedin-skills](https://github.com/sergebulaev/linkedin-skills), Serge Bulaev (MIT) : les accroches par objectif, la règle de densité des tics, le filtre chiffré des commentaires et les modèles de réponse R1 à R5, les règles de planning, les règles par source du recyclage
- [claude-skills (linkedin)](https://github.com/alirezarezvani/claude-skills), Alireza Rezvani (MIT) : les niveaux de preuve, les 5 questions de stratégie, la note du titre et des Infos, l'analyse par médiane et permutation, le plan d'expérience, le registre de réutilisation
- [taplio-linkedin-claude-skills](https://github.com/TaplioOfficial/taplio-linkedin-claude-skills), Taplio (MIT) : les contextes d'invitation, la notation des leads chauds, la routine de 15 minutes, sans l'outil payant ni ses liens
- [linkedin-post-writing-skill](https://github.com/marian-kamenistak/linkedin-post-writing-skill), Marian Kamenistak (MIT) : la calibration de la voix à partir de ses propres posts
- [marketingskills](https://github.com/coreyhaines31/marketingskills), Corey Haines (MIT) : lire le contexte produit d'abord, la grille de priorité des posts à commenter, les structures de carrousel
- [Boileau](https://github.com/alxbd/boileau), alxbd (MIT), dérivé de [humanizer](https://github.com/blader/humanizer), Siqi Chen (MIT) : les marqueurs d'écriture IA en français, les passes de l'humaniseur, le contrôle de sur-correction
- [skills (skill-creator)](https://github.com/anthropics/skills), Anthropic (Apache 2.0) : la méthode (descriptions qui disent quand déclencher, références lues à la demande, `evals.json` par Skill), sans texte ni code repris
- [Aide:Identifier l'usage d'une IA générative](https://fr.wikipedia.org/wiki/Aide:Identifier_l%27usage_d%27une_IA_g%C3%A9n%C3%A9rative), Wikipédia (CC BY-SA) : la liste des signes d'écriture IA et la règle « un signe isolé ne prouve rien », sans texte copié
- [linkedin-writer](https://github.com/kvsdileep/linkedin-writer), kvsdileep (MIT annoncée) : l'idée d'afficher le nombre de caractères
- [linkedin-algorithm-skill](https://github.com/attainmentlabs/linkedin-algorithm-skill), Attainment (sans licence formelle) : l'idée de marquer chaque affirmation d'un niveau de confiance, réécrite

Les faits sur LinkedIn viennent des pages d'aide de LinkedIn, des Professional
Community Policies, des publications de LinkedIn Engineering et de la CNIL,
consultées et datées dans `commun/preuves.md`. Les études tierces citées (La
Growth Machine, MagicPost, AuthoredUp, Richard van der Blom) y sont marquées
comme telles. Les matrices de capacités (ce qui a été repris, amélioré ou
écarté, et pourquoi) sont dans `recherche/linkedin-v2/MATRICES.md` à la racine
du dépôt.

Ce que le pack ajoute : le français et le marché français (typographie,
CNIL et RGPD de la prospection, mention de partenariat de la loi du 9 juin
2023, jours fériés et ponts, exemples en euros), un socle commun avec preuves
datées et garde-fou exécutable, des scripts testés pour chaque Skill, séparés
du jugement, et une boucle d'apprentissage validée par l'utilisateur.

Les mentions de copyright exigées par la licence MIT sont reproduites dans
[`LICENSE`](LICENSE).
