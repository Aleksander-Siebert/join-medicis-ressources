# Profil article : ce qui change pour un article ou une page SEO

Le moteur est celui de `/linkedin-human` (quatre passes, trois niveaux,
densité par paragraphe, garde anti-sur-correction, fidélité des faits). Le
profil `article`, par défaut dans ce pack, l'adapte à un texte publié sur un
site.

## 1. Ce qui est gardé

| Élément | Profil `article` | Profil `court` |
|---|---|---|
| Titres Markdown (`#`, `##`) | gardés, hors de l'analyse de la prose | retirés |
| Gras (`**…**`) | gardé, compté seulement s'il y en a trop | retiré |
| Blocs de code (```` ``` ````) | intacts : aucune correction, aucun signalement | intacts |
| URL, heures, émojis composés | intacts | intacts |

## 2. Ce qui est signalé en plus

| Contrôle | Exemple | Piste |
|---|---|---|
| Section type d'IA | `## Conclusion`, `## Défis et perspectives`, `## Ce qu'il faut retenir` | finir sur une action ou une réponse utile |
| Intro méta | « Dans cet article, nous allons voir… » | répondre tout de suite à la question du lecteur |
| Formule de remplissage | « Sans plus attendre », « Vous l'aurez compris », « Bonne lecture » | couper |
| Fausse gamme | « Que vous soyez freelance ou dirigeant… » | parler au lecteur visé |
| Titre répété | `## Pourquoi changer de mutuelle` suivi de « Changer de mutuelle, pourquoi ? … » | commencer par la réponse |
| Voix passive avec agent | « Votre dossier est traité par nos équipes » | « Nos équipes traitent votre dossier » |
| Gras en excès | plus d'un passage en gras pour 150 mots (3 au moins) | réserver le gras aux notions clés |

## 3. Les règles du site

Elles viennent de `site-context.md` (créé par `/seo-context`) et passent
avant les règles générales :

| Option | Règle du site | Effet |
|---|---|---|
| `--affirmatif` | style affirmatif demandé | signale les verbes modaux (« peut-être », « pourrait », « il semblerait ») |
| `--remplacer "chez Marque=>à Marque"` | formulation imposée | remplacement automatique, répétable |
| `--interdire "mot"` | mot banni par le site | signalé à chaque occurrence |

## 4. Les notes d'un article

Les six signaux de `detect.py` se calculent sur la prose seule : titres,
code et gras sont retirés avant le calcul, pour qu'un article bien structuré
ne soit pas pénalisé par sa mise en forme. Un article long a plusieurs
paragraphes : la densité par paragraphe y est plus parlante que la note
globale. Corrige d'abord les paragraphes à 3 marqueurs.

## 5. Ce que l'humaniseur ne fait pas pour un article

- Il ne raccourcit pas et n'allonge pas pour atteindre une longueur : la
  longueur se décide dans le brief (`/seo-brief`).
- Il ne touche pas aux mots-clés validés dans le brief, ni aux titres H2
  validés, ni au bloc méta : il les signale au besoin.
- Il n'ajoute aucun fait : un passage vague devient `{{à compléter : …}}`
  dans la version enrichie, jamais un chiffre plausible.
- Il ne promet aucun verdict d'un détecteur tiers.
