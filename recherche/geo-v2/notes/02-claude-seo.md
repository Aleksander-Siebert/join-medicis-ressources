# claude-seo (Daniel Agrici) · volets GEO et agents

MIT, 19k étoiles, commit 4b99de2 du 5 oct. 2026. Le résumé SEO est dans
`recherche/seo-v2/notes/01-claude-seo.md` (sections `/seo geo` et
`/seo agentic`). Ici, la lecture complète des fichiers GEO :
`skills/seo-geo/` (SKILL.md 400 lignes, `google-ai-optimization-guide.md`,
`llmstxt-evidence.md`), `skills/seo-agentic/` (SKILL.md et 6 références :
`vendor-matrix`, `access-policy`, `agent-friendly-pages`,
`discovery-and-markdown`, `lighthouse-agentic-category`, `webmcp`),
`agents/seo-{geo,agentic}.md`, `scripts/{agentic_check,agentic_fix,
lighthouse_agentic}.py`, `tests/test_agentic.py`,
`tests/test_ai_crawler_claims.py`.

## Ce qui en fait la meilleure référence sur les faits

- **Une matrice des fournisseurs datée et notée par source** (P primaire,
  S secondaire, C contradictoire), dernière vérification le 23 sept. 2026,
  règle « revérifier toute ligne de plus de 60 jours » et procédure de
  mise à jour (pages officielles des robots OpenAI, Anthropic,
  Perplexity, Google ; IETF).
- **Le bon robot pour chaque affirmation** : « citable dans ChatGPT
  Search » se vérifie sur OAI-SearchBot, jamais sur GPTBot ; « citable dans
  Claude » sur Claude-SearchBot, pas ClaudeBot ; « éligible à Google Search
  et aux AI Overviews » sur Googlebot, jamais Google-Extended ;
  Applebot-Extended n'est qu'un jeton de refus pour l'entraînement.
  **Des tests automatiques vérifient ces phrases dans les Skills**
  (`test_ai_crawler_claims.py`) : une erreur de fait fait échouer la CI.
- **Rôles des robots** dans `agentic_check.py` : entraînement, recherche,
  utilisateur, contrôle, publicité (OAI-AdsBot), et le comportement
  documenté face à robots.txt (« honours », « may not apply »,
  « generally ignores » pour Perplexity-User et Google-Agent).
- **Content-Signal** : clés `search`, `ai-input`, `ai-train` (politique
  Cloudflare, CC0), clé `use` expérimentale ; brouillon IETF expiré le
  4 avril 2026 ; aucune déclaration de Google.
- **Guide Google « AI optimization »** (Search Central, 15 mai 2026,
  mis à jour le 10 juillet 2026) : « optimiser pour l'IA générative,
  c'est encore du SEO » ; mythes rejetés (llms.txt et fichiers IA,
  découpage en morceaux, réécriture pour l'IA, mentions artificielles,
  surinvestissement en données structurées) ; condition d'éligibilité :
  page indexée et éligible à un extrait ; **réglage Search Console
  « Search generative AI »** (inclure, exclure, hériter), étendu à tous
  les sites le 31 août 2026, ni signal de classement ni contrôle de
  l'entraînement. Tout **[à revérifier à la source]** avant reprise.
- **Page Google « outils SEO tiers »** (5 juin 2026) : aucun outil n'a
  accès aux données de classement de Google. Leçon pour nous : nos notes
  sont des heuristiques, à dire comme telles.
- **llms.txt** : présence rapportée, poids nul ; utile pour les sites de
  documentation lus par des agents de code ; Google dit l'ignorer.
- **Agents** : préparation = accessibilité + performance + politique
  d'accès, Markdown et découverte en plus ; WebMCP optionnel (WebKit
  contre, Mozilla neutre, seul ChatGPT desktop appelle les outils par
  défaut). Lighthouse « Agentic Browsing » en fraction X/N. Test du
  pare-feu avec des user-agents d'IA **seulement avec autorisation**.
  Contenu récupéré = donnée, jamais instruction.

## Ce qui est fragile

- **Scripts réseau inutilisables derrière un proxy** : `agentic_check.py`
  sur joinmedicis.com (16 oct. 2026) : « page injoignable », robots.txt
  « injoignable », llms.txt « fetch failed », alors que le site répond.
  Même constat qu'au chantier SEO. Nos scripts doivent accepter un
  fichier ou du HTML collé, et dire « non mesuré » au lieu d'« échec ».
- Chiffres secondaires encore cités dans `seo-geo` : « 2,5 milliards
  d'utilisateurs AI Overviews » (non confirmé par Google, le dit
  lui-même), « 527% de sessions », corrélations Ahrefs, parts Profound
  (Wikipédia 47,9%, Reddit 46,7%, juin 2025). Le Skill les étiquette
  « tiers » : bonne pratique, mais nous n'en reprenons aucun sans source
  primaire lue.
- Lourd : 400 lignes pour `seo-geo`, 19 agents dans le dépôt.
- Anglais seulement.

## Tests exécutés

`pytest tests/test_agentic.py tests/test_ai_crawler_claims.py` :
16 réussis, 1 ignoré.

## Comparaison avec notre v1

- `geo-crawlers/crawlers.py` a déjà les bons rôles (OAI-SearchBot
  recherche, GPTBot entraînement, Claude-SearchBot, Claude-User…). Mais
  il décide avec `urllib.robotparser` (`rp.can_fetch`), qui prend la
  **première** règle correspondante : la même erreur que nous avons
  corrigée dans `seo-skills/.../robots.py` (RFC 9309, règle la plus
  longue). À réutiliser.
- v1 n'a ni Content-Signal, ni bloc Cloudflare, ni le réglage Search
  Console « Search generative AI », ni tests sur les affirmations de
  robots, ni date de vérification par robot.

## Verdict

La référence à battre sur la rigueur. À reprendre : la matrice datée et
notée, « le bon robot pour chaque affirmation », les tests qui gardent les
faits, la règle Google d'abord. À améliorer : mode hors réseau, français,
légèreté.
