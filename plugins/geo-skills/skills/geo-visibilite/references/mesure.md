# Mesurer : protocole, échantillon, marge d'erreur

## 1. Le protocole manuel (mode gratuit, par défaut)

1. Une **nouvelle conversation** par passage. Pas d'historique, mémoire
   désactivée si le moteur le permet, de préférence sans être connecté ou
   avec un compte sans personnalisation.
2. **Recherche web activée** quand le moteur la propose (ChatGPT, Gemini,
   Claude, Mistral Vibe) : c'est ce que voient la plupart des clients.
   Note-le dans le nom du moteur si tu mesures les deux modes
   (« ChatGPT (recherche) », « ChatGPT (sans recherche) »).
3. Même pays et même langue que les clients visés.
4. Colle la réponse **entière** : texte, liens, liste des sources.
5. Note la date de la série (le nom du fichier suffit :
   `reponses-2026-10.txt`).

L'appli grand public et l'API d'un même éditeur ne donnent pas les mêmes
réponses : une mesure faite par API s'étiquette « API », jamais « ce que
voient les clients ».

## 2. Combien de passages

Les listes de marques changent presque à chaque réponse. Ce qui est stable,
c'est la **part des réponses** qui nomment une marque. Repères (préprint
« Dice Roll Method », 2026, à présenter comme tel) :

| Passages par question et par moteur | Usage |
|---|---|
| 5 | explorer |
| 10 | confirmer un constat |
| 15 et plus | affirmer, comparer finement |

Budget réaliste en mode manuel : le cœur (15 à 20 questions) × 1 ou
2 moteurs × 5 passages, une fois par mois. Dis toujours combien de passages
ont été faits.

## 3. La marge d'erreur

Chaque taux sort avec son **intervalle de Wilson à 95%** (`commun/stats.py`).
Repères pour un taux autour de 30 à 50% :

| Réponses (n) | Marge approximative |
|---|---|
| 5 | ±33 points |
| 10 | ±25 à ±26 points |
| 20 | ±19 à ±20 points |
| 50 | ±12 à ±13 points |
| 100 | ±9 à ±10 points |
| 300 | ±5 à ±6 points |

```bash
python3 commun/stats.py taux 7 20          # 35% (7/20, IC 95% : 18-57%)
python3 commun/stats.py echantillon --marge 10 --p 0.3   # passages pour ±10 points
```

Un écart entre deux périodes ne compte que si l'intervalle de la
différence exclut zéro (`visibilite.py comparer`, méthode de Newcombe).
Sinon : « pas de changement détectable ».

## 4. Étiqueter chaque chiffre

| Étiquette | Exemple |
|---|---|
| mesuré | « mentionnée dans 35% des réponses (7/20) de ChatGPT, 1er au 3 oct. 2026 » |
| première partie | « Search Console, rapport IA générative, 28 jours au 12 oct. 2026 » |
| publié | « selon Profound, juillet 2026, étude d'éditeur » |
| approximation | « moteur de Tavily, pas ChatGPT » |
| estimé | à éviter ; jamais présenté comme une mesure |

## 5. Ce que le script compte, et ses limites

- **Mentionnée** : nom entier ou alias, sans accents ni majuscules. Un nom
  commun (« Orange ») demande des alias précis et une relecture.
- **Citée** : domaine de la marque dans un lien ou écrit en clair. Un
  moteur sans recherche web ne cite rien : 0 par construction.
- **Recommandée** : marqueur français de conseil dans la phrase qui nomme
  la marque, seule ou dans une liste courte (« choisissez un revendeur
  certifié : A, B ou C » compte pour A, B et C), sans négation juste avant
  et sans que la marque soit la partie écartée d'une opposition (« je
  recommande Cigna plutôt qu'Assurly » ne compte pas pour Assurly). Relis
  les cas limites : c'est un indice, pas un jugement.
- **Déconseillée** : marqueur de mise en garde dans la phrase qui nomme la
  marque (« à éviter », « je déconseille », « nombreuses plaintes »).
- **Pas de rang** : la position dans la liste change à chaque passage
  (SparkToro et Gumshoe, 2026) ; un rang moyen cache cette variance.
- **Récupéré** (page lue sans être citée) : invisible dans une réponse.
  Les rapports « requêtes d'ancrage » de Bing ou les journaux du serveur en
  donnent une partie.

## 6. Sans exécution de code

Compte à la main, question par question, dans un tableau
moteur × mentionnée × citée × recommandée, puis lis la marge dans la table
du §3. Écris « comptage manuel » dans la sortie.
