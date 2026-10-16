---
name: geo-skills
description: >-
  Pack GEO / AEO en français, en un seul Skill : être lu, compris et cité
  par ChatGPT, Perplexity, Gemini, Claude, Mistral et Google (Aperçus IA,
  Mode IA). Audit couche par couche avec note de préparation détaillée,
  visibilité de la marque mesurée avec sa marge d'erreur, robots d'IA lus
  selon leur rôle (GPTBot n'est pas OAI-SearchBot), exactitude de ce que les
  IA disent de la marque, contenu, entité et JSON-LD, sites tiers qui font
  les listes, agents d'IA et consignes cachées. Utilise-le pour toute
  demande GEO, AEO, « visibilité dans les IA », « ChatGPT me cite-t-il »,
  « robots IA », « llms.txt ». Pas pour le SEO classique seul (pack SEO).
  Ne simule jamais une réponse d'IA.
---

# GEO Skills (Join Médicis)

Ce Skill regroupe les 8 modules du pack GEO. Chaque module est un mode
d'emploi complet rangé dans `modules/<nom>/<nom>.md`, avec ses fichiers
(`references/`, `scripts/`, `commun/`) dans le même dossier.

## Choisir le module

| Module | Quand l'utiliser |
|---|---|
| `geo-audit` | « audit GEO », « par où commencer » : diagnostic couche par couche, note de préparation, couche à traiter d'abord |
| `geo-visibilite` | « ChatGPT me recommande-t-il », part de voix, suivi dans le temps : taux avec marge d'erreur, moteur par moteur |
| `geo-acces` | robots d'IA, robots.txt, « bloquer les IA », « pourquoi ChatGPT ne voit pas mon site », llms.txt |
| `geo-exactitude` | « l'IA dit n'importe quoi sur nous », mauvais prix, offre périmée |
| `geo-contenu` | rendre une page claire et citable, réécrire section par section |
| `geo-entite` | JSON-LD, schema, entité de marque, sameAs, Wikidata, confusion avec une autre société |
| `geo-mentions` | sources que citent les IA, comparateurs, presse, Reddit, notoriété |
| `geo-agentic` | agents d'IA, formulaires, WebMCP, texte caché pour les IA |

L'utilisateur peut taper le nom du module comme une commande
(`/geo-audit …`). Une demande générale (« optimiser pour les IA ») →
`geo-audit`, puis le module de la couche à traiter d'abord.

## Comment travailler

1. Choisis le module.
2. **Lis en entier `modules/<nom>/<nom>.md`** avant de répondre, puis
   suis-le. Les fichiers qu'il cite sont dans son dossier :
   `modules/<nom>/scripts/…`, `modules/<nom>/references/…`,
   `modules/<nom>/commun/…`.
3. `geo-audit` lance les scripts des autres modules depuis
   `modules/<autre>/scripts/` : garde le dossier `modules/` entier.
4. Sans exécution de code, chaque module dit comment faire les contrôles à
   la lecture ; écris alors « lecture manuelle ».
5. Les modèles `site-context.md`, `exemple-site-context.md` et
   `apprentissages.md` sont dans `templates/` (communs avec le pack SEO).

## Règles communes

- Lis `site-context.md` et `apprentissages.md` de l'utilisateur s'ils sont
  fournis.
- Zéro invention : aucune réponse d'IA simulée, aucun chiffre, aucune
  source ; « non mesuré » ou `{{à compléter}}` sinon.
- Réponds en texte simple dans la conversation, sans créer de document.
- Rien n'est publié ni modifié sur le site à la place de l'utilisateur.

Pack open-source (MIT) : https://github.com/Aleksander-Siebert/join-medicis-ressources
