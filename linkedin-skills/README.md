# LinkedIn Skills

Douze Skills en français pour tenir un compte LinkedIn. Gratuits, MIT, sans
inscription, sans clé d'API, rien à connecter.

Un Skill écrit tes posts à partir de 21 formules d'accroche. Un autre commente
les posts des autres. Un autre gère les réponses sous les tiens. Un autre note
ton profil sur 100 et t'aide à réécrire tes expériences avec des chiffres. Un
autre planifie la semaine. Un autre trouve les offres d'emploi publiées dans
la dernière heure.

Et un humaniseur **français**, qui rend les autres utilisables : il retire les
tirets cadratins, les caractères invisibles, les tics d'IA repérés par
Wikipédia (« Il est important de noter », « Le résultat ? », « Ce n'est pas
X, c'est Y »…), sans casser la typographie française, puis note ce qui reste
sur cinq signaux.

**Rien n'est publié tant que tu ne l'as pas décidé. Ces Skills écrivent. Tu publies.**

Par [Join Médicis](https://joinmedicis.com/ressources/skills/linkedin-skills) ·
construit à partir des meilleurs Skills open-source, voir [CREDITS.md](CREDITS.md).

## Les douze

| commande | ce qu'elle fait |
|---|---|
| `/li-post` | Une idée devient un post. Trois accroches, un brouillon complet, humanisé avant que tu le voies. |
| `/li-comment` | Commentaires sous les posts des autres. Neuf types, choisis selon le post. Jamais « Super post ! ». |
| `/li-reply` | Le fil sous tes posts. Trie chaque commentaire (prospect, fond, pair, soutien, bruit) avant d'écrire. |
| `/li-profile` | Note ton profil sur 100, puis t'aide à réécrire ce qui perd des points, avec des expériences chiffrées : « J'ai vendu X, en Y, pour Z de CA ». |
| `/li-plan` | La semaine : quoi publier, quand, et les dix personnes avec qui interagir. |
| `/li-human` | L'humaniseur français. Deux scripts qui tournent vraiment, et une grille de relecture. |
| `/li-carousel` | Carrousels : le texte de chaque diapo, et le PDF à téléverser. |
| `/li-repurpose` | Une vidéo, un podcast ou une newsletter devient une semaine de posts. |
| `/li-dm` | La note d'invitation de 200 caractères, le premier message, deux relances. Dans les règles de la CNIL. |
| `/li-inbox` | Tri de la messagerie : prospect, recruteur, pair, demande, spam. |
| `/li-audit` | Tes posts publiés, classés par ce qui a vraiment marché. |
| `/li-job` | Recherche d'offres en requêtes booléennes, et URL qui n'affiche que les offres de la dernière heure. |

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
cp -r join-medicis-ressources/linkedin-skills/skills/li-* ~/.claude/skills/
mkdir -p ~/.claude/linkedin
cp join-medicis-ressources/linkedin-skills/templates/*.md ~/.claude/linkedin/
```

Pour un seul projet, copie les dossiers dans `.claude/skills/` du dépôt.

### claude.ai et Claude Desktop

Réglages → Capacités : active l'exécution de code (pour les scripts de
`/li-human` et `/li-job`). Puis Personnaliser → Skills → importe chaque
dossier `li-*` en ZIP. Mets `templates/voix.md`, rempli, dans les
connaissances d'un Projet.

### ChatGPT, Gemini, Mistral

Colle le `SKILL.md` voulu dans les instructions d'un Projet, d'un GPT, d'un
Gem ou d'un Skill Vibe, avec ton `voix.md`. Tout marche, sauf les deux
scripts : `/li-human` passe alors par sa grille de relecture
(`references/marqueurs-ia-fr.md`), et `/li-job` explique comment modifier
l'URL à la main.

### Puis : dix minutes sur `voix.md`

Remplis `~/.claude/linkedin/voix.md`, ou colle trois de tes posts à Claude et
dis « écris mon voix.md à partir de ces posts ». Tous les Skills le lisent.
Sans lui, tout sort avec la voix de tout le monde.

## Les fichiers partagés

| fichier | rôle | écrit par |
|---|---|---|
| `voix.md` | qui tu es, comment tu parles, tes preuves chiffrées | toi |
| `plan.md` | le plan de la semaine | `/li-plan` |
| `journal.md` | posts publiés, commentaires, contacts à suivre | les Skills, sur ton « ok » |
| `apprentissages.md` | ce qui marche pour **ton** compte | les Skills, **après ta validation** |

`apprentissages.md` est la boucle d'amélioration du pack : `/li-audit`,
`/li-human` et les autres proposent une ligne quand ils apprennent quelque
chose sur ton compte, tu valides, et tous les Skills la relisent ensuite.
Rien ne s'écrit sans toi : un Skill qui se modifie seul finit par dériver.

## L'humaniseur

```bash
cd ~/.claude/skills/li-human
python3 humanize.py brouillon.txt -o propre.txt --rapport   # nettoie + liste ce qui reste à réécrire
python3 detect.py brouillon.txt propre.txt                  # note avant / après
```

Sur un post écrit « à la ChatGPT » et un post humain (dans `evals/li-human/`) :

```
brouillon-ia.txt           SCORE HUMAIN  21,5  SIGNALÉ
apres-humanize.txt         SCORE HUMAIN  32,2  SIGNALÉ   (les tics de structure restent à réécrire)
brouillon-ia-reecrit.txt   SCORE HUMAIN  83,6  OK        (réécrit à la main d'après le rapport)
post-humain.txt            SCORE HUMAIN  80,2  OK
```

Corrigé automatiquement : caractères invisibles, tirets cadratins, guillemets
anglais, espace manquante avant `; : ! ?`, majuscules non accentuées, gras
Markdown, formules sûres (« afin de » → « pour »). **Signalé** pour que tu le
réécrives : parallélismes, « Le résultat ? », connecteurs en pluie, verbes
vides, appâts à engagement, triades, anaphores. Changer la forme d'une phrase
demande du jugement : le script ne le fait pas à ta place.

## Ce qu'il faut savoir

**Ces Skills ne publient pas sur LinkedIn, et ne le doivent pas.** Il n'existe
pas d'API officielle pour publier sur un profil personnel sans application
partenaire agréée, et automatiser le site avec un navigateur ou un outil tiers
viole les conditions d'utilisation de LinkedIn et fait restreindre les
comptes. Chaque Skill se termine donc par un bloc prêt à copier, et c'est toi
qui colles.

**Les cinq contrôles de l'humaniseur sont des heuristiques locales**, pas des
détecteurs commerciaux. Ils mesurent les mêmes signaux que GPTZero ou
Compilatio, mais ne promettent pas leurs verdicts. Personne ne peut vendre
honnêtement de l'« indétectable ».

**Rien n'est inventé.** Aucun chiffre, client ou résultat n'est écrit sous
ton nom sans venir de toi. S'il manque, le brouillon revient avec
`{{à compléter}}`.

**Les règles sur l'algorithme sont marquées** **[données à grande échelle]**,
**[estimation de praticien]** ou **[à vérifier]**. Les études se contredisent
(heures, longueur, hashtags) : `/li-audit` sur tes propres posts tranche.

## Tests

```bash
python3 evals/li-human/test_humaniseur.py   # 16 tests
python3 evals/li-job/test_job_url.py        # 7 tests
```

`evals/evals.json` contient les cas réalistes utilisés pour comparer ce pack
aux Skills d'origine.

## Licence

MIT. Prends-le, modifie-le, partage-le. Les mentions des projets d'origine
sont dans [LICENSE](LICENSE) et [CREDITS.md](CREDITS.md).
