# Faits : ce qu'on sait de ChatGPT Ads, et d'où ça vient

Chaque affirmation sur la plateforme a un **niveau de preuve** et une **date
de vérification**. Un fait absent de ce fichier porte **[à vérifier]**. La
plateforme change vite : on revérifie quand la date a plus de 3 mois, et les
règles publicitaires à chaque lancement.

Sources officielles :

- **[H]** Help Center d'OpenAI, « Ads in ChatGPT: The Basics » (mise à jour
  vers le 10 oct. 2026, relue le 15 oct. 2026),
  https://help.openai.com/en/articles/20001207-ads-in-chatgpt-the-basics
- **[P]** Règles publicitaires d'OpenAI (Ad Policies), version 1.6 du
  10 sept. 2026, version française relue en entier le 20 oct. 2026 :
  https://openai.com/fr-FR/policies/ad-policies/ (synthèse complète :
  `commun/politiques-openai.md`)
- **[D]** Documentation développeur Ads, https://developers.openai.com/ads
  (export complet `llms-full.txt`, 8 485 lignes, journal des modifications
  au 30 sept. 2026, relu le 20 oct. 2026)
- **[M]** Le modèle d'import d'Ads Manager à 3 onglets, lu dans un
  exemplaire fourni par un annonceur (non redistribué)
- **[S]** Le schéma d'annonces « Schema - ChatGPT ads » (un onglet,
  10 colonnes), fourni le 20 oct. 2026 comme seul format compatible avec
  l'import d'Ads Manager ; le pack écrit sa propre copie vierge
- **[R]** Presse et blogs spécialisés qui citent OpenAI (Blog du
  Modérateur, 1er sept. 2026 ; AirOps, lu le 14 oct. 2026) : faits à
  confirmer sur la page d'OpenAI quand elle est lisible

## 1. Le fichier d'import

### Le schéma d'annonces (format de sortie du pack)

