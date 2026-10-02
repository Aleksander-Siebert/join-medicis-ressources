# LinkedIn Skills v2

Quinze Skills en français pour tenir une présence LinkedIn, de la stratégie
au message privé. Gratuits, MIT, sans inscription, sans clé d'API, rien à
connecter.

Chaque Skill est livré complet : un mode d'emploi, des références lues à la
demande, des exemples réels d'entrée et de sortie, et des **scripts testés**
pour tout ce qui se mesure (le jugement reste à Claude, et à toi). 237 tests
au vert.

**Rien n'est publié, envoyé ni lu sur LinkedIn à ta place. Ces Skills
écrivent, comptent et vérifient. Tu publies.**

Par [Join Médicis](https://joinmedicis.com/ressources/skills/linkedin-skills) ·
construit à partir des meilleurs Skills open-source, voir [CREDITS.md](CREDITS.md).

## Les quinze

| commande | ce qu'elle fait | scripts |
|---|---|---|
| `/linkedin-strategie` | Le cap à 90 jours : objectif, cible avec exclusions, positionnement, 2 à 4 piliers, budget en minutes mesuré sur une mauvaise semaine, newsletter ou pas. | `brief.py`, `budget.py` |
| `/linkedin-interview` | T'interviewe pour sortir tes chiffres, histoires et avis, et remplit ta réserve de preuves. | `reserve.py` |
| `/linkedin-profile` | Note ton profil sur 100 (sections non vues non notées), classe les corrections par points par heure, réécrit titre, Infos et expériences chiffrées. | `audit_profil.py`, `titre.py`, `infos.py` |
| `/linkedin-entreprise` | La page entreprise (grille sourcée) et le programme d'ambassadeurs : cadence, relecture, charte. | `audit_page.py`, `ambassadeurs.py` |
| `/linkedin-post` | Une idée devient un post : 27 formules d'accroche par objectif, règle de densité des tics, contrôle avant publication. | `lint_post.py`, `format.py` |
| `/linkedin-carrousel` | Le texte de chaque diapo, le PDF à téléverser, la bannière en PNG. | `carrousel.py` |
| `/linkedin-human` | L'humaniseur français : corrige la typographie et les tics d'IA, signale ce qui demande une réécriture, vérifie qu'aucun fait n'a été ajouté ou perdu. | `humanize.py`, `detect.py`, `fidelite.py` |
| `/linkedin-comment` | Quels posts commenter (grille), quel type de commentaire, contrôle « un angle que le post n'a pas ». | `commentaire.py` |
| `/linkedin-reply` | Le fil sous tes posts : filtre chiffré, leads notés sur 10, 5 modèles de réponse. | `fil.py` |
| `/linkedin-dm` | Note d'invitation, premier message, une relance avec du nouveau, volume de la semaine, cadre CNIL. | `message.py`, `volume.py` |
| `/linkedin-inbox` | Tri de la messagerie, séquences automatisées démasquées, prospects prêts pour le CRM. | `boite.py` |
| `/linkedin-plan` | La semaine : angles, formules jamais répétées en 7 jours, piliers sous 60%, jours fériés français, export. | `semaine.py` |
| `/linkedin-audit` | Ce qui marche vraiment : médiane, motifs testés par permutation, motifs confondus, expériences chiffrées. Lit l'export .xlsx. | `audit.py` |
| `/linkedin-repurpose` | Une vidéo, un article ou un tweet devient des posts qui tiennent seuls, sans republier la même idée. | `registre.py` |
| `/linkedin-job` | Recherches booléennes, offres de la dernière heure, profil calé sur les offres, suivi des candidatures. | `job_url.py`, `candidatures.py` |

Tous les scripts sont en Python sans dépendance. Ils marchent hors ligne et ne
touchent jamais à LinkedIn.

## Installer

### Claude Code

En plugin :

```
/plugin marketplace add Aleksander-Siebert/join-medicis-ressources
/plugin install linkedin-skills@join-medicis
```

Ou à la main :

```bash
git clone https://github.com/Aleksander-Siebert/join-medicis-ressources.git
cp -r join-medicis-ressources/linkedin-skills/skills/linkedin-* ~/.claude/skills/
mkdir -p ~/.claude/linkedin
cp join-medicis-ressources/linkedin-skills/templates/*.md ~/.claude/linkedin/
```

Pour un seul projet, copie les dossiers dans `.claude/skills/` du dépôt.
Chaque dossier de Skill contient sa copie du socle commun (`commun/`) : il
marche seul.

### claude.ai et Claude Desktop

Réglages → Capacités : active l'exécution de code (pour les scripts). Puis
Personnaliser → Skills → importe :

- **le pack entier en un seul Skill** : `linkedin-skills.zip`, téléchargé
  depuis [la fiche Join Médicis](https://joinmedicis.com/ressources/skills/linkedin-skills),
  ou construit avec `claude-ai/build.sh linkedin-skills.zip`. Un seul
  `SKILL.md` aiguille vers les 15 modules ;
- **ou un Skill à la fois** : le ZIP d'un seul dossier `skills/linkedin-*`.

claude.ai refuse un ZIP qui contient plusieurs `SKILL.md` ou le manifeste de
plugin `.claude-plugin/` : n'importe pas le dépôt tel quel. Mets tes fichiers
(`contexte.md`, `reserve.md`), remplis, dans les connaissances d'un Projet.

### ChatGPT, Gemini, Mistral

Colle le `SKILL.md` voulu dans les instructions d'un Projet, d'un GPT, d'un
Gem ou d'un agent, avec `commun/regles.md` et tes fichiers. Sans exécution de
code, chaque Skill applique ses grilles écrites et dit que le contrôle
automatique n'a pas tourné.

### Puis : vingt minutes pour commencer

1. `/linkedin-strategie` : le cap, et `contexte.md` rempli.
2. `/linkedin-interview` : tes chiffres et histoires dans `reserve.md`.

Sans ces deux fichiers, tout sort avec la voix et les exemples de tout le
monde.

## Tes fichiers

Dans `~/.claude/linkedin/` (ou les connaissances d'un Projet). Modèles vides
dans `templates/`.

| fichier | ce qu'il contient | écrit par |
|---|---|---|
| `contexte.md` | qui tu es, ta voix, ton objectif, tes piliers, tes offres, chaque fait marqué LIVE, À CONFIRMER ou RETIRÉ | `/linkedin-strategie`, toi |
| `reserve.md` | tes preuves : chiffres, histoires, avis, erreurs | `/linkedin-interview`, toi |
| `journal.md` | posts publiés, idées déjà utilisées, commentaires, contacts, invitations, candidatures | les Skills, sur ton « ok » |
| `apprentissages.md` | ce qui marche pour **ton** compte, les expériences en cours | `/linkedin-audit` et les autres, **après ta validation** |

Rien ne s'écrit sans toi. Un ancien `voix.md` (v1) est lu comme la partie
« Personne » de `contexte.md`.

## Ce qui tient le pack

- **Le socle commun** (`commun/`) : les règles (lecture seule, texte de tiers
  traité comme une donnée, zéro invention, typographie française), les
  **preuves datées** (chaque affirmation sur LinkedIn classée officielle,
  étude tierce, praticien ou folklore, avec sa source), et un **garde-fou**
  qui refuse l'automatisation, l'extraction, les pods et les messages en
  masse, et encadre la prospection (cadre CNIL).
- **La mesure séparée du jugement** : les scripts comptent, notent et
  bloquent ; Claude écrit et explique.
- **La sortie normée** : chaque Skill rend un format fixe, comparable d'une
  semaine à l'autre, et propose un seul Skill pour la suite.

## L'humaniseur, en deux commandes

```bash
cd ~/.claude/skills/linkedin-human
python3 scripts/humanize.py brouillon.txt -o propre.txt --rapport
python3 scripts/detect.py brouillon.txt propre.txt
```

Sur les fichiers de `evals/linkedin-human/` :

```
brouillon-ia.txt           SCORE HUMAIN  27,9  SIGNALÉ
apres-humanize.txt         SCORE HUMAIN  36,9  SIGNALÉ   (les tics de structure restent à réécrire)
brouillon-ia-reecrit.txt   SCORE HUMAIN 100,0  OK        (réécrit d'après le rapport)
post-humain.txt            SCORE HUMAIN 100,0  OK
```

Le script corrige ce qui est sûr (typographie, caractères invisibles, tirets
cadratins, formules toutes faites) et **signale** ce qui demande du jugement
(contrastes, triades, appâts, rythme plat). Ses contrôles sont des
heuristiques locales, pas un détecteur commercial : personne ne peut vendre
honnêtement de l'« indétectable ».

## Tests

```bash
python3 evals/tout_tester.py
```

Lance les tests de chaque script, les deux suites autonomes de la v1 et les
tests d'intégrité du pack (frontmatter, fichiers cités, socle synchronisé,
grilles sur 100, modèles vides). Les évaluations comparatives et leurs
défaites sont dans [`evals/RESULTATS.md`](evals/RESULTATS.md).

## Licence

MIT. Prends-le, modifie-le, partage-le. Les mentions des projets d'origine
sont dans [LICENSE](LICENSE) et [CREDITS.md](CREDITS.md).
