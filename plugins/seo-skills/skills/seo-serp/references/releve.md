# Le relevé de SERP lu par `serp.py`

Un CSV, une ligne par résultat organique, dans l'ordre de la SERP. En-têtes
en français, ordre libre, séparateur virgule ou point-virgule.

| Colonne | Obligatoire | Valeurs | Comment la remplir |
|---|---|---|---|
| `position` | oui | 1 à 10 | rang organique, annonces exclues |
| `url` | oui | URL complète | celle du résultat, pas celle d'une redirection |
| `type` | oui | `guide`, `liste`, `comparatif`, `produit`, `categorie`, `outil`, `local`, `forum`, `video`, `actualite`, `officiel`, `definition`, `accueil` | ce que la page **est**, après l'avoir lue ; pas ce que dit son titre |
| `auteur` | non | `oui` / `non` | un auteur nommé et identifiable (page auteur, profil) |
| `date` | non | AAAA-MM-JJ | date de mise à jour affichée ; vide si aucune |
| `mots` | non | nombre | longueur estimée du corps de la page lue |
| `donnees` | non | `oui` / `non` | chiffres, test ou expérience propres à la page, pas repris ailleurs |
| `titre` | non | texte | le title affiché |

Une page qui n'a pas pu être lue : `type` reste celui que montre la SERP
(par exemple `produit` pour une fiche), les autres colonnes restent vides,
et la sortie la liste dans « NON LU ».

Exemple (fictif) :

```
position,url,type,auteur,date,mots,donnees,titre
1,https://www.comparateur-1.example/mutuelle-independant/,comparatif,non,2026-09-01,2400,non,Mutuelle indépendant : comparez
2,https://www.comparateur-2.example/mutuelle-tns/,comparatif,oui,2026-06-12,3100,oui,Mutuelle TNS 2026
3,https://www.blog-freelance.example/mutuelle/,guide,non,2025-03-10,1500,oui,Ma mutuelle de freelance après 3 ans
```

Les éléments de SERP passent en options : `--ai-overview`,
`--extrait-marque`, `--annonces N`.
