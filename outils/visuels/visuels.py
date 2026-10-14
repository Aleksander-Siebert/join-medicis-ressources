#!/usr/bin/env python3
"""Icônes maison et bannière des README de Join Médicis (Python 3, sans dépendance).

Chaque pack décrit ses visuels dans <pack>/docs/media/visuels.json :

  {"pack": "LinkedIn Skills", "surtitre": "Join Médicis · pack de Skills",
   "accroche": "…", "puces": ["15 Skills", "247 tests", "MIT"],
   "familles": {"Écrire": "#B5552B", …},
   "icones": [{"nom": "linkedin-post", "glyphe": "plume", "famille": "Écrire"}, …],
   (« "a_venir": true » : Skill annoncé, estompé dans la bannière, sans tuile)
   "piliers": [{"nom": "garde-fou", "glyphe": "bouclier"}, …]}

  python3 outils/visuels/visuels.py linkedin-skills/docs/media/visuels.json
      Écrit icones/<nom>.svg (une tuile par Skill et par pilier) et banniere.svg.

  python3 outils/visuels/visuels.py … --verifier
      Code 1 si un SVG ne correspond plus au manifeste.

Les glyphes sont dessinés au trait sur une grille de 24 (style des icônes
d'interface), en crème sur une tuile de la couleur de la famille : lisibles
sur GitHub en thème clair comme sombre. Pas de police web dans les SVG : les
images d'un README ne peuvent pas en charger.
"""
import argparse
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

CREME = "#FAF7F2"
FORET = "#0E3F2D"
FORET_CLAIR = "#1F5B43"
OR = "#B89253"
OR_CLAIR = "#D4B681"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"

