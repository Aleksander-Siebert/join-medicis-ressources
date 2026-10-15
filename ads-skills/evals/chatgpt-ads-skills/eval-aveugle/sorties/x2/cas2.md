# Campagne ChatGPT Ads : Factoria, demandes de démo, France et Belgique

Voici la campagne, prête à reporter dans le fichier d'import. Une campagne de conversions, 3 groupes d'annonces actifs (un par situation de l'artisan), 2 annonces par groupe, toutes vers https://www.factoria.example/demo/. Toutes les annonces respectent les limites du fichier : titre de 24 caractères au plus, texte de 48 au plus.

**Deux champs obligatoires bloquent l'import tant qu'ils sont vides :** l'identifiant de l'événement de conversion (`conversion_event_setting_ids`) et l'enchère (`max_bid`). Je les ai laissés à {{à compléter}} plutôt que d'inventer des valeurs. Et je n'ai pas mis en ligne le groupe « réforme de la facturation électronique » : voir plus bas.

## Campagne

| Colonne | Valeur |
|---|---|
| campaign_name | Factoria - FR BE - Démos - fin 2026 |
| budget_max | 40 |
| budget_type | Daily |
| launch_date | 2026-11-02 |
| end_date | 2026-12-31 |
| objective | Conversions |
| conversion_event_setting_ids | ["{{à compléter}}"] |
| target_countries | ["FR", "BE"] |

Liens : `https://www.factoria.example/demo/?utm_source=chatgpt&utm_medium=cpc&utm_campaign=factoria-frbe-demos-fin2026&utm_content={groupe}_{a|b}`.

## À faire avant l'import

1. **Créer l'événement de conversion dans Ads Manager.** Déclenchez-le sur la confirmation de réservation de la démo, pas sur la simple visite de `/demo/`, sinon la campagne optimisera vers des visiteurs et non vers des rendez-vous. Copiez ensuite son identifiant dans `conversion_event_setting_ids`. Le marqueur de suivi doit passer par votre bandeau de consentement aux cookies, en France comme en Belgique.
2. **Fixer l'enchère.** Règle de calcul proposée : **enchère max par démo = taux de démos qui deviennent clients × valeur d'un client**, avec valeur d'un client = 24 € HT × nombre moyen d'utilisateurs × durée moyenne d'abonnement en mois. Vos chiffres : {{à compléter}}% × {{à compléter}} €. Même valeur pour les 3 groupes au départ. À vérifier dans Ads Manager : l'unité exacte de `max_bid` pour l'objectif Conversions [à vérifier].
3. **Retirer le texte provisoire de votre page d'accueil.** La section « Facturation électronique » affiche encore « {{à compléter : statut exact de la plateforme}} ». Un prospect qui passe de `/demo/` à l'accueil le verra.

## Groupe 1 : Devis du soir sur tableur

Image : https://www.factoria.example/img/tableur.png

Context Hints :
- modèle de devis artisan sur Excel ou sur tableur
- faire ses devis le soir après le chantier
- remplacer un tableur par un logiciel de devis
- faire signer un devis en ligne à un client
- transformer un devis en facture

| | Titre (car.) | Texte (car.) |
|---|---|---|
| 1A | Vos devis sur tableur ? (23) | Créez vos devis sur téléphone, signés en ligne. (47) |
| 1B | Le devis devient facture (24) | En un clic. Voyez-le en démo de 20 minutes. (43) |

1A part du problème (le tableur), 1B d'une fonction précise.

## Groupe 2 : Factures impayées

Image : https://www.factoria.example/img/relances.png

Context Hints :
- client qui ne paie pas sa facture, comment le relancer
- modèle de mail de relance pour facture impayée
- relancer automatiquement ses factures
- retards de paiement quand on est artisan ou TPE

| | Titre (car.) | Texte (car.) |
|---|---|---|
| 2A | Des factures impayées ? (23) | Relances automatiques par e-mail. Démo 20 min. (46) |
| 2B | Relancez sans y penser (22) | Les impayés relancés automatiquement par e-mail. (48) |

Pas d'indice sur la mise en demeure ou l'injonction de payer : ces conversations relèvent du juridique, et Factoria n'y répond pas.

## Groupe 3 : Choix d'un logiciel de devis

Image : https://www.factoria.example/img/devis.png

Context Hints :
- logiciel de devis et factures pour artisan du bâtiment
- comparatif de logiciels de facturation pour TPE
- faire ses devis sur téléphone depuis le chantier
- logiciel de facturation pour indépendant en Belgique
- logiciel de devis pour artisan seul ou petite équipe

| | Titre (car.) | Texte (car.) |
|---|---|---|
| 3A | Logiciel de devis ? (19) | Pour artisans du bâtiment et TPE de services. (45) |
| 3B | Une démo de 20 minutes (22) | Du devis signé à la relance, vu en direct. (42) |

## Groupe non importé : réforme de la facturation électronique

C'est un de vos moments forts, et l'image `reforme.png` est prête, mais je ne le lance pas maintenant. Un artisan inquiet de la réforme cherche un outil prêt ; vous m'avez dit que Factoria n'est pas encore plateforme agréée, et votre page n'indique pas encore de statut. Une annonce sur ce sujet attirerait des demandes de démo qui ne peuvent pas aboutir, ou laisserait croire à une conformité que vous n'avez pas.

Je l'ajoute dès que deux conditions sont remplies : le statut exact est écrit sur la page, et vous validez une formulation qui ne laisse pas entendre que Factoria est agréée.

## Deux points de vigilance

1. **Belgique.** D'après mes connaissances, la facturation électronique structurée entre entreprises est obligatoire en Belgique depuis le 1er janvier 2026 [à vérifier sur le site du SPF Finances]. Si c'est confirmé, un artisan belge qui facture des professionnels a besoin d'un outil conforme dès maintenant, et une partie du budget belge risque de produire des démos sans suite. Côté France, le calendrier que je connais prévoit la réception des factures électroniques pour toutes les entreprises depuis le 1er septembre 2026 et l'émission pour les TPE et PME au 1er septembre 2027 [à vérifier sur impots.gouv.fr]. Je garde la Belgique dans `target_countries` comme vous l'avez demandé ; si la vérification confirme l'obligation belge, je vous conseille de passer à `["FR"]` jusqu'à ce que votre statut soit réglé. Autre point : vos annonces sont en français, elles toucheront peu la Flandre.
2. **Les images.** J'ai associé `tableur.png`, `relances.png` et `devis.png` aux trois groupes ; les deux annonces d'un groupe partagent la même image puisque le test porte sur le texte. Je n'utilise pas `comptable.png` : les comptables ne sont pas votre cible, et un visuel centré sur eux risque de les attirer. Vérifiez que vos visuels de 1 080 px correspondent au format exigé par Ads Manager [à vérifier] et qu'ils restent lisibles en vignette d'environ 100 px : pas de texte, une seule forme forte, pas de logo (il s'affiche déjà dans le coin de l'annonce).

Vos interdits sont respectés : aucun gain de temps chiffré (les « 20 minutes » sont la durée de la démo), aucune promesse sur la facturation électronique. Formats du fichier : dates au format AAAA-MM-JJ, pays en codes ISO, budget en euros, à confirmer avec le modèle d'import [à vérifier].

Je peux préparer d'autres titres pour un groupe précis, ou rédiger le groupe « réforme » dès que votre statut est écrit sur la page.
