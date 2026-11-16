# Données pour la recherche de mots-clés : quoi récupérer, et comment

Mode gratuit par défaut. Chaque chiffre de la sortie dit d'où il vient et
de quelle période.

| Source | Coût | Quoi récupérer | Comment | Limite |
|---|---|---|---|---|
| Search Console, interface | gratuit | requêtes du site, clics, impressions, position, sur 3 à 16 mois | Performances → Résultats de recherche → Exporter | l'export sépare requêtes et pages : il ne dit pas quelle page porte quelle requête |
| Search Console, requête × page | gratuit | le croisement requête × page, nécessaire à `cannibalisation` et `groupes` | API Search Console (connecteur), Looker Studio (dimensions Requête et Page de destination), ou un module de tableur | les requêtes rares sont anonymisées et absentes de l'export |
| Google, lecture manuelle | gratuit | 10 premiers résultats, recherches associées, « Autres questions posées » | outil de lecture web, ou relevé collé par l'utilisateur ; toujours avec date, pays et appareil | une SERP change d'un jour et d'un lieu à l'autre |
| Semrush, Ahrefs, autre outil | payant | volume, difficulté de l'outil, SERP historiques | connecteur s'il existe ; sinon export CSV de l'utilisateur | les volumes sont des estimations de l'outil, à citer avec son nom ; deux outils divergent |
| Service client, avis, FAQ | gratuit | les mots exacts des clients | fichiers ou textes collés | pas de volume |

## Format des fichiers lus par `motscles.py`

**SERP** (`recouvrement`) : texte, une requête par titre puis ses URL dans
l'ordre :

```
# mutuelle indépendant
https://www.exemple-a.fr/mutuelle-independant/
https://www.exemple-b.fr/guide/mutuelle-tns
…
# mutuelle pour indépendant
…
```

ou JSON `{"mutuelle indépendant": ["https://…", …]}`.

**Search Console** (`cannibalisation`, `groupes`) : CSV avec au moins les
colonnes requête, page et impressions (clics et position en plus si
possible). En-têtes français ou anglais, séparateur virgule ou
point-virgule, décimales à la virgule acceptées.

## Ce qu'on n'utilise pas

- Une courbe de CTR générique pour « prévoir » des clics : le CTR attendu se
  calcule sur les données du site (`/seo-refresh`), sinon on n'en donne pas.
- Un score de difficulté d'outil présenté comme une mesure : c'est
  l'estimation d'un outil, avec son nom.
- Une « Domain Authority » ou un score de domaine comme indicateur de
  réussite : métrique d'outil tiers, pas de Google.
