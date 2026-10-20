# Pack Ads : matrice du Skill `/chatgpt-ads-skills`

Collecte et dissection du 15 octobre 2026. Brief d'Aleksander : un Skill qui
aide un annonceur à **cibler et rédiger** pour ChatGPT Ads (carte des
intentions, ad groups, context hints, titres et copies, export du fichier
d'import), sans piloter ni optimiser de campagne.

## Sources analysées

| Code | Source | Lu | Statut |
|---|---|---|---|
| T | Modèle d'import d'Ads Manager (exemplaire fourni par Aleksander) | XML des 3 onglets, styles, liens | format de sortie ; le fichier n'est pas redistribué |
| G | Documents d'onboarding non publics remis à l'annonceur (guide) | intégral | **confidentiel** : compris, jamais repris (ni prompts, ni formulations, ni chiffres) |
| D | Documents d'onboarding non publics (présentation) | intégral | **confidentiel** : idem ; aucun cas chiffré n'est cité |
| M | Exemple de campagne d'un annonceur réel | intégral | **ne pas reprendre** : sert à repérer les erreurs fréquentes, aucun texte repris |
| F | fseixas, `chatgpt-ads-builder` (MIT, 8 fichiers : SKILL, 3 références, script, README) | intégral | public |
| A | AgriciDaniel, `claude-ads` (MIT, 354 fichiers) ; Hainrixz, `claude-ads` (MIT, 159 fichiers) | Skills `ads-validate`, `ads-launch`, `ads-budget`, recherche « ChatGPT » | public ; ne traitent pas ChatGPT Ads |
| H | Help Center d'OpenAI, « Ads in ChatGPT: The Basics » | intégral (texte fourni par Aleksander le 15 oct. 2026, la page refuse les lectures automatiques) | public, officiel |
| P | Règles publicitaires d'OpenAI (Ad Policies) v1.6, septembre 2026, version française | intégral (texte fourni par Aleksander) | public, officiel |
| DV | Documentation développeur Ads, export complet `llms-full.txt` (8 450 lignes : API, Bulk API, ciblage, enchères, conversions, événements, dépannage) | sections utiles à la préparation lues en entier | public, officiel |
| W | Guides tiers sur les context hints, les limites et les pays (une dizaine) | extraits | praticien, contradictoires entre eux |

## Ce que les sources apprennent

1. **Le modèle fait foi pour l'import, pas les guides.** T impose titre 24 et
   copie 48 caractères au plus. Les documents d'onboarding non publics
   donnent des repères différents d'une page à l'autre ; W rapporte 16-24 et
   32-48 recommandés, 50 et 100 acceptés d'après le Help Center ; F impose 35
   et 67 sans source. Le script lit les
   limites **dans le modèle** (ligne 2 : « max 24 chars ») : si OpenAI change
   le modèle, le contrôle suit.
2. **L'exemple du modèle est un piège.** Sa ligne 4 (`oaitest…`) serait
   importée si on la laisse, et ses cellules sont **en italique** (polices 4
   et 8) : d'où la consigne « texte normal ». L'export retire la ligne 4 et
   écrit avec les styles non italiques déjà présents (11 : texte, 8 : date).
3. **Le modèle n'a aucune validation de données** (seulement une mise en
   forme conditionnelle sur `campaigns`). Tout se contrôle par script.
4. **La liste de pays du modèle est périmée** (9 pays ; l'Europe a ouvert en
   août 2026 d'après l'annonce publique). Le script accepte tout code
   ISO 3166-1 alpha-2 et rappelle de vérifier la disponibilité dans Ads Manager.
5. **Les exemples clients dépassent les limites.** M : des titres et des copies
   bien au-delà des limites. Les LLM comptent mal : tout ce qui
   se compte passe par le script.
6. **Le nombre de context hints n'a pas de source officielle.** W : de 1 à 15
   selon les auteurs, plafond API de 2 000 rapporté. Le brief : 3 par défaut
   (2 à 5), hypothèse à tester.
7. **Les règles publicitaires bougent.** W et H : santé, finance et
   juridique ont changé de statut plusieurs fois depuis mars 2026 ; les
   conversations sensibles restent exclues. Le Skill signale et renvoie aux
   Ad Policies datées, il ne tranche pas.

## Matrice

Verdicts : ✅ reprendre · ⬆ reprendre en améliorant · ✖ écarter (avec la raison) · ➕ nouveau.

