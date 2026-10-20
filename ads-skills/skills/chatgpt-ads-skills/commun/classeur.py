#!/usr/bin/env python3
"""classeur.py : le classeur d'annonces ChatGPT Ads au format « Schema » (Python 3, sans dépendance).

Socle commun du pack : lecture d'un XLSX ou d'un CSV, contrôle du format,
réparation sûre et écriture d'un classeur propre. Utilisé par
/chatgpt-ads-excel, /chatgpt-ads-skills, /chatgpt-ads-bulk, /chatgpt-ads-ids et
/chatgpt-ads-exports. Ne modifie jamais skills/<nom>/commun/ à la main :
modifier commun/ à la racine du pack, puis lancer outils/propager.py.

Le format (fourni par l'utilisateur le 20 oct. 2026, compatible avec Ads
Manager) : un seul onglet, une ligne d'en-tête, puis une annonce par ligne.

  ad_id | ad_group_id | adgroup_name | ad_name | status | title | copy | link | image_url | image_file_id

Ce qui n'est pas documenté publiquement est marqué « à vérifier » dans les
messages : le classeur fourni ne dit ni quelles colonnes sont obligatoires,
ni les limites de caractères qu'Ads Manager applique à ce format.
"""
import csv
from pathlib import Path
import io
import re
import unicodedata
import urllib.parse
import zipfile
from xml.sax.saxutils import escape

COLONNES = ["ad_id", "ad_group_id", "adgroup_name", "ad_name", "status", "title", "copy", "link",
            "image_url", "image_file_id"]
ONGLET = "Feuil1"            # nom de l'onglet du schéma fourni
BLOQUANT, ATTENTION, INFO = "BLOQUANT", "ATTENTION", "INFO"

# Limites de caractères. « import » : modèle d'import d'Ads Manager (titre 24, copie 48, relu le
# 15 oct. 2026). « api » : documentation développeur (titre 3 à 50, texte 100). Le pack écrit par
# défaut pour la plus stricte, qui passe partout.
LIMITES = {"import": {"title": 24, "copy": 48}, "api": {"title": 50, "copy": 100}}
TITRE_MIN, NOM_MIN, NOM_MAX, URL_MAX = 3, 3, 1000, 2048
STATUTS = ("active", "paused")
MAX_ANNONCES_COMPTE = 5000   # annonces actives ou en pause par compte (docs, Bulk API, relu le 20 oct. 2026)

# Préfixes des identifiants dans la documentation (exemples ad_123, adgrp_123, file_123) : un écart est
# signalé, pas bloqué, car le format réel n'est pas garanti.
PREFIXES = {"ad_id": "ad_", "ad_group_id": "adgrp_", "image_file_id": "file_"}

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⬀-⯿]")
INVISIBLES = re.compile("[​‌‍⁠﻿­]")


# ---------------------------------------------------------------- texte

def longueur(s):
    """Longueur affichée : caractères composés (é décomposé = 1), invisibles exclus."""
    return len(unicodedata.normalize("NFC", INVISIBLES.sub("", str(s or ""))))


def plier(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s.lower()).strip()


def texte(v):
    """Valeur de cellule en texte (un nombre entier lu 12.0 redevient « 12 »)."""
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


# ---------------------------------------------------------------- lecture XLSX

def _desechapper(s):
    return (s or "").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"') \
        .replace("&apos;", "'").replace("&#10;", "\n").replace("&#13;", "\r").replace("&amp;", "&")


