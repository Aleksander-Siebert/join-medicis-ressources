# SEO v2 · matrices de capacités et comparaison avec la v1

12 octobre 2026. Fondé sur les notes `notes/00` à `notes/07` : 7 dépôts
clonés et lus fichier par fichier, scripts exécutés, 4 sources hors dépôts.
**Aucun Skill n'est écrit avant ta validation.**

Légende des verdicts : **reprendre** (idée juste, réécrite en français),
**améliorer** (idée juste, exécution à refaire), **écarter** (avec la
raison). Sources : `cs` claude-seo, `ms` marketingskills, `gsc`
geo-seo-claude, `sm` seomachine, `ss` superseo-skills, `ls`
localseoskills, `A` Agent A, `U` ton workflow, `G` guide Google, `MM`
Marketer Milk, `v1` notre pack actuel.

## 1. Ce que la dissection montre

1. **Personne ne mesure en français.** Les scripts de texte des
   références ratent tout dans un texte français (tests du 12 oct.) :
   - `cs content_quality` : 0 tic détecté ;
   - `cs content_verify` : 0 affirmation extraite ;
   - `gsc citability` : 30/100 en français contre 49/100 en anglais pour
     le même passage ;
   - `sm content_scorer` : « humanité 90/100 », et conseille des
     contractions anglaises.

   Notre avantage durable est là : des contrôles qui comprennent le
   français.
2. **Les meilleures références se sont trompées sur les faits.**
   - claude-seo a publié puis retiré un « watershed de décembre 2025 »
     inventé.
   - superseo a dû ajouter en septembre des règles « n'invente rien ».
   - geo-seo-claude classe encore l'absence de `llms.txt` en gravité
     haute.
   - seomachine impose des histoires avec des personnes inventées.

   Notre règle zéro invention, les faits datés et les sources primaires
   sont un vrai différenciateur, pas un détail.
3. **claude-seo est le plus profond techniquement** : il mesure beaucoup,
   s'appuie sur un registre daté des mises à jour Google, distingue
   chaque robot IA et refuse toute note sans mesure. Mais :
   - il est anglophone ;
   - il est lourd (19 agents, PDF) ;
   - ses scripts réseau échouent derrière un proxy local (cas de
     claude.ai et de Claude Code web).
4. **marketingskills et superseo ont le meilleur jugement éditorial** :
   - poussée des positions 8-20 avec règle d'arrêt ;
   - grille de couverture du rafraîchissement ;
   - discipline de preuve des comparatifs ;
   - local respectueux de la vie privée ;
   - interview courte ;
   - « une précision inventée est pire qu'une phrase générique ».
5. **Ton workflow reste la meilleure base de rédaction** :
   - persona ;
   - 4 cadres ;
   - YMYL sans hallucination ;
   - 3 phases avec validation du plan ;
   - éradication des signes d'IA.

   Aucune référence ne fait mieux sur le fond. Il lui manque surtout des
   contrôles automatiques.
6. **Notre v1 est honnête mais mince** :
   - 16 Skills, dont 11 sans aucun script ;
   - aucune référence ni aucun exemple réel pour la plupart ;
   - 41 tests ;
   - pas d'éval à l'aveugle.

   Elle n'atteint pas la barre S-tier de `CLAUDE.md`.

## 2. Comparaison honnête avec la v1

