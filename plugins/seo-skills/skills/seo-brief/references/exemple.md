# Exemple : du mot-clé au plan validable

> **Exemple fictif.** Assurly, ses chiffres et les plans « concurrents » sont
> inventés pour montrer la méthode. Les sorties des scripts, elles, sont
> réelles : elles viennent des fichiers de `evals/seo-brief/` du pack, lancés
> le 12 octobre 2026.

## La demande

> « Fais-moi le plan d'un article sur la mutuelle pour indépendant. »

`site-context.md` (exemple rempli du pack) répond déjà aux questions 2 à 5 :
persona 1 (indépendant qui se lance), offre `/mutuelle-independant/`, termes
obligatoires (contrat responsable, délai de carence, Madelin), données
produit étiquetées. Restent les questions 1 et 6, posées une à une :

> Q1. La requête principale est-elle « mutuelle indépendant », en français,
> pour une intention informationnelle ?
> → « Oui. »
>
> Q6. Les premiers résultats sont surtout des guides : je propose un guide
> MECE avec un tableau des remboursements. D'accord ?
> → « Oui. »

## La SERP (version courte)

Guides 7 sur 10, deux comparatifs, une page d'offre : consensus fort pour un
guide. Quatre concurrents lus en entier (plans enregistrés dans
`concurrent-a.md` à `concurrent-d.md`) ; un site public (service-public.fr)
gardé comme source, pas comme concurrent.

## Le champ sémantique

24 requêtes (`requetes-mutuelle-independant.txt`) : questions de la SERP,
suggestions de recherche, export Search Console du site. Pas une requête
inventée.

## Premier plan, première mesure

```
$ python3 scripts/couverture.py couvrir plan-mutuelle-independant.md requetes-mutuelle-independant.txt
COUVERTURE · plan-mutuelle-independant.md · 24 requêtes · 6 sections
  couvertes 15 · partielles 1 · non couvertes 8
  termes de tête (sujet de la page, ignorés pour le rattachement) : independant, mutuell

NON COUVERTES (section à créer ou à élargir, à relire : synonymes non vus)
  - mutuelle indépendant pas cher
  - meilleure mutuelle indépendant
  - mutuelle auto-entrepreneur
  - mutuelle micro-entrepreneur obligatoire
  - mutuelle indépendant famille
  - mutuelle indépendant enfants
  - mutuelle indépendant senior
  - mutuelle indépendant arrêt de travail

PARTIELLES (la section en parle, sans répondre à toute la requête)
  - mutuelle indépendant déductible impôts  →  Mutuelle Madelin : la déduction des cotisations (50%)
…
VERDICT : À REVOIR
```

Ce que le Skill en fait, requête par requête :

| Requête | Lecture | Décision |
|---|---|---|
| pas cher | synonyme de « prix » | écrire « pas chère » dans la description de la section prix |
| meilleure, comparatif | intention de comparaison | « comparatif des garanties » dans la section « Comment choisir » ; pas de classement inventé |
| auto-entrepreneur, micro-entrepreneur obligatoire | vraie absence | H3 « Micro-entrepreneur : les mêmes règles ? » |
| famille, enfants | vraie absence | H3 « Couvrir sa famille et ses enfants » |
| senior | vraie absence | H3 « Après 60 ans » |
| arrêt de travail | autre intention : la prévoyance | renvoi vers `/prevoyance-independant/` dans la section « confusion mutuelle et prévoyance » |
| déductible impôts | partielle | « cotisations déductibles des impôts » dans la description Madelin |

## La grille face aux concurrents

```
$ python3 scripts/couverture.py grille plan-mutuelle-independant.md --concurrent concurrent-a.md \
      --concurrent concurrent-b.md --concurrent concurrent-c.md --concurrent concurrent-d.md
classe      chez eux  chez nous                          sous-thème
attendu       4/4     Combien coûte une mutuelle indépen Combien coûte une mutuelle pour indépendant ?
attendu       4/4     Faut-il une mutuelle quand on est  La mutuelle est-elle obligatoire pour un indépendant ?
attendu       4/4     Mutuelle Madelin : la déduction de Mutuelle Madelin : avantages fiscaux
courant       2/4     Comment choisir sa mutuelle d'indé Comment comparer les mutuelles pour indépendants
courant       2/4     Ce que rembourse une mutuelle pour Les garanties essentielles : hospitalisation, dentaire, optique
distinctif    1/4     Comment choisir sa mutuelle d'indé Le délai de carence
distinctif    1/4     ABSENT                             Le remboursement de la Sécurité sociale pour les indépendants
distinctif    1/4     ABSENT                             Mutuelle auto-entrepreneur : les spécificités
distinctif    1/4     Ce que nous voyons en rendez-vous  Mutuelle et prévoyance : quelle différence ?
distinctif    1/4     Comment choisir sa mutuelle d'indé Résilier sa mutuelle à tout moment

ATTENDUS ABSENTS DE NOTRE PLAN (à ajouter) : aucun
NOS ANGLES PROPRES (aucun concurrent ne les traite) : Comment choisir sa mutuelle d'indépendant en 4 étapes
```

