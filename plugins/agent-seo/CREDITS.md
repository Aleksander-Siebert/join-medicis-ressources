# Méthode et crédits

L'agent est une création Join Médicis. L'écriture repose sur le pack SEO
Join Médicis (`/seo-article` et ses Skills voisins), dont les crédits sont
dans `plugins/seo-skills/CREDITS.md` du dépôt Join Médicis.

Pour la couche agent, nous avons lu le 16 novembre 2026 les dépôts et
articles suivants. Aucun texte ni code n'a été recopié. Matrice complète :
`recherche/agent-seo/MATRICE.md` du dépôt Join Médicis.

- [seo-agent-kit](https://github.com/kevinbadi/seo-agent-kit), KevBuildsApps
  (MIT) :
  - les sujets trouvés dans les requêtes Search Console en page 2 ;
  - une intention par article ;
  - la fiche « vérité produit » contrôlée par script avant toute relecture.

  Nous avons écarté sa publication automatique.
- [groundskeeper](https://github.com/samynym/groundskeeper), samynym (MIT) :
  aucune affirmation sans source connue, et la relecture faite sur un
  tableau « affirmation → source ».
- [claude-blog](https://github.com/AgriciDaniel/claude-blog), AgriciDaniel
  (MIT) : la vérification d'une citation en ouvrant la source.
- [SEO Skill](https://github.com/iannuttall/seo) (seoskill.dev), Ian Nuttall
  (Apache 2.0) : le connecteur Search Console utilisé par défaut. Il n'est
  pas copié ici, l'agent s'y connecte.
- [NotFair Plugin](https://github.com/nowork-studio/notfair-plugin),
  nowork-studio (MIT) : rien n'est publié sans un oui explicite.
- Dust, « How I Use AI Agents to Run a More Structured SEO Workflow »
  (Davis Christenhuis, 17 juin 2026) : la chaîne d'agents spécialisés, le
  tableau de sujets daté, le contrôle de pertinence avant d'écrire.
- Ahrefs, « Les agents SEO IA » (Louise Linehan) : commencer par un seul
  workflow, des Skills séparés, un fichier mémoire.

Écartés : la publication automatique, les sous-agents rédacteur et relecteur
(coût sans gain mesuré), les connecteurs hébergés aux coûts de données non
précisés.
