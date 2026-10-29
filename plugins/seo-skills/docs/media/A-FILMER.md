# À filmer : les GIF du README SEO

Deux prises. Chacune a déjà sa place dans `README.md`, en commentaire HTML :
quand le fichier existe, décommente la ligne et retire l'image qu'elle
remplace. Les captures SVG restent : elles sont régénérées par
`outils/visuels/capture.py`, pas les GIF.

## Réglages communs

- Fenêtre en 1280 × 720, police du terminal ou de l'éditeur à 16 px au moins.
- Exemple fictif seulement : Assurly (assurly.example). Aucun vrai site client,
  aucune donnée Search Console réelle à l'écran.
- 10 à 20 secondes, sans temps mort (coupe les attentes de réponse).
- GIF de 760 px de large, 12 à 15 images par seconde, 8 Mo au plus.

```bash
ffmpeg -i prise.mp4 -vf "fps=12,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" -loop 0 demo.gif
```

## Prise 1 : `demo.gif` (en tête du README)

**Du mot-clé au plan validé.**

1. Claude Code ouvert, `site-context.md` d'Assurly déjà rempli.
2. Taper `/seo-brief mutuelle indépendant`.
3. Montrer une question posée, la réponse, puis le plan avec la ligne
   « COUVERTURE 24/24 requêtes ».
4. Finir sur « Je rédige sur ce plan, ou tu veux changer quelque chose ? ».

Remplace : `docs/media/capture-controle.svg` en tête de README.

## Prise 2 : `demo-maillage.gif` (section « En images »)

**Le sitemap devient des clusters et des liens.**

1. `/seo-maillage` avec le sitemap d'un site de démonstration (pas un site
   client).
2. Montrer les clusters, une page orpheline, puis trois liens proposés avec
   leur ancre.
