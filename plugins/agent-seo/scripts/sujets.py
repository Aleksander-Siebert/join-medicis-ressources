#!/usr/bin/env python3
"""
sujets.py : trouver les prochains articles à écrire, à partir de Search Console.

La partie mesurable du choix des sujets, sans IA (Python 3.9+, sans dépendance) :
lire les requêtes réelles du site, garder celles où il est presque visible,
regrouper celles qui veulent la même page, écarter ce qu'une page couvre déjà
et ce qui a déjà été écrit, puis classer. L'agent juge ensuite la pertinence.

Commandes :

  proposer EXPORT [--site URL] [--pages FICHIER] [--marque MOT …] [--exclure MOT …]
           [--min-impressions N] [--positions 8-40] [--max 10] [--json]
      EXPORT : requêtes × pages de Search Console, en CSV (colonnes requête,
      page, clics, impressions, position, en français ou en anglais) ou en JSON
      (liste d'objets avec les mêmes clés, ou réponse brute d'un connecteur).
      Écrit sujets.md et memoire/sujets.json.

  retenir REQUÊTE     marque le sujet « en cours » (il ne sera plus proposé)
  livrer REQUÊTE --fichier CHEMIN   marque le sujet livré, avec la date
  abandonner REQUÊTE [--raison TEXTE]   le sujet ne sera plus proposé
  bilan EXPORT [--jours 28]
      Pour chaque sujet livré depuis au moins N jours : impressions, clics et
      meilleure position de sa requête aujourd'hui. Ce qui marche guide les
      prochains choix.

Codes de sortie : 0 · 1 erreur d'utilisation · 2 rien à proposer.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
import urllib.parse
from datetime import date, datetime
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

# Mots sans poids pour comparer deux requêtes ou une requête et une adresse.
MOTS_VIDES = set(
    "le la les l un une des du de d au aux a à et ou en pour par sur dans avec sans ce cette ces son sa ses "
    "mon ma mes ton ta tes notre nos votre vos leur leurs qui que quoi quel quelle quels quelles comment "
    "pourquoi est sont the of for to in on and or with how what is are vs".split()
)

COLONNES = {
    "requete": ("requete", "requetes", "query", "queries", "keys", "top queries", "requetes les plus frequentes", "search query"),
    "page": ("page", "pages", "landing page", "url", "page de destination", "top pages", "pages les plus populaires"),
    "clics": ("clics", "clicks", "url clicks"),
    "impressions": ("impressions",),
    "position": ("position", "position moyenne", "average position", "avg position"),
}


# ------------------------------------------------------------------ outils


def plier(s) -> str:
    s = unicodedata.normalize("NFD", str(s or ""))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()


def mots(texte: str) -> list[str]:
    return [m for m in re.split(r"[^a-z0-9]+", plier(texte)) if m and m not in MOTS_VIDES and len(m) > 1]


def racine(m: str) -> str:
    """Pluriels et féminins simples ramenés au même mot (assurances -> assurance)."""
    for fin in ("aux", "es", "s", "e", "x"):
        if len(m) > 4 and m.endswith(fin):
            return m[: -len(fin)]
    return m


def cles(texte: str) -> set[str]:
    return {racine(m) for m in mots(texte)}


def nombre(v) -> float:
    if isinstance(v, (int, float)):
        return float(v)
    t = re.sub(r"[\s  %]", "", str(v or "")).replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return 0.0


def chemin_url(u: str) -> str:
    u = u.strip()
    if not re.match(r"https?://", u, re.I):
        u = "https://" + u
    p = urllib.parse.urlsplit(u)
    return re.sub(r"/+$", "", p.path) or "/"


def maintenant() -> date:
    return date.today()


# ------------------------------------------------------------------ lecture


def _ligne(d: dict) -> dict | None:
    """Une ligne de Search Console, quelle que soit la forme des clés."""
    pliees = {plier(k): v for k, v in d.items()}
    if "keys" in pliees and isinstance(pliees["keys"], list):  # API Search Console : keys = [requête, page]
        k = pliees["keys"]
        pliees.setdefault("query", k[0] if k else "")
        pliees.setdefault("page", k[1] if len(k) > 1 else "")
    trouve = {}
    for cle, noms in COLONNES.items():
        for n in noms:
            if n in pliees and n != "keys":
                trouve[cle] = pliees[n]
                break
    if not str(trouve.get("requete", "")).strip():
        return None
    return {
        "requete": str(trouve["requete"]).strip(),
        "page": str(trouve.get("page", "")).strip(),
        "clics": nombre(trouve.get("clics", 0)),
        "impressions": nombre(trouve.get("impressions", 0)),
        "position": nombre(trouve["position"]) if "position" in trouve else None,
    }


def lire_export(chemin: str) -> list[dict]:
    brut = Path(chemin).read_text(encoding="utf-8-sig").strip()
    if not brut:
        raise SystemExit("Export vide.")
    if brut[0] in "[{":
        d = json.loads(brut)
        if isinstance(d, dict):  # réponse d'un connecteur : la première liste trouvée
            d = next((v for v in d.values() if isinstance(v, list)), [])
        lignes = [l for l in (_ligne(x) for x in d if isinstance(x, dict)) if l]
    else:
        tete = brut.split("\n", 1)[0]
        sep = ";" if tete.count(";") > tete.count(",") else ("\t" if tete.count("\t") > tete.count(",") else ",")
        tableau = list(csv.reader(io.StringIO(brut), delimiter=sep))
        entetes = tableau[0]
        lignes = [l for l in (_ligne(dict(zip(entetes, r))) for r in tableau[1:]) if l]
    if not lignes:
        raise SystemExit("Aucune requête lue : il faut les colonnes requête et impressions (et page si possible).")
    if not any(l["page"] for l in lignes):
        print("ATTENTION : export sans colonne page, les pages existantes ne peuvent pas être repérées.", file=sys.stderr)
    return lignes


def lire_pages(chemin: str | None) -> list[str]:
    """Adresses des pages du site : sitemap XML, ou une adresse par ligne."""
    if not chemin:
        return []
    texte = Path(chemin).read_text(encoding="utf-8-sig")
    urls = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", texte) or [l.strip() for l in texte.splitlines() if l.strip().startswith(("http", "/"))]
    return urls


# ------------------------------------------------------------------ mémoire


def charger_memoire() -> dict:
    f = RACINE / "memoire" / "sujets.json"
    if f.exists():
        try:
            return json.loads(f.read_text("utf-8"))
        except json.JSONDecodeError:
            pass
    return {"sujets": {}}


def sauver_memoire(m: dict) -> None:
    (RACINE / "memoire").mkdir(exist_ok=True)
    (RACINE / "memoire" / "sujets.json").write_text(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True), "utf-8")


def cle_sujet(requete: str) -> str:
    return " ".join(sorted(cles(requete)))


def deja_traite(requete: str, memoire: dict) -> dict | None:
    k = cles(requete)
    for cle, s in memoire["sujets"].items():
        if s.get("etat") not in ("en cours", "livré", "abandonné"):
            continue
        autre = set(cle.split())
        if k and autre and len(k & autre) / len(k | autre) >= 0.6:
            return s
    return None


# ------------------------------------------------------------------ proposer


def page_qui_couvre(requete: str, pages: list[str]) -> str | None:
    """Une page dont l'adresse reprend au moins 70% des mots de la requête : la requête est déjà son sujet."""
    k = cles(requete)
    if not k:
        return None
    meilleure, score = None, 0.0
    for p in pages:
        c = cles(chemin_url(p).replace("/", " "))
        part = len(k & c) / len(k)
        if part > score:
            meilleure, score = p, part
    return meilleure if score >= 0.7 else None


