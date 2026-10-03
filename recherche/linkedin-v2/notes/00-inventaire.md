# LinkedIn v2, inventaire des sources (2 octobre 2026)

Clones dans /tmp/claude-0/refs/ (toutes MIT sauf mention)

| Source | Fichiers | Lignes | Rôle |
|---|---|---|---|
| Jakeschincariol/linkedin-agent-skill | 22 | 2 710 | base du pack v1 : 11 Skills li-*, humanize.py/detect.py/slop.json, hooks.json, rubric.json, voice.md |
| JoshuaDIWork/Linkedin_SKILL | 26 | 6 427 | dérivé de Jake (di-li-*) : + positioning.md, page_rubric.json (page entreprise), tag_status.py (audit), tests/test_pack.py, slop.json 2 582 l. |
| sergebulaev/linkedin-skills | 208 (104 hors doublon .codex-marketplace) | 27 267 | 12 Skills + references racine (hook-formulas 681 l., algorithm-heuristics, founder-topics, industry-benchmarks, story-bank, voice-profile, untrusted-content), humanizer très riche (scrub-rules 554 l., tier-rationale, detector-list, sub-skills), interviewer, employee-advocacy, thread-monitor, engager-analytics, hook-extractor ; lib/ (Apify, Publora, Pixfaro : APIs payantes), tests, evals/run_evals.py, CLAUDE.md, AGENTS.md, SECURITY.md, 131 commits |
| alirezarezvani/claude-skills (marketing/linkedin) | 64 | ~16 000 | plugin LinkedIn : 6 Skills avec references + assets + scripts (post_linter, headline_scorer, profile_completeness_auditor, outreach_volume_guard, pattern_miner, experiment_planner, cadence_planner, policy_gate…), agents (editor, orchestrator), commandes (grill, outreach…) |
| TaplioOfficial/taplio-linkedin-claude-skills | 30 | 3 397 | 26 Skills courts (~100 l.) : persona, niche, pillars, CTA, watchlist, warm leads, swipe file, viral analyzer, story extractor, analytics interpreter |
| marian-kamenistak/linkedin-post-writing-skill | 9 | 1 915 | LinkedIn_SKILL.md 682 l., anti-ai-writing-guide 471 l., weekly system, exemples |
| alxbd/boileau | 4 | 968 | humaniseur FR (SKILL 765 l.) |
| blader/humanizer | 14 | 964 | humaniseur EN (SKILL 397 l.), CHANGELOG 116 l., issues templates, 97 commits |
| Wikipédia EN « Signs of AI writing » | wikitext 222 Ko | | source primaire des marqueurs |
| Wikipédia FR « Identifier l'usage d'une IA générative » | wikitext 8,7 Ko | | |
| coreyhaines31/marketingskills | 469 | 86 749 | pertinents : social (1 958 l., carousel-frameworks, reverse-engineering, listening, platform-limits), copywriting, copy-editing, prospecting (compliance), product-marketing (contexte), customer-research, marketing-psychology, content-strategy, lead-magnets, cold-email, video ; chaque Skill a evals/evals.json |
| anthropics/skills (skill-creator) | 5 654 l. | | méthode officielle : écriture de Skills, évals, comparateur à l'aveugle, optimisation des descriptions |

Hors périmètre (pas de dépôt public trouvé ou payant) : smfardeen7 linkedin-outreach (à rechercher).
