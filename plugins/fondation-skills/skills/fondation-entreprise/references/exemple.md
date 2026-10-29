# Exemple : un passage complet, de l'URL au fichier

> **Exemple fictif.** Assurly, ses pages et ses numéros sont inventés. Les
> sorties des scripts sont **réelles** : elles ont été produites par
> `entreprise.py` et `contexte.py` sur les fichiers de test du pack
> (`evals/fondation-entreprise/fixtures/`) le 13 octobre 2026.

## 1. La demande

> « Voilà notre site : https://www.assurly.example. Présente mon entreprise à
> Claude, une fois pour toutes. »

Aucun `entreprise.md` n'existe, une URL est donnée : mode **brouillon depuis
le site**, puis entretien sur ce qui manque.

## 2. La lecture du site

Pages lues : accueil, à propos, /mutuelle-independant/,
/prevoyance-independant/, /mentions-legales/. La page /tarifs/ est rendue en
JavaScript : elle est notée « non lue ».

Mentions légales :

```
$ python3 scripts/entreprise.py mentions mentions-legales.html
Lu sur la page :
  raison sociale               Assurly SAS
                               « … site www.assurly.example est édité par Assurly SAS, au capital social de 50 000 … »
  forme                        SAS
                               « … est édité par Assurly SAS, au capital social de 50 000 … »
  capital                      50 000 €
                               « … est édité par Assurly SAS, au capital social de 50 000 €, immatriculée au RCS de Lyon sous le … »
  SIREN                        123 456 782 (lu après le RCS)
                               « … social de 50 000 €, immatriculée au RCS de Lyon sous le numéro 123 456 782. Siège social : 10 rue de l'Exemple, … »
  SIRET                        123 456 782 00010
                               « … : 10 rue de l'Exemple, 69000 Lyon. SIRET : 123 456 782 00010 N° de TVA intracommunautaire : FR 11 … »
  RCS                          Lyon
                               « … social de 50 000 €, immatriculée au RCS de Lyon sous le numéro 123 456 782. Siège … »
  TVA                          FR 11 123 456 782
                               « … 00010 N° de TVA intracommunautaire : FR 11 123 456 782 Courtier en assurance immatriculé à … »
  siège                        10 rue de l'Exemple, 69000 Lyon
                               « … de Lyon sous le numéro 123 456 782. Siège social : 10 rue de l'Exemple, 69000 Lyon. SIRET : 123 456 782 00010 N° de TVA … »
  ORIAS                        12 345 678
                               « … en assurance immatriculé à l'ORIAS sous le n° 12 345 678 (www.orias.fr). Directrice de la … »
  directeur de la publication  Claire M., présidente
                               « … sous le n° 12 345 678 (www.orias.fr). Directrice de la publication : Claire M., présidente. Hébergement Hébergeur : Hébergeur … »
  hébergeur                    Hébergeur Exemple SAS, 1 avenue du Test, 75000 Paris
                               « … : Claire M., présidente. Hébergement Hébergeur : Hébergeur Exemple SAS, 1 avenue du Test, 75000 Paris. »
Contrôles :
  SIREN  123 456 782 : clé correcte
  SIRET  123 456 782 00010 : clé correcte
  TVA    FR11123456782 : clé correcte
  Annuaire des entreprises : https://annuaire-entreprises.data.gouv.fr/entreprise/123456782
  Activité du numéro de TVA : VIES (https://ec.europa.eu/taxation_customs/vies/)
[code 0]
```

Le script ignore le SIREN placé dans un `<script>` et celui d'un commentaire
HTML de la page de test : seuls les numéros visibles comptent.

Si l'utilisateur avait tapé son SIREN avec une faute :

```
$ python3 scripts/entreprise.py siren "123 456 789"
SIREN 123 456 789 : clé fausse
  - clé de contrôle fausse : faute de frappe probable, relis le numéro à la source
[code 2]
```

## 3. Le résumé montré avant les questions

```
J'ai lu 5 pages de assurly.example. Ce que j'ai trouvé :
- Courtier santé et prévoyance pour indépendants et TPE (accueil, à propos)
- 3 offres : mutuelle indépendant, mutuelle entreprise, prévoyance (prix sur devis)
- Assurly SAS, Lyon, SIREN 123 456 782 : clé correcte, TVA cohérente (mentions légales)
- Courtier immatriculé à l'ORIAS : secteur réglementé (assurance)
- Déduit, à confirmer : « depuis 2019 » laisse penser à une création en 2019
Non lu : /tarifs/ (rendu JavaScript)
Il me manque 6 réponses. Première question : parmi les trois offres, laquelle
se vend le plus, et à qui ?
```

## 4. L'entretien (extraits)

Une question par message. Les réponses de la gérante sont inventées pour
l'exemple.

