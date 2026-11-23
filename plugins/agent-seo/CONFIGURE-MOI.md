# Configure-moi

Ouvre ce dépôt dans une session sur claude.ai/code, puis colle le texte
ci-dessous. Compte 15 minutes. Tu ne remplis aucun fichier à la main.

---

Tu vas configurer l'agent SEO de ce dépôt. Lis d'abord `AGENTS.md`,
`config.json` et `site-context.md`.

Pose tes questions par groupes de 2 à 4, avec l'outil AskUserQuestion s'il
existe, sinon dans la conversation. Propose des choix quand c'est possible.
N'invente aucune adresse, aucun chiffre, aucune offre : uniquement ce que je
te donne ou ce que tu as lu sur mon site.

**1. Vérifie l'accès aux données Search Console.**

- Si un outil `seo_sites` (connecteur seoskill) est disponible, appelle-le et
  montre-moi les propriétés trouvées. Demande-moi laquelle suivre.
- Sinon, regarde s'il y a un export dans `donnees/`.
- Sinon, explique-moi les deux façons de faire, en suivant la partie
  « Données » de `README.md`, et attends que j'aie branché le connecteur ou
  déposé un export.

**2. Remplis `site-context.md` avec moi.**

Suis `/seo-context` (dans `.claude/skills/seo-context/`) avec l'adresse de
mon site. Il lit mon site, pose ses questions et remplit le fichier. Insiste
sur deux sections :

- §4, les pages à pousser : les articles mèneront vers elles ;
- §7, les données produit : seuls les faits marqués LIVE, avec leur source,
  pourront être écrits sur ma marque. Ce que je ne confirme pas reste
  À CONFIRMER.

**3. Règle `config.json`.**

- `marques` : le nom de ma marque et ses variantes (les requêtes de marque ne
  sont jamais proposées) ;
- `search_console.propriete` et `source` (`connecteur` ou `export`) ;
- `exclure` : les sujets que je ne veux pas (offres d'emploi, autre
  activité…) ;
- `ymyl` : `true` si je parle de santé, d'argent, d'assurance ou de droit ;
- `positions` et `min_impressions` : garde 8-40 et 20 sauf demande de ma part.

**4. Fais un premier passage, sans rien écrire.**

Suis `AGENTS.md`, étapes 1 à 3. Montre-moi les 5 premiers sujets et les
requêtes écartées parce qu'une page les couvre déjà. Demande-moi si le
classement me parle, et reporte mes retours dans `config.json` ou
`site-context.md`.

**5. Écris un premier article avec moi**, sur le sujet que je choisis, en
suivant `/seo-article` étape par étape (sans `--autonome`) : je valide le
plan avant la rédaction. Livre-le en `.md` et `.docx`.

**6. Enregistre tout dans le dépôt** : commit des fichiers de configuration,
de `sujets.md`, de `memoire/` et du dossier de l'article, puis push.

**7. Programme la veille hebdomadaire.** Donne-moi les étapes de
`README.md`, partie « Tous les lundis », avec le texte « planifié » de
`LANCER.md` à coller dans les instructions.

Termine par un récapitulatif : propriété suivie, pages à pousser, nombre de
faits LIVE, réglages, et comment changer tout ça plus tard.

---