| Capacité | Source | Verdict | Ce que nous en faisons |
|---|---|---|---|
| Entretien une question à la fois, sauter ce qui est déjà répondu | F, brief | ✅ | 6 questions du brief, une par message |
| Ne pas inventer : « TBD » si l'utilisateur ne sait pas | F | ⬆ | `{{à compléter}}` et liste « à vérifier », règle commune des packs |
| Liste des allégations étayées avant toute rédaction | G (méthode), brief | ⬆ | réécrite : tableau allégation, source, statut ; le script bloque un chiffre, un prix ou un superlatif absent de la liste |
| Carte des intentions (persona, besoin, réponse attendue, étape, ad group) | brief, G (méthode) | ⬆ | « intention envisagée » comme pivot ; colonnes du brief |
| Un ad group = une intention, 5 au moins | brief, H | ✅ | contrôle du nombre de groupes ; test des 3 prompts simulés |
| Context hints : thèmes, pas mots-clés exacts ; situations riches | H, brief | ✅ | règles et contre-exemples réécrits |
| Nombre et longueur des hints | brief, W | ⬆ | 3 par défaut (2 à 5), environ 4 à 5 mots : **hypothèses** marquées à confirmer ; le script avertit au-delà |
| Termes vagues, hints de marque, variantes mineures, chevauchements | brief, H | ⬆ | détection par script (liste de termes vagues, similarité entre hints et entre groupes) |
| Titre 24 / copie 48, cibles 16-24 / 32-48 | T, D | ⬆ | maxima lus dans le modèle ; cibles en information |
| Limites 35 / 67 | F | ✖ | sans source, contredites par le modèle |
| Titre et copie complémentaires, angles distincts | brief, F | ✅ | contrôle de recouvrement titre/copie et de quasi-doublons |
| Patrons de copie (contraste, preuve, impératif, promesse) | F | ⬆ | réécrits en français, avec la contrainte « preuve seulement si étayée » |
| Tactiques de longueur (chiffres, couper la marque…) | F | ⬆ | adaptées à la typographie française (l'espace avant « : ? ! » compte) |
| 2 annonces par groupe | F | ✖ | trop peu pour un lancement ; brief : 40 à 50 au total, 100 en grande échelle |
| 100 annonces au minimum | G | ⬆ | mode « grande échelle » ; défaut 40 à 50 ; écart marqué à confirmer |
| Prompts d'images génératives (icônes) | F | ✖ | décision du 15 oct. 2026 : une idée de visuel par groupe, pas de prompt |
| Idée de visuel + contrôle des liens d'images | brief, T | ➕ | idée dans le tableau de relecture ; le script contrôle URL, extension et, en ligne, taille et format carré |
| Export XLSX au format du modèle | brief, T | ➕ | `valider_exporter.py` (Python sans dépendance) : 3 onglets, en-têtes et styles conservés, ligne d'exemple retirée, texte normal |
| Repli sans exécution de code | G (méthode), brief | ✅ | tableaux prêts à coller, et le dire |
| Validation finale humaine | G, T | ✅ | checklist de vérification humaine |
| Mesure (pixel, API Conversions) avant d'augmenter les dépenses | brief, D | ✅ | section « Avant de dépenser » |
| Optimisation, pilotage, enchères automatiques | A | ✖ | hors périmètre (brief) |
| Ciblage : audiences, géo fine, plateformes | D | ✖ | réglages d'Ads Manager, hors fichier d'import ; mentionnés seulement |
| Cas chiffrés | D | ✖ | confidentiels et invérifiables |

## Ce que les sources officielles ont changé (15 octobre 2026, deuxième passe)

1. **Éligibilité** : santé, finance (dont l'assurance) et juridique sont
   admis aux États-Unis seulement, au cas par cas ; hors États-Unis,
   généralement interdits (P). Nouvelle étape du Skill, nouveau contrôle du
   script (`annonceur.categorie`), nouvelle référence `politiques.md`. Le
   cas de test « secteur sensible » (Assurly, mutuelle, France) devient un
   cas d'arrêt.
2. **Context hints** : « descriptions or keywords », jamais en
   correspondance exacte, précis plutôt que vagues, sans géographie (à
   régler dans le ciblage), jusqu'à 2 000 mais « inutile de remplir la
   limite » (H, DV). Contrôle des hints géographiques ajouté.
3. **Enchère** : second prix pondéré par la pertinence (H) ; point à
   confirmer n° 4 résolu. CPC de départ conseillé : 3 à 5 USD (H).
4. **Limites** : l'API accepte 3 à 50 et 100 caractères, le fichier
   d'import 24 et 48 (DV, T). Le pack écrit pour le fichier.
5. **Imitation de ChatGPT** interdite (P) : contrôle ajouté.
6. **Noms** de 3 à 1 000 caractères, **liens** de 2 048 au plus, **images**
   JPEG, PNG ou WebP (DV) : contrôles ajoutés.
7. **Conversions** : 13 événements standard, un seul par campagne, figé à
   la création ; API Conversions plus fiable que le pixel seul (DV).
8. **Modèle d'import** : à la demande d'Aleksander, le fichier d'OpenAI
   n'est plus dans le dépôt. Le pack écrit son propre modèle
   (`outils/construire_modele.py`) : mêmes onglets et colonnes, explications
   en français, contrôles de saisie, pas de ligne d'exemple piégée. Le
   script exporte aussi vers le modèle d'Ads Manager (`--modele`).

## Décisions d'Aleksander (15 octobre 2026)

1. **Nom et place** : un nouveau pack Ads ; commande `/chatgpt-ads-skills`
   (rangée dans `ads-skills/skills/chatgpt-ads-skills/`).
2. **Images** : une idée de visuel par ad group et des contrôles ; sans image
   fournie, la cellule reste vide et c'est bloquant.
3. **Cas de test** : 3 cas fictifs (B2C, B2B, secteur sensible).
4. **Éval à l'aveugle** : contre fseixas (`chatgpt-ads-builder`) **et**
   contre Claude sans Skill.

## Points à confirmer (marqués comme tels dans le Skill)

1. Nombre de hints : 2 à 3 conseillés par un contact OpenAI, 5 dans un
   exemple, « pas de max » dans le modèle.
2. Longueur des hints : environ 4 à 5 mots, ou 1 à 2 phrases selon d'autres
   sources.
3. Volume d'annonces : 40 à 50 (notes d'Aleksander) ou 100 au minimum.
4. ~~Pondération pertinence et enchère~~ : résolu, enchère au second prix
   pondérée par la pertinence (Help Center).
5. ~~Redistribution du modèle d'OpenAI~~ : résolu, retiré ; modèle maison.
   Reste à confirmer : Ads Manager accepte-t-il le modèle maison à
   l'import ? (import d'essai recommandé dans la checklist)
