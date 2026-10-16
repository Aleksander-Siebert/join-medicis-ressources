# Images et type de page

## 1. Les images

- **alt** : descriptif sur les images porteuses de sens, vide (`alt=""`) sur
  les décoratives ; l'attribut absent est l'erreur.
- **width et height** sur chaque image : sans eux, la page bouge pendant le
  chargement (CLS).
- **Image principale** (souvent l'élément LCP) : jamais `loading="lazy"`,
  idéalement `fetchpriority="high"`. Les autres images : `loading="lazy"`.
- **Format et poids** : WebP ou AVIF, à la taille affichée, moins de 200 Ko
  pour une image de contenu.
- **Images générées par IA** : Google Merchant Center exige la métadonnée
  IPTC `DigitalSourceType` = `TrainedAlgorithmicMedia` sur les images de
  produit créées par IA, et interdit de la retirer
  (https://support.google.com/merchants/answer/14743464). Pour les vérifier :
  `exiftool -XMP-iptcExt:DigitalSourceType image.webp`.
- Nom de fichier parlant (`assurance-expatrie-dubai.webp`, pas `IMG_0042.jpg`).

## 2. Le bon type de page

Une page bien optimisée ne se classe pas si elle n'est pas du type que Google
affiche pour la requête. On compare le type de la page au type dominant des
10 premiers résultats (`/seo-serp`) :

| La page est | La SERP montre | Gravité | Que faire |
|---|---|---|---|
| un article | des pages produit ou d'offre | critique | créer une page produit ; l'article la soutient |
| un article | des comparatifs | haute | restructurer en comparatif avec tableau |
| une page produit | des guides | haute | ajouter un vrai contenu explicatif, ou un guide séparé |
| une landing page | des outils, simulateurs | haute | proposer l'outil (calculateur, simulateur) |
| une page service | le pack local (carte) | moyenne | signaux locaux, fiche Google (`/seo-local`) |
| même type | | aligné | travailler la profondeur et la clarté |

Si la SERP mélange les types, c'est une ouverture : le format le plus utile
pour le lecteur peut gagner. Adapté de seo-sxo (claude-seo, MIT ; auteur
d'origine Florian Schmitz).

