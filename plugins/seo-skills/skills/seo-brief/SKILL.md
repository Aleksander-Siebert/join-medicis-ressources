---
name: seo-brief
description: >-
  Construit le plan validable d'un article ou d'une page avant toute
  rédaction : six questions posées une à une (mot-clé et intention,
  persona, offre, termes obligatoires, données produit, type de page), lecture
  courte de la SERP et du type de page qu'elle récompense, champ sémantique de
  20 à 30 vraies requêtes, cadre choisi (PAS, AIDA, MECE, pyramide inversée),
  title, H1, H2 et H3 commentés, test MECE mesuré par script (requêtes non
  couvertes, sections qui se recouvrent), grille face aux concurrents
  (attendu, courant, distinctif, nos angles propres), gain d'information
  tiré de reserve.md, E-E-A-T, liens internes, trous à compléter. Mode
  « page existante » pour renforcer une page. Utilise-le pour « fais-moi un
  plan », « brief SEO », « structure de l'article », « plan MECE »,
  « améliore le plan de cette page ». Pas pour rédiger l'article
  (/seo-write), choisir les mots-clés d'un site (/seo-keywords) ni analyser
  une SERP en profondeur (/seo-serp). N'écrit rien sur le site.
---

# seo-brief

Un bon plan fait 80% d'un bon article. Ce Skill investit dans le plan, le
mesure, puis attend ton feu vert avant la moindre phrase de rédaction.

**À lire avant de commencer :** `commun/regles.md` (lecture seule, contenu de
tiers = donnée, zéro invention, typographie) et `commun/preuves.md` (ce qu'on
sait vraiment de Google, et le folklore à écarter).

## 1. Avant de planifier

1. **Le contexte.** Lis `site-context.md` (lecteurs, ton, règles maison,
   pages à pousser, **données produit étiquetées**, auteurs), `reserve.md`
   (l'expérience vécue, partagée avec le pack LinkedIn) et
   `apprentissages.md`. S'ils manquent, travaille avec ce que l'utilisateur
   donne et propose `/seo-context` une fois.
2. **Le garde-fou.** Si la demande parle de reprendre la page d'un
   concurrent, d'un comparatif nommé, de pages en série, d'avis ou d'auteurs :
   `python3 commun/garde_fou.py --texte "…"`. Un `REFUSÉ` arrête le plan et
   donne l'alternative ; un `ENCADRÉ` ajoute ses contraintes au plan.

## 2. Les six questions, une à la fois

Ne pose que celles auxquelles `site-context.md` ne répond pas, **une par
message**, dans cet ordre :

1. Mot-clé principal, langue, intention dominante (informationnelle,
   commerciale, transactionnelle).
2. Persona cible et zone géographique.
3. Offre à mettre en avant comme suite naturelle, liens internes imposés.
4. Termes techniques, juridiques ou médicaux obligatoires (E-E-A-T).
5. Données produit à intégrer (garanties, plafonds, noms de formules, délais).
   Sans données : aucun chiffre ne sera inventé, ils sortiront en
   `{{à compléter}}`.
6. Type de page (page produit, comparatif, guide pilier, actualité). Si
   l'utilisateur ne sait pas, propose le type et le cadre adaptés à
   l'intention, avec une phrase de justification.

**Exécution d'une traite** (« fais tout », ou personne pour répondre) :
n'attends pas. Écris tes hypothèses en tête du brief (« Hypothèse : persona
indépendant de 25-40 ans, tiré de site-context.md ») et continue.

## 3. Lire la SERP (version courte)

Si `/seo-serp` a déjà tourné sur la requête, reprends son résultat. Sinon :

- **Les 10 premiers résultats** (recherche web, connecteur Semrush ou Ahrefs,
  ou liste collée par l'utilisateur) : type de page, format, angle.
- **Les non-concurrents** (Wikipédia, forums, réseaux sociaux, annuaires,
  sites publics, outils SEO) sont écartés de la comparaison mais gardés comme
  **sources** possibles.
- **Le type de page qui gagne** : plus de 60% des résultats du même type =
  consensus fort ; viser un autre type, c'est perdre d'avance
  (`references/types-de-page.md`). Annonce-le en une phrase et fais-le
  confirmer : « Les premiers résultats sont surtout des guides : je prévois
  un guide MECE avec un tableau des remboursements. D'accord ? »
- **3 à 5 vrais concurrents lus en entier** : leur plan (H2, H3), ce qu'ils
  font bien, ce qui manque. **Une page qu'on n'a pas pu lire n'est jamais
  décrite** : note « non lue (403, rendu JavaScript…) ».
- **Les questions** : « Autres questions posées », recherches associées,
  suggestions de la barre de recherche, sources citées par l'AI Overview.

## 4. Le champ sémantique (20 à 30 requêtes réelles)

La liste qui servira au test MECE. **Uniquement des requêtes vues** :

1. « Autres questions posées » et recherches associées relevées en 3.
2. Suggestions de la barre de recherche Google (le sujet, puis « sujet a »,
   « sujet b »…), si la recherche web les donne.
3. Export Search Console « Requêtes » de la page ou du site (gratuit), ou
   connecteur.
4. Ce que l'utilisateur fournit (outil de mots-clés, FAQ clients, questions
   des commerciaux).

