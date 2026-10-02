# Ce qu'on sait vraiment de LinkedIn (niveaux de preuve)

Fichier commun à tous les Skills du pack. Vérifié le **2 octobre 2026**.
Avant de citer un chiffre sur LinkedIn, cherche-le ici et cite-le avec son
niveau. S'il n'y est pas, il porte **[à vérifier]**.

Pourquoi ce fichier existe : presque tous les chiffres qui circulent sur
LinkedIn viennent d'outils qui vendent du LinkedIn (planificateurs,
automatisation, agences). LinkedIn ne publie presque rien sur son classement.
Un Skill qui répète ces chiffres comme des règles transmet du folklore.

## Les quatre niveaux

| Niveau | Ce que c'est | Comment le citer |
|---|---|---|
| **officiel** | page d'aide, conditions, règles ou publication d'ingénieurs LinkedIn | comme un fait, avec la source |
| **étude tierce** | grand échantillon de posts publics, méthode non auditée | « une étude de {qui} sur {N} posts ({année}) observe… » |
| **praticien** | avis ou observation d'un créateur, d'une agence ou d'un vendeur, sans données publiées | « avis de praticien », jamais comme une règle |
| **folklore** | répété partout, sourcé nulle part, ou démenti | seulement pour le reconnaître et le nommer |

Règle pratique : une affirmation avec un pourcentage précis et aucune étude
nommée est du folklore. Donne alors le conseil qui tient **que le chiffre
soit vrai ou non**.

Mention « vendeur » : l'étude vient d'une entreprise qui vend un outil lié à la
conclusion. Ce n'est pas une raison de l'écarter, c'est une raison de le dire.

---

## Limites et formats (officiel)

