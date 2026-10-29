# Construire le portefeuille de questions

Les questions suivies décident de ce que les chiffres veulent dire. Un
portefeuille rempli de questions de définition (« qu'est-ce qu'une
mutuelle ? ») donne une visibilité flatteuse et ne dit rien des ventes.

Sources de la méthode : marketingskills `ai-seo` (Corey Haines, MIT),
Skills de Profound (MIT), Skill `aeo` d'elmo (MIT), réécrits pour le
français.

## 1. D'abord la décision

Écris la décision que la mesure doit éclairer, avant la première question :

- « Sommes-nous dans la liste courte des familles qui s'expatrient ? »
- « Notre nouvelle offre freelance a-t-elle changé ce que disent les IA ? »
- « Gagnons-nous du terrain face à April International sur les
  comparatifs ? »

Une décision différente donne un portefeuille différent.

## 2. D'où viennent les questions

Par ordre de préférence :

1. **Ce que les clients disent avoir demandé** à une IA. Ajoute un choix
   « une IA (ChatGPT, Perplexity…) » au champ « comment nous avez-vous
   connus ? », suivi de « qu'avez-vous demandé ? ».
2. **Les mots des clients** avant qu'ils connaissent la marque : appels,
   tickets, formulaires, objections des commerciaux.
3. **Search Console** : requêtes longues (6 mots et plus) avec des
   impressions, qui commencent par « comment », « quel », « quelle »,
   « pourquoi », ou contiennent « vs », « ou », « pour ».
4. **Forums et communautés** : fils qui demandent une recommandation dans
   la catégorie.
5. **Recherches associées et autocomplétion**, pour les variantes de
   formulation.

Ne transforme pas mécaniquement une liste de mots-clés en questions :
« mutuelle expat » et « je pars à Dubaï avec deux enfants, quelle
assurance santé ? » ne font pas lire les mêmes sources à une IA.

## 3. Les intentions

| Intention | Forme typique (Assurly, fictif) | Valeur |
|---|---|---|
| `decouverte` | « Je pars travailler à Dubaï avec deux enfants, quelle assurance santé ? » | haute : client qui ne connaît pas encore la marque |
| `comparaison` | « Quelle est la meilleure assurance santé pour un expatrié français ? » | haute : liste courte |
| `alternative` | « Quelle alternative à April International pour un expatrié ? » | haute : client d'un concurrent |
| `usage` | « CFE ou assurance au premier euro, que choisir quand on part en Asie ? » | moyenne : prépare la décision |
| `prix` | « Combien coûte une assurance santé expatrié pour une famille ? » | moyenne ; vérifie aussi l'exactitude |
| `confiance` | « Assurly est-il fiable ? », « Assurly a-t-il des litiges ? » | contrôle de réputation |
| `marque` | « Que propose Assurly ? » | contrôle d'exactitude, peu de valeur de visibilité |

Pondère par la valeur : une citation sur une question de définition vend
rarement quelque chose. Supprime les questions qui ne changeraient aucune
décision d'achat. **Trente questions nettes valent mieux que trois cents
floues.**

## 4. Les trois cohortes

| Cohorte | Rôle | Règles |
|---|---|---|
| `coeur` | la tendance que l'on rapporte | 15 à 30 questions ; 70 à 85% sans la marque ; **figé** : on ajoute, on ne modifie pas une question existante (sinon l'historique n'est plus comparable) |
| `exploratoire` | nouvelles demandes, nouveaux concurrents, formulations à tester | tourne librement ; une question qui compte entre au cœur, avec une nouvelle version |
| `temoin` | détecter une dérive de la mesure | au moins une question où la marque **doit** apparaître (`attendu = present`) et une où elle **ne doit pas** (`attendu = absent`) |

Si un témoin bouge, c'est l'outil, la saisie ou le moteur qui a changé, pas
le travail de l'équipe.

## 5. Formulation

- Comme on parle à une IA : phrases complètes, contexte, contraintes
  (« pour une famille de 4 », « budget 300 € par mois », « je suis
  freelance »).
- En français de France, avec les mots du secteur en France (CFE, mutuelle,
  « reconditionné », « garantie légale de conformité »), pas une traduction.
- 2 ou 3 formulations seulement pour les intentions les plus précieuses ;
  sinon, une question par intention.
- Pas de question orientée : « Pourquoi Assurly est-il le meilleur ? »
  contient déjà la réponse.
- Langue et pays sont deux dimensions : une mesure en français pour la
  Belgique est une autre configuration qu'en France ; ne les mélange pas.

## 6. Parcours en plusieurs tours (option)

Un achat ne se joue pas en une question. Pour 2 ou 3 intentions clés, écris
une question d'ouverture et 2 relances réalistes (« et pour un séjour de
6 mois ? », « laquelle est la moins chère ? »). Mesure la réponse **finale**
séparément, avec un identifiant à part (ex. `P01-R2`).

## 7. Le fichier

```
id;cohorte;intention;prompt;attendu
P01;coeur;decouverte;Je pars travailler à Dubaï avec deux enfants, quelle assurance santé prendre ?;
P02;coeur;comparaison;Quelle est la meilleure assurance santé pour un expatrié français ?;
P06;coeur;marque;Assurly est-il un courtier fiable pour les expatriés ?;
P07;exploratoire;prix;Combien coûte une assurance santé expatrié pour une famille ?;
T01;temoin;marque;Que propose Assurly ?;present
T02;temoin;hors-sujet;Quelle tondeuse robot acheter pour un petit jardin ?;absent
```

Séparateur `;` (ou `,`). Garde un journal des versions : date, questions
ajoutées, raison. Ne compare jamais deux périodes mesurées avec des cœurs
différents sans le dire.
