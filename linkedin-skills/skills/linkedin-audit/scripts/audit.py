#!/usr/bin/env python3
"""audit.py : ce qui marche vraiment sur un compte LinkedIn, sans conclure trop vite.

  decrire --fichier posts.csv|.json|.xlsx [--journal journal.md] [--abonnes 2400]
          [--metrique engagement|commentaires|portee] [--voix profil|page]
      Médiane et écart absolu médian (MAD), coefficient de variation robuste,
      bandes (exceptionnel, fort, typique, faible, très faible), top 5 et
      flop 5. Sous 10 posts : description seulement (code 2).

  motifs --fichier … [--journal …] [--attributs formule,format,pilier,longueur,lien,appel,reponse,jour]
      Teste chaque motif candidat avec 4 filtres : au moins 5 posts dedans et
      5 dehors ; écart de médianes d'au moins 15% ; test de permutation
      (2 000 tirages, graine fixe) battu à 90% ; décompte des faux positifs
      attendus. Le jour de la semaine est testé en dernier. « Rien n'a
      survécu » est un résultat (code 2). Sous 10 posts : refus (code 3).

  experience --hypothese "…" --variable "…" --cv 0.45 --effet 0.30
             --posts-semaine 2 [--semaines-max 12] [--alpha 0.10] [--puissance 0.80]
      Taille d'une expérience à deux variantes : posts par variante, semaines,
      effet minimal détectable dans la fenêtre, critère d'échec écrit avant,
      ligne prête pour apprentissages.md. Code 0 faisable, 2 trop long, 3 refusé.

Taux d'engagement = (réactions + commentaires + republications) / impressions.
Fichier : CSV (virgule ou point-virgule), JSON, ou l'export .xlsx de LinkedIn
(lu sans dépendance : choisir la feuille avec --feuille). Les colonnes sont
reconnues en français ou en anglais (date, impressions, réactions,
commentaires, republications, enregistrements, envois, format…).

D'après post_performance_analyzer.py, pattern_miner.py et
experiment_planner.py (alirezarezvani, claude-skills, MIT), réécrits en
français, avec lecture du journal du pack, de l'export .xlsx et séparation
page / profil. Sans dépendance. Rien n'est lu sur LinkedIn.
"""

import argparse
import csv
import io
import json
import math
import random
import re
import sys
import unicodedata
import zipfile
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

MIN_POSTS = 10
MIN_GROUPE = 5
EFFET_MIN = 0.15
ALPHA = 0.10
TIRAGES = 2000
GRAINE = 20261002
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
Z_ALPHA = {0.20: 1.282, 0.10: 1.645, 0.05: 1.960}
Z_PUISSANCE = {0.70: 0.524, 0.80: 0.842, 0.90: 1.282}

ALIAS = {
    "date": ["date", "date de publication", "publie le", "post publish date", "published", "date du post"],
    "impressions": ["impressions", "affichages", "vues du post"],
    "reactions": ["reactions", "j'aime", "likes"],
    "commentaires": ["commentaires", "comments"],
    "republications": ["republications", "partages", "reposts", "shares", "republication"],
    "sauvegardes": ["enregistrements", "sauvegardes", "saves"],
    "envois": ["envois", "sends", "envois en message"],
    "clics": ["clics", "clicks"],
    "formule": ["formule", "formula", "hook"],
    "format": ["format", "type de post", "type"],
    "pilier": ["pilier", "pillar", "theme", "thème"],
    "caracteres": ["caracteres", "longueur", "chars", "characters"],
    "lien": ["lien", "lien dans le post", "links_in_body"],
    "appel": ["appel a l'action", "appel", "cta"],
    "reponse": ["reponse rapide", "reponses sous 2 h", "reponse"],
    "voix": ["voix", "compte"],
    "titre": ["titre", "premiere ligne", "title", "post", "post url", "url"],
    "objectif": ["objectif", "goal"],
}

