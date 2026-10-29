# L'entité de la marque hors du site

Le site décrit l'entité ; le reste du web la confirme. Un modèle qui lit
« Assurly » sur LinkedIn, une fiche Google, l'annuaire des entreprises et
un comparateur, avec le même nom, la même adresse et la même activité, a
une entité nette. Un nom écrit trois façons fait trois candidats.

## 1. Les profils à aligner

| Profil | Ce qui doit concorder | Qui |
|---|---|---|
| Annuaire des entreprises (annuaire-entreprises.data.gouv.fr), SIRENE | raison sociale, adresse du siège, activité | source officielle : c'est la référence |
| Fiche Google (Business Profile) | nom, adresse, téléphone, catégorie, site | marque ; `/seo-local` du pack SEO |
| LinkedIn (page entreprise) | nom, site, secteur, description d'une phrase | marque |
| Wikidata, Wikipédia | voir §2 | communauté, pas la marque seule |
| Comparateurs, annuaires du secteur, places de marché | nom, offre, prix, lien | demande de correction au site (`/geo-exactitude`, `references/corriger.md`) |
| Avis (Trustpilot, Avis Vérifiés, Google) | nom de l'établissement, lien | marque ; droit des avis : Code de la consommation L111-7-2 |

Garde une **phrase de description** unique (ce que fait la marque, pour
qui) et réutilise-la partout : JSON-LD `description`, LinkedIn, fiche
Google, page « à propos ».

## 2. Wikidata

Wikidata est la base de connaissances libre liée à Wikipédia ; beaucoup de
systèmes s'en servent pour relier les identifiants d'une entité
**[à vérifier : usage par chaque moteur de réponse, non documenté]**.

1. **Chercher** : `entite.py --wikidata`, ou wikidata.org. Le script donne
   des candidats ; l'utilisateur confirme lequel est la marque, s'il y en
   a un.
2. **L'élément existe** : vérifier le libellé français, la description,
   « site officiel » (P856), l'identifiant SIREN (P1616) s'il est
   renseigné, les comptes. Proposer les corrections avec une source.
   Ajouter son URL au `sameAs`.
3. **Il n'existe pas** : Wikidata a des critères d'admissibilité (page
   « Wikidata:Notability ») : une entité décrite par des sources sérieuses
   et publiques **[à vérifier : texte en vigueur]**. Une entreprise sans
   couverture indépendante ne remplit pas ces critères ; créer un élément
   promotionnel expose à sa suppression.
4. **Conflit d'intérêts** : les conditions d'utilisation de Wikimedia
   imposent de déclarer une contribution rémunérée **[à vérifier : article
   en vigueur]** ; sur Wikipédia, on propose les modifications sur la page
   de discussion plutôt que de rédiger soi-même l'article de sa société.

Le Skill ne crée ni ne modifie d'élément : il prépare les informations et
leurs sources.

## 3. Homonymes et confusions

| Cas | Signe | Correction |
|---|---|---|
| Concurrent au nom proche (« Assurly » et « Assurlink ») | les IA mélangent les offres | nom exact partout, `alternateName` limité aux vraies variantes, `/geo-exactitude` avec le concurrent en `--concurrent` |
| Homonyme dans un autre pays ou une autre ville | adresse ou fondateur faux dans les réponses | `address`, `areaServed`, `foundingDate`, SIREN dans le JSON-LD ; page « à propos » explicite |
| Entreprise sans adresse publique (service à domicile) | une adresse inventée dans les réponses | dire la zone servie (`areaServed`) et ne pas publier d'adresse fictive ; l'écrire sur la page « à propos » |
| Ancienne marque, rachat, changement de nom | l'ancien nom revient | `alternateName` avec l'ancien nom, page « à propos » datée (« anciennement X, depuis 2025 ») |
| Nom commun (« Orange ») | réponses hors sujet | toujours le nom avec le métier dans les questions de mesure (`/geo-visibilite`) |

## 4. Ce qu'on ne fait pas

- Ajouter des `sameAs` vers des profils qui ne sont pas ceux de la marque.
- Baliser des avis, une note ou un prix qui ne s'affichent pas.
- Créer des profils, pages ou fiches de complaisance pour « peupler »
  l'entité : `/geo-mentions` explique les lignes rouges.
