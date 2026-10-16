---
name: geo-contenu
description: >-
  Relit une page section par section pour qu'un lecteur, et donc un moteur
  de réponse, y trouve vite une réponse vraie : réponse en tête sans
  préambule, section qui se lit seule, statistiques sourcées, promesses à
  prouver (« n°1 », « le moins cher »), élément de première main, un seul
  H1, date visible, texte présent sans JavaScript ; puis les familles de
  faits qu'une question appelle (prix, comparaison, démarche, définition,
  choix). Montre l'avant et l'après section par section, sans rien inventer.
  Utilise-le pour « rendre ma page citable par ChatGPT », « optimiser pour
  les Aperçus IA », « citabilité », « pourquoi les IA citent un concurrent
  plutôt que ma page ». Pas pour un brief ou un article neuf (/seo-brief,
  /seo-write), l'accès des robots (/geo-acces) ni le JSON-LD (/geo-entite).
  Aucune note sur 100 ni promesse de citation.
---

# geo-contenu

Les moteurs de réponse citent des passages qui répondent. Google le dit
sans détour : pas besoin de découper ses pages ni de les réécrire « pour
l'IA », ses systèmes trouvent le bon passage dans une page longue, et ce
qui compte est un contenu original fait par des gens qui savent. Ce Skill
ne fabrique donc pas de « contenu pour IA » : il trouve les sections qui
tournent autour du pot, les chiffres sans source et les promesses sans
preuve, et propose une réécriture pour le lecteur.

**À lire avant de commencer :** `commun/regles.md` et `commun/preuves.md`
(§2 Google, §5 recherche, §7 folklore). Si `site-context.md` existe, lis-le :
les données produit, le ton et les auteurs en viennent.

## 1. Ce qu'on ne promet pas

- **Aucune note sur 100.** Le pack l'a retirée : aucun outil ne voit les
  signaux des moteurs, et une note de « citabilité » mélange des choses qui
  ne s'additionnent pas. La sortie donne des contrôles réussis ou manqués,
  chacun avec la phrase lue.
- **Aucun gain de citation chiffré.** Les « +40% » du papier GEO de 2024 ne
  valent que dans son cadre ; sur les moteurs actuels, la réécriture seule
  est en général inefficace (C-SEO Bench, NeurIPS 2025). Une page plus
  claire aide d'abord le lecteur.
- **Pas de découpage en blocs de N mots**, pas de « TL;DR pour les IA »,
  pas de FAQ ajoutée pour un balisage qui ne s'affiche plus.

## 2. Lancer le contrôle

```bash
python3 scripts/contenu.py https://www.site.fr/guide/ --question "Combien coûte une mutuelle pour indépendant ?"
python3 scripts/contenu.py article.md --json
```

`--question` : la question à laquelle la page doit répondre (prends-la dans
le portefeuille de `/geo-visibilite`, idéalement une question perdue).

Par section (titres H1 à H3, navigation et pied de page ignorés, texte
`aria-hidden` ignoré) :

| Contrôle | Réussi quand | Manqué, exemple |
|---|---|---|
| réponse en tête | la 1re phrase définit, chiffre ou tranche ; ou la section s'ouvre sur une liste ou un tableau | « Dans cet article, nous allons voir… » |
| autonome | pas de pronom ni de connecteur en tête, pas de renvoi | « Elle couvre… », « comme vu plus haut » |
| statistiques sourcées | chaque %, « millions », « 7 sur 10 » a une source nommée ou une date | « les tarifs ont augmenté de 8% » seul |
| sans promesse à prouver | pas de « n°1 », « le meilleur », « le moins cher », « 100% garanti » | « le meilleur courtier du marché » |

Les prix et délais de l'offre ne sont pas des statistiques : leur
exactitude se vérifie avec `/geo-exactitude`.

Pour la page : un seul H1 (le script signale un doublon exact), texte
présent dans le HTML serveur, date de publication ou de mise à jour,
**élément de première main** (cas réel, donnée maison, expérience,
citation attribuée), title qui reprend la question.

**Familles de faits** (`--question`) : ce qu'une question de ce type
appelle. Exemple pour un prix : montant, période, ce qui le fait varier,
inclus et exclus, date du tarif. Les familles sont **déduites** du type de
question, pas observées dans les moteurs : confirme-les avec les sources
que citent les réponses (`/geo-visibilite`, colonne « sources »). Liste
complète : `references/familles.md`.

