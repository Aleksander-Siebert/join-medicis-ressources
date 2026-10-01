---
name: li-profile
description: >-
  Note un profil LinkedIn sur 100 (12 critères), puis aide à le réécrire et à
  le peaufiner dans l'ordre des points perdus : titre, section Infos,
  Sélection, et surtout des expériences chiffrées au format « J'ai fait X, en
  Y, et ça a rapporté Z ». Utilise-le quand l'utilisateur veut améliorer son
  profil, son titre, sa section Infos, ses expériences, se préparer à une
  recherche d'emploi ou attirer des clients via son profil.
---

# li-profile

Un profil n'est pas un CV. Un CV répond à « qu'as-tu fait ? ». Un profil
répond à « est-ce que je contacte cette personne ? », et il y répond en
quatre secondes, avec le titre et les deux premières lignes des Infos.

Ce Skill note, puis **aide à réécrire et à peaufiner** : il ne se contente pas
de proposer un texte, il va chercher avec l'utilisateur les chiffres qui
rendent chaque expérience crédible.

## Entrée

Demande à l'utilisateur de coller : titre, section Infos, poste actuel et deux
expériences précédentes, et s'il a une bannière et une section Sélection. Une
capture de l'en-tête suffit pour un premier passage. Ne te connecte jamais à
LinkedIn à sa place.

Lis `~/.claude/linkedin/voix.md` : cible, offre, objectif (clients, job,
recrutement) et section « Preuves utilisables ». L'objectif change tout : un
profil pour trouver un job parle au recruteur, un profil pour vendre parle au
client.

## 1. Noter

Lis `grille.json` : 12 critères, 100 points, avec ce que vaut la note
maximale. Note chaque critère, montre le tableau, donne le total. Sois
honnête : la plupart des profils démarrent entre 30 et 45, et une note
généreuse ne sert à rien.

```
PROFIL  41/100

  titre                3/12   intitulé seul, ni résultat ni cible
  infos (ouverture)    2/10   commence par « Passionné par »
  infos (corps)        3/8    un historique, pas une offre
  sélection            0/6    vide
  bannière             0/5    dégradé par défaut
  poste actuel         4/14   des missions, aucun chiffre
  ...
```

## 2. Aller chercher les chiffres (le cœur du Skill)

Les expériences pèsent 24 points sur 100. Elles se jouent sur un format :

> **J'ai [verbe d'action] [X : quoi, combien], en [Y : délai ou moyens], ce qui a [Z : résultat business].**
>
> « J'ai vendu 340 abonnements annuels en 9 semaines, soit 210 k€ de chiffre d'affaires signé. »
> « J'ai lancé 12 campagnes d'emailing en un trimestre, ce qui a fait passer le taux de réactivation de 4 % à 11 %. »
> « J'ai recruté 8 commerciaux en 4 mois, l'équipe a atteint 120 % de son objectif dès le deuxième trimestre. »

C'est la même logique que la formule « accompli X, mesuré par Y, en faisant
Z » popularisée par les recruteurs de Google, remise dans l'ordre où on lit
un profil : l'action, l'échelle, le résultat.

**Ne jamais inventer.** Si l'utilisateur n'a pas le chiffre, pose les
questions qui le font sortir, une série courte par poste :

- **Volume** : combien de clients, de projets, de campagnes, de personnes, de
  pages, de tickets ?
- **Temps** : en combien de temps ? Par rapport à combien avant ?
- **Argent** : quel chiffre d'affaires, quel budget géré, quelle économie ?
- **Avant / après** : quel indicateur a bougé, de combien ?
- **Classement** : premier de l'équipe ? Dans le top 10 % ?
- **Périmètre** : combien de pays, de marques, de produits ?

Si le chiffre est confidentiel ou approximatif :

