---
name: linkedin-audit
description: >-
  Dit ce qui marche vraiment sur un compte LinkedIn, à partir de ses propres
  données (export .xlsx des statistiques, CSV, captures), sans conclure trop
  vite : taux d'engagement défini, médiane et écart absolu médian, bandes
  (exceptionnel à très faible), top et flop 5 (script) ; motifs testés
  (formule, format, pilier, longueur, lien, appel à l'action, réponse rapide,
  jour en dernier) avec 4 filtres : 5 posts par groupe, effet de 15% au
  moins, test de permutation, faux positifs attendus, et motifs confondus
  signalés ; refus sous 10 posts ; « rien n'a survécu » est un résultat ;
  plan d'expérience chiffré avec critère d'échec écrit avant ; conversations
  et prospects avant la portée ; page et profil séparés ; leçons proposées
  pour apprentissages.md. Utilise-le pour « qu'est-ce qui marche chez moi ? »,
  « analyse mes stats LinkedIn », « les carrousels marchent-ils mieux ? ».
  Pas pour auditer le profil (/linkedin-profile) ni la page (/linkedin-entreprise).
---

# linkedin-audit

La seule source honnête de ce qui marche pour un compte, c'est ce compte.
Mais la phrase typique de l'analyse LinkedIn, « les carrousels font ×3 chez
moi », repose souvent sur quatre posts. Avec des résultats aussi dispersés,
quatre posts montrent un ×3 entre presque n'importe quels groupes. Ce Skill
décrit honnêtement, teste avant de conclure, et transforme une intuition en
expérience.

**À lire avant de commencer :** `commun/regles.md` et `commun/preuves.md`.

## 1. Les données

**Uniquement celles de l'utilisateur.** Rien n'est lu sur LinkedIn (règle 1) :
l'extraction de données est interdite (aide LinkedIn a1341387).

| Source | Comment |
|---|---|
| **Export des statistiques du profil** | Profil, section Statistiques (Analytics), « Afficher toutes les statistiques », bouton Exporter : un fichier .xlsx (aide LinkedIn a704175). `audit.py` le lit directement ; choisir la feuille avec `--feuille` |
| **Export des statistiques de la page** | Page, Statistiques, Exporter (aide LinkedIn a551206) : à auditer à part (`--voix page`) |
| **Un tableau fait à la main** | un post par ligne : date, impressions, réactions, commentaires, republications, et si possible enregistrements, envois. Modèle : `assets/modele-posts.csv` |
| **Captures** | recopier les chiffres dans le modèle |

L'export ne dit pas quelle formule, quel pilier, quel appel à l'action : le
script les reprend de `journal.md` (même date) avec `--journal`. C'est pour ça
que `/linkedin-post` y écrit une ligne par post publié.

**Page et profil ne se mélangent jamais** : deux audiences, deux
dénominateurs. Le script le signale (colonne `voix`).

## 2. Les métriques, dans l'ordre qui compte

D'après `linkedin_metrics_canon.md` (alirezarezvani, MIT) :

| Rang | Métrique | Comment |
|---|---|---|
| 1 | **conversations entrantes, prospects, opportunités** | comptées à la main dans `journal.md` (contacts, origine) ; c'est l'objectif à 90 jours |
| 2 | **taux d'engagement** | (réactions + commentaires + republications) / impressions |
| 2 | **ratio de commentaires** | commentaires / réactions : discussion ou hochement de tête |
| 2 | **enregistrements, envois** | quand l'export les donne |
| 3 | **portée relative** | impressions / abonnés (`--abonnes`) |
| - | **abonnés, impressions brutes** | vanité : ils dépendent surtout de la taille du compte |

Un post à 900 impressions et 40 commentaires a battu celui à 12 000
impressions et 6.

## 3. Décrire (script)

```
python3 scripts/audit.py decrire --fichier export.xlsx --journal ~/.claude/linkedin/journal.md \
  [--metrique engagement|commentaires_ratio|portee] [--abonnes {{n}}] [--voix profil]
```

- **Médiane et écart absolu médian**, jamais la moyenne : un post qui décolle
  fait décrire à la moyenne une courbe à laquelle aucun post n'appartient.
- **CV robuste** = 1,4826 × écart absolu médian / médiane : il sert à
  dimensionner l'expérience (section 5).
- **Bandes** : exceptionnel (au-delà de Q3 + 1,5 × écart interquartile), fort
  (Q3), typique (Q1 à Q3), faible, très faible.
- **Top 5 et flop 5** côte à côte.
- **Sous 10 posts : description seulement** (code 2). Le dire, ne rien
  conclure.

## 4. Tester les motifs (script)

```
python3 scripts/audit.py motifs --fichier export.xlsx --journal ~/.claude/linkedin/journal.md
```

Facteurs testés, dans cet ordre : formule, format, pilier, longueur, lien
dans le post, appel à l'action, réponse rapide, **jour en dernier** (c'est la
cause qu'on aimerait trouver, et presque jamais la bonne).

