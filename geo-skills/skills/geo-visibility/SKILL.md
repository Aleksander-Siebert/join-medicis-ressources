---
name: geo-visibility
description: >-
  Mesure la visibilité d'une marque dans les réponses de ChatGPT, Perplexity,
  Gemini, Claude, Mistral et Google AI Mode : génère 15 à 30 prompts réalistes
  en français selon les personas, l'utilisateur les pose et colle les
  réponses, puis le Skill calcule la présence, le rang, la part de voix face
  aux concurrents et les sources citées, et compare d'un mois sur l'autre.
  Utilise-le pour « est-ce que ChatGPT me recommande », « part de voix IA »,
  « visibilité dans les IA ».
---

# geo-visibility

Une seule question compte : quand un client potentiel demande conseil à une
IA, votre marque est-elle citée, et à quel rang ? On le mesure avec des
prompts réels, posés à la main : c'est gratuit et c'est ce que voit
l'utilisateur, pas ce que renvoie une API.

## 1. Générer les prompts (15 à 30)

À partir des personas, des produits et des concurrents de `site-context.md`,
des prompts **comme les écrit un vrai client**, en français :

| Type | Part | Exemple |
|---|---|---|
| Problème (sans marque) | 40% | « Je pars travailler à Dubaï avec deux enfants, quelle assurance santé ? » |
| Comparatif | 25% | « Meilleure assurance santé expatrié 2026 » |
| Alternative | 15% | « Alternative à April International pour un expatrié » |
| Marque | 10% | « Assurly est-il un bon courtier ? » |
| Expertise | 10% | « CFE ou assurance au premier euro, que choisir ? » |

Pas de prompt qui contient déjà la réponse (« Pourquoi Assurly est le
meilleur ? »).

## 2. Les poser

Dans chaque IA visée, en **nouvelle conversation**, de préférence sans être
connecté (pour limiter la personnalisation), et avec la recherche web activée
quand l'option existe. Coller chaque réponse dans un fichier :

```
=== ChatGPT | Je pars travailler à Dubaï avec deux enfants, quelle assurance santé ?
(réponse collée)
=== Perplexity | Je pars travailler à Dubaï avec deux enfants, quelle assurance santé ?
(réponse collée)
```

## 3. Mesurer

```bash
python3 visibilite.py reponses.txt --marque "Assurly" --alias "assurly.example" \
  --concurrent "April International" --concurrent "Allianz Care" --avant reponses-mois-precedent.txt
```

Sans exécution de code : compte à la lecture, prompt par prompt.

- **Présence** : % de réponses qui citent la marque.
- **Rang** : position de la 1re mention parmi les marques suivies.
- **Part de voix** : mentions de la marque / mentions de toutes les marques.
- **Sources citées** : les domaines que les IA utilisent sur le sujet. Ce sont
  les cibles de `/geo-mentions`.

## 4. Lire le résultat

- Les réponses varient d'une fois sur l'autre : 15 prompts donnent une
  tendance, pas une mesure exacte. Comparer d'un mois sur l'autre avec les
  **mêmes** prompts.
- Absent des réponses **sans** recherche web mais présent **avec** : la
  marque est peu connue des modèles, mais les pages sont bonnes
  (→ `/geo-mentions`).
- Absent dans les deux : contenu peu citable ou robots bloqués
  (→ `/geo-citability`, `/geo-crawlers`).
- Si un outil de suivi est connecté (Semrush AI Toolkit, HubSpot AEO, Ahrefs
  Brand Radar), utilise ses données et dis-le.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : ne simule jamais la réponse d'une IA ; on mesure seulement
  des réponses réellement collées.
- Texte simple dans la conversation, sans créer de document.
