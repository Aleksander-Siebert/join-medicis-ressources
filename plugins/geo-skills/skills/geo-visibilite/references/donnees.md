# Les données : quoi récupérer, et comment

**Mode gratuit par défaut** : les réponses collées. Les connecteurs et les
outils payants s'ajoutent, ils ne se mélangent pas aux réponses collées.

## 1. Google Search Console (gratuit, première partie)

- **Rapport de performance « IA générative »** : impressions du site dans
  les Aperçus IA, le Mode IA et Discover (Google, guide « AI
  optimization », maj. 10 juil. 2026). Détail exact des métriques (clics,
  requêtes, période) **[à vérifier dans ton compte]**.
- **Réglage « Contrôle de l'IA générative dans la Recherche »**
  (Paramètres) : vérifie que le site est **inclus**. Exclu = absent des
  Aperçus IA et du Mode IA, quoi qu'on fasse ailleurs.
- **Requêtes longues** du rapport Performance (type « Web ») : la meilleure
  source de questions pour le portefeuille.

Export : Performance → filtre → Exporter (CSV ou Google Sheets).

## 2. Bing Webmaster Tools (gratuit, première partie)

Rapport « AI Performance » : citations dans Copilot et les résumés de Bing,
pages citées, **requêtes d'ancrage** (les recherches que l'IA a lancées),
export CSV, sans clics **[à vérifier sur la page Microsoft]**. Les requêtes
d'ancrage nourrissent le portefeuille (cohorte exploratoire).

## 3. Journaux du serveur (gratuit, première partie)

Les visites d'OAI-SearchBot, Claude-SearchBot, PerplexityBot,
MistralAI-Index et des robots « utilisateur » (ChatGPT-User, Claude-User,
Perplexity-User, MistralAI-User) montrent quelles pages les moteurs lisent.
Détail des robots : `/geo-acces`.

## 4. Outils de suivi (payants)

Peec AI, Otterly, Profound, Ahrefs Brand Radar, Semrush (AI toolkit),
SE Ranking (via son serveur MCP), HubSpot :

- Récupère : réponses brutes si possible, sinon taux par moteur et par
  question, **nombre de passages**, dates, sources citées.
- Garde l'étiquette de l'outil : ses moteurs passent parfois par l'API, pas
  par l'appli ; ses échantillons ne sont pas ceux d'un autre outil, ne
  compare pas deux outils entre eux.
- Si l'outil donne un « score de visibilité » composite, rapporte-le à part
  et recalcule les taux simples quand c'est possible.

## 5. Tavily (option, désactivée par défaut)

L'API de recherche de Tavily répond sans clé (débit limité) et renvoie une
réponse rédigée avec ses sources. Testé le 16 oct. 2026 : réponse en
anglais à une question française, sources françaises.

- **Seulement à la demande**, après avoir dit que les questions partent
  chez Tavily, un service tiers.
- **Approximation** : c'est le moteur de Tavily, ni ChatGPT, ni Perplexity,
  ni Google. Utile pour voir quelles sources du web ressortent sur une
  question, pas pour dire ce que voient les clients.
- Toujours dans un fichier séparé ; jamais additionné aux réponses collées.

```bash
python3 scripts/visibilite.py tavily portefeuille.csv --accepte-tiers > reponses-tavily.txt
python3 scripts/visibilite.py mesurer reponses-tavily.txt --marque "Assurly" --approximation
```

## 6. Quand une donnée manque

| Manque | Que faire |
|---|---|
| Pas d'accès à Search Console | Portefeuille depuis les mots des clients et les forums ; le dire. |
| Pas le temps de 5 passages | 2 passages sur le cœur, étiqueté « exploratoire ». |
| Un moteur inaccessible (pays, compte) | Le retirer de la mesure, le dire ; ne pas le remplacer par un autre. |
| Réponses d'un outil sans nombre de passages | Rapporter les chiffres de l'outil sans intervalle, étiquetés « outil, échantillon inconnu ». |
