# Inventaire des sources GEO v2 (16 octobre 2026)

Clones complets (`git clone --depth 1`) dans un dossier de travail.
Étoiles, licence et dernier commit relevés via shields.io le même jour.
Scripts lancés quand c'était possible (résultats dans chaque note).

| Source | Étoiles | Licence | Dernier commit | Fichiers | Note |
|---|---|---|---|---|---|
| [zubair-trabzada/geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) | 11k | MIT | 2026-10-05 | 71 | 01 |
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | 19k | MIT | 2026-10-05 | 469 | 02 |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) `ai-seo` | 55k | MIT | 2026-10-15 | 684 (dont 17 pour `ai-seo`) | 03 |
| [retieedra-profound/skills-marketing-library](https://github.com/retieedra-profound/skills-marketing-library) (Profound) | 0 | MIT | 2026-08-31 | 25 | 03 |
| [Auriti-Labs/geo-optimizer-skill](https://github.com/Auriti-Labs/geo-optimizer-skill) | 1,1k | MIT | 2026-10-16 | 683 | 04 |
| [onvoyage-ai/gtm-engineer-skills](https://github.com/onvoyage-ai/gtm-engineer-skills) | 1,3k | MIT | 2026-10-11 | 75 | 05 |
| [jianruntech/geo-score](https://github.com/jianruntech/geo-score) | 323 | MIT | 2026-10-15 | 1 621 | 06 |
| [elmohq/elmo](https://github.com/elmohq/elmo) | 459 | MIT | 2026-10-15 | 1 503 (dont 8 pour le Skill `aeo`) | 07 |
| [aaron-he-zhu/aaron-marketing-skills](https://github.com/aaron-he-zhu/aaron-marketing-skills) | 3k | Apache 2.0 | 2026-10-16 | 1 089 | 08 |
| [mverab/eGEOagents](https://github.com/mverab/eGEOagents) | 202 | MIT | 2026-10-15 | 254 | 08 |
| [seranking/seo-skills](https://github.com/seranking/seo-skills) | 173 | MIT | 2026-06-24 | 287 | 08 |
| [mykpono/ultimate-seo-geo](https://github.com/mykpono/ultimate-seo-geo) | 90 | MIT | 2026-10-01 | 408 | 08 |
| Sources primaires (OpenAI, Anthropic, Perplexity, Mistral, Google, Apple, Cloudflare, arXiv, Légifrance) | | | | | 09 |
| Notre v1 (`geo-skills` 1.1.0) | | MIT | | 8 Skills, 5 scripts, 8 tests | 10 |

Écartés : voir la fin de la note 08.

## Ce qui a tourné

| Outil | Résultat sur joinmedicis.com |
|---|---|
| geo-optimizer `geo audit` | 71/100 ; trouve un H1 doublé sur l'accueil |
| geo-score | 84/100 ; « pas de lexique français » pour 2 contrôles |
| elmo `check_ai_access.py` | 17 robots, tous à 200 |
| claude-seo `agentic_check.py` | échoue derrière le proxy (faux « injoignable ») |
| Tavily (via aaron-marketing-skills) | réponse d'IA sans clé, en anglais pour une question française |
| Tests | claude-seo 16/16, gtm 7/7, ultimate-seo-geo 1 775/1 775 |