EXEMPLE = [
    # date, impressions, réactions, commentaires, republications, formule, format, pilier, caractères, réponse rapide
    ("2026-05-05", 2100, 41, 12, 2, "chiffre-d-abord", "texte", "Rétention", 1250, "oui"),
    ("2026-05-07", 1650, 22, 3, 0, "liste-promise", "carrousel", "Acquisition", 700, "non"),
    ("2026-05-12", 2900, 66, 21, 4, "erreur-datee", "texte", "Rétention", 1400, "oui"),
    ("2026-05-14", 1400, 19, 2, 1, "liste-promise", "texte", "Acquisition", 650, "non"),
    ("2026-05-19", 3300, 80, 26, 3, "chiffre-d-abord", "texte", "Rétention", 1320, "oui"),
    ("2026-05-21", 1500, 25, 4, 1, "comparatif", "image", "Acquisition", 820, "non"),
    ("2026-05-26", 2500, 52, 15, 2, "cas-a-trancher", "texte", "Acquisition", 980, "oui"),
    ("2026-05-28", 1200, 15, 1, 0, "liste-promise", "carrousel", "Équipe", 600, "non"),
    ("2026-06-02", 4100, 98, 35, 6, "erreur-datee", "texte", "Rétention", 1500, "oui"),
    ("2026-06-04", 1700, 27, 5, 1, "comparatif", "image", "Acquisition", 760, "non"),
    ("2026-06-09", 2300, 47, 13, 2, "scene", "texte", "Équipe", 1100, "oui"),
    ("2026-06-11", 1350, 18, 3, 0, "releve", "carrousel", "Acquisition", 680, "non"),
    ("2026-06-16", 2800, 61, 19, 3, "chiffre-d-abord", "texte", "Rétention", 1280, "oui"),
    ("2026-06-18", 1600, 24, 4, 1, "liste-promise", "texte", "Acquisition", 720, "non"),
]


