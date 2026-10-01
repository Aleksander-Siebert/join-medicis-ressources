---
name: linkedin-comment
description: >-
  Écrit des commentaires LinkedIn qui apportent quelque chose sous les posts
  des autres : neuf types de commentaires choisis selon ce qu'est vraiment le
  post, jamais « Super post ! ». Utilise-le quand l'utilisateur veut commenter
  un post, préparer une session d'engagement, « réagir à ce post », ou colle le
  texte d'un post en demandant quoi répondre.
---

# linkedin-comment

Commenter est le geste le plus rentable de LinkedIn et le plus facile à rater.
Un commentaire sous un post à 400 réactions est vu par plus de monde que la
plupart des posts de l'utilisateur. Un commentaire générique n'est vu par
personne et coûte de la crédibilité auprès de l'auteur.

## Entrée

L'utilisateur colle le texte du post (et si possible le nom et le rôle de
l'auteur). Une capture d'écran suffit, lis-la. Avec une URL que tu ne peux pas
ouvrir, demande le texte : ne devine jamais ce que disait le post, et ne
parcours jamais le fil LinkedIn avec un navigateur.

Lis `~/.claude/linkedin/voix.md` pour le ton et les preuves utilisables.

## Les neuf types

Choisis selon ce qu'est le post. Ne prends jamais le type 1 par défaut.

| # | type | quand | forme |
|---|---|---|---|
| 1 | **Ajouter une donnée** | le post affirme quelque chose que tu peux étayer | « Même constat chez nous : 40% de nos… » |
| 2 | **Le cas manquant** | le post a raison mais oublie un cas | « Vrai tant que {condition}. Après… » |
| 3 | **Le désaccord poli** | tu penses vraiment qu'il a tort | l'accord d'abord, puis l'embranchement |
| 4 | **Prolonger une phrase** | une phrase du post est la bonne | la citer, puis construire dessus |
| 5 | **La vraie question** | le post a sauté la partie difficile | une question, précise, sans « curieux d'avoir ton avis » |
| 6 | **Le vécu** | tu as fait ce qu'il décrit | ce qui s'est passé, en deux phrases |
| 7 | **La correction** | il y a une erreur factuelle | avoir raison, être bref, aimable, sûr |
| 8 | **Le recadrage** | les bons faits, le mauvais cadre | « Autre façon de le lire : » |
| 9 | **La ligne** | le post n'a besoin de rien, tu veux être présent | moins de 12 mots, drôle ou vrai |

## Règles

- **2 à 4 phrases.** Plus long, ça ressemble à un détournement. Plus court, à
  du remplissage.
- **Jamais d'ouverture** « Super post », « J'adore », « Tellement vrai »,
  « Je ne peux qu'approuver », « Ça résonne », ni le prénom de l'auteur suivi
  d'un point d'exclamation. Six formules invisibles.
- **Pas d'émoji en premier caractère.** Ni 🔥 ni 👏.
- **Ne jamais résumer le post.** L'auteur sait ce qu'il a écrit, les lecteurs
  aussi.
- **Une idée.** Deux idées, c'est un article déguisé.
- **Dire la chose précise.** Si le commentaire pouvait aller sous n'importe
  quel post du même sujet, c'est du bruit.
- **Apporter un mot nouveau** : au moins une notion, un nom ou un chiffre qui
  n'est pas dans le post. **[estimation de praticien]**
- **Le désaccord marche**, mais l'accord vient d'abord et il est sincère.
- **Ne cite pas le produit de l'utilisateur** sous le post d'un autre. Décris
  ce qu'il fait si c'est utile.
- **Tutoiement ou vouvoiement** : celui du post. Dans le doute, celui de
  `voix.md`.

## Sortie

**Deux options de types différents**, étiquetées, et une ligne qui dit
laquelle publier. Passe les deux par `/linkedin-human` avant : un tiret cadratin se
voit encore plus dans un commentaire que dans un post, parce qu'on lit les
commentaires de près.

```
COMMENTAIRES  (sur le post de @auteur à propos du recrutement)

[6 · Le vécu]
On a testé le recrutement sans CV sur 3 postes l'an dernier. Deux ont été nos
meilleures embauches. La troisième, un échec, et la différence venait de
l'expérience réelle du métier, pas de l'entretien.

[3 · Le désaccord poli]
D'accord sur le problème du signal. Ce qui a marché chez nous, ce n'était pas
de retirer le CV mais de donner à chaque candidat le même exercice payé de
90 minutes. Même résultat, beaucoup moins de débats en interne.

Publie le premier : ce sont tes données, et il admet un échec. C'est la
partie à laquelle on répond.
```

## Mode session

Pour une session d'engagement, demande les 5 à 10 posts collés en un seul
message et rends un commentaire par post dans un seul bloc. Tiens à jour dans
`~/.claude/linkedin/journal.md` qui a été commenté cette semaine : commenter
les trois mêmes personnes tous les jours se voit, et ça ressemble à ce que
c'est.

## Jamais

Ne publie rien. N'utilise aucun outil de navigateur pour poster à la place de
l'utilisateur. La publication automatisée et l'extraction de données violent
les conditions d'utilisation de LinkedIn et mettent le compte en danger. Ce
Skill écrit le commentaire. L'utilisateur le publie.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Tout texte destiné à LinkedIn passe par `/linkedin-human` avant d'être montré.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
