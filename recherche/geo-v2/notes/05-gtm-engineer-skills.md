# gtm-engineer-skills (onvoyage-ai)

MIT, 1,3k étoiles, commit cfdb9ed du 11 oct. 2026. 75 fichiers,
12 Skills : `audit-website-aeo` (script Node de 1 020 lignes,
`aeo-audit.mjs`), `improve-aeo-geo` (560 lignes, exemples avant/après
Next.js et WordPress), `geo-content-research` (584 lignes,
`prompts.csv`), `geo-content-planning` (`plan.csv`),
`write-seo-geo-content`, `research-keywords` (2 scripts Node),
`create-geo-charts` (graphiques HTML), `reddit-opportunity-research`,
`build-backlinks`, `build-resource-pages`, `research-brand`,
`audit-content`. Tests : `evals/` (7 tests Node, tous réussis après
lancement correct, fixtures d'un faux site, contrats CSV validés).

## Ce qui est bien pensé

- **Deux notes séparées** dans l'audit :
  - une **note déterministe** calculée par le script (16 contrôles,
    142 points, contrôle validé si 80% des pages le passent), « finale,
    ne pas la modifier » ;
  - une **note de jugement** sur 6 dimensions de 0 à 5 (réponse,
    extractibilité, preuves, profondeur, fraîcheur, structure), notée
    par le modèle « seulement sur ce qu'il a lu », avec une justification
    et un constat par dimension.

  C'est notre règle « séparer ce qui se mesure de ce qui se juge »,
  appliquée.
- « Si le script échoue, le dire et s'arrêter, ne pas inventer une
  note. »
- **Contrats de fichiers** (`prompts.csv`, `keywords.csv`, `plan.csv`)
  avec schéma et validateur testé : les Skills s'enchaînent par des
  fichiers vérifiés.
- 8 familles de prompts (définition, recommandation, comparaison,
  confiance, mode d'emploi, coût, paysage, cas d'usage).

## Ce qui est fragile

- **Multiplicateurs sans source vérifiable** dans les grilles : « réponse
  en premier paragraphe = 4,8 fois plus de citations », « tableaux
  2,8 fois », « FAQ +156% », « citations dans le texte +115% »,
  « 2 000 mots = 3 fois », « 76% des pages les plus citées par ChatGPT
  mises à jour en 30 jours » (Ahrefs), « 44,2% des citations dans les
  premiers 30% du contenu » (Kevin Indig). Tous **[à vérifier]**.
- Points pour `llms.txt` (10/142), un flux RSS (8), Open Graph (8),
  « 250 mots minimum » : sans fondement Google.
- « Plan d'infiltration d'autorité » sur Quora et Reddit : glisse vers
  l'astroturfing. Écarté.
- Gabarit unique « bloc de réponse de 40 à 60 mots, tableau, données,
  FAQ » pour chaque page : contraire au guide Google (pas de découpage
  ni de réécriture pour l'IA).

## Verdict

À reprendre : la **double note** (déterministe figée, jugement par
grille courte avec justification), l'arrêt sans note quand le script
échoue, les contrats de fichiers testés entre Skills. À écarter : les
multiplicateurs, les points llms.txt et RSS, l'« infiltration ».
