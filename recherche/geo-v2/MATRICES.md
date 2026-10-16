# GEO v2 · matrices de capacités et comparaison avec la v1

16 octobre 2026. Fondé sur les notes `notes/00` à `notes/10` :
- 12 dépôts clonés et lus fichier par fichier ;
- 6 outils lancés sur un vrai site, 4 suites de tests exécutées ;
- les faits revérifiés aux sources primaires (note 09).

**Aucun Skill n'est écrit avant ta validation.**

Légende des verdicts :
- **reprendre** : idée juste, réécrite en français ;
- **améliorer** : idée juste, exécution à refaire ;
- **écarter** : avec la raison.

Sources :
- `gsc` geo-seo-claude ;
- `cs` claude-seo ;
- `ms` marketingskills `ai-seo` ;
- `pf` Profound ;
- `go` geo-optimizer ;
- `gtm` gtm-engineer-skills ;
- `gs` geo-score ;
- `el` elmo ;
- `am` aaron-marketing-skills ;
- `usg` ultimate-seo-geo ;
- `sr` SE Ranking ;
- `P` source primaire (note 09) ;
- `v1` notre pack actuel.

## 1. Ce que la dissection montre

1. **La recherche a changé la doctrine depuis notre v1.**
   - Deux travaux de 2025-2026 concluent que les réécritures « pour être
     cité » n'ont pas d'effet stable sur les modèles actuels :
     C-SEO Bench (NeurIPS 2025) et une revue de 45 études (juillet 2026).
   - Ce qui marche est surtout le SEO classique : être récupéré et bien
     placé dans le contexte.
   - Google dit la même chose dans son guide (10 juillet 2026) : ne pas
     découper, ne pas réécrire pour l'IA, ni llms.txt ni schema spécial.

   Notre v1 promet encore trop avec la citabilité et les « méthodes
   validées par la recherche ».
2. **La mesure est le vrai manque, chez nous comme chez presque tous.**
   Les meilleures références (`el`, `pf`, `ms`, `gs`, `usg`) convergent :
   - des taux sur des passages répétés, pas des captures ;
   - une marge d'erreur, et chaque moteur à part ;
   - un portefeuille de prompts figé, avec des témoins ;
   - l'échelle cité, mentionné, recommandé ;
   - pas de note composite pour la visibilité.

   Notre `/geo-visibility` calcule un « rang » et une part de voix sans
   échantillon ni marge.
3. **Personne ne mesure en français.**
   - geo-score sort de son calcul deux contrôles sur notre site, faute de
     « lexique fr ».
   - geo-optimizer ne parle qu'anglais et italien.
   - Les motifs de faits de marque d'`usg` sont anglais.
   - Tavily a répondu en anglais à une question française.

   Notre avantage durable est le même qu'au pack SEO : des contrôles qui
   comprennent le français, et le droit français.
4. **Les faits bougent vite, et la v1 a déjà vieilli.**
   - Mistral a trois robots.
   - Search Console a un réglage d'inclusion (31 août 2026) et un rapport
     de performance IA générative.
   - Bing a un rapport « AI Performance ».
   - Les résultats FAQ ont disparu le 7 mai 2026.
   - Il faut une table des robots datée, notée par source, avec une
     procédure de mise à jour (`cs`), et des tests qui gardent les
     affirmations (`cs`).
5. **Notre v1 a un bug** de « réponse fausse donnée avec assurance » :
   `crawlers.py` prend une erreur réseau pour un robots.txt absent (donc
   « tout permis »), et lit robots.txt avec la première règle au lieu de
   la plus longue. Notre `robots.py` du pack SEO fait juste.

## 2. Comparaison honnête avec la v1

