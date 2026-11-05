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

Ce que nous ajoutons :
- dates vérifiées par script ;
- mémoire de 90 jours, enregistrée seulement après envoi ;
- regroupement des doublons avec toutes leurs sources ;
- suivi des pages tarifs ligne à ligne ;
- contrôle bloquant des sources dans le mail ;
- protection contre les instructions cachées dans les pages ;
- mail « rien de neuf » honnête ;
- configuration guidée en français ;
- version cloud.
