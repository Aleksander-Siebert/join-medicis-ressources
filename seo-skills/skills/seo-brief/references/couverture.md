# Le champ sémantique et le test MECE

Le test MECE ne vaut que par sa liste de requêtes. Une liste inventée donne
un test faux qui rassure. On ne garde donc que des requêtes **vues**.

## Construire la liste sans outil payant (20 à 30 requêtes)

| Source | Comment | Ce qu'elle apporte |
|---|---|---|
| « Autres questions posées » | recherche sur la requête principale ; ouvrir quelques questions en fait apparaître d'autres | les questions exactes du lecteur |
| Recherches associées | bas de la première page | les variantes et les étapes voisines |
| Suggestions de la barre de recherche | taper le sujet, puis « sujet a », « sujet b »… ; « sujet pour », « sujet sans », « sujet ou » | la longue traîne réelle |
| Search Console | Performances → Requêtes, filtrées sur la page ou le dossier, puis Exporter (CSV) | ce que le site reçoit déjà, avec impressions |
| Questions clients | FAQ du service client, questions des commerciaux, avis | les mots exacts du lecteur, souvent absents des outils |
| Connecteur (Semrush, Ahrefs) | s'il est branché ; annoncer le coût s'il y en a un | volumes et variantes |

Écris la source de chaque lot dans le brief (« 11 questions de la SERP au
12 oct. 2026, 9 requêtes Search Console 28 jours, 4 questions clients »).

Ce qu'on ne fait pas : générer des variantes « plausibles », traduire des
requêtes anglaises, ajouter l'année partout, inventer des volumes.

## Le format des fichiers

`requetes.txt` : une requête par ligne. Les lignes qui commencent par `#`
sont ignorées. Un export CSV de Search Console marche tel quel (première
colonne, en-tête ignoré, virgule, point-virgule ou tabulation).

`plan.md` : le plan en Markdown (`# H1`, `## H2`, `### H3`, avec une ligne
de description sous chaque titre), ou le format du brief
(`H2 Titre → description`). La description compte : c'est elle qui dit ce
que la section couvre.

Plans concurrents : un fichier par concurrent, en Markdown (`## Titre` par
section), ou la page HTML enregistrée (le script lit les H1 à H3).

## Lire `couverture.py couvrir`

- **Termes de tête** : les mots présents dans au moins 60% des requêtes (le
  sujet de la page, « mutuelle indépendant »). Ils sont ignorés pour
  rattacher une requête à une section, sinon tout serait « couvert » par le
  H1. Une requête faite seulement de ces mots est rattachée au H1.
- **Couverte** : au moins 75% des mots de la requête (hors tête) sont dans
  une section (titre, description, H3).
- **Partielle** : 40 à 75%. La section en parle sans répondre à toute la
  requête : élargir la description, ou ajouter un H3.
- **Non couverte** : moins de 40%. Relis-la : le script ne voit pas les
  synonymes (« freelance » et « indépendant »). Trois issues :
  1. vraie absence → une section ou un H3 à créer ;
  2. synonyme → écrire le mot du lecteur dans la description de la section
     (c'est aussi utile au lecteur) ;
  3. autre intention → renvoyer la requête vers une autre page (lien
     interne), ne pas l'ajouter au plan.
- **Recouvrements** : une même requête est pleinement couverte par deux
  sections. Test : « si je supprime l'une, l'autre l'absorbe-t-elle ? ».
- **Sections proches** : vocabulaire très semblable (cosinus TF-IDF ≥ 0,5).
  Même test.
- **Sections sans requête** : ce peut être le gain d'information (une
  section que personne ne cherche encore mais que le lecteur doit lire), ou
  une section inutile. Justifie-la en une ligne.

Verdict `MECE OK` (code 0) : aucune requête non couverte et aucun
recouvrement. `À REVOIR` (code 2) sinon. Le verdict ne dispense pas de
relire : il trouve les manques évidents.

## Lire `couverture.py grille`

Les titres H2 et H3 des concurrents sont regroupés par sous-thème (mots en
commun, hors termes de tête), puis classés :

| Classe | Concurrents qui le traitent | Décision |
|---|---|---|
| attendu | 80% ou plus (4 ou 5 sur 5) | le lecteur s'attend à le trouver : l'ajouter s'il manque |
| courant | 40 à 79% | l'ajouter s'il sert le lecteur |
| distinctif | 1 seul | l'ajouter seulement s'il est vraiment utile ; ne pas copier un concurrent |
| angle propre | aucun, mais dans notre plan | le gain d'information : le défendre et le développer |

Avec moins de 3 concurrents, seules les classes « attendu » (tous) et
« distinctif » sont calculées. On ignore le nombre de mots des concurrents :
on comble les manques qui comptent, et on s'arrête quand la question du
lecteur a sa réponse.

Méthode inspirée de la grille de couverture du rafraîchissement de contenu
(marketingskills, MIT) et du test MECE du workflow de l'utilisateur.