> **Claude :** Si Assurly n'existait pas, que ferait un indépendant qui vous
> appelle aujourd'hui ?
>
> **Utilisatrice :** Honnêtement, on n'a pas vraiment de concurrent, on est
> les seuls à faire du vrai conseil.
>
> **Claude :** Avant de vous trouver, vos derniers clients faisaient comment ?
>
> **Utilisatrice :** Beaucoup n'avaient pas de prévoyance du tout. Les autres
> passaient par un comparateur, et se plaignaient des appels en série.

Signal d'alerte (« pas de concurrent ») → une relance → deux alternatives
réelles : le statu quo et les comparateurs.

> **Claude :** Pourquoi ceux qui vous choisissent vous choisissent-ils ?
> Qu'est-ce qui le prouve ?
>
> **Utilisatrice :** On a les meilleurs prix du marché.
>
> **Claude :** Comparé à quoi, mesuré comment ?
>
> **Utilisatrice :** … En vrai, on ne peut pas le prouver. Ce que les clients
> disent, c'est qu'ils ont toujours la même courtière au téléphone.

« Les meilleurs prix du marché » passe en §10 « Formulations retirées » (avec
l'accord de l'utilisatrice) ; « un courtier nommé suit le dossier » devient
un attribut, avec sa preuve (fiche CRM).

## 5. Le fichier montré, puis enregistré

Le fichier complet est `commun/modeles/exemple-entreprise.md`. Avant
l'enregistrement :

```
ENTREPRISE · Assurly · mode brouillon + entretien · 13/10/2026
Lu           5 pages (accueil, à propos, 2 offres, mentions légales) · non lu : /tarifs/ (JavaScript)
Identité     Assurly SAS, Lyon · SIREN 123 456 782 : clé correcte · TVA FR11123456782 cohérente
Offre        3 offres LIVE · 1 RETIRÉE (premier mois offert)
Différence   2 attributs prouvés · 1 superlatif retiré (« meilleurs prix du marché »)
Phrase       « Pour les indépendants qui ne veulent plus découvrir leurs garanties le jour d'un arrêt… »
Contraintes  assurance (textes à fournir) · B2B et B2C · pas de prospection email · pas de données clients dans l'IA
État         27 faits utilisables sur 35 · 6 à revoir · 4 trous (contexte.py etat)
À vérifier   date de création (Annuaire des entreprises) · catégorie réelle (avis clients) · textes du secteur
J'enregistre ce fichier dans ~/.claude/fondation/entreprise.md ?
```

Après le « oui » :

```
$ python3 commun/contexte.py etat ~/.claude/fondation/entreprise.md
templates/exemple-entreprise.md : À REVOIR
  27 faits utilisables (LIVE, datés, sourcés) sur 35 lignes
  6 à revoir · 2 retirés · 0 vides · 4 trous {{à compléter}}
  - 1. Identité › Date de création : à confirmer
  - 3. Le marché › Catégorie réelle (où les clients nous rangent) : à confirmer
  - 3. Le marché › Catégorie possible (si on la change) : à confirmer
  - 4. Les alternatives › Banque ou assureur du compte pro : à confirmer
  - 4. Les alternatives › Expert-comptable qui recommande un contrat : trou à compléter, à confirmer
  - 8. Les contraintes › Secteur réglementé (lequel, quels textes) : trou à compléter, à confirmer
[code 2]
```

Le verdict « À REVOIR » est normal pour un premier passage : il liste
exactement les 6 faits à confirmer. Un modèle vide sort « VIDE » (code 3) :
le score ne récompense jamais un fichier non rempli.

## 6. L'export, si l'utilisateur le demande

```
$ python3 commun/contexte.py exporter --vers linkedin ~/.claude/fondation/entreprise.md
<!-- Pré-remplissage depuis la Fondation (entreprise.md), le 2026-10-13. Brouillon : relis-le, complète les {{…}}, puis colle-le toi-même. -->

## Qui nous sommes

| Fait | Valeur | Étiquette | Au | Source |
|---|---|---|---|---|
| Nom | Assurly | LIVE | 13/10/2026 | entreprise.md, page d'accueil |
| Ce que nous faisons, en une phrase | Courtier en assurance santé et prévoyance pour les indépendants et les TPE en France. | LIVE | 13/10/2026 | entreprise.md, entretien avec la gérante |
| Site | https://www.assurly.example | LIVE | 13/10/2026 | entreprise.md, page d'accueil |
| Page LinkedIn | {{à compléter}} | | | |

## Offres
…
```

Rien n'est écrit : Claude montre ces sections, puis les fusionne dans
`~/.claude/linkedin/contexte.md` sur « oui », sans écraser ce qui s'y trouve.

## 7. Fin de tâche

```
À vérifier : date de création (Annuaire des entreprises) · catégorie réelle
(4 avis sur 10, à confirmer) · textes applicables à l'assurance (service
conformité) · alternative « expert-comptable » (pourquoi ces clients viennent
quand même)
Suivant : /fondation-clients, pour confirmer « pour qui cette valeur compte le
plus », qui repose aujourd'hui sur une impression de l'équipe.
```