| Skill v1 | Ce qu'il fait déjà bien | Ce qui lui manque (face aux références) |
|---|---|---|
| `/seo-context` | fichier de contexte lu par tous, YMYL, règles maison | réserve de preuves de l'utilisateur (comme `/linkedin-interview`) ; règles d'entité de la marque ; préférence de longueur ; « leçons » datées et approuvées (`ls`) |
| `/seo-plan` | 4 phases, cibles fixées avec l'utilisateur, aucune promesse | options Marketer Milk pas encore intégrées ; arborescence type par secteur (`cs`) ; note de priorité des idées (`ms`) |
| `/seo-keywords` | une page par intention, recouvrement de SERP (7-10 / 4-6 / 2-3 / 0-1), aucun volume inventé | **aucun script** : ni cannibalisation depuis Search Console (requête sur 2+ pages), ni calcul du recouvrement, ni difficulté lue dans la SERP en mode gratuit (`ss`) |
| `/seo-serp` | consensus de type de page, concurrents /40, gain d'information, user stories | pas de script ; filtre des non-concurrents à la française ; signaux « ne pas tenter » (`ss`) ; grille de difficulté sans outil payant |
| `/seo-brief` | ton workflow (6 questions, 4 cadres, plan validé), règle de pertinence | test MECE **non mesuré** (couverture des requêtes, non-chevauchement) ; grille attendu / courant / distinctif / non couvert (`ms`) ; type de page confirmé contre la SERP (`ss`) |
| `/seo-write` | résumé de 3 lignes, voix active, zéro invention, sections interdites, bloc méta, contrôle qualité Google | **aucun contrôle automatique** des affirmations sans source, de la méta en pixels, des tics du lexique de ton workflow ; règle des 30% de première main (`ss`) ; interview courte (`ss`, `/linkedin-interview`) |
| `/seo-article` | chemin complet avec validations | étapes nommées et rejouables une à une (`A`) ; boucle de qualité avec seuil (`sm`) |
| `/seo-human` | profil article, Markdown préservé | moteur plus faible que l'humaniseur LinkedIn v2 (test du 12 oct. : « En somme » non vu, pas de paragraphe désigné, pas de contrôle de fidélité des faits) |
| `/seo-audit` | ordre d'analyse, `onpage.py` (≈20 points), CWV terrain/labo, images, bon type de page, « à mesurer » | JSON-LD absent du HTML brut déclaré « MANQUANT » (faux positif si injecté en JS, `ms`) ; robots IA par robot (`cs`) ; registre daté des mises à jour Google (`cs`) ; limites de récupération de Googlebot, rendu JS, signaux « non mesuré = non noté » ; méta gabarits entre pages ; temps jusqu'à la valeur (`ss`) |
| `/seo-drift` | photo avant/après, règles de gravité | comparer nos règles aux 17 de `cs` ; URL normalisée (UTM) |
| `/seo-maillage` | **déjà au-dessus des références** : sitemap, TF-IDF, liens existants exclus, trafic, phrase d'insertion, cannibalisation, 404 du sitemap | clusters depuis les **requêtes Search Console** partagées (`sm`) ; profondeur en clics ; diversité des ancres (≤ 40%, `cs`) ; classes cœur → lointain (`A`) ; premier lien contextuel rayon → pilier (`ss`) ; ordre de publication d'un nouveau cluster (`ss`) |
| `/seo-refresh` | 4 analyses, liste de modifications à accepter, date changée seulement si le contenu change | poussée 8-20 / clic faible / presque en tête avec **règle d'arrêt** et journal avant/après (`ms`) ; grille de couverture (`ms`) ; Garder / Réviser / Nouveau (`ms`, `A`) |
| `/seo-veille` | sitemaps concurrents, rapport mensuel, causes = hypothèses | corrélation avec le registre Google daté (`cs`) ; CTR attendu calculé sur le site ; l'IA propose, l'humain conclut (`A`) |
| `/seo-local` | type d'entreprise, 6 axes, annuaires français, droit des avis, test du remplacement | fiches en double (`ls`) ; vie privée de l'adresse (`ms`) ; deux surfaces séparées et observations datées (`ms`) ; contrôle NAP HTML / JSON-LD / fiche (`cs`) ; textes français à revérifier |
| `/seo-social` | YouTube, Pinterest, TikTok, LinkedIn, Discover, lien vers la page exacte | couche texte YouTube dans l'ordre de levier (`ms`) ; vidéo intégrée aux meilleurs articles en option (`MM`, `sm`) ; propriétés sociales dans Search Console **[à vérifier]** ; aucun script |
| `/seo-programmatic` | portes de qualité, test du remplacement | hors de ta liste de besoins ; candidat à devenir une option de `/seo-plan` |

Tests v1 : 21 + 9 + 11 = 41 au vert. Éval à l'aveugle : aucune (écrit dans
`evals/RESULTATS.md`).

