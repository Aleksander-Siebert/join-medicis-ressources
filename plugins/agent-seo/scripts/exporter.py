#!/usr/bin/env python3
"""
exporter.py : l'article Markdown devient un document Word (.docx).

Python 3.9+ sans dépendance : le fichier .docx est écrit à la main (c'est un ZIP
de quelques fichiers XML). Il s'ouvre dans Word, LibreOffice, Pages et Google
Docs.

Ce qui est rendu : titres (# à ####), paragraphes, gras, italique, liens
cliquables, listes à puces et numérotées, citations, tableaux, blocs de code,
lignes horizontales. Le reste passe en texte simple.

Utilisation :
  python3 scripts/exporter.py articles/2026-11-16-decennale/article.md
  python3 scripts/exporter.py article.md --sortie article.docx --titre "Assurance décennale"
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'


def x(t: str) -> str:
    """Texte protégé pour le XML, sans caractères de contrôle interdits."""
    t = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", t)
    return escape(t, {'"': "&quot;"})


class Document:
    def __init__(self):
        self.corps: list[str] = []
        self.liens: list[str] = []

    # ---------------------------------------------------------- texte en ligne

    def lien(self, url: str) -> str:
        self.liens.append(url)
        return f"rIdLien{len(self.liens)}"

    def runs(self, texte: str, base: str = "") -> str:
        """Gras **…**, italique *…* ou _…_, code `…`, liens [texte](url)."""
        sortie = []
        motif = re.compile(r"(\*\*(.+?)\*\*|__(.+?)__|\[([^\]]+)\]\(([^)\s]+)\)|`([^`]+)`|(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])|(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_]))")
        pos = 0
        for m in motif.finditer(texte):
            if m.start() > pos:
                sortie.append(self.run(texte[pos:m.start()], base))
            if m.group(2) or m.group(3):
                sortie.append(self.runs(m.group(2) or m.group(3), base + "<w:b/>"))
            elif m.group(4):
                rid = self.lien(m.group(5))
                texte_lien = self.runs(m.group(4), base + '<w:rStyle w:val="Lien"/>')
                sortie.append(f'<w:hyperlink r:id="{rid}">{texte_lien}</w:hyperlink>')
            elif m.group(6):
                sortie.append(self.run(m.group(6), base + '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'))
            else:
                sortie.append(self.runs(m.group(7) or m.group(8), base + "<w:i/>"))
            pos = m.end()
        if pos < len(texte):
            sortie.append(self.run(texte[pos:], base))
        return "".join(sortie)

    @staticmethod
    def run(texte: str, props: str = "") -> str:
        if not texte:
            return ""
        rpr = f"<w:rPr>{props}</w:rPr>" if props else ""
        return f'<w:r>{rpr}<w:t xml:space="preserve">{x(texte)}</w:t></w:r>'

    # ---------------------------------------------------------- blocs

    def paragraphe(self, texte: str, style: str | None = None, extra: str = "", brut: bool = False):
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/>{extra}</w:pPr>' if style else (f"<w:pPr>{extra}</w:pPr>" if extra else "")
        contenu = self.run(texte, '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/>') if brut else self.runs(texte)
        self.corps.append(f"<w:p>{ppr}{contenu}</w:p>")

    def liste(self, texte: str, numerotee: bool, niveau: int):
        num = 2 if numerotee else 1
        self.paragraphe(texte, "Liste", f'<w:numPr><w:ilvl w:val="{min(niveau, 2)}"/><w:numId w:val="{num}"/></w:numPr>')

    def tableau(self, lignes: list[list[str]]):
        cols = max(len(l) for l in lignes)
        xml = ['<w:tbl><w:tblPr><w:tblStyle w:val="Tableau"/><w:tblW w:w="5000" w:type="pct"/>'
               '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="BFBFBF"/><w:left w:val="single" w:sz="4" w:color="BFBFBF"/>'
               '<w:bottom w:val="single" w:sz="4" w:color="BFBFBF"/><w:right w:val="single" w:sz="4" w:color="BFBFBF"/>'
               '<w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/></w:tblBorders></w:tblPr>']
        xml.append("<w:tblGrid>" + "".join('<w:gridCol w:w="2000"/>' for _ in range(cols)) + "</w:tblGrid>")
        for i, l in enumerate(lignes):
            xml.append("<w:tr>")
            for c in l + [""] * (cols - len(l)):
                props = "<w:b/>" if i == 0 else ""
                xml.append(f'<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/></w:tcPr><w:p>{self.runs(c.strip(), props)}</w:p></w:tc>')
            xml.append("</w:tr>")
        xml.append("</w:tbl>")
        self.corps.append("".join(xml))
        self.corps.append("<w:p/>")

    # ---------------------------------------------------------- lecture du Markdown

    def depuis_markdown(self, md: str):
        md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)  # en-tête YAML éventuel
        lignes = md.splitlines()
        i, para = 0, []

        def vider():
            if para:
                self.paragraphe(" ".join(s.strip() for s in para))
                para.clear()

        while i < len(lignes):
            l = lignes[i]
            s = l.strip()
            if s.startswith("```"):
                vider()
                i += 1
                while i < len(lignes) and not lignes[i].strip().startswith("```"):
                    self.paragraphe(lignes[i], "Code", brut=True)
                    i += 1
                i += 1
                continue
            if not s:
                vider()
                i += 1
                continue
            m = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", s)
            if m:
                vider()
                n = len(m.group(1))
                self.paragraphe(m.group(2), "Titre" if n == 1 else f"Titre{min(n - 1, 3)}")
                i += 1
                continue
            if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
                vider()
                self.corps.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="BFBFBF"/></w:pBdr></w:pPr></w:p>')
                i += 1
                continue
            if s.startswith("|") and i + 1 < len(lignes) and re.match(r"^\|?\s*:?-{2,}", lignes[i + 1].strip()):
                vider()
                tab = []
                while i < len(lignes) and lignes[i].strip().startswith("|"):
                    cellules = [c for c in re.split(r"(?<!\\)\|", lignes[i].strip().strip("|"))]
                    if not re.match(r"^\s*:?-{2,}", cellules[0] if cellules else ""):
                        tab.append([c.replace("\\|", "|") for c in cellules])
                    i += 1
                self.tableau(tab)
                continue
            m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", l)
            if m:
                vider()
                niveau = len(m.group(1).replace("\t", "  ")) // 2
                self.liste(m.group(3), m.group(2)[0].isdigit(), niveau)
                i += 1
                continue
            if s.startswith(">"):
                vider()
                bloc = []
                while i < len(lignes) and lignes[i].strip().startswith(">"):
                    bloc.append(lignes[i].strip().lstrip(">").strip())
                    i += 1
                self.paragraphe(" ".join(bloc), "Citation")
                continue
            para.append(l)
            i += 1
        vider()

    # ---------------------------------------------------------- fichier

    def ecrire(self, chemin: Path, titre: str):
        maintenant = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rels_liens = "".join(
            f'<Relationship Id="rIdLien{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="{x(u)}" TargetMode="External"/>'
            for i, u in enumerate(self.liens, 1)
        )
        fichiers = {
            "[Content_Types].xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
            '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            "</Types>",
            "_rels/.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            "</Relationships>",
            "docProps/core.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f"<dc:title>{x(titre)}</dc:title><dc:creator>Agent SEO Join Médicis</dc:creator>"
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{maintenant}</dcterms:created></cp:coreProperties>',
            "word/_rels/document.xml.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
            f"{rels_liens}</Relationships>",
            "word/styles.xml": STYLES,
            "word/numbering.xml": NUMEROTATION,
            "word/document.xml": f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>'
            + "".join(self.corps)
            + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1418" w:right="1418" w:bottom="1418" w:left="1418" w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>'
            "</w:body></w:document>",
        }
        with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", fichiers.pop("[Content_Types].xml"))
            for nom, contenu in fichiers.items():
                z.writestr(nom, contenu)


def _style(id_, nom, taille, gras=False, couleur="000000", avant=0, apres=120, base="Normal", para=True):
    b = "<w:b/>" if gras else ""
    return (f'<w:style w:type="{"paragraph" if para else "character"}" w:styleId="{id_}"><w:name w:val="{nom}"/><w:basedOn w:val="{base}"/>'
            f'<w:pPr><w:keepNext/><w:spacing w:before="{avant}" w:after="{apres}"/></w:pPr>'
            f'<w:rPr>{b}<w:color w:val="{couleur}"/><w:sz w:val="{taille}"/></w:rPr></w:style>')


STYLES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f"<w:styles {W}>"
    '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="22"/><w:lang w:val="fr-FR"/></w:rPr></w:rPrDefault>'
    '<w:pPrDefault><w:pPr><w:spacing w:after="160" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
    + _style("Titre", "Title", 40, True, "1F3A2E", 0, 240)
    + _style("Titre1", "heading 1", 32, True, "1F3A2E", 360, 120)
    + _style("Titre2", "heading 2", 26, True, "1F3A2E", 240, 80)
    + _style("Titre3", "heading 3", 23, True, "404040", 200, 60)
    + '<w:style w:type="paragraph" w:styleId="Liste"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="60"/></w:pPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Citation"><w:name w:val="Quote"/><w:basedOn w:val="Normal"/>'
    '<w:pPr><w:ind w:left="567"/><w:pBdr><w:left w:val="single" w:sz="12" w:space="8" w:color="B88F45"/></w:pBdr></w:pPr><w:rPr><w:i/><w:color w:val="404040"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/>'
    '<w:pPr><w:spacing w:after="0"/><w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/></w:pPr></w:style>'
    '<w:style w:type="character" w:styleId="Lien"><w:name w:val="Hyperlink"/><w:rPr><w:color w:val="0E5B8C"/><w:u w:val="single"/></w:rPr></w:style>'
    '<w:style w:type="table" w:styleId="Tableau"><w:name w:val="Table Grid"/><w:tblPr><w:tblCellMar><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>'
    "</w:styles>"
)


def _niveaux(puces: bool) -> str:
    sortie = []
    for n in range(3):
        fmt, texte = ("bullet", "•–◦"[n]) if puces else ("decimal", f"%{n + 1}.")
        sortie.append(f'<w:lvl w:ilvl="{n}"><w:start w:val="1"/><w:numFmt w:val="{fmt}"/><w:lvlText w:val="{texte}"/>'
                      f'<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="{720 + 360 * n}" w:hanging="360"/></w:pPr></w:lvl>')
    return "".join(sortie)


NUMEROTATION = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f"<w:numbering {W}>"
    f'<w:abstractNum w:abstractNumId="1">{_niveaux(True)}</w:abstractNum>'
    f'<w:abstractNum w:abstractNumId="2">{_niveaux(False)}</w:abstractNum>'
    '<w:num w:numId="1"><w:abstractNumId w:val="1"/></w:num><w:num w:numId="2"><w:abstractNumId w:val="2"/></w:num>'
    "</w:numbering>"
)


def convertir(md: str, sortie: Path, titre: str | None = None) -> Path:
    d = Document()
    d.depuis_markdown(md)
    if not titre:
        m = re.search(r"^#\s+(.+)$", md, re.M)
        titre = m.group(1).strip() if m else sortie.stem
    d.ecrire(sortie, titre)
    return sortie


def main(argv: list[str] | None = None) -> int:
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Article Markdown vers document Word (.docx)")
    ap.add_argument("markdown")
    ap.add_argument("--sortie", help="chemin du .docx (par défaut : à côté du .md)")
    ap.add_argument("--titre", help="titre du document (par défaut : le premier titre #)")
    a = ap.parse_args(argv)
    src = Path(a.markdown)
    if not src.exists():
        print(f"Fichier introuvable : {src}", file=sys.stderr)
        return 1
    sortie = Path(a.sortie) if a.sortie else src.with_suffix(".docx")
    convertir(src.read_text("utf-8"), sortie, a.titre)
    print(f"Document Word prêt : {sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