6. Caractères autorisés dans les noms (« no special characters ») : espaces
   et accents tolérés ou non.

# v0.2 : collecte du 20 octobre 2026

## Sources ajoutées

| Code | Source | Lu | Statut |
|---|---|---|---|
| N | nowork-studio/NotFair v0.27.1 (MIT), via la sauvegarde manak-debug/claude-skills : `paid-ads-chatgpt` (19 lignes), les 12 Skills `paid-ads-*`, les 2 contrats partagés, `google-ads/copy`, `policy-registry.json`, CHANGELOG | intégral | public |
| SD | Fiche skillsdirectory.com du même Skill (note de sécurité, pas de qualité) | intégral | public |
| MCP | avyanshkatiyar/openai-ads-mcp (MIT, 21 fichiers) : client, schémas, analyseur de brief, 3 Skills, 52 tests (exécutés : réussis avec `mcp<2`, échec de collecte avec `mcp` 2.x non épinglé) | intégral, exécuté | public |
| ST | studeria.fr, guide ChatGPT Ads France (22 sept., maj 28 sept. 2026) | intégral | presse ; plusieurs erreurs (date France, image 256 px, ciblage par historique dans l'EEE) |
| LX | launchcodex.com, 9 formats (29 mai 2026) | intégral | presse ; 1 format sur 9 documenté, chiffres sans source |
| DV2 | Documentation développeur, `llms-full.txt` du 20 oct. 2026 (8 485 lignes, journal au 30 sept.) | sections utiles en entier | officiel |
| P2 | Ad Policies v1.6 du 10 sept. 2026, texte français fourni par l'utilisateur | intégral | officiel |
| S | Schéma d'annonces à 10 colonnes fourni par l'utilisateur, « seul format compatible » | XML | format de sortie ; l'exemplaire (métadonnées d'un poste) n'est pas redistribué |
| G2, D2 | Guide de scaling (EN, FR, 22 juin 2026) et présentation d'onboarding | intégral | **confidentiels** : compris, jamais repris (ni prompts, ni chiffres, ni études de cas) |
| M2 | Exemple de campagne d'un annonceur réel | intégral | **non repris** : 4 titres sur 4 et 4 textes sur 4 au-delà des limites, produit d'assurance |

## Matrice v0.2

