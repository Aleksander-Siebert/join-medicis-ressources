# Le diagnostic, contrôle par contrôle

## 1. Les 24 contrôles

Les points disent l'ordre d'importance pour **lire et citer** la page, pas
un poids publié par un moteur : aucun moteur n'en publie. Le plus lourd va
à ce qui empêche tout le reste (lecture, indexation, extrait), d'après les
conditions que Google publie pour les Aperçus IA et le Mode IA.

| Id | Contrôle | Pts | Source | Skill |
|---|---|---|---|---|
| A1 | robots.txt lisible (pas de 5xx) | 3 | Google, introduction à robots.txt ; RFC 9309 | /geo-acces |
| A2 | Googlebot autorisé | 5 | Google, robots.txt ; guide IA (indexation requise) | /geo-acces |
| A3 | page indexable (pas de noindex) | 5 | Google, bloquer l'indexation | /geo-acces |
| A4 | extrait autorisé (pas de nosnippet ni max-snippet:0) | 5 | Google, guide IA (page éligible à un extrait) | /geo-acces |
| A5 | OAI-SearchBot autorisé | 4 | OpenAI, page des robots (`commun/preuves.md` §1) | /geo-acces |
| A6 | Bingbot autorisé (Copilot) | 3 | table du pack | /geo-acces |
| A7 | PerplexityBot autorisé | 3 | Perplexity, page des robots | /geo-acces |
| A8 | Claude-SearchBot autorisé | 3 | Anthropic, page des robots | /geo-acces |
| A9 | pas de refus au user-agent des robots | 4 | table du pack ; à confirmer dans le pare-feu | /geo-acces |
| P1 | texte dans le HTML serveur (150 mots ou plus) | 8 | Google, bases du JavaScript pour le SEO | /geo-contenu |
| P2 | canonical vers cette page | 3 | Google, URL en double | /geo-acces |
| P3 | un seul H1 | 2 | règle de clarté du pack | /geo-contenu |
| P4 | date de publication ou de mise à jour | 2 | Google, contenu utile (« qui, comment, pourquoi ») | /geo-contenu |
| C1 | 60% des sections répondent en tête | 8 | Google, contenu utile ; clarté pour le lecteur | /geo-contenu |
| C2 | statistiques sourcées | 5 | Google, contenu utile | /geo-contenu |
| C3 | aucune promesse à prouver | 3 | Code de la consommation (pratiques trompeuses) ; règle du pack | /geo-contenu |
| C4 | élément de première main | 4 | Google, guide IA (contenu original, non générique) | /geo-contenu |
| E1 | nom de la marque cohérent | 5 | règle du pack | /geo-entite |
| E2 | un bloc Organization par entité | 4 | Google, règles des données structurées | /geo-entite |
| E3 | sameAs vers les profils de l'organisation | 3 | règle du pack | /geo-entite |
| E4 | note et prix balisés visibles | 3 | Google, règles des données structurées | /geo-entite |
| G1 | boutons, liens et champs nommés | 5 | web.dev, sites adaptés aux agents ; Lighthouse | /geo-agentic |
| G2 | rien de cliquable caché ou non sémantique | 3 | idem | /geo-agentic |
| G3 | aucune consigne cachée aux IA | 7 | Google, guide IA (tactiques inutiles) ; règle du pack | /geo-agentic |

Sans points, rapportés : familles de faits (`--question`), llms.txt,
version Markdown, WebMCP, Content-Signal, bloc Cloudflare (dans
`/geo-acces`).

Écarté de la note, une fois pour toutes : llms.txt, longueur de page ou de
passage, FAQ balisée, « schema pour l'IA », nombre de mots-clés, scores
d'autorité tiers. Aucun n'a de source primaire qui le relie aux réponses
des moteurs (`commun/preuves.md` §7).

## 2. États

| État | Sens | Dans la note |
|---|---|---|
| ok | contrôle passé, preuve à l'appui | points obtenus |
| manqué | contrôle échoué, preuve à l'appui | points possibles, non obtenus |
| non mesuré | le script n'a pas pu mesurer (fichier absent, réseau, option non lancée, objet absent) | hors calcul |
| à vérifier | mesure ambiguë (refus au faux user-agent) | hors calcul |

## 3. Le journal

`--journal journal-geo.csv` ajoute une ligne : date, URL, note, points,
contrôles manqués, contrôles non mesurés, et `{{à compléter}}` pour
l'action menée, que l'utilisateur remplit.

- Une action à la fois par page, notée avant de relancer.
- Relancer après publication : un contrôle passe de « manqué » à « ok »,
  c'est vérifié ; la visibilité, elle, se remesure 4 à 6 semaines plus tard
  avec `/geo-visibilite comparer` **[repère praticien]**.
- Deux tours sans effet sur la visibilité : l'action ne touchait pas la
  bonne couche, ou le levier est hors du site (`/geo-mentions`).

## 4. La grille de jugement (à part, jamais dans la note)

Ce que le script ne voit pas. Six critères, chacun noté 0 à 5 **avec la
phrase lue** qui justifie la note ; sans phrase, pas de note.

| Critère | 0 | 5 |
|---|---|---|
| Gain d'information | redit les autres pages | apporte un fait, un cas ou une méthode introuvable ailleurs |
| Compétence visible | aucun auteur | auteur nommé, rôle et preuve vérifiable (inscription, cas) |
| Exactitude | faits faux ou périmés | faits datés, conformes aux données `LIVE` |
| Clarté de l'offre | on ne sait pas qui fait quoi pour qui | une phrase le dit dès le début |
| Preuves | aucune | avis vérifiables, cas, chiffres sourcés |
| Fraîcheur | dates anciennes, offres retirées | date de mise à jour récente et contenu à jour |

Total sur 30, présenté sous la note de préparation, jamais additionné.
