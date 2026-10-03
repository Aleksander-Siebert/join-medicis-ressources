# Résultats de l'évaluation v2.0 (2 et 3 octobre 2026)

10 tâches réelles ont été jouées deux fois par Claude, chaque fois avec un
seul jeu de Skills :

- **v2** : ce pack ;
- **référence** : pour chaque tâche, le meilleur Skill open-source analysé
  pour ce sujet (tableau ci-dessous), avec ses scripts.

Un troisième agent a jugé **à l'aveugle** : les deux réponses de chaque cas
étaient nommées X et Y au hasard (`resultats-v2.0/cle.json`), les attentes
étaient neutres (aucune ne cite un script ou un fichier propre à l'un des
deux packs), et le juge n'avait accès qu'au dossier `resultats-v2.0/aveugle/`.

Tout est publié : les demandes (`cas.json`), les réponses complètes
(`join-medicis/`, `reference/`), les paires anonymes, le jugement intégral
(`jugement.md`) et les problèmes relevés par l'agent qui a joué la v2
(`join-medicis/notes.md`).

## Résultat

**La v2 gagne 8 cas sur 10, en perd 1, 1 égalité. Note moyenne : 7,95 contre
7,15 sur 10.**

| Cas | Tâche | Référence | v2 | réf. | Verdict |
|---|---|---|---|---|---|
| 1 | Post sur les 60 appels | Serge Bulaev, linkedin-post-writer | 8 | 6,5 | **v2** : 3 accroches de formes différentes, rien d'ajouté ; la référence cite des chiffres externes sans source |
| 2 | Répondre aux commentaires | Serge Bulaev, linkedin-reply-handler | 8,5 | 8 | **v2**, de peu : plus court, garde le vouvoiement de Sarah ; la référence suppose une répartition des appels |
| 3 | Message pour 200 DAF | Alireza Rezvani, linkedin-engagement | 8,5 | 6,5 | **v2** : cadre CNIL appliqué (profession, moyen de dire non), note de 147 caractères ; la note de la référence dépasse 200 une fois remplie |
| 4 | Audit de 14 posts | Alireza Rezvani, linkedin-analytics | 7,5 | 8,5 | **référence** : même rigueur, présentation bien plus claire (tableau mardi/jeudi) ; la v2 colle 60 lignes de sortie de script |
| 5 | Noter et réécrire le profil | Alireza Rezvani, linkedin-profile | 8 | 5,5 | **v2** : marque « ? » ce qui n'a pas été montré ; la référence note photo et bannière à partir de réponses supposées |
| 6 | Trier la messagerie | Joshua (Design Industries), di-li-inbox | 8,5 | 8 | **v2**, de peu : seule à fournir la ligne CRM avec sa source |
| 7 | Humaniser un texte | Boileau | 7 | 7 | **égalité** : la v2 est fidèle mais rend un texte à trous ; la référence est publiable mais affaiblit le fond (« plus que le prix ») et ajoute une opinion |
| 8 | Recycler un webinaire | Alireza Rezvani, linkedin-content | 7,5 | 7 | **v2**, de peu : respecte toutes les attentes, mais n'écrit aucun post ; la référence écrit 2 posts avec des maximes inventées et frôle la redite |
| 9 | Plan de la semaine | Serge Bulaev, linkedin-content-planner | 8 | 7 | **v2** : angles tirés de la semaine, marge de temps ; la référence avance des normes sans source |
| 10 | Stratégie, « plus d'abonnés » | Alireza Rezvani, linkedin-strategy | 8 | 7,5 | **v2**, de peu : plan construit sur la semaine de 30 minutes, publics exclus |

## Contrôles automatiques (textes à coller)

| Cas | Score humain v2 | réf. | Tirets cadratins v2 / réf. | Ponctuation collée v2 / réf. | Longueur v2 / réf. |
|---|---|---|---|---|---|
| 1 · post | 96,9 | 92,8 | 0 / 0 | 0 / 0 | 424 / 960 car. |
| 2 · réponses | 82,6 | 92,8 | 0 / 0 | 0 / 0 | 488 / 553 car. |
| 3 · note et message | 93,6 | 100 | 0 / 0 | 0 / 0 | 966 / 929 car. |
| 7 · texte humanisé | 58,4 | 60,0 | 0 / 0 | 0 / 0 | 363 / 333 car. |

