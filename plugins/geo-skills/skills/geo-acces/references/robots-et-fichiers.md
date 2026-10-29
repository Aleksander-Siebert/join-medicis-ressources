# Robots, jetons et fichiers pour les IA

Table complète et datée : `commun/preuves.md` §1 (même contenu que
`commun/robots_ia.json`). Sources : pages officielles d'OpenAI, Anthropic,
Perplexity, Mistral, Google et Apple, lues le 16 octobre 2026.

## 1. Quatre rôles, quatre conséquences

| Rôle | Exemples | Bloquer revient à… |
|---|---|---|
| Recherche (index d'un moteur de réponse) | OAI-SearchBot, Claude-SearchBot, PerplexityBot, MistralAI-Index | disparaître des réponses avec recherche web de ce moteur |
| Visite d'un utilisateur | ChatGPT-User, Claude-User, Perplexity-User, MistralAI-User | empêcher l'IA d'ouvrir la page quand un client le lui demande ; certains ignorent robots.txt |
| Entraînement | GPTBot, ClaudeBot, MistralAI-Training, CCBot | sortir des données d'entraînement futures ; aucun effet direct sur la recherche |
| Jeton d'usage (pas de robot) | Google-Extended, Applebot-Extended | interdire un usage (entraînement, ancrage Gemini) de ce que Googlebot ou Applebot ont lu ; aucun effet sur Google Search ni sur Spotlight |

Moteurs classiques : Googlebot (Google Search, donc Aperçus IA et Mode IA),
Bingbot (Bing et Copilot), Applebot (Spotlight, Siri, Safari, et aussi
réponses générées d'Apple ; `nosnippet` en refuse l'usage).

## 2. Les erreurs qu'on voit le plus

- Juger la présence dans ChatGPT sur GPTBot (c'est OAI-SearchBot).
- Bloquer Google-Extended pour « sortir des Aperçus IA » : sans effet ; les
  Aperçus IA dépendent de Googlebot, de l'extrait autorisé et du réglage
  Search Console.
- Croire qu'un `Disallow: /` dans `*` couvre un robot qui a son propre
  groupe : le groupe propre remplace `*` (RFC 9309).
- Lire avec un outil qui applique la première règle (module `robotparser`
  de Python) : « Disallow: / » puis « Allow: /blog/ » bloque /blog/ à tort.
- Prendre une erreur réseau de l'outil pour un robots.txt absent.
- Oublier le bloc ajouté par Cloudflare, invisible dans le fichier du site.

## 3. Content-Signal

Politique publiée par Cloudflare : une ligne dans robots.txt,
`Content-Signal: search=yes, ai-input=yes, ai-train=no`.

| Clé | Usage visé |
|---|---|
| `search` | index de recherche et liens, sans résumé d'IA |
| `ai-input` | contenu donné à un modèle pour répondre (RAG, ancrage) |
| `ai-train` | entraînement ou ajustement de modèles |

Préférence à respect volontaire, présentée comme réserve de droits
(directive (UE) 2019/790, art. 4). Ce n'est pas un contrôle d'accès : seul
`Disallow` empêche la lecture. Statut du brouillon IETF [à vérifier].

## 4. llms.txt

Proposition de Jeremy Howard (llmstxt.org, sept. 2024) : un fichier
Markdown à la racine qui résume le site et liste ses pages clés.

- Google Search ne l'utilise pas (guide « AI optimization », 10 juil. 2026).
- Aucun grand moteur de réponse n'a documenté qu'il le lit pour citer.
- Utile pour une documentation de produit lue par des agents de code.
- Format minimal : `# Nom`, `> résumé`, sections `##` avec des liens
  Markdown. Le pack ne lui donne aucun point.

## 5. Les journaux du serveur

La meilleure preuve qu'un moteur lit le site. Filtre les user-agents de la
table et compte, par robot et par section : visites, codes de réponse (403,
429, 5xx), pages lues. Un robot de recherche qui ne reçoit que des 403
révèle un pare-feu. Vérifie l'identité d'un robot par ses plages d'adresses
publiées (OpenAI, Anthropic, Google) avant de conclure : un user-agent se
falsifie.
