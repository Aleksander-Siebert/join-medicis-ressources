# Éligibilité : l'annonceur, le pays, les conversations

Avant d'écrire une seule annonce, vérifie que l'annonceur peut faire de la
publicité dans les pays visés. Source : règles publicitaires d'OpenAI (Ad
Policies), version 1.6 de septembre 2026, relues le 15 oct. 2026
(`commun/faits.md` § 3). Elles changent souvent : si la date a plus d'un
mois au moment du lancement, l'annonceur les relit.

Le Skill **signale** et **renvoie à la règle** ; il ne promet jamais
qu'une annonce sera acceptée. L'examen d'OpenAI porte sur le texte,
l'image **et la page de destination**.

## 1. La catégorie de l'annonceur

Déclare-la dans le JSON (`"annonceur": {"categorie": "…"}`) : le script en
tire un verdict, et cherche dans les annonces et les hints les mots qui
signalent une autre catégorie.

| Valeur | Ce que c'est | Statut au 15 oct. 2026 |
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
| États-Unis seulement, pays hors US | **arrête la préparation** et dis-le en une phrase, avec la règle et sa date ; propose ce qui reste possible (un autre produit de l'annonceur dans une catégorie autorisée, une campagne aux États-Unis si l'annonceur y exerce légalement, ou attendre une nouvelle version des règles) |
| États-Unis seulement, ciblage US | continue en signalant l'examen au cas par cas et le justificatif d'autorisation d'exercer |
| interdite | arrête ; aucune annonce, aucun fichier |
| doute (catégorie mixte) | écris la question précise pour l'annonceur, et continue seulement sur ce qui est clairement autorisé |

Ne cherche jamais à contourner une règle (euphémisme, page de destination
différente du produit réel, hint qui masque le sujet) : les règles exigent
une annonce cohérente de bout en bout et interdisent de tromper l'examen.

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