| Fait | Valeur | Source (consultée le 2 oct. 2026) |
|---|---|---|
| Longueur maximale d'un post | 3 000 caractères | Aide LinkedIn a528176 |
| Note d'invitation, compte gratuit | 200 caractères, **3 notes personnalisées par mois** | Aide LinkedIn a563153 « Personalize invitations to connect » |
| Note d'invitation, Premium | notes personnalisées illimitées ; 300 caractères selon des sources tierces **[à vérifier]** | Aide LinkedIn a563153 (nombre), longueur non indiquée |
| Photo de profil | de 400 × 400 à 7 680 × 4 320 px, PNG ou JPG, 8 Mo maximum | Aide LinkedIn a549049 |
| Bannière (photo d'arrière-plan) | 1 584 × 396 px recommandés, 8 Mo maximum | Aide LinkedIn a549049 |
| Document (carrousel PDF) | PDF, PPT, PPTX, DOC, DOCX ; 100 Mo et 300 pages maximum | Aide LinkedIn a523054 |
| Newsletter | évaluation possible au-delà de **150 abonnés ou relations**, avec du contenu original récent et un historique conforme aux règles | Aide LinkedIn a591266 |
| Titre du profil | 220 caractères | consensus de sources tierces, compteur de l'éditeur **[à vérifier]** |
| Section Infos | 2 600 caractères | consensus de sources tierces **[à vérifier]** |
| Nombre de Skills (compétences) | 50 | consensus de sources tierces **[à vérifier]** |

Ce que LinkedIn **ne publie pas** : la limite hebdomadaire d'invitations, la
position exacte du « … voir plus » selon l'appareil, le poids de chaque
signal dans le classement, tous les critères de la newsletter.

## Règles (officiel)

Citées mot pour mot, vérifiées le 2 octobre 2026.

- **Professional Community Policies** (linkedin.com/legal/professional-community-policies) :
  - « Don't do things to artificially increase engagement with your content. »
  - « Respond authentically to others' content and don't agree with others ahead
    of time to like or re-share each other's content. » → les pods et les
    échanges de likes sont visés.
  - « We don't allow untargeted, irrelevant, obviously unwanted, unauthorized,
    inappropriate commercial or promotional, or gratuitously repetitive
    messages or similar content. » → messages en masse.
  - « Do not share content that is false, misleading, or intended to deceive. »
    → preuves, chiffres et témoignages inventés.
- **Logiciels interdits** (Aide a1341387) : « We don't permit the use of any
  third party software, including "crawlers", bots, browser plug-ins, or
  browser extensions that scrape, modify the appearance of, or automate
  activity on LinkedIn's website. » Conséquence annoncée : compte restreint ou
  fermé.
- **Conditions d'utilisation, §8.2 « À ne pas faire »** : pas de robots ni de
  méthodes automatisées pour ajouter des contacts, envoyer des messages,
  créer, commenter, aimer ou partager des posts ; pas d'extraction de profils ;
  pas de fausse identité ; pas d'informations inexactes.
- Le chemin autorisé : le planificateur de posts intégré à LinkedIn et les
  partenaires officiels de son API marketing.

Conséquences pour le pack : pas de publication automatique, pas de lecture de
LinkedIn par un robot ou un navigateur piloté, pas de pods, pas de
« commente X pour recevoir Y », pas de message copié à l'identique.

## Comment le fil classe les posts

| Affirmation | Niveau | Source |
|---|---|---|
| Le classement optimise **plusieurs objectifs à la fois** ; aucun signal n'est « le » signal | officiel | Borisyuk et al., « LiRank: Industrial Large Scale Ranking Models at LinkedIn », arXiv 2402.06859 (KDD 2024) |
| Le temps de lecture (dwell time) est un objectif explicite, mesuré par rapport à un seuil qui dépend du contexte | officiel | LinkedIn Engineering Blog, « Understanding feed dwell time to improve LinkedIn feed ranking » |
| « Rallonger un post pour gagner du temps de lecture » | folklore | construit sur le fait précédent, qui ne le soutient pas : le seuil est relatif et le remplissage dégrade les autres objectifs |
| 360Brew, modèle de LinkedIn qui « lirait » les posts | prudence | arXiv 2501.16450, **retiré par ses auteurs en août 2025**. Les conseils « optimisés pour 360Brew » s'appuient sur un article retiré |
| Un commentaire de fond pèse plus qu'une réaction | étude tierce (mécanisme cohérent avec l'officiel) | études de posts publics ; un commentaire crée une notification et un fil |
| Portée moyenne d'un post : environ 8 à 12% des abonnés, en baisse d'année en année | étude tierce | van der Blom, *Algorithm Insights* (Just Connecting), éditions récentes. La tendance est fiable, le pourcentage indicatif |
| Les premières 60 à 90 minutes sont corrélées à la portée finale | étude tierce | corrélation, causalité non prouvée |
| « Golden hour » avec une coupure précise | folklore | personne hors de LinkedIn ne connaît la courbe |
| Modifier un post dans les X premières heures « réinitialise » sa diffusion | praticien | aucune donnée publiée **[à vérifier]** |

## Liens, hashtags, formats

| Affirmation | Niveau | Source |
|---|---|---|
| Un lien externe dans le corps du post réduit la portée médiane d'environ **19%** (18,8%) | étude tierce, **contestée** | van der Blom, *Algorithm Insights 2026*, environ 1,3 M posts. LinkedIn n'a jamais confirmé de pénalité ; explication non punitive possible (le lien fait quitter le fil, donc moins de temps de lecture) |
| « −40 à −60% avec un lien » | praticien | chiffres d'outils et de blogs sans méthode publiée |
| Le lien en premier commentaire serait aussi pénalisé depuis début 2026 | praticien **[à vérifier]** | articles secondaires, pas d'étude primaire trouvée |
| Hashtags : 0 à 3 en fin de post ; au-delà, signal de « course à la portée » pour les lecteurs | praticien | LinkedIn a retiré peu à peu le suivi des hashtags ; aucune donnée officielle sur leur effet |
| Longueur « idéale » 900-1 300, 1 200-1 500 ou 1 300-2 500 caractères | praticien | chaque source donne une fourchette différente → **aucune fourchette n'est imposée par le pack** ; la médiane personnelle vient de `/linkedin-audit` |
| Le « … voir plus » coupe vers 140 caractères sur mobile et 210 sur ordinateur | praticien (observation) | position non publiée, varie selon l'appareil et les retours à la ligne |
| La section Infos se replie après environ 200 à 265 caractères | praticien (observation) | variable ; écrire pour le plus court |
| Le carrousel PDF obtient plus de portée que l'image seule | étude tierce (vendeurs) | AuthoredUp, MagicPost et autres ; multiplicateurs variables d'une étude à l'autre |
| Ouvrir sur une question fait baisser les likes d'environ 34% | étude tierce (vendeur) | MagicPost, cité par Serge Bulaev ; à tester sur son propre compte |
| Pseudo-gras Unicode (𝗴𝗿𝗮𝘀) : illisible pour les lecteurs d'écran, non trouvé par la recherche | officiel côté accessibilité | les caractères « Mathematical Alphanumeric Symbols » sont lus comme des symboles par les lecteurs d'écran (norme Unicode, bloc U+1D400) |