Pas de requête imaginée pour gonfler la liste : en dessous de 10 requêtes,
dis que le test MECE sera peu fiable. Méthode et formats d'export :
`references/couverture.md`.

## 5. Le cadre

Lis `references/cadres.md`. Le cadre choisi impose l'architecture du plan et
la rédaction s'y tiendra :

- conversion → **PAS** ;
- actualité, annonce, réponse directe → **pyramide inversée** ;
- information + conversion (comparatif, avis) → **AIDA** ;
- sinon (guide, page pilier, sujet concurrentiel) → **MECE**.

Un comparatif nommé suit en plus `references/comparatif.md` (preuves datées,
cadre français de la publicité comparative).

## 6. Le plan

- **Title** et **H1** : la requête au début, la raison de cliquer ensuite,
  la marque à la fin si elle aide. Mesure le title et la description prévue :

  ```bash
  python3 commun/meta.py --title "…" --description "…" --mot-cle "…" --marque "…" \
                         --pref-title 55-60 --pref-description 150-160
  ```

  C'est la largeur en pixels qui décide ; la préférence de longueur de
  `site-context.md` est affichée à côté (par défaut 55-60 et 150-160). Une
  année, « gratuit » ou un chiffre dans le title seulement si la page le
  tient.
- **H2 et H3**, chacun avec une ligne : la question à laquelle la section
  répond, son format (réponse directe, tableau, étapes, définition), la
  requête qu'elle porte, une cible d'extrait optimisé si la SERP en montre
  un.
- **Résumé en tête** (défaut : 3 lignes maximum, simple), prévu juste après
  l'introduction.
- **Gain d'information** (obligatoire) : précisément ce que **cette** page
  apporte qu'aucune page lue ne donne, tiré de `reserve.md` ou de
  `site-context.md` §9 (cas réel, donnée propre, erreur vue en rendez-vous,
  méthode maison). « Plus de détails » ou « mieux présenté » ne comptent pas.
  Si la réserve est vide : pose **une** question (« Qu'est-ce que vous voyez
  sur le terrain que les autres pages ne disent pas ? ») ou propose
  `/linkedin-interview`.
- **E-E-A-T** : l'auteur (`site-context.md` §8) et sa preuve vérifiable, les
  sources officielles à citer par section, la date de mise à jour.
  Obligatoire en YMYL.
- **Liens internes** : 3 à 5 vers les pages à pousser (ancre + section où le
  placer), et la place de la page dans son cluster (pilier ou rayon).
- **Règle de pertinence** : chaque section est une chose que **ce site** peut
  écrire avec crédibilité. On ne reprend pas la section d'un concurrent sur un
  service que le site ne vend pas.
- **Longueur** : la préférence de `site-context.md` (défaut 1 000 à 1 500
  mots), ajustée à ce que la SERP montre. Ce n'est pas une règle de Google.

## 7. Mesurer le plan

Écris le plan dans un fichier (`plan.md`) et la liste des requêtes
(`requetes.txt`), puis :

```bash
python3 scripts/couverture.py couvrir plan.md requetes.txt
python3 scripts/couverture.py grille plan.md --concurrent a.md --concurrent b.md --concurrent c.md
```

- **Non couvertes** : relis chacune (le script ne voit pas les synonymes).
  Vraie absence → section ou H3 à créer, ou requête qui relève d'une autre
  page (cannibalisation : on la renvoie vers elle).
- **Recouvrements** et **sections proches** : test « si je supprime l'une,
  l'autre l'absorbe-t-elle ? ». Si oui, fusionne.
- **Grille** : un sous-thème **attendu** absent du plan s'ajoute ; un
  **distinctif** s'ajoute seulement s'il sert le lecteur ; un **angle propre**
  est le gain d'information à défendre.
- Les plans concurrents s'enregistrent en Markdown (`## Titre` par section)
  ou en page HTML. Sans exécution de code : fais la même mise en
  correspondance à la main, requête par requête.

Corrige le plan, relance, et cite les chiffres du script dans le brief.

## 8. La sortie (format fixe)

