"""Construit les modèles de l'agent IA SEO pour Dust.

- agent-ia-seo-google-sheet.xlsx : les 5 onglets du Google Sheet partagé ;
- contexte-du-site.docx : le contexte du site, à ouvrir avec Google Docs,
  converti depuis contexte-du-site.md (source de vérité).

Dépendances (seulement pour reconstruire les fichiers) :
    python3 -m pip install openpyxl python-docx
Usage :
    python3 construire.py [dossier_de_sortie]
"""

import re
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

ICI = Path(__file__).resolve().parent

# Doit rester identique à SEO_SHEET_TABS (site, agent-ia-seo-dust.ts).
ONGLETS = [
    ("Sujets", ["sujet", "requêtes", "impressions", "meilleure position", "page qui ressort",
                "pourquoi", "date de détection", "statut", "raison"]),
    ("Pages", ["adresse", "titre", "groupe", "requête principale", "clics 28 jours", "mis à jour le"]),
    ("Articles", ["date", "sujet", "titre", "lien du Google Doc", "adresse publiée"]),
    ("Journal", ["date", "agent", "étape", "résultat"]),
    ("Consignes et retours", ["date", "agent", "règle", "exemple"]),
]
STATUTS = ["proposé", "retenu", "écrit", "abandonné"]
VERT = "0E3F2D"


def construire_sheet(sortie: Path) -> Path:
    wb = Workbook()
    wb.remove(wb.active)
    for nom, colonnes in ONGLETS:
        ws = wb.create_sheet(nom)
        ws.append(colonnes)
        for i, _ in enumerate(colonnes, start=1):
            c = ws.cell(row=1, column=i)
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor=VERT)
            c.alignment = Alignment(vertical="center", wrap_text=True)
            ws.column_dimensions[c.column_letter].width = 34 if colonnes[i - 1] in (
                "pourquoi", "résultat", "règle", "exemple", "requêtes", "titre", "raison") else 18
        ws.freeze_panes = "A2"
        if nom == "Sujets":
            dv = DataValidation(type="list", formula1='"' + ",".join(STATUTS) + '"', allow_blank=True)
            ws.add_data_validation(dv)
            dv.add("H2:H1000")
    chemin = sortie / "agent-ia-seo-google-sheet.xlsx"
    wb.save(chemin)
    return chemin


def _texte(par, ligne: str) -> None:
    """Ajoute une ligne Markdown simple : **gras** et *italique*."""
    for morceau in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", ligne):
        if not morceau:
            continue
        if morceau.startswith("**"):
            par.add_run(morceau[2:-2]).bold = True
        elif morceau.startswith("*"):
            r = par.add_run(morceau[1:-1])
            r.italic = True
            r.font.color.rgb = RGBColor(0x52, 0x50, 0x49)
        else:
            par.add_run(morceau)


def construire_docx(source: Path, sortie: Path) -> Path:
    doc = Document()
    doc.styles["Normal"].font.size = Pt(11)
    lignes = source.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lignes):
        l = lignes[i]
        if l.startswith("# "):
            doc.add_heading(l[2:], level=0)
        elif l.startswith("## "):
            doc.add_heading(l[3:], level=1)
        elif l.startswith("|"):
            bloc = []
            while i < len(lignes) and lignes[i].startswith("|"):
                if not re.match(r"^\|[-| ]+\|$", lignes[i]):
                    bloc.append([c.strip() for c in lignes[i].strip("|").split("|")])
                i += 1
            t = doc.add_table(rows=len(bloc), cols=len(bloc[0]))
            t.style = "Table Grid"
            for r, row in enumerate(bloc):
                for c, val in enumerate(row):
                    cell = t.cell(r, c)
                    cell.text = val
                    if r == 0:
                        cell.paragraphs[0].runs[0].bold = True
            continue
        elif l.startswith("- "):
            _texte(doc.add_paragraph(style="List Bullet"), l[2:])
        elif re.match(r"^\d+\. ", l):
            _texte(doc.add_paragraph(style="List Number"), re.sub(r"^\d+\. ", "", l))
        elif l.strip():
            _texte(doc.add_paragraph(), l)
        i += 1
    chemin = sortie / "contexte-du-site.docx"
    doc.save(chemin)
    return chemin


if __name__ == "__main__":
    sortie = Path(sys.argv[1]) if len(sys.argv) > 1 else ICI
    sortie.mkdir(parents=True, exist_ok=True)
    print(construire_sheet(sortie))
    print(construire_docx(ICI / "contexte-du-site.md", sortie))
