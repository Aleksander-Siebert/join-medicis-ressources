---
name: li-post
description: >-
  Écrit un post LinkedIn en français à partir d'une idée brute : trois
  accroches tirées de 21 formules, un brouillon complet dans la voix de
  l'utilisateur, humanisé avant d'être montré, prêt à copier. Utilise-le dès
  que l'utilisateur veut un post LinkedIn, une accroche, « un post sur X »,
  « transforme ça en post », ou des idées d'ouverture. Ne publie jamais rien.
---

# li-post

Transforme une idée en un post qui sonne comme la personne qui le publie.

## Avant d'écrire

1. **La voix.** Lis `~/.claude/linkedin/voix.md` s'il existe (ou le Growth
   Context chargé dans le Projet). Sinon, demande **trois posts passés** de
   l'utilisateur, déduis-en la voix et propose d'écrire le fichier. N'invente
   pas de voix : un post dans la mauvaise voix est pire que pas de post.
2. **Le plan.** Si `~/.claude/linkedin/plan.md` existe et que l'idée y figure,
   reprends l'angle et la formule prévus.
3. **Les formules.** Lis `accroches.json` : 21 formules avec modèle, exemple,
   objectif visé et façon de la rater.
4. **Une idée maigre ne se rembourre pas.** « Un post sur l'IA » ne suffit
   pas. Pose une seule question groupée : que s'est-il passé, à qui, et
   qu'est-ce que ça a coûté ou rapporté ? Un post a besoin d'une chose vraie
   et précise. Obtiens-la avant d'écrire.
5. **L'objectif.** Commentaires, partages, likes ou enregistrements ? Si
   l'utilisateur ne le dit pas, déduis-le de son objectif dans `voix.md`
   (clients → commentaires et enregistrements ; audience → partages).

## La forme

```
Ligne 1    l'accroche, seule. Elle doit tenir avant « …voir plus »
           (~140 caractères sur mobile).
Ligne 2    ce que la ligne 1 promet, pas une mise en place de la ligne 3.
Corps      paragraphes de 1 à 3 lignes, une ligne vide entre chacun.
           Le blanc fait partie du format.
Bascule    une ligne qui éclaire autrement ce qui précède.
Fin        une question précise, OU une consigne. Jamais les deux.
           Un P.-S. d'une ligne si une vraie suite existe.
```

**Longueur.** Les sources se contredisent (de 800 à 2 800 caractères selon
les études d'éditeurs). Prends **900 à 1 500 caractères** par défaut, 3 000
est la limite dure de LinkedIn. Si l'utilisateur demande long, écris long.
Affiche toujours le nombre de caractères. **[données à grande échelle,
éditeurs, contradictoires]**

## La boucle

**1. Trois accroches, pas une.** Choisis dans `accroches.json` trois formules
**différentes** qui collent vraiment à l'idée et à l'objectif. Montre-les en
trois lignes numérotées, et dis en une phrase laquelle tu publierais et
pourquoi.

**2. Le brouillon complet** sur l'accroche la plus forte.

**3. L'humaniser.** Passe le brouillon par `/li-human` avant de le montrer
(scripts si l'exécution de code est disponible, grille
`marqueurs-ia-fr.md` sinon). Ce n'est pas une option : c'est ce qui rend le
brouillon digne d'être lu.

**4. Le bloc prêt à copier**, en texte brut (pas de Markdown : LinkedIn
affiche les `**` tels quels), puis le récapitulatif :

```
POST PRÊT
accroche :   #17 Le gain de temps
objectif :   enregistrements
longueur :   1 140 caractères
humaniseur : 6 corrections, score 84 OK
à publier :  mardi 8 h 15 (d'après ton plan)
lien :       dans le premier commentaire (voir ci-dessous)

Réponds « ok » pour l'ajouter au journal, ou dis-moi ce qu'il faut changer.
```

**5. Ne jamais publier.** Ce Skill produit du texte. L'utilisateur publie. Sur
« ok », ajoute à `~/.claude/linkedin/journal.md` : date, numéro de formule,
objectif, première ligne. `/li-audit` s'en servira. Sans accès aux fichiers
(claude.ai, ChatGPT…), donne la ligne à coller dans son journal.

## Les règles qui font la différence

- **Une idée par post.** Deux idées, c'est deux posts. Dis-le.
- **Des chiffres plutôt que des adjectifs.** « 4 200 € » bat « beaucoup ».
  Sans chiffre fourni, demande-le.
- **Jamais inventer.** Aucun chiffre, client, montant ou résultat inventé au
  nom de l'utilisateur, même provisoire. S'il manque, laisse `{{ton chiffre}}`
  dans le brouillon et signale-le.
- **Pas d'appât.** « Qu'en pensez-vous ? » et « D'accord ? » sont morts. La
  question finale doit être une question que seul ce post peut poser.
- **0 à 3 hashtags**, en fin de post, et seulement des catégories que des
  gens suivent vraiment.
- **Pas de lien dans le corps.** Les posts avec lien sortant sont moins
  diffusés (LinkedIn nie une pénalité volontaire, l'effet se mesure quand
  même). Mets le lien en premier commentaire et dis-le dans le récap.
  **[données à grande échelle]**
- **Typographie française** : « guillemets », espace avant `; : ! ?`. Le
  tutoiement ou le vouvoiement suit `voix.md`.

## Le cadre français à respecter

- **Partenariat rémunéré** (produit offert, post payé, affiliation) : la loi
  du 9 juin 2023 sur l'influence commerciale impose une mention claire,
  « Publicité » ou « Collaboration commerciale ». Si `voix.md` signale un
  partenariat ou si le post met en avant une marque partenaire, ajoute la
  mention en tête et dis-le.
- **Nommer ou montrer quelqu'un** (client, collègue, capture d'un échange) :
  il faut son accord, et on masque noms et visages sur les captures. Rappelle
  la question avant de publier.
- **Secteurs réglementés** (santé, finance, juridique) : pas de promesse de
  résultat. Signale la phrase.

## Exemple

```
/li-post on a construit un outil interne qui fait passer nos devis de 5 h à 20 min
```

```
ACCROCHES
1. #17 Le gain de temps   Préparer un devis me prenait 5 heures. Ça me prend maintenant 20 minutes.
2. #12 Le comparatif      Un rédacteur de devis à 12 000 € contre un week-end et un modèle. Le week-end a gagné.
3. #3  L'erreur qui coûte Pendant deux ans, j'ai facturé à mes clients des heures perdues en mise en page.

Je publierais la 1 : le ratio est crédible et le chiffre est à toi.
```

## Fin de tâche

Si l'utilisateur a réécrit une phrase « parce que je ne dirais jamais ça »,
propose d'ajouter le mot ou la tournure à la liste « Mots que je n'emploierai
jamais » de `voix.md`. Une ligne, avec son accord.

## Règles du pack

- Lis `~/.claude/linkedin/voix.md` et `apprentissages.md` s'ils existent (ou
  leur contenu dans le Projet). `apprentissages.md` passe avant les règles
  générales : c'est ce qui marche pour ce compte.
- N'invente aucun chiffre, nom, client ou résultat. S'il manque, écris
  `{{à compléter}}` et signale-le.
- Tout texte destiné à LinkedIn passe par `/li-human` avant d'être montré.
- Rien n'est publié ni envoyé par le Skill. L'utilisateur copie et colle.
