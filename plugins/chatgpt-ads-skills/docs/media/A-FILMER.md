# À filmer : le GIF du README Ads

Une prise. Elle a déjà sa place dans `README.md`, en commentaire HTML : quand
le fichier existe, décommente la ligne et retire l'image qu'elle remplace.
Les captures SVG restent : elles sont régénérées par
`outils/visuels/capture.py`, pas le GIF.

## Réglages

- Fenêtre en 1280 × 720, police à 16 px au moins.
- Exemple fictif seulement : Vélora (velora.example) ou Plantéa
  (plantea.example), jamais un vrai annonceur.
- 15 à 25 secondes, sans temps mort (coupe les attentes de réponse).
- GIF de 760 px de large, 12 à 15 images par seconde, 8 Mo au plus.

```bash
ffmpeg -i prise.mp4 -vf "fps=12,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" -loop 0 demo.gif
```

## Prise 1 : `demo.gif` (en tête du README)

**Une page de destination devient une campagne contrôlée et un fichier d'import.**

1. Taper `/chatgpt-ads-skills` puis l'URL de la page de démonstration.
2. Montrer le tableau des allégations (une refusée).
3. Faire défiler la carte des intentions et un ad group avec ses 3 hints.
4. Finir sur « CAMPAGNE · PRÊT » et « Fichier écrit ».

Remplace : `docs/media/capture-corriger.svg` en tête de README.
