# Annonces : titre, copie, angles et visuel

Une annonce ChatGPT se lit en passant, sous une réponse qui a déjà donné de
l'information. Elle gagne sa place si elle apporte **ce que la réponse ne
peut pas donner** : l'offre précise, une preuve, un service, une prochaine
étape.

## 1. Les limites

| Champ | Maximum (modèle d'import, 15 oct. 2026) | Cible | Statut de la cible |
|---|---|---|---|
| `title` | 24 caractères | 16 à 24 | praticien, à confirmer |
| `copy` | 48 caractères | 32 à 48 | praticien, à confirmer |

- Le maximum est lu dans le modèle (`valider_exporter.py modele`) : si
  OpenAI change le modèle, le contrôle suit.
- L'API accepte 3 à 50 caractères de titre et 100 de texte, mais le
  fichier d'import en fixe 24 et 48 : on écrit pour le fichier. Les
  35 et 67 caractères de certains guides relèvent du folklore
  (`commun/faits.md` § 5).
- Tout compte : espaces, ponctuation, **et l'espace avant `: ? ! ;`** de la
  typographie française. « Neuf ou reconditionné ? » fait 23 caractères.
- Ne compte jamais de tête : le script compte en forme NFC (« é » vaut 1).

## 2. Titre et copie se complètent

| À éviter | Pourquoi | Mieux |
|---|---|---|
| Vélo électrique reconditionné / Achetez un vélo électrique reconditionné. | la copie répète le titre | Neuf ou reconditionné ? / Comparez état, garantie et prix avant d'acheter. |
| Vélora, vélos électriques / Vélora, le spécialiste du VAE. | centré sur la marque, aucun bénéfice | Au bureau sans sueur / Un VAE reconditionné pour vos trajets du matin. |

*Exemples fictifs.* Le titre accroche la situation ou le bénéfice ; la copie
apporte la preuve, la précision ou l'étape suivante. Le script signale un
recouvrement de plus de la moitié des termes, et un titre qui commence par
la marque : le nom et le logo de l'annonceur s'affichent déjà au-dessus du
titre (Help Center, relu le 15 oct. 2026).

## 3. Les angles

Un angle par annonce ; 4 angles au moins par groupe pour que les annonces
ne soient pas des reformulations les unes des autres.

| Angle | Ce que l'annonce fait | Exemple fictif |
|---|---|---|
| situation | nomme le moment vécu | Les enfants à l'école / Des vélos cargo électriques révisés en atelier. |
| bénéfice | dit le résultat pour la personne | Livré prêt à rouler / Votre VAE arrive monté et réglé en atelier. |
| objection | répond à la crainte de l'intention | Et la batterie ? / Chaque batterie est testée avant la vente. |
| preuve | ancre une allégation approuvée | Un VAE révisé, garanti / 12 mois de garantie, batterie testée. |
| comparaison | aide à choisir, sans dénigrer | Quel cargo choisir ? / Biporteur ou longtail : comparez nos modèles. |
| contraste | « pas X : Y », la différence en une phrase | VAE d'occasion, contrôlé / Pas une annonce entre particuliers : un atelier. |
| processus | dit ce qui se passe après le clic | Le vélo vient à vous / Commandez en ligne, recevez un vélo prêt. |
| conseil | promet une aide, la page la donne | Bien choisir son VAE / Nos conseils pour choisir sans se tromper. |
| question | reprend la question de la conversation | Neuf ou reconditionné ? / Comparez état, garantie et prix avant d'acheter. |

Le patron « contraste » et la preuve ancrée viennent de `chatgpt-ads-builder`
(fseixas, MIT), réécrits avec une contrainte en plus : **une preuve n'est
écrite que si elle est approuvée**.

## 4. Tactiques de longueur, en français

1. Coupe l'article et le verbe d'état : « Un vélo révisé, garanti » plutôt
   que « Un vélo qui est révisé et garanti ».
2. Chiffres en chiffres : « 12 mois » (7) contre « douze mois » (10).
3. Une abréviation seulement si la cible l'emploie (VAE pour un acheteur de
   vélo électrique, oui ; jargon interne, non).
