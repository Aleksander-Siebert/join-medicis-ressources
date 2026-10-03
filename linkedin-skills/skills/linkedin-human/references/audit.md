# Mode audit : relire un post avant publication

Aucune réécriture. Le mode audit rend une liste de **bloquants** (à corriger
avant de publier) et d'**avertissements** (à décider). Il réunit l'humaniseur
et le linter de `/linkedin-post`.

## Lancer

```bash
python3 scripts/detect.py post.txt --contexte ~/.claude/linkedin/contexte.md
python3 ../linkedin-post/scripts/lint_post.py --fichier post.txt     # si /linkedin-post est installé
```

Sans le linter, applique la section « Mécanique » ci-dessous à la main.

## Bloquants

| Contrôle | Règle | Source |
|---|---|---|
| Fuite de modèle | aucune (`detect.py` FORENSIQUE = 100) | niveau forensique |
| Formulation retirée | aucune de `contexte.md` | contexte de l'utilisateur |
| Longueur | 3 000 caractères au plus | officiel (aide LinkedIn) |
| Pseudo-gras Unicode | aucun (𝗴𝗿𝗮𝘀) | accessibilité : lu comme des symboles par les lecteurs d'écran |
| Appât d'engagement | aucun (« commente OUI », « like si », « tague ») | Professional Community Policies |
| Fait inventé | `fidelite.py` sans AJOUTS non justifiés ; aucun chiffre absent de `reserve.md` ou de la conversation | règle « zéro invention » |
| `{{à compléter}}` restant | aucun dans la version à publier | |
| Tiret cadratin | aucun | règle de l'utilisateur |

## Avertissements

| Contrôle | Règle |
|---|---|
| Début | une phrase complète avant ~140 caractères (le « voir plus » mobile, position observée, non publiée) |
| Ouverture | pas de question en première ligne par défaut, sauf si `apprentissages.md` montre que ça marche pour ce compte |
| Densité | aucun paragraphe à 3 marqueurs ; aucun marqueur fort |
| Rythme | ni paragraphe plat, ni staccato, 2 fragments au plus |
| Triades | une au plus, et pas creuse |
| Sincérité | aucune annonce (« Honnêtement, ») |
| Concret | au moins un chiffre avec son référent et une entité nommée |
| Lien externe | dans le premier commentaire plutôt que dans le corps (précaution : effet d'environ −19% de portée médiane selon une étude tierce, contesté, jamais confirmé par LinkedIn) |
| Hashtags | 0 à 3, en fin de post |
| Appel à l'action | un seul, en une phrase, choisi dans `contexte.md` (sujet → offre) ; beaucoup de posts n'en méritent aucun |
| Question de fin | une question que seul ce post pouvait poser ; pas « Qu'en pensez-vous ? » |
| Voix | les réactions et opinions de l'auteur ont survécu au nettoyage |
| Fait daté | si le post parle d'un échec ou d'un tournant : énoncé à plat, sans annonce |

## Écarté de la liste de contrôle

Certaines listes de praticiens ajoutent ces points ; le pack ne les reprend
pas :

- « laisser 3 à 5 commentaires sous son propre post pour lancer le fil »
  (engagement artificiel, visé par les Professional Community Policies) ;
- « commenter 15 minutes avant de publier pour chauffer l'algorithme »
  (aucune donnée publiée ; commenter est utile pour la relation, pas comme
  rituel) ;
- « ne rien modifier pendant 3 heures » (aucune donnée publiée **[à
  vérifier]**) ;
- des fourchettes de longueur imposées (aucune source ne s'accorde : la
  médiane personnelle vient de `/linkedin-audit`).

## Format de sortie

```
AUDIT AVANT PUBLICATION · {{date}}
Verdict : PRÊT | À CORRIGER ({{n}} bloquant(s)) | À DÉCIDER ({{n}} avertissement(s))

BLOQUANTS
✖ {{contrôle}} : {{ce qui ne va pas}} → {{correction}}

AVERTISSEMENTS
! {{contrôle}} : {{constat}} → {{option}}

Note humaniseur : {{note}} {{verdict}} · Caractères : {{n}}/3 000 · Début visible : « {{140 premiers caractères}} »
```

Puis propose : « Je corrige les bloquants ? » (passe en mode collé).
