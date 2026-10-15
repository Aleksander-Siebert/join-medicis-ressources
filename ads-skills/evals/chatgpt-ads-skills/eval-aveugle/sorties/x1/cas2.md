Voici la campagne Factoria : 6 ad groups et 46 annonces vers la page de démo. Deux valeurs manquent avant l'import, l'identifiant de l'événement de conversion et l'enchère maximale. Je les détaille plus bas.

## 1. Brief, éligibilité, allégations

| Point | Réponse |
|---|---|
| Offre | Logiciel en ligne de devis et factures ; démonstration de 20 minutes |
| Page de destination | https://www.factoria.example/demo/ pour tous les groupes |
| Marché, langue | France et Belgique, français seulement, vouvoiement dans les annonces |
| Personas | Artisans du bâtiment seuls ou avec 1 à 5 salariés ; gérants de TPE de services |
| Hors cible | Grandes entreprises, comptables |
| Moments | Devis faits le soir sur tableur ; factures impayées ; réforme de la facturation électronique |
| Objectif | Conversions (demandes de démo), événement pas encore créé |
| Pays, budget, dates | `["FR","BE"]`, 40 € par jour (Daily), du 2 novembre au 31 décembre 2026 |
| Enchère | {{à compléter : coût par demande de démo visé}} |
| Images | 5 visuels carrés de 1 080 px : devis, relances, tableur, reforme, comptable |

**Éligibilité : autorisée en France et en Belgique.** Un logiciel de facturation est un outil de gestion qui ne vend aucun produit financier : il relève de la catégorie « logiciel », admise par les règles publicitaires d'OpenAI (v1.6, septembre 2026, relues le 15 octobre 2026). L'examen porte aussi sur la page de destination.

**À corriger sur ta page :** la section « Facturation électronique » affiche en clair `{{à compléter : statut exact de la plateforme}}`. OpenAI examine la page, et un prospect inquiet de la réforme tomberait sur ce trou. Remplace-le par ta formulation réelle (« nous ne sommes pas encore plateforme agréée, nous y travaillons ») avant de lancer le groupe réforme.

**Allégations**

| Allégation | Source | Statut |
|---|---|---|
| Logiciel en ligne de devis et de facturation pour les artisans du bâtiment et les TPE de services | page d'accueil | approuvée |
| Créer un devis sur téléphone et le faire signer en ligne | page d'accueil | approuvée |
| Transformer le devis en facture en un clic | page d'accueil | approuvée |
| Relancer automatiquement les factures impayées par e-mail | page d'accueil | approuvée |
| Exporter les écritures pour votre expert-comptable | page d'accueil | approuvée |
| Démonstration de 20 minutes | page d'accueil, lien vers /demo/ | approuvée |
| Disponible en France et en Belgique | page d'accueil | approuvée |
| Nous préparons la réforme de la facturation électronique | page d'accueil | approuvée, telle quelle |
| Essai gratuit de 14 jours, sans carte bancaire | page d'accueil | approuvée, non utilisée |
| 24 € HT par mois et par utilisateur, sans engagement | page d'accueil | approuvée, non utilisée |
| « Conforme », « prêt » ou « agréé » pour la facturation électronique | ta réponse : pas encore plateforme agréée | refusée |
| Gain de temps chiffré (« en quelques minutes », « X heures gagnées ») | interdit par toi | refusée |

Je n'ai pas utilisé l'essai gratuit ni le prix. L'objectif est la demande de démo, et une annonce qui pousse l'essai enverrait vers une autre action que celle que la campagne optimise. J'ai aussi écarté le « en quelques minutes » du titre de la page : c'est trop proche du gain de temps chiffré que tu as interdit.

## 2. Carte des intentions

| Persona | Besoin, dans ses mots | Intention envisagée | Réponse probable de ChatGPT | Étape | Page | Ad group |
|---|---|---|---|---|---|---|
| Artisan seul | « je fais mes devis sur Excel tous les soirs » | sortir du tableur pour les devis et factures | modèles Excel, critères pour passer à un logiciel | découverte | /demo/ | `devis_soir_tableur` |
| Artisan avec 1 à 5 salariés | « faire mes devis chez le client » | faire et faire signer un devis sur place | applis mobiles, valeur de la signature électronique | comparaison | /demo/ | `devis_chantier_signature` |
| Artisan ou gérant de TPE | « des clients ne m'ont pas payé » | relancer les impayés sans le faire à la main | modèles de relance, étapes de recouvrement | découverte | /demo/ | `factures_impayees_relance` |
| Artisan qui a un expert-comptable | « mon comptable me réclame mes factures » | transmettre ses factures sans ressaisie | organisation des pièces, outils d'export | découverte | /demo/ | `export_expert_comptable` |
| Artisan ou gérant de TPE | « la facture électronique devient obligatoire ? » | comprendre la réforme et s'équiper | calendrier, obligations, plateformes agréées | découverte | /demo/ | `reforme_facture_electronique` |
| Gérant de TPE de services | « quel logiciel de devis pour ma petite boîte ? » | comparer des logiciels de devis et factures | critères de choix, liste d'outils | comparaison | /demo/ | `choisir_logiciel_tpe_services` |

