# entreprise.md : exemple rempli

> **Exemple fictif.** Assurly et toutes ses données sont inventés pour montrer
> le format. Ne copie aucun chiffre, aucun nom ni aucun numéro de cet exemple
> dans un vrai fichier.

## État

- rempli : oui
- mis à jour le : 13 octobre 2026
- prochaine relecture : 13 janvier 2027

## Comment lire les étiquettes

| Étiquette | Sens | Ce que font les Skills |
|---|---|---|
| **LIVE** | vrai aujourd'hui, vérifiable | l'utilisent |
| **À CONFIRMER** | déduit, ancien, incertain | l'écrivent `{{à confirmer : …}}` |
| **RETIRÉ** | n'est plus vrai ou n'est plus dit | ne l'utilisent jamais |

Chaque fait porte une étiquette, une date (« au … ») et une source.

---

## 1. Identité

| Fait | Valeur | Étiquette | Au | Source |
|---|---|---|---|---|
| Nom commercial | Assurly | LIVE | 13/10/2026 | page d'accueil |
| Ce que nous faisons, en une phrase | Courtier en assurance santé et prévoyance pour les indépendants et les TPE en France. | LIVE | 13/10/2026 | entretien avec la gérante |
| Site | https://www.assurly.example | LIVE | 13/10/2026 | page d'accueil |
| Raison sociale et forme | Assurly SAS | LIVE | 13/10/2026 | /mentions-legales/ |
| SIREN | XXX XXX XXX (un vrai fichier porte le numéro lu sur les mentions légales) | LIVE | 13/10/2026 | /mentions-legales/, contrôlé par `entreprise.py siren` |
| Siège | Lyon (69) | LIVE | 13/10/2026 | /mentions-legales/ |
| Date de création | 2019 | À CONFIRMER | 13/10/2026 | déduit de « depuis 2019 » sur /a-propos/, à comparer à l'Annuaire des entreprises |
| Taille de l'équipe | 14 personnes, dont 6 courtiers | LIVE | 13/10/2026 | entretien avec la gérante |
| Pays et langues servis | France métropolitaine et DROM, en français | LIVE | 13/10/2026 | /a-propos/ |

## 2. L'offre

| Offre | Ce que c'est | Pour qui | Format et prix | Étiquette | Au | Source |
|---|---|---|---|---|---|---|
| Mutuelle indépendant | 3 formules : Essentielle, Confort, Intégrale | indépendants, freelances, artisans | prix sur devis, selon l'âge et la formule | LIVE | 13/10/2026 | /mutuelle-independant/ |
| Mutuelle entreprise | contrat collectif pour les salariés | TPE de 1 à 20 salariés | prix sur devis | LIVE | 13/10/2026 | /mutuelle-entreprise/ |
| Prévoyance indépendant | indemnités journalières, invalidité, décès | indépendants installés | prix sur devis | LIVE | 13/10/2026 | /prevoyance-independant/ |
| Premier mois offert | réduction de bienvenue | nouveaux clients | | RETIRÉ | 30/06/2026 | offre terminée le 30 juin 2026 |

**Modèle économique :** commission versée par les assureurs partenaires sur
chaque contrat placé ; aucun frais facturé au client (LIVE, au 13/10/2026,
entretien avec la gérante).

## 3. Le marché

| Fait | Valeur | Étiquette | Au | Source |
|---|---|---|---|---|
| Catégorie annoncée (ce que dit le site) | « courtier en assurance » | LIVE | 13/10/2026 | balise title de l'accueil |
| Catégorie réelle (où les clients nous rangent) | « comparateur de mutuelles » | À CONFIRMER | 13/10/2026 | 4 avis Google sur 10 lus emploient « comparateur » ; à confirmer par `/fondation-clients` |
| Catégorie possible (si on la change) | « conseiller santé et prévoyance des indépendants » | À CONFIRMER | 13/10/2026 | proposition de l'entretien, pas encore décidée |
| Clients servis aujourd'hui | B2C (indépendants) et B2B (TPE) ; « 3 200 clients indépendants » | LIVE | 13/10/2026 | /a-propos/, mis à jour en septembre 2026 |

## 4. Les alternatives

Ce que le client ferait si nous n'existions pas. Le **statu quo** (faire sans,
un tableur, un prestataire habituel) est toujours la première ligne.

| Alternative | Type | Ce qu'elle fait bien | Pourquoi des clients nous choisissent quand même | Étiquette | Au | Source |
|---|---|---|---|---|---|---|
| Statu quo : rester sans prévoyance, garder une mutuelle choisie à la va-vite | statu quo | ne coûte rien tout de suite | un arrêt de travail ou une facture d'hospitalisation qui les a fait réagir | LIVE | 13/10/2026 | entretien (3 exemples de clients cités) |
| Comparateurs en ligne | directe | rapides, affichent des prix | pas de conseil sur la prévoyance, appels commerciaux en série | LIVE | 13/10/2026 | entretien ; 3 avis Google qui citent les appels |
| Banque ou assureur du compte pro | secondaire | déjà connu, un seul interlocuteur | une seule gamme proposée | À CONFIRMER | 13/10/2026 | dit en entretien, aucun avis ne le confirme |
| Expert-comptable qui recommande un contrat | indirecte | confiance déjà établie | {{à compléter : pourquoi des clients venus par leur comptable nous choisissent}} | À CONFIRMER | 13/10/2026 | entretien |

Types : statu quo · directe (même solution, même problème) · secondaire
(autre solution, même problème) · indirecte (autre façon de faire).

## 5. La différence

