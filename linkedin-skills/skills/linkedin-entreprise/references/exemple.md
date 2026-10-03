# Exemple : la page et l'équipe d'Assurly

> Les faits de cet exemple sont fictifs (Assurly, Camille et leurs chiffres) : ils
> montrent la méthode. Ne les reprends jamais dans une réponse à l'utilisateur.

Entreprise fictive : Assurly (assurly.example), assurance habitation en ligne
pour locataires, 120 salariés. Entrées : `assets/exemple-page.json` et
`assets/exemple-equipe.json`. Sorties recopiées telles quelles.

## Audit de la page

```
PAGE ENTREPRISE  48/100 points notables (48%)  ·  FAIBLE

Corrections, par points gagnés par heure :
  +3.6  pts  ~0.2 h  Bouton d'action : présent ; manque : page utile, UTM
  +8    pts  ~0.5 h  Post épinglé et pages vitrines : épinglé il y a 210 jours, promeut une offre ou formulation retirée
  +5    pts  ~0.5 h  Présentation : avant « voir plus » : ouvre sur l'entreprise, pas sur le lecteur
  +4    pts  ~0.5 h  Cohérence avec contexte.md : 1 formulation(s) retirée(s) encore visible(s)
  …
```

Les 12 critères sont notés : la marketeuse a fourni la page, l'export des
statistiques et `contexte.md`. Sans l'export, rythme, qualité et engagement
seraient « n/a » et la note serait donnée sur 74 points notables.

## Première heure (proposée)

1. Bouton : vers la page de devis, avec
   `?utm_source=linkedin&utm_medium=social&utm_campaign=page`.
2. Post épinglé : retirer l'ancien (il présente « le leader de l'assurance
   digitale », formulation retirée) ; épingler le post de septembre sur le
   délai de remboursement.
3. Présentation : nouvelle ouverture (voir `references/page.md`), puis
   `/linkedin-human`.

## Programme d'ambassadeurs, semaine 3

```
python3 scripts/ambassadeurs.py plan --fichier assets/exemple-equipe.json --semaine 3
  Directrice générale  régime : 3 post(s), 30 commentaires, … · cette semaine (premier post) : 1 post(s), 12 commentaires
  Camille              régime : 2 post(s), 15 commentaires, … · cette semaine (premier post) : 1 post(s), 6 commentaires
  …
  Léa                  … [hors programme]
  Équipe au régime : 7 posts, 85 commentaires, 5 repartages, ~8,0 h par semaine
  ! Léa : sous le plancher (1 post et 5 commentaires par semaine) ; à associer à un collègue, ou hors programme.
```

Léa (service client) commentera avec Karim, sans objectif de posts.

## Relecture d'un brouillon de Karim

```
python3 scripts/ambassadeurs.py relecture --texte "Grâce à notre nouvelle offre, Maison Durand a réduit son churn de 12% en 2025." --clients "Maison Durand"
RELECTURE  niveau B : relecture des faits par le marketing, objectif 4 h ouvrées, accord tacite à 24 h
  · client nommé : Maison Durand (accord pour ce post ?)
  · chiffre interne possible : « churn de 12% en 2025 » (publiable ?)
  · annonce : « nouvelle offre » (déjà annoncée officiellement ?)
```

Le marketing vérifie l'accord du client et le chiffre ; il ne touche pas au
reste du texte de Karim.
