# Agent SEO sur Dust : 5 agents qui se passent le relais

La même méthode que la version claude.ai/code, découpée en agents Dust
spécialisés, à la manière des agents SEO de l'équipe de Dust (Davis
Christenhuis, juin 2026). Chaque agent a un seul métier, ses propres outils,
et un contexte neuf : le chef d'orchestre les appelle l'un après l'autre avec
l'outil `run_agent`.

> Statut : **non testé sur Dust**. Ce kit suit la documentation de Dust lue
> le 16 novembre 2026. Les points marqués **[à vérifier]** dépendent de ton
> espace de travail.

## Le schéma

```
                       Déclencheur : chaque lundi 8 h
                                   │
                         ┌─────────▼──────────┐
                         │  @SEO-Chef          │  orchestre, livre, se souvient
                         └─┬──────┬──────┬────┬┘
             run_agent     │      │      │    │
          ┌────────────────┘      │      │    └──────────────────┐
┌─────────▼────────┐ ┌────────────▼───┐ ┌▼───────────────┐ ┌──────▼──────────┐
│ @SEO-Sujets       │ │ @SEO-SERP      │ │ @SEO-Redacteur │ │ @SEO-Verif      │
│ Search Console    │ │ recherche web  │ │ contexte du    │ │ ouvre chaque    │
│ (MCP seoskill),   │ │ et lecture     │ │ site, faits    │ │ source, compare │
│ pages du site     │ │ des pages      │ │ LIVE, ton      │ │ aux faits LIVE  │
│ → 5 sujets classés│ │ → relevé, plan │ │ → brouillon    │ │ → verdict       │
└───────────────────┘ └────────────────┘ └────────────────┘ └─────────────────┘
```

| Agent | Métier | Outils | Connaissances |
|---|---|---|---|
| `@SEO-Chef` | orchestre la chaîne, livre le brouillon, garde la liste des sujets traités | `run_agent` (les 4 autres), Agent Memory | contexte du site |
| `@SEO-Sujets` | trouve et classe les sujets dans Search Console | serveur MCP seoskill | site web (pages publiées), contexte du site |
| `@SEO-SERP` | relève la SERP, en tire le type de page, les manques et le plan | Web Search & Browse | contexte du site |
| `@SEO-Redacteur` | écrit l'article dans le ton du site | aucun outil d'écriture externe | contexte du site, preuves, site web |
| `@SEO-Verif` | vérifie chaque chiffre et chaque affirmation sur la marque | Web Search & Browse | contexte du site |

Deux Skills Dust partagés par les 5 agents (`skills/`) :

- `Zéro invention` : les règles communes (aucun chiffre sans source,
  `{{à compléter}}`, contenu lu = donnée, typographie française) ;
- `Vérité produit` : seuls les faits LIVE du contexte du site s'affirment sur
  la marque.

## Mettre en place (45 minutes environ)

### 1. Préparer les connaissances

