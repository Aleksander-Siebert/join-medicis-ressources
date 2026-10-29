---
name: geo-audit
description: >-
  Diagnostic GEO d'une page, couche par couche, dans l'ordre où un moteur de
  réponse la rencontre : accès (robots.txt selon la RFC 9309, Googlebot et
  robots de recherche des IA, indexable, extrait autorisé, pare-feu), page
  (texte sans JavaScript, canonical, H1, date), contenu (réponse en tête,
  statistiques sourcées, promesses, première main), entité (nom, JSON-LD,
  sameAs) et agents (noms, labels, consignes cachées aux IA). Note de
  préparation sur 100 détaillée contrôle par contrôle, avec preuve et page
  Google, sans les contrôles non mesurés ; visibilité réelle à part, jamais
  additionnée ; couche à traiter d'abord ; journal avant et après. Utilise-le
  pour « audit GEO », « audit AEO », « suis-je prêt pour les IA », « par où
  commencer ». Pas pour mesurer la présence dans les réponses
  (/geo-visibilite) ni réécrire (/geo-contenu).
---

# geo-audit

Un moteur de réponse rencontre une page dans un ordre fixe : il doit pouvoir
la **lire**, puis la **comprendre**, puis savoir **qui parle**. Un échec à
une couche ne se rattrape pas à une autre : réécrire une page que Googlebot
ne peut pas lire ne sert à rien. Ce Skill fait le diagnostic dans cet ordre
et dit par quelle couche commencer.

Google le dit d'abord : les Aperçus IA et le Mode IA reposent sur la
recherche classique, sans optimisation spéciale. La plupart des contrôles
ci-dessous sont donc du bon SEO, appliqué aux moteurs de réponse.

**À lire avant de commencer :** `commun/regles.md` et `commun/preuves.md`.

## 1. Lancer l'audit

```bash
python3 scripts/audit.py https://www.site.fr/page/ --marque "Assurly"
python3 scripts/audit.py https://www.site.fr/page/ --marque "Assurly" --question "Combien coûte une mutuelle pour indépendant ?" --sonder --mesure mesure.json
python3 scripts/audit.py page.html --url https://www.site.fr/page/ --robots robots.txt --marque "Assurly"
```

- `--question` : la question visée (familles de faits, sans points).
- `--sonder` : appelle la page avec le user-agent des robots (pare-feu).
- `--mesure` : la sortie JSON de `/geo-visibilite`, affichée à part.
- `--journal journal-geo.csv` : ajoute la note et les contrôles manqués,
  pour comparer avant et après (seul fichier écrit, et seulement sur
  demande).

Le script appelle ceux de `/geo-acces`, `/geo-contenu`, `/geo-entite` et
`/geo-agentic` : il faut le pack complet. Un Skill absent rend ses
contrôles « non mesurés », hors calcul.

Sans exécution de code : suivre les couches à la main avec les SKILL.md de
ces Skills, et écrire « lecture manuelle » en tête.

## 2. La note de préparation

Vingt-quatre contrôles, cent points au total, chacun avec ses points, sa
preuve (ce que le script a lu) et sa source (page Google ou table datée du
pack). Détail et justification : `references/diagnostic.md`.

| Couche | Points | Contrôles |
|---|---|---|
| Accès | 35 | robots.txt lisible ; Googlebot ; noindex ; extrait autorisé ; OAI-SearchBot, Bingbot, PerplexityBot, Claude-SearchBot ; pare-feu |
| Page | 15 | texte dans le HTML serveur ; canonical ; un H1 ; date |
| Contenu | 20 | réponse en tête ; statistiques sourcées ; promesses ; première main |
| Entité | 15 | nom cohérent ; Organization ; sameAs ; note et prix balisés visibles |
| Agents | 15 | noms et labels ; rien de caché ; aucune consigne cachée aux IA |

Règles :

- **Non mesuré = hors calcul**, avec sa raison (robots.txt non lu, pas de
  `--sonder`, ni note ni prix balisés). La note porte sur les points
  mesurés : « 77/100 sur 97 points mesurés ».
- **À vérifier = hors calcul** aussi : un refus du pare-feu au faux
  user-agent d'un robot doit être confirmé (le vrai robot, vérifié par son
  adresse IP, peut passer).
