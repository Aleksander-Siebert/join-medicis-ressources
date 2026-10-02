# SEO Skills

Seize Skills en français pour faire du SEO sérieux avec Claude, ChatGPT,
Gemini ou Mistral. Vous partez d'un mot-clé, vous repartez avec un article
publiable, un audit classé par priorité ou un plan de maillage interne.

Pas besoin d'outil payant. Si vous avez connecté Search Console, Semrush ou
Ahrefs à votre IA, les Skills s'en servent et travaillent sur vos vraies
données. Ils n'inventent rien : un chiffre, un prix ou une condition sans
source devient `{{à compléter}}`. En santé, en assurance ou en finance, ça
change tout.

Par [Join Médicis](https://joinmedicis.com/ressources/skills/seo-skills).
Sources d'inspiration dans [CREDITS.md](CREDITS.md).

## Les seize

| Commande | Ce qu'elle fait |
|---|---|
| `/seo-plan` | La stratégie sur 12 mois : piliers, feuille de route en 4 phases, indicateurs partant de vos vraies données. |
| `/seo-context` | Remplit `site-context.md` : secteur, personas, pages à pousser, ton, règles maison. Tous les autres le lisent. |
| `/seo-keywords` | Mots-clés et intentions, regroupés en pages (une intention, une page), cannibalisation vérifiée. |
| `/seo-serp` | Lit la SERP à l'envers : type de page attendu, concurrents notés sur 40, manques, gain d'information. |
| `/seo-brief` | Le plan validable : framework PAS, AIDA, MECE ou pyramide inversée, title, H1 à H3 commentés, liens. |
| `/seo-write` | Rédige sur le plan validé : résumé de 3 lignes en tête, voix active, zéro invention, bloc méta. |
| `/seo-article` | Le chemin complet, avec une validation à chaque étape. |
| `/seo-human` | Retire les marques d'écriture IA d'un article sans casser son Markdown ni la typographie française. |
| `/seo-audit` | Audit d'une page ou d'un site par ordre de priorité : on-page, images, Core Web Vitals, bon type de page. |
| `/seo-drift` | Photo des éléments SEO avant une mise en ligne, comparaison après : `noindex` oublié, canonical cassé, H1 supprimé. |
| `/seo-maillage` | Lit le sitemap et regroupe vos pages en clusters. Repère les pages orphelines et la cannibalisation, puis propose les liens. |
| `/seo-refresh` | Met à jour un article publié : chiffres datés, manques face à la SERP, liens, modifications à accepter. |
| `/seo-veille` | Nouvelles pages des concurrents (sitemaps) et rapport mensuel Search Console. |
| `/seo-programmatic` | Pages à grande échelle sans pages satellites. |
| `/seo-local` | Fiche Google, avis dans le respect du droit français, pages locales, annuaires français. |
| `/seo-social` | SEO de YouTube, Pinterest, TikTok, LinkedIn et Google Discover. |

## Installer

Claude Code :

```
/plugin marketplace add Aleksander-Siebert/join-medicis-ressources
/plugin install seo-skills@join-medicis
```

claude.ai et Claude Desktop : activez l'exécution de code (Réglages →
Capacités), puis importez `seo-skills.zip` dans Personnaliser → Skills. Le
pack entier s'installe comme un seul Skill. Le ZIP se télécharge sur
[la fiche Join Médicis](https://joinmedicis.com/ressources/skills/seo-skills)
ou se construit avec `claude-ai/build.sh seo-skills.zip`.

ChatGPT, Gemini, Mistral : collez le `SKILL.md` voulu dans un Projet, un GPT,
un Gem ou un Skill Vibe. Tout marche, sauf les scripts : les Skills font alors
les mêmes contrôles à la lecture.

Ensuite, lancez `/seo-context` avec l'URL de votre site.

## Les scripts

Cinq scripts Python sans dépendance, qui tournent sur votre machine :

```bash
python3 skills/seo-maillage/maillage.py --sitemap https://www.site.fr/sitemap.xml --lire --max 300
python3 skills/seo-audit/onpage.py https://www.site.fr/page/ --mot-cle "mot clé" --poids-images --cwv
python3 skills/seo-drift/drift.py photo --sitemap https://www.site.fr/sitemap.xml --max 50
python3 skills/seo-veille/veille.py rapport pages-octobre.csv pages-septembre.csv
python3 skills/seo-human/humanize.py article.md --profil article --affirmatif --rapport
```

Le maillage rapproche les pages par leur vocabulaire (TF-IDF, sans clé
d'API) et note chaque lien possible : 0,7 × proximité + 0,3 × trafic de la
page hôte. Claude relit chaque proposition, vous validez.

`--cwv` lit les Core Web Vitals avec l'API PageSpeed Insights : créez une
clé gratuite dans Google Cloud et passez-la avec `--cle` ou `PSI_API_KEY`.

## Tests

```bash
python3 evals/seo-human/test_humaniseur.py   # 21 tests
python3 evals/seo-human/test_article.py      # 9 tests
python3 evals/scripts/test_scripts.py        # 11 tests
```

## Licence

MIT. Les mentions des projets d'origine sont dans [LICENSE](LICENSE).
