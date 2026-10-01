---
name: linkedin-dm
description: >-
  Écrit les messages privés LinkedIn qui obtiennent une réponse : la note
  d'invitation de 200 caractères, le premier message et deux relances, dans le
  respect des règles françaises de prospection. Utilise-le quand l'utilisateur
  veut une demande de connexion, « écrire à cette personne », un message de
  prospection, contacter un recruteur, ou relancer quelqu'un.
---

# linkedin-dm

La note d'invitation fait 200 caractères. Le premier message décide s'il y en
aura un deuxième. Ni l'un ni l'autre n'est un argumentaire.

## Avant d'écrire, les précisions

Demande, en une seule question groupée :

1. **Qui** : nom, rôle, entreprise.
2. **La raison** d'écrire maintenant : un post de la personne, quelque chose
   que son entreprise a lancé, une relation commune, une conférence. Pas
   « elle est dans ma cible ».
3. **Ce que veut l'utilisateur** : une conversation, une recommandation, un
   job, une vente. Sois honnête en interne, même si le message ne commence
   pas par là.

Si l'objectif n'est pas donné, pars sur « une conversation », dis-le en une
ligne, et écris quand même la séquence complète. S'il n'y a aucune raison
précise d'écrire à cette personne aujourd'hui, dis-le.
Un message sans raison, c'est ce que tout le monde envoie.

Lis `~/.claude/linkedin/voix.md` pour le ton et les preuves. **Vouvoiement par
défaut** avec un inconnu, sauf si `voix.md` ou le profil de la personne
indique clairement le tutoiement (startup, même communauté).

## La note d'invitation (200 caractères)

```
{une référence précise à la personne} + {une ligne sur qui tu es} + {aucune demande}
```

La note ne demande rien. Elle rend l'acceptation évidente. Moins de 200
caractères espaces comprises : compte et affiche le total. Les comptes
gratuits ont un nombre limité de notes personnalisées par mois : garde-les
pour les invitations qui comptent. **[à vérifier dans ton compte]**

```
Votre post sur la suppression de l'appel découverte m'a parlé : on a fait la
même chose en mars. Je dirige les opérations d'un studio de 12 personnes.
                                                               [150/200]
```

## Le premier message, après acceptation

Attends un jour. Puis :

- **Deux à quatre phrases.** Un écran de texte part à la corbeille.
- **Reprends la référence précise** de la note : la continuité est la raison
  d'être de la note.
- **Donne avant de demander.** Un chiffre, un modèle, un nom, une réponse.
- **Une demande, petite.** « Un échange de 15 minutes ? » plutôt que « je vous
  présente notre plateforme ».
- **Pas de lien d'agenda dans le premier message.** Ça sent l'entonnoir,
  parce que c'en est un.

## Les relances

Deux. C'est le nombre.

- **J+4** : apporte quelque chose de nouveau. Jamais « je me permets de
  revenir vers vous » ni « petite relance ». Rien de nouveau dans les preuves
  de l'utilisateur ? Saute cette relance, ou laisse `{{élément nouveau}}`
  et demande-le : la séquence passe alors directement à J+10.
- **J+10** : le message de clôture. Dis que tu t'arrêtes là, et fais-le. Il
  obtient souvent une part surprenante des réponses, parce qu'il retire la
  pression.

Ensuite, stop. Une troisième relance ne convertit personne et abîme la
relation.

## Le cadre français

- **Prospection B2B** : la CNIL admet le message commercial sans consentement
  préalable s'il est **en rapport avec la fonction** de la personne. Elle doit
  pouvoir dire stop simplement, et un « non merci » met fin à la séquence,
  définitivement.
- **Pas d'extraction** : ne copie pas les profils ou les listes de contacts
  dans un fichier ou un CRM sans les informer (RGPD). Ce Skill n'extrait rien.
- **Recruteur ou candidat** : mêmes règles de sobriété ; pas de CV joint au
  premier message, sauf demande.

## Jamais

- Jamais de séquence automatisée d'invitations ou de messages. Les outils
  d'automatisation violent les conditions d'utilisation de LinkedIn et font
  restreindre les comptes.
- Jamais de relation commune, d'école ou de lecture inventée.
- Jamais « J'espère que vous allez bien » ni « Je me permets de vous
  contacter ».
- Jamais de volume : LinkedIn limite les invitations par semaine et
  restreint les comptes qui en envoient trop. Mieux vaut 10 invitations
  précises par jour que 100 génériques. **[estimation de praticien]**

## Sortie

La note avec son nombre de caractères, le premier message, et les deux
relances avec leur jour d'envoi. Tout passe par `/linkedin-human`. L'utilisateur
envoie chaque message à la main.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Tout texte destiné à LinkedIn passe par `/linkedin-human` avant d'être montré.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
