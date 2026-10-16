# Faits vérifiés aux sources primaires (16 octobre 2026)

Chaque ligne : le fait, la source lue, sa date. Ce qui n'a pas pu être lu
à la source reste **[à vérifier]**.

## Robots et jetons

| Robot | Éditeur | Rôle | robots.txt | Source |
|---|---|---|---|---|
| OAI-SearchBot | OpenAI | index de la recherche ChatGPT ; bloqué = absent des réponses de recherche (peut rester en lien de navigation) ; prise en compte en 24 h environ | oui | developers.openai.com/api/docs/bots (lu le 16 oct. 2026, non daté) |
| GPTBot | OpenAI | entraînement des modèles fondamentaux | oui | idem |
| ChatGPT-User | OpenAI | visite demandée par un utilisateur, pas un robot automatique | « peut ne pas s'appliquer » | idem |
| OAI-AdsBot | OpenAI | conformité des pages de destination des annonces ChatGPT, pas d'entraînement | non précisé | idem |
| ClaudeBot | Anthropic | entraînement | oui, Crawl-delay accepté | support.claude.com, article du 7 avr. 2026 |
| Claude-SearchBot | Anthropic | index de recherche ; bloqué = moins de visibilité dans les résultats | oui | idem |
| Claude-User | Anthropic | visite pour une question d'utilisateur ; bloqué = contenu non récupéré | oui | idem |
| PerplexityBot | Perplexity | résultats de recherche, pas d'entraînement | oui | docs.perplexity.ai/guides/bots (non daté) |
| Perplexity-User | Perplexity | visite pour une question d'utilisateur | « ignore généralement » | idem |
| **MistralAI-User** | Mistral | action d'un utilisateur dans Vibe, pas d'exploration ni d'entraînement | soumis à des règles non détaillées | docs.mistral.ai/robots (non daté) |
| **MistralAI-Index** | Mistral | **indexation pour la recherche de Vibe**, pas d'entraînement | non précisé | idem |
| **MistralAI-Training** | Mistral | entraînement | excluable par robots.txt | idem |
| Google-Extended | Google | **jeton sans robot propre** : entraînement des futurs Gemini, et ancrage (grounding) dans les applis Gemini et Vertex AI ; **n'affecte ni l'inclusion dans Search ni le classement** | oui | developers.google.com, « Google common crawlers », maj. 15 oct. 2026 |
| Applebot-Extended | Apple | **ne crawle pas** ; refuse l'usage des données d'Applebot pour entraîner les modèles d'Apple ; sans effet sur Spotlight, Siri, Safari ni le classement | oui | support.apple.com/119829, 4 sept. 2026 |
| Applebot | Apple | recherche Spotlight, Siri, Safari ; aussi entraînement et contexte de réponses générées ; `nosnippet` refuse l'usage dans les réponses | oui | idem |

**Corrections pour notre v1** : Mistral a trois robots (v1 n'en a qu'un) ;
Applebot (pas seulement Applebot-Extended) sert aussi aux réponses
générées ; Google-Extended couvre l'ancrage Gemini.

## Google

- **Guide « AI optimization »** (Search Central, maj. 10 juil. 2026) :
  - **Éligibilité** : page indexée et éligible à un extrait dans
    Google Search, **et** site inclus via le réglage Search Console.
  - **Inutile** :
    - llms.txt, fichiers texte pour IA, Markdown (« Google Search ne
      les utilise pas ») ;
    - découper le contenu (« pas de longueur de page idéale ») ;
    - réécrire pour l'IA ;
    - chercher des mentions non authentiques ;
    - données structurées spéciales (pas requises, aucun schema
      propre à l'IA).
  - **Ce qui compte** :
    - contenu original et non générique, fait par des personnes
      compétentes ;
    - exploration possible, HTML sémantique, JavaScript bien conçu ;
    - images et vidéos ;
    - fiches Business Profile et Merchant Center à jour.
  - **Mesure** : rapport de performance « IA générative » dans Search
    Console.
  - Méfiance envers les outils qui promettent un classement.
  - **Agents** : renvoi aux bonnes pratiques web.dev, UCP en cours.
- **Réglage « Contrôle de l'IA générative dans la Recherche »** (Search
  Console, Paramètres) : inclure (par défaut), exclure, hériter ; couvre
  Aperçus IA, Mode IA et fonctionnalités d'IA de Discover ; **ni signal
  de classement, ni contrôle de l'entraînement** (pour ça :
  Google-Extended) ; effet en 1 à 2 jours ; **ouvert à tous les sites le
  31 août 2026** (support.google.com/webmasters/answer/16908024).
