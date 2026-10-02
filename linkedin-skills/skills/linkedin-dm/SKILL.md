---
name: linkedin-dm
description: >-
  Écrit les messages privés LinkedIn qui obtiennent une réponse, une personne
  à la fois : raison d'écrire maintenant (sinon le dire), ligne propre à la
  personne vérifiée (« aurait-il pu partir à quelqu'un d'autre ? »), note
  d'invitation sans demande (200 caractères), premier message avec une seule
  petite demande, une relance avec du nouveau. 7 contextes (froid, après
  commentaire, lead de son fil, événement, contact commun, recruteur, reprise
  de contact). Contrôle par script (phrases à supprimer, plafonds, lien
  d'agenda, lot copié à l'identique), garde-fou de volume (invitations en
  attente, taux d'acceptation sous 20% = stop, temps), cadre CNIL et RGPD.
  Utilise-le pour « écris à cette personne », « note d'invitation », « message
  de prospection », « relance ». Pas pour répondre sous ses posts
  (/linkedin-reply), ni trier sa boîte (/linkedin-inbox). N'envoie rien,
  n'automatise rien.
---

# linkedin-dm

Un message privé échoue pour une raison : il aurait pu être envoyé à
n'importe qui. Ce Skill n'écrit pas de message sans une ligne que seule cette
personne pouvait recevoir, et il ne met aucune demande dans une note
d'invitation. La note sert à ouvrir la conversation, pas à obtenir la
connexion : d'après La Growth Machine (plus de 20 millions d'invitations), une
note change à peine l'acceptation (26,42% avec, 26,37% sans), mais double à peu
près le taux de réponse une fois l'invitation acceptée (étude tierce, éditeur
d'un outil de prospection, `commun/preuves.md`).

**À lire avant de commencer :** `commun/regles.md`. Toute demande de
prospection passe par le garde-fou :

```
python3 commun/garde_fou.py --texte "{{la demande de l'utilisateur}}"
```

Envoi automatique, séquence programmée, extraction de profils, message copié
pour 200 personnes : REFUSÉ (règles R1, R2, R5), avec l'alternative manuelle.
Prospection : ENCADRÉ (E1), le cadre CNIL s'applique.

## 1. Avant d'écrire : quatre réponses

Demande-les en une seule question groupée, sauf si `journal.md` ou la
conversation les donnent déjà :

1. **Qui** : prénom, rôle, entreprise.
2. **Pourquoi maintenant** : son post, son commentaire, son intervention, son
   recrutement, une relation commune, un échange dans ton fil. « Elle est dans
   ma cible » n'est pas une raison.
3. **La ligne propre** : ce que l'utilisateur a lu ou vu d'elle, et ce qui lui
   a servi ou ce qu'il conteste. S'il n'a rien lu : « Lis un de ses posts
   d'abord. Si tu ne prends pas 3 minutes pour la lire, ne lui prends pas les
   siennes. »
4. **Ce que veut l'utilisateur**, honnêtement : une conversation, un conseil,
   une vente, un poste, une introduction. Le message ne commence pas par là,
   mais la demande finale en dépend.

**Pas de raison d'écrire maintenant → dis-le** et propose l'ordre qui marche
(section 3) au lieu d'écrire.

Lis `contexte.md` (ton, tutoiement, offres), `reserve.md` (ce que
l'utilisateur peut donner : un chiffre, un modèle, un retour d'expérience) et
`journal.md` (échanges passés avec cette personne).

**Vouvoiement par défaut** avec un inconnu, sauf si `contexte.md` ou le
registre de la personne indiquent le tutoiement.

## 2. Le contexte décide du message

7 contextes, modèles complets (note, premier message, relance) dans
`references/contextes.md` :

| Contexte | La ligne propre vient de | Note d'invitation |
|---|---|---|
| **Froid** | un post, un article, une intervention de la personne | oui, si l'une des notes du mois est disponible |
| **Après commentaire** | l'échange sous son post ou le tien | souvent inutile : le commentaire a fait le travail |
| **Lead de son fil** (`/linkedin-reply`) | son commentaire sous le post de l'utilisateur | oui, elle cite le commentaire |
| **Après un événement** | ce qu'elle a dit, la question posée | oui, dans les 48 heures |
| **Contact commun** | la personne qui recommande (avec son accord) | oui, elle nomme la personne |
| **Recruteur ou salarié** (`/linkedin-job`) | l'offre, une décision de l'équipe | oui |
| **Reprise de contact** | ce qu'on a fait ensemble, ce qu'elle devient | message direct, déjà en relation |

