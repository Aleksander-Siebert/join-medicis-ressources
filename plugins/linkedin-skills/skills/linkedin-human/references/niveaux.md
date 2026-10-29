# Niveaux, règles défendables et vocabulaire daté

## Pourquoi trois niveaux

| Niveau | Contenu | Défendable ? |
|---|---|---|
| **forensique** | fuites qu'aucun humain ne produit : jetons de citation (`oaicite`, `contentReference`, `turn0search0`), `utm_source=chatgpt.com`, « En tant qu'IA », « à ma dernière mise à jour », gabarits (`[Votre nom]`, `2026-XX-XX`), phrases adressées à l'assistant (« Voici une version révisée de votre post ») ; plus les formulations retirées de `contexte.md` | non : on corrige toujours |
| **strict** | ce que les lecteurs repèrent et ce que LinkedIn pénalise : grappes de vocabulaire, mises en scène, staccato, sincérité annoncée, appâts, triades creuses | rarement : on demande à l'auteur avant de toucher à un tic qui fait partie de sa voix |
| **esthétique** | ce que l'IA fait mais que les humains font aussi : « constitue », « représente », voix passive, une triade naturelle, mots de 2023-2024 en déclin | oui : à n'appliquer que sur demande |

Pourquoi l'esthétique est à part : une triade (« Veni, vidi, vici »), une
voix passive (tout article scientifique), « représente » (tout journaliste)
ne prouvent rien. Les interdire sans distinction ferait passer de grands
auteurs pour des machines.

## Conflit entre la voix et une règle

Ordre : forensique > règles de l'utilisateur (tiret cadratin, « 15% ») >
`apprentissages.md` et posts de référence de l'auteur > strict > esthétique.

- L'auteur écrit « du coup » dans tous ses posts : garde-le (note-le dans
  `apprentissages.md`, section « Mots et tournures »).
- L'auteur met des tirets cadratins : la règle de l'utilisateur du pack (tiret
  supprimé ou virgule) s'applique quand même, sauf s'il l'a explicitement
  levée dans `apprentissages.md`.
- L'auteur ouvre souvent par une question : `/linkedin-audit` dira si ça
  marche pour lui ; d'ici là, signale-le sans le retirer.

## Vocabulaire daté

Les mots que les modèles surutilisent changent avec les générations. Wikipédia
EN (« Signs of AI writing », consulté le 2 octobre 2026) les classe ainsi :

| Période | Modèle de référence | Mots (anglais) |
|---|---|---|
| 2023 à mi-2024 | GPT-4 | additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate, interplay, key, landscape, meticulous, pivotal, underscore, tapestry, testament, valuable, vibrant |
| mi-2024 à mi-2025 | GPT-4o | align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant |
| depuis mi-2025 | GPT-5 | emphasizing, enhance, highlighting, showcasing, et les formules d'insistance sur la notoriété et les sources |

Wikipédia précise : **un mot surutilisé ne rend pas ses synonymes suspects**,
et le contexte compte (« souligner » au sens propre n'est pas un tic).

Pour le français, aucune étude datée équivalente n'a été trouvée (vérifié le
2 octobre 2026). `tics-ia.json` date donc certains marqueurs par leur
équivalent anglais, avec le champ `equivalent_en`. C'est une **inférence** :

| Marqueur français | Équivalent | Période |
|---|---|---|
| « plonger dans » | delve | 2023-2024, en déclin |
| « crucial » | crucial | 2023-2025 |
| « paysage », « tapisserie », « témoigne de », « méticuleux » | landscape, tapestry, testament, meticulous | 2023-2024 |
| « en adéquation avec », « favoriser » | align with, fostering | 2024-2025 |
| « …, soulignant / mettant en lumière », « rehausser », « sublimer » | emphasizing, highlighting, enhance, showcase | depuis 2025 |
| couche LinkedIn (« discrètement », « l'effet composé », « relisez cette phrase ») | liste anglaise de S | 2025-2026 |

Conséquence pratique : les mots de 2023-2024 se raréfient parce que les gens
les évitent ; un seul ne signale presque plus rien. Les **tics de structure**
(mises en scène, parallélismes, staccato, triades creuses, participe de fin de
phrase) durent : ce sont eux qui pèsent le plus.

## Ce qui ne marche pas comme indicateur

D'après Wikipédia EN, ces signes ne permettent pas de conclure :

- une grammaire parfaite ;
- un mélange de registres ;
- une prose « fade » ou « académique » ;
- un mot de transition isolé ;
- l'absence de sources.

Et sur les détecteurs : leurs taux d'erreur ne sont pas négligeables ; une
étude de 2025 montre que des humains ne font pas mieux que le hasard, tandis
que de gros utilisateurs de modèles reconnaissent environ 90% des textes
générés. On corrige un texte pour qu'il soit meilleur pour son lecteur, pas
pour un détecteur.

## Ce qui a été écarté, et pourquoi

| Idée trouvée dans les sources | Pourquoi on ne la reprend pas |
|---|---|
| Plafonner le tiret cadratin à 1 pour 100 mots (S) | règle de l'utilisateur : supprimé ou virgule. En français, le tiret cadratin est rare hors dialogue |
| Envoyer le texte à des détecteurs payants pour comparer (S) | le texte part chez des tiers ; scores bruités sous 300 mots |
| Glisser des fautes volontaires (M) | dégrade le texte, et la sur-correction se repère |
| « Varier le rythme » comme remède (B, H) | la variation forcée est devenue un tic ; on corrige le plat, on ne fabrique rien |
| « Honnêtement, je ne sais pas… » pour donner de la voix (B) | annonce de sincérité ; on garde le doute réel, sans l'annonce |

## Sources

- Serge Bulaev, linkedin-humanizer V3, `scrub-rules.md`, `tier-rationale.md`
  (MIT, septembre 2026).
- blader/humanizer v3.1, SKILL.md et CHANGELOG (MIT).
- Boileau (alxbd/boileau), humaniseur français (MIT).
- Wikipédia EN, « Signs of AI writing » ; Wikipédia FR, « Aide:Identifier
  l'usage d'une IA générative » (CC BY-SA), consultés le 2 octobre 2026.
- Marian Kamenistak, anti-ai-writing-guide (MIT).
