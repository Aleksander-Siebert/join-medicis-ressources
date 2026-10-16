<div align="center">

<img src="docs/media/banniere.svg" width="100%" alt="SEO Skills, par Join Médicis : quatorze Skills SEO en français, du mot-clé à l'article publié">

<br>

**Quatorze Skills SEO en français pour Claude, ChatGPT, Gemini et Mistral.**<br>
Du mot-clé à l'article publiable, de l'audit au maillage interne. **Aucun chiffre inventé** : ce qui manque devient `{{à compléter}}`.

<!-- github-seulement -->
[![Version](https://img.shields.io/badge/version-2.0.0-0E3F2D)](#versions)
[![Tests](https://img.shields.io/badge/tests-240%20au%20vert-2D7259)](#preuves)
[![Licence MIT](https://img.shields.io/badge/licence-MIT-B89253)](LICENSE)
[![Python](https://img.shields.io/badge/Python%203-sans%20d%C3%A9pendance-34495E?logo=python&logoColor=white)](#les-scripts)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-D97757?logo=claude&logoColor=white)](#claude-code)
[![claude.ai](https://img.shields.io/badge/claude.ai-ZIP%20importable-D97757)](#claudeai-et-claude-desktop)
[![Autres IA](https://img.shields.io/badge/ChatGPT%20%C2%B7%20Gemini%20%C2%B7%20Mistral-compatibles-525049)](#chatgpt-gemini-mistral)
[![Étoiles GitHub](https://img.shields.io/github/stars/Aleksander-Siebert/join-medicis-ressources?style=social)](https://github.com/Aleksander-Siebert/join-medicis-ressources)

[**Installer**](#installer) · [Les quatorze Skills](#les-quatorze-skills) · [En images](#en-images) · [Fiche Join Médicis](https://joinmedicis.com/ressources/skills/seo-skills) · [Crédits](CREDITS.md)
<!-- /github-seulement -->

<!-- Emplacement du GIF de démonstration (voir docs/media/A-FILMER.md, prise 1).
     Quand il existe, remplace l'image ci-dessous par :
     <img src="docs/media/demo.gif" width="760" alt="Un mot-clé devient un plan validé puis un article contrôlé"> -->
<img src="docs/media/capture-controle.svg" width="760" alt="Sortie réelle de controle.py : un article écrit par une IA, ses défauts classés par priorité, chacun avec sa correction">

<sub>Sortie réelle du contrôle de rédaction sur un article de test : chaque défaut classé par priorité, avec sa correction.</sub>

</div>

---

## Pourquoi

Les Skills SEO en circulation produisent vite des articles qui se
ressemblent : plan copié sur les concurrents, chiffres sans source, « dans
cet article, nous allons voir », conclusion de remplissage. En santé, en
assurance ou en finance, un chiffre inventé n'est pas un détail : c'est un
risque.

**Ce pack travaille comme un rédacteur SEO exigeant.** Il lit votre contexte
(`site-context.md`), la SERP et vos données, fait valider le plan avant la
moindre phrase, mesure ce qui se mesure (couverture des requêtes, largeur du
title en pixels, affirmations sans source) et ne publie jamais rien. Pas
besoin d'outil payant ; si Search Console, Semrush ou Ahrefs sont connectés à
votre IA, les Skills s'en servent.

## Les quatorze Skills

### Stratégie

<table>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-plan.svg" width="44" alt=""></td>
<td><b><code>/seo-plan</code></b> <sup>v2</sup><br>La stratégie sur 12 mois : piliers, feuille de route en 4 phases, idées classées par script, indicateurs partant de vos vraies données. Option pages en série contrôlées, options 2026 au choix.</td>
<td width="150"><code>priorite.py</code></td>
</tr>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-context.svg" width="44" alt=""></td>
<td><b><code>/seo-context</code></b> <sup>v2</sup><br>Remplit <code>site-context.md</code> une question à la fois : secteur, lecteurs, pages à pousser, ton, règles maison, données produit étiquetées. Tous les autres le lisent.</td>
<td width="150"></td>
</tr>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-keywords.svg" width="44" alt=""></td>
<td><b><code>/seo-keywords</code></b> <sup>v2</sup><br>Mots-clés et intentions, regroupés en pages (une intention, une page) par recouvrement de SERP, cannibalisation lue dans l'export Search Console.</td>
<td width="150"><code>motscles.py</code></td>
</tr>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-serp.svg" width="44" alt=""></td>
<td><b><code>/seo-serp</code></b> <sup>v2</sup><br>Lit la SERP : type de page qui gagne (consensus mesuré), difficulté lue dans les résultats, signaux « ne pas tenter », manques, gain d'information.</td>
<td width="150"><code>serp.py</code></td>
</tr>
</table>

### Écrire

<table>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-brief.svg" width="44" alt=""></td>
<td><b><code>/seo-brief</code></b> <sup>v2</sup><br>Le plan validable avant toute rédaction : six questions une à une, cadre PAS, AIDA, MECE ou pyramide inversée, title et H1 à H3 commentés, couverture de 20 à 30 vraies requêtes mesurée par script, grille face aux concurrents.</td>
<td width="150"><code>couverture.py</code> <code>meta.py</code></td>
</tr>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-write.svg" width="44" alt=""></td>
<td><b><code>/seo-write</code></b> <sup>v2</sup><br>Rédige sur le plan validé : résumé de 3 lignes en tête, réponse directe sous chaque H2, voix active, chaque affirmation chiffrée vérifiée contre ses sources, bloc méta mesuré en pixels.</td>
<td width="150"><code>controle.py</code> <code>affirmations.py</code></td>
</tr>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-article.svg" width="44" alt=""></td>
<td><b><code>/seo-article</code></b> <sup>v2</sup><br>Le chemin complet, du mot-clé à l'article, en étapes validées une à une et rejouables, puis un portail qualité qui bloque au lieu de faire une moyenne : une affirmation sans source en YMYL arrête la livraison. Mode autonome avec hypothèses écrites.</td>
<td width="150"><code>pipeline.py</code></td>
</tr>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-human.svg" width="44" alt=""></td>
<td><b><code>/seo-human</code></b> <sup>v2</sup><br>Retire les marques d'écriture IA d'un article sans casser son Markdown ni la typographie française.</td>
<td width="150"><code>humanize.py</code> <code>detect.py</code></td>
</tr>
</table>

### Contrôler

<table>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-audit.svg" width="44" alt=""></td>
<td><b><code>/seo-audit</code></b> <sup>v2</sup><br>Audit par ordre de priorité : robots.txt robot par robot (RFC 9309), title en pixels, JSON-LD à vérifier rendu, type de page, et la photo avant / après d'une mise en ligne.</td>
<td width="150"><code>onpage.py</code> <code>robots.py</code> <code>drift.py</code></td>
</tr>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-maillage.svg" width="44" alt=""></td>
<td><b><code>/seo-maillage</code></b> <sup>v2</sup><br>Clusters depuis le sitemap, pages du cœur au lointain, orphelines, cannibalisation, ancres répétées, puis liens proposés un par un.</td>
<td width="150"><code>maillage.py</code></td>
</tr>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-veille.svg" width="44" alt=""></td>
<td><b><code>/seo-veille</code></b> <sup>v2</sup><br>Nouvelles pages des concurrents et rapport mensuel Search Console, avec les événements de la période présentés comme des hypothèses.</td>
<td width="150"><code>veille.py</code></td>
</tr>
</table>

### Durer et étendre

<table>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-refresh.svg" width="44" alt=""></td>
<td><b><code>/seo-refresh</code></b> <sup>v2</sup><br>Quelles pages mettre à jour d'abord (trois paniers Search Console, CTR comparé au site lui-même), le plus petit changement, puis le bilan à 21 jours.</td>
<td width="150"><code>positions.py</code></td>
</tr>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-local.svg" width="44" alt=""></td>
<td><b><code>/seo-local</code></b> <sup>v2</sup><br>Fiche Google, fiches en double, avis dans le droit français, pages locales sans pages satellites, NAP comparé entre site, fiche et annuaires.</td>
<td width="150"><code>nap.py</code></td>
</tr>
<tr>
<td width="64" align="center"><img src="docs/media/icones/seo-social.svg" width="44" alt=""></td>
<td><b><code>/seo-social</code></b> <sup>v2</sup><br>SEO de YouTube, Pinterest, TikTok, LinkedIn et Discover ; chapitres et texte d'une vidéo contrôlés selon les règles de YouTube.</td>
<td width="150"><code>video.py</code></td>
</tr>
</table>

<sup>v2</sup> : réécrits en octobre 2026 sur le socle commun (règles, preuves datées, scripts de contrôle).

## En images

Sorties réelles des scripts, sur les fichiers de test du pack. Elles sont
régénérées à chaque version (`outils/visuels/capture.py`) : si un script
change, l'image change avec lui.

<p align="center"><img src="docs/media/capture-affirmations.svg" width="820" alt="affirmations.py en mode YMYL : 5 affirmations sans source, publication bloquée"><br>
<sub><b>/seo-write</b> · en santé, assurance ou finance, une affirmation sans source bloque la publication.</sub></p>

<p align="center"><img src="docs/media/capture-couverture.svg" width="820" alt="couverture.py : 24 requêtes réelles, toutes rattachées à une section du plan"><br>
<sub><b>/seo-brief</b> · chaque vraie requête rattachée à une section du plan, avant d'écrire.</sub></p>

<details>
<summary><b>Deux autres captures</b> : le title en pixels, le rapport Search Console</summary>
<br>
<p align="center"><img src="docs/media/capture-meta.svg" width="820" alt="meta.py : title de 490 px, description coupée sur mobile"><br>
<sub><b>/seo-brief</b> · le title et la description mesurés en pixels, pas en caractères.</sub></p>

<p align="center"><img src="docs/media/capture-veille.svg" width="820" alt="veille.py : clics du mois contre le mois précédent, pages gagnantes et perdantes"><br>
<sub><b>/seo-veille</b> · le rapport mensuel à partir de deux exports Search Console.</sub></p>
</details>

<!-- Emplacement d'un GIF (voir docs/media/A-FILMER.md, prise 2) :
     <img src="docs/media/demo-maillage.gif" width="760" alt="Le sitemap d'un site devient des clusters et des liens à ajouter"> -->

## Installer

### Claude Code

```
/plugin marketplace add Aleksander-Siebert/join-medicis-ressources
/plugin install seo-skills@join-medicis
```

### claude.ai et Claude Desktop

1. Réglages → Capacités : activez l'exécution de code (pour les scripts).
2. Personnaliser → Skills → importez **`seo-skills.zip`**, téléchargé depuis
   [la fiche Join Médicis](https://joinmedicis.com/ressources/skills/seo-skills).
   Le pack entier s'installe comme un seul Skill.
3. Mettez votre `site-context.md` dans les connaissances d'un Projet.

<details>
<summary>Construire le ZIP soi-même</summary>

`claude-ai/build.sh seo-skills.zip` construit le ZIP du pack. claude.ai
refuse un ZIP qui contient plusieurs `SKILL.md` ou le manifeste de plugin :
n'importez pas le dépôt tel quel.

</details>

### ChatGPT, Gemini, Mistral

Collez le `SKILL.md` voulu dans un Projet, un GPT, un Gem ou un agent. Tout
marche, sauf les scripts : les Skills font alors les mêmes contrôles à la
lecture, et le disent.

**Ensuite** : lancez `/seo-context` avec l'URL de votre site. Le pack GEO
partage le même `site-context.md`.

## Les scripts

Python 3, sans dépendance, sur votre machine :

```bash
python3 skills/seo-maillage/scripts/maillage.py --sitemap https://www.site.fr/sitemap.xml --lire --max 300
python3 skills/seo-audit/scripts/onpage.py https://www.site.fr/page/ --mot-cle "mot clé" --poids-images --cwv
python3 skills/seo-audit/scripts/drift.py photo --sitemap https://www.site.fr/sitemap.xml --max 50
python3 skills/seo-veille/scripts/veille.py rapport pages-octobre.csv pages-septembre.csv
python3 skills/seo-audit/scripts/robots.py https://www.site.fr --chemin /blog/
python3 skills/seo-refresh/scripts/positions.py paniers gsc-requetes-pages.csv
python3 skills/seo-local/scripts/nap.py --source site=page.html --source fiche=fiche.txt
python3 skills/seo-social/scripts/video.py --description description.txt --duree 12:40
python3 skills/seo-plan/scripts/priorite.py idees idees.csv
python3 skills/seo-article/scripts/pipeline.py etat --dossier articles/mon-article/
python3 skills/seo-brief/scripts/couverture.py couvrir plan.md requetes.txt
python3 skills/seo-write/scripts/controle.py article.md --affirmatif
python3 commun/affirmations.py article.md --ymyl
python3 commun/meta.py --title "…" --description "…"
```

<details>
<summary>Comment le maillage note les liens, et la clé PageSpeed</summary>

Le maillage rapproche les pages par leur vocabulaire (TF-IDF, sans clé
d'API) et note chaque lien possible : 0,7 × proximité + 0,3 × trafic de la
page hôte. Claude relit chaque proposition, vous validez.

`--cwv` lit les Core Web Vitals avec l'API PageSpeed Insights : créez une
clé gratuite dans Google Cloud et passez-la avec `--cle` ou `PSI_API_KEY`.

</details>

## Ce qui tient le pack

<table>
<tr>
<td width="56" valign="top"><img src="docs/media/icones/pilier-garde-fou.svg" width="44" alt=""></td>
<td><b>Un garde-fou et des preuves datées.</b> Le socle commun refuse le contenu copié, les fausses preuves, les liens artificiels, les pages en masse et la fausse fraîcheur ; il encadre les comparatifs nommés, les avis clients et les sujets YMYL. Ce qu'on sait de Google est classé officiel, étude, praticien ou folklore, avec sa source et sa date (<a href="commun/preuves.md"><code>commun/preuves.md</code></a>).</td>
</tr>
<tr>
<td width="56" valign="top"><img src="docs/media/icones/pilier-mesure.svg" width="44" alt=""></td>
<td><b>La mesure séparée du jugement.</b> Les scripts mesurent la couverture, les pixels, les affirmations sans source ; Claude écrit et explique. Une donnée sans source ne sort jamais comme un fait.</td>
</tr>
<tr>
<td width="56" valign="top"><img src="docs/media/icones/pilier-sortie.svg" width="44" alt=""></td>
<td><b>Une validation à chaque étape.</b> Le plan est validé avant la rédaction, chaque modification d'un article publié est acceptée une par une. Rien n'est publié à votre place.</td>
</tr>
</table>

## Preuves

```bash
python3 evals/tout_tester.py
```

**240 tests** : les scripts, le socle commun et l'intégrité du pack (frontmatter,
fichiers cités, socle synchronisé, typographie). Les évaluations comparatives
sont dans [`evals/RESULTATS.md`](evals/RESULTATS.md).

## Versions

| Version | Date | Ce qui change |
|---|---|---|
| **2.0.0** | 16 oct. 2026 | Les 14 Skills réécrits sur un socle commun (règles, preuves datées, garde-fou, mesures en pixels, affirmations). `/seo-drift` entre dans `/seo-audit`, `/seo-programmatic` devient une option de `/seo-plan`. Nouveaux scripts : `pipeline.py`, `robots.py`, `positions.py`, `nap.py`, `video.py`, `priorite.py`. |
| 1.1.0 | 2 oct. 2026 | Corrections d'après les guides Google, `/seo-drift`, `/seo-plan`. |
| 1.0.0 | 2 oct. 2026 | 14 Skills en français, 4 scripts, tests. |

## Crédits et licence

MIT. Le pack est né de l'analyse des Skills SEO les plus utilisés, réécrits
pour le français : la liste est dans [CREDITS.md](CREDITS.md), les mentions
de licence dans [LICENSE](LICENSE).

<div align="center">
<br>
<sub>Un pack <a href="https://joinmedicis.com">Join Médicis</a>, la bibliothèque IA gratuite des marketeurs francophones.</sub>
</div>
