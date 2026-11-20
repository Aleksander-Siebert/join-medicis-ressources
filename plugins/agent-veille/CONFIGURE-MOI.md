# Configure-moi

Ouvre ce dossier dans Claude (onglet Code de l'application, ou
claude.ai/code pour la version cloud), puis colle le texte ci-dessous.
Compte un quart d'heure. Tu ne remplis aucun fichier à la main.

---

Tu vas configurer l'agent de veille de ce dossier. Lis d'abord `AGENT.md`,
`veille.md`, `sources.json` et `mail.json`.

Pose tes questions par groupes de 2 à 4, avec l'outil AskUserQuestion s'il
existe, sinon dans la conversation. Propose des choix quand c'est possible
et accepte une réponse courte. N'invente aucun site, aucune adresse, aucun
concurrent : uniquement ce que je te donne ou ce que tu as vérifié en
ouvrant la page.

**1. Vérifie l'installation, sans me poser de question technique.**

- Essaie `python3 --version`, puis `python --version`, puis `py --version`.
- Python 3.9 ou plus répond : retiens la commande qui marche et utilise-la
  partout à la place de `python3`.
- Rien ne répond : dis-moi en une phrase ce que ça change (dates et
  doublons vérifiés à la main, pas d'appels d'offres ni d'offres d'emploi)
  et propose deux choix : « installe-le pour moi » (suis
  `references/installation.md`, partie 3) ou « continue sans Python »
  (suis `references/sans-python.md` pour toute la suite).
- Si ce dossier est un dépôt GitHub ouvert dans le cloud, dis-le : la veille
  pourra tourner ordinateur éteint (`references/installation.md`, partie 1).

**2. Demande-moi ce que je veux suivre.**

Premier groupe :

1. Mon entreprise et ce que je vends, en une phrase. Mon prix d'entrée ou
   mon offre principale, si je veux que tu compares.
2. Le type de veille, plusieurs choix possibles :
   - mes concurrents (3 à 10, avec leur site si je l'ai) ;
   - un sujet ou une tendance de mon marché (5 mots-clés) ;
   - la réglementation de mon secteur ;
   - les appels d'offres publics qui me concernent.
3. Ce qui compte le plus pour moi : prix et offres, produit, marketing et
   campagnes, clients et partenariats, financement, recrutement, presse.
4. Ce que je veux ignorer (exemples : offres d'emploi isolées, sponsoring
   sportif, articles « top 10 », contenus sponsorisés).

Second groupe, selon mes réponses :

- Concurrents : des pages précises à surveiller (tarifs, nouveautés, salle
  de presse) ? Leur page carrière, pour suivre les recrutements ? Sinon, tu
  proposeras les tiennes.
- Sujet ou tendance : les 5 à 10 sites ou médias que je lis déjà.
- Réglementation : mon secteur et les autorités qui me concernent. Propose
  les flux officiels de `references/sources-officielles.md` qui
  correspondent.
- Appels d'offres : les mots qui décrivent ce que je vends aux acheteurs
  publics, et la zone (France entière ou départements).
- La période couverte (7 jours par défaut) et la langue des sources.

**3. Prépare les sources.**

- Trouve le site officiel de chaque concurrent s'il manque. En cas de doute
  (homonymes), demande-moi.
- Ajoute les alias utiles (ancien nom, nom de marque) et, pour un nom
  courant (« Alan », « Orange »), un ou deux `mots_cles` du secteur pour
  éviter les homonymes.
- Écris `sources.json`, puis lance
  `python3 scripts/collecte.py --test-sources`.
- Le test liste les flux RSS trouvés et les pages à surveiller possibles.
  Garde au plus 3 pages par concurrent : tarifs ou offres d'abord, puis
  nouveautés ou salle de presse. Pour une page tarifs, propose l'intention
  « seulement si un prix change ». Montre-moi la liste et demande mon accord.
- Une ligne « REFUS » : le site interdit cette page aux robots. Retire-la
  sans chercher à la lire autrement, et dis-le-moi.
- Retire ou remplace chaque source en erreur, puis relance le test jusqu'à
  ce qu'il n'y ait plus d'erreur.
- Laisse `"mode": "standard"`. Ne me propose le mode étendu que si je le
  demande, en m'expliquant sa limite (`references/sources-officielles.md`).

**4. Demande-moi comment je veux recevoir la veille.**

1. Le format. Montre-moi les 3 modèles avec l'exemple fourni : copie
   `exemples/resume.json` dans `sortie/`, lance
   `python3 scripts/mail.py --modele themes`, puis `recap`, puis `flash`,
   et montre-moi chaque rendu.
   - `themes` : 3 points à retenir, puis les infos par rubrique, avec
     « pour toi » ;
   - `recap` : 5 points clés, puis toutes les sources numérotées ;
   - `flash` : l'essentiel en 5 lignes, puis les titres.
2. Le ton : tutoiement ou vouvoiement, court ou détaillé, pour moi ou pour
   une équipe.
3. L'habillage : un titre (« Veille Assurly »), une couleur principale, un
   logo en ligne, une signature. Tout est facultatif.
4. Où envoyer, plusieurs choix possibles : mail (Gmail ou Outlook), canal
   Slack, base Notion, fichier dans le dossier. Pour chaque choix, la
   destination exacte, et le jour et l'heure (par défaut : le lundi à 8 h).

Écris mes choix dans `mail.json` et dans `veille.md`. Pour chaque canal,
vérifie que le connecteur est disponible. S'il manque, donne-moi le chemin
(Paramètres → Connecteurs) et continue avec les autres.

**5. Remplis `veille.md`** avec mes réponses, sans laisser de
`{{à compléter}}`. Montre-le-moi avant de l'écrire.

**6. Fais un essai à blanc** en suivant `AGENT.md` : collecte, recherches
web, tri, `sortie/resume.json`, `python3 scripts/mail.py`, puis montre-moi
la veille. N'envoie rien et ne lance pas `--valider`. Demande-moi ce qu'il
faut ajuster (sujets à écarter, ton, longueur, format) et reporte mes
retours dans `veille.md` ou `mail.json`.

**7. Envoie-moi une première veille de test**, après mon accord. Ensuite
seulement, lance `python3 scripts/collecte.py --valider`.

**8. Programme la veille.** Propose-moi de créer une tâche planifiée au
rythme choisi, avec le texte de `LANCER.md` comme instructions (le texte
« cloud » si ce dossier est un dépôt ouvert dans le cloud). Si tu ne peux
pas la créer toi-même, donne-moi les étapes de
`references/installation.md`. Rappelle-moi de cliquer une fois sur « Run
now » et de répondre « toujours autoriser » pour l'envoi, sinon la tâche
restera bloquée.

Termine par un récapitulatif : ce qui est suivi, pages surveillées, format,
destinations, rythme, et comment modifier tout ça plus tard (« dis-moi
“ajoute tel concurrent”, “passe au format récap” ou “change la couleur” »).

---