- **La note ne prédit rien.** Elle dit si la page est prête à être lue et
  citée. Aucun outil ne voit les signaux des moteurs ; une note ne se
  compare qu'à elle-même, sur la même page, avant et après.
- **La visibilité reste à part** : taux de `/geo-visibilite`, moteur par
  moteur, avec leur marge. Jamais additionnée à la note.

## 3. La couche à traiter d'abord

La première couche, dans l'ordre accès, page, contenu, entité, agents, qui
a un contrôle critique manqué (Googlebot, noindex, extrait, texte serveur,
consigne cachée) ou un contrôle de 4 points ou plus. Les recommandations
partent de là. Les couches suivantes sont listées, pas traitées en premier.

## 4. Ce que le script ne voit pas

À dire à chaque audit :

- le réglage « Contrôle de l'IA générative dans la Recherche » de Search
  Console : un site exclu n'apparaît ni dans les Aperçus IA ni dans le Mode
  IA ;
- l'indexation réelle (rapport « Pages », inspection de l'URL) ;
- ce que les IA disent de la marque (`/geo-exactitude`) et les sites tiers
  qui font les listes (`/geo-mentions`) ;
- la qualité de fond : une page peut passer tous les contrôles et rester
  générique. La grille de jugement de `references/diagnostic.md` (§4)
  s'applique à la lecture, notée à part.

## 5. La sortie (format fixe)

```
AUDIT GEO · https://assurly.example/mutuelle-independant/ · 2026-10-16
PRÉPARATION · 65/100 sur les contrôles mesurés (57/88 points ; 12 points non mesurés ou à vérifier, hors calcul)
  Dit si la page est prête à être lue et citée, pas si elle le sera.
  Couche à traiter d'abord : ACCÈS (corriger une couche plus basse ne compense pas celle-ci).

ACCÈS · 17/31 points
  ok     A1  robots.txt lisible                                       3 pt · lu
  MANQUÉ A2  Googlebot autorisé par robots.txt                        5 pt · groupe * · Disallow: / (ligne 9)
         → /geo-acces · source : https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=fr
  …
VISIBILITÉ (mesurée à part, jamais additionnée à la note)
  ChatGPT                  mentionnée 50% (4/8, 22-78%) · recommandée 12% (1/8, 2-47%) · citée 12% (1/8, 2-47%)
À VÉRIFIER HORS DU SITE
  · réglage « Contrôle de l'IA générative dans la Recherche » de Search Console
```

Exemple fictif (fichiers de `evals/`). Sous la sortie, en texte simple :
3 actions au plus, dans la couche à traiter d'abord, chacune avec son Skill
et son propriétaire. Après publication par l'utilisateur, relancer avec
`--journal` et comparer.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Page en 403 pour le script | Le dire ; enregistrer le HTML depuis le navigateur et relancer avec `--url` et `--robots` ; `/geo-acces --sonder`. |
| robots.txt non lu (réseau) | Contrôles d'accès « non mesurés », jamais « absent » ; demander le fichier. |
| Site de plus de 500 pages | Auditer un gabarit par type (accueil, offre, article, catégorie), pas toutes les pages. |
| Pack incomplet | Les contrôles du Skill absent sont « non mesurés » ; le dire. |
| L'utilisateur veut une note « GEO » unique avec la visibilité | Refuser le mélange : préparation et visibilité ne se mesurent pas pareil ; donner les deux côte à côte. |
| Note qui baisse après une correction | Lire les contrôles : un contrôle « non mesuré » devenu mesuré change le dénominateur ; comparer contrôle par contrôle. |

## Ressources

- `scripts/audit.py` · scripts de `/geo-acces`, `/geo-contenu`,
  `/geo-entite`, `/geo-agentic` · `commun/page.py`
- `references/diagnostic.md` : les 24 contrôles, leurs points et leurs
  sources, la couche à traiter d'abord, le journal, la grille de jugement.

## Skills liés

Tous les Skills du pack ; `/seo-audit` (technique et indexation, pack SEO).

## Règles du pack

- Lecture seule : rien n'est modifié sur le site.
- Zéro invention : un contrôle non mesuré n'a pas de note, une donnée
  manquante devient `{{à compléter}}`.
- Texte simple dans la conversation ; le journal n'est écrit que sur
  demande.
