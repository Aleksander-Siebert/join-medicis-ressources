# Exemple : de la consigne aux contrôles

> **Exemple fictif.** Assurly, ses données et le brouillon « IA » sont
> inventés pour montrer la méthode. Les sorties des scripts sont réelles :
> elles viennent des fichiers `evals/seo-write/` du pack, lancés le
> 12 octobre 2026. Le plan est celui de `/seo-brief` (`references/exemple.md`
> de ce Skill-là).

## 1. Ce qu'un brouillon « IA » donne aux contrôles

Le brouillon de départ (`article-ia.md`) ouvre sur « Dans un monde en
constante évolution », annonce son plan, cite « une étude récente »,
promet « la moins chère du marché, remboursée à 100% sans aucun risque »,
écrit « Chez Assurly » et finit sur « Défis et perspectives » puis
« Conclusion ».

```
$ python3 scripts/controle.py article-ia.md --affirmatif --remplacer "chez Assurly=à Assurly" \
      --interdire cash --longueur 1000-1500 --mot-cle "mutuelle indépendant" --marque Assurly
CONTRÔLE · 203 mots · 1 lien(s) interne(s) · 1 gras · 0 trou(s)
  title 102 car. / 910 px · description 74 car. / 467 px

HAUTE
  [structure] résumé en tête absent (citation « > » de 3 lignes juste après l'introduction)
  [bloc méta] année dépassée dans le title (2025)
      → Google réécrit les titles périmés. Mettre à jour la page, puis l'année ; ou retirer l'année.
  [bloc méta] description en liste de mots-clés
      → Écrire une phrase qui résume la page.
  [maison] l.13 « Chez Assurly » au lieu de « à Assurly »
  [structure] l.19 section interdite : « Défis et perspectives »
      → Finir sur une réponse utile ou une action concrète, sans section de clôture.
  [structure] l.23 section interdite : « Conclusion »
      → Finir sur une réponse utile ou une action concrète, sans section de clôture.

MOYENNE
  [forme] phrase entière en gras : « Il est essentiel de bien comparer les offres avant de signer »
      → Le gras marque une notion, pas une phrase.
  [bloc méta] title de 910 px (repère ≈ 600 px) : probablement coupé
      → Affichage estimé : « Mutuelle indépendant 2025 : le guide ultime de la mutuelle pour i … ». Garder les mots importants au début.
  [bloc méta] marque répétée dans le title
      → Une fois, au début ou à la fin.
…
VERDICT : À REVOIR
```

```
$ python3 commun/affirmations.py article-ia.md --ymyl --contexte site-context.md
AFFIRMATIONS · 5 relevées · 0 sourcées ou fournies · 0 à vérifier · 5 bloquantes · 0 trous · mode YMYL

BLOQUANTES (YMYL : pas de publication sans source)
  l.9    [pourcentage, étude · vague] Selon une étude récente, 73% des indépendants regrettent leur choix de mutuelle.
         → Nommer la source (organisme, date, lien) ou retirer l'affirmation. « Une étude » n'est pas une source.
  l.9    [étude · vague] Les experts estiment que c'est une erreur coûteuse.
         → Nommer la source (organisme, date, lien) ou retirer l'affirmation. « Une étude » n'est pas une source.
  l.13   [montant · sans source] Une mutuelle pourrait coûter entre 30 € et 150 € par mois.
         → Ajouter la source (lien ou « selon X, date »), ou la donnée dans site-context.md, ou remplacer par une formulation sans chiffre, ou {{à compléter : source}}.
…
VERDICT : BLOQUÉ
```

Humaniseur (profil article) : **31,6, SIGNALÉ**.

Ce brouillon ne se corrige pas ligne à ligne : il se réécrit sur le plan.

## 2. L'article rédigé sur le plan validé

````markdown
# Mutuelle indépendant : comment choisir sa couverture santé en 2026

Vous quittez un CDI pour vous installer à votre compte : la mutuelle de votre ancien employeur s'arrête, et la question arrive vite. Faut-il en prendre une, laquelle, et à quel prix ?

> Une mutuelle n'est pas obligatoire pour un indépendant, mais l'Assurance maladie ne rembourse pas tout.
> Ce guide montre ce qu'elle couvre, ce qui fait varier son prix et comment déduire vos cotisations.
> Il se termine sur l'erreur que nous voyons le plus souvent en rendez-vous.

## Faut-il une mutuelle quand on est indépendant ?

Non, aucune loi ne vous oblige à souscrire une mutuelle pour vous-même quand vous êtes indépendant (source : {{à compléter : page service-public.fr sur la complémentaire santé des travailleurs indépendants}}). L'Assurance maladie rembourse une partie de vos soins ; la mutuelle complète tout ou partie du reste.

