# Veille sans Python

À suivre quand Python n'est pas installé, ou quand tu ne peux lancer aucune
commande (claude.ai sans dossier, autre IA). Les étapes 1, 3, 3 bis, 5, 7 et
9 de `AGENT.md` ne changent pas. Celle-ci remplace les étapes 2, 6 et 8.

Ce mode demande seulement la recherche web. Il est moins fiable que les
scripts sur deux points, à dire en bas de chaque veille : « Veille faite
sans les scripts : dates et doublons vérifiés à la main. »

## Ce qui remplace la collecte (étape 2)

1. Lis `sources.json` : concurrents, sujets, flux, pages, période (`jours`).
2. Lis `memoire/historique.md` : la liste des liens déjà envoyés.
3. Pour chaque concurrent et chaque mot-clé suivi, cherche sur le web les
   articles de la période. Ouvre aussi chaque flux et chaque page de
   `sources.json`.
4. Pour chaque résultat, vérifie en ouvrant la page :
   - la date de publication, lue sur la page, est dans la période ;
   - le lien mène à l'article, pas à une page d'accueil ;
   - le lien n'est pas dans `memoire/historique.md` ;
   - ce n'est pas la même info qu'un article déjà retenu (dans ce cas,
     garde l'article le plus complet et cite l'autre comme seconde source).
5. Ne garde que des articles réellement ouverts. Une page qui refuse la
   lecture (mur payant, protection anti-robot) est sautée, jamais devinée.

Pages suivies : note dans `memoire/pages.md`, pour chaque page, la date et
les éléments utiles relevés (prix, noms d'offres). À la visite suivante,
compare avec cette note et ne signale que les différences.

Appels d'offres, offres d'emploi, sujets qui montent : ces parties demandent
les scripts. Dis-le une fois à l'utilisateur s'il les a demandées.

## Ce qui remplace la mise en forme (étape 6)

Écris la veille toi-même, selon le modèle choisi dans `mail.json` :

**`themes`**

```
Objet : {l'info principale}

À retenir
1. …  (3 points au plus)

{Rubrique}
- {Titre de l'info} ({date})
  {2 ou 3 phrases de faits.}
  Pour toi : {pourquoi ça compte.}
  Source : {nom} {lien direct}

À surveiller
- …
```

**`recap`**

```
Objet : {l'info principale}

Les points clés
1. …  (5 points au plus, chacun avec le numéro de sa source)

Les sources
1. {Titre exact} · {média}, {date} : {une ligne}. {lien direct}
```

**`flash`**

```
Objet : {l'info principale}

- …  (5 lignes au plus)

{Titre} ({média}) {lien direct}
```

Avant d'envoyer, relis-toi avec cette liste :

- chaque info a au moins un lien, et tu as ouvert chaque lien ;
- aucun chiffre ni nom qui ne soit dans la page source ;
- pas de tiret cadratin, « 15% » sans espace, guillemets « ».

## Ce qui remplace la mémoire (étape 8)

Seulement si l'envoi a réussi : ajoute à `memoire/historique.md` une ligne
par lien envoyé, avec la date du jour. Crée le fichier s'il n'existe pas,
avec l'en-tête « Liens déjà envoyés ».

## Passer aux scripts plus tard

Dis « installe Python et passe à la version complète » : l'agent suit
`references/installation.md`. La mémoire de `historique.md` n'est pas
reprise par les scripts : la première veille complète peut répéter des
infos des 7 derniers jours.
