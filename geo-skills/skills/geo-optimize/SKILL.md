---
name: geo-optimize
description: >-
  Plan d'optimisation GEO / AEO d'un site ou d'un contenu : trois piliers
  (structure citable, autorité, présence hors du site), types de contenus que
  les IA citent le plus, méthodes validées par la recherche (sources,
  statistiques, citations d'experts), fraîcheur, et priorités par plateforme
  (AI Overviews, ChatGPT, Perplexity, Gemini, Claude, Mistral). Utilise-le
  pour « optimiser pour les IA », « AEO », « GEO », « être cité par ChatGPT »,
  « stratégie AI search ».
---

# geo-optimize

Ce Skill assemble les autres en une stratégie. Il ne remplace pas le SEO :
la plupart des moteurs génératifs avec recherche web partent des résultats
d'un moteur classique. Une page mal indexée a peu de chances d'être citée.

## Les trois piliers

1. **Structure** : chaque page répond, en passages autonomes et chiffrés
   (`/geo-citability`), lisibles par les robots (`/geo-crawlers`), balisés
   (`/geo-schema`).
2. **Autorité** : auteur expert nommé, sources citées, données propres,
   expérience de terrain, dates de mise à jour réelles (E-E-A-T).
3. **Présence** : la marque est mentionnée là où les IA puisent
   (`/geo-mentions`).

## Ce qui aide, d'après la recherche

L'étude GEO de Princeton (Aggarwal et al., KDD 2024) a testé des réécritures
sur des moteurs génératifs. Ordre de grandeur de la visibilité gagnée dans
leurs tests **[étude académique, 2024 ; résultats variables selon le moteur
et le sujet]** :

| Méthode | Effet observé |
|---|---|
| Citer des sources | jusqu'à +40% |
| Ajouter des statistiques | jusqu'à +37% |
| Ajouter des citations d'experts attribuées | jusqu'à +30% |
| Ton assuré et précis | jusqu'à +25% |
| Clarté, phrases simples | jusqu'à +20% |
| Termes techniques justes | jusqu'à +18% |
| Bourrage de mots-clés | environ −10% |

Dans le pack, ça devient : pas de fait sans source, pas de chiffre inventé
(`{{à compléter}}`), citations réelles seulement, style affirmatif
(`--affirmatif` de l'humaniseur du pack SEO).

## Les contenus que les IA citent le plus

| Format | Pourquoi | Règle |
|---|---|---|
| Définition et « qu'est-ce que » | réponse courte, reprise telle quelle | 40 à 60 mots dès le début |
| Comparatif « X ou Y », « X vs Y » | les IA aiment les tableaux | tableau de critères + verdict par profil |
| « Meilleurs… » et classements | réponse aux prompts de recommandation | critères publics, honnêteté sur ses propres produits |
| Guide pratique en étapes | « comment » | étapes numérotées, durée, coût |
| Données propres, étude, baromètre | seul le site les possède | méthode et date publiées |
| FAQ visible | une question, une réponse | réponses complètes, pas de teasing |

## Fraîcheur

Les moteurs avec recherche web préfèrent les contenus récents sur les sujets
qui bougent. Afficher une date de mise à jour réelle, mettre à jour les
chiffres de l'année (`/seo-refresh` du pack SEO), et ne jamais changer la date
sans changer le contenu.

## Par plateforme

Tendances observées par les praticiens **[estimation de praticien]** :

| Plateforme | Ce qui compte |
|---|---|
| Google AI Overviews / AI Mode | être bien classé sur Google, passages qui répondent, Googlebot autorisé |
| ChatGPT (recherche) | index de recherche tiers + OAI-SearchBot, comparatifs, presse |
| Perplexity | sources récentes et citées, forums et Reddit, PerplexityBot |
| Gemini | index Google, YouTube, entités Google |
| Claude | recherche web + Claude-SearchBot |
| Mistral (Le Chat) | recherche web, sources francophones |

Ces tendances changent vite : vérifier avec `/geo-visibility` (sources
citées) plutôt que les supposer.

## Méthode

1. Lancer `/geo-audit` sur 3 à 5 pages clés et `/geo-visibility` sur 15
   prompts.
2. Lire les écarts : technique (bloquant, à corriger d'abord), citabilité
   (pages), marque (hors site).
3. Plan sur 90 jours, 5 actions maximum, chacune avec le Skill qui la fait,
   l'effort et l'indicateur suivi.
4. Mesurer de nouveau au bout de 30 jours, avec les mêmes prompts. Ajouter ce
   qui marche dans `apprentissages.md`.

## Sortie

```
PLAN GEO · assurly.example · 90 jours
1. Débloquer PerplexityBot et Claude-SearchBot (1 h) → /geo-crawlers
2. Réécrire l'ouverture des 5 guides les plus lus (2 j) → /geo-citability
3. Comparatif « assurance expatrié Dubaï » avec tableau (1 j) → /seo-article
4. Étude « coût des soins à Dubaï » avec vos données anonymisées (5 j) → /geo-mentions
5. BlogPosting + Person sur tout le blog (2 h) → /geo-schema
INDICATEUR : présence dans les réponses 7% → objectif 25% sur les 15 mêmes prompts
```

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : pas de promesse de résultat ; les effets cités sont ceux
  d'études, présentés comme tels.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