## 3. L'ordre qui marche

D'après alirezarezvani (`outreach_ethics_and_benchmarks.md`, MIT) :

1. **Commenter son travail pendant deux semaines**, sur le fond
   (`/linkedin-comment`, modèles « réchauffer un compte »).
2. **Inviter**, avec une note qui cite ce qu'on a lu ou l'échange.
3. **Après l'acceptation, attendre** un à trois jours. Puis **une petite
   demande**, une seule.
4. **Une relance**, au moins une semaine après, **seulement avec du nouveau**.
   Une deuxième, seulement si quelque chose d'autre a changé. Ensuite, stop.

Cet ordre convertit mieux que n'importe quelle note optimisée **[praticien]** :
on écrit à quelqu'un qui reconnaît déjà le nom.

## 4. Écrire

### La note d'invitation (200 caractères en compte gratuit)

```
{{la ligne propre}} + {{qui tu es, une demi-phrase, si utile}}. Aucune demande.
```

- 200 caractères en compte gratuit, **3 notes personnalisées par mois** (aide
  LinkedIn a563153). En Premium, notes illimitées ; la limite de 300
  caractères vient de sources tierces **[à vérifier]**.
- Avec 3 notes par mois, la note est rare : garde-la pour les invitations qui
  comptent. Les autres partent sans note, et le premier message porte la ligne
  propre. Les données ci-dessus montrent que l'acceptation n'en souffre pas.
- Ni pitch, ni lien, ni « 15 minutes ».

### Le premier message (après acceptation)

- **2 à 4 phrases, 600 caractères au plus.**
- **Reprendre la ligne propre** de la note ou du commentaire.
- **Donner avant de demander** : un chiffre, un modèle, un retour, une
  réponse à sa question. Tiré de `reserve.md`, jamais inventé.
- **Une seule demande, petite**. « Pick your brain » devient **une question
  précise à laquelle on répond en deux phrases**, avec « pas besoin de
  répondre si vous êtes pris ».
- **Pas de lien d'agenda** dans le premier message.
- **Prospection : un moyen simple de dire non** (« Si ce n'est pas le sujet,
  un mot suffit et je n'insiste pas »), et l'utilisateur est identifiable
  (cadre CNIL, section 6).

### La relance

- Au moins **7 jours** après, **une seule**, avec un élément nouveau : un
  résultat, une ressource utile sans contrepartie, une actualité de la
  personne.
- Jamais « Petite relance », « Je reviens vers vous », « Sans nouvelle de
  votre part ».
- Un « non merci » ou une absence de réponse après la relance clôt la
  séquence, définitivement. Noter dans `journal.md` (prochaine étape : aucune).

## 5. Contrôler (scripts) et humaniser

```
python3 scripts/message.py verifier --type note|message|relance --texte "…" \
  [--prospection] [--premium] [--relance-n 1] [--nouveau "…"] [--ligne "…"]
```

| Niveau | Contrôle |
|---|---|
| BLOQUANT | aucune ligne propre à la personne ; note au-delà de 200 caractères ; demande, pitch ou lien dans la note ; lien d'agenda dans un premier message ; relance sans élément nouveau ; 3e relance ; tiret cadratin |
| ATTENTION | 35 phrases qui sentent l'envoi en masse (« Je me permets », « J'espère que vous allez bien », « Je suis tombé sur votre profil », « élargir mon réseau », « Petite relance », « synergie »…) ; demande de temps sans question précise ; plus de 600 caractères ; plusieurs questions ; prospection sans moyen de dire non |

Plusieurs messages pour des personnes différentes :

```
python3 scripts/message.py lot --fichier messages.txt
```

Au-delà de 60% de texte commun (noms retirés), deux messages sont le même
message : c'est un envoi en masse, visé par les Professional Community
Policies. Réécris chacun à partir de sa ligne propre.

