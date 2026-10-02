---
name: geo-crawlers
description: >-
  Vérifie que les robots d'IA (OpenAI, Anthropic, Perplexity, Google,
  Mistral, Apple, Meta…) peuvent lire le site : robots.txt robot par robot,
  directives noai et noindex, contenu lisible sans JavaScript, fichier
  llms.txt. Propose un robots.txt selon la stratégie choisie (visibilité,
  équilibre, blocage) et un brouillon de llms.txt. Utilise-le pour « robots
  IA », « GPTBot », « llms.txt », « bloquer ou autoriser les IA ».
---

# geo-crawlers

Un site que les robots d'IA ne peuvent pas lire ne sera pas cité. Beaucoup de
sites bloquent ces robots sans le savoir (règle de sécurité, CDN, plugin).

## Trois familles de robots

| Rôle | Exemples | Effet d'un blocage |
|---|---|---|
| **Recherche** | OAI-SearchBot, Claude-SearchBot, PerplexityBot | le site n'apparaît plus comme source dans les réponses avec recherche web |
| **Utilisateur** | ChatGPT-User, Claude-User, Perplexity-User, MistralAI-User | l'IA ne peut plus lire une page quand un utilisateur le lui demande |
| **Entraînement** | GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot | le contenu ne sert plus à entraîner les modèles ; effet indirect sur la notoriété de la marque dans les modèles |

À savoir : les **AI Overviews et l'AI Mode de Google** utilisent Googlebot.
Bloquer Google-Extended ne retire pas un site des AI Overviews ; bloquer
Googlebot le retire de Google. Pour y apparaître, une page doit être
indexée et **éligible à l'extrait** : `nosnippet` ou `max-snippet:0` l'en
excluent. Le site ne doit pas non plus être exclu des fonctionnalités d'IA
générative dans Search Console. La liste des robots change souvent :
**[à vérifier]** dans la documentation de chaque éditeur avant de modifier
un robots.txt.

## Avec exécution de code

```bash
python3 crawlers.py https://www.site.fr --chemin /blog/
python3 crawlers.py https://www.site.fr --robots-propose equilibre
python3 crawlers.py https://www.site.fr --llms-propose --nom "Assurly" --resume "Courtier en assurance santé internationale."
```

Sans exécution de code : lis `https://site/robots.txt` et `/llms.txt`, et le
code source de la page (meta robots).

## La stratégie (décision de l'utilisateur)

- **Visibilité** : tout autoriser. Pour la plupart des marques qui veulent
  être recommandées.
- **Équilibre** : bloquer l'entraînement, autoriser recherche et utilisateurs.
  Pour les éditeurs qui protègent leur contenu mais veulent être cités.
- **Blocage** : tout bloquer. Pour un contenu payant ou sensible ; la marque
  disparaît alors des réponses avec recherche.

Explique les conséquences, laisse l'utilisateur choisir, puis donne le bloc
robots.txt à coller. Rappelle de vérifier aussi le pare-feu ou le CDN
(Cloudflare peut bloquer les robots d'IA par défaut).

## llms.txt

Un fichier Markdown à la racine (`/llms.txt`) qui présente le site aux
assistants : `# Nom`, `> résumé`, puis des sections `##` avec des liens vers
les pages clés. C'est une proposition communautaire (llmstxt.org).

- **Google l'ignore** : son guide officiel dit qu'aucun fichier pour l'IA
  n'est nécessaire pour apparaître dans Google Search, et que ces fichiers
  n'aident ni ne nuisent (https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).
- Aucun autre grand éditeur n'a confirmé l'utiliser pour choisir ses sources.
- Lighthouse le vérifie dans sa catégorie « Agentic Browsing » (voir
  `/geo-agentic`) : il peut servir aux agents qui naviguent sur le site.

Il ne compte dans aucun score du pack. Propose-le comme une option peu
coûteuse, jamais comme un levier de visibilité.

## Sortie

```
ROBOTS D'IA · assurly.example
BLOQUÉS SANS LE SAVOIR : PerplexityBot, Claude-SearchBot (règle « User-agent: * Disallow: /api » trop large)
DIRECTIVES : aucune restriction (ni noindex, ni nosnippet) · 1 084 mots lisibles sans JavaScript
LLMS.TXT : absent (sans effet sur Google) → brouillon ci-dessous si vous le souhaitez
STRATÉGIE CONSEILLÉE : visibilité (marque qui veut être recommandée)
```

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : ne déclare pas un robot bloqué ou autorisé sans avoir lu
  le robots.txt.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est modifié sur le site par le Skill.