Lecture : les trois sous-thèmes attendus sont couverts. « Micro-entrepreneur »
(distinctif) entre parce que 2 requêtes le demandent. « Remboursement de la
Sécurité sociale » est déjà la réponse directe du premier H2. Le gain
d'information est la section « ce que nous voyons en rendez-vous », que
seul un concurrent effleure (« quelle différence ? ») sans cas réel.

## Plan corrigé, deuxième mesure

```
$ python3 scripts/couverture.py couvrir plan-mutuelle-independant-v2.md requetes-mutuelle-independant.txt
COUVERTURE · plan-mutuelle-independant-v2.md · 24 requêtes · 6 sections
  couvertes 24 · partielles 0 · non couvertes 0
…
VERDICT : MECE OK
```

## Le title et la description

```
$ python3 commun/meta.py --title "Mutuelle indépendant : bien la choisir en 2026 | Assurly" \
    --description "Obligatoire ou non, remboursements, prix, déduction Madelin : ce qu'un indépendant doit vérifier avant de choisir sa mutuelle, expliqué par une courtière." \
    --mot-cle "mutuelle indépendant" --marque Assurly --pref-title 55-60 --pref-description 150-160
TITLE        Mutuelle indépendant : bien la choisir en 2026 | Assurly
             56 caractères · 490 px (repère ≈ 600 px)
DESCRIPTION  Obligatoire ou non, remboursements, prix, déduction Madelin : ce qu'un indépendant doit vérifier avant de choisir sa mutuelle, expliqué par une courtière.
             154 caractères · 947 px (repères ≈ 680 px mobile, 920 px ordinateur)
  [basse] description de 947 px : coupée sur ordinateur (repère ≈ 920 px)
VERDICT : OK
```

154 caractères respectent la préférence, mais les mots larges dépassent la
largeur affichée : « courtière » sera coupé. On garde l'essentiel au début ;
la fin peut sauter.

## Le brief rendu

```
BRIEF · « mutuelle indépendant » · informationnelle · guide MECE
Hypothèses   aucune (Q1 et Q6 confirmées)
SERP         guides 7/10 · 2 comparatifs · 1 page d'offre · 4 concurrents lus · source : service-public.fr
Title        Mutuelle indépendant : bien la choisir en 2026 | Assurly  (56 car., 490 px)
Description  Obligatoire ou non, remboursements, prix, déduction Madelin : … (154 car., 947 px, fin coupée sur ordinateur)
H1           Mutuelle indépendant : comment choisir sa couverture santé en 2026
Résumé       3 lignes en tête : qui doit en prendre une, ce qu'elle rembourse, comment ne pas se tromper
H2 Faut-il une mutuelle quand on est indépendant ?       → réponse directe (cible extrait), Assurance maladie, reste à charge
   H3 Micro-entrepreneur : les mêmes règles ?
H2 Ce que rembourse une mutuelle pour indépendant        → tableau des niveaux (hospitalisation, optique, dentaire, médecine douce)
   H3 Couvrir sa famille et ses enfants
   H3 Après 60 ans
H2 Combien coûte une mutuelle indépendant                → facteurs de prix ; aucun tarif sans devis (YMYL)
H2 Mutuelle Madelin : la déduction des cotisations       → règle datée, plafond à sourcer
H2 Comment choisir sa mutuelle d'indépendant en 4 étapes → étapes numérotées, délai de carence, résiliation
H2 Ce que nous voyons en rendez-vous                     → gain d'information ; renvoi prévoyance (arrêt de travail)
COUVERTURE   24/24 requêtes · 0 recouvrement · « arrêt de travail » renvoyée à /prevoyance-independant/
GRILLE       3 attendus sur 3 couverts · angle propre : « ce que nous voyons en rendez-vous »
GAIN D'INFO  41% des demandes de prévoyance viennent d'indépendants de moins de 3 ans (CRM Assurly, S1 2026, anonymisé)
E-E-A-T      Claire M., courtière (lien vers le registre ORIAS) · sources : ameli.fr, service-public.fr, impots.gouv.fr
LIENS        /mutuelle-independant/ (H2 2, ancre « mutuelle indépendant ») · /prevoyance-independant/ (H2 6) · /devis/ (fin)
À FOURNIR    {{à compléter}} plafond Madelin 2026 (impots.gouv.fr) · niveaux de remboursement des formules (conditions générales)
Je rédige sur ce plan, ou tu veux changer quelque chose ?
```

Puis, après le feu vert : `/seo-write`.
