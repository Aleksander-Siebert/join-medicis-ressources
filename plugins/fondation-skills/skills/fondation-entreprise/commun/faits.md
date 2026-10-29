# Faits : ce qu'on sait, et d'où ça vient

Chaque affirmation du pack sur le droit, les registres publics ou les
méthodes a un **niveau de preuve** et une **date de vérification**. Un fait
absent de ce fichier porte **[à vérifier]**. On le revérifie quand la date a
plus de 6 mois.

| Niveau | Ce que c'est | Comment l'écrire |
|---|---|---|
| **Officiel** | texte de loi, autorité (CNIL, INSEE, DGCCRF), registre public | affirmé, avec la source |
| **Méthode** | méthode publiée par un auteur reconnu (positionnement, entretien) | présentée comme une méthode, pas comme une loi |
| **Praticien** | constat répété de professionnels, sans preuve publique | proposé comme repère |
| **Folklore** | répété partout, sans source ou contredit | reconnu et écarté |

## 1. Données publiques de l'entreprise (France)

| Fait | Source | Niveau | Vérifié le |
|---|---|---|---|
| Le SIREN compte 9 chiffres ; le SIRET, 14 (SIREN + NIC de 5 chiffres). Leur chiffre de contrôle suit l'algorithme de Luhn. Exception : les établissements de La Poste (SIREN 356 000 000, sauf le siège 356 000 000 00048), dont la somme des chiffres du SIRET doit être un multiple de 5. Une clé correcte ne prouve pas que le numéro est attribué. | bibliothèque python-stdnum 2.2 (`stdnum/fr/siret.py`), synthèses concordantes ; **[à vérifier : page INSEE de référence]** | praticien | 13 oct. 2026 |
| Le numéro de TVA intracommunautaire français s'écrit FR + clé de 2 chiffres + SIREN ; clé = (12 + 3 × (SIREN modulo 97)) modulo 97. Un numéro bien formé ne prouve pas qu'il est valide : seul le service européen VIES le confirme. | synthèses concordantes (Eurofiscalis, La Fabrique du Net) ; même calcul dans python-stdnum 2.2 (`stdnum/fr/tva.py`) ; VIES pour la validité | praticien | 13 oct. 2026 |
| Le site sirene.fr a fermé le 2 décembre 2025. La recherche d'entreprises passe par l'Annuaire des entreprises (annuaire-entreprises.data.gouv.fr), plateforme publique pilotée par la DINUM ; l'avis de situation reste sur avis-situation-sirene.insee.fr ; la base complète se télécharge sur data.gouv.fr. | INSEE, « Fermeture du site Sirene » (insee.fr/fr/information/8672439, mise à jour du 28 nov. 2025) | officiel | 13 oct. 2026 |
| La page d'une entreprise sur l'Annuaire suit l'adresse `annuaire-entreprises.data.gouv.fr/entreprise/` + SIREN ; elle affiche forme, siège, date de création, TVA, code NAF. Les dirigeants et le capital viennent du RNE (INPI). | exemple d'adresse vu sur un site tiers **[à vérifier : schéma d'adresse et périmètre RNE]** | praticien | 13 oct. 2026 |

## 2. Prospection et données personnelles

| Fait | Source | Vérifié le |
|---|---|---|
| Email, SMS : prospection vers des **particuliers** sur consentement préalable (libre, spécifique, éclairé, univoque ; l'acceptation de conditions générales ne suffit pas ; case pré-cochée interdite). Exception : client existant, produits ou services analogues de la même entreprise. | CNIL, « La prospection commerciale par courrier électronique » (page du 10 juin 2026) | 13 oct. 2026 |
| Vers des **professionnels** : intérêt légitime possible si le message est en rapport avec la profession de la personne ; information et droit d'opposition simple et gratuit. Les adresses génériques de personnes morales (contact@, info@) ne sont pas soumises à ces principes. | même source | 13 oct. 2026 |
| Chaque message permet d'identifier l'émetteur et de refuser simplement les envois suivants ; réponse aux demandes d'exercice des droits sous un mois. | même source | 13 oct. 2026 |

Le pack **ne donne pas de conseil juridique** : il pose trois questions
(B2B ou B2C, prospection par email, données clients confiées à une IA) et
renvoie à ces sources datées.

## 3. Secteurs réglementés (liste de vigilance)

Santé, pharmacie et dispositifs médicaux ; banque, crédit, placement ;
assurance et intermédiation ; juridique ; alcool ; jeux d'argent ; tabac et
vapotage ; produits pour enfants ; allégations environnementales.
**[à vérifier]** : chaque secteur a ses textes (Code de la santé publique,
Code monétaire et financier, Code des assurances, loi Évin, Code de la
consommation…). Le pack les **signale**, il ne les résume pas : l'utilisateur
vérifie avec son service juridique ou son organisme de tutelle.

## 4. Méthodes reprises

| Méthode | Auteur | Ce qu'on en garde |
|---|---|---|
| Positionnement en 5 éléments : alternatives, attributs uniques, valeur, clients qui s'en soucient le plus, catégorie | April Dunford, *Obviously Awesome* (2019) | l'ordre (on part des alternatives réelles, pas de la catégorie) |
| Jobs à accomplir, forces du changement (pousser, attirer, habitude, anxiété) | Clayton Christensen ; Bob Moesta, entretien « switch » | pour `/fondation-clients` |
| Fait lu contre déduction ; pas de recommandation de fournisseur | Anthropic, plugin small-business (`smb-onboard`, Apache 2.0) | principes, réécrits |

## 5. Folklore (à reconnaître et écarter)

- Un score de complétude qui compte des mots-clés : il donne 100/100 à un
  modèle vide (validateur de `marketing-context`, testé le 13 oct. 2026).
- Des personas avec prénom, âge et citation inventés.
- « Nous n'avons pas de concurrent » : il y a toujours le statu quo.
- Des chiffres d'exemple (« LTV:CAC 5:1 ») recopiés comme s'ils étaient ceux
  de l'entreprise.