# Glyphes au trait, grille 24 × 24. « plein » : formes remplies (en plus du trait).
GLYPHES = {
    "boussole": {"trait": "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z", "plein": "M15.5 8.5 13.3 13.3 8.5 15.5 10.7 10.7z"},
    "micro": {"trait": "M12 3a3 3 0 0 0-3 3v5a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3z M6 11a6 6 0 0 0 12 0 M12 17v4 M9 21h6"},
    "carte": {"trait": "M5 5h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z "
                       "M9 9a2 2 0 1 0 0 4a2 2 0 1 0 0-4z M6 16.5c.7-1.6 1.7-2.2 3-2.2s2.3.6 3 2.2 M14.5 10h4 M14.5 13.5h3"},
    "batiment": {"trait": "M4 21V6l8-3v18 M12 9h8v12 M2 21h20 M7.5 8h1.5 M7.5 12h1.5 M7.5 16h1.5 M15.5 13h1.5 M15.5 17h1.5"},
    "plume": {"trait": "M20 3C12 4 7.5 9 6.5 18 M6.5 18 4 21 M9.5 14C14 13.2 18 9.5 20 3 M8 11h4.5"},
    "diapos": {"trait": "M8 4h11a1.5 1.5 0 0 1 1.5 1.5v9a1.5 1.5 0 0 1-1.5 1.5H8a1.5 1.5 0 0 1-1.5-1.5v-9A1.5 1.5 0 0 1 8 4z "
                        "M3.5 8v10a2 2 0 0 0 2 2h11"},
    "visage": {"trait": "M12 4a4 4 0 1 0 0 8a4 4 0 1 0 0-8z M4.5 20.5c1.2-4 4-6 7.5-6s6.3 2 7.5 6 M18.5 3.5v3 M17 5h3"},
    "bulle": {"trait": "M5 4h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-8l-5 4v-4H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z M8 9h8 M8 12h5"},
    "retour": {"trait": "M9.5 6.5 4 12l5.5 5.5 M4 12h10a6 6 0 0 1 6 6v1.5"},
    "avion": {"trait": "M21 3 3 10.5l7.5 3L13.5 21z M10.5 13.5 21 3"},
    "plateau": {"trait": "M3 13 6 5h12l3 8v6a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z M3 13h5l1.2 3h5.6l1.2-3h5"},
    "calendrier": {"trait": "M5 5h14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z M3 10h18 M8 3v4 M16 3v4",
                   "plein": "M7 13h2.5v2.5H7z M11 13h2.5v2.5H11z M7 17h2.5v2H7z"},
    "barres": {"trait": "M3 20h18 M6 20v-7 M11 20V5 M16 20v-10 M20 20v-4"},
    "recycler": {"trait": "M4.5 11a7.5 7.5 0 0 1 13.4-4.3 M18.5 3v4h-4 M19.5 13a7.5 7.5 0 0 1-13.4 4.3 M5.5 21v-4h4"},
    "mallette": {"trait": "M5 7h14a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2z "
                          "M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7 M3 13h18 M11 13v2h2v-2"},
    "bouclier": {"trait": "M12 3l7 3v5.5c0 4.6-3 8.1-7 9.5-4-1.4-7-4.9-7-9.5V6z M9 12l2 2 4-4.5"},
    "jauge": {"trait": "M4 17a8 8 0 1 1 16 0 M12 17l4-5.5 M7 17h.01 M17 17h.01 M12 9v.01"},
    "document": {"trait": "M7 3h7l5 5v12a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z M14 3v5h5 M9 12h7 M9 15h7 M9 18h4"},
    "loupe": {"trait": "M10.5 4a6.5 6.5 0 1 0 0 13a6.5 6.5 0 1 0 0-13z M15.3 15.3 20 20"},
    "plan": {"trait": "M4 5h16 M4 5v14h16 M8 9h9 M8 13h6 M8 17h8"},
    "lien": {"trait": "M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1 M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"},
    "arbre": {"trait": "M12 4v6 M12 10H6v4 M12 10h6v4 M12 10v4 M4 14h4v5H4z M10 14h4v5h-4z M16 14h4v5h-4z M10 2h4v3h-4z"},
    "epingle": {"trait": "M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0C18.5 14.8 12 21 12 21z M12 7.5a2.5 2.5 0 1 0 0 5a2.5 2.5 0 1 0 0-5z"},
    "etincelle": {"trait": "M12 3v4 M12 17v4 M3 12h4 M17 12h4 M12 9l1.2 1.8L15 12l-1.8 1.2L12 15l-1.2-1.8L9 12l1.8-1.2z"},
    "robot": {"trait": "M6 8h12a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2z M12 4v4 M9 13h.01 M15 13h.01 M9.5 16h5 M2 12v3 M22 12v3"},
    "code": {"trait": "M8.5 7 3.5 12l5 5 M15.5 7l5 5-5 5 M13.5 4.5l-3 15"},
    "citation": {"trait": "M5 11h4v6H4v-4c0-3 1.5-5 4-6 M14 11h4v6h-5v-4c0-3 1.5-5 4-6"},
    "cible": {"trait": "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z M12 7.5a4.5 4.5 0 1 0 0 9a4.5 4.5 0 1 0 0-9z", "plein": "M12 11a1 1 0 1 0 0 2a1 1 0 1 0 0-2z"},
    "rafraichir": {"trait": "M20 11a8 8 0 1 0-2.3 5.7 M20 4v7h-7"},
    "radar": {"trait": "M12 3a9 9 0 1 0 9 9 M12 7a5 5 0 1 0 5 5 M12 12l6.5-6.5"},
    "pellicule": {"trait": "M4 5h16v14H4z M4 9h16 M4 15h16 M8 5v4 M12 5v4 M16 5v4 M8 15v4 M12 15v4 M16 15v4"},
    "voix": {"trait": "M4 10v4 M8 7v10 M12 4v16 M16 8v8 M20 10v4"},
    "entreprise": {"trait": "M4 21V8l8-5 8 5v13 M2 21h20 M9 21v-6h6v6 M9 11h.01 M15 11h.01"},
    "personnes": {"trait": "M9 4a3.5 3.5 0 1 0 0 7a3.5 3.5 0 1 0 0-7z M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5 "
                           "M16 4.3a3.5 3.5 0 0 1 0 6.4 M18 14.8c1.8.8 3 2.5 3.5 5.2"},
    "sceau": {"trait": "M12 3a6 6 0 1 0 0 12a6 6 0 1 0 0-12z M9 14l-2 7 5-2.5 5 2.5-2-7 M10 9l1.5 1.5L14.5 7.5"},
}


def glyphe(nom, couleur=CREME, largeur_trait=1.8):
    g = GLYPHES[nom]
    o = f'<path d="{g["trait"]}" fill="none" stroke="{couleur}" stroke-width="{largeur_trait}" ' \
        f'stroke-linecap="round" stroke-linejoin="round"/>'
    if "plein" in g:
        o += f'<path d="{g["plein"]}" fill="{couleur}"/>'
    return o


def tuile(nom_glyphe, fond, taille=48, titre=""):
    t = f"<title>{escape(titre)}</title>" if titre else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{taille}" height="{taille}" viewBox="0 0 48 48" '
            f'role="img" aria-label="{escape(titre)}">{t}'
            f'<rect width="48" height="48" rx="12" fill="{fond}"/>'
            f'<rect x="0.5" y="0.5" width="47" height="47" rx="11.5" fill="none" stroke="#FFFFFF" stroke-opacity="0.12"/>'
            f'<g transform="translate(12 12)">{glyphe(nom_glyphe)}</g></svg>\n')


