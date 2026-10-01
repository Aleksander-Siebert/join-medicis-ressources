# Résultats de l'évaluation v1.0 (1er octobre 2026)

Les 8 cas de [`evals.json`](evals.json) ont été joués deux fois par Claude, chaque
fois avec un seul pack installé :

- **référence** : [linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill)
  de Jake Schincariol, le pack d'origine (en anglais), avec ses scripts ;
- **v1** : ce pack.

Les réponses complètes sont dans [`resultats-v1.0/`](resultats-v1.0/). Les
contrôles automatiques viennent de [`noter.py`](noter.py), les scores de
`detect.py` (v1).

## Contrôles automatiques

| contrôle | référence | v1 |
|---|---|---|
| Cas 1 · score humain du post | 77,3 OK | 87,4 OK |
| Cas 1 · ponctuation collée (« modèle: », « envoi? ») | **3** | 0 |
| Cas 1 · hashtags | 3 | 2 |
| Cas 3 · brouillon IA → texte final | 21,5 → 77,8 OK | 21,5 → 78,7 OK |
| Cas 4 · ouverture interdite (« Super post »…) | 0 | 0 |
| Cas 7 · URL avec `f_TPR=r3600` et `sortBy=DD` | oui | oui |
| Cas 8 · tient compte d'août | oui | oui |

## Ce que la comparaison montre

1. **La typographie française.** Le script de la référence supprime l'espace
   avant `: ? !` : son post final en garde trois fautes. La v1 n'en a aucune.
2. **L'humaniseur de la référence ne marche pas en français.** Son contrôle
   VOICE compte les contractions et pronoms anglais : aucun texte français
   n'atteint PASS, même bien écrit. Le score du cas 3 de la référence
   (77,8) vient de la réécriture faite à la main par Claude, notée ici avec
   `detect.py` v1.
3. **Le reste est proche.** Claude suit bien les deux packs : profil noté
   honnêtement (critères non vus marqués « ? »), plan d'août allégé, aucune
   ouverture interdite, aucun chiffre inventé. La v1 ajoute surtout le
   contexte français (15 août, heure de Paris, CNIL, formules en français),
   `/li-job` (absent de la référence, qui improvise) et le profil centré sur
   les réalisations chiffrées.
4. **Une faiblesse de la v1** : son post du cas 1 contenait 7 `{{à compléter}}`,
   un squelette plus qu'un post. Corrigé : au-delà de deux trous, `/li-post`
   pose d'abord la question.

## Limites de l'exercice

- Un seul passage par cas, sans répétition : les écarts de score de quelques
  points ne sont pas significatifs.
- Les agents avaient accès au fichier `evals.json`, attentes comprises. Ça
  explique sans doute que la référence connaisse `f_TPR=r3600` au cas 7 sans
  Skill dédié. La prochaine série masquera les attentes.
- Les sorties sont jugées par le même modèle qui les a produites. Le vrai test
  reste tes propres demandes et tes propres posts.

## Corrections faites après l'évaluation

Remontées par l'agent qui a joué la v1 :

- `detect.py` : « j' », « m' », « t' » n'étaient pas comptés comme pronoms (bug
  de regex) ; les textes courts (note d'invitation, commentaire) étaient
  bloqués par RYTHME et VOIX, désormais « n/a ».
- `/li-profile` : réalisations en tête de verbe (« Vendu 340 abonnements… »),
  sans « J'ai » répété que `/li-human` signalait comme anaphore ; règle de
  notation des critères non fournis ; livraison section par section.
- `/li-human` : n'ajoute un fait que s'il vient de l'utilisateur.
- `/li-dm` : objectif par défaut « une conversation » ; relance J+4 sautée
  s'il n'y a rien de nouveau.
- `/li-job` : `NOT stage` exclut aussi « early stage » ; « Paris ou à
  distance » demande deux URL.
- `/li-plan` : 15 août, et alerte si la semaine demandée est passée.
- `/li-post` : horaires par défaut quand il n'y a pas de plan.
