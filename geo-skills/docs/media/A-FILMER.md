# À filmer : les GIF du README GEO

Deux prises. Chacune a déjà sa place dans `README.md`, en commentaire HTML :
quand le fichier existe, décommente la ligne et retire l'image qu'elle
remplace. Les captures SVG restent : elles sont régénérées par
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

**Des réponses d'IA collées deviennent un tableau.**

1. `/geo-visibilite` : montrer le portefeuille de questions proposé.
2. Coller les réponses (préparées à l'avance, exemple fictif).
3. Finir sur le tableau des taux avec leur marge d'erreur, les questions perdues et les sources citées.

Remplace : `docs/media/capture-visibilite.svg` en tête de README.

## Prise 2 : `demo-crawlers.gif` (section « En images »)

**Qui peut lire le site ?**

1. `/geo-crawlers` sur un site de démonstration.
2. Montrer les robots autorisés ou bloqués, un par un, puis le robots.txt
   proposé selon la stratégie choisie.