def _col_index(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n


def _col_lettre(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _onglets(z):
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8-sig")
    cibles = {}
    for rel in re.findall(r"<(?:\w+:)?Relationship\b[^>]*>", rels):
        i, t = re.search(r'\bId="([^"]+)"', rel), re.search(r'\bTarget="([^"]+)"', rel)
        if i and t:
            cibles[i.group(1)] = t.group(1)
    res = []
    for balise in re.findall(r"<(?:\w+:)?sheet\b[^>]*>", wb):
        nom = re.search(r'\bname="([^"]*)"', balise)
        rid = re.search(r'\br:id="([^"]+)"|\bid="([^"]+)"', balise)
        etat = re.search(r'\bstate="([^"]+)"', balise)
        if not (nom and rid):
            continue
        cible = cibles.get(rid.group(1) or rid.group(2), "")
        cible = cible.lstrip("/")
        chemin = cible if cible.startswith("xl/") else "xl/" + cible
        res.append({"nom": _desechapper(nom.group(1)), "chemin": chemin,
                    "masque": bool(etat and etat.group(1) != "visible")})
    return res


def _styles_italiques(z):
    """Indices de style de cellule (cellXfs) dont la police est en italique."""
    if "xl/styles.xml" not in z.namelist():
        return set()
    st = z.read("xl/styles.xml").decode("utf-8")
    fonts = re.search(r"<(?:\w+:)?fonts\b[^>]*>(.*?)</(?:\w+:)?fonts>", st, re.S)
    polices = re.findall(r"<(?:\w+:)?font\b[^>]*?(?:/>|>(.*?)</(?:\w+:)?font>)", fonts.group(1) if fonts else "", re.S)
    italiques = {i for i, f in enumerate(polices) if re.search(r"<(?:\w+:)?i(?:\s+val=\"(?:1|true)\")?\s*/>", f or "")}
    xfs = re.search(r"<(?:\w+:)?cellXfs\b[^>]*>(.*?)</(?:\w+:)?cellXfs>", st, re.S)
    res = set()
    for i, xf in enumerate(re.findall(r"<(?:\w+:)?xf\b[^>]*>", xfs.group(1) if xfs else "")):
        f = re.search(r'\bfontId="(\d+)"', xf)
        if f and int(f.group(1)) in italiques:
            res.add(i)
    return res


def lire_xlsx(chemin):
    """Classeur brut : {"onglets": [{"nom", "masque", "lignes": {num: {col: cellule}}, "fusions"}]}.

    Une cellule : {"valeur", "type" (texte|nombre|booleen|erreur|vide), "formule", "italique"}.
    """
    with zipfile.ZipFile(chemin) as z:
        noms = z.namelist()
        partages = []
        if "xl/sharedStrings.xml" in noms:
            ss = z.read("xl/sharedStrings.xml").decode("utf-8")
            for si in re.findall(r"<(?:\w+:)?si>(.*?)</(?:\w+:)?si>", ss, re.S):
                si = re.sub(r"<(?:\w+:)?rPh\b.*?</(?:\w+:)?rPh>", "", si, flags=re.S)   # phonétique : à ignorer
                partages.append(_desechapper("".join(re.findall(r"<(?:\w+:)?t\b[^>]*>(.*?)</(?:\w+:)?t>", si, re.S))))
        italiques = _styles_italiques(z)
        res = {"onglets": []}
        for o in _onglets(z):
            if o["chemin"] not in noms:
                continue
            xml = z.read(o["chemin"]).decode("utf-8")
            lignes = {}
            for num, corps in re.findall(r'<(?:\w+:)?row\b[^>]*?\br="(\d+)"[^>]*?(?:/>|>(.*?)</(?:\w+:)?row>)', xml, re.S):
                cellules = {}
                for ref, attrs, contenu in re.findall(
                        r'<(?:\w+:)?c\b[^>]*?\br="([A-Z]+)\d+"([^>]*?)(?:/>|>(.*?)</(?:\w+:)?c>)', corps or "", re.S):
                    t = re.search(r'\bt="(\w+)"', attrs)
                    t = t.group(1) if t else "n"
                    s = re.search(r'\bs="(\d+)"', attrs)
                    f = re.search(r"<(?:\w+:)?f\b[^>]*?(?:/>|>(.*?)</(?:\w+:)?f>)", contenu or "", re.S)
                    v = re.search(r"<(?:\w+:)?v>(.*?)</(?:\w+:)?v>", contenu or "", re.S)
                    if t == "inlineStr":
                        val = _desechapper("".join(re.findall(r"<(?:\w+:)?t\b[^>]*>(.*?)</(?:\w+:)?t>", contenu or "", re.S)))
                        typ = "texte"
                    elif v is None:
                        val, typ = "", "vide"
                    elif t == "s":
                        val, typ = partages[int(v.group(1))], "texte"
                    elif t in ("str",):
                        val, typ = _desechapper(v.group(1)), "texte"
                    elif t == "b":
                        val, typ = v.group(1) == "1", "booleen"
                    elif t == "e":
                        val, typ = v.group(1), "erreur"
                    else:
                        brut = v.group(1)
                        try:
                            val = float(brut)
                        except ValueError:
                            val = brut
                        typ = "nombre"
                    cellules[_col_index(ref)] = {
                        "valeur": val, "type": typ, "formule": bool(f),
                        "italique": bool(s and int(s.group(1)) in italiques)}
                lignes[int(num)] = cellules
            fusions = re.findall(r'<(?:\w+:)?mergeCell\b[^>]*\bref="([^"]+)"', xml)
            res["onglets"].append({"nom": o["nom"], "masque": o["masque"], "lignes": lignes, "fusions": fusions})
    return res


def lire_csv(chemin):
    """Même structure que lire_xlsx, depuis un CSV (UTF-8, UTF-16 ; séparateur deviné)."""
    brut = Path(chemin).read_bytes()
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            contenu = brut.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        contenu = brut.decode("utf-8", "replace")
    try:
        dialecte = csv.Sniffer().sniff(contenu[:4096], delimiters=",;\t")
    except csv.Error:
        dialecte = csv.excel
    lignes = {}
    for i, rang in enumerate(csv.reader(io.StringIO(contenu), dialecte), 1):
        lignes[i] = {j: {"valeur": v, "type": "texte" if v != "" else "vide", "formule": False, "italique": False}
                     for j, v in enumerate(rang, 1)}
    return {"onglets": [{"nom": "csv", "masque": False, "lignes": lignes, "fusions": []}], "csv": True}


def lire(chemin):
    return lire_csv(chemin) if str(chemin).lower().endswith((".csv", ".tsv", ".txt")) else lire_xlsx(chemin)


def squelette(x):
    """En-tête réduit à ses lettres : « Ad Group ID », « ad_group_id » et « adgroupid » se rejoignent."""
    return re.sub(r"[\s_\-]", "", plier(x))


CANONIQUES = {squelette(c): c for c in COLONNES}


def onglet_annonces(classeur):
    """L'onglet qui porte les en-têtes du schéma (sinon le premier)."""
    for o in classeur["onglets"]:
        entetes = {plier(texte(c["valeur"])) for c in o["lignes"].get(1, {}).values()}
        if {"title", "copy", "link"} <= {CANONIQUES.get(squelette(e), e) for e in entetes}:
            return o
    return classeur["onglets"][0] if classeur["onglets"] else None


def annonces(classeur):
    """(entêtes lus, liste d'annonces {colonne: valeur, "_ligne": n, "_cellules": {...}})."""
    o = onglet_annonces(classeur)
    if not o:
        return [], []
    tete = o["lignes"].get(1, {})
    entetes = {j: CANONIQUES.get(squelette(texte(c["valeur"])), texte(c["valeur"]).strip()) for j, c in tete.items()}
    res = []
    for num in sorted(n for n in o["lignes"] if n > 1):
        cellules = o["lignes"][num]
        ligne = {"_ligne": num, "_cellules": {}}
        for j, cel in cellules.items():
            nom = entetes.get(j)
            if not nom:
                if texte(cel["valeur"]).strip():
                    ligne.setdefault("_hors_colonnes", []).append(_col_lettre(j))
                continue
            ligne[nom] = cel["valeur"]
            ligne["_cellules"][nom] = cel
        if any(texte(ligne.get(c, "")).strip() for c in COLONNES) or ligne.get("_hors_colonnes"):
            res.append(ligne)
    return [entetes[j] for j in sorted(entetes)], res


# ---------------------------------------------------------------- contrôle

class Rapport:
    def __init__(self):
        self.points = []

    def ajoute(self, niveau, ou, message, conseil=""):
        self.points.append({"niveau": niveau, "ou": ou, "message": message, "conseil": conseil})

    def compte(self, niveau):
        return sum(1 for p in self.points if p["niveau"] == niveau)

    def code(self):
        return 3 if self.compte(BLOQUANT) else 2 if self.compte(ATTENTION) else 0

    def texte(self, titre="Contrôle du classeur"):
        lignes = [f"{titre} : {self.compte(BLOQUANT)} bloquant(s), {self.compte(ATTENTION)} attention, "
                  f"{self.compte(INFO)} info"]
        for niveau in (BLOQUANT, ATTENTION, INFO):
            for p in self.points:
                if p["niveau"] == niveau:
                    lignes.append(f"[{niveau}] {p['ou']} : {p['message']}" + (f" → {p['conseil']}" if p["conseil"] else ""))
        return "\n".join(lignes)


def _url_ok(u):
    p = urllib.parse.urlsplit(u)
    return p.scheme in ("http", "https") and bool(p.netloc) and "." in p.netloc and not re.search(r"\s", u)


def verifier_structure(classeur, r):
    """Onglets, en-têtes, fusions : ce qui empêche Ads Manager de lire le fichier."""
    o = onglet_annonces(classeur)
    if not o:
        r.ajoute(BLOQUANT, "classeur", "aucun onglet lisible")
        return None
    if not classeur.get("csv"):
        autres = [x["nom"] for x in classeur["onglets"] if x is not o]
        if autres:
            r.ajoute(BLOQUANT, "classeur", f"onglets en trop : {', '.join(autres)}",
                     "le format n'a qu'un onglet ; « reparer » les retire")
        if o["masque"]:
            r.ajoute(BLOQUANT, "classeur", f"l'onglet « {o['nom']} » est masqué")
        if o["nom"] != ONGLET:
            r.ajoute(INFO, "classeur", f"onglet nommé « {o['nom']} » (schéma : « {ONGLET} »)",
                     "sans effet connu sur l'import [à vérifier] ; « reparer » reprend le nom du schéma")
    if o["fusions"]:
        r.ajoute(BLOQUANT, "classeur", f"cellules fusionnées : {', '.join(o['fusions'][:5])}", "les défusionner")
    tete = o["lignes"].get(1, {})
    lus = [texte(tete[j]["valeur"]).strip() if j in tete else "" for j in range(1, max(tete or {0: 0}) + 1)]
    while lus and not lus[-1]:
        lus.pop()
    if lus == COLONNES:
        return o
    manquantes = [c for c in COLONNES if c not in lus]
    en_trop = [c for c in lus if c and c not in COLONNES]
    proches = {c: x for x in en_trop for c in manquantes if squelette(x) == squelette(c)}
    for c, x in proches.items():
        r.ajoute(BLOQUANT, "ligne 1", f"en-tête « {x} » au lieu de « {c} »", "reprendre l'orthographe exacte du schéma")
    for c in manquantes:
        if c not in proches:
            r.ajoute(BLOQUANT, "ligne 1", f"colonne « {c} » absente", "les 10 colonnes du schéma sont attendues, même vides")
    for x in en_trop:
        if x not in proches.values():
            r.ajoute(BLOQUANT, "ligne 1", f"colonne « {x} » hors schéma", "la retirer (notes et sources vont ailleurs)")
    if not manquantes and not en_trop:
        r.ajoute(BLOQUANT, "ligne 1", "colonnes dans un autre ordre que le schéma",
                 "ordre attendu : " + " | ".join(COLONNES))
    if "" in lus:
        r.ajoute(BLOQUANT, "ligne 1", "en-tête vide entre deux colonnes")
    return o


def verifier_annonces(lignes, r, limites="import", en_ligne=None):
    """Contrôle ligne à ligne. `lignes` : dicts {colonne: valeur} (lecture ou JSON)."""
    lim = LIMITES[limites] if isinstance(limites, str) else limites
    if not lignes:
        r.ajoute(BLOQUANT, "classeur", "aucune annonce")
        return
    if len(lignes) > MAX_ANNONCES_COMPTE:
        r.ajoute(ATTENTION, "classeur", f"{len(lignes)} annonces : au-delà de {MAX_ANNONCES_COMPTE} par compte (docs)")
    groupe_nom, nom_groupe, paires, lignes_vues, noms_par_groupe, ids = {}, {}, {}, {}, {}, {}
    sans_statut, maj_statut, sans_id_groupe, sans_nom = [], [], [], []
    for i, a in enumerate(lignes):
        ou = f"ligne {a['_ligne']}" if "_ligne" in a else f"annonce {i + 1}"
        cel = a.get("_cellules", {})
        if a.get("_hors_colonnes"):
            r.ajoute(BLOQUANT, ou, f"valeur hors des colonnes du schéma (colonne {', '.join(a['_hors_colonnes'])})")
        for c in COLONNES:
            x = cel.get(c)
            if not x:
                continue
            if x["formule"]:
                r.ajoute(BLOQUANT, ou, f"{c} : formule", "coller la valeur seule (« reparer » le fait)")
            if x["type"] == "erreur":
                r.ajoute(BLOQUANT, ou, f"{c} : erreur Excel {x['valeur']}")
            if x["italique"]:
                r.ajoute(ATTENTION, ou, f"{c} : en italique", "texte normal attendu (« reparer » le fait)")
            if x["type"] == "nombre" and c in ("ad_id", "ad_group_id", "image_file_id", "ad_name", "adgroup_name"):
                r.ajoute(ATTENTION, ou, f"{c} : enregistré comme nombre", "Excel peut l'abîmer (zéros, notation 1E+15) : le stocker en texte")
        v = {c: texte(a.get(c, "")) for c in COLONNES}
        for c, x in v.items():
            if x != x.strip():
                r.ajoute(ATTENTION, ou, f"{c} : espace au début ou à la fin", "« reparer » les retire")
            if "\n" in x or "\r" in x:
                r.ajoute(BLOQUANT, ou, f"{c} : retour à la ligne dans la cellule")
            if INVISIBLES.search(x):
                r.ajoute(ATTENTION, ou, f"{c} : caractère invisible", "« reparer » le retire")
        v = {c: x.strip() for c, x in v.items()}
        # identifiants
        for c, pref in PREFIXES.items():
            if v[c] and not v[c].startswith(pref):
                r.ajoute(ATTENTION, ou, f"{c} « {v[c]} » ne commence pas par « {pref} »",
                         "copier l'identifiant depuis Ads Manager ou l'API (/chatgpt-ads-ids) ; format réel à vérifier")
            if v[c] and re.search(r"\s", v[c]):
                r.ajoute(BLOQUANT, ou, f"{c} contient un espace")
        if v["ad_id"]:
            if v["ad_id"] in ids:
                r.ajoute(BLOQUANT, ou, f"ad_id {v['ad_id']} déjà en {ids[v['ad_id']]}", "un identifiant d'annonce par ligne")
            ids[v["ad_id"]] = ou
        # groupe
        if not v["ad_group_id"] and not v["adgroup_name"]:
            r.ajoute(BLOQUANT, ou, "ni ad_group_id ni adgroup_name", "relier l'annonce à un ad group existant")
        elif not v["ad_group_id"]:
            sans_id_groupe.append(ou)
        elif not v["adgroup_name"]:
            r.ajoute(INFO, ou, "adgroup_name vide", "le remplir aide la relecture")
        if v["ad_group_id"] and v["adgroup_name"]:
            avant = groupe_nom.setdefault(v["ad_group_id"], v["adgroup_name"])
            if avant != v["adgroup_name"]:
                r.ajoute(BLOQUANT, ou, f"ad_group_id {v['ad_group_id']} porte deux noms : « {avant} » et « {v['adgroup_name']} »")
            autre = nom_groupe.setdefault(v["adgroup_name"], v["ad_group_id"])
            if autre != v["ad_group_id"]:
                r.ajoute(BLOQUANT, ou, f"adgroup_name « {v['adgroup_name']} » relié à deux identifiants : {autre} et {v['ad_group_id']}")
        # nom
        if not v["ad_name"]:
            sans_nom.append(ou)
        elif not (NOM_MIN <= len(v["ad_name"]) <= NOM_MAX):
            r.ajoute(BLOQUANT, ou, f"ad_name de {len(v['ad_name'])} caractère(s) : {NOM_MIN} à {NOM_MAX} (API)")
        else:
            g = v["ad_group_id"] or v["adgroup_name"]
            vu = noms_par_groupe.setdefault(g, {})
            if v["ad_name"] in vu:
                r.ajoute(ATTENTION, ou, f"ad_name « {v['ad_name']} » déjà utilisé dans ce groupe ({vu[v['ad_name']]})",
                         "un nom par annonce facilite le suivi")
            vu.setdefault(v["ad_name"], ou)
        # statut
        if not v["status"]:
            sans_statut.append(ou)
        elif v["status"] not in STATUTS:
            if v["status"].lower() in STATUTS:
                maj_statut.append(ou)
            else:
                r.ajoute(BLOQUANT, ou, f"status « {v['status']} » : active ou paused")
        elif v["status"] == "active":
            r.ajoute(INFO, ou, "status active : l'annonce peut diffuser dès son approbation",
                     "paused conseillé pour relire dans Ads Manager avant de lancer")
        # textes
        for c, mini in (("title", TITRE_MIN), ("copy", 1)):
            n = longueur(v[c])
            if not v[c]:
                r.ajoute(BLOQUANT, ou, f"{c} vide")
            elif n > lim[c]:
                r.ajoute(BLOQUANT, ou, f"{c} : {n} caractères pour {lim[c]} au plus", f"« {v[c]} »")
            elif n < mini:
                r.ajoute(BLOQUANT, ou, f"{c} : {n} caractère(s), {mini} au moins")
            if EMOJI.search(v[c]):
                r.ajoute(ATTENTION, ou, f"{c} : emoji", "rendu et acceptation non garantis [à vérifier]")
            if "  " in v[c]:
                r.ajoute(ATTENTION, ou, f"{c} : double espace")
        if v["title"] and v["copy"]:
            if plier(v["title"]) == plier(v["copy"]):
                r.ajoute(ATTENTION, ou, "title et copy identiques", "la copie doit compléter le titre")
            cle = (plier(v["title"]), plier(v["copy"]))
            if cle in paires:
                r.ajoute(ATTENTION, ou, f"même titre et même copie qu'en {paires[cle]}")
            paires.setdefault(cle, ou)
        # liens
        if not v["link"]:
            r.ajoute(BLOQUANT, ou, "link vide")
        elif not _url_ok(v["link"]):
            r.ajoute(BLOQUANT, ou, f"link « {v['link']} » : adresse http(s) complète attendue")
        elif len(v["link"]) > URL_MAX:
            r.ajoute(BLOQUANT, ou, f"link de {len(v['link'])} caractères : {URL_MAX} au plus")
        elif v["link"].startswith("http://"):
            r.ajoute(ATTENTION, ou, "link en http", "préférer https")
        if not v["image_url"] and not v["image_file_id"]:
            r.ajoute(BLOQUANT, ou, "ni image_url ni image_file_id", "une image par annonce")
        if v["image_url"]:
            if not _url_ok(v["image_url"]):
                r.ajoute(BLOQUANT, ou, f"image_url « {v['image_url']} » : adresse http(s) complète attendue")
            elif not re.search(r"\.(png|jpe?g|webp)$", urllib.parse.urlsplit(v["image_url"]).path, re.I):
                r.ajoute(ATTENTION, ou, "image_url sans extension .png, .jpg ou .webp",
                         "lien direct vers l'image attendu, pas une page")
        lignes_vues.setdefault(tuple(v[c] for c in COLONNES), ou)
    def liste(x):
        return ", ".join(x[:3]) + (" …" if len(x) > 3 else "")
    if sans_id_groupe:
        r.ajoute(ATTENTION, liste(sans_id_groupe), f"ad_group_id vide sur {len(sans_id_groupe)} ligne(s)",
                 "l'annonce doit rejoindre un ad group existant : récupérer son identifiant (/chatgpt-ads-ids) "
                 "[à vérifier : obligatoire ou non]")
    if sans_nom:
        r.ajoute(ATTENTION, liste(sans_nom), f"ad_name vide sur {len(sans_nom)} ligne(s)",
                 "« reparer » le remplit (nom du groupe + numéro) [à vérifier : obligatoire ou non]")
    if sans_statut:
        r.ajoute(ATTENTION, ", ".join(sans_statut[:3]) + (" …" if len(sans_statut) > 3 else ""),
                 f"status vide sur {len(sans_statut)} ligne(s)", "« reparer » écrit paused")
    if maj_statut:
        r.ajoute(ATTENTION, ", ".join(maj_statut[:3]) + (" …" if len(maj_statut) > 3 else ""),
                 f"status avec majuscules sur {len(maj_statut)} ligne(s)", "minuscules attendues : « reparer » corrige")
    doublons = len(lignes) - len(lignes_vues)
    if doublons:
        r.ajoute(BLOQUANT, "classeur", f"{doublons} ligne(s) en double exact", "« reparer » les retire")
    if en_ligne:
        en_ligne(lignes, r)


def verifier(chemin, limites="import", en_ligne=None):
    r = Rapport()
    try:
        cl = lire(chemin)
    except (zipfile.BadZipFile, KeyError) as e:
        r.ajoute(BLOQUANT, "classeur", f"fichier illisible comme XLSX ({e})", "réenregistrer depuis Excel au format .xlsx")
        return r, None, []
    o = verifier_structure(cl, r)
    _, lignes = annonces(cl)
    verifier_annonces(lignes, r, limites, en_ligne)
    return r, cl, lignes


# ---------------------------------------------------------------- contrôle en ligne (facultatif)

def dimensions_image(octets):
    """(format, largeur, hauteur) d'un PNG, JPEG ou WebP, depuis ses premiers octets ; None si inconnu."""
    b = octets
    if b[:8] == b"\x89PNG\r\n\x1a\n" and len(b) >= 24:
        return "png", int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big")
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP" and len(b) >= 30:
        bloc = b[12:16]
        if bloc == b"VP8X":
            return "webp", 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
        if bloc == b"VP8 ":
            return "webp", int.from_bytes(b[26:28], "little") & 0x3FFF, int.from_bytes(b[28:30], "little") & 0x3FFF
        if bloc == b"VP8L":
            x = int.from_bytes(b[21:25], "little")
            return "webp", (x & 0x3FFF) + 1, ((x >> 14) & 0x3FFF) + 1
    if b[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(b):
            if b[i] != 0xFF:
                i += 1
                continue
            marque = b[i + 1]
            if marque in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                return "jpeg", int.from_bytes(b[i + 7:i + 9], "big"), int.from_bytes(b[i + 5:i + 7], "big")
            if marque in (0xD8, 0x01) or 0xD0 <= marque <= 0xD7:
                i += 2
                continue
            i += 2 + int.from_bytes(b[i + 2:i + 4], "big")
    return None


def controle_en_ligne(lignes, r, delai=10, lire_url=None):
    """Ouvre chaque lien et chaque image une fois. `lire_url(url)` → (code, type, octets) ; remplaçable en test."""
    import urllib.request

    def defaut(url):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; join-medicis-ads-check)",
                                                   "Range": "bytes=0-262143"})
        try:
            with urllib.request.urlopen(req, timeout=delai) as rep:
                return rep.status, rep.headers.get("Content-Type", ""), rep.read(262144)
        except urllib.error.HTTPError as e:
            return e.code, "", b""
        except Exception as e:  # réseau, DNS, TLS : signalé, pas fatal
            return None, str(e)[:80], b""

    lire_url = lire_url or defaut
    cache = {}
    for i, a in enumerate(lignes):
        ou = f"ligne {a['_ligne']}" if "_ligne" in a else f"annonce {i + 1}"
        lien, image = texte(a.get("link", "")).strip(), texte(a.get("image_url", "")).strip()
        if lien and _url_ok(lien):
            if lien not in cache:
                cache[lien] = lire_url(lien)
            code, typ, _ = cache[lien]
            if code is None:
                r.ajoute(ATTENTION, ou, f"link injoignable ({typ})", "l'ouvrir dans un navigateur ; OpenAI doit pouvoir le lire aussi")
            elif code >= 400:
                r.ajoute(BLOQUANT if code in (404, 410) else ATTENTION, ou, f"link répond {code}",
                         "page introuvable ou bloquée pour les robots : OpenAI refuse une page qu'il ne peut pas vérifier")
        if image and _url_ok(image):
            if image not in cache:
                cache[image] = lire_url(image)
            code, typ, octets = cache[image]
            if code is None or code >= 400:
                r.ajoute(BLOQUANT, ou, f"image_url {'injoignable' if code is None else 'répond ' + str(code)}")
                continue
            dim = dimensions_image(octets)
            if not dim:
                r.ajoute(ATTENTION, ou, f"image_url : format non reconnu ({typ or 'type inconnu'})",
                         "PNG, JPG ou WebP en lien direct attendu")
                continue
            fmt, l, h = dim
            if l != h:
                r.ajoute(BLOQUANT, ou, f"image {l} × {h} : carrée attendue")
            if min(l, h) < 640:
                r.ajoute(BLOQUANT, ou, f"image {l} × {h} : 640 × 640 au moins")
            if max(l, h) > 1200:
                r.ajoute(ATTENTION, ou, f"image {l} × {h} : le modèle d'import d'Ads Manager indique 1 200 × 1 200 au plus")
            if fmt == "webp":
                r.ajoute(INFO, ou, "image WebP : acceptée par l'API, le modèle d'import ne cite que PNG et JPG")


