# Crédits

Ce pack est une synthèse. La v2 a été construite en lisant en entier les
dépôts ci-dessous (Skills, références, scripts, tests, historique), en
gardant ce qui tenait, en écartant ce qui était fragile ou contraire aux
règles de LinkedIn, puis en réécrivant tout en français pour le marché
français. Les matrices de capacités (ce qui a été repris, amélioré ou écarté,
et pourquoi) sont dans `recherche/linkedin-v2/MATRICES.md` à la racine du
dépôt.

| Source | Licence | Ce qu'on a repris |
|---|---|---|
| [Jake Schincariol, linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill) | MIT | L'architecture de la v1 (commandes, fichier de voix, journal), les types de commentaires, la structure des scripts de l'humaniseur, le tri de la messagerie |
| [Joshua, Design Industries, Linkedin_SKILL](https://github.com/JoshuaDIWork/Linkedin_SKILL) | MIT | Les faits marqués LIVE, À CONFIRMER, RETIRÉ ; la lecture seule stricte ; les 6 catégories de messagerie et le signalement CRM ; « ne demander que ce qui change chaque semaine » |
| [Serge Bulaev, linkedin-skills](https://github.com/sergebulaev/linkedin-skills) | MIT | Les accroches par objectif, la règle de densité des tics, le filtre chiffré des commentaires et les modèles de réponse R1 à R5, les règles de planning (formule, pilier, objectifs), les règles par source du recyclage |
| [Alireza Rezvani, claude-skills (linkedin)](https://github.com/alirezarezvani/claude-skills) | MIT | Les niveaux de preuve, les 5 questions de stratégie, le budget sur une mauvaise semaine, la note du titre et des Infos, la ligne propre à la personne et le garde-fou de volume, l'analyse par médiane et permutation, le plan d'expérience, le découpage des sources et le registre de réutilisation |
| [Taplio, taplio-linkedin-claude-skills](https://github.com/TaplioOfficial/taplio-linkedin-claude-skills) | MIT | Les contextes d'invitation, la notation des leads chauds, la routine de 15 minutes. Sans l'outil payant ni ses liens |
| [Marian Kamenistak, linkedin-post-writing-skill](https://github.com/marian-kamenistak/linkedin-post-writing-skill) | MIT | La calibration de la voix à partir de ses propres posts |
| [Corey Haines, marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT | Lire le contexte produit d'abord, la grille de priorité des posts à commenter, les structures de carrousel |
| [alxbd, Boileau](https://github.com/alxbd/boileau), dérivé de [Siqi Chen, humanizer](https://github.com/blader/humanizer) | MIT | Les marqueurs d'écriture IA en français, les passes de l'humaniseur, le contrôle de sur-correction |
| [Anthropic, skills (skill-creator)](https://github.com/anthropics/skills) | Apache 2.0 | La méthode : descriptions qui disent quand déclencher, références lues à la demande, `evals.json` par Skill. Aucun texte ni code repris |
| [Wikipédia, Aide:Identifier l'usage d'une IA générative](https://fr.wikipedia.org/wiki/Aide:Identifier_l%27usage_d%27une_IA_g%C3%A9n%C3%A9rative) | CC BY-SA | Inspiration seulement : la liste des signes d'écriture IA et la règle « un signe isolé ne prouve rien ». Rien n'est copié |
| [kvsdileep, linkedin-writer](https://github.com/kvsdileep/linkedin-writer) | MIT annoncée | Idée : afficher le nombre de caractères |
| [Attainment, linkedin-algorithm-skill](https://github.com/attainmentlabs/linkedin-algorithm-skill) | sans licence formelle | Idée seulement, réécrite : marquer chaque affirmation d'un niveau de confiance |

Les faits sur LinkedIn viennent des pages d'aide de LinkedIn, des Professional
Community Policies, des publications de LinkedIn Engineering et de la CNIL,
consultées et datées dans `commun/preuves.md`. Les études tierces citées (La
Growth Machine, MagicPost, AuthoredUp, Richard van der Blom) y sont marquées
comme telles.

Merci à leurs auteurs. Les mentions de copyright exigées par la licence MIT
sont reproduites dans [`LICENSE`](LICENSE).

## Ce que le pack ajoute

- Le français et le marché français : typographie, CNIL et RGPD de la
  prospection, mention de partenariat (loi du 9 juin 2023), jours fériés et
  ponts, exemples en euros.
- Un socle commun : règles, preuves datées par niveau, garde-fou exécutable.
- Des scripts testés pour chaque Skill, séparés du jugement.
- `/linkedin-job`, `/linkedin-entreprise`, `/linkedin-interview` et
  `/linkedin-strategie` dans leur forme actuelle.
- Une boucle d'apprentissage contrôlée : `apprentissages.md`, validé par
  l'utilisateur, alimenté par des expériences dont le critère d'échec est
  écrit avant.
