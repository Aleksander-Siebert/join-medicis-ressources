# seomachine (TheCraigHewitt, à l'origine Castos) · dissection

MIT. Dernier commit le 6 oct. 2026. **Espace de travail de rédaction**
plutôt que pack de Skills : 24 commandes (`/write`, `/article`,
`/rewrite`, `/analyze-existing`, `/optimize`, `/cluster`,
`/research-*`, `/performance-review`, `/priorities`, `/scrub`,
`/landing-*`, `/publish-draft`…), 11 agents (éditeur, liens internes,
mots-clés, méta, titres, performance, CRO…), 24 modules Python
(12 495 lignes), 13 scripts de recherche à la racine, dossiers de
contexte (`brand-voice.md`, `writing-examples.md`, `style-guide.md`,
`seo-guidelines.md`, `internal-links-map.md`, `target-keywords.md`,
`competitor-analysis.md`), publication WordPress (REST + Yoast). Les
`.claude/skills/` sont une ancienne copie de marketingskills : ignorés.
Tests : 3 fichiers, **8 réussis**.

## Le flux de rédaction (`/write`, `/article`)

- Lit d'abord les fichiers de contexte de la marque (voix, exemples
  d'écriture, guide de style, mots-clés, carte des liens internes). C'est
  le même principe que notre `contexte.md` LinkedIn et que le Projet
  Claude de l'utilisateur : **à reprendre** (un `contexte-seo.md` avec
  persona, voix, exemples, pages piliers, liens prioritaires).
- **Réponse directe dans les 1-2 premières phrases**, puis accroche, puis
  « Agree, Promise, Preview ».
- **Bloc « À retenir »** de 3-5 puces après l'introduction, écrit après
  l'article pour qu'il soit exact.
- Vidéo YouTube intégrée (rejoint la tendance Marketer Milk demandée).
- Chaque fichier sauvegardé daté, puis enchaînement automatique : nettoyage,
  analyse de contenu, SEO, méta, liens internes, mots-clés, puis **boucle
  de qualité** (note composite ≥ 70 avant de livrer).

## Ce qui est dangereux

- **Mini-histoires obligatoires avec personnes et chiffres inventés** (« même
  fictifs : Sarah, Mike… » ; l'exemple invente un client, des montants, un
  partenariat perdu). Contraire à notre règle zéro invention, et grave en
  YMYL (assurance, finance, santé). **À écarter** : chez nous, une histoire
  vient de la réserve de preuves de l'utilisateur ou devient
  `{{à compléter}}`.
- Statistiques sans source dans les consignes : « 22× plus mémorisé »,
  « CTA intégrés +121% de conversions ».
- 2 000 mots minimum, densité 1-2%, mots-clés « LSI », Flesch 8e-10e
  année : folklore.
- `/scrub` présenté comme moyen de « faire paraître le contenu écrit par
  un humain » ; remplace le tiret cadratin par **des points-virgules**
  (contraire à la règle de l'utilisateur : virgule seulement).
- Projection de clics avec un **CTR fixe de 5,5%** et une courbe de CTR
  par position non sourcée (31,6% en position 1…) : prévision inventée.

## Scripts exécutés (12 oct. 2026)

- `content_scorer.py` : la commande documentée
  (`python data_sources/modules/content_scorer.py`) **plante** (import
  relatif) ; marche avec `PYTHONPATH`. Sur un article français de test
  contenant « Il est important de noter », « Dans un monde en constante
  évolution », « En somme » : **humanité 90/100**, « spécificité
  100/100 », conseil « utilise des contractions comme don't, can't »,
  Flesch 0, « allonge à 2 000 mots ». Inutilisable en français.
- NLTK tente de télécharger `cmudict` au premier lancement (refusé derrière
  un proxy) : dépendance réseau cachée.
- `research_quick_wins.py` : positions 11-20, 50 impressions minimum sur
  30 jours, enrichi par DataForSEO et GA4, puis note d'opportunité
  (volume 25, position 20, intention 20, concurrence 15, cluster 10, CTR 5,
  fraîcheur 5, tendance 5). Idée utile, données payantes obligatoires,
  projection inventée (voir plus haut).
- `research_topic_clusters.py` : **regroupe les requêtes Search Console du
  site** (TF-IDF + k-means, ou regroupement simple), note d'autorité par
  thème, trous par thème. Similarité de texte, que claude-seo déconseille
  pour décider d'une page, mais **l'idée de partir des requêtes réelles du
  site est la bonne** pour notre besoin « maillage par clusters d'un site
  existant ».

## Agents utiles

- `internal-linker` : emplacements (corps d'abord, une seule en
  introduction, 1-2 en conclusion), à éviter (plus de 1-2 liens par
  paragraphe, même lien répété, « cliquez ici »), formules d'ancre (exacte
  avec parcimonie, partielle par défaut, de marque), 3-5 liens par article,
  rayon → pilier obligatoire. Dépend d'une carte des liens tenue à la main.
- `editor`, `meta-creator`, `headline-generator`, `performance` : à
  relire au moment de la matrice du Skill de rédaction.
- `/research-ai-citations` : liste de plus de 100 prompts par catégorie
  pour tester sa présence dans les réponses d'IA (GEO v2).

## Verdict

Le meilleur **flux de rédaction de bout en bout** lu (contexte de marque,
brief, rédaction, contrôles, boucle de qualité, publication), mais bâti sur
des règles anglaises, des chiffres sans source et des histoires inventées.
À reprendre : l'enchaînement, les fichiers de contexte, la réponse directe,
le bloc « À retenir », la boucle de qualité avec seuil, le point de départ
« requêtes Search Console du site » pour les clusters. À écarter : tout le
reste des seuils et l'invention.