Puis `/linkedin-human` en mode intégré.

### Le volume de la semaine

```
python3 scripts/volume.py --invitations {{n}} --en-attente {{n}} --messages {{n}} \
  --minutes {{n}} --journal ~/.claude/linkedin/journal.md [--notes {{n}}]
```

| Seuil | Niveau | Pourquoi |
|---|---|---|
| plus de 40 invitations par jour | REFUSÉ | plan d'automatisation (aide LinkedIn a1341387) |
| plus de 25 par jour | attention | ce n'est plus écrit à la main |
| prévues + en attente au-delà d'environ 100 par semaine | bloquant | limite observée, non publiée par LinkedIn **[praticien]** |
| taux d'acceptation sous 20% | STOP | ciblage à revoir ; seuil de prudence **[praticien]** |
| temps nécessaire (5 min par invitation, 8 par message) au-delà du budget | bloquant | une invitation bâclée coûte plus qu'une invitation pas envoyée |
| plus de 3 notes par mois en compte gratuit | attention | aide LinkedIn a563153 |

Le taux d'acceptation se lit dans `journal.md` (section « Invitations
envoyées », 4 dernières semaines). « Si c'est le nombre qui compte, la
publicité est le bon outil. »

## 6. Le cadre français (prospection B2B)

Détail et sources dans `references/cnil.md`. L'essentiel :

- La prospection de professionnels est possible sans consentement préalable
  si le message est **en rapport avec la profession** de la personne
  (intérêt légitime, CNIL).
- La personne doit pouvoir **s'opposer simplement** : un « non » arrête tout,
  pour toujours.
- **L'expéditeur est identifiable** : le profil de l'utilisateur dit qui il
  est et pour qui il travaille.
- **Copier le contact dans un CRM** oblige à informer la personne, au plus
  tard lors de la première communication (RGPD, article 14), et à noter la
  source et la date. Format prêt à coller : `/linkedin-inbox`.
- Ce Skill n'extrait aucun profil, ne lit pas LinkedIn, n'envoie rien.

## Sortie (format fixe)

```
MESSAGE · {{Prénom}} ({{rôle}}, {{entreprise}}) · contexte {{contexte}} · objectif {{objectif}}
Pourquoi maintenant : {{raison}}
Ligne propre : {{ligne}}

NOTE D'INVITATION ({{n}}/200)
{{note}}  ← ou « sans note : le premier message porte la ligne propre »
(contrôle : OK)

PREMIER MESSAGE, {{1 à 3}} jours après l'acceptation ({{n}} caractères)
{{message}}
(contrôle : OK)

RELANCE, à partir du {{date J+7}}, seulement si {{élément nouveau}}
{{relance}}

Ensuite : stop. Dans journal.md : {{ligne contact proposée}}.
```

Rien n'est envoyé. Sur « ok », une ligne dans `journal.md` (contacts :
date, nom, origine, note, prochaine étape, échéance ; invitations : la
semaine).

## Jamais

- Envoyer, programmer, automatiser, ou écrire « le même message pour ma
  liste » (refusé, règles R1 et R5 du garde-fou).
- Inventer une lecture, un événement commun, une relation, un résultat.
- Écrire à quelqu'un qui a dit non.
- Promettre au nom de l'utilisateur ce qu'il n'a pas validé (un modèle, un
  prix, un rendez-vous).

## Ressources

- `scripts/message.py` : contrôle d'une note, d'un message, d'une relance,
  d'un lot.
- `scripts/volume.py` : le volume de la semaine.
- `references/contextes.md` : les 7 contextes, modèles, phrases à remplacer.
- `references/cnil.md` : le cadre CNIL et RGPD, sources datées.
- `references/exemple.md` : un cas complet, du commentaire à la relance.

## Skills liés

- `/linkedin-comment` : les deux semaines avant l'invitation.
- `/linkedin-reply` : les leads repérés dans son propre fil.
- `/linkedin-inbox` : trier les réponses, reporter les leads dans le CRM.
- `/linkedin-job` : le message au recruteur.
- `/linkedin-human` : passe obligatoire.
