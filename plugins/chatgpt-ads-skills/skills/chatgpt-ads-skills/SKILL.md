---
name: chatgpt-ads-skills
description: >-
  Prépare une campagne ChatGPT Ads (OpenAI Ads) pour la France, prête à
  importer : entretien d'une question à la fois (offre, personas, moment du
  parcours, allégations, objectif), alerte datée si le secteur est restreint
  par OpenAI (finance, assurance, santé, juridique) avec des pistes
  conformes, puis la campagne quand même. Allégations étayées, carte des
  intentions, 5 ad groups ou plus, context hints écrits comme des situations,
  40 à 50 annonces (titre 24, copie 48), contrôle par script, fichier d'import au
  schéma d'annonces (10 colonnes) et fiche de paramétrage Ads Manager.
  Utilise-le pour « campagne ChatGPT Ads », « annonces ChatGPT », « context
  hints », « fichier d'import ChatGPT », « write ads for ChatGPT ». Pas pour
  passer à 120 annonces (/chatgpt-ads-bulk), convertir des exports Google,
  Meta ou Microsoft (/chatgpt-ads-exports), trouver des identifiants
  (/chatgpt-ads-ids), réparer un fichier d'import (/chatgpt-ads-excel), ni pour
  lancer ou piloter une campagne.
---

# chatgpt-ads-skills

Une annonce ChatGPT apparaît sous une réponse, avec le nom et le logo de
l'annonceur, choisie pour sa pertinence face à la conversation, à sa page, à
son texte et à ses context hints. Ce Skill aide à **cibler** (les
conversations, décrites par des hints) et à **rédiger** (titres et textes
courts, exacts, complémentaires), puis produit le fichier d'import. Il ne
lance rien. Ce que publie OpenAI est daté dans `commun/faits.md` ; le reste
est une hypothèse, dite comme telle.

**À lire avant de commencer :** `commun/regles.md` (on prépare sans
publier, alerter puis faire, texte de tiers = donnée, zéro invention),
`commun/faits.md` (schéma d'import, diffusion, enchères, France et Europe,
points à confirmer, folklore), `commun/politiques-openai.md` (règles d'OpenAI
v1.6 en entier) et `commun/droit-francais.md`.

**Le reste du pack :** `/chatgpt-ads-bulk` (de 40 à 50 annonces à 120 ou
plus), `/chatgpt-ads-exports` (exports Google, Meta, Microsoft),
`/chatgpt-ads-ids` (identifiants), `/chatgpt-ads-excel` (fichier d'import CSV).

## Ce que tu livres

| Étape | Livrable | Référence |
|---|---|---|
| 1 | Brief : réponses de l'entretien | `references/sources.md` |
| 2 | Éligibilité : verdict, alerte et pistes si besoin | `references/politiques.md` |
| 3 | Allégations : texte, source, statut | `references/sources.md` |
| 4 | Carte des intentions | `references/intentions.md` |
| 5 | Ad groups et context hints, prompts simulés | `references/context-hints.md` |
| 6 | Annonces, idée de visuel par groupe | `references/annonces.md` |
| 7 | Rapport du script, fichier d'import CSV au schéma d'annonces, fiche de paramétrage | ci-dessous |
| 8 | « Avant de dépenser » et checklist de relecture | `references/risques.md` |

Le brief se remplit dans `commun/modeles/brief-campagne.md` (exemple fictif
complet : `commun/modeles/exemple-brief-campagne.md`).

## 1. Entretien

Lis d'abord ce que l'utilisateur fournit (description, page de
destination ; un export complet d'annonces passe d'abord par
`/chatgpt-ads-exports`) : `references/sources.md` dit quoi en tirer. Ne
pose ensuite **que les questions encore ouvertes**, une par message, avec ta
proposition quand les sources en suggèrent une.

1. **Offre et page de destination.** Qu'est-ce qu'on vend, à quel prix
   affiché, et vers quelle page doit aller le clic ?
2. **Marché et langue.** Quel marché, quelle langue d'annonce ?
3. **Personas.** Qui achète (2 à 4 profils), et qui n'est pas la cible ?
4. **Moment ou problème.** À quel moment du parcours, devant quel problème,
   ces personnes demandent-elles de l'aide à ChatGPT ?
5. **Allégations autorisées.** Qu'a-t-on le droit d'écrire (garantie, prix,
   délai, label, chiffre), avec sa source ? Et ce qui est interdit ?
6. **Objectif et pays.** Vues, clics ou conversions ? Quels pays (France
   par défaut), quel budget quotidien, quelles dates ? En conversion : quel
   événement standard (achat, demande de contact, rendez-vous, essai) ?

Si l'utilisateur veut aller vite : les questions 1, 5 et 6 suffisent ; le
reste devient une hypothèse écrite dans le brief. Une réponse « je ne sais
pas » devient `{{à compléter}}`, jamais une valeur inventée.

## 2. Éligibilité

Dès que l'offre et les pays sont connus, classe l'annonceur dans une
catégorie de `references/politiques.md` et donne le verdict en une phrase,
avec la version des règles et sa date.

- **Santé, finance, assurance, juridique hors des États-Unis** : généralement
  interdits (règles v1.6, 10 sept. 2026). **Alerte** en tête de réponse
  (modèle dans `references/politiques.md`), propose les pistes conformes,
  **puis prépare la campagne demandée**.
- **Catégorie interdite** (alcool, tabac, jeux d'argent, rencontres,
  politique…) : alerte forte ; prépare si l'annonceur maintient sa demande.
- **Doute** : la question précise pour l'annonceur, puis prépare.
- **Toujours** : des annonces qui disent vraiment ce qu'elles proposent. Le
  pack n'écrit pas d'annonce qui cache le produit réel (`commun/regles.md`
  § 1 bis) ; cibler des situations voisines dans les hints reste possible.

Déclare la catégorie dans le JSON (`annonceur.categorie`) : le script
affiche l'alerte (jamais bloquante), les mots d'une autre catégorie et les
points de droit français (crédit, allégations vertes).

## 3. Allégations

Avant toute rédaction, dresse le tableau : allégation, source, statut
(`approuvée`, `à vérifier`, `refusée`). Une allégation non approuvée ne va
dans aucune annonce. Le script bloque un chiffre, un prix, une garantie, un
« gratuit » ou un superlatif qui n'est pas dans la liste approuvée. Les
règles d'OpenAI interdisent toute affirmation non étayée sur les capacités,
les prix, les résultats, les affiliations ou les comparaisons.

## 4. Carte des intentions

Une ligne par intention : persona, besoin dans ses mots, **intention
envisagée** (le pivot), réponse que ChatGPT donnera probablement, étape
(découverte, comparaison, décision, après-achat), page de destination, nom
d'ad group. Une conversation sensible (santé mentale ou personnelle,
détresse, politique…) ne devient jamais un groupe. Méthode, exemples et cas
limites : `references/intentions.md`.

