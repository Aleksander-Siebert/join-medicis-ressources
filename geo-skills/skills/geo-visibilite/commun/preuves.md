# Preuves : ce qu'on sait des moteurs d'IA, et d'où ça vient

Chaque affirmation du pack sur un moteur, un robot, Google ou le droit a un
**niveau de preuve** et une **date de vérification**. Un fait absent de ce
fichier porte **[à vérifier]**. Les robots et les réglages changent vite : on
revérifie une ligne quand sa date a plus de **60 jours** (procédure en fin
de fichier).

| Niveau | Ce que c'est | Comment l'écrire |
|---|---|---|
| **Officiel** | documentation d'un moteur ou d'un éditeur de robot, texte de loi | affirmé, avec la source |
| **Recherche** | article évalué ou préprint, méthode publiée | « selon [auteurs], [date], dans [cadre] » ; jamais généralisé hors de son cadre |
| **Étude** | étude d'un éditeur d'outil, données d'observation | « selon [éditeur], [date], sur [échantillon] » ; corrélation, pas cause |
| **Praticien** | constat répété, sans preuve publique | repère ou option, jamais règle |
| **Folklore** | répété partout, contredit ou sans source | nommé pour être écarté |

## 1. Robots et jetons (officiel)

| Nom | Éditeur | Rôle | robots.txt | Source | Vérifié le |
|---|---|---|---|---|---|
| OAI-SearchBot | OpenAI | index de la recherche ChatGPT ; bloqué = absent des réponses de recherche ; prise en compte en 24 h environ | respecté | developers.openai.com/api/docs/bots | 16 oct. 2026 |
| GPTBot | OpenAI | entraînement des modèles | respecté | idem | 16 oct. 2026 |
| ChatGPT-User | OpenAI | visite demandée par un utilisateur, pas un robot automatique | « peut ne pas s'appliquer » | idem | 16 oct. 2026 |
| OAI-AdsBot | OpenAI | conformité des pages de destination des annonces | non précisé | idem | 16 oct. 2026 |
| Claude-SearchBot | Anthropic | index de recherche de Claude | respecté | support.claude.com (article du 7 avr. 2026) | 16 oct. 2026 |
| Claude-User | Anthropic | visite pour une question d'utilisateur | respecté | idem | 16 oct. 2026 |
| ClaudeBot | Anthropic | entraînement ; `Crawl-delay` accepté | respecté | idem | 16 oct. 2026 |
| PerplexityBot | Perplexity | résultats de recherche, pas d'entraînement | respecté | docs.perplexity.ai/guides/bots | 16 oct. 2026 |
| Perplexity-User | Perplexity | visite pour une question d'utilisateur | « ignore généralement » | idem | 16 oct. 2026 |
| MistralAI-Index | Mistral | index de la recherche de Vibe, pas d'entraînement | non précisé | docs.mistral.ai/robots | 16 oct. 2026 |
| MistralAI-User | Mistral | action d'un utilisateur dans Vibe | non détaillé | idem | 16 oct. 2026 |
| MistralAI-Training | Mistral | entraînement | excluable | idem | 16 oct. 2026 |
| Googlebot | Google | Google Search, donc les Aperçus IA et le Mode IA | respecté | Search Central | 16 oct. 2026 |
| Google-Extended | Google | **jeton sans robot propre** : entraînement des futurs Gemini et ancrage dans les applis Gemini et Vertex AI ; **sans effet sur l'inclusion dans Search ni le classement** | respecté | « Google common crawlers », maj. 15 oct. 2026 | 16 oct. 2026 |
| Applebot | Apple | recherche Spotlight, Siri, Safari ; aussi entraînement et contexte de réponses générées ; `nosnippet` refuse l'usage dans les réponses | respecté | support.apple.com/119829 (4 sept. 2026) | 16 oct. 2026 |
| Applebot-Extended | Apple | **ne crawle pas** : refuse l'usage pour entraîner les modèles d'Apple ; sans effet sur la recherche | respecté | idem | 16 oct. 2026 |

**Le bon robot pour chaque affirmation** (règle du pack, testée) :

| Pour dire… | Regarde | Pas |
|---|---|---|
| « citable dans ChatGPT Search » | OAI-SearchBot | GPTBot |
| « citable dans la recherche de Claude » | Claude-SearchBot | ClaudeBot |
| « présent dans la recherche de Vibe (Mistral) » | MistralAI-Index | MistralAI-Training |
| « éligible aux Aperçus IA de Google » | Googlebot et l'extrait autorisé | Google-Extended |
| « refuse l'entraînement » | GPTBot, ClaudeBot, MistralAI-Training, Google-Extended, Applebot-Extended | les robots de recherche |

## 2. Google (officiel)

