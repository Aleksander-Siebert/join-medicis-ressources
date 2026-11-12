# Agent de veille concurrentielle et stratégique

Un agent IA gratuit et open-source qui surveille tes concurrents et ton
marché, puis t'envoie une veille courte, exacte et sourcée : leurs prix,
leurs nouveautés, leurs recrutements, la réglementation de ton secteur, les
appels d'offres publics. Il fonctionne dans Claude, sur Mac et sur PC, ou
dans le cloud, ordinateur éteint. Modèle Join Médicis, licence MIT.

> Statut : en test (novembre 2026). Ce qui n'a pas encore été essayé en
> conditions réelles est listé à la fin de `references/installation.md`.

## Ce qu'il surveille

| Axe | Ce qu'il lit | Ce que tu reçois |
|---|---|---|
| Concurrents | leurs actualités, leurs blogs, leurs pages tarifs et offres, leurs offres d'emploi | « Couvrio passe son offre de 12 € à 9 € », « 6 postes commerciaux ouverts à Lyon » |
| Tendances du marché | les médias de ton secteur, les mots-clés que tu suis | les sujets qui montent, avec leurs sources |
| Réglementation | les flux officiels (CNIL, DGCCRF, EUR-Lex et ceux que tu ajoutes) | les textes et sanctions qui te concernent |
| Appels d'offres | le BOAMP (France) et TED (Europe), sans clé | les marchés ouverts, et qui a gagné les marchés attribués |

Brevets et marques : pas encore, les sources officielles demandent une clé.

## Ce qui le rend fiable

La plupart des agents de veille confient tout à l'IA. Celui-ci sépare ce
qui se mesure de ce qui se juge.

**Fait par script, sans IA** (`scripts/collecte.py`) :

- la vraie date de chaque article, pas celle que l'IA croit lire ;
- la mémoire de 90 jours : une info envoyée ne revient pas ;
- le regroupement d'une même info reprise par plusieurs médias ;
- la comparaison ligne à ligne des pages suivies ;
- le respect du fichier `robots.txt` de chaque site.

**Fait par l'IA** (`AGENT.md`) : écarter les homonymes et le bruit, noter
l'importance avec une règle écrite, résumer avec les seuls faits des
sources, dire pourquoi l'info compte pour toi.

**Contrôlé avant l'envoi** (`scripts/mail.py`) : chaque info doit renvoyer à
une source que la collecte a trouvée. Sinon, l'envoi est bloqué. Une veille
ne part jamais deux fois.

## Installer en 15 minutes

Trois façons, détaillées dans `references/installation.md` :

| | Cloud | Local, sans rien installer | Local, version complète |
|---|---|---|---|
| Tourne ordinateur éteint | oui | non | non |
| À installer | rien | rien | Python, installé par l'agent |
| Il faut | un compte GitHub gratuit | l'application Claude | l'application Claude |

1. **Récupère l'agent** : « Use this template » sur GitHub pour la version
   cloud, ou « Code » → « Download ZIP » pour la version locale.
2. **Ouvre le dossier dans Claude** (onglet Code).
3. **Colle le texte de `CONFIGURE-MOI.md`.** L'agent pose ses questions,
   trouve et teste tes sources, te montre les 3 formats de mail, fait un
   essai sans rien envoyer, puis programme la veille.

Il faut une offre Claude payante (pour les tâches planifiées) et, pour le
mail, le connecteur Gmail ou Outlook activé dans Claude.

## Personnaliser sans ouvrir un fichier

Tout se demande à l'agent, en une phrase :

| Tu dis | Il fait |
|---|---|
| « Ajoute Protecta » | trouve son site, teste ses sources, propose ses pages à suivre |
| « Surveille sa page tarifs, seulement les prix » | suit la page et ne te prévient que si un prix change |
| « Suis la réglementation sur la facturation électronique » | ajoute les mots-clés et les flux officiels |
| « Passe au format récap » | change le modèle de mail |
| « Mets notre vert et notre logo » | règle `mail.json` et montre le rendu |
| « Plus court, et vouvoie-moi » | l'écrit dans `veille.md` |
| « Envoie aussi sur Slack » | ajoute le canal |

**Trois formats de mail** : `themes` (3 points à retenir, puis les infos par
rubrique avec « pour toi »), `recap` (5 points clés, puis toutes les sources
numérotées), `flash` (l'essentiel en 5 lignes). Un modèle sur mesure se
crée en copiant un fichier de `modeles/`.

**Quatre destinations** : mail (Gmail, Outlook), Slack, Notion, fichier.

## Les fichiers

```
agent-veille/
├── CONFIGURE-MOI.md      le texte à coller pour tout paramétrer
├── LANCER.md             le texte de la tâche planifiée
├── AGENT.md              la méthode que l'agent suit
├── veille.md             qui tu es, ce qui compte, où envoyer
├── sources.json          concurrents, sujets, pages, flux
├── mail.json             format, couleurs, logo, canaux
├── modeles/              les 3 modèles de mail
├── scripts/              collecte et mise en forme (Python sans dépendance)
├── references/           installation, sources officielles, mode sans Python
├── memoire/              ce qui a déjà été envoyé
├── exemples/             une veille fictive complète (Assurly)
└── tests/                67 tests automatiques
```

## Deux modes de collecte

- **Standard, par défaut** : flux RSS, pages publiques, sources officielles
  et recherche web de l'IA. Aucun agrégateur d'actualités.
- **Étendu, à activer toi-même** : ajoute les flux de Google Actualités et
  de Bing Actualités. Plus complet, mais ces flux sont prévus pour un usage
  personnel : lis `references/sources-officielles.md` avant.

Dans les deux modes, l'agent ne contourne aucune protection : pas de
navigateur furtif, pas de CAPTCHA résolu, pas de compte connecté, pas de
réseaux sociaux.

## Limites

- L'agent lit ce qui est public. Un mur payant, une page interdite aux
  robots ou un site qui bloque les serveurs restent fermés.
- Sans Python, les dates et les doublons sont vérifiés par l'IA : c'est
  moins sûr, et la veille le dit.
- Le résumé est écrit par une IA : chaque info porte sa source, vérifie-la
  avant de la reprendre.
- Les tâches planifiées cloud de Claude sont en aperçu : leur
  fonctionnement peut changer.

## Vérifier et contribuer

```bash
python3 -m unittest discover -s tests        # 67 tests, sans réseau
python3 scripts/collecte.py --diagnostic     # ton installation, étape par étape
```

Les tests tournent sur Linux, macOS et Windows à chaque modification.
Méthode et sources étudiées : `CREDITS.md`. Cas d'évaluation de l'agent :
`evals/CAS.md`.

Un bug, une source officielle à ajouter ? Ouvre une issue sur GitHub.
Fait par [Join Médicis](https://joinmedicis.com), pour les marketeurs
francophones.
