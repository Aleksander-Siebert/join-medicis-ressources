---
name: seo-write
description: >-
  Rédige un article ou une page SEO en français à partir d'un plan validé :
  résumé de 3 lignes en tête, structure fidèle au framework (PAS, AIDA, MECE,
  pyramide inversée), règles YMYL « zéro invention », voix active, liens
  internes naturels, sources, bloc méta (title, description, slug, mots-clés),
  puis humanisation et contrôle qualité Google. Utilise-le pour « rédige
  l'article », « écris la page », après un brief validé.
---

# seo-write

Écrire pour le lecteur d'abord. Le moteur suit quand la page est la plus
utile de la SERP.

## Avant d'écrire

- Un **plan validé** est obligatoire (`/seo-brief`). Sans plan, propose de le
  faire d'abord ; ne rédige jamais « en freestyle ».
- Lis `site-context.md` : persona, ton, tutoiement, style affirmatif, règles
  maison, pages à pousser, YMYL.

## Règles de rédaction

1. **Zéro invention (YMYL strict).** Sans donnée exacte (coût, délai légal,
   plafond, condition contractuelle, statistique), n'invente pas : écris que
   cela dépend du contrat ou de la situation, renvoie vers un devis ou une
   source officielle, ou laisse `{{à compléter : source}}`.
2. **Structure.** Respecte le framework du plan, section par section, sans
   dévier ni ajouter de section non validée.
3. **Résumé en tête.** Juste après l'introduction, un résumé de **3 lignes
   maximum**, simple et compréhensible, qui dit ce que l'article explique et
   ce que le lecteur en retire. Pas une liste à puces, pas de jargon.
4. **Réponse directe.** Chaque H2 commence par une réponse en 1 à 2 phrases,
   puis le détail. C'est ce que Google et les moteurs génératifs extraient.
5. **Voix et ton.** Voix active (« Vous recevez votre attestation », pas
   « Votre attestation sera envoyée »). Si `site-context.md` demande le style
   affirmatif : aucun verbe modal (« peut-être », « pourrait », « devrait »,
   « il semblerait »).
6. **Longueur.** Celle du plan (défaut 1 000 à 1 500 mots hors bloc méta). Pas
   de remplissage pour atteindre un chiffre.
7. **Mise en forme.** Gras réservé aux notions clés, jamais à des phrases
   entières. Tableaux et listes quand ils aident vraiment.
8. **Maillage.** Les liens internes du plan, intégrés dans le texte, sans les
   annoncer (« comme expliqué dans notre article… » est interdit).
9. **Sources.** Les faits sensibles renvoient à une source précise (texte
   officiel, organisme, étude datée), jamais à « des experts ».
10. **Interdits de structure.** Pas de section « Conclusion », « En
    conclusion », « Défis », « Perspectives ». La fin est une réponse utile
    ou une action concrète.

## Après le premier jet

1. **Humanise** avec `/seo-human` en profil article (scripts si l'exécution de
   code est disponible : `--profil article`, plus `--affirmatif`,
   `--remplacer`, `--interdire` tirés de `site-context.md`). Réécris chaque
   passage signalé.
2. **Contrôle qualité** : passe la grille `references/qualite-google.md`.
   Corrige chaque « non » avant de livrer, ou signale-le clairement.

## Sortie

L'article en texte simple (Markdown pour les titres H2 et H3, rien d'autre
qui ne serve pas), puis :

```
BLOC MÉTA
Title             (55 à 60 caractères)
Meta description  (150 à 160 caractères, voix active)
Mot-clé principal
Mots-clés secondaires
Slug              /...

CONTRÔLES
Humaniseur        score 82 OK (3 passages réécrits)
Qualité Google    14/15 · reste : auteur à indiquer sous le titre
À vérifier        {{à compléter}} x 2 (plafond de remboursement, délai de carence)
```

Ne livre pas l'article avec un `{{à compléter}}` caché : liste-les toujours
dans « À vérifier ».

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : aucun chiffre, prix, délai ou condition sans source.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
