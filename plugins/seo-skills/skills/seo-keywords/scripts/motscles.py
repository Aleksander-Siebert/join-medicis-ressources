#!/usr/bin/env python3
"""motscles.py : une page par intention, mesuré (Python 3, sans dépendance).

Trois commandes :

  recouvrement SERP [--garder-omnipresents] [--json]
      Compare les 10 premiers résultats de chaque paire de requêtes et dit
      lesquelles méritent la même page. SERP : un fichier texte (« # requête »
      puis une URL par ligne) ou JSON {"requête": ["url", …]}. Les domaines
      présents dans 60% des SERP ou plus (Wikipédia, YouTube…) sont retirés
      avant le calcul quand ce sont des plateformes généralistes (Wikipédia,
      YouTube, Reddit…) : elles gonflent le recouvrement sans rien dire de
      l'intention. Un concurrent présent partout reste compté. Seuils (praticien, à confirmer sur ses données) :
      7 à 10 URL communes = même page ; 4 à 6 = même cluster, pages liées ;
      2 à 3 = clusters voisins ; 0 à 1 = sujets séparés.

  cannibalisation EXPORT [--marque MOT …] [--min-impressions N] [--json]
      Repère les requêtes pour lesquelles plusieurs pages du site se
      partagent les impressions. EXPORT : CSV requête × page de Search
      Console (API, connecteur, Looker Studio ou module de tableur ; l'export
      de l'interface ne croise pas requête et page). Colonnes reconnues en
      français ou en anglais : requête/query, page/landing page, clics/clicks,
      impressions, position.

  groupes EXPORT [--json]
      Regroupe les requêtes réelles du site par page qui les porte (la page
      qui reçoit le plus d'impressions) : ce pour quoi chaque page est déjà
      vue, et les requêtes orphelines à rattacher.

Codes de sortie : 0 rien à revoir · 2 points à revoir (cannibalisation,
échantillon bruité, paires à trancher) · 1 erreur d'utilisation.

Le script ne donne aucun volume de recherche : il n'en a pas. Un volume vient
d'un outil nommé (Search Console, Semrush, Ahrefs…) ou n'est pas écrit.

Exemples :
  python3 motscles.py recouvrement serp.txt
  python3 motscles.py cannibalisation gsc-requetes-pages.csv --marque assurly
  python3 motscles.py groupes gsc-requetes-pages.csv --json
"""

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
import urllib.parse
from collections import defaultdict
from itertools import combinations
from pathlib import Path

SEUIL_OMNIPRESENT = 0.6
# Plateformes généralistes : présentes dans presque toutes les SERP, elles ne disent rien de l'intention.
GENERIQUES = ("wikipedia.org", "youtube.com", "reddit.com", "quora.com", "facebook.com", "linkedin.com",
              "pinterest.com", "pinterest.fr", "instagram.com", "tiktok.com", "x.com", "twitter.com",
              "amazon.fr", "amazon.com", "doctissimo.fr", "commentcamarche.net", "leboncoin.fr")
SEUILS = ((7, "même page", "une seule page vise les deux requêtes"),
          (4, "même cluster", "deux pages distinctes, liées entre elles"),
          (2, "clusters voisins", "un lien croisé suffit"),
          (0, "sujets séparés", "aucun lien imposé"))


# ---------------------------------------------------------------- outils