Score humain : `detect.py` de ce pack, donc favorable par construction aux
textes écrits avec lui. À lire comme un contrôle, pas comme une preuve.

## Les défaites, et ce qui a été corrigé

**Cas 4 (perdu) : la v2 montrait la sortie brute de ses scripts.** Une
marketeuse ne lit pas « CV robuste 0,447 » dans un bloc de 60 lignes.
Corrigé :

- règle commune (`commun/regles.md`, section 8) : la sortie d'un script est
  une matière, pas la réponse ; on la traduit en phrases et tableaux courts ;
- `/linkedin-audit` : sortie en phrases et tableaux, et un tableau qui met les
  facteurs confondus côte à côte (repris de la meilleure idée de la
  référence) ; l'exemple est réécrit ainsi.

**Cas 7 (égalité) : la v2 rendait un texte à trous.** Corrigé : `/linkedin-human`
rend toujours une version publiable sans trou (on retire ce qui manque au
lieu de l'inventer), et une version enrichie avec les `{{à compléter}}` à
côté. Il interdit aussi d'affaiblir une affirmation pour faire joli (le défaut
de la référence).

**Cas 8 (gagné, mais) : aucun post écrit.** Corrigé : `/linkedin-repurpose`
rédige tout de suite le premier post.

**Bugs trouvés par l'agent qui jouait la v2** (`join-medicis/notes.md`),
tous corrigés et couverts par un test :

| Problème | Correction |
|---|---|
| L'humaniseur ratait « Le résultat ? » en milieu de paragraphe, « véritable » seul, la triade sans « et », « les clés du succès » | 4 détections ajoutées ; le texte du cas 7 est désormais signalé en entier |
| `fidelite.py` bloquait un `{{à compléter}}` ajouté comme un fait inventé | un trou est signalé, jamais bloquant |
| Le garde-fou classait « un message pour ma liste de 200 DAF » en ENCADRÉ | REFUSÉ (règle R5) ; `/linkedin-dm` dit quoi livrer pour une liste |
| `audit.py experience --help` plantait | corrigé ; le test d'intégrité lance désormais `--help` sur chaque sous-commande |
| Motifs confondus mal regroupés | recouvrement mesuré dans les deux sens, avec tous les membres du groupe |
| `titre.py` ne voyait pas « 60 résiliés » ni « de 12 à 5 jours » comme des preuves | volumes et avant/après reconnus ; un caractère de contrôle glissé dans une expression régulière a été trouvé au passage, et le test d'intégrité les cherche désormais partout |
| Une ouverture « Bienvenue sur mon profil ! » gardait 7/10 | 4/10 |
| `budget.py` donnait 0 post pour 120 minutes en démarrage | le minimum de commentaires suit la part d'engagement : 1 post et 12 commentaires |
| Phrase de positionnement agrammaticale | virgules, et avertissement quand le problème ou l'angle est mal formulé |
| Note CRM coupée en pleine phrase | coupée à la fin d'une phrase |
| `--type webinaire` refusé | accepté |
| 30 minutes de réponses dans le SKILL, 20 dans le script | 20 partout |
| Le modèle de refus de `/linkedin-inbox` était signalé par l'humaniseur | réécrit |
| Les exemples Assurly pouvaient être recopiés comme des faits | chaque exemple porte un avertissement ; le gabarit de plan ne nomme plus personne |

## Limites

- Un seul passage par cas : un écart d'un demi-point n'est pas significatif.
- Le juge est le même modèle que les joueurs. Il ne connaissait pas la clé,
  mais certains indices (noms de scripts dans les réponses) pouvaient trahir
  un pack.
- La v2 a été jouée avant les corrections ci-dessus : les défaites sont
  celles de la version jouée, pas de la version publiée.
- Les cas viennent du contexte fictif Assurly, pas de demandes réelles de
  l'utilisateur. La prochaine série devrait partir de vraies demandes.
- Plusieurs scripts de référence ne reconnaissent que des mots anglais :
  l'agent les a utilisés tels quels, avec des notes parfois faussées en
  français (cas 5).

L'évaluation de la v1 (1er octobre 2026) est dans
[`resultats-v1.0/RESULTATS.md`](resultats-v1.0/RESULTATS.md).