| Fait | Source | Vérifié le |
|---|---|---|
| Un onglet (`Feuil1` dans l'exemplaire fourni), une ligne d'en-tête, puis une annonce par ligne. Colonnes, dans l'ordre : `ad_id`, `ad_group_id`, `adgroup_name`, `ad_name`, `status`, `title`, `copy`, `link`, `image_url`, `image_file_id`. | S | 20 oct. 2026 |
| Format de fichier à importer : **CSV uniquement** (pas XLSX), d'après la plateforme d'import consultée par l'utilisateur ; le pack écrit un CSV UTF-8 sans BOM, à virgules. | S (usage) | 27 oct. 2026 |
| Un CSV à **points-virgules** (enregistré par Excel en français) est refusé à l'import : « le fichier n'a pas les bonnes en-têtes », alors que les noms de colonnes sont exacts. Le même fichier à virgules passe le contrôle du pack. Encodages autres qu'UTF-8 : non documentés. | usage | 27 oct. 2026 |
| Règles d'usage retenues par l'utilisateur : `status` à `active` pour lancer à l'import ; `ad_group_id`, `ad_id`, `image_file_id` laissés vides s'ils ne sont pas fournis ; toute case vide signalée pour vérification. | usage | 20 oct. 2026 |
| Le schéma ne contient ni campagne ni ad group : ils se créent dans Ads Manager (ou par l'API), puis chaque annonce est reliée à son ad group par `ad_group_id`. Les context hints se saisissent donc dans Ads Manager, au niveau de l'ad group. | S, D | 20 oct. 2026 |
| Colonnes obligatoires, limites de caractères et valeurs de `status` propres à ce format : **non documentées**. Le pack applique les limites du modèle d'import (titre 24, copie 48), les statuts de l'API (`active`, `paused`) et demande au moins une image (`image_url` ou `image_file_id`). | S, M, D | 20 oct. 2026 **[à vérifier par un import d'essai]** |
| Identifiants dans la documentation : `ad_…` (annonce), `adgrp_…` (ad group), `cmpn_…` (campagne), `file_…` (image téléversée) ; ce sont des exemples, le format réel peut différer. | D | 20 oct. 2026 |

### Le modèle d'import à 3 onglets (ancien format)

| Fait | Source | Vérifié le |
|---|---|---|
| 3 onglets exactement : `campaigns`, `adgroups`, `ads`. 3 lignes d'en-tête (nom du champ, obligatoire ou non, explication), puis les données à partir de la ligne 4. | M | 15 oct. 2026 |
| Le modèle d'Ads Manager contient une ligne d'exemple en italique (`oaitest…`) en ligne 4 : à retirer, et les données s'écrivent en texte normal. | M | 15 oct. 2026 |
| `campaigns` : `campaign_name`, `budget_max` obligatoires ; `budget_type`, `launch_date`, `end_date`, `objective`, `target_countries` facultatifs ; `conversion_event_setting_ids` obligatoire en campagne de conversion (un seul identifiant, en tableau JSON). | M, D | 15 oct. 2026 |
| `adgroups` : `campaign_name`, `adgroup_name` obligatoires ; `max_bid` obligatoire au clic et à la conversion ; `Context Hints` facultatif, en tableau JSON. | M | 15 oct. 2026 |
| `ads` : `adgroup_name`, `title` (24 caractères au plus), `copy` (48 au plus), `link`, `image_link` obligatoires. | M | 15 oct. 2026 |
| L'API accepte des titres de 3 à 50 caractères et des textes de 100 au plus ; **le fichier d'import fixe 24 et 48** : c'est lui qui fait foi pour ce pack. | D, M | 15 oct. 2026 |
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
| Sans ciblage géographique, une campagne peut diffuser dans **tous les pays disponibles** : le pays se renseigne toujours. | D | 20 oct. 2026 |
| Ciblage web séparé par appareil (`desktop_web`, `ios_web`, `android_web`) depuis le 10 sept. 2026. | D | 20 oct. 2026 |
| Rapports de conversions : fenêtres d'attribution par défaut de 30 jours après clic et 1 jour après affichage depuis le 30 sept. 2026 ; les totaux diffèrent des anciens rapports. | D | 20 oct. 2026 |
| Bulk API (création et mise à jour en masse par programme) : aperçu limité, ouvert compte par compte, 1 000 opérations par tâche, mode « validation seule ». | D | 20 oct. 2026 |
| Limites par compte en libre-service : 5 000 campagnes, 5 000 ad groups, 5 000 annonces actives ou en pause. | D | 20 oct. 2026 |

## 2 bis. France et Europe

| Fait | Source | Vérifié le |
|---|---|---|
| Annonce du 18 août 2026 : ChatGPT Ads s'ouvre à 31 marchés européens (les 27 pays de l'UE, Norvège, Islande, Liechtenstein, Suisse), dont la France ; diffusion à partir du 24 août par l'équipe commerciale d'OpenAI et des agences partenaires. | R (citant OpenAI) | 20 oct. 2026 **[à vérifier sur openai.com, page illisible par robot]** |
| Ads Manager en libre-service ouvert en Europe le 31 août 2026, sans engagement minimum de dépense ; inscription avec vérification de l'entreprise et moyen de paiement. | R (citant OpenAI) | 20 oct. 2026 **[à vérifier]** |
| **EEE et Suisse : pas de publicité personnalisée pour l'instant ; les audiences personnalisées ne s'appliquent pas aux campagnes qui ciblent ces pays.** La sélection repose sur la conversation en cours et un contexte limité (localisation générale, appareil, langue). | D (audiences), R (sélection) | 20 oct. 2026 |
| Pixel : le consentement est considéré comme acquis par défaut ; `oaiq("consent", false)` avant `init` bloque l'envoi des événements jusqu'à l'accord. En France, le bandeau de consentement doit piloter ce réglage. | D | 20 oct. 2026 |
| Le budget quotidien minimum dépend de la devise du compte ; montant en euros non trouvé. | D, H | 20 oct. 2026 **[à vérifier dans Ads Manager]** |

## 3. Règles publicitaires (Ad Policies v1.6, 10 septembre 2026)

Synthèse complète, section par section : `commun/politiques-openai.md`.


| Fait | Source | Vérifié le |
|---|---|---|
| Pas d'annonce près des conversations sensibles : santé mentale et personnelle, dépendance émotionnelle, parcours sensibles, et 19 catégories dont sécurité des enfants, politique, vie privée, suicide, armes, biens réglementés. | P | 15 oct. 2026 |
| Catégories de la phase de test : biens ménagers et de consommation, style de vie, services locaux, voyages et expériences, divertissement, produits numériques et éducation. | P | 15 oct. 2026 |
| Services financiers (dont l'assurance), santé et juridique : admis **aux États-Unis seulement**, au cas par cas, pour des annonceurs approuvés ; **hors États-Unis, généralement interdits**. Le pack **alerte** sans bloquer : la décision revient à l'annonceur et à l'examen d'OpenAI. | P | 20 oct. 2026 |
| OpenAI peut refuser un annonceur ou une annonce « pour quelque raison que ce soit », y compris sa position concurrentielle (ajout de la v1.6). | P | 20 oct. 2026 |
| Interdits : contenus adultes et rencontres, alcool (plus de 0,5%), tabac et vapotage, jeux d'argent, contrefaçons, substances récréatives, contenu politique, allégations de bien-être non étayées (détox, minceur), redressement de crédit et règlement de dettes, investissements alternatifs (or), offres d'emploi ou de logement individuelles. | P | 15 oct. 2026 |
| Toute annonce doit être véridique : pas d'affirmation non étayée sur les capacités, les prix, les résultats, les affiliations ou les comparaisons. | P | 15 oct. 2026 |
| L'annonce ne doit pas imiter l'apparence, les fonctions ou la voix de ChatGPT. | P | 15 oct. 2026 |
| Les règles s'appliquent au texte, à l'image et à la page de destination, qui doivent être cohérents de bout en bout. | P | 15 oct. 2026 |
| Examen par systèmes automatisés (dont des LLM) sous contrôle humain ; une annonce ou une page qui ne peut pas être vérifiée ne peut pas être diffusée. | P | 15 oct. 2026 |
| Historique : v1.0 mars 2026, v1.1 avril (conseils médicaux, juridiques et financiers plus bloqués d'office pour le placement), v1.2 mai (examen et application), v1.3 juillet (politiques annonceurs, finance et santé précisées), v1.4 août (logement et emploi), v1.5 août (juridique admis aux États-Unis), v1.6 septembre (droit de refus). | P | 20 oct. 2026 |

## 4. Points à confirmer (choix par défaut du pack)

| Point | Versions en présence | Défaut du pack |
|---|---|---|
| Nombre de hints par ad group | 2 à 3 conseillés en direct à un annonceur ; jusqu'à 2 000 permis (D), « inutile de remplir la limite » | **3** (curseur 2 à 5), avertissement au-delà de 5 |
| Longueur d'un hint | la documentation donne des exemples de 5 à 8 mots ; d'autres sources parlent d'une ou deux phrases | **4 à 8 mots**, une situation par hint |
| Volume d'annonces au lancement | 40 à 50, ou 100 au minimum ; plafond de 5 000 annonces actives par compte (D) ; l'éval à l'aveugle du 15 oct. 2026 a jugé 40 annonces illisibles pour 30 € par jour | **40 à 50** (5 groupes ou plus) quand le budget le permet ; sinon 2 ou 3 annonces par groupe, au choix de l'annonceur ; mode « grande échelle » : 100 |
| Caractères autorisés dans les noms | « no special characters » sans liste | lettres non accentuées, chiffres, `_` et `-` |
| Format d'import | schéma d'annonces à 10 colonnes (S, « seul format compatible » selon l'utilisateur) ; modèle à 3 onglets (M) | **schéma** par défaut ; 3 onglets en option ; import d'essai d'un petit fichier avant la campagne |
| Limites de caractères du schéma | 24 et 48 (M) ; 50 et 100 (D) ; recommandations différentes selon les supports | **24 et 48** (passent partout) ; `--limites api` sur décision de l'annonceur |

## 5. Folklore (à reconnaître et écarter)

- Des limites de 35 et 67 caractères : sans source, contredites par le
  modèle d'import et par l'API.
- « Mettre le maximum de hints pour toucher plus de monde » : la
  documentation dit le contraire (« inutile de remplir la limite ») ; un hint
  hors sujet élargit vers des conversations où l'annonce n'a pas sa place.
- « Les hints sont des mots-clés » : ils peuvent en contenir, mais ne
  fonctionnent pas en correspondance exacte.
- Des taux de conversion ou des retours sur dépense « typiques » de ChatGPT
  Ads : aucun chiffre public vérifiable n'est généralisable ; ne pas en citer.
