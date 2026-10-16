# Corriger à la source

Une IA ne se corrige pas par un message : elle se corrige quand ce qu'elle
lit change. Le travail porte donc sur les pages, les profils et les
documents qui portent l'erreur.

## 1. Trouver la source probable

Pour chaque verdict grave (devise, faux, différent, périmé) :

1. **Réponse avec sources** (Perplexity, ChatGPT avec recherche, Aperçus IA,
   Copilot) : ouvre chaque lien, cherche la valeur fautive (Ctrl+F sur le
   chiffre). Note l'URL et la phrase. Si elle n'y est pas, la source n'est
   pas prouvée : écris « source non trouvée ».
2. **Sur le site de la marque**, cherche la valeur fautive :
   `site:assurly.example "45 €"` dans un moteur, les PDF (conditions,
   plaquettes), les anciennes pages d'offre toujours en ligne, les pages
   en anglais (cause fréquente des prix en dollars).
3. **Profils tiers** : comparateurs, annuaires, places de marché,
   Wikipédia et Wikidata, fiches d'avis, communiqués repris par la presse.
4. **Aucune source** : affirmation probablement issue des données
   d'entraînement. Elle peut persister jusqu'au modèle suivant.

Une source probable est une hypothèse tant qu'on n'a pas vu la phrase :
écris « probable » ou « vu sur ».

## 2. Corriger, par propriétaire

| Propriétaire | Action |
|---|---|
| Équipe du site | mettre à jour la page ; rediriger l'ancienne offre vers l'actuelle ; dater les prix (« tarif au 1er septembre 2026 ») ; une page en anglais avec la bonne devise |
| Juridique ou conformité | relire toute correction de prix, garantie ou condition avant publication (domaines sensibles) |
| Marketing | demander la correction aux profils tiers, preuve à l'appui |
| Direction | Wikipédia : ne pas modifier soi-même la page de sa propre entreprise ; proposer sur la page de discussion (règles de conflit d'intérêts de Wikipédia) |

## 3. Modèle de demande de correction (profil tiers)

```
Objet : correction d'une information sur {{nom de la marque}}

Bonjour,

La page {{URL}} indique « {{phrase fautive}} ». L'information à jour est
« {{valeur juste}} », d'après {{source primaire avec date}} : {{lien}}.

Pourriez-vous la corriger ? Je reste disponible pour toute précision.

{{prénom nom, fonction}}
```

L'utilisateur l'envoie lui-même ; le Skill ne contacte personne.

## 4. Signaler dans l'outil de l'IA

Les assistants proposent en général un retour sur une réponse (pouce,
« signaler »). Effet sur les réponses futures non documenté par les
éditeurs **[à vérifier]** : à faire en complément, jamais à la place de la
correction de la source.

## 5. Suivi

- Garder le registre du mois (`--json`) avec la date et le fichier de
  réponses.
- Le mois suivant : mêmes questions, mêmes moteurs, mêmes données de
  référence (ou leur nouvelle version datée).
- Comparer ligne à ligne : erreur disparue, persistante, nouvelle.
- Une erreur persistante sur un moteur sans recherche web est attendue :
  elle dépend du prochain modèle.
- Ne pas conclure sur une seule réponse : une réponse d'IA est un tirage.
  `/geo-visibilite` donne les taux.

## 6. Ce qu'on ne fait pas

- Publier de faux avis, de fausses mentions ou de faux articles pour
  « noyer » l'erreur : pratique commerciale trompeuse (Code de la
  consommation, L121-4) et contraire à `commun/regles.md`.
- Écrire des pages « pour l'IA » cachées aux visiteurs : `/geo-agentic`
  les détecte comme instructions cachées.
- Promettre un délai de correction.
