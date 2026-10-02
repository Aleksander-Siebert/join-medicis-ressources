# Exemple : un webinaire de 23 minutes

Utilisatrice fictive : Camille D., acquisition chez Assurly
(assurly.example). Elle colle la transcription de son webinaire sur les
résiliations (`evals/linkedin-repurpose/source-exemple.md`). Son registre
contient déjà une idée tirée de ce webinaire, publiée le 8 septembre.

## Découpe (sortie réelle)

```
python3 scripts/registre.py decouper --fichier source-exemple.md --type video \
  --journal journal-exemple.md --source webinaire
SOURCE  UNITÉS UTILISABLES · 4 unités, 2 utilisable(s) · rendement habituel pour ce type : 3 à 6
  TROUVÉ  0 affirmation(s), 10 chiffre(s), 9 histoire(s), 1 mécanisme(s), 1 erreur(s), 15 phrase(s) citable(s)

  [1] Le chiffre que personne ne croyait · 100/100 · 391 car. · texte, récit (formules scene, erreur-datee)
      accroche possible : « En mars 2024, on a mesuré pour la première fois notre taux de départ à six mois. »

  [2] Les 60 appels · écartée · 344 car. · texte, récit (formules scene, erreur-datee)
      accroche possible : « Inès et moi, à deux, en 3 semaines. »
      - commence par un renvoi (« Du coup ») à ce que le lecteur n'a pas lu : le retirer et réécrire l'ouverture
      ! trace à retirer : tics d'oral de transcription
      ! déjà publiée : 2026-09-08 : Rappeler 60 clients partis a montré que la moitié citait le délai de remboursement, pas le prix

  [3] Le script · 100/100 · 377 car. · carrousel (étapes) : /linkedin-carrousel
      accroche possible : « Les appels duraient 6 minutes en moyenne. »
      ! trace à retirer : renvoi au format d'origine (« dans cette vidéo »)

  [4] Ce qui a changé · écartée · 175 car. · texte, récit (formules scene, erreur-datee)
      accroche possible : « Le coût par lead est redescendu à 23 € en 4 mois, à budget constant. »
      - 175 caractères : trop court pour une affirmation et sa preuve
      - commence par un renvoi (« Donc on a raccourci le dé ») à ce que le lecteur n'a pas lu : le retirer et réécrire l'ouverture
      ! trace à retirer : appel à s'abonner d'une autre plateforme

  Chaque unité est une matière, pas un post. Il manque toujours la phrase que seul l'auteur peut écrire : ce que ça a coûté, ce qu'il croyait, ce qu'il ferait autrement.
```

Ce qui se lit :

- l'unité 2 (les 60 appels) est **déjà publiée** le 8 septembre : elle sort
  de la semaine, même réécrite ;
- l'unité 4 (ce qui a changé) commence par « Donc » et fait 175 caractères :
  elle ne tient pas seule, elle sert de preuve à l'unité 1 ;
- l'unité 3 est un mécanisme en 5 étapes : un carrousel.

## Les idées vérifiées dans le registre

```
python3 scripts/registre.py verifier --idee "Le taux de départ à six mois était de 31% et personne n'y croyait" --journal journal-exemple.md
IDÉE  NOUVELLE · aucune idée proche dans le registre.

python3 scripts/registre.py verifier --idee "La moitié des 60 clients rappelés citait le délai de remboursement, pas le prix" --journal journal-exemple.md
IDÉE  DÉJÀ PUBLIÉE · publiée il y a moins de 90 jours : l'audience s'en souviendra avant toi.
```

## Sortie

```
SOURCE · « Pourquoi nos clients partaient » (webinaire, 23 min) · auteur : Camille
TROUVÉ  10 chiffres, 9 histoires, 1 mécanisme, 1 erreur, 15 phrases citables
UNITÉS  2 utilisables · 2 à réécrire (renvoi pendant) · 1 déjà publiée

PROPOSITION
MAR  chiffre-d-abord  texte  « En mars 2024, on a mesuré pour la première fois notre taux de départ à six mois. Il était de 31%. »
      avec l'unité 4 comme preuve : coût par lead redescendu de 41 € à 23 € en 4 mois
      il manque : ce que ça a coûté (« deux comités à parler de budget payant » est
      dans la source : à confirmer, c'est la phrase qui porte le post)
JEU  liste-promise  carrousel  « Les 5 questions qu'on pose à un client parti »
      traces retirées : « Comme je le disais dans cette vidéo »
      il manque : ce que tu ferais autrement (une 6e question ? un ordre différent ?)

Pas de 3e post cette semaine : l'unité des 60 appels est déjà sortie le 8 septembre.
Dis « écris le 1 » et /linkedin-post le rédige.
```

## Après publication

```
python3 scripts/registre.py noter --idee "Le taux de départ à six mois était de 31% et personne n'y croyait" \
  --source "webinaire résiliations" --format texte --journal ~/.claude/linkedin/journal.md
```