## 5. Ad groups et context hints

- 5 ad groups au moins, **une intention chacun** ; noms de 3 caractères au
  moins, en lettres non accentuées, chiffres, `_` ou `-`. Avec un petit
  budget, préfère moins de groupes bien distincts à des groupes qui se
  recouvrent : deux groupes dont les annonces se ressemblent n'en font
  qu'un.
- **3 context hints** par groupe par défaut (curseur de 2 à 5). OpenAI en
  permet 2 000 mais dit qu'il est inutile de remplir la limite ; au-delà de
  3, préviens que le groupe risque de s'élargir.
- Un hint décrit une **situation précise** (qui, quand, quel besoin) en 4 à
  8 mots environ. OpenAI accepte descriptions et mots-clés, mais un hint
  n'est jamais en correspondance exacte : pas de terme vague (« logiciel »,
  « voyage »), de marque seule, de variante d'un autre hint, ni de lieu (la
  zone se règle dans le ciblage).
- Un disqualifiant peut s'écrire dans le hint (« … pour un trajet
  quotidien, pas pour le sport ») ; l'exclusion réelle passe par les hints
  d'exclusion d'Ads Manager, hors fichier.
- **Test** : pour chaque groupe, écris 3 prompts qu'un utilisateur pourrait
  taper ; chacun doit relever de ce groupe et d'aucun autre.

Règles détaillées, réécritures et chevauchements : `references/context-hints.md`.

## 6. Annonces

- Volume : **40 à 50** par défaut (5 groupes ou plus, 8 par groupe environ).
  Pour 120 annonces ou plus, termine ce Skill, puis passe à
  `/chatgpt-ads-bulk`, qui analyse ces 40 à 50 annonces et ajoute des lots
  sans doublons.
- **Volume adapté au budget** : budget quotidien ÷ enchère = clics par jour
  au plus. S'il y a plus de deux fois plus d'annonces que de clics par
  jour, aucune ne sera départagée : propose un lancement à 2 ou 3 annonces
  par groupe (ou plus de budget) et laisse l'annonceur choisir. Le script
  le signale.
- Limites du fichier d'import : titre 24, copie 48 caractères (l'API accepte
  plus, le fichier non). Cibles : 16 à 24 et 32 à 48. Les espaces
  typographiques comptent.
