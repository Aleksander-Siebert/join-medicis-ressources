# Crédits

Ce pack est une synthèse. Il a été construit en décortiquant les meilleurs
Skills LinkedIn open-source, en gardant le meilleur de chacun, puis en le
réécrivant pour le français, le marché français et ses règles.

| Source | Licence | Ce qu'on a repris | Ce qu'on a changé |
|---|---|---|---|
| [Jake Schincariol, linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill) | MIT | L'architecture : 11 commandes `/li-*` (renommées `/linkedin-*` ici), le fichier de voix partagé, le journal, le refus de publier et d'inventer, les 21 formules d'accroche (`hooks.json`), la grille de profil sur 100, la structure des deux scripts de l'humaniseur | Tout traduit et réécrit en français. Humaniseur refait pour le français (son original casse la typographie française et note 33/100 un texte français correct). Grille de profil repondérée vers les expériences chiffrées. Ajout de `/linkedin-job` |
| [Serge Bulaev, linkedin-skills](https://github.com/sergebulaev/linkedin-skills) | MIT | Le choix des accroches par objectif (commentaires, partages, likes, enregistrements), la règle de densité des tics (un contraste, une triade par post), la Story Bank devenue « Preuves utilisables » dans `voix.md` | Aucune dépendance à des API tierces (publication, extraction de données, images) |
| [Marian Kamenistak, linkedin-post-writing-skill](https://github.com/marian-kamenistak/linkedin-post-writing-skill) | MIT | La calibration de la voix à partir de ses propres posts, la passe « qu'est-ce qui sonne encore IA ? » | Méthode intégrée à `voix.md` et à `/linkedin-human` |
| [Corey Haines, marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT | Le principe « lire le contexte produit d'abord », les structures de carrousel | Le contexte vient de `voix.md` ou du Growth Context de Join Médicis |
| [alxbd, Boileau](https://github.com/alxbd/boileau), dérivé de [Siqi Chen, humanizer](https://github.com/blader/humanizer) | MIT | Les 38 marqueurs d'écriture IA en français (lexique, faux registre soutenu, calques de l'anglais, typographie française cassée…) | Condensés dans `marqueurs-ia-fr.md` et `tics-ia.json`, avec les tics propres à LinkedIn |
| [Wikipédia, Aide:Identifier l'usage d'une IA générative](https://fr.wikipedia.org/wiki/Aide:Identifier_l%27usage_d%27une_IA_g%C3%A9n%C3%A9rative) | CC BY-SA (source d'inspiration, pas de texte repris) | La liste de référence des signes d'écriture IA, et la règle de prudence : un signe isolé ne prouve rien | Rien n'est copié : les marqueurs sont reformulés et illustrés par des exemples LinkedIn |
| [kvsdileep, linkedin-writer](https://github.com/kvsdileep/linkedin-writer) | MIT annoncée dans le README | Idées seulement : afficher le nombre de caractères, l'export en texte brut prêt à coller | Réécrit |
| [Attainment, linkedin-algorithm-skill](https://github.com/attainmentlabs/linkedin-algorithm-skill) | « Libre d'utilisation », sans licence formelle | Idée seulement : marquer chaque affirmation sur l'algorithme d'un niveau de confiance | Réécrit : **[données à grande échelle]**, **[estimation de praticien]**, **[à vérifier]** |

Merci à leurs auteurs. Les mentions de copyright exigées par la licence MIT
sont reproduites dans [`LICENSE`](LICENSE).

## Ce que le pack ajoute

- Un humaniseur **français** : typographie française respectée, lexique tiré
  de Wikipédia FR et de Boileau, contrôle de la « voix » adapté au français
  (« on », « ça », « j' » au lieu des contractions anglaises).
- `/linkedin-job` : recherche d'offres en requêtes booléennes et URL limitée à la
  dernière heure.
- `/linkedin-profile` centré sur les réalisations chiffrées « X / Y / Z », avec les
  questions pour faire sortir les chiffres sans jamais les inventer.
- Le cadre français : mention « Collaboration commerciale » (loi du 9 juin
  2023), règles CNIL de prospection B2B, RGPD, accord des personnes citées.
- Une boucle d'apprentissage contrôlée : `apprentissages.md`, validé par
  l'utilisateur, relu par tous les Skills.
