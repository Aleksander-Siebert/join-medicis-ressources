# À filmer : les GIF du README LinkedIn

Trois prises. Chacune a déjà sa place dans `README.md`, en commentaire HTML :
quand le fichier existe, décommente la ligne et retire l'image qu'elle
remplace. Les captures SVG restent : elles sont régénérées par
`outils/visuels/capture.py`, pas les GIF.

## Réglages communs

- Fenêtre en 1280 × 720, police du terminal ou de l'éditeur à 16 px au moins.
- Exemple fictif seulement : Assurly (assurly.example). Aucun vrai nom, aucun
  vrai compte, aucune notification visible.
- 10 à 20 secondes, sans temps mort (coupe les attentes de réponse).
- GIF de 760 px de large, 12 à 15 images par seconde, 8 Mo au plus.

Conversion d'une vidéo en GIF net (ffmpeg, palette optimisée) :

```bash
ffmpeg -i prise.mp4 -vf "fps=12,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" -loop 0 demo.gif
```

## Prise 1 : `demo.gif` (en tête du README)

**Ce qu'on doit comprendre en 15 secondes : une idée devient un post propre,
contrôlé, sans rien publier.**

1. Claude Code ouvert, `contexte.md` déjà rempli (exemple Assurly).
2. Taper : `/linkedin-post` puis l'idée en une phrase (« les 60 appels aux
   résiliés : la moitié parlait du délai, pas du prix »).
3. Laisser apparaître le post et le reçu « POST PRÊT » (note, longueur,
   heure proposée).
4. Finir sur la ligne « Réponds « ok » pour l'ajouter au journal ».

Remplace : `docs/media/capture-humaniseur.svg` en tête de README.

## Prise 2 : `demo-claude-ai.gif` (section « En images »)

**Installer sans terminal.**

1. claude.ai → Personnaliser → Skills → importer `linkedin-skills.zip`.
2. Un Projet avec `contexte.md` dans ses connaissances.
3. Taper « /linkedin-plan » et montrer la semaine proposée.

## Prise 3 : `demo-avant-apres.gif` (section « En images »)

**L'humaniseur, avant et après.**

1. Coller le brouillon de `evals/linkedin-human/brouillon-ia.txt` dans
   `/linkedin-human`.
2. Montrer le rapport (paragraphes à reprendre), puis la version réécrite.
3. Finir sur le score : 27,9 avant, 100 après (chiffres réels des fichiers de
   test, voir `evals/RESULTATS.md`).
