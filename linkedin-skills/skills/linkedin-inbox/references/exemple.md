# Exemple : une messagerie de 7 fils

> Les faits de cet exemple sont fictifs (Assurly, Camille et leurs chiffres) : ils
> montrent la méthode. Ne les reprends jamais dans une réponse à l'utilisateur.

Utilisatrice fictive : Camille D., acquisition chez Assurly
(assurly.example). Son `contexte.md` liste une offre « étude des
résiliations » (LIVE) et les catégories par défaut. Elle colle 7 fils
(`evals/linkedin-inbox/boite-exemple.txt`).

## Tri (sortie réelle du script)

```
python3 scripts/boite.py trier --fichier boite-exemple.txt --offre "accompagnement,étude,résiliation"

MESSAGERIE · 7 fils · 1 PROSPECT, 1 RECRUTEUR, 1 PAIR, 1 DEMANDE, 1 PARTENAIRE, 2 SPAM

PROSPECT (1) · aujourd'hui, réponse complète
  Nadia K. (Directrice marketing · Mutuelle régionale)
PARTENAIRE (1) · cette semaine
  Sophie L. (Fondatrice · podcast Marketing Assurance)
RECRUTEUR (1) · sous 48 h si le poste t'intéresse, une ligne sinon
  Hélène B. (Talent Acquisition · Assureur en ligne)
DEMANDE (1) · cette semaine si c'est précis et rapide, refus net sinon
  Léo T. (Étudiant en école de commerce)
PAIR (1) · cette semaine
  Marc W. (Consultant acquisition) · déjà répondu

SPAM (2) · à archiver
  Paul Martin : premier message 4 min après l'acceptation; variable de modèle oubliée;
    « petite question »; accroche générique; lien d'agenda dès le premier message;
    offre de leads, de visibilité ou promesse chiffrée; relance sans élément nouveau;
    relances à intervalle exact (J+4); même modèle que le message de Julien V.
  Julien V. : premier message 3 min après l'acceptation; « petite question »; …;
    même modèle que le message de Paul Martin
```

## Sortie du Skill

```
MESSAGERIE · 7 fils · 1 PROSPECT, 1 PARTENAIRE, 1 RECRUTEUR, 1 DEMANDE, 1 PAIR, 2 SPAM

PROSPECT (1) · aujourd'hui · ligne CRM prête
@Nadia K. (Directrice marketing, mutuelle régionale) · « Vous accompagnez des équipes sur ce type d'étude ? »
> Nadia, oui. Le plus utile tient en trois choses : appeler dans le mois qui
> suit la résiliation, 5 questions au plus, et classer les réponses par
> ancienneté du client. Pour un projet au premier trimestre, je vous envoie
> le déroulé et le prix : {{page de l'offre}}.

PARTENAIRE · cette semaine
@Sophie L. · « je co-organise une table ronde sur la rétention en novembre »
> Sophie, la rétention en assurance, c'est exactement mon sujet. Avant de
> dire oui : c'est quelle date en novembre, et vous visez plutôt des
> marketeurs ou des dirigeants ?

RECRUTEUR · sous 48 h
@Hélène B. · Head of Acquisition, CDI, Lyon
Camille n'a pas dit si elle cherche un poste : deux brouillons, à choisir.
> (intéressée) Merci Hélène. Le poste m'intéresse. Quelle rémunération brute
> annuelle, combien de jours sur site, et quelle taille d'équipe ?
> (pas intéressée) Merci Hélène, je ne suis pas en recherche.

DEMANDE · cette semaine
@Léo T. · « 30 minutes pour un café virtuel »
> Léo, pas de café possible ce mois-ci. Pour votre mémoire, partez des
> motifs de résiliation, pas des taux. Les taux, tout le monde les a ; les
> motifs, personne ne les demande.

PAIR
@Marc W. · déjà répondu, rien à faire.

SPAM (2) · à archiver
2 suivent la même séquence : message 3 à 4 minutes après l'acceptation,
« petite question », lien Calendly, promesse de 30 rendez-vous par mois, même
texte chez deux agences.

CRM : 1 ligne (Nadia K.), voir le bloc CSV.
```

## La ligne CRM (sortie réelle, date d'entrée = jour de l'import)

```
Prénom;Nom;Poste;Entreprise;Source;Date d'entrée;Base légale;Note;Prochaine étape;Échéance
Nadia;K.;Directrice marketing;Mutuelle régionale;LinkedIn, message reçu le 2026-09-29;2026-10-03;contact entrant, mesures précontractuelles ou intérêt légitime [à valider];Bonjour Camille, j'ai lu votre post sur les 60 appels aux résiliés. On a le même problème de départs à 6 mois. Vous accompagnez des équipes sur ce type d'étude ? On aurait un projet pour le premier trimestre.;répondre aujourd'hui;2026-10-03
```

## Ce que le Skill n'a pas fait

- Répondre aux deux agences, même pour « les remettre à leur place ».
- Écrire « deux équipes accompagnées » dans la réponse à Nadia : le chiffre
  n'est pas dans `reserve.md`.
- Proposer un créneau à Sophie : l'agenda de Camille n'est pas connu.
