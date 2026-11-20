# Pack Emailing & CRM : collecte et matrice à valider

Statut : **proposition** (20 novembre 2026). Rien n'est écrit dans
`plugins/emailing-skills/` avant la validation de l'utilisateur.

Décisions de l'utilisateur (20 novembre 2026) :

- un 6e Skill, **SMS et WhatsApp** ;
- **rien n'est rédigé** pour l'instant : matrice, structure et infos seulement ;
- **sans connecteur** par défaut (voir « Données ») ;
- exemple d'entreprise : **Join Médicis**, plus Assurly.

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
| CNIL, même page que la première ligne | 10 juin 2026 | le SMS et le MMS suivent les mêmes règles que l'email ; SMS indésirables signalés au 33700 ; aucune mention « STOP » ni plage horaire imposée sur cette page |
| WhatsApp, [Business Messaging Policy](https://whatsappbusiness.com/policy/) | 23 septembre 2026 | accord (opt-in) obligatoire avant tout message ; hors de la fenêtre de 24 h après le dernier message du client, seulement des modèles approuvés ; toute demande d'arrêt respectée, même faite hors WhatsApp ; sanctions : limitation d'envoi, blocage, exclusion |
| Meta, [Getting opt-in](https://developers.facebook.com/docs/whatsapp/overview/getting-opt-in) | pas de date | l'accord nomme l'entreprise et dit clairement à quoi la personne s'inscrit ; il peut être recueilli hors de WhatsApp (site, SMS, papier) ; débit limité si la qualité reste basse |
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
- SMS : mention « STOP » (avec ou sans le 36111) et interdiction d'envoyer
  la nuit, le dimanche et les jours fériés. Ce sont des pratiques courantes,
  mais aucune source n'a été trouvée : ni la CNIL ni le site de la
  Fédération française des télécoms ne les donnent.
- WhatsApp : définition des catégories de messages (marketing, utilitaire,
  authentification) et tarifs : pages produit non lues.
- SMS : 160 caractères par message en alphabet GSM 7 bits, 70 dès qu'un
  caractère hors de cet alphabet apparaît (en français : ê, â, ô, î, û, ç
  minuscule…). Norme 3GPP TS 23.038, pas encore lue à la source.

**Trois dépôts disséqués fichier par fichier (20 novembre 2026)**

Repérés par la recherche des Skills externes
(`recherche/skills-externes/REPERAGE-2026-11-20.md`, 24 dépôts), puis lus
en entier : 143 fichiers. Le détail, Skill par Skill, et la liste des
fichiers lus sont dans `recherche/emailing-crm/DISSECTION.md`.

| Dépôt | Commit, licence | Points forts | Points faibles |
|---|---|---|---|
| `getbrevo/brevo-skills` (officiel Brevo, v1.3.0) | `88db934`, MIT | rédaction HTML (11 arcs narratifs, règles de design), contrôle en 22 points, automatisations en brouillon jamais activées sans « oui », contenu lu traité comme une donnée, mode hors ligne | tout passe par le MCP Brevo pour agir ; rien sur la délivrabilité, le RGPD ou la prospection ; pied de page en anglais |
| `AgriciDaniel/claude-email` (v1.0.0) | `182270a`, MIT | 7 types de séquences et leur logique conditionnelle, réengagement sur les clics plutôt que les ouvertures, modèles par secteur | **3 scripts buggés une fois lancés** (voir ci-dessous) ; chiffres sans source ; très lié à Claude (sous-agents, hooks jamais branchés) ; droit américain ; témoignage inventé attribué à une personne réelle |
| `sendx/email-skills` (v1.2.0) | `ae6f6ce`, MIT | diagnostic de délivrabilité en 4 piliers, triage, 18 questions, plan de reprise, segments d'engagement et politique d'extinction | erreurs juridiques (« double opt-in obligatoire en Europe ») ; volumes non sourcés ; publicité SendX |

Les scripts de claude-email, lancés en isolement sans réseau :

- `score_subject_line.py` compte les accents comme des émojis, ne reconnaît
  ni « GRATUIT » ni les balises Brevo, et note un objet anglais à 93 contre
  75 pour un objet français propre ;
- `analyze_email_html.py` rend **100/100 sans rien vérifier** quand une
  bibliothèque manque, plante en sortie texte, ne déduit jamais les images
  ni le poids, ne reconnaît ni « Se désinscrire » ni une adresse française ;
- `check_deliverability.py` ne suit pas les `include` du SPF, ne voit pas
  deux SPF (invalide selon la RFC 7208), compte une clé DKIM révoquée comme
  présente, ignore `pct` et `sp` de DMARC, et lit une panne réseau comme
  « aucun SPF ».

Conséquence : on reprend leurs **listes de contrôle**, pas leur code. Nos
scripts distinguent « absent » de « non vérifiable » et sont testés sur
des cas français.

Aucun des trois ne nettoie une base CSV, ne traite sérieusement la
prospection, ni WhatsApp. Aucun ne cite L34-5, la CNIL ou Signal Spam.

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

## Skills prévus (6), préfixe `/email-*`

Chaque Skill lit `entreprise.md` (pack Fondation) s'il existe, ne publie et
n'envoie rien, et rend du texte dans la conversation par défaut.

| Skill | Ce qu'il fait | Script testé |
|---|---|---|
| `/email-sequence` | séquences automatisées : bienvenue, nurturing, onboarding, relance de panier, réactivation, fin d'essai. Pour chaque email : déclencheur, délai, objet, prétexte, corps, appel à l'action, condition de sortie, **base légale** (consentement, client, professionnel) et **mesure sans pixel** si pas de consentement | `controle_email.py` (partagé) |
| `/email-newsletter` | newsletter éditoriale : promesse, rubriques, rythme, gabarit, objets, recyclage des contenus du blog et de LinkedIn, numéro complet prêt à coller dans Brevo, Mailchimp ou HubSpot | `controle_email.py` |
| `/email-prospection` | email à froid B2B dans le cadre CNIL : tri des contacts (professionnel, adresse générique, particulier exclu), premier message, 3 à 4 relances, message de rupture, mention de la source des données, réponses classées (reprise de reply-handler), opposition appliquée partout | `base.py --prospection` |
| `/email-delivrabilite` | vérifier le domaine d'envoi (SPF, DKIM, DMARC, MX, en-têtes de désabonnement), contrôler un email avant envoi (.eml ou HTML : poids, liens, pixels, mentions, texte brut), lire un rapport de campagne (rebonds, plaintes, désinscriptions) face aux seuils Google et Yahoo | `domaine.py`, `controle_email.py`, `rapport.py` |
| `/email-base` | nettoyer et mettre en conformité une base exportée (CSV) : syntaxe, doublons, adresses génériques et jetables, webmails (probables particuliers), contacts de plus de 3 ans sans clic ni réponse, base légale manquante, segments actifs et inactifs, plan de fusion pour HubSpot ou Brevo | `base.py` |
| `/email-sms-whatsapp` | SMS et WhatsApp marketing : accord à recueillir (texte de la case, preuve), messages courts (promo, rappel, relance de rendez-vous), identité de l'émetteur et moyen simple de refuser dans chaque SMS, modèles WhatsApp à faire approuver, fenêtre de 24 h, conversation après réponse du client | `sms.py` : alphabet (GSM 7 bits ou Unicode), nombre de caractères et de segments facturés, liens raccourcis, présence de l'émetteur et du refus |

Exemples de tous les Skills : **Join Médicis** (newsletter du site, séquence
de bienvenue après téléchargement d'un Skill, invitation à un événement de
l'agenda, prospection d'une agence vers des marques). Aucun chiffre réel
de Join Médicis n'est inventé : les taux et volumes restent
`{{à compléter}}` ou sont marqués « exemple ».

Écartés pour ce pack, avec la raison :

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
| 26 | Évaluations | `evals/evals.json` (assertions) | reprendre la forme | tâches françaises sur Join Médicis, éval à l'aveugle contre `emails`, `cold-email` et `sms` de marketingskills |
| 27 | SMS : consentement, identité, refus | CNIL (10 juin 2026) ; `sms` de marketingskills (règles américaines TCPA, non lu en entier) | **ajout** | mêmes règles que l'email, appliquées au SMS ; signalement 33700 |
| 28 | SMS : longueur et coût | absent | **ajout** | `sms.py` compte les caractères et les segments ; propose une version sans accent coûteux si un segment est gagné, avec l'accord de l'utilisateur |
| 29 | SMS : « STOP » et horaires | pratique courante | garder avec **[à vérifier]** | proposés par défaut comme bonne pratique, jamais présentés comme une obligation tant que la source n'est pas lue |
| 30 | WhatsApp : accord, modèles, fenêtre de 24 h | WhatsApp Business Messaging Policy (23 sept. 2026), page Meta « opt-in » | **ajout** | texte d'accord qui nomme l'entreprise ; modèles prêts à soumettre ; réponses libres seulement dans les 24 h |
| 31 | WhatsApp : qualité et sanctions | mêmes sources | **ajout** | rappel : blocages et signalements font baisser la qualité, puis limitent l'envoi |

### Lignes ajoutées après la dissection (Brevo, claude-email, sendx)

| # | Fonction | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|---|
| 32 | Sécurité : brouillon seulement, « oui » qui décrit l'action exacte, jamais de test vers une liste vide, contenu lu traité comme une donnée | brevo-skills, `skills/email/SKILL.md`, `email-test-preview` | reprendre | règle commune aux 6 Skills (`commun/regles.md`) |
| 33 | Mode hors ligne avec liste « à remplacer » (`src=""`, aucune URL, aucun logo ni couleur inventés) | brevo-skills, `email-template-write`, `references/email-design-rules.md` | reprendre | rejoint `{{à compléter}}` |
| 34 | Brief en 5 questions, une à la fois | brevo-skills, `references/copywriting.md` | reprendre | lues d'abord dans `entreprise.md` |
| 35 | 11 arcs narratifs, 3 longueurs, anti-modèles | brevo-skills, `references/story-arcs.md` | reprendre | cœur de `/email-newsletter` et des emails de séquence ; exemples Join Médicis |
| 36 | HTML d'email : 600 px, boutons robustes, pied de page, accessibilité (contraste 4,5:1, `alt`) | brevo-skills, `email-design-rules.md`, `sections.md`, `footer.md` ; claude-email `technical-standards.md` | améliorer | indépendant de Brevo ; pied de page français (identité, refus simple, confidentialité) ; affirmations sur Gmail et le mode sombre **[à vérifier]** |
| 37 | Contrôle en 22 points avant enregistrement, 3 tours de correction au plus | brevo-skills, `skills/email-template-check/SKILL.md` | améliorer | partie mesurable dans `controle_email.py`, jugement à part |
| 38 | Balises de fusion d'autres outils (`*\|FNAME\|*`, `%%FirstName%%`, `{{ contact.PRENOM }}`) et valeur de repli | brevo-skills `email-template-check` ; sendx `email-copywriting` | reprendre | détectées par script (migration d'outil, « Bonjour , ») |
| 39 | Calcul de contraste et couleur du texte des boutons | brevo-skills, `skills/email-brand-kit/SKILL.md` | reprendre | en script testé |
| 40 | Logique conditionnelle par email (cliqué, sans engagement, désinscrit, premier achat) ; réengagement sur les clics | claude-email, `skills/email-sequence/SKILL.md` | reprendre | sans relance des « non-ouvreurs » (pixel et protection Apple) |
| 41 | Automatisation : catalogue des déclencheurs, réentrée, activation séparée de la création, suppression de contact en dernier avec « oui » | brevo-skills, `skills/automation-create/SKILL.md` | reprendre | méthode valable pour tout outil, Brevo ou HubSpot en mode connecté |
| 42 | Objets : 6 mots au plus (sendx), 6 à 10 mots (claude-email), 40 à 50 caractères (Brevo) | trois dépôts | **écarter comme règle** | contradictoires et sans source : le script affiche la mesure, l'utilisateur décide |
| 43 | Ratio images et texte (60/40 dans un sens chez Brevo, dans l'autre chez claude-email) | brevo-skills, claude-email | **écarter comme règle** | seul l'email « tout image » est signalé |
| 44 | Diagnostic de délivrabilité : 2 modes (audit, incendie), 4 piliers, triage, 18 questions, lecture croisée par fournisseur | sendx, `email-deliverability-expert-skill/SKILL.md`, `references/provider-specific-tactics.md` | reprendre | cœur de `/email-delivrabilite` |
| 45 | Plan de reprise et volumes de montée en charge (25, 50, 200 par jour) | sendx, `references/warmup-playbook.md` | améliorer | méthode reprise ; volumes marqués « pratique d'opérateur, non sourcée » |
| 46 | Achat d'un domaine d'occasion pour éviter la période de chauffe | sendx, `warmup-playbook.md` | **écarter** | contournement risqué |
| 47 | Vérification DNS du domaine | claude-email, `scripts/check_deliverability.py` | **écarter le code**, reprendre la liste | `domaine.py` : SPF récursif (10 requêtes au plus), SPF multiples, `redirect`, clé DKIM révoquée et longueur de clé, `pct` et `sp` de DMARC, état « non vérifiable », **mode gratuit sur enregistrements collés** |
| 48 | Listes noires (Spamhaus, Barracuda, SpamCop, SURBL, URIBL) | claude-email, `references/deliverability-rules.md` | améliorer | conditions d'usage de chaque liste **[à vérifier]** ; SORBS retiré si fermé **[à vérifier]** |
| 49 | Segments d'engagement et politique d'extinction (180 jours, un email de reconquête, puis suppression) | sendx, `skills/smart-segmentation/SKILL.md` | reprendre | durées en paramètres ; articulées avec les 3 ans de la CNIL (ligne 23) |
| 50 | Rebonds durs, rebonds de l'ancien outil réimportés, signes d'une liste achetée (« calcul de cohérence ») | sendx, `ESP-hardbounce-unlock`, `ESP-malicious-behavior-SKILL` | reprendre | alertes calculées par `base.py` |
| 51 | Ne jamais afficher de contacts dans la conversation : travailler sur des comptes et des identifiants | brevo-skills, `skills/email/SKILL.md` | reprendre | minimisation RGPD : `base.py` rend des comptes et des lignes numérotées |
| 52 | Import CSV : encodage UTF-8 ou Windows-1252, séparateur `;` (exports Excel français), dates `AAAA-MM-JJ`, casse des attributs | absent ; brevo-skills pour les attributs | **ajout** | cas réels des exports français |
| 53 | Preuve du consentement (date, source, méthode) dans la base | claude-email, `email/references/compliance.md` | reprendre | colonnes contrôlées par `base.py` |
| 54 | SMS : alphabet GSM, passage en Unicode, fenêtre d'envoi avec fuseau `Europe/Paris` | brevo-skills, `skills/automation-create/SKILL.md` | reprendre | `sms.py` |
| 55 | Test A/B (une variable, taille d'échantillon) | sendx `ab-testing` ; claude-email `benchmarks.md` | améliorer | calcul de significativité en script |
| 56 | Droit : « double opt-in obligatoire en Europe », « single opt-in non conforme au RGPD », prospection B2B rangée en « soft opt-in » | sendx `compliance-navigator` ; claude-email `references/compliance.md` | **écarter** | la page CNIL du 10 juin 2026 n'exige pas le double opt-in et distingue particuliers et professionnels |
| 57 | Benchmarks par secteur, KPI cibles, ROI « 36 pour 1 », prix des outils | claude-email `benchmarks.md`, `email-plan/*` ; sendx | **écarter** | aucune source ; la mesure se fait sur les données de l'utilisateur |
| 58 | Calendrier commercial américain (Thanksgiving, Memorial Day) | claude-email, `email-plan/assets/*.md` | **écarter** | calendrier français (soldes, fêtes) **[dates à vérifier aux sources officielles]** |
| 59 | Messageries françaises (Orange, SFR, Free, laposte.net) et Signal Spam | absent des trois dépôts | **ajout** | **[sources publiques à trouver et dater]** |
| 60 | Bloctel (démarchage téléphonique) et différence avec le SMS | absent | **ajout** | **[périmètre de Bloctel à vérifier]** |
| 61 | Manifestes multi-IA (Claude, ChatGPT, Codex, Cursor, Grok, Gemini) | brevo-skills, `.cursor-plugin/`, `gemini-extension.json`, `openai-plugin/`, `docs/platforms.md` | reprendre comme référence | pour le ZIP par IA prévu dans « Compatibilité multi-IA » |

## Données : sans connecteur par défaut

Aucun Skill n'exige de connecteur. Trois niveaux, du plus simple au plus
outillé :

1. **Coller** : l'email, le SMS, quelques lignes de la base ou les chiffres
   d'une campagne, directement dans la conversation. Marche sur toutes les
   IA.
2. **Joindre un export CSV** : Brevo, Mailchimp et HubSpot
   exportent contacts et statistiques. Le Skill dit quelles colonnes
   exporter et où les trouver **[à vérifier : chemins des menus par outil]**.
   Les scripts lisent ce fichier.
3. **Connecteur en lecture** (facultatif) : MCP HubSpot ou Brevo si
   l'utilisateur l'a déjà. Jamais d'écriture, de fusion ni d'envoi par le
   Skill.

La vérification du domaine (`domaine.py`) lit le DNS public : aucun compte
n'est nécessaire. Sans réseau, le Skill donne les enregistrements à
vérifier à la main (`dig`, ou un vérificateur en ligne au choix de
l'utilisateur).

## Structure du pack

```
plugins/emailing-skills/
├── .claude-plugin/plugin.json
├── README.md, CREDITS.md, LICENSE
├── skills/
│   ├── email-sequence/
│   │   ├── SKILL.md
│   │   ├── references/  sequences-types.md, audit-cycle-de-vie.md,
│   │   │                redaction.md, mesure-sans-pixel.md
│   │   └── commun/      regles-fr.md, faits.md (règles datées, partagées)
│   ├── email-newsletter/
│   │   ├── SKILL.md
│   │   ├── references/  ligne-editoriale.md, rubriques.md, recyclage.md
│   │   ├── modeles/     numero.md, numero.html
│   │   └── commun/
│   ├── email-prospection/
│   │   ├── SKILL.md
│   │   ├── references/  cadre-cnil.md, premier-message.md, relances.md,
│   │   │                reponses.md, pays.md
│   │   └── commun/
│   ├── email-delivrabilite/
│   │   ├── SKILL.md
│   │   ├── references/  regles-messageries.md, domaine.md, controle.md,
│   │   │                seuils-et-arret.md
│   │   ├── scripts/     domaine.py, controle_email.py, rapport.py
│   │   └── commun/
│   ├── email-base/
│   │   ├── SKILL.md
│   │   ├── references/  colonnes-par-outil.md, doublons.md,
│   │   │                conservation.md, fusion.md
│   │   ├── scripts/     base.py
│   │   └── commun/
│   └── email-sms-whatsapp/
│       ├── SKILL.md
│       ├── references/  sms.md, whatsapp.md, accord.md
│       ├── scripts/     sms.py
│       └── commun/
├── tests/               un fichier de tests par script, données d'exemple
├── templates/           exemples Join Médicis (entrée et sortie)
├── evals/               taches.md, RESULTATS.md
└── claude-ai/           SKILL.md (routeur), build.sh, modules/<nom>/
```

`commun/` est recopié dans chaque Skill (même mécanique que les packs
LinkedIn et Fondation), pour que chaque dossier marche seul une fois
installé. Les règles datées sont dans `commun/faits.md`, revérifiées tous
les 6 mois.

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

1. Les 6 Skills ci-dessus, et leurs noms (`/email-sms-whatsapp` garde le
   préfixe du pack ; autre nom possible : `/email-sms`).
2. Le Skill modèle à écrire en premier, une fois la rédaction lancée : je
   propose `/email-prospection`, le plus risqué juridiquement.
3. Les lignes 32 à 61, ajoutées après la dissection de Brevo Skills,
   claude-email et sendx.
4. Des tâches réelles de Join Médicis pour l'éval à l'aveugle (la vraie
   newsletter, un export anonymisé de la base, un email envoyé).
5. La règle « l'exemple d'entreprise est Assurly » du `CLAUDE.md` : la
   remplacer par Join Médicis pour tous les packs, ou seulement pour
   celui-ci.
