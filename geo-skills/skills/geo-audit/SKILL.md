---
name: geo-audit
description: >-
  Audit GEO / AEO d'une page ou d'un site : peut-on être lu, compris et cité
  par ChatGPT, Perplexity, Gemini, Claude, Mistral et les AI Overviews de
  Google ? Score sur 100 en six catégories (citabilité, marque, E-E-A-T,
  technique, données structurées, plateformes), mesuré quand c'est mesurable,
  et plan d'action classé. Utilise-le pour « audit GEO », « audit AEO »,
  « suis-je visible dans les IA », « pourquoi ChatGPT ne me cite pas ».
---

# geo-audit

Le SEO fait apparaître une page dans une liste de liens. Le GEO (ou AEO) la
fait **citer** dans une réponse générée. Une page peut être 1re sur Google et
absente des réponses d'IA, et l'inverse.

## Les six catégories

| Catégorie | Poids | Comment on la note | Skill |
|---|---|---|---|
| Citabilité | 25% | mesurée : passages qui répondent, se comprennent seuls, chiffrés | `/geo-citability` |
| Marque et mentions | 20% | évaluée : présence sur les sources que les IA citent | `/geo-mentions` |
| E-E-A-T | 20% | évaluée : auteur, sources, expérience, fraîcheur | ce Skill |
| Technique | 15% | mesurée : robots d'IA, directives, contenu lisible sans JavaScript, llms.txt | `/geo-crawlers` |
| Données structurées | 10% | mesurée : types JSON-LD utiles | `/geo-schema` |
| Plateformes | 10% | évaluée : présence réelle dans les réponses | `/geo-visibility` |

Pondération reprise de geo-seo-claude (MIT). C'est une grille de travail,
pas une mesure officielle : aucun moteur ne publie ses critères.

## Avec exécution de code

```bash
python3 geo_audit.py https://www.site.fr/guide/
python3 geo_audit.py https://www.site.fr/guide/ --marque 40 --eeat 65 --plateformes 30
```

Le script mesure citabilité, technique et données structurées, et affiche un
**score partiel** tant que les trois autres ne sont pas évaluées. Il a besoin
des scripts de `geo-citability` et `geo-crawlers` (pack complet).

Sans exécution de code : fais les contrôles à la lecture de la page, du
robots.txt et du code source, avec les grilles des Skills cités.

## Évaluer les trois catégories qualitatives

- **E-E-A-T (0-100)** : auteur nommé avec une biographie pertinente (25) ;
  sources précises et datées (25) ; expérience de première main visible (25) ;
  date de mise à jour et contenu à jour (15) ; page « à propos » et mentions
  légales claires (10).
- **Marque (0-100)** : résultat de `/geo-mentions` (présence sur Wikipédia ou
  Wikidata, presse, comparateurs, forums, avis, YouTube, LinkedIn).
- **Plateformes (0-100)** : taux de présence de `/geo-visibility`. Sans test,
  laisse « à évaluer ».

N'invente jamais une note : une catégorie non évaluée reste « à évaluer » et
le score reste « partiel ».

## Sortie

```
AUDIT GEO · /blog/cfe-ou-premier-euro/ · 58/100 (score complet)

Citabilité 46 · Marque 30 · E-E-A-T 60 · Technique 95 · Schema 100 · Plateformes 20

PRIORITÉS
1. Citabilité : 3 sections ne répondent pas dès la première phrase → /geo-citability
2. Marque : absente des 3 comparatifs cités par Perplexity sur le sujet → /geo-mentions
3. Plateformes : citée dans 1 réponse sur 5 (ChatGPT, Perplexity) → refaire le test dans 30 jours
DÉJÀ BON : robots d'IA autorisés, schema Article + Person
```

Puis propose de suivre l'évolution : même audit et même test de visibilité
chaque mois.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent (fichier commun
  aux packs SEO et GEO).
- Zéro invention : pas de note, de citation ou de chiffre de visibilité sans
  mesure ; « à évaluer » sinon.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est modifié sur le site par le Skill.
