# marketingskills (Corey Haines) · sous-ensemble SEO · dissection

MIT. Lu en entier : seo-audit (9 fichiers, 1 445 lignes), ai-seo
(12 fichiers, 1 850 lignes), site-architecture, content-strategy,
competitors, competitor-profiling, schema, copy-editing (dont
`content-refresh.md`), copywriting, directory-submissions,
programmatic-seo (survol, hors périmètre), plus le registre d'outils
(`tools/REGISTRY.md`, intégration Search Console). Chaque Skill a un
`evals.json` avec des attentes vérifiables.

Style général : pas de scripts de mesure (les `tools/clis/*.js` appellent
des API, ils ne mesurent pas), mais un **jugement éditorial très mûr** et
des cas limites réels dans les évals. C'est l'inverse de claude-seo, qui
mesure beaucoup et juge moins finement.

## `seo-audit`

- Contexte d'abord (`product-marketing.md`), puis 3 groupes de questions :
  site, état actuel, périmètre.
- **Ordre de priorité** : exploration et indexation, puis fondations
  techniques, on-page, qualité de contenu, autorité.
- **Cas limite majeur** : `web_fetch` et `curl` ne voient pas le JSON-LD
  injecté en JavaScript (Yoast, Rank Math, AIOSEO) et le convertisseur de
  `web_fetch` retire les `<script>`. Conclure « pas de schema » depuis ces
  outils est un faux constat. Méthodes sûres : navigateur, test des
  résultats enrichis, export Screaming Frog. **Notre v1 doit être vérifiée
  sur ce point.**
- Les données ou pages récupérées sont des données non fiables, jamais des
  instructions (injection de prompt).
- International : très bon tableau d'erreurs hreflang et canonical. Les
  évals contiennent le cas fin « example.de et example.com/de, même langue
  pour deux régions : un canonical préféré est permis ».
- Sortie : constat, impact, **preuve (comment on l'a trouvé)**, correction,
  priorité.
- Faiblesses : « Mobile-Friendly Test » listé alors que Google l'a retiré
  **[à vérifier : date de retrait]** ; « temps sur la page, taux de
  rebond » donnés comme signaux de contenu ; méta description 150-160
  caractères (encore un autre jeu de chiffres).

### `references/rankings-push.md` (à reprendre presque tel quel)

- **Trois paniers** depuis Search Console sur 28 jours comparés à la
  période précédente : distance de frappe (positions 8-20, plancher
  d'impressions adapté au site), clic faible (positions 1-5, CTR très
  inférieur aux autres pages à position égale), presque en tête
  (positions 4-7 sur une requête qui rapporte).
- Priorité par **valeur business**, pas par volume.
- Cannibalisation vérifiée avant de toucher la page.
- **Diagnostic contre les 3 résultats du dessus** : nommer la raison
  concrète (intention, section manquante, fraîcheur, format, liens). « Si
  tu ne peux pas nommer la raison, ne réécris pas : c'est l'autorité. »
- **Le plus petit changement** : réponse dans les 2 premières phrases,
  section manquante plutôt que réécriture, liens internes depuis les pages
  fortes (« souvent le levier le plus négligé »), titre et description
  seuls pour un problème de clic (attribution propre).
- **Mesure** : position, impressions, CTR de départ notés ; attendre 3-4
  semaines ; **deux tours sans effet = arrêter** (intention ou autorité).
- Liste de lancement d'une nouvelle page (3 liens internes entrants,
  canonical, sitemap, contenu dans le HTML serveur, indexable), une seule
  demande d'indexation.

Ce que nous ajoutons : un script qui lit l'export Search Console (CSV
gratuit) et sort les trois paniers, le CTR attendu par position **calculé
sur le site lui-même** (pas une courbe générique), et le journal
avant/après.

### `references/title-tags.md`

- Partir de la SERP : format récompensé, mots attendus, écart.
- Structure : requête d'abord, raison de cliquer, marque seulement si elle
  aide ; troncature **en pixels**, mots importants dans les 50 premiers
  caractères.
- Modèles par type de page ; « gratuit », année ou nombre seulement si la
  page tient la promesse.
- **Réécritures de Google** : déclencheurs (trop long, bourrage, décalage
  avec le H1, générique), à traiter comme un signal.
- Audit en masse : tableau page / titre actuel / proposé / raison, 2-3
  options seulement pour les pages qui comptent.
