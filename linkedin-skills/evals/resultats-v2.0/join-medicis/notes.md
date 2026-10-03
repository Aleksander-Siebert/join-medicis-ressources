# Problèmes rencontrés dans les Skills

## Scripts

- **linkedin-human / marqueurs** : « Le résultat ? » n'est détecté qu'en début de ligne (motif `^` dans tics-ia.json) ; au milieu d'un paragraphe (cas 7), il passe. « véritable » n'est repéré qu'après « un/une » (« véritable pilier » passe). La triade sans « et » (« Rapidité, transparence, proximité : ») et « voilà les clés du succès » ne sont pas signalées.
- **linkedin-human / fidelite.py** : les champs `{{à compléter}}` comptent comme des AJOUTS bloquants. Une réécriture honnête qui laisse des trous sort « FIDÉLITÉ : AJOUTS ».
- **garde_fou.py** : « un message que je peux envoyer à ma liste de 200 DAF » sort ENCADRÉ (E1), pas REFUSÉ (R5), alors que le SKILL.md de linkedin-dm dit que « le même message pour ma liste » est refusé. R5 exige « même/identique » ou « en masse ».
- **linkedin-audit / audit.py** :
  - `audit.py experience --help` plante (ValueError, `%` non échappé dans une aide argparse).
  - Le regroupement des motifs confondus ne compare chaque motif qu'au premier du groupe, en Jaccard. Il rate « longueur courte » (6 posts, tous des jeudis) et « pilier Rétention » (5 posts, tous des mardis), alors que methode.md parle de recouvrement « dans un sens ou dans l'autre ».
  - La ligne « Expériences en cours » répète la variable pour A et pour B au lieu de nommer les deux variantes.
- **linkedin-profile / titre.py** : la preuve ne reconnaît que %, €, « ex- » et une liste de mots de volume. « 60 résiliés rappelés » et « de 12 à 5 jours » valent 0. Le script pousse donc vers des preuves en euros, même quand la preuve en jours ou en appels sert mieux l'offre.
- **linkedin-profile / audit_profil.py** : des Infos qui s'ouvrent sur « Bienvenue sur mon profil ! » obtiennent 7/10 pour le pli, alors que infos.md classe cette ouverture parmi celles à éviter.
- **linkedin-inbox / boite.py crm** : la colonne Note coupe le message au milieu d'une phrase (« Vous accompagnez des équipes »).
- **linkedin-repurpose / registre.py** : SKILL.md et la description citent le webinaire, mais `--type` le refuse (seul `video` passe).
- **linkedin-strategie / budget.py** : à l'étape « départ » avec 120 min, le script rend 0 post, parce que le minimum de commentaires est codé à 5 par jour × 6 min = 150 min. Ça contredit la règle des 60% du SKILL.md et la « semaine minimale » (~75 min, 1 post) que le même script affiche.
- **linkedin-strategie / brief.py** : la phrase de positionnement générée colle les champs sans grammaire (« … dont les résiliations montent à ils ne savent pas pourquoi… grâce à rappeler… »).

## Incohérences entre fichiers

- **linkedin-plan** : le SKILL.md bloque 30 min de réponses après chaque post, semaine.py en compte 20.
- **linkedin-inbox** : le modèle de refus de reponses.md (« voici ce que je vous aurais dit ») est signalé comme méta-annonce par l'humaniseur, à qui chaque brouillon doit passer.
- **Les exemples Assurly ne racontent pas tous la même histoire.** linkedin-post/references/exemple.md parle de janvier 2026 et d'un délai de 21 à 9 jours. Les exemples de linkedin-reply et linkedin-inbox ajoutent des faits absents du contexte : « le plus long a été de retrouver des numéros à jour », « chez certains de nos clients c'était la première raison », « deux équipes ». Les cas d'éval reprennent presque mot pour mot ces exemples, d'où un risque de recopier ces faits comme s'ils venaient de l'utilisatrice.
- **linkedin-plan/assets/plan-exemple.json** nomme Inès, alors que le contexte de l'utilisateur ne la donne pas. Ce fichier est fait pour être copié.

## Consignes peu claires

- **linkedin-human, cas sans contexte (cas 7)** : la passe 3 demande d'ajouter un chiffre avec son référent, ou de poser une question. Aucun format de sortie ne prévoit de rendre le texte avec ses trous **et** les questions. Je les ai mises sous le reçu.
- **linkedin-dm** : pour une vraie liste de 200 personnes, le Skill ne dit pas quoi livrer. Je refuse le message unique, puis je donne un gabarit avec la ligne propre en champ, un message par personne. Le format de sortie fixe est prévu pour une seule personne.
