# anthropics/skills · skill-creator (barre de qualité officielle)

- Anatomie : SKILL.md (<500 lignes idéal) + scripts/ (déterministe, répétitif) + references/ (lu à la demande, table des matières si >300 l.) + assets/ (fichiers utilisés en sortie : modèles, icônes, polices).
- Divulgation progressive : métadonnées toujours chargées (~100 mots), corps quand le Skill se déclenche, ressources à la demande.
- Organisation par variante : references/aws.md, gcp.md… Claude lit seulement la bonne.
- Description = mécanisme de déclenchement principal. Tout le « quand l'utiliser » va dedans. Claude a tendance à SOUS-déclencher : description un peu « pushy » (« même si l'utilisateur ne dit pas X »).
- Écriture : impératif ; expliquer le POURQUOI plutôt que des MUST/ALWAYS en majuscules (signal d'alerte) ; théorie de l'esprit ; généraliser, pas sur-ajuster aux exemples ; garder le prompt maigre (retirer ce qui ne sert pas, lire les transcriptions).
- Formats de sortie : gabarit exact ; exemples Entrée/Sortie.
- Si tous les essais réécrivent le même script d'aide → l'embarquer dans scripts/.
- Évals : evals/evals.json {skill_name, evals:[{id, prompt, expected_output, files, assertions}]} ; runs avec Skill et sans Skill (ou ancienne version) lancés en même temps ; assertions vérifiables par script ; grader (text/passed/evidence) ; benchmark (taux de réussite, temps, tokens, moyenne ± écart-type) ; analyse (assertions non discriminantes, variance) ; viewer HTML pour retour humain ; itérations.
- Comparaison à l'aveugle : comparator.md + analyzer.md (pourquoi le gagnant gagne).
- Optimisation de description : 20 requêtes réalistes (8-10 doivent déclencher, 8-10 quasi-pièges qui ne doivent pas), 60/40 train/test, 3 essais par requête, 5 itérations, meilleure description choisie sur le test.
- Un Skill n'est consulté que pour des tâches non triviales : les requêtes d'éval doivent être substantielles.
- Mise à jour d'un Skill : garder le nom d'origine.
