#!/usr/bin/env python3
"""meta.py : title et meta description, mesurés en pixels et contrôlés.

Google ne fixe aucune limite de longueur : il tronque le lien de titre et
l'extrait selon la largeur de l'appareil, et réécrit souvent les titles
(documentation Search Central, title-link maj 10 déc. 2025, snippet maj
20 avr. 2026). Ce script estime donc la **largeur en pixels** (police Arial,
20 px pour le title, 14 px pour la description) et la compare à des repères
de praticiens (title ≈ 600 px ; description ≈ 920 px sur ordinateur,
≈ 680 px sur mobile). Ce sont des estimations, pas des règles Google.

Contrôles d'une page : largeur, mot-clé au début, marque, année dépassée,
description qui recopie le title, liste de mots-clés, typographie française.
Contrôles d'un lot (--lot) : titles ou descriptions en double, gabarit
répété, même formule de fin sur beaucoup de pages.

Codes de sortie : 0 rien à revoir · 2 à revoir · 1 erreur d'utilisation.

Exemples :
  python3 meta.py --title "Mutuelle indépendant : comment la choisir | Assurly" \\
                  --description "…" --mot-cle "mutuelle indépendant" --marque Assurly
  python3 meta.py --lot pages.csv          (colonnes url,title,description)
  python3 meta.py --lot pages.json --json  (liste de {url, title, description})
"""

import argparse
import csv
import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path

