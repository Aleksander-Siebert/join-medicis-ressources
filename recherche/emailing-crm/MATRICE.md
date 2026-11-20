# Pack Emailing & CRM : collecte et matrice à valider

Statut : **proposition** (20 novembre 2026). Rien n'est écrit dans
`plugins/emailing-skills/` avant la validation de l'utilisateur.

## Sources lues

**Dépôts (clonés en entier)**

- `coreyhaines31/marketingskills`, commit `5b2b400` (19 novembre 2026), MIT.
  Déjà au catalogue du site en externe (commit `1f83744`). Lus en entier :
  - `skills/emails/` : SKILL.md (v2.1.9), `references/copy-guidelines.md`,
    `sequence-templates.md`, `email-types.md` (structure et grille d'audit),
    `evals/evals.json` ;
  - `skills/cold-email/` : SKILL.md (v2.2.7), `references/deliverability.md`,
    `benchmarks.md`, `personalization.md`, `follow-up-sequences.md`,
    `reply-handling.md`, `subject-lines.md` ;
  - `skills/prospecting/references/compliance.md` ;
  - `skills/revops/SKILL.md` (structure : cycle de vie, scoring, routage,
    hygiène des données) ;
  - `tools/integrations/hubspot.md`, `brevo.md`, `precleared.md` (mention
    France), liste de `tools/clis/` et de `tests/clis/`.
- `l3mpire/claude-skills` (lemlist), commit `f3a97ea` (18 mai 2026), MIT.
  Déjà au catalogue. Lus : `copywriting-first-touch`, `reply-handler`,
  `crm-duplicate-detector`, et la liste des 40 Skills avec leur taille.

**Sources primaires (lues le 20 novembre 2026)**

| Source | Date affichée | Ce qu'on en tire |
|---|---|---|
| CNIL, [prospection par courrier électronique](https://www.cnil.fr/fr/la-prospection-commerciale-par-courrier-electronique) | 10 juin 2026 | particuliers : consentement préalable, sauf client existant pour des produits ou services analogues (une simple création de compte ne suffit pas) ; professionnels : information et opposition simple et gratuite si l'objet est en rapport avec la profession ; adresses génériques (contact@, info@) hors de ces règles ; chaque message identifie l'émetteur et permet de refuser simplement |
| CNIL, [recommandation pixels de suivi](https://cnil.fr/fr/recommandation-pixel-suivi-courriels), délibération n° 2026-042 du 12 mars 2026 | 14 avril 2026 | consentement pour les pixels, sauf mesure individuelle de la délivrabilité d'un courriel lié à un service demandé ; adresses déjà collectées : informer sous 3 mois pour permettre l'opposition |
| CNIL, [FAQ de la recommandation](https://cnil.fr/fr/faq-recommandation-pixels-courriers-electroniques) | 22 juillet 2026 | prospection au titre de L34-5 et relance panier : consentement requis ; taux d'ouverture global possible sur des données anonymisées de façon effective ; liens traçants pas visés directement mais soumis à l'article 82 ; l'ouverture d'un courriel n'est pas un « contact » |
| CNIL, [Q/R référentiels gestion commerciale](https://cnil.fr/fr/questions-reponses-sur-les-referentiels-relatifs-la-gestion-des-activites-commerciales-et-des) | 28 janvier 2022 | prospects : 3 ans après la collecte ou le dernier contact venant du prospect (un clic compte), puis relance ou suppression ; clients : durée de la relation puis 3 ans |
| Google, [sender guidelines](https://support.google.com/a/answer/81126) et [FAQ](https://support.google.com/a/answer/14229414) | pas de date | tous : SPF ou DKIM, DNS inverse, TLS, plaintes sous 0,3% ; envoi en masse (environ 5 000 messages par jour vers des comptes Gmail personnels, statut définitif) : SPF et DKIM, DMARC `p=none` au minimum, alignement, désabonnement en un clic (RFC 8058) et lien visible, traitement sous 48 h ; objectif de plaintes sous 0,1% |
| Yahoo, [sender best practices](https://senders.yahooinc.com/best-practices/) | pas de date | mêmes règles ; désabonnements traités sous 2 jours ; seuil d'envoi en masse non chiffré |
| Microsoft, [Outlook.com high-volume senders](https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730) | 30 avril 2025 (v4.0) | plus de 5 000 courriels par jour : SPF, DKIM, DMARC `p=none` aligné ; d'abord en indésirables, refus `550 5.7.515` annoncé, date contradictoire sur la page |

**Non vérifié (reste [à vérifier] tant que la source n'est pas lue)**

- Texte en vigueur de l'article L34-5 du Code des postes et des
  communications électroniques : Légifrance refuse le robot (403). La page
  CNIL le résume.
- Texte intégral de la recommandation pixels (PDF), dernier quart de la FAQ.
- Règles allemande, italienne et autrichienne citées par marketingskills
  (consentement préalable en B2B) : pas lues à la source.
- Coupure des emails de plus de 102 Ko par Gmail : chiffre courant, aucune
  source Google lue.
- MCP officiels HubSpot (annoncé « GA le 13 avril 2026 » par marketingskills)
  et Brevo : à vérifier aux pages des éditeurs.

## Ce que les Skills existants font bien, et où ils cassent pour un public français

**Ce qu'on reprend** : un email, un objectif ; la valeur avant la demande ;
les séquences types (bienvenue, nurturing, réactivation, onboarding) ; la
grille d'audit des emails du cycle de vie ; les tics d'IA interdits ; la
classification des réponses et ce qu'un agent peut faire seul ; les règles
d'arrêt (rebonds, plaintes) ; les relances qui apportent chacune un angle
nouveau ; le message de rupture qui est ensuite respecté.

**Où ils cassent**

1. **Le droit français est absent.** `compliance.md` traite les USA, le
   Royaume-Uni, l'Allemagne, l'Italie et l'Autriche, pas la France. La
   différence particuliers / professionnels de la CNIL et l'exception
   « client, produits analogues » n'apparaissent nulle part.
2. **Le taux d'ouverture.** `emails` le suit toujours (en tendance). Depuis
   la recommandation CNIL d'avril 2026, le pixel qui le mesure demande le
   consentement, notamment en prospection. Les deux Skills ignorent ce
   point. `cold-email` conseille déjà de couper le suivi des ouvertures,
   pour d'autres raisons.
3. **Des chiffres d'éditeurs présentés comme des faits** : « +250% de
   réponses » (Lavender), « 2 mots = 60% d'ouvertures en plus », « jeudi
   6,87% »… Le fichier `benchmarks.md` reconnaît lui-même que ces chiffres
   viennent de vendeurs d'outils et se mesurent différemment.
4. **Des dates trop affirmées** : « rejets permanents depuis novembre 2025 »
   chez Gmail, alors que la FAQ Google dit « renforce progressivement » ;
   « rejet depuis le 5 mai 2025 » chez Microsoft, alors que la page est
   contradictoire.
5. **Aucun script de mesure.** marketingskills a des clients d'API en Node
   (Brevo, Mailchimp, Klaviyo…), utiles pour envoyer, pas pour contrôler.
   Le détecteur de doublons de lemlist fait tout le travail par le modèle,
   sans script : peu fiable au-delà de quelques centaines de lignes.
6. **Pas de newsletter éditoriale.** `emails` la cite en une ligne (« monthly
   roundup ») ; rien sur la ligne éditoriale, le rythme, le recyclage.
7. **Claude seulement par endroits** : chemins `.claude/`, renvois à
   d'autres Skills du même dépôt, guides en ligne. Utilisable ailleurs, mais
   pas pensé pour.

## Skills prévus (5), préfixe `/email-*`

Chaque Skill lit `entreprise.md` (pack Fondation) s'il existe, ne publie et
n'envoie rien, et rend du texte dans la conversation par défaut.

| Skill | Ce qu'il fait | Script testé |
|---|---|---|
| `/email-sequence` | séquences automatisées : bienvenue, nurturing, onboarding, relance de panier, réactivation, fin d'essai. Pour chaque email : déclencheur, délai, objet, prétexte, corps, appel à l'action, condition de sortie, **base légale** (consentement, client, professionnel) et **mesure sans pixel** si pas de consentement | `controle_email.py` (partagé) |
| `/email-newsletter` | newsletter éditoriale : promesse, rubriques, rythme, gabarit, objets, recyclage des contenus du blog et de LinkedIn, numéro complet prêt à coller dans Brevo, Mailchimp ou HubSpot | `controle_email.py` |
| `/email-prospection` | email à froid B2B dans le cadre CNIL : tri des contacts (professionnel, adresse générique, particulier exclu), premier message, 3 à 4 relances, message de rupture, mention de la source des données, réponses classées (reprise de reply-handler), opposition appliquée partout | `base.py --prospection` |
| `/email-delivrabilite` | vérifier le domaine d'envoi (SPF, DKIM, DMARC, MX, en-têtes de désabonnement), contrôler un email avant envoi (.eml ou HTML : poids, liens, pixels, mentions, texte brut), lire un rapport de campagne (rebonds, plaintes, désinscriptions) face aux seuils Google et Yahoo | `domaine.py`, `controle_email.py`, `rapport.py` |
| `/email-base` | nettoyer et mettre en conformité une base exportée (CSV) : syntaxe, doublons, adresses génériques et jetables, webmails (probables particuliers), contacts de plus de 3 ans sans clic ni réponse, base légale manquante, segments actifs et inactifs, plan de fusion pour HubSpot ou Brevo | `base.py` |

Écartés pour ce pack, avec la raison :

- **SMS et WhatsApp** : autre canal, autres règles ; plus tard si demandé.
- **Lead scoring et routage RevOps** : utile aux équipes commerciales, pas au
  marketeur qui envoie ; `revops` de marketingskills le couvre déjà.
- **Envoi par API** : contraire à la règle « rien n'est publié à la place de
  l'utilisateur ». Les connecteurs lisent, ils n'envoient pas.

## Matrice

| # | Fonction | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|---|
| 1 | Questions de départ (type de séquence, public, déclencheur, objectif) | `emails` SKILL.md | reprendre | lues dans `entreprise.md` d'abord ; une question à la fois |
| 2 | Séquences types et délais (bienvenue, nurturing, réactivation, onboarding) | `emails/references/sequence-templates.md` | reprendre | exemples Assurly en français ; délais donnés comme points de départ, pas comme normes |
| 3 | Grille d'audit des emails du cycle de vie | `emails/references/email-types.md` | reprendre | ajout des emails imposés ou attendus en France : confirmation d'inscription, rappel de renouvellement **[à vérifier : obligations par secteur]** |
| 4 | Structure et longueur d'un email, boutons ou liens | `emails/references/copy-guidelines.md` | reprendre | typographie française ; vouvoiement ou tutoiement lu dans la voix (Tone of Voice) |
| 5 | Tics d'IA interdits | `emails` et `cold-email` | améliorer | liste française (« N'hésitez pas à », « J'espère que ce message vous trouve bien », « Et si… ? ») reprise du pack LinkedIn |
| 6 | Taux d'ouverture comme indicateur | `emails/references/copy-guidelines.md` | **écarter** comme indicateur par défaut | recommandation CNIL d'avril 2026 : clics, réponses, conversions et désinscriptions par défaut ; ouvertures seulement avec consentement ou en statistique globale anonymisée |
| 7 | Base légale par email | absent | **ajout** | consentement, client et produits analogues, professionnel et profession, adresse générique ; d'après la CNIL (10 juin 2026) |
| 8 | Mentions de chaque message | `cold-email` (CAN-SPAM : adresse postale, désinscription) | améliorer | identité de l'émetteur et refus simple (CNIL) ; source des données au premier message à froid (RGPD article 14, cité par `compliance.md`) **[à vérifier au texte]** |
| 9 | Pixels et liens traçants | absent | **ajout** | contrôle par script : pixel détecté → rappel du consentement, sauf délivrabilité d'un service demandé |
| 10 | Newsletter éditoriale | `email-types.md` (une entrée) | **ajout** | promesse, rubriques, rythme, recyclage des contenus, gabarit |
| 11 | Email à froid : principes, structures, objets | `cold-email` SKILL.md, `frameworks.md`, `subject-lines.md` ; lemlist `copywriting-first-touch` | reprendre | sans les pourcentages d'éditeurs ; objets courts donnés comme pratique, pas comme loi |
| 12 | Personnalisation, faits avant l'angle, « aucun signal trouvé » | `cold-email/references/personalization.md` | reprendre | chaque fait porte sa source (URL et date) ; zéro invention |
| 13 | Relances et message de rupture | `follow-up-sequences.md` | reprendre | rupture « 1, 2, 3 » : la réponse « 3 » vaut opposition et met fin à tout envoi |
| 14 | Réponses classées et ce qu'un agent fait seul | `reply-handling.md` ; lemlist `reply-handler` | reprendre et fusionner | « Comment avez-vous eu mon adresse ? » → source réelle + suppression proposée ; demande de suppression = opposition |
| 15 | Statistiques d'éditeurs (Lavender, Gong, Belkins, Instantly) | `benchmarks.md`, `subject-lines.md` | **écarter** | non reproductibles ; la mesure se fait sur les chiffres de l'utilisateur (`rapport.py`) |
| 16 | Règles Google, Yahoo, Microsoft | `cold-email/references/deliverability.md` | améliorer | chaque règle datée et liée à sa page ; Microsoft marqué contradictoire ; seuils 0,1% et 0,3% contrôlés par script |
| 17 | Domaines secondaires, boîtes, montée en charge, règles d'arrêt | `deliverability.md` | reprendre | volumes donnés comme points de départ d'éditeurs, à confirmer par ses propres tests |
| 18 | Vérification SPF, DKIM, DMARC, MX | absent (conseil seulement) | **ajout** | `domaine.py` : DNS sur HTTPS, sans dépendance ; sélecteurs DKIM courants testés ; rien sans réseau → mode manuel guidé |
| 19 | Contrôle d'un email avant envoi | absent | **ajout** | `controle_email.py` : en-têtes List-Unsubscribe et One-Click, lien de désinscription visible, poids HTML, images sans texte alternatif, liens raccourcis, pixels, mentions |
| 20 | Rapport de campagne | absent | **ajout** | `rapport.py` sur un export CSV (Brevo, Mailchimp, HubSpot) : rebonds, plaintes, désinscriptions, clics, avec les seuils de la ligne 16 |
| 21 | Pays exclus de l'email à froid (Allemagne, Italie, Autriche) | `prospecting/references/compliance.md` | garder avec **[à vérifier]** | règle signalée, pas affirmée, tant que les sources ne sont pas lues |
| 22 | Doublons dans le CRM | lemlist `crm-duplicate-detector` (par le modèle) | améliorer | `base.py` : normalisation (accents, casse, Gmail), courriel exact puis domaine et nom ; plan de fusion relu par l'utilisateur |
| 23 | Durées de conservation | absent | **ajout** | `base.py` signale les prospects sans contact depuis 3 ans (référentiel CNIL) ; l'ouverture ne compte pas comme contact |
| 24 | Hygiène et champs obligatoires du CRM | `revops` (Data Hygiene) | reprendre en partie | champs `source`, `date de collecte`, `base légale` exigés pour la prospection |
| 25 | Connecteurs | `tools/integrations/` (HubSpot, Brevo, Mailchimp…) | améliorer | mode gratuit par défaut : export CSV ; HubSpot et Brevo en lecture par MCP ou API **[à vérifier]** ; jamais d'écriture ni d'envoi |
| 26 | Évaluations | `evals/evals.json` (assertions) | reprendre la forme | tâches françaises, éval à l'aveugle contre `emails` et `cold-email` |

## Compatibilité multi-IA (demande du 20 novembre 2026)

Chaque Skill doit marcher sur Claude, ChatGPT, Gemini et Mistral, et dans
les outils du menu « Autres » du site (Claude Code, Codex, Cursor,
VS Code, GitHub Copilot, Gemini CLI, Mistral Vibe, Hermes Agent, Goose,
Kiro, OpenClaw).

- Standard Agent Skills seulement : `SKILL.md` avec `name` et `description`,
  `references/`, `scripts/`. Aucun nom d'outil propre à Claude, aucun
  chemin `.claude/`, pas de sous-agent ni de hook.
- **Le jugement d'abord, les scripts ensuite.** Sans exécution de code
  (ChatGPT, Gemini, Mistral sur le web), chaque script a sa grille à suivre
  à la main dans le SKILL.md. Le script affine, il n'est jamais indispensable.
- Les scripts : Python 3 standard, sans dépendance, testés sous 3.9 et plus.
- Connecteurs facultatifs : un CSV collé ou joint suffit toujours.
- À tester sur les quatre IA avant de changer la pastille « En test ».

## Points à valider

1. Les 5 Skills ci-dessus, et leurs noms.
2. Le Skill modèle à écrire en premier : je propose `/email-prospection`,
   le plus risqué juridiquement et le plus demandé.
3. Le connecteur prioritaire : Brevo (français, très utilisé) ou HubSpot.
4. Des tâches réelles pour l'éval à l'aveugle (une séquence à écrire, une
   base anonymisée, un email à contrôler), sinon j'utilise Assurly.