## 3. Périmètre proposé (à valider)

Profondeur avant couverture : **14 Skills**, au lieu de 16, plus un socle
commun.

| # | Skill | Changement |
|---|---|---|
| | `commun/` | nouveau socle partagé, comme LinkedIn v2 :<br>- règles ;<br>- preuves datées SEO ;<br>- registre des mises à jour Google ;<br>- garde-fou anti-black hat |
| 1 | `/seo-context` | renforcé (réserve de preuves partagée) |
| 2 | `/seo-plan` | renforcé, **absorbe `/seo-programmatic`** comme option |
| 3 | `/seo-keywords` | script nouveau |
| 4 | `/seo-serp` | script nouveau |
| 5 | `/seo-brief` | script nouveau |
| 6 | `/seo-write` | 3 scripts nouveaux |
| 7 | `/seo-article` | orchestration en étapes rejouables |
| 8 | `/seo-human` | moteur LinkedIn v2, profil article |
| 9 | `/seo-audit` | **absorbe `/seo-drift`** (`audit photo` / `audit compare`) |
| 10 | `/seo-maillage` | script v2 |
| 11 | `/seo-refresh` | script nouveau |
| 12 | `/seo-veille` | script v2 |
| 13 | `/seo-local` | script nouveau |
| 14 | `/seo-social` | script nouveau |

Le SEO agentique reste `/geo-agentic` (pack GEO), et `/seo-audit` l'appelle.
C'est à trancher, voir section 6.

## 4. Matrices par Skill

### commun/ (socle)

| Fonction | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Règles du pack (lecture seule, données tierces = données, zéro invention, typo FR, texte simple) | `v1`, LinkedIn v2 | reprendre | un seul fichier propagé, comme `linkedin-skills/commun` |
| Preuves datées et classées (officiel, étude tierce, praticien, folklore) | LinkedIn v2, `cs` « non revérifié le… » | reprendre | chaque fait SEO avec source primaire et date de vérification ; folklore listé (densité, Flesch, minimums de mots, « title jamais sous 50 ») |
| Registre des mises à jour Google, URL Google par entrée, alerte de péremption, « coïncidence = hypothèse » | `cs seo_updates.py` | reprendre | registre réécrit et revérifié par nous, script sans dépendance, alerte au-delà de 60 jours |
| Garde-fou : refus du black hat (microsites IA, faux avis, PBN, cloaking, détournement du bouton retour) | `MM` 6, `G`, `cs` | reprendre | refus motivé avec la règle Google citée |
| Récupération web qui marche derrière un proxy, ou contenu collé à défaut | leçon des tests `cs` | améliorer | `HTTPS_PROXY` respecté ; repli « colle le HTML ou l'export » |
| Leçons proposées par l'agent, validées par l'humain, avec date de revérification | `ls lessons.md`, `apprentissages.md` v1 | reprendre | format commun avec LinkedIn |
| Coût annoncé avant tout connecteur payant | `cs dataforseo_costs.py` | reprendre | règle écrite, mode gratuit par défaut |
| 19 agents parallèles, rapports PDF, marque blanche, publicité de l'auteur | `cs`, `gsc` | écarter | lourd, hors règle « texte simple par défaut » |

### 1. /seo-context

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| Contexte persistant lu par tous, emplacement confirmé | `v1`, `ss write-content` | reprendre | |
| Persona, ton, YMYL, règles d'entité (« à Marque », pas « chez Marque »), référence locale à éviter | `U` | reprendre | modèle anonymisé Assurly |
| Préférence de longueur (défaut 1 000-1 500 mots, modifiable) | `U`, `G` (« pas de nombre de mots ») | améliorer | une préférence, jamais une règle de classement |
| Réserve de preuves (chiffres, cas, avis, erreurs) | `/linkedin-interview`, `ss expert-interview` | reprendre | **une seule réserve pour LinkedIn et SEO** (à trancher) |
| Pages à pousser, concurrents, outils connectés | `v1` | reprendre | |

