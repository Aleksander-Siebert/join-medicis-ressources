# La forme d'un post

## Structure

| Partie | Règle | Pourquoi |
|---|---|---|
| Ligne 1 | l'accroche seule, une phrase complète avant ~140 caractères | le « voir plus » coupe vers 140 caractères sur mobile et 210 sur ordinateur (position observée, non publiée) ; le mobile décide |
| Ligne 2 | paie la ligne 1 : le chiffre, la conséquence, la réponse | une ligne 2 de mise en place perd le lecteur avant le clic |
| Corps | paragraphes de 1 à 3 lignes, une ligne vide entre chacun | lisible sur téléphone ; ce n'est pas un tic d'IA, c'est la mise en page de LinkedIn |
| Bascule | une ligne qui éclaire autrement ce qui précède | ce qui donne au lecteur quelque chose à ajouter |
| Fin | une question que seul ce post peut poser, OU une consigne, OU rien | « Qu'en pensez-vous ? » est un réflexe, pas une question |
| P.-S. | une ligne, s'il existe une vraie suite | lien en premier commentaire, prochain épisode de série |
| Hashtags | 0 à 3, en fin de post | au-delà, course à la portée |

## Longueur

Aucune fourchette imposée. Les sources se contredisent :

| Source | Fourchette conseillée |
|---|---|
| Jake Schincariol, Serge Bulaev | 900 à 1 300 caractères |
| Corey Haines | 1 200 à 1 500 |
| alirezarezvani | 1 300 à 2 500 |
| AuthoredUp (étude tierce, 3 M posts) | plus de 1 000 caractères : portée ×1,18 (corrélation) |

Règle du pack : la longueur que l'utilisateur choisit gagne ; plafond 3 000
(officiel) ; le reçu affiche sa médiane personnelle (`/linkedin-audit`). Si
le post fait plus du double ou moins de la moitié de sa médiane, `lint_post.py
--mediane` le signale, sans le bloquer. Un post court peut être juste ; un post
long doit mériter chaque paragraphe.

## Entrées : chaque type a sa méthode

D'après Marian Kamenistak (MIT), adapté.

| L'utilisateur donne | Méthode |
|---|---|
| un sujet brut (« l'IA en assurance ») | une question groupée : que s'est-il passé, quand, combien ? Sinon `/linkedin-interview` mode post |
| une expérience vécue | trouver la tension (peur, doute, obstacle) ; sans tension, demander la friction |
| un chiffre | ouvrir dessus (formule « chiffre d'abord ») ; demander ce qu'il mesure et quand |
| une opinion | demander qui n'est pas d'accord et ce que ça coûte de la tenir (contre-pied) |
| la transcription d'un échange (appel, séance de coaching) | anonymiser personnes et entreprises ; garder une phrase forte mot pour mot (avec accord) |
| un brouillon | resserrer sans sur-polir ; garder les tics de voix de l'auteur ; `fidelite.py` |
| un événement (salon, conférence) | ce que tu en rapportes de précis, pas « super journée » |
| un remerciement | merci nommé, avec l'accord des personnes |
| une méthode, un processus | « je donne ce que je facture » ou liste ; proposer de nommer la méthode |

## Le premier commentaire

Proposé dans chaque reçu, publié par l'utilisateur juste après son post :

- **le lien** (article, inscription, page d'offre) s'il y en a un : le post
  dit « lien en commentaire » ;
- sinon **un complément utile** : la source d'un chiffre, un exemple de plus,
  la réponse à l'objection la plus probable ;
- jamais une demande de réaction, jamais un faux commentaire pour « lancer le
  fil » (engagement artificiel).

Niveau de preuve : le lien en commentaire plutôt que dans le corps est une
précaution (environ −19% de portée médiane avec un lien dans le corps, étude
tierce contestée ; certaines sources disent que le lien en commentaire serait
aussi pénalisé depuis 2026 [à vérifier]). Si le clic est l'objectif du post,
garder le lien dans le corps est un choix légitime.

## Le visuel

| Cas | Conseil |
|---|---|
| un chiffre clé, une comparaison | une image simple du chiffre (texte alternatif obligatoire) |
| une suite d'étapes | carrousel (`/linkedin-carrousel`) |
| une histoire personnelle | une vraie photo, ou rien ; pas d'image de banque |
| une opinion | souvent rien : le texte suffit |
| une capture d'écran | masquer noms, visages, données ; texte alternatif |

Le reçu dit si un visuel est utile et quoi demander (au graphiste, en début
de semaine). Un post sans visuel n'est pas un défaut.

## Le potentiel de sauvegarde

| Niveau | Quand |
|---|---|
| élevé | méthode en étapes, liste vérifiable, relevé chiffré, modèle à réutiliser, explication d'un terme |
| moyen | une histoire avec une leçon applicable, une comparaison chiffrée |
| faible | une opinion, une célébration, une annonce |

Le dire dans le reçu, avec la raison. Les sauvegardes ne sont pas publiques ;
`/linkedin-audit` les lit dans les statistiques de l'utilisateur.

## Séries numérotées

Un format récurrent reconnaissable (« Histoire de client n°12 », « Le chiffre
du lundi #7 ») crée un rendez-vous. Seulement si l'utilisateur peut tenir le
rythme (`budget.py` de `/linkedin-strategie`) et si chaque épisode tient
seul.

## Méthodes nommées

Quand le post décrit un processus que l'utilisateur répète vraiment, propose
de le nommer : « la méthode des 3 appels », « le test des 5 minutes ». Un nom
se retient, se cite et s'associe à son auteur. Ne pas en inventer un pour
chaque post.

## Typographie et accessibilité

- Pas de Markdown (LinkedIn affiche les `**`).
- Pas de pseudo-gras Unicode : lu comme des symboles par les lecteurs d'écran.
- Pas de tiret cadratin (règle de l'utilisateur) ; « 15% » ; espaces avant
  `: ; ! ?` ; guillemets « ».
- Un émoji en début de ligne de temps en temps, pas sur chaque ligne ; jamais
  en tout début de post.
- Texte alternatif sur chaque image.