- un **ordre de grandeur** honnête (« plus de 200 clients », « ~1 M€ ») ;
- un **pourcentage** à la place d'un montant (« +35 % de panier moyen ») ;
- un **multiplicateur** (« ×3 en un an ») ;
- et si rien n'est mesurable, une **conséquence concrète** (« process repris
  par les 4 autres agences du réseau »).

Laisse `{{chiffre à confirmer}}` plutôt qu'un nombre plausible inventé, et
liste à la fin ce qu'il reste à vérifier.

**Verbes d'action** qui ouvrent bien une réalisation : lancé, signé, vendu,
réduit, doublé, recruté, construit, négocié, automatisé, ouvert (un marché),
redressé, formé, migré. À éviter : « participé à », « contribué à », « en
charge de », « accompagné », « optimisé » (sans chiffre).

## 3. Réécrire, dans l'ordre des points perdus

Ne réécris pas tout d'un coup : l'utilisateur doit coller chaque section
lui-même.

**Titre (220 caractères).** La formule qui marche :
`{ce que tu fais pour qui} | {preuve} | {comment commencer}`. Pas l'intitulé
seul. Pas « J'aide les X à Y » en trois premiers mots, comme un profil sur
deux. Donne trois options. Pour une recherche d'emploi : l'intitulé visé
(celui qu'utilisent les recruteurs dans leurs recherches) + la spécialité +
une preuve.

**Infos, deux premières lignes.** Tout ce qui suit la ligne 2 est caché
derrière « voir plus » sur mobile : ces deux lignes sont toute la section pour
la plupart des lecteurs. Elles disent qui tu aides et ce qui change. Ni
« passionné », ni « orienté résultats », ni biographie à la troisième
personne, ni ouverture par ton nom.

**Infos, corps.** Écrit à un lecteur, à la deuxième personne (le tutoiement
ou vouvoiement de `voix.md`). Structure : son problème, ce que tu fais, une
preuve chiffrée, ce qu'il doit faire ensuite. Moins de 1 400 caractères,
même si la limite est 2 600.

**Poste actuel et expériences.** Une ligne de périmètre, puis 2 à 4
réalisations au format X / Y / Z, une par ligne. Ce qui a plus de dix ans
tient en une ligne.

**Sélection.** Trois éléments : le meilleur post, une preuve, le moyen de
contact. Une Sélection vide, c'est 6 points perdus sur la seule zone du
profil entièrement sous contrôle.

**Bannière.** Une phrase de positionnement et un moyen de contact. Propose le
texte ; `/li-carousel` peut en faire l'image (1584 × 396 px).

**Compétences.** Remonte les trois pour lesquelles l'utilisateur veut être
choisi.

## 4. Peaufiner

Une fois les sections réécrites, une passe de finition :

- chaque phrase passe par `/li-human` (les profils IA se reconnaissent vite :
  « passionné », « dynamique », « orienté solutions ») ;
- les mots-clés du métier visé apparaissent dans le titre, le poste actuel et
  les compétences (c'est ce que les recruteurs tapent : vérifie avec
  `/li-job`) ;
- cohérence : mêmes chiffres partout, mêmes dates que le CV ;
- lecture à voix haute du titre et des deux premières lignes : est-ce qu'on
  sait, en quatre secondes, si on doit écrire à cette personne ?

## Sortie

Le tableau des notes, puis les réécritures en blocs prêts à copier, dans
l'ordre des points perdus, déjà humanisées. Renote à la fin et montre l'écart
honnêtement : si la réécriture atteint 82 et pas 98, dis 82, et dis ce qui
manque (souvent des recommandations, une vraie bannière et une activité
régulière, qu'aucune réécriture ne peut créer).

Rien n'est enregistré sur LinkedIn par ce Skill. L'utilisateur colle chaque
section.

## Fin de tâche

Propose d'ajouter les réalisations chiffrées validées à la section « Mes
expériences » de `voix.md` : `/li-post` et `/li-dm` pourront s'en servir sans
reposer la question.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Tout texte destiné à LinkedIn passe par `/li-human` avant d'être montré.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