Ce que l'annonce apporte que la réponse ne donne pas : voir l'outil en 20 minutes, sur la fonction qui correspond au problème.

**Le groupe réforme demande de la prudence.** ChatGPT parlera de plateformes agréées, et Factoria ne l'est pas encore. Les annonces de ce groupe disent seulement ce qui est vrai (« nous préparons la réforme ») et n'emploient jamais « conforme », « prêt » ou « agréé ». Je l'ai mis dans le fichier, mais ne le lance qu'une fois la page corrigée. Sinon, mets-le en pause juste après l'import. Autre point : la page ne dit pas de quelle réforme il s'agit. Des artisans belges verront aussi ces annonces, vérifie que ton message vaut pour eux {{à compléter}}.

## 3. Ad groups, hints, prompts simulés et annonces

3 hints par groupe (choix par défaut, hypothèse à tester). Chaque hint décrit une situation, sans pays : la France et la Belgique se règlent dans `target_countries`. Les 3 prompts simulés de chaque groupe relèvent de ce groupe et d'aucun autre. Tous les liens vont vers /demo/ avec `utm_source=chatgpt&utm_medium=ads&utm_campaign=factoria_demo_fr_be&utm_content=<nom du groupe>`.

Images : `tableur.png` pour `devis_soir_tableur`, `devis.png` pour `devis_chantier_signature` et `choisir_logiciel_tpe_services`, `relances.png` pour `factures_impayees_relance`, `comptable.png` pour `export_expert_comptable`, `reforme.png` pour `reforme_facture_electronique`. Toutes sont sous https://www.factoria.example/img/. Les idées de visuel ci-dessous servent à vérifier que chaque image colle à son groupe.

### devis_soir_tableur

- Intention : Arrêter de faire ses devis et factures le soir sur un tableur.
- Hints : « artisan qui fait ses devis le soir sur Excel » · « remplacer le tableur pour ses devis et factures » · « artisan seul débordé par la paperasse du soir »
- Prompts simulés :
  - « Je suis plombier, je fais mes devis sur Excel tous les soirs, il y a plus simple ? »
  - « Comment arrêter de passer mes soirées sur les devis et les factures ? »
  - « Modèle de devis Excel pour électricien, ou il vaut mieux passer à un logiciel ? »
- Idée de visuel : Un ordinateur portable ouvert sur un tableur, sur une table de cuisine le soir, lampe allumée, sans texte lisible.

| Titre | Car. | Texte | Car. | Angle |
|---|---|---|---|---|
| Vos devis le soir ? | 19 | Voyez une autre façon en démo de 20 minutes. | 44 | question |
| Quittez le tableur | 18 | Devis, factures et relances au même endroit. | 44 | contraste |
| Le devis devient facture | 24 | Un clic suffit. Démo de 20 minutes en ligne. | 44 | bénéfice |
| Le soir, sans devis | 19 | Faites le devis sur place, depuis le téléphone. | 47 | situation |
| Logiciel pour artisans | 22 | Devis et factures en ligne, pour le bâtiment. | 45 | preuve |
| Assez des formules ? | 20 | Découvrez Factoria en 20 minutes de démo. | 41 | question |
| Du tableur au logiciel | 22 | On vous montre la bascule en démo de 20 min. | 44 | processus |
| Fini la double saisie | 21 | Le devis signé devient facture en un clic. | 42 | objection |

### devis_chantier_signature

- Intention : Faire un devis sur place, depuis le chantier, et le faire signer vite par le client.
- Hints : « faire un devis sur téléphone depuis le chantier » · « faire signer un devis en ligne au client » · « envoyer un devis juste après la visite client »
- Prompts simulés :
  - « Il existe une appli pour faire mes devis directement chez le client sur mon téléphone ? »
  - « Comment faire signer un devis à distance, c'est valable une signature en ligne ? »
  - « Mes clients signent chez la concurrence avant que j'envoie mon devis, comment aller plus vite ? »