| Skill v1 | Ce qu'il fait déjà bien | Ce qui lui manque |
|---|---|---|
| `/geo-audit` | score partiel honnête (catégories non mesurées « à évaluer »), plan classé | diagnostic par couche (`pf`) au lieu d'une moyenne pondérée sans base causale ; note déterministe séparée du jugement (`gtm`) ; contrôles d'éligibilité Google liés à leur page (`go`) ; réglage Search Console ; « non mesuré = hors du dénominateur, et pourquoi » (`gs`) |
| `/geo-crawlers` | rôles des robots justes | bug réseau → « absent » ; RFC 9309 ; Mistral ×3, OAI-AdsBot, Applebot ; appel avec le vrai user-agent pour voir un pare-feu (`el`, `gs`) ; bloc Cloudflare (`gsc`) ; Content-Signal (`cs`, `P`) ; `nosnippet` / `max-snippet` / `data-nosnippet` ; table datée |
| `/geo-visibility` | prompts en français par persona, réponses collées, part de voix | passages répétés, taux avec n et intervalle (`el`, `usg`) ; cohortes et témoins (`ms`) ; échelle à 4 niveaux (`ms`, `el`) ; classes de sources (`pf`) ; comparaison de périodes « changement détectable ou non » ; connecteurs (Search Console, Bing) ; option Tavily |
| `/geo-citability` | lit le français (définitions, euros, « selon ») | promet la citation alors que les réécritures n'ont pas d'effet démontré (`P`) ; à recadrer en contrôle de clarté et de gain d'information |
| `/geo-optimize` | trois piliers, refus des tactiques douteuses | « méthodes validées » et priorités par plateforme sans source primaire ; pas de diagnostic par couche ; pas de familles de faits (`pf`) |
| `/geo-mentions` | sources que lisent les IA, cadre français des avis, pas d'astroturfing | partir des **sources réellement citées** sur les prompts perdus (`el`, `pf`) au lieu d'une liste générale ; cohérence des profils (`ms`) ; cité mais pas recommandé (`ms`) ; Wikidata par API (`gsc`) |
| `/geo-schema` | JSON-LD rempli avec du vrai et visible | cohérence du nom de l'entité entre H1, title, og:title, JSON-LD (`go`) ; `sameAs` qui répondent (`gs`) ; balisage = contenu visible (`go`, `P`) ; FAQ sans résultat enrichi depuis mai 2026 |
| `/geo-agentic` | 8 contrôles d'accessibilité, renvoi à Lighthouse | matrice datée des agents (`cs`) ; Content-Signal ; négociation Markdown non notée (`gsc`) ; détecteur d'instructions cachées (`go`) |

**Rien de la v1 ne vérifie l'exactitude** de ce que les IA disent de la
marque (prix, garanties, délais). C'est pourtant le cas le plus concret
pour un marketeur (« ChatGPT donne notre ancien tarif »), et le plus
fort en YMYL. `ms`, `pf`, `el` et `usg` le traitent.

## 3. Périmètre proposé (à valider)

8 Skills, comme la v1, mais plus profonds et réorganisés autour de la
mesure. Chacun avec SKILL.md, `references/`, script testé, cas
d'évaluation.

