# Résultats de l'évaluation v1.0 (2 octobre 2026)

## 1. Citabilité en français : référence contre v1

Huit passages français sur l'assurance santé expatrié
([`comparaison/passages.json`](comparaison/passages.json)) :

- 4 **bons** passages, qui répondent dès la 1re phrase, avec des chiffres et une source ;
- 4 **faibles** : ils ouvrent sur « Il faut », « Cela », « Ainsi », renvoient à
  « plus haut » et ne contiennent aucun fait.

Chaque passage est noté par deux scoreurs :

- `citability_scorer.py` de [geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) (la **référence**) ;
- `citability.py` de ce pack (**v1**).

| | bons (moyenne) | faibles (moyenne) | écart |
|---|---|---|---|
| référence | 39,5 | 30,5 | 9,0 |
| v1 | 76,5 | 34,8 | **41,8** |

Les deux classent les bons passages au-dessus des faibles. Mais la référence
cherche « is a », « refers to », « according to » et « $ ». En français, elle
note un bon passage 40 au mieux : elle ne voit ni les définitions, ni les
montants en euros, ni les sources. La v1 reconnaît « est », « coûte »,
« dure », « selon », « d'après », « loi n° », les euros et les délais.

Pour refaire le test :

```bash
git clone https://github.com/zubair-trabzada/geo-seo-claude /tmp/geo-seo-claude
python3 evals/comparaison/comparer.py /tmp/geo-seo-claude/scripts
```

## 2. Sur des sites réels

- **joinmedicis.com, article « anatomie d'un Skill Claude »** :
  - `geo_audit.py` donne 72 (score partiel) ;
  - la citabilité est de 46 : plusieurs sections ouvrent sur une consigne et non
    sur une réponse.
- **lemonde.fr** : `crawlers.py` signale les robots bloqués (Anthropic,
  Google-Extended, Mistral, entre autres) et un llms.txt mal formé.
- **Fiche GEO Skills sur joinmedicis.com**, avant publication :
  - la citabilité est de 54 ;
  - l'audit on-page du pack SEO a trouvé 4 défauts communs à toutes les fiches
    Skills : title sans la marque, meta description de 255 caractères, deux H1,
    saut H2 → H4 dans le pied de page ;
  - les 4 sont corrigés sur le site.

## 3. Tests automatiques

`python3 evals/scripts/test_geo.py` : 8 sur 8.

Les tests couvrent :

- la citabilité (Markdown et HTML) ;
- les règles robots.txt robot par robot ;
- les propositions de robots.txt et de llms.txt ;
- la part de voix à partir de réponses collées ;
- le score partiel de l'audit ;
- `nosnippet` et `max-snippet:0` (exclusion d'AI Overviews) ;
- les obstacles pour les agents d'IA (`agentic.py`).

## Corrections après vérification des sources (v1.1)

La v1.0 contenait trois affirmations dépassées, repérées en relisant
claude-seo puis vérifiées chez Google :

- **FAQ** : les résultats enrichis FAQ ne s'affichent plus du tout sur Google
  depuis le 7 mai 2026 (la v1.0 parlait de « quelques sites officiels et de
  santé »). FAQPage et HowTo ne comptent plus dans le score.
- **Découpage** : le guide de Google sur l'IA générative (10 juillet 2026)
  dit qu'il n'est pas nécessaire de découper ses contenus en petits morceaux.
  La règle « bloc de 40 à 60 mots » devient « la réponse en 2 ou 3 phrases ».
- **llms.txt** : Google l'ignore. Il ne compte plus dans le score technique
  (il valait 5 points sur 100).

## Limites

- Huit passages, choisis par l'auteur du pack : c'est un contrôle de bon
  sens, pas un banc d'essai. Le scoreur de référence est conçu pour l'anglais :
  le test montre qu'il ne faut pas l'utiliser tel quel sur un site français,
  pas qu'il est mauvais.
- Aucun test ne mesure encore l'effet réel sur les citations par les IA. Il
  faudra 2 ou 3 mois de suivi avec `/geo-visibility` sur les mêmes prompts.
