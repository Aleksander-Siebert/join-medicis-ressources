# Exemple : une recherche de poste, du profil au suivi

Utilisatrice fictive : Camille D., acquisition chez Assurly
(assurly.example), en poste. Elle vise un poste de Head of Growth dans
l'assurance, à Paris, en hybride ou à distance, discrètement.

## Les recherches ciblées (sorties réelles de job_url.py)

« Paris en hybride, ou à distance » fait deux URL : mélanger les deux perd
soit les offres à distance, soit le filtre de lieu.

```
python3 scripts/job_url.py construire --titres "head of growth" "growth marketing manager" "responsable acquisition" \
  --mots-cles assurance fintech --exclure stagiaire internship alternance --experience confirme \
  --lieu "Paris" --teletravail hybride
REQUÊTE  ("head of growth" OR "growth marketing manager" OR "responsable acquisition") AND (assurance OR fintech) NOT stagiaire NOT internship NOT alternance
URL      https://www.linkedin.com/jobs/search/?keywords=%28%22head%20of%20growth%22%20OR%20%22growth%20marketing%20manager%22%20OR%20%22responsable%20acquisition%22%29%20AND%20%28assurance%20OR%20fintech%29%20NOT%20stagiaire%20NOT%20internship%20NOT%20alternance&location=Paris&f_TPR=r3600&f_WT=3&f_E=4&sortBy=DD

… --lieu "France" --teletravail distanciel
REQUÊTE  ("head of growth" OR "growth marketing manager" OR "responsable acquisition") AND (assurance OR fintech) NOT stagiaire NOT internship NOT alternance
URL      https://www.linkedin.com/jobs/search/?keywords=%28%22head%20of%20growth%22%20OR%20%22growth%20marketing%20manager%22%20OR%20%22responsable%20acquisition%22%29%20AND%20%28assurance%20OR%20fintech%29%20NOT%20stagiaire%20NOT%20internship%20NOT%20alternance&location=France&f_TPR=r3600&f_WT=2&f_E=4&sortBy=DD
```

## Le profil contre 4 offres (sortie réelle)

```
python3 scripts/candidatures.py mots --offres offres-exemple.txt --profil profil-exemple.txt
OFFRES · 4 offres · un terme compte s'il apparaît dans au moins 2 offres
  INTITULÉS : Head of Growth (2), Responsable acquisition (1), Growth Marketing Manager (1)
  ABSENTS DU PROFIL (à ajouter seulement si c'est vrai) :
    ga4 · 3 offres
    growth · 3 offres
    marketing · 3 offres
    attribution · 2 offres
    head · 2 offres
    lifecycle marketing · 2 offres
    sql · 2 offres
  DÉJÀ DANS LE PROFIL : acquisition, acquisition payante, hubspot, retention, seo, assurance, cout, lead, ligne
  DANS LE PROFIL, JAMAIS DANS LES OFFRES : Meta Ads, études clients, prise de parole
  Un terme absent ne s'ajoute que s'il est vrai : jamais une compétence ou un outil que tu n'as pas pratiqué.
```

Ce que le Skill en tire, avec Camille :

- « Head of Growth » est l'intitulé le plus fréquent. Il va dans les
  recherches. Le titre du profil décrit ce qu'elle fait, pas le poste visé :
  « Acquisition et rétention · assurance en ligne · coût par lead divisé par
  2 en 4 mois » (`/linkedin-profile`).
- GA4 apparaît dans 3 offres sur 4 : Camille l'utilise chaque jour, il
  manquait seulement. Ajouté aux compétences et à l'expérience Assurly.
- SQL apparaît dans 2 offres : Camille ne le pratique pas. **Pas ajouté.**
  C'est un écart à assumer en entretien, ou à combler.
- « Attribution » : Camille confirme qu'elle la pilote, ajoutée.
  « Lifecycle marketing » : non, pas ajouté.
- Open to Work : **recruteurs seulement**, elle est en poste (aide LinkedIn
  a507508 : LinkedIn essaie de le masquer aux recruteurs de son employeur,
  sans garantie).

## Le suivi (sortie réelle, au 3 octobre)

```
python3 scripts/candidatures.py etat --journal journal-exemple.md --aujourdhui 2026-10-03
CANDIDATURES · 4 · taux de réponse 50% · 2 envoyee, 1 entretien, 1 refus
  offre : 0 réponse(s) sur 2 (0%)
  réseau : 1 réponse(s) sur 1 (100%)
  spontanée : 1 réponse(s) sur 1 (100%)
  ! relance due : Mutuelle C (Growth Marketing Manager) : envoyée il y a 8 jours. Une relance, avec un élément nouveau (un projet, un résultat, une question sur l'équipe), au recruteur ou à la personne qui a publié l'offre.
  · à classer : Néo-assurance A (Head of Growth) : 23 jours sans réponse. Classer et passer à la suite.
  Sous 10 candidatures par source, les taux sont indicatifs.
```

La relance pour Mutuelle C passe par `/linkedin-dm` (contexte « recruteur »),
avec un élément nouveau : le webinaire de Camille sur les résiliations, en
lien avec la rétention citée dans l'offre.