| Skill v2 | Remplace | Ce qu'il fait | Script |
|---|---|---|---|
| `/geo-audit` | `/geo-audit` + `/geo-optimize` | diagnostic par couche (accès, récupération, prêt à citer, marque et récit, écosystème, résultat), plus petite intervention crédible, plan daté avec mesure avant / après | `audit.py` (orchestre, note de préparation déterministe, non mesuré hors du dénominateur) |
| `/geo-acces` | `/geo-crawlers` | qui peut lire et utiliser le site : robots par rôle (recherche, utilisateur, entraînement, jeton), RFC 9309, vrai user-agent, pare-feu, Cloudflare, Content-Signal, `nosnippet`, rendu serveur, réglage Search Console, llms.txt rapporté sans poids ; propose un robots.txt par stratégie | `acces.py` (reprend `robots.py` du pack SEO) |
| `/geo-visibilite` | `/geo-visibility` | portefeuille de prompts français (cœur figé, exploratoire, témoins), grille de passages, taux par moteur avec intervalle, échelle récupéré / cité / mentionné / recommandé, part de voix face à un jeu figé, classes de sources citées, comparaison de périodes | `visibilite.py` v2 (+ `sources.py` pour classer les domaines) |
| `/geo-exactitude` | nouveau | registre de ce que les IA disent de la marque : 7 verdicts, gravité, source probable, à corriger d'abord à la source ; compare aux données `LIVE` de `site-context.md` | `exactitude.py` (phrases qui nomment la marque, motifs français : prix en euros, délais, « fondée en », garanties) |
| `/geo-contenu` | `/geo-citability` | page par page : réponse en tête, phrases autonomes, faits sourcés, gain d'information, couverture des **familles de faits** que les moteurs vont chercher ; ni découpage ni réécriture « pour l'IA » | `contenu.py` (citabilité v1 + lexiques français de question, de source, de définition) |
| `/geo-mentions` | `/geo-mentions` | à partir des sources citées sur les prompts perdus : quels sites tiers comptent, profils incohérents, cité mais pas recommandé, plan de mentions légitimes, lignes rouges du droit français | `sources.py` partagé, Wikidata par API |
| `/geo-entite` | `/geo-schema` | l'entité de la marque : nom cohérent partout, `sameAs` qui répondent, Wikidata, JSON-LD vrai et visible ; produit le bloc à coller | `entite.py` |
| `/geo-agentic` | `/geo-agentic` | agents qui naviguent et agissent : accessibilité, stabilité, politique d'accès, Markdown et WebMCP en option, instructions cachées | `agentic.py` v2 |

Socle commun (`geo-skills/commun/`) :
- `regles.md` et `preuves.md`, avec la table datée des robots et des
  faits Google ;
- `lexiques_fr.json` : question, source, définition, marqueurs de
  recommandation (« je recommande », « à éviter ») ;
- `stats.py` : intervalle de Wilson, test de différence entre deux
  périodes ;
- **tests qui gardent les affirmations**, par exemple « aucun Skill ne
  dit que GPTBot sert à la recherche ChatGPT ».

## 4. Matrices par Skill

### `/geo-audit`

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Diagnostic dans l'ordre accès → récupération → prêt à citer → marque → écosystème → résultat ; « un échec à une couche ne justifie pas une réécriture à une autre » | `pf` aeo-operator | reprendre | sortie en français, une ligne par couche avec sa preuve |
| Note déterministe figée (script) + note de jugement sur grille courte avec justification | `gtm` | reprendre | la note de jugement reste sur 6 critères 0-5, chacun avec la phrase lue |
| Non mesuré = hors du dénominateur, avec la raison | `gs`, `v1` | reprendre | déjà dans v1 ; ajouter la raison |
| Contrôles d'éligibilité Google liés à la page Google (indexable, extrait autorisé, canonical, dates, auteur, liens explorables) | `go` (G-*), `P` | reprendre | lien vers la page Google en français quand elle existe |
| Réglage Search Console « IA générative » à vérifier | `P`, `go` | reprendre | instruction pas à pas, « non mesurable de l'extérieur » |
| Note GEO pondérée (citabilité 25, marque 20…) | `gsc`, `v1` | **écarter** | aucune base causale ; Google : aucun outil n'a ses signaux |
| Score sur 100 « seulement si utile à la communication » | `pf` | améliorer | note de **préparation** (mesurable), jamais mélangée à la visibilité |
| Plus petite intervention crédible, journal avant / après, arrêt si sans effet | `pf`, `el`, notre `positions.py` | reprendre | même mécanique que `/seo-refresh` |
| Livrables d'agence (PDF, proposition, CRM) | `gsc` | écarter | règle : texte simple, rien envoyé à la place de l'utilisateur |

