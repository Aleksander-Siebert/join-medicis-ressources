# Fondation Skills

Le contexte de ton entreprise, écrit une fois, que toute IA lit avant
d'écrire pour toi. Chaque fait dit d'où il vient, à quelle date, et s'il est
encore vrai : `LIVE`, `À CONFIRMER` ou `RETIRÉ`. Rien n'est inventé, rien
n'est enregistré sans ton « oui ».

> **Version 0.1 : Skill modèle.** `/fondation-entreprise` est prêt pour
> relecture. `/fondation-clients`, `/fondation-voix` et `/fondation-preuves`
> suivront sur le même gabarit.

## Les Skills

| Skill | Fichier produit | Ce qu'il fait |
|---|---|---|
| `/fondation-entreprise` | `entreprise.md` | Lit ton site et tes mentions légales (SIREN, SIRET, TVA contrôlés), puis te pose les questions qui manquent, une à la fois : offre, clients servis, alternatives dont le statu quo, différence prouvée, positionnement, objectifs du trimestre, ce qui coince, contraintes de secteur et de données (règles CNIL datées), outils. Mise à jour des faits périmés tous les 3 mois. |

Chaque Skill marche seul. Les packs SEO, GEO et LinkedIn marchent sans la
Fondation ; si tu les utilises, la Fondation peut pré-remplir leurs fichiers
de contexte (`contexte.py exporter`), toujours sur ton accord.

## Installer

**Claude Code :**

```
/plugin marketplace add Aleksander-Siebert/join-medicis-ressources
/plugin install fondation-skills@join-medicis
```

Ou copie `skills/fondation-entreprise/` dans `~/.claude/skills/`.

**claude.ai :** construis le ZIP avec `claude-ai/build.sh fondation-skills.zip`,
puis importe-le dans Personnaliser → Skills. Les fichiers de contexte vont
dans les connaissances de ton Projet.

**ChatGPT, Gemini, Mistral :** colle le contenu de
`skills/fondation-entreprise/SKILL.md` dans les instructions de ton Projet
(GPT, Gem, agent) et mets `templates/entreprise.md` dans ses connaissances.

## Ce qu'il y a dedans

```
fondation-skills/
├── commun/              règles, faits datés (CNIL, Sirene, TVA), contexte.py
├── skills/
│   └── fondation-entreprise/
│       ├── SKILL.md
│       ├── references/  site, entretien, positionnement, contraintes, exemple
│       ├── scripts/     entreprise.py (SIREN, SIRET, TVA, mentions légales)
│       └── commun/      copie du socle (outils/propager.py)
├── templates/           entreprise.md (vide) et exemple-entreprise.md (Assurly, fictif)
├── evals/               tests des scripts, intégrité, cas d'éval
└── claude-ai/           aiguilleur et construction du ZIP
```

## Les scripts (Python 3, sans dépendance)

```bash
python3 skills/fondation-entreprise/scripts/entreprise.py siren "123 456 782"
python3 skills/fondation-entreprise/scripts/entreprise.py mentions https://www.exemple.fr/mentions-legales
python3 commun/contexte.py etat ~/.claude/fondation/entreprise.md
python3 commun/contexte.py exporter --vers seo ~/.claude/fondation/entreprise.md
```

Codes de sortie : 0 rien à revoir · 2 à revoir · 3 bloqué ou vide · 1 erreur
d'usage. Un modèle vide n'obtient jamais une bonne note.

## Tester

```bash
python3 evals/tout_tester.py
```

## Ce que le pack ne fait pas

Il ne donne pas d'avis juridique : il pose trois questions sur tes données,
rappelle les règles de la CNIL avec leur date et renvoie à un juriste. Il ne
recommande aucun outil. Il ne publie rien.

## Licence

MIT. Sources et crédits : [CREDITS.md](CREDITS.md).
