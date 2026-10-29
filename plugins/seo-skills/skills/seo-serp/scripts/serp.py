#!/usr/bin/env python3
"""serp.py : ce que la SERP dit, mesuré sur un relevé (Python 3, sans dépendance).

  python3 serp.py releve.csv [--requete "…"] [--json]

Le relevé est fait par le Skill (lecture des pages) ou par l'utilisateur :
un CSV, une ligne par résultat organique, dans l'ordre. Colonnes (en-têtes
français, ordre libre ; seules position, url et type sont obligatoires) :

  position, url, type, auteur, date, mots, donnees, titre

  type     guide, liste, comparatif, produit, categorie, outil, local, forum,
           video, actualite, officiel, definition, accueil
  auteur   oui / non : auteur nommé et identifiable sur la page
  date     AAAA-MM-JJ de mise à jour affichée (vide si aucune)
  mots     longueur estimée de la page lue (nombre)
  donnees  oui / non : données, test ou expérience propres à la page

Éléments de la SERP en options : --ai-overview, --extrait-marque (extrait
optimisé tenu par une marque connue), --annonces N, --aujourdhui AAAA-MM-JJ.

Sortie :
  - CONSENSUS : type de page dominant (plus de 60% = consensus fort) ;
  - DIFFICULTÉ lue dans la SERP (directionnelle, jamais un score d'outil) :
    signaux comptés, facile / moyenne / difficile ;
  - NE PAS TENTER : signaux qui disent qu'une nouvelle page a très peu de
    chances (Wikipédia ou site public en tête sur une question
    réglementaire, forums dominants, actualité chaude, pages produits de
    marques sur une requête générique) ;
  - CONCURRENTS RÉELS : résultats comparables, sans plateformes ni sites
    publics (gardés comme sources).

Codes de sortie : 0 tentable · 2 difficile ou consensus faible · 3 « ne pas
tenter » · 1 erreur d'utilisation.

La difficulté est une lecture de praticien, pas une règle de Google : elle
guide la décision, elle ne la prend pas.
"""

import argparse
import csv
import datetime as dt
import io
import json
import re
import sys
import unicodedata
import urllib.parse
from collections import Counter
from pathlib import Path

TYPES = {"guide", "liste", "comparatif", "produit", "categorie", "outil", "local", "forum", "video",
         "actualite", "officiel", "definition", "accueil"}
OFFICIELS = ("service-public.fr", "gouv.fr", "legifrance.gouv.fr", "ameli.fr", "urssaf.fr", "impots.gouv.fr",
             "economie.gouv.fr", "cnil.fr", "has-sante.fr", "ordre", "europa.eu", "insee.fr", "banque-france.fr")
ENCYCLOPEDIES = ("wikipedia.org", "larousse.fr", "universalis.fr")
FORUMS = ("reddit.com", "quora.com", "doctissimo.fr", "commentcamarche.net", "forum", "jeuxvideo.com")
PLATEFORMES = ENCYCLOPEDIES + FORUMS + ("youtube.com", "facebook.com", "linkedin.com", "pinterest", "instagram.com",
                                        "tiktok.com", "amazon.", "pagesjaunes.fr", "leboncoin.fr", "trustpilot.com")
REGLEMENTAIRE = re.compile(r"\b(obligatoire|loi|droit|impot|impots|taxe|declaration|demarche|formulaire|aide|allocation|"
                           r"retraite|cotisation|urssaf|caf|cpf|permis|visa|titre de sejour|amende|delai legal)\b")


