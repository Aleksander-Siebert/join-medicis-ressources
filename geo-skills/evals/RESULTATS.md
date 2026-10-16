# Comparaison avec les Skills GEO publics (16 octobre 2026)

Pas de note sur 100 : une note ne dit pas **sur quoi** un outil a raison.
Ici, chaque outil passe **les mêmes cas, dont la bonne réponse est connue
d'avance**, et chaque tableau dit, cas par cas, qui répond juste (✅), qui
se trompe (❌), qui ne donne pas de verdict (· ou —), et ce que l'outil a
affiché. Les sorties brutes de chaque outil sont dans
[`banc/sorties/`](banc/sorties/).

## En bref

| Banc | Question posée | Join Médicis | Meilleur autre outil | Écart le plus net |
|---|---|---|---|---|
| 1. robots.txt pièges (9 cas × 4 robots) | ce robot peut-il lire cette page ? | 36/36 (32/36 au premier passage) | elmo 36/36 | sur un robots.txt en 503, 5 outils sur 6 ne concluent pas « tout interdit » ; 2 disent même tout autorisé |
| 2. Exactitude (10 réponses, FR et EN) | faut-il signaler une erreur sur la marque ? | FR 10/10 · EN 10/10 (EN 8/10 au premier passage) | ultimate-seo-geo : FR 5/10 · EN 10/10 | « 45 € » (symbole après le nombre) n'est pas lu par ultimate-seo-geo |
| 3. Lecture d'une réponse (10 réponses, FR et EN) | mentionnée, recommandée, déconseillée ? | FR 30/30 · EN 30/30 (29/30 et 26/30 au premier passage) | geo-optimizer : FR 25/30 · EN 24/30 | lu sur toute la réponse, « Avoid Alan. I recommend Assurly » devient une mise en garde contre Assurly |
| 4. Pièges de page (6 pages) | H1 animé, consignes cachées, sous-type d'Organization, nom incohérent, note invisible | 6/6 | geo-optimizer 3/6 | le H1 animé lu en double ; la note balisée invisible récompensée |
| 5. Fait ou folklore (6 idées reçues × 10 dépôts) | le dépôt affirme-t-il l'idée reçue ? | n'en affirme aucune (test d'intégrité) | claude-seo, Profound, geo-score, elmo : aucune relevée | 6 dépôts affirment une longueur de passage ou un gain chiffré sans source primaire |

Ce que ce banc ne dit pas :

- **Les cas sont écrits par nous**, pour le marché français. Plusieurs
  viennent des CHANGELOG des autres dépôts (leurs propres bugs), mais un
  banc écrit par l'un des concurrents n'est pas neutre. Il est publié pour
  être refait et contesté.
- **Les seconds passages ne sont plus des mesures indépendantes** : nos
  scripts ont été corrigés sur ces cas. Le premier passage, avant
  correction, est donné à chaque fois ; c'est lui qu'il faut retenir pour
  juger la v2 « à froid ».
- Les outils font beaucoup d'autres choses que ces bancs ne testent pas
  (§7).

## 1. Méthode

- **Dépôts, commit et date** : geo-optimizer-skill 19e69a6 (16 oct.),
  ultimate-seo-geo c92fdba (1er oct.), elmo 9612d98 (15 oct.), geo-score
  65bf9ee (15 oct.), geo-seo-claude 989cae0 (5 oct.), gtm-engineer-skills
  cfdb9ed (11 oct.), claude-seo 4b99de2 (5 oct.), marketingskills 365b412
  (15 oct.), Profound skills-marketing-library 80293f1 (31 août),
  aaron-marketing-skills 7975010 (16 oct.).
- **Même site pour tous** : un serveur local par cas
  ([`banc/serveur.py`](banc/serveur.py)) sert le robots.txt et la page du
  cas, avec le statut voulu (200, 404, 503, connexion coupée).
- **Garde anti-SSRF** : geo-optimizer et ultimate-seo-geo refusent les
  adresses locales, à juste titre en usage normal. Pour qu'ils lisent le
  même site, [`banc/lanceur.py`](banc/lanceur.py) remplace leur seule
  fonction de garde ; rien d'autre n'est modifié.
- **Lecture des sorties** : un adaptateur par outil traduit sa sortie JSON
  en « autorisé », « bloqué », « non lu » (bancs 1 à 3). Une réponse
  partielle (« partiel », « renvoie à * ») compte « sans verdict », pas
  « faux ». Au banc 4, les verdicts sont relevés à la main dans les
  sorties brutes et cités.
- **Outils sans script pour la question** (marketingskills, Profound :
  instructions seules ; claude-seo pour les robots) : absents du banc
  concerné, présents au banc 5.

## 2. Banc robots.txt : ce robot peut-il lire cette page ?

Vérité : RFC 9309 (règle la plus longue, Allow à égalité, groupe propre
qui remplace `*`, 4xx tout permis, 5xx tout interdit) et pages des
éditeurs. Cas : [`banc/cas_robots.json`](banc/cas_robots.json).

| Outil | Justes | Faux | Sans verdict |
|---|---|---|---|
| Join Médicis | 36/36 | 0 | 0 |
| geo-optimizer | 24/36 | 8 | 4 |
| ultimate-seo-geo | 12/36 | 4 | 20 |
| elmo | 36/36 | 0 | 0 |
| geo-score | 24/36 | 3 | 9 |
| geo-seo-claude | 20/36 | 7 | 9 |
| gtm-engineer-skills | 17/36 | 7 | 12 |

Premier passage de Join Médicis : **32/36**. `acces.py` retirait la
requête de l'URL (`/guide.pdf?v=2` lu `/guide.pdf`), donc
`Disallow: /*.pdf$` bloquait la page à tort (cas R6). Corrigé, avec un
test.

À retenir :

- **elmo** lit robots.txt aussi juste que nous sur ces 9 cas.
- **503 et connexion coupée** (R3, R9) : geo-optimizer conseille de
  « créer un robots.txt » (il le croit absent), gtm-engineer-skills dit
  tout autorisé, geo-score et geo-seo-claude disent « illisible » sans
  conclure. Pour un robot qui respecte la RFC 9309, un 503 interdit tout.
- **Allow plus long que Disallow** (R1) : geo-optimizer, ultimate-seo-geo
  et geo-seo-claude ne jugent pas la page demandée, seulement la racine.
- **Casse et groupe à plusieurs agents** (R7) : geo-seo-claude et
  gtm-engineer-skills laissent passer PerplexityBot, bloqué en minuscules.
- **ultimate-seo-geo** répond souvent « hérite des règles de * » sans
  dire si le robot passe.

#### R1 · Disallow: / puis Allow: /blog/ (règle la plus longue)

Piège : un lecteur qui applique la première règle bloque /blog/ à tort. Page : `/blog/article`.

| Robot | Vérité | Join Médicis | geo-optimizer | ultimate-seo-geo | elmo | geo-score | geo-seo-claude | gtm-engineer-skills |
|---|---|---|---|---|---|---|---|---|
| OAI-SearchBot | autorisé | ✅ autorisé | · partiel | ❌ bloqué | ✅ autorisé | ✅ autorisé | ❌ bloqué | ✅ autorisé |
| GPTBot | autorisé | ✅ autorisé | · partiel | ❌ bloqué | ✅ autorisé | — | ❌ bloqué | ✅ autorisé |
| PerplexityBot | autorisé | ✅ autorisé | · partiel | ❌ bloqué | ✅ autorisé | ✅ autorisé | ❌ bloqué | ✅ autorisé |
| Claude-SearchBot | autorisé | ✅ autorisé | · partiel | ❌ bloqué | ✅ autorisé | ✅ autorisé | — | — |

#### R2 · groupe propre pour OAI-SearchBot, tout interdit pour *

Piège : le groupe propre remplace * : OAI-SearchBot passe, GPTBot non. Page : `/`.

| Robot | Vérité | Join Médicis | geo-optimizer | ultimate-seo-geo | elmo | geo-score | geo-seo-claude | gtm-engineer-skills |
|---|---|---|---|---|---|---|---|---|
| OAI-SearchBot | autorisé | ✅ autorisé | ✅ autorisé | ✅ autorisé | ✅ autorisé | ✅ autorisé | ✅ autorisé | — |
| GPTBot | bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | — | ✅ bloqué | — |
| PerplexityBot | bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | — |
| Claude-SearchBot | bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | — | — |

#### R3 · robots.txt en erreur 503

Piège : RFC 9309 : erreur serveur = tout interdit. Page : `/`.

| Robot | Vérité | Join Médicis | geo-optimizer | ultimate-seo-geo | elmo | geo-score | geo-seo-claude | gtm-engineer-skills |
|---|---|---|---|---|---|---|---|---|
| OAI-SearchBot | bloqué | ✅ bloqué | ❌ autorisé (lu comme absent) | — | ✅ bloqué | ❌ non lu | ❌ non lu | ❌ autorisé |
| GPTBot | bloqué | ✅ bloqué | ❌ autorisé (lu comme absent) | — | ✅ bloqué | — | ❌ non lu | ❌ autorisé |
| PerplexityBot | bloqué | ✅ bloqué | ❌ autorisé (lu comme absent) | — | ✅ bloqué | ❌ non lu | ❌ non lu | ❌ autorisé |
| Claude-SearchBot | bloqué | ✅ bloqué | ❌ autorisé (lu comme absent) | — | ✅ bloqué | ❌ non lu | — | — |

#### R4 · robots.txt absent (404)

Piège : absent = tout permis. Page : `/`.

| Robot | Vérité | Join Médicis | geo-optimizer | ultimate-seo-geo | elmo | geo-score | geo-seo-claude | gtm-engineer-skills |
|---|---|---|---|---|---|---|---|---|
| OAI-SearchBot | autorisé | ✅ autorisé | ✅ autorisé (lu comme absent) | ✅ autorisé | ✅ autorisé | ✅ autorisé (absent) | ✅ autorisé | ✅ autorisé |
| GPTBot | autorisé | ✅ autorisé | ✅ autorisé (lu comme absent) | ✅ autorisé | ✅ autorisé | — | ✅ autorisé | ✅ autorisé |
| PerplexityBot | autorisé | ✅ autorisé | ✅ autorisé (lu comme absent) | ✅ autorisé | ✅ autorisé | ✅ autorisé (absent) | ✅ autorisé | ✅ autorisé |
| Claude-SearchBot | autorisé | ✅ autorisé | ✅ autorisé (lu comme absent) | ✅ autorisé | ✅ autorisé | ✅ autorisé (absent) | — | — |

#### R5 · GPTBot bloqué seul

Piège : GPTBot entraîne ; la recherche de ChatGPT passe par OAI-SearchBot, toujours autorisé. Page : `/`.

| Robot | Vérité | Join Médicis | geo-optimizer | ultimate-seo-geo | elmo | geo-score | geo-seo-claude | gtm-engineer-skills |
|---|---|---|---|---|---|---|---|---|
| OAI-SearchBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| GPTBot | bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | — | ✅ bloqué | ✅ bloqué |
| PerplexityBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| Claude-SearchBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | ✅ autorisé | — | — |

#### R6 · joker de fin : Disallow: /*.pdf$

Piège : /guide.pdf bloqué, /guide.pdf?v=2 permis. Page : `/guide.pdf?v=2`.

| Robot | Vérité | Join Médicis | geo-optimizer | ultimate-seo-geo | elmo | geo-score | geo-seo-claude | gtm-engineer-skills |
|---|---|---|---|---|---|---|---|---|
| OAI-SearchBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| GPTBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | — | ✅ autorisé | ✅ autorisé |
| PerplexityBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| Claude-SearchBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | ✅ autorisé | — | — |

#### R7 · casse du jeton et groupe à plusieurs agents

Piège : les jetons ne tiennent pas compte de la casse ; deux User-agent à la suite forment un seul groupe. Page : `/`.

| Robot | Vérité | Join Médicis | geo-optimizer | ultimate-seo-geo | elmo | geo-score | geo-seo-claude | gtm-engineer-skills |
|---|---|---|---|---|---|---|---|---|
| OAI-SearchBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| GPTBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | — | ✅ autorisé | ✅ autorisé |
| PerplexityBot | bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ❌ autorisé | ❌ autorisé |
| Claude-SearchBot | bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | — | — |

#### R8 · bloc « Cloudflare Managed content » qui bloque l'entraînement

Piège : le bloc ajouté par Cloudflare ne touche pas les robots de recherche. Page : `/`.

| Robot | Vérité | Join Médicis | geo-optimizer | ultimate-seo-geo | elmo | geo-score | geo-seo-claude | gtm-engineer-skills |
|---|---|---|---|---|---|---|---|---|
| OAI-SearchBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| GPTBot | bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | ✅ bloqué | — | ✅ bloqué | ✅ bloqué |
| PerplexityBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| Claude-SearchBot | autorisé | ✅ autorisé | ✅ autorisé | · renvoie à * | ✅ autorisé | ✅ autorisé | — | — |

#### R9 · robots.txt injoignable (connexion coupée)

Piège : une erreur réseau n'est pas un robots.txt absent : « non lu », à vérifier. Page : `/`.

| Robot | Vérité | Join Médicis | geo-optimizer | ultimate-seo-geo | elmo | geo-score | geo-seo-claude | gtm-engineer-skills |
|---|---|---|---|---|---|---|---|---|
| OAI-SearchBot | non lu ou bloqué | ✅ non lu | ❌ autorisé (lu comme absent) | — | ✅ bloqué | ✅ non lu | ✅ non lu | ❌ autorisé |
| GPTBot | non lu ou bloqué | ✅ non lu | ❌ autorisé (lu comme absent) | — | ✅ bloqué | — | ✅ non lu | ❌ autorisé |
| PerplexityBot | non lu ou bloqué | ✅ non lu | ❌ autorisé (lu comme absent) | — | ✅ bloqué | ✅ non lu | ✅ non lu | ❌ autorisé |
| Claude-SearchBot | non lu ou bloqué | ✅ non lu | ❌ autorisé (lu comme absent) | — | ✅ bloqué | ✅ non lu | — | — |

## 3. Banc exactitude : faut-il signaler une erreur sur la marque ?

Join Médicis (`exactitude.py`) contre ultimate-seo-geo
(`citation_sampling.py --facts`), le seul autre dépôt qui vérifie par
script les faits de la marque dans les réponses. Mêmes réponses, mêmes
données de référence, chacune au format de l'outil
([`banc/faits-banc.csv`](banc/faits-banc.csv),
[`banc/faits-banc-ultimate.json`](banc/faits-banc-ultimate.json)). Les cas
X5, X9 et X10 reprennent des bugs corrigés dans le CHANGELOG
d'ultimate-seo-geo.

| Outil | Français | Anglais |
|---|---|---|
| Join Médicis | 10/10 | 10/10 |
| ultimate-seo-geo | 5/10 | 10/10 |

Premier passage de Join Médicis : **FR 10/10, EN 8/10**. La négation
anglaise (« does not have a free plan ») et le pronom de reprise anglais
(« It also covers pets ») n'étaient pas lus. Corrigés : un moteur répond
parfois en anglais à une question française.

ultimate-seo-geo lit très bien l'anglais. En français, il ne voit ni
« 45 € » (il attend le symbole avant le nombre), ni « fondée en », ni
« Elle … », et prend « n'a pas de formule gratuite » pour une affirmation.

| Cas | Langue | Vérité | Join Médicis | ultimate-seo-geo |
|---|---|---|---|---|
| X1 prix faux | fr | erreur à signaler | ✅ signale (différent) | ❌ ne signale rien |
| X1 prix faux | en | erreur à signaler | ✅ signale (différent) | ✅ signale (pricing) |
| X2 prix dans une autre devise | fr | erreur à signaler | ✅ signale (devise) | ❌ ne signale rien |
| X2 prix dans une autre devise | en | erreur à signaler | ✅ signale (devise) | ✅ signale (pricing) |
| X3 prix exact | fr | rien à signaler | ✅ ne signale rien | ✅ ne signale rien |
| X3 prix exact | en | rien à signaler | ✅ ne signale rien | ✅ ne signale rien |
| X4 année de création fausse | fr | erreur à signaler | ✅ signale (différent) | ❌ ne signale rien |
| X4 année de création fausse | en | erreur à signaler | ✅ signale (différent) | ✅ signale (founding year) |
| X5 année d'un concurrent entre parenthèses | fr | rien à signaler | ✅ ne signale rien | ✅ ne signale rien |
| X5 année d'un concurrent entre parenthèses | en | rien à signaler | ✅ ne signale rien | ✅ ne signale rien |
| X6 phrase fausse niée | fr | rien à signaler | ✅ ne signale rien | ❌ signale (free plan) |
| X6 phrase fausse niée | en | rien à signaler | ✅ ne signale rien | ✅ ne signale rien |
| X7 offre terminée présentée comme actuelle | fr | erreur à signaler | ✅ signale (périmé) | ✅ signale (false claim: premier mois offert) |
| X7 offre terminée présentée comme actuelle | en | erreur à signaler | ✅ signale (périmé) | ✅ signale (false claim: first month free) |
| X8 erreur dans la phrase qui reprend la marque | fr | erreur à signaler | ✅ signale (faux) | ❌ ne signale rien |
| X8 erreur dans la phrase qui reprend la marque | en | erreur à signaler | ✅ signale (faux) | ✅ signale (false claim: covers pets) |
| X9 concurrent dont le nom contient la marque | fr | rien à signaler | ✅ ne signale rien | ✅ ne signale rien |
| X9 concurrent dont le nom contient la marque | en | rien à signaler | ✅ ne signale rien | ✅ ne signale rien |
| X10 prix d'un concurrent dans la même phrase | fr | rien à signaler | ✅ ne signale rien | ✅ ne signale rien |
| X10 prix d'un concurrent dans la même phrase | en | rien à signaler | ✅ ne signale rien | ✅ ne signale rien |

## 4. Banc lecture : mentionnée, recommandée, déconseillée ?

Join Médicis (`visibilite.py`) contre geo-optimizer (les fonctions de sa
commande `citations` : `brand_matches` et `_classify_strength`) et
ultimate-seo-geo (réponses qui nomment la marque ; recommandation et mise
en garde y sont notées à la main dans un tableur).

| Outil | Français | Anglais | Ce qu'il lit |
|---|---|---|---|
| Join Médicis | 30/30 | 30/30 | mention, recommandation, mise en garde |
| geo-optimizer | 25/30 | 24/30 | mention, recommandation, mise en garde |
| ultimate-seo-geo | 9/10 | 9/10 | mention seulement (le reste est noté à la main) |

Premier passage de Join Médicis : **FR 29/30, EN 26/30**. « Assurly évite
les délais de carence » sortait déconseillée (« évite » était dans les
mises en garde) ; les marqueurs anglais manquaient. Corrigés.

geo-optimizer lit la force de recommandation **sur toute la réponse**, pas
sur la phrase de la marque : une mise en garde contre un concurrent
devient une mise en garde contre la marque (V3), une recommandation
d'Alan devient une recommandation d'Assurly (V5). Il compte « Assurly
Pro » comme Assurly (V8). Ses marqueurs sont anglais.

| Cas | Langue | Vérité (mentionnée · recommandée · déconseillée) | Join Médicis | geo-optimizer | ultimate-seo-geo |
|---|---|---|---|---|---|
| V1 recommandation directe | fr | oui · oui · non | ✅ oui · ✅ oui · ✅ non | ✅ oui · ❌ non · ✅ non | ✅ oui · — · — |
| V1 recommandation directe | en | oui · oui · non | ✅ oui · ✅ oui · ✅ non | ✅ oui · ✅ oui · ✅ non | ✅ oui · — · — |
| V2 simple option dans une liste | fr | oui · non · non | ✅ oui · ✅ non · ✅ non | ✅ oui · ✅ non · ✅ non | ✅ oui · — · — |
| V2 simple option dans une liste | en | oui · non · non | ✅ oui · ✅ non · ✅ non | ✅ oui · ✅ non · ✅ non | ✅ oui · — · — |
| V3 mise en garde contre un concurrent | fr | oui · oui · non | ✅ oui · ✅ oui · ✅ non | ✅ oui · ❌ non · ✅ non | ✅ oui · — · — |
| V3 mise en garde contre un concurrent | en | oui · oui · non | ✅ oui · ✅ oui · ✅ non | ✅ oui · ❌ non · ❌ oui | ✅ oui · — · — |
| V4 mise en garde contre la marque | fr | oui · non · oui | ✅ oui · ✅ non · ✅ oui | ✅ oui · ✅ non · ❌ non | ✅ oui · — · — |
| V4 mise en garde contre la marque | en | oui · non · oui | ✅ oui · ✅ non · ✅ oui | ✅ oui · ✅ non · ✅ oui | ✅ oui · — · — |
| V5 recommandation d'un autre, contre la marque | fr | oui · non · non | ✅ oui · ✅ non · ✅ non | ✅ oui · ✅ non · ✅ non | ✅ oui · — · — |
| V5 recommandation d'un autre, contre la marque | en | oui · non · non | ✅ oui · ✅ non · ✅ non | ✅ oui · ❌ oui · ✅ non | ✅ oui · — · — |
| V6 verbe « éviter » qui n'est pas une mise en garde | fr | oui · non · non | ✅ oui · ✅ non · ✅ non | ✅ oui · ✅ non · ✅ non | ✅ oui · — · — |
| V6 verbe « éviter » qui n'est pas une mise en garde | en | oui · non · non | ✅ oui · ✅ non · ✅ non | ✅ oui · ✅ non · ❌ oui | ✅ oui · — · — |
| V7 domaine homonyme | fr | non · non · non | ✅ non · ✅ non · ✅ non | ✅ non · ✅ non · ✅ non | ❌ oui · — · — |
| V7 domaine homonyme | en | non · non · non | ✅ non · ✅ non · ✅ non | ✅ non · ✅ non · ✅ non | ❌ oui · — · — |
| V8 concurrent dont le nom contient la marque | fr | non · non · non | ✅ non · ✅ non · ✅ non | ❌ oui · ✅ non · ✅ non | ✅ non · — · — |
| V8 concurrent dont le nom contient la marque | en | non · non · non | ✅ non · ✅ non · ✅ non | ❌ oui · ✅ non · ✅ non | ✅ non · — · — |
| V9 recommandation niée | fr | oui · non · oui | ✅ oui · ✅ non · ✅ oui | ✅ oui · ✅ non · ❌ non | ✅ oui · — · — |
| V9 recommandation niée | en | oui · non · oui | ✅ oui · ✅ non · ✅ oui | ✅ oui · ✅ non · ✅ oui | ✅ oui · — · — |
| V10 recommandation dans une autre phrase que la marque | fr | oui · non · non | ✅ oui · ✅ non · ✅ non | ✅ oui · ✅ non · ✅ non | ✅ oui · — · — |
| V10 recommandation dans une autre phrase que la marque | en | oui · non · non | ✅ oui · ✅ non · ✅ non | ✅ oui · ❌ oui · ✅ non | ✅ oui · — · — |

## 5. Banc pièges de page

Six pages servies en local ([`banc/cas_pages.json`](banc/cas_pages.json)),
lues par chaque outil. Verdicts relevés dans les sorties brutes
([`banc/sorties/pages/`](banc/sorties/pages/)).

| Cas | Vérité | Join Médicis | geo-optimizer | geo-score | ultimate-seo-geo |
|---|---|---|---|---|---|
| P1 titre animé (texte pour lecteur d'écran + lettres `aria-hidden`) : H1 doublé ? | non, un seul `<h1>` | ✅ « 1 H1 » | ❌ lit le titre deux fois : `"h1_text": "Le courtier des indépendantsLe co…"`, et en fait un nom de marque | pas de contrôle | pas de contrôle |
| P2 consignes aux IA cachées à 4 endroits | les 4 | ✅ 4 sur 4 (texte caché, commentaire, attribut `data-*`, caractères Unicode « tag » décodés) | ❌ 2 sur 4 (texte caché, attribut) ; `"html_comment_injection_found": false`, `"invisible_unicode_found": false` | pas de contrôle | ❌ 1 sur 4 : les caractères « tag », décodés ; ses motifs sont anglais |
| P3 page qui parle de prompts, sans rien cacher | rien à signaler | ✅ rien | ✅ rien | pas de contrôle | ✅ rien |
| P4 organisation déclarée en `InsuranceAgency` | c'est une Organization | ✅ « 1 bloc » | ✅ type relevé (`"found_types": ["InsuranceAgency"]`) | ❌ « Neither Organization nor WebSite JSON-LD found » et « No sameAs declared » alors que `sameAs` est rempli | pas de contrôle |
| P5 nom « Assurly Courtage » dans le JSON-LD, « Assurly » ailleurs | à signaler | ✅ « JSON-LD Organization.name « Assurly Courtage » » | ✅ `"brand_name_consistent": false` ; mais il dit aussi « incohérent » sur P1 à P4, où le nom est cohérent (il prend « Mutuelle des indépendants », début du title, pour un nom de marque) | pas de contrôle | pas de contrôle |
| P6 note 4,8 et 1 200 avis balisés, absents du texte | à signaler (règles de Google) | ✅ « note 4.8, nombre d'avis 1200 » | ❌ rien ; la page gagne des points de schéma (8/14 contre 5/14 sans la note) | pas de contrôle | pas de contrôle |

claude-seo (`agentic_check.py`) a aussi lu les six pages : il contrôle
robots.txt, llms.txt, Markdown et les fichiers `.well-known`, pas ces
pièges.

Sur le vrai site joinmedicis.com, geo-optimizer avait signalé « un H1
doublé sur l'accueil ». C'était le cas P1 : un seul `<h1>`, un titre
animé. Nous l'avions d'abord cru ; la note d'inventaire est corrigée.

## 6. Banc fait ou folklore

Six idées reçues du GEO, cherchées dans les SKILL.md et références de
chaque dépôt (recherche par motifs, puis lecture de chaque ligne).
« Affirme » = présenté comme vrai ; « écarte » = nommé pour être réfuté ;
« · » = rien relevé (la recherche peut avoir manqué une formulation).

| Idée reçue (vérité) | geo-seo-claude | claude-seo | marketingskills `ai-seo` | Profound | geo-optimizer | gtm-engineer-skills | geo-score | elmo | ultimate-seo-geo | aaron-marketing-skills |
|---|---|---|---|---|---|---|---|---|---|---|
| GPTBot sert à la recherche de ChatGPT (faux : OAI-SearchBot) | **affirme** `skills/geo-crawlers/SKILL.md:154` « Powers ChatGPT Search » | écarte `skills/seo-geo/SKILL.md:157` | écarte `SKILL.md:449` | écarte `aeo-operator-2026/SKILL.md:267` | écarte `SKILL.md:30` | **confond** `improve-aeo-geo/SKILL.md:54` (GPTBot parmi les robots à ne jamais bloquer pour l'AEO) | écarte `reference/ai-crawlers.md:18` | · | écarte `references/ai-search-geo.md:241` | · |
| Bloquer Google-Extended retire des Aperçus IA (faux : Googlebot) | · | écarte `skills/seo-geo/SKILL.md:208` | · | · | **affirme** `references/ai-bots-list.md:193` | **confond** `improve-aeo-geo/SKILL.md:54` | · | écarte `references/evidence.md:85` | écarte `references/ai-search-geo.md:262` | · |
| Passages de 134-167 ou 40-60 mots (aucune source primaire ; Google : pas de longueur idéale) | **affirme** `skills/geo-citability/SKILL.md:17` | · | **affirme** `SKILL.md:220` | · | · | **affirme** `audit-website-aeo/SKILL.md:72` | · | écarte `SKILL.md:143` | **affirme** `references/ai-search-geo.md:61` | **affirme** `references/platforms/linkedin.md:22` |
| Gains chiffrés (+40%, +115%) présentés comme acquis (résultats d'un cadre simulé, non reproduits) | **affirme** `skills/geo-audit/SKILL.md:21` | · | **affirme** `SKILL.md:246` | · | **affirme** `references/princeton-geo-methods.md:47` | **affirme** `audit-website-aeo/SKILL.md:80` | · | écarte `SKILL.md:146` | · | · |
| Le balisage FAQPage sert l'IA (aucune source primaire ; une étude citée par elmo ne trouve aucun effet) | **affirme** `skills/geo-schema/SKILL.md:139` | · | **affirme** `SKILL.md:355` | écarte `aeo-operator-2026/SKILL.md:32` | · | **affirme** `geo-content-research/README.md:73` | · | écarte `references/evidence.md:74` | **affirme** `references/schema-types.md:54` | · |
| llms.txt est essentiel (Google ne l'utilise pas) | · | écarte `references/llmstxt-evidence.md:16` | · | écarte `aeo-operator-2026/SKILL.md:32` | **affirme** dans sa sortie : `cli/formatters.py:279` « essential for AI indexing! » | · | écarte `reference/platform-source-selection.md:100` | · | · | · |

Join Médicis : ces six idées sont écartées dans `commun/preuves.md` §7, et
un test d'intégrité ([`integrite/test_integrite.py`](integrite/test_integrite.py))
échoue si un fichier du pack en affirme une.

## 7. Ce que les autres font mieux ou en plus

- **elmo** : lecture de robots.txt aussi juste ; un fichier de preuves
  (`evidence.md`) exemplaire, qui écarte le folklore avec ses sources.
- **ultimate-seo-geo** : vérification des faits très fiable en anglais,
  faits par segment (prix entreprise contre particulier), 1 775 tests,
  analyse des journaux du serveur.
- **geo-optimizer** : 27 robots, contrôles Google reliés à leur page
  officielle, mesure des citations par API (clés de l'utilisateur), suivi
  dans le temps, serveur MCP.
- **claude-seo** : lancement de Lighthouse (catégorie Agentic Browsing) par
  PageSpeed Insights, contrôles `.well-known`.
- **geo-score** : grille publique, échantillon de pages, moteurs chinois.
- **Profound** : la meilleure méthode de diagnostic par couches, reprise
  dans `/geo-audit`.

Nos limites : pas de mesure automatique par API des moteurs (réponses
collées, ou Tavily en approximation), marqueurs surtout français, et ces
bancs ont été écrits par nous.

## 8. Sur des sites réels

- **joinmedicis.com** :
  - l'audit donne 77/100 sur 97 points mesurés ; la couche à traiter
    d'abord est le contenu : 2 sections sur 15 répondent en tête, rien de
    propre au site ;
  - le `sameAs` de l'organisation pointe vers un profil LinkedIn
    personnel ;
  - la sonde a d'abord pris une erreur réseau passagère pour un refus du
    pare-feu : bug corrigé (second essai, « non lu »).
- **Un site e-commerce de reconditionné** (14 questions, Tavily, 2
  passages, approximation) :
  - la marque est mentionnée dans 50% des réponses (13/26, intervalle
    32-68%) ;
  - sur les questions perdues, `sources.py --verifier` trouve des guides
    cités par le moteur qui ne nomment pas la marque, et des comparatifs
    qui la nomment ;
  - `agentic.py` relève 7 boutons sans nom et une version Markdown servie
    à la demande.

## 9. Refaire le banc

```bash
git clone --depth 1 https://github.com/Auriti-Labs/geo-optimizer-skill depots/geo-optimizer-skill
# … idem pour ultimate-seo-geo, elmo, geo-score, geo-seo-claude, gtm-engineer-skills, claude-seo
python3 -m venv venv && venv/bin/pip install requests beautifulsoup4 ./depots/geo-optimizer-skill
python3 evals/banc/banc_robots.py --depots depots --venv venv/bin
python3 evals/banc/banc_exactitude.py --depots depots
python3 evals/banc/banc_visibilite.py --depots depots
python3 evals/banc/banc_pages.py --depots depots --venv venv/bin
```

Tests automatiques du pack : `python3 evals/tout_tester.py`.
