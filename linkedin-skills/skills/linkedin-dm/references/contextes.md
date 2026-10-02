# Les 7 contextes : note, premier message, relance

Exemples fictifs : Camille, acquisition chez Assurly (assurly.example). Chaque
chiffre vient de son `reserve.md`. Ce qui manque reste en `{{à compléter}}`.

Contextes d'après `linkedin-connection-request-hook` (Taplio, MIT, 5
contextes, chiffres d'acceptation non repris car contredits par des données
plus larges) et `outreach_worksheet.md` (alirezarezvani, MIT), complétés par
le recruteur et la reprise de contact.

## 1. Froid (aucun échange)

La ligne propre vient de ce qu'elle a publié. Idéalement, deux semaines de
commentaires d'abord (`/linkedin-comment`) : le contexte devient alors
« après commentaire ».

```
NOTE (153/200)
Votre post sur les clients qui partent avant 6 mois m'a fait revoir nos
chiffres : même courbe chez nous, même cause. Je suis l'acquisition chez Assurly.

PREMIER MESSAGE
Merci d'avoir accepté. Vous écriviez que vos clients partent avant 6 mois :
chez nous, rappeler 60 clients partis a montré que la moitié citait le délai
de remboursement, pas le prix. Vous savez ce que disent vos résiliés ? Pas
besoin de répondre si vous êtes pris.

RELANCE (J+7 au plus tôt, seulement avec du nouveau)
On a publié le script des 60 appels, les 5 questions. Je vous l'envoie s'il
peut servir à votre équipe.
```

## 2. Après un échange en commentaire

Le commentaire a fait le travail : la note est souvent inutile (garde-la pour
un contexte froid). Le premier message reprend le fil.

```
PREMIER MESSAGE
On parlait des résiliations sous votre post de mardi. Vous disiez tester un
appel à J+30 : quel taux de décroché obtenez-vous ? Le nôtre est resté bas
tant qu'on appelait en journée.
```

## 3. Lead de son propre fil (`/linkedin-reply`)

```
NOTE (133/200)
Merci pour votre question sous mon post sur les 60 appels. J'y ai répondu
dans le fil ; le script est en bas de ma réponse si besoin.

PREMIER MESSAGE
Vous parliez du même problème de résiliations chez {{entreprise}}. Si ça vous
sert, je peux vous dire ce qu'on a changé dans les 4 mois qui ont suivi. Si ce
n'est pas le moment, un mot suffit et je n'insiste pas.
```

## 4. Après un événement

Dans les 48 heures, quand le souvenir est frais.

```
NOTE (131/200)
J'étais à la table ronde de {{événement}} jeudi ; votre réponse sur le coût
d'acquisition en assurance m'a fait noter trois choses.
```

## 5. Contact commun

Seulement avec l'accord de la personne qui recommande, et en la nommant.

```
NOTE (142/200)
{{Prénom du contact}} m'a conseillé de vous écrire : vous avez mené la
refonte du parcours de résiliation chez {{entreprise}}, on s'y attaque.
```

## 6. Recruteur ou salarié de l'entreprise visée (`/linkedin-job`)

Pas de CV dans le premier message, sauf demande. La ligne propre porte sur
l'équipe, pas sur le poste.

```
NOTE (147/200)
Votre post sur le passage de l'équipe acquisition au SEO m'a parlé : j'ai
fait ce virage chez Assurly en 2025. Je regarde votre offre de {{poste}}.

PREMIER MESSAGE
Merci d'avoir accepté. Vous écriviez que l'équipe acquisition passe au SEO :
pilote-t-elle aussi les campagnes payantes, ou seulement l'organique ? Ça
change ce que je mettrais en avant dans ma candidature.
```

## 7. Reprise de contact

Déjà en relation, pas de note. Ce qu'on a fait ensemble, puis une raison
d'aujourd'hui.

```
MESSAGE
On avait travaillé ensemble sur {{projet}} en {{année}}. Je vois que tu as
rejoint {{entreprise}} : bravo. Je cherche un avis sur {{question précise}},
tu as 2 minutes pour me dire si je fais fausse route ?
```

## Phrases à remplacer

| À supprimer | À la place |
|---|---|
| « Je me permets de vous contacter » | la ligne propre, directement |
| « J'espère que vous allez bien » | rien |
| « Je suis tombé sur votre profil » | ce que tu lisais quand tu l'as trouvée |
| « Je souhaiterais élargir mon réseau » | pourquoi elle, pourquoi maintenant |
| « Votre parcours est inspirant » | ce qui, dans son travail, t'a servi |
| « Seriez-vous disponible pour un échange de 15 minutes ? » | une question précise, répondable en deux phrases |
| « Pourrais-je vous piquer quelques idées ? » | la question elle-même |
| « Petite relance », « Je reviens vers vous » | l'élément nouveau, ou pas de relance |
| « Nous aidons les entreprises comme la vôtre à… » | ce que tu as appris en le faisant, sans le vendre |
| « N'hésitez pas à me contacter » | rien |

## Pourquoi pas de chiffres d'acceptation ici

Les sources annoncent souvent « 30-40% sans note, 70% avec ». La plus large
étude disponible (La Growth Machine, plus de 20 millions d'invitations) trouve
26,42% avec note et 26,37% sans. Le pack ne promet aucun taux : il mesure
celui de l'utilisateur (`volume.py`, `journal.md`).
