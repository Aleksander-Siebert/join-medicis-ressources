---
name: seo-skills
description: >-
  Pack SEO en français, en un seul Skill : contexte du site, recherche de
  mots-clés, analyse de SERP et concurrents, brief selon le framework (PAS,
  AIDA, MECE, pyramide inversée), rédaction YMYL sans invention, article
  complet de bout en bout, humanisation, audit SEO, maillage interne et
  clusters depuis le sitemap, mise à jour d'articles, veille concurrents et
  rapport Search Console, SEO programmatique, SEO local et SEO des réseaux
  sociaux (YouTube, Pinterest, TikTok). Utilise-le pour toute demande SEO.
---

# SEO Skills (Join Médicis)

Ce Skill regroupe les 14 modules du pack SEO. Chaque module est un mode
d'emploi complet rangé dans `modules/<nom>/<nom>.md`, avec ses fichiers
(références, scripts) dans le même dossier.

## Choisir le module

| Module | Quand l'utiliser |
|---|---|
| `seo-context` | premier usage, « voici mon site », remplir `site-context.md` |
| `seo-keywords` | mots-clés, intentions, idées d'articles, cannibalisation |
| `seo-serp` | analyser la SERP et les concurrents d'une requête |
| `seo-brief` | plan validable d'une page (framework, H1-H3, liens) |
| `seo-write` | rédiger une page ou un article depuis un plan validé |
| `seo-article` | tout le chemin, du mot-clé à l'article, avec validations |
| `seo-human` | humaniser un texte, « ça fait IA ? » |
| `seo-audit` | audit SEO d'une page ou d'un site, baisse de trafic |
| `seo-maillage` | sitemap, clusters, pages orphelines, liens internes |
| `seo-refresh` | mettre à jour un article publié |
| `seo-veille` | nouvelles pages des concurrents, rapport Search Console |
| `seo-programmatic` | pages à grande échelle (villes, comparatifs, glossaire) |
| `seo-local` | fiche Google, avis, pages locales, annuaires |
| `seo-social` | SEO YouTube, Pinterest, TikTok, LinkedIn, Discover |

L'utilisateur peut taper le nom du module comme une commande (`/seo-brief …`).

## Comment travailler

1. Choisis le module. Une demande d'article complet → `seo-article`, qui
   enchaîne les autres.
2. **Lis en entier `modules/<nom>/<nom>.md`** avant de répondre, puis
   suis-le. Les fichiers qu'il cite (`references/…`, `humanize.py`,
   `maillage.py`, `onpage.py`, `veille.py`) sont dans son dossier.
3. Quand un module renvoie à un autre (« passe par `/seo-human` »), lis le
   fichier de ce module et applique-le.
4. Les modèles `site-context.md`, `exemple-site-context.md` et
   `apprentissages.md` sont dans `templates/`. Sur claude.ai, propose de
   garder `site-context.md` rempli dans les connaissances du Projet.

## Règles communes

- Lis `site-context.md` et `apprentissages.md` de l'utilisateur s'ils sont
  fournis.
- Zéro invention : aucun chiffre, prix, délai, condition ou source inventé ;
  écris `{{à compléter}}`. Strict en YMYL.
- Réponds en texte simple dans la conversation, sans créer de document.
- Données : connecteur (Search Console, Semrush, Ahrefs) s'il est là, sinon
  recherche web ou export collé. Dis d'où vient chaque chiffre.
- Rien n'est publié ni modifié sur le site à la place de l'utilisateur.

Pack open-source (MIT) : https://github.com/Aleksander-Siebert/join-medicis-ressources
