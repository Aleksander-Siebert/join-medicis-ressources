# geo-seo-claude (Zubair Trabzada) · dissection

MIT. Dernier commit le 5 oct. 2026. Orchestrateur `geo/SKILL.md`,
15 sous-Skills, 5 agents, 5 scripts Python (2 508 lignes), modèles
JSON-LD par type d'activité, application Flask de CRM, rapport PDF,
« marque blanche » pour agences. Tests : 2 fichiers (SSR, robots.txt
Cloudflare) et un compte rendu manuel sur 6 sites.

**Positionnement** : « GEO d'abord, SEO en appui », pensé pour une agence
qui vend des audits (Skills `geo-prospect`, `geo-proposal` avec projection
de ROI et grille tarifaire, `geo-compare` mensuel pour le client, CRM). La
dissection complète des volets IA ira au chantier GEO v2 ; ici, ce qui
sert le pack SEO.

## Ce qui est lu et ce qu'il fait

- `geo-audit` : type d'activité détecté (SaaS, local, e-commerce, éditeur,
  agence), jusqu'à 50 pages depuis le sitemap ou par liens (2 niveaux,
  30 s par page, robots.txt respecté), 5 agents en parallèle, **note GEO**
  (citabilité 25, autorité de marque 20, E-E-A-T 20, technique 15,
  schema 10, plateformes 10), gravités Critique à Basse, plan à 30 jours.
- `geo-technical` : 8 catégories notées sur 100 (exploration 15,
  indexabilité 12, sécurité 10, URL 8, mobile 10, CWV 15, **rendu serveur
  15**, vitesse 15) + une catégorie **non notée** de préparation des agents
  (en-têtes `Link` RFC 8288, négociation Markdown) avec une bonne règle :
  « absence normale sur un site d'entreprise ordinaire = ne pas en
  parler ».
- `geo-content` : grille E-E-A-T sur 100 avec points par signal
  (« récit à la première personne précis 5, générique 3, absent 0 »…),
  liste des signes de contenu IA pauvre et des signes de qualité « quel
  que soit le mode de production », fraîcheur par paliers, modificateur
  d'autorité thématique (+10 à -5).
- `geo-schema` : détection, validation, stratégie `sameAs` pour l'entité,
  génération depuis `schema/*.json`.
- `geo-crawlers`, `geo-llmstxt`, `geo-citability`, `geo-brand-mentions`,
  `geo-platform-optimizer` : volet IA, pour GEO v2.
- `geo-report`, `geo-report-pdf`, `geo-compare`, `geo-proposal`,
  `geo-prospect`, `geo-update` : livrables d'agence. Écartés (notre règle :
  texte simple par défaut, rien d'envoyé à la place de l'utilisateur).

## Scripts exécutés (12 oct. 2026)

`citability_scorer.score_passage` sur **le même passage factuel**, en
français puis en anglais (définition + « en 2025, Assurly a indemnisé
1 240 sinistres en 19 jours en moyenne ») :

| langue | note | réponse | densité statistique |
|---|---|---|---|
| français | **30/100 (F)** | 6/30 | 2 |
| anglais | **49/100 (D)** | 30/30 | 2 |

Les motifs de définition sont anglais (« is a », « refers to ») : un texte
français perd 19 points pour rien. La densité statistique reste à 2 malgré
trois nombres. Le « bon » passage est fixé à **134-167 mots**, chiffre tiré
d'une étude d'éditeur et contredit par Google (pas de découpage pour l'IA).
Les autres scripts (`fetch_page`, `brand_scanner`, `llmstxt_generator`)
exigent un accès réseau direct.

## Erreurs et folklore relevés

- **Gravités fausses** : « pas de llms.txt » classé **Haute** (Google dit
  que Search l'ignore) ; « absence totale de données structurées »
  classée **Critique** ; « FAQ schema manquant » en Moyenne alors que les
  résultats FAQ sont retirés ; GPTBot et ClaudeBot (robots
  d'entraînement) bloqués classés Haute pour la visibilité, ce qui
  confond entraînement et citation (claude-seo traite ce point
  correctement).
- « Googlebot dépriorise le contenu JS, indexation retardée de jours ou de
  semaines » **[à vérifier : Google a communiqué des délais de rendu
  courts]**.
- « +30 à 115% de visibilité » (étude GEO 2024) présenté comme un résultat
  général.
- Compte rendu de test : la clé Content-Signal `ai-input` notée
  « inconnue », alors qu'elle fait partie des trois clés de la politique
  Content Signals de Cloudflare (`search`, `ai-input`, `ai-train`)
  **[à vérifier à la source]**.
- Fraîcheur : « sans date ou plus de 24 mois = critique » sans distinguer
  l'evergreen dans la note (le Skill le distingue seulement en texte).

## Ce qui vaut d'être repris

- Règle « non applicable = ne pas en parler » pour les signaux émergents.
- Rendu serveur vérifié par comparaison HTML brut contre DOM rendu, avec
  la liste de ce qui doit être dans le HTML brut (texte principal, titres,
  méta, canonical, JSON-LD, liens internes).
- Grille E-E-A-T **par signaux observables avec points** : plus
  reproductible qu'une note globale, à réécrire en français et en
  séparant ce qu'un script compte (auteur présent, date, sources
  liées) de ce que le jugement évalue.
- Signes de contenu IA pauvre « quel que soit le mode de production »
  (rejoint le guide Google « people-first »).

## Verdict

Source utile pour le volet technique et la grille E-E-A-T, mais nettement
moins rigoureuse que claude-seo sur les faits (llms.txt, FAQ, robots
d'entraînement). Ses scripts sont anglophones. Rien à copier tel quel ;
quelques idées à réécrire.
