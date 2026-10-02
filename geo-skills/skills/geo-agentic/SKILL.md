---
name: geo-agentic
description: >-
  Prépare un site aux agents d'IA, les assistants qui naviguent, comparent,
  remplissent un formulaire ou réservent pour l'utilisateur (ChatGPT agent,
  Claude, Gemini dans Chrome…) : contenu lisible sans JavaScript, boutons et
  liens nommés, champs avec label, page stable, robots des agents autorisés,
  llms.txt et outils WebMCP en option. Utilise-le pour « agents IA », « web
  agentique », « agent-ready », « WebMCP », « Lighthouse Agentic Browsing ».
---

# geo-agentic

Après « être cité », l'étape suivante est « être utilisé » : un agent
d'IA ouvre la page, compare des offres, remplit le formulaire de devis. S'il
ne trouve pas le bouton ou ne comprend pas un champ, il passe au concurrent.

Google le formule ainsi : un agent lit une page par **capture d'écran**, par
le **HTML** et par l'**arbre d'accessibilité**. Tout ce qui rend un site
accessible le rend utilisable par un agent, et tout ce qu'on fait pour les
agents sert aussi aux humains.

Sources : « Build agent-friendly websites » (web.dev/articles/ai-agent-site-ux,
avril 2026) et la catégorie « Agentic Browsing » de Lighthouse
(developer.chrome.com/docs/lighthouse/agentic-browsing).

## Ce qui compte

| Priorité | Contrôle | Correction |
|---|---|---|
| Bloquant | contenu principal dans le HTML | rendu serveur ou statique ; beaucoup d'agents n'exécutent pas JavaScript |
| Bloquant | robots.txt qui répond (pas de 5xx) et robots des agents autorisés | voir `/geo-crawlers` (ChatGPT-User, Claude-User, Perplexity-User…) |
| Accès | `<button>` et `<a href>`, pas de `<div onclick>` | sinon `role` et `tabindex` |
| Accès | chaque bouton et lien a un nom | texte, `aria-label`, ou `alt` sur l'image du bouton icône |
| Accès | chaque champ a un `<label for>` | un placeholder ne suffit pas |
| Accès | rien de cliquable sous `aria-hidden="true"` ni derrière un calque transparent | |
| Stabilité | page qui ne bouge pas (`width`/`height` sur les images, pas d'insertion tardive) | un agent qui clique sur une capture rate sa cible |
| Option | `cursor: pointer` sur ce qui est cliquable, éléments de plus de 8 px² | recommandation Google |
| Option | llms.txt | contrôlé par Lighthouse, ignoré par Google Search |
| Option | outils **WebMCP** | `toolname` et `tooldescription` sur un `<form>` déclarent le formulaire aux agents ; standard en essai dans Chrome **[à vérifier : spécification en évolution]** |

## Avec exécution de code

```bash
python3 agentic.py https://www.site.fr/devis/
python3 agentic.py page.html --url https://www.site.fr/devis/ --hors-ligne
```

Le script lit le HTML livré par le serveur et donne une fraction (contrôles
passés sur contrôles faits), pas une note sur 100 : les standards du web
agentique ne sont pas stables. Il ne voit ni le rendu JavaScript ni l'arbre
d'accessibilité calculé par le navigateur. Pour la mesure officielle :
Lighthouse, catégorie Agentic Browsing, dans Chrome 150 ou plus. Le script
a besoin de `crawlers.py` du Skill `geo-crawlers` (pack complet).

Sans exécution de code : lis le code source de la page (formulaires,
boutons, liens) avec le tableau ci-dessus.

## Quelles pages

Les pages où un agent agit pour un client : demande de devis, prise de
rendez-vous, simulateur, page produit avec panier, contact, recherche
interne. La page d'accueil seule ne suffit pas.

## Sortie

```
AGENTS D'IA · /devis/ · 5/8 contrôles passés
À CORRIGER
  - 2 champs sans label : « tel », « date-depart » → <label for>
  - bouton « → » sans nom → aria-label="Envoyer la demande de devis"
  - formulaire rendu en JavaScript : 40 mots dans le HTML → rendu serveur
OPTION : déclarer le formulaire de devis en WebMCP (toolname="demande_devis")
```

Chaque correction avec la ligne de HTML à changer. Puis rappelle que ces
corrections servent aussi l'accessibilité. L'Acte européen sur
l'accessibilité s'applique depuis le 28 juin 2025 à une partie des services
en ligne (commerce en ligne, banque, transport…) **[à vérifier selon
l'entreprise et sa taille]**.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : ne promets aucun effet sur le trafic ; le web agentique
  débute, on prépare le site, on ne garantit rien.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est modifié sur le site par le Skill.
