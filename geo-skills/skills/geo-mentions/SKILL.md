---
name: geo-mentions
description: >-
  Cartographie où la marque est mentionnée sur les sources que les IA lisent
  et citent (Wikipédia et Wikidata, presse, comparateurs, forums et Reddit,
  avis, YouTube, LinkedIn, annuaires professionnels), score la présence et
  construit un plan pour gagner des mentions légitimes, sans faux avis ni
  astroturfing. Utilise-le pour « notoriété dans les IA », « mentions de
  marque », « où les IA prennent leurs sources », « Reddit », « Wikipédia ».
---

# geo-mentions

Les modèles recommandent les marques dont **d'autres** parlent. Le contenu
du site aide à être cité comme source ; les mentions ailleurs aident à être
recommandé. Les sources les plus citées varient selon l'IA et le secteur :
on les mesure, on ne les devine pas.

## 1. Trouver les sources qui comptent

- **Les mesurer** : les « sources citées » de `/geo-visibility` disent quels
  domaines les IA utilisent sur le sujet. C'est la liste de départ.
- **Compléter par la recherche web** : « meilleur {{catégorie}} », « avis
  {{marque}} », « {{concurrent}} vs », « {{catégorie}} forum » ; noter les
  domaines qui reviennent.

## 2. Faire l'état des lieux (marque et concurrents)

| Source | À vérifier | Points |
|---|---|---|
| Wikipédia, Wikidata | article ou élément existant, exact | 15 |
| Presse et médias spécialisés | articles des 24 derniers mois | 20 |
| Comparateurs et classements | présent dans les « meilleurs… » du secteur | 20 |
| Forums, Reddit, communautés | discussions où la marque est citée, ton | 10 |
| Avis (Google, Trustpilot, sites du secteur) | volume, note, réponses | 15 |
| YouTube | vidéos de la marque ou qui en parlent | 10 |
| LinkedIn et profils d'experts | page à jour, dirigeants et experts actifs | 10 |

Le total (0-100) alimente la catégorie « Marque » de `/geo-audit`. Fais le
même tableau pour 2 ou 3 concurrents : l'écart montre où agir.

## 3. Le plan (90 jours)

Classé par effet attendu et effort :

- **Comparateurs et classements** : demander à être évalué, fournir des
  informations exactes, proposer un test du produit.
- **Presse** : une donnée propre (étude, baromètre, chiffres anonymisés de
  l'activité) vaut plus qu'un communiqué. Relations presse classiques.
- **Expertise** : interventions, podcasts, tribunes, contributions à des
  guides de référence ; les experts de l'entreprise nommés.
- **Communautés** : répondre en son nom, avec transparence, là où la question
  est posée. Une aide utile, pas une publicité.
- **Avis** : demander leur avis à tous les clients, de la même façon, sans
  contrepartie ni tri (voir `/seo-local` du pack SEO pour le droit français).
- **Wikipédia et Wikidata** : un article ne se crée que si la marque est
  admissible (sources secondaires indépendantes et de qualité). Ne pas
  l'écrire soi-même : conflit d'intérêts déclaré obligatoire. Wikidata peut
  souvent être complété plus simplement, avec des sources.
- **YouTube et LinkedIn** : contenu d'expertise régulier (voir `/seo-social`).

## Interdits

Faux avis, avis achetés ou triés, faux comptes sur les forums, messages
sponsorisés non signalés, modification de Wikipédia sans déclarer son lien
avec la marque. En France, les faux avis et les pratiques commerciales
trompeuses sont sanctionnés **[à vérifier : Code de la consommation, article
L121-1 et suivants]**, et les plateformes les suppriment.

## Sortie

```
MENTIONS · Assurly · 35/100 (April International 70, Allianz Care 80)
ABSENT DE : 3 comparatifs cités par Perplexity (liste), Wikidata
FORT SUR : avis Google (4,6, 212 avis), LinkedIn
90 JOURS : 1. comparatifs (3 contacts) · 2. étude « coût des soins à Dubaï » avec vos données · 3. réponses sur 2 forums d'expatriés
```

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : aucune mention, note ou nombre d'avis sans l'avoir vu ;
  « non vérifié » sinon.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
