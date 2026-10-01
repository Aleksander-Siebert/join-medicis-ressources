---
name: linkedin-job
description: >-
  Cherche des offres d'emploi LinkedIn taillées pour le profil de l'utilisateur :
  construit des recherches booléennes précises (AND, OR, NOT, "expression
  exacte"), puis réécrit les URL pour n'afficher que les offres publiées dans
  la dernière heure (f_TPR=r3600), triées par date. Utilise-le quand
  l'utilisateur cherche un job, veut « les offres les plus récentes », « être
  dans les premiers à postuler », affiner une recherche LinkedIn Jobs, ou colle
  une URL de recherche LinkedIn à améliorer.
---

# linkedin-job

Sur LinkedIn, une offre reçoit l'essentiel de ses candidatures dans ses
premières heures. Le menu « Date de publication » descend au mieux à 24 heures.
L'URL, elle, accepte une fenêtre d'une heure. Ce Skill fait deux choses : une
requête qui ne ramène que les bonnes offres, et une URL qui ne montre que les
plus fraîches.

## Avant de chercher

Lis `~/.claude/linkedin/voix.md` (section « Qui je suis ») ou le Growth Context
s'il est chargé. S'il manque quelque chose, pose **une seule** question groupée :

1. **Le poste visé**, et les 2-3 intitulés qu'il porte réellement sur le marché.
   En France, un même poste s'affiche en français et en anglais : « Responsable
   acquisition », « Growth Marketing Manager », « Head of Growth ».
2. **Le niveau** : premier emploi, confirmé, senior, direction.
3. **Le lieu** et le rythme : sur site, hybride, à distance.
4. **Ce qui est exclu** : stage, alternance, freelance, un secteur, une entreprise.
5. **Les mots qui doivent apparaître** : un outil (HubSpot), un secteur (SaaS),
   une langue.

Si un CV ou un profil LinkedIn est fourni, déduis-en les intitulés et les
mots-clés, puis montre-les avant de construire la requête.

## Construire la requête booléenne

La recherche d'offres LinkedIn comprend :

| Syntaxe | Effet | Exemple |
|---|---|---|
| `"expression exacte"` | le groupe de mots tel quel | `"head of growth"` |
| `OR` | l'un ou l'autre (synonymes, FR/EN) | `"growth manager" OR "responsable acquisition"` |
| `AND` | les deux (implicite entre deux mots) | `growth AND saas` |
| `NOT` | exclut | `NOT stagiaire NOT internship NOT alternance` |
| `( )` | regroupe | `("growth manager" OR "head of growth") AND b2b` |

Règles qui évitent les recherches vides ou polluées :

- **Opérateurs en MAJUSCULES.** `or` en minuscules est cherché comme un mot.
- **Guillemets droits** `" "`, jamais « » ni “ ”.
- **Pas de `+` ni de `-`** : LinkedIn ne les gère pas, utilise `AND` et `NOT`.
- **Intitulés entre guillemets**, sinon `growth manager` ramène tous les
  « manager » qui parlent de croissance.
- **Toujours la version française et anglaise** de l'intitulé.
- **NOT avec parcimonie** : `NOT junior` exclut aussi les offres « encadrer
  des juniors », et `NOT stage` exclut les startups « early stage », fréquentes
  en SaaS. Préfère `NOT stagiaire NOT internship NOT alternance`.
- **« Paris ou à distance » = deux URL** : une avec `location=Paris`, une avec
  `location=France` et `f_WT=2` (à distance). Mélanger les deux dans une URL
  perd soit les offres à distance, soit le filtre de lieu.

## Les trois recherches à livrer

1. **Large** : tous les intitulés en `OR`, les exclusions, le lieu.
   Sert à mesurer le marché.
2. **Ciblée** : intitulés `AND` 1-2 mots-clés métier (outil, secteur).
   C'est celle qu'on consulte tous les jours.
3. **Dernière heure** : la ciblée avec `f_TPR=r3600` et `sortBy=DD`.
   À ouvrir 2-3 fois par jour, ou à mettre en favori.

## L'URL « dernière heure »

### Avec exécution de code

```bash
# Construire de zéro
python3 job_url.py construire \
  --titres "growth marketing manager" "head of growth" "responsable acquisition" \
  --mots-cles saas b2b --exclure stagiaire internship alternance \
  --lieu "Paris" --teletravail hybride distanciel --experience confirme

# Réécrire une URL copiée depuis LinkedIn
python3 job_url.py reecrire "https://www.linkedin.com/jobs/search/?keywords=growth&f_TPR=r86400"

# Vérifier une requête
python3 job_url.py verifier '("growth" OR "acquisition") NOT stagiaire'
```

La réécriture garde les filtres de l'URL (lieu, télétravail, niveau), retire
les paramètres de pistage (`currentJobId`, `trk`, `refId`…), force
`f_TPR=r3600` et le tri par date.

### Sans exécution de code : à la main

1. Fais ta recherche sur LinkedIn Jobs avec le filtre « Date de publication :
   dernières 24 heures ».
2. Dans l'URL, repère `f_TPR=r86400` (86 400 secondes = 24 h).
3. Remplace par `f_TPR=r3600` (3 600 secondes = 1 h). Si `f_TPR` n'y est pas,
   ajoute `&f_TPR=r3600` à la fin.
4. Remplace `sortBy=R` par `sortBy=DD`, ou ajoute `&sortBy=DD`.
5. Supprime `currentJobId=…` s'il y est.

Donne toujours les URL complètes, prêtes à cliquer, avec la requête en clair
au-dessus.

### Ce qu'il faut dire honnêtement

- `r3600` n'est pas dans le menu de LinkedIn : c'est un paramètre d'URL que
  LinkedIn accepte aujourd'hui. Il peut cesser de marcher sans prévenir.
  **[estimation de praticien]**
- Une fenêtre d'une heure ramène souvent **zéro résultat** sur une niche. C'est
  normal. Propose `r7200` (2 h) ou `r21600` (6 h) si l'utilisateur veut moins
  de pages vides.
- Les offres « Sponsorisées » et republiées peuvent apparaître malgré le
  filtre : la date affichée sur l'offre fait foi.

## Sortie

```
RECHERCHES  ·  Growth Marketing Manager, Paris, hybride ou à distance

LARGE
  ("growth marketing manager" OR "head of growth" OR "responsable acquisition"
   OR "growth manager") NOT stagiaire NOT internship NOT alternance
  https://www.linkedin.com/jobs/search/?keywords=...&location=Paris&f_TPR=r86400&sortBy=DD

CIBLÉE
  (...) AND (saas OR b2b) NOT stagiaire NOT internship NOT alternance
  https://...

DERNIÈRE HEURE  (à ouvrir 2-3 fois par jour)
  même requête, f_TPR=r3600, tri par date
  https://...

À AJUSTER
  - 0 résultat sur 1 h ? passe à r7200.
  - Trop de « Sales » dans les résultats ? ajoute NOT sales.
```

## Après la recherche

- Pour une offre qui plaît : `/linkedin-profile` vérifie que le titre et l'expérience
  récente parlent le langage de l'offre ; `/linkedin-dm` écrit la demande de
  connexion au recruteur ou au futur manager (200 caractères, sans demande).
- Ne postule jamais, ne parcours jamais LinkedIn à la place de l'utilisateur :
  l'automatisation et l'extraction de données violent les conditions
  d'utilisation de LinkedIn. Ce Skill fabrique les liens ; l'utilisateur
  clique.

## Fin de tâche

Si une recherche a bien marché (ou est revenue vide), propose de noter la
requête et le réglage `f_TPR` retenu dans `~/.claude/linkedin/apprentissages.md`,
avec l'accord de l'utilisateur.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Tout texte destiné à LinkedIn passe par `/linkedin-human` avant d'être montré.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
