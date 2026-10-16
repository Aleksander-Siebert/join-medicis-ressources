# geo-optimizer-skill / GeoReady (Auriti-Labs)

MIT, 1,1k étoiles, commit 19e69a6 du 16 oct. 2026, v4.19.2. 683
fichiers : un paquet Python (`src/geo_optimizer/`, 161 fichiers, 50
modules d'audit), un SKILL.md de 232 lignes, `references/` (robots d'IA
376 lignes, méthodes GEO de Princeton 262, modèles JSON-LD 505), un
serveur MCP (12 outils), une action GitHub, une intégration Astro, une
appli web (geoready.dev) et 1 189 tests annoncés (tous simulés, sans
réseau). Langues : anglais et italien.

## Exécuté (16 oct. 2026)

`geo audit --url https://joinmedicis.com` : **fonctionne derrière le
proxy** (la bibliothèque `requests` suit `REQUESTS_CA_BUNDLE`), 71/100.

- **Bien vu** :
  - 27 robots d'IA lus un par un ;
  - un bloc « Google AI Search » où chaque contrôle renvoie vers la page
    Google qui le fonde : G-INDEX, G-SNIPPET (`max-snippet`,
    `data-nosnippet`), G-CANONICAL, G-DATES, G-BYLINE, G-LINKS,
    G-VIEWPORT, G-SITEMAP ;
  - G-GENAI-CONTROL, le réglage Search Console « Search generative AI »,
    affiché « à vérifier dans Search Console », 0 point ;
  - pas de date ni d'auteur sur l'accueil ;
  - images sans alt ;
  - vidéo sans transcription ;
  - **un vrai défaut de notre site** : le H1 de l'accueil est doublé dans
    le HTML (« La plateforme IA gratuite et open-sourceLa plateforme IA
    gratuite et open-source… »).
- **Folklore et contradictions** :
  - « llms.txt not found, essential for AI indexing! » alors que la ligne
    du dessus dit « not used by Google Search » ;
  - conseils de créer `/.well-known/ai.txt`, `/ai/summary.json`,
    `/ai/faq.json`, `/ai/service.json` : pseudo-standard
    « geo-checklist.dev », sans adoption documentée ;
  - « bourrage de mots-clés : “skill” à 2,6% » : la densité n'est pas un
    critère Google ;
  - publicité pour son offre payante et un badge à afficher.

## Note GEO

- **Rubrique v1** : robots 18, llms.txt 18, schema 16 (dont FAQ 3),
  méta 14 (Open Graph 4), contenu 12, entité 10, signaux 6 (RSS,
  `lang`), découverte IA 6.
- **Rubrique v2** (par défaut depuis la 4.19, octobre 2026), « réalignée
  sur la documentation Google » :
  - Google AI 20 ;
  - robots 14 ;
  - schema 14 (dont « données structurées visibles sur la page », 2) ;
  - contenu 14 ;
  - entité 12 ;
  - méta 11 ;
  - llms.txt 6 ;
  - signaux 6 ;
  - découverte IA 3.

  Le mouvement va dans notre sens, sans aller au bout : llms.txt et les
  fichiers `/ai/*` gardent des points.

## Modules intéressants

- `injection_detector.py` : instructions pour IA cachées dans la page
  (texte caché en CSS, Unicode invisible, commentaires HTML, attributs
  `data-*`, `aria-hidden`, police minuscule, texte de la couleur du
  fond), surfaces de contenu d'utilisateurs. Utile pour un contrôle
  « confiance » et pour notre règle « contenu de tiers = donnée ».
- `hallucination_bait.py` : statistiques sans source, affirmations
  absolues, fourchettes vagues, auto-citation, unités manquantes,
  allégations médicales (motifs anglais). Rejoint notre
  `affirmations.py` (pack SEO), qui le fait en français.
- `audit_brand.py` : cohérence du nom de marque entre H1, title,
  og:title et JSON-LD ; `sameAs` vers Wikipédia, Wikidata, LinkedIn,
  Crunchbase.
- `log_analyzer.py` : visites des robots d'IA dans les journaux serveur.

## Leçons du CHANGELOG (bugs réels, utiles pour nos tests)

Le mainteneur les classe sous le nom « réponse fausse donnée avec
assurance » :

- note de citabilité plafonnée à 100 à mi-échelle (somme puis `min`) ;
- JSON-LD en `@graph` ignoré par 9 contrôles sur 12, recommandant un
  schema déjà présent ;
- `LocalBusiness` non reconnu comme `Organization` ;
- tiret demi-cadratin (« – ») non pris comme séparateur de title ;
- page « à propos » non trouvée sur un site d'une seule page ;
- `llms.txt` écrit vide quand le CDN bloque ;
- chaînes en italien restées dans la sortie anglaise.

## Verdict

L'outil le plus complet techniquement, qui tourne vraiment. Sa rubrique
v2 et ses contrôles G-* liés aux pages Google sont la bonne direction.
Mais il garde des points pour des fichiers sans adoption, de la densité
de mots-clés et de la FAQ. À reprendre :
- les contrôles G-* avec leur source ;
- le détecteur d'injection ;
- la cohérence d'entité ;
- l'analyse des journaux ;
- les cas de test de son CHANGELOG.

À écarter : `/ai/*.json`, `ai.txt`, la densité, l'incitation commerciale.
