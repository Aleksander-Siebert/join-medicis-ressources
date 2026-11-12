# Méthode et crédits

L'agent est une création Join Médicis. Avant de l'écrire, nous avons lu neuf
exemples d'agents de veille (5 novembre 2026), dont un en entier (code,
tests, CHANGELOG). Aucun texte ni code n'a été recopié.

- [Luciole](https://github.com/josuerochadev/luciole), Josué Xavier Rocha
  et son équipe (MIT) :
  - le pipeline collecte, filtre, enrichissement et digest ;
  - le dédoublonnage par similarité de titres ;
  - le seuil de pertinence et la limite du nombre d'articles par envoi.

  Nous avons écarté la base de données, le RAG et l'interface web, trop
  lourds pour un débutant. Nous avons aussi corrigé un défaut : en cas
  d'erreur de l'IA, Luciole garde une note moyenne et laisse passer
  l'article.
- Journal du Net, « Créer son agent IA pour automatiser sa veille » :
  la note de pertinence, le prompt en trois parties (contexte, objectif,
  format) et le mail trié par score. Cet exemple n'a pas de vrai
  dédoublonnage et confie la récence à l'IA : nous le faisons par script.
- ANCT, Les Bases, « Automatisez votre veille avec l'IA » : le parcours
  pas à pas pour non-techniciens, commencer avec 2 ou 3 sources.
- AI Discipline (Maven), « Créer son agent de veille concurrentielle » :
  la mémoire qui détecte ce qui est nouveau, la synthèse du lundi.
- French Tech Bordeaux, cas d'usage « Veille par IA personnalisée » :
  le mail du lundi, chaque info avec sa source vérifiable.
- Samuel Braniste (LinkedIn), agent Dust de veille : le format par info
  (résumé, source, impact, priorité).
- Swiftask et Sindup : pages lues, rien de technique à reprendre.
- Un fil Reddit (r/AI_Agents) n'a pas pu être lu (accès refusé aux robots).

Pour la version 2 (12 novembre 2026), nous avons cloné 20 dépôts publics et
lu chaque fichier des plus proches. Aucun texte ni code n'a été recopié. La
matrice complète est dans `recherche/agent-veille-v2/MATRICE.md` du dépôt
Join Médicis.

- [competitor-watch](https://github.com/muguang1224/competitor-watch),
  muguang1224 (MIT) : la comparaison clé par clé d'une réponse JSON
  publique, et le principe « public seulement, sans connexion ».
- [compete](https://github.com/yassnemo/compete), Yassine Erradouani (MIT) :
  le respect de `robots.txt` et du délai demandé par le site, et la lecture
  des offres d'emploi par les API publiques de Greenhouse, Lever et Ashby.
- [changedetection.io](https://github.com/dgtlmoon/changedetection.io),
  dgtlmoon (Apache 2.0) : la consigne en langage courant par page suivie,
  le texte à ignorer et les mots déclencheurs.
- [daybrief](https://github.com/valuationgeek/daybrief), valuationgeek
  (MIT) : les garde-fous pour tourner sans surveillance (refus du réseau
  local, jamais deux envois), le diagnostic par étape, et la détection des
  sujets qui montent par comparaison à la fréquence habituelle.
- [Vigil-Agent](https://github.com/gpavan1992/Vigil-Agent), gpavan1992
  (sans licence : idées seulement) : la note calculée par une règle écrite
  et la mémoire des tendances d'une veille à l'autre.
- [startup-skill](https://github.com/ferdinandobons/startup-skill),
  Ferdinando Bons (MIT), et [UnifAPI Agents](https://github.com/unifapi-agent/agents)
  (MIT) : la distinction entre ce qui est confirmé et ce qui est déduit.
- [news-recap](https://github.com/andgineer/news-recap), Andrey Sorokin
  (MIT) : lire l'article quand le titre ne dit rien.

Écartés après analyse : les bases de données et tableaux de bord (trop
lourds à installer), les sous-agents spécialisés (coût sans gain démontré),
et les navigateurs conçus pour ne pas être détectés (Camoufox et ses
serveurs MCP), contraires à notre règle de ne contourner aucune protection.

Ce que nous ajoutons :
- dates vérifiées par script ;
- mémoire de 90 jours, enregistrée seulement après envoi ;
- regroupement des doublons avec toutes leurs sources ;
- suivi des pages tarifs ligne à ligne ;
- contrôle bloquant des sources dans le mail ;
- protection contre les instructions cachées dans les pages ;
- mail « rien de neuf » honnête ;
- configuration guidée en français ;
- version cloud ;
- veille stratégique sur sources officielles françaises et européennes
  (BOAMP, TED, CNIL, DGCCRF, EUR-Lex) ;
- deux modes de collecte, dont un sans aucun agrégateur ;
- trois formats de mail et quatre destinations, réglables par la
  conversation ;
- fonctionnement sans Python, et tests sur Windows, macOS et Linux.
