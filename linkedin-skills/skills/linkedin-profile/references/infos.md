# La section Infos : écrire pour le pli

LinkedIn replie la section Infos après les premiers caractères et cache la
suite derrière « … voir plus ». La position n'est pas publiée : on l'observe
entre ~200 caractères (téléphone) et ~265 (ordinateur), et elle bouge avec
l'interface. Écris pour le plus court.

Ce qui est au-dessus du pli est **toute la section** pour la plupart des
lecteurs. Le reste sert à celui qui évalue et à celui qui décide.

## Les règles qui ne se discutent pas

- **Une phrase complète avant le pli**, idéalement avant le 200e caractère. Un
  mot coupé est le signal pour arrêter de lire. (`infos.py` : bloquant.)
- **Le pli porte l'audience ou une preuve.** Sinon c'est un échauffement, et
  c'est tout ce qu'on lira. (bloquant)
- **Première personne.** Un profil à la troisième personne se lit comme un
  communiqué écrit par quelqu'un d'autre.
- **Un appel à l'action** à la fin (sauf objectif autorité, où c'est conseillé).
  (bloquant)
- **2 600 caractères au plus** ; **400 à 1 500 conseillés**. Au-delà de 1 500,
  chaque phrase doit mériter sa place.
- Des sauts de ligne toutes les 2 ou 3 phrases : sur mobile, un paragraphe de
  600 caractères est un mur.
- Pas de pseudo-gras Unicode (𝗴𝗿𝗮𝘀) : illisible pour les lecteurs d'écran.

## Structure en 7 temps

| Temps | Rôle | Budget indicatif |
|---|---|---|
| 1. Accroche | le problème du lecteur, dans ses mots, ou un chiffre qui surprend | ~120 car. |
| 2. Pour qui et quoi | ce que tu fais, pour qui (assez précis pour exclure) | ~120 car. |
| 3. Preuves | 2 ou 3 résultats chiffrés au format X / Y / Z, tirés de `reserve.md` | ~300 car. |
| 4. Comment tu travailles | ce qui t'est propre, pas ce que fait ton intitulé | ~250 car. |
| 5. Une ligne humaine (facultatif) | un détail vrai, pas une liste de loisirs | ~80 car. |
| 6. Mots-clés en phrases | les termes qu'on cherche, dans de vraies phrases | ~150 car. |
| 7. Appel à l'action | qui doit t'écrire, et ce qu'il obtient | ~120 car. |

Les temps 1 et 2 doivent tenir avant le pli. Le temps 6 n'est pas une liste de
mots-clés en bas de page : un terme utilisé dans une phrase vaut plus que le
même terme dans une liste (`infos.py --mots-cles` vérifie qu'ils sont dans le
texte).

## L'appel à l'action selon l'objectif

| Objectif | Exemple |
|---|---|
| Clients | « Tu diriges le marketing d'un assureur en ligne et ton coût par lead monte ? Écris-moi : en 20 minutes, je te dis où je chercherais en premier. » |
| Emploi | « Je cherche un poste de responsable acquisition B2C en CDI, à Lyon ou en télétravail partiel. Le plus simple : un message ici. » |
| Autorité | « J'écris chaque semaine sur l'acquisition en assurance : le lien vers la newsletter est dans la Sélection. » |

Interdits : « N'hésitez pas à me contacter ! » (ne dit ni qui ni pourquoi),
« Commentez INFO pour recevoir… » (appât, voir `commun/preuves.md`),
« Restons connectés » (aucune prochaine étape).

## Ouvertures à éviter

| Ouverture | Pourquoi | À la place |
|---|---|---|
| « Fort de 15 ans d'expérience… » | la formule de CV la plus courante ; l'ancienneté n'est pas un résultat | le problème du lecteur ou un chiffre |
| « Passionné(e) par… » | une attitude, pas une information | ce que tu fais pour qui |
| « Bonjour et bienvenue sur mon profil ! » | le lecteur n'apprend rien | entrer dans le sujet |
| « Je suis Camille, … » | le nom est déjà au-dessus | commencer par le lecteur |
| « Mon parcours m'a mené… » | méta-annonce, biographie | ce que le parcours permet aujourd'hui |
| « Camille est une professionnelle… » | troisième personne | « je » |

## Exemple complet (objectif clients)

Personne fictive : Camille, responsable acquisition chez Assurly, qui lance
une activité de conseil avec l'accord de son employeur.

```
Un tiers des clients d'une assurance en ligne ne renouvelle pas, et la
plupart des équipes pensent que c'est une question de prix. Chez Assurly,
j'ai appris que c'était souvent le délai de remboursement.

Je dirige l'acquisition d'Assurly, une assurance en ligne de 120 salariés :
publicité, SEO, emailing et fidélisation.

Ce que j'ai fait, en chiffres :
· Réduit le coût par lead de 41 € à 23 € en 4 mois, budget constant.
· Relancé 1 400 clients dormants en 6 semaines : 212 contrats réactivés.

Comment je travaille : je pars des appels clients avant de toucher aux
campagnes. Les mots qu'ils emploient finissent dans nos annonces.

Tu diriges le marketing d'un assureur ou d'un courtier en ligne et ton coût
par lead monte ? Écris-moi en message privé : je te dis en 20 minutes où je
chercherais en premier.
```

`python3 scripts/infos.py --exemple` donne `PASSE` : la première phrase finit
avant le pli, le pli porte l'audience (« assurance en ligne ») et un chiffre
(« un tiers »), l'appel à l'action dit qui et quoi.

À vérifier avant publication : « un tiers des clients ne renouvelle pas »
vient d'un chiffre interne. Est-il publiable ? Sinon : « Beaucoup de clients
d'une assurance en ligne ne renouvellent pas » perd en force, mais pas en
vérité.

## Sources

- alirezarezvani, `profile_architecture.md` et `about_section_builder.py`
  (MIT) : le pli, les refus (pli coupé, pli vide, pas d'appel à l'action).
- Serge Bulaev, `about-section-templates.md` (MIT) : la structure en 7 temps
  et ses budgets. Son exemple d'appel à l'action « Comment "AUDIT" » n'est pas
  repris (appât).
- Barbara Minto, *The Pyramid Principle* : la réponse d'abord, le soutien
  ensuite.