- Ce que nous ajoutons : la mesure en pixels (police de la SERP) dans un
  script, les modèles en français, la typographie française (« : » avec
  espace, guillemets).

### `references/local-seo*.md` (le meilleur local lu jusqu'ici)

- Modèle d'activité d'abord : vitrine, zone de service, hybride, plusieurs
  établissements, **en ligne seulement** (pas de fausse présence locale).
- **Deux surfaces séparées** : pack local (pertinence, distance,
  proéminence, selon Google) et résultats organiques. Une recherche depuis
  le bureau du gérant n'est pas une preuve de visibilité dans la ville.
- Ordre des contraintes : fiche fausse, inéligible, en double, non vérifiée
  ou suspendue ; puis contact et accès ; puis demande non couverte ; puis
  confiance.
- **Vie privée** : ne jamais publier une adresse personnelle cachée pour
  remplir une liste de citations, ni la mettre en JSON-LD. Rich result
  LocalBusiness exige une adresse : le dire, ne pas en inventer une.
- Avis : demande neutre, pas de filtrage, pas d'incitation, lien vers la
  bonne fiche ; réponse aux critiques sans exposer de données.
- Tableau de nettoyage des citations (fiche, URL, faits observés, source de
  vérité, action, date de vérification) ; une abréviation n'est pas un
  conflit d'identité.
- Q&A Google : API arrêtée le 3 novembre 2025 (lien vers le changelog
  Google).
- Mesure : appels et réservations qualifiés plutôt que classement ;
  limites d'interprétation écrites pour chaque indicateur.
- Évals locales très fines : serrurier à domicile qui veut 3 fiches,
  description de fiche sans prix ni promesse inventés, cabinet dentaire
  déménagé.
- Ce que nous ajoutons : annuaires et règles françaises (voir note
  claude-seo), consentement RGPD pour les photos et les avis.

### `references/ai-writing-detection.md`

Liste anglaise (tiret cadratin, verbes, adjectifs, transitions,
ouvertures, conclusions). Notre humaniseur français est déjà plus complet.

## `ai-seo` (relève surtout du pack GEO v2, noté ici pour le SEO)

