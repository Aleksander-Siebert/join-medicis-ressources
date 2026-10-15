# Sources d'inspiration

Ce pack est né d'une méthode : lire en entier les Skills publicitaires
publics, garder ce qui marche, écarter ce qui n'a pas de source, puis
réécrire pour le français. Merci aux auteurs de ces projets :

- [chatgpt-ads-builder](https://github.com/fseixas/chatgpt-ads-builder), Softo (MIT) : l'entretien une question à la fois, les patrons de copie « contraste » et « preuve ancrée », réécrits en français avec la règle « preuve seulement si étayée » ; ses limites de 35 et 67 caractères sont écartées (contredites par le modèle d'import)
- [claude-ads](https://github.com/AgriciDaniel/claude-ads), AgriciDaniel (MIT) : la validation mécanique séparée du jugement, les règles de budget données comme des heuristiques et non comme des lois ; aucun fichier repris
- OpenAI, sources publiques relues le 15 octobre 2026 (voir `commun/faits.md`) : Help Center « Ads in ChatGPT: The Basics », règles publicitaires (Ad Policies, version 1.6 de septembre 2026), documentation développeur Ads (developers.openai.com/ads), annonce de l'ouverture européenne (août 2026)
- Le format du fichier d'import d'Ads Manager (onglets et noms de colonnes) : le pack fournit son propre modèle, `modele-import.xlsx`, sans reprendre le fichier d'OpenAI

Ce que le pack ajoute : la carte des intentions comme pivot, des context
hints écrits comme des situations et testés sur des prompts simulés, un
contrôle des allégations contre une liste étayée, un export XLSX sans
dépendance qui respecte le modèle (en-têtes, styles, ligne d'exemple
retirée), les niveaux de preuve et les points à confirmer dits comme tels,
et la typographie française comptée dans les limites.
