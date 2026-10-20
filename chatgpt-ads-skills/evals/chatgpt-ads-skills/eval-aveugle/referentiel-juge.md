# Référentiel pour le juge : faits officiels relus le 15 octobre 2026

Sources publiques d'OpenAI : Help Center « Ads in ChatGPT: The Basics », règles publicitaires (Ad Policies) v1.6 de septembre 2026, documentation développeur Ads. Ces faits servent à juger l'exactitude des réponses ; une réponse n'est pas tenue de les citer tous.

## 1. Le fichier d'import

| Fait | Source | Vérifié le |
|---|---|---|
| 3 onglets exactement : `campaigns`, `adgroups`, `ads`. 3 lignes d'en-tête (nom du champ, obligatoire ou non, explication), puis les données à partir de la ligne 4. | M | 15 oct. 2026 |
| Le modèle d'Ads Manager contient une ligne d'exemple en italique (`oaitest…`) en ligne 4 : à retirer, et les données s'écrivent en texte normal. | M | 15 oct. 2026 |
| `campaigns` : `campaign_name`, `budget_max` obligatoires ; `budget_type`, `launch_date`, `end_date`, `objective`, `target_countries` facultatifs ; `conversion_event_setting_ids` obligatoire en campagne de conversion (un seul identifiant, en tableau JSON). | M, D | 15 oct. 2026 |
| `adgroups` : `campaign_name`, `adgroup_name` obligatoires ; `max_bid` obligatoire au clic et à la conversion ; `Context Hints` facultatif, en tableau JSON. | M | 15 oct. 2026 |
| `ads` : `adgroup_name`, `title` (24 caractères au plus), `copy` (48 au plus), `link`, `image_link` obligatoires. | M | 15 oct. 2026 |
| L'API accepte des titres de 3 à 50 caractères et des textes de 100 au plus ; **le fichier d'import fixe 24 et 48** : c'est lui qui fait foi pour l'import. | D, M | 15 oct. 2026 |
| Noms de campagne et d'ad group : de 3 à 1 000 caractères (API) ; « no special characters » dans le modèle, sans liste. | D, M | 15 oct. 2026 |
| Image : carrée, PNG ou JPG, de 640 × 640 à 1 200 × 1 200 dans le modèle ; l'API accepte JPEG, PNG ou WebP d'au moins 640 × 640. | M, D | 15 oct. 2026 |
| Lien : HTTP ou HTTPS, 2 048 caractères au plus, accessible aux robots d'OpenAI qui vérifient les annonces ; paramètres de suivi (UTM) permis. | D, H | 15 oct. 2026 |
| Codes pays ISO 3166-1 alpha-2 ; un code valide n'est pas forcément ouvert à la publicité pour le compte. | D | 15 oct. 2026 |

## 2. Diffusion, enchères, mesure