| Fait | Source | Vérifié le |
|---|---|---|
| Éligibilité aux Aperçus IA et au Mode IA : page indexée et éligible à un extrait dans Google Search, **et** site inclus via le réglage Search Console. Aucune garantie d'affichage. | developers.google.com/search/docs/fundamentals/ai-optimization-guide (maj. 10 juil. 2026) | 16 oct. 2026 |
| Inutile pour Google : llms.txt, fichiers pour IA, Markdown ; découper le contenu (« pas de longueur de page idéale ») ; réécrire pour l'IA ; chercher des mentions non authentiques ; données structurées spéciales (aucun schema propre à l'IA). | même source | 16 oct. 2026 |
| Ce qui compte : contenu original et non générique, fait par des personnes compétentes ; site explorable, HTML sémantique, JavaScript bien conçu ; images et vidéos ; Business Profile et Merchant Center à jour. | même source | 16 oct. 2026 |
| Mesure : rapport de performance « IA générative » dans Search Console. Méfiance envers les outils qui promettent un classement ou prétendent voir des signaux internes de Google. | même source | 16 oct. 2026 |
| Réglage « Contrôle de l'IA générative dans la Recherche » (Paramètres) : inclure (défaut), exclure, hériter ; couvre Aperçus IA, Mode IA et Discover ; **ni signal de classement, ni contrôle de l'entraînement** ; effet en 1 à 2 jours ; ouvert à tous les sites le 31 août 2026. | support.google.com/webmasters/answer/16908024 | 16 oct. 2026 |
| Détail du rapport IA générative (impressions par surface, sans clics ni requêtes, données depuis le 18 mai 2026). | sources secondaires seulement | **[à vérifier]** |
| Les résultats enrichis FAQ ne s'affichent plus depuis le 7 mai 2026. | page « FAQPage », maj. 16 oct. 2026 | 16 oct. 2026 |

## 3. Bing

| Fait | Source | Vérifié le |
|---|---|---|
| Rapport « AI Performance » de Bing Webmaster Tools : citations dans Copilot et les résumés de Bing, pages citées, requêtes d'ancrage, exports CSV, pas de clics ; aperçu public depuis février 2026. | Search Engine Land, Search Influence (secondaires) | **[à vérifier sur la page Microsoft]** |

## 4. Content Signals (préférence, pas contrôle d'accès)

| Fait | Source | Vérifié le |
|---|---|---|
| Clés `search` (index et liens, hors résumés d'IA), `ai-input` (contenu donné à un modèle pour répondre), `ai-train` (entraînement). Syntaxe `Content-Signal: search=yes, ai-train=no`. Clé absente = pas de préférence exprimée. Respect volontaire. Présenté comme réserve de droits (directive (UE) 2019/790, art. 4). | Cloudflare, billet « Content Signals Policy » | 16 oct. 2026 |
| Brouillon IETF expiré le 4 avril 2026 ; aucune déclaration de Google. | claude-seo (secondaire) | **[à vérifier sur datatracker]** |

## 5. Recherche (ce que valent les « optimisations pour l'IA »)

| Fait | Source | Niveau |
|---|---|---|
| Dans son cadre expérimental, le GEO augmente la visibilité « jusqu'à 40% », avec une efficacité variable selon le domaine. | Aggarwal et al., KDD 2024 (arXiv 2311.09735) | Recherche |
| Sur les moteurs actuels, la plupart des méthodes de réécriture sont inefficaces et souvent négatives ; le SEO classique, qui améliore la place de la source dans le contexte, est nettement plus efficace ; plus il y a d'adoptants, moins il y a de gain. | Puerto et al., C-SEO Bench, NeurIPS 2025 (arXiv 2506.11097) | Recherche |
| Aucune technique GEO examinée (2023-2026) n'a d'effet causal stable, durable et multi-plateformes sur la découvrabilité ; les gains du papier fondateur ne valent que dans son cadre. | O. Martinez, revue critique, arXiv 2607.14035 (15 juil. 2026) | Recherche (préprint) |
| Environ 5, 10 et 15 passages par question donnent une fiabilité exploratoire, de confirmation et solide. | « Dice Roll Method », arXiv 2609.04047 (sept. 2026) | Recherche (préprint) **[à relire]** |
| La même liste de marques revient moins d'une fois sur 100 réponses. | SparkToro et Gumshoe, janv. 2026, 2 961 passages | Étude **[à relire]** |

## 6. Droit français

| Fait | Source | Vérifié le |
|---|---|---|
| Avis en ligne : dire si les avis sont contrôlés et comment, dater chaque avis, motiver un refus, permettre de signaler un doute. | Code de la consommation, L111-7-2 ; D111-16 à D111-19 (décret 2017-1436) | 16 oct. 2026 |
| Faux avis : pratiques réputées trompeuses (avis présentés comme vérifiés sans vérification, faux avis diffusés directement ou par un tiers). | Code de la consommation, L121-4, 27° et 28° (ordonnance 2021-1734, en vigueur le 28 mai 2022) | 16 oct. 2026 |
| Peines applicables. | L132-2, cité par des avocats | **[à vérifier sur Légifrance]** |
| Influence commerciale : mentions obligatoires. | loi n° 2023-451 du 9 juin 2023 | **[à relire]** |

## 7. Folklore à reconnaître et écarter

- « llms.txt est essentiel pour être indexé par les IA » (Google dit
  l'ignorer ; poids nul dans le pack).
- « Bloquer GPTBot retire de ChatGPT Search » (c'est OAI-SearchBot).
- « Les passages de 134 à 167 mots » ou « de 40 à 60 mots » sont cités ;
  « 2 000 mots pour ChatGPT » (aucune source primaire ; Google : pas de
  longueur idéale).
- Gains par méthode « +40% citer des sources, +37% statistiques » présentés
  comme des résultats généraux.
- Schema FAQ ou HowTo « pour l'IA ».
- Fichiers `ai.txt`, `/ai/summary.json` (aucune adoption documentée).
- Rang moyen dans ChatGPT (instable d'un passage à l'autre).

## Mettre à jour ce fichier

1. Robots : pages OpenAI, Anthropic, Perplexity, Mistral, Google, Apple
   (liens ci-dessus) ; une ligne par changement, avec la date.
2. Google : guide « AI optimization », page du réglage, journal « Latest
   documentation updates » de Search Central.
3. Recherche : nouvelles versions des articles cités.
4. Mettre la même date dans `CHECKED_ON` des scripts qui portent la table.
