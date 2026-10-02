# Réécrire la page entreprise

## Ce que la page doit faire

La page est consultée **avant** une décision : un prospect qui vérifie à qui
il parle, un candidat qui se renseigne, un journaliste, un partenaire. Elle
doit répondre en quelques secondes à : qui êtes-vous, pour qui, qu'est-ce qui
change avec vous, est-ce vivant ?

## Slogan (120 caractères [à vérifier dans l'éditeur])

Pour qui, ce qui change, une preuve.

| Avant | Après (fictif) |
|---|---|
| « Assurly, l'assurance réinventée » | « L'assurance habitation en ligne pour les locataires : remboursement en 9 jours en moyenne » |
| « Leader de l'assurance digitale » (formulation retirée) | « Assurance habitation pour locataires, souscrite en 4 minutes, 38 000 assurés » |

Chaque chiffre vient de `contexte.md` (preuve LIVE). Un chiffre À CONFIRMER
reste en `{{à confirmer}}`.

## Présentation (2 000 caractères [à vérifier dans l'éditeur])

Structure :

1. **Le problème du lecteur**, avant « voir plus » (les deux premières lignes).
2. **Ce que vous faites, pour qui**, dans les mots des clients (vocabulaire de
   `contexte.md`).
3. **Les offres actuelles**, nommées comme dans `contexte.md`, rien de retiré.
4. **Une ou deux preuves chiffrées**, datées.
5. **La porte d'entrée** : où aller, quoi faire (site, devis, page carrières).

| Ouverture à éviter | Pourquoi |
|---|---|
| « Assurly est une société fondée en 2019 qui… » | parle de l'entreprise avant le lecteur |
| « Leader de… », « solutions innovantes », « équipe passionnée » | mots creux, preuves absentes |
| « Notre mission est de… » | méta-annonce |

Exemple fictif :

```
Un locataire attend en moyenne {{à confirmer : délai du marché}} pour être
remboursé après un dégât des eaux. Chez Assurly, c'est 9 jours.

Assurly assure les locataires en ligne : habitation, responsabilité civile,
objets de valeur. Souscription en 4 minutes, sans papier.

38 000 locataires assurés au 30 septembre 2026.

Devis en ligne sur assurly.example (lien du bouton). Nous recrutons : page
Carrières.
```

## Informations de la page

Site (page en ligne), secteur, taille, siège, date de création : identiques à
`contexte.md` et au site. Les spécialités listent les offres actuelles, pas
l'historique.

## Bouton

Vers la page la plus utile pour le visiteur type : la page de devis plutôt que
l'accueil pour une marque B2C, la page « prendre rendez-vous » pour un cabinet.
Avec des UTM (`utm_source=linkedin&utm_medium=social&utm_campaign=page`) pour
que l'analytics distingue ce trafic.

## Post épinglé et pages vitrines

- Post épinglé : récent (moins de 3 mois), utile à un visiteur qui découvre la
  page (preuve, offre, recrutement), rien de RETIRÉ.
- Pages vitrines : seulement pour une offre ou une audience vraiment distincte
  (une marque employeur, une gamme pour les professionnels). Une vitrine vide
  fait plus de mal que pas de vitrine.

## Logo et couverture (officiel, Aide LinkedIn a563309, vérifié le 2 oct. 2026)

- Logo : 400 × 400 px recommandés (268 × 268 minimum), PNG ou JPEG, 3 Mo.
- Couverture : 1 512 × 256 px, une phrase de positionnement et un moyen de
  contact, contraste suffisant, rien d'important sur les bords (recadrage
  mobile). Pas d'image de banque.

## Ce que publie la page

| Type | Exemple | Fréquence indicative |
|---|---|---|
| conseil pratique pour les clients | « Dégât des eaux : les 3 photos à prendre avant d'appeler » | chaque semaine |
| coulisses, équipe (avec accord) | une personne, son métier, un chiffre de son travail | toutes les 2 semaines |
| cas client autorisé | accord écrit du client pour ce post | quand il y en a |
| repartage du dirigeant, avec une ligne | 2 jours après son meilleur post | chaque semaine |
| recrutement | le poste, les vraies conditions, un salarié qui en parle | selon les besoins |

Au moins une publication par semaine, des originaux plus que des repartages,
0 à 3 hashtags, réponses aux commentaires sous 2 h quand c'est possible.

## Sources

- JoshuaDIWork, `page_rubric.json` et `positioning.md` (MIT) : grille de la
  page, deux voix, coordination, UTM, formulations retirées.
- Aide LinkedIn a563309, « Image specifications for your LinkedIn Pages and
  Career Pages » (consultée le 2 octobre 2026).
