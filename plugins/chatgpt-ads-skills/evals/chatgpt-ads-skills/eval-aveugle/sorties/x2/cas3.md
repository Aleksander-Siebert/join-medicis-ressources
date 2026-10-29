# Campagne ChatGPT Ads : Assurly, mutuelle des indépendants, France

Voici la campagne, prête à reporter dans le fichier d'import. Une campagne de conversions, 3 groupes d'annonces (un par moment de vie du freelance), 2 annonces par groupe, toutes vers https://www.assurly.example/mutuelle-independant/. Toutes les annonces respectent les limites du fichier : titre de 24 caractères au plus, texte de 48 au plus.

**Ne lancez pas avant d'avoir publié votre numéro ORIAS sur la page.** Votre page affiche encore « immatriculé à l'ORIAS sous le numéro {{à compléter}} ». Un courtier doit communiquer son immatriculation [à vérifier : article exact du Code des assurances], et envoyer du trafic payant vers une page d'assurance sans ce numéro expose Assurly sur le plan réglementaire et fragilise la confiance au moment où le prospect laisse ses coordonnées. Les annonces sont prêtes ; c'est la page qui ne l'est pas.

## Campagne

| Colonne | Valeur |
|---|---|
| campaign_name | Assurly - FR - Devis mutuelle - 2026 |
| budget_max | 60 |
| budget_type | Daily |
| launch_date | 2026-11-09 |
| end_date | vide (vous n'avez pas donné de date de fin) |
| objective | Conversions |
| conversion_event_setting_ids | ["{{à compléter}}"] |
| target_countries | ["FR"] |

Liens : `https://www.assurly.example/mutuelle-independant/?utm_source=chatgpt&utm_medium=cpc&utm_campaign=assurly-fr-devis-2026&utm_content={groupe}_{a|b}`.

## À faire avant l'import

1. **Événement de conversion.** Si l'événement « demande de devis » n'existe pas encore dans Ads Manager, créez-le sur la validation du questionnaire (page ou message de confirmation), puis copiez son identifiant dans `conversion_event_setting_ids`. Sans lui, l'import d'une campagne de conversions est refusé.
2. **Enchère (`max_bid`, obligatoire).** Laissée à {{à compléter}}. Règle de calcul proposée : **enchère max par demande de devis = taux de demandes qui aboutissent à un contrat × commission moyenne par contrat**. Vos chiffres : {{à compléter}}% × {{à compléter}} €. Même valeur pour les 3 groupes au départ ; l'unité exacte de `max_bid` est à confirmer dans Ads Manager [à vérifier].
3. **Images.** Pas encore prêtes : `image_link` vaut {{à compléter}}. Prompts plus bas.
4. **Page de destination.** Je n'ai vu que le contenu de votre page d'accueil. Vérifiez que `/mutuelle-independant/` reprend les mêmes éléments que les annonces : questionnaire de 5 minutes, rappel par un courtier, 3 200 indépendants accompagnés avec sa date, rémunération par l'assureur, prise en charge de la résiliation.

## Groupe 1 : Création d'entreprise

Context Hints :
- je viens de créer mon entreprise, dois-je prendre une mutuelle
- mutuelle santé pour freelance ou micro-entrepreneur
- protection sociale quand on devient indépendant
- démarches après la création d'une entreprise individuelle

| | Titre (car.) | Texte (car.) |
|---|---|---|
| 1A | Vous vous lancez ? (18) | Un courtier compare des mutuelles pour vous. (44) |
| 1B | Mutuelle d'indépendant (22) | Déjà 3 200 indépendants accompagnés. (36) |

## Groupe 2 : Fin de la mutuelle d'entreprise

Context Hints :
- je quitte mon CDI, que devient ma mutuelle d'entreprise
- mutuelle après une démission pour se mettre à son compte
- passer de salarié à freelance, quelle couverture santé
- fin de la portabilité de la mutuelle d'entreprise

| | Titre (car.) | Texte (car.) |
|---|---|---|
| 2A | Vous quittez votre CDI ? (24) | Votre mutuelle d'indépendant, via un courtier. (46) |
| 2B | Mutuelle après un CDI (21) | 5 min en ligne, puis un courtier vous rappelle. (47) |

## Groupe 3 : Changer de mutuelle

Context Hints :
- comment changer de mutuelle en cours d'année
- résilier sa mutuelle santé d'indépendant
- comparer les mutuelles pour indépendants
- ma mutuelle d'indépendant ne me convient plus

| | Titre (car.) | Texte (car.) |
|---|---|---|
| 3A | Changer de mutuelle ? (21) | Nous gérons la résiliation de l'ancien contrat. (47) |
| 3B | Conseil gratuit (15) | Nous sommes rémunérés par l'assureur. (37) |

## Pourquoi ces formulations

- **Uniquement ce qui est sur votre page.** Le rappel « sous 24 h » n'y figure pas : je ne l'ai pas utilisé. Ajoutez-le à la page si vous voulez que je l'intègre aux annonces.
- **Pas de promesse de prix ni de couverture.** Ni « moins cher », ni « meilleure mutuelle », ni économies : vos prix sont sur devis. J'écris « compare des mutuelles » et non « toutes les mutuelles », puisque le courtier compare les formules de vos assureurs partenaires.
- **« Conseil gratuit » est toujours accompagné de son explication** (rémunération par l'assureur), comme sur votre page.
- **« 3 200 indépendants accompagnés »** date du 30 septembre 2026 : mettez le chiffre à jour dans l'annonce 1B à chaque fois que vous le changez sur la page.
- **Changement en cours d'année.** Je ne promets pas qu'on peut changer « à tout moment » : la résiliation sans frais en cours d'année n'est possible qu'après un an de contrat [à vérifier : loi du 14 juillet 2019 sur la résiliation sans frais des complémentaires santé].
- **Aucun indice de contexte lié à une maladie, un traitement ou un état de santé.** Les annonces ne visent que des conversations administratives (création, départ de CDI, résiliation). Cibler des conversations sur la santé des personnes serait délicat au regard du RGPD et probablement des règles publicitaires de la plateforme sur la santé et l'assurance [à vérifier dans la politique publicitaire d'OpenAI].

## Données personnelles

Si votre questionnaire demande des informations de santé, ce sont des données sensibles au sens du RGPD (article 9). L'événement de conversion ne doit transmettre aucune réponse du questionnaire à la plateforme publicitaire, seulement le fait qu'une demande a été envoyée. Le marqueur de suivi passe par votre bandeau de consentement aux cookies.

## Images (`image_link`, obligatoire)

Une image par groupe, partagée par ses deux annonces. Elle s'affiche en vignette d'environ 100 px : une seule forme simple, sans texte ni logo (il s'affiche déjà dans le coin de l'annonce). Vérifiez dans Ads Manager le format et la taille exigés [à vérifier].

Couleurs : je n'ai pas vos codes. Par défaut, fond `#0F0F0F` et couleur d'accent {{à compléter : couleur de marque en hexadécimal}}.

Prompt de base, à coller dans Gemini ou Imagen :

```
Crée une icône carrée de 1024 x 1024 px. Composition géométrique pure, sans texte, sans personne, sans élément photographique.
Fond : uni #0F0F0F.
Forme principale : [FORME PRINCIPALE], en blanc (#FFFFFF), occupant environ 70% de l'image, centrée.
Forme d'accent : [FORME D'ACCENT], en [COULEUR D'ACCENT], point focal à l'intérieur ou à la base de la forme principale.
Style : minimaliste, fort contraste, formes pleines, lisible en vignette de 80 à 100 px. Pas de dégradé, pas d'ombre, pas de halo, pas de détail fin, pas de contour.
```

| Groupe | Forme principale | Forme d'accent |
|---|---|---|
| 1. Création d'entreprise | trois barres horizontales empilées aux coins arrondis, de plus en plus larges vers le bas | la barre du bas, la plus large |
| 2. Fin de la mutuelle d'entreprise | un bouclier plein | un petit carré plein au centre du bouclier |
| 3. Changer de mutuelle | un chevron plein pointant vers la droite | un second chevron plus petit, juste derrière, légèrement décalé |

Dès que le numéro ORIAS est en ligne et l'événement de conversion créé, la campagne peut partir telle quelle. Je peux aussi proposer d'autres titres pour un groupe précis.