### 2. /seo-plan

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| 4 phases, indicateurs avec point de départ mesuré, cibles fixées avec l'utilisateur | `v1`, `cs` | reprendre | |
| Arborescence type par secteur | `cs seo-plan/assets` | améliorer | sans minimums de mots ni « % unique » non sourcés |
| Note de priorité des idées (impact 40, adéquation 30, recherche 20, ressources 10) | `ms content-strategy` | reprendre | calcul par script ou à la lecture, poids modifiables |
| Options tendances 2026 : preuve sociale, recherche de marque associée, titles personnels, vidéo, pas tout sur l'IA, contenu vécu | `MM` | reprendre en **options** | chaque chiffre ou cas [à vérifier] |
| Programmatique : portes de qualité, test « publiable seul ? », lots de 50-100 | `cs`, `v1` | reprendre en option | absorbe `/seo-programmatic` |
| « Domain Authority » comme indicateur | `cs` | écarter | métrique d'outil tiers |

### 3. /seo-keywords

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| Une page par intention, 4 intentions, modificateurs | `v1`, `cs cluster`, `ms` | reprendre | modificateurs français |
| Recouvrement de SERP 7-10 / 4-6 / 2-3 / 0-1, bris d'égalité, domaines omniprésents retirés | `cs serp-overlap` | reprendre | **script** : calcule la matrice depuis des listes d'URL collées ou un export ; dit quand l'échantillon est trop bruité |
| Cannibalisation depuis Search Console (une requête, plusieurs pages) | `ms`, `sm` | améliorer | **script** sur l'export gratuit requête × page |
| Regroupement des requêtes réelles du site | `sm research_topic_clusters` | améliorer | par pages partagées, pas par similarité de texte |
| Difficulté lue dans la SERP (10 signaux, « ne pas tenter ») | `ss keyword-deep-dive` | reprendre | version française (Wikipédia, service-public.fr, ordres) ; « directionnel » écrit |
| Aucun volume sans source | `v1` | reprendre | |
| Courbe de CTR générique, projection de clics à 5,5% | `sm` | écarter | prévision inventée |

### 4. /seo-serp

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| Lecture à rebours, consensus > 60%, éléments de SERP, AI Overview et sources citées | `v1`, `cs sxo` | reprendre | |
| Décalage de type de page en premier (taxonomie 8 types, gravités) | `cs sxo` | reprendre | déjà partiel dans `v1 audit` |
| Filtre des non-concurrents | `cs content-brief` | reprendre | liste française |
| Concurrents /40, 3 types d'écart, priorité impact × avantage / effort | `cs`, `v1` | reprendre | |
| « Ne jamais déduire ce que couvre une page non lue » | `ss` (0.2.1), `cs` | reprendre | |
| Récits utilisateurs tirés de la SERP | `cs sxo`, `v1` | reprendre | |
| Personas déduits des annonces, notes sur 25 | `cs sxo` | écarter | fragile, peu utile au rédacteur |
| **Script** | nouveau | | `serp.py` : consensus de type, grille de difficulté et signaux « ne pas tenter » depuis un relevé collé |

### 5. /seo-brief

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| 6 questions une par une, 4 cadres, plan détaillé, validation | `U`, `v1` | reprendre | |
| Type de page annoncé et confirmé contre la SERP | `ss write-content` | reprendre | |
| **MECE mesuré** : chaque requête rattachée à une section, sections sans recouvrement | `U` (méthode CE/ME) | améliorer | **script** `couverture.py` : requêtes non couvertes, sections qui se recouvrent |
| Grille attendu / courant / distinctif / non couvert face à 5 concurrents | `ms content-refresh` | reprendre | même script |
| Information Gain non négociable, règle de pertinence, couverture du hub | `cs content-brief`, `ms` | reprendre | |
| Pas de nom de méthode ou d'outil dans le livrable | `cs` | reprendre | |
| Méta « jamais sous 50 / 130 », « Google tronque aux guillemets » | `cs` | écarter | folklore ; règle en pixels |
| Mode comparatif (X vs Y, alternatives) avec discipline de preuve | `cs competitor-pages`, `ms competitors` | reprendre comme **type de page** | cadre français de la publicité comparative [à vérifier] |

