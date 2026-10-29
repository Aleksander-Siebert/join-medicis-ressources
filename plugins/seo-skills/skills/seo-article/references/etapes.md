# Les étapes du pipeline

Chaque étape a une entrée, une sortie et une question de validation. L'ordre
est fixe ; une étape refaite renvoie en revue les étapes suivantes déjà
faites (« à revoir »), jamais les précédentes.

L'idée des étapes nommées, montrées et rejouables une à une vient du pipeline
d'article d'Agent A (Ahrefs, article du 20 mai 2026) ; l'enchaînement
rédaction, contrôles et boucle de qualité, de seomachine (MIT). Les deux sont
réécrits ici avec nos règles : zéro invention, YMYL, français.

## Les statuts

| Statut | Sens | Ce qui le produit |
|---|---|---|
| à faire | pas commencée | `init` |
| à valider | produite, en attente du feu vert | `fait` |
| validé | acceptée | `valider`, ou `fait` en mode autonome |
| passée | résultat fourni par l'utilisateur | `passer` (mots-clés, SERP, maillage) |
| à refaire | l'utilisateur a demandé une correction | `refaire --retour` |
| à revoir | une étape d'avant a changé | `refaire` ou `fait` d'une étape précédente |

Une étape « à revoir » n'est pas forcément à réécrire en entier : regarde ce
que le changement touche (une section du plan → la section de l'article), et
dis ce qui est gardé.

## cadrage

- **Entrée** : la demande, `site-context.md`, `apprentissages.md`.
- **Fait** : les 6 questions de `/seo-brief` §2, une par message, en sautant
  celles auxquelles `site-context.md` répond déjà. Le garde-fou si la
  demande touche à des avis, un comparatif nommé, des auteurs ou des pages en
  série (`commun/garde_fou.py`).
- **Sortie** : 6 réponses (ou hypothèses), le drapeau YMYL.
- **Question** : « Voici le cadrage : … On part là-dessus ? »
- **L'invalide** : un changement de persona, d'offre ou de zone.

## mots-cles

- **Entrée** : le cadrage.
- **Fait** : `/seo-keywords`, version courte. Mot-clé principal, 3 à 6
  secondaires, intention dominante. Avec l'export Search Console du site :
  `motscles.py cannibalisation` pour vérifier qu'aucune page ne vise déjà la
  requête.
- **Sortie** : mot-clé principal, secondaires, intention, alerte de
  cannibalisation s'il y en a une.
- **Passer** : l'utilisateur impose le mot-clé et connaît l'intention.
- **L'invalide** : un changement de sujet ou d'intention.

## serp

- **Entrée** : le mot-clé principal.
- **Fait** : `/seo-serp` (`serp.py`) : consensus de type de page, difficulté
  lue dans la SERP, signaux « ne pas tenter », manques des concurrents lus
  en entier.
- **Sortie** : le type de page qui gagne, 3 à 5 manques, le gain
  d'information prévu (tiré de `reserve.md`).
- **Passer** : SERP déjà analysée et collée par l'utilisateur.
- **Arrêt** : « ne pas tenter » rendu par `serp.py`. Le dire, proposer une
  autre requête ; ne pas continuer sans accord.

## plan

- **Entrée** : cadrage, mots-clés, SERP.
- **Fait** : `/seo-brief` en entier : cadre (PAS, AIDA, MECE, pyramide
  inversée), title, H1, H2 et H3 commentés, champ sémantique, test MECE
  (`couverture.py`), liens internes, trous prévus.
- **Sortie** : `plan.md`.
- **Ne se passe jamais.** Un plan fourni par l'utilisateur s'enregistre avec
  `fait plan --fichier`, puis se vérifie (cadre, H2 commentés, requêtes).
- **L'invalide** : une section ajoutée, retirée ou déplacée, un autre cadre.

## redaction

- **Entrée** : le plan validé, `site-context.md`, `reserve.md`.
- **Fait** : `/seo-write` §1 et §2, section par section, sans section
  ajoutée.
- **Sortie** : `article.md` avec le bloc méta à la fin.
- **Ne se passe jamais.**

## controles

- **Entrée** : `article.md`.
- **Fait** : `pipeline.py controler` (voir `portail.md`). Chaque lancement
  compte un tour.
- **Sortie** : le bloc « Contrôles », l'historique des tours.
- Le statut suit le verdict : LIVRABLE → « à valider » (ou « validé » en
  autonome) ; sinon « à refaire ».

## maillage

- **Entrée** : l'article contrôlé, le sitemap du site.
- **Fait** : `/seo-maillage` en mode nouvel article
  (`maillage.py --sitemap … --lire --cible article.md`) : les 3 pages hôtes
  les plus proches, avec l'ancre et la phrase où placer le lien.
- **Sortie** : liens entrants proposés, à poser par l'utilisateur.
- **Passer** : site sans sitemap accessible, ou maillage fait à la main.
  Le dire dans la livraison : un article sans lien entrant est une page
  orpheline.

## livraison

- **Entrée** : tout ce qui précède.
- **Fait** : `pipeline.py rapport`, puis la sortie au format fixe
  (SKILL.md §5).
- **Ne se passe jamais.** Rien n'est publié : l'utilisateur publie.