### `/geo-acces`

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Robots par rôle (recherche, utilisateur, entraînement, jeton sans robot) | `cs`, `el`, `P` | reprendre | table datée avec la source de chaque ligne ; Mistral ×3 |
| Lecture RFC 9309 (règle la plus longue, Allow à égalité, 5xx = tout interdit) | `cs`, notre `robots.py` | reprendre | corrige le bug v1 |
| Appel avec le vrai user-agent pour voir pare-feu et CDN | `el`, `gs` | reprendre | « refusé au robot mais pas au navigateur » = à confirmer, jamais conclu seul |
| Bloc robots.txt géré par Cloudflare | `gsc` | reprendre | explication du réglage Cloudflare |
| Content-Signal (`search`, `ai-input`, `ai-train`) | `cs`, `P` | reprendre | non noté ; « préférence, pas contrôle d'accès » ; directive UE 2019/790 art. 4 |
| `noindex`, `nosnippet`, `max-snippet`, `data-nosnippet`, `X-Robots-Tag` | `go`, `P` | reprendre | « extrait interdit = pas d'Aperçus IA » (condition Google) |
| Contenu principal dans le HTML serveur | `gs`, `el`, `v1` | reprendre | mots visibles comptés |
| llms.txt : présence rapportée, poids nul ; utile pour une documentation lue par des agents de code | `cs`, `P` | reprendre | Google dit l'ignorer (10 juil. 2026) |
| `ai.txt`, `/ai/*.json` | `go` | écarter | aucune adoption documentée |
| robots.txt proposé par stratégie (visibilité, équilibre, refus de l'entraînement) | `v1`, `cs` | améliorer | chaque ligne dit ce qu'elle change, jamais « bloquer les IA » en bloc |
| Changements à risque confirmés avant de donner le code | `usg` | reprendre | robots.txt, noindex |

### `/geo-visibilite`

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Portefeuille depuis la demande réelle (requêtes longues Search Console, appels, tickets, forums) | `el`, `ms`, `pf` | reprendre | prompts écrits comme on parle en français, pas traduits |
| 70 à 85% de prompts sans la marque, 2-3 formulations par intention clé | `el` | reprendre | |
| Cœur figé versionné, exploratoire, **témoins** | `ms`, `pf` | reprendre | témoins types fournis (nom de marque, catégorie sans rapport) |
| 5 / 10 / 15 passages (explorer, confirmer, affirmer) | `el` (préprint) | reprendre | marqué « repère, préprint » |
| Taux avec intervalle de Wilson, marge, « pas de changement détectable » | `el`, `usg` | reprendre | **script** `stats.py`, testé |
| Échelle récupéré / cité / mentionné / recommandé, et « déconseillé » | `ms`, `el` | reprendre | marqueurs français de recommandation et de mise en garde |
| Part de voix face à un jeu de concurrents figé et nommé | `el`, `v1` | améliorer | |
| Rang moyen, note composite | `v1`, divers | **écarter** | instable (`el`, SparkToro) |
| Classes de sources citées (propre site, concurrent, presse, institution, social, annuaire, autre) | `pf`, `el` | reprendre | **script** `sources.py`, domaines français types (presse, comparateurs, annuaires) |
| API ≠ appli grand public, à étiqueter | `el`, `gs` | reprendre | |
| Étiquette de chaque chiffre (mesuré n, première partie, publié, estimé) | `el`, `am` | reprendre | |
| Données : rapport Search Console IA générative, rapport « AI Performance » de Bing, exports Peec, Otterly, Profound, SE Ranking | `P`, `sr`, `ms` | reprendre | **mode gratuit par défaut** : réponses collées ; détails Search Console **[à vérifier]** |
| Test automatique par Tavily sans clé | `am` | à trancher (§6) | une approximation, pas ChatGPT ; requête envoyée à un tiers |

### `/geo-exactitude` (nouveau)

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Registre des affirmations (moteur, date, prompt, phrase, type, verdict, preuve, source probable, gravité, responsable) | `ms`, `pf` | reprendre | format texte stable, comparable d'un mois sur l'autre |
| 7 verdicts (exact, incomplet, ambigu, périmé, faux, opinion présentée comme un fait, invérifiable) | `ms` | reprendre | |
| Vérifier les faits de la marque dans les phrases qui la nomment, faits par segment | `usg` | améliorer | **en français**, depuis les données `LIVE` / `À CONFIRMER` / `RETIRÉ` de `site-context.md` |
| Réponse sans citation = données d'entraînement, change au prochain modèle | `el` | reprendre | |
| Corriger la source d'abord (page qui doit porter le fait, profils tiers) | `ms`, `pf`, `el` | reprendre | YMYL : priorité aux prix, garanties, délais, conditions |

### `/geo-contenu`

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Réponse en tête, phrase autonome, fait sourcé | `gsc`, `ms`, `v1` | améliorer | présenté comme clarté pour le lecteur, sans promesse de citation |
| Gain d'information, contenu de première main | `P` (Google), `ms` | reprendre | `reserve.md` partagée avec LinkedIn et SEO |
| Familles de faits que le moteur va chercher (entités, sous-questions, critères, contraintes), une page forte plutôt qu'une page par requête dérivée | `pf` | reprendre | « déduit » si non observé |
| Titre qui correspond à la requête dérivée | `el` (Ahrefs) | reprendre | marqué « étude d'éditeur, corrélation » |
| Lexiques français : question, source, définition | `gs` (manque), `v1` | améliorer | **notre apport** |
| Gains par méthode de Princeton (+40%…), blocs de 40-60 ou 134-167 mots, « 2 000 mots » | `ms`, `gsc`, `gtm` | **écarter** | non reproduits sur les modèles actuels ; Google : pas de longueur idéale |
| « Suggérer des statistiques à ajouter » | `gsc` | écarter | règle zéro invention, `{{à compléter}}` |
| « Urgence », superlatifs, « n°1 » | eGEO | écarter | ton et Code de la consommation |

### `/geo-mentions`

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Partir des sources citées sur les prompts perdus (« cette liste est le plan ») | `el`, `pf` | reprendre | depuis `sources.py` |
| Cité mais pas recommandé ; le guide qui se classe premier | `ms` | reprendre | étude citée **[à vérifier]** |
| Profils tiers alignés sur la page « à propos » | `ms` | reprendre | annuaires et comparateurs français |
| Note d'autorité YouTube 25%, Reddit 25%… | `gsc` | écarter | corrélations d'éditeur, pas de base causale |
| Lignes rouges : faux avis, avis non vérifiés présentés comme vérifiés, mentions non déclarées | `el`, `ms`, `P` | reprendre | **droit français** : L111-7-2, D111-16 s., L121-4 27° et 28°, loi influence 2023 |

### `/geo-entite`

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Nom de marque cohérent entre H1, title, og:title, JSON-LD (séparateurs « – », « — », « \| ») | `go` | reprendre | cas du CHANGELOG de `go` en tests |
| `sameAs` qui répondent, Wikidata par API | `gs`, `gsc` | reprendre | |
| JSON-LD vrai et visible, `@graph` lu, `LocalBusiness` = `Organization` | `go`, `P` | reprendre | cas de test |
| Schema FAQ ou HowTo « pour l'IA » | `ms`, `sr`, `am` | écarter | Google : aucun schema propre à l'IA ; FAQ sans résultat enrichi depuis le 7 mai 2026 |

### `/geo-agentic`

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| 8 contrôles d'accessibilité et de stabilité | `v1`, `cs` | reprendre | |
| Matrice datée des agents et de leur lecture (arbre d'accessibilité, DOM, captures) | `cs` | reprendre | notée P/S |
| Instructions cachées pour IA dans la page (texte caché, Unicode invisible, commentaires, `aria-hidden`) | `go` | reprendre | contrôle « confiance », motifs français |
| Négociation Markdown, `Link` RFC 8288, WebMCP | `gsc`, `cs` | reprendre | non notés ; « absence normale = ne pas en parler » |
| Test du pare-feu avec des user-agents d'IA | `cs` | reprendre | seulement avec l'accord du propriétaire du site |

## 5. Écartés, une fois pour toutes

- **Note GEO composite** mêlant préparation, citabilité et visibilité.
- **Gains chiffrés « garantis »** :
  - Princeton par méthode ;
  - multiplicateurs « 4,8× », « +156% » ;
  - corrélations d'éditeur présentées comme des causes.
- **Fichiers sans adoption** comme leviers : llms.txt noté,
  `ai.txt`, `/ai/*.json`, `pricing.md`.
- **Schema FAQ ou HowTo « pour l'IA »** ; densité de mots-clés.
- **« Infiltration »** de Reddit ou Quora, faux avis, Wikipédia créée
  par la marque.
- **Livrables d'agence** (PDF, CRM, proposition commerciale) et
  **incitations commerciales** d'outils.

## 6. Questions à trancher

1. **Les 8 Skills et leurs noms.**
   - `/geo-crawlers` devient `/geo-acces`, `/geo-schema` devient
     `/geo-entite`, `/geo-citability` devient `/geo-contenu`,
     `/geo-optimize` entre dans `/geo-audit`, et `/geo-exactitude` est
     nouveau.
   - Le site garde des redirections depuis les anciennes fiches.
   - Tu valides, ou tu préfères garder les anciens noms ?
2. **La note.** Je propose :
   - une note de **préparation** sur 100, mesurée par script, avec les
     contrôles non mesurés sortis du calcul ;
   - des **taux de visibilité** à part, jamais additionnés à la note.

   On abandonne la note GEO globale de la v1. D'accord ?
3. **Tavily** (test automatique sans clé, réponse d'IA avec sources) :
   - **pour** : gratuit, automatisable, le seul moyen de mesurer sans
     coller les réponses à la main ;
   - **contre** : ce n'est ni ChatGPT ni Perplexity, la requête part chez
     un tiers, et la réponse est arrivée en anglais à une question
     française.

   Je propose de l'offrir **en option**, étiqueté « approximation ».
   Oui ou non ?
4. **`/geo-exactitude` en Skill séparé**, ou intégré à `/geo-visibilite` ?
   Je le propose séparé : c'est un usage distinct (« ChatGPT dit un faux
   prix ») et fort en YMYL.
5. **L'éval à l'aveugle.** Il me faudrait 2 ou 3 cas réels :
   - un site ;
   - 10 à 20 questions qu'un client poserait à une IA ;
   - si possible, quelques réponses de ChatGPT, Perplexity ou Gemini
     collées.

   Les noms resteront anonymisés dans le dépôt, comme pour l'éval SEO.

## 7. À signaler hors chantier

- **joinmedicis.com** : le texte du H1 de l'accueil apparaît deux fois
  dans le HTML (« La plateforme IA gratuite et open-sourceLa plateforme
  IA gratuite et open-source… »), vu par geo-optimizer le 16 oct. 2026.
  Probablement une version mobile et une version bureau du même titre.
  À corriger sur le site.
- geo-score liste des fiches LinkedIn du sitemap non liées depuis le HTML
  serveur des pages qu'il a lues : à regarder avec `/seo-maillage`.

## 8. Décisions de l'utilisateur (16 octobre 2026)

1. Les 8 Skills et leurs noms : **validés**.
2. Note de préparation sur 100 et taux de visibilité à part : **validé**
   (« je te fais confiance »).
3. Tavily : **option désactivée par défaut**, sur ma recommandation. Le
   mode normal reste les réponses collées. Tavily seulement à la demande,
   chaque résultat étiqueté « approximation, moteur Tavily », jamais
   mélangé aux réponses collées, avec l'avertissement que la requête part
   chez un tiers.
4. `/geo-exactitude` en Skill séparé : **validé**.
5. Éval à l'aveugle sur **un site e-commerce de produits reconditionnés
   fourni par l'utilisateur** ; les questions sont générées par Claude.
   Dans le dépôt, le site reste anonymisé, comme pour l'éval SEO.

Skill modèle : `/geo-visibilite` (le cœur de la mesure, le plus gros
écart avec la v1). L'utilisateur le relit avant les 7 autres.
