# Preuves : ce qu'on sait du SEO, et d'où ça vient

Chaque affirmation du pack sur Google, le SEO ou le droit a un **niveau de
preuve** et une **date de vérification**. Un fait absent de ce fichier porte
**[à vérifier]**. On le revérifie quand la date a plus de 6 mois.

| Niveau | Ce que c'est | Comment l'écrire |
|---|---|---|
| **Officiel** | documentation Google Search Central, texte de loi, documentation d'une plateforme | affirmé, avec la source |
| **Étude** | étude d'un éditeur d'outil ou d'un chercheur, avec méthode publiée | « selon [éditeur], [date], sur [échantillon] » ; jamais généralisé |
| **Praticien** | constat répété de professionnels, sans preuve publique | proposé comme repère ou option, jamais comme règle |
| **Folklore** | répété partout, contredit par la source officielle ou sans source | reconnu et nommé pour être écarté |

## 1. Contenu et qualité (officiel)

| Fait | Source | Vérifié le |
|---|---|---|
| Google n'a pas de nombre de mots préféré ; viser une longueur est un signal de contenu « pour les moteurs ». | Google, « Créer des contenus utiles, fiables et people-first » (version FR fournie, créée le 11 févr. 2026) | 12 oct. 2026 |
| Changer la date d'une page sans changement significatif, ou ajouter et supprimer en masse pour paraître « à jour », ne fonctionne pas. | même source | 12 oct. 2026 |
| E-E-A-T n'est pas un facteur de classement en soi ; la fiabilité est primordiale ; le poids est plus fort sur les sujets YMYL. | même source | 12 oct. 2026 |
| Qui, Comment, Pourquoi : signature attendue, dire comment le contenu est produit (y compris l'IA quand le lecteur peut se le demander), créer d'abord pour aider. L'automatisation pour manipuler le classement est du spam. | même source | 12 oct. 2026 |
| « Optimiser pour la recherche IA générative, c'est optimiser pour l'expérience de recherche, donc encore du SEO. » Pas besoin de fichiers pour l'IA, de Markdown, de découpage en petits morceaux ni d'écriture spéciale pour l'IA. Les données structurées ne sont pas requises pour la recherche IA. Contenu unique tiré d'une expérience réelle plutôt que contenu « commodité ». | developers.google.com/search/docs/fundamentals/ai-optimization-guide (mise à jour du 10 juil. 2026) | 12 oct. 2026 |
| Pour apparaître dans les fonctionnalités d'IA générative, le site doit y être inclus dans Search Console ; un rapport de performance « IA générative » existe. | même source | 12 oct. 2026 |
| Politiques anti-spam : contenu à grande échelle pour manipuler le classement, abus de réputation de site, domaines expirés, scraping, bourrage de mots-clés, texte caché, pages satellites, détournement du bouton retour (pratiques malveillantes)… | developers.google.com/search/docs/essentials/spam-policies (mise à jour du 28 août 2026) | 12 oct. 2026 |
| Les résultats enrichis FAQ n'apparaissent plus dans Google Search depuis le 7 mai 2026 ; documentation retirée le 15 juin 2026. Ne pas en promettre ; ne pas exiger de retirer un balisage existant. | Search Central, « Latest documentation updates » (entrées du 8 mai et du 15 juin 2026) | 12 oct. 2026 |

## 2. Title et meta description (officiel)

| Fait | Source | Vérifié le |
|---|---|---|
| Aucune limite de longueur pour `<title>` ; le lien de titre est tronqué selon la largeur de l'appareil. | developers.google.com/search/docs/appearance/title-link (mise à jour du 10 déc. 2025) | 12 oct. 2026 |
| Google peut réécrire le lien de titre à partir du `<title>`, du H1, de `og:title`, de textes mis en valeur, des ancres de liens. Il corrige les titres incomplets, périmés (année dépassée), non représentatifs, au gabarit répété, sans titre principal clair, ou en double avec le nom du site. | même source | 12 oct. 2026 |
| Bonnes pratiques de title : descriptif et concis, pas de bourrage, pas de gabarit répété, marque concise au début ou à la fin avec un séparateur, même langue que la page, un titre principal visible (H1). | même source | 12 oct. 2026 |
| Aucune limite de longueur pour la meta description ; elle est tronquée selon l'appareil. Google construit d'abord l'extrait à partir du contenu de la page et prend la description quand elle décrit mieux la page. | developers.google.com/search/docs/appearance/snippet (mise à jour du 20 avr. 2026) | 12 oct. 2026 |
| Descriptions identiques ou semblables sur toutes les pages : inutiles. Une liste de mots-clés : à éviter. Génération par programme acceptée si elle reste lisible et variée. | même source | 12 oct. 2026 |

## 3. Repères de praticiens (à présenter comme tels)

| Repère | Pourquoi on l'utilise | Niveau |
|---|---|---|
| Title visible jusqu'à environ 580-600 px sur ordinateur ; description d'environ 920 px sur ordinateur, moins sur mobile. | les largeurs changent avec l'interface de Google ; `meta.py` estime la largeur en pixels (police Arial) au lieu de compter les caractères | praticien |
| Title de 55 à 60 caractères, description de 150 à 160. | préférence de l'utilisateur (workflow), conservée comme réglage par défaut de `site-context.md` ; c'est la largeur en pixels qui décide | préférence |
| Réponse directe en 1 à 2 phrases en tête de section. | utile au lecteur pressé, aux extraits optimisés et aux réponses génératives ; aucun minimum ou maximum de mots officiel | praticien |
| Les pages en positions 8 à 20 sont les gains les plus rapides ; attendre 3 à 4 semaines entre deux changements ; arrêter après 2 tours sans effet. | marketingskills, `rankings-push.md` | praticien |
| Un lien contextuel dans le corps vaut mieux qu'un lien de pied de page. | tests publiés par SearchPilot (5 à 25% selon les tests) ; la « priorité au premier lien » n'est pas confirmée par Google | étude |

## 4. Folklore (à reconnaître et écarter)

- Densité de mots-clés à viser (1-3%), mots-clés « LSI ».
- Scores de lisibilité anglais (Flesch) appliqués au français.
- Nombre de mots minimum par type de page (« un article = 1 500 mots »).
- « Title jamais sous 50 caractères », « Google coupe la description aux
  guillemets ».
- Blocs de 40-60 ou 130-170 mots « pour être cité par l'IA », FAQ ou HowTo
  « pour l'IA », `llms.txt` comme levier Google.
- « 3× plus cité », « +121% de conversions », « 22× plus mémorisé » : chiffres
  d'éditeurs sans méthode publique.

## 5. Droit français (à vérifier sur Légifrance avant toute publication)

| Fait | Source | Statut |
|---|---|---|
| Publicité comparative (art. L. 122-1 et suivants du Code de la consommation) : licite si elle n'est pas trompeuse, compare des biens ou services répondant aux mêmes besoins, et compare objectivement des caractéristiques essentielles, pertinentes, vérifiables et représentatives (le prix peut en faire partie) ; l'annonceur doit pouvoir prouver l'exactitude de ses affirmations (art. L. 122-5). | synthèses de cabinets d'avocats (Gouache, CMS Francis Lefebvre) ; Légifrance inaccessible depuis l'outil le 12 oct. 2026 | **[à vérifier]** |
| Avis en ligne : toute personne qui collecte, modère ou publie des avis de consommateurs informe de façon loyale, claire et transparente sur leurs modalités de publication et de traitement (art. L. 111-7-2, loi du 7 oct. 2016) ; décret n° 2017-1436 (art. D. 111-16 à D. 111-19), en vigueur depuis le 1er janv. 2018 : date de l'avis, date de l'expérience, existence d'une procédure de vérification. | Légifrance (référence du décret), synthèse INC | **[à vérifier]** pour le texte consolidé |

## Règles (ce que le garde-fou applique)

1. **Refusé** : recopier ou « réécrire » le texte d'un concurrent pour le
   publier (scraping, spinning) ; faux avis, faux témoignages, faux auteurs,
   faux diplômes ou fausses certifications ; texte ou liens cachés ;
   bourrage de mots-clés ; achat ou échange de liens pour le classement,
   réseaux de sites (PBN), microsites IA qui renvoient vers le site ;
   pages satellites par ville sans contenu propre ; contenu généré en masse
   sans relecture pour occuper des requêtes ; détournement du bouton retour ;
   cloaking ; dates de mise à jour changées sans changement réel.
2. **Encadré** : génération de pages à grande échelle (portes de qualité,
   lots, relecture humaine) ; demande d'avis aux clients (à tous, sans
   filtrage, sans contrepartie) ; pages comparatives (preuves datées, cadre
   de la publicité comparative) ; contenu YMYL (sources nommées, aucun
   chiffre plausible inventé) ; mention de l'usage de l'IA.
3. **Autorisé** : tout le reste du travail éditorial et technique.
