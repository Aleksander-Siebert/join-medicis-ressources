---
name: linkedin-strategie
description: >-
  Construit la stratégie LinkedIn d'une personne ou d'un dirigeant avant
  d'écrire le moindre post : objectif à 90 jours vérifiable (pas un nombre
  d'abonnés), audience assez précise pour exclure quelqu'un, positionnement
  « J'aide X à Y grâce à Z » et anti-positionnement, 2 à 4 piliers avec parts
  et preuves, équilibre notoriété, éducation et conversion, budget en minutes
  mesuré sur une mauvaise semaine (script), newsletter oui ou non, angles
  selon le profil (fondateur, freelance, salarié, commercial, marketeur).
  Écrit contexte.md, lu par tous les Skills du pack. Utilise-le quand
  l'utilisateur dit « je ne sais pas quoi poster », « ma présence LinkedIn
  n'a pas de cap », « je veux une stratégie LinkedIn », « faut-il lancer une
  newsletter ? », « combien de temps y passer ? », ou démarre sur LinkedIn.
  Pas pour le planning de la semaine (utiliser /linkedin-plan), ni pour un
  post (utiliser /linkedin-post), ni pour la page entreprise (utiliser
  /linkedin-entreprise).
---

# linkedin-strategie

Trois décisions, dans cet ordre : **le brief** (objectif, audience,
exclusions, piliers), **le rythme** (combien de temps, vraiment), **la
newsletter** (seulement si la promesse peut être tenue). Dans le désordre,
on obtient un fil de remarques sans lien, abandonné la 5e semaine.

Ce Skill ne rédige pas de posts. Il écrit `contexte.md`, que tous les autres
Skills lisent.

**À lire avant de commencer :** `commun/regles.md` et `commun/preuves.md`.

## 1. Lire ce qui existe

- `contexte.md` : s'il est rempli, ne repose que ce qui manque ou a changé
  (une stratégie se revoit chaque trimestre, pas chaque semaine).
- `reserve.md` : les preuves existantes décident des piliers possibles.
- `apprentissages.md` et l'audit le plus récent : ce qui a marché.

Si rien n'existe, annonce le cadre en deux lignes : 20 à 30 minutes, une
question à la fois, chaque question vient avec une réponse recommandée.

## 2. Les cinq questions qui forcent

Une question par message, **chacune avec une réponse recommandée**. Relance
une fois une réponse faible, puis accepte-la et **note-la comme faible** dans
le brief : elle sera visible plus tard, au lieu d'être discutée maintenant.
Détail, relances et exemples : `references/questions.md`.

| # | Question | Réponse recommandée |
|---|---|---|
| 1 | Qu'est-ce qui doit être vrai dans 90 jours pour que ça ait valu le coup ? | un résultat qu'un tiers peut vérifier : des conversations entrantes, des rendez-vous, une offre, une invitation. Pas un nombre d'abonnés |
| 2 | Pour qui, assez précis pour exclure quelqu'un ? | rôle + taille ou stade de l'entreprise + le problème qu'ils ont ce trimestre |
| 3 | Combien de minutes par semaine, mesurées sur une **mauvaise** semaine ? | le chiffre honnête ; sous 90, on commence par des semaines « commentaires seulement » |
| 4 | Quelle preuve existe déjà ? | un résultat chiffré, un projet livré, un client, une intervention ; sinon le premier pilier parle du processus, pas des résultats |
| 5 | De quoi tu ne parleras pas ? | deux sujets, dont le sujet tendance sur lequel tu n'as aucun avantage |

Si l'utilisateur refuse de répondre aux questions 1 ou 2 : dis simplement que
le travail ne peut pas être visé sans elles, et propose `/linkedin-profile`,
qui n'en a pas besoin.

## 3. Affiner la niche (si le positionnement reste flou)

Sept questions, une à la fois, avec reformulation après chaque réponse
(`references/questions.md`, partie 2) : ce que tu fais vraiment de tes
journées ; les 3 personnes qui te paient, t'embauchent ou te recommandent ;
leur problème ; ce que tu sais et que 90% de ton métier ignore ; ce pour quoi
tu ne veux pas être connu ; qui tu détesterais attirer ; la phrase qu'un
inconnu dirait de toi après 5 posts.

