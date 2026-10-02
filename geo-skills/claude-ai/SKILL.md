---
name: geo-skills
description: >-
  Pack AEO / GEO en français, en un seul Skill : être lu, compris et cité par
  ChatGPT, Perplexity, Gemini, Claude, Mistral et les AI Overviews de Google,
  et utilisable par les agents d'IA. Audit GEO sur 100, citabilité des
  passages, robots d'IA et llms.txt, test de visibilité de la marque dans les
  réponses, données structurées JSON-LD, mentions de marque, préparation aux
  agents, plan d'optimisation. Utilise-le pour toute demande GEO, AEO ou
  « visibilité dans les IA ».
---

# GEO Skills (Join Médicis)

Ce Skill regroupe les 8 modules du pack AEO / GEO. Chaque module est un mode
d'emploi complet rangé dans `modules/<nom>/<nom>.md`, avec ses fichiers
(références, scripts) dans le même dossier.

## Choisir le module

| Module | Quand l'utiliser |
|---|---|
| `geo-audit` | audit GEO d'une page ou d'un site, score sur 100 |
| `geo-citability` | rendre des passages citables, réécrire les sections faibles |
| `geo-crawlers` | robots d'IA, robots.txt, llms.txt, bloquer ou autoriser |
| `geo-visibility` | la marque est-elle citée par les IA ? part de voix |
| `geo-schema` | données structurées JSON-LD, entité de marque |
| `geo-mentions` | présence de la marque sur les sources que lisent les IA |
| `geo-agentic` | agents d'IA qui naviguent et remplissent des formulaires, WebMCP |
| `geo-optimize` | stratégie GEO complète, plan sur 90 jours |

L'utilisateur peut taper le nom du module comme une commande
(`/geo-audit …`).

## Comment travailler

1. Choisis le module. Une demande générale (« optimiser pour les IA ») →
   `geo-optimize`, qui enchaîne les autres.
2. **Lis en entier `modules/<nom>/<nom>.md`** avant de répondre, puis
   suis-le. Les fichiers qu'il cite (`references/…`, `geo_audit.py`,
   `citability.py`, `crawlers.py`, `visibilite.py`, `agentic.py`) sont dans son
   dossier.
   `geo_audit.py` et `agentic.py` importent leurs voisins (`citability.py`,
   `crawlers.py`) depuis les dossiers du pack.
3. Les modèles `site-context.md`, `exemple-site-context.md` et
   `apprentissages.md` sont dans `templates/` (communs avec le pack SEO).

## Règles communes

- Lis `site-context.md` et `apprentissages.md` de l'utilisateur s'ils sont
  fournis.
- Zéro invention : aucun score, aucune citation, aucune réponse d'IA simulée ;
  « à évaluer » ou `{{à compléter}}` sinon.
- Réponds en texte simple dans la conversation, sans créer de document.
- Rien n'est publié ni modifié sur le site à la place de l'utilisateur.

Pack open-source (MIT) : https://github.com/Aleksander-Siebert/join-medicis-ressources