Sans exécution de code : même grille à la lecture, section par section, et
« lecture manuelle » en tête.

## 3. Réécrire

Pour chaque section manquée, dans cet ordre :

1. **La réponse en une phrase**, sujet nommé : « Une mutuelle pour
   indépendant coûte de 39 € à 95 € par mois chez Assurly, selon la formule
   et l'âge. » Le chiffre vient de `site-context.md` ou de l'utilisateur ;
   sinon `{{à compléter}}`.
2. **Le format de la question** : définition pour « qu'est-ce que »,
   étapes numérotées pour « comment », tableau pour « X ou Y », liste avec
   « pour qui » pour « quel… choisir ».
3. **Une source nommée par statistique** (organisme, texte, étude datée).
   Pas de source : on retire le chiffre, on n'en cherche pas un « probable ».
4. **La promesse** devient un fait vérifiable (« note de 4,6 sur 5 sur
   1 200 avis vérifiés, octobre 2026 ») ou disparaît. Un superlatif sans
   preuve expose à la qualification de pratique commerciale trompeuse
   (Code de la consommation, L121-2) **[à faire valider par un juriste]**.
5. **Ce que le site est seul à savoir** : un cas client anonymisé, une
   donnée interne, une expérience de terrain, si l'utilisateur la fournit.
   C'est ce que Google appelle contenu original, et ce qu'un concurrent ne
   peut pas reprendre.

Montre **l'avant et l'après section par section**, jamais la page entière
réécrite d'un bloc. Méthode, exemples et cas limites :
`references/reecrire.md`. Puis passe le texte par l'humaniseur
(`/seo-human` du pack SEO, s'il est installé).

## 4. La sortie (format fixe)

```
CONTENU · page-assurly.html · 5 sections de 15 mots ou plus

BILAN (sections qui passent le contrôle / sections concernées)
  réponse en tête           4/5
  autonome                  4/5
  statistiques sourcées     1/2
  sans promesse à prouver   4/5
  première main             1 section(s), dont « Notre avis » : « Nous avons analysé 1 200 dossiers… »
PAGE
  ! 2 H1 dont un doublon exact
FAMILLES DE FAITS · « Combien coûte une mutuelle pour indépendant ? » · type prix (déduit, pas observé)
  présente  montant chiffré
  ABSENTE   date du tarif
SECTIONS
  ## Introduction · 29 mots · 1 à revoir
      ✗ réponse en tête : préambule avant la réponse
          « Dans cet article, nous allons voir pourquoi… »
```

Exemple fictif (`evals/geo-contenu/`). Sous la sortie : 3 réécritures au
plus, les sections qui répondent à la question visée d'abord.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Page en 403 ou non lue | Le script le dit et s'arrête ; demander le HTML enregistré depuis le navigateur. |
| Peu de mots dans le HTML serveur | Contenu rendu en JavaScript : `/geo-acces` (texte sans JavaScript), sinon lire la page rendue copiée par l'utilisateur. |
| Page d'accueil, catégorie, fiche produit | Les contrôles de section servent peu ; regarder H1, title, date et familles de faits, et choisir plutôt la page qui doit répondre à la question. |
| Section de moins de 15 mots | Ignorée (titre de carte, bouton). |
| Titre animé lettre par lettre | Le texte `aria-hidden` est ignoré ; un seul H1 compté. |
| Question qui mêle deux types | Lancer deux fois avec deux formulations ; garder les familles des deux. |
| Contenu santé, finance, droit | Statistiques et promesses passent avant tout ; l'auteur et sa compétence doivent être visibles. |
| L'utilisateur veut des chiffres « pour faire sérieux » | Refuser d'en inventer ; proposer de les mesurer (`{{à compléter}}`). |

## Ressources

- `scripts/contenu.py` · `commun/page.py`
- `references/reecrire.md` : réécrire une section, avant et après,
  promesses, première main.
- `references/familles.md` : familles de faits par type de question, et
  comment les confirmer.

## Skills liés

`/geo-visibilite` (questions perdues et sources citées : quoi réécrire),
`/geo-exactitude` (prix et données de l'offre), `/geo-entite` (JSON-LD et
nom de la marque), `/seo-write` et `/seo-human` (pack SEO).

## Règles du pack

- Zéro invention : pas un chiffre, une source, un avis ou un cas client
  ajouté sans venir de l'utilisateur ou d'une source primaire.
- Rien n'est publié : la réécriture est proposée, l'utilisateur publie.
- Texte simple dans la conversation, sans créer de document.
