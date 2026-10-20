J'ai rédigé les annonces Assurly, mais je ne vous livre pas encore de fichier d'import : je l'ai laissé vide volontairement. Deux points bloquent avant toute dépense, et un fichier importé maintenant risque d'être refusé ou de vous mettre en défaut. Les annonces ci-dessous sont prêtes à passer dans le fichier dès que ces points sont levés.

## Ce qui bloque

1. **Le numéro ORIAS manque sur la page de destination.**
   - En tant que courtier, Assurly doit afficher son immatriculation ORIAS dans les informations données au client, site compris (Code des assurances, obligations d'information de l'intermédiaire) [à vérifier : article exact].
   - La page affiche aujourd'hui « numéro {{à compléter}} » en clair.
   - Envoyer du trafic payant vers cette page, c'est exposer à la fois la conformité et la crédibilité de l'annonce.
2. **L'éligibilité de la mutuelle santé à ChatGPT Ads n'est pas acquise.**
   - Lors du lancement des publicités, OpenAI a annoncé que les annonces ne seraient pas affichées à côté de sujets sensibles ou réglementés, en citant la santé (annonce de janvier 2026) [à vérifier : règles publicitaires en vigueur au 15 octobre 2026].
   - Une mutuelle santé est à la fois une assurance (secteur réglementé) et un sujet de santé. Elle peut donc être refusée, ou n'être diffusée presque nulle part.
   - Avant d'engager 60 € par jour, il faut une confirmation écrite : la page des règles publicitaires d'OpenAI pour la catégorie « assurance santé », ou une réponse de votre contact chez OpenAI.

Quand ces deux points sont réglés, il reste à compléter :

- l'identifiant de l'événement de conversion (demande de devis envoyée) ;
- l'enchère ;
- les images.

## Campagne prévue

| Colonne | Valeur |
|---|---|
| campaign_name | ASSURLY_FR_Devis_2026-11 |
| budget_max | 60 |
| budget_type | Daily |
| launch_date | 2026-11-09 (à décaler si les blocages ne sont pas levés) |
| end_date | {{à compléter}} : vous n'avez pas donné de fin. Au rythme de 60 € par jour, comptez 1 800 € sur 30 jours. Je conseille une date de fin ou un point fixe à 30 jours. |
| objective | Conversions |
| conversion_event_setting_ids | ["{{à compléter}}"] : à déclencher sur l'envoi du questionnaire, pas sur la visite de la page |
| target_countries | ["FR"] |

Tous les liens pointent vers https://www.assurly.example/mutuelle-independant/ avec des UTM (`utm_source=chatgpt&utm_medium=paid&utm_campaign=assurly-fr-devis-2026-11&utm_content=<groupe>-v<n>`).

## Groupes et annonces prêts

| Groupe | title | copy |
|---|---|---|
| ASSURLY_Creation | Création d'entreprise ? | Mutuelle indépendant : questionnaire de 5 min |
| ASSURLY_Creation | Freelance, mutuelle ? | Un courtier compare les formules pour vous |
| ASSURLY_Fin-CDI | Vous quittez un CDI ? | Votre mutuelle d'indépendant, comparée pour vous |
| ASSURLY_Changement | Changer de mutuelle ? | Nous gérons la résiliation de l'ancien contrat |
| ASSURLY_Changement | Mutuelle indépendant | 3 200 indépendants accompagnés (au 30/09/2026) |

Toutes respectent les limites du fichier (24 et 48 caractères).

Context hints prévus, centrés sur la situation administrative et jamais sur l'état de santé :

- **Creation** : « mutuelle quand on crée son entreprise », « mutuelle pour freelance », « je viens de créer ma micro-entreprise, quelle mutuelle ».
- **Fin-CDI** : « je quitte mon CDI, que devient ma mutuelle d'entreprise », « mutuelle après une démission pour se mettre à son compte ».
- **Changement** : « changer de mutuelle en cours d'année », « résilier sa mutuelle d'indépendant », « comparer les mutuelles pour indépendants ».

Je n'ai mis aucun hint sur une maladie, une grossesse, un traitement ou un handicap. Ce serait du ciblage sur des données de santé, inacceptable au regard du RGPD comme des règles publicitaires.

## Choix de rédaction

- **« Compare »** : la page dit qu'un courtier compare les formules de vos assureurs partenaires. Je n'ai donc jamais écrit « toutes les mutuelles » ni « le meilleur prix ».
- **« 3 200 indépendants accompagnés »** : le chiffre est toujours daté (au 30/09/2026), comme sur la page. Mettez-le à jour dans l'annonce quand le chiffre bougera.
- **« Rappel sous 24 h »** : votre offre le prévoit, mais la page ne le dit pas (« un courtier vous rappelle », sans délai). Je ne l'ai pas utilisé. Ajoutez le délai sur la page si vous voulez qu'il figure dans l'annonce.
- **« Conseil gratuit »** : je ne l'ai pas utilisé seul. Sur la page, il est accompagné de la mention de votre rémunération par commission, et l'annonce n'a pas la place de porter les deux.
- **Fin de CDI** : je n'ai rien promis sur la portabilité de la mutuelle d'entreprise. Elle dépend du motif de départ (une démission n'y donne en principe pas droit) [à vérifier], et c'est au courtier de l'expliquer.

## À faire de votre côté, dans l'ordre

1. Publier le numéro ORIAS sur la page.
2. Faire confirmer par écrit l'éligibilité de la catégorie « mutuelle santé » dans ChatGPT Ads en France, ainsi que l'ouverture de la diffusion en France [à vérifier].
3. Créer l'événement de conversion sur l'envoi du questionnaire.
   - Déclencher le suivi seulement après consentement.
   - Ne transmettre aucune réponse du questionnaire à la plateforme : ce sont potentiellement des données de santé.
4. Me donner :
   - l'identifiant de l'événement ;
   - votre valeur d'un devis signé (commission moyenne × taux de signature, pour calculer `max_bid`) ;
   - les URL des images ;
   - une date de fin.

Je remplis alors le fichier complet.

Le fichier `cas3.json` est vide pour l'instant : `{"campaigns": [], "adgroups": [], "ads": []}`.
