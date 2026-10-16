# Le mode autonome

Quand l'utilisateur dit « fais tout », « je ne serai pas là », ou lance le
pipeline sans pouvoir répondre : `pipeline.py init … --autonome`. Le
pipeline avance sans attendre de validation, et chaque décision que
l'utilisateur aurait prise devient une **hypothèse écrite**, listée au
rapport.

L'idée vient de superseo-skills (Apache 2.0, version 0.2.1 du 3 septembre
2026) : des « échappatoires pour l'exécution autonome », où le Skill avance
avec des hypothèses écrites au lieu de bloquer. Nous y ajoutons une frontière
nette entre un choix et un fait.

## Ce qui peut être supposé : des choix

| Choix | D'où le tirer, dans l'ordre | Exemple d'hypothèse écrite |
|---|---|---|
| Persona | `site-context.md`, puis la page à pousser | « persona : indépendant qui se lance, 25-40 ans (site-context.md §3, lecteur 1) » |
| Intention | la SERP (`serp.py`) | « intention commerciale : comparatifs les plus fréquents (serp.py) » |
| Type de page et cadre | le consensus de la SERP, `types-de-page.md` | « comparatif, consensus partagé à 40% (serp.py) » |
| Longueur | préférence de `site-context.md`, sinon celle des concurrents lus | « 1 000 à 1 500 mots, préférence du site » |
| Liens internes | pages à pousser de `site-context.md` | « lien vers /devis/, page à pousser » |
| Angle du gain d'information | `reserve.md` | « angle : la confusion mutuelle et prévoyance (site-context.md §9) » |
| Title | le mot-clé, la règle d'entité | « title sans marque en tête, règle du site » |

Chaque hypothèse dit **d'où elle vient**. Une hypothèse sans source (« le
lecteur est sans doute une PME ») se signale comme telle : « hypothèse sans
appui, à confirmer ».

## Ce qui ne se suppose jamais : des faits

- Un chiffre, un prix, un taux, un plafond, un délai, une date.
- Une condition contractuelle, une garantie, une exclusion.
- Une règle légale ou fiscale.
- Une citation, un témoignage, un cas client, un nom d'expert.
- Une réponse d'IA, un avis, une note.

Un fait manquant devient `{{à compléter : quoi, source attendue}}`, en mode
autonome comme ailleurs. Le portail qualité tourne avec les mêmes portes : le
mode autonome n'en baisse aucune, et un BLOQUÉ arrête la livraison.

## Ce qui arrête le mode autonome

Le pipeline s'arrête et attend l'utilisateur, même en autonome, quand :

- le garde-fou rend `REFUSÉ` (reprise d'un concurrent, faux avis, pages en
  série sans valeur) ;
- `serp.py` rend « ne pas tenter » ;
- le portail rend BLOQUÉ au dernier tour ;
- `motscles.py cannibalisation` montre qu'une page du site vise déjà la
  requête (écrire un second article la concurrencerait).

## À la livraison

`pipeline.py rapport` liste les hypothèses par étape. Elles vont dans la
sortie, sous « HYPOTHÈSES À CONFIRMER », avant les trous. L'utilisateur qui
en corrige une relance l'étape concernée (`refaire … --retour`), et les
suivantes passent en revue.
