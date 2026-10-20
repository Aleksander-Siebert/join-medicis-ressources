# Notre méthodologie

Les skills Join Médicis sont une production 100% Join Médicis, conçue à la main.

Nous sommes partis d'un constat simple, la majorité des prompts et agents disponibles aujourd'hui sont pensés pour le marché américain, restent trop généralistes et se cassent souvent les dents sur les règles d'une plateforme publicitaire toute neuve (les bonnes pratiques qui circulent sur ChatGPT Ads se contredisent, et certains secteurs n'y sont pas admis hors des États-Unis).

Pour créer ce pack, nous n'avons pas fait de simple compilation. Notre processus repose sur la rétro-ingénierie :
- Analyse de l'écosystème : Nous décortiquons la logique des meilleurs skills mondiaux.
- Rétro-ingénierie : Nous isolons les mécaniques qui performent réellement (architecture des pipelines, boucles de qualité, logique de raisonnement, scripts, etc.).
- Reconstruction & expertise : Nous recréons entièrement le skill en y injectant notre expérience de terrain, nos propres workflows et notre contexte métier.
- Localisation experte : Nous calibrons chaque instruction pour les nuances de la langue française, les règles/réglementations locales et la rigueur de rédaction anti-hallucination indispensable aux différents secteurs.

Le résultat ? Ce que ce pack vous apporte en exclusivité : une campagne ChatGPT Ads pensée pour la France, une éligibilité vérifiée selon les règles d'OpenAI avant d'écrire, des annonces dont chaque promesse a une source, et un fichier d'import contrôlé par script qui n'est écrit que s'il est importable.

# Transparence & inspirations
Bien que le code et les directives de chaque skill soient une création propre à Join Médicis, nous croyons en la culture open-source. Nos travaux de R&D s'appuient sur l'analyse et la compréhension d'excellents projets internationaux.

Nous tenons à remercier et créditer les auteurs des projets suivants, qui ont nourri notre réflexion :

- [chatgpt-ads-builder](https://github.com/fseixas/chatgpt-ads-builder), Softo (MIT) : l'entretien une question à la fois, les patrons de copie « contraste » et « preuve ancrée », réécrits en français avec la règle « preuve seulement si étayée » ; ses limites de 35 et 67 caractères sont écartées (contredites par le modèle d'import)
- [claude-ads](https://github.com/AgriciDaniel/claude-ads), AgriciDaniel (MIT) : la validation mécanique séparée du jugement, les règles de budget données comme des heuristiques et non comme des lois ; aucun fichier repris
- OpenAI, sources publiques relues le 15 octobre 2026 (voir `commun/faits.md`) : Help Center « Ads in ChatGPT: The Basics », règles publicitaires (Ad Policies, version 1.6 de septembre 2026), documentation développeur Ads (developers.openai.com/ads), annonce de l'ouverture européenne (août 2026)
- Le format du fichier d'import d'Ads Manager (onglets et noms de colonnes) : le pack fournit son propre modèle, `modele-import.xlsx`, sans reprendre le fichier d'OpenAI
- [openai-ads-mcp](https://github.com/avyanshkatiyar/openai-ads-mcp), Avyansh Katiyar (MIT) : l'idée d'un client d'API à transport remplaçable pour tester sans réseau, et la règle « ne jamais deviner un identifiant » ; aucun fichier repris (ses contrôles, écrits pour la documentation de juin 2026, refusent des campagnes au clic aujourd'hui valides)
- [NotFair](https://github.com/nowork-studio/NotFair), Toprank Contributors (MIT) : les statuts d'un livrable (brouillon, prêt à relire) et le registre de règles daté ; aucun fichier repris
- OpenAI, sources publiques relues le 20 octobre 2026 : règles publicitaires v1.6 du 10 septembre 2026 (texte français, synthèse complète dans `commun/politiques-openai.md`), documentation développeur Ads (journal des modifications au 30 septembre 2026), Bulk API, ciblage, audiences personnalisées et consentement du pixel
- Le schéma d'annonces à 10 colonnes fourni par l'utilisateur le 20 octobre 2026 : le pack écrit ses propres classeurs à ce format

Ce que le pack ajoute : la spécialisation France (règles d'OpenAI et droit
français datés, pas de personnalisation dans l'EEE, consentement du pixel),
l'alerte suivie du travail pour les secteurs restreints, la montée en
volume par lots contrôlés, la reprise d'exports Google, Meta et Microsoft
Ads, la recherche d'identifiants en lecture seule, le contrôle cellule par
cellule du classeur d'import, la carte des intentions comme pivot, des context
hints écrits comme des situations et testés sur des prompts simulés, un
contrôle des allégations contre une liste étayée, un export XLSX sans
dépendance qui respecte le modèle (en-têtes, styles, ligne d'exemple
retirée), les niveaux de preuve et les points à confirmer dits comme tels,
et la typographie française comptée dans les limites.

Les mentions de copyright exigées par la licence MIT sont reproduites dans
[`LICENSE`](LICENSE).