def plier(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()


def normaliser_url(u):
    """Même page = même hôte (sans www), même chemin (sans / final), sans paramètres ni ancre."""
    u = u.strip()
    if not re.match(r"https?://", u, re.I):
        u = "https://" + u
    p = urllib.parse.urlsplit(u)
    hote = (p.hostname or "").lower()
    hote = hote[4:] if hote.startswith("www.") else hote
    chemin = re.sub(r"/+$", "", p.path) or "/"
    return f"{hote}{chemin}", hote


def lire_serp(chemin):
    texte = Path(chemin).read_text(encoding="utf-8-sig")
    if texte.lstrip().startswith("{"):
        d = json.loads(texte)
        return {k: [u for u in v if str(u).strip()] for k, v in d.items()}
    serp, courante = {}, None
    for ligne in texte.splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue
        if ligne.startswith("#"):
            courante = ligne.lstrip("#").strip()
            serp[courante] = []
        elif courante is not None and re.match(r"(https?://)?[\w.-]+\.\w{2,}", ligne):
            serp[courante].append(ligne.split()[0])
    return serp


COLONNES = {
    "requete": ("requete", "requetes", "query", "queries", "top queries", "requetes les plus frequentes", "search query"),
    "page": ("page", "pages", "landing page", "url", "page de destination", "top pages", "pages les plus populaires"),
    "clics": ("clics", "clicks", "url clicks"),
    "impressions": ("impressions",),
    "position": ("position", "position moyenne", "average position", "avg position"),
}


def nombre(v):
    t = re.sub(r"[\s  %]", "", str(v or "")).replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return 0.0


def lire_export(chemin):
    brut = Path(chemin).read_text(encoding="utf-8-sig")
    sep = ";" if brut.split("\n", 1)[0].count(";") > brut.split("\n", 1)[0].count(",") else ","
    lignes = list(csv.reader(io.StringIO(brut), delimiter=sep))
    if not lignes:
        raise SystemExit("export vide")
    entetes = [plier(h) for h in lignes[0]]
    idx = {}
    for cle, noms in COLONNES.items():
        for i, h in enumerate(entetes):
            if h in noms:
                idx[cle] = i
                break
    manquantes = [c for c in ("requete", "page", "impressions") if c not in idx]
    if manquantes:
        raise SystemExit(f"colonnes introuvables : {', '.join(manquantes)} (en-têtes lus : {', '.join(lignes[0])}). "
                         "Il faut un export qui croise requête et page.")
    out = []
    for l in lignes[1:]:
        if len(l) <= max(idx.values()) or not l[idx["requete"]].strip():
            continue
        out.append({"requete": l[idx["requete"]].strip(), "page": l[idx["page"]].strip(),
                    "clics": nombre(l[idx["clics"]]) if "clics" in idx else 0.0,
                    "impressions": nombre(l[idx["impressions"]]),
                    "position": nombre(l[idx["position"]]) if "position" in idx else None})
    return out


# ---------------------------------------------------------------- recouvrement

def recouvrement(serp, garder_omnipresents=False):
    alertes = []
    domaines = defaultdict(int)
    normes = {}
    for req, urls in serp.items():
        vus = []
        for u in urls[:10]:
            n, hote = normaliser_url(u)
            if n not in [x[0] for x in vus]:
                vus.append((n, hote))
        normes[req] = vus
        for hote in {h for _, h in vus}:
            domaines[hote] += 1
        if len(urls) < 8:
            alertes.append(f"« {req} » : {len(urls)} résultat(s) seulement, échantillon court")
    omni = set()
    if len(serp) >= 4 and not garder_omnipresents:
        omni = {d for d, n in domaines.items() if n / len(serp) >= SEUIL_OMNIPRESENT
                and any(d == g or d.endswith("." + g) for g in GENERIQUES)}
    ensembles = {r: {u for u, h in v if h not in omni} for r, v in normes.items()}
    for r, e in ensembles.items():
        if len(e) < 5:
            alertes.append(f"« {r} » : {len(e)} URL après retrait des domaines omniprésents, comparaison bruitée")
    paires = []
    for a, b in combinations(serp, 2):
        n = len(ensembles[a] & ensembles[b])
        verdict, conseil = next((v, c) for s, v, c in SEUILS if n >= s)
        paires.append({"a": a, "b": b, "communes": n, "verdict": verdict, "conseil": conseil,
                       "a_trancher": n in (4, 5, 6)})
    # Pages : requêtes reliées par « même page » (union des paires à 7 ou plus).
    parent = {r: r for r in serp}

    def racine(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for p in paires:
        if p["communes"] >= 7:
            parent[racine(p["a"])] = racine(p["b"])
    pages = defaultdict(list)
    for r in serp:
        pages[racine(r)].append(r)
    return {"omnipresents": sorted(omni), "paires": sorted(paires, key=lambda p: -p["communes"]),
            "pages": sorted(pages.values(), key=len, reverse=True), "alertes": alertes}


# ---------------------------------------------------------------- Search Console

def cannibalisation(lignes, marques=(), min_impr=10):
    par_req = defaultdict(list)
    for l in lignes:
        if any(plier(m) in plier(l["requete"]) for m in marques if m):
            continue
        par_req[l["requete"]].append(l)
    cas = []
    for req, ls in par_req.items():
        ls = sorted(ls, key=lambda x: -x["impressions"])
        total = sum(x["impressions"] for x in ls)
        if len(ls) < 2 or total < min_impr:
            continue
        p1, p2 = ls[0], ls[1]
        part2 = p2["impressions"] / p1["impressions"] if p1["impressions"] else 0
        if part2 < 0.2:
            continue
        clics = sum(x["clics"] for x in ls)
        domine = clics and max(x["clics"] for x in ls) / clics >= 0.8
        positions = [x["position"] for x in ls[:2] if x["position"]]
        if domine:
            piste = "une page reçoit 80% des clics ou plus : garder, vérifier que l'autre ne vise pas la même intention"
        elif positions and all(4 <= p <= 20 for p in positions):
            piste = "aucune page ne s'impose (positions 4 à 20) : fusionner ou différencier après relecture des deux pages"
        else:
            piste = "à relire : même intention (fusionner, rediriger) ou intentions différentes (différencier les titres)"
        cas.append({"requete": req, "impressions": total, "clics": clics,
                    "pages": [{"page": x["page"], "impressions": x["impressions"], "clics": x["clics"],
                               "position": x["position"]} for x in ls[:4]],
                    "part_seconde": round(part2, 2), "piste": piste})
    return sorted(cas, key=lambda c: -c["impressions"])


def groupes(lignes):
    par_req = defaultdict(list)
    for l in lignes:
        par_req[l["requete"]].append(l)
    pages = defaultdict(list)
    for req, ls in par_req.items():
        tete = max(ls, key=lambda x: (x["impressions"], x["clics"]))
        pages[tete["page"]].append({"requete": req, "impressions": tete["impressions"], "clics": tete["clics"],
                                    "position": tete["position"]})
    return sorted(({"page": p, "requetes": sorted(r, key=lambda x: -x["impressions"]),
                    "impressions": sum(x["impressions"] for x in r)} for p, r in pages.items()),
                  key=lambda g: -g["impressions"])


# ---------------------------------------------------------------- affichage

def virgule(x, d=1):
    return f"{x:.{d}f}".replace(".", ",") if x is not None else "n/a"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("recouvrement", help="recouvrement des SERP")
    r.add_argument("serp")
    r.add_argument("--garder-omnipresents", action="store_true")
    r.add_argument("--json", action="store_true")
    c = sub.add_parser("cannibalisation", help="requêtes partagées entre pages (Search Console)")
    c.add_argument("export")
    c.add_argument("--marque", action="append", default=[], help="requêtes de marque à ignorer (répétable)")
    c.add_argument("--min-impressions", type=int, default=10)
    c.add_argument("--json", action="store_true")
    g = sub.add_parser("groupes", help="requêtes regroupées par page (Search Console)")
    g.add_argument("export")
    g.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "recouvrement":
        try:
            serp = lire_serp(a.serp)
        except (OSError, json.JSONDecodeError) as e:
            print(f"SERP illisible : {e}", file=sys.stderr)
            return 1
        if len(serp) < 2:
            print("Il faut au moins deux requêtes avec leurs résultats.", file=sys.stderr)
            return 1
        res = recouvrement(serp, a.garder_omnipresents)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
        else:
            print(f"RECOUVREMENT · {len(serp)} requêtes · {len(res['pages'])} page(s) à prévoir")
            if res["omnipresents"]:
                print(f"  domaines retirés (présents dans 60% des SERP ou plus) : {', '.join(res['omnipresents'])}")
            print("\nPAGES")
            for i, p in enumerate(res["pages"], 1):
                print(f"  {i}. {p[0]}" + (f"  + {', '.join(p[1:])}" if len(p) > 1 else ""))
            print("\nPAIRES (URL communes sur 10)")
            for p in res["paires"]:
                if p["communes"] >= 2:
                    print(f"  {p['communes']:>2}  {p['a']}  ×  {p['b']}  → {p['verdict']}" + ("  (à trancher : l'intention décide)" if p["a_trancher"] else ""))
            if res["alertes"]:
                print("\nÀ REVOIR")
                for x in res["alertes"]:
                    print(f"  · {x}")
            print("\nSeuils de praticien, à confirmer sur ses données. Aucun volume : il vient d'un outil nommé.")
        return 2 if res["alertes"] or any(p["a_trancher"] for p in res["paires"]) else 0

    try:
        lignes = lire_export(a.export)
    except OSError as e:
        print(f"export illisible : {e}", file=sys.stderr)
        return 1
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 1

    if a.cmd == "cannibalisation":
        cas = cannibalisation(lignes, a.marque, a.min_impressions)
        if a.json:
            print(json.dumps(cas, ensure_ascii=False, indent=1))
        else:
            print(f"CANNIBALISATION · {len({l['requete'] for l in lignes})} requêtes lues · {len(cas)} partagée(s) entre pages")
            for x in cas:
                print(f"\n  « {x['requete']} » · {int(x['impressions'])} impressions, {int(x['clics'])} clics")
                for p in x["pages"]:
                    print(f"     {p['page']}  {int(p['impressions'])} impr. · {int(p['clics'])} clics · position {virgule(p['position'])}")
                print(f"     → {x['piste']}")
            if not cas:
                print("  Aucune requête partagée au-dessus des seuils.")
        return 2 if cas else 0

    gr = groupes(lignes)
    if a.json:
        print(json.dumps(gr, ensure_ascii=False, indent=1))
    else:
        print(f"GROUPES · {len(gr)} page(s) · {len({l['requete'] for l in lignes})} requêtes")
        for x in gr:
            tete = ", ".join(r["requete"] for r in x["requetes"][:5])
            print(f"\n  {x['page']} · {int(x['impressions'])} impressions · {len(x['requetes'])} requête(s)")
            print(f"     {tete}" + (" …" if len(x["requetes"]) > 5 else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
