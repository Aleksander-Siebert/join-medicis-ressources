# Pack Fondation : matrices de capacités

État : **à valider par Aleksander** avant toute rédaction (étape 5 du processus,
voir `CLAUDE.md`). Rédigé le 13 octobre 2026.

Objectif fixé par Aleksander : remplacer Growth Context par un pack « vraiment
utile pour n'importe qui », avec quelques Skills essentiels pour que l'IA
comprenne les enjeux d'une entreprise, ses clients et leurs besoins.

## Sources analysées

| Code | Source | Lu | Licence | Dernier commit |
|---|---|---|---|---|
| C | Corey Haines, marketingskills : `product-marketing`, `customer-research` (SKILL, 2 références, évals) | 6 fichiers | MIT | 2026-10-12 |
| P | PMA / Maja Voje, product-marketing-skills : 6 Skills de production + 6 du « Signal Pack » (archives `.skill` décompressées) | 12 SKILL.md + CLAUDE.md | MIT | 2026-07-10 |
| R | Alireza Rezvani, claude-skills : `marketing-context` (SKILL, modèle, script) et `cs-onboard` (SKILL, guide d'entretien, modèle) | 6 fichiers, script exécuté | MIT | 2026-08-26 |
| AS | Anthropic, knowledge-work-plugins / small-business : `smb-onboard` (5 fichiers), `voice-profile.md`, `icp_method.md` | 7 fichiers | Apache 2.0 | 2026-10-11 |
| T | Tribe AI, plugin `brand-voice` (dans knowledge-work-plugins) : découverte, génération, application, agents | 23 fichiers | MIT | 2026-10-11 |
| AR | Arnab, Brand-building-skills : `brand-context`, `target-audience`, `brand-voice`, `brand-positioning` | 4 SKILL.md sur 33 (les autres sont hors sujet : naming, packaging, ads) | MIT | 2026-06-12 |
| B | borghei, Claude-Skills : script d'entretien « switch » (JTBD, Bob Moesta), canevas des 4 forces, 12 erreurs d'entretien | 3 fichiers | **Commons Clause + MIT** : inspiration seulement, rien n'est copié | |
| JM | Nos packs : `seo-context` + `site-context.md` (SEO, GEO), `contexte.md` + `reserve.md` + `reserve.py` (LinkedIn) | 6 fichiers | MIT | |
| GC | Growth Context v1 (le Skill à remplacer) | 1 fichier | MIT | |

Verdicts : ✅ reprendre · ⬆ reprendre en améliorant · ✖ écarter (avec la raison) · ➕ nouveau (aucune source ne le fait).

---

## Ce que les sources nous apprennent (les 9 leçons)

1. **Tout le monde converge vers un fichier de contexte partagé** que les autres
   Skills lisent en premier (C, P, R, AR, AS). La différence se joue sur
   *comment* il est rempli et *si on peut s'y fier*.
2. **Les scores de complétude ne mesurent rien.** Le validateur de R donne
   **100/100 au modèle vide** et 81/100 à une liste de mots-clés sans aucune
   phrase (testé le 13 octobre). Il compte des mots-clés anglais au lieu de
   champs réellement remplis. Il pousse même à inventer : il avertit s'il ne
   trouve « aucun chiffre ».
3. **Les meilleurs séparent le fait de la déduction.** AS : « "a l'air haut de
   gamme" d'après une photo est une supposition ; "à partir de 200 €" sur la
   page tarifs est un fait ». Notre pack LinkedIn va plus loin avec
   LIVE / À CONFIRMER / RETIRÉ, une date et une source par fait. C'est la
   meilleure pratique vue, et elle est chez nous.
4. **Les exemples des sources inventent des chiffres** (P : « LTV:CAC 5:1 »,
   « 40% d'attribution en plus » ; AR : personas avec prénom, âge et citation
   à la première personne inventés). Incompatible avec « zéro invention ».
5. **Un persona sans données est une fiction.** C : pas de persona sous 5 à
   10 données réelles d'un même segment ; sans avis clients, on part de
   sources de substitution (avis des concurrents, produits voisins), chacune
   étiquetée, à remplacer par du premier rang dès que possible.
6. **L'ICP se déduit des clients qui paient, pas de la description du
   dirigeant** (AS) : classer par valeur (revenu × ancienneté, pénalisé par
   les retards de paiement), comparer le premier et le dernier quart, ne
   garder que les critères qui les séparent, 5 critères au plus. Sous 10
   clients, dire honnêtement qu'il n'y a pas encore de motif.
7. **La voix se tire de vrais textes, pas d'adjectifs** (AS, T) :
   « professionnel et chaleureux » décrit tous les emails du monde. Ce qui
   compte : formules d'appel et de fin exactes, longueur de phrase, place de
   la demande, et surtout **ce que la personne n'écrit jamais**. T ajoute :
   la voix est constante, le ton varie sur trois réglages (formalité,
   énergie, technicité) selon le canal.
8. **L'entretien est un savoir-faire** (R, B, C) : une question à la fois,
   relances selon le type de réponse (vague, trop lisse, évitée), signaux
   d'alerte (« on n'a pas de concurrent », « on n'a pas de conflit »),
   tensions entre ce qui est dit et vécu, niveau de confiance de l'entretien.
   Les 4 forces (pousser, attirer, habitude, anxiété) expliquent pourquoi un
   client change ou reste.
9. **Nos trois packs reposent déjà la même question.** `site-context.md`
   (SEO, GEO) et `contexte.md` (LinkedIn) demandent chacun l'entreprise, la
   cible, le ton, les concurrents. La Fondation doit être la source unique
   qu'ils lisent, avec un export vers leurs formats, pas un quatrième
   questionnaire.

---

## Les Skills prévus

Quatre Skills, préfixe `/fondation-*`, un fichier par sujet dans
`~/.claude/fondation/` (ou les connaissances du Projet). Chacun se suffit à
lui-même ; ensemble, ils forment le contexte que lisent les packs SEO, GEO et
LinkedIn.

| Skill | Fichier produit | Ce qu'il fait |
|---|---|---|
| `/fondation-entreprise` | `entreprise.md` | L'entreprise, son offre, son marché, ses concurrents et alternatives, sa différence, ses objectifs du trimestre, ses contraintes (secteur réglementé, RGPD), ses outils |
| `/fondation-clients` | `clients.md` | ICP déduit des vrais clients, personas étayés, jobs à accomplir, 4 forces, objections, anti-persona |
| `/fondation-voix` | `voix.md` | Voix et ton tirés de vrais textes : « nous sommes / nous ne sommes pas », réglages par canal, vocabulaire, interdits |
| `/fondation-preuves` | `preuves.md` | Banque de mots clients (citations sourcées), bibliothèque d'objections, et vérification de chaque promesse marketing contre les preuves disponibles |

Un aiguilleur `claude-ai/SKILL.md` regroupe les quatre pour claude.ai, comme
pour les autres packs.

---

## Matrice 1 : `/fondation-entreprise`

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Fichier de contexte partagé lu par les autres Skills | C, P, R, AR, AS | ✅ | Un fichier par sujet, pas un fourre-tout : les Skills ne lisent que ce qui leur sert |
| Trois modes : brouillon depuis le site, entretien guidé, mise à jour | C, R | ⬆ | Brouillon depuis le site **sans rien inventer** : chaque champ déduit est marqué À CONFIRMER (AS) |
| Lire 3 ou 4 pages du site (accueil, à propos, offres, tarifs), pas un crawl | AS | ✅ | Plus les mentions légales (SIREN, forme, siège) : faits publics vérifiables en France |
| Séparer fait lu et déduction, montrer avant d'enregistrer | AS | ✅ | Étiquettes LIVE / À CONFIRMER / RETIRÉ + date + source par fait, reprises de notre pack LinkedIn |
| Entretien une question à la fois, version courte possible | AS, R | ⬆ | Version courte en 3 questions (offre, client, objectif) quand l'utilisateur est pressé, puis complément au fil des usages |
| Relances selon la réponse (vague, trop lisse, évitée) et signaux d'alerte | R | ⬆ | Réécrites en français et pour un marketeur, pas seulement pour un fondateur de start-up |
| Concurrents directs, secondaires, indirects, statu quo | C, P | ✅ | Le statu quo (« on fait sans », Excel, une agence) toujours listé : c'est souvent le premier concurrent |
| Positionnement (Dunford : alternatives, attributs, valeur, cible, catégorie) | P | ⬆ | Catégorie « annoncée / réelle / possible » (AR) ; filtre « un concurrent pourrait-il dire la même chose ? » |
| Phrase de positionnement (Moore) | P, AR | ⬆ | Version publique en une phrase, sans superlatif invérifiable |
| Objectifs et indicateurs du trimestre | C, R, GC | ⬆ | Objectif vérifiable par un tiers, chiffre seulement s'il est fourni, sinon `{{à compléter}}` |
| Profil fondateur (angles morts, conflits d'équipe, sortie) | R | ✖ | Hors sujet marketing et trop intime pour un fichier partagé ; on garde « la décision repoussée » et « ce qui a cassé ce trimestre », utiles aux priorités |
| Contraintes : secteur réglementé, ce qu'on ne doit jamais affirmer | JM (site-context) | ⬆ | Déplacé ici pour servir tous les packs ; liste des secteurs sensibles en France (santé, finance, assurance, juridique, alcool, jeux) **[à vérifier]** aux sources officielles |
| RGPD de base (base légale de la prospection, mentions) | site (fiche rgpd-context annoncée) | ⬆ | Trois questions seulement (B2B ou B2C, prospection par email, données clients dans l'IA) ; renvoi aux sources CNIL datées, sans conseil juridique |
| Outils et connecteurs disponibles | JM, GC, AS | ✅ | Ne jamais recommander un outil plutôt qu'un autre (règle de neutralité AS) |
| Statut frais / périmé (90 jours) et journal des versions | R, C | ✅ | `contexte.py etat` le calcule ; journal daté « ce qui a changé et pourquoi » (C) |
| Score de complétude par mots-clés | R | ✖ | Mesure fausse (leçon 2). Remplacé par un comptage des champs réellement remplis et sourcés |
| Export vers `site-context.md` et `contexte.md` | (nouveau) | ➕ | `contexte.py exporter --vers seo|linkedin` pré-remplit les fichiers des autres packs |
| Brouillon depuis le code (README, package.json) | C, R | ✖ | Pensé pour des développeurs ; notre public n'a pas de dépôt. On lit le site, une plaquette ou un document collé |

## Matrice 2 : `/fondation-clients`

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| ICP déduit des clients qui paient, premier contre dernier quart | AS | ✅ | `clients.py icp` sur un export CSV (CRM, facturation) : valeur, critères qui séparent, 5 au plus |
| Sous 10 clients, pas de motif : le dire | AS | ✅ | Sortie normée « hypothèse » au lieu d'une fausse analyse |
| ICP par paliers et anti-ICP | P | ⬆ | Sans les chiffres d'exemple inventés de P |
| Persona = rôle, job, déclencheurs, douleurs, résultats, objections, vocabulaire | C, P | ✅ | Chaque ligne porte sa source ; pas de prénom ni d'âge inventés (contre AR) |
| Seuil de 5 données par segment avant un persona | C | ✅ | `clients.py personas` compte les sources par persona et bloque sous le seuil |
| Sources de substitution quand il n'y a pas de clients | C | ✅ | Avis des concurrents (Google, Trustpilot, Avis Vérifiés, G2), forums FR, groupes LinkedIn, chacun étiqueté |
| Acheteurs B2B : utilisateur, prescripteur, décideur, financeur | C, P | ✅ | « Celui qui signe, pas celui qui clique » (repris de JM LinkedIn) |
| Jobs à accomplir (fonctionnel, émotionnel, social) | C, P | ✅ | Format « Quand…, je veux…, pour… » |
| 4 forces (pousser, attirer, habitude, anxiété) | C, R, B | ⬆ | Guide d'entretien « switch » réécrit en français (B n'est pas copiable) |
| Guide d'entretien client + 5 pourquoi + erreurs à éviter | C, P, B | ⬆ | Questions sur des faits passés, jamais « est-ce que vous paieriez… » ; consentement et RGPD pour l'enregistrement |
| Incitations (50 $ l'appel) | C | ✖ | Montants américains non transposables ; on dit seulement « prévois une contrepartie » |
| Questionnaire PMF de Sean Ellis (seuil de 40% « très déçu ») | C | ⬆ | Gardé en option, seuil cité comme repère de praticien **[à vérifier]** |
| Niveau de confiance par conclusion (3 sources, 2, 1) | C, T | ✅ | Même grille dans tout le pack |
| Biais d'échantillon (avis = utilisateurs passionnés, tickets = problèmes) | C | ✅ | Rappelé dans chaque synthèse |
| Persona en « journée type » et quotes inventées | P, AR | ✖ | Fiction : contredit la règle zéro invention |

## Matrice 3 : `/fondation-voix`

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Voix tirée de 15 à 30 vrais textes, sinon demander 3 exemples, ne jamais deviner | AS | ✅ | Sources possibles : emails, posts, pages du site, newsletters |
| Traits mesurables : appel, fin, longueur de phrase, place de la demande, exclamations | AS | ⬆ | `voix.py profil` les mesure, plus tutoiement / vouvoiement, « on » / « nous », émojis, anglicismes |
| Liste « n'écrit jamais » | AS | ✅ | Fusion avec la liste anti-IA de `/linkedin-human` et `/seo-human` (une seule liste) |
| « Nous sommes / nous ne sommes pas » (4 à 7 lignes, avec preuves) | T | ✅ | |
| Voix constante, ton réglable : formalité, énergie, technicité | T | ✅ | Canaux FR : site, email, LinkedIn, service client, devis ; tutoiement par canal |
| Niveau de confiance par section, questions ouvertes avec recommandation | T | ✅ | |
| Classement des sources (officielle, appliquée, conversationnelle, contexte, périmée) | T | ✅ | |
| Avant / après pour 4 ou 5 textes | AR, T | ✅ | Exemples Assurly |
| Règles d'écriture (ponctuation, chiffres, majuscules) | AR, R | ⬆ | Typographie française : espaces avant `: ; ! ?`, guillemets « », pourcentage collé, pas de tiret cadratin |
| Chaque correction de l'utilisateur est enregistrée, jamais à refaire | AS | ✅ | `voix.md` garde un journal « retiré le… parce que… » |
| Contrôle d'un texte contre la voix | T | ⬆ | `voix.py verifier TEXTE` : interdits, tutoiement incohérent, longueur hors profil |
| Connecteurs Confluence, Gong, Box | T | ✖ | Outils de grands comptes ; notre public colle ses textes ou les dépose dans le Projet |

## Matrice 4 : `/fondation-preuves`

| Capacité | Source | Verdict | Ce que nous ajoutons |
|---|---|---|---|
| Banque de mots clients : citation exacte + source + fréquence | P, C | ✅ | Jamais reformulée en langage marketing |
| Fouille des avis et forums (« Sales Safari ») | C | ⬆ | Plateformes FR : avis Google, Trustpilot, Avis Vérifiés, forums, groupes Facebook et LinkedIn |
| Bibliothèque d'objections : mots du client, étape, fréquence, réponse qui marche | P | ✅ | Réponses tirées de ce qui marche déjà ; tout ajout « de pratique générale » étiqueté |
| Vérification de chaque promesse marketing : étayée, mince, non étayée | P | ✅ | `preuves.py verifier` extrait chiffres, superlatifs (« n°1 », « le meilleur »), garanties, comparaisons, et cherche la preuve dans `preuves.md` |
| Signaler ce qui demande une relecture juridique | P | ⬆ | Repères FR : pratiques commerciales trompeuses, publicité comparative, allégations « vertes » **[à vérifier]** aux textes officiels avec leur date |
| Preuves étiquetées et datées, clients nommés seulement avec accord | JM LinkedIn | ✅ | |
| Win / loss : pourquoi on gagne, pourquoi on perd | P, C | ⬆ | Version légère : 5 questions après chaque affaire, rangées dans `preuves.md` |
| Rapports « volume analysé » en tête | P | ✅ | Chaque synthèse dit combien de sources et sur quelle période |
| Recommandation « Fable » et traitement par lots | P | ⬆ | Dit simplement : au-delà d'environ 100 éléments, traiter par lots et fusionner |

---

## Comparaison honnête avec ce que nous avons

**Growth Context v1 (à remplacer)** : un modèle à trous de 64 lignes, sans
entretien, sans distinction fait / déduction, sans source ni date, sans lien
avec les autres packs. Ses métadonnées sont fausses (`time_saved: "30 min /
usage"`, `tested_by: 31`). Il mélange entreprise, client, canaux, outils et
voix dans un seul bloc, et ses titres sont en anglais (« Pain », « Trigger »).
Aucune ligne n'est reprise telle quelle.

**Nos packs SEO, GEO et LinkedIn** : leur contexte est bon mais redondant.
`contexte.md` (LinkedIn) est la référence de qualité (étiquettes, preuves,
formulations retirées) ; la Fondation reprend ses conventions pour que tout
le site parle la même langue.

**Ce qu'aucune source ne fait et que nous ferons** :
- un contexte vérifiable (chaque fait sourcé et daté) plutôt que déclaratif ;
- un score honnête qui ne récompense pas un modèle vide ;
- l'export vers les autres packs, pour ne jamais reposer une question ;
- le terrain français : mentions légales, CNIL, droit de la publicité,
  plateformes d'avis françaises, typographie.

## Scripts prévus (Python 3.8+, sans dépendance, testés)

| Script | Commandes |
|---|---|
| `contexte.py` | `etat` (champs remplis, sourcés, périmés, par fichier) · `exporter --vers seo\|linkedin` |
| `clients.py` | `icp FICHIER.csv` (quartiles, critères qui séparent) · `personas clients.md` (seuil de sources) |
| `voix.py` | `profil` (mesures sur des textes collés) · `verifier TEXTE` (contre `voix.md`) |
| `preuves.py` | `verifier TEXTE` (promesses étayées, minces, non étayées) |

## Questions pour Aleksander

1. **Les 4 Skills** te conviennent-ils, ou en veux-tu moins (par exemple
   fusionner `preuves` dans `clients`) ?
2. **Les fiches annoncées « Bientôt » sur le site** : brand-context,
   persona-context, tone-of-voice, objectives-context et stack-outils sont
   couverts par ces 4 Skills. rgpd-context et legal-context deviennent une
   section de `entreprise.md`. ethical-marketing devient une partie de
   `preuves`. meeting et weekly-report ne sont pas de la fondation : je les
   retire du pack (ils pourront devenir un autre pack). D'accord ?
3. **L'export vers les packs SEO, GEO et LinkedIn** : je modifie aussi
   `seo-context` et `/linkedin-strategie` pour qu'ils lisent la Fondation
   d'abord ? (Petite modification, mais dans deux autres packs.)
4. **Une tâche réelle pour l'éval à l'aveugle** : as-tu une entreprise (la
   tienne, Join Médicis, ou un client anonymisé) sur laquelle comparer notre
   pack à `product-marketing` de Corey Haines ?
