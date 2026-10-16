# Préparer les données de référence

Le registre ne vaut que ce que vaut la référence. Une donnée fausse ou
périmée dans le fichier fait passer une IA juste pour fautive.

## 1. Deux formats

### site-context.md (section « Les données produit »)

```
| Fait | Valeur | Source (page, document, date) | Étiquette |
|---|---|---|---|
| Délai d'envoi de l'attestation | 48 h ouvrées | conditions générales, juin 2026 | LIVE |
| Réduction « premier mois offert » | | offre terminée le 30 juin 2026 | RETIRÉ |
```

Le script tire jusqu'à 4 mots-clés du libellé (mots de 4 lettres et plus,
sans les mots vides) et relie une phrase à la donnée quand **deux** de ces
mots y figurent. Libellés précis : « Délai de carence de la formule
Essentielle », pas « Carence ».

### faits.csv (plus fin, recommandé pour le suivi)

```
id;mots;valeur;unite;statut;source;gravite
F2;formule essentielle|essentielle;39;€;LIVE;grille tarifaire, sept. 2026;critique
F3;premier mois offert|mois offert;1;mois;RETIRÉ;offre terminée le 30 juin 2026;
F5;assure aussi les animaux;assure aussi les animaux;;FAUX;Assurly n'assure pas les animaux;haute
```

- `mots` : variantes séparées par `|` ; **une seule** suffit. Écris-les
  sans majuscule, avec ou sans accent (le script les retire).
- `valeur` et `unite` : un nombre et son unité (`€`, `$`, `%`, `mois`, `an`,
  `jour`, `semaine`, `h`, `Go`). Une année se note avec l'unité `an`.
- `statut` :
  - `LIVE` : vérifiée, en vigueur ;
  - `À CONFIRMER` : pas encore vérifiée ;
  - `RETIRÉ` : n'existe plus (offre terminée, ancien prix) ;
  - `FAUX` : phrase fausse déjà vue dans une réponse, à suivre.
- `gravite` : `critique`, `haute`, `moyenne`, `basse`. Vide : critique si
  les mots parlent de prix, garantie, délai, rétractation, remboursement,
  franchise, carence ou frais, sinon haute.

## 2. Que mettre dans la référence

Dans l'ordre :

1. prix et formules, avec leur devise ;
2. garanties, exclusions, franchises, carences ;
3. délais (livraison, attestation, remboursement, rétractation) ;
4. conditions d'accès (âge, statut, zone géographique) ;
5. identité : année de création, siège, nom légal, dirigeant si public ;
6. chiffres de preuve publiés (clients, avis) avec leur date.

Chaque ligne cite sa source primaire et sa date. Un chiffre lu sur un
comparateur n'est pas une source : c'est peut-être l'erreur qu'on cherche.

## 3. Cas limites connus du script

| Cas | Comportement | Parade |
|---|---|---|
| Prix « à partir de 39 € » et IA « 39 € » | exact | relire : « incomplet » si la nuance compte |
| Plusieurs prix dans une phrase | exact si l'un d'eux correspond | relire la phrase |
| Petits nombres sans unité (« 3 formules ») | ignorés | ajouter une ligne `faits.csv` avec unité vide et le mot-clé |
| Chiffre sans mot-clé de la donnée | invérifiable (s'il a une unité ou vaut 10 ou plus) | compléter les mots-clés |
| Pronom après une phrase sans la marque | non lu | la question nomme la marque, ou relecture |
| Phrase sur un concurrent dans une réponse sur la marque | lue (toute la réponse l'est) | écarter à la relecture |