### 6. /seo-write

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| Plan validé obligatoire, persona, voix active, zéro modal (option), YMYL zéro hallucination | `U`, `v1` | reprendre | |
| Résumé de 3 lignes après l'intro | ta décision du 2 oct. | reprendre | |
| Réponse directe en tête de chaque H2 | `v1`, `sm`, `ss` | reprendre | |
| Interview courte (2-3 questions) si la réserve est vide | `ss`, `/linkedin-interview` | reprendre | |
| « Une précision inventée est pire qu'une phrase générique » ; 30% de première main | `ss` | reprendre | contrôle : part des paragraphes qui citent la réserve |
| **Affirmations sans source nommée** (%, €, délais, dates, « selon une étude ») | `cs content_verify` (anglais, bogué) | améliorer | **script** `affirmations.py` en français : une « étude récente » sans nom n'est pas une source |
| **Méta en pixels**, title qui recopie la description, mêmes formules sur plusieurs pages | `ms title-tags`, `cs metadata_template` | améliorer | **script** `meta.py` |
| Lexique et structures interdits de ton workflow | `U`, Wikipédia « Signs of AI writing » | reprendre | dans le moteur de `/seo-human` |
| Vidéo YouTube intégrée en option | `MM`, `sm` | reprendre en option | |
| Mention de l'usage de l'IA là où le lecteur la cherche | `G` | reprendre en option | |
| Histoires avec personnes inventées, densité 1-2%, 2 000 mots minimum, contractions | `sm`, `ss` | écarter | contraires à zéro invention et à `G` |

### 7. /seo-article

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| Chemin complet avec validations | `v1` | reprendre | |
| Étapes nommées, montrées, rejouables une à une | `A` | reprendre | |
| Boucle de qualité avec seuil avant livraison | `sm` | reprendre | seuil sur nos contrôles français |
| Exécution autonome : hypothèses écrites au lieu de bloquer | `ss` 0.2.1 | reprendre | |

### 8. /seo-human

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| Moteur LinkedIn v2 (marqueurs par paragraphe, fidélité des faits, score humain) | LinkedIn v2 | reprendre | profil « article » : Markdown, titres, listes, liens préservés |
| Caractères invisibles, typo française préservée | `v1`, `cs` | reprendre | test : ne jamais retirer l'espace fine avant `!` (bogue de `cs`) |
| Lexique de ton workflow + Wikipédia « Signs of AI writing » | `U` | reprendre | |
| « Faire paraître humain », tiret cadratin → point-virgule | `sm scrub` | écarter | promesse malhonnête ; ta règle : virgule seulement |

### 9. /seo-audit (absorbe /seo-drift)

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| Ordre d'analyse, gravités, « à mesurer » | `v1`, `ms` | reprendre | |
| **Non mesuré = non noté**, pas de note sans données | `cs` (technique, liens) | reprendre | |
| JSON-LD injecté en JS invisible au HTML brut | `ms` | reprendre | `onpage.py` : « absent du HTML brut, à vérifier rendu » au lieu de « MANQUANT » |
| Robots IA par robot, chaque affirmation sur son robot | `cs geo` | reprendre | **script** `robots.py` (sélection des groupes RFC 9309) |
| Faits techniques datés (limites de Googlebot, rendu JS, canonical, détournement du bouton retour, `nosnippet`) | `cs technical` | reprendre | revérifiés aux sources Google |
| Corrélation avec le registre Google | `cs` | reprendre | depuis `commun/` |
| Temps jusqu'à la valeur, fautes avec emplacement | `ss page-audit` | reprendre | dans `onpage.py` |
| Découverte du sitemap avant de le déclarer absent, `lastmod` suspect | `cs sitemap` | reprendre | |
| Photo avant / après (ex-`/seo-drift`) | `v1`, `cs drift` | reprendre | 17 règles de `cs` comparées aux nôtres |
| Agents parallèles, 500 pages, PDF | `cs` | écarter | échantillon raisonné + Screaming Frog si fourni |
| Note GEO avec llms.txt en gravité haute, FAQ manquant | `gsc` | écarter | faux |