## Invitations et messages

| Affirmation | Niveau | Source |
|---|---|---|
| Une note personnalisée **ne change presque pas** le taux d'acceptation (26,42% avec, 26,37% sans) | étude tierce (vendeur) | La Growth Machine, plus de 20 M invitations. Vendeur d'un outil de prospection |
| Une fois l'invitation acceptée, la note augmente nettement le taux de réponse (environ ×2) | étude tierce (vendeur) | même source ; d'où la règle du pack : **la note sert à ouvrir la conversation, pas à obtenir la connexion** |
| « Une note triple l'acceptation » | folklore | démenti par la source précédente |
| Limite d'environ 100 invitations par semaine, invitations en attente comprises | praticien (observation) | non publiée par LinkedIn, ajustée par compte |
| Une invitation retirée ne peut pas être renvoyée à la même personne pendant environ 3 semaines | praticien (observation) | **[à vérifier]** |
| Taux d'acceptation durablement sous 20% : signe de ciblage raté, risque de restriction | praticien | seuil de prudence repris d'alirezarezvani ; LinkedIn ne publie pas ses seuils |

## Prospection et données personnelles (France)

| Affirmation | Niveau | Source |
|---|---|---|
| Prospection de professionnels : possible sur la base de l'intérêt légitime si le message est **en rapport avec la profession** de la personne ; elle doit être **informée** et pouvoir **s'opposer simplement et gratuitement** ; l'expéditeur est identifié | officiel | CNIL, « La prospection commerciale par courrier électronique » et « La prospection commerciale » (cnil.fr), consultées le 2 oct. 2026 |
| Un message privé LinkedIn relève des mêmes règles que le courrier électronique | **[à vérifier]** | interprétation prudente retenue par le pack ; pas de position CNIL trouvée sur la messagerie LinkedIn en particulier |
| Copier des contacts LinkedIn dans un CRM oblige à informer la personne (article 14 du RGPD) et à noter la source, la date et la base légale | officiel (RGPD) | Règlement (UE) 2016/679, art. 14 ; CNIL |
| Extraire des profils avec un outil | interdit (LinkedIn) et risqué (RGPD) | Aide a1341387 ; CNIL |

## Profil

| Affirmation | Niveau | Source |
|---|---|---|
| Les 60 premiers caractères du titre sont ceux qu'on voit dans les invitations, commentaires et résultats de recherche | praticien (observation) | alirezarezvani ; d'autres sources disent 45 ; écrire pour le plus court |
| « Un profil complet reçoit X fois plus de vues » | praticien (vendeur) | chiffres de vendeurs non vérifiables, **non repris** |
| « Open to work » ou « Services » rend visible dans les recherches correspondantes | officiel (fonction) | fonctions décrites dans l'aide LinkedIn ; l'effet chiffré n'est pas publié |

## Ce que le pack fait de ces niveaux

- Une règle du pack s'appuie sur de l'officiel, ou sur une précaution qui
  tient même si l'étude tierce est fausse (exemple : le lien en premier
  commentaire ne coûte rien et peut aider).
- Un chiffre de praticien n'est jamais présenté comme une règle. Il devient une
  **hypothèse à tester** avec `/linkedin-audit` (plan d'expérience).
- Les données de l'utilisateur (`apprentissages.md`) passent avant toutes ces
  sources pour son propre compte, à condition d'avoir assez de posts (10 au
  moins, voir `/linkedin-audit`).

Mise à jour : quand un fait change, corrige la ligne, mets la nouvelle date et
garde l'ancienne valeur dans le CHANGELOG du pack.
