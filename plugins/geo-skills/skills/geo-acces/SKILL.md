---
name: geo-acces
description: >-
  Vérifie qui peut lire le site et pour en faire quoi : robots d'IA un par un
  selon leur rôle (recherche, visite d'un utilisateur, entraînement, jeton
  d'usage) avec la table datée d'OpenAI, Anthropic, Perplexity, Mistral,
  Google et Apple ; robots.txt lu selon la RFC 9309 ; noindex, nosnippet,
  max-snippet et data-nosnippet (conditions des Aperçus IA) ; texte présent
  sans JavaScript ; bloc robots.txt ajouté par Cloudflare ; Content-Signal ;
  appel avec le vrai user-agent pour voir un pare-feu ; réglage Search Console
  à vérifier. Propose un robots.txt par stratégie. Utilise-le pour « robots
  IA », « GPTBot », « bloquer ou autoriser les IA », « pourquoi ChatGPT ne
  voit pas mon site », « refuser l'entraînement », « llms.txt ». Pas pour la
  visibilité dans les réponses (/geo-visibilite) ni les agents qui remplissent
  des formulaires (/geo-agentic). Ne modifie jamais robots.txt.
---

# geo-acces

Avant tout travail de contenu, une question : les moteurs d'IA peuvent-ils
lire la page, et le site leur permet-il d'en faire ce qu'on croit ? La
confusion la plus répandue est de juger « citable dans ChatGPT » sur GPTBot,
qui ne sert qu'à l'entraînement. Ce Skill lit chaque robot pour ce qu'il
fait vraiment.

**À lire avant de commencer :** `commun/regles.md` et `commun/preuves.md`
(table des robots, vérifiée le 16 oct. 2026).

## 1. Le bon robot pour chaque affirmation

| Pour dire… | Regarde | Jamais |
|---|---|---|
| « citable dans la recherche de ChatGPT » | OAI-SearchBot | GPTBot |
| « citable dans la recherche de Claude » | Claude-SearchBot | ClaudeBot |
| « dans les résultats de Perplexity » | PerplexityBot | Perplexity-User |
| « dans la recherche de Vibe (Mistral) » | MistralAI-Index | MistralAI-Training |
| « éligible aux Aperçus IA et au Mode IA » | Googlebot, page indexable, extrait autorisé, site inclus dans Search Console | Google-Extended |
| « dans Copilot » | Bingbot | |
| « refuse l'entraînement » | GPTBot, ClaudeBot, MistralAI-Training, CCBot ; jetons Google-Extended et Applebot-Extended | les robots de recherche |

Google-Extended et Applebot-Extended **ne sont pas des robots** : ce sont
des jetons qui règlent l'usage de ce que Googlebot et Applebot ont déjà lu.
Les robots « utilisateur » (ChatGPT-User, Perplexity-User) peuvent ignorer
robots.txt : leurs éditeurs le disent.

## 2. Lancer le contrôle

```bash
python3 scripts/acces.py https://www.site.fr/page-importante/
python3 scripts/acces.py https://www.site.fr/page-importante/ --sonder --llms
python3 scripts/acces.py https://www.site.fr/x/ --robots robots.txt --html page.html   # hors ligne
```

Le script :

1. lit robots.txt selon la RFC 9309 : groupe du robot sinon `*`, règle la
   plus longue, Allow à égalité, jokers `*` et `$` ;
2. distingue « absent » (404, tout permis), « erreur serveur » (5xx, tout
   interdit) et « **non lu** » (erreur réseau du script, à vérifier) : il ne
   présente jamais une erreur réseau comme un fichier absent ;
3. lit la page : `noindex`, `nosnippet`, `max-snippet`, `data-nosnippet`
   (balise robots, balise googlebot, en-tête `X-Robots-Tag`), mots présents
   dans le HTML serveur, canonical ;
4. repère le bloc « Cloudflare Managed content » : Cloudflare l'ajoute au
   robots.txt servi, il n'est pas dans le fichier du site, et il bloque
   souvent les robots d'entraînement à l'insu du propriétaire ;
5. lit `Content-Signal` (`search`, `ai-input`, `ai-train`) : une préférence
   d'usage à respect volontaire, pas un contrôle d'accès ;
6. avec `--sonder`, appelle la page avec un navigateur puis avec le
   user-agent de chaque robot de recherche : « refusé au robot mais pas au
   navigateur » signale un pare-feu ou un CDN, **à confirmer** dans ses
   réglages (certains pare-feu refusent un faux user-agent mais acceptent le
   vrai robot, vérifié par son adresse IP).

Sans exécution de code : lis robots.txt groupe par groupe avec les mêmes
règles et écris « lecture manuelle ».

## 3. Ce que le script ne peut pas voir

- **Le réglage « Contrôle de l'IA générative dans la Recherche »** de
  Search Console (Paramètres) : inclure, exclure ou hériter. Un site exclu
  n'apparaît ni dans les Aperçus IA ni dans le Mode IA, quoi que dise
  robots.txt. Ce n'est ni un signal de classement ni un contrôle de
  l'entraînement. Demande à l'utilisateur de le vérifier.
- L'indexation réelle : rapport « Pages » de Search Console.
- Les vraies visites des robots : journaux du serveur (filtrer
  OAI-SearchBot, Claude-SearchBot, PerplexityBot, MistralAI-Index, et les
  robots « utilisateur »).

## 4. Choisir une stratégie

| Stratégie | Ce qu'elle fait | Pour qui |
|---|---|---|
| `visibilite` | tout autoriser, entraînement compris | marque qui veut être connue des modèles futurs |
| `equilibre` | recherche et visites autorisées, robots d'entraînement refusés, `Content-Signal: ai-train=no` | la plupart des entreprises |
| `refus-entrainement` | comme équilibre, plus les jetons Google-Extended et Applebot-Extended | éditeur de contenu qui protège ses textes |

```bash
python3 scripts/acces.py --proposer equilibre
```

Le bloc proposé ne remplace pas le robots.txt existant : il se fusionne
avec, ligne par ligne, et **l'utilisateur publie**. Avant de donner le code,
dis en une phrase ce qui change (règle 1 de `commun/regles.md`). Refuser
Google-Extended coupe aussi l'ancrage dans les applis Gemini : dis-le.

## 5. llms.txt

Rapporté, sans poids. Google dit que Search ne l'utilise pas (guide du
10 juillet 2026) ; aucun grand moteur de réponse n'a documenté qu'il le lit.
Utile pour un site de documentation lu par des agents de code. Ne le
présente jamais comme un levier de citation. Format et cas d'usage :
`references/robots-et-fichiers.md`.

