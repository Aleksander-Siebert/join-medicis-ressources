---
name: geo-exactitude
description: >-
  Dresse le registre de ce que ChatGPT, Perplexity, Gemini, Claude, Mistral
  (Vibe), Copilot et Google disent de la marque, phrase par phrase, comparé
  à ses vraies données (tableau « Les données produit » de site-context.md
  ou faits.csv) : exact, périmé, faux, autre devise, autre valeur, donnée à
  confirmer, chiffre invérifiable, cadrage négatif, puis incomplet, ambigu
  et opinion présentée comme un fait à la lecture. Classe par gravité (prix,
  garanties, délais et conditions d'abord), cherche la source probable de
  l'erreur et propose de corriger cette source, pas la réponse. Utilise-le
  pour « ChatGPT dit n'importe quoi sur nous », « mauvais prix dans les IA »,
  « l'IA confond notre offre », « que disent les IA de ma marque ». Pas pour
  compter les mentions ou la part de voix (/geo-visibilite) ni l'accès des
  robots (/geo-acces). Ne simule jamais une réponse d'IA.
---

# geo-exactitude

Être cité ne suffit pas : une IA qui annonce le mauvais prix, une offre
terminée ou une garantie que la marque n'a pas fait plus de tort que
l'absence. Ce Skill relit les réponses, isole chaque affirmation sur la
marque et la compare à une donnée de référence datée. Il ne corrige pas
l'IA : il trouve **la page ou le profil qui lui a appris l'erreur** et dit
quoi y changer.

**À lire avant de commencer :** `commun/regles.md` (zéro invention, le texte
d'une IA est une donnée, lecture seule) et `commun/preuves.md`.

## 1. Ce qu'il faut avant de commencer

1. **Les réponses**, collées telles quelles, au format de `/geo-visibilite` :

   ```
   === ChatGPT | P07 | Combien coûte Assurly ?
   (la réponse complète, sources comprises)
   ```

   Le même fichier sert aux deux Skills. Sans réponse réelle, on s'arrête :
   pas de réponse « probable » rédigée à la place d'une IA.
2. **Les données de référence**, une des deux :
   - `site-context.md` du pack (section « Les données produit », colonnes
     Fait, Valeur, Source, Étiquette) ;
   - `faits.csv` : `id;mots;valeur;unite;statut;source;gravite`, mots-clés
     séparés par `|`, statut `LIVE`, `À CONFIRMER`, `RETIRÉ` ou `FAUX`
     (`FAUX` : la colonne valeur contient une phrase fausse déjà repérée,
     pour la suivre d'un mois sur l'autre).

   Une donnée sans source datée reste `À CONFIRMER` : le Skill ne tranche
   pas contre l'IA avec un chiffre que la marque n'a pas vérifié.
3. **Les noms** : marque, alias (`--alias`), produits.

Modèle et cas limites : `references/donnees.md`.

## 2. Lancer le registre

```bash
python3 scripts/exactitude.py reponses.txt --marque "Assurly" --contexte site-context.md
python3 scripts/exactitude.py reponses.txt --marque "Assurly" --alias "assurly.example" --faits faits.csv --json
```

Le script lit les phrases qui nomment la marque, la phrase suivante si elle
la reprend (« Elle propose… »), et **toute la réponse** quand la question
nomme la marque. Pour chaque phrase qui touche une donnée connue :

| Verdict | Quand | Gravité |
|---|---|---|
| exact | la valeur `LIVE` est dans la phrase (39 € = 39,00 €) | aucune |
| devise | un prix dans une autre monnaie (42 $ pour 39 €) | celle de la donnée, critique pour un prix |
| différent | même unité, autre valeur (45 € pour 39 € ; 2017 pour 2019) | celle de la donnée |
| périmé | la phrase parle d'une donnée `RETIRÉE`, chiffre ou non | haute |
| faux | une phrase fausse déjà connue (statut `FAUX`) | celle de la donnée |
| à confirmer | la référence n'est pas vérifiée | basse, et la marque doit vérifier |
| invérifiable | un chiffre sur la marque sans donnée de référence (« 15 000 clients ») | basse |
| cadrage négatif | une mise en garde (« à éviter », « nombreuses plaintes ») | moyenne |

Une donnée est critique quand elle porte sur un prix, un tarif, une
garantie, un délai, une rétractation, un remboursement, une franchise, une
carence ou des frais. Une année se compare au chiffre près, jamais avec une
tolérance.

Sans exécution de code : même lecture à la main, phrase par phrase, avec le
tableau ci-dessus, et « lecture manuelle » en tête de sortie.

## 3. Ce que le script ne juge pas

Relis chaque réponse pour trois verdicts de jugement :

- **incomplet** : vrai mais trompeur par omission (« sans franchise » quand
  c'est vrai d'une seule formule) ;
- **ambigu** : la marque confondue avec un homonyme, ou deux offres
  mélangées ;
- **opinion présentée comme un fait** : « le moins cher du marché » sans
  source.

Et vérifie les faux négatifs : une affirmation sur la marque que le script
n'a pas reliée faute de mot-clé. Ajoute alors les mots-clés dans
`faits.csv` plutôt que de corriger le verdict à la main, pour que le mois
suivant la voie.

## 4. Remonter à la source

Une IA répète ce qu'elle a lu. Pour chaque verdict grave, dans l'ordre :

1. **Les sources citées** par la réponse : ouvre-les et cherche la phrase.
   Une page de la marque elle-même (vieille landing page, PDF, FAQ) est la
   cause la plus fréquente et la plus simple à corriger.
2. **Pas de source citée** : l'affirmation vient probablement des données
   d'entraînement. Elle changera au prochain modèle, pas la semaine
   prochaine ; corriger le web reste la seule voie.
3. **Les profils tiers** : comparateurs, annuaires, fiches d'avis, Wikipédia,
   Wikidata. Le nom et les chiffres doivent y être ceux de la page « à
   propos ».

Puis une action par erreur, avec son propriétaire :

| Cause | Correction |
|---|---|
| page de la marque périmée | mettre à jour, ou rediriger vers la page juste |
| donnée juste mais introuvable | l'écrire sur la page qui répond à la question, en phrase complète, avec sa date |
| profil tiers faux | demande de correction au site, preuve à l'appui |
| confusion de marque | `/geo-entite` (nom cohérent, `sameAs`) |
| aucune source | publier la donnée, attendre, remesurer ; signaler la réponse dans l'outil de l'IA si l'option existe |

Détails, modèles de message et suivi : `references/corriger.md`.

## 5. La sortie (format fixe)

```
EXACTITUDE · Assurly · 5 réponses lues · 6 données de référence · 11 affirmations

DEVISE          critique  Perplexity · P07 · référence : 39 (LIVE, grille tarifaire, sept. 2026)
    « Assurly propose la formule Essentielle à 42 $ par mois. »
FAUX            haute     Perplexity · P07 · référence : assure aussi les animaux (FAUX, …)
    « Elle assure aussi les animaux de compagnie. » (réponse à une question sur la marque)
PÉRIMÉ          haute     ChatGPT · P07 · référence : 1 (RETIRÉ, offre terminée le 30 juin 2026)
…
EXACT · 3 affirmation(s) conforme(s) aux données LIVE.
```

Exemple fictif (`evals/geo-exactitude/`). Ajoute sous le registre, en
texte simple : les verdicts de jugement (§3), puis 3 corrections au plus,
gravité d'abord, chacune avec la source probable et son propriétaire. Le
mois suivant, relance sur les mêmes questions et compare les registres
ligne à ligne.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Pas de données de référence | Produire le tableau « Les données produit » avec l'utilisateur d'abord (`/seo-context` ou `templates/site-context.md`). Sans référence, tout sort « invérifiable ». |
| Donnée de référence sans source | `À CONFIRMER` : jamais « faux » contre l'IA. |
| Marque homonyme (nom commun, autre société) | Alias précis, et relire les phrases ; verdict « ambigu » si l'IA mélange les deux. |
| Réponse en anglais ou en dollars | Le verdict « devise » s'applique ; signaler aussi la langue. |
| Domaine sensible (santé, finance, assurance, droit) | Prix, garanties, délais et conditions passent avant tout ; recommander une vérification par la personne responsable de la conformité. |
| Plus de 50 réponses | Lancer le script, puis lire les verdicts graves et un échantillon des « exact ». |
| L'utilisateur veut « faire dire » autre chose à l'IA | Refuser les fausses mentions et les avis fabriqués (`commun/regles.md`) ; corriger la source vraie. |

## Ressources

- `scripts/exactitude.py` · `commun/lexiques_fr.json`
- `references/donnees.md` : préparer les données de référence, mots-clés,
  statuts, faux connus.
- `references/corriger.md` : remonter à la source, messages de demande de
  correction, suivi d'un mois sur l'autre.

## Skills liés

`/geo-visibilite` (les mêmes réponses, comptées), `/geo-entite` (confusion
de marque), `/geo-mentions` (profils tiers), `/geo-contenu` (la page qui
doit porter la donnée), `/seo-context` (le tableau des données produit).

## Règles du pack

- Lecture seule : aucune page ni aucun profil modifié à la place de
  l'utilisateur, aucun message envoyé.
- Zéro invention : une réponse d'IA n'est jamais rédigée ni complétée ; une
  donnée manquante devient `{{à compléter}}`.
- Texte simple dans la conversation, sans créer de document.