Synthèse :

```
Audience : …            Problème : …
Angle : …               Anti-positionnement : …
« J'aide {{audience}} à {{résultat}} grâce à {{angle}}. »
3 variantes : …
Filtre pour chaque post : « Est-ce que ça sert {{audience}} sur {{problème}} avec {{angle}} ? Sinon, on ne publie pas. »
```

## 4. Les piliers

2 à 4 piliers. Chacun a un nom (dans les mots de l'audience), une part en
pourcentage, un « pourquoi moi », une preuve (ou « expérimental ») et une
étape de l'entonnoir. Règles et mélanges par profil :
`references/objectifs-piliers.md`.

- Les parts font 100%. C'est un budget : il dit ce qu'on coupe une semaine
  chargée.
- Au moins un pilier s'appuie sur une preuve qui existe déjà.
- Au moins un pilier expérimental à 10-20% : le pilier principal du trimestre
  prochain viendra de là.
- Aucun pilier au-delà de 60%.
- Entonnoir : notoriété, éducation, conversion ; **la conversion ne dépasse pas
  un post sur cinq**.
- Profil fondateur, freelance, salarié, commercial ou marketeur : des angles
  propres à chacun dans `references/angles.md`.

## 5. Vérifier le brief (script)

Remplis le JSON décrit en tête de `scripts/brief.py`, puis :

```
python3 scripts/brief.py --fichier brief.json
```

Il refuse : objectif hors liste, objectif à 90 jours mesuré en abonnés,
audience trop large, moins de 2 exclusions, piliers hors 2-4 ou parts qui ne
font pas 100. Il demande de reprendre : aucun pilier prouvé, pas de pilier
expérimental, pilier au-delà de 60%, conversion au-delà de 20%, exclusions de
façade. Il rend les **critères à 90 jours** (vérifiables, à chiffrer avec
l'utilisateur) et un brouillon de phrase de positionnement à raccourcir.

Sans exécution de code : applique les mêmes règles à la main.

## 6. Le budget en minutes (script)

```
python3 scripts/budget.py --minutes {{minutes}} --etape {{depart|reconstruction|etabli}} --posts {{n}}
```

- Chaque activité est chiffrée en minutes, **réponses aux commentaires
  comprises** : répondre sous son post fait partie du post.
- Étape « départ » (moins d'environ 1 000 abonnés) : 60% du temps en
  commentaires sous les posts des autres, parce qu'un post publié pour personne
  ne touche personne [praticien, cohérent entre sources].
- Sous 90 minutes : semaine « commentaires seulement ».
- Toujours une **semaine minimale** : 1 post le même jour chaque semaine,
  1 commentaire utile par jour ouvré, réponse à chaque commentaire sous 24 h.
- Les coûts sont des ordres de grandeur ; remplace-les par les temps mesurés
  de l'utilisateur (`--cout texte=40`).

## 7. Newsletter : oui ou non

Seulement si les trois conditions tiennent (`references/rythme-newsletter.md`) :

1. **Éligibilité** : plus de 150 abonnés ou relations, du contenu original
   récent, un historique conforme aux règles [officiel, aide LinkedIn
   a591266] ; 150 est un seuil d'évaluation, pas une garantie.
2. **Soutenabilité sur 6 mois** : rythme × coût d'un numéro ≤ budget (un
   numéro ≈ 150 min [praticien]). Baisser le rythme avant le lancement ne coûte
   rien ; après, c'est une promesse rompue.
3. **Règle d'arrêt écrite avant le n°1** : par exemple, 3 numéros d'affilée
   sous la moitié de l'engagement médian des posts → retour aux posts.

Avant le lancement : 2 numéros d'avance, un nom qui dit le problème (pas
« La newsletter de Camille »), un arc de 12 numéros qui alterne les types
(méthode, décorticage, carnet de terrain, contre-pied, question de lecteur,
sélection).

## 8. Écrire contexte.md (après « oui »)

Montre d'abord ce qui sera écrit, section par section, puis écris dans
`~/.claude/linkedin/contexte.md` (modèle : `commun/modeles/contexte.md`) :

- partie « Personne » : objectif à 90 jours, budget, positionnement, piliers,
  positions, hors-limites ;
- partie « Entreprise » (si clients, recrutement ou dirigeant) : offres, sujet
  → offre → phrase d'appel à l'action, preuves avec étiquette **LIVE /
  À CONFIRMER / RETIRÉ**, date et source, vocabulaire client mot pour mot,
  formulations retirées ;
- « rempli : oui », la date, la date de la prochaine relecture (3 mois).

Un fait dont l'utilisateur n'est pas sûr est étiqueté **À CONFIRMER** :
les autres Skills l'écriront `{{à confirmer : …}}`. Rien n'est inventé.

## Sortie (format fixe)

```
STRATÉGIE LINKEDIN · {{prénom}} · {{date}} · revue le {{date + 3 mois}}

Objectif à 90 jours : {{…}}  ({{faible si noté faible}})
Critères vérifiables : · … · … · …
Audience : {{…}}   Exclusions : {{…}}, {{…}}
Positionnement : « J'aide … à … grâce à … »

Piliers
| Pilier | Part | Étape | Pourquoi moi | Preuve |

Budget : {{n}} min/semaine · étape {{…}} → {{n}} posts, {{n}} commentaires
Semaine minimale : {{…}}
Newsletter : {{oui (rythme, nom, règle d'arrêt) | pas maintenant (raison)}}

Brief : {{VALIDE | À REPRENDRE : …}}
À vérifier : {{…}}
Suite proposée : /linkedin-interview (si reserve.md est vide) ou /linkedin-plan
```

## Erreurs et cas limites

| Situation | Que faire |
|---|---|
| « Je veux devenir influenceur » | demander ce que l'influence doit apporter dans 90 jours ; si c'est une audience, l'objectif est « communauté » ou « autorité », avec des critères vérifiables |
| Deux objectifs (clients et emploi) | un seul par trimestre ; les audiences se recoupent moins qu'on ne croit |
| Aucune preuve (débutant, reconversion) | premier pilier « processus » : ce que tu apprends, testes, construis, daté ; jamais de résultat inventé |
| Salarié dont l'employeur encadre la parole | vérifier la charte interne ; exclusions explicites (clients, chiffres internes) ; le garde-fou signale le sujet |
| Dirigeant qui délègue l'écriture | normal s'il relit et valide chaque post ; il reste l'auteur (garde-fou, règle R4) |
| Secteur réglementé (santé, finance, droit) | exclusions réglementaires dans le brief ; pas de promesse de résultat |
| Budget sous 90 min | semaines « commentaires seulement » d'abord ; on refait le budget dans un mois |
| Demande de pods, d'automatisation ou de croissance « rapide » | garde-fou : refus avec la règle et l'alternative (`commun/garde_fou.py`) |
| Pas d'accès aux fichiers | rendre `contexte.md` en bloc à coller dans les connaissances du Projet |

## Ressources

- `scripts/brief.py` : vérifie le brief, rend les critères à 90 jours.
- `scripts/budget.py` : budget en minutes, étapes, semaine minimale.
- `references/questions.md` : les 5 questions, les 7 questions de niche, la
  fiche persona.
- `references/objectifs-piliers.md` : objectifs, piliers, entonnoir, mélanges
  par profil.
- `references/angles.md` : angles fondateur, freelance, salarié, commercial,
  marketeur.
- `references/rythme-newsletter.md` : coûts en minutes, étapes, newsletter.
- `references/exemple.md` : une stratégie complète (Assurly).
- `commun/modeles/contexte.md` : le fichier écrit par ce Skill.

## Skills liés

- `/linkedin-interview` : remplit `reserve.md`, les preuves des piliers.
- `/linkedin-profile` : le titre et les Infos découlent du positionnement.
- `/linkedin-plan` : transforme la stratégie en semaine.
- `/linkedin-entreprise` : la page et les ambassadeurs, si l'objectif est porté
  par l'entreprise.
- `/linkedin-audit` : revue trimestrielle, avec des données.