- Idée de visuel : Un téléphone posé sur un plan de travail de chantier, écran flouté, outils autour, sans visage.

| Titre | Car. | Texte | Car. | Angle |
|---|---|---|---|---|
| Devis signé sur place | 21 | Créé sur téléphone, signé en ligne. | 35 | bénéfice |
| Le devis sur le chantier | 24 | Créez et envoyez-le depuis votre téléphone. | 43 | situation |
| Signature en ligne | 18 | Votre client signe le devis à distance. | 39 | processus |
| Un client qui hésite ? | 22 | Faites-lui signer le devis en ligne. | 36 | objection |
| Le devis avant de partir | 24 | Créez-le sur votre téléphone, chez le client. | 45 | situation |
| Du devis à la facture | 21 | Un clic transforme le devis signé en facture. | 45 | processus |
| Voir l'appli en 20 min | 22 | Une démo du devis sur téléphone, pour artisans. | 47 | conseil |
| Fait pour le bâtiment | 21 | Devis sur téléphone et signature en ligne. | 42 | preuve |

### factures_impayees_relance

- Intention : Se faire payer les factures en retard sans relancer chaque client à la main.
- Hints : « artisan avec des factures impayées à relancer » · « relancer automatiquement les clients en retard de paiement » · « suivre les paiements clients d'une petite entreprise »
- Prompts simulés :
  - « J'ai trois clients qui ne m'ont pas payé depuis deux mois, comment les relancer sans les fâcher ? »
  - « Modèle de mail de relance pour une facture impayée d'artisan ? »
  - « Comment savoir rapidement quelles factures sont encore impayées dans ma petite boîte ? »
- Idée de visuel : Une pile de factures papier avec une enveloppe ouverte, cadrage serré, sans texte lisible.

| Titre | Car. | Texte | Car. | Angle |
|---|---|---|---|---|
| Des factures impayées ? | 23 | Factoria relance vos clients par e-mail. | 40 | question |
| Relances automatiques | 21 | Les factures en retard relancées par e-mail. | 44 | bénéfice |
| Relancer sans y penser | 22 | Relance des impayés par e-mail, automatique. | 44 | contraste |
| Un client qui tarde ? | 21 | La relance part par e-mail, automatiquement. | 44 | situation |
| Les relances, en démo | 21 | 20 minutes pour voir les relances automatiques. | 47 | processus |
| Qui n'a pas payé ? | 18 | Suivez factures et relances au même endroit. | 44 | preuve |
| Relancer sans gêne | 18 | Un e-mail de relance part pour vous. | 36 | objection |
| Pour artisans et TPE | 20 | Relance automatique des factures impayées. | 42 | preuve |

### export_expert_comptable

- Intention : Transmettre ses factures à son expert-comptable sans tout ressaisir (côté artisan, pas côté cabinet).
- Hints : « artisan qui envoie ses factures à son comptable » · « préparer les documents pour son expert-comptable » · « simplifier sa compta de TPE, pas pour un cabinet »
- Prompts simulés :
  - « Mon comptable me réclame toutes mes factures de l'année, comment je les lui envoie proprement ? »
  - « Quel outil pour que mon expert-comptable récupère mes factures sans que je ressaisisse tout ? »
  - « Je suis menuisier à mon compte, comment je m'organise pour la compta avec mon comptable ? »
- Idée de visuel : Un classeur fermé et une clé USB posés sur un bureau, lumière naturelle, sans texte.

| Titre | Car. | Texte | Car. | Angle |
|---|---|---|---|---|
| Votre comptable attend ? | 24 | Exportez vos écritures depuis Factoria. | 39 | situation |
| Export pour le comptable | 24 | Vos écritures exportées depuis vos factures. | 44 | bénéfice |
| Moins de papiers à trier | 24 | Vos devis et factures en ligne, au même endroit. | 48 | bénéfice |
| Bilan en vue ? | 14 | Exportez vos écritures pour l'expert-comptable. | 47 | situation |
| Le lien avec le cabinet | 23 | Factoria exporte les écritures pour lui. | 40 | processus |
| Ressaisir ? Non merci | 21 | Exportez les écritures pour votre comptable. | 44 | contraste |
| Voir l'export en démo | 21 | 20 minutes pour voir l'export comptable. | 40 | conseil |
| Facturer, puis exporter | 23 | Le devis devient facture, l'export suit. | 40 | processus |

### reforme_facture_electronique