Ce reste à charge pèse surtout sur l'hospitalisation, le dentaire et l'optique. Sans mutuelle, vous le payez seul.

L'obligation existe dans un autre cas : si vous embauchez un salarié, vous devez lui proposer une mutuelle collective. Notre page [mutuelle entreprise](/mutuelle-entreprise/) détaille ce point.

### Micro-entrepreneur : les mêmes règles ?

Oui pour l'obligation : un micro-entrepreneur choisit librement de prendre une mutuelle ou non. La différence porte sur la fiscalité, expliquée plus bas avec le dispositif Madelin.

## Ce que rembourse une mutuelle pour indépendant

Une mutuelle rembourse ce que l'Assurance maladie laisse à votre charge, selon le niveau de garanties que vous choisissez. Les quatre postes à regarder en premier :

| Poste | Ce que vous vérifiez dans le tableau des garanties |
|---|---|
| Hospitalisation | chambre particulière, dépassements d'honoraires du chirurgien |
| Dentaire | prothèses, implants, orthodontie |
| Optique | montures et verres, fréquence de renouvellement |
| Médecine douce | nombre de séances par an, montant par séance |

À Assurly, les trois formules pour indépendants s'appellent Essentielle, Confort et Intégrale. Leurs niveaux de remboursement figurent dans les conditions générales : {{à compléter : niveaux de remboursement par formule, conditions générales 2026}}.

### Couvrir sa famille et ses enfants

Vous ajoutez votre conjoint et vos enfants à charge comme ayants droit sur le même contrat. Le prix augmente avec chaque personne couverte : demandez un devis pour toute la famille plutôt que d'additionner des contrats séparés.

### Après 60 ans

Les besoins changent avec l'âge : l'optique, l'audition et l'hospitalisation comptent davantage. Relisez vos garanties à chaque échéance annuelle, avant de résilier.

## Combien coûte une mutuelle indépendant

Le prix d'une mutuelle dépend de votre âge, de votre lieu de résidence, du nombre de personnes couvertes et du niveau de garanties. Aucun tarif sérieux ne se donne sans ces quatre informations : c'est pourquoi nous les demandons avant tout chiffre.

Une mutuelle pas chère couvre souvent bien les soins courants et peu l'hospitalisation. Avant de comparer deux prix, comparez les deux tableaux de garanties sur les mêmes postes.

Pour un prix exact, faites une [demande de devis](/devis/) : vous recevez votre attestation sous 48 h ouvrées après la souscription.

## Mutuelle Madelin : la déduction des cotisations

Un contrat dit « Madelin » permet à certains indépendants de déduire leurs cotisations de leur bénéfice imposable, dans la limite d'un plafond revu chaque année : {{à compléter : plafond Madelin 2026, source impots.gouv.fr}}.

Le dispositif concerne les indépendants imposés au régime réel. Sous le régime micro-fiscal, l'abattement forfaitaire tient déjà compte des charges : la déduction Madelin ne s'applique pas (source : {{à compléter : page impots.gouv.fr sur la déduction Madelin}}). Votre expert-comptable vous dit en cinq minutes si votre contrat est déductible.

## Comment choisir sa mutuelle d'indépendant en 4 étapes

1. **Listez vos besoins réels** : lunettes, soins dentaires prévus, enfants, médecine douce.
2. **Comparez les garanties**, poste par poste, avant de comparer les prix.
3. **Vérifiez le délai de carence** : certaines formules ne remboursent pas tout dès le premier jour.
4. **Regardez les conditions de résiliation**, pour changer de contrat si votre situation évolue.

La meilleure mutuelle d'indépendant n'existe pas dans l'absolu : c'est celle qui couvre vos dépenses probables au prix le plus juste.

## Ce que nous voyons en rendez-vous : la confusion entre mutuelle et prévoyance

La mutuelle rembourse vos soins. Elle ne verse rien si vous ne pouvez plus travailler. Ce rôle revient à la prévoyance, qui verse des indemnités journalières en cas d'arrêt de travail.

Nos courtiers rencontrent cette confusion chaque semaine. Au premier semestre 2026, 41% des demandes de prévoyance reçues à Assurly venaient d'indépendants installés depuis moins de trois ans, souvent après un premier arrêt. Si votre activité dépend de votre capacité à travailler, regardez aussi notre page [prévoyance indépendant](/prevoyance-independant/).

Pour comparer les formules sur votre situation, une [mutuelle indépendant](/mutuelle-independant/) se choisit avec le tableau des garanties sous les yeux : demandez-le avec votre devis.

