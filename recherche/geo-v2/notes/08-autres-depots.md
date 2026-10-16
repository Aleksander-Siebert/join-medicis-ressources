# Autres dépôts lus

## aaron-marketing-skills (Aaron He Zhu)

Apache 2.0, 3k étoiles, commit 7975010 du 16 oct. 2026, 1 089 fichiers.
Remplace `seo-geo-claude-skills` (221 étoiles, devenu un dépôt de renvoi).
Lu : `seo-geo/` (16 Skills, dont `implement/geo-content-optimizer` et ses
6 références, `evaluate/offsite-signal-analyzer`,
`tune/content-quality-auditor`), `references/core-eeat-benchmark.md`
(80 critères), `scripts/connectors/tavily.py`.

- **Étiquette de chaque chiffre** : mesuré (outil ou export), fourni par
  l'utilisateur, estimé (déduit par le modèle) ; une donnée absente est
  « N/A », jamais inventée. Même principe qu'elmo.
- **Test gratuit dans un vrai moteur de réponse** : l'API de recherche de
  Tavily marche **sans clé** (accès limité en débit) et `--answer` renvoie
  une réponse rédigée avec ses sources. Testé le 16 oct. 2026 sur
  « meilleure assurance santé expatrié » : 200, réponse et 5 sources
  françaises, **mais réponse en anglais**. À présenter comme une
  approximation (« le moteur de Tavily, pas ChatGPT ni Perplexity ») et
  avec l'avertissement que la requête part chez un tiers.
- Contrôle robots.txt avant toute extraction déléguée à un tiers ; refus
  si interdit.
- Grille CORE-EEAT (80 critères) et auto-contrôle GEO : lourde, et des
  techniques à écarter (« définitions autonomes de 25 à 50 mots »,
  schema FAQ « pour l'IA »).
- Beaucoup d'outillage interne (contrats, routage, maturité) sans intérêt
  pour nous.

## eGEOagents / E-GEO (mverab)

MIT, 202 étoiles, commit 28fea4d du 15 oct. 2026. CLI Python, 5 Skills
Claude Code, un mode boucle (« une unité de travail par réveil, une
entrée de journal, historique en ajout seul, ne jamais inventer »), un
article de recherche (arXiv 2511.20867, GEO pour le e-commerce).

- **À écarter pour nous** : la grille `content-scoring` note sur 10
  « l'urgence » (rareté, « maintenant »), « l'emphase de classement »
  (superlatifs, « n°1 ») et la « narration persuasive ». C'est contraire
  à notre ton (style affirmatif, sans superlatif creux) et risqué au
  regard des pratiques commerciales trompeuses (Code de la consommation)
  **[à vérifier : articles exacts]**.
- **À noter** : validation pré-enregistrée (`PREREG-v4.md`), juge avec
  identifiants neutres pour qu'il ne reconnaisse pas les sections de
  l'utilisateur : même logique que notre éval à l'aveugle.

## seranking/seo-skills (SE Ranking)

MIT, 173 étoiles, commit fd6d140 du 24 juin 2026. 32 Skills qui
**exigent le serveur MCP de SE Ranking** (payant) : `seo-geo` (une URL,
requêtes AIO qui la citent ou non), `seo-ai-search-share-of-voice`
(classement par moteur, 10 prompts par marque où elle est source et
10 où elle est nommée, regroupement par thème). Utile comme modèle de
**sortie avec un connecteur** pour notre section « Données ». Il
recommande encore le schema FAQ et HowTo.

## ultimate-seo-geo (mykpono)

MIT, 90 étoiles, commit c92fdba du 1er oct. 2026. Agent SEO + GEO
« indépendant du modèle » (Claude, Codex, Gemini, ChatGPT), 215 fichiers
Python, **1 775 tests réussis** (16 oct. 2026).

- **`citation_sampling.py`** : sans API ni clé, transforme des passages
  notés à la main (CSV : date, moteur, prompt, passage, cité, mentionné,
  domaines cités, réponse) en **taux avec intervalle de Wilson à 95%** ;
  génère la grille à remplir ; vérifie les faits de la marque dans les
  réponses (année de création, siège, prix, oui/non, phrases fausses
  connues) en ne lisant que les phrases qui nomment la marque ; faits
  par segment (prix entreprise contre particulier). **Le plus proche de
  ce que doit devenir notre `visibilite.py`**, mais ses motifs sont
  anglais (« founded in », « headquartered in »).
- `ai_bot_logs.py` (journaux serveur), `ai_bot_access.py`,
  `faq_parity.py` (FAQ balisée = FAQ visible), `finding_verifier.py`
  (dédoublonne et retire les constats contredits par les preuves),
  `llms_txt_checker.py`.
- Changements à risque (robots.txt, canonical, redirections, noindex) :
  expliquer et faire confirmer avant de donner le code. Bonne règle.

## Écartés après examen

- SNLabat/SEO-GEO-AEO-Skill (244 étoiles) : pas de licence détectée, un
  seul fichier.
- thevibegarage/geo-visibility-skill, geofn-com/open-geo : 1 étoile.
- Infrasity-Labs/dev-gtm-claude-skills (141, juin) : orienté
  documentation développeurs.
- irinabuht12-oss/google-meta-ads-ga4-mcp : vitrine d'un service payant.
