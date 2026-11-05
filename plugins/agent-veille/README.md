# Agent de veille concurrentielle

Un agent qui surveille tes concurrents et t'envoie chaque semaine un mail
court, exact et sourcé : leurs prix, leurs nouveautés, ce que la presse dit
d'eux. Il tourne dans Claude, sur ton ordinateur, ou dans le cloud avec
GitHub Actions. Modèle Join Médicis, gratuit, licence MIT.

> Statut : en test (novembre 2026). Les étapes marquées **[à vérifier]**
> dépendent des menus de Claude et de GitHub, qui changent souvent.

## Ce qu'il fait

1. **Collecte** (script `scripts/collecte.py`, sans IA) :
   - les actualités qui citent chaque concurrent ;
   - les flux de leurs blogs ;
   - les pages que tu surveilles (tarifs, offres, nouveautés), comparées à la visite précédente.
2. **Tri mécanique** :
   - garde seulement ce qui est daté de la période, d'après la vraie date ;
   - écarte ce qui a déjà été envoyé (mémoire de 90 jours) ;
   - regroupe la même info reprise par plusieurs médias.
3. **Analyse par l'IA** (`AGENT.md`) :
   - écarte les homonymes et le bruit ;
   - classe par importance ;
   - résume avec les seuls faits des sources ;
   - explique « pourquoi c'est pour toi ».
4. **Contrôle** (`scripts/mail.py`) : chaque info doit renvoyer à une source trouvée par la collecte. Sinon, le mail est bloqué.
5. **Envoi à toi seul**, puis mémorisation. Si l'envoi échoue, rien n'est perdu.

## Installer dans Claude (10 minutes)

1. **Télécharge ce dossier** et ouvre-le dans Claude :
   - Cowork : choisis le dossier comme espace de travail **[à vérifier]** ;
   - Claude Code : `cd agent-veille` puis `claude`.
2. **Relie Gmail** dans les connecteurs de Claude si tu veux recevoir le
   mail. Sans connecteur, le mail s'affiche dans la conversation.
3. **Ouvre `CONFIGURE-MOI.md`** et colle son contenu dans la conversation.
   L'agent :
   - pose 6 questions ;
   - trouve les sites et les pages tarifs de tes concurrents et vérifie chaque source ;
   - fait un essai à blanc, puis t'envoie un mail de test ;
   - te propose la tâche planifiée.

