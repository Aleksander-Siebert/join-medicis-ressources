# Campagne ChatGPT Ads : Plantéa, France, clics

Voici la campagne complète, prête à reporter dans le fichier d'import (onglets `campaigns`, `adgroups`, `ads`). Une campagne, 5 groupes d'annonces (un par moment de la conversation), 2 annonces par groupe pour tester deux angles. Toutes les annonces respectent les limites du fichier : titre de 24 caractères au plus, texte de 48 au plus.

Trois champs obligatoires restent à compléter avant l'import : l'enchère (`max_bid`), les liens des images (`image_link`) et, pour les images, votre couleur de marque.

## Campagne

| Colonne | Valeur |
|---|---|
| campaign_name | Plantéa - FR - Clics - fin 2026 |
| budget_max | 30 |
| budget_type | Daily |
| launch_date | 2026-11-16 |
| end_date | 2026-12-20 |
| objective | Clicks |
| conversion_event_setting_ids | vide (non requis pour une campagne de clics) |
| target_countries | ["FR"] |

Liens : chaque annonce pointe vers la collection correspondante, avec `?utm_source=chatgpt&utm_medium=cpc&utm_campaign=plantea-fr-clics-fin2026&utm_content={groupe}_{a|b}`, pour lire les résultats par groupe et par variante dans votre outil d'analyse.

## Enchère : ma proposition

Je n'ai aucune donnée fiable sur le coût d'un clic dans ChatGPT Ads, et je ne veux pas vous donner un chiffre inventé. Je vous propose donc une règle de calcul plutôt qu'un montant :

**enchère max par clic = panier moyen × taux de marge brute × taux de conversion (visite vers achat)**

Exemple de calcul à faire avec vos chiffres : panier moyen {{à compléter}} € × marge {{à compléter}}% × conversion {{à compléter}}% = enchère plafond. Au-delà, chaque clic vous coûte plus qu'il ne rapporte en marge. Avec 30 € par jour, vous obtiendrez au plus 30 ÷ enchère clics par jour : si ce nombre est très faible, 5 groupes se partageront trop peu de clics pour comparer les variantes, et je réduirais à 3 groupes (plantes faciles, animaux, cadeau).

Même valeur pour les 5 groupes au départ. À vérifier dans Ads Manager : que `max_bid` est bien un plafond par clic pour l'objectif Clicks, et s'il propose une enchère suggérée [à vérifier].

## Groupe 1 : Plantes faciles - oubli d'arrosage

Lien : https://www.plantea.example/plantes-faciles/

Context Hints :
- quelle plante d'intérieur choisir quand on oublie d'arroser
- plantes d'intérieur faciles d'entretien pour débutant
- plante qui supporte le manque d'eau en appartement
- acheter une plante d'intérieur en ligne
- idées de plantes pour un appartement en ville

| | Titre (car.) | Texte (car.) |
|---|---|---|
| 1A | Vous oubliez d'arroser ? (24) | Plantes faciles livrées en pot, dès 19 €. (41) |
| 1B | Plantes faciles dès 19 € (24) | Livrées arrosées, avec leur fiche d'entretien. (46) |

1A part de la situation, 1B de l'offre et du prix.

## Groupe 2 : Plante qui dépérit

Lien : https://www.plantea.example/plantes-faciles/

Context Hints :
- ma plante d'intérieur perd ses feuilles
- plante d'intérieur qui jaunit ou qui sèche
- comment sauver une plante d'intérieur qui dépérit
- remplacer une plante morte par une plante plus facile

| | Titre (car.) | Texte (car.) |
|---|---|---|
| 2A | Votre plante dépérit ? (22) | Passez à une plante facile, livrée arrosée. (43) |
| 2B | Une plante plus facile (22) | Chaque plante arrive avec sa fiche d'entretien. (47) |

## Groupe 3 : Pièces sombres

Lien : https://www.plantea.example/peu-de-lumiere/

Context Hints :
- plante d'intérieur pour une pièce sans lumière
- plante pour salle de bains sans fenêtre
- plante pour couloir sombre ou bureau orienté nord
- quelles plantes pour un appartement peu lumineux

| | Titre (car.) | Texte (car.) |
|---|---|---|
| 3A | Appartement sombre ? (20) | Des plantes choisies pour les pièces sombres. (45) |
| 3B | Un bureau orienté nord ? (24) | Des plantes pour pièces sombres, livrées en pot. (48) |

## Groupe 4 : Chats et chiens - plantes non toxiques

Lien : https://www.plantea.example/animaux/

Context Hints :
- plantes d'intérieur non toxiques pour les chats
- plantes d'intérieur sans danger pour les chiens
- mon chat mâchouille mes plantes, lesquelles choisir
- quelles plantes d'intérieur éviter quand on a un animal