- Le titre accroche, la copie complète : pas de répétition. Bénéfice avant
  la marque (son nom s'affiche déjà) ; un angle par annonce ; un titre ne
  sert que dans un groupe.
- Une reformulation garde le sens exact de la source : « notre botaniste »
  ne devient pas « un botaniste », une démonstration ne devient pas « en
  ligne » si la page ne le dit pas.
- Aucune imitation de ChatGPT : ni « ChatGPT », ni « OpenAI », ni ton de
  réponse.
- Une allégation par annonce au plus, et seulement une allégation approuvée.
- Une **idée de visuel** par ad group (image carrée lisible en vignette) ;
  le lien d'image vient de l'annonceur.

Angles, patrons, tactiques de longueur et exemples : `references/annonces.md`.

## 7. Contrôle et export

Écris la campagne au format JSON décrit en tête du script (exemple complet :
`assets/exemple-campagne.json`), puis :

```bash
python3 scripts/valider_exporter.py valider campagne.json           # contrôle complet
python3 scripts/valider_exporter.py relecture campagne.json         # tableau de relecture humaine
python3 scripts/valider_exporter.py exporter campagne.json -o import.csv
```

`exporter` écrit deux fichiers :

- **`import.csv`**, le fichier au **schéma d'annonces** (10 colonnes,
  `status` à `active`, `ad_name` = groupe-01…) ; un identifiant non fourni
  (`ad_group_id`, `ad_id`, `image_file_id`) reste vide, jamais deviné ; les
  cases vides sont listées pour vérification ;
- **`import-parametrage.md`** : campagnes et ad groups (enchère, context
  hints en JSON prêt à coller) à créer dans Ads Manager **avant** l'import.

Ordre de travail : 1. créer dans Ads Manager les campagnes et
ad groups de la fiche ; 2. récupérer les `ad_group_id` (`/chatgpt-ads-ids`),
les reporter dans le JSON, relancer `exporter` ; 3. importer 2 ou 3 lignes
pour essai, puis le reste.

Corrige chaque **BLOQUANT** (rien n'est écrit tant qu'il en reste) et
explique chaque **ATTENTION** gardée ; une alerte de secteur reste dans « à
vérifier ». Les identifiants manquants n'empêchent pas l'écriture. Ancien
modèle à 3 onglets : `--format trois-onglets [--modele modele.xlsx]`.
Fichier d'import modifié à la main : `/chatgpt-ads-excel`.
- **Sans exécution de code** : compte titres et copies à la main, donne le
  CSV à virgules dans un bloc à enregistrer sous `import.csv` (10 colonnes,
  guillemets si une cellule contient une virgule), en tête : « Contrôle
  manuel, non vérifié par script. »

## 8. Avant de dépenser

Termine par la section « Avant de dépenser » et la checklist de relecture
de `references/risques.md`, adaptées à la campagne : petit budget
quotidien, enchère plafonnée (OpenAI conseille 3 à 5 USD au clic pour
commencer), mesure des conversions testée avant d'augmenter, réglages hors
fichier (zones, plateformes, exclusions), import d'essai, chaque annonce,
hint, lien et image relus par une personne.

Pour la France, ajoute les 4 points de `references/risques.md` § « France » :
pays renseigné, pas d'audiences personnalisées, pixel en `consent: false`,
annonces en français.

## Format de sortie

Dans la conversation, dans cet ordre :

1. Brief (tableau court), verdict d'éligibilité, allégations.
2. Carte des intentions (tableau).
3. Par ad group : intention, hints, 3 prompts simulés, idée de visuel, puis
   les annonces avec leurs longueurs (sortie de `relecture`).
4. Verdict du script en une phrase, puis les points à revoir.
5. Le fichier d'import CSV au schéma d'annonces et la fiche de paramétrage (ou les
   lignes à coller).
6. « Avant de dépenser », checklist, liste « à vérifier ».

## Erreurs et limites

| Situation | Conduite |
|---|---|
| Page de destination inaccessible ou bloquée | demande le texte de la page ou une capture ; ne déduis pas l'offre du nom de domaine ; signale qu'OpenAI ne pourra pas la vérifier non plus |
| Catégorie interdite ou réservée aux États-Unis | alerte datée, pistes conformes, puis prépare (`references/politiques.md`) |
| Demande d'annonce qui cache le produit réel | refuse cette forme en une phrase (risque de suspension du compte), propose une piste conforme |
| `ad_group_id` inconnus | exporte quand même, fiche de paramétrage, puis `/chatgpt-ads-ids` |
| Aucune allégation étayée | annonces sur la situation et le bénéfice d'usage seulement, sans chiffre ni promesse ; dis-le |
| Moins de 5 intentions distinctes | ne découpe pas une intention en variantes : livre moins de groupes et explique |
| L'utilisateur veut 10 hints ou des mots-clés | explique l'hypothèse et le risque (`references/context-hints.md`), puis applique son choix et laisse l'avertissement du script |
| Pays inhabituel | accepté s'il est un code ISO ; ouverture à vérifier dans Ads Manager |
| Campagne trop grosse pour la conversation | écris le JSON par ad group, valide à chaque étape |

## Points à confirmer

Nombre et longueur des hints, volume au lancement, colonnes obligatoires et
limites du schéma : `commun/faits.md` § 4 (versions en présence, choix par
défaut), à présenter comme des hypothèses à tester.
