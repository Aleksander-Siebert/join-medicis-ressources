# Agent SEO : du mot-clé à l'article

Un agent IA gratuit et open-source qui lit tes vraies données Search Console,
trouve les articles qui manquent à ton site, et en écrit un, du mot-clé au
brouillon relu, en Markdown et en Word. Il tourne sur claude.ai/code, sans
rien installer, à la demande ou chaque semaine. Modèle Join Médicis, licence
MIT.

> Statut : en test (novembre 2026). Ce qui n'a pas encore été essayé en
> conditions réelles est listé en bas de cette page.

## Ce qu'il fait

1. **Trouve les sujets dans tes données**, pas dans une liste d'idées
   générique : les requêtes où ton site est presque visible (positions 8 à 40),
   regroupées quand elles veulent la même page, sans tes requêtes de marque,
   sans ce qu'une de tes pages couvre déjà, sans ce qu'il a déjà écrit.
   Classées par impressions réelles et potentiel de la position.
2. **Écrit l'article** avec `/seo-article` du pack SEO Join Médicis :
   mots-clés, SERP, plan, rédaction, contrôles, maillage, en étapes
   enregistrées qu'on peut reprendre.
3. **Contrôle avant de livrer** :
   - rien sur ta marque qui ne soit une donnée LIVE de `site-context.md`
     (`scripts/verite.py`) ;
   - chaque chiffre vérifié en ouvrant sa source ;
   - aucune affirmation sans source en mode YMYL (santé, argent, assurance,
     droit) ;
   - pas de tics d'écriture IA.
4. **Livre un brouillon** : `article.md`, `article.docx`, le tableau
   « affirmation → source », la liste des trous `{{à compléter}}` et des
   hypothèses. Rien n'est publié.
5. **Se souvient** de ce qu'il a proposé, écrit ou abandonné, et fait le bilan
   des articles livrés après 28 jours.

## Ce qu'il faut

- Une offre Claude qui donne accès à claude.ai/code (Pro ou plus).
- Un compte GitHub gratuit : l'agent vit dans un dépôt privé.
- L'accès à la Search Console de ton site.

## Installer en 15 minutes

1. **Copie l'agent dans un dépôt privé.** Sur la page GitHub de l'agent :
   « Use this template » → « Create a new repository », visibilité
   « Private ». Sans ce bouton : télécharge le dossier et pousse-le dans un
   nouveau dépôt privé. Le dépôt contiendra le contexte de ton site : ne le
   rends jamais public.
2. **Ouvre claude.ai/code**, connecte GitHub si ce n'est pas fait, et
   choisis ce dépôt.
3. **Branche Search Console** (partie « Données » ci-dessous).
4. **Colle le texte de `CONFIGURE-MOI.md`** dans la session. L'agent remplit
   le contexte de ton site avec toi, te montre ses premiers sujets et écrit
   un premier article que tu valides étape par étape.

## Données

**Par défaut, le connecteur seoskill.dev.** Un serveur MCP gratuit et
open-source (Apache 2.0) qui lit Search Console avec ta connexion Google, en
lecture seule.

1. Sur claude.ai : Paramètres → Connecteurs → ajouter un connecteur
   personnalisé, adresse `https://seoskill.dev/mcp` **[à vérifier : libellés
   exacts du menu]**.
2. Connecte-toi avec le compte Google qui voit ta Search Console.

À savoir, d'après sa politique de confidentialité (lue le 16 novembre
2026) : le serveur hébergé garde tes jetons de connexion chiffrés, mais pas
tes données Search Console. Tu peux tout supprimer depuis ton compte
seoskill.dev.

**Sans connecteur : un export déposé dans `donnees/`.** Aucun tiers, mais à
refaire à la main : la tâche hebdomadaire travaillera sur un export qui
vieillit. Comment l'obtenir : `donnees/LISEZ-MOI.md`.

**En option** : Semrush ou Ahrefs, s'ils sont connectés à ton compte Claude,
pour relever la SERP. Jamais requis.

## Tous les lundis

1. Sur claude.ai/code/routines, crée une tâche planifiée.
2. Choisis ton dépôt, un rythme hebdomadaire et, dans les connecteurs,
   **seulement** seoskill.
3. Colle comme instructions le texte « Tous les lundis » de `LANCER.md`.
4. Clique sur « Run now » une première fois et vérifie :
   - un dossier est apparu dans `articles/` sur la branche principale ;
   - `memoire/sujets.json` a changé ;
   - un second « Run now » ne réécrit pas le même sujet.

À savoir :

- La tâche repart chaque fois d'une copie neuve du dépôt. Sa mémoire n'est
  gardée que si elle est poussée sur la branche principale, ce que demande le
  texte de `LANCER.md`. Si ta branche principale est protégée, la tâche le
  dira : lève la protection, ou fusionne toi-même chaque semaine.
- Les tâches planifiées cloud de Claude sont en aperçu (« research
  preview ») : leur fonctionnement peut changer. Chaque passage compte dans
  l'usage de ton offre Claude.

## À la demande

Ouvre une session sur ton dépôt et colle un texte de `LANCER.md` :
« Propose-moi des sujets » ou « Écris le prochain article ». L'article arrive
sur la branche de la session : relis-le, puis fusionne la pull request pour
garder la mémoire.

## Les fichiers

```
agent-seo/
├── CONFIGURE-MOI.md       le texte à coller pour tout paramétrer
├── LANCER.md              les textes pour lancer l'agent ou la tâche planifiée
├── AGENT.md               la méthode que l'agent suit
├── site-context.md        ton site, tes lecteurs, ton ton, tes faits produit
├── reserve.md             tes preuves et ton expérience
├── apprentissages.md      ce qui marche pour ton site
├── config.json            marque, seuils, exclusions
├── donnees/               exports Search Console (si pas de connecteur)
├── sujets.md              les sujets proposés, classés
├── articles/              un dossier par article : .md, .docx, état
├── memoire/               ce qui a été proposé, écrit, abandonné
├── scripts/               sujets.py, verite.py, exporter.py (Python sans dépendance)
├── .claude/skills/        les Skills du pack SEO Join Médicis
├── dust/                  la version Dust, en plusieurs agents
└── tests/                 tests automatiques
```

## Limites

- **La SERP.** La recherche web d'une session cloud ne cherche pas
  forcément depuis la France. Sans Semrush, Ahrefs ou une clé DataForSEO,
  l'agent le signale dans son relevé et peut te demander une SERP collée.
- **Aucun volume de recherche inventé.** L'agent classe par impressions
  Search Console réelles. Un volume ne s'écrit que s'il vient d'un outil
  nommé.
- **Un site jeune** a peu de requêtes en position 8 à 40 : les propositions
  sont alors fragiles, et l'agent le dit.
- **Un brouillon reste un brouillon.** Chaque chiffre porte sa source, mais
  la relecture et la décision de publier restent les tiennes.

## Vérifier

```bash
python3 -m unittest discover -s tests
```

Pas encore testé en conditions réelles :

- le connecteur seoskill dans claude.ai/code et dans une tâche planifiée ;
- le push sur la branche principale depuis une tâche planifiée ;
- la lecture des sources par la session cloud, selon le réseau de
  l'environnement : si la lecture des pages échoue, crée un environnement en
  accès réseau « Full » ou ajoute les domaines utiles.

Méthode et sources étudiées : `CREDITS.md`. Fait par
[Join Médicis](https://joinmedicis.com), pour les marketeurs francophones.
