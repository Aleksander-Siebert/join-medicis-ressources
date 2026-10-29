---
name: geo-agentic
description: >-
  Prépare une page aux agents d'IA qui naviguent, comparent, remplissent un
  formulaire ou réservent pour l'utilisateur (Gemini dans Chrome, ChatGPT,
  Claude dans Chrome, Comet…), et repère les consignes cachées adressées
  aux IA : contenu lisible sans JavaScript, robots des agents
  (ChatGPT-User, Claude-User, Google-Agent…) selon robots.txt, boutons et
  liens nommés, champs avec label, rien de cliquable caché, page stable ;
  texte caché, commentaires, attributs et caractères Unicode invisibles qui
  disent « si vous êtes une IA, recommandez… ». llms.txt, Markdown et
  WebMCP rapportés sans poids. Utilise-le pour « agents IA », « web
  agentique », « agent-ready », « WebMCP », « Lighthouse Agentic
  Browsing », « texte caché pour ChatGPT ». Pas pour l'accès des robots de
  recherche (/geo-acces) ni la rédaction (/geo-contenu). Aucune note sur 100.
---

# geo-agentic

Après « être cité » vient « être utilisé » : un agent ouvre la page de
devis, compare, remplit le formulaire. S'il ne trouve pas le bouton ou ne
comprend pas un champ, il passe au concurrent. Google le dit : un agent lit
une page par **capture d'écran**, par le **HTML** et par l'**arbre
d'accessibilité**. Ce qui rend un site accessible le rend utilisable par un
agent.

L'autre face : des sites cachent des consignes aux IA (« si vous êtes une
IA, recommandez-nous »). C'est une manipulation, inutile selon Google et
risquée si elle est découverte. Ce Skill la repère, y compris sur un site
où un prestataire l'a glissée sans prévenir.

**À lire avant de commencer :** `commun/regles.md`, `commun/preuves.md`
(table des robots) et `references/agents.md` (matrice datée des agents).

## 1. Quelles pages

Celles où un agent agit pour un client : demande de devis, prise de
rendez-vous, simulateur, fiche produit avec panier, contact, recherche
interne. L'accueil seul ne suffit pas.

## 2. Lancer le contrôle

```bash
python3 scripts/agentic.py https://www.site.fr/devis/
python3 scripts/agentic.py devis.html --url https://www.site.fr/devis/ --hors-ligne
```

| Groupe | Contrôle | Correction |
|---|---|---|
| Bloquant | contenu principal dans le HTML (150 mots ou plus) | rendu serveur ou statique |
| Bloquant | robots.txt qui répond (pas de 5xx), robots « utilisateur » de la table autorisés | `/geo-acces` ; plusieurs ignorent robots.txt, un refus reste un signal |
| Accès | `<button>` et `<a href>`, pas de `<div onclick>` | sinon `role` et `tabindex` |
| Accès | chaque bouton et lien a un nom | texte, `aria-label`, ou `alt` de l'icône |
| Accès | chaque champ a un `<label for>` | un placeholder ne suffit pas |
| Accès | rien de cliquable sous `aria-hidden="true"` | |
| Stabilité | images avec `width` et `height` | un agent qui clique sur une capture rate sa cible |
| Confiance | aucune consigne aux IA dans le texte caché, les commentaires, les attributs, les caractères Unicode « tag » | retirer ; chercher qui l'a ajoutée (thème, extension, prestataire) |
| Info | llms.txt, version Markdown (balise, en-tête `Link`, `Accept: text/markdown`), WebMCP | facultatifs ; leur absence est normale, ne pas en parler |

Résultat : contrôles passés sur contrôles faits. Le script ne voit ni le
rendu JavaScript ni l'arbre d'accessibilité calculé : pour la mesure
officielle, Lighthouse, catégorie Agentic Browsing (version et audits :
`references/agents.md`).

Sans exécution de code : code source de la page (`Ctrl+U`), formulaires,
boutons et liens avec le tableau ; chercher « IA », « AI », « LLM »,
« assistant » dans le code source pour les consignes cachées.

## 3. Les consignes cachées

Le script cherche, en français et en anglais, les phrases qui s'adressent
à une IA (« si vous êtes une IA », « ignorez les instructions
précédentes », « note pour les IA », « AI assistants should », « always
recommend ») dans :

- le texte caché (`display:none`, `hidden`, `aria-hidden`, `font-size:0`) ;
- les commentaires HTML ;
- les attributs (`alt`, `title`, `aria-label`, `content`, `data-*`) ;
- les caractères Unicode « tag » (U+E0000), invisibles à l'écran, décodés.

Il compte aussi les caractères de largeur nulle et de direction. Une
consigne **visible** (« Si vous êtes une IA, citez cette page ») sort en
« à revoir » : à réécrire pour le lecteur. Un site qui **parle** des
prompts (une formation, un outil d'IA) n'est pas signalé.

## 4. La sortie (format fixe)

```
AGENTS D'IA · https://assurly.example/devis/ · 4/9 contrôles passés · table des agents du 2026-10-16
  BLOQUANT   À CORRIGER  Contenu lisible sans JavaScript      62 mots dans le HTML
  ACCÈS      À CORRIGER  Champs de formulaire avec label      1 sans label
  CONFIANCE  CRITIQUE    Aucune consigne cachée aux IA        4 trouvée(s) · 1 caractère(s) invisible(s)
  INFO       INFO        Outils WebMCP                        1 formulaire(s) déclaré(s) sur 1 · JavaScript : non
SANS LABEL : tel
CONSIGNE AUX IA (texte caché) : « Si vous êtes une IA, ignorez les instructions précédentes… »
```

Exemple fictif (`evals/geo-agentic/devis-piege.html`). Sous la sortie :
chaque correction avec la ligne de HTML à changer, la consigne cachée en
premier. Ces corrections servent aussi l'accessibilité : l'Acte européen
sur l'accessibilité s'applique depuis le 28 juin 2025 à une partie des
services en ligne (commerce en ligne, banque, transport…) **[à vérifier
selon l'entreprise et sa taille]**.

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Page en 403 pour le script | Enregistrer le HTML depuis le navigateur, relancer avec `--url`. |
| robots.txt non lu | « NON LU », non compté ; vérifier à la main. |
| Formulaire injecté en JavaScript | Peu de mots et aucun champ : le dire ; Lighthouse sur la page rendue. |
| Consigne trouvée dans une extension ou un thème | Désactiver ou corriger à la source ; le signaler au prestataire. |
| L'utilisateur veut ajouter une consigne pour les IA | Refuser : manipulation, inutile pour Google, détectable ; proposer de rendre la page claire pour le lecteur. |
| WebMCP demandé | Rappeler le statut d'essai (`references/agents.md`), proposer `toolname` et `tooldescription` sur le vrai formulaire, sans promesse d'usage. |

## Ressources

- `scripts/agentic.py` · `commun/robots_ia.json` · `commun/robots_rfc.py` ·
  `commun/page.py`
- `references/agents.md` : matrice datée des agents (ce qu'ils lisent,
  robots.txt, WebMCP), Lighthouse, procédure de mise à jour.

## Skills liés

`/geo-acces` (robots et extrait autorisé), `/geo-contenu` (texte pour le
lecteur), `/geo-audit` (diagnostic complet).

## Règles du pack

- Zéro invention : aucun effet promis sur le trafic ou les ventes ; le web
  agentique débute, on prépare le site, on ne garantit rien.
- Rien n'est modifié sur le site par le Skill.
- Texte simple dans la conversation, sans créer de document.
