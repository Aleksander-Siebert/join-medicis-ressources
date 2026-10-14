# À filmer : le GIF du README Fondation

Une prise. Elle a déjà sa place dans `README.md`, en commentaire HTML : quand
le fichier existe, décommente la ligne et retire l'image qu'elle remplace.
Les captures SVG restent : elles sont régénérées par
`outils/visuels/capture.py`, pas le GIF.

## Réglages

- Fenêtre en 1280 × 720, police à 16 px au moins.
- Exemple fictif seulement : Assurly (assurly.example), numéros fictifs.
- 15 à 25 secondes, sans temps mort (coupe les attentes de réponse).
- GIF de 760 px de large, 12 à 15 images par seconde, 8 Mo au plus.

```bash
ffmpeg -i prise.mp4 -vf "fps=12,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" -loop 0 demo.gif
```

## Prise 1 : `demo.gif` (en tête du README)

**L'URL d'un site devient une fiche sourcée, montrée avant d'être enregistrée.**

1. Taper `/fondation-entreprise` puis l'URL du site de démonstration.
2. Montrer le résumé « J'ai lu 5 pages… », avec ce qui est déduit et ce qui
   n'a pas pu être lu.
3. Une question, une réponse.
4. Finir sur le bloc « ENTREPRISE · … » et « J'enregistre ce fichier ? ».

Remplace : `docs/media/capture-mentions.svg` en tête de README.