Un motif doit passer **4 filtres** (`references/methode.md`) :

1. au moins **5 posts dedans et 5 dehors** ;
2. un écart de médianes d'au moins **15%** ;
3. un **test de permutation** : plus grand que 90% de 2 000 tirages au hasard
   (graine fixe : mêmes données, même verdict) ;
4. le **décompte des faux positifs** : à ce seuil, 10 tests en font passer
   environ 1 par hasard.

Et le script signale les **motifs confondus** : « format texte », « réponse
rapide » et « jeudi » qui désignent les mêmes posts ne sont qu'un seul
signal, dont la cause ne se sépare qu'avec une expérience.

**« Rien n'a survécu » est le résultat le plus fréquent et un vrai
résultat.** Le dire comme tel, sans l'adoucir en demi-conclusion.

Un motif trouvé dans des posts passés reste **une hypothèse** : les carrousels
ont été faits quand il y avait de la matière structurée, sur les sujets les
mieux connus, les semaines où il y avait du temps.

## 5. Transformer un motif en expérience (script)

```
python3 scripts/audit.py experience --hypothese "{{…}}" --variable "{{…}}" \
  --cv {{CV de decrire}} --effet 0.30 --posts-semaine {{n}} --semaines-max 12
```

Le script calcule les posts par variante, les semaines, l'effet minimal
détectable dans la fenêtre, écrit le **critère d'échec avant le premier post**
et la ligne pour `apprentissages.md` (« Expériences en cours »). Protocole :
une seule variable, A et B alternés, résultat regardé à la fin seulement.

Il dira souvent que l'expérience demande plus de posts qu'un trimestre n'en
permet. **C'est la réponse honnête** : tester une variable à gros effet,
accepter un seuil plus haut, ou renoncer.

## 6. Ce qui n'est pas une preuve

- **Un post qui a décollé** : la cause la plus fréquente d'un changement de
  stratégie, et l'événement le moins informatif.
- **Ce mois-ci contre le mois dernier** : saison, actualité, croissance du
  compte et changements de LinkedIn mélangés.
- **Les chiffres de quelqu'un d'autre** : autre audience, autre dénominateur,
  souvent l'échantillon d'un éditeur.
- **Un motif cherché après coup** jusqu'à ce qu'il apparaisse.

## Sortie (format fixe)

```
AUDIT · {{n}} posts · {{période}} · {{voix}}

RÉSULTATS QUI COMPTENT
  {{conversations entrantes, prospects (journal.md) : n, d'où ils viennent}}

DESCRIPTION
  médiane {{x}} · écart absolu médian {{y}} · CV {{z}} · bandes {{…}}
  TOP 5 / FLOP 5 (avec formule, format, pilier)

CE QUE DISENT LES DONNÉES
  1. {{motif soutenu ou « rien n'a survécu »}} · n = {{a}} contre {{b}} · {{effet}} · {{confondu avec…}}
  2. …
  Hypothèses, pas conclusions : {{rappel de confusion}}

À TESTER
  {{expérience : variable, posts par variante, semaines, critère d'échec}}

ARRÊTER : {{ce qui ne marche pas, avec n}}   FAIRE PLUS : {{…}}   NE PLUS OPTIMISER : {{jour, heure si rien}}

Proposition pour apprentissages.md : {{1 à 3 lignes, n ≥ 10}}
```

Les conclusions passent à `/linkedin-plan`. Sur « oui », les lignes vont dans
`apprentissages.md` : « Ce qui marche » ou « Ce qui ne marche pas » si le
motif est soutenu et repose sur 10 posts ou plus, « Expériences en cours »
sinon. Un audit qui contredit une ligne existante propose de la retirer.

## Erreurs et cas limites

| Cas | Ce qu'on fait |
|---|---|
| Moins de 10 posts | description seule ; « relance dans six semaines » |
| L'export n'a pas de colonne reconnue | `--feuille 2, 3…` ; sinon le modèle CSV |
| Formule ou pilier absents | `--journal` ; sinon les motifs ne portent que sur format, longueur, jour |
| Un post viral écrase tout | la médiane le neutralise ; il apparaît en « exceptionnel », on le lit à part |
| Page et profil dans le même fichier | `--voix` ; deux audits |
| L'utilisateur veut un benchmark | refuser la comparaison externe ; comparer le compte à lui-même |

## Ressources

- `scripts/audit.py` : décrire, motifs, expérience ; lit .xlsx, CSV, JSON.
- `assets/modele-posts.csv` : le tableau à remplir à la main.
- `references/methode.md` : les 4 filtres, la confusion, l'arithmétique des
  expériences, sources.
- `references/exemple.md` : un audit complet de 14 posts.

## Skills liés

- `/linkedin-plan` : reprend les conclusions et l'expérience en cours.
- `/linkedin-post` : écrit la ligne de `journal.md` qui rend l'audit possible.
- `/linkedin-strategie` : si l'audit montre que l'objectif à 90 jours n'avance
  pas, c'est la stratégie qu'on revoit.