- Intention : S'inquiéter de la réforme de la facturation électronique et chercher un outil pour s'y préparer.
- Hints : « artisan inquiet de la réforme de la facture électronique » · « préparer sa TPE à la facturation électronique » · « choisir un logiciel de factures avant la réforme »
- Prompts simulés :
  - « La facturation électronique devient obligatoire, qu'est-ce que je dois faire en tant qu'artisan ? »
  - « Je fais mes factures sur Word, est-ce que ça va encore passer avec la réforme ? »
  - « Quel logiciel de facturation choisir pour être prêt pour la facture électronique ? »
- Idée de visuel : Une facture papier à côté d'un écran d'ordinateur portable, sans texte lisible ni logo officiel.

| Titre | Car. | Texte | Car. | Angle |
|---|---|---|---|---|
| Facture électronique ? | 22 | Nous préparons la réforme : parlons-en en démo. | 47 | question |
| Réforme en vue ? | 16 | Voyez en démo où en est Factoria sur la réforme. | 48 | transparence |
| Quittez Word et Excel | 21 | Factures en ligne, réforme en préparation. | 42 | contraste |
| Facturation : on avance | 23 | Nous préparons la réforme, démo de 20 minutes. | 46 | processus |
| Préparer la réforme | 19 | Nous y travaillons : voyez où nous en sommes. | 45 | conseil |
| Vos factures en ligne | 21 | Pour artisans, réforme en préparation. | 38 | preuve |

### choisir_logiciel_tpe_services

- Intention : Gérant de TPE de services qui compare des logiciels de devis et factures simples.
- Hints : « gérant de TPE de services qui compare des outils de facturation » · « choisir un logiciel de devis pour une petite équipe » · « facturation simple pour TPE, pas pour une grande entreprise »
- Prompts simulés :
  - « Je gère une petite société de nettoyage avec 4 salariés, quel logiciel de devis et factures prendre ? »
  - « Quels critères pour choisir un logiciel de facturation quand on est une TPE ? »
  - « On est 3 dans ma boîte de dépannage, on cherche un outil simple pour les devis, des conseils ? »
- Idée de visuel : Un petit bureau d'équipe avec deux ordinateurs portables ouverts, écrans flous, sans visage.

| Titre | Car. | Texte | Car. | Angle |
|---|---|---|---|---|
| Une TPE, un seul outil | 22 | Devis, factures et relances au même endroit. | 44 | bénéfice |
| Quel outil pour la TPE ? | 24 | Voyez Factoria en démo de 20 minutes. | 37 | question |
| Pensé pour les TPE | 18 | Devis et factures pour les TPE de services. | 43 | preuve |
| Avant de choisir, voyez | 23 | Une démo de 20 minutes pour vous faire un avis. | 47 | conseil |
| Devis signés en ligne | 21 | Vos clients signent le devis en ligne. | 38 | bénéfice |
| France ou Belgique | 18 | Factoria est disponible dans les deux pays. | 43 | situation |
| Relances incluses | 17 | Les factures impayées relancées par e-mail. | 43 | preuve |
| Plusieurs utilisateurs | 22 | Un logiciel en ligne pour toute l'équipe. | 41 | bénéfice |

## 4. Contrôle par script

Verdict : **bloqué par les deux valeurs manquantes**, rien d'autre. `max_bid` est vide sur les 6 groupes : il est obligatoire en campagne Conversions. L'identifiant de l'événement de conversion n'existe pas encore : j'ai mis un `{{à compléter}}` à sa place, et le script refuse aussi une campagne Conversions sans identifiant. Avec des valeurs de test à ces deux endroits, la campagne passe à « prêt » : 0 bloquant, 0 attention. Tous les titres font 24 caractères au plus, tous les textes 48 au plus, chaque chiffre renvoie à une allégation approuvée, il n'y a ni chevauchement de hints entre groupes ni mot d'une catégorie restreinte, et les noms sont identiques d'un onglet à l'autre. Restent deux informations : un titre court (« Bilan en vue ? », 14 caractères), gardé volontairement ; et les codes FR et BE, valides mais pas forcément ouverts à la publicité pour ton compte, à vérifier dans Ads Manager.

## 5. Le fichier d'import

Le XLSX n'est pas écrit : le script refuse tant qu'il reste un point bloquant. Le contenu est prêt :

- `campaigns` : `factoria_demo_fr_be` · budget_max 40 · Daily · 2026-11-02 · 2026-12-31 · Conversions · `["{{à compléter}}"]` · `["FR","BE"]`
- `adgroups` : les 6 groupes ci-dessus, max_bid `{{à compléter}}`, hints en tableau JSON
- `ads` : les 46 annonces ci-dessus, lien /demo/ avec UTM, image du groupe

Dès que tu me donnes les deux valeurs, je valide de nouveau et j'exporte le fichier.