| Fait | Source | Vérifié le |
|---|---|---|
| Les annonces s'affichent sous les réponses de ChatGPT, avec le nom de l'annonceur, son logo (favicon), un titre, un texte, une page de destination et une image. | H | 15 oct. 2026 |
| Pas d'annonce pour les abonnés Plus, Pro et Business, ni pour les comptes identifiés comme mineurs. | H | 15 oct. 2026 |
| Sélection selon la pertinence et les résultats attendus : contexte et intention de la conversation, page de destination, titre, texte, context hints et, si la personnalisation est activée, d'autres signaux du compte. | H | 15 oct. 2026 |
| Enchère au second prix pondérée par la pertinence. | H | 15 oct. 2026 |
| Context hints : décrivent les conversations, thèmes, produits, usages ou besoins où l'annonce peut aider (« descriptions or keywords ») ; ce ne sont pas des mots-clés en correspondance exacte et ils ne garantissent pas la diffusion. | H, D | 15 oct. 2026 |
| La documentation préfère un hint précis à un mot vague (« Shoes » moins utile que « Lightweight trail running shoes for rocky terrain ») et dit de régler la géographie dans le ciblage, pas dans les hints. | D | 15 oct. 2026 |
| Jusqu'à 2 000 hints par ad group ; « inutile de remplir la limite ». | D | 15 oct. 2026 |
| Des hints d'exclusion (`exclusion_hints`, API Bulk) et des « Negative Phrases » (annonceurs qualifiés) existent ; ils ne passent pas par le fichier d'import. | D, H | 15 oct. 2026 |
| Objectifs : Views (paiement à l'affichage, CPM), Clicks (au clic valide), Conversions (oCPC : optimisé vers un événement, facturé au clic valide, pas à la conversion). | H, D | 15 oct. 2026 |
| En oCPC, l'enchère maximale est un coût par conversion visé ; un seul événement standard par campagne, qui ne change plus après création ; les événements personnalisés ne peuvent pas être l'objectif. | D | 15 oct. 2026 |
| Événements standard : `app_installed`, `app_opened`, `appointment_scheduled`, `checkout_started`, `contents_viewed`, `items_added`, `lead_created`, `order_created`, `page_viewed`, `registration_completed`, `subscription_created`, `trial_started` (plus `custom`). | D | 15 oct. 2026 |
| Mesure : pixel JavaScript, API Conversions (plus fiable que le pixel seul) ou balise image. | D | 15 oct. 2026 |
| OpenAI conseille de commencer à 3 à 5 USD de CPC maximum ; Ads Manager peut indiquer si l'enchère est trop faible (pas d'alerte dans les 24 h qui suivent une modification). | H, D | 15 oct. 2026 |
| Stratégies « Maximize Results » (clics ou conversions) : budget quotidien obligatoire, pas d'enchère maximale. Un budget total (Lifetime) ne se convertit pas en quotidien dans l'autre sens. | D | 15 oct. 2026 |
| Le modèle d'import conseille le budget quotidien : le budget total n'a « pas encore » de lissage de diffusion. | M | 15 oct. 2026 |
| Rapports : affichages, clics et CTR rafraîchis toutes les 15 minutes environ ; la dépense peut avoir 7 à 8 heures de retard. | H | 15 oct. 2026 |
| Ciblage de campagne : pays ou zones (identifiants de lieux), plateformes (`ios_app`, `android_app`, `web`), audiences personnalisées (25 000 personnes reconnues au moins pour une inclusion). | D | 15 oct. 2026 |
| Ouverture de 31 pays européens, dont la France, à partir du 24 août 2026. | officiel **[à vérifier : relire la page]**, annonce d'OpenAI « ChatGPT Ads expands across Europe » | 15 oct. 2026 |

## 3. Règles publicitaires (Ad Policies v1.6, septembre 2026)

| Fait | Source | Vérifié le |
|---|---|---|
| Pas d'annonce près des conversations sensibles : santé mentale et personnelle, dépendance émotionnelle, parcours sensibles, et 19 catégories dont sécurité des enfants, politique, vie privée, suicide, armes, biens réglementés. | P | 15 oct. 2026 |
| Catégories de la phase de test : biens ménagers et de consommation, style de vie, services locaux, voyages et expériences, divertissement, produits numériques et éducation. | P | 15 oct. 2026 |
| Services financiers (dont l'assurance), santé et juridique : admis **aux États-Unis seulement**, au cas par cas, pour des annonceurs approuvés ; **hors États-Unis, généralement interdits**. | P | 15 oct. 2026 |
| Interdits : contenus adultes et rencontres, alcool (plus de 0,5%), tabac et vapotage, jeux d'argent, contrefaçons, substances récréatives, contenu politique, allégations de bien-être non étayées (détox, minceur), redressement de crédit et règlement de dettes, investissements alternatifs (or), offres d'emploi ou de logement individuelles. | P | 15 oct. 2026 |
| Toute annonce doit être véridique : pas d'affirmation non étayée sur les capacités, les prix, les résultats, les affiliations ou les comparaisons. | P | 15 oct. 2026 |
| L'annonce ne doit pas imiter l'apparence, les fonctions ou la voix de ChatGPT. | P | 15 oct. 2026 |
| Les règles s'appliquent au texte, à l'image et à la page de destination, qui doivent être cohérents de bout en bout. | P | 15 oct. 2026 |
| Examen par systèmes automatisés (dont des LLM) sous contrôle humain ; une annonce ou une page qui ne peut pas être vérifiée ne peut pas être diffusée. | P | 15 oct. 2026 |
| Historique : v1.0 mars 2026, v1.1 avril (conseils médicaux, juridiques et financiers plus bloqués d'office pour le placement), v1.3 juillet (finance et santé précisées), v1.5 août (juridique admis aux États-Unis), v1.6 septembre. | P | 15 oct. 2026 |

