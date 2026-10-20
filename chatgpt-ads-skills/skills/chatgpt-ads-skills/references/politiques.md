# Éligibilité : l'annonceur, le pays, les conversations

Avant d'écrire une seule annonce, dis à l'annonceur ce que les règles
permettent dans les pays visés. Source : règles publicitaires d'OpenAI (Ad
Policies), version 1.6 du 10 sept. 2026, relues en entier le 20 oct. 2026
(`commun/politiques-openai.md`, synthèse complète). Elles changent souvent :
si la date a plus d'un mois au moment du lancement, l'annonceur les relit.
Le droit français s'ajoute : `commun/droit-francais.md`.

Le Skill **alerte**, **renvoie à la règle**, puis **fait ce que demande
l'annonceur** (`commun/regles.md` § 1 bis) ; il ne promet jamais qu'une
annonce sera acceptée. L'examen d'OpenAI porte sur l'annonceur, le texte,
l'image **et la page de destination**.

## 1. La catégorie de l'annonceur

Déclare-la dans le JSON (`"annonceur": {"categorie": "…"}`) : le script en
tire un verdict, et cherche dans les annonces et les hints les mots qui
signalent une autre catégorie.

| Valeur | Ce que c'est | Statut (v1.6, relue le 20 oct. 2026) |
|---|---|---|
| `consommation`, `maison`, `style_de_vie` | biens ménagers et de consommation, mode, équipement | autorisée |
| `services_locaux` | artisans, réparation, services à domicile | autorisée |
| `voyage`, `divertissement` | voyages, expériences, loisirs, spectacles | autorisée |
| `numerique`, `logiciel`, `education` | applications, logiciels, formations | autorisée |
| `finance`, `assurance` | crédit, compte, paiement, investissement, assurance | **États-Unis seulement**, au cas par cas ; ailleurs généralement interdite |
| `sante` | dispositifs, dentaire, compléments, assurance santé, vision, diagnostics | **États-Unis seulement**, au cas par cas ; ailleurs généralement interdite |
| `juridique` | conseil ou représentation juridique | **États-Unis seulement**, avocat habilité ; ailleurs interdite |
| `alcool`, `tabac`, `jeux_argent`, `rencontres`, `adulte`, `substances`, `armes`, `contrefacon`, `politique` | | **interdite** |
| `bien_etre_allegations` | détox, minceur, compléments avec allégations santé, coaching santé | **interdite** |
| `dette` | redressement de crédit, règlement de dettes, investissements alternatifs | **interdite** |
| `offre_emploi`, `annonce_logement` | une offre d'emploi ou un logement précis | **interdite** (une plateforme d'offres reste possible si l'annonce ne cite aucune offre) |

Cas limites écrits dans les règles :

- Un **outil financier qui ne vend pas de produit financier** (application
  de budget, logiciel de comptabilité, formation) est en général admis :
  catégorie `logiciel` ou `education`.
- **Bien-être sans allégation médicale** (matériel de sport, nutrition
  générale, produits menstruels) : admis.
- **Lingerie, maillots** : admis dans un cadre de mode classique.
- **Hôtel avec casino** : admis si le jeu n'est pas l'objet de l'annonce.
- **CBD sans THC** (crèmes, huiles), vêtements en chanvre : admis sans usage
  intoxicant.
- **Mention incidente d'alcool** : admise si l'alcool n'est pas l'objet.
- **Films et jeux réservés aux adultes** : admis si l'annonce et la page ne
  sont ni explicites ni choquantes.

## 2. La conduite à tenir

| Verdict | Ce que tu fais |
|---|---|
| autorisée | continue ; rappelle que la page de destination est examinée aussi |
| États-Unis seulement, pays hors US (France comprise) | **alerte** en tête de réponse (modèle ci-dessous), propose les pistes conformes, **puis prépare la campagne demandée** ; l'alerte reste dans « à vérifier » |
| États-Unis seulement, ciblage US | continue en signalant l'examen au cas par cas et le justificatif d'autorisation d'exercer |
| interdite | **alerte forte** (refus quasi certain), pistes, puis prépare seulement si l'annonceur maintient sa demande après l'alerte |
| doute (catégorie mixte) | écris la question précise pour l'annonceur ; en attendant, prépare en signalant le doute |

### Modèle d'alerte (à adapter, 4 lignes au plus)

> **Attention, règles d'OpenAI (v1.6, 10 sept. 2026) :** l'assurance fait
> partie des services financiers, admis aux États-Unis seulement et
> « généralement interdits » ailleurs, dont la France. Risque : refus des
> annonces, voire de l'annonceur. Pistes ci-dessous ; je prépare la campagne
> demandée, à soumettre à l'examen d'OpenAI en connaissance de cause.

### Les pistes conformes, dans cet ordre

1. **Les offres non restreintes de l'annonceur** : un service, un outil,
   un contenu qui ne relève pas de la catégorie restreinte.
2. **Un contenu pédagogique sans vente** : guide, calculateur, check-list,
   avec une page qui ne vend pas le produit restreint (admis pour la finance
   et l'information juridique ; l'éligibilité de l'annonceur reste examinée).
3. **Des situations voisines dans les context hints** : viser « préparer un
   départ à l'étranger » plutôt que « comparer des assurances », avec une
   annonce qui dit clairement ce qu'elle propose. C'est une stratégie de
   ciblage, pas un maquillage.
4. **Demander un examen** à l'équipe commerciale d'OpenAI ou au
   gestionnaire de compte, par écrit.
5. **Un autre canal** si le refus est confirmé.

### La limite du pack

Le pack n'écrit pas d'annonce qui **cache le produit réel** : titre
« voyage » et page qui vend une assurance, euphémisme qui masque un crédit,
page différente pour l'examen. C'est trompeur pour l'utilisateur, contraire
à la cohérence de bout en bout exigée par OpenAI et à l'interdiction de
contourner les règles (§ 3 « Utilisation abusive »), et le motif de
suspension de compte le plus probable. Dis-le en une phrase et propose une
piste ci-dessus.

## 3. Les conversations exclues

Même pour une catégorie autorisée, les annonces ne s'affichent pas près des
conversations sensibles. Une intention qui en relève ne devient pas un ad
group :

- santé mentale et santé personnelle, dépendance émotionnelle, parcours
  sensibles ;
- sécurité des enfants, suicide ou automutilation, violence, contenus
  haineux, terrorisme, armes ;
- fraude, cybermalveillance, contournement des protections, contenus
  illicites, désinformation, atteinte à la propriété intellectuelle ;
- politique, sujets de société controversés, vie privée ;
- contenus sexuels, obscènes ou vulgaires ; biens réglementés (jeux
  d'argent, tabac).

## 4. Les règles de contenu qui touchent la rédaction

- **Véracité** : aucune affirmation non étayée sur les capacités, les prix,
  les résultats, les affiliations ou les comparaisons. C'est la liste des
  allégations du Skill.
- **Pas d'imitation de ChatGPT** : ni sa voix (« Réponse : … »), ni son
  apparence, ni une affiliation suggérée (« recommandé par ChatGPT »). Le
  script signale toute mention de ChatGPT, d'OpenAI ou de GPT.
- **Langage** : professionnel, sans obscénité, sans dénigrement ni
  exclusion de groupes.
- **Sujets sensibles** : pas d'appui sur une tragédie, une controverse de
  société ou un événement grave.
- **Cohérence** : la page de destination montre l'offre de l'annonce ; une
  annonce admise ne renvoie pas vers un contenu interdit.
