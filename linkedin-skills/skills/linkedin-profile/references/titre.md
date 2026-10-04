# Le titre : 220 caractères qui te suivent partout

Le titre est la seule phrase de LinkedIn qui voyage. Il accompagne chaque
commentaire que tu laisses sous le post d'un autre, chaque résultat de
recherche où tu apparais, chaque invitation que tu envoies. Quelqu'un peut le
lire quarante fois avant d'ouvrir ton profil.

La plupart des titres sont un intitulé de poste. C'est la seule chose qu'un
lecteur aurait pu deviner.

## Les limites

| Limite | Valeur | Niveau de preuve |
|---|---|---|
| Longueur maximale | 220 caractères | consensus de sources tierces, à vérifier dans le compteur de l'éditeur |
| Visible dans la recherche et les invitations | ~60 caractères (certaines sources disent 45) | observation, varie selon l'écran |
| Visible à côté d'un commentaire | moins encore, coupé au milieu d'un mot | observation |

Conséquence : le titre se **charge par l'avant**. Les 60 premiers caractères
font l'essentiel du travail, le reste est un bonus que certains verront.
« Directrice marketing | Ex-L'Oréal | Conférencière | Maman de 3 » échoue : le
segment le plus fort est en deuxième position et le plus faible là où l'œil
tombe.

## Les cinq choses qu'un titre doit faire

`scripts/titre.py` note chacune sur 20.

1. **Nommer l'audience.** « pour les assureurs en ligne », « pour les PME
   industrielles ». Un titre qui pourrait appartenir à n'importe qui ne
   s'adresse à personne.
2. **Nommer le résultat.** Ce qui change grâce à toi. « Réduire le coût par
   lead » est un résultat. « Passionnée par l'expérience client » est une
   humeur.
3. **Porter une preuve.** Un chiffre, une ancienne entreprise (« ex-Publicis »),
   un titre reconnu, un volume (« 14 clients »). Une suffit, et elle doit être
   vraie.
4. **Rester trouvable.** La recherche LinkedIn lit le titre. Un intitulé
   inventé (« Chief Happiness Growth Officer ») ne remonte pour rien. Garde au
   moins un terme de métier que les gens tapent.
5. **Rester lisible.** Trois segments au plus, un émoji au plus, aucun mot
   creux.

## Structures qui marchent

Propose toujours **trois options de structures différentes**, puis compare-les
avec `titre.py`.

**A. Métier pour audience | preuve | ce qui t'est propre**

```
Consultante SEO pour les PME industrielles | +180% de trafic organique pour
14 clients en 2025 | Je parle technique et commerce
```

**B. Ce que tu fais pour eux, sans le coût qu'ils redoutent**

```
Responsable acquisition chez Assurly | Je fais baisser le coût par lead des
assureurs en ligne sans augmenter le budget | −44% en 4 mois
```

**C. Poste actuel · destination · preuve du passage** (reconversion,
évolution)

```
Chargée de communication → Product marketing B2B | 3 lancements de produit
pilotés en 2025 | Je traduis la technique en arguments de vente
```

Cette troisième structure compte pour les reconversions : **dis la
destination, pas seulement l'origine**. Un titre qui décrit seulement d'où tu
viens oblige chaque lecteur à t'imaginer ailleurs, et la plupart ne le feront
pas.

**D. Pour une recherche d'emploi** : l'intitulé exact que tapent les
recruteurs (vérifie-le avec `/linkedin-job` sur 5 offres visées), la
spécialité, une preuve.

```
Responsable acquisition B2C | SEA, SEO, CRM | Budget de 1,2 M€ géré en 2025,
coût par lead divisé par 1,8
```

## Avant / après

| Avant | Ce qui ne va pas | Après |
|---|---|---|
| « Responsable marketing chez Assurly » | intitulé seul, ni audience ni preuve | « Responsable acquisition chez Assurly · J'aide les assureurs en ligne à baisser leur coût par lead · −44% en 4 mois » |
| « Passionnée de marketing digital 🚀 Dynamique et créative » | trois mots creux, aucun métier précis | « Social media manager pour les marques de cosmétiques · 3 comptes passés de 5 k à 40 k abonnés en 2024 » |
| « Consultant indépendant » | ne dit ni quoi ni pour qui | « Consultant CRM HubSpot pour les PME B2B · 31 migrations depuis 2021 · J'en sors avec des pipelines que les commerciaux remplissent » |
| « CEO & Founder @Assurly \| Entrepreneur \| Visionnaire \| Speaker \| Mentor » | cinq segments, deux mots creux | « Fondateur d'Assurly, l'assurance habitation en ligne pour les locataires · 38 000 assurés · On recrute des développeurs » |
| « En recherche active d'opportunités » | la recherche d'emploi prend la place d'une preuve | « Chef de projet digital · 6 refontes de sites e-commerce livrées · Disponible en CDI à Lyon » (et le badge « Open to work ») |

Les chiffres des exemples sont fictifs (Assurly est l'entreprise de
démonstration du pack). Dans un vrai titre, chaque chiffre vient de
`reserve.md` ou de l'utilisateur.

## Le positionnement avant les mots

Un titre ne répare pas un positionnement qui n'existe pas. Si l'utilisateur ne
sait pas répondre à ces trois questions, les réécritures resteront génériques :

1. Pour qui, précisément, au point d'exclure quelqu'un ?
2. Qu'obtiennent-ils avec toi qu'ils n'auraient pas avec la prochaine personne
   qui a ton intitulé ?
3. Quelle est la preuve, et est-elle déjà publique ?

Dans ce cas, propose `/linkedin-strategie` d'abord. Le titre en sort en dix
minutes.

## Changer de titre pendant une transition

Deux risques, et on n'en voit souvent qu'un :

- changer trop tôt : les collègues lisent « il s'en va » ;
- changer trop tard : chaque nouveau lecteur te range dans l'ancienne case,
  celle que tu veux quitter.

Le titre est lu surtout par des inconnus, et les inconnus sont justement le
public d'une transition. Change-le, et laisse le poste actuel porter la
continuité dans les expériences.

## Tester

On ne peut pas faire de test A/B sur un titre : il n'y en a qu'un, il
s'applique partout, et les vues de profil sont trop bruitées à l'échelle d'une
personne. Ce qu'on peut faire :

- le lire à voix haute : si tu ne le dirais pas en conférence, coupe ;
- le montrer à **une** personne de la cible et lui demander ce que tu fais.
  Si elle se trompe, le titre est faux. Ce test vaut plus que n'importe quel
  outil ;
- `titre.py` pour les défauts mécaniques, puis la personne.

## Mots creux à supprimer

passionné(e), dynamique, orienté(e) résultats, orienté(e) client,
motivé(e), rigoureux, créatif, curieux, touche-à-tout, couteau suisse,
multi-casquettes, expert(e) reconnu(e), visionnaire, ninja, gourou,
rockstar, serial entrepreneur, thought leader, leader d'opinion, en quête de
nouveaux défis, ouvert(e) aux opportunités, polyvalent(e), force de
proposition, esprit d'équipe, proactif, innovant(e).

## Sources

- alirezarezvani, `linkedin-profile/references/headline_and_positioning.md`
  (MIT) : les cinq dimensions, le chargement par l'avant, la structure de
  transition.
- Serge Bulaev, `profile-headline-formulas.md` (MIT) : avant/après par
  persona. Ses statistiques de vendeur (« 3× plus d'apparitions ») ne sont pas
  reprises.
- Nielsen Norman Group, « Microcontent: How to Write Headlines, Page Titles,
  and Subject Lines » : charger l'avant de tout texte tronqué.