ICI = Path(__file__).resolve().parent
for _c in (ICI, ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (_c / "texte_fr.py").exists():
        sys.path.insert(0, str(_c))
        break
import texte_fr as tf  # noqa: E402

# Largeurs Arial (Helvetica) en millièmes de cadratin.
_LARG = {
    " ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667, "'": 191, "(": 333, ")": 333,
    "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278, ":": 278, ";": 278, "<": 584, "=": 584,
    ">": 584, "?": 556, "@": 1015, "[": 278, "]": 278, "_": 556, "|": 260, "«": 556, "»": 556, "’": 222,
    "€": 556, "–": 556, "—": 1000, "…": 1000, "°": 400, "·": 278, " ": 278, " ": 278,
    "A": 667, "B": 667, "C": 722, "D": 722, "E": 667, "F": 611, "G": 778, "H": 722, "I": 278, "J": 500,
    "K": 667, "L": 556, "M": 833, "N": 722, "O": 778, "P": 667, "Q": 778, "R": 722, "S": 667, "T": 611,
    "U": 722, "V": 667, "W": 944, "X": 667, "Y": 667, "Z": 611,
    "a": 556, "b": 556, "c": 500, "d": 556, "e": 556, "f": 278, "g": 556, "h": 556, "i": 222, "j": 222,
    "k": 500, "l": 222, "m": 833, "n": 556, "o": 556, "p": 556, "q": 556, "r": 333, "s": 500, "t": 278,
    "u": 556, "v": 500, "w": 722, "x": 500, "y": 500, "z": 500, "œ": 944, "æ": 889, "Œ": 1000, "Æ": 1000,
}
for _d in "0123456789":
    _LARG[_d] = 556

TITLE_PX, TITLE_TAILLE = 600, 20
DESC_PX_ORDI, DESC_PX_MOBILE, DESC_TAILLE = 920, 680, 14

CTA_FIN = re.compile(r"(d[ée]couvrez[^.!?]*|en savoir plus|cliquez ici|contactez[- ]nous|demandez (?:un|votre) devis"
                     r"|essayez gratuitement|profitez[^.!?]*|lisez la suite)\s*[.!]*\s*$", re.I)


def largeur(texte, taille):
    """Largeur estimée en pixels (accents mesurés comme la lettre de base)."""
    total = 0
    for c in texte:
        base = tf.fold(c) if c not in _LARG else c
        if c.isupper() and c not in _LARG:
            base = tf.fold(c).upper()
        total += _LARG.get(c, _LARG.get(base[:1] if base else c, 556))
    return round(total * taille / 1000)


def couper(texte, taille, limite):
    """Le texte tel qu'il s'afficherait coupé (avec « … »)."""
    if largeur(texte, taille) <= limite:
        return texte
    out = ""
    for c in texte:
        if largeur(out + c + "…", taille) > limite:
            break
        out += c
    return out.rstrip() + " …"


def typographie(texte):
    pb = []
    if re.search(r"\S[:;!?](?:\s|$)", texte) and not re.search(r"https?:", texte):
        pb.append("espace manquante avant « : ; ! ? »")
    if "—" in texte or re.search(r"\s–\s", texte):
        pb.append("tiret cadratin ou demi-cadratin (remplacer par une virgule)")
    if re.search(r'"[^"]+"', texte):
        pb.append("guillemets droits (utiliser « »)")
    if re.search(r"\d\s%", texte):
        pb.append("pourcentage détaché (écrire « 15% »)")
    if re.search(r"[!?]{2,}|\.{2}(?!\.)", texte):
        pb.append("ponctuation doublée")
    return pb


def analyser(title, description="", mot_cle="", marque="", annee=None, pref_title=None, pref_desc=None):
    annee = annee or dt.date.today().year
    constats = []
    t = (title or "").strip()
    d = (description or "").strip()
    r = {"title": t, "description": d}

    def c(gravite, quoi, conseil=""):
        constats.append({"gravite": gravite, "constat": quoi, "conseil": conseil})

    if not t:
        c("haute", "title absent", "Chaque page a un title descriptif et unique.")
    else:
        px = largeur(t, TITLE_TAILLE)
        r.update(title_car=len(t), title_px=px)
        if px > TITLE_PX:
            c("moyenne", f"title de {px} px (repère ≈ {TITLE_PX} px) : probablement coupé",
              f"Affichage estimé : « {couper(t, TITLE_TAILLE, TITLE_PX)} ». Garder les mots importants au début.")
        elif px < 250:
            c("info", f"title court ({px} px)", "Il peut porter une raison de cliquer (bénéfice, format, public).")
        if pref_title and not pref_title[0] <= len(t) <= pref_title[1]:
            c("info", f"title de {len(t)} caractères, hors de ta préférence {pref_title[0]}-{pref_title[1]}",
              "Préférence de site-context.md ; c'est la largeur en pixels qui décide de la coupure.")
        if re.fullmatch(r"(accueil|home|page d'accueil|sans titre|untitled|bienvenue)", t.lower()):
            c("haute", "title générique", "Décrire la page, pas son rôle.")
        if mot_cle:
            tm, tt = tf.termes(mot_cle), tf.termes(t)
            if not tm:
                pass
            elif not set(tm) <= set(tt):
                manquants = [m for m in mot_cle.split() if tf.termes(m) and not set(tf.termes(m)) <= set(tt)]
                c("haute", f"mot-clé absent ou incomplet dans le title (manque : {', '.join(manquants) or mot_cle})",
                  "Placer la requête principale dans les premiers mots, si elle se lit naturellement.")
            else:
                pos = max(tt.index(m) for m in tm)
                if pos > max(3, len(tt) // 2):
                    c("basse", "mot-clé dans la seconde moitié du title", "Le mettre au début : c'est là que le lecteur lit.")
            compte = sum(1 for m in tf.termes(t) if m in set(tm))
            if tm and compte > 2 * len(set(tm)):
                c("haute", "mot-clé répété dans le title (bourrage)", "Une fois suffit.")
        if marque:
            fm = tf.fold(marque)
            n = tf.fold(t).count(fm)
            if n > 1:
                c("moyenne", "marque répétée dans le title", "Une fois, au début ou à la fin.")
            elif n == 1 and not (tf.fold(t).startswith(fm) or tf.fold(t).rstrip(" .").endswith(fm)):
                c("basse", "marque au milieu du title", "Au début ou à la fin, séparée par « | » ou « - ».")
        for y in re.findall(r"\b(20\d\d)\b", t):
            if int(y) < annee:
                c("haute", f"année dépassée dans le title ({y})",
                  "Google réécrit les titles périmés. Mettre à jour la page, puis l'année ; ou retirer l'année.")
        for p in typographie(t):
            c("basse", f"title : {p}")

    if not d:
        c("moyenne", "meta description absente", "Google construit alors l'extrait depuis la page ; une description "
                                                  "qui résume vraiment la page peut être reprise.")
    else:
        px = largeur(d, DESC_TAILLE)
        r.update(description_car=len(d), description_px=px)
        if px > DESC_PX_ORDI:
            c("basse", f"description de {px} px : coupée sur ordinateur (repère ≈ {DESC_PX_ORDI} px)",
              f"Affichage estimé : « {couper(d, DESC_TAILLE, DESC_PX_ORDI)} »")
        elif px > DESC_PX_MOBILE:
            c("info", f"description de {px} px : coupée sur mobile (repère ≈ {DESC_PX_MOBILE} px)",
              "Mettre l'essentiel dans la première moitié.")
        if pref_desc and not pref_desc[0] <= len(d) <= pref_desc[1]:
            c("info", f"description de {len(d)} caractères, hors de ta préférence {pref_desc[0]}-{pref_desc[1]}",
              "Préférence de site-context.md ; Google n'a pas de limite et réécrit souvent la description.")
        if len(d) < 70:
            c("basse", f"description très courte ({len(d)} caractères)", "Résumer ce que la page apporte.")
        if t:
            coeur = re.split(r"\s[|\-–—·]\s", t)[0].strip()
            if len(coeur) >= 25 and tf.fold(d).startswith(tf.fold(coeur)[:max(25, len(coeur) - 3)]):
                c("moyenne", "la description recopie le title", "Ouvrir sur une information que le title ne donne pas.")
        mots_d = d.split()
        if d.count(",") >= 4 and len(mots_d) / (d.count(",") + 1) < 3.5:
            c("haute", "description en liste de mots-clés", "Écrire une phrase qui résume la page.")
        if mot_cle and tf.termes(mot_cle) and not set(tf.termes(mot_cle)) <= set(tf.termes(d)):
            c("info", "mot-clé absent de la description", "Google met en gras les mots de la requête : utile, pas obligatoire.")
        for p in typographie(d):
            c("basse", f"description : {p}")
    r["constats"] = constats
    r["verdict"] = "À REVOIR" if any(x["gravite"] in ("haute", "moyenne") for x in constats) else "OK"
    return r


def squelette(texte):
    """Forme d'un texte sans ses mots variables (nombres, mots capitalisés)."""
    t = re.sub(r"\d+([.,]\d+)?", "#", texte.lower())
    return " ".join(t.split())


def analyser_lot(pages, mot_cle="", marque="", annee=None, pref_title=None, pref_desc=None):
    res = [dict(analyser(p.get("title", ""), p.get("description", ""), mot_cle, marque, annee, pref_title, pref_desc),
                url=p.get("url", ""))
           for p in pages]
    n = len(pages)
    alertes = []
    for champ, nom in (("title", "titles"), ("description", "descriptions")):
        compte = Counter(p.get(champ, "").strip().lower() for p in pages if p.get(champ, "").strip())
        doublons = {k: v for k, v in compte.items() if v > 1}
        if doublons:
            alertes.append({"gravite": "haute", "constat": f"{sum(doublons.values())} {nom} en double "
                                                          f"({len(doublons)} texte(s) répété(s))",
                            "exemples": list(doublons)[:3]})
    # même début et même fin sur beaucoup de pages : gabarit
    descs = [p.get("description", "").strip() for p in pages if p.get("description", "").strip()]
    fins = Counter(" ".join(d.split()[-4:]).lower() for d in descs if len(d.split()) >= 8)
    for fin, k in fins.items():
        if k >= 3 and k / max(1, len(descs)) >= 0.2:
            alertes.append({"gravite": "moyenne", "constat": f"même fin de description sur {k} pages : « {fin} »",
                            "exemples": []})
    cta = Counter(CTA_FIN.search(d).group(1).lower() for d in descs if CTA_FIN.search(d))
    for phrase, k in cta.items():
        if k >= 3 and k / max(1, len(descs)) >= 0.2:
            alertes.append({"gravite": "moyenne", "constat": f"appel à l'action identique en fin de {k} descriptions : « {phrase} »",
                            "exemples": []})
    titles = [p.get("title", "").strip() for p in pages if p.get("title", "").strip()]
    if len(titles) >= 4:
        debuts = Counter(" ".join(squelette(t).split()[:3]) for t in titles)
        for debut, k in debuts.items():
            if k / len(titles) >= 0.5 and k >= 3:
                alertes.append({"gravite": "basse", "constat": f"{k} titles commencent pareil : « {debut} … »",
                                "exemples": []})
    return {"pages": res, "nombre": n, "alertes_lot": alertes,
            "a_revoir": sum(1 for x in res if x["verdict"] != "OK"),
            "verdict": "À REVOIR" if alertes or any(x["verdict"] != "OK" for x in res) else "OK"}


def lire_lot(chemin):
    texte = Path(chemin).read_text(encoding="utf-8-sig")
    if chemin.lower().endswith(".json") or texte.lstrip().startswith("["):
        data = json.loads(texte)
        return [{"url": x.get("url", ""), "title": x.get("title", ""),
                 "description": x.get("description", x.get("meta_description", ""))} for x in data]
    premiere = texte.splitlines()[0] if texte else ""
    delim = ";" if premiere.count(";") > premiere.count(",") else ("\t" if "\t" in premiere else ",")
    pages = []
    for ligne in csv.DictReader(texte.splitlines(), delimiter=delim):
        low = {k.strip().lower(): (v or "") for k, v in ligne.items() if k}

        def pick(*noms):
            for n in noms:
                for k, v in low.items():
                    if k == n or k.startswith(n):
                        return v
            return ""
        pages.append({"url": pick("url", "address", "adresse"),
                      "title": pick("title", "title 1", "titre"),
                      "description": pick("meta description", "meta description 1", "description")})
    return pages


def afficher(r):
    out = []
    if "title_px" in r:
        out.append(f"TITLE        {r['title']}")
        out.append(f"             {r['title_car']} caractères · {r['title_px']} px (repère ≈ {TITLE_PX} px)")
    if "description_px" in r:
        out.append(f"DESCRIPTION  {r['description']}")
        out.append(f"             {r['description_car']} caractères · {r['description_px']} px "
                   f"(repères ≈ {DESC_PX_MOBILE} px mobile, {DESC_PX_ORDI} px ordinateur)")
    for x in r["constats"]:
        out.append(f"  [{x['gravite']}] {x['constat']}" + (f"\n          → {x['conseil']}" if x["conseil"] else ""))
    out.append(f"VERDICT : {r['verdict']}")
    return "\n".join(out)


def afficher_lot(r):
    out = [f"LOT · {r['nombre']} pages · {r['a_revoir']} à revoir"]
    for a in r["alertes_lot"]:
        out.append(f"  [{a['gravite']}] {a['constat']}")
        for e in a["exemples"]:
            out.append(f"      · {e}")
    for p in r["pages"]:
        graves = [x for x in p["constats"] if x["gravite"] in ("haute", "moyenne")]
        if graves:
            out.append(f"  {p['url'] or p['title'][:50]}")
            for x in graves:
                out.append(f"      [{x['gravite']}] {x['constat']}")
    out.append(f"VERDICT : {r['verdict']}")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Title et meta description : largeur en pixels et contrôles.")
    p.add_argument("--title", default="")
    p.add_argument("--description", default="")
    p.add_argument("--mot-cle", default="")
    p.add_argument("--marque", default="")
    p.add_argument("--annee", type=int, help="année de référence (défaut : année en cours)")
    p.add_argument("--pref-title", help="préférence de longueur du title en caractères, ex. 55-60")
    p.add_argument("--pref-description", help="préférence de longueur de la description, ex. 150-160")
    p.add_argument("--lot", help="CSV (url,title,description ; export Screaming Frog accepté) ou JSON")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    def borne(x):
        if not x:
            return None
        m = re.fullmatch(r"\s*(\d+)\s*[-–à]\s*(\d+)\s*", x)
        if not m:
            p.error(f"préférence illisible : {x} (attendu : 55-60)")
        return int(m.group(1)), int(m.group(2))
    pt, pd = borne(a.pref_title), borne(a.pref_description)
    if a.lot:
        try:
            pages = lire_lot(a.lot)
        except (OSError, ValueError, json.JSONDecodeError) as e:
            print(f"Erreur : {e}", file=sys.stderr)
            return 1
        if not pages:
            print("Erreur : aucune page lue dans le lot.", file=sys.stderr)
            return 1
        r = analyser_lot(pages, a.mot_cle, a.marque, a.annee, pt, pd)
        print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher_lot(r))
        return 0 if r["verdict"] == "OK" else 2
    if not a.title and not a.description:
        p.print_help(sys.stderr)
        return 1
    r = analyser(a.title, a.description, a.mot_cle, a.marque, a.annee, pt, pd)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return 0 if r["verdict"] == "OK" else 2


if __name__ == "__main__":
    sys.exit(main())