### 10. /seo-maillage

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| Sitemap, TF-IDF, liens existants exclus, trafic, phrase d'insertion | `v1`, `A` | reprendre | |
| Clusters par requêtes Search Console partagées | `sm` | améliorer | export gratuit requête × page |
| Classes cœur → lointain par distance au centre du site | `A` | reprendre | heuristique sans dépendance |
| Profondeur en clics, orphelines, 3 liens entrants | `cs cluster`, `ms` | reprendre | |
| Diversité des ancres (une ancre ≤ 40% des liens vers une page) | `cs` | reprendre | |
| Premier lien rayon → pilier dans le corps | `ss` (avec la nuance de sa référence) | reprendre | |
| Ordre de publication d'un nouveau cluster | `ss` | reprendre | |
| Cannibalisation et décision fusionner / différencier / garder | `v1` | reprendre | |
| Carte HTML interactive | `cs` | écarter | texte simple par défaut ; option Mermaid |
| Nombre de mots pilier et rayons | `cs` | écarter | folklore |

### 11. /seo-refresh

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| Affirmations datées, écarts SERP, requêtes 5-20, maillage | `v1`, `A` | reprendre | |
| **Trois paniers** (8-20, clic faible, presque en tête) depuis Search Console | `ms rankings-push` | reprendre | **script** `positions.py` ; CTR attendu calculé sur le site |
| Diagnostic contre les 3 du dessus, plus petit changement | `ms` | reprendre | |
| Journal avant/après, 3-4 semaines, **arrêt après 2 tours sans effet** | `ms` | reprendre | dans `apprentissages.md` |
| Garder / Réviser / Nouveau, modifications acceptées une par une | `ms`, `A` | reprendre | |
| Date changée seulement si le contenu change | `G`, `v1` | reprendre | |

### 12. /seo-veille

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| Sitemaps concurrents, rapport mensuel deux exports | `v1`, `A` | reprendre | |
| L'IA propose 6-10 pistes, l'humain conclut | `A` | reprendre | |
| Corrélation avec le registre Google, « hypothèse jamais preuve » | `cs` | reprendre | |
| Requêtes de marque associées suivies | `MM` 2 | reprendre en option | |
| Rapport « Generative AI » de Search Console, erreur de journalisation des impressions 2025-2026 | `cs seo-google` | **[à vérifier]** | n'entre que revérifié aux sources Google |

### 13. /seo-local

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| Modèle d'activité (vitrine, zone, hybride, multi, en ligne seulement) | `ms`, `v1` | reprendre | |
| Deux surfaces séparées, observations datées et localisées | `ms` | reprendre | |
| Fiches en double : recherche, catalogue, fusionner / garder / consolider, suivi 3 mois | `ls` | reprendre | |
| NAP comparé HTML / JSON-LD / fiche ; abréviation ≠ conflit | `cs`, `ms` | reprendre | **script** `nap.py` (téléphones et adresses français normalisés) |
| Vie privée : adresse personnelle jamais publiée ni en JSON-LD | `ms` | reprendre | RGPD |
| Avis : demande neutre, pas de filtrage, réponses sans données | `ms`, `ls`, `v1` | reprendre | textes français revérifiés [à vérifier] |
| Test du remplacement, pages locales utiles | `cs`, `ls`, `v1` | reprendre | |
| Statistiques Whitespark / BrightLocal, BBB, Yelp, « signaux sociaux confirmés » | `cs`, `ls` | écarter | américain ou non sourcé |

### 14. /seo-social

| Fonction | Source | Verdict | Ajout |
|---|---|---|---|
| YouTube : la couche texte (transcription, sous-titres corrigés, titre en question, chapitres par sous-question, description, commentaire épinglé) | `ms youtube-ai-citations` | reprendre | **script** `video.py` : chapitres valides, titre, premières lignes, mot-clé dans la transcription |
| Pinterest, TikTok, LinkedIn, Discover | `v1` | reprendre | sources officielles de chaque plateforme, datées |
| Vidéo intégrée aux meilleurs articles + `VideoObject` (`creator` recommandé) | `MM`, `cs` | reprendre en option | |
| Propriétés sociales dans Search Console, profils Search | `cs` | **[à vérifier]** | |