# ---------------------------------------------------------------- réparation sûre

def reparer_lignes(lignes):
    """Corrections sans changer le sens : espaces, invisibles, statut, noms vides, doublons exacts.

    Ne raccourcit jamais un titre ni une copie : un dépassement reste à corriger par une personne.
    """
    sortie, vus, journal, compteurs = [], set(), [], {}
    for a in lignes:
        ou = f"ligne {a['_ligne']}" if "_ligne" in a else "annonce"
        v = {}
        for c in COLONNES:
            x = texte(a.get(c, ""))
            y = INVISIBLES.sub("", x).strip()
            if c not in ("title", "copy"):
                y = re.sub(r"\s+", " ", y)
            if y != x:
                journal.append(f"{ou} : {c} nettoyé (espaces ou caractères invisibles)")
            v[c] = y
        if v["status"].lower() in STATUTS and v["status"] != v["status"].lower():
            v["status"] = v["status"].lower()
            journal.append(f"{ou} : status mis en minuscules")
        if not v["status"]:
            v["status"] = "paused"
            journal.append(f"{ou} : status vide → paused")
        groupe = v["adgroup_name"] or v["ad_group_id"] or "annonce"
        compteurs[groupe] = compteurs.get(groupe, 0) + 1
        if not v["ad_name"]:
            v["ad_name"] = f"{groupe}-{compteurs[groupe]:02d}"
            journal.append(f"{ou} : ad_name vide → {v['ad_name']}")
        cle = tuple(v[c] for c in COLONNES)
        if cle in vus:
            journal.append(f"{ou} : doublon exact retiré")
            continue
        vus.add(cle)
        sortie.append(v)
    return sortie, journal