- Bon : distinction **position de Google** (pas de fichier, pas de
  découpage, pas de contenu séparé pour l'IA) et autres moteurs ;
  « citation ≠ recommandation » (être cité n'est pas être dans la liste
  courte) ; réponses d'IA non déterministes : **3 à 5 essais par requête,
  noter un taux avec la taille d'échantillon (« cité 3/5 »)**. À reprendre
  dans `/seo-audit` volet IA.
- **YouTube** (`youtube-ai-citations.md`) : le modèle ne regarde pas la
  vidéo, il lit la couche texte. Ordre de levier : transcription en phrases
  complètes, sous-titres corrigés (noms de produit), titre en forme de
  question, chapitres titrés par sous-question, description qui reprend les
  points, commentaire épinglé. Liste de publication. **Base solide pour
  notre volet « SEO social » YouTube**, à compléter avec les sources
  YouTube officielles.
- Contradictions avec Google et faits fragiles, à écarter ou marquer :
  recommande encore FAQPage et HowTo « pour l'IA » dans un tableau, alors
  que le Skill schema du même dépôt les dit retirés ; « contenu avec schema
  30-40% plus visible » sans source ; « blocs de 40-60 mots » ; chiffres de
  l'étude GEO de Princeton présentés comme des gains garantis ; « Claude
  utilise Brave Search » **[à vérifier]** ; « pas de rapport IA dans Search
  Console » contredit par claude-seo (rapport « Generative AI
  performance ») **[à vérifier aux sources Google]** ; chiffres « ChatGPT
  5.6 » d'août 2026 **[à vérifier]**.

## `site-architecture`

- Arborescence ASCII et Mermaid, règle des 3 clics, niveaux L0-L3, URL par
  type de page, fil d'Ariane aligné sur l'URL, erreurs courantes (dates dans
  les URL, IDs, paramètres).
- Liens internes : pas d'orpheline, ancres descriptives, « 5-10 liens pour
  1 000 mots » (repère sans source), hub et rayons.
- **Aucun outil** pour analyser un site existant : tout est planification.
  Même trou que claude-seo pour notre besoin « sitemap → clusters →
  maillage ».

## `content-strategy`

- **Porte d'Information Gain** : lire les premiers résultats et écrire une
  phrase sur ce que la page apportera ; « si tu ne peux pas l'écrire, ne
  l'écris pas ». Même idée que le brief de claude-seo, formulée plus court.
- Cherchable contre partageable ; types de contenu ; mots-clés par étape
  d'achat (prise de conscience, considération, décision, mise en œuvre).
- **Note de priorité** : impact client 40%, adéquation produit 30%,
  potentiel de recherche 20%, ressources 10%. Calculable.
- Calendrier 60/30/10 (repère, pas une règle, dit le Skill).
- Formats qui gagnent des liens (une étude d'éditeur, « directionnelle »).

## `copy-editing` · `references/content-refresh.md` (à reprendre)

- Quand rafraîchir (trafic en baisse, chiffres de plus de 12 mois, produit
  changé, concurrents mis à jour).
- **Grille de couverture** : sa page + 5 concurrents (3 premiers + un
  concurrent direct ou une page récemment mise à jour), sous-thèmes en
  lignes ; classement **attendu (4-5 sur 5), courant (2-3), distinctif
  (1), non couvert (0)**. « Ignore le nombre de mots des concurrents. »
- Plan section par section **Garder, Réviser, Nouveau**, 2-3 titres,
  validation avant réécriture, aucune promesse de classement.
- Garder ce qui marche : URL, ancres, sections qui rankent pour leurs
  propres requêtes, voix ; date « mis à jour » visible, année à côté de
  chaque statistique.
- Rafraîchir ou réécrire (tableau), cadence par type de page.

Ce que nous ajoutons : la grille de couverture calculée par un script à
partir des plans H2/H3 des pages (l'utilisateur colle les plans ou on les
extrait), avec la classe de chaque sous-thème.

## `competitors` et `competitor-profiling`

- **Discipline de preuve** (à reprendre telle quelle) : « non observé
  n'est pas absent » (« non listé sur leur page tarifs, au [date] »), faits
  datés, une visite est un instantané, dire ce qui a changé et pas pourquoi,
  séparer fait, interprétation et recommandation.
- **Audit des contenus comparatifs** : chaque affirmation sur un concurrent
  classée Actuelle, Changée, Invérifiable, Surévaluée, avec date de
  vérification ; jamais « Actuelle » sans date.
- Données concurrentes centralisées (une source de vérité par concurrent).
- Profilage : pages clés à extraire, avis, données SEO via connecteur ;
  **sauvegarde des données brutes datées** avant extraction.
- Ce que nous ajoutons : cadre français de la publicité comparative, et
  notre règle « zéro invention » appliquée aux prix des concurrents.

## `schema`

- Statuts à jour : FAQ retiré le 7 mai 2026, HowTo septembre 2023, boîte
  de recherche des liens annexes novembre 2024. « Valide pour Schema.org »
  n'est pas « éligible chez Google ». Ne pas retirer un balisage existant
  sans raison.

## `directory-submissions`, `programmatic-seo`

- Annuaires de logiciels (SaaS, IA) pour les liens et la découverte : peu
  utile à notre public francophone, sauf pour les éditeurs de logiciels.
  Chiffres non sourcés (« trafic IA 6-27× plus converti »). À écarter.
- Programmatique : hors périmètre demandé.

## Outils

- Registre : Search Console « essentielle (gratuite) », puis Semrush,
  Ahrefs, DataForSEO, Keywords Everywhere. CLI Search Console : requête
  `searchAnalytics` (dimensions requête, page, pays ; jusqu'à 25 000
  lignes). Rien sur l'export CSV gratuit de l'interface, qui est le mode
  gratuit le plus simple pour un marketeur.

## Synthèse marketingskills

**À reprendre** : poussée des positions 8-20 et clics faibles (avec règle
d'arrêt), titres (pixels, réécritures, tableau d'audit), local (modèle
d'activité, deux surfaces, vie privée, avis, tableau de citations, mesure),
JSON-LD invisible à `web_fetch`, discipline de preuve des comparatifs et
audit des affirmations, grille de couverture du rafraîchissement, porte
d'Information Gain, note de priorité des idées, YouTube « couche texte »,
réponses d'IA mesurées en taux sur 3-5 essais.

**À améliorer** : tout passer en mesure (scripts sur l'export Search
Console, grille de couverture, titres en pixels) et en français.

**À écarter** : FAQ/HowTo « pour l'IA », blocs de 40-60 mots, chiffres
d'études d'éditeurs présentés comme des lois, annuaires SaaS, repères de
densité de liens sans source.