## 6. La sortie (format fixe)

```
ACCÈS DES IA · https://assurly.example/blog/expat/ · robots.txt lu · table des robots du 2026-10-16

CE QUE ÇA VEUT DIRE
  citable dans la recherche de ChatGPT             OUI        OAI-SearchBot autorisé
  éligible aux Aperçus IA et au Mode IA de Google  NON        Googlebot autorisé ; extrait interdit (nosnippet)
  …
PAGE · statut 200 · 8 mots dans le HTML serveur
  CRITIQUE  nosnippet : meta robots (plus d'extrait, donc plus d'Aperçus IA ni de Mode IA)
ROBOT · ÉDITEUR · RÔLE · ACCÈS · RÈGLE (ligne) · SONDE
ENTRAÎNEMENT · refusé pour : GPTBot, ClaudeBot
CLOUDFLARE · bloc « Managed content » présent …
À VÉRIFIER HORS DU SITE · réglage « Contrôle de l'IA générative » de Search Console
```

Exemple fictif (fichiers de `evals/geo-acces/`). Traduis en 3 constats au
plus, chacun avec sa correction et son propriétaire.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| robots.txt « non lu » (erreur réseau, proxy) | Le dire ; demander le fichier, relancer avec `--robots`. Jamais « absent ». |
| Pare-feu anti-robots, page en 403 pour le script | Le dire ; demander le HTML (`--html`) ; `--sonder` montre qui est refusé. |
| Site de plus de 500 pages | Contrôler les gabarits (accueil, offre, article, catégorie), pas toutes les pages. |
| L'utilisateur veut « bloquer toutes les IA » | Expliquer ce qu'il perd (citation dans ChatGPT, Perplexity, Vibe), proposer `refus-entrainement`. |
| Bloc Cloudflare non voulu | Réglage dans Cloudflare (Security, Bots), pas dans le fichier du site. |
| Robot inconnu de la table | Ne rien affirmer ; vérifier la documentation de l'éditeur, proposer d'ajouter la ligne datée à `commun/robots_ia.json`. |
| Table des robots de plus de 60 jours | Le dire en tête de sortie ; procédure dans `commun/preuves.md`. |

## Ressources

- `scripts/acces.py` · `commun/robots_rfc.py` · `commun/robots_ia.json` ·
  `commun/page.py`
- `references/robots-et-fichiers.md` : table commentée, stratégies,
  llms.txt, Content-Signal, journaux du serveur.

## Skills liés

`/geo-visibilite` (mesurer la présence après une correction),
`/geo-agentic` (agents qui agissent sur le site), `/geo-audit` (diagnostic
complet), `/seo-audit` (indexation et technique, pack SEO).

## Règles du pack

- Lecture seule : robots.txt, pare-feu et Search Console restent à
  l'utilisateur.
- Zéro invention : un robot ou un comportement absent de la table porte
  [à vérifier].
- Texte simple dans la conversation, sans créer de document.