## 5. Écartés, une fois pour toutes

- Densité de mots-clés, mots « LSI », Flesch, minimums de mots par type de
  page, pilier de 2 500-4 000 mots : contraires à `G` ou non sourcés.
- Blocs de 40-60 ou 130-170 mots « pour l'IA », FAQPage et HowTo « pour
  l'IA », `llms.txt` comme levier Google : contraires au guide IA de Google.
- Statistiques d'éditeurs d'outils présentées comme des lois (« 3× plus
  cité », « +121% de conversions », « 22× plus mémorisé »).
- Histoires, clients ou chiffres fictifs dans les articles.
- Rapports PDF, CRM, prospection, propositions commerciales, marque
  blanche.
- E-commerce, maps, hreflang, liens payants : hors de ton périmètre (à
  rouvrir si tu le demandes).

## 6. Questions à trancher

1. **Périmètre** : 14 Skills (programmatique dans le plan, drift dans
   l'audit) ou garder les 16 noms actuels ?
2. **SEO agentique** : `/geo-agentic` reste dans le pack GEO (appelé par
   l'audit), ou un `/seo-agentic` dans le pack SEO ?
3. **Réserve de preuves** commune LinkedIn + SEO (un seul fichier
   `reserve.md`), ou séparée ?
4. **Skill modèle** à écrire en premier et à relire : `/seo-maillage`
   (ta demande explicite, déjà le plus avancé) ou le duo
   `/seo-brief` + `/seo-write` (ton usage quotidien) ?

## 7. Décisions de l'utilisateur (12 octobre 2026)

1. Périmètre : **14 Skills**. `/seo-programmatic` devient une option de
   `/seo-plan`, `/seo-drift` devient `audit photo` / `audit compare` dans
   `/seo-audit`, avec des redirections sur le site.
2. SEO agentique : **reste `/geo-agentic`** (refait au chantier GEO v2),
   et `/seo-audit` l'appelle.
3. Réserve de preuves : **un seul `reserve.md`**, partagé par LinkedIn et
   SEO.
4. Skill modèle : **`/seo-brief` + `/seo-write`**, relus avant
   d'appliquer le gabarit aux autres, avec une éval à l'aveugle contre tes
   articles.

## 8. Avancement (12 octobre 2026)

- **Faits revérifiés aux sources primaires** (détail dans
  `seo-skills/commun/preuves.md`) :
  - guide Google sur l'IA générative (maj 10 juil. 2026), y compris
    l'inclusion dans Search Console et le rapport « IA générative » : les
    deux lignes [à vérifier] des sections 4.12 et 4.14 sont confirmées pour
    ce qui concerne Google ;
  - title (10 déc. 2025) et meta description (20 avr. 2026) : aucune limite
    de longueur, troncature selon l'appareil ;
  - politiques anti-spam (28 août 2026) ;
  - retrait des résultats FAQ (7 mai 2026).
- **Restent [à vérifier]** : les textes français (publicité comparative,
  avis en ligne). Légifrance et economie.gouv.fr refusent l'outil (403) ;
  seules des synthèses de cabinets sont lues.
- **Socle commun écrit** : `regles.md`, `preuves.md`, `garde_fou.py`,
  `texte_fr.py`, `meta.py`, `affirmations.py`, modèles (réserve partagée
  avec LinkedIn), `outils/propager.py`.
- **Skills modèles écrits** : `/seo-brief` (`couverture.py`) et
  `/seo-write` (`controle.py`), avec leurs références, exemples réels et
  tests. 100 tests au vert.
- **Exemple Assurly anonymisé** : courtier santé et prévoyance pour
  indépendants. Il ne reprend plus le profil réel du workflow de
  l'utilisateur.
- **Prochaine étape** : relecture du modèle par l'utilisateur, puis éval à
  l'aveugle contre ses articles. Viendront ensuite `/seo-human` (moteur
  LinkedIn v2, nécessaire à `/seo-write`) et les autres Skills.