Méthode : des alternatives aux attributs, des attributs à la valeur, de la
valeur aux clients qui s'en soucient le plus (April Dunford). Chaque attribut
a une preuve, sinon il reste `À CONFIRMER`.

| Attribut que les alternatives n'ont pas | Preuve | Valeur pour le client | Étiquette | Au | Source |
|---|---|---|---|---|---|
| Un courtier nommé suit le dossier, du devis au sinistre | fiche client du CRM : un courtier attribué par dossier | une seule personne à appeler en cas d'arrêt de travail | LIVE | 13/10/2026 | CRM Assurly, entretien |
| Mutuelle et prévoyance étudiées ensemble au premier rendez-vous | trame du rendez-vous découverte | évite la confusion entre les deux, l'erreur la plus fréquente relevée en rendez-vous | LIVE | 13/10/2026 | trame interne, relevé des courtiers 2026 |
| « Les meilleurs prix du marché » | aucune | | RETIRÉ | 13/10/2026 | invérifiable, retiré du site |

**Pour qui cette valeur compte le plus :** indépendants installés depuis plus
de 3 ans, qui ont déjà connu un arrêt ou en ont vu un autour d'eux
(À CONFIRMER, au 13/10/2026 : impression de l'équipe, à vérifier avec
`/fondation-clients`).

**Phrase de positionnement** (publique, sans superlatif invérifiable) :

> Pour les indépendants qui ne veulent plus découvrir leurs garanties le jour
> d'un arrêt de travail, Assurly est un courtier santé et prévoyance qui étudie
> les deux ensemble et vous laisse un seul interlocuteur, du devis au sinistre.
> Contrairement aux comparateurs en ligne, un courtier nommé suit votre dossier.

Test : un concurrent pourrait-il signer cette phrase ? Un autre courtier
pourrait signer « un seul interlocuteur ». La preuve (courtier nommé,
mutuelle et prévoyance au même rendez-vous) doit rester dans tout texte qui
reprend la phrase.

## 6. Les objectifs du trimestre

Un objectif se vérifie par un tiers. Un chiffre seulement s'il est fourni.

| Objectif | Indicateur | Point de départ | Cible | Échéance | Étiquette | Au | Source |
|---|---|---|---|---|---|---|---|
| Plus de demandes de devis prévoyance | demandes /devis/ avec « prévoyance » cochée, par mois | 38 en septembre 2026 | 60 | 31/12/2026 | LIVE | 13/10/2026 | CRM Assurly ; cible fixée par la gérante |
| Lancer la page Mutuelle entreprise refondue | page en ligne | brouillon | en ligne | 30/11/2026 | LIVE | 13/10/2026 | entretien |

**Action de conversion principale :** demande de devis (/devis/).

## 7. Ce qui coince

| Fait | Valeur | Étiquette | Au | Source |
|---|---|---|---|---|
| Ce qui a cassé ou ralenti ce trimestre | le délai de réponse aux devis est passé à 3 jours ouvrés pendant l'été | LIVE | 13/10/2026 | entretien |
| La décision repoussée | publier ou non des fourchettes de prix sur le site | LIVE | 13/10/2026 | entretien |
| Ce qui manque le plus | du temps de courtier pour écrire ; aucune donnée sur l'origine des demandes avant juin 2026 | LIVE | 13/10/2026 | entretien |

## 8. Les contraintes

| Fait | Valeur | Étiquette | Au | Source |
|---|---|---|---|---|
| Secteur réglementé (lequel, quels textes) | assurance et intermédiation ; {{à compléter : textes applicables, à demander au service conformité}} | À CONFIRMER | 13/10/2026 | liste de vigilance du pack |
| Ce qu'on n'affirme jamais | qu'un contrat « couvre tout » ; un prix sans devis ; une obligation légale sans texte cité | LIVE | 13/10/2026 | entretien |
| Mentions obligatoires sur nos contenus | numéro ORIAS en pied de page | LIVE | 13/10/2026 | entretien ; pied de page du site |
| Clients : particuliers, professionnels, les deux | les deux (indépendants et TPE) | LIVE | 13/10/2026 | /a-propos/ |
| Prospection par email (oui / non, vers qui) | non : uniquement des clients existants et des demandes entrantes | LIVE | 13/10/2026 | entretien |
| Données clients confiées à une IA (oui / non, lesquelles) | non ; les exports du CRM sont anonymisés avant analyse | LIVE | 13/10/2026 | entretien |

Règles de prospection et de données : voir les sources datées de la CNIL dans
le pack Fondation (`commun/faits.md`). Ce fichier ne remplace pas un avis juridique.

## 9. Les outils

| Catégorie | Outil utilisé | Connecté à l'IA ? |
|---|---|---|
| Site, CMS | WordPress | non |
| CRM | {{à compléter}} | non |
| Emailing | {{à compléter}} | non |
| Analytique | Search Console | export CSV |
| Facturation | sans objet (commissions versées par les assureurs) | non |

## 10. Formulations retirées

Ce que nous disions et ne disons plus. Les Skills ne l'emploient jamais.

| Ancienne formulation | Retirée le | Pourquoi | Remplacée par |
|---|---|---|---|
| « Les meilleurs prix du marché » | 13/10/2026 | invérifiable | « Un courtier compare pour vous les contrats de nos assureurs partenaires. » |
| « Sans engagement » | 01/09/2026 | faux pour certains contrats | « Conditions de résiliation précisées dans votre devis. » |
| « Premier mois offert » | 30/06/2026 | offre terminée | rien |

## 11. Journal des modifications

| Date | Ce qui a changé | Pourquoi |
|---|---|---|
| 13/10/2026 | création du fichier (brouillon depuis le site, puis entretien de 25 minutes) | `/fondation-entreprise` |
