#!/usr/bin/env python3
"""construire_modele.py : écrit le modèle d'import du pack ChatGPT Ads (Python 3, sans dépendance).

Le modèle de Join Médicis reprend ce qu'un fichier d'import ChatGPT Ads doit
contenir pour être lu (3 onglets, noms de colonnes, ordre) et rien d'autre :
explications en français, mise en forme et contrôles de saisie sont les
nôtres. Pas de ligne d'exemple dans la zone de données (piège classique :
elle serait importée), l'exemple est écrit dans la ligne d'aide.

  python3 outils/construire_modele.py
      Écrit skills/chatgpt-ads-skills/assets/modele-import.xlsx.

  python3 outils/construire_modele.py --verifier
      Code 1 si le fichier publié ne correspond plus à ce script.

Les tests utilisent construire(..., prefixe="x:", exemple=True, langue="en")
pour imiter un modèle d'Ads Manager (préfixe XML, ligne d'exemple en
italique, lien hypertexte, libellés en anglais) sans redistribuer ce fichier.
"""
import argparse
import io
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

PACK = Path(__file__).resolve().parent.parent
SORTIE = PACK / "skills" / "chatgpt-ads-skills" / "assets" / "modele-import.xlsx"
DATE_FIXE = (2026, 10, 15, 0, 0, 0)          # dates des entrées du ZIP : fichier reproductible

# (colonne, statut FR, statut EN, aide, largeur)
ONGLETS = {
    "campaigns": [
        ("campaign_name", "Obligatoire", "Required",
         "Nom unique, lettres sans accent, chiffres, _ ou -. Ex. : velora_lancement_fr", 30),
        ("budget_max", "Obligatoire", "Required",
         "Montant dans la devise du compte, sans symbole. Ex. : 50", 14),
        ("budget_type", "Facultatif · Daily ou Lifetime", "Optional",
         "Daily conseillé : un budget total ne se rebascule pas en quotidien", 18),
        ("launch_date", "Facultatif · AAAA-MM-JJ", "Optional",
         "Date de lancement. Ex. : 2026-11-02", 14),
        ("end_date", "Facultatif · AAAA-MM-JJ", "Optional",
         "Date de fin, après le lancement", 14),
        ("objective", "Facultatif · Views, Clicks ou Conversions", "Optional",
         "Views : paiement aux 1 000 affichages ; Clicks : au clic ; Conversions : au clic, optimisé vers un événement", 22),
        ("conversion_event_setting_ids", "Obligatoire si objective = Conversions", "Required for conversion campaigns",
         "Un seul identifiant d'événement standard, en tableau JSON. Ex. : [\"ces_123\"]", 30),
        ("target_countries", "Facultatif · tableau JSON", "Optional",
         "Codes pays ISO à 2 lettres, ouverts dans Ads Manager. Ex. : [\"FR\",\"BE\"]", 22),
    ],
    "adgroups": [
        ("campaign_name", "Obligatoire", "Required",
         "Identique, caractère pour caractère, au nom de l'onglet campaigns", 30),
        ("adgroup_name", "Obligatoire", "Required",
         "Une intention par ad group. Nom unique sans accent. Ex. : batterie_occasion", 30),
        ("max_bid", "Obligatoire pour Clicks et Conversions", "Required for click and conversion campaigns",
         "Clicks : CPC maximum ; Conversions : coût par conversion visé ; Views : CPM maximum", 16),
        ("Context Hints", "Facultatif · tableau JSON", "Optional (no max)",
         "Situations où l'annonce aide, pas des mots-clés exacts. Ex. : [\"vérifier la batterie d'un vélo électrique d'occasion\"]", 60),
    ],
    "ads": [
        ("adgroup_name", "Obligatoire", "Required",
         "Identique au nom de l'onglet adgroups", 30),
        ("title", "Obligatoire · 24 caractères max", "Required - max 24 chars",
         "Titre : espaces et ponctuation comptent. Ex. : Et la batterie ?", 26),
        ("copy", "Obligatoire · 48 caractères max", "Required - max 48 chars",
         "Complète le titre sans le répéter. Ex. : Chaque batterie est testée avant la vente.", 50),
        ("link", "Obligatoire", "Required",
         "Page de destination https, UTM permis", 50),
        ("image_link", "Obligatoire", "Required",
         "Image carrée publique, PNG ou JPG, 640 à 1200 px de côté", 40),
    ],
}

