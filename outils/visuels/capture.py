#!/usr/bin/env python3
"""Captures de terminal en SVG, tirées des vraies sorties des scripts (Python 3, sans dépendance).

Les README des packs montrent ce que font les scripts. Pour que l'image ne
mente jamais, elle n'est pas dessinée : la commande est exécutée, et sa
sortie exacte devient un SVG (fenêtre de terminal, couleurs de Join Médicis).

  python3 outils/visuels/capture.py --manifeste linkedin-skills/docs/media/captures.json
      Exécute chaque commande du manifeste et écrit ses SVG.

  python3 outils/visuels/capture.py --manifeste … --verifier
      Exécute et compare aux SVG déjà écrits : code 1 si une capture ne
      correspond plus à la sortie réelle du script (à régénérer).

  python3 outils/visuels/capture.py --texte sortie.txt --titre "…" --commande "…" -o capture.svg
      Une capture à partir d'un texte déjà obtenu.

Manifeste (JSON) : {"captures": [{"id": "humaniseur", "titre": "linkedin-human · detect.py",
"dossier": ".", "commande": "python3 …", "lignes": [1, 30]}]}. « dossier » est
relatif au dossier du pack ; « lignes » (facultatif) garde un extrait, bornes
comprises, numérotées à partir de 1.
"""
import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

# Couleurs : fond encre, texte crème, accents vert forêt et or (charte Join Médicis).
FOND = "#141311"
BARRE = "#1F1E1B"
BORD = "#2A2925"
TEXTE = "#E8E1D5"
DISCRET = "#8E8C85"
VERT = "#6FC79B"
OR = "#D4B681"
ROUGE = "#E58A7B"
INVITE = "#B89253"

TAILLE = 14
INTERLIGNE = 20
CHASSE = 8.43  # largeur d'un caractère à 14 px dans les polices monospace courantes (0,6 em)
MARGE = 20
HAUT_BARRE = 34
COLONNES_MAX = 100
POLICE = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# Mots qui portent un verdict : colorés pour qu'on lise le résultat d'un coup d'œil.
VERDICTS = [
    (re.compile(r"\b(PRÊT|OK|SOLIDE|ANALYSÉ|SOUTENU|À JOUR|clé correcte|FIDÈLE)\b"), VERT),
    (re.compile(r"\b(SIGNALÉ|À AFFÛTER|ATTENTION|INCOMPLET|À REVOIR|ENCADRÉ|À CONFIRMER|NON SOUTENU|TROP PETIT|INFO)\b"), OR),
    (re.compile(r"\b(BLOQUANT|BLOQUÉ|À RÉÉCRIRE|FAIBLE|REFUSÉ|clé fausse|INUTILISABLE)\b"), ROUGE),
    (re.compile(r"[✖✗]"), ROUGE),
    (re.compile(r"[✔✓]"), VERT),
    (re.compile(r"^\s*!(?= )"), OR),
    (re.compile(r"#{2,}"), VERT),
    (re.compile(r"(?<=\[)#+(?=\.)"), VERT),
]


def couper(ligne, largeur=COLONNES_MAX):
    """Coupe une ligne trop longue en gardant l'indentation pour la suite."""
    if len(ligne) <= largeur:
        return [ligne]
    retrait = len(ligne) - len(ligne.lstrip()) + 2
    morceaux, reste = [], ligne
    while len(reste) > largeur:
        coupe = reste.rfind(" ", retrait + 10, largeur)
        if coupe <= retrait:
            coupe = largeur
        morceaux.append(reste[:coupe].rstrip())
        reste = " " * retrait + reste[coupe:].lstrip()
    morceaux.append(reste)
    return morceaux


def segments(ligne):
    """[(texte, couleur ou None)] : les verdicts en couleur, le reste en crème."""
    marques = []
    for motif, couleur in VERDICTS:
        for m in motif.finditer(ligne):
            if not any(a < m.end() and m.start() < b for a, b, _ in marques):
                marques.append((m.start(), m.end(), couleur))
    marques.sort()
    res, pos = [], 0
    for a, b, couleur in marques:
        if a > pos:
            res.append((ligne[pos:a], None))
        res.append((ligne[a:b], couleur))
        pos = b
    if pos < len(ligne):
        res.append((ligne[pos:], None))
    return res


