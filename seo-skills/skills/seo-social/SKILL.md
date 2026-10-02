---
name: seo-social
description: >-
  SEO des plateformes sociales, souvent oublié : YouTube (titres, descriptions,
  chapitres, sous-titres), Pinterest (épingles, tableaux, mots-clés), TikTok et
  Instagram (recherche interne, légendes, texte à l'écran), LinkedIn (articles
  et pages entreprise) et Google Discover. Trouve ce que les gens cherchent
  sur chaque plateforme et optimise les contenus pour y être trouvé, et pour
  apparaître dans Google. Utilise-le pour « SEO YouTube », « Pinterest SEO »,
  « être trouvé sur TikTok », « optimiser mes vidéos ».
---

# seo-social

YouTube et Pinterest sont des moteurs de recherche. TikTok et Instagram aussi,
de plus en plus, pour une partie du public. Leurs résultats remontent dans
Google (vidéos, images, « Ce que disent les internautes »). Peu de marques
optimisent ces contenus : c'est de la visibilité facile à prendre.

## 1. Trouver ce qu'on cherche sur la plateforme

- La **barre de recherche** de chaque plateforme : ses suggestions
  automatiques sont les requêtes réelles (tape le sujet, puis « sujet a »,
  « sujet b »…).
- Les **contenus en tête** pour ces requêtes : format, durée, angle.
- Google : la requête affiche-t-elle des vidéos, des images, des
  discussions ? Si oui, la plateforme peut aussi ramener du trafic Google.

## 2. Par plateforme

| Plateforme | Ce qui est lu par le moteur | À faire |
|---|---|---|
| **YouTube** | titre, description, chapitres, sous-titres, texte prononcé, miniature (clic) | mot-clé au début du titre (≤ 60 car. visibles) ; 2 premières lignes de description qui répondent ; chapitres horodatés nommés avec les requêtes ; sous-titres français relus ; dire le mot-clé à l'oral dans les 30 premières secondes ; playlists par sujet |
| **Pinterest** | titre et description de l'épingle, texte de l'image, nom et description du tableau, lien | une épingle par intention, format vertical 2:3 ; mots-clés de la recherche Pinterest dans titre, description et tableau ; tableaux thématiques (pas « Divers ») ; lien vers la page exacte ; épingles régulières plutôt que par lots |
| **TikTok / Reels** | légende, texte à l'écran, voix, sous-titres, hashtags | mot-clé dit à voix haute et écrit à l'écran au début ; légende qui reprend la requête ; 3 à 5 hashtags précis plutôt que génériques |
| **LinkedIn** | titre et premières lignes des articles, page entreprise, nom des documents | articles LinkedIn sur les requêtes métier ; page entreprise complète (description avec mots-clés) ; voir le pack LinkedIn Skills pour les posts |
| **Google Discover** | grande image, titre, fraîcheur, E-E-A-T | image d'au moins 1 200 px de large (`max-image-preview:large`), titre précis sans piège à clic, contenu frais et expert |

## 3. Relier la plateforme et le site

- Chaque contenu social renvoie vers **la page du site** qui approfondit
  (pas l'accueil).
- Les vidéos YouTube intégrées dans l'article correspondant, avec le schema
  `VideoObject`.
- Les questions des commentaires deviennent des sections d'articles ou de
  FAQ (`/seo-refresh`).

## Sortie

```
SEO SOCIAL · sujet « assurance expatrié » · YouTube + Pinterest

YOUTUBE   requêtes : « assurance expatrié comment choisir », « CFE ou assurance privée »…
          vidéo 1 : titre « CFE ou assurance privée : comment choisir avant de partir »
                    chapitres : 0:00 La CFE en 1 minute · 1:40 Ce qu'elle ne couvre pas · …
                    description (2 premières lignes) : …
PINTEREST tableau « Partir vivre à l'étranger » · 5 épingles : « Checklist santé avant expatriation »…
LIENS     chaque contenu → /blog/cfe-ou-premier-euro/
```

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : pas de volume de recherche ni de statistique de plateforme
  sans source ; les règles d'algorithme sont des pratiques constatées, pas
  des garanties.
- Texte simple dans la conversation, sans créer de document.
- Rien n'est publié par le Skill.
