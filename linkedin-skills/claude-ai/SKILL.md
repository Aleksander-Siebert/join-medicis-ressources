---
name: linkedin-skills
description: >-
  Pack LinkedIn en français, en un seul Skill : écrire un post (21 formules
  d'accroche), commenter les posts des autres, répondre aux commentaires,
  noter et réécrire un profil avec des expériences chiffrées, planifier la
  semaine, faire un carrousel PDF, recycler un contenu long, écrire des
  messages privés et relances, trier la messagerie, auditer ses posts,
  chercher des offres d'emploi de la dernière heure, et humaniser un texte
  (retirer les marques d'écriture IA). Utilise-le pour toute demande liée à
  LinkedIn, ou quand un texte doit sonner moins IA.
---

# LinkedIn Skills (Join Médicis)

Ce Skill regroupe les 12 modules du pack LinkedIn Skills. Chaque module est
un mode d'emploi complet rangé dans `modules/<nom>/<nom>.md`, avec ses
fichiers (formules, grilles, scripts) dans le même dossier.

## Choisir le module

| Module | Quand l'utiliser |
|---|---|
| `linkedin-post` | écrire un post, trouver une accroche, « fais un post sur… » |
| `linkedin-comment` | commenter le post de quelqu'un d'autre |
| `linkedin-reply` | répondre aux commentaires sous un de ses posts |
| `linkedin-profile` | noter, réécrire ou peaufiner son profil, chiffrer ses expériences |
| `linkedin-plan` | planifier la semaine LinkedIn, calendrier éditorial |
| `linkedin-human` | humaniser un texte, « ça fait IA ? », retirer les tirets cadratins |
| `linkedin-carousel` | carrousel, post document, slides LinkedIn en PDF |
| `linkedin-repurpose` | transformer une vidéo, un podcast, une newsletter en posts |
| `linkedin-dm` | demande de connexion, message privé, relances |
| `linkedin-inbox` | trier la messagerie LinkedIn |
| `linkedin-audit` | analyser ses posts publiés, ce qui marche |
| `linkedin-job` | chercher des offres d'emploi, URL des offres de la dernière heure |

L'utilisateur peut aussi taper le nom du module comme une commande
(`/linkedin-post …`).

## Comment travailler

1. Choisis le module qui correspond à la demande. Si deux conviennent,
   prends celui qui produit le texte final et appelle l'autre ensuite.
2. **Lis en entier `modules/<nom>/<nom>.md`** avant de répondre, puis suis-le.
   Les fichiers qu'il cite (`accroches.json`, `grille.json`, `humanize.py`,
   `job_url.py`, `gabarit.html`, `references/…`) sont dans son dossier.
3. Quand un module dit « passe par `/linkedin-human` », lis
   `modules/linkedin-human/linkedin-human.md` et applique-le : scripts si
   l'exécution de code est disponible, grille
   `modules/linkedin-human/references/marqueurs-ia-fr.md` sinon.
4. Les modèles `voix.md`, `journal.md` et `apprentissages.md` sont dans
   `templates/`. Sur claude.ai, ils ne sont pas enregistrés entre deux
   conversations : propose à l'utilisateur de remplir `voix.md` et de le
   garder dans les connaissances de son Projet.

## Règles communes

- Lis `voix.md` et `apprentissages.md` de l'utilisateur s'ils sont fournis.
- N'invente aucun chiffre, nom, client ou résultat : écris `{{à compléter}}`.
- Typographie française : espace avant `; : ! ?`, guillemets « », « 15% »,
  pas de tiret cadratin.
- Rien n'est publié ni envoyé à la place de l'utilisateur. Il copie et colle.

Pack open-source (MIT) : https://github.com/Aleksander-Siebert/join-medicis-ressources
