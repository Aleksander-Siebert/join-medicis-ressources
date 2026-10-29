# Carte des intentions : du client à l'ad group

La carte relie une personne à une conversation probable avec ChatGPT, puis à
un ad group. Son pivot est l'**intention envisagée** : ce que la personne
cherche à faire au moment où elle écrit, dit en une phrase. Les hints, les
annonces et la page de destination en découlent.

## 1. Les colonnes

| Colonne | Question | Exemple (Vélora, fictif) |
|---|---|---|
| Persona | qui ? | salariée en périphérie, 18 km de trajet |
| Besoin, dans ses mots | qu'écrirait-elle ? | « je veux arrêter la voiture pour aller au bureau » |
| Intention envisagée | que cherche-t-elle à faire maintenant ? | remplacer la voiture pour le trajet domicile-travail |
| Réponse attendue de ChatGPT | que va probablement contenir la réponse ? | comparaison voiture, transports, vélo électrique ; autonomie ; budget |
| Étape | découverte, comparaison, décision, après-achat | comparaison |
| Page de destination | où le clic doit-il mener ? | /velos-ville/ |
| Ad group | nom technique | `trajet_travail_sans_voiture` |

La colonne « réponse attendue » sert à vérifier que l'annonce complète la
réponse au lieu de la répéter : si ChatGPT donne déjà la liste des critères,
l'annonce apporte ce que la réponse ne peut pas donner (l'offre, la
garantie, le service).

## 2. Trouver les intentions

1. Pars des personas et du moment du parcours (questions 3 et 4 de
   l'entretien).
2. Pour chaque persona, écris les situations où elle demanderait de l'aide :
   un problème, un choix, une crainte, une préparation, un « comment faire ».
3. Ajoute ce que disent les sources : termes de recherche, FAQ, avis,
   questions au service client (`references/sources.md`).
4. Regroupe ce qui appelle **le même message et la même page**. Sépare ce
   qui demande un message ou une page différents.
5. Garde 5 à 8 intentions pour un lancement, classées par proximité avec
   l'offre.

## 3. Le test « une intention, un groupe »

Deux lignes vont dans le même ad group seulement si les trois réponses sont
« oui » :

- même page de destination ?
- les mêmes annonces conviendraient-elles aux deux ?
- une personne qui écrit l'une pourrait-elle écrire l'autre dans la même
  conversation ?

Sinon, deux groupes. Et à l'inverse : deux groupes dont les annonces sont
interchangeables n'en font qu'un.

## 4. Nommer les groupes

- Lettres non accentuées, chiffres, `_` ou `-` : le modèle demande « no
  special characters » sans en donner la liste (`commun/faits.md` § 3).
- Le nom dit l'intention, pas le produit : `batterie_occasion_inquietude`
  plutôt que `groupe3` ou `produit_batterie`.
- Le même nom, à l'identique, dans les onglets `adgroups` et `ads` : le
  script le vérifie.

## 5. Cas limites

| Cas | Conduite |
|---|---|
| Un seul produit, une seule page | découpe par situation ou par objection (prix, fiabilité, mise en route) ; si les annonces restent interchangeables, livre moins de 5 groupes et dis-le |
| B2B à cycle long | les intentions de découverte et de comparaison dominent ; la décision passe souvent par une démonstration : objectif clics ou conversions sur une page dédiée |
| Commerce local | le fichier d'import ne descend pas sous le pays : la ville ou la région se règle dans Ads Manager (identifiants de lieux) ; les hints gardent le besoin |
| Marque peu connue | pas d'intention « marque » : personne ne la cherche encore |
| Intentions trop larges (« s'informer sur l'assurance ») | descends d'un niveau : quel événement déclenche la question ? |
| Intention sensible (santé personnelle ou mentale, détresse, dépendance émotionnelle, mineurs, politique) | ne la cible pas : ces conversations sont exclues de la publicité (`references/politiques.md` § 3) et le ciblage serait inapproprié |
| Intention locale (« près de chez moi ») | décris le besoin sans nom de lieu dans les hints ; la zone se règle dans le ciblage de la campagne |

## 6. Exemple de carte (fictif)

| Persona | Intention envisagée | Étape | Page | Ad group |
|---|---|---|---|---|
| salariée en périphérie | remplacer la voiture pour le trajet domicile-travail | comparaison | /velos-ville/ | `trajet_travail_sans_voiture` |
| acheteur au budget serré | choisir entre un VAE neuf et reconditionné | comparaison | /reconditionne/ | `reconditionne_ou_neuf` |
| acheteur prudent | vérifier l'état de la batterie d'un VAE d'occasion | décision | /batterie/ | `etat_batterie_occasion` |
| parent de deux enfants | emmener les enfants à l'école à vélo | découverte | /cargo/ | `cargo_enfants_ecole` |
| acheteur en ligne non bricoleur | savoir comment le vélo est livré et réglé | décision | /livraison/ | `livraison_velo_monte` |

Le fichier complet est `assets/exemple-campagne.json`.