EXEMPLE = {
    "campaigns": ["oaitestcmp1234567", 100, "Daily", 46062, 46092, "Clicks", "[]", "[\"US\"]"],
    "adgroups": ["oaitestcmp1234567", "oaitestadg9876543", 2, "[\"good\",\"json\"]"],
    "ads": ["oaitestadg9876543", "Example title", "Example copy for the ad", "https://example.com/", "https://example.com/i.png"],
}

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<{p}styleSheet xmlns{ns}="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<{p}numFmts count="1"><{p}numFmt numFmtId="164" formatCode="yyyy\\-mm\\-dd"/></{p}numFmts>
<{p}fonts count="5">
<{p}font><{p}sz val="11"/><{p}color rgb="FF1F1F1F"/><{p}name val="Calibri"/></{p}font>
<{p}font><{p}b/><{p}sz val="11"/><{p}color rgb="FFFAF7F2"/><{p}name val="Calibri"/></{p}font>
<{p}font><{p}b/><{p}sz val="10"/><{p}color rgb="FF0E3F2D"/><{p}name val="Calibri"/></{p}font>
<{p}font><{p}sz val="9"/><{p}color rgb="FF525049"/><{p}name val="Calibri"/></{p}font>
<{p}font><{p}i/><{p}sz val="11"/><{p}color rgb="FF1F1F1F"/><{p}name val="Calibri"/></{p}font>
</{p}fonts>
<{p}fills count="4">
<{p}fill><{p}patternFill patternType="none"/></{p}fill>
<{p}fill><{p}patternFill patternType="gray125"/></{p}fill>
<{p}fill><{p}patternFill patternType="solid"><{p}fgColor rgb="FF0E3F2D"/><{p}bgColor indexed="64"/></{p}patternFill></{p}fill>
<{p}fill><{p}patternFill patternType="solid"><{p}fgColor rgb="FFF3EBDD"/><{p}bgColor indexed="64"/></{p}patternFill></{p}fill>
</{p}fills>
<{p}borders count="1"><{p}border><{p}left/><{p}right/><{p}top/><{p}bottom/><{p}diagonal/></{p}border></{p}borders>
<{p}cellStyleXfs count="1"><{p}xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></{p}cellStyleXfs>
<{p}cellXfs count="6">
<{p}xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<{p}xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
<{p}xf numFmtId="0" fontId="2" fillId="3" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
<{p}xf numFmtId="0" fontId="3" fillId="3" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><{p}alignment vertical="top" wrapText="1"/></{p}xf>
<{p}xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
<{p}xf numFmtId="0" fontId="4" fillId="0" borderId="0" xfId="0" applyFont="1"/>
</{p}cellXfs>
<{p}cellStyles count="1"><{p}cellStyle name="Normal" xfId="0" builtinId="0"/></{p}cellStyles>
</{p}styleSheet>"""


def _col(i):
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]


def _cellule(p, ref, v, style):
    if isinstance(v, (int, float)):
        return f'<{p}c r="{ref}" s="{style}"><{p}v>{v}</{p}v></{p}c>'
    return f'<{p}c r="{ref}" s="{style}" t="inlineStr"><{p}is><{p}t xml:space="preserve">{escape(v)}</{p}t></{p}is></{p}c>'


def _feuille(nom, cols, p, ns, exemple, langue):
    lignes = []
    for num, (champ, style) in enumerate(((0, 1), (1, 2), (3, 3)), start=1):
        cells = []
        for i, c in enumerate(cols):
            texte = c[0] if champ == 0 else (c[1] if langue == "fr" else c[2]) if champ == 1 else c[3]
            cells.append(_cellule(p, f"{_col(i)}{num}", texte, style))
        hauteur = ' ht="48" customHeight="1"' if num == 3 else ""
        lignes.append(f'<{p}row r="{num}"{hauteur}>{"".join(cells)}</{p}row>')
    if exemple:
        cells = [_cellule(p, f"{_col(i)}4", v, 5) for i, v in enumerate(EXEMPLE[nom])]
        lignes.append(f'<{p}row r="4">{"".join(cells)}</{p}row>')
    largeurs = "".join(f'<{p}col min="{i + 1}" max="{i + 1}" width="{c[4]}" customWidth="1"/>' for i, c in enumerate(cols))
    validations = []
    if nom == "campaigns":
        validations.append(("C4:C2000", "list", '"Daily,Lifetime"', "Daily ou Lifetime"))
        validations.append(("F4:F2000", "list", '"Views,Clicks,Conversions"', "Views, Clicks ou Conversions"))
    if nom == "ads":
        validations.append(("B4:B5000", "textLength", "24", "24 caractères au plus"))
        validations.append(("C4:C5000", "textLength", "48", "48 caractères au plus"))
    dv = ""
    if validations:
        items = []
        for sqref, typ, f1, msg in validations:
            op = ' operator="lessThanOrEqual"' if typ == "textLength" else ""
            items.append(f'<{p}dataValidation type="{typ}"{op} allowBlank="1" showErrorMessage="1" '
                         f'errorTitle="Valeur refusée" error="{escape(msg)}" sqref="{sqref}">'
                         f'<{p}formula1>{escape(f1)}</{p}formula1></{p}dataValidation>')
        dv = f'<{p}dataValidations count="{len(items)}">{"".join(items)}</{p}dataValidations>'
    liens = f'<{p}hyperlinks><{p}hyperlink ref="D4" r:id="rId1"/></{p}hyperlinks>' if exemple and nom == "ads" else ""
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<{p}worksheet xmlns{ns}="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'<{p}sheetViews><{p}sheetView workbookViewId="0"><{p}pane ySplit="3" topLeftCell="A4" activePane="bottomLeft" state="frozen"/>'
            f'</{p}sheetView></{p}sheetViews><{p}cols>{largeurs}</{p}cols><{p}sheetData>{"".join(lignes)}</{p}sheetData>'
            f'{dv}{liens}<{p}pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/></{p}worksheet>')


def construire(sortie=SORTIE, prefixe="", exemple=False, langue="fr"):
    """Écrit le classeur ; renvoie ses octets."""
    p = prefixe
    ns = f":{prefixe[:-1]}" if prefixe else ""
    noms = list(ONGLETS)
    fichiers = {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
                      'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                      for i in range(1, 4))
            + '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            '</Types>'),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '</Relationships>'),
        "docProps/core.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<dc:title>Modèle d\'import ChatGPT Ads (Join Médicis)</dc:title>'
            '<dc:creator>Join Médicis, pack ChatGPT Ads (MIT)</dc:creator></cp:coreProperties>'),
        "xl/workbook.xml": (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<{p}workbook xmlns{ns}="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><{p}sheets>'
            + "".join(f'<{p}sheet name="{n}" sheetId="{i}" r:id="rId{i}"/>' for i, n in enumerate(noms, 1))
            + f'</{p}sheets></{p}workbook>'),
        "xl/_rels/workbook.xml.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                      f'Target="worksheets/sheet{i}.xml"/>' for i in range(1, 4))
            + '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '</Relationships>'),
        "xl/styles.xml": STYLES.format(p=p, ns=ns),
    }
    for i, n in enumerate(noms, 1):
        fichiers[f"xl/worksheets/sheet{i}.xml"] = _feuille(n, ONGLETS[n], p, ns, exemple, langue)
    if exemple:
        fichiers["xl/worksheets/_rels/sheet3.xml.rels"] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
            'Target="https://example.com/" TargetMode="External"/></Relationships>')
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, "w", zipfile.ZIP_DEFLATED) as z:
        for nom, contenu in fichiers.items():
            info = zipfile.ZipInfo(nom, DATE_FIXE)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, contenu.encode("utf-8"))
    octets = tampon.getvalue()
    if sortie:
        Path(sortie).write_bytes(octets)
    return octets


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--verifier", action="store_true", help="vérifier sans écrire")
    a = ap.parse_args()
    octets = construire(None)
    if a.verifier:
        if not SORTIE.exists() or SORTIE.read_bytes() != octets:
            print(f"{SORTIE.relative_to(PACK)} ne correspond plus : relancer outils/construire_modele.py")
            return 1
        print("Modèle d'import à jour.")
        return 0
    SORTIE.write_bytes(octets)
    print(f"Écrit : {SORTIE.relative_to(PACK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