def banniere(m):
    L, H = 1280, 400
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{H}" viewBox="0 0 {L} {H}" role="img" '
         f'aria-label="{escape(m["pack"])}, par Join Médicis">',
         f'<title>{escape(m["pack"])}, par Join Médicis</title>',
         '<defs><radialGradient id="lueur" cx="0.18" cy="0.1" r="0.9">'
         f'<stop offset="0" stop-color="{FORET_CLAIR}"/><stop offset="1" stop-color="{FORET}"/></radialGradient></defs>',
         f'<rect width="{L}" height="{H}" rx="20" fill="url(#lueur)"/>',
         f'<rect x="18" y="18" width="{L - 36}" height="{H - 36}" rx="10" fill="none" stroke="{OR}" stroke-opacity="0.55"/>']
    # coins ornés
    for x, y, sx, sy in ((18, 18, 1, 1), (L - 18, 18, -1, 1), (18, H - 18, 1, -1), (L - 18, H - 18, -1, -1)):
        o.append(f'<path d="M{x + sx * 0} {y + sy * 34} V{y + sy * 10} Q{x} {y} {x + sx * 10} {y} H{x + sx * 34}" '
                 f'fill="none" stroke="{OR_CLAIR}" stroke-width="2.5" stroke-linecap="round"/>')
    o.append(f'<text x="72" y="104" font-family="{SANS}" font-size="16" font-weight="700" letter-spacing="3.2" '
             f'fill="{OR_CLAIR}">{escape(m["surtitre"].upper())}</text>')
    o.append(f'<text x="70" y="186" font-family="{SERIF}" font-size="76" fill="{CREME}">{escape(m["pack"])}</text>')
    y = 236
    for ligne in m["accroche"]:
        o.append(f'<text x="72" y="{y}" font-family="{SANS}" font-size="23" fill="{CREME}" fill-opacity="0.86">'
                 f'{escape(ligne)}</text>')
        y += 32
    x = 72
    for puce in m["puces"]:
        w = round(len(puce) * 9.2 + 30)
        o.append(f'<rect x="{x}" y="318" width="{w}" height="36" rx="18" fill="{CREME}" fill-opacity="0.1" '
                 f'stroke="{OR_CLAIR}" stroke-opacity="0.6"/>')
        o.append(f'<text x="{x + w / 2:.0f}" y="342" text-anchor="middle" font-family="{SANS}" font-size="16" '
                 f'font-weight="600" fill="{CREME}">{escape(puce)}</text>')
        x += w + 12
    # mosaïque des icônes à droite
    icones = m["icones"]
    cols = m.get("colonnes", 5)
    pas, cote = 72, 56
    rangs = (len(icones) + cols - 1) // cols
    x0 = L - 72 - (cols - 1) * pas - cote
    y0 = (H - ((rangs - 1) * pas + cote)) / 2
    for i, ic in enumerate(icones):
        cx, cy = x0 + (i % cols) * pas, y0 + (i // cols) * pas
        fond = m["familles"][ic["famille"]]
        opacite = ' opacity="0.35"' if ic.get("a_venir") else ""
        o.append(f'<g transform="translate({cx:.0f} {cy:.0f}) scale({cote / 48:.4f})"{opacite}>'
                 f'<rect width="48" height="48" rx="12" fill="{fond}"/>'
                 f'<rect x="0.5" y="0.5" width="47" height="47" rx="11.5" fill="none" stroke="#FFFFFF" stroke-opacity="0.16"/>'
                 f'<g transform="translate(12 12)">{glyphe(ic["glyphe"])}</g></g>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def fichiers(m):
    """{chemin relatif : contenu} pour tout ce que décrit le manifeste."""
    res = {}
    for ic in m["icones"]:
        if ic.get("a_venir"):
            continue  # Skill annoncé : estompé dans la bannière, pas encore de tuile
        res[f"icones/{ic['nom']}.svg"] = tuile(ic["glyphe"], m["familles"][ic["famille"]], titre=ic["nom"])
    for p in m.get("piliers", []):
        res[f"icones/{p['nom']}.svg"] = tuile(p["glyphe"], p.get("couleur", FORET), titre=p["nom"])
    res["banniere.svg"] = banniere(m)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifeste", help="<pack>/docs/media/visuels.json")
    ap.add_argument("--verifier", action="store_true")
    a = ap.parse_args(argv)
    chemin = Path(a.manifeste).resolve()
    m = json.loads(chemin.read_text(encoding="utf-8"))
    inconnus = [x["glyphe"] for x in m["icones"] + m.get("piliers", []) if x["glyphe"] not in GLYPHES]
    if inconnus:
        print("glyphes inconnus : " + ", ".join(inconnus), file=sys.stderr)
        return 1
    ecarts = 0
    for rel, contenu in fichiers(m).items():
        cible = chemin.parent / rel
        if a.verifier:
            if not cible.exists() or cible.read_text(encoding="utf-8") != contenu:
                print(f"  à régénérer : {rel}")
                ecarts += 1
        else:
            cible.parent.mkdir(parents=True, exist_ok=True)
            cible.write_text(contenu, encoding="utf-8")
    print(("visuels à jour" if not ecarts else f"{ecarts} visuel(s) à régénérer") if a.verifier
          else f"{len(fichiers(m))} visuels écrits dans {chemin.parent.name}/")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