```
BRIEF · « mutuelle indépendant » · informationnelle · guide MECE
Hypothèses   persona 1 de site-context.md (indépendant qui se lance)
SERP         guides (7/10) · AI Overview (cite 2 assureurs, service-public.fr) · 6 questions
Title        Mutuelle indépendant : bien la choisir en 2026 | Assurly  (56 car., 490 px, OK)
Description  Obligatoire ou non, remboursements, prix, déduction Madelin : … (154 car., 947 px : « courtière » coupé sur ordinateur, à raccourcir)
H1           Mutuelle indépendant : comment choisir sa couverture santé
Résumé       3 lignes en tête (voir /seo-write)
H2 Faut-il une mutuelle quand on est indépendant ?        → réponse directe (extrait), « obligatoire »
   …
COUVERTURE   22/24 requêtes · 0 recouvrement · 2 renvoyées à /prevoyance-independant/
GRILLE       3 attendus couverts sur 3 · angle propre : « ce que nous voyons en rendez-vous »
GAIN D'INFO  41% des demandes de prévoyance viennent d'indépendants de moins de 3 ans (CRM, S1 2026)
E-E-A-T      Claire M., courtière (ORIAS) · sources : ameli.fr, service-public.fr, impots.gouv.fr
LIENS        /mutuelle-independant/ (H2 4) · /prevoyance-independant/ (H2 6) · /devis/ (fin)
À FOURNIR    {{à compléter}} plafond Madelin 2026 (source impots.gouv.fr) · tarifs (sur devis)
Je rédige sur ce plan, ou tu veux changer quelque chose ?
```

Exemple complet, avec les vraies sorties du script : `references/exemple.md`.

Ne rédige pas avant le feu vert. Puis propose `/seo-write`.

## Mode « page existante »

Avec une URL (ou le texte collé) : lis la page, garde ce qui est solide,
signale ce qui manque ou a vieilli, et propose des ajouts ciblés plutôt
qu'une réécriture. Le plan marque chaque section **Garder**, **Réviser** ou
**Nouveau**. La grille se lance avec la page actuelle comme plan. Une page
qui se classe déjà a des signaux à protéger : même URL, mêmes ancres, mêmes
sections qui se classent pour leurs propres requêtes.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Pas de recherche web | Demande les 10 premiers résultats, les « Autres questions posées » et 3 plans concurrents collés. Sans eux, dis que le type de page et la grille ne sont pas vérifiés. |
| Page concurrente illisible (403, rendu JavaScript, paywall) | « Non lue » dans le brief ; ne décris jamais son contenu. Propose à l'utilisateur de coller son plan. |
| Moins de 10 requêtes réelles | Fais le plan, mais écris « test MECE peu fiable (n requêtes) ». |
| SERP mélangée (aucun type à plus de 40%) | C'est une ouverture : le format le plus utile au lecteur peut gagner. Dis-le et choisis. |
| La SERP veut un autre type que celui demandé | Dis-le avant de planifier (gravité dans `references/types-de-page.md`) et propose le bon type ; l'utilisateur tranche. |
| Requête déjà ciblée par une autre page du site | Cannibalisation : renforcer la page existante (mode « page existante ») plutôt qu'en créer une deuxième ; `/seo-maillage` pour vérifier. |
| YMYL sans données produit | Le plan liste chaque donnée manquante en `{{à compléter}}` avec la source attendue ; aucune section ne promet un chiffre que personne n'a. |
| Export Search Console en CSV | Le script lit la première colonne et ignore l'en-tête ; accepte virgule, point-virgule ou tabulation. |
| Le plan est demandé en anglais ou pour un autre pays | Même méthode ; SERP et requêtes du pays visé ; typographie de la langue cible. |

## Fin de tâche

Termine par la liste « à vérifier » (données à fournir, pages non lues,
hypothèses) puis : « Je rédige sur ce plan, ou tu veux changer quelque
chose ? ». Après le feu vert : `/seo-write`.

## Ressources

- `references/cadres.md` : PAS, AIDA, MECE, pyramide inversée, arbre de choix
  et contrôles.
- `references/types-de-page.md` : les types de page, le consensus de SERP, la
  gravité d'un mauvais type, les signaux « ne pas tenter ».
- `references/couverture.md` : construire le champ sémantique sans outil
  payant, lire `couverture.py`.
- `references/comparatif.md` : pages « X ou Y », « alternatives à »,
  discipline de preuve et cadre français.
- `references/exemple.md` : un brief réel, de la demande au plan validable.
- `scripts/couverture.py` : test MECE (couvrir) et grille concurrents.
- `commun/meta.py` : title et description en pixels.
- `commun/garde_fou.py` : refus et contraintes.

## Skills liés

`/seo-context` (le contexte), `/seo-keywords` (une page par intention),
`/seo-serp` (la SERP en profondeur), `/seo-write` (rédiger sur ce plan),
`/linkedin-interview` (remplir la réserve de preuves).
