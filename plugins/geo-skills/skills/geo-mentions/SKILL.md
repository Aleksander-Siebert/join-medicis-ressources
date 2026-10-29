---
name: geo-mentions
description: >-
  Trouve les sites tiers qui façonnent les réponses des IA là où la marque
  perd : à partir des questions perdues de /geo-visibilite, classe les
  domaines cités (comparateurs, presse, avis, forums, Wikipédia, sites
  concurrents), ouvre chaque page citée pour dire si la marque y figure et
  quels concurrents y sont, puis donne l'action qui convient à chaque
  classe et un plan de mentions légitimes, sans faux avis, faux comptes ni
  contenu sponsorisé caché (lignes rouges du droit français). Utilise-le
  pour « où les IA prennent leurs sources », « pourquoi ChatGPT cite mes
  concurrents », « notoriété dans les IA », « comparateurs », « Reddit »,
  « relations presse pour les IA ». Pas pour mesurer la visibilité
  (/geo-visibilite) ni corriger une erreur factuelle (/geo-exactitude).
  Aucun score de notoriété.
---

# geo-mentions

Les moteurs recommandent les marques dont **d'autres** parlent. Quand une
question est perdue, la liste des sources citées dans la réponse dit qui a
fait la liste : un comparateur, un article de presse, un fil Reddit, la
page d'un concurrent. **Cette liste est le plan.** Ce Skill la sort de la
mesure, vérifie page par page si la marque y figure, et propose une action
par site, toujours légitime.

**À lire avant de commencer :** `commun/regles.md` (règle 6 : aucune
manipulation) et `references/lignes-rouges.md`.

## 1. Partir de la mesure

Il faut une mesure de `/geo-visibilite` avec les sources citées (moteurs
qui donnent leurs liens : Perplexity, ChatGPT avec recherche, Aperçus IA,
Copilot) :

```bash
python3 ../geo-visibilite/scripts/visibilite.py mesurer reponses.txt --marque "Assurly" \
    --domaine assurly.example --concurrent "April=April International,april.fr" --json > mesure.json
python3 scripts/sources.py mesure.json --marque "Assurly" --domaine assurly.example --concurrent "April=april.fr"
python3 scripts/sources.py mesure.json --reponses reponses.txt --marque "Assurly" \
    --domaine assurly.example --concurrent "April=April International,april.fr" --verifier
```

Sans mesure : faire d'abord `/geo-visibilite`. Une liste de sites « que
les IA aiment » tirée d'une étude générale ne remplace pas les sources
citées sur vos questions.

## 2. Ce que donne le script

| Colonne | Sens |
|---|---|
| perdue(s) | nombre de paires question × moteur perdues où le domaine est cité |
| questions, moteurs | lesquelles |
| nommés | concurrents cités dans ces réponses |
| classe | comparateur, presse, consommateurs, communauté, place de marché, référence, institution, concurrent, autre (`commun/sources_fr.json`) |
| page (`--verifier`) | **MARQUE ABSENTE** de la page citée, marque présente, non lu (403, 429…), URL exacte inconnue |

« Cité sur une question perdue, marque absente de la page » est la ligne
la plus utile : le moteur a lu une page qui ne parle pas de vous. « Marque
présente » sur une question perdue veut dire autre chose : la page vous
cite mais ne vous met pas en avant, ou le moteur a retenu d'autres noms ;
lis le passage.

## 3. L'action par classe

| Classe | Action | À ne jamais faire |
|---|---|---|
| comparateur | demander à être évalué ou mis à jour ; données exactes et datées | payer un classement non signalé comme publicité |
| presse | une donnée propre (étude, baromètre) ou un expert nommé, au journaliste qui couvre le sujet | acheter un article non signalé |
| consommateurs | vérifier la fiche, répondre publiquement aux réclamations | |
| communauté (Reddit, forums, YouTube) | répondre en son nom, avec transparence, là où la question est posée | faux comptes, faux témoignages |
| place de marché | fiche complète et exacte ; avis collectés selon la loi | avis triés, achetés ou rédigés |
| référence (Wikipédia, Wikidata) | proposer des corrections sourcées, déclarer son lien | écrire soi-même l'article de sa marque |
| institution | rien à obtenir ; la page de la marque reprend exactement ces règles | |
| concurrent | le concurrent a la page qui répond : `/geo-contenu` | copier sa page |
| autre | ouvrir la page, la classer (`--classe domaine=classe`), puis appliquer sa ligne | |

Messages types, ordre de priorité et suivi : `references/plan.md`.

## 4. Le plan (3 actions au plus par mois)

1. Les sites **cités sur le plus de questions perdues** avec **marque
   absente** de la page.
2. Parmi eux, ceux où la marque a un vrai titre à figurer (offre
   comparable, public visé) : sinon, le dire et passer.
3. Une action par site, un propriétaire, une date ; la remesure dit si
   ça a joué (`/geo-visibilite comparer`, même portefeuille).

Pas de « 90 jours pour gagner X% » : aucune source ne permet de le
promettre.

## 5. La sortie (format fixe)

```
SOURCES TIERCES · Assurly · 2 paires question × moteur perdues sur 6 questions · mesuré (réponses collées)

CLASSES SUR LES QUESTIONS PERDUES · comparateur 1 · consommateurs 1 · communaute 1

À TRAVAILLER (cités là où la marque perd)
  lelynx.fr                   comparateur   1 perdue(s) · P01 · ChatGPT · nommés : Allianz Care (2), April (2)
      MARQUE ABSENTE    https://www.lelynx.fr/expat · concurrents sur la page : April International
      → demander à être évalué ou mis à jour, fournir des données exactes et datées …
```

Exemple fictif (`evals/geo-mentions/`). Sous la sortie : le plan du §4 en
3 lignes.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Aucune source dans la mesure | Le moteur ne donne pas ses liens (ChatGPT sans recherche, Claude sans web) : remesurer sur un moteur qui cite, ou demander les sources à la main. |
| Page en 403, 429 ou non lue | « non lu » : l'ouvrir dans un navigateur ; ne jamais conclure « absente ». |
| Domaine cité sans lien complet | « URL exacte inconnue » : chercher la page sur le site. |
| Réponses obtenues par Tavily | Étiquette « approximation » reprise : ce n'est ni ChatGPT ni Perplexity. |
| Concurrent nommé « Apple », « Orange » | Nom commun : la présence sur la page peut être fortuite ; lire. |
| Marque présente partout, questions toujours perdues | Le problème n'est pas la présence mais la place ou le ton : lire les passages, `/geo-exactitude` pour le cadrage. |
| L'utilisateur veut « acheter des mentions » | Expliquer les lignes rouges ; un partenariat signalé comme tel reste possible. |

## Ressources

- `scripts/sources.py` · `commun/sources_fr.json` · `commun/page.py`
- `references/plan.md` : priorités, messages types (comparateur,
  journaliste, communauté), suivi.
- `references/lignes-rouges.md` : faux avis, influence commerciale,
  Wikipédia, ce que dit le droit français.

## Skills liés

`/geo-visibilite` (la mesure de départ), `/geo-contenu` (la page qui
manque), `/geo-exactitude` (une source tierce fausse), `/geo-entite`
(profils alignés), `/seo-local` (avis et fiche Google, pack SEO).

## Règles du pack

- Rien n'est envoyé ni publié : les messages sont proposés, l'utilisateur
  les envoie.
- Zéro invention : aucune mention, note, nombre d'avis ou présence affirmé
  sans l'avoir vu ; « non lu » sinon.
- Texte simple dans la conversation, sans créer de document.