4. Le deux-points remplace une proposition : « Batterie : testée en
   atelier ». Il coûte 2 caractères avec son espace.
5. Retire la marque du titre : elle s'affiche déjà.
6. Dernier recours : changer d'angle plutôt que comprimer jusqu'à
   l'illisible.

## 5. Les interdits

- Une allégation absente de la liste approuvée : chiffre, prix, délai,
  garantie, « gratuit », « offert », « sans engagement », superlatif,
  « n° 1 », « leader », « le moins cher » (le script bloque ou signale).
- Fausse urgence (« Dernière chance », « Plus que 2 jours ») sans offre
  datée réelle.
- Capitales criées, emoji, points d'exclamation en série, tiret cadratin.
- Une promesse que la page de destination ne tient pas.
- Le dénigrement d'un concurrent nommé.
- Toute imitation de ChatGPT : mention de ChatGPT, d'OpenAI ou de GPT, ton
  de réponse (« Réponse : … »), affiliation suggérée (règles publicitaires,
  `references/politiques.md` § 4 ; le script la signale).
- Dans un secteur sensible : toute formulation qui promet un résultat de
  santé, financier ou juridique (`references/politiques.md`).

## 6. Volume et répartition

- **40 à 50 annonces** par défaut quand le budget le permet, réparties à
  peu près également : 8 par groupe pour 5 groupes. Avec un petit budget
  (moins de clics par jour que la moitié du nombre d'annonces), 2 ou 3
  annonces par groupe suffisent pour commencer ; on en ajoute quand les
  premières ont des résultats. Le script signale un groupe qui a plus du double
  d'un autre, et un groupe de moins de 3 annonces.
- **Mode « grande échelle »** (`"mode": "grande-echelle"`) : 100 annonces,
  pour un annonceur qui a le budget de les départager. Le seuil entre les
  deux est un point à confirmer (`commun/faits.md` § 3).
- Pas de doublon exact (bloqué), pas de reformulation minime (signalée
  au-delà de 70% de termes communs) : chaque annonce teste quelque chose.

## 7. Le visuel

Le modèle d'import demande une image carrée, 640 × 640 au moins,
1 200 × 1 200 au plus, PNG ou JPG ; l'API accepte aussi le WebP
(`commun/faits.md` § 1). L'image s'affiche petite, à côté du titre.

- Une **idée de visuel** par ad group, dans `idee_visuel` : un sujet unique
  et reconnaissable, lié à la situation du groupe, sans texte incrusté,
  sans visage identifiable si l'annonceur n'a pas les droits, sans logo
  (déjà affiché).
- Le lien de l'image (`image_link`) vient de l'annonceur : sans lien, la
  cellule reste vide et le script bloque l'export.
- Le script vérifie l'URL et l'extension ; la taille et le format carré se
  vérifient à l'ouverture du fichier, dans la checklist de relecture.

## 8. Liens et suivi

- `link` : la page de destination de l'intention, pas la page d'accueil
  (signalée en information). 2 048 caractères au plus, accessible aux
  robots d'OpenAI : pas de page protégée par un mot de passe ou un
  pare-feu anti-robots. Une page qui ne peut pas être vérifiée ne peut pas
  être diffusée (règles publicitaires).
- Paramètres UTM autorisés : ils restent sur le lien au clic (Help Center).
  Ads Manager peut aussi ajouter des paramètres au niveau du compte, de la
  campagne ou de l'annonce, avec des variables comme `{campaign_id}` et
  `{ad_id}` (documentation développeur) ; le niveau le plus fin l'emporte.
  Convention proposée pour le fichier :
  `utm_source=chatgpt&utm_medium=ads&utm_campaign=<campaign_name>&utm_content=<adgroup_name>`,
  à aligner sur celle de l'annonceur s'il en a une.
- Domaine du lien : celui déclaré dans `annonceur.domaines` (le script
  signale un autre domaine).
