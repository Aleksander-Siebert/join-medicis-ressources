Voici la campagne Factoria pour les demandes de démo. Elle couvre la France et la Belgique, en français, avec 1 campagne, 3 groupes et 7 annonces. Tout respecte les limites du fichier (24 et 48 caractères). Deux éléments bloquent l'import tel quel : l'identifiant de l'événement de conversion, qui n'existe pas encore, et l'enchère. J'ai aussi laissé de côté l'angle « réforme de la facturation électronique », pour les raisons expliquées plus bas.

## Campagne

| Colonne | Valeur |
|---|---|
| campaign_name | FACTORIA_FR-BE_Demo_2026-11 |
| budget_max | 40 |
| budget_type | Daily |
| launch_date | 2026-11-02 |
| end_date | 2026-12-31 |
| objective | Conversions |
| conversion_event_setting_ids | ["{{à compléter}}"] |
| target_countries | ["FR", "BE"] |

Dépense maximale sur la période : 60 jours × 40 € = 2 400 €.

## Groupes, cibles et images

| Groupe | Persona / moment | Images |
|---|---|---|
| FACTORIA_Devis-chantier | Artisans du bâtiment qui font leurs devis le soir sur tableur | devis.png, tableur.png |
| FACTORIA_Impayes | Artisans et TPE confrontés aux factures impayées | relances.png |
| FACTORIA_Gestion-TPE | Gérants de TPE de services, artisans seuls, envoi à l'expert-comptable | comptable.png |

Les context hints décrivent les conversations d'un artisan ou d'un gérant : « faire un devis depuis son téléphone sur le chantier », « remplacer mon tableur Excel pour les devis et factures », « comment relancer une facture impayée », « logiciel de facturation pour TPE de services »… La liste complète est dans le fichier.

Je n'ai mis aucun hint pour les grandes entreprises ni pour le métier de comptable. Le visuel comptable.png sert à parler à l'artisan dont le comptable attend les écritures, et pas aux cabinets.

## Annonces

Toutes pointent vers https://www.factoria.example/demo/ avec des UTM (`utm_source=chatgpt&utm_medium=paid&utm_campaign=factoria-fr-be-demo-2026-11&utm_content=<groupe>-v<n>`).

| Groupe | title | copy | image |
|---|---|---|---|
| Devis-chantier | Devis faits le soir ? | Faites-les sur le chantier, signés en ligne | devis.png |
| Devis-chantier | Devis sur tableur ? | Devis et factures en ligne pour artisans | tableur.png |
| Devis-chantier | Devis depuis le chantier | Signé en ligne, transformé en facture en un clic | devis.png |
| Impayés | Factures impayées ? | Relances automatiques par e-mail. Démo 20 min | relances.png |
| Impayés | Relancez sans y penser | Factoria relance vos impayés par e-mail | relances.png |
| Gestion-TPE | Gérant de TPE ? | Devis, factures et relances en ligne. Démo | comptable.png |
| Gestion-TPE | Votre comptable attend ? | Exportez vos écritures pour l'expert-comptable | comptable.png |

Allégations : uniquement celles de la page (devis sur téléphone et signature en ligne, devis transformé en facture en un clic, relance automatique par e-mail, export pour l'expert-comptable, démo de 20 minutes). Il n'y a aucun gain de temps chiffré. J'ai même évité « en quelques minutes » (le titre de votre page), trop proche d'une promesse de temps.

## Pourquoi l'angle « réforme » n'est pas dans le fichier

C'est le moment qui inquiète le plus vos prospects, mais aujourd'hui une annonce sur ce sujet vous expose :

- **Statut de Factoria** : vous n'êtes pas encore plateforme agréée. Une annonce « réforme » laisse entendre que vous y répondez, et le prospect découvrira le contraire en démo. C'est une démo gâchée, et c'est une pratique potentiellement trompeuse.
- **La page n'est pas prête** : la section « Facturation électronique » affiche encore `{{à compléter : statut exact de la plateforme}}` en clair. Corrigez-la avant le 2 novembre, même sans annonce dédiée, car les prospects des autres groupes la liront.
- **Belgique** : l'obligation de facturation électronique B2B (via Peppol) s'applique depuis le 1er janvier 2026 [à vérifier]. Un artisan belge risque donc de demander une démo pour un besoin que Factoria ne couvre peut-être pas encore. En France, l'obligation de réception démarre le 1er septembre 2026 pour toutes les entreprises, et l'émission le 1er septembre 2027 pour les TPE et PME [à vérifier].

Le visuel reforme.png reste donc de côté. Quand le statut sera publié sur la page, voici un brouillon prêt à ajouter (groupe FACTORIA_Reforme, France seulement) :

| title | copy |
|---|---|
| Facture électronique ? | Ce que la réforme change pour votre entreprise |

Je ne le mettrai dans le fichier qu'avec une phrase de la page qui dit exactement où en est Factoria.

## À compléter avant l'import

1. **conversion_event_setting_ids** : créez l'événement dans Ads Manager.
   - Déclenchez-le sur la confirmation de réservation de la démo (page de remerciement ou validation du créneau), et non sur la simple visite de /demo/.
   - Collez ensuite son identifiant à la place de `{{à compléter}}`.
   - Activez ce suivi seulement après consentement au bandeau cookies (RGPD).
   - Si l'événement n'est pas prêt le 2 novembre, deux options sont possibles, et c'est à vous de choisir : décaler le lancement, ou démarrer en objectif Clicks puis basculer.
2. **max_bid** : `{{à compléter}}` pour les 3 groupes. Je n'ai pas vos chiffres, donc je ne propose pas de montant. La règle de calcul :
   - coût max acceptable d'une démo = valeur d'un client (24 € HT par mois et par utilisateur × durée moyenne d'abonnement {{à compléter}}) × taux démo vers client {{à compléter}} × part que vous acceptez d'investir ;
   - vérifiez aussi ce que `max_bid` représente pour une campagne Conversions (enchère au clic ou coût par conversion) et dans quelle devise [à vérifier dans Ads Manager].
3. **Images** : j'ai repris les noms que vous m'avez donnés, sous https://www.factoria.example/img/. Vérifiez que les 4 URL utilisées répondent bien en accès public.

## Points de vigilance

- **Belgique en français seulement** : le fichier ne cible qu'un pays, pas une langue. Les hints et les annonces en français limitent la diffusion aux conversations francophones en pratique [à vérifier], mais rien ne garantit l'exclusion des conversations en néerlandais.
- **Formats** : j'ai mis les dates en AAAA-MM-JJ et les pays en codes ISO à deux lettres [à vérifier sur la ligne d'exemple du fichier].
- **Disponibilité** : vérifiez dans Ads Manager que la diffusion est ouverte en France et en Belgique [à vérifier].
- **Fin décembre** : les deux dernières semaines de l'année sont souvent creuses pour les prises de rendez-vous B2B. Surveillez le coût par démo après le 20 décembre plutôt que de dépenser 40 € par jour à l'aveugle.

Le contenu complet du fichier est dans `cas2.json`.
