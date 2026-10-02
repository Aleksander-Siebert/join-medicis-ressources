---
name: linkedin-entreprise
description: >-
  Pour la présence LinkedIn d'une entreprise, côté marketing : note la page
  entreprise sur 100 (12 critères sourcés, « n/a » quand une donnée manque,
  script), réécrit slogan, présentation, bouton et post épinglé, coordonne la
  page et les dirigeants (deux voix, jamais le même jour), et lance un
  programme d'ambassadeurs salariés (14 jours, rythme par rôle, ce que le
  marketing relit et ne relit pas, niveaux de relecture A, B, C, ROI sur
  3 niveaux, script). Utilise-le pour « audite notre page entreprise »,
  « notre page ne sert à rien », « faire publier l'équipe », « programme
  d'ambassadeurs », « employee advocacy », « charte de prise de parole des
  salariés », « coordonner la page et le CEO ». Pas pour le profil d'une
  personne (utiliser /linkedin-profile), ni pour écrire un post précis
  (/linkedin-post), ni pour la publicité payante. Ne publie rien.
---

# linkedin-entreprise

Deux chantiers, souvent confiés au même marketeur : **la page** (la vitrine
de l'entreprise) et **les personnes** (dirigeants et salariés qui parlent en
leur nom). La page informe et rassure ; les personnes portent la conversation.
Ce Skill fait travailler les deux ensemble sans les mélanger.

**À lire avant de commencer :** `commun/regles.md` et `commun/preuves.md`
(formats officiels des pages, annonces de LinkedIn de 2026).

## 1. Lire le contexte

`contexte.md`, partie « Entreprise » : offres, sujet → offre → phrase d'appel
à l'action, preuves étiquetées **LIVE / À CONFIRMER / RETIRÉ**, deux voix,
formulations retirées, convention UTM, qui valide quoi. S'il est vide, propose
`/linkedin-strategie` (partie entreprise) avant d'auditer : sans offres ni
preuves de référence, l'audit ne peut pas juger la cohérence.

## 2. Auditer la page (script)

Demande ce que tu ne peux pas voir toi-même : la page collée ou en capture,
l'export des statistiques de la page (rubrique statistiques de l'admin,
« Exporter »), et la liste des salariés reliés à la page si elle est connue.
Rien n'est lu sur LinkedIn par un robot.

