# Appliquer la voix, puis la mettre à jour

## 1. Réécrire un texte dans la voix

1. Lis `tone-of-voice.md` en entier. Note la confiance : « faible » veut dire
   que le rythme est indicatif.
2. Lis 2 extraits de la section 10.
3. Repère le canal et prends sa ligne en section 8 (adresse, longueur,
   ouverture, fin, formule d'appel, signature). Canal absent : demande-le, ou
   prends le plus proche et dis lequel.
4. Liste les faits du texte d'origine (chiffres, noms, dates, promesses).
   La réécriture les garde tous et n'en ajoute aucun. Un fait qui manque pour
   bien écrire devient `{{à compléter}}`.
5. Réécris : ouverture de la voix, traits de la section 2, mots de la
   section 5, aucune expression de la section 6.
6. Contrôle :
   `python3 scripts/ecart.py tone-of-voice.md brouillon.txt`
   (`--adresse tutoiement` ou `--adresse vouvoiement` si la ligne du canal
   diffère de la voix générale). Corrige tout écart « fort ».
7. Rends le texte, puis en 3 lignes au plus : ce qui a changé et pourquoi.
   Pas d'autre commentaire.

## 2. Vérifier qu'un texte sonne juste

Deux parties, toujours séparées : ce qui se mesure, ce qui se juge.

**Mesuré** (`ecart.py`) : adresse, rythme, ponctuation, « ça » / « cela »,
formules administratives, mise en page, expressions interdites, marques
d'écriture IA. Verdict DANS LA VOIX, À RETOUCHER ou HORS VOIX, note sur 100.

**Jugé** (par toi) : chaque trait de la section 2, noté de 1 à 5, d'après le
test de résistance de rampstack (MIT) :

| Trait | Note | Passage qui le justifie |
|---|---|---|
| Concrète, pas technique | 4 | « Douze minutes. » |
| Franche, pas dure | 2 | l'erreur est annoncée en fin de texte |

Une note sous 3 : le texte est hors voix sur ce trait, propose la phrase
corrigée. Toutes les notes à 5 : sois plus exigeant, ou les traits sont trop
larges.

**Format de sortie** :

```
Verdict : À RETOUCHER (mesuré 78/100, trait « franche » à 2/5)
À corriger :
1. [fort] « n'hésitez pas » (section 6) → « Appelez-moi au … »
2. [trait] l'erreur arrive en dernier → la dire en première phrase
Version corrigée : …
```

## 3. Mettre à jour la voix

La personne ne modifie jamais le fichier. Trois cas :

| Ce qui arrive | Ce que tu fais |
|---|---|
| **Retour explicite** : « jamais ce mot », « sur WhatsApp je tutoie » | applique tout de suite, montre la ligne changée |
| **Version retouchée** : la personne colle le texte qu'elle a corrigé | compare avec ta version (voir ci-dessous), propose la règle, applique après « oui » |
| **Nouveaux textes** | relance `voix.py` sur l'ancien et le nouveau corpus, remplace le bloc de la section 12, dis ce qui a bougé (« phrases un peu plus longues : 8 → 10 mots ») |

**Apprendre d'une version retouchée** (idée de voice-learn, athola, MIT,
simplifiée) :

1. Liste chaque modification et range-la : ton adouci ou durci, ajout d'une
   tournure personnelle, coupe, précision (vague → chiffre), structure
   (ordre, paragraphes), mot remplacé.
2. Ne garde que ce qui ressemble à une règle (le même genre de retouche deux
   fois, ou une retouche que la personne explique).
3. Propose la règle en une phrase, avec la section où elle va :
   « Tu as remplacé “nos équipes” par “Inès et Théo” deux fois. Règle
   proposée (section 4) : nommer les personnes plutôt que “l'équipe”. On
   garde ? »
4. Une retouche qui contredit une règle existante : montre les deux, la
   personne tranche, le journal garde la raison.

Plus de 8 règles dans une section : propose d'en fusionner, une liste trop
longue est mal suivie.

**À chaque mise à jour** : version + 1, date d'en-tête, ligne de journal,
`profil.py verifier`, puis rends le fichier complet (ou, sur claude.ai et
ChatGPT, le fichier à recharger dans le Projet ou le ZIP « ma-voix » à
réimporter).
