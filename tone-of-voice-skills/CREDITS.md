# Notre méthodologie

Les Skills Join Médicis sont une production 100% Join Médicis, conçue à la main.

Les guides de « brand voice » qui circulent sont pensés pour des marques
américaines, décrivent la voix avec des adjectifs que tout le monde
revendique, et ne mesurent rien. Pour ce Skill, nous avons lu dix projets en
entier (Skills, références, scripts, tests, CHANGELOG), gardé ce qui marche,
écarté ce qui ne sert pas un marketeur seul devant son clavier, et tout
réécrit pour le français : tutoiement et vouvoiement, « ça » et « cela »,
négation sans « ne », typographie française.

# Transparence & inspirations

Le code et les consignes sont une création Join Médicis. Aucun texte n'a été
recopié. Nous remercions les auteurs des projets suivants :

- [knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), Anthropic (Apache 2.0) : `small-business/shared/voice-profile.md` (un fichier de voix partagé par tous les Skills, les « jamais » comme partie la plus utile, un journal qui garde la raison) ; `partner-built/brand-voice` de Tribe AI (MIT) : la voix constante et le ton qui varie, « Nous sommes / Nous ne sommes pas », les questions ouvertes accompagnées d'une recommandation
- [claude-night-market](https://github.com/athola/claude-night-market), athola (MIT) : plugin `scribe`, la comparaison avec la sortie par défaut de l'IA, le test de spécificité, les négations, l'apprentissage à partir des retouches
- [cc-prose](https://github.com/rhuss/cc-prose), Roland Huss (MIT) : les mesures de corpus, la détection des textes à part et du mélange d'auteurs, la confiance selon le volume
- [voice-analyser-mcp](https://github.com/houtini-ai/voice-analyser-mcp), Houtini (Apache 2.0, projet archivé) : le Skill de voix qui apprend par l'exemple, les règles écrites seulement quand le corpus les justifie
- [claude-code-toolkit](https://github.com/notque/claude-code-toolkit), notque, Claude Code Agents Contributors (MIT) : le seuil « rare » de la ponctuation, la bande d'écart-type des phrases, le test A/B
- [ai-marketing-claude-code-skills](https://github.com/brianrwagner/ai-marketing-claude-code-skills), Brian Wagner (MIT annoncé dans le README) : la priorité aux écrits spontanés, les zones où l'on tranche, le test « ça sonne comme toi ? »
- [everything-claude-code](https://github.com/affaan-m/everything-claude-code), Affaan Mustafa (MIT) : `brand-voice`, l'empreinte de voix qui ne va pas dans un dépôt public
- [claude-skills](https://github.com/rampstackco/claude-skills), RampStack Co. (MIT) : `brand-voice`, le test de résistance par trait et contre un concurrent, la voix « aspirationnelle »
- [brand-building-skills](https://github.com/arnabbagxd/brand-building-skills), arnabbagxd (MIT) : `brand-voice`, le parcours par questions seules
- Kate Moran, « The Four Dimensions of Tone of Voice », Nielsen Norman Group, 17 juillet 2016 (revu le 16 août 2023) : les quatre curseurs
- Spécification Agent Skills (agentskills.io/specification, lue le 27 octobre 2026) : règles du nom et de la description du Skill « ma-voix »

Ce que le pack ajoute : des mesures françaises par script, une voix vérifiable
texte par texte (`ecart.py`), un calibrage par variantes, un Skill « ma-voix »
construit et contrôlé par script, et une mise à jour sans retouche à la main.
