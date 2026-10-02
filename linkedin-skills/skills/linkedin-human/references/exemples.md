# Exemple complet : un post IA, avant et après

Fichiers : `evals/linkedin-human/brouillon-ia.txt` et
`brouillon-ia-reecrit.txt` (dépôt du pack). Sorties des scripts recopiées
telles quelles.

## Le brouillon

```
🚀 Et si je vous disais que la prospection LinkedIn n'est pas morte — elle a simplement changé ?

Dans un monde en constante évolution, il est important de noter que les décideurs sont submergés de messages. Ce n'est pas une question de volume, c'est une question de pertinence.

Le résultat ? Une véritable révolution dans notre approche.

Par ailleurs, nous avons mis en place une stratégie holistique. De plus, cette démarche constitue un levier crucial afin de répondre aux besoins de nos clients, témoignant de notre engagement.

✅ **Personnalisation :** chaque message est unique
✅ **Timing :** le bon moment, le bon canal
✅ **Suivi :** une relance intelligente et efficace

En somme, l'avenir s'annonce prometteur. Qu'en pensez-vous ?

#Prospection #LinkedIn #Growth #B2B #Sales #Marketing
```

## Passe 1 automatique (humanize.py)

Tiret cadratin → virgule, « il est important de noter que » supprimé,
« véritable » retiré, « afin de » → « pour », gras Markdown retiré. Le sens
n'a pas bougé (`fidelite.py` : FIDÈLE).

## Ce que detect.py demande de reprendre

```
SCORE HUMAIN  27.9   SIGNALÉ (se lit IA)
§1 (l.1) REMPLACER · 2 marqueur(s) : « 🚀 », « Et si je vous disais »
§2 (l.3) REMPLACER · 2 marqueur(s) : « Dans un monde en », « Ce n'est pas une question de volume, c'est »
§3 (l.5) REMPLACER · 1 marqueur(s) : « Le résultat ? »
§4 (l.7) RÉÉCRIRE LE PARAGRAPHE · 9 marqueur(s) : « Par ailleurs », « mis en place », « holistique »
§5 (l.9) RÉÉCRIRE LE PARAGRAPHE · 6 marqueur(s) : « ✅ », « **Personnalisation :** », « ✅ »
§6 (l.13) RÉÉCRIRE LE PARAGRAPHE · 3 marqueur(s) : « En somme », « l'avenir s'annonce », « Qu'en pensez-vous ? »
```

Le brouillon n'a **aucun fait** : pas un chiffre, pas un nom, pas une date. La
passe 3 ne peut rien ajouter sans l'utilisateur. Questions posées, une à une :

1. « Tes prospects reçoivent combien de messages par semaine, d'après eux ? »
   → 30 à 40, six décideurs interrogés.
2. « Qu'est-ce que vous avez changé, concrètement ? » → commenter un post de
   la personne avant de lui écrire, 20 minutes par jour.
3. « Avant, après : combien de réponses pour combien de messages ? » → 9 pour
   412 au trimestre précédent, 14 pour 60 sur le dernier.

## La réécriture

```
La prospection LinkedIn marche encore. Mais pas comme on la faisait en 2023.

Les décideurs qu'on vise reçoivent 30 à 40 messages par semaine. On l'a demandé à six d'entre eux. Aucun ne lit ceux qui commencent par « Je me permets ».

Alors on a changé une chose : on ne contacte plus personne sans avoir commenté un de ses posts avant. Ça nous coûte 20 minutes par jour.

Sur le dernier trimestre, 14 réponses pour 60 messages, contre 9 pour 412 au trimestre d'avant.

Vous commentez avant d'écrire, ou vous écrivez à froid ?

#Prospection #B2B
```

## Contrôle (passe 4)

```
detect.py avant après
  SCORE HUMAIN 100.0   OK (se lit humain)
  ÉCART  +72.1 points (SIGNALÉ -> OK)
  Garde anti-sur-correction : rien à signaler.

fidelite.py avant après
  FIDÉLITÉ : AJOUTS
  ✖ Ajouté : chiffres : 14, 20, 30, 40, 412, 60, 9 · dates : 2023 · citations : Je me permets
  ! Perdu : liens et mentions : #Growth, #LinkedIn, #Marketing, #Sales
```

Les ajouts sont **attendus et justifiés** : chaque chiffre vient des trois
réponses de l'utilisateur, ce que le reçu dit en toutes lettres. Les hashtags
perdus le sont par une règle (0 à 3). Sans ces réponses, la réécriture aurait
gardé `{{à compléter}}` à la place des chiffres, et `fidelite.py` aurait
bloqué tout chiffre apparu.

## Le reçu rendu à l'utilisateur

```
HUMANISEUR · niveau strict · 2026-10-02
Avant 27.9 SIGNALÉ → après 100.0 OK
Corrigé : 9 automatiques · 6 paragraphes réécrits
Laissé volontairement : la question de fin (elle est propre à ce post)
Fidélité : 7 chiffres et 1 date ajoutés, tous donnés par toi dans cette conversation ;
4 hashtags retirés (règle : 3 au plus)
À compléter : rien
```

Ce que la réécriture n'a pas fait : inventer « 3× plus de réponses », ajouter
« Honnêtement, on a galéré », couper chaque phrase en fragments, ni remplacer
« levier » par « catalyseur ».
