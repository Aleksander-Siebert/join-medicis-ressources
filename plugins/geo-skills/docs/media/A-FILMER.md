# À filmer : les GIF du README GEO

Deux prises. Quand le fichier existe, il remplace dans `README.md` la
capture indiquée. Les captures SVG restent : elles sont régénérées par
`outils/visuels/capture.py`, pas les GIF.

## Réglages communs

- Fenêtre en 1280 × 720, police à 16 px au moins.
- Exemple fictif seulement : Assurly (assurly.example) et « Concurrent A ».
  Aucune vraie marque concurrente à l'écran.
- 10 à 20 secondes, sans temps mort.
- GIF de 760 px de large, 12 à 15 images par seconde, 8 Mo au plus.

```bash
ffmpeg -i prise.mp4 -vf "fps=12,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" -loop 0 demo.gif
```

## Prise 1 : `demo.gif` (en tête du README)

**Des réponses d'IA collées deviennent des taux avec leur marge.**

1. `/geo-visibilite` : montrer le portefeuille de questions proposé.
2. Coller les réponses (préparées à l'avance, exemple fictif).
3. Finir sur les taux par moteur, les questions perdues et les sources citées.

Remplace : `docs/media/capture-audit.svg` en tête de README.

## Prise 2 : `demo-acces.gif` (section « En images »)

**Qui peut lire le site, et pour en faire quoi ?**

1. `/geo-acces` sur un site de démonstration.
2. Montrer « citable dans ChatGPT : OAI-SearchBot » à côté de « GPTBot :
   entraînement », puis le robots.txt proposé selon la stratégie choisie.

Remplace : `docs/media/capture-acces.svg`.
