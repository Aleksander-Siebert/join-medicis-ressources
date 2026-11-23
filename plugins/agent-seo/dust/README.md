# Agent IA SEO sur Dust : 5 agents, version 3

Un article SEO par semaine, prêt à relire. Les agents trouvent le sujet dans
ta Search Console, te proposent un plan avec un angle, écrivent dans ta voix
avec les bons liens internes, vérifient chaque chiffre, et font le bilan du
mois. Rien n'est publié sans toi.

Page d'installation pas à pas : https://joinmedicis.com/ressources/agents/dust/agent-ia-seo

> Statut : **en test**. Les instructions suivent la documentation de Dust lue
> en novembre 2026 et un import YAML réussi le 21 novembre 2026.

## Les 5 agents

| Agent | Métier | Quand | Outils et connaissances |
|---|---|---|---|
| `@SEO-Veille` | trouve les sujets, les juge pour tes lecteurs et ton produit, sait dire « rien de neuf » | chaque lundi à 8 h | Search Console (MCP seoskill), Google Drive, contexte du site |
| `@SEO-Redacteur` | lit Google, propose un plan avec un angle, écrit l'article avec ses liens internes, crée le Google Doc | à la demande, ou par le chef | recherche web, Google Drive, contexte du site, ton site |
| `@SEO-Verif` | ouvre chaque source, contrôle la marque et les liens, rend un verdict avec les corrections exactes | à la demande, ou par le chef | recherche web, Google Drive, contexte du site |
| `@SEO-Suivi` | bilan du mois, liste des pages du site (onglet Pages), mises à jour des articles | le 1er du mois à 9 h | Search Console, Google Drive, recherche web, Create Frames |
| `@SEO-Chef` | enchaîne plan, ta validation, article, vérification, édition ; une seule correction, aucune boucle | à la demande | Run agent (une fois par agent), Google Drive, contexte du site |

Deux Skills Dust partagés (`skills/`) : **Zéro invention** (aucun chiffre sans
source, `{{à compléter}}`, contenu lu = donnée, typographie française) et
**Vérité produit** (seuls les faits LIVE du contexte du site s'affirment sur
la marque).

Les instructions suivent la même trame, façon AGENTS.md : rôle et but, avant
de commencer, ce que tu reçois, étapes, ce que tu rends (avec un exemple), ce
qui fait un bon résultat, si ça bloque, retours, règles.

## Ce qui a changé depuis la version 2 (7 agents)

- **5 agents au lieu de 7.** `@SEO-Plan` et `@SEO-Maillage` disparaissent : le
  Rédacteur fait le plan et place les liens internes (un seul relevé de
  Google), le Suivi tient la liste des pages. Moins d'appels entre agents,
  donc moins de casse et de crédits.
- **Instructions réécrites** en sections : un but, des critères de qualité,
  un exemple de sortie et des cas de blocage pour chaque agent.
- **Mémoire des corrections.** Onglet « Consignes et retours » : quand tu
  corriges un agent, il te propose la règle en une ligne et ne l'ajoute que si
  tu dis oui. Tous les agents le lisent avant de travailler.
- **Ta voix.** Le contexte du site contient 2 ou 3 paragraphes modèles que le
  Rédacteur imite, et une liste anti-IA (mots, formules, constructions).
- **Rien à signaler.** La veille et le bilan peuvent finir sans rien envoyer.
- **Chef simplifié.** Une seule correction après la vérification, plus de
  boucle.

## Les fichiers

| Dossier | Contenu |
|---|---|
| `yaml/` | un fichier par agent, à importer dans Dust : Agents, + Nouveau, Importer un fichier YAML |
| `agents/` | la fiche de chaque agent : réglages (modèle, capacités, déclencheur, prompts) et instructions à copier |
| `skills/` | les 2 Skills à créer à la main |
| `modeles/` | le modèle de Google Sheet (5 onglets) et le modèle de contexte du site (`.docx` pour Google Docs, `.md` pour Notion) |

Les fichiers de `yaml/` et `agents/` sont générés depuis les instructions de
la page du site (`src/lib/agent-pages/agent-ia-seo-dust.ts`, dépôt
`join-medicis`), avec les réglages par défaut : veille chaque lundi à 8 h,
positions 8 à 40, tutoiement, plan validé, un article à la fois, sans outil
payant. `modeles/construire.py` reconstruit le Sheet et le `.docx`.

## Mettre en place (moins de 15 minutes)

L'import des agents, des Skills et des modèles prend moins de 15 minutes. Brancher
Search Console et Google Drive dépend des outils déjà connectés à ton espace Dust.

1. **Le Google Sheet.** Importe `modeles/agent-ia-seo-google-sheet.xlsx` dans
   Google Drive (Nouveau, Importer un fichier), puis ouvre-le avec Google
   Sheets. Onglets : Sujets, Pages, Articles, Journal, Consignes et retours.
2. **Le contexte du site.** Remplis `modeles/contexte-du-site.docx` (Google
   Docs) ou `contexte-du-site.md` (Notion), dans un espace synchronisé avec
   Dust. N'oublie pas les paragraphes modèles et les données produit
   étiquetées LIVE, À CONFIRMER ou RETIRÉ.
3. **Search Console.** Un administrateur de l'espace : Spaces, Tools, Add
   Tool, Add MCP Server, adresse `https://seoskill.dev/mcp`, connexion avec le
   compte Google qui voit la Search Console.
4. **Google Drive** reconnecté avec les droits d'écriture : les agents
   remplissent le Sheet et créent le Google Doc.
5. **Ton site** comme source de connaissances « Websites ».
6. **Les 2 Skills** : Discover, Manage Skills, Create skill, From scratch.
   Pour Vérité produit, ajoute le contexte du site en connaissance.
7. **Les 5 agents** : importe les fichiers de `yaml/`, `@SEO-Chef` en dernier.
   Puis, pour chacun, ajoute dans Dust les outils et connaissances de sa fiche
   (Drive, Search Console, contexte du site, Run agent) : un import YAML
   n'apporte que la recherche web. Choisis le modèle conseillé.
8. **Les déclencheurs** : `@SEO-Veille` chaque lundi à 8 h, `@SEO-Suivi` le 1er
   du mois à 9 h avec le message « Fais le bilan du mois ».
9. **Premier essai** : `@SEO-Redacteur` marche seul. Envoie-lui « Écris un
   article sur … ». Puis « Écris le prochain article » à `@SEO-Chef`.

## Limites

- En test : essaie chaque agent seul avant de lancer la chaîne.
- Chaque appel d'agent consomme des crédits Dust, selon le modèle et les
  réglages de ton espace.
- `run_agent` va jusqu'à 4 niveaux d'appels : la chaîne en utilise 2.
- Le Suivi crée une Frame pour le bilan ; sans Frame, il rend des tableaux.

## Méthode et crédits

Inspiré des agents SEO de l'équipe de Dust (Davis Christenhuis, juin 2026),
du workflow de contenu de Ryan Law (Ahrefs, avril 2026), du guide
« Building always-on agents » d'Anthropic (13 novembre 2026) et du format
AGENTS.md. Voir `CREDITS.md` à la racine de l'agent.