Python 3 doit être installé (il l'est déjà sur macOS et Linux). Sans exécution
de code (claude.ai, autres IA), l'agent fait la collecte par recherche web et
le signale dans le mail : les dates et doublons sont alors moins fiables.

## Recevoir le mail : les connecteurs

L'agent n'embarque aucun accès à ta messagerie. Il utilise ce que tu as déjà
branché :

- **Dans Claude** : le connecteur Gmail (ou Microsoft 365 pour Outlook
  **[à vérifier]**), à activer une fois dans les réglages des connecteurs de
  Claude. L'agent l'utilise s'il est là. Sinon, il affiche le mail dans la
  conversation.
- **En automatique** (`lancer.sh` ou GitHub Actions) : un envoi SMTP
  classique, réglé dans `.env` ou dans les secrets GitHub. Pour Gmail, il
  faut un « mot de passe d'application » Google.

## Lancer à la main ou automatiquement

L'agent ne tourne pas tout seul tant que tu ne l'as pas programmé. Trois
façons, de la plus simple à la plus autonome :

| Façon | Comment | Il faut |
|---|---|---|
| **À la main** | Colle `LANCER.md` dans Claude, quand tu veux. | Rien de plus |
| **Tâche planifiée de Claude** | Dans l'application Claude, crée une tâche planifiée avec le texte de `LANCER.md` **[à vérifier : menu exact]**. `CONFIGURE-MOI.md` le propose à la fin. | Ordinateur allumé, application ouverte à l'heure prévue **[à vérifier]** |
| **Lanceur `lancer.sh`** (macOS, Linux) | `crontab -e`, puis la ligne `0 8 * * 1 /chemin/vers/agent-veille/lancer.sh` (chaque lundi à 8 h). Le journal est dans `sortie/journal.log`. | Claude Code installé, `.env` rempli (copie `.env.exemple`), ordinateur allumé |
| **GitHub Actions** | Voir plus bas : tourne dans le cloud. | Un compte GitHub, une clé API, les secrets SMTP |

## Personnaliser

- **Concurrents, sources, sujets, adresse** : dis-le à l'agent (« ajoute
  tel concurrent », « surveille sa page nouveautés », « ignore les offres
  d'emploi »). Il modifie `sources.json` et `veille.md` et vérifie la
  source. La liste des demandes comprises est dans `AGENT.md`.
- **Apparence du mail** : `modele-mail.html` est un fichier HTML ordinaire.
  Change les couleurs, les polices, les textes et l'ordre des blocs, sans
  toucher à Python. Le mode d'emploi est en tête du fichier.
- **Méthode** (rubriques, règles d'importance, longueur) : `AGENT.md`, en
  français.

## Version cloud (GitHub Actions, ordinateur éteint)

1. Crée un dépôt **privé** sur GitHub et copie-y le contenu de ce dossier.
   Ta config et ta mémoire ne doivent pas être publiques.
2. Le workflow `.github/workflows/veille.yml` doit être à la racine du
   dépôt : c'est déjà le cas si tu copies le dossier tel quel.
3. Dans *Settings → Secrets and variables → Actions*, crée :
   - `ANTHROPIC_API_KEY` : clé de la console Anthropic, facturée à l'usage.
     Un abonnement Claude peut servir à la place via un jeton
     `CLAUDE_CODE_OAUTH_TOKEN` **[à vérifier]**.
   - Pour Gmail : `SMTP_HOST` = `smtp.gmail.com`, `SMTP_PORT` = `465`,
     `SMTP_USER` = ton adresse, `SMTP_PASSWORD` = un mot de passe
     d'application Google (pas ton mot de passe), `MAIL_TO` = ton adresse.
4. Configure `veille.md` et `sources.json` avec `CONFIGURE-MOI.md` sur ton
   ordinateur, puis envoie-les dans le dépôt.
5. Onglet *Actions* → « Veille concurrentielle » → *Run workflow* pour un
   premier essai. Ensuite, il tourne chaque lundi.

Les noms exacts des paramètres de l'action `anthropics/claude-code-action`
sont **[à vérifier]** dans sa documentation avant la première exécution.

## Limites à connaître

- **Google Actualités** : le flux RSS de Google est réservé à un usage
  personnel et non commercial, d'après la mention de copyright du flux
  (relevée le 5 novembre 2026). Pour une veille d'entreprise, désactive
  `actualites_google` et donne les flux RSS des médias et des blogs
  concernés, ou des alertes Google en flux RSS.
- **Extraits courts** : les actualités Google ne donnent souvent que le
  titre. Le script cherche alors l'article dans le flux RSS du média (un
  sur trois environ lors de nos essais), puis l'agent tente une recherche
  web pour les infos importantes. Sinon, il écrit « D'après le titre… »
  et ne complète rien. Certains médias bloquent les robots (Les Echos,
  ZDNet lors de nos essais).
- **Sites protégés** : certains sites refusent les robots (erreur 403).
  L'agent ne contourne rien et propose de suivre ce concurrent par ses
  actualités seulement.
- **Pages refaites** : une refonte de site donne beaucoup de changements
  d'un coup. L'agent le signale sans détailler.
- **Ce n'est pas une veille exhaustive** : réseaux sociaux, publicités et
  sources payantes ne sont pas lus.

## Tester les scripts

```bash
python3 -m unittest discover -s tests
python3 scripts/collecte.py --test-sources
```

## Fichiers

| Fichier | Rôle |
|---|---|
| `AGENT.md` | méthode de l'agent (lue à chaque lancement) |
| `CLAUDE.md` | point d'entrée pour Claude Code et Cowork |
| `CONFIGURE-MOI.md` | prompt de configuration guidée |
| `LANCER.md` | prompt de lancement et de la tâche planifiée |
| `veille.md` | ton profil et tes préférences |
| `sources.json` | concurrents, pages, flux, réglages |
| `scripts/collecte.py` | collecte, dates, doublons, mémoire, pages |
| `scripts/mail.py` | contrôle, mise en forme, envoi SMTP (automatique) |
| `modele-mail.html` | apparence du mail, en HTML |
| `lancer.sh`, `.env.exemple` | lancement automatique sur ton ordinateur |
| `memoire/` | ce qui a été envoyé, état des pages |
| `exemples/` | exemple de résumé et de mail (Assurly, fictif) |
| `evals/` | cas de test de l'agent |
