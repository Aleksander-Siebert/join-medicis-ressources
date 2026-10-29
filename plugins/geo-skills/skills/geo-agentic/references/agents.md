# Les agents d'IA : ce qu'ils lisent, ce qu'ils respectent

Faits qui bougent vite. Chaque ligne porte sa source et son niveau :
**P** = source primaire (documentation de l'éditeur, spécification, code
source), **S** = source secondaire seulement. Sauf mention, les lignes
viennent de la matrice de `seo-agentic` (claude-seo, MIT), **vérifiée par
son auteur le 23 septembre 2026**, traduite et resserrée ; nous n'avons
revérifié que les lignes marquées « revérifié le 16 oct. 2026 ». À revoir
quand la date a plus de 60 jours.

## 1. Les agents

| Éditeur, produit | Ce qu'il lit | WebMCP | Identité, robots.txt | Niveau |
|---|---|---|---|---|
| OpenAI, navigateur intégré de ChatGPT (bureau) | arbre d'accessibilité (FAQ éditeurs) | oui, outils déclarés en JavaScript seulement | ChatGPT-User, « peut ne pas s'appliquer » ; signature Web Bot Auth | P |
| Google, Gemini dans Chrome | éléments de la page et positions à l'écran | aucune preuve d'usage ; Google coécrit la spécification | **Google-Agent**, robot déclenché par un utilisateur, ignore en général robots.txt ; Web Bot Auth en essai (`https://agent.bot.goog`) | P (identité, revérifié le 16 oct. 2026), S (lecture) |
| Microsoft, Edge et Copilot | non documenté | Edge le prend en charge pour les tests ; aucun usage connu par Copilot | non étudié | P (Edge), S |
| Anthropic, Claude dans Chrome | texte, DOM, console et réseau, captures | aucun | ClaudeBot, Claude-SearchBot, Claude-User, tous respectent robots.txt | P (robots), S (lecture) |
| Perplexity, Comet | arbre d'accessibilité et captures | aucun signal public | PerplexityBot respecte robots.txt, Perplexity-User en général non | P (robots), S (lecture) |
| Apple, Safari | sans objet | **s'y oppose** (un agent est plus proche d'une aide technique ; un site ne devrait pas le détecter) | sans objet | P (position), S |
| Mozilla, Firefox | sans objet | neutre, pas d'implémentation | sans objet | P |

À dire sans détour dans un rapport :

- aucune source primaire ne montre un agent grand public qui demande
  `Accept: text/markdown` ;
- le comportement envers robots.txt des actions d'agents de Dia, Opera et
  Comet n'est pas vérifié ;
- aucune étude contrôlée publique ne relie la qualité de l'arbre
  d'accessibilité ou WebMCP au succès des tâches d'un agent : ce sont des
  hypothèses raisonnables, pas des résultats.

État des produits rapporté (S, à revérifier avant de le citer) : le
navigateur ChatGPT Atlas et « ChatGPT agent » arrêtés début août 2026 ;
Project Mariner arrêté en mai 2026.

## 2. Lighthouse, catégorie Agentic Browsing

D'après le code de Lighthouse 13.5.0 (P, vérifié par claude-seo le
23 sept. 2026 ; la catégorie est « en développement ») :

| Audit | Ce qu'il mesure | Notre script |
|---|---|---|
| `agent-accessibility-tree` | 33 règles axe (noms des boutons, liens, champs, `aria-hidden-focus`, `tabindex`…) ; contraste, ordre des titres et repères **non** inclus | en partie : noms, labels, interactifs cachés, cliquables non sémantiques |
| `cumulative-layout-shift` | CLS mesuré en laboratoire | en partie : images sans dimensions |
| `llms-txt` | `/llms.txt` : un H1, un lien Markdown, 50 caractères ; 4xx = sans objet | rapporté, sans poids |
| `webmcp-form-coverage`, `webmcp-registered-tools`, `webmcp-schema-validity` | formulaires déclarés (`toolname`, `tooldescription`), outils, validité ; sans objet sans WebMCP | rapporté |
| `ard-schema` | catalogue `ai-catalog.json` s'il est signalé | non |

Lancer : PageSpeed Insights (API v5, `category=AGENTIC_BROWSING`), ou
`npx lighthouse@latest <url> --only-categories=agentic-browsing`, ou le
panneau Lighthouse de Chrome. Résultat en fraction, comme notre script.

## 3. WebMCP

Proposition de standard (dépôt `webmachinelearning/webmcp`) : un site
déclare des « outils » qu'un agent du navigateur peut appeler, soit sur un
formulaire (`toolname`, `tooldescription`), soit en JavaScript
(`navigator.modelContext`). Essai d'origine dans Chrome, versions 149 à 156
(P pour la plage), sans date de sortie annoncée. Ne le proposer que sur un
vrai formulaire, sans promesse d'usage.

## 4. Mettre à jour cette page

1. Robots : pages d'OpenAI, Anthropic, Perplexity, Mistral, Google
   (« user-triggered fetchers »), Apple ; reporter dans
   `commun/robots_ia.json` et `commun/preuves.md` avec la date.
2. Lighthouse : `npm view lighthouse version`, puis la liste des audits de
   la catégorie dans `core/config/default-config.js`.
3. WebMCP : dernier commit de la spécification, page chromestatus.
4. Agents : pages d'aide de chaque produit ; une ligne sans source
   primaire reste en S.