Verdicts : ✅ reprendre · ⬆ reprendre en améliorant · ✖ écarter (avec la raison) · ➕ nouveau.

| Capacité | Source | Verdict | Ce que nous en faisons |
|---|---|---|---|
| Statuts d'un livrable, registre de règles daté | N | ⬆ | `commun/faits.md` daté, alerte qui reste dans « à vérifier » |
| « Ne jamais inventer un identifiant » | N, MCP | ✅ | `/chatgpt-ads-ids` : identifiants lus, jamais devinés ; noms ambigus non remplis |
| Client d'API à transport remplaçable, lecture paginée | MCP | ⬆ | `ids.py` : lecture seule, 500 par page, nouvel essai sur 429 ; tests sur API simulée |
| Création, activation, archivage par l'API | MCP | ✖ | règle « rien n'est publié à la place de l'utilisateur » ; seule écriture : téléverser une image, sur confirmation |
| Contrôles de l'API de juin 2026 (CPM seul, budget total seul) | MCP | ✖ | périmés (objectifs clics et conversions, budget quotidien) |
| Format de sortie | S | ➕ | `commun/classeur.py` : lecture, contrôle cellule par cellule, réparation, écriture du schéma |
| Campagnes et ad groups hors du classeur | S, DV2 | ➕ | fiche de paramétrage écrite par `exporter`, hints en JSON prêts à coller |
| Secteur restreint : arrêt | v0.1 | ✖ | décision de l'utilisateur (20 oct.) : alerte datée, pistes conformes, puis le travail ; annonces véridiques seulement |
| Règles d'OpenAI en entier | P2 | ➕ | `commun/politiques-openai.md`, mise en forme fidèle, pas une copie |
| Droit français des annonces | (expertise) | ➕ | `commun/droit-francais.md` : langue, pratiques trompeuses, réduction, crédit, santé, allégations vertes, traceurs |
| EEE sans personnalisation, audiences personnalisées exclues | DV2 | ➕ | faits § 2 bis, checklist France |
| Pixel : consentement acquis par défaut | DV2 | ➕ | `consent: false` avant `init`, relié au bandeau |
| Pays vide = tous les pays disponibles | DV2 | ➕ | ATTENTION du script, pays FR par défaut |
| Volume : 100 au lancement | G2 | ⬆ | 40 à 50 par défaut, puis `/chatgpt-ads-bulk` par lots de 50 jusqu'à 120 ou plus (choix de l'utilisateur) |
| Lots équilibrés, doublons, notes | G2 (méthode générique) | ⬆ | réécrit : `analyser_lot.py` (structures, facettes, mots répétés, quasi-doublons, remplissage par le bas, notes mesurées séparées du jugement) |
| Exports Google, Meta, Microsoft comme source | G2 | ⬆ | `lire_exports.py` : lecture complète, en-têtes FR et EN, lignes de structure et de total ignorées, allégations avec ligne source, termes longs → situations |
| 9 formats créatifs | LX | ✖ | 8 sur 9 non documentés par OpenAI |
| Chiffres de CTR, CPM, revenus | LX, ST | ✖ | sans source vérifiable |
| Limites 32 et 54, 16 à 24 et 32 à 48 | D2, G2 | ⬆ | le modèle d'import fait foi : 24 et 48 ; `--limites api` (50 et 100) sur décision |
| Bulk API (JSON) | DV2 | ✖ pour l'instant | aperçu limité, ouvert sur demande ; l'Excel suffit (décision du 20 oct.) |
| Macros de suivi `{campaign_id}`, `{ad_id}`, `{oppref}` | DV2 | ➕ | commande `utm` ; identifiants retrouvés aussi dans l'analyse d'audience |

## Décisions de l'utilisateur (20 octobre 2026)

1. Le nom `/chatgpt-ads-skills` reste ; 40 à 50 annonces par défaut.
2. Un Skill bulk pour passer à 120 ou plus ; un Skill pour les exports ; un
   Skill pour les identifiants ; un Skill pour le classeur.
3. Spécialisé France ; ne pas bloquer les secteurs restreints : prévenir,
   proposer des pistes, puis répondre à la demande.
4. Le classeur final suit le schéma d'annonces fourni.
5. Pas d'export JSON pour la Bulk API.

## Reste à faire

- Import d'essai du schéma : colonnes obligatoires, limites, `status`,
  rôle d'`ad_id` (création ou modification).
- Captures du compte pour les chemins d'interface marqués « à vérifier ».
- Éval à l'aveugle de la v0.2 sur des cas réels anonymisés.
