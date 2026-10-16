# geo-score (Jianrun Tech)

MIT, 323 étoiles, commit 65bf9ee du 15 oct. 2026, v1.8.3. Un script
Python **sans dépendance** (`cli/geo_score.py`), un SKILL.md de
177 lignes, un serveur MCP, une rubrique publique versionnée
(`rubric/v1.0`, `v1.1`, calibration, preuves, questions ouvertes), un
**banc de mesure** (`benchmark/` : 324 sites notés en public,
reproductibilité, sensibilité, validité, pré-enregistrement), 294
fixtures de test. Anglais et chinois.

## Exécuté (16 oct. 2026)

`python3 cli/geo_score.py joinmedicis.com` : fonctionne derrière le proxy
(`SSL_CERT_FILE`), 46 s, **84/100 « Leading »**, 57/68 points
observables.

- Chaque contrôle donne sa preuve et ce qu'il faut pour le palier
  suivant.
- **Ce qui n'est pas mesuré sort du dénominateur et est nommé** :
  « p2.question-intent (no question-intent lexicon for fr) »,
  « p2.sourced-stats (no source-phrase lexicon for fr) »,
  « knowledge-graph (Wikidata et Wikipédia n'ont pas tous répondu) ».
  **La place de notre pack est exactement là** : les lexiques français
  (formulations de question, de source, de définition), qui manquent à
  tous les outils lus.
- « Observé, jamais noté » : comparaison RFC 9309 et lecture
  « première règle » sur 81 pages ; pages du sitemap non liées depuis le
  HTML serveur (liste de nos fiches LinkedIn non liées : utile pour notre
  maillage).

## La méthode : ce qu'aucun autre dépôt ne fait

- **Rubrique versionnée et publique**, chaque contrôle en paliers avec
  une règle écrite. Les ambiguïtés trouvées sur de vrais sites sont
  publiées avec leur résolution (« Open questions », 8 points résolus
  en v1.1) : libellés de bande trompeurs (« Critique » pour un site
  sain), passages de 40 à 90 mots sans équivalent en chinois (fixé à
  50-200 caractères, l'anglais élargi à 25-120 mots), `sameAs` absent =
  zéro et non « sans objet ».
- **Validité** : la CLI comparée à un audit humain de la même rubrique
  sur 5 sites (même palier sur 80% des paires, 92% pour les contrôles à
  règle, 69% pour les heuristiques ; écart moyen -2,4 points), avec ses
  limites écrites (n=5, données de développement, un seul auditeur).
- **Pré-enregistrement** avant toute donnée : « le score va-t-il avec
  le fait d'être cité ? ». Teste l'instrument, pas le GEO ; distingue
  être choisi comme source et être absorbé dans la réponse ; dit qu'une
  réponse d'API n'est pas celle des applis grand public.
- **Trois niveaux** : note (gratuite, sans clé) ; « Ask » une question
  aux API des moteurs avec ses propres clés ; « Watch » une liste de
  questions chaque semaine. **La partie citation n'est jamais ajoutée à
  la note.**
- **Portes** : un site injoignable ou bloqué voit sa note plafonnée.

## Ce qui reste discutable

- `llms.txt` vaut 5 points (sur 68 observables) : contraire à la
  position de Google, même si la rubrique est explicite.
- Points pour la vidéo et les profils de plateformes : corrélations
  supposées.
- Seuils de mots des passages « citables » : choix calibrés, sans
  source Google (Google dit de ne pas découper pour l'IA).

## Verdict

La meilleure **méthode de mesure** lue : rubrique en paliers
versionnée, « non mesuré = hors du dénominateur, et dit pourquoi »,
validité contre audit humain, pré-enregistrement, citation séparée de
la note. À reprendre comme modèle de rigueur pour notre score GEO. Notre
apport : les lexiques français qui lui manquent.
