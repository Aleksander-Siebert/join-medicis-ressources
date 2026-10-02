# Exemple : du commentaire à la relance

Utilisatrice fictive : Camille D., acquisition chez Assurly (assurly.example).
Sarah M., directrice marketing d'un courtier en ligne, a demandé sous son post
« Comment vous avez fait pour rappeler 60 clients sans y passer un mois ? »
(`/linkedin-reply`, lead 8/10). Camille a répondu dans le fil. Elle veut
maintenant écrire à Sarah. Objectif honnête : une conversation qui pourrait
mener à son offre de conseil, sans la nommer.

## Garde-fou

```
python3 commun/garde_fou.py --texte "écrire à Sarah, une prospect venue de mon post"
GARDE-FOU : ENCADRÉ
! E1-PROSPECTION · Prospection à la main
```

## Sortie

```
MESSAGE · Sarah M. (directrice marketing, courtier en ligne) · contexte lead de son fil · objectif conversation
Pourquoi maintenant : sa question sous le post « 60 clients rappelés », il y a 2 jours
Ligne propre : sa question sur le temps passé à rappeler 60 clients

NOTE D'INVITATION (133/200)
Merci pour votre question sous mon post sur les 60 appels. J'y ai répondu
dans le fil ; le script est en bas de ma réponse si besoin.
(contrôle : OK)

PREMIER MESSAGE, 1 à 3 jours après l'acceptation (212 caractères)
Vous parliez du même problème de résiliations chez votre courtier. Si ça vous
sert, je peux vous dire ce qu'on a changé dans les 4 mois qui ont suivi. Si
ce n'est pas le moment, un mot suffit et je n'insiste pas.
(contrôle : OK, prospection : moyen de dire non présent)

RELANCE, à partir de J+7, seulement si le script des 60 appels est publié (103 caractères)
On a publié le script des 60 appels, les 5 questions. Je vous l'envoie s'il
peut servir à votre équipe.
(contrôle : OK)

Ensuite : stop. Dans journal.md : | 2026-10-02 | Sarah M. | commentaire sur « 60 appels » | 8 | premier message après acceptation | 2026-10-05 |
```

La note utilise une des 3 notes personnalisées du mois : Sarah est le lead le
plus chaud de la semaine. Le premier message ne nomme pas l'offre de
Camille : il propose ce qu'elle a appris, la vente viendra si Sarah la
demande.

## Le volume de la semaine (sortie réelle)

```
python3 scripts/volume.py --invitations 20 --en-attente 40 --messages 8 --minutes 180 \
  --journal journal-exemple.md --notes 2
VOLUME  OK  ·  4.0 invitations par jour · 60 dans la semaine (en attente comprises) · 164 min nécessaires
  Taux d'acceptation récent : 38% (sur 65 invitations, journal.md)
  Invitations conseillées cette semaine : 23
```

## Ce que le Skill a refusé

Camille avait préparé un modèle pour sa liste de courtiers :

```
python3 scripts/message.py lot --fichier lot-exemple.txt
LOT  ENVOI EN MASSE  ·  3 messages
  ✖ messages 1 et 2 : 91% de texte commun, noms retirés. Un message copié à
    l'identique est un envoi en masse : réécris chacun à partir de sa ligne propre.
```

Et le message 1 seul :

```
python3 scripts/message.py verifier --type message --prospection --texte "Bonjour Paul, je me permets…"
MESSAGE  BLOQUÉ
  ✖ Aucune ligne propre à la personne […]
  ! Une demande de temps sans question précise […]
  ! Prospection sans moyen simple de dire non […]
  ! « je me permets » : formule de courrier type […]
```

Le message 3 (Thomas, « vous écriviez mardi que vos clients partent avant
6 mois ») passe : il ne pouvait partir qu'à Thomas.
