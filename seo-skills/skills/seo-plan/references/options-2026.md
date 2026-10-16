# Options 2026 : les tendances, à proposer, jamais à imposer

Source : Marketer Milk, « SEO trends 2026 »
(https://www.marketermilk.com/blog/seo-trends-2026), texte relu le
2 octobre 2026. C'est un **avis de praticien**, pas une source primaire :
chaque chiffre ou cas qu'il cite porte [à vérifier]. Le plan les présente
comme des options ; l'utilisateur choisit.

| Option | Ce qu'elle propose | Où elle s'applique | Garde-fou |
|---|---|---|---|
| E-E-A-T comme preuve sociale | faire parler les autres de la marque : podcasts, interviews, avis tiers, mentions, études de cas sur d'autres sites | `/geo-mentions` (pack GEO), bloc auteur de `/seo-write` | aucune mention achetée ni avis fabriqué (garde-fou du pack) |
| Recherches de marque associées | provoquer des recherches « {marque} + {mot-clé} » (contenus d'utilisateurs, influence, relations presse) | ce plan, suivi dans `/seo-veille` | l'effet sur le classement n'est pas démontré [à vérifier] |
| Titles personnels et émotionnels | « J'ai testé… », « Mon avis après 2 ans » | `/seo-brief`, `/seo-write`, `/seo-refresh` (panier « clic faible ») | **seulement si le contenu le prouve** (test réel, durée réelle) ; mesurer le CTR avant / après |
| Vidéo YouTube dans les meilleurs articles | une vidéo par article phare, intégrée à l'article | `/seo-social`, `/seo-refresh` | le cas cité (une page passée en tête après l'intégration) est une anecdote [à vérifier] : tester sur une page, mesurer |
| Ne pas tout basculer sur l'IA | Google reste la source principale de trafic ; les taux de conversion attribués aux assistants d'IA sont biaisés (visites de bas de tunnel) | ce plan, `/geo-optimize` | la part de marché citée par l'article est [à vérifier] |
| Refus du black hat pour les LLM | pas de microsites générés par IA reliés au site principal | `commun/garde_fou.py` | refus motivé, règle anti-spam de Google citée |
| Expérience vécue plutôt que volume | moins d'articles, chacun avec une preuve d'expérience (cas, photos, chiffres de l'entreprise) | `/seo-write` (réserve de preuves), `/seo-audit` | zéro invention : une expérience qui n'existe pas devient un `{{à compléter}}` |

## Comment les proposer

À la fin du plan (§8 du SKILL.md), une ligne par option retenue avec son
Skill et sa mesure : « Option retenue : vidéo dans les 3 meilleurs articles,
mesurée par la position et le CTR sur 6 semaines (`/seo-refresh` journal). »
Une option non mesurable n'est pas proposée.
