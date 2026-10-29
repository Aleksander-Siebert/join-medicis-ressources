# Notre méthodologie

Les skills Join Médicis sont une production 100% Join Médicis, conçue à la main.

Nous sommes partis d'un constat simple, la majorité des prompts et agents disponibles aujourd'hui sont pensés pour le marché américain, restent trop généralistes et se cassent souvent les dents sur les réponses des IA en français et les secteurs exigeants (notamment les thématiques YMYL - Your Money or Your Life).

Pour créer ce pack, nous n'avons pas fait de simple compilation. Notre processus repose sur la rétro-ingénierie :
- Analyse de l'écosystème : Nous décortiquons la logique des meilleurs skills mondiaux.
- Rétro-ingénierie : Nous isolons les mécaniques qui performent réellement (architecture des pipelines, boucles de qualité, logique de raisonnement, scripts, etc.).
- Reconstruction & expertise : Nous recréons entièrement le skill en y injectant notre expérience de terrain, nos propres workflows et notre contexte métier.
- Localisation experte : Nous calibrons chaque instruction pour les nuances de la langue française, les règles/réglementations locales et la rigueur de rédaction anti-hallucination indispensable aux différents secteurs.

Le résultat ? Ce que ce pack vous apporte en exclusivité : une visibilité dans les réponses des IA pensée pour le français, des scripts sans clé d'API, un test de visibilité à partir de réponses réelles et un score qui n'invente jamais ce qu'il n'a pas mesuré.

# Transparence & inspirations
Bien que le code et les directives de chaque skill soient une création propre à Join Médicis, nous croyons en la culture open-source. Nos travaux de R&D s'appuient sur l'analyse et la compréhension d'excellents projets internationaux.

Nous tenons à remercier et créditer les auteurs des projets suivants, qui ont nourri notre réflexion. La version 2.0 est née de l'étude, fichier par fichier, de douze dépôts (notes dans `recherche/geo-v2/`).

- [geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude), Zubair Trabzada (MIT) : la rubrique de citabilité de la v1, devenue les contrôles de `/geo-contenu`
- [claude-seo](https://github.com/AgriciDaniel/claude-seo), Daniel Agrici (MIT) : le module seo-agentic (matrice datée des agents, catégorie Lighthouse), Content-Signal, et l'idée de confronter chaque conseil GEO aux sources de Google
- [marketingskills](https://github.com/coreyhaines31/marketingskills), Corey Haines (MIT) : l'échelle de visibilité, les verdicts d'exactitude, « cité mais pas recommandé »
- [skills-marketing-library](https://github.com/retieedra-profound/skills-marketing-library), Profound (MIT) : le diagnostic par couches dans l'ordre où le moteur rencontre la page, les familles de faits, la plus petite intervention crédible
- [geo-optimizer-skill](https://github.com/Auriti-Labs/geo-optimizer-skill), Juan Camilo Auriti (MIT) : la cohérence du nom de marque et ses cas réels (séparateurs, sous-types d'Organization, domaines homonymes), la détection des consignes cachées aux IA
- [elmo](https://github.com/elmohq/elmo), Blue Whale Software (MIT) : « les sources citées sur les questions perdues sont le plan », la correction à la source
- [ultimate-seo-geo](https://github.com/mykpono/ultimate-seo-geo), Myk Pono (MIT) : la vérification des faits de marque dans les réponses et les cas de son CHANGELOG (faits des concurrents, homonymes)
- [gtm-engineer-skills](https://github.com/onvoyage-ai/gtm-engineer-skills), OnVoyage AI (MIT) : la séparation entre note mesurée par script et note de jugement
- [geo-score](https://github.com/jianruntech/geo-score), Jianrun Tech (MIT) : un contrôle non mesuré sort du dénominateur
- [aaron-marketing-skills](https://github.com/aaron-he-zhu/aaron-marketing-skills), aaron-he-zhu (Apache 2.0) : l'appel sans clé à Tavily ; idée reprise, code réécrit
- Recherche : Aggarwal et al., « GEO », KDD 2024 ; Puerto et al., C-SEO Bench, NeurIPS 2025 ; O. Martinez, revue critique du GEO, 2026 ; méthode des passages répétés (arXiv 2609.04047)
- Sources primaires : pages des robots d'OpenAI, Anthropic, Perplexity, Mistral, Google et Apple ; Google Search Central (guide sur l'IA générative, réglage de Search Console, données structurées) ; RFC 9309 ; Cloudflare (Content Signals) ; web.dev et Lighthouse ; Code de la consommation (Légifrance)

Ce que le pack ajoute : le français et ses formulations (lexiques de
recommandation, de mise en garde, de source), des taux de visibilité avec
leur marge d'erreur et une comparaison de périodes qui ne confond pas bruit
et tendance, la lecture de chaque robot selon son rôle, le registre
d'exactitude sur les données de la marque, des scripts sans clé d'API
testés sur des cas réels, et le cadre français sur les avis, l'influence et
les pratiques commerciales.

Les mentions de copyright exigées par la licence MIT sont reproduites dans
[`LICENSE`](LICENSE).