def plier(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()


def hote(url):
    u = url if re.match(r"https?://", url or "", re.I) else "https://" + (url or "")
    h = (urllib.parse.urlsplit(u).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def est(h, liste):
    return any(x in h for x in liste)


def lire(chemin):
    brut = Path(chemin).read_text(encoding="utf-8-sig")
    sep = ";" if brut.split("\n", 1)[0].count(";") > brut.split("\n", 1)[0].count(",") else ","
    lignes = list(csv.DictReader(io.StringIO(brut), delimiter=sep))
    out, erreurs = [], []
    for i, l in enumerate(lignes, 2):
        l = {plier(k): (v or "").strip() for k, v in l.items() if k}
        if not l.get("url"):
            continue
        t = plier(l.get("type", ""))
        if t not in TYPES:
            erreurs.append(f"ligne {i} : type « {l.get('type', '')} » inconnu ({', '.join(sorted(TYPES))})")
        try:
            mots = int(re.sub(r"\D", "", l.get("mots", "")) or 0) or None
        except ValueError:
            mots = None
        out.append({"position": int(re.sub(r"\D", "", l.get("position", "")) or len(out) + 1), "url": l["url"],
                    "hote": hote(l["url"]), "type": t, "auteur": plier(l.get("auteur", "")) == "oui",
                    "date": l.get("date", ""), "mots": mots, "donnees": plier(l.get("donnees", "")) == "oui",
                    "titre": l.get("titre", "")})
    return sorted(out, key=lambda r: r["position"]), erreurs


def analyser(res, requete="", ai_overview=False, extrait_marque=False, annonces=0, aujourdhui=None):
    aujourdhui = aujourdhui or dt.date.today()
    top10 = res[:10]
    types = Counter(r["type"] for r in top10)
    dominant, n = types.most_common(1)[0] if types else ("?", 0)
    part = n / len(top10) if top10 else 0
    consensus = "fort" if part > 0.6 else "partagé" if part >= 0.4 else "fragmenté"

    top3, top5 = top10[:3], top10[:5]
    signaux = []

    def signal(cond, texte):
        if cond:
            signaux.append(texte)
    signal(any(est(r["hote"], OFFICIELS + ENCYCLOPEDIES) for r in top3), "site public ou encyclopédie dans les 3 premiers")
    longs = [r["mots"] for r in top5 if r["mots"]]
    signal(len(longs) >= 3 and sorted(longs)[len(longs) // 2] >= 2000, "pages longues en tête (médiane des 5 premiers ≥ 2 000 mots)")
    signal(extrait_marque, "extrait optimisé tenu par une marque connue")
    signal(ai_overview, "AI Overview affiché (moins de clics vers les résultats)")
    signal(sum(r["auteur"] for r in top5) >= 3, "auteurs identifiés sur 3 des 5 premiers résultats ou plus")
    signal(sum(r["donnees"] for r in top5) >= 2, "données ou tests propres sur 2 des 5 premiers ou plus")
    recents = 0
    for r in top5:
        try:
            if (aujourdhui - dt.date.fromisoformat(r["date"])).days <= 365:
                recents += 1
        except ValueError:
            pass
    signal(recents >= 3, "pages mises à jour depuis moins d'un an sur 3 des 5 premiers ou plus")
    signal(annonces >= 3, f"{annonces} annonces payantes au-dessus des résultats")
    editorial_top3 = any(not est(r["hote"], PLATEFORMES + OFFICIELS) and r["type"] in ("guide", "liste", "comparatif", "definition")
                         for r in top3)
    signal(not editorial_top3, "aucune page éditoriale indépendante dans les 3 premiers")
    difficulte = "difficile" if len(signaux) >= 6 else "moyenne" if len(signaux) >= 3 else "facile"

    stop = []
    req = plier(requete)
    if any(est(r["hote"], ENCYCLOPEDIES) for r in top3) and types.get("definition", 0) + types.get("officiel", 0) >= 3:
        stop.append("Wikipédia en tête d'une SERP de définitions : la requête attend une définition neutre")
    if req and REGLEMENTAIRE.search(req) and any(est(r["hote"], OFFICIELS) for r in top3):
        stop.append("question réglementaire avec un site public dans les 3 premiers : viser plutôt une requête de cas pratique")
    if sum(est(r["hote"], FORUMS) or r["type"] == "forum" for r in top5) >= 3:
        stop.append("forums dominants dans les 5 premiers : la requête attend des avis vécus, pas un article")
    if sum(r["type"] == "actualite" for r in top5) >= 3:
        stop.append("actualité chaude : la SERP change chaque jour, une page pérenne n'y tiendra pas")
    if sum(r["type"] in ("produit", "categorie") for r in top10) >= 6 and types.get("guide", 0) + types.get("liste", 0) <= 1:
        stop.append("pages produits et catégories de marques sur une requête générique : un article n'y a pas sa place")

    concurrents = [r for r in top10 if not est(r["hote"], PLATEFORMES + OFFICIELS)]
    sources = [r for r in top10 if est(r["hote"], OFFICIELS + ENCYCLOPEDIES)]
    return {"requete": requete, "resultats": len(top10), "types": dict(types), "dominant": dominant,
            "part": round(part, 2), "consensus": consensus, "signaux": signaux, "difficulte": difficulte,
            "ne_pas_tenter": stop, "concurrents": [r["url"] for r in concurrents],
            "sources": [r["url"] for r in sources]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("releve")
    ap.add_argument("--requete", default="")
    ap.add_argument("--ai-overview", action="store_true")
    ap.add_argument("--extrait-marque", action="store_true")
    ap.add_argument("--annonces", type=int, default=0)
    ap.add_argument("--aujourdhui", help="AAAA-MM-JJ (tests)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        res, erreurs = lire(a.releve)
    except OSError as e:
        print(f"relevé illisible : {e}", file=sys.stderr)
        return 1
    if erreurs:
        print("\n".join(erreurs), file=sys.stderr)
        return 1
    if len(res) < 5:
        print(f"{len(res)} résultat(s) : il en faut 5 au moins pour lire une SERP.", file=sys.stderr)
        return 1
    auj = dt.date.fromisoformat(a.aujourdhui) if a.aujourdhui else None
    r = analyser(res, a.requete, a.ai_overview, a.extrait_marque, a.annonces, auj)
    code = 3 if r["ne_pas_tenter"] else 2 if r["difficulte"] == "difficile" or r["consensus"] == "fragmenté" else 0
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return code
    pc = round(r["part"] * 100)
    print(f"SERP · « {r['requete'] or '?'} » · {r['resultats']} résultats lus")
    print(f"  CONSENSUS    {r['dominant']} ({pc}%) · {r['consensus']} · " +
          ", ".join(f"{t} {n}" for t, n in sorted(r["types"].items(), key=lambda x: -x[1])))
    print(f"  DIFFICULTÉ   {r['difficulte']} (directionnelle) · {len(r['signaux'])} signal(s) sur 9")
    for s in r["signaux"]:
        print(f"               · {s}")
    if r["ne_pas_tenter"]:
        print("  NE PAS TENTER")
        for s in r["ne_pas_tenter"]:
            print(f"               · {s}")
    print(f"  CONCURRENTS  {len(r['concurrents'])} comparables · SOURCES À CITER {len(r['sources'])}")
    return code


if __name__ == "__main__":
    sys.exit(main())