BLOC MÉTA
Title : Mutuelle indépendant : bien la choisir en 2026 | Assurly
Meta description : Obligatoire ou non, remboursements, prix, Madelin : ce qu'un indépendant vérifie avant de choisir sa mutuelle, expliqué par une courtière.
Mot-clé principal : mutuelle indépendant
Mots-clés secondaires : mutuelle auto-entrepreneur, mutuelle Madelin, prix mutuelle indépendant
Slug : /blog/mutuelle-independant/
````

## 3. Les contrôles de l'article

```
$ python3 scripts/controle.py article.md --affirmatif --remplacer "chez Assurly=à Assurly" \
      --interdire cash --longueur 1000-1500 --mot-cle "mutuelle indépendant" --marque Assurly
CONTRÔLE · 763 mots · 4 lien(s) interne(s) · 4 gras · 4 trou(s)
  title 56 car. / 490 px · description 138 car. / 852 px

INFO
  [forme] 763 mots, hors de la préférence 1000-1500
      → Préférence de site-context.md, pas une règle de Google : couper le remplissage ou compléter un manque réel.

À COMPLÉTER PAR L'UTILISATEUR
  {{à compléter : page service-public.fr sur la complémentaire santé des travailleurs indépendants}}
  {{à compléter : niveaux de remboursement par formule, conditions générales 2026}}
  {{à compléter : plafond Madelin 2026, source impots.gouv.fr}}
  {{à compléter : page impots.gouv.fr sur la déduction Madelin}}

VERDICT : PRÊT
```

```
$ python3 commun/affirmations.py article.md --ymyl --contexte site-context.md
AFFIRMATIONS · 6 relevées · 2 sourcées ou fournies · 0 à vérifier · 0 bloquantes · 4 trous · mode YMYL

TROUS ASSUMÉS (à fournir par l'utilisateur)
  l.11   [à compléter · trou] Non, aucune loi ne vous oblige à souscrire une mutuelle pour vous-même quand vous êtes indépendant (source : {{à compléter : page service…
  l.32   [à compléter · trou] Leurs niveaux de remboursement figurent dans les conditions générales : {{à compléter : niveaux de remboursement par formule, conditions …
  l.52   [à compléter · trou] Un contrat dit « Madelin » permet à certains indépendants de déduire leurs cotisations de leur bénéfice imposable, dans la limite d'un pl…
  l.54   [à compléter · trou] Sous le régime micro-fiscal, l'abattement forfaitaire tient déjà compte des charges : la déduction Madelin ne s'applique pas (source : {{…

SOURCÉES OU FOURNIES
  l.48   [fournie] Pour un prix exact, faites une demande de devis : vous recevez votre attestation sous 48 h ouvrées après la so
  l.69   [fournie] Au premier semestre 2026, 41% des demandes de prévoyance reçues à Assurly venaient d'indépendants installés de

VERDICT : OK
```

Humaniseur (profil article) : **72,4, OK**.

Lecture :

- **763 mots**, sous la préférence de 1 000 à 1 500 : l'article répond aux
  24 requêtes du plan sans remplissage. On le livre tel quel et on le dit ;
  les sections s'allongeront avec les données à compléter (niveaux de
  remboursement, règle Madelin sourcée).
- **Deux faits fournis** par `site-context.md` (48 h ouvrées, 41% des
  demandes), **quatre trous** listés : la règle légale et la règle fiscale
  ne sont pas affirmées sans leur page officielle.
- **Qualité Google 15/16** : il manque la signature de l'auteure (contrôle 8)
  sous le titre.

## 4. Le bloc rendu à l'utilisateur

```
CONTRÔLES
Rédaction       PRÊT (controle.py) · 763 mots (préférence 1 000-1 500, non rembourré) · 4 liens internes
Affirmations    OK en mode YMYL · 2 faits fournis (site-context.md) · 4 trous assumés
Humaniseur      72,4 OK (profil article)
Qualité Google  15/16 · reste : signature de Claire M. (courtière, ORIAS) sous le titre
À COMPLÉTER
  {{à compléter : page service-public.fr sur la complémentaire santé des travailleurs indépendants}}
  {{à compléter : niveaux de remboursement par formule, conditions générales 2026}}
  {{à compléter : plafond Madelin 2026, source impots.gouv.fr}}
  {{à compléter : page impots.gouv.fr sur la déduction Madelin}}
```

Version publiable sans trou, si l'utilisateur la demande : on retire la
parenthèse de source de la première réponse (la phrase reste prudente), la
phrase sur les niveaux de remboursement, le plafond et la phrase sur le
régime micro-fiscal, en renvoyant au devis et à l'expert-comptable.
