# Le portail qualité

`pipeline.py controler` lance les contrôles déjà écrits dans le pack et lit
chacun pour ce qu'il mesure. Il ne recalcule rien lui-même.

## Pourquoi des portes et pas une moyenne

seomachine (MIT) fait passer chaque brouillon dans une boucle de qualité :
une note composite pondérée (humanité 30%, spécificité 25%, structure 20%,
SEO 15%, lisibilité 10%), un seuil à 70, deux révisions au plus, puis un
dossier « à relire » avec les notes. L'enchaînement est bon et nous le
reprenons. La moyenne, non :

- **Une moyenne compense.** Un article bien structuré et lisible peut passer
  70 avec un chiffre inventé. En YMYL, un seul chiffre faux suffit à rendre
  l'article dangereux : la porte « Affirmations » bloque seule.
- **Ses mesures sont anglaises.** Lancé le 12 octobre 2026 sur un article
  français plein de tics (« Il est important de noter », « Dans un monde en
  constante évolution »), le correcteur de seomachine donnait 90/100 en
  humanité, conseillait des contractions anglaises et un Flesch inapplicable
  au français (`recherche/seo-v2/notes/04-seomachine.md`).

Ce que nous gardons : la boucle, le seuil, le nombre de tours limité, et la
sortie vers une relecture humaine avec la liste de ce qui reste.

## Les trois portes

### Rédaction · `controle.py` (/seo-write)

Structure (H1 unique, résumé, sections interdites), style (voix active,
modaux si le site est affirmatif), règles maison (`--remplacer`,
`--interdire`), liens internes, longueur, typographie, bloc méta en pixels.

- **OK** : verdict PRÊT.
- **À CORRIGER** : verdict À REVOIR. Les constats hauts et moyens sont
  listés ; les bas et les informations restent dans le rapport du script.

### Affirmations · `affirmations.py` (commun/)

Chaque phrase qui affirme un fait vérifiable (pourcentage, montant, délai,
date, « selon une étude », promesse) et sa source : nommée dans la phrase,
fournie par `site-context.md` (étiquette LIVE) ou `reserve.md`, ou trou
assumé.

- **OK** : aucune affirmation sans source.
- **À CORRIGER** : hors YMYL, des affirmations « à vérifier ».
- **BLOQUÉ** : en YMYL, une affirmation sans source. Il ne devient jamais
  « relecture humaine » : il se source, se reformule sans chiffre, ou devient
  un `{{à compléter : quoi, source attendue}}`.

Le contrôle est lexical : une phrase signalée qui n'affirme rien (conseil,
définition) se garde, et on le note.

### Humaniseur · `detect.py` (/seo-human, profil article)

- **BLOQUÉ** : verdict SIGNALÉ, une fuite de modèle (« En tant qu'IA »,
  balises, consignes recopiées).
- **À CORRIGER** : au moins un paragraphe à réécrire ou à alléger, désigné
  par sa ligne.
- **AVIS** : la note globale est sous le seuil (70 par défaut,
  `--seuil-humain`) mais aucun paragraphe n'est désigné. L'avis dit quel
  indicateur est bas (concret, voix, rythme) ; il ne bloque pas, parce qu'il
  ne dit pas quoi réécrire. Le faire bloquer ferait tourner la boucle à vide.
- **OK** : note au seuil ou au-dessus, rien à réécrire.

Un article YMYL plein de `{{à compléter}}` a souvent une note « concret »
basse : les trous remplacent des chiffres. C'est le prix de zéro invention,
pas un défaut d'écriture.

## Le verdict

Dans l'ordre : un BLOQUÉ donne **BLOQUÉ** ; sinon un À CORRIGER donne **À
CORRIGER** ; sinon une porte qui n'a pas tourné donne **CONTRÔLES
INCOMPLETS** ; sinon **LIVRABLE**. Les avis et les trous n'empêchent pas
LIVRABLE : ils sont listés.

Les tours : chaque `controler` avec `--dossier` ajoute un tour à
l'historique. Au tour `max_tours` (2 par défaut), un À CORRIGER ou un
CONTRÔLES INCOMPLETS devient **RELECTURE HUMAINE** : on livre avec la liste,
on ne relance pas.

## Où le portail trouve les scripts

Dans les Skills voisins : `../seo-write/scripts/controle.py`,
`../seo-write/commun/affirmations.py` (ou `commun/affirmations.py` de ce
Skill), `../seo-human/scripts/detect.py`. Ce chemin marche dans le plugin
Claude Code, dans une copie de `skills/`, et dans le ZIP claude.ai
(`modules/`). Ailleurs : `--outils <dossier qui contient seo-write/ et
seo-human/>`.