# ---------------------------------------------------------------- écriture

def ecrire_xlsx(chemin, lignes, onglet=ONGLET):
    """Classeur propre au format du schéma : un onglet, en-têtes, valeurs en texte, sans italique ni métadonnées."""
    chaines, index = [], {}

    def ss(s):
        if s not in index:
            index[s] = len(chaines)
            chaines.append(s)
        return index[s]

    def ligne_xml(num, valeurs):
        cellules = []
        for j, val in enumerate(valeurs, 1):
            if val == "":
                continue
            cellules.append(f'<c r="{_col_lettre(j)}{num}" t="s"><v>{ss(val)}</v></c>')
        return f'<row r="{num}">{"".join(cellules)}</row>'

    rangs = [ligne_xml(1, COLONNES)]
    for n, a in enumerate(lignes, 2):
        rangs.append(ligne_xml(n, [texte(a.get(c, "")) for c in COLONNES]))
    der = _col_lettre(len(COLONNES)) + str(max(1, len(lignes) + 1))
    feuille = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
               '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
               'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
               f'<dimension ref="A1:{der}"/><sheetViews><sheetView workbookViewId="0">'
               '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
               '<sheetFormatPr defaultRowHeight="15"/>'
               '<cols><col min="1" max="4" width="18" customWidth="1"/><col min="5" max="5" width="10" customWidth="1"/>'
               '<col min="6" max="6" width="28" customWidth="1"/><col min="7" max="7" width="52" customWidth="1"/>'
               '<col min="8" max="10" width="40" customWidth="1"/></cols>'
               f'<sheetData>{"".join(rangs)}</sheetData>'
               '<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/></worksheet>')
    sst = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           f'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(chaines)}" '
           f'uniqueCount="{len(chaines)}">'
           + "".join(f'<si><t xml:space="preserve">{escape(s)}</t></si>' for s in chaines) + "</sst>")
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
              '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<fonts count="1"><font><sz val="11"/><color theme="1"/><name val="Calibri"/><family val="2"/>'
              '<scheme val="minor"/></font></fonts>'
              '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
              '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
              '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>')
    classeur = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                f'<sheets><sheet name="{escape(onglet)}" sheetId="1" r:id="rId1"/></sheets></workbook>')
    rels_wb = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
               '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
               '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
               '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
               '</Relationships>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>')
    types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
             '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
             '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
             '<Default Extension="xml" ContentType="application/xml"/>'
             '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
             '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
             '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
             '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
             '</Types>')
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", types)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", classeur)
        z.writestr("xl/_rels/workbook.xml.rels", rels_wb)
        z.writestr("xl/worksheets/sheet1.xml", feuille)
        z.writestr("xl/styles.xml", styles)
        z.writestr("xl/sharedStrings.xml", sst)


def tableau_a_coller(lignes):
    """Repli sans fichier : en-têtes et lignes séparés par des tabulations."""
    sortie = ["\t".join(COLONNES)]
    for a in lignes:
        sortie.append("\t".join(texte(a.get(c, "")).replace("\t", " ") for c in COLONNES))
    return "\n".join(sortie)
