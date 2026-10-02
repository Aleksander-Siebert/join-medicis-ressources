# GEO Skills

Sept Skills en français pour que votre marque soit citée par ChatGPT,
Perplexity, Gemini, Claude, Mistral et les AI Overviews de Google. On dit
aussi AEO (Answer Engine Optimization) : le but est le même, apparaître dans
la réponse et pas seulement dans la liste de liens.

Pas besoin d'outil payant. Les scripts mesurent ce qui se mesure (citabilité,
robots d'IA, données structurées) ; le reste est évalué et affiché comme tel.
Aucun score, aucune réponse d'IA n'est inventé : sans mesure, le Skill
écrit « à évaluer ».

Par [Join Médicis](https://joinmedicis.com/ressources/skills/geo-skills).
Sources d'inspiration dans [CREDITS.md](CREDITS.md).

## Les sept

| Commande | Ce qu'elle fait |
|---|---|
| `/geo-audit` | Score GEO sur 100 en six catégories. Chaque note dit si elle est mesurée ou évaluée. |
| `/geo-citability` | Note chaque section (réponse, autonomie, structure, données, originalité) et réécrit les passages faibles. |
| `/geo-crawlers` | Robots d'IA autorisés ou bloqués, un par un, robots.txt selon votre stratégie, brouillon de llms.txt. |
| `/geo-visibility` | 15 à 30 prompts réalistes, vous collez les réponses, le Skill calcule présence, rang, part de voix et sources citées. |
| `/geo-schema` | Ce qui manque en JSON-LD et le bloc à coller, rempli seulement avec des informations vraies. |
| `/geo-mentions` | Où la marque est citée (presse, comparateurs, forums, avis, Wikipédia) face aux concurrents, et un plan propre. |
| `/geo-optimize` | La stratégie : trois piliers, méthodes validées par la recherche, plan sur 90 jours. |

Le pack partage `site-context.md` et `apprentissages.md` avec le
[pack SEO](../seo-skills). Les deux s'installent ensemble sans conflit.

## Installer

Claude Code :

```
/plugin marketplace add Aleksander-Siebert/join-medicis-ressources
/plugin install geo-skills@join-medicis
```

claude.ai et Claude Desktop : activez l'exécution de code (Réglages →
Capacités), puis importez `geo-skills.zip` dans Personnaliser → Skills. Le ZIP
se télécharge sur [la fiche Join Médicis](https://joinmedicis.com/ressources/skills/geo-skills)
ou se construit avec `claude-ai/build.sh geo-skills.zip`.

ChatGPT, Gemini, Mistral : collez le `SKILL.md` voulu dans un Projet, un GPT,
un Gem ou un Skill Vibe. Les Skills font alors les contrôles à la lecture.

Ensuite, lancez `/geo-audit` sur votre page la plus importante.

## Les scripts

Quatre scripts Python sans dépendance :

```bash
python3 skills/geo-audit/geo_audit.py https://www.site.fr/guide/
python3 skills/geo-citability/citability.py https://www.site.fr/guide/ --top 5
python3 skills/geo-crawlers/crawlers.py https://www.site.fr --robots-propose equilibre
python3 skills/geo-visibility/visibilite.py reponses.txt --marque "Assurly" --concurrent "April International"
```

## Tests

```bash
python3 evals/scripts/test_geo.py   # 6 tests
```

## Licence

MIT. Les mentions des projets d'origine sont dans [LICENSE](LICENSE).
