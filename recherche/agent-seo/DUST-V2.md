# Agent SEO sur Dust, v2 : conception à valider

Statut : **proposition, rien n'est écrit dans `plugins/agent-seo/dust/`**
tant que l'utilisateur n'a pas validé (16 novembre 2026).

Sources : Dust, « AI agents SEO workflow » (Davis Christenhuis, 17 juin 2026) ;
Ahrefs, Ryan Law, « How I do content engineering with Claude Code » (captures
fournies par l'utilisateur, dépôt privé), « My complete AI content process »,
« AI content wasn't good enough. Now it is », « 15 Ahrefs MCP use cases » ;
kit Dust v1 de ce dépôt.

## 1. Ce qui manque honnêtement à la v1 Dust

| Manque de la v1 | Conséquence | Correction v2 |
|---|---|---|
| Mémoire = Agent Memory, personnelle | un collègue repart de zéro, le déclencheur ne la lit peut-être pas | base partagée Google Sheet (comme SEOMonitor de Dust) |
| Priorité = impressions × position seulement | des sujets sans lien avec le produit remontent | grille adéquation blog + produit (Ryan, `/keyword-prioritization`) |
| Aucun point de validation | le brouillon part sur un plan non relu | validation du plan BLUF avant rédaction (Ryan), mode autonome sinon |
| Pas de référence aux articles du site | ton générique, risque de réécrire l'existant | étape références (Ryan, `/ahrefs-reference`) |
| Produit cité au hasard | mentions forcées ou absentes | emplacements produit dans le plan, faits LIVE seuls (Ryan, `/ahrefs-mentions`) |
| Livraison brute en Markdown | relecture pénible | aperçu Frame au style du site + bloc CMS (Ryan, `/preview`, `/format-for-publish`) |
| Pas de mise à jour d'articles | la moitié du gain SEO ignorée | chaîne mise à jour avec avant/après (Ryan, pipeline `update-*`) |
| Pas de tableau de bord | aucun retour sur ce qui marche | Frame Search Console + GA4 (SEOVisualizer) |
| Données gratuites seulement | ni volume ni écart concurrentiel | mode Ahrefs/Semrush optionnel, branche par branche |
| Le chef transmet de longs textes | coût en crédits, pertes entre agents | identifiant de sujet + ligne du Sheet, chaque agent relit la source |

## 2. Le schéma v2 (première version à 8 agents, remplacée par le §4 : 5 agents + chef)

```
 Déclencheurs : lundi 8 h (veille)      1er du mois (bilan)       à la demande
        │                                    │                        │
 ┌──────▼────────┐                   ┌───────▼────────┐      ┌────────▼────────┐
 │ @SEO-Veille   │──► Sheet « Sujets »│ @SEO-Tableau   │      │ @SEO-Chef       │
 │ 1 sujets      │   (date détectée,  │ Frame GSC+GA4  │      │ 3 modes :       │
 │ 2 priorité    │    statut, score)  │ → « à mettre   │      │ créer, mettre à │
 └───────────────┘                   │   à jour »     │      │ jour, bilan     │
                                     └────────────────┘      └──┬──────────────┘
                     run_agent, dans l'ordre                    │
   ┌────────────┬──────────────┬──────────────┬─────────────┬──┴───────────┐
┌──▼───────┐ ┌──▼─────────┐ ┌──▼──────────┐ ┌─▼──────────┐ ┌▼───────────┐ ┌▼────────────┐
│@SEO-SERP │ │@SEO-Plan   │ │@SEO-Redact. │ │@SEO-Verif  │ │@SEO-Edition│ │@SEO-MiseAJour│
│3 recherche│ │5 plan BLUF │ │7 brouillon  │ │8 sources   │ │9 aperçu    │ │extraire,     │
│4 références│ │6 mentions  │ │             │ │+ vérité    │ │10 CMS      │ │auditer, écart│
│« pour nous ?»│ │⏸ validation│ │             │ │produit     │ │            │ │avant/après   │
└──────────┘ └────────────┘ └─────────────┘ └────────────┘ └────────────┘ └──────────────┘
```

Étape 0 (direction) : une phrase de l'utilisateur, transmise par le chef à
chaque agent (angle, sous-sujets, produit à montrer), comme le `--context` de
Ryan.

## 3. Matrice : chaque fonction, sa source, son verdict

### Création

| # | Fonction | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|---|
| 0 | Direction en amont | Ryan `--context` ; Ryan 2025 « front-load the brief » | reprendre | champ « Direction » dans chaque appel, gardé dans le Sheet |
| 1 | Sujets depuis Search Console | v1 `@SEO-Sujets` | reprendre | positions 8-40, regroupement, marque et pages existantes écartées |
| 1b | Écart concurrentiel | Ryan `/content-gap-analysis` (Ahrefs) | améliorer | mode Ahrefs/Semrush seulement, marqué « outil : … » ; gratuit : questions de la SERP |
| 1c | Tableau cumulé avec date détectée | Dust SEOMonitor | reprendre | Sheet partagé, dédoublonné, statut (proposé, retenu, écrit, abandonné + raison) |
| 1d | Volume, KD | Dust SEOMonitor (Semrush) | reprendre en option | jamais de volume sans outil nommé |
| 2 | Priorisation adéquation blog + produit | Ryan `/keyword-prioritization` | reprendre | Skill Dust « Priorisation » : grille 0-3 lecteurs, 0-3 produit, × score GSC |
| 3 | Contrôle « est-ce pour nous ? » | Dust SERPScout | reprendre | avant toute recherche, contre le contexte du site |
| 3b | Relevé top 10 (titre, URL, type, éditeur, en-têtes) | SERPScout ; v1 `@SEO-SERP` | reprendre | origine du relevé écrite (pays, outil, date) |
| 3c | Signaux « ne pas tenter » | pack SEO `/seo-serp` | reprendre | institutions, Wikipédia, actualité chaude |
| 4 | Articles du site comme référence | Ryan `/ahrefs-reference` | reprendre | source « Websites » du site : 2-3 articles proches pour le ton et pour ne pas réécrire |
| 5 | Plan BLUF + emplacements de preuves | Ryan `/outline` ; Ryan 2025 approbation du plan | reprendre | ⏸ validation dans la conversation (sauf mode autonome : hypothèse écrite) |
| 6 | Emplacements produit | Ryan `/ahrefs-mentions` | améliorer | seulement les faits LIVE, 1 à 3 mentions, jamais dans l'intro |
| 6b | Liens internes réels | Ryan 2025 (URL inventées corrigées en fournissant les vraies) | reprendre | liens tirés de la source « Websites » uniquement |
| 7 | Brouillon par catégories d'instructions | Dust SEOArticles | reprendre | ton, bons et mauvais exemples, règles marque, GEO/AEO, typographie française |
| 7b | Méta, slug, TL;DR, FAQ, CTA | Dust SEOArticles | reprendre | longueur = concurrents lus, pas 2 000-2 500 mots imposés |
| 7c | Rôle « expert de terrain » | Ryan `/draft` | **écarter** | fait inventer des anecdotes ; l'expérience vient de la réserve de preuves |
| 8 | Vérifier chaque affirmation, liens vers la source | Ryan `/verify-claims` ; v1 `@SEO-Verif` | reprendre | statuts CONFIRMÉ/PARAPHRASE/ABSENT/INACCESSIBLE, vérité produit, autre modèle |
| 8b | Critères qualité | Ryan « AI content… now it is » | reprendre | Skill « Critères qualité » : intention, consensus, manques, info nouvelle, MECE, objections, essentiel d'abord |
| 8c | Captures Ahrefs générées | Ryan `/generate-ahrefs-screenshot` | **écarter** | propre à leur produit ; emplacement d'image décrit à la place |
| 9 | Aperçu au style du site | Ryan `/preview` | adapter | Frame Dust (comme SEOVisualizer) **[à vérifier : rendu HTML libre]** |
| 10 | Format CMS | Ryan `/format-for-publish` (WordPress) | adapter | Markdown, HTML ou blocs Gutenberg au choix ; `.docx` via `exporter.py` hors Dust |

### Mise à jour

| Fonction | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Choisir quoi mettre à jour | Ahrefs MCP cas 3 et 10 ; pack `/seo-refresh` | reprendre | paniers : à portée 8-20, CTR faible, presque en tête 4-7 (Search Console) |
| Extraire l'article publié | Ryan `/extract-content` | reprendre | lecture de l'URL, texte et structure |
| Consignes de mise à jour | Ryan `/update-guidance` | reprendre | requêtes réelles de la page dans Search Console |
| Chiffres datés | Ryan `/update-claims` | reprendre | chaque chiffre de plus de 12 mois rouvert |
| Manques face à la SERP | Ryan `/update-topic-gaps` | reprendre | écart avec les 3 résultats du dessus |
| Mentions produit | Ryan `/update-ahrefs-mentions` | reprendre | faits RETIRÉ retirés, LIVE vérifiés |
| Réécriture minimale | Ryan `/update-draft` | reprendre | liste de changements acceptés ou refusés un par un |
| Avant/après | Ryan `/update-preview` | adapter | Frame côte à côte **[à vérifier]**, sinon tableau avant/après |

### Tableau de bord

| Fonction | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Frame de suivi | Dust SEOVisualizer | reprendre | Search Console obligatoire |
| Sessions, inscriptions, formulaires | SEOVisualizer | reprendre si GA4 branché | GA4 optionnel, autres connecteurs plus tard |
| Articles de l'agent vs reste du blog | — | ajout | lu dans le Sheet (statut « écrit ») |
| Opportunités par priorité, articles faibles | SEOVisualizer ; Ahrefs MCP cas 1, 4, 7 | reprendre | les faibles partent vers `@SEO-MiseAJour` |
| Enseignements | SEOVisualizer | reprendre | « un mois ne prouve rien » écrit ; proposition pour l'onglet Apprentissages |

### Transverse

| Fonction | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Un fichier par étape | Ryan (dossiers numérotés) | adapter | dans Dust : une ligne par étape dans l'onglet « Journal » du Sheet, relançable par étape |
| Tests avec et sans Skill | Ryan (skill-creator) | reprendre | `evals/` : même sujet, v1 vs v2, à l'aveugle |
| Skills partagés | Dust Skills | reprendre | Zéro invention, Vérité produit, Priorisation, Critères qualité, Format de sortie |
| Mode gratuit / Ahrefs / Semrush | Ahrefs et Semrush MCP | reprendre | chaque agent dit quoi faire avec ou sans l'outil |

## 4. Décisions de l'utilisateur (16 novembre 2026)

- **Base partagée : Google Sheet.**
- **5 agents + le chef**, pour limiter les crédits :

| Agent | Étapes | Lancement |
|---|---|---|
| `@SEO-Chef` | orchestre, 3 modes : créer, mettre à jour, bilan ; transmet la direction (étape 0) | à la demande |
| `@SEO-Veille` | 1 sujets, 1c Sheet « Sujets », 2 priorité | lundi 8 h |
| `@SEO-Plan` | 3 « pour nous ? » et relevé, 4 références, 5 plan BLUF, 6 mentions, ⏸ validation | par le chef |
| `@SEO-Redacteur` | 7 brouillon ; après la vérif : 9 aperçu Frame, 10 format CMS, Google Doc | par le chef (2 passages) |
| `@SEO-Verif` | 8 sources, vérité produit, critères qualité ; autre modèle | par le chef |
| `@SEO-Suivi` | tableau de bord + chaîne de mise à jour | 1er du mois, ou à la demande |

- **Données : mode gratuit construit et testé ; mode Ahrefs/Semrush décrit,
  marqué non testé** (l'utilisateur n'a pas d'outil payant).

## 5. Vérifié dans la doc de Dust (16 novembre 2026)

- **Écrire dans un Google Sheet** : l'outil Google Sheets est déprécié ; l'outil
  Google Drive le remplace avec « Append to Spreadsheet » et « Update
  Spreadsheet ». Il faut reconnecter Google Drive avec les droits d'écriture
  (portée `drive.file`). Source : docs.dust.tt, page « Google Sheets
  (deprecated) » et changelog « Dust agents can now create and edit Google
  Drive documents ».
- **Créer un Google Doc** : possible avec le même outil (changelog ci-dessus).
  La v1 disait l'inverse d'après une FAQ ancienne : à corriger.
- **Frames** : compétence « Create Frames » dans Ajouter des capacités ;
  rapports, tableaux de bord, visualisations ; export PDF, PNG ou source ;
  l'agent peut suivre logo et couleurs fournis. Un aperçu d'article au style
  du site n'est pas décrit tel quel **[à tester]**. Les Frames avec backend
  consomment des crédits après le 18 novembre 2026.
- **GA4** : aucune intégration native trouvée dans la doc de Dust ; passer par
  un serveur MCP tiers **[à vérifier]**. D'où : Search Console obligatoire,
  GA4 en option.

## 6. Points ouverts
- Ahrefs MCP (offre Lite et plus, 25 000 unités selon le centre d'aide) et
  Semrush MCP (offres One Starter et plus) **[à vérifier]**.
- Coût : 8 agents = plus d'appels `run_agent`, donc plus de crédits.
