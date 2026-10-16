# Option programmatique : des pages en série

Option de `/seo-plan` (ex-`/seo-programmatic`). Adapté de seo-programmatic
(claude-seo, MIT) et des règles anti-spam de Google (contenu à grande échelle,
pages satellites, `commun/preuves.md`).

Des pages à l'échelle ne marchent que si **chaque page** est utile seule.
Changer le nom de la ville dans un même texte, c'est une page satellite :
Google la déclasse, et souvent le reste du site avec.

## 1. Le schéma de requêtes

| Schéma | Requête type | Exemple |
|---|---|---|
| Lieux | [service] + [ville] | « assurance santé expatrié Dubaï » |
| Personas | [produit] pour [public] | « CRM pour agents immobiliers » |
| Comparaisons | [A] vs [B] | « CFE vs assurance premier euro » |
| Alternatives | alternative à [outil] | « alternative à Lemlist » |
| Glossaire | définition de [terme] | « délai de carence définition » |
| Modèles | modèle de [document] | « modèle de lettre de résiliation » |
| Intégrations | [outil A] + [outil B] | « HubSpot Slack intégration » |
| Conversions, calculs | [X] en [Y] | « salaire brut en net » |
| Annuaires, listes | meilleurs [catégorie] | « meilleurs CRM français » |

Vérifie la demande réelle (connecteur ou recherche web) sur un échantillon de
10 requêtes avant de prévoir 500 pages.

## 2. Les données (ce qui rend chaque page unique)

Du plus défendable au plus faible : données propres > issues du produit >
contenu des utilisateurs > données sous licence > données publiques. Pour
chaque page, liste ce qui **change vraiment** d'une page à l'autre (prix
locaux, réglementation du pays, avis, cas, chiffres). S'il ne change que le
nom : pas de page.

**Test du remplacement** : remplace « Dubaï » par « Lisbonne » dans le texte.
S'il reste vrai, la page est une page satellite.

## 3. Le modèle de page

- Blocs fixes (structure, explication générale, CTA) et blocs variables
  (données, FAQ propre à la page, exemples locaux).
- Au moins 60 à 70% de contenu propre à la page sur les sujets sensibles
  (repère de praticiens, pas une règle de Google).
- Title, H1, description, schema générés depuis les données, relus sur un
  échantillon.

## 4. Structure et maillage

- Sous-dossiers (`/destinations/dubai/`), pas de sous-domaine.
- Une page hub par schéma (`/destinations/`) qui lie toutes les pages ;
  chaque page lie le hub et 3 à 5 pages sœurs proches.
- Fil d'Ariane et `BreadcrumbList`.

## 5. Lancement

- Commencer par 20 à 50 pages, mesurer l'indexation et le trafic 4 à 8
  semaines, puis élargir par lots de 50 à 100 (`scripts/priorite.py lot`
  le signale au-delà de 100).
- Sitemap dédié, pages sans demande ni données en `noindex` ou supprimées.
- Avant lancement : échantillon de 10 pages relues, test du remplacement,
  aucune cannibalisation avec les pages existantes (`/seo-maillage`).

## 6. Le contrôle du lot, mesuré

```bash
python3 scripts/priorite.py lot pages.csv --modele "Assurance {metier} à {ville}"
```

Une ligne par page, une colonne par donnée. Le script dit combien de pages
sont « publiables seules » : pas de doublon de titre, pas de champ vide ni
de `{{à compléter}}`, au moins une donnée propre à la page. Si aucune
donnée ne varie d'une page à l'autre en dehors du titre, le verdict est
« À NE PAS PUBLIER » : ce sont des pages interchangeables. On valide le
modèle sur 3 pages relues avant de générer le lot.
