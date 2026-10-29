#!/usr/bin/env python3
"""positions.py : quelles pages mettre à jour en premier, d'après Search Console.

Trois commandes, sans dépendance :

  paniers EXPORT [--precedent EXPORT] [--min-impressions 100] [--marque MOT …] [--json]
      Range les paires requête × page en trois paniers :
        à portée       position 8 à 20, impressions au-dessus du plancher :
                       contenu et liens ;
        clic faible    position 1 à 5, CTR nettement sous celui des autres
                       pages du site à position comparable : title et
                       description seulement ;
        presque en tête  position 4 à 7 : contenu, liens, format d'extrait.
      Le CTR attendu est calculé sur le site lui-même (médiane de sa tranche
      de position), jamais sur une courbe générique. Une requête servie par
      plusieurs pages est sortie des paniers : cannibalisation à régler avant
      (/seo-keywords). Avec --precedent, une hausse d'impressions de plus de
      3 fois est marquée « pic » (à confirmer sur la période suivante).

  noter JOURNAL --page URL --requete "…" --export EXPORT --changement "…" [--date AAAA-MM-JJ]
      Inscrit une modification au journal avec le point de départ mesuré
      (position, impressions, CTR).

  bilan JOURNAL --export EXPORT [--aujourdhui AAAA-MM-JJ] [--json]
      Pour chaque modification : attendre (moins de 21 jours), effet,
      sans effet. Deux tours sans effet sur la même page : arrêter d'y
      toucher (l'obstacle est l'intention ou l'autorité, pas le texte).

Export : CSV requête × page de Search Console (API, Looker Studio ou
connecteur ; l'interface seule ne croise pas les deux). Colonnes reconnues en
français ou en anglais : requête/query, page, clics/clicks, impressions,
ctr, position. Le CTR est recalculé (clics ÷ impressions) s'il manque.

Inspiré de la référence « rankings push » de marketingskills (Corey Haines,
MIT) : paniers, plus petit changement, attendre 3 à 4 semaines, arrêter
après deux tours sans effet. Les seuils sont des réglages, pas des règles de
Google.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import statistics
import sys
import unicodedata
from datetime import date
from pathlib import Path

COLONNES = {
    "requete": ("requete", "requetes", "query", "queries", "top queries", "requetes les plus frequentes", "search query"),
    "page": ("page", "pages", "landing page", "url", "page de destination", "top pages", "pages les plus populaires"),
    "clics": ("clics", "clicks", "url clicks"),
    "impressions": ("impressions",),
    "ctr": ("ctr", "taux de clics", "url ctr"),
    "position": ("position", "position moyenne", "average position", "avg position"),
}
ATTENTE_JOURS = 21
GAIN_POSITION = 1.0   # une place gagnée au moins
GAIN_CTR = 0.2        # ou +20% de CTR relatif (panier « clic faible »)


class Erreur(Exception):
    pass


def plier(s: str) -> str:
    s = unicodedata.normalize("NFD", (s or "").strip().lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def nombre(v) -> float:
    t = re.sub(r"[\s  %]", "", str(v or "")).replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return 0.0


def lire_export(chemin: str) -> list[dict]:
    try:
        brut = Path(chemin).read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise Erreur(f"export illisible : {chemin} ({exc})") from exc
    tete = brut.split("\n", 1)[0]
    sep = ";" if tete.count(";") > tete.count(",") else ","
    lignes = list(csv.reader(io.StringIO(brut), delimiter=sep))
    if not lignes:
        raise Erreur("export vide")
    entetes = [plier(h) for h in lignes[0]]
    idx = {}
    for cle, noms in COLONNES.items():
        for i, h in enumerate(entetes):
            if h in noms:
                idx[cle] = i
                break
    manque = [c for c in ("requete", "page", "impressions", "position") if c not in idx]
    if manque:
        raise Erreur(f"colonnes introuvables : {', '.join(manque)} (en-têtes lus : {', '.join(lignes[0])}). "
                     "Il faut un export qui croise requête et page, avec la position.")
    out = []
    for l in lignes[1:]:
        if len(l) <= max(idx.values()) or not l[idx["requete"]].strip():
            continue
        impr = nombre(l[idx["impressions"]])
        clics = nombre(l[idx["clics"]]) if "clics" in idx else 0.0
        if "ctr" in idx and l[idx["ctr"]].strip():
            ctr = nombre(l[idx["ctr"]])
            ctr = ctr / 100 if ctr > 1 or "%" in l[idx["ctr"]] else ctr
        else:
            ctr = clics / impr if impr else 0.0
        out.append({"requete": l[idx["requete"]].strip(), "page": l[idx["page"]].strip(), "clics": clics,
                    "impressions": impr, "ctr": ctr, "position": nombre(l[idx["position"]])})
    if not out:
        raise Erreur("aucune ligne exploitable dans l'export")
    return out


def tranche(pos: float) -> int:
    return max(1, int(round(pos)))


def paniers(lignes: list[dict], precedent: list[dict] | None = None, min_impr: float = 100,
            marques: tuple = ()) -> dict:
    marques = tuple(plier(m) for m in marques if m)
    hors_marque = [l for l in lignes if not any(m in plier(l["requete"]) for m in marques)]

    # Cannibalisation : une requête, plusieurs pages avec des impressions.
    pages_par_req: dict[str, set] = {}
    for l in hors_marque:
        if l["impressions"] > 0:
            pages_par_req.setdefault(l["requete"], set()).add(l["page"])
    canni = {r for r, p in pages_par_req.items() if len(p) > 1}

    # CTR attendu : médiane du site par tranche de position (1, 2, 3…), 5 lignes au moins.
    par_tranche: dict[int, list[float]] = {}
    for l in hors_marque:
        if l["impressions"] >= min_impr / 2:
            par_tranche.setdefault(tranche(l["position"]), []).append(l["ctr"])
    attendu = {t: statistics.median(v) for t, v in par_tranche.items() if len(v) >= 5}

    avant = {(p["requete"], p["page"]): p for p in (precedent or [])}
    res = {"a_portee": [], "clic_faible": [], "presque_en_tete": [], "cannibalisation": sorted(canni),
           "ctr_attendu": {str(t): round(v, 4) for t, v in sorted(attendu.items())},
           "tranches_sans_reference": sorted(t for t in range(1, 6) if t not in attendu)}
    for l in hors_marque:
        if l["requete"] in canni:
            continue
        item = dict(l)
        a = avant.get((l["requete"], l["page"]))
        if precedent is not None:
            item["pic"] = bool(a is None or (a["impressions"] and l["impressions"] > 3 * a["impressions"]))
        pos = l["position"]
        if 8 <= pos <= 20 and l["impressions"] >= min_impr:
            res["a_portee"].append(item)
        if 4 <= pos < 8 and l["impressions"] >= min_impr:
            res["presque_en_tete"].append(item)
        if 1 <= pos <= 5 and l["impressions"] >= min_impr:
            ref = attendu.get(tranche(pos))
            if ref is not None and l["ctr"] < 0.5 * ref:
                item["ctr_attendu"] = round(ref, 4)
                res["clic_faible"].append(item)
    for k in ("a_portee", "presque_en_tete"):
        res[k].sort(key=lambda x: -x["impressions"])
    res["clic_faible"].sort(key=lambda x: -(x["ctr_attendu"] - x["ctr"]) * x["impressions"])
    res["min_impressions"] = min_impr
    return res


def pct(x: float) -> str:
    return f"{x * 100:.1f}%".replace(".", ",")


def pos_txt(x: float) -> str:
    return f"{x:.1f}".replace(".", ",")


def afficher_paniers(r: dict) -> str:
    out = [f"PANIERS · plancher {r['min_impressions']:g} impressions sur la période"]
    def ligne(x, extra=""):
        pic = " · PIC (à confirmer)" if x.get("pic") else ""
        return f"    {pos_txt(x['position']):>5}  {x['impressions']:>7g} impr.  {pct(x['ctr']):>6}  {x['requete']} → {x['page']}{extra}{pic}"
    out.append(f"  À PORTÉE (8 à 20) · {len(r['a_portee'])} · contenu et liens")
    out += [ligne(x) for x in r["a_portee"][:20]]
    out.append(f"  PRESQUE EN TÊTE (4 à 7) · {len(r['presque_en_tete'])} · contenu, liens, format d'extrait")
    out += [ligne(x) for x in r["presque_en_tete"][:20]]
    out.append(f"  CLIC FAIBLE (1 à 5) · {len(r['clic_faible'])} · title et description seulement")
    out += [ligne(x, f" · attendu ≈ {pct(x['ctr_attendu'])} (médiane du site)") for x in r["clic_faible"][:20]]
    if r["tranches_sans_reference"]:
        out.append(f"  CTR attendu non calculé pour les positions {', '.join(map(str, r['tranches_sans_reference']))} "
                   "(moins de 5 lignes) : pas de verdict « clic faible » sur ces positions.")
    if r["cannibalisation"]:
        out.append(f"  CANNIBALISATION · {len(r['cannibalisation'])} requête(s) servies par plusieurs pages, sorties des paniers :")
        out += [f"    {q}" for q in r["cannibalisation"][:15]]
        out.append("    → régler d'abord avec /seo-keywords (motscles.py cannibalisation).")
    out.append("SUITE · Classe par valeur pour l'entreprise, pas par impressions. Une page à la fois, le plus petit changement.")
    return "\n".join(out)


# ---------------------------------------------------------------- journal

def charger_journal(chemin: str) -> list[dict]:
    p = Path(chemin)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def trouver(lignes: list[dict], page: str, requete: str) -> dict | None:
    return next((l for l in lignes if l["page"] == page and plier(l["requete"]) == plier(requete)), None)


def noter(journal: str, page: str, requete: str, lignes: list[dict], changement: str, jour: str) -> dict:
    l = trouver(lignes, page, requete)
    if l is None:
        raise Erreur(f"« {requete} » sur {page} absent de l'export : point de départ introuvable")
    j = charger_journal(journal)
    tour = 1 + sum(1 for e in j if e["page"] == page)
    entree = {"date": jour, "page": page, "requete": requete, "changement": changement, "tour": tour,
              "depart": {"position": l["position"], "impressions": l["impressions"], "ctr": round(l["ctr"], 4)}}
    j.append(entree)
    Path(journal).write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return entree


def bilan(journal: list[dict], lignes: list[dict], aujourdhui: date) -> list[dict]:
    res = []
    sans_effet: dict[str, int] = {}
    for e in sorted(journal, key=lambda x: x["date"]):
        jours = (aujourdhui - date.fromisoformat(e["date"])).days
        l = trouver(lignes, e["page"], e["requete"])
        r = {**e, "jours": jours}
        if jours < ATTENTE_JOURS:
            r["verdict"] = f"attendre ({ATTENTE_JOURS - jours} jours)"
        elif l is None:
            r["verdict"] = "absente de l'export : vérifier l'indexation et la période"
        else:
            d = e["depart"]
            gain_pos = d["position"] - l["position"]
            gain_ctr = (l["ctr"] - d["ctr"]) / d["ctr"] if d["ctr"] else 0.0
            r["actuel"] = {"position": l["position"], "impressions": l["impressions"], "ctr": round(l["ctr"], 4)}
            if gain_pos >= GAIN_POSITION or gain_ctr >= GAIN_CTR:
                r["verdict"] = "effet"
            else:
                sans_effet[e["page"]] = sans_effet.get(e["page"], 0) + 1
                r["verdict"] = "sans effet"
                if sans_effet[e["page"]] >= 2:
                    r["verdict"] = "sans effet, 2e tour : arrêter de modifier cette page"
        res.append(r)
    return res


def afficher_bilan(res: list[dict]) -> str:
    out = ["BILAN DES MODIFICATIONS"]
    for r in res:
        d = r["depart"]
        a = r.get("actuel")
        mesure = (f"position {pos_txt(d['position'])} → {pos_txt(a['position'])}, CTR {pct(d['ctr'])} → {pct(a['ctr'])}"
                  if a else f"départ : position {pos_txt(d['position'])}, CTR {pct(d['ctr'])}")
        out.append(f"  {r['date']} · tour {r['tour']} · {r['requete']} → {r['page']}")
        out.append(f"    {r['changement']} · {mesure} · {r['verdict']}")
    out.append("Une variation n'est pas une preuve : saison, mise à jour Google ou concurrent peuvent l'expliquer (registre dans commun/preuves.md).")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Paniers de mise à jour et journal des modifications, d'après Search Console.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("paniers")
    p.add_argument("export")
    p.add_argument("--precedent")
    p.add_argument("--min-impressions", type=float, default=100)
    p.add_argument("--marque", action="append", default=[])
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("noter")
    p.add_argument("journal")
    p.add_argument("--page", required=True)
    p.add_argument("--requete", required=True)
    p.add_argument("--export", required=True)
    p.add_argument("--changement", required=True)
    p.add_argument("--date", default=date.today().isoformat())
    p = sub.add_parser("bilan")
    p.add_argument("journal")
    p.add_argument("--export", required=True)
    p.add_argument("--aujourdhui", default=date.today().isoformat())
    p.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "paniers":
            r = paniers(lire_export(a.export), lire_export(a.precedent) if a.precedent else None, a.min_impressions, tuple(a.marque))
            print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher_paniers(r))
        elif a.cmd == "noter":
            e = noter(a.journal, a.page, a.requete, lire_export(a.export), a.changement, a.date)
            print(f"NOTÉ · tour {e['tour']} · {e['requete']} → {e['page']} · départ position {pos_txt(e['depart']['position'])}, "
                  f"CTR {pct(e['depart']['ctr'])} · bilan dans {ATTENTE_JOURS} jours au plus tôt")
        else:
            res = bilan(charger_journal(a.journal), lire_export(a.export), date.fromisoformat(a.aujourdhui))
            print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else afficher_bilan(res))
        return 0
    except (Erreur, ValueError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
