# marketingskills `ai-seo` (Corey Haines) et skills.marketing (Profound)

## marketingskills `ai-seo` v2.9.0

MIT, 55k étoiles, commit 365b412 du 15 oct. 2026. Lu : `SKILL.md`
(499 lignes) et ses 15 références (`agent-defaults`, `agent-readiness`,
`ai-attribution`, `answer-accuracy`, `citations-vs-recommendations`,
`content-patterns`, `content-types`, `format-volatility`,
`linkedin-ai-citations`, `multilingual-and-commerce`, `okf`,
`platform-ranking-factors`, `positioning-and-consensus`,
`prompt-portfolio`, `youtube-ai-citations`), `evals/evals.json`. Le Skill
a beaucoup grandi depuis notre v1 (qui n'en tirait que « les trois
piliers »).

### Le meilleur

- **Hiérarchie des preuves** écrite dans le Skill : documentation
  officielle, puis expériences contrôlées, puis grandes données
  d'observation (souvent d'éditeurs), puis cas de praticiens. En cas de
  conflit, la documentation décide pour l'éligibilité et les robots, la
  donnée reste une hypothèse. « Ne jamais transformer le pourcentage d'une
  étude en prévision client. »
- **L'échelle de visibilité** : récupéré, cité, mentionné, recommandé ; et
  « déconseillé » (le modèle nomme un produit à éviter). La
  recommandation dépend du consensus du web (avis, forums, analystes,
  presse), pas du site.
- **Portefeuille de prompts** : partir de la demande réelle (ce que les
  acheteurs disent avoir demandé, appels commerciaux, tickets), familles
  d'intention pondérées par la valeur, **trois cohortes** (cœur stable
  versionné, exploratoire, **témoins** où la marque doit toujours ou ne
  doit jamais apparaître : s'ils bougent, c'est l'outil ou le moteur qui
  a changé), parcours d'achat en plusieurs tours.
- **Mesure non déterministe** : 3 à 5 passages par prompt et par moteur,
  un taux avec sa taille d'échantillon (« cité 3/5, n=5 »), comparer des
  taux et non des passages ; 4/5 → 3/5 est du bruit.
- **Exactitude des réponses** : un registre des affirmations (moteur,
  date, prompt, phrase du modèle, type, verdict, preuve, source probable,
  gravité, responsable), **7 verdicts** (exact, exact mais incomplet,
  ambigu, périmé, faux, opinion présentée comme un fait, invérifiable),
  « corriger la source d'abord ».
- **Attribution en 4 couches** : exposition, comportement immédiat
  (référents IA groupés), comportement différé (recherches de marque,
  visites directes à 1 h, 24 h, 7 jours), résultat business ; plans
  d'évaluation (groupe témoin, comparaison appariée, série temporelle) et
  vocabulaire « observation, association, résultat causal ».
- **Multilingue** : la langue et le pays sont deux dimensions ; prompts
  construits depuis la demande locale, pas traduits ; trouver les sources
  locales citées ; trois écarts (traduction, information, entité).
- **Positionnement** : chaque profil tiers doit dire la même chose que la
  page « à propos » ; le guide d'achat qui se classe lui-même premier est
  cité mais ne fait pas recommander (étude Lily Ray, 2026, 69% des
  citations recommandaient un autre produit **[à vérifier]**) ; option :
  nommer le leader d'abord, honnêtement.
- **YouTube** : le modèle lit la couche texte (transcription, chapitres,
  description) ; déjà repris dans notre `/seo-social`.

### Le fragile

- Tableau de l'étude GEO de Princeton avec des gains par méthode (+40%,
  +37%, +30%…, « bourrage de mots-clés -10% », « jusqu'à 115% ») :
  chiffres à confronter au papier (Aggarwal et al., KDD 2024)
  **[à vérifier]**.
- « Blocs de réponse de 40 à 60 mots », « FAQ schema cité plus souvent
  par Perplexity », « Perplexity privilégie les PDF », `pricing.md`
  présenté comme un besoin : sans source primaire.
