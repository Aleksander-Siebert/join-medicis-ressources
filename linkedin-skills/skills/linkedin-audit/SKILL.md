---
name: linkedin-audit
description: >-
  Analyse les posts LinkedIn déjà publiés et les classe selon ce qui a
  vraiment marché (taux d'engagement, ratio de commentaires, portée au-delà
  des abonnés), pas selon les impressions. Fait ressortir les formules, formats
  et thèmes qui marchent pour ce compte. Utilise-le quand l'utilisateur veut
  un bilan, « qu'est-ce qui marche chez moi », analyser ses statistiques
  LinkedIn ou décider quoi faire de plus et de moins.
---

# linkedin-audit

La seule source honnête de ce qui marche pour un compte, c'est ce compte.
Chaque règle de chaque guide LinkedIn, y compris celles de ce pack, n'est
qu'un a priori. Les 30 derniers posts de l'utilisateur sont la preuve.

## Entrée

Demande ce que l'utilisateur a :

- l'export des statistiques (LinkedIn : Statistiques → Contenu → Exporter),
  un fichier Excel ;
- ou une capture par post avec impressions, réactions, commentaires,
  republications ;
- ou juste les posts et leurs réactions, qui suffisent pour un premier
  passage.

Lis aussi `~/.claude/linkedin/journal.md` s'il existe : il dit quelle formule
d'accroche chaque post a utilisée. Avec exécution de code, lis l'export
directement (pandas, openpyxl) et montre le calcul.

## Ce qu'il faut mesurer

Les impressions brutes sont le chiffre le moins utile de la page : elles
dépendent surtout du nombre d'abonnés. Calcule plutôt, et montre le calcul :

| indicateur | calcul | ce qu'il dit |
|---|---|---|
| **Taux d'engagement** | (réactions + commentaires + republications) / impressions | si le post a mérité sa portée |
| **Ratio de commentaires** | commentaires / réactions | s'il a lancé une discussion ou juste obtenu un hochement de tête |
| **Portée relative** | impressions / abonnés | s'il est sorti du cercle des abonnés |
| **Enregistrements et envois** | si disponibles | le meilleur indicateur de la portée future |

Classe par taux d'engagement et portée relative, pas par impressions. Un post
à 900 impressions et 40 commentaires a battu celui à 12 000 impressions et 6.

## Trouver la tendance

Avec les 5 meilleurs et les 5 moins bons côte à côte, cherche ce qui les
sépare vraiment, et accepte une conclusion qui déplaira :

- La formule d'accroche (numéros de `linkedin-post/accroches.json`).
- Le format : texte, carrousel, image, vidéo.
- La longueur.
- Le thème.
- Les réponses dans la première heure : posts où l'utilisateur a répondu
  vite, ou non.
- Le jour et l'heure, **en dernier**, et seulement si rien d'autre ne ressort.
  Ce n'est presque jamais la cause, et c'est là qu'on aimerait qu'elle soit.

Énonce chaque conclusion comme une affirmation, avec ses preuves et son
niveau de confiance. Avec 30 posts, on voit une tendance ; avec 6, non, et il
faut le dire au lieu d'en inventer une.

## Sortie

```
AUDIT  ·  31 posts  ·  12 juin - 5 sept.

TOP 5 PAR TAUX D'ENGAGEMENT
  8,1%  #3  L'erreur qui coûte  « 18 000 €, c'est ce que m'a coûté… »   1 940 imp.
  6,4%  #20 Le renoncement      « J'ai refusé notre plus gros client »  2 210 imp.
  ...

FLOP 5
  0,4%  #5  La liste promise    « 7 outils indispensables »            11 400 imp.
  ...

CE QUE DISENT LES DONNÉES
1. Les posts où tu as le mauvais rôle : 6,2% en moyenne contre 1,1% pour le
   reste. n = 6. C'est ton signal le plus fort, et de loin.
2. Les listes d'outils font des impressions et rien d'autre : beaucoup de
   portée, pas de commentaires, pas de prospects. Trois de tes cinq flops.
3. Le jour de la semaine ne montre rien. Mardi et vendredi sont dans le bruit.
   Arrête de l'optimiser.

ARRÊTER : les listes d'outils.
FAIRE PLUS : les posts avec un coût payé et un chiffre.
```

Passe ensuite les conclusions à `/linkedin-plan`, pour que le plan de la semaine
suivante parte des preuves de l'utilisateur plutôt que des valeurs par défaut.

## Fin de tâche : la boucle d'apprentissage

Propose d'ajouter les deux ou trois conclusions solides (n suffisant) à
`~/.claude/linkedin/apprentissages.md`, datées. Tous les Skills du pack le
relisent. Ne l'écris qu'avec l'accord de l'utilisateur, et retire une
conclusion quand un audit suivant la contredit : un apprentissage non vérifié
finit par faire dériver le pack.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Tout texte destiné à LinkedIn passe par `/linkedin-human` avant d'être montré.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
