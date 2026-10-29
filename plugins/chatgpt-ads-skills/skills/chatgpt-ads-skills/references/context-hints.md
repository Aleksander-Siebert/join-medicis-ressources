# Context hints : décrire la conversation où l'annonce a sa place

Ce que dit OpenAI (Help Center et documentation développeur, relus le
15 oct. 2026, `commun/faits.md` § 2) :

- un context hint décrit les conversations, thèmes, produits, usages ou
  besoins où l'annonce peut aider, surtout ce que l'annonce et la page ne
  disent pas déjà ; il peut s'agir de descriptions ou de mots-clés ;
- ce n'est **pas un mot-clé en correspondance exacte** et il ne garantit
  pas la diffusion : la plateforme combine les hints avec la conversation,
  la page, le titre et le texte ;
- un hint précis vaut mieux qu'un mot vague (« Shoes » contre
  « Lightweight trail running shoes for rocky terrain ») ;
- la géographie, les plateformes et les audiences se règlent dans le
  ciblage de la campagne, **pas dans les hints** ;
- jusqu'à 2 000 hints par ad group, « inutile de remplir la limite » ;
- facultatif dans le fichier d'import, en tableau JSON.

Le reste de cette page est **pratique de terrain** : des hypothèses
cohérentes avec ces règles, à tester sur les données de l'annonceur.

## 1. Anatomie d'un bon hint

Une situation, en 4 à 8 mots environ : **qui** (ou quel contexte), **quand**
(quel déclencheur), **quel besoin**.

| Faible | Pourquoi | Mieux |
|---|---|---|
| vélo électrique | étiquette de produit, toutes les conversations du sujet | vélo électrique pour un long trajet domicile travail |
| voyage | terme vague, bloqué par le script | préparer un week-end en train avec deux enfants |
| Vélora | marque seule : personne ne la cherche encore, et la conversation n'est pas décrite | (supprimé) |
| meilleur vélo pas cher | mot-clé de recherche, et deux allégations en creux | acheter un vélo électrique avec un budget serré |
| logiciel de facturation | catégorie, pas une situation | facturer ses clients sans tableur quand on se lance |
| vélo cargo, vélo cargo électrique, cargo bike | variantes mineures : un seul signal compté trois fois | choisir un vélo cargo pour transporter deux enfants |

*Exemples fictifs.*

## 2. Combien de hints

| Version | Source | Statut |
|---|---|---|
| 2 à 3 par groupe | conseil reçu en direct de la plateforme par un annonceur, non publié | à confirmer |
| jusqu'à 2 000, « inutile de remplir la limite » | documentation développeur | officiel, ce n'est pas une recommandation de nombre |
| exemples de 1 à 2 hints | documentation développeur | officiel, à titre d'illustration |
| de 1 à 15 | guides tiers | praticien, contradictoire |

**Défaut du pack : 3** (curseur 2 à 5). Au-delà de 3, préviens : chaque hint
en plus élargit les conversations visées ; si l'un d'eux décrit une autre
intention, le groupe se dilue. Le script donne une information à 4 ou 5,
un avertissement au-delà de 5.

## 3. Les interdits

1. **Terme vague** : « logiciel », « shopping », « voyage », « IA »,
   « assurance », « solution »… seul ou en deux mots (le script bloque).
2. **Marque seule ou concurrent seul** : bloqué par le script quand le hint
   ne contient que des noms de marques déclarés dans `annonceur`.
3. **Variante mineure** d'un autre hint du groupe : pluriel, synonyme,
   ordre des mots (le script signale au-delà de 60% de termes communs).
4. **Terme populaire sans rapport** avec l'offre, pour « toucher plus de
   monde » : il attire des conversations où l'annonce n'a pas sa place.
5. **Conversation exclue** : santé mentale et personnelle, dépendance
   émotionnelle, politique, mineurs et les autres contextes sensibles
   (`references/politiques.md` § 3).
6. **Allégation dans le hint** : « meilleur », « pas cher », « gratuit ».
   Le hint décrit le besoin, l'annonce porte la promesse.
7. **Géographie** (« … à Lyon », « en Belgique ») : elle se règle dans le
   ciblage de la campagne, d'après la documentation d'OpenAI ; le script la
   signale. Un besoin local reste possible sans nom de lieu (« trouver un
   réparateur de vélo près de chez soi »).

## 4. Le disqualifiant dans le hint

Pour écarter une situation voisine, écris-le dans le hint lui-même plutôt
que de compter sur un réglage :

- « vélo électrique pour aller travailler, pas pour le sport »
- « mutuelle santé pour un indépendant, pas pour une entreprise »
- « logiciel de facturation pour un artisan seul, sans comptable »

Hypothèse de terrain : rien ne documente comment la plateforme lit une
négation dans un hint. Le disqualifiant précise la situation ; il ne
garantit pas l'exclusion.

Pour exclure vraiment, OpenAI propose des hints d'exclusion
(`exclusion_hints`, par l'API) et des « Negative Phrases » (annonceurs
qualifiés). Ils ne passent pas par le fichier d'import : note-les dans la
checklist pour Ads Manager.

## 5. Chevauchements entre groupes

Deux groupes qui visent la même conversation se font concurrence et
brouillent la lecture des résultats. Le script compare chaque hint à ceux
des autres groupes et signale les paires proches.

Pour corriger : garde le hint dans le groupe dont la page répond le mieux,
et réécris l'autre avec le déclencheur propre à son intention (« … avec un
budget serré » contre « … pour un trajet de 20 km »).

## 6. L'auto-test : 3 prompts simulés par groupe

Pour chaque groupe, écris 3 messages qu'une vraie personne pourrait taper
dans ChatGPT, avec ses mots, ses fautes de précision, son contexte. Puis
vérifie :

1. chaque prompt relève de ce groupe ;
2. aucun prompt ne relève mieux d'un autre groupe ;
3. au moins un hint du groupe décrit la situation de chaque prompt ;
4. l'annonce affichée sous la réponse serait utile à cette personne.

Un prompt qui échoue au point 2 signale un chevauchement ; au point 3, un
hint manquant ; au point 4, un groupe mal relié à l'offre. Les prompts vont
dans `prompts_test` : le script vérifie qu'il y en a 3.

Exemple fictif (`etat_batterie_occasion`) :

- « Comment savoir si la batterie d'un vélo électrique d'occasion est encore bonne ? »
- « Quelle autonomie réelle pour un VAE reconditionné de 3 ans ? »
- « Combien coûte le remplacement d'une batterie de vélo électrique ? »

## 7. Langue

Aucune source publique ne dit si un hint en français couvre une conversation
en anglais. **Défaut du pack** : les hints dans la langue des conversations
visées, un groupe par langue si la campagne en couvre plusieurs
**[à confirmer]**.