Remplis le JSON décrit en tête de `scripts/audit_page.py` (laisse absent ce qui
n'a pas été fourni), puis :

```
python3 scripts/audit_page.py --fichier page.json
```

12 critères de `grille-page.json`, chacun avec sa source. Une source absente
donne **n/a**, pas zéro, et la note est donnée **sur les points notables**
(« 41/66 notables »). Les corrections sortent classées par points gagnés par
heure. Sans exécution de code : même grille, à la main.

Comparer l'engagement de la page à **son propre historique**, jamais à un
« benchmark » : les définitions du taux d'engagement varient du simple au
quintuple selon les outils.

## 3. Réécrire la page

Dans l'ordre des points par heure, chaque texte passe par `/linkedin-human`.
Règles et exemples : `references/page.md`.

| Élément | Règle | Limite |
|---|---|---|
| Slogan | pour qui, ce qui change, une preuve | 120 caractères [à vérifier dans l'éditeur] |
| Présentation | commence par le problème du lecteur, pas par « X est une société fondée en… » ; offres actuelles ; un chiffre ; une porte d'entrée | 2 000 caractères [à vérifier dans l'éditeur] |
| Logo, couverture | logo net ; couverture avec une phrase et un moyen de contact | logo 400 × 400 recommandés ; couverture 1 512 × 256 ; 3 Mo [officiel] |
| Bouton | vers la page la plus utile (pas forcément l'accueil), avec UTM | |
| Post épinglé | récent, ne promeut rien de RETIRÉ | |
| Pages vitrines | seulement pour une offre ou une audience vraiment distincte | |

La couverture se fabrique avec `/linkedin-carrousel` (adapter le format au
1 512 × 256 de la page).

## 4. Deux voix, un calendrier

| Voix | Qui | Personne | Rôle |
|---|---|---|---|
| Dirigeant ou expert | la personne | « je » | opinions, histoires, positions |
| Page | l'entreprise | « nous » | conseils pratiques, équipe, événements, cas clients autorisés |

- Les deux voix ne se mélangent jamais dans un texte.
- **Jamais le même jour, jamais le même sujet** : la page et le dirigeant ne
  se font pas concurrence dans le fil des mêmes abonnés [praticien,
  JoshuaDIWork].
- **La page repartage le meilleur post de la semaine du dirigeant**, deux jours
  après, avec une ligne qui ajoute quelque chose (pas un repartage nu).
- Les posts personnels touchent en général plus de monde que ceux d'une page
  [étude tierce et praticien, sans chiffre retenu : les multiplicateurs
  publiés viennent de vendeurs]. La page n'est pas pour autant inutile :
  c'est elle qu'on consulte avant d'acheter ou de postuler.
- UTM sur chaque lien vers le site : `utm_source=linkedin`,
  `utm_medium=social` (organique) ou `paid` (publicité),
  `utm_campaign={{campagne}}`, pour que l'analytics fasse la somme.

## 5. Programme d'ambassadeurs salariés

Détail complet : `references/ambassadeurs.md`.

**Quatre principes** (Serge Bulaev, MIT) : chacun écrit **dans sa voix** ; la
relecture porte sur les **risques**, jamais sur le style ; **5 minutes** de
friction au plus par post ; le ROI se **prouve** sur trois niveaux.

**Lancement en 14 jours** :

| Jours | Ce qui se passe |
|---|---|
| 1 à 3 | entretien de 5 à 10 minutes par personne (sa voix, son expertise, 2-3 piliers ; `/linkedin-interview` en version courte), rythme individuel |
| 4 à 7 | premier post de chacun, dans sa voix ; relecture des faits seulement ; on célèbre chaque premier post en interne |
| 8 à 10 | réserve d'idées partagée (victoires internes, questions clients, actualité du métier) ; chacun choisit, rien n'est imposé |
| 11 à 14 | jours fixes par personne, tableau de bord, première revue hebdomadaire |

**Rythme par rôle et montée en charge** (script) :

```
python3 scripts/ambassadeurs.py plan --fichier equipe.json --semaine 3
```

Semaines 1-2 : commenter seulement ; 3-4 : un premier post ; 5-8 : la moitié
de la cible ; 9 et après : la cible. Plancher : 1 post et 5 commentaires par
semaine, sinon la personne est hors programme (ou en binôme). Plafond : pas
de salarié à 5 posts par semaine.

**Relecture : les faits, jamais la voix** (script) :

```
python3 scripts/ambassadeurs.py relecture --texte "{{brouillon}}" --clients "{{liste}}" --concurrents "{{liste}}"
```

| Niveau | Quand | Délai |
|---|---|---|
| **A** | opinion, histoire, leçon personnelle, commentaire, repartage avec avis | aucune relecture |
| **B** | client nommé, chiffre interne, concurrent, annonce | relecture des faits par le marketing, objectif **4 h ouvrées**, accord tacite à 24 h |
| **C** | sujet réglementé, prévision financière, litige, données personnelles | accord explicite sous 48 h (juridique ou direction) |

Le relecteur ne touche **jamais** à la voix, au ton, à l'accroche, aux
opinions ni au rythme de publication.

**ROI sur trois niveaux** : personne (impressions, commentaires, vues du
profil), équipe (portée totale, taux de participation), business
(conversations entrantes, rendez-vous, affaires dont LinkedIn est le premier
contact, candidatures). Les abonnés et le nombre de posts ne sont pas des
résultats. `/linkedin-audit` lit les exports de chaque personne.

**Anti-modèles** : le même texte copié sur plusieurs comptes ; l'écriture
fantôme qui efface la voix ; un rythme imposé à tous ; une relecture de plus
de 24 h ; mesurer seulement la vanité ; tout le monde sur les mêmes piliers ;
des « pods » internes où l'équipe like et commente sur commande (engagement
artificiel visé par LinkedIn, annonce du 12 mars 2026).

## 6. Alignement de l'équipe

Les profils des salariés sont la première chose qu'un prospect ou un candidat
regarde après la page. Vérifier que chacun indique l'entreprise comme employeur
actuel **reliée à la page**, et proposer (jamais imposer) des formulations
maison pour le titre. Chaque profil reste celui de la personne
(`/linkedin-profile`).

## Sortie (format fixe)

```
ENTREPRISE · {{nom}} · {{date}}

PAGE  {{note}}/{{notables}} notables ({{%}}) · {{verdict}}
Corrections, par points par heure :
1. {{…}} : bloc prêt à copier
…
Non noté : {{critères n/a et source à fournir}}

COORDINATION : calendrier page / dirigeant de la semaine, repartage prévu, UTM
AMBASSADEURS (si demandé) : plan des 14 jours, rythme par personne, niveaux de relecture, tableau de bord ROI
À VÉRIFIER : {{faits À CONFIRMER, accords clients}}
Suite proposée : {{/linkedin-plan pour le calendrier, /linkedin-audit pour les chiffres}}
```

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| Pas d'accès aux statistiques | critères rythme, qualité, engagement en n/a ; le dire, ne pas estimer |
| Pas d'accès admin à la page | proposer les changements, l'admin les applique |
| Salarié qui ne veut pas publier | il ne publie pas ; le programme est volontaire |
| Demande d'imposer des posts identiques à toute l'équipe | refuser (anti-modèle, et LinkedIn réduit le contenu répétitif) ; proposer un sujet commun que chacun écrit dans sa voix |
| Demande d'un groupe interne qui like tout sur commande | garde-fou : refus (engagement artificiel) ; proposer de commenter quand on a quelque chose à ajouter |
| Crise, incident, litige | suspendre le niveau A pour l'équipe concernée 5 à 7 jours ; seule la voix désignée parle |
| Secteur réglementé | tout ce qui touche au produit ou au conseil passe en niveau C |
| Petite entreprise (moins de 10 salariés) | le dirigeant porte l'essentiel ; la page reste à jour et repartage |

## Ressources

- `grille-page.json` : 12 critères, sources, effort.
- `scripts/audit_page.py` : note, n/a, corrections par points par heure.
- `scripts/ambassadeurs.py` : plan de l'équipe, niveau de relecture.
- `references/page.md` : réécrire la page, avant/après, deux voix, UTM.
- `references/ambassadeurs.md` : lancement, gouvernance, rythmes, ROI,
  anti-modèles, charte à faire signer.
- `references/exemple.md` : audit et plan pour Assurly.

## Skills liés

- `/linkedin-strategie` : la partie « Entreprise » de `contexte.md`.
- `/linkedin-profile` : le profil du dirigeant et des salariés.
- `/linkedin-post`, `/linkedin-human` : les textes de la page et des
  ambassadeurs.
- `/linkedin-plan` : le calendrier page et dirigeant.
- `/linkedin-audit` : la page et les profils, audités séparément.
