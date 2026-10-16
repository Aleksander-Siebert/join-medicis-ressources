# geo-seo-claude (Zubair Trabzada) · volets IA

MIT, 11k étoiles, commit 989cae0 du 5 oct. 2026 (le même qu'au chantier
SEO v2 : la partie SEO est déjà disséquée dans
`recherche/seo-v2/notes/03-geo-seo-claude.md`). Ici : robots d'IA,
llms.txt, citabilité, mentions de marque, plateformes, signaux d'agents.
Fichiers lus : `skills/geo-{crawlers,llmstxt,citability,brand-mentions,
platform-optimizer,audit}`, `agents/geo-{ai-visibility,platform-analysis}`,
`docs/scoring-methodology.md`, `pr-draft-*.md`, `scripts/{brand_scanner,
citability_scorer,llmstxt_generator,fetch_page}.py`, `tests/*`.

## Ce que font les Skills

- **geo-crawlers** : 14 robots en 3 niveaux, statut par robot dans
  robots.txt, balises meta et en-têtes `X-Robots-Tag` (`noai`,
  `noimageai`), fichiers `llms.txt`, `ai.txt`, `ai-plugin.json`, rendu
  JavaScript, directive `Content-Signal`, et **détection du bloc
  « Cloudflare Managed content »** ajouté par Cloudflare au robots.txt
  servi (le propriétaire ne le voit pas dans son fichier). Note d'accès
  sur 100 (niveau 1 : 50%, niveau 2 : 25%, pas de blocage global : 15%,
  fichiers IA : 10%).
- **geo-llmstxt** : analyse (format, qualité, pages manquantes, note sur
  100) et génération d'un llms.txt et d'un llms-full.txt.
- **geo-citability** : 5 critères par bloc (réponse 30%, autonomie 25%,
  structure 20%, statistiques 15%, originalité 10%), « couverture » =
  part des blocs au-dessus de 70, réécriture des blocs sous 60.
- **geo-brand-mentions** : note d'autorité de marque (YouTube 25%,
  Reddit 25%, Wikipédia/Wikidata 20%, LinkedIn 15%, autres 15%), le
  script n'interroge vraiment que l'API Wikipédia/Wikidata ; YouTube,
  Reddit et LinkedIn renvoient des liens de recherche à ouvrir à la main.
- **geo-platform-optimizer** : une grille sur 100 par plateforme
  (AI Overviews, ChatGPT, Perplexity, Gemini, Copilot).
- **Signaux d'agents** (PR en brouillon) : négociation `Accept:
  text/markdown`, en-têtes `Link` (RFC 8288). Non notés : « recommandation,
  jamais de pénalité ».
- **Note GEO globale** : citabilité 25, marque 20, E-E-A-T 20,
  technique 15, schema 10, plateformes 10.

## Erreurs de fait (à corriger chez nous, sources primaires à l'appui)

- **GPTBot présenté comme le robot de ChatGPT Search** (« le plus
  important à autoriser »). OpenAI distingue GPTBot (entraînement),
  OAI-SearchBot (recherche) et ChatGPT-User (action de l'utilisateur)
  **[à vérifier sur la page officielle des robots OpenAI]**.
- **`anthropic-ai`** donné comme robot d'entraînement actif, ClaudeBot
  comme robot de recherche : Anthropic documente d'autres noms
  (ClaudeBot, Claude-User, Claude-SearchBot) **[à vérifier]**.
- **Content Signals** : clés `ai-train`, `search`, `ai-personalization`,
  `ai-retrieval` ; la politique de Cloudflare cite `search`, `ai-input`,
  `ai-train` **[à vérifier : contentsignals.org et brouillon IETF]**.
- **Chiffres sans source vérifiable** : « 35% des 1 000 premiers sites
  bloquent un robot IA » (Originality.ai), « 11% des domaines cités par
  ChatGPT et AI Overviews », « 92% des citations AIO dans le top 10 »,
  « Wikipédia 47,9% des citations ChatGPT », « Reddit 46,7% pour
  Perplexity », « corrélation 0,737 YouTube » (Ahrefs, déc. 2025),
  « moins de 5% des sites ont un llms.txt ». Tous **[à vérifier]** ;
  aucun ne doit passer dans nos Skills sans source primaire datée.
- **Conseils sans fondement** : « 2 000 mots et plus pour ChatGPT »,
  « passages de 134 à 167 mots », « Copilot écarte les pages de plus de
  2 s », « llms.txt = avantage du premier arrivé ».
- **Réécriture** : « suggérer des statistiques à ajouter » pousse à
  inventer des chiffres. Notre règle : `{{à compléter}}`.
- **Modèle « visibilité maximale »** : autorise `anthropic-ai` et bloque
  CCBot, sans dire que c'est un choix d'entraînement et non de
  visibilité.

## Ce qui vaut d'être repris

- Détection du bloc Cloudflare géré dans le robots.txt servi.
- Lecture des en-têtes `X-Robots-Tag` et des balises propres à un robot.
- Signaux d'agents **non notés** (négociation Markdown, `Link`), avec la
  règle « absence normale = ne pas en parler ».
- Couverture de citabilité (part des blocs au-dessus d'un seuil) : un
  indicateur plus parlant qu'une moyenne.
- Wikidata interrogé par API (gratuit, sans clé).

## Verdict

Large couverture, beaucoup de folklore chiffré. Bon inventaire de
contrôles techniques ; à reprendre seulement après vérification de
chaque robot et de chaque clé à la source.
