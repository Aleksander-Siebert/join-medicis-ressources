# Publier le dépôt modèle `agent-veille`

Le bouton « Use this template » de GitHub ne fonctionne que sur un dépôt
entier. Le dossier `plugins/agent-veille/` de ce dépôt est prêt à devenir ce
dépôt. Compte 5 minutes. Rien n'est publié tant que tu ne l'as pas fait.

## 1. Créer le dépôt

Sur github.com → « New repository » :

- Owner : ton compte ou l'organisation Join Médicis.
- Nom : `agent-veille`.
- Description : `Agent IA de veille concurrentielle et stratégique, gratuit et open-source. Concurrents, tendances, réglementation, appels d'offres. Pour Claude, sur Mac, PC ou dans le cloud.`
- Public. Ne coche ni README, ni .gitignore, ni licence : le dossier les a déjà.

## 2. Y pousser le dossier

Depuis une copie de `join-medicis-ressources` à jour, une fois la PR fusionnée :

```bash
git subtree split --prefix=plugins/agent-veille -b modele-agent-veille
git push https://github.com/TON-COMPTE/agent-veille.git modele-agent-veille:main
git branch -D modele-agent-veille
```

Les mêmes commandes servent à chaque mise à jour : le dossier de ce dépôt
reste la source, le dépôt modèle en est la copie.

## 3. En faire un modèle

Dans le nouveau dépôt → « Settings » → « General » :

- coche « Template repository » ;
- dans « Features », garde « Issues » pour recevoir les retours.

Sur la page d'accueil du dépôt, roue dentée à côté de « About » :

- Website : l'adresse de la fiche de l'agent sur joinmedicis.com ;
- Topics : `veille-concurrentielle`, `competitive-intelligence`, `ai-agent`,
  `claude`, `claude-code`, `veille`, `marketing`, `open-source`, `french`.

## 4. Vérifier

- L'onglet « Actions » montre le workflow « Tests » au vert sur Linux,
  macOS et Windows.
- Le bouton vert « Use this template » apparaît en haut à droite.
- Essaie-le : crée `ma-veille` en privé, puis suis
  `references/installation.md`, partie 1.

## 5. Pour ressortir dans Google

Ce qui compte, dans l'ordre :

1. Le nom du dépôt, sa description et ses topics (faits ci-dessus).
2. Le titre et les premières lignes du README, qui reprennent « agent IA de
   veille concurrentielle », « gratuit » et « open-source » (déjà écrits).
3. Une page sur joinmedicis.com qui pointe vers le dépôt : la fiche de
   l'agent, et un article « Créer son agent de veille concurrentielle avec
   Claude » qui reprend l'atelier.
4. Des liens entrants : ton post LinkedIn de l'atelier, les annuaires de
   Skills et d'agents (liste à établir ensemble).

Aucune promesse de classement : c'est une recherche peu disputée en
français aujourd'hui, mais la position se constate, elle ne se décrète pas.

## Ce qui reste à faire après la publication

- Remplacer, dans la fiche d'atelier (artifact « Ton agent de veille en
  15 minutes »), les 4 fichiers par le lien du dépôt modèle.
- Mettre le lien du dépôt dans la fiche « L'Espion » ou « Le Guetteur » du
  site et activer son bouton de téléchargement.