- **Rapport de performance IA générative** : billet Search Central de
  juin 2026 confirmé (titre lu) ; détail des métriques non lu à la
  source. Selon des sources secondaires : lancé le 3 juin 2026,
  impressions par surface (Aperçus IA, Mode IA, Discover), **sans clics
  ni requêtes**, données depuis le 18 mai 2026 **[à vérifier]**.
- **FAQ** : les résultats enrichis FAQ ne s'affichent plus depuis le
  7 mai 2026 ; documentation retirée le 15 juin 2026 (page faqpage,
  maj. 16 oct. 2026).

## Bing

- Rapport « AI Performance » de Bing Webmaster Tools : aperçu public
  depuis février 2026, citations dans Copilot et les résumés de Bing,
  pages citées, **requêtes d'ancrage** (grounding queries), exports CSV,
  pas de clics (sources secondaires : Search Engine Land, Search
  Influence) **[à vérifier sur la page Microsoft]**.

## Content Signals

- Politique de Cloudflare (billet « Content Signals Policy ») : trois
  clés `search` (index et liens, **hors résumés d'IA**), `ai-input`
  (contenu donné à un modèle au moment de répondre : RAG, ancrage),
  `ai-train` (entraînement) ; syntaxe `Content-Signal: search=yes,
  ai-train=no` ; une clé absente = aucune préférence exprimée ; robots
  .txt géré par Cloudflare : `search=yes, ai-train=no` ; présenté comme
  réserve de droits au titre de l'article 4 de la directive (UE)
  2019/790. **Ce n'est pas un contrôle d'accès** : respect volontaire.
  Brouillon IETF expiré le 4 avril 2026 selon claude-seo
  **[à vérifier sur datatracker]**.

## Recherche

- **Aggarwal et al., « GEO: Generative Engine Optimization »**, KDD 2024
  (arXiv 2311.09735, v3 du 28 juin 2024) : « jusqu'à 40% » de
  visibilité, efficacité variable selon le domaine. Les gains par méthode
  (+37%, +30%…) cités par les dépôts ne figurent pas dans le résumé
  **[à vérifier dans le tableau du papier]**.
- **C-SEO Bench** (Puerto et al., NeurIPS 2025 Datasets & Benchmarks,
  arXiv 2506.11097) : la plupart des méthodes de réécriture
  conversationnelle sont inefficaces et souvent négatives ; le SEO
  classique, qui améliore la place de la source dans le contexte, est
  nettement plus efficace ; plus il y a d'adoptants, moins il y a de
  gain.
- **Revue critique 2023-2026** (O. Martinez, arXiv 2607.14035,
  15 juil. 2026) : un contenu déjà récupéré peut changer sa citation ;
  **aucune technique n'a d'effet causal stable, durable et
  multi-plateformes sur la découvrabilité** ; les gains du papier GEO ne
  valent que dans son cadre (source déjà dans un contexte fixe).

## Droit français

- **Avis en ligne** : Code de la consommation, art. L111-7-2 (version
  en vigueur modifiée par la loi du 21 mai 2024) et D111-16 à D111-19
  (décret 2017-1436, en vigueur le 1er janv. 2018) : dire si les avis
  sont contrôlés et comment, dater chaque avis, motiver un refus,
  permettre de signaler un doute.
- **Faux avis** : art. L121-4, 27° et 28° (ordonnance 2021-1734,
  en vigueur le 28 mai 2022) : pratiques réputées trompeuses (avis
  présentés comme vérifiés sans vérification ; faux avis diffusés
  directement ou par un tiers). Peines de l'art. L132-2 citées par des
  avocats **[à vérifier sur Légifrance]**.
- Influence commerciale : loi n° 2023-451 du 9 juin 2023
  **[à relire pour les mentions « publicité »]**.