def potentiel(position: float | None) -> float:
    """Gain possible selon la position actuelle. Règle de travail, pas une mesure :
    juste derrière la première page, le gain d'un article dédié est le plus probable."""
    if position is None:
        return 0.5
    if position < 8:
        return 0.2
    if position <= 15:
        return 1.0
    if position <= 30:
        return 0.7
    return 0.4


def proposer(lignes, pages, marques=(), exclus=(), min_impr=20, positions=(8, 40), maxi=10, memoire=None):
    memoire = memoire or {"sujets": {}}
    toutes_pages = sorted({l["page"] for l in lignes if l["page"]} | set(pages))
    marques_p = [plier(m) for m in marques if m.strip()]
    exclus_p = [plier(m) for m in exclus if m.strip()]

    # 1. une ligne par requête : total des impressions, meilleure position, page qui reçoit le plus
    par_requete: dict[str, dict] = {}
    for l in lignes:
        r = par_requete.setdefault(plier(l["requete"]), {"requete": l["requete"], "impressions": 0.0, "clics": 0.0, "position": None, "pages": {}})
        r["impressions"] += l["impressions"]
        r["clics"] += l["clics"]
        if l["position"]:
            r["position"] = l["position"] if r["position"] is None else min(r["position"], l["position"])
        if l["page"]:
            r["pages"][l["page"]] = r["pages"].get(l["page"], 0) + l["impressions"]

    # requêtes où le site est déjà bien placé : leurs variantes reviennent à la même page
    bien_placees = [(cles(r["requete"]), max(r["pages"], key=r["pages"].get) if r["pages"] else None, r["requete"])
                    for r in par_requete.values() if r["position"] is not None and r["position"] < positions[0]
                    and not any(re.search(rf"\b{re.escape(m)}\b", plier(r["requete"])) for m in marques_p)]

    ecartes = {"marque": 0, "exclus": 0, "peu_vue": 0, "deja_bien_placee": 0, "trop_loin": 0, "page_existante": [], "deja_traite": 0}
    candidats = []
    for r in par_requete.values():
        rp = plier(r["requete"])
        if any(re.search(rf"\b{re.escape(m)}\b", rp) for m in marques_p):
            ecartes["marque"] += 1
            continue
        if any(m in rp for m in exclus_p):
            ecartes["exclus"] += 1
            continue
        if r["impressions"] < min_impr:
            ecartes["peu_vue"] += 1
            continue
        if r["position"] is not None and r["position"] < positions[0]:
            ecartes["deja_bien_placee"] += 1
            continue
        if r["position"] is not None and r["position"] > positions[1]:
            ecartes["trop_loin"] += 1
            continue
        couvre = page_qui_couvre(r["requete"], toutes_pages)
        if not couvre:
            k = cles(r["requete"])
            for kb, page, _ in bien_placees:
                if page and k and kb and (kb <= k or len(k & kb) / len(k | kb) >= 0.6):
                    couvre = page  # variante d'une requête où cette page est déjà bien placée
                    break
        if couvre:
            ecartes["page_existante"].append({"requete": r["requete"], "page": couvre, "position": r["position"], "impressions": r["impressions"]})
            continue
        if deja_traite(r["requete"], memoire):
            ecartes["deja_traite"] += 1
            continue
        candidats.append(r)

    # 2. regrouper les requêtes qui veulent la même page (mêmes mots, à l'ordre près)
    sujets: list[dict] = []
    for r in sorted(candidats, key=lambda x: -x["impressions"]):
        k = cles(r["requete"])
        cible = None
        for s in sujets:
            ks = s["_cles"]
            if k and ks and (k <= ks or ks <= k or len(k & ks) / len(k | ks) >= 0.6):
                cible = s
                break
        if cible:
            cible["requetes"].append(r["requete"])
            cible["impressions"] += r["impressions"]
            cible["clics"] += r["clics"]
            if r["position"] is not None:
                cible["position"] = r["position"] if cible["position"] is None else min(cible["position"], r["position"])
            for p, n in r["pages"].items():
                cible["pages"][p] = cible["pages"].get(p, 0) + n
            continue
        sujets.append({"requete": r["requete"], "requetes": [r["requete"]], "impressions": r["impressions"], "clics": r["clics"],
                       "position": r["position"], "pages": dict(r["pages"]), "_cles": k})

    for s in sujets:
        s["score"] = round(s["impressions"] * potentiel(s["position"]))
        s["page_actuelle"] = max(s["pages"], key=s["pages"].get) if s["pages"] else None
        del s["_cles"], s["pages"]
    sujets.sort(key=lambda s: (-s["score"], s["requete"]))
    return {"sujets": sujets[:maxi], "en_trop": max(0, len(sujets) - maxi), "ecartes": ecartes, "lues": len(par_requete)}