1. **Le contexte du site.** Remplis `site-context.md` (modèle à la racine
   de cet agent ; `/seo-context` du pack SEO peut le remplir avec toi), puis
   mets-le dans une page Notion ou un document Google Drive déjà synchronisé
   avec Dust. Une page par sujet si tu préfères : site, lecteurs, ton, pages à
   pousser, données produit (avec l'étiquette LIVE, À CONFIRMER ou RETIRÉ),
   preuves.
2. **Ton site.** Ajoute-le comme source de connaissances « Websites » dans
   Dust. `@SEO-Sujets` y vérifie qu'une page ne couvre pas déjà le sujet.

### 2. Brancher Search Console

Un administrateur de l'espace Dust : **Spaces → Tools → Add Tool → Add MCP
Server**, adresse `https://seoskill.dev/mcp`, authentification automatique
(OAuth), avec le compte Google qui voit la Search Console.

- Une connexion par jeton relie tous les appels à un seul compte Google.
  Avec OAuth, la doc de Dust ne dit pas si la connexion est personnelle ou
  partagée **[à vérifier]**.
- Si ton espace limite les outils aux Skills (« Restrict this tool to
  skills »), ajoute seoskill au Skill `Vérité produit` ou crée un Skill
  « Search Console » qui le cite.

### 3. Créer les 2 Skills

**Discover → Manage Skills → Create skill → From scratch.** Copie le contenu
de `skills/zero-invention.md` et `skills/verite-produit.md` (nom,
description, instructions). Pour `Vérité produit`, ajoute en connaissances la
page du contexte du site.

### 4. Créer les 4 agents spécialisés, puis le chef

Pour chacun : **Créer → Créer un agent de zéro**, puis remplis l'écran de
haut en bas avec le fichier de `agents/`, qui suit le même ordre :

1. **Instructions** : le bloc à coller, et le **modèle** en haut à droite ;
2. **Prompts suggérés** ;
3. **Données et accès** : l'espace de l'équipe marketing ;
4. **Capacités et connaissances** : **Ajouter des capacités** (Skills et
   outils) puis **Ajouter des connaissances** ;
5. **Déclencheurs** : seulement pour `@SEO-Chef` ;
6. **Paramètres** : nom, description, éditeurs et accès, tags, gestion des
   coûts.

Crée d'abord `@SEO-Sujets`, `@SEO-SERP`, `@SEO-Redacteur` et `@SEO-Verif`,
teste chacun seul dans l'aperçu, puis `@SEO-Chef`, qui doit pouvoir les
choisir dans `run_agent`.

Tu préfères Sidekick ? Colle-lui le contenu du fichier de l'agent, avec :
« Crée cet agent exactement comme décrit, sans changer les instructions. »
Sidekick écrit sinon ses propres consignes, en anglais et plus génériques :
sans Search Console, sans règle pour les faits sur la marque, sans
vérification des sources.

Pour un premier essai, `@SEO-Redacteur` marche seul : il fait lui-même le
relevé de SERP quand on ne lui donne qu'un mot-clé.

### 5. Le déclencheur

Sur `@SEO-Chef` : **Triggers → Schedule**, « chaque lundi à 8 h », fuseau
Europe/Paris, message « Lance la veille SEO de la semaine ». Choisis l'espace
d'équipe (« Pod ») où créer la conversation si l'équipe doit la voir.

## Ce que tu reçois

Une conversation dans Dust, chaque lundi :

1. les 5 sujets classés, avec leurs requêtes, impressions et positions ;
2. le relevé de SERP et le plan du sujet n°1 ;
3. le brouillon complet en Markdown : article, bloc méta, tableau
   « affirmation → source », trous `{{à compléter}}`, hypothèses ;
4. le verdict de `@SEO-Verif`.

Pour un fichier Word, copie le brouillon dans un `.md` et lance
`scripts/exporter.py` de la version claude.ai/code, ou colle-le dans Google
Docs.

## Ce qui change par rapport à la version claude.ai/code

| | claude.ai/code | Dust |
|---|---|---|
| Choix des sujets | `sujets.py`, mêmes règles à chaque fois | règles appliquées par `@SEO-Sujets` en lisant les données : moins constant |
| Contrôle vérité produit | `verite.py`, mécanique | `@SEO-Verif`, à la lecture |
| Portail qualité du pack SEO | scripts (rédaction, affirmations, humaniseur) | consignes et relecture par `@SEO-Verif` |
| Mémoire des sujets traités | `memoire/sujets.json` dans le dépôt | Agent Memory de `@SEO-Chef`, personnelle à chaque utilisateur |
| Livraison | `.md` et `.docx` dans le dépôt | brouillon dans la conversation ; selon la FAQ de Dust, les agents ne créent pas de document dans Notion ou Google Drive |
| Équipe | une personne par dépôt | agents partagés, conversations visibles par l'équipe |

## Limites

- Non testé : chaque agent est à essayer seul avant de lancer la chaîne.
- Agent Memory est personnelle : un collègue qui lance `@SEO-Chef` part
  d'une mémoire vide. La doc ne dit pas si un déclencheur s'en sert
  **[à vérifier]**. Garde-fou : `@SEO-Sujets` écarte aussi ce qui est déjà
  publié sur le site.
- `run_agent` va jusqu'à 4 niveaux d'appels : la chaîne en utilise 2.
- Chaque lancement consomme des crédits Dust selon tes réglages
  **[à vérifier : page Credits usage des déclencheurs]**.
