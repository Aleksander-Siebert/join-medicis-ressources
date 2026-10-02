# Consignes pour Claude : création de Skills Join Médicis

Ce dépôt publie les Skills open-source de Join Médicis (joinmedicis.com), un
site pour les marketeurs francophones. Le propriétaire est Aleksander Siebert.
Ces consignes s'appliquent **chaque fois qu'on te demande de créer, refaire
ou améliorer des Skills**.

## L'objectif

Des Skills **S-tier** qui font gagner du temps, de l'argent et de l'énergie
sur de vraies tâches marketing. **La profondeur passe avant la couverture.**
Mieux vaut 6 Skills excellents que 20 Skills moyens. La barre est celle des
meilleurs Skills Claude, toutes langues confondues. Le français et le marché
français sont le terrain, pas le seul critère.

## Le processus (à suivre dans l'ordre, sans sauter d'étape)

1. **Collecte complète.** Clone chaque dépôt de référence en entier
   (`git clone --depth 1`, ça fonctionne) : ceux fournis par l'utilisateur, et
   d'autres dépôts bien notés trouvés sur GitHub pour comparer. Inventaire de
   **chaque fichier** : SKILL.md, references, assets, modèles, exemples,
   scripts, agents, hooks, extensions, tests, docs, CHANGELOG, issues.
   **Ne jamais travailler depuis les seuls README** (erreur de la v1 des
   packs SEO et GEO, octobre 2026 : 17 SKILL.md lus sur 446 fichiers).
2. **Dissection fichier par fichier.** Pour chaque Skill de chaque dépôt :
   - comment il se déclenche ;
   - ses étapes ;
   - ses grilles, exemples et cas limites ;
   - ce que font réellement ses scripts (les lire et les exécuter) ;
   - ce qui marche, ce qui est fragile, ce qui manque.

   Le CHANGELOG et les issues montrent les bugs et les cas limites réels.
3. **Matrice de capacités par Skill.** Chaque fonction trouvée devient une
   ligne avec :
   - la source précise (dépôt, fichier) ;
   - le verdict : reprendre, améliorer, ou écarter avec la raison ;
   - ce que nous ajoutons (expertise de l'utilisateur, marché français, RGPD).
4. **Comparaison** avec les Skills Join Médicis existants : ce qui leur manque,
   honnêtement.
5. **Point de validation avec l'utilisateur, avant d'écrire.** Présente les
   matrices et la liste des Skills prévus, avec ce que chacun fera. Attends
   sa validation.
6. **Rédaction en profondeur, Skill par Skill.** Commence par un Skill modèle
   que l'utilisateur relit, puis applique ce gabarit aux autres. Chaque Skill
   est livré complet : SKILL.md, references, modèles, exemples, scripts et
   tests.
7. **Validation :**
   - tests automatiques des scripts ;
   - comparaison **à l'aveugle** avec la référence sur des tâches réelles,
     fournies de préférence par l'utilisateur ;
   - chaque ligne de la matrice est soit faite, soit écartée avec une raison ;
   - les faits sont revérifiés aux sources primaires, avec leur date ;
   - les résultats sont publiés, défaites comprises (`evals/RESULTATS.md`).
8. **Publication :** ce dépôt, les fiches du site `join-medicis`, les ZIP
   claude.ai, puis une PR sur chaque dépôt.

Donne des points d'avancement courts. Prends le temps nécessaire : plusieurs
sessions par pack, c'est normal.

## La grille S-tier (chaque Skill doit la passer)

- **Déclenchement** : la description dit précisément quand l'utiliser et quand
  ne pas l'utiliser (1 024 caractères au plus).
- **Profondeur** : grilles de contrôle complètes, cas limites et exemples
  réels d'entrée et de sortie. Les détails vont dans `references/`, lus à la
  demande, pour que le SKILL.md reste lisible.
- **Mesure** : un script testé pour tout ce qui se mesure (Python sans
  dépendance si possible), séparé de ce qui relève du jugement.
- **Données** : pour chaque connecteur (Search Console, GA4, Semrush, Ahrefs,
  HubSpot…), quoi récupérer et comment, avec un mode gratuit par défaut.
- **Erreurs et limites** : que faire si le site est inaccessible, bloqué, trop
  gros, ou si une donnée manque.
- **Sources** : primaires et datées. Une affirmation non vérifiée porte
  **[à vérifier]**.
- **Sortie** : format normé, comparable dans le temps.
- **Preuves** : tests et éval comparative.

## Règles de l'utilisateur (permanentes)

- **Zéro invention** : aucun chiffre, prix, délai, condition, source ou
  réponse d'IA inventé. Ce qui manque devient `{{à compléter}}`.
- **Rien n'est publié** ni modifié à la place de l'utilisateur.
- **Typographie française** :
  - pourcentage collé au nombre (« 15% ») ;
  - tiret cadratin supprimé, ou remplacé **uniquement par une virgule**,
    jamais par un point-virgule ;
  - espaces avant `: ; ! ?` et guillemets « ».
- **Ton** : style affirmatif, pas de remplissage, pas de tics d'IA.
- **Sortie par défaut** : texte simple dans la conversation, sans créer de
  document, pour économiser les tokens. Markdown si nécessaire.
- **Nommage** : préfixe par pack (`/linkedin-*`, `/seo-*`, `/geo-*`).
- **Exemples** : anonymisés. L'exemple d'entreprise est « Assurly »
  (assurly.example), jamais un vrai client.
- **Crédits** : une liste sobre dans CREDITS.md. Mentions de licence MIT dans
  LICENSE. Un dépôt sans licence n'est pas copié : on s'en inspire et on
  réécrit.

## Mécanique du dépôt

- Un dossier par pack :
  - `skills/<nom>/SKILL.md` et ses fichiers ;
  - `.claude-plugin/plugin.json` ;
  - `claude-ai/SKILL.md` (routeur) et `claude-ai/build.sh` ;
  - `templates/` ;
  - `evals/` ;
  - `README.md`, `CREDITS.md`, `LICENSE`.
- Marketplace racine : `.claude-plugin/marketplace.json` (nom `join-medicis`).
- claude.ai refuse plusieurs SKILL.md et le manifeste de plugin :
  `claude-ai/build.sh` construit un ZIP avec un seul SKILL.md, et les modules
  sont rangés dans `modules/<nom>/`.
- Site (`Aleksander-Siebert/join-medicis`, branche `master`) :
  - un fichier par pack dans `src/lib/` (`linkedin-pack.ts`, `seo-pack.ts`,
    `geo-pack.ts`, outil commun `skill-pack.ts`) ;
  - `scripts/sync-skill-packs.sh ../join-medicis-ressources` copie les
    fichiers et construit les ZIP ;
  - vérifier avec `npx tsc --noEmit` et `npm run build` (`next lint` est
    cassé depuis Next 16).
- Avant de publier : frontmatter valide, bundle claude.ai construit, tous les
  tests au vert.