def svg(texte, titre, commande):
    lignes = []
    for brute in texte.rstrip("\n").expandtabs(4).splitlines():
        lignes.extend(couper(brute.rstrip()))
    invite = f"$ {commande}"
    tout = couper(invite) + lignes
    colonnes = max([len(l) for l in tout] + [60])
    largeur = round(2 * MARGE + colonnes * CHASSE)
    hauteur = HAUT_BARRE + MARGE + len(tout) * INTERLIGNE + MARGE - 6
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}" height="{hauteur}" '
         f'viewBox="0 0 {largeur} {hauteur}" role="img" aria-label="{escape(titre, {chr(34): "&quot;"})}">',
         f'<title>{escape(titre)}</title>',
         f'<rect width="{largeur}" height="{hauteur}" rx="12" fill="{FOND}" stroke="{BORD}"/>',
         f'<path d="M0 12a12 12 0 0 1 12-12h{largeur - 24}a12 12 0 0 1 12 12v{HAUT_BARRE - 12}H0z" fill="{BARRE}"/>',
         f'<circle cx="22" cy="17" r="6" fill="#E58A7B"/><circle cx="42" cy="17" r="6" fill="#D4B681"/>'
         f'<circle cx="62" cy="17" r="6" fill="#6FC79B"/>',
         f'<text x="{largeur / 2:.0f}" y="22" text-anchor="middle" font-family="{POLICE}" font-size="12" '
         f'fill="{DISCRET}">{escape(titre)}</text>',
         f'<g font-family="{POLICE}" font-size="{TAILLE}" fill="{TEXTE}" xml:space="preserve">']
    y = HAUT_BARRE + MARGE + 4
    for i, ligne in enumerate(tout):
        if i < len(couper(invite)):
            corps = f'<tspan fill="{INVITE}">{escape(ligne[:2])}</tspan>{escape(ligne[2:])}' if i == 0 else escape(ligne)
        else:
            corps = "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' if c else escape(t) for t, c in segments(ligne))
        o.append(f'<text x="{MARGE}" y="{y}" xml:space="preserve" style="white-space:pre">{corps}</text>')
        y += INTERLIGNE
    o.append("</g></svg>")
    return "\n".join(o) + "\n"


def executer(entree, pack):
    dossier = (pack / entree.get("dossier", ".")).resolve()
    p = subprocess.run(shlex.split(entree["commande"]), cwd=dossier, capture_output=True, text=True,
                       env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin:/usr/local/bin", "LANG": "C.UTF-8"})
    sortie = p.stdout if p.stdout.strip() else p.stderr
    if not sortie.strip():
        raise RuntimeError(f"{entree['id']} : la commande n'a rien affiché (code {p.returncode})")
    if "lignes" in entree:
        a, b = entree["lignes"]
        sortie = "\n".join(sortie.splitlines()[a - 1:b])
    return sortie


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifeste", help="captures.json d'un pack (dans <pack>/docs/media/)")
    ap.add_argument("--verifier", action="store_true", help="comparer sans écrire ; code 1 si une capture a changé")
    ap.add_argument("--texte", help="fichier texte déjà obtenu (au lieu d'exécuter)")
    ap.add_argument("--titre", default="terminal")
    ap.add_argument("--commande", default="")
    ap.add_argument("-o", "--sortie")
    a = ap.parse_args(argv)

    if a.texte:
        if not a.sortie:
            ap.error("-o est requis avec --texte")
        Path(a.sortie).write_text(svg(Path(a.texte).read_text(encoding="utf-8"), a.titre, a.commande), encoding="utf-8")
        return 0
    if not a.manifeste:
        ap.error("--manifeste ou --texte")

    manifeste = Path(a.manifeste).resolve()
    media = manifeste.parent
    pack = media.parents[1]
    ecarts = 0
    for entree in json.loads(manifeste.read_text(encoding="utf-8"))["captures"]:
        cible = media / f"capture-{entree['id']}.svg"
        contenu = svg(executer(entree, pack), entree["titre"], entree.get("affiche", entree["commande"]))
        if a.verifier:
            if not cible.exists() or cible.read_text(encoding="utf-8") != contenu:
                print(f"  à régénérer : {cible.relative_to(pack)}")
                ecarts += 1
        else:
            cible.write_text(contenu, encoding="utf-8")
            print(f"  {cible.relative_to(pack)}")
    if a.verifier:
        print("captures à jour" if not ecarts else f"{ecarts} capture(s) ne correspondent plus aux scripts")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