def norme(t):
    t = unicodedata.normalize("NFKD", str(t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'").strip()


def mediane(xs):
    s = sorted(xs)
    n = len(s)
    if not n:
        return 0.0
    return float(s[n // 2]) if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def centile(xs, p):
    s = sorted(xs)
    if not s:
        return 0.0
    k = (len(s) - 1) * p / 100.0
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


# ---------- lecture ----------

def lire_xlsx(chemin, feuille=1):
    """Lit une feuille d'un .xlsx (bibliothèque standard seulement)."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(chemin) as z:
        partages = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
                partages.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
        nom = f"xl/worksheets/sheet{feuille}.xml"
        if nom not in z.namelist():
            raise OSError(f"feuille {feuille} absente ({', '.join(n for n in z.namelist() if 'worksheets/sheet' in n)})")
        lignes = []
        for row in ET.fromstring(z.read(nom)).iter("{%s}row" % ns["m"]):
            cel = {}
            for c in row.findall("m:c", ns):
                ref = re.match(r"[A-Z]+", c.get("r", "A")).group(0)
                col = 0
                for ch in ref:
                    col = col * 26 + ord(ch) - 64
                v = c.find("m:v", ns)
                if c.get("t") == "s" and v is not None:
                    val = partages[int(v.text)]
                elif c.get("t") == "inlineStr":
                    val = "".join(t.text or "" for t in c.iter("{%s}t" % ns["m"]))
                else:
                    val = v.text if v is not None else ""
                cel[col] = val
            if cel:
                lignes.append([cel.get(i, "") for i in range(1, max(cel) + 1)])
    # la première ligne qui contient « impressions » sert d'en-tête (les exports ont des lignes de titre)
    for i, l in enumerate(lignes):
        if any(norme(x) in ALIAS["impressions"] for x in l):
            entete = l
            return [dict(zip(entete, r)) for r in lignes[i + 1:] if any(str(x).strip() for x in r)]
    raise OSError("aucune colonne « impressions » dans cette feuille : essaie --feuille 2, 3…")


def lire(chemin, feuille=1):
    p = Path(chemin)
    if p.suffix.lower() == ".xlsx":
        return lire_xlsx(p, feuille)
    texte = p.read_text(encoding="utf-8-sig")
    if texte.lstrip().startswith(("[", "{")):
        d = json.loads(texte)
        return d.get("posts", []) if isinstance(d, dict) else d
    dialecte = ";" if texte.split("\n", 1)[0].count(";") > texte.split("\n", 1)[0].count(",") else ","
    return [dict(r) for r in csv.DictReader(io.StringIO(texte), delimiter=dialecte)]


def nombre(v):
    if v in (None, ""):
        return None
    s = str(v).replace(" ", "").replace("\xa0", "").replace(" ", "")
    s = s.replace("%", "")
    if re.fullmatch(r"-?\d{1,3}(?:\.\d{3})+(?:,\d+)?", s):
        s = s.replace(".", "").replace(",", ".")
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def lire_date(v):
    s = str(v or "").strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return date(int(m[1]), int(m[2]), int(m[3]))
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return date(int(m[3]), int(m[2]), int(m[1]))
    if re.fullmatch(r"\d{5}(?:\.0+)?", s):  # date Excel
        return date(1899, 12, 30).fromordinal(date(1899, 12, 30).toordinal() + int(float(s)))
    return None


def normaliser(lignes):
    """Ramène chaque ligne aux clés canoniques ; rend (posts, colonnes non reconnues)."""
    if not lignes:
        return [], []
    cles = {}
    inconnues = []
    for k in lignes[0].keys():
        kn = norme(k)
        trouve = next((canon for canon, al in ALIAS.items() if kn in [norme(a) for a in al]), None)
        if trouve and trouve not in cles.values():
            cles[k] = trouve
        else:
            inconnues.append(k)
    posts = []
    for l in lignes:
        p = {canon: l.get(k) for k, canon in cles.items()}
        posts.append(p)
    return posts, inconnues


def joindre_journal(posts, chemin):
    """Complète formule, objectif, format, pilier, longueur, appel depuis journal.md (même date)."""
    if not chemin or not Path(chemin).exists():
        return 0
    texte = Path(chemin).read_text(encoding="utf-8")
    m = re.search(r"## Posts[^\n]*\n(?:[^|\n][^\n]*\n|\n)*((?:\|.*\n?)+)", texte)
    if not m:
        return 0
    lignes = m.group(1).splitlines()
    entete = [norme(c) for c in lignes[0].strip().strip("|").split("|")]
    par_date = {}
    for l in lignes[2:]:
        d = dict(zip(entete, [c.strip() for c in l.strip().strip("|").split("|")]))
        jd = lire_date(d.get("date"))
        if jd:
            par_date.setdefault(jd, []).append(d)
    n = 0
    for p in posts:
        jd = lire_date(p.get("date"))
        if jd in par_date and len(par_date[jd]) == 1:
            j = par_date[jd][0]
            for cle, col in (("formule", "formule"), ("objectif", "objectif"), ("format", "format"),
                             ("pilier", "pilier"), ("caracteres", "longueur"), ("appel", "appel a l'action")):
                if not p.get(cle) and j.get(col):
                    p[cle] = j[col]
            n += 1
    return n


def contacts_journal(chemin, debut=None, fin=None):
    """Conversations et prospects notés dans journal.md (section « Contacts »), par origine."""
    if not chemin or not Path(chemin).exists():
        return None
    texte = Path(chemin).read_text(encoding="utf-8")
    m = re.search(r"## Contacts[^\n]*\n(?:[^|\n][^\n]*\n|\n)*((?:\|.*\n?)+)", texte)
    if not m:
        return None
    lignes = m.group(1).splitlines()
    entete = [norme(c) for c in lignes[0].strip().strip("|").split("|")]
    total, origines = 0, {}
    for l in lignes[2:]:
        d = dict(zip(entete, [c.strip() for c in l.strip().strip("|").split("|")]))
        jd = lire_date(d.get("date"))
        if not jd or (debut and jd < debut) or (fin and jd > fin):
            continue
        total += 1
        cle = next((k for k in d if k.startswith("origine")), None)
        o = (d.get(cle) or "non renseignée").split(" ")[0] if cle else "non renseignée"
        origines[o] = origines.get(o, 0) + 1
    return {"total": total, "origines": origines}


def preparer(posts, abonnes=None, voix=None):
    out, ecartes = [], 0
    for p in posts:
        if voix and p.get("voix") and norme(p["voix"]) != norme(voix):
            continue
        imp = nombre(p.get("impressions"))
        if not imp or imp <= 0:
            ecartes += 1
            continue
        r, c, rep = (nombre(p.get(k)) or 0 for k in ("reactions", "commentaires", "republications"))
        d = lire_date(p.get("date"))
        car = nombre(p.get("caracteres"))
        lien = norme(p.get("lien"))
        rec = {
            "date": d.isoformat() if d else str(p.get("date") or ""),
            "titre": str(p.get("titre") or p.get("formule") or "")[:60],
            "impressions": int(imp), "reactions": int(r), "commentaires": int(c), "republications": int(rep),
            "engagement": (r + c + rep) / imp,
            "commentaires_ratio": c / r if r else (1.0 if c else 0.0),
            "portee": imp / abonnes if abonnes else None,
            "sauvegardes": nombre(p.get("sauvegardes")), "envois": nombre(p.get("envois")),
            "formule": str(p.get("formule") or "non renseigné"),
            "format": norme(p.get("format")) or "non renseigné",
            "pilier": str(p.get("pilier") or "non renseigné"),
            "longueur": ("non renseigné" if not car else "court (<800)" if car < 800 else
                         "moyen (800-1500)" if car <= 1500 else "long (>1500)"),
            "lien": "non renseigné" if not lien else "oui" if lien in ("oui", "yes", "1", "true", "vrai") else "non",
            "appel": norme(p.get("appel")) or "non renseigné",
            "reponse": "non renseigné" if not p.get("reponse") else ("oui" if norme(p["reponse"]) in ("oui", "yes", "1", "true", "vrai") else "non"),
            "jour": JOURS[d.weekday()] if d else "non renseigné",
            "voix": norme(p.get("voix")) or "",
        }
        out.append(rec)
    return out, ecartes


# ---------- décrire ----------

def decrire(posts, metrique="engagement"):
    vals = [p[metrique] for p in posts if p.get(metrique) is not None]
    if not vals:
        return {"verdict": "INUTILISABLE", "code": 3, "posts": 0,
                "message": f"aucune valeur pour « {metrique} » (portée : donne --abonnes)."}
    med = mediane(vals)
    mad = mediane([abs(v - med) for v in vals])
    q1, q3 = centile(vals, 25), centile(vals, 75)
    iqr = q3 - q1
    haut, bas = q3 + 1.5 * iqr, q1 - 1.5 * iqr
    for p in posts:
        v = p.get(metrique)
        if v is None:
            p["bande"] = "-"
        elif v >= haut:
            p["bande"] = "exceptionnel"
        elif v >= q3:
            p["bande"] = "fort"
        elif v >= q1:
            p["bande"] = "typique"
        elif v > bas:
            p["bande"] = "faible"
        else:
            p["bande"] = "très faible"
    tries = sorted([p for p in posts if p.get(metrique) is not None], key=lambda p: -p[metrique])
    n = len(vals)
    cv = 1.4826 * mad / med if med else None
    return {
        "verdict": "DESCRIPTION SEULE" if n < MIN_POSTS else "ANALYSÉ", "code": 2 if n < MIN_POSTS else 0,
        "posts": n, "metrique": metrique, "mediane": med, "mad": mad, "cv": round(cv, 3) if cv is not None else None,
        "q1": q1, "q3": q3, "seuil_exceptionnel": haut,
        "bandes": {b: sum(1 for p in posts if p.get("bande") == b) for b in ("exceptionnel", "fort", "typique", "faible", "très faible")},
        "top": tries[:5], "flop": tries[-5:][::-1] if n >= 10 else [],
        "periode": [min(p["date"] for p in posts), max(p["date"] for p in posts)] if posts else [],
        "avertissement": (f"{n} posts : sous {MIN_POSTS}, on décrit, on ne conclut pas." if n < MIN_POSTS else ""),
    }


# ---------- motifs ----------

def _p_permutation(groupe, autre, observe, rng):
    pool = groupe + autre
    k = len(groupe)
    extreme = 0
    for _ in range(TIRAGES):
        rng.shuffle(pool)
        if abs(mediane(pool[:k]) - mediane(pool[k:])) >= abs(observe):
            extreme += 1
    return (extreme + 1) / (TIRAGES + 1)


def motifs(posts, attributs, metrique="engagement"):
    data = [p for p in posts if p.get(metrique) is not None]
    if len(data) < MIN_POSTS:
        return {"verdict": "DONNÉES INSUFFISANTES", "code": 3, "posts": len(data),
                "message": f"{len(data)} posts : sous {MIN_POSTS}, il n'y a rien à tester. L'écart entre deux posts "
                           "sur LinkedIn dépasse tout ce qu'un si petit échantillon peut montrer. Continue le plan, "
                           "relance dans six semaines."}
    # le jour de la semaine en dernier : c'est la cause qu'on aimerait trouver, et presque jamais la bonne
    attributs = [a for a in attributs if a != "jour"] + (["jour"] if "jour" in attributs else [])
    rng = random.Random(GRAINE)
    candidats, miroirs = [], []
    for attr in attributs:
        valeurs = sorted({d[attr] for d in data if d[attr] != "non renseigné"})
        if len(valeurs) < 2:
            continue
        if len(valeurs) == 2:
            miroirs.append(f"{attr} : seul « {valeurs[0]} » est testé, « {valeurs[1]} » est la même comparaison inversée")
            valeurs = valeurs[:1]
        for val in valeurs:
            g = [d[metrique] for d in data if d[attr] == val]
            o = [d[metrique] for d in data if d[attr] != val and d[attr] != "non renseigné"]
            c = {"attribut": attr, "valeur": val, "n_dedans": len(g), "n_dehors": len(o),
                 "_posts": {i for i, d in enumerate(data) if d[attr] == val},
                 "_connus": {i for i, d in enumerate(data) if d[attr] != "non renseigné"}}
            if len(g) < MIN_GROUPE or len(o) < MIN_GROUPE:
                c.update(verdict="NON TESTÉ", raison=f"il faut {MIN_GROUPE} posts dedans et {MIN_GROUPE} dehors ; il y en a {len(g)} et {len(o)}")
                candidats.append(c)
                continue
            mg, mo = mediane(g), mediane(o)
            rel = (mg - mo) / mo if mo else 0.0
            c.update(mediane_dedans=mg, mediane_dehors=mo, effet=round(rel, 3))
            if abs(rel) < EFFET_MIN:
                c.update(verdict="TROP PETIT", raison=f"écart de {rel:+.0%} : sous le seuil de {EFFET_MIN:.0%}, vrai ou non, ce n'est pas une raison de changer".replace(" %", "%"))
                candidats.append(c)
                continue
            p = _p_permutation(list(g), list(o), mg - mo, rng)
            c["p"] = round(p, 4)
            if p < ALPHA:
                c.update(verdict="SOUTENU", raison=f"écart de {rel:+.0%}, plus grand que {1 - p:.0%} des {TIRAGES} tirages au hasard".replace(" %", "%"))
            else:
                c.update(verdict="NON SOUTENU", raison=f"écart de {rel:+.0%}, mais {p:.0%} des tirages au hasard en font autant : c'est du bruit".replace(" %", "%"))
            candidats.append(c)
    testes = [c for c in candidats if "p" in c]
    soutenus = [c for c in candidats if c["verdict"] == "SOUTENU"]
    # motifs confondus : deux motifs qui désignent (presque) les mêmes posts ne sont qu'un seul signal
    groupes = []

    def recouvre(c, ref):
        """Les deux motifs désignent-ils (presque) les mêmes posts, dans un sens ou dans l'autre ?"""
        commun = c["_connus"] & ref["_connus"]
        if not commun:
            return False
        a, b = c["_posts"] & commun, ref["_posts"] & commun
        for x, y in ((a, b), (a, commun - b)):
            if x and y and len(x & y) / min(len(x), len(y)) >= 0.8:
                return True
        return False

    for c in soutenus:
        for gr in groupes:
            if any(recouvre(c, ref) for ref in gr):
                gr.append(c)
                break
        else:
            groupes.append([c])
    confondus = [[f"{c['attribut']} = {c['valeur']}" for c in gr] for gr in groupes if len(gr) > 1]
    for c in candidats:
        c.pop("_posts", None)
        c.pop("_connus", None)
    attendus = round(len(testes) * ALPHA, 1)
    return {
        "verdict": "MOTIFS TROUVÉS" if soutenus else "RIEN N'A SURVÉCU", "code": 0 if soutenus else 2,
        "posts": len(data), "metrique": metrique,
        "methode": f"écart de médianes, test de permutation ({TIRAGES} tirages, graine {GRAINE}), seuil {ALPHA}, "
                   f"effet minimal {EFFET_MIN:.0%}, {MIN_GROUPE} posts par groupe".replace(" %", "%").replace("0.1,", "0,1,"),
        "candidats": candidats, "testes": len(testes), "soutenus": soutenus, "miroirs": miroirs,
        "confondus": confondus, "signaux_distincts": len(groupes),
        "faux_positifs_attendus": attendus,
        "note": (f"{len(testes)} motif(s) testé(s) au seuil de {str(ALPHA).replace('.', ',')} : le hasard seul en ferait passer environ {str(attendus).replace('.', ',')}. "
                 f"{len(soutenus)} passe(nt). " +
                 ("Ce sont des hypothèses à tester (experience), pas des conclusions." if len(soutenus) <= max(1, attendus)
                  else "C'est plus que le hasard : un indice, à confirmer par une expérience.")),
        "confusion": "Un motif trouvé dans des posts passés est une hypothèse : tu as fait des carrousels quand tu avais "
                     "de la matière structurée, sur des sujets que tu connaissais, des semaines où tu avais du temps.",
    }


# ---------- expérience ----------

def experience(hypothese, variable, cv, effet, posts_semaine, semaines_max=12, alpha=0.10, puissance=0.80,
               variante_a="{{variante A}}", variante_b="{{variante B}}"):
    if not hypothese.strip() or not variable.strip():
        return {"verdict": "REFUSÉ", "code": 3, "message": "Écris l'hypothèse et la seule variable qui change."}
    if cv <= 0 or effet <= 0 or posts_semaine <= 0:
        return {"verdict": "REFUSÉ", "code": 3, "message": "cv, effet et posts par semaine doivent être positifs (cv : sortie de « decrire »)."}
    if alpha not in Z_ALPHA or puissance not in Z_PUISSANCE:
        return {"verdict": "REFUSÉ", "code": 3, "message": f"alpha parmi {sorted(Z_ALPHA)}, puissance parmi {sorted(Z_PUISSANCE)}."}
    za, zb = Z_ALPHA[alpha], Z_PUISSANCE[puissance]
    n = math.ceil(2 * (za + zb) ** 2 * cv ** 2 / effet ** 2)
    total = 2 * n
    semaines = math.ceil(total / posts_semaine)
    possible = max(1, int(posts_semaine * semaines_max) // 2)
    mde = math.sqrt(2 * (za + zb) ** 2 * cv ** 2 / possible)
    faisable = semaines <= semaines_max
    fin = f"{semaines} semaines" if faisable else f"{semaines_max} semaines"
    critere = (f"Si, après {n if faisable else possible} posts par variante, la médiane de la variante B ne dépasse pas "
               f"celle de A d'au moins {round(effet * 100) if faisable else round(mde * 100)}%, l'hypothèse est abandonnée.")
    return {
        "verdict": "FAISABLE" if faisable else "TROP LONG", "code": 0 if faisable else 2,
        "posts_par_variante": n, "posts_total": total, "semaines": semaines,
        "effet_minimal_detectable": round(mde, 3),
        "message": ("" if faisable else
                    f"Il faudrait {semaines} semaines. En {semaines_max} semaines, tu ne verras qu'un effet d'au moins "
                    f"{round(mde * 100)}%. Teste une variable qui peut avoir un gros effet, accepte ce seuil, ou renonce "
                    "et écris ce que tu préfères écrire : c'est une réponse honnête."),
        "protocole": [
            "Une seule variable change ; formule, pilier, format, longueur et créneau restent comparables.",
            "Alterner A et B (A, B, A, B…), jamais un bloc de A puis un bloc de B.",
            "Le critère d'échec est écrit avant le premier post, dans apprentissages.md.",
            "Ne pas regarder le résultat avant la fin : on arrête toujours au moment où ça arrange.",
        ],
        "critere_echec": critere,
        "ligne_apprentissages": f"| {date.today().isoformat()} | {hypothese} | {variable} : {variante_a} | {variable} : {variante_b} | "
                                f"{n if faisable else possible} | {critere} | dans {fin} |",
    }


# ---------- sortie ----------

def pct(x):
    return f"{x * 100:.1f}%".replace(".", ",")


def afficher_description(r, ecartes, joints, voix_melangees):
    if r["code"] == 3:
        return f"AUDIT  INUTILISABLE · {r['message']}"
    m = r["metrique"]
    fmt = pct if m in ("engagement",) else (lambda x: f"{x:.2f}".replace(".", ","))
    l = [f"AUDIT  {r['verdict']} · {r['posts']} posts · {r['periode'][0]} au {r['periode'][1]} · métrique : {m}"]
    if m == "engagement":
        l.append("  taux d'engagement = (réactions + commentaires + republications) / impressions")
    l.append(f"  médiane {fmt(r['mediane'])} · écart absolu médian {fmt(r['mad'])} · CV robuste {str(r['cv']).replace('.', ',')}"
             f" · exceptionnel au-delà de {fmt(r['seuil_exceptionnel'])}")
    l.append("  bandes : " + ", ".join(f"{n} {b}" for b, n in r["bandes"].items()))
    if ecartes:
        l.append(f"  ! {ecartes} ligne(s) sans impressions ignorée(s)")
    if joints:
        l.append(f"  {joints} post(s) complétés par journal.md (formule, pilier, format)")
    if voix_melangees:
        l.append("  ! Page et profil mélangés : relance avec --voix profil puis --voix page. On ne compare pas deux audiences.")
    if r["avertissement"]:
        l.append(f"  ! {r['avertissement']}")
    c = r.get("contacts")
    if c is not None:
        l.insert(1, f"  RÉSULTATS QUI COMPTENT : {c['total']} conversation(s) ou prospect(s) dans journal.md sur la période"
                    + (" (" + ", ".join(f"{n} {o}" for o, n in c["origines"].items()) + ")" if c["origines"] else ""))
    l.append("\nTOP 5")
    for p in r["top"]:
        l.append(f"  {fmt(p[m]):>7}  {p['date']}  {p['formule']:<18} {p['format']:<10} {p['impressions']:>6} imp.  [{p['bande']}]")
    if r["flop"]:
        l.append("FLOP 5")
        for p in r["flop"]:
            l.append(f"  {fmt(p[m]):>7}  {p['date']}  {p['formule']:<18} {p['format']:<10} {p['impressions']:>6} imp.  [{p['bande']}]")
    return "\n".join(l)


def afficher_motifs(r):
    if r["code"] == 3 and "message" in r:
        return f"MOTIFS  {r['verdict']}\n  {r['message']}"
    l = [f"MOTIFS  {r['verdict']} · {r['posts']} posts · {r['methode']}"]
    for c in r["soutenus"]:
        l.append(f"  ✔ {c['attribut']} = {c['valeur']} : {c['raison']} (n = {c['n_dedans']} contre {c['n_dehors']})")
    for c in r["candidats"]:
        if c["verdict"] != "SOUTENU":
            l.append(f"  · {c['attribut']} = {c['valeur']} : {c['verdict'].lower()}, {c['raison']}")
    for m in r["miroirs"]:
        l.append(f"  · {m}")
    for gr in r.get("confondus", []):
        l.append(f"  ! Confondus : {', '.join(gr)} désignent presque les mêmes posts. C'est un seul signal ; "
                 "la cause ne se sépare qu'avec une expérience.")
    l.append(f"  {r['note']}")
    l.append(f"  {r['confusion']}")
    return "\n".join(l)


def main():
    a = argparse.ArgumentParser(description="Audit statistique d'un compte LinkedIn, sans conclure trop vite.")
    sous = a.add_subparsers(dest="cmd", required=True)
    for nom in ("decrire", "motifs"):
        s = sous.add_parser(nom)
        s.add_argument("--fichier")
        s.add_argument("--exemple", action="store_true")
        s.add_argument("--feuille", type=int, default=1)
        s.add_argument("--journal")
        s.add_argument("--abonnes", type=float)
        s.add_argument("--metrique", choices=["engagement", "commentaires_ratio", "portee"], default="engagement")
        s.add_argument("--voix")
        s.add_argument("--json", action="store_true")
        if nom == "motifs":
            s.add_argument("--attributs", default="formule,format,pilier,longueur,lien,appel,reponse,jour")
    e = sous.add_parser("experience")
    e.add_argument("--hypothese", required=True)
    e.add_argument("--variable", required=True)
    e.add_argument("--cv", type=float, required=True)
    e.add_argument("--effet", type=float, required=True, help="effet visé, relatif (0.30 = +30%%)")
    e.add_argument("--posts-semaine", type=float, required=True)
    e.add_argument("--semaines-max", type=int, default=12)
    e.add_argument("--alpha", type=float, default=0.10)
    e.add_argument("--puissance", type=float, default=0.80)
    e.add_argument("--a", default="{{variante A}}", help="la variante A (ex. « texte »)")
    e.add_argument("--b", default="{{variante B}}", help="la variante B (ex. « carrousel »)")
    e.add_argument("--json", action="store_true")
    x = a.parse_args()

    if x.cmd == "experience":
        r = experience(x.hypothese, x.variable, x.cv, x.effet, x.posts_semaine, x.semaines_max, x.alpha, x.puissance, x.a, x.b)
        if x.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        elif r["code"] == 3:
            print(f"EXPÉRIENCE  REFUSÉE · {r['message']}")
        else:
            print(f"EXPÉRIENCE  {r['verdict']} · {r['posts_par_variante']} posts par variante, {r['posts_total']} au total, "
                  f"environ {r['semaines']} semaines · effet minimal détectable en {x.semaines_max} semaines : {round(r['effet_minimal_detectable'] * 100)}%")
            if r["message"]:
                print(f"  ! {r['message']}")
            for p in r["protocole"]:
                print(f"  - {p}")
            print(f"  Critère d'échec : {r['critere_echec']}")
            print(f"  Ligne pour apprentissages.md (Expériences en cours) :\n  {r['ligne_apprentissages']}")
        return r["code"]

    try:
        if x.exemple:
            brut = [dict(zip(["date", "impressions", "reactions", "commentaires", "republications", "formule", "format",
                              "pilier", "caracteres", "reponse"], t)) for t in EXEMPLE]
        elif x.fichier:
            brut = lire(x.fichier, x.feuille)
        else:
            a.error("--fichier ou --exemple")
        lignes, inconnues = normaliser(brut)
        joints = joindre_journal(lignes, x.journal)
        voix_melangees = not x.voix and len({norme(p.get("voix")) for p in lignes if p.get("voix")}) > 1
        posts, ecartes = preparer(lignes, x.abonnes, x.voix)
    except (OSError, json.JSONDecodeError, zipfile.BadZipFile, ET.ParseError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    if x.metrique == "portee" and not x.abonnes:
        print("Erreur : --metrique portee demande --abonnes.", file=sys.stderr)
        return 1
    if x.cmd == "decrire":
        r = decrire(posts, x.metrique)
        if r.get("periode"):
            r["contacts"] = contacts_journal(x.journal, lire_date(r["periode"][0]), lire_date(r["periode"][1]) and
                                             date.fromordinal(lire_date(r["periode"][1]).toordinal() + 14))
        r.update(ignorees=ecartes, completes_par_journal=joints, colonnes_non_reconnues=inconnues, voix_melangees=voix_melangees)
        print(json.dumps(r, ensure_ascii=False, indent=2, default=str) if x.json else afficher_description(r, ecartes, joints, voix_melangees))
        return r["code"]
    r = motifs(posts, [s.strip() for s in x.attributs.split(",") if s.strip()], x.metrique)
    print(json.dumps(r, ensure_ascii=False, indent=2) if x.json else afficher_motifs(r))
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
