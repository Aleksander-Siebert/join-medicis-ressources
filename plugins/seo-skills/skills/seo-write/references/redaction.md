# Les règles de rédaction, avec exemples

Règles tirées du workflow de rédaction de l'utilisateur (persona de
rédacteur senior en secteur YMYL, éprouvé sur un vrai site), complétées par
la liste Wikipédia « Signs of AI writing » et le guide Google « Créer des
contenus utiles ». Les exemples utilisent Assurly, entreprise fictive.

## 1. Zéro invention (YMYL)

| Avant | Après |
|---|---|
| Une mutuelle coûte entre 30 et 150 € par mois. | Le prix dépend de votre âge, de votre lieu de résidence, des personnes couvertes et des garanties : demandez un devis. |
| Le délai de carence est de 3 mois chez la plupart des assureurs. | Certaines formules ont un délai de carence : vérifiez-le dans les conditions générales avant de signer. |
| Le plafond Madelin est de 3 400 € environ. | Le plafond Madelin change chaque année : {{à compléter : plafond 2026, source impots.gouv.fr}}. |
| Selon une étude récente, 73% des indépendants… | (retirer, ou citer l'organisme, la date et le lien) |

Une source privée (blog d'assureur, comparateur) ne prouve pas une règle
légale : on cherche la source officielle (`sources.md`), ou on laisse le
lien en trou.

## 2. Entrer dans le sujet

| Avant | Après |
|---|---|
| Dans un monde en constante évolution, la protection santé des indépendants est un véritable pilier. | Vous quittez un CDI pour vous installer à votre compte : la mutuelle de votre ancien employeur s'arrête. |
| Dans cet article, nous allons voir comment choisir sa mutuelle. | (supprimer : le titre le dit déjà) |

## 3. Le résumé de 3 lignes

Une citation `>` juste après l'introduction. Trois phrases au plus, une idée
chacune : de quoi parle l'article, ce que le lecteur en retire, ce qu'il
trouvera de particulier. Pas de puces, pas de jargon.

```
> Une mutuelle n'est pas obligatoire pour un indépendant, mais l'Assurance maladie ne rembourse pas tout.
> Ce guide montre ce qu'elle couvre, ce qui fait varier son prix et comment déduire vos cotisations.
> Il se termine sur l'erreur que nous voyons le plus souvent en rendez-vous.
```

(Ce résumé remplace l'ancien encadré « L'essentiel en 5 points », à la
demande de l'utilisateur.)

## 4. Réponse directe en tête de section

| Avant | Après |
|---|---|
| ## Combien ça coûte ? Est-ce cher ? Tout dépend. | ## Combien coûte une mutuelle indépendant · Le prix dépend de quatre choses : votre âge, votre lieu de résidence, les personnes couvertes et le niveau de garanties. |

La première phrase répond ; le détail suit. Une question en ouverture de
section n'est pas une réponse.

## 5. Voix active, style affirmatif

| Avant | Après |
|---|---|
| Votre attestation sera envoyée sous 48 h. | Vous recevez votre attestation sous 48 h ouvrées. |
| Votre dossier est étudié par nos conseillers. | Nos conseillers étudient votre dossier. |
| Une mutuelle pourrait être utile pour les soins dentaires. | Une mutuelle rembourse une partie des soins dentaires, selon votre niveau de garanties. |
| Il semblerait que les indépendants sous-estiment ce poste. | (affirmer avec la preuve, ou retirer) |

Affirmatif ne veut pas dire promettre : « remboursé à 100% », « sans aucun
risque », « le moins cher du marché » restent interdits sans la preuve
contractuelle.

## 6. Ce qui sonne IA (à réécrire)

- **Lexique** : crucial, essentiel (en tic), tissu, souligner, témoignage (au
  sens figuré), paysage en évolution, vibrant, révolutionnaire,
  incontournable, naviguer (au figuré), véritable pilier, clés du succès.
- **Participes déductifs en fin de phrase** : « …, renforçant ainsi sa
  sécurité financière », « …, illustrant une dynamique globale ». Une phrase
  pour le fait, une autre pour la conséquence si elle est prouvée.
- **Triade automatique** : « rapide, simple et efficace ». Garder ce qui est
  vrai, souvent un seul mot.
- **Parallélisme moralisateur** : « non seulement X, mais aussi Y ».
- **Verbes d'état gonflés** : « se positionne comme », « sert de », « offre une
  approche », « joue un rôle crucial ». Écrire « est ».
- **Transitions toutes faites** : « il convient de noter », « il est
  important de souligner », « dans ce contexte », « force est de constater »,
  « en définitive ».
- **Sections de clôture** : « Conclusion », « En conclusion », « Défis »,
  « Perspectives d'avenir ».
- **Tiret cadratin** en incise : une virgule, ou une autre phrase.

`controle.py` repère la structure, les verbes d'état, les participes, les
transitions et les liens annoncés ; `/seo-human` repère le lexique, les
triades et le rythme.

## 7. Gras, listes, tableaux

- Gras : une notion (« **délai de carence** »), jamais une phrase.
- Liste numérotée : des étapes dans l'ordre. Liste à puces : des éléments
  sans ordre. Tableau : une comparaison sur les mêmes critères.

## 8. Liens internes

| Avant | Après |
|---|---|
| Comme expliqué dans notre article sur la prévoyance, l'arrêt de travail n'est pas couvert. | La mutuelle ne verse rien en cas d'arrêt de travail : c'est le rôle de la [prévoyance indépendant](/prevoyance-independant/). |
| Pour en savoir plus, [cliquez ici](/devis/). | Pour un prix exact, faites une [demande de devis](/devis/). |

## 9. La fin

Pas de conclusion qui résume : une dernière réponse utile ou une action
concrète (« demandez le tableau des garanties avec votre devis »).

## 10. Les règles d'entité et le contexte international

Ce que `site-context.md` impose s'applique partout, titres compris : la
formule pour nommer l'entreprise (« à Assurly »), les références à ne pas
prendre comme norme (un système national quand le public est international),
les mots interdits.
