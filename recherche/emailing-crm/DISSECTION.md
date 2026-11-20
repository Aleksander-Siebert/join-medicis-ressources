# Dissection de trois dépôts de Skills email, pour le futur pack « Emailing & CRM »

Date de la dissection : 20 novembre 2026. Aucun dépôt Join Médicis modifié, rien publié.

Les clones existaient déjà sous `scratchpad/externes/` et correspondent au HEAD distant vérifié par `git ls-remote` le jour même. Les fichiers de travail (exemple HTML, sujets, banc d'essai) sont dans `scratchpad/dissection/work/`.

| Dépôt | Commit | Date du commit | Licence | Fichiers (hors .git) |
|---|---|---|---|---|
| getbrevo/brevo-skills | `88db934` (« chore: publish skills v1.3.0 ») | 17/11/2026 | MIT, © 2026 Brevo | 65 |
| AgriciDaniel/claude-email | `182270a` | 10/04/2026 | MIT, © 2026 Daniel Agrici | 49 |
| sendx/email-skills | `ae6f6ce` (v1.2.0) | 20/07/2026 | MIT, © 2026 SendPost, LLC | 29 |

Les trois licences MIT autorisent la reprise, avec mention dans LICENSE et CREDITS.md.

**Issues et PR.** L'API GitHub est bloquée pour ces dépôts dans cette session, je les ai lues sur les pages publiques :
- brevo-skills : aucune issue ouverte ou fermée visible. 15 PR fermées (CI Slack, ZIP ChatGPT, durcissement sécurité du `sync`, bumps Dependabot, « make this repository a published copy »). Les Skills sont écrits dans un dépôt source privé de Brevo : leurs evals et `skill.json` ne sont pas publiés. Evals : {{à compléter}}.
- claude-email : 1 issue ouverte, n°5 du 29/04/2026, « Can't import plugin into Claude Cowork » : il manque `.claude-plugin/marketplace.json`, et l'import Cowork échoue. 7 PR, toutes de Dependabot (lxml, checkdmarc, beautifulsoup4).
- sendx/email-skills : 0 issue, 0 PR.

Repère de lecture : « Solide » = à reprendre, « Fragile » = à corriger ou vérifier, « Manquant » = à construire. Les affirmations que je n'ai pas pu revérifier aux sources primaires portent **[à vérifier]**.

---

## Synthèse en 12 points

1. **Brevo est le plus solide sur l'exécution** (rédaction HTML, vérification, brouillons, automatisations) et le plus rigoureux sur la sécurité : brouillons seulement, oui explicite avant toute écriture, jamais d'envoi de test à une liste vide, contenu traité comme de la donnée. Mais tout dépend de son serveur MCP et rien ne parle de délivrabilité, de RGPD ou de prospection.
2. **claude-email est le plus complet en surface** (6 sous-Skills, 4 agents, 3 scripts, 2 hooks), mais ses scripts sont buggés, centrés sur l'anglais et les États-Unis, et ses chiffres n'ont aucune source.
3. **sendx est le meilleur sur le diagnostic de délivrabilité** (4 piliers, triage, questions, montée en charge par fournisseur), avec des opinions fortes d'un opérateur d'ESP, mais avec beaucoup de chiffres non sourcés et des erreurs juridiques.
4. **Erreurs juridiques pour la France**, présentes dans deux dépôts : « double opt-in obligatoire en Europe » (sendx), « single opt-in non conforme au RGPD » (sendx), « opt-in explicite » exigé pour l'UE (claude-email), prospection B2B froide rangée sous « soft opt-in » (claude-email). Aucun dépôt ne cite l'article L34-5 du CPCE, la CNIL, Bloctel, Signal Spam, ni la règle « STOP » des SMS.
5. **Les trois scripts Python de claude-email, lancés en isolement**, révèlent : score 100/100 silencieux quand BeautifulSoup manque, plantage `KeyError` en sortie texte, problèmes d'images et de poids jamais déduits du score, adresse française jamais reconnue, « Se désinscrire » non reconnu, accents français comptés comme des émojis, arguments `--file` et `--subject` documentés mais refusés, comptage SPF non récursif, absence de réseau lue comme « aucun SPF ».
6. **Aucun dépôt ne nettoie une base CRM en CSV.** Le Skill `email-base` est à construire presque entièrement (quelques règles reprenables chez sendx).
7. **Presque rien sur le SMS, rien sur WhatsApp.** Seul Brevo `automation-create` donne des éléments SMS (alphabet GSM, unicode, type, expéditeur, suivi des liens).
8. **La prospection à froid n'est traitée nulle part sérieusement** : un modèle PAS et une plage de 50 à 125 mots chez claude-email.
9. **Seuils contradictoires entre dépôts** : objet de 6 mots au plus (sendx), de 6 à 10 mots (claude-email), de 40 à 50 caractères (Brevo). Ratio images/texte de 60/40 dans un sens (Brevo) puis dans l'autre (claude-email). Ce qui se mesure doit devenir une mesure, pas une règle d'autorité.
10. **À reprendre en priorité** : la liste de contrôle en 22 points de `email-template-check` (Brevo), les 11 arcs narratifs (Brevo), les règles de design HTML (Brevo), le cadre de diagnostic et le playbook de montée en charge (sendx), les types de séquences et leur logique conditionnelle (claude-email), les règles de sécurité et de confirmation (Brevo).
11. **Dépendances propres à Claude** : claude-email repose sur `allowed-tools`, `user-invocable`, des sous-agents dans `~/.claude/agents`, des hooks jamais enregistrés et des MCP déclarés au mauvais endroit. Brevo repose sur son MCP OAuth (avec une variante par IA). sendx est du Markdown pur.
12. **Des scripts testés sont à écrire** : vérificateur HTML d'email, analyse d'objet en français, contrôle DNS hors ligne (enregistrements collés), compteur de segments SMS, nettoyeur CSV, calcul de contraste.

---

# 1. getbrevo/brevo-skills (commit 88db934, v1.3.0)

## 1.1 Architecture commune

- **10 Skills** sous `skills/<nom>/SKILL.md`, chacun avec `agents/openai.yaml` (métadonnées Codex : nom affiché, description courte, dépendance MCP `streamable_http` vers `https://mcp.brevo.com/v1/openai/mcp`).
- **Aucun script, aucun test publié.** CHANGELOG : « Skills are text only ». Les evals existent dans le dépôt source privé (« `public` once their evals pass on Claude and ChatGPT »). Contenu des evals : {{à compléter}}.
- **Blocs partagés identiques** dans chaque Skill email, vérifiés par comparaison automatique : « Brevo connection rules », « Where this skill comes from », « Working rules for every step », « Conversation cache » (absent d'`automation-create`), « Output rules ». Ils sont dupliqués à la génération à partir de fichiers `shared/*.md` du dépôt source.
- **Manifestes multi-plateformes** : `.claude-plugin/` (MCP `https://mcp.brevo.com/v1/anthropic/mcp`), `.cursor-plugin/`, `.grok-plugin/`, `plugin.json` et `mcp.json` (Agent Plugins), `gemini-extension.json` (MCP `…/v1/google/mcp`), `openai-plugin/` (gabarit du ZIP ChatGPT avec cas de test positifs et négatifs pour la revue OpenAI), `catalog.json` (version, sha256, `requires`, `requires_tools` par Skill, lu par la CLI Brevo).
- **Vérification de fraîcheur** : outil MCP `list_brevo_guides` avec `installed` (nom vers version), statuts `current`, `stale`, `ahead`, `unknown`, `not_installed`. Les Skills peuvent aussi être lus à la demande par `get_brevo_guide`.
- **Règles de connexion** : jamais de clé API ; 401 ou 403 « login » mènent à une reconnexion ; 403 « required scope not present » fait sauter l'étape (avec repli prévu) ; un outil absent arrête l'étape sans improvisation ; `subaccount_id` à chaque appel sur un sous-compte ; l'erreur de l'outil est montrée telle quelle.
- **Règles de travail** : étapes dans l'ordre, outils nommés seulement, oui de l'utilisateur avant toute création ou modification (« un oui ne couvre que ce qui a été décrit »), chaque objet lu une seule fois, résultat rapporté uniquement d'après le retour de l'outil, réponse dans la langue de l'utilisateur.
- **Cache de conversation** : notes dans la conversation, jamais un fichier, clé compte et sous-compte, `fetchedAt`, durées (environ 10 min pour compte, expéditeurs et attributs ; toute la conversation pour le kit de marque et les modèles ; listes et segments jamais en cache), budget d'appels chiffré (11 appels avec cache, 16 sans, pour un modèle transactionnel).
- **Règles de sortie** : un objet par demande, pas de gros HTML ou JSON collé dans la conversation, problèmes décrits par ce que voit l'utilisateur, fin systématique sur nom, ID, lien Brevo et reste à faire.

**Dépendances propres à Claude ou à Brevo** : aucune `allowed-tools`. Tout passe par le MCP Brevo (OAuth 2.1 avec PKCE). Sans connexion, seul `email-template-write` fonctionne (« mode hors ligne » avec marqueurs à remplacer). `brevo-cli` exige un terminal (`compatibility`).

**Bugs et cas limites tirés du CHANGELOG et des fichiers** :
- `email-test-send` supprimé en 1.1.0, remplacé par `email-test-preview`. Pourtant le README (« What you can ask ») et les deux modèles d'issue citent encore `email-test-send`.
- `GEMINI.md`, généré, ne liste que `brevo-cli` et `brevo-guide` : les Skills email ne ciblent pas Gemini (`platforms: claude, openai`), car le serveur Google n'expose pas certains outils (CHANGELOG 0.1.0 : « The google server does not expose `templates_get_smtp_template` or `templates_send_test_template` »).
- `{% else %}` dans un `{% for %}` fait échouer l'aperçu et l'enregistrement glisser-déposer (« Tag 'else' not found »).
- Un filtre de date (`time_parse`) sur une valeur vide fait échouer **tout** l'email. Les envois de test n'ont pas de `params`.
- Un envoi de test avec `emailTo` vide part vers **toute la liste de test du compte**.
- `email_editor_create_template` prend `automation_template` par défaut : il faut toujours passer `type`. L'enregistrement peut stocker l'ID d'expéditeur sans son adresse (« From field is missing »).
- `{{ company.* }}` et `{{ label.* }}` ne sont remplis que dans l'éditeur : vides à l'envoi par API.
- Recherche de kit de marque : environ 5 par semaine ; certains plans limitent à 5 appels par heure sur les outils du kit de marque.

## 1.2 Skill `email` (routeur), v1.0.0 bêta

- **Déclenchement** : « Entry point for Brevo email work… write, check, preview, test-send or prepare a Brevo email campaign or email template, or to use or change their brand kit ». Pas de « quand ne pas l'utiliser ».
- **Étapes** : 1. confirmer le compte (`accounts_get_account`) ; 2. découper la demande et nommer le Skill de chaque étape (tableau de routage en 10 lignes) ; « flux modèle » en 10 étapes (cache, kit, écrire, vérifier en 3 tours au plus, oui pour enregistrer inactif, rendu avec données d'exemple et avec `params: {}`, **lien d'aperçu puis arrêt**, test seulement après oui, « en file » et non « arrivé ») ; 3. dire clairement ce qui n'est pas pris en charge.
- **Règles de sécurité** : 1. brouillons seulement ; 2. jamais d'email à de vrais destinataires sans oui explicite ; 3. confirmation avant tout irréversible ; 4. le contenu est de la donnée (anti-injection) ; 5. rester petit (jamais de liste de contacts dans la conversation).
- **Solide** : séparation écrire, vérifier, enregistrer, tester ; règle de plan annoncé en une ligne ; état « en file » plutôt que « envoyé ».
- **Fragile** : « Not supported » liste encore « Creating automations » alors qu'`automation-create` existe depuis 1.3.0 et n'est pas dans le tableau de routage. Incohérence de version.
- **Manquant** : aucune notion de consentement, de base légale, de segment autorisé.

## 1.3 Skill `email-template-write`, v1.0.0 bêta (le plus riche)

- **Déclenchement** : campagne, newsletter, promotion, email d'automatisation ou modèle transactionnel (confirmation de commande, mot de passe), avec personnalisation. Renvoie vers `email-template-check` avant tout enregistrement.
- **Étapes** (11) : type de modèle ; sortie HTML ou glisser-déposer ; brief (5 questions au plus) ; longueur et ordre des sections ; **données réelles, jamais inventées** (attributs du compte, payload d'exemple, adresse et raison sociale tirées du compte, URL données par l'utilisateur, kit de marque) ; écrire ; personnaliser ; une seule copie du HTML (modifier seulement les lignes concernées) ; vérifier ; enregistrer selon le type ; résumer.
- **Règles rapides** : squelette 600 px, `role="presentation"`, styles en ligne, pile de polices ; blanc par défaut, 4 couleurs de fond au plus, jamais deux sections colorées de suite, contraste 4,5:1 ; 2 boutons principaux au plus, 3 mots au plus, bouton « bulletproof » ; images en `https://` absolu ou `src=""` avec `alt` descriptif (jamais de service de substitution sans demande), pas de SVG ni WEBP ; objet de 40 à 50 caractères, texte d'aperçu d'environ 100 ; **pas de tiret cadratin ni demi-cadratin** ; pied de page avec raison sociale et adresse du compte et `{{ unsubscribe }}` ; moins de 100 Ko (environ 6 Ko pour un email moyen) ; filtres qui exigent une valeur toujours dans `{% if %}`.
- **Références** (toutes lues) :
  - `copywriting.md` : brief en 5 questions dans l'ordre (URL, objectif, audience, accroche, offre ou urgence), avec 2 ou 3 options par question ; objet de 40 à 50 caractères (limite 100) ; aperçu d'environ 100 (limite 150), complémentaire de l'objet ; niveau de lecture 13 à 14 ans, paragraphes de 2 à 3 phrases, phrases de 10 à 20 mots ; « Tease, don't tell » ; cibles de 100, 175 et 300 mots ; intertitres de 2 à 4 mots ; la conclusion fait écho à l'ouverture ; boutons de 3 mots selon le type (e-commerce, B2B, newsletter, événement) ; **« les affirmations correspondent aux données »** (`slice:":5"` donne les 5 premiers du flux, pas les « 5 meilleurs »).
  - `story-arcs.md` : 11 arcs (`flash_sale`, `new_launch`, `founders_letter`, `curated_digest`, `win_back`, `social_proof`, `teacher`, `vip_moment`, `seasonal_greeting`, `personal_outreach`, `second_chance`), 3 longueurs (2-3, 4-5, 6-8 sections) avec longueur par défaut par arc, séquences de sections pour chaque arc, tableau d'anti-modèles par arc (exemple `second_chance` : pas de culpabilisation ni de fausse urgence).
  - `template-types.md` : campagne (`classic`), automatisation (`automation_template`), transactionnel (`template`) ; ce qui marche dans chacun (`params` toujours vide en campagne) ; pied de page ajouté ou non ; texte d'aperçu ; règles de conversion vers le glisser-déposer ; spécificités transactionnelles (payload d'exemple plus variante vide, URL entière dans un seul param, pas d'arithmétique ni de filtre monétaire, dates gardées par `{% if %}`, expéditeur de domaine non authentifié ou gratuit rejeté par Gmail et Yahoo) ; structures sûres (réinitialisation de mot de passe, code OTP, confirmation de commande, suivi d'expédition).
  - `template-language.md` : espaces de noms (`contact`, `params`, `feed`, `unsubscribe`, `mirror`, `update_profile`, `doubleoptin`, `time_now`), variables, conditions, boucles (`{% empty %}`), filtres (`date_i18n:"fr,…"`, `time_in_location:"Europe/Paris"`, `lang_format:"fr,%.2f"`), interdits (`{#`, balises dans les commentaires HTML, syntaxes d'autres outils).
  - `email-design-rules.md` : squelette complet, colonnes et classes `col-*`, couleur, boutons, espacements (24 à 40 px entre sections, interligne 1,7 à 1,9), ordre d'ouverture (h1 jamais une salutation), images (« Aim for about 60% images, 40% text »), logo 90 px puis 60 px, pied de page gris neutre, `data-role` pour la conversion.
  - `sections.md` : extraits prêts (en-tête, héros en deux sections, colonne image et texte, grille de 3 produits, bandeau d'appel à l'action, liste d'articles en boucle dans un seul `<p>`).
  - `footer.md` : pied de page gris, couleur du lien sur un `<span>` (sinon il devient la couleur globale des liens).
  - `global-styles.md` : le premier `<p>`, `<h1>`-`<h3>`, bouton et lien coloré fixent les styles globaux de l'éditeur ; `#FFFFFF` en majuscules.
  - `dnd-blocks.md` : 14 motifs (séparateur, espaceur, citation, réseaux sociaux, navigation, code promo, bouton, deux boutons, avatar, lignes de total, vignette vidéo, grille produits, liens de pied de page, « voir dans le navigateur ») et les blocs impossibles à produire en HTML.
- **Exemples** : extraits HTML complets avec contenus anglais (vélo cargo), prix en euros.
- **Solide** : interdiction d'inventer URL, couleurs, attributs, logos ; mode hors ligne avec liste « Placeholders to replace » ; payload d'exemple gardé avec le HTML ; règle anti-tiret alignée sur la typographie Join Médicis.
- **Fragile** : textes par défaut en anglais (« Unsubscribe », `default:"there"`, « All rights reserved ») ; « environ 60% d'images, 40% de texte » sans source, contredit claude-email ; objet de 40 à 50 caractères sans source.
- **Manquant** : mentions légales françaises du pied de page (identité de l'annonceur, lien de désinscription, politique de confidentialité) ; règles de typographie française ; accessibilité au-delà du contraste.

## 1.4 Skill `email-template-check`, v1.0.0 bêta

- **Déclenchement** : HTML qui vient d'être écrit ou modifié, avant de créer une campagne ou un modèle, ou pour déboguer (« a variable that shows empty, a template that won't save »).
- **Liste de contrôle en 22 points** : syntaxe (1 à 5 : accolades fermées, `if`/`endif`, pas de `{#`, guillemets droits, filtres sous forme deux-points, pas d'arithmétique), variables (6 à 10 : attribut existant écrit exactement, `default` ou `if`, `params` jamais en campagne, chaque chemin `params` dans le payload, lecture avec payload vide, pas de `company.*` ni `label.*`, pas de balises d'autres outils comme `*|FNAME|*` ou `%%FirstName%%`), pied et action (11 et 12 : `{{ unsubscribe }}` obligatoire en automatisation, avertissement en campagne ; au moins un appel à l'action ; pas de `javascript:`), HTML (13 à 17 : images `https://` avec `alt` et `width`, pas de SVG ni WEBP, chaque URL d'image une fois ; balises interdites ; bordure toujours colorée ; doctype et viewport ; moins de 100 Ko), glisser-déposer (18 à 20), objet (21 et 22 : sujet lisible même avec un `params` vide).
- **Corrections** : seulement les lignes concernées, jamais supprimer un contenu demandé, **3 tours au plus**, puis montrer ce qui reste.
- **Rendu serveur** (si enregistré) : 3 rendus (payload complet, payload vide, `params: {}`).
- **Rapport honnête en une ligne** : « Checked by hand against Brevo's rules (no automatic validation was run) ».
- **Solide** : c'est la meilleure grille du lot ; la règle d'honnêteté sur ce qui a été exécuté ; le contrôle lettre à lettre des attributs (une faute de frappe passe sans erreur et affiche la valeur par défaut).
- **Fragile** : tout est fait « à la main » par le modèle, sans script. La majorité des 22 points est mesurable par un script.
- **Manquant** : script de vérification ; mentions légales FR.

## 1.5 Skill `email-template-to-dnd`, v1.0.0 bêta

- **Déclenchement** : rendre un HTML éditable dans l'éditeur glisser-déposer de Brevo.
- **Étapes** : entrées (type toujours passé, aperçu en `previewText`, expéditeur actif, langue `en|fr|de|it|pt`) ; conversion `email_editor_convert_html` (2 Mio au plus, normalisation par défaut, rapport `normalizer` : `changes`, `dropped`, `remaining`, `warning`) ; **vérifier que rien n'est perdu** (textes, liens, ordre, balises) ; confirmer et enregistrer ; relire l'expéditeur et le corriger si l'adresse manque ; lister les étapes restantes dans l'éditeur.
- **Références** : `converter-notes.md` (comment le convertisseur lit le HTML : table de 600 px, une section par `<tr>`, seule la première cellule lue, listes supprimées, 15 px par défaut sur un côté de remplissage manquant), `native-blocks.md` (blocs que seul l'éditeur produit).
- **Intérêt Join Médicis** : propre à Brevo. Le principe « vérifier ce qu'une conversion a perdu » est généralisable (import dans un ESP).

## 1.6 Skill `email-campaign-create`, v1.0.0 bêta

- **Étapes** : entrées (HTML vérifié, objet, aperçu, destinataires) ; liste ou segment (jamais de contacts dans la conversation, poser la question si plusieurs correspondent) ; expéditeur actif, avertissement si domaine non authentifié ou domaine de messagerie gratuite (« Gmail and Yahoo reject or bounce that mail (DMARC) ») ; récapitulatif puis oui ; création **sans jamais `scheduledAt` ni `sendAtBestTime`** ; modification en place ; « Ready to send » : l'utilisateur envoie depuis Brevo.
- **Solide** : l'agent ne planifie ni n'envoie jamais ; le gabarit de confirmation ; l'avertissement DMARC sur les domaines gratuits.
- **Manquant** : aucun contrôle de base légale ni de segment de désinscrits.

## 1.7 Skill `email-test-preview`, v1.0.0 bêta

- **Étapes** : entrées ; rendu serveur (3 rendus, données d'exemple inventées, jamais celles d'un vrai client) ; **lien d'aperçu puis arrêt** ; contrôle du domaine de l'expéditeur ; confirmation à chaque envoi (« Test sends carry no params and are limited to 50 a day ») ; « en file » et contrôle du résultat par `campaign_analytics_get_email_event_report` (lecture de `delivered`, `error`, `softBounces`, `hardBounces`, `blocked`, `invalid`, avec `reason` expliquée).
- **Tableau d'erreurs** : adresse de test inconnue, « Contact not found », limite de 50 par jour, échec de rendu, « From field is missing », rebond lié à DMARC.
- **Solide** : distinction « mis en file » et « délivré » ; interdiction d'un `emailTo` vide.
- **Fait à revérifier** : « limited to 50 a day » est une donnée de la plateforme Brevo [à vérifier dans la doc Brevo, avec date].

## 1.8 Skill `email-brand-kit`, v1.0.4 bêta

- **Étapes** : sous-compte ; lire le kit et le traduire en styles ; proposer un kit depuis le site (environ 5 recherches par 7 jours) ; enregistrer seulement les parties approuvées (`partialUpdateField` ou les 4 parties, en recopiant à l'identique celles non approuvées) ; changer une partie.
- **Règle de couleur mesurable** : seule la première couleur sert aux boutons et liens ; texte de bouton `#FFFFFF` si (299 R + 587 G + 114 B) / 1000 est inférieur ou égal à 140 ; garde-fou contraste 4,5:1 (3:1 seulement pour 18,66 px gras), exemple « `#0092FF` avec blanc = 3,2:1 ». Jamais éclaircir ni mélanger une couleur du kit.
- **Contrôle des liens sociaux** : l'hôte doit correspondre au réseau (`apple-music` vers google.com signalé).
- **Référence** `field-rules.md` : corps d'appel, 12 polices standard, réseaux admis, formats de couleur.
- **Intérêt Join Médicis** : le calcul de contraste est un script simple à écrire et tester. Le reste est propre à Brevo.

## 1.9 Skill `automation-create`, v1.0.0 bêta (ajouté en 1.3.0)

- **Déclenchement** : « send a welcome email when someone joins my newsletter list », « email customers 2 days after their order », « remind contacts on their birthday », et modifications d'une automatisation existante.
- **Étapes** : entrées (déclencheur, étapes, emails, nom, **réentrée** : une fois par contact par défaut, `reentry` si « chaque », « à chaque commande »…) ; lire le catalogue de déclencheurs et d'étapes du compte (`unavailable_triggers`, `readiness: no_event_yet`) ; schéma de chaque type ; **chercher chaque ID avec un outil, jamais de mémoire** ; valider (`automation_validate_workflow`, lire `valid`, 3 essais) ; plan puis oui ; créer en brouillon ; relire et comparer ; activer **seulement sur demande explicite** (« Create it and turn it on » ne suffit pas) ; modifier une existante (version, `changes`, `impact`, contacts qui sortiraient, `confirm_contact_exit` après oui, conflit de version).
- **Cas limites documentés** : `anniversary` compare jour et mois, donc il faut `reentry` pour un anniversaire annuel ; dernier pas jamais un délai ; `delete_contact` toujours en dernier et nommé « suppression définitive » ; `go_to_step` limité à 5 passages, avec délai obligatoire ; `percentage_split` (2 variantes sur tous les plans, jusqu'à 10 sur Pro ou Enterprise) ; fenêtre d'envoi avec fuseau IANA ; durées ISO 8601 (`P2D`, `PT3H`).
- **SMS** (utile au futur Skill SMS) : `send_sms` avec `sender`, `sms_type`, `content` ou `template_id`, avertissement `unicode_needed` (caractères hors alphabet GSM), `link_tracking`, champs de conformité américains (`organisation_prefix`, `unsubscribe_instructions`, `manage_us_compliance`).
- **Solide** : processus « catalogue, schéma, recherche d'ID, validation, plan, oui, création, relecture » ; activation séparée ; gestion des contacts en cours lors d'une modification.
- **Manquant** : pas de conditions (« si ouvert, sinon ») dans ce flux ; aucune règle de pression marketing ni de consentement SMS.

## 1.10 Skills `brevo-guide` et `brevo-cli`

- `brevo-guide` (v1.0.0) : charge un Skill Brevo depuis le serveur MCP. Sa description cite « email, SMS, WhatsApp, contacts, CRM » : le serveur sert peut-être d'autres guides que ceux publiés ici. {{à compléter}}
- `brevo-cli` (v2.6.1, synchronisé depuis getbrevo/brevo-cli) : CLI développeur (applications OAuth, UI, Functions, M2M, revue de publication). Bonnes pratiques génériques (« `--help` est la source de vérité », secrets jamais affichés, `[hidden]` n'est pas un secret, `submit` ne vaut pas soumission). **Hors périmètre marketing : écarté.**

---

# 2. AgriciDaniel/claude-email (commit 182270a, v1.0.0 du 16/02/2026)

## 2.1 Architecture et dépendances propres à Claude

- Orchestrateur `email/SKILL.md` (nom `email`) ; 6 sous-Skills `skills/email-*/SKILL.md` avec `user-invocable: false` ; 4 sous-agents `agents/email-*.md` (frontmatter `allowed-tools`) installés dans `~/.claude/agents` ; 6 références `email/references/` ; 6 modèles sectoriels `skills/email-plan/assets/` ; 3 scripts Python ; 2 hooks ; installeurs bash et PowerShell vers `~/.claude/skills` et `~/.claude/agents`.
- **`allowed-tools`** : orchestrateur `Read, Grep, Glob, Bash, WebFetch, WebSearch` ; sous-Skills restreints (par exemple `email-check` : `Read, Grep, Glob`, alors qu'il doit appeler des outils MCP Gmail : contradiction).
- **MCP** : Gmail (taylorwilsdon/google_workspace_mcp) présenté comme « Required », Microsoft 365, SendGrid, Mailchimp, Kit. La configuration est indiquée dans `~/.claude/settings.json` [à vérifier : Claude Code lit les serveurs MCP dans `~/.claude.json` ou `.mcp.json`, pas dans `settings.json`]. Le paquet Mailchimp est écrit « mailchip-mcp-server » (coquille). La doc cite `ListMcpResourcesTool`.
- **Profil utilisateur** : `email-profile.md` à la racine du projet (README, SKILL) ; le CHANGELOG annonce `~/.claude/profiles/email/profile.json`. Incohérence.
- **Hooks jamais branchés** : `install.sh` copie `hooks/` mais n'écrit aucune entrée dans `settings.json`. `pre-send-check.sh` se dit « PreToolUse (Bash) » mais lit ses arguments ou stdin comme un email brut, alors qu'un hook Claude Code reçoit du JSON. `validate-email-html.py` attend un chemin en `argv[1]`, alors qu'un hook PostToolUse reçoit du JSON sur stdin. Ils ne marchent donc pas comme hooks.
- **Installeur** : `pip3 install -r requirements.txt` global, alors que SECURITY.md affirme « Python dependencies install in isolated virtual environments ». Faux. Le contrôle exige « Python 3.7+ » alors que le README dit 3.10+.
- **Désinstalleur buggé** : `uninstall.sh` utilise `((REMOVED_COUNT++))` sous `set -euo pipefail`. Quand le compteur vaut 0, l'expression renvoie le code 1 et le script s'arrête après la première suppression. J'ai reproduit le comportement avec mon propre extrait (`bash -c 'set -e; N=0; ((N++)); echo atteint'` ne va pas jusqu'à l'echo), sans exécuter leur script.
- **Plugin** : `.claude-plugin/plugin.json` seul, sans `marketplace.json` (issue n°5). L'arborescence n'est pas celle d'un plugin (`email/` à la racine plutôt que `skills/email/`).
- **Chemins cassés après installation** : les sous-Skills renvoient à `references/copy-frameworks.md` ou `../../references/copy-frameworks.md`. Une fois installés dans `~/.claude/skills/email-sequence/`, le second chemin pointe vers `~/.claude/references/`, qui n'existe pas. Les références sont dans `~/.claude/skills/email/references/`.
- `requirements.txt` : `beautifulsoup4`, `lxml<6`, `checkdmarc`. **`checkdmarc` n'est importé par aucun script** (le README et la doc disent le contraire).

## 2.2 Orchestrateur `email`

- **Déclenchement** : description très large (« Triggers on: "email", "inbox", "check email", "write email"… »). Risque de déclenchement sur toute mention du mot « email ». Pas de « quand ne pas l'utiliser ».
- **Étapes** : sans argument, profil (4 questions : type d'entreprise, plateforme, régions de conformité US ou EU, voix), détection des MCP, menu ; routage des commandes `/email check|write|review|audit|sequence|plan` ; audit délégué en parallèle à deux sous-agents.
- **« Quality gates »** : objet de 6 à 10 mots ou 30 à 50 caractères ; plaintes sous 0,1% (limite 0,3%) ; rebonds sous 2% ; HTML sous 102 Ko ; « minimum 60% text / 40% images » ; désinscription et adresse postale (CAN-SPAM) ; en-têtes RFC 8058 ; désinscription traitée sous 2 jours ouvrés ; **jamais plus de 20 emails par session sans accord ; toujours montrer le brouillon avant envoi**.
- **Pondérations** : santé (authentification 40%, listes noires 20%, DNS 15%, conformité 15%, TLS 10%) et qualité (objet 25%, texte 25%, HTML 20%, délivrabilité 15%, conformité 15%).
- **Fragile** : régions limitées à « US / EU / both » ; adresse postale obligatoire présentée comme règle universelle.

## 2.3 Sous-Skill `email-sequence`

- **Déclenchement** : séquences automatisées (bienvenue, nurturing, réengagement, panier abandonné, après-achat, demande d'avis, personnalisée).
- **Étapes** : contexte (profil, références) ; besoins ; architecture (nombre, délais, cadre de rédaction par email, logique conditionnelle, KPI) ; chaque email (position, 3 objets notés de 60 à 100, aperçu de 30 à 80 caractères, corps, appel à l'action, logique) ; notes de mise en œuvre.
- **7 gabarits** : bienvenue 4 à 6 emails sur 14 jours (J0, J1, J2, J4, J7, J14) ; nurturing 6 à 10 sur 6 à 10 semaines (80% valeur, 20% promotion) ; réengagement 3 à 5 sur 28 jours, déclenché après **90 jours sans clic** (« not opens, due to Apple MPP »), puis retrait des non-répondants ; panier abandonné 3 sur 3 jours (1 h, 24 h, 48 à 72 h, remise au 3e) ; après-achat 4 à 6 sur 30 jours ; demande d'avis (délais par secteur) ; personnalisée.
- **Logique conditionnelle** : ouvert sans clic, cliqué, 2 emails sans engagement, désinscrit (arrêt immédiat), panier élevé, premier achat, client récurrent.
- **Format de sortie** complet (chronologie, tableau d'objets, aperçu, cadre, corps, logique, test A/B, notes, KPI, suivi, segments) et liste de contrôle.
- **Solide** : catalogue de séquences, déclencheur sur clics plutôt qu'ouvertures (MPP), format normé.
- **Fragile** : KPI cibles sans source (bienvenue 40 à 60% d'ouverture, récupération de panier 10 à 18% puis 5 à 15% ailleurs, contradiction interne) ; « If not opened: wait 24h, resend with subject line variant #2 » (renvoi aux non-ouvreurs, fiabilité nulle avec MPP) ; cadre 4Ps écrit de trois façons selon les fichiers (Promise-Picture-Proof-Push, Picture-Promise-Prove-Push, Problem-Promise-Proof-Proposal) ; seuil « panier élevé » en dollars (« over $200 »).
- **Manquant** : consentement, pression marketing, calendrier français, règles sur les relances de panier en France [à vérifier : position CNIL sur la relance de panier abandonné].

## 2.4 Sous-Skill `email-write`

- **Étapes** : contexte ; choix du cadre (PAS pour la prospection, AIDA pour le lancement, BAB pour la bienvenue, FAB pour une fonctionnalité, 4Ps pour une étude de cas, « Direct » pour un rappel) ; 3 objets (curiosité, bénéfice, urgence) notés avec une grille ; aperçu ; corps ; HTML responsive avec mode sombre ; version texte ; sortie normée avec métadonnées (mots, temps de lecture, caractères, nombre d'appels à l'action) ; 10 contrôles qualité.
- **Fragile** : grille de notation d'objet incohérente (poids 20, 20, 25, -50, 20, 15) ; « power words » (exclusive, secret, breakthrough) qui recoupent les déclencheurs de spam ailleurs ; média query qui passe le corps à 14 px alors que la règle dit 16 px ; renvoi à un Skill `email-send` qui n'existe pas.

## 2.5 Sous-Skill `email-review`

- **Étapes** : entrée (texte, fichier, ID de brouillon Gmail, HTML) ; scripts ; notation manuelle en 5 dimensions ; références ; rapport ; confirmation.
- **Grilles** : objet (longueur, -5 par déclencheur, +5 par « power word », +10 pour personnalisation, émoji +5 ou -5), texte (150 à 300 mots, 1 appel à l'action = 25 points, cadre détecté = 15), HTML (102 Ko, 60/40, viewport, mode sombre, alt, tables, polices, bouton de 44 px, version texte, préheader), délivrabilité (mots de spam, liens : 6 ou plus = -15, raccourcisseurs -10, expéditeur générique -10), conformité (adresse -20, désinscription -25, objet trompeur -15, RFC 8058 -10).
- **Blocages durs** : pas de désinscription, pas d'adresse, plus de 102 Ko, email tout image, objet trompeur.
- **Cas limites** : email texte seul (repondération), **email non anglais (détection de spam sautée)**, transactionnel (règles marketing relâchées).
- **Bugs** : appelle `score_subject_line.py --subject "…"` et `analyze_email_html.py --file …`, deux options refusées par les scripts (vérifié, `unrecognized arguments`). L'exemple RFC 8058 utilise `List-Unsubscribe: <mailto:…>` alors que `compliance.md` exige HTTPS pour le one-click.

## 2.6 Sous-Skill `email-audit`

- **9 catégories et poids** : SPF 10, DKIM 15, DMARC 15, MX 10, PTR 5, TLS 10, listes noires 20, conformité expéditeurs en masse 10, bonus 5 (BIMI, MTA-STS, TLS-RPT, alignement). Barèmes détaillés par catégorie, commandes `dig` et `openssl s_client -starttls smtp`.
- **Délégation à 3 agents**, dont un `email-reputation` qui n'existe pas.
- **Erreur de méthode** : MX, PTR et STARTTLS sont contrôlés sur les serveurs **de réception** (MX) du domaine, alors que la délivrabilité d'une campagne dépend des IP **d'envoi** de l'ESP. Le PTR des MX n'a pas de rapport avec les emails envoyés par Brevo ou Mailchimp.
- **Fragile** : SORBS cité alors que le service a fermé [à vérifier : fermeture annoncée en 2024] ; « DKIM 2048 bits, minimum NIST » [à vérifier] ; « Google : application stricte, rejets 5xx en novembre 2025 » [à vérifier] ; exemple de domaine `rankenstein.cloud` (vrai domaine probable, à ne pas reprendre).
- **Solide** : liste des exigences expéditeurs en masse (SPF et DKIM, DMARC, désinscription en un clic, plaintes sous 0,3%, DNS direct et inverse, désinscription traitée sous 2 jours, TLS), à revérifier aux pages Google, Yahoo et Microsoft avec date ; enregistrements DNS prêts à copier ; gestion d'erreur DNS (« Unable to verify »).

## 2.7 Sous-Skill `email-check` (tri de boîte de réception)

- Score d'importance : base 50, +20 contact VIP, +15 destinataire direct, +10 fil actif, +15 mots d'urgence, +20 invitation, +25 échéance sous 48 h, ±15 pertinence ; catégories Urgent (85+), Important, Routine, Basse, Archive ; 2 réponses proposées (brève, détaillée) pour l'urgent ; cas où il ne faut pas rédiger.
- **Fragile** : le tableau de référence (CC -10, inconnu -10) contredit l'algorithme (CC 0) ; l'agent `email-inbox` utilise un autre barème pondéré ; ses exemples ont des totaux faux (« Score: 95 » pour un total de 90, « 8 » pour 5) ; les mots « suspicious activity, account locked, verify now » augmentent l'urgence, ce qui **fait remonter les emails d'hameçonnage**.
- **Intérêt Join Médicis** : faible pour le pack (gestion de boîte), sauf le tri des réponses de prospection.

## 2.8 Sous-Skill `email-plan` et ses 6 modèles

- **Étapes** : type d'entreprise ; modèle sectoriel ; stratégie en 7 sections (fondations, segmentation, séquences prioritaires, calendrier éditorial, KPI, configuration de plateforme, feuille de route sur 90 jours en 6 jalons).
- **Modèles** `generic`, `saas`, `ecommerce`, `creator`, `agency`, `local-business` : méthodes de collecte, 5 segments avec taille et fréquence, 5 séquences détaillées, mix de contenus, calendrier saisonnier **américain** (Independence Day, Memorial Day, Thanksgiving), plateformes et **prix** (Mailchimp 13 à 45 $, HubSpot 800 $ et plus, Substack 10%…), KPI.
- **Erreurs pour la France** : « Optional newsletter opt-in (pre-checked or checkbox) » (case précochée invalide en UE) ; « Pre-Checked Boxes: Illegal in EU, allowed in US » ; portail Wi-Fi qui « exige » l'email (consentement conditionné, donc pas libre au sens du RGPD) ; « incentive for review » (avis contre récompense, encadré en France [à vérifier : article L111-7-2 du Code de la consommation] et interdit par Google [à vérifier]) ; « business cards = legitimate interest » (B2B).
- **Fragile** : prix des plateformes non datés ; benchmarks contradictoires (ouverture moyenne 15 à 25% ici, 43,46% dans `benchmarks.md`).

## 2.9 Références de claude-email

- `deliverability-rules.md` : SPF (10 requêtes DNS, un seul enregistrement, qualificatifs, aplatissement), DKIM (sélecteurs par fournisseur, en-têtes à signer, rotation), ARC, DMARC (montée p=none, quarantine, reject, balises), montée en charge d'IP en % du volume cible sur 30 jours, facteurs de réputation, exigences expéditeurs en masse 2024-2026, listes noires (`dig` sur zen.spamhaus.org, dbl.spamhaus.org), MX, PTR, barème. Chiffres sans source : « 18% des grands domaines ont un DMARC valide », « 2,7 fois plus d'arrivée en boîte », « domaine de moins de 30 jours : réputation 40 à 50% plus basse ». Sélecteurs Brevo « mail, mail2 » [à vérifier].
- `compliance.md` : CAN-SPAM, RGPD, CCPA, CASL, RFC 8058, tableau comparatif, conformité par type d'email et par zone. **Erreurs ou approximations** : RGPD réduit à « consentement ou intérêt légitime » sans la directive ePrivacy ni sa transposition française (L34-5 du CPCE) ; « EU/UK Audience : Must obtain explicit consent » (le consentement doit être libre, spécifique, éclairé et univoque ; « explicite » vise les données sensibles) ; « B2B cold outreach (soft opt-in) » sous intérêt légitime (le soft opt-in français vise les clients existants et des produits analogues) ; CASL « droit d'action privé jusqu'à 200 $ par violation » [à vérifier : disposition suspendue depuis 2017] ; amende CAN-SPAM « 51 744 $ » (montant de 2024, revalorisé chaque année [à vérifier]).
- `benchmarks.md` : tableaux par secteur (ouverture moyenne 43,46%, clics 2,2%…), seuils de notation, ROI « 36 $ pour 1 $ », « 760% de revenus en plus avec la segmentation », séquences, délivrabilité, appareils, objet (+26% avec personnalisation), aperçu, tests A/B (1 000 par variante, 95%), fréquences, heures d'envoi américaines. **Aucune source pour aucun chiffre.**
- `copy-frameworks.md` : PAS, AIDA, BAB, FAB, 4Ps avec gabarits et exemples. **L'exemple AIDA met en scène une vraie marque (Cursor) et un témoignage inventé attribué à une personne d'une vraie entreprise (« Sarah Chen, VP Eng @ Lattice »)** : à ne jamais reprendre (règle « zéro invention » et exemples anonymisés). L'exemple PAS cite « 73% of consumers trust online reviews… » sans source.
- `technical-standards.md` : parts de marché des clients mail (sans source), tables, 600 px, CSS en ligne, polices sûres, couleurs, responsive, 44 px, mode sombre, images, coupure Gmail à 102 Ko, limite de 8 192 caractères des blocs `<style>` chez Gmail [à vérifier], préheader, accessibilité (contraste 4,5:1), conditionnels Outlook, VML. **Erreurs** : « Gmail strips `<style>` tags » (Gmail accepte les `<style>` dans `<head>` depuis 2016 [à vérifier]), contredit quelques lignes plus bas par la limite de 8 192 caractères ; `data-ogsc` et `data-ogsb` décrits à l'envers (ce sont des attributs ajoutés par Outlook, « couleur d'origine » et « fond d'origine » [à vérifier]).
- `mcp-integration.md` : installation des serveurs MCP, mode hors ligne, dépannage. Offres gratuites non datées (SendGrid « 100 emails/day forever » [à vérifier]).

## 2.10 Agents de claude-email

- `email-compliance` : régions et règlements, extraction du pied de page, regex d'adresse **américaine** (rue, État, code ZIP à 5 chiffres), regex de lien de désinscription (contient « unsubscribe »), test du lien par `curl -I` (un GET sur un lien de désinscription peut désinscrire réellement), RFC 8058 et couverture DKIM (`h=` contient `list-unsubscribe`), RGPD (preuve du consentement avec horodatage, IP et double opt-in), CCPA, barème, JSON de sortie. **Bug** : le code région « CA » sert à la Californie (CCPA), donc le Canada (CASL) n'est jamais contrôlé.
- `email-deliverability` : script ou contrôles `dig` manuels, barème par composant, recommandations par priorité, JSON. Incohérence : listes noires notées « 0 ou -20 » mais pondérées 20%.
- `email-content` : type d'email et longueur optimale (prospection 50 à 125 mots, promotion 100 à 200, newsletter 200 à 500, nurturing 300 à 600), objet sur 50, cadre sur 20, appel à l'action sur 30, lisibilité, nombre de mots, personnalisation. « 371% more clicks with 1 CTA » sans source. L'exemple AIDA promet « 47% increase in inbox placement » (chiffre inventé dans un exemple).
- `email-inbox` : tri pondéré, voix de marque, exemples (totaux faux, voir 2.7).

## 2.11 Scripts : ce qu'ils font réellement et résultats

Lancés avec `python3 -I chemin/script.py`, depuis `scratchpad/dissection/work/`, sans réseau, sans rien installer. BeautifulSoup et lxml sont absents de l'environnement, `dig` aussi.

### `scripts/score_subject_line.py` (bibliothèque standard seulement)

- **Entrées** : un objet en argument positionnel, ou `--batch fichier`, `--json`. **Sortie** : score de 0 à 100, détail, 5 recommandations, 3 « alternatives ». Code de sortie 1 si score inférieur à 60 (mode unitaire seulement).
- **Calcul** : base 50 ; longueur de 0 à 30 (30 si 6 à 10 mots **et** 30 à 50 caractères, 25 si l'un des deux) ; -5 par déclencheur de spam (liste anglaise de 31 expressions, plafond -25 ; « free » seulement en majuscules ou suivi de « ! ») ; mise en forme (tout en capitales -15, -10 par point d'exclamation au-delà d'un, 2 points d'interrogation -5, **« 3 émojis ou plus » = 3 caractères non ASCII ou plus, -5**) ; « power words » +3 chacun (plafond +15) ; balises de fusion +10 (motifs `{first_name}`, `{{name}}`…) ; nombre +5 ; question en anglais (« How », « What »…) +5, deux-points +3, crochets +3.
- **Résultats sur mes objets d'exemple** :

| Objet | Score | Ce que montre le script |
|---|---|---|
| Votre attestation 2027 est prête | 80 | 5 mots, 32 caractères : la base de 50 et la longueur suffisent à 80 |
| Découvrez l'été à prix réduit chez Assurly | 75 | **« Multiple emoji detected (5) »** : les accents sont comptés comme des émojis |
| Économisez dès aujourd'hui sur votre assurance habitation | 75 | Aucun signal reconnu en français |
| GRATUIT : votre devis en 2 minutes | 88 | « GRATUIT » en capitales non détecté (liste anglaise) |
| {{contact.PRENOM}}, votre devis habitation vous attend | 75 | La balise de fusion Brevo n'est pas reconnue |
| Limited time: new tips to save on insurance | 90 | Déclencheur « limited time » (-5), mais « limited » compté aussi comme « power word » : note finale plus haute que les objets français propres |
| How to save 3 hours a week on claims | 93 | Bonus anglais cumulés |
| FREE!!! ACT NOW | 15 | Seul cas où le script fonctionne comme annoncé |

- Les « alternatives » mélangent anglais et français (« Your Votre attestation Guide: What Top Businesses Know »).
- Appel documenté par `email-review` : `--subject` refusé (`unrecognized arguments: --subject`).
- **Verdict** : écarter tel quel ; l'idée d'une mesure d'objet reste bonne mais à réécrire (longueur en caractères comptés en graphèmes, capitales, ponctuation, balises de fusion des ESP courants, alerte sur un mot de spam seulement si la liste est sourcée).

### `scripts/analyze_email_html.py` (BeautifulSoup facultatif)

- **Entrées** : fichier HTML positionnel ou `--stdin`, `--json`. **Sortie** : poids (alerte au-delà de 80 Ko, critique au-delà de 102 Ko), images (nombre, `alt` manquants, ratio texte/image estimé avec 50 Ko par image divisé par 10), responsive (viewport, `@media`, max-width au-delà de 640 px), mode sombre (`prefers-color-scheme`, meta `color-scheme`, toute occurrence de `#fff`, `white`… signalée comme « fond blanc pur »), mise en page (tables, `display:grid`, `display:flex` écrits exactement ainsi), liens (plus de 5 liens = alerte, raccourcisseurs, lien contenant « unsubscribe »), préheader (classe ou id `preheader`, ou premier `div` ou `span` caché, 30 à 80 caractères), conformité CAN-SPAM (regex d'adresse anglaise, mot « unsubscribe » dans le texte). Score : 100 moins 15, 8 ou 3 par problème.
- **Résultats** (fichier `work/exemple.html`, email Assurly en français, conforme sur le fond) :
  - Sans BeautifulSoup : avertissement sur stderr, puis **score 100, aucun problème**, toutes les cases à `false`. Le script ne détecte plus rien mais affirme que tout va bien.
  - Sortie texte (sans `--json`) : **plantage `KeyError: 'issues'`** dans `format_human_readable`. Ce bug existe aussi avec BeautifulSoup, car le dictionnaire `results["images"]` est recopié sans sa clé `issues`.
  - Appel documenté `--file exemple.html` : refusé (`unrecognized arguments: --file`).
  - Banc d'essai (fonctions chargées depuis le fichier, faux objet `soup`) :
    - `analyze_compliance` sur « Assurly SAS, 12 rue de la Paix, 75002 Paris. Se désinscrire » : adresse `False`, désinscription `False`.
    - Sur « We have 2 new students this year. Unsubscribe » : adresse `True` (« 2 new st » correspond au motif `st`, sans limite de mot).
    - `calculate_score` avec 3 images sans `alt`, un ratio de 10/90 et 120 Ko : **100**, car les problèmes d'images et de poids ne sont jamais recopiés dans `results`.
- **Verdict** : reprendre la liste des contrôles, réécrire le script (bibliothèque standard `html.parser`, échec explicite si l'analyse est impossible, français et anglais, tests).

### `scripts/check_deliverability.py` (bibliothèque standard, mais appelle `dig`)

- **Entrées** : un domaine, `--json`, `--verbose`. **Sortie** : SPF (premier enregistrement `v=spf1`, niveau d'application d'après la **fin** de la chaîne, nombre de requêtes compté sur les seuls mécanismes écrits dans l'enregistrement), DKIM (11 sélecteurs courants, présence d'un enregistrement contenant `v=DKIM1`, `k=rsa` ou `p=`), DMARC (balise `p`, `rua`, `ruf`), MX (fournisseur reconnu). Score : SPF 10, DKIM 15, DMARC 15, MX 10, sur 50 ramené à 100. Code 1 si moins de 60. **N'utilise pas checkdmarc, ne mesure pas la taille des clés DKIM, ne consulte aucune liste noire**, contrairement à la doc.
- **Non lancé tel quel** : il appelle `dig` (réseau) et `dig` est absent. J'ai chargé ses fonctions dans un banc d'essai avec des réponses DNS figées (aucun réseau) :

| Cas | Résultat du script | Problème |
|---|---|---|
| SPF avec 6 `include:` (Google, Brevo, SendGrid, Mailgun, Mailchimp, Microsoft) et `~all` | 6 requêtes, aucun problème | Le décompte n'est pas récursif : chaque `include` en déclenche d'autres, le vrai total dépasse sans doute 10 [à vérifier par résolution réelle] |
| Deux enregistrements SPF | `hard_fail`, aucun problème | Deux SPF rendent l'authentification invalide (RFC 7208, « permerror ») : non détecté |
| `v=spf1 redirect=_spf.example` | niveau `none`, 3 points | Le `redirect` n'est pas suivi |
| DKIM `mail` avec `p=` vide (clé révoquée) | « trouvé » | Une clé révoquée compte comme présente |
| Sélecteur `brevo1` | non essayé | Liste de sélecteurs incomplète [sélecteurs Brevo actuels à vérifier] |
| DMARC `p=quarantine; pct=10; sp=none` | 11 sur 15 | `pct` et `sp` ignorés |
| Toutes les requêtes en échec (pas de réseau) | score 0, « No SPF record found » | Une panne réseau est lue comme une absence d'enregistrement, aucun état « non vérifiable » |
| Domaine exemple ci-dessus | 86/100 | Score flatteur malgré les défauts |

- **Verdict** : écarter le script ; reprendre la liste des contrôles ; réécrire un vérificateur qui accepte des enregistrements collés (mode gratuit, hors ligne) et distingue « absent » de « non vérifiable ».

### Hooks

- `hooks/validate-email-html.py` (lu, non lancé : ce n'est pas un des 3 scripts) : bloque au-delà de 102 Ko, **bloque toute grille ou flexbox** (`display:flex` même dans une media query), avertit sans `<table>`, sans viewport ou avec `<style>`.
- `hooks/pre-send-check.sh` (bash, non lancé) : 8 mots de spam anglais dans l'objet, objet en capitales, corps de moins de 20 mots, blocage si un mot « marketing » est présent sans « unsubscribe ». Détection anglaise seulement.

---

# 3. sendx/email-skills (commit ae6f6ce, v1.2.0)

## 3.1 Architecture et dépendances

- 13 Skills en Markdown pur, sans script ni test. `validate-skills.sh` vérifie seulement le frontmatter (`name`, `description`) et la longueur (moins de 200 caractères = avertissement).
- **Aucune dépendance propre à Claude.** Chaque Skill commence par un bloc « Your Setup — Fill These In » (variables à remplir par l'utilisateur).
- `.claude-plugin/marketplace.json` : 13 plugins séparés (`pluginRoot: ./skills`). Le README dit `/plugin install email-skills`, alors qu'aucun plugin ne porte ce nom.
- **Noms incohérents** : dossiers `ESP-hardbounce-unlock`, `ESP-malicious-behavior-SKILL` et `email-deliverability-expert-skill` ; frontmatter `hardbounce-unlock`, `malicious-behavior` et `email-deliverability` ; marketplace `email-deliverability-expert` ; CLAUDE.md et AGENTS.md écrivent `esp-hardbounce-unlock`. CONTRIBUTING parle de 15 Skills, il en reste 13. Trois `.DS_Store` sont versionnés alors que `.gitignore` les exclut.
- Ton commercial : renvoi constant aux fonctions et aux prix SendX.

## 3.2 `email-deliverability-expert-skill` (nom `email-deliverability`)

- **Déclenchement** : description longue et précise (« audit my email », « why are we hitting spam », réputation, liste noire, montée en charge, rebonds, authentification ; « Even if they just say "our emails aren't working" »). Pas de « quand ne pas l'utiliser ».
- **Deux modes** : audit (liste de contrôle, sévérité, liste de corrections ordonnée) et diagnostic (« the SendPost Way » : triage, 4 piliers, plan, suivi).
- **4 piliers** : infrastructure (SPF, DKIM, DMARC, HELO et DNS inverse, IP partagée ou dédiée), données (rebonds durs sous 0,25 à 0,5%, rebonds temporaires sous 1%, adresses invalides, bounces réimportés d'un ancien ESP), contenu (« en quoi cet email se distingue-t-il d'une arnaque ? », images sous 300 Ko et email sous 1,5 Mo, version texte, taille de police de la désinscription), forme du trafic (lissage sur 3 ou 4 jours, jamais plus de 50% de hausse d'une semaine sur l'autre, limitation par fournisseur, pause en cas de panne Microsoft).
- **Audit** : SPF (10 requêtes, `+all`), DKIM (1024 bits minimum, 2048 préféré), DMARC (de `p=none` avec rapports à `p=reject`), infrastructure (IP partagée sous 100 000 emails par mois), domaine récent (30 à 60 jours), sous-domaine marketing, rebonds temporaires (3 essais sur 72 h), Postmaster Tools et SNDS, qualité de liste (inactifs à 6 mois, adresses de rôle, jetables, fautes de frappe), contenu (60% de texte), cadence. Sévérités rouge, jaune, vert avec exemples.
- **Triage en 5 types** (blocage massif, réputation d'un expéditeur, filtrage de contenu, échec d'authentification, nouveau domaine) avec « première question » pour chacun ; **points de corrélation Gmail** (adresse physique, IP d'hébergement, noms de domaine voisins, identité incohérente, contenus identiques, absence de marque) ; **18 questions de diagnostic en 4 phases** ; arbre de décision de reprise ; **tableau de seuils** (ouverture, rebonds durs, temporaires et totaux, réputation Gmail, plaintes 0,1 et 0,3%, désinscriptions, croissance nette).
- **Références** :
  - `warmup-playbook.md` : semaine de pause consacrée à l'analyse ; 5 segments d'engagement (inscrits de moins de 30 jours, « super fans », actifs à 90 jours, à 180 jours, inactifs) croisés par fournisseur ; validation de la liste ; volumes de départ en reprise (Microsoft 25, Yahoo 50, Gmail 200, iCloud 50 par jour) ; **« jamais plus de 4 fois les ouvertures de la veille »** ; nouveau domaine : 90 jours de « vieillissement » et suggestion d'acheter un domaine d'occasion (à écarter) ; critères de sortie (ouverture au-dessus de 20%, réputation « High »).
  - `provider-specific-tactics.md` : Gmail, Microsoft, Yahoo, iCloud, Proofpoint, Spamhaus ; lecture croisée des signaux par fournisseur ; règle des 4 fois.
  - `shared-pool-management.md` : vue d'opérateur d'ESP (contamination d'IP partagée, garde-fous, secteurs à risque, quand se séparer d'un client). Utile pour comprendre, hors sujet pour un marketeur.
- **Boîte à outils SendX** avec prix (« Inbox Warmup 200 $/mois », « Dedicated IP 300 $/an »…) : publicité, à écarter.
- **Solide** : la structure de diagnostic, les questions, la lecture par fournisseur, « sous 10% d'ouverture, il y a un problème de délivrabilité, quoi qu'on pense de la fiabilité des ouvertures », la priorité aux causes plutôt qu'aux symptômes, les limites (« tu ne peux pas vérifier le DNS toi-même »).
- **Fragile** : chiffres issus d'expérience sans source (règle des 4 fois, volumes de départ, 90 jours de vieillissement) ; « un décalage HELO et DNS inverse provoque un listage Spamhaus automatique » [à vérifier] ; « Microsoft sépare Outlook.com et Hotmail » [à vérifier] ; « Microsoft greylisting with code 400 » [à vérifier] ; indicateurs de pièges à spam « domaines personnalisés à 5 lettres » (heuristique non sourcée) ; SORBS cité alors qu'il a fermé [à vérifier] ; ouverture « saine » au-dessus de 20% sans tenir compte de MPP.
- **Manquant** : fournisseurs français (Orange, SFR, Free, laposte.net) [à vérifier : particularités publiques de chacun] ; Signal Spam ; exigences Google, Yahoo et Microsoft en détail (désinscription en un clic) ; aucun outil de mesure.

## 3.3 `email-copywriting` (v1.1.0, mis à jour en 1.2.0)

- **Contenu** : objet de **6 mots au plus** (« every top-open-rate email… No exceptions ») ; structure « [Résultat] + sans / même si + [sacrifice] » ; préheader comme second objet (« environ 40 caractères ») ; corps en pyramide inversée en 6 temps ; « différenciateur sacré » ; « tuer l'objection n°1 dans chaque email (90% et plus des gagnants) » ; histoires « 2 à 3 fois plus de clics » ; peur de l'inaction ; cohérence avec la page d'atterrissage ; balises de fusion avec valeur de repli ; ton par type de campagne ; mobile d'abord (« 70% et plus des ouvertures ») ; appel à l'action (pas d'appel « aspirationnel », formule « prix + action + précision » pour une offre payante) ; réengagement ; 6 scénarios de réponse.
- **Solide** : cohérence email et page d'atterrissage, valeur de repli des balises, appel à l'action précis, « use it honestly : jamais de catastrophe inventée ».
- **Fragile** : tout repose sur « an AI-agent analysis of 1,200+ campaigns and 8M+ sends » interne et invérifiable ; le « Limitations » dit « You won't write the entire email body » alors que l'usage attendu est l'inverse.

## 3.4 `compliance-navigator`

- **Contenu** : CAN-SPAM, RGPD, CASL, CCPA ; single ou double opt-in ; désinscription ; conservation ; plaintes ; consentement par liste ; suppression ; centre de préférences ; méthode d'audit en questions.
- **Erreurs** :
  - « the FTC can fine you up to forty-three dollars per email » : erreur manifeste (le montant par email est de plusieurs dizaines de milliers de dollars [à vérifier, montant annuel revalorisé]).
  - « Single opt-in… is not compliant in Europe under GDPR » : faux, un single opt-in avec consentement valable est conforme ; le double opt-in est une preuve recommandée, pas une obligation.
  - « Double opt-in is legally required in Europe and Canada » : faux pour la France [à revérifier sur le site de la CNIL] et pour le CASL [à vérifier].
  - « Implied consent does not work » (CASL) : contredit par le régime de consentement tacite du CASL, que claude-email décrit [à vérifier].
  - « within… thirty days (GDPR in some cases) » : délai non sourcé.
- **Manquant** : L34-5 du CPCE, CNIL, distinction B2C et B2B en France, soft opt-in, durée de conservation des prospects [à vérifier : recommandation CNIL de 3 ans à compter du dernier contact].

## 3.5 Autres Skills sendx

- `email-analytics` : définitions des métriques, matrice métrique, diagnostic, action (ouvertures hautes et clics bas, etc.), MPP et robots, comparaison sur 3 campagnes. **Erreur** : le taux de clic est défini comme « % des emails ouverts où quelqu'un a cliqué » (c'est le taux de clic sur ouvertures). Chiffres d'exemple non sourcés (« B2B security expects fifty percent », « eight percent industry average »).
- `smart-segmentation` : listes, tags et segments ; 8 types de conditions ; 5 segments de départ (engagement, cycle de vie, source, intérêt, réengagement) ; dormance selon la fréquence (90 jours pour un envoi hebdomadaire, 30 pour un envoi quotidien) ; segmentation par fournisseur (MX) ; **politique d'extinction** (180 jours sans engagement, un email de reconquête, puis suppression ou mise en liste de suppression). Réutilisable pour `email-base`.
- `workflow-automation` : cartographier le parcours, déclencheur, branches, délais, **condition de sortie toujours définie**, version la plus simple d'abord, test avec un contact fictif, « no more than 1-2 per day ». Le reste est propre à SendX.
- `campaign-strategy` : choix entre envoi unique, test A/B, séquence, déclenché, RSS. Propre à SendX.
- `ab-testing` : une variable, 1 000 par variante au moins, 24 à 48 h, pas de vainqueur sur un petit écart, calendrier de tests, détection des robots. Aucun calcul statistique.
- `list-growth-engine` : déclencheurs de pop-up (exit intent « captures 2-4% »), formulaires, pages, aimants à prospects, conversions « popups 1 à 3%, landing pages 5 à 15% » (sans source). « Add a GDPR checkbox if you're in the EU. It's not optional—it's law » : approximation.
- `industry-playbooks` : 10 secteurs (3 automatisations, segments, cadence, fonctions SendX). « A strong abandon cart email often recovers 10-15% » sans source. Contenu générique.
- `api-campaign-builder` : API REST SendX. Hors sujet, écarté.
- `ESP-hardbounce-unlock` et `ESP-malicious-behavior-SKILL` : pour le support d'un ESP (déblocage de compte, enquête sur un spammeur). Hors sujet pour un marketeur. À retenir pour `email-base` : le **« math check »** (contacts divisés par mois d'activité ; plus que quelques centaines d'inscrits par jour = suspect), les signes d'une liste achetée (rebonds dès la 1re campagne, domaines sans rapport, pas de formulaire), la distinction pic de rebonds à la première campagne (import) et hausse progressive (vieillissement).

---

# 4. Lignes de matrice candidates, rangées par Skill Join Médicis

Format : Fonction | Source précise (dépôt, fichier) | Verdict proposé.

## 4.1 `email-sequence`

| Fonction | Source précise | Verdict proposé |
|---|---|---|
| Catalogue de 7 types de séquences avec nombre d'emails, durée et délais (bienvenue, nurturing, réengagement, panier abandonné, après-achat, demande d'avis, personnalisée) | claude-email, `skills/email-sequence/SKILL.md` | Améliorer : délais présentés comme points de départ, KPI cibles retirés ou sourcés, calendrier français |
| Logique conditionnelle par email (ouvert sans clic, cliqué, 2 sans engagement, désinscrit, panier élevé, premier achat, récurrent) | claude-email, `skills/email-sequence/SKILL.md` | Reprendre, sans le « renvoi aux non-ouvreurs » (non fiable avec MPP) |
| Format de sortie normé par email (position, 3 objets, aperçu, cadre, corps, appel à l'action, logique, test A/B) | claude-email, `skills/email-sequence/SKILL.md` | Reprendre, avec typographie française et sortie texte simple par défaut |
| Réengagement déclenché sur les clics plutôt que les ouvertures (MPP) | claude-email, `skills/email-sequence/SKILL.md` | Reprendre |
| Condition de sortie toujours définie, version la plus simple d'abord, test avec un contact fictif, 1 à 2 emails par jour au plus | sendx, `skills/workflow-automation/SKILL.md` | Reprendre |
| Processus « catalogue des déclencheurs, schéma, recherche de chaque ID par outil, validation, plan, oui, brouillon, relecture » | brevo-skills, `skills/automation-create/SKILL.md` | Reprendre comme méthode générique pour tout ESP connecté (Brevo, HubSpot) |
| Réentrée (une fois par contact par défaut, « chaque », « à chaque commande » = réentrée), anniversaire annuel qui exige la réentrée | brevo-skills, `skills/automation-create/SKILL.md` | Reprendre (cas limites réels) |
| Activation séparée de la création, jamais sur « crée-le et active-le » | brevo-skills, `skills/automation-create/SKILL.md` | Reprendre |
| Suppression de contact toujours en dernière étape, nommée « suppression définitive », oui explicite | brevo-skills, `skills/automation-create/SKILL.md` | Reprendre |
| Modification d'une automatisation existante : contacts qui sortiraient, conflit de version | brevo-skills, `skills/automation-create/SKILL.md` | Reprendre en référence pour le mode connecté Brevo |
| Arcs `win_back`, `second_chance`, `personal_outreach` avec anti-modèles (pas de culpabilisation, pas de fausse urgence) | brevo-skills, `skills/email-template-write/references/story-arcs.md` | Reprendre |
| Séquences sectorielles (SaaS : essai vers payant, adoption, prévention du churn ; e-commerce ; local ; agence : relance de proposition, QBR ; créateur) | claude-email, `skills/email-plan/assets/*.md` | Améliorer : retirer prix, chiffres non sourcés et calendrier américain |
| Cadres PAS, AIDA, BAB, FAB, 4Ps attribués par email | claude-email, `email/references/copy-frameworks.md` | Améliorer : une seule définition du 4Ps, exemples Assurly, aucun témoignage inventé |
| Exemple AIDA avec vraie marque et témoignage inventé attribué à une personne réelle | claude-email, `email/references/copy-frameworks.md` | Écarter : contraire à « zéro invention » et aux exemples anonymisés |
| KPI cibles par séquence (ouverture 40 à 60%, récupération de panier 10 à 18%…) | claude-email, `skills/email-sequence/SKILL.md`, `email/references/benchmarks.md` | Écarter : aucun chiffre sourcé, contradictions internes ; remplacer par la mesure de la base propre de l'utilisateur |
| Paramètres d'événement (`params`) gardés par `{% if %}`, payload d'exemple et variante vide | brevo-skills, `skills/email-template-write/references/template-types.md` et `template-language.md` | Reprendre pour les séquences transactionnelles et déclenchées |
| Calendrier saisonnier (Independence Day, Memorial Day, Thanksgiving) | claude-email, `skills/email-plan/assets/ecommerce.md`, `local-business.md` | Écarter, remplacer par un calendrier français (soldes aux dates réglementées, fêtes françaises) [dates à vérifier aux sources officielles] |
| Ajout Join Médicis : relance de panier abandonné et base légale en France | Aucune source dans les trois dépôts | Ajouter [position CNIL à vérifier] |
| Ajout Join Médicis : demande d'avis client sans contrepartie cachée | claude-email `assets/local-business.md` propose une incitation | Ajouter la règle française [L111-7-2 du Code de la consommation et règles Google à vérifier] |

## 4.2 `email-newsletter`

| Fonction | Source précise | Verdict proposé |
|---|---|---|
| Brief en 5 questions dans l'ordre (URL, objectif, audience, accroche, offre), options proposées, appel à l'action déduit | brevo-skills, `skills/email-template-write/references/copywriting.md` | Reprendre |
| 11 arcs narratifs, 3 longueurs, ordre des sections, anti-modèles par arc | brevo-skills, `skills/email-template-write/references/story-arcs.md` | Reprendre (cœur du Skill) |
| Règles de rédaction (paragraphes de 2 à 3 phrases, « tease, don't tell », intertitres-accroches, conclusion en écho, pas de tiret cadratin) | brevo-skills, `references/copywriting.md` | Reprendre, traduire, ajouter la typographie française |
| « Les affirmations correspondent aux données » (5 premiers du flux ne sont pas les 5 meilleurs) | brevo-skills, `references/copywriting.md` | Reprendre (rejoint « zéro invention ») |
| Squelette HTML 600 px, colonnes, couleur, boutons « bulletproof », espacements, ordre d'ouverture, images, pied de page | brevo-skills, `references/email-design-rules.md`, `sections.md`, `footer.md` | Reprendre, rendre indépendant de Brevo |
| Interdiction d'inventer URL, logos, couleurs ; `src=""` avec `alt` et liste « à remplacer » | brevo-skills, `references/email-design-rules.md` | Reprendre (cohérent avec `{{à compléter}}`) |
| Liste de contrôle en 22 points avant enregistrement, 3 tours de correction au plus, rapport honnête « vérifié à la main » | brevo-skills, `skills/email-template-check/SKILL.md` | Améliorer : en faire un script testé (bibliothèque standard) pour la partie mesurable, garder le jugement à part |
| Détection des balises d'autres outils (`*|FNAME|*`, `%%FirstName%%`) et correspondance | brevo-skills, `skills/email-template-check/SKILL.md` | Reprendre dans le script, étendre aux ESP courants en France [liste à établir] |
| Contrôles HTML mesurés (poids, viewport, préheader, images, liens, raccourcisseurs, tables) | claude-email, `scripts/analyze_email_html.py` | Améliorer : réécrire (score 100 sans BeautifulSoup, `KeyError`, images et poids jamais déduits, adresse et désinscription anglaises seulement) |
| Hook de validation HTML après écriture | claude-email, `hooks/validate-email-html.py` | Écarter : jamais branché, mauvais format d'entrée, bloque à tort toute flexbox |
| Analyse d'objet notée | claude-email, `scripts/score_subject_line.py` | Écarter tel quel (accents comptés comme émojis, listes anglaises, base de 50) ; réécrire une mesure d'objet bilingue |
| Longueur d'objet (6 mots au plus ; 6 à 10 mots ; 40 à 50 caractères) | sendx `skills/email-copywriting/SKILL.md` ; claude-email `email/SKILL.md` ; brevo-skills `references/copywriting.md` | Améliorer : afficher la mesure (caractères visibles, mots) sans règle d'autorité ; règles contradictoires et non sourcées |
| Préheader complémentaire de l'objet, jamais « voir dans le navigateur » | brevo-skills `references/copywriting.md` ; sendx `email-copywriting` | Reprendre |
| Cohérence email et page d'atterrissage | sendx, `skills/email-copywriting/SKILL.md` | Reprendre |
| Valeur de repli des balises de fusion (« Bonjour , ») | sendx `email-copywriting` ; brevo-skills `template-language.md` | Reprendre |
| Mode sombre, mobile, accessibilité (contraste 4,5:1, alt, `role="presentation"`) | claude-email `email/references/technical-standards.md` ; brevo-skills `email-design-rules.md` | Améliorer : corriger « Gmail strips `<style>` » et `data-ogsc`/`data-ogsb` [à vérifier] |
| Calcul de contraste et couleur du texte de bouton | brevo-skills, `skills/email-brand-kit/SKILL.md` | Reprendre en script testé |
| Ratio images et texte (60/40 dans un sens chez Brevo, dans l'autre chez claude-email) | brevo-skills `email-design-rules.md` ; claude-email `technical-standards.md` | Écarter comme règle : contradictoire et sans source ; mesurer et signaler l'email « tout image » seulement |
| Benchmarks par secteur (ouverture moyenne 43,46%…), ROI 36 pour 1 | claude-email, `email/references/benchmarks.md` | Écarter : aucune source ; si un benchmark est cité, source primaire datée |
| Lecture des métriques (ouvertures hautes et clics bas, MPP, robots, comparaison sur 3 envois) | sendx, `skills/email-analytics/SKILL.md` | Améliorer : corriger la définition du taux de clic, retirer les chiffres d'exemple |
| Test A/B (une variable, 1 000 par variante, 24 à 48 h) | sendx `skills/ab-testing/SKILL.md` ; claude-email `benchmarks.md` | Améliorer : ajouter un calcul de significativité en script |
| Mentions légales françaises du pied de page (identité de l'annonceur, désinscription, lien vers la politique de confidentialité) | Absentes (CAN-SPAM seulement chez claude-email) | Ajouter [textes à vérifier : L34-5 CPCE, LCEN] |

## 4.3 `email-prospection`

| Fonction | Source précise | Verdict proposé |
|---|---|---|
| Cadre PAS pour la prospection, gabarit et exemple | claude-email, `email/references/copy-frameworks.md` | Améliorer : exemple Assurly, retirer la statistique non sourcée |
| Longueur d'un email de prospection (50 à 125 mots) et détection du type | claude-email, `agents/email-content.md` | Améliorer : à présenter comme repère [source à trouver] |
| Séquence de relance de proposition (J1, J3, J7, J10, J14) et « ne jamais seulement relancer, toujours apporter de la valeur » | claude-email, `skills/email-plan/assets/agency.md` | Reprendre, adapter à la prospection |
| Expéditeur dynamique (l'email part du commercial attitré) | sendx, `skills/campaign-strategy/SKILL.md`, `industry-playbooks/SKILL.md` | Reprendre comme principe, sans la fonction SendX |
| « Différenciateur » et « objection n°1 » | sendx, `skills/email-copywriting/SKILL.md` | Améliorer : garder la méthode, retirer « 90% des gagnants » (non vérifiable) |
| Prospection B2B présentée comme « soft opt-in » sous intérêt légitime | claude-email, `email/references/compliance.md` | Écarter : confusion ; réécrire selon le droit français (B2B : message en rapport avec la profession, information et droit d'opposition ; B2C : consentement préalable sauf client existant et produits analogues) [à revérifier sur le site de la CNIL et Légifrance, avec date] |
| Signes d'une liste achetée ou aspirée (rebonds dès le 1er envoi, domaines sans rapport, pas de formulaire, « math check ») | sendx, `skills/ESP-malicious-behavior-SKILL/SKILL.md`, `ESP-hardbounce-unlock/SKILL.md` | Reprendre comme alerte avant tout envoi de prospection |
| Tri des réponses et réponses proposées (brève, détaillée), cas où l'humain doit répondre | claude-email, `skills/email-check/SKILL.md`, `agents/email-inbox.md` | Améliorer : barème unique, ne jamais promouvoir les messages d'hameçonnage, réutiliser pour les réponses de prospection |
| Domaine d'envoi séparé, montée en charge, plafonds par jour | sendx `references/warmup-playbook.md` | Améliorer : chiffres non sourcés, à présenter comme pratiques d'opérateur |
| Plafond « jamais plus de 20 emails par session sans accord », brouillon toujours montré | claude-email, `email/SKILL.md` | Reprendre (aucun envoi à la place de l'utilisateur) |
| Ajout Join Médicis : durée de conservation des prospects et information des personnes | Absent | Ajouter [recommandation CNIL à vérifier] |
| Ajout Join Médicis : LinkedIn et email dans une même séquence | claude-email `assets/agency.md` cite « Email + LinkedIn message » | Améliorer en lien avec le pack LinkedIn existant |

## 4.4 `email-delivrabilite`

| Fonction | Source précise | Verdict proposé |
|---|---|---|
| Deux modes : audit (préventif) et diagnostic (problème en cours) | sendx, `skills/email-deliverability-expert-skill/SKILL.md` | Reprendre |
| 4 piliers (infrastructure, données, contenu, forme du trafic) et triage en 5 types avec « première question » | sendx, `email-deliverability-expert-skill/SKILL.md` | Reprendre |
| 18 questions de diagnostic en 4 phases | sendx, `email-deliverability-expert-skill/SKILL.md` | Reprendre |
| Points de corrélation Gmail (adresse, hébergement, noms de domaine, contenu identique) | sendx, `email-deliverability-expert-skill/SKILL.md`, `references/provider-specific-tactics.md` | Améliorer : présenter comme hypothèses d'opérateur [non documenté par Google, à vérifier] |
| Lecture croisée des signaux par fournisseur (tous en baisse, un seul en baisse, chute brutale, baisse lente) | sendx, `references/provider-specific-tactics.md` | Reprendre |
| Playbook de reprise : semaine d'analyse, segments d'engagement croisés par fournisseur, validation de liste | sendx, `references/warmup-playbook.md` | Reprendre la méthode |
| Volumes de départ (25, 50, 200 par jour) et règle des « 4 fois les ouvertures de la veille » | sendx, `references/warmup-playbook.md` | Améliorer : marquer comme pratique d'opérateur non sourcée, jamais comme règle des fournisseurs |
| Achat d'un domaine d'occasion pour éviter le vieillissement | sendx, `references/warmup-playbook.md` | Écarter : pratique risquée, contournement |
| Tableau de seuils (rebonds, plaintes 0,1 et 0,3%, désinscriptions) | sendx, `email-deliverability-expert-skill/SKILL.md` ; claude-email `references/deliverability-rules.md` | Améliorer : garder seulement les seuils publiés par Google et Yahoo, sources datées [à vérifier] |
| Exigences des expéditeurs en masse (SPF et DKIM, DMARC, désinscription en un clic RFC 8058, plaintes sous 0,3%, traitement sous 2 jours, DNS direct et inverse, TLS) | claude-email, `email/references/deliverability-rules.md`, `compliance.md`, `skills/email-audit/SKILL.md` | Améliorer : revérifier chaque point aux pages Google, Yahoo et Microsoft, dater [dates d'application à vérifier] |
| Barème de santé pondéré (SPF 10, DKIM 15, DMARC 15, MX 10, PTR 5, TLS 10, listes noires 20…) | claude-email, `skills/email-audit/SKILL.md` | Améliorer : retirer MX, PTR et STARTTLS des serveurs de réception (sans rapport avec les IP d'envoi de l'ESP) |
| Vérificateur DNS (SPF, DKIM, DMARC, MX) | claude-email, `scripts/check_deliverability.py` | Écarter tel quel ; réécrire : SPF récursif, SPF multiples, `redirect`, clé DKIM révoquée et longueur de clé, `pct` et `sp` de DMARC, état « non vérifiable », mode gratuit sur enregistrements collés |
| Sélecteurs DKIM par fournisseur | claude-email, `email/references/deliverability-rules.md`, `agents/email-deliverability.md` | Améliorer : sélecteurs Brevo et autres à revérifier dans la doc de chaque ESP |
| Avertissement sur un expéditeur au domaine non authentifié ou de messagerie gratuite (DMARC) | brevo-skills, `skills/email-campaign-create/SKILL.md`, `email-test-preview/SKILL.md` | Reprendre |
| Envoi de test « mis en file » et non « délivré », lecture des événements (délivré, rebond, bloqué) avec la raison | brevo-skills, `skills/email-test-preview/SKILL.md` | Reprendre (mode connecté Brevo), principe généralisable |
| Listes noires à consulter (Spamhaus ZEN et DBL, Barracuda, SpamCop, SURBL, URIBL) | claude-email, `references/deliverability-rules.md` | Améliorer : retirer SORBS [fermeture à vérifier], vérifier les conditions d'usage de chaque liste |
| « Décalage HELO et DNS inverse = listage Spamhaus automatique » | sendx, `email-deliverability-expert-skill/SKILL.md` | Écarter ou marquer [à vérifier] |
| Outils gratuits (Postmaster Tools, SNDS, Safe Browsing) | sendx, `email-deliverability-expert-skill/SKILL.md` | Reprendre, avec un mode gratuit par défaut |
| Prix des outils SendX | sendx, `email-deliverability-expert-skill/SKILL.md` | Écarter : publicité |
| Gestion d'IP partagées et critères pour se séparer d'un client | sendx, `references/shared-pool-management.md` | Écarter : point de vue d'ESP, hors marketeur |
| Ajout Join Médicis : fournisseurs français (Orange, SFR, Free, laposte.net), Signal Spam | Absent des trois dépôts | Ajouter [sources publiques à trouver et dater] |

## 4.5 `email-base` (nettoyage CRM en CSV)

Aucun dépôt ne traite un fichier CSV. Ce Skill est à construire presque entièrement.

| Fonction | Source précise | Verdict proposé |
|---|---|---|
| Suppression des rebonds durs, rebonds temporaires traités après 3 essais en 72 h | sendx, `email-deliverability-expert-skill/SKILL.md` | Reprendre comme règle de nettoyage paramétrable |
| Rebonds de l'ancien ESP réimportés par erreur (exemple : 20% de la liste à retirer) | sendx, `email-deliverability-expert-skill/SKILL.md`, `references/warmup-playbook.md` | Reprendre comme contrôle à l'import |
| Adresses de rôle (info@, admin@), domaines jetables, fautes de frappe de domaine | sendx, `email-deliverability-expert-skill/SKILL.md` | Reprendre, en script testé (listes de domaines à sourcer, fautes de frappe sur les domaines courants en France) |
| Segments d'engagement (actifs, à 90 jours, à 180 jours, jamais ouverts) et politique d'extinction (180 jours, un email de reconquête, puis suppression) | sendx, `skills/smart-segmentation/SKILL.md`, `references/warmup-playbook.md` | Reprendre, avec les durées comme paramètres |
| Dormance selon la fréquence d'envoi (90 jours pour un hebdomadaire, 30 pour un quotidien) | sendx, `skills/smart-segmentation/SKILL.md` | Améliorer : paramètres, pas une règle |
| « Math check » (contacts par mois d'activité) et signes de liste achetée | sendx, `skills/ESP-hardbounce-unlock/SKILL.md`, `ESP-malicious-behavior-SKILL/SKILL.md` | Reprendre en alerte |
| Segmentation par fournisseur de messagerie (domaine ou MX) | sendx, `skills/smart-segmentation/SKILL.md`, `references/warmup-playbook.md` | Reprendre (répartition calculée par le script) |
| Indicateur de piège à spam « domaines personnalisés à 5 lettres » | sendx, `references/warmup-playbook.md` | Écarter : heuristique non sourcée |
| Noms d'attributs exacts, différences de casse, attribut catégorie (`index` et `value`), date `AAAA-MM-JJ` | brevo-skills, `skills/automation-create/SKILL.md`, `skills/email-template-check/SKILL.md` | Reprendre pour la normalisation des colonnes à l'import |
| Correspondance des balises de fusion entre outils | brevo-skills, `skills/email-template-check/SKILL.md` | Reprendre (migration d'ESP) |
| Ne jamais afficher de contacts dans la conversation ; travailler sur des comptes et des identifiants | brevo-skills, `skills/email/SKILL.md` | Reprendre (RGPD, minimisation) |
| Validation d'adresse par envoi ou service tiers (« List Cleaning », « Threat Check ») | sendx, `email-deliverability-expert-skill/SKILL.md` | Écarter les offres SendX ; mentionner l'existence de services de validation sans les recommander [à évaluer] |
| Preuve du consentement (date, source, méthode) dans la base | claude-email, `email/references/compliance.md`, `agents/email-compliance.md` | Reprendre : colonnes de preuve à contrôler dans le CSV |
| Ajout Join Médicis : script de nettoyage CSV (encodage UTF-8 ou Windows-1252, séparateur `;`, doublons, casse, espaces, adresses invalides, colonnes de consentement, rapport avant et après) | Absent | Ajouter, Python sans dépendance, testé |
| Ajout Join Médicis : durées de conservation et suppression des inactifs selon la CNIL | Absent | Ajouter [recommandation CNIL à vérifier] |

## 4.6 Skill SMS et WhatsApp

Les trois dépôts sont presque vides sur ce sujet.

| Fonction | Source précise | Verdict proposé |
|---|---|---|
| Étape SMS d'une automatisation : expéditeur, type, contenu ou modèle, suivi des liens | brevo-skills, `skills/automation-create/SKILL.md` | Reprendre pour le mode connecté Brevo |
| Avertissement sur les caractères hors alphabet GSM (passage en unicode) | brevo-skills, `skills/automation-create/SKILL.md` | Reprendre et en faire un script : compteur de segments GSM-7 et UCS-2 [longueurs de segment à vérifier dans la spécification] |
| Fenêtre d'envoi avec fuseau IANA (`Europe/Paris`), jours et heures | brevo-skills, `skills/automation-create/SKILL.md` | Reprendre, avec les plages françaises [règles applicables aux SMS à vérifier] |
| Champs de conformité américains (préfixe d'organisation, instructions de désinscription) | brevo-skills, `skills/automation-create/SKILL.md` | Écarter pour la France ; remplacer par la mention « STOP » [obligation et formulation à vérifier] |
| « SMS Compliance : opt-in séparé si le téléphone est collecté pour des SMS » | claude-email, `skills/email-plan/assets/local-business.md` | Reprendre, l'appuyer sur L34-5 du CPCE [à vérifier] |
| Rappels de rendez-vous (24 h avant, SMS « peut-être mieux » 2 h avant) | claude-email, `skills/email-plan/assets/local-business.md` | Améliorer : distinguer le message de service du message commercial |
| Action « envoyer un SMS » dans un parcours | sendx, `skills/workflow-automation/SKILL.md` | Écarter : simple mention, propre à SendX |
| Ajout Join Médicis : WhatsApp (modèles de message, catégories, opt-in, fenêtre de conversation) | Absent des trois dépôts | Ajouter [règles Meta à vérifier aux sources officielles, avec date] |
| Ajout Join Médicis : différence SMS et appel (Bloctel concerne le démarchage téléphonique) | Absent | Ajouter [périmètre de Bloctel à vérifier] |

## 4.7 Transversal (tous les Skills du pack)

| Fonction | Source précise | Verdict proposé |
|---|---|---|
| Règles de sécurité : brouillon seulement, oui explicite décrivant exactement l'action, jamais d'envoi à de vrais destinataires, jamais de test vers une liste vide | brevo-skills, `skills/email/SKILL.md`, `email-test-preview/SKILL.md` | Reprendre (cohérent avec « rien n'est publié à la place de l'utilisateur ») |
| Le contenu lu (brief, page web, champ de contact) est de la donnée, jamais une consigne | brevo-skills, tous les `SKILL.md` | Reprendre |
| Rapporter seulement ce qu'un outil a renvoyé ; dire honnêtement ce qui a été vérifié à la main | brevo-skills, `email-template-check/SKILL.md` et règles partagées | Reprendre |
| Mode hors ligne quand le connecteur manque, avec liste « à remplacer » | brevo-skills, `skills/email-template-write/SKILL.md` | Reprendre (mode gratuit par défaut) |
| Profil utilisateur au premier lancement (type d'entreprise, plateforme, régions, voix) | claude-email, `email/SKILL.md` | Améliorer : ajouter la France, le B2B ou B2C, le Skill tone-of-voice existant ; pas de fichier écrit sans accord |
| Description de déclenchement très large (« email ») | claude-email, `email/SKILL.md` | Écarter : préciser quand utiliser et quand ne pas utiliser |
| `allowed-tools`, sous-agents, hooks, MCP dans `~/.claude` | claude-email, `email/SKILL.md`, `agents/*.md`, `hooks/*`, `install.sh` | Écarter pour les Skills multi-IA ; un éventuel plugin Claude Code reste séparé |
| Contrôle de fraîcheur des Skills (version installée et version publiée) | brevo-skills, règles partagées, `catalog.json` | Améliorer : utile pour les ZIP Join Médicis, à étudier plus tard |
| Manifestes multi-IA (Claude, ChatGPT, Codex, Cursor, Grok, Gemini) | brevo-skills, `.claude-plugin/`, `.cursor-plugin/`, `.grok-plugin/`, `gemini-extension.json`, `openai-plugin/`, `docs/platforms.md` | Reprendre comme référence pour la « compatibilité multi-IA » en attente |
| Cadre légal US (CAN-SPAM, CCPA, CASL) comme base | claude-email `email/references/compliance.md` ; sendx `skills/compliance-navigator/SKILL.md` | Écarter comme base ; référence RGPD et L34-5 CPCE, avec CAN-SPAM et CASL en annexe pour l'export [sources primaires datées] |
| « Double opt-in obligatoire en Europe et au Canada », « single opt-in non conforme au RGPD », amende CAN-SPAM de 43 $ | sendx, `skills/compliance-navigator/SKILL.md` | Écarter : faux [à confirmer aux sources] |
| Prix de plateformes et offres gratuites | claude-email `skills/email-plan/*`, `email/references/mcp-integration.md` ; sendx `email-deliverability-expert-skill/SKILL.md` | Écarter : non datés, invérifiables, publicitaires |

---

# 5. Fichiers lus, par dépôt

Tous les fichiers texte ont été lus en entier. Pour Brevo, les 5 blocs partagés ont été lus en entier une fois (dans `email-campaign-create`), puis leur identité dans chaque autre Skill a été vérifiée par un script de comparaison ; les sections propres de chaque Skill ont été lues en entier. Les fichiers binaires sont signalés.

## getbrevo/brevo-skills (65 fichiers)

- Racine : `LICENSE`, `README.md`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `.gitignore`, `brevo-skills.json`, `catalog.json`, `mcp.json`, `plugin.json`, `gemini-extension.json`
- `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`, `.cursor-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, `.grok-plugin/marketplace.json`, `.grok-plugin/plugin.json`
- `.github/CODEOWNERS`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/config.yml`, `.github/ISSUE_TEMPLATE/skill_request.yml`, `.github/workflows/notify-skills-published.yml`
- `docs/distribution.md`, `docs/openai-plugin-update.md`, `docs/platforms.md`
- `scripts/build-openai-plugin.sh` (lu, non exécuté : bash, réseau)
- `openai-plugin/.mcp.json`, `openai-plugin/.codex-plugin/plugin.json`, `openai-plugin/assets/brevo.png` (binaire, PNG 512 × 512, non lu)
- `skills/README.md`
- `skills/automation-create/SKILL.md`, `skills/automation-create/agents/openai.yaml`
- `skills/brevo-cli/SKILL.md`, `skills/brevo-cli/agents/openai.yaml`
- `skills/brevo-guide/SKILL.md`, `skills/brevo-guide/agents/openai.yaml`
- `skills/email/SKILL.md`, `skills/email/agents/openai.yaml`
- `skills/email-brand-kit/SKILL.md`, `skills/email-brand-kit/agents/openai.yaml`, `skills/email-brand-kit/references/field-rules.md`
- `skills/email-campaign-create/SKILL.md`, `skills/email-campaign-create/agents/openai.yaml`
- `skills/email-template-check/SKILL.md`, `skills/email-template-check/agents/openai.yaml`
- `skills/email-template-to-dnd/SKILL.md`, `skills/email-template-to-dnd/agents/openai.yaml`, `skills/email-template-to-dnd/references/converter-notes.md`, `skills/email-template-to-dnd/references/native-blocks.md`
- `skills/email-template-write/SKILL.md`, `skills/email-template-write/agents/openai.yaml`, `skills/email-template-write/references/copywriting.md`, `dnd-blocks.md`, `email-design-rules.md`, `footer.md`, `global-styles.md`, `sections.md`, `story-arcs.md`, `template-language.md`, `template-types.md`
- `skills/email-test-preview/SKILL.md`, `skills/email-test-preview/agents/openai.yaml`
- Pages GitHub publiques : liste des issues (vide) et des PR fermées (15)

## AgriciDaniel/claude-email (49 fichiers)

- Racine : `LICENSE`, `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `.gitignore`, `requirements.txt`, `install.sh`, `install.ps1`, `uninstall.sh`, `uninstall.ps1` (scripts d'installation lus, non exécutés)
- `.claude-plugin/plugin.json`
- `.github/ISSUE_TEMPLATE/bug_report.yml`, `config.yml`, `feature_request.yml`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/dependabot.yml`, `.github/release.yml`
- `assets/header.jpeg` (binaire, image d'en-tête du README, non lu)
- `email/SKILL.md`, `email/references/benchmarks.md`, `compliance.md`, `copy-frameworks.md`, `deliverability-rules.md`, `mcp-integration.md`, `technical-standards.md`
- `skills/email-audit/SKILL.md`, `skills/email-check/SKILL.md`, `skills/email-plan/SKILL.md`, `skills/email-review/SKILL.md`, `skills/email-sequence/SKILL.md`, `skills/email-write/SKILL.md`
- `skills/email-plan/assets/agency.md`, `creator.md`, `ecommerce.md`, `generic.md`, `local-business.md`, `saas.md`
- `agents/email-compliance.md`, `email-content.md`, `email-deliverability.md`, `email-inbox.md`
- `hooks/pre-send-check.sh`, `hooks/validate-email-html.py` (lus, non exécutés)
- `scripts/analyze_email_html.py` (exécuté en isolement et testé fonction par fonction), `scripts/check_deliverability.py` (fonctions testées avec un DNS figé, sans réseau), `scripts/score_subject_line.py` (exécuté en isolement)
- Pages GitHub publiques : issue n°5 et liste des 7 PR

## sendx/email-skills (29 fichiers)

- Racine : `LICENSE`, `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `SKILL_TEMPLATE.md`, `VERSIONS.md`, `.gitignore`, `validate-skills.sh` (lu, non exécuté)
- `.claude-plugin/marketplace.json`
- `skills/ab-testing/SKILL.md`, `skills/api-campaign-builder/SKILL.md`, `skills/campaign-strategy/SKILL.md`, `skills/compliance-navigator/SKILL.md`, `skills/email-analytics/SKILL.md`, `skills/email-copywriting/SKILL.md`, `skills/industry-playbooks/SKILL.md`, `skills/list-growth-engine/SKILL.md`, `skills/smart-segmentation/SKILL.md`, `skills/workflow-automation/SKILL.md`, `skills/ESP-hardbounce-unlock/SKILL.md`, `skills/ESP-malicious-behavior-SKILL/SKILL.md`
- `skills/email-deliverability-expert-skill/SKILL.md`, `references/provider-specific-tactics.md`, `references/shared-pool-management.md`, `references/warmup-playbook.md`
- `skills/campaign-strategy/.DS_Store`, `skills/ESP-hardbounce-unlock/.DS_Store`, `skills/ESP-malicious-behavior-SKILL/.DS_Store` (binaires macOS, examinés avec `strings`, sans contenu utile)
- Pages GitHub publiques : 0 issue, 0 PR

## Fichiers de travail créés (hors dépôts)

- `scratchpad/dissection/work/exemple.html` : email Assurly en français
- `scratchpad/dissection/work/sujets.txt`, `sujets.json` : objets testés et résultats
- `scratchpad/dissection/work/harness.py` : banc d'essai sans réseau (DNS figé, faux objet `soup`)
- `scratchpad/dissection/work/strip_shared.py` : comparaison des blocs partagés Brevo, plus les extraits `*.unique.txt`
