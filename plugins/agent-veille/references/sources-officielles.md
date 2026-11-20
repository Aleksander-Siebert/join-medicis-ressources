# Sources : ce que l'agent lit, et dans quelles conditions

Vérifié le 12 novembre 2026, par un appel réel à chaque source, sans clé.

## Les deux modes

**Standard (par défaut).** L'agent lit :

- les flux RSS et les pages publiques que tu lui donnes, en respectant le
  fichier `robots.txt` de chaque site ;
- les sources officielles ci-dessous ;
- le web, par l'outil de recherche de ton IA, pour les actualités.

Aucun agrégateur d'actualités n'est interrogé par le script.

**Étendu (à activer toi-même : `"mode": "etendu"`).** En plus, le script
interroge les flux RSS de Google Actualités et, si tu l'ajoutes à
`agregateurs`, de Bing Actualités. La collecte est plus complète et les
dates plus sûres, mais :

- ces flux sont prévus pour un lecteur de flux personnel, pas pour un usage
  commercial. Les conditions de Google Actualités en vigueur sont à relire
  par toi **[à vérifier]** ;
- le `robots.txt` de news.google.com interdit `/rss` aux robots (constaté le
  12 novembre 2026). Le mode étendu passe outre pour ces seuls flux : c'est
  la raison pour laquelle il n'est pas activé par défaut.

Choisis le mode étendu pour une veille personnelle. Pour une veille
d'entreprise diffusée à une équipe, reste en mode standard.

## Ce que l'agent ne fait dans aucun mode

- lire une page que son site interdit aux robots ;
- se faire passer pour un navigateur, résoudre un CAPTCHA, utiliser un
  navigateur furtif ou des adresses tournantes ;
- se connecter à un compte ;
- lire les réseaux sociaux, qui l'interdisent dans leurs conditions.

## Sources officielles gratuites

| Domaine | Source | Adresse | État |
|---|---|---|---|
| Appels d'offres, France | BOAMP, API ouverte de la DILA | `boamp-datadila.opendatasoft.com` | lu par le script |
| Appels d'offres, Europe | TED, API v3 | `api.ted.europa.eu` | lu par le script |
| Données personnelles | CNIL, flux RSS | `https://www.cnil.fr/fr/rss.xml` | à mettre dans `flux` |
| Consommation, concurrence | DGCCRF, flux RSS | `https://www.economie.gouv.fr/dgccrf/rss` | à mettre dans `flux` |
| Droit européen | EUR-Lex, flux RSS | `https://eur-lex.europa.eu/EN/display-feed.rss?rssId=162` | à mettre dans `flux` |
| Offres d'emploi | API publiques de Greenhouse, Lever, Ashby | page carrière du concurrent | lu par le script |
| Lois et décrets | Légifrance, Journal officiel | | **bloqué** (protection anti-robot). Voie officielle : API PISTE, compte gratuit **[à vérifier]** |
| Brevets et marques | INPI, Office européen des brevets | | **bloqué** sans clé. Prévu pour une version suivante |

Un marché attribué au BOAMP donne le nom du gagnant : c'est souvent la
meilleure source gratuite pour savoir quel concurrent a remporté quoi.

D'autres autorités publient un flux RSS (AMF, ACPR, Arcom, ANSSI, Autorité
de la concurrence…). Demande à l'agent « trouve le flux RSS de … » : il le
teste avant de l'ajouter.

## Limites connues

- Un serveur cloud est plus souvent bloqué qu'un ordinateur personnel. Une
  page en erreur dans une tâche cloud peut passer en local.
- Le même marché européen paraît au BOAMP et sur TED sous deux titres : le
  script ne les rapproche pas toujours, l'agent le fait à la lecture.
- TED cherche dans le titre de l'avis, le BOAMP dans son objet : un marché
  dont le titre ne contient pas tes mots-clés n'est pas vu.
