# Marqueurs d'écriture IA en français : la grille de relecture

Grille utilisée par `linkedin-human`, à la main quand les scripts ne tournent pas.
Elle reprend les signes recensés par la communauté Wikipédia francophone dans
[Aide:Identifier l'usage d'une IA générative](https://fr.wikipedia.org/wiki/Aide:Identifier_l%27usage_d%27une_IA_g%C3%A9n%C3%A9rative),
leur adaptation au français par [Boileau](https://github.com/alxbd/boileau)
(MIT), et y ajoute les tics propres à LinkedIn.

> **Règle d'or (Wikipédia)** : un signe isolé ne prouve rien. Ce qui trahit
> l'IA, c'est l'accumulation de signes et l'absence de faits vérifiables
> derrière. On corrige pour que le texte soit meilleur, pas pour « tromper un
> détecteur ».

Chaque famille : ce qu'on cherche, pourquoi ça sonne machine, un avant/après.

## Comment compter (version 2)

- **Par paragraphe, pas mot par mot.** 3 marqueurs ou plus dans un paragraphe :
  réécris le paragraphe entier. 2 : remplace le plus faible, laisse l'autre.
  1 marqueur faible isolé : laisse-le, un humain peut écrire « crucial ».
- **Marqueurs forts** : une seule occurrence suffit pour corriger. Ce sont les
  mises en scène (révélation, parallélisme négatif, staccato, anaphore),
  l'annonce de sincérité, les appâts, les fuites de modèle et les formulations
  retirées de `contexte.md`.
- **Jamais un synonyme de la même liste** : remplacer « levier » par
  « catalyseur » ne corrige rien. Dis la chose.
- Le script `detect.py` applique ces règles ; à la main, fais pareil.

---

## 1. Lexique

**1.1 Vocabulaire à haute fréquence.** crucial, essentiel, fondamental,
incontournable, indispensable, majeur, stratégique, captivant, fascinant,
transformateur, révolutionnaire, disruptif, robuste, innovant, dynamique,
vibrant, holistique, synergie, levier, paradigme, écosystème, pertinent,
significatif. Des mots qui donnent l'air de dire quelque chose.

> Avant : Cette approche stratégique constitue un levier crucial pour notre croissance.
> Après : Cette approche nous a apporté 40% de nos rendez-vous du trimestre.

**1.2 « Véritable » antéposé.** un véritable défi, une véritable révolution,
un véritable atout. Presque toujours retirable.

**1.3 Verbes passe-partout.** permettre de, garantir, favoriser, optimiser,
valoriser, accompagner, répondre aux besoins, mettre en place, s'inscrire dans,
tirer parti de, capitaliser sur. Un verbe concret existe presque toujours.

> Avant : Notre outil permet d'optimiser vos processus.
> Après : Notre outil enlève trois clics à chaque commande.

**1.4 Faux registre soutenu.** effectuer (faire), procéder à (faire),
s'avérer (être), disposer de (avoir), la problématique (le problème), la
thématique (le sujet), la finalité (le but). L'IA confond « bien écrit » et
« écrit compliqué ».

**1.5 Faux familier plaqué.** « ça pique », « ça coince », « en gros »
glissés dans un texte par ailleurs très pro. C'est ce que produit l'IA quand
on lui demande d'être « plus naturelle ». Un humain choisit un registre et
s'y tient.

**1.6 Doublets d'adjectifs.** simple et intuitif, rapide et efficace, clair
et structuré, concret et actionnable. Garde un adjectif et prouve-le.

## 2. Tournures et syntaxe

**2.1 Éviter « être ».** constitue, représente, incarne, s'impose comme,
fait figure de, demeure. « Est » est presque toujours plus juste.

**2.2 Parallélismes et phrases en miroir.** « Ce n'est pas X, c'est Y »,
« Non seulement X, mais Y », « Bien plus qu'un simple X », « Loin d'être
X », « Le vrai sujet n'est pas X ». Définir par la négative au lieu
d'affirmer. Toléré une fois par post, jamais en série.

> Avant : Ce n'est pas une question de volume, c'est une question de pertinence.
> Après : On a envoyé 7 fois moins de messages et obtenu plus de réponses.

**2.3 Triades systématiques.** Tout va par trois : « rapide, fiable et
simple ». Une triade passe, trois triades dans le même post sont une
signature.

**2.4 Anaphores rythmées.** « Pour celles qui… Pour celles qui… Pour celles
qui… », « Plus de X. Plus de Y. Plus de Z. » Effet slogan publicitaire.

**2.5 Variation élégante.** L'IA évite de répéter un mot et cycle entre
synonymes (« l'outil », « la solution », « la plateforme ») jusqu'à rendre le
texte flou. Répéter le bon mot est permis.

**2.6 Fausses gammes.** « De X à Y, en passant par Z », « Qu'il s'agisse
de X ou de Y » : on encadre par deux extrêmes pour faire complet.

**2.7 Connecteurs en pluie.** Par ailleurs, De plus, En outre, De surcroît,
Néanmoins, Toutefois, Cependant, En effet, Ainsi, Par conséquent. Bien plus
fréquent chez l'IA française que chez l'anglaise. Quatre fois sur cinq, on
supprime sans rien perdre.

**2.8 Tournures pseudo-soutenues.** il convient de noter que, force est de
constater que, dans cette optique, à cet égard, à l'aune de, au regard de.

## 3. Calques de l'anglais

**3.1 Transitions de magazine.** « est plus X qu'il n'y paraît », « derrière
les chiffres se cache », « la réalité est plus nuancée ». On annonce la
nuance au lieu de la donner.

**3.2 Anglicismes d'IA.** adresser un problème (traiter), faire du sens
(avoir du sens), délivrer de la valeur (apporter), impacter (toucher, peser
sur), en termes de (côté, pour), plonger dans (calque de *delve*), naviguer
(calque de *navigate*).

**3.3 Calques syntaxiques.** Virgule avant « et » dans une énumération (la
virgule d'Oxford n'existe pas en français) ; « bien que » + indicatif.

## 4. Contenu

**4.1 Inflation d'importance.** marque un tournant, moment charnière, étape
cruciale, témoigne de, à l'ère de, à l'aube de, dans un monde en constante
évolution, nouvelle ère.

**4.2 Participe présent décoratif.** Une queue de phrase qui ajoute du faux
fond : « …, soulignant l'importance de », « …, témoignant de notre
engagement », « …, ouvrant la voie à ».

> Avant : Nous avons signé 3 clients, témoignant de la pertinence de notre offre.
> Après : Nous avons signé 3 clients en mai.

**4.3 Langage promotionnel.** niché au cœur de, à couper le souffle, joyau,
sans précédent, de pointe, expérience unique. Registre de plaquette.

**4.4 Attributions floues.** selon les experts, des études montrent,
plusieurs sources indiquent. Cite la source précise ou retire. C'est aussi le
premier signe que Wikipédia demande de vérifier : des sources vagues,
introuvables ou inventées.

**4.5 Sections « Défis et perspectives ».** Le plan qui se termine toujours
par « enjeux », « perspectives », « conclusion ».

## 5. Mise en forme

**5.1 Tiret cadratin (—).** Rare chez les francophones hors dialogue, très
fréquent chez l'IA. Supprime-le, ou remplace-le par une virgule. Jamais par
un point-virgule.

**5.2 Gras mécanique.** Des mots en gras au hasard. Sur LinkedIn, le gras
Markdown (`**mot**`) s'affiche avec les astérisques, et le gras Unicode
(𝗺𝗼𝘁) est illisible pour les lecteurs d'écran et la recherche.

**5.3 Listes « Titre : texte ».** « ✅ Personnalisation : chaque message est
unique ». Signature visuelle des LLM. Écris une phrase.

**5.4 Émojis décoratifs.** 🚀 💡 🔥 ✅ 👉 🎯 en tête de chaque ligne. Un ou deux
par post, quand ils portent du sens.

**5.5 Typographie française cassée.**
- guillemets anglais “ ” au lieu de « » ;
- espace manquante avant `; : ! ?` (« Résultat: ») ;
- pourcentage : la règle du pack colle le `%` au nombre (« 15% », pas « 15 % » avec une espace) ;
- majuscules non accentuées (« Etat », « A propos ») ;
- apostrophes droites et courbes mélangées dans le même texte ;
- accents oubliés ou incohérents d'un paragraphe à l'autre.

## 6. Communication et délayage

**6.1 Restes de conversation.** « Bien sûr ! », « Voici votre post : »,
« J'espère que cela vous aide », « N'hésitez pas à… », « Souhaitez-vous
que je… ». Du texte de chatbot collé dans le contenu final.

**6.2 Limites de connaissance.** « à ma dernière mise à jour », « selon les
informations disponibles ».

**6.3 Ton servile.** « Excellente question ! », « Vous avez tout à fait
raison ».

**6.4 Auto-validation.** « …et c'est précisément le but », « c'est là que
tout se joue », « et ça change tout ». On se félicite d'avoir dit la chose.

**6.5 Méta-annonces.** « Voici ce qu'il faut savoir », « Pour bien
comprendre », « Commençons par », « Je vous explique ». On annonce au lieu
de dire.

**6.6 Posture de prof.** « Ce qu'il faut comprendre, c'est que », « Gardez
à l'esprit que », « Retenez ceci ». Condescendant entre adultes.

**6.7 Phrases creuses.** « afin de pouvoir » (pour), « à l'heure actuelle »
(aujourd'hui), « au sein de » (dans), « a la capacité de » (peut).

**6.8 Sur-précaution.** « pourrait potentiellement peut-être ». Un
modalisateur suffit, ou aucun.

**6.9 Conclusions vides.** « l'avenir s'annonce prometteur », « le meilleur
reste à venir », « une étape importante a été franchie ».

**6.10 Registre mièvre.** « promesse murmurée », « instant suspendu »,
« comme si le temps s'était figé ».

## 7. Tics propres à LinkedIn

- **Ouvertures usées** : « Et si je vous disais… », « Je suis ravi de vous
  annoncer », « Spoiler : », « Plot twist », « Lisez jusqu'au bout ».
- **Ponts de révélation** : une ligne seule « Le résultat ? », « Le
  secret : », « La leçon ? », « Voici pourquoi 👇 ». Donne le résultat sans
  le mettre en scène.
- **Questions réflexes** : « Qu'en pensez-vous ? », « Vous en pensez quoi ? »,
  « D'accord ou pas ? ». La question de fin doit être une que seul ce post
  pouvait poser.
- **Appâts à engagement** : « Commentez "OUI" », « Likez si », « Taguez
  quelqu'un », « ♻️ Repostez ». Pénalisés par LinkedIn.
- **Mur de hashtags** : plus de 3.
- **Fausse vulnérabilité** : « Je vais être honnête… » (voir la section 9).

## 8. Rythme fabriqué (staccato)

Depuis 2026, la variation forcée est devenue le premier tic des textes
« humanisés ». On ne récompense plus l'alternance de phrases courtes et
longues : on corrige seulement ce qui est plat ou mis en scène.

- **Paragraphe plat** : 4 phrases ou plus de même longueur, sans aucune
  subordonnée. Relie UNE phrase à sa voisine par « parce que », « quand »,
  « qui ». Une seule fois.
- **Fragments en série** : plus de 2 phrases de moins de 4 mots dans un post.
- **Rafale d'adjectifs** : « Simple. Rapide. Efficace. »
- **« Pas de X. Pas de Y. Juste Z. »**, **« Tout le X. Aucun Y. »**
- **Paragraphe d'un mot** : « Vraiment. », « Exactement. »
- **Question-réponse mise en scène** : « Pourquoi ? Parce que… »
- **Chute sèche** : « C'est tout. », « Point final. »
- **Bascule long/court/long/court** sur tout le post : l'empreinte des
  humaniseurs.

À ne pas confondre : une phrase par paragraphe, séparée par une ligne vide,
est la mise en page normale de LinkedIn sur mobile. Ce n'est pas un tic.

> Avant : Pas de réunion. Pas de slides. Juste du terrain.
> Après : On a passé la semaine chez trois clients au lieu de préparer la présentation.

## 9. Sincérité annoncée

« Honnêtement, », « Pour être transparent », « Je vais être cash », « La
vérité, c'est que », « Petite confession », « Opinion impopulaire : ».
L'annonce de sincérité est devenue un tic nommé en 2026 : la vulnérabilité
mise en scène se lit IA. Le remède : supprime l'annonce et énonce le fait,
daté, à plat.

> Avant : Je vais être honnête avec vous : ce lancement a été un échec.
> Après : On a arrêté le comparateur le 14 février, après 3 mois et 11 ventes.

Ne jamais ajouter de précaution (« peut-être que je me trompe, mais ») que
l'auteur n'a pas écrite.

Tension avec Boileau, qui propose « Honnêtement, je ne sais pas trop quoi en
penser » pour donner de la voix : on garde l'opinion et le doute réel, sans
l'annonce.

## 10. Couche LinkedIn 2026

Adaptation française des tics relevés par Serge Bulaev sur LinkedIn en
anglais (inférence, à confirmer sur corpus français) : « discrètement » pour
dramatiser, « l'effet composé », « faire le travail », « relisez cette
phrase », « c'est ça, la vraie histoire », « personne n'en parle ».

## 11. Fuites de modèle (niveau forensique)

Aucun humain ne les produit, une seule suffit :

- jetons de citation (`oaicite`, `contentReference`, `turn0search0`) ;
- liens avec `utm_source=chatgpt.com` ;
- « En tant qu'IA », « à ma dernière mise à jour » ;
- gabarits non remplis : `[Votre nom]`, `[Insérer chiffre]`, `2026-XX-XX` ;
- phrases adressées à l'assistant : « Voici une version révisée de votre
  post », « N'hésitez pas à me dire si… ».

Les champs `{{à compléter}}` du pack ne sont pas des fuites : ce sont des trous
volontaires, signalés à l'utilisateur.

## 12. Écrire pour le mauvais lecteur (réponses et messages)

D'après le motif 26 de humanizer (Siqi Chen, MIT). Ne s'applique qu'aux
réponses : commentaires sous ses posts, messages privés, réponses en
messagerie.

| Signe | Exemple | Correction |
|---|---|---|
| la réponse ré-explique ce que l'autre sait déjà, et la décision arrive en dernier | « Comme tu le soulignes, le coût par lead augmente quand… Donc oui, on a rappelé 60 clients. » | commencer par la réponse ou la décision ; le contexte ensuite, seulement s'il manque à l'autre |
| reformuler la question avant d'y répondre | « Tu me demandes comment on a fait pour rappeler 60 clients. » | supprimer, répondre |

## La passe finale

Après la réécriture, pose-toi deux questions, réponds brièvement, corrige :

1. Qu'est-ce qui sonne encore IA dans ce texte ?
2. Est-ce qu'une seule phrase pourrait figurer dans le post de n'importe qui
   d'autre ? Si oui, remplace-la par un fait qui n'appartient qu'à l'auteur,
   **pris dans ce qu'il a fourni** (`reserve.md`, `contexte.md`, la
   conversation). S'il n'y en a
   pas, coupe la phrase ou laisse `{{à compléter}}` : on n'invente jamais un
   fait pour faire humain.