def ecrire_sujets_md(res: dict, chemin: Path, source: str) -> None:
    l = [
        "# Sujets proposés",
        "",
        f"Mis à jour le {maintenant().isoformat()} par `scripts/sujets.py`, à partir de {source}.",
        f"{res['lues']} requêtes lues. Le score = impressions × potentiel de la position (règle de travail, pas une prévision).",
        "",
        "| # | Requête principale | Requêtes du même sujet | Impressions | Meilleure position | Page qui ressort aujourd'hui | Score |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, s in enumerate(res["sujets"], 1):
        autres = ", ".join(r for r in s["requetes"][1:6]) or "aucune"
        pos = f"{s['position']:.1f}".replace(".", ",") if s["position"] is not None else "?"
        l.append(f"| {i} | {s['requete']} | {autres} | {int(s['impressions'])} | {pos} | {s['page_actuelle'] or 'aucune'} | {s['score']} |")
    if not res["sujets"]:
        l.append("| | Aucun sujet : voir les écartés ci-dessous. | | | | | |")
    e = res["ecartes"]
    l += [
        "",
        "## Écartés",
        "",
        f"- Requêtes de marque : {e['marque']}",
        f"- Mots exclus : {e['exclus']}",
        f"- Trop peu vues : {e['peu_vue']}",
        f"- Déjà bien placées (avant la position de départ) : {e['deja_bien_placee']}",
        f"- Trop loin (après la position limite) : {e['trop_loin']}",
        f"- Déjà écrites, en cours ou abandonnées : {e['deja_traite']}",
        f"- Déjà le sujet d'une page du site : {len(e['page_existante'])} (à mettre à jour plutôt qu'à réécrire, avec /seo-refresh)",
    ]
    for p in e["page_existante"][:10]:
        pos = f"{p['position']:.1f}".replace(".", ",") if p["position"] is not None else "?"
        l.append(f"  - « {p['requete']} » → {p['page']} (position {pos}, {int(p['impressions'])} impressions)")
    chemin.write_text("\n".join(l) + "\n", "utf-8")


# ------------------------------------------------------------------ suivi


def marquer(requete: str, etat: str, **plus) -> str:
    m = charger_memoire()
    cle = cle_sujet(requete)
    s = m["sujets"].setdefault(cle, {"requete": requete})
    s.update({"etat": etat, f"{etat.replace(' ', '_')}_le": maintenant().isoformat(), **{k: v for k, v in plus.items() if v}})
    sauver_memoire(m)
    return f"« {requete} » : {etat}."


def bilan(lignes: list[dict], jours: int = 28) -> list[dict]:
    m = charger_memoire()
    par_requete: dict[str, dict] = {}
    for l in lignes:
        r = par_requete.setdefault(cle_sujet(l["requete"]), {"impressions": 0.0, "clics": 0.0, "position": None})
        r["impressions"] += l["impressions"]
        r["clics"] += l["clics"]
        if l["position"]:
            r["position"] = l["position"] if r["position"] is None else min(r["position"], l["position"])
    sortie = []
    for cle, s in sorted(m["sujets"].items()):
        if s.get("etat") != "livré" or not s.get("livré_le"):
            continue
        age = (maintenant() - datetime.strptime(s["livré_le"], "%Y-%m-%d").date()).days
        if age < jours:
            continue
        now = par_requete.get(cle)
        sortie.append({"requete": s["requete"], "livré_le": s["livré_le"], "jours": age, "fichier": s.get("fichier"),
                       "impressions": now["impressions"] if now else 0, "clics": now["clics"] if now else 0,
                       "position": now["position"] if now else None, "avant": {"impressions": s.get("impressions"), "position": s.get("position")}})
    return sortie


# ------------------------------------------------------------------ commande


def main(argv: list[str] | None = None) -> int:
    for flux in (sys.stdout, sys.stderr):  # Windows : console pas en UTF-8 par défaut
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Trouver les prochains articles à écrire, à partir de Search Console")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("proposer")
    p.add_argument("export")
    p.add_argument("--pages", help="sitemap XML ou liste d'adresses du site")
    p.add_argument("--marque", nargs="*", default=[])
    p.add_argument("--exclure", nargs="*", default=[])
    p.add_argument("--min-impressions", type=int, default=20)
    p.add_argument("--positions", default="8-40", help="positions de départ et limite, ex. 8-40")
    p.add_argument("--max", type=int, default=10)
    p.add_argument("--json", action="store_true")
    for nom in ("retenir", "abandonner"):
        q = sub.add_parser(nom)
        q.add_argument("requete")
        q.add_argument("--raison")
    q = sub.add_parser("livrer")
    q.add_argument("requete")
    q.add_argument("--fichier", required=True)
    b = sub.add_parser("bilan")
    b.add_argument("export")
    b.add_argument("--jours", type=int, default=28)
    a = ap.parse_args(argv)

    if a.cmd == "proposer":
        try:
            debut, fin = (int(x) for x in a.positions.split("-"))
        except ValueError:
            print("--positions s'écrit début-fin, par exemple 8-40.", file=sys.stderr)
            return 1
        res = proposer(lire_export(a.export), lire_pages(a.pages), a.marque, a.exclure, a.min_impressions, (debut, fin), a.max, charger_memoire())
        ecrire_sujets_md(res, RACINE / "sujets.md", Path(a.export).name)
        m = charger_memoire()
        for s in res["sujets"]:
            entree = m["sujets"].setdefault(cle_sujet(s["requete"]), {"requete": s["requete"]})
            if entree.get("etat") in (None, "proposé"):
                entree.update({"etat": "proposé", "proposé_le": maintenant().isoformat(), "impressions": s["impressions"], "position": s["position"]})
        sauver_memoire(m)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
        else:
            print(f"{res['lues']} requêtes lues, {len(res['sujets'])} sujets proposés dans sujets.md"
                  + (f" ({res['en_trop']} de plus non affichés)" if res["en_trop"] else "") + ".")
            for i, s in enumerate(res["sujets"][:5], 1):
                print(f"  {i}. {s['requete']} : {int(s['impressions'])} impressions, score {s['score']}")
            n = len(res["ecartes"]["page_existante"])
            if n:
                print(f"{n} requêtes sont déjà le sujet d'une page du site : à mettre à jour, pas à réécrire (liste dans sujets.md).")
        return 0 if res["sujets"] else 2
    if a.cmd in ("retenir", "abandonner"):
        print(marquer(a.requete, "en cours" if a.cmd == "retenir" else "abandonné", raison=a.raison))
        return 0
    if a.cmd == "livrer":
        print(marquer(a.requete, "livré", fichier=a.fichier))
        return 0
    if a.cmd == "bilan":
        res = bilan(lire_export(a.export), a.jours)
        if not res:
            print(f"Aucun article livré depuis au moins {a.jours} jours : pas encore de bilan.")
            return 0
        for r in res:
            pos = f"{r['position']:.1f}".replace(".", ",") if r["position"] is not None else "absente"
            print(f"- « {r['requete']} » (livré il y a {r['jours']} jours) : {int(r['impressions'])} impressions, {int(r['clics'])} clics, position {pos}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