| | Titre (car.) | Texte (car.) |
|---|---|---|
| 4A | Vous avez un chat ? (19) | Plantes non toxiques pour chats et chiens. (42) |
| 4B | Un chien à la maison ? (22) | Non toxiques : vérifiées par notre botaniste. (45) |

Je n'ai volontairement mis aucun indice du type « mon chat a mangé une plante » : dans une urgence vétérinaire, une publicité pour des plantes serait déplacée.

## Groupe 5 : Offrir une plante

Lien : https://www.plantea.example/cadeau/

Context Hints :
- idée cadeau plante d'intérieur
- offrir une plante pour Noël
- cadeau de pendaison de crémaillère
- envoyer une plante en cadeau avec un message
- cadeau durable et sans plastique

| | Titre (car.) | Texte (car.) |
|---|---|---|
| 5A | Offrir une plante (17) | Message personnalisé, emballage sans plastique. (47) |
| 5B | Un cadeau qui pousse (20) | Frais de port offerts dès 49 € d'achat. (39) |

## Points à régler avant le lancement

1. **Cadeaux de dernière minute.** Votre livraison est de 3 à 5 jours ouvrés. Si les jours ouvrés vont du lundi au vendredi et que le décompte part du lendemain de la commande [à vérifier avec votre transporteur], une commande passée le jeudi 17 décembre arrive au plus tard le jeudi 24. À partir du vendredi 18, elle peut n'arriver que le lundi 28 (le 25 est férié). Aucune annonce ne promet de date, mais je vous conseille de mettre en pause le groupe « Offrir une plante » le 17 décembre au soir (le fichier d'import ne prévoit pas de date de fin par groupe, c'est donc à faire à la main dans Ads Manager).
2. **« Non toxiques ».** L'allégation figure sur votre page, je l'ai reprise telle quelle et toujours rattachée à votre botaniste. Comme aucun document n'est publié, un client dont l'animal serait malade n'aurait rien à quoi se référer. Je vous conseille de publier sur la page `/animaux/` la liste des espèces et la source utilisée par votre botaniste avant de dépenser sur ce groupe.
3. **Vos interdits sont respectés.** Aucune mention « n° 1 ». Les frais de port offerts apparaissent toujours avec leur condition (« dès 49 € d'achat »), et le mot « gratuit » n'est utilisé nulle part.
4. **Formats du fichier.** J'ai écrit les dates au format AAAA-MM-JJ, le pays en code ISO (« FR ») et le budget en euros : vérifiez que le modèle d'import attend bien ces formats et la devise de votre compte [à vérifier].

## Images (`image_link`, obligatoire)

Vos images ne sont pas prêtes : `image_link` vaut {{à compléter}} pour les 10 annonces. Une image par groupe suffit, les deux variantes la partagent puisque le test porte sur le texte. L'image s'affiche en vignette d'environ 100 px : une seule forme simple, pas de texte, pas de logo (il s'affiche déjà dans le coin de l'annonce). Vérifiez dans Ads Manager le format et la taille exigés [à vérifier] ; les prompts ci-dessous demandent un carré de 1 024 px.

Couleurs : je n'ai pas vos codes. Par défaut, fond `#0F0F0F` et couleur d'accent {{à compléter : couleur de marque en hexadécimal}} ; à défaut, un vert saturé, à valider.

Prompt de base, à coller dans Gemini ou Imagen en remplaçant les deux lignes « Forme » :

```
Crée une icône carrée de 1024 x 1024 px. Composition géométrique pure, sans texte, sans personne, sans élément photographique.
Fond : uni #0F0F0F.
Forme principale : [FORME PRINCIPALE], en blanc (#FFFFFF), occupant environ 70% de l'image, centrée.
Forme d'accent : [FORME D'ACCENT], en [COULEUR D'ACCENT], point focal à l'intérieur ou à la base de la forme principale.
Style : minimaliste, fort contraste, formes pleines, lisible en vignette de 80 à 100 px. Pas de dégradé, pas d'ombre, pas de halo, pas de détail fin, pas de contour.
```

| Groupe | Forme principale | Forme d'accent |
|---|---|---|
| 1. Plantes faciles | une grande feuille pleine en amande, pointe vers le haut | une goutte d'eau pleine à la base de la feuille |
| 2. Plante qui dépérit | un pot trapézoïdal plein | une feuille pleine qui sort du pot, bien droite |
| 3. Pièces sombres | une grande feuille pleine en amande | un demi-disque en haut à droite, comme une lumière faible |
| 4. Chats et chiens | un bouclier plein | une petite feuille pleine au centre du bouclier |
| 5. Offrir une plante | une boîte cadeau carrée pleine | un ruban en croix sur la boîte |

Si vous préférez des photos de vos plantes, gardez la même règle : une plante seule, sur fond uni, cadrée serré.

Je peux ensuite générer ces 5 icônes directement, ou proposer d'autres titres pour un groupe précis.