**L'événement de conversion.** Crée-le dans Ads Manager avant tout, avec le pixel ou l'API Conversions (plus fiable que le pixel seul), déclenché à la confirmation de la réservation sur /demo/. Événement standard conseillé : `appointment_scheduled`, puisque la page propose de « réserver une démonstration ». Si ton formulaire enregistre seulement une demande, sans créneau, prends `lead_created`. Ce choix est définitif : une campagne n'a qu'un événement standard, et il ne change plus après la création. Colle ensuite son identifiant dans `conversion_event_setting_ids`, sous la forme `["identifiant"]`.

**L'enchère.** En Conversions, `max_bid` est le coût par demande de démo que tu vises, mais tu paies au clic. Les 3 à 5 USD qu'OpenAI conseille pour commencer valent pour une enchère au clic, pas pour celle-ci. Je ne peux pas fixer le montant sans tes chiffres. Le calcul : ce que tu acceptes de payer pour une démo = valeur d'un client {{à compléter}} × part des démos qui deviennent clients {{à compléter}}, avec une marge de prudence au lancement. Même montant sur les 6 groupes pour commencer, afin de pouvoir les comparer.

## 6. Avant de dépenser

1. **Corrige la section réforme de la page**, puis relis les règles publicitaires d'OpenAI à la date du lancement.
2. **Mesure testée avant la première dépense** : une demande de démo de test doit remonter dans les événements récents d'Ads Manager. Sans elle, l'optimisation Conversions travaille à l'aveugle.
3. **Budget quotidien** : c'est ton choix, et c'est ce que conseille le modèle d'import. Il est aussi exigé si tu passes plus tard en stratégie « Maximize Results », sans enchère maximale.
4. **Commence petit** : 40 € par jour sur 6 groupes, c'est peu par groupe. Le groupe réforme reste en pause tant que la page n'est pas corrigée.
5. **Lire par groupe** et changer un réglage à la fois. La dépense peut s'afficher avec 7 à 8 heures de retard. Fixe ton seuil de décision avant de couper un groupe {{à compléter : seuil de décision}}.
6. **Dans Ads Manager, hors fichier** : hints d'exclusion (si ton compte y a accès) pour « logiciel pour cabinet d'expertise comptable », « ERP pour grande entreprise » et « recouvrement judiciaire, injonction de payer, avocat » ; choix des plateformes (iOS, Android, web).
7. **Import d'essai** : importe d'abord un petit fichier (une campagne en pause, un groupe, une annonce).

**Checklist de relecture** (une personne de ton équipe, avant import)

- [ ] Catégorie et pays éligibles, règles publicitaires relues le {{à compléter : date}}.
- [ ] Section « Facturation électronique » de la page corrigée.
- [ ] Chaque annonce relue en entier, à voix haute. Aucune ne laisse croire que Factoria est déjà conforme ou agréé.
- [ ] Aucun gain de temps chiffré, aucune imitation de ChatGPT, aucune affiliation suggérée.
- [ ] /demo/ ouverte : bonne page, accessible sans connexion, cohérente avec les fonctions citées dans les annonces, UTM corrects.
- [ ] Les 5 images ouvertes : carrées, 1 080 px, PNG, lisibles en petit, droits acquis. `devis.png` sert à deux groupes.
- [ ] Hints : aucun ne vise une conversation sensible ni un pays.
- [ ] Noms de campagne et d'ad groups identiques dans les 3 onglets.
- [ ] Budget, Daily, dates, Conversions, `["FR","BE"]`, enchères conformes à ta décision.
- [ ] Événement de conversion créé, testé, identifiant collé.
- [ ] Import d'essai réussi, rapport du script à 0 bloquant.

**À vérifier**

- Identifiant de l'événement de conversion {{à compléter}}, et choix entre `appointment_scheduled` et `lead_created`.
- Enchère maximale (coût par démo visé) {{à compléter}}.
- Formulation exacte de ton statut sur la facturation électronique, à publier sur la page {{à compléter}}.
- La réforme évoquée par la page vaut-elle pour la Belgique ? {{à compléter}}
- Je n'ai lu que la page d'accueil. Vérifie que /demo/ reprend les fonctions citées (devis sur téléphone, signature en ligne, relances, export comptable).
- Ouverture de la France et de la Belgique à la publicité dans ton compte Ads Manager (annonce d'OpenAI sur l'ouverture européenne du 24 août 2026 [à vérifier]).
- Hypothèses à tester, pas des règles : 3 hints par groupe, 46 annonces au lancement, acceptation du modèle d'import par Ads Manager.