- « Claude utilise Brave Search » **[à vérifier]** ; « ChatGPT 5.6
  (août 2026) a divisé par deux les citations de listicles »
  **[à vérifier]**.
- « Pas de rapport IA dans Search Console » : contredit par le réglage
  « Search generative AI » cité par claude-seo **[à vérifier à la
  source]**.
- OKF (Open Knowledge Format, Google Cloud, juin 2026) : expérimental, le
  Skill le dit lui-même.
- Beaucoup de chiffres Profound (éditeur d'un outil de suivi) : le Skill
  les étiquette « recherche d'éditeur », bonne pratique.

## skills.marketing (Profound)

`retieedra-profound/skills-marketing-library`, MIT (copyright 2026
Profound), commit 80293f1 du 31 août 2026, 0 étoile (dépôt source de
skills.marketing). 12 Skills Profound lus, dont 10 sur l'AEO :
`aeo-operator-2026` (375 lignes) et 9 Skills courts (60 à 80 lignes) dont
marketingskills a repris et crédité la matière.

### `aeo-operator-2026` : la meilleure méthode de diagnostic lue

- **Règles** : l'AEO est probabiliste, ne jamais promettre une citation
  ou un gain ; séparer moteurs, modèles, surfaces, langues, marchés,
  périodes ; quatre résultats distincts (visibilité, influence sur les
  citations, cadrage et exactitude, impact business) ; pas de llms.txt,
  de « schema AEO », de découpage mécanique ni de FAQ en tactique
  universelle.
- **La pile de visibilité, dans l'ordre** : accès et éligibilité,
  adéquation à la récupération, prêt à être cité, visibilité et récit de
  marque, écosystème de sources, résultat. « Un échec à une couche ne
  justifie pas une réécriture à une autre » ; « la plus petite
  intervention crédible ».
- **Classes de sources** pour le diagnostic (propre site, concurrent,
  presse, communiqué, institution, social, autre) et regroupement pour la
  direction (site de marque, gagné ou institutionnel, social).
- **Diagnostic de baisse** : confirmer sur une cohorte stable avant de
  conclure, chercher les changements d'accès, de contenu, de sources
  tierces, de concurrents ; ne pas accuser une mise à jour sans preuve.
- **Note sur 100 optionnelle**, « seulement si utile à la communication ».
- Mentionne un rapport « AI Performance » dans Bing Webmaster Tools
  **[à vérifier]**.

### Les Skills courts

- `ai-retrieval-fanout-mapper` : décomposer la tâche en entités, sous-
  questions factuelles, critères, contraintes ; grouper en familles de
  faits ; **pas une page par requête dérivée** ; étiqueter « déduit »
  quand les requêtes ne sont pas observées.
- `ai-prompt-portfolio-builder` : étude « once a day » (753 prompts,
  7 plateformes, 2 semaines) ; la composition du portefeuille compte plus
  que la fréquence.
- `ai-citation-mix-strategist` : 11,84 milliards de citations, environ
  57% vers des sites d'entreprise, mix très variable par modèle et
  secteur ; « diagnostiquer avant de prescrire Reddit ou la presse ».
- `ai-answer-accuracy-auditor`, `ai-search-attribution-planner`,
  `international-aeo-strategist`, `ai-commerce-readiness-auditor`,
  `commercial-ai-journey-mapper`, `claude-code-discoverability-auditor` :
  matière déjà reprise par marketingskills (voir plus haut).

## Verdict

C'est la partie « mesure et stratégie » qui manque le plus à notre v1 :
portefeuille de prompts à cohortes et témoins, taux avec échantillon,
échelle cité/mentionné/recommandé, registre d'exactitude à 7 verdicts,
attribution en couches, diagnostic par couche. À reprendre en français,
avec nos scripts, sans aucun chiffre d'éditeur présenté comme une règle.
