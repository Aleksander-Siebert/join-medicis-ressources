#!/usr/bin/env python3
"""sources.py : quels sites tiers façonnent les réponses où la marque perd ?

Part de la mesure de /geo-visibilite (`visibilite.py mesurer … --json`) :
les questions perdues (la marque absente, des concurrents nommés) et les
domaines que les moteurs y citent. Sortie : la liste des sites tiers à
travailler, classés par nombre de questions perdues où ils sont cités, avec
leur classe (comparateur, presse, communauté, avis, référence…) et l'action
qui convient à cette classe.

  python3 sources.py mesure.json
  python3 sources.py mesure.json --reponses reponses.txt --marque "Assurly" --verifier
      --reponses retrouve les URL exactes citées ; --verifier ouvre chaque
      page tierce et dit si la marque y figure (et quels concurrents) :
      « cité sur une question perdue, la marque absente de la page » est la
      ligne la plus utile du plan.

Python 3 sans dépendance. Code 0 ; 1 si la mesure est illisible.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ICI = Path(__file__).resolve().parent
for cand in (ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (cand / "sources_fr.json").exists():
        COMMUN = cand
        sys.path.insert(0, str(cand))
        break
else:  # pragma: no cover
    sys.exit("commun/ introuvable : lance outils/propager.py")
import page as pg  # noqa: E402

ACTIONS = {
    "comparateur": "demander à être évalué ou mis à jour, fournir des données exactes et datées ; jamais payer un classement non signalé",
    "presse": "proposer une donnée propre (étude, baromètre) ou un expert nommé au journaliste qui couvre le sujet",
    "consommateurs": "vérifier la fiche et les informations ; répondre aux questions et réclamations publiquement",
    "communaute": "répondre en son nom, avec transparence, là où la question est posée ; jamais de faux compte",
    "marketplace": "fiche complète et exacte (nom, offre, prix, photos) ; avis collectés selon L111-7-2",
    "reference": "Wikipédia et Wikidata : proposer des corrections sourcées, déclarer son lien avec la marque",
    "institution": "rien à obtenir ; vérifier que la page de la marque reprend exactement ces règles",
    "concurrent": "le concurrent a la page qui répond : /geo-contenu, la page qui manque avec un vrai gain d'information",
    "autre": "ouvrir la page : blog, média de niche ou annuaire ? Classer, puis appliquer l'action de la classe",
}


def norm(t: str) -> str:
    t = unicodedata.normalize("NFD", t or "")
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", t.lower().replace("’", "'")).strip()


def classes():
    d = json.loads((COMMUN / "sources_fr.json").read_text(encoding="utf-8"))
    return {k.lower(): v for k, v in d.get("domaines", {}).items()}


def racine(dom: str, connus) -> str:
    parts = dom.split(".")
    for i in range(len(parts) - 1):
        cand = ".".join(parts[i:])
        if cand in connus:
            return cand
    return ".".join(parts[-2:]) if len(parts) >= 2 else dom


RE_URL = re.compile(r"https?://[^\s)\]>\"'<]+", re.I)
RE_TETE = re.compile(r"(?m)^===\s*(.+?)\s*$")


def urls_citees(chemin: str) -> dict[tuple[str, str], list[str]]:
    """(id de question, domaine) -> URL citées, lues dans le fichier de réponses collées.
    L'id est celui de l'en-tête « === Moteur | id | question » (sinon la question)."""
    brut = Path(chemin).read_text(encoding="utf-8-sig")
    tetes = list(RE_TETE.finditer(brut))
    out = defaultdict(list)
    for i, m in enumerate(tetes):
        champs = [c.strip() for c in m.group(1).split("|")]
        ident = champs[1] if len(champs) >= 3 else champs[-1]
        corps = brut[m.end():tetes[i + 1].start() if i + 1 < len(tetes) else len(brut)]
        for u in RE_URL.findall(corps):
            u = u.rstrip(".,;:!?»")
            d = re.sub(r"^www\.", "", re.match(r"https?://([^/:?#]+)", u, re.I).group(1).lower())
            if u not in out[(ident, d)]:
                out[(ident, d)].append(u)
    return out


def analyser(mesure: dict, marque_domaines=(), concurrents_domaines=(), extra=None) -> dict:
    connus = {**classes(), **(extra or {})}
    perdues = mesure.get("perdues", [])
    sur_perdues = defaultdict(lambda: {"paires": 0, "questions": set(), "moteurs": set(), "concurrents": Counter()})
    for p in perdues:
        for d, n in p.get("sources", {}).items():
            x = sur_perdues[d]
            x["paires"] += 1
            x["questions"].add(p["id"])
            x["moteurs"].add(p["moteur"])
            x["concurrents"].update(p.get("concurrents", {}))
    total = mesure.get("sources", {})
    lignes = []
    for d in set(total) | set(sur_perdues):
        if any(d == m or d.endswith("." + m) for m in marque_domaines):
            continue
        if any(d == c or d.endswith("." + c) for c in concurrents_domaines):
            classe = "concurrent"
        else:
            classe = connus.get(racine(d, connus), "autre")
        x = sur_perdues.get(d)
        lignes.append({"domaine": d, "classe": classe, "perdues": x["paires"] if x else 0,
                       "questions": sorted(x["questions"]) if x else [], "moteurs": sorted(x["moteurs"]) if x else [],
                       "concurrents": dict(x["concurrents"].most_common(4)) if x else {},
                       "citations": total.get(d, 0), "action": ACTIONS.get(classe, ACTIONS["autre"])})
    lignes.sort(key=lambda l: (-l["perdues"], -l["citations"], l["domaine"]))
    par_classe = Counter()
    for l in lignes:
        par_classe[l["classe"]] += l["perdues"]
    return {"lignes": lignes, "par_classe": dict(par_classe.most_common()), "perdues": len(perdues),
            "questions": mesure.get("questions"), "etiquette": mesure.get("etiquette", "")}


def verifier(lignes, urls, marque, concurrents, limite=15):
    motif = re.compile(rf"(?<![\w]){re.escape(norm(marque))}(?![\w])")
    conc = {c: re.compile(rf"(?<![\w]){re.escape(norm(c))}(?![\w])") for c in concurrents}
    for l in [l for l in lignes if l["perdues"] and l["classe"] != "concurrent"][:limite]:
        l["pages"] = []
        mes_urls = list(dict.fromkeys(u for q in l["questions"] for u in urls.get((q, l["domaine"]), [])))
        for u in mes_urls[:3]:
            r = pg.lire(u, ua=pg.UA_NAVIGATEUR, timeout=20)
            if r["statut"] != 200:
                l["pages"].append({"url": u, "etat": "non lu", "detail": r["erreur"] or f"statut {r['statut']}"})
                continue
            t = norm(pg.analyser(r["texte"])["texte"])
            l["pages"].append({"url": u, "etat": "marque présente" if motif.search(t) else "marque absente",
                               "concurrents": [c for c, m in conc.items() if m.search(t)]})
        if not mes_urls:
            l["pages"].append({"url": None, "etat": "URL exacte inconnue", "detail": "domaine cité sans lien complet"})


def afficher(r: dict, marque: str | None) -> str:
    L = [f"SOURCES TIERCES · {marque or 'marque'} · {r['perdues']} paires question × moteur perdues"
         f" sur {r['questions']} questions · {r['etiquette']}", ""]
    if not r["lignes"]:
        L.append("Aucune source citée dans la mesure : sans liens dans les réponses, impossible de dire qui façonne la liste.")
        return "\n".join(L)
    if r["par_classe"]:
        L.append("CLASSES SUR LES QUESTIONS PERDUES · " + " · ".join(f"{c} {n}" for c, n in r["par_classe"].items() if n))
        L.append("")
    L.append("À TRAVAILLER (cités là où la marque perd)")
    for l in [l for l in r["lignes"] if l["perdues"]]:
        conc = ", ".join(f"{c} ({n})" for c, n in l["concurrents"].items())
        L.append(f"  {l['domaine']:<28}{l['classe']:<14}{l['perdues']} perdue(s) · {', '.join(l['questions'])}"
                 f" · {', '.join(l['moteurs'])}" + (f" · nommés : {conc}" if conc else ""))
        for p in l.get("pages", []):
            extra = f" · concurrents sur la page : {', '.join(p['concurrents'])}" if p.get("concurrents") else ""
            L.append(f"      {p['etat'].upper() if p['etat'] == 'marque absente' else p['etat']:<18}"
                     f"{p['url'] or ''}{extra}{(' · ' + p['detail']) if p.get('detail') else ''}")
        L.append(f"      → {l['action']}")
    autres = [l for l in r["lignes"] if not l["perdues"]]
    if autres:
        L += ["", "CITÉS AILLEURS (questions gagnées ou neutres) · " +
              ", ".join(f"{l['domaine']} ({l['classe']})" for l in autres[:12])]
    L += ["", "Une source citée n'est pas une cause prouvée : c'est là que le moteur a lu.",
          "Lignes rouges (faux avis, faux comptes, contenus sponsorisés non signalés) : references/lignes-rouges.md"]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Sites tiers cités sur les questions où la marque perd.")
    ap.add_argument("mesure", help="sortie JSON de visibilite.py mesurer --json")
    ap.add_argument("--reponses", help="fichier de réponses collées, pour retrouver les URL exactes")
    ap.add_argument("--marque", help="nom de la marque (pour --verifier)")
    ap.add_argument("--domaine", action="append", default=[], help="domaine de la marque (répétable)")
    ap.add_argument("--concurrent", action="append", default=[],
                    help="« Nom=domaine.fr » ou « Nom » (répétable) : site concurrent et nom cherché sur les pages")
    ap.add_argument("--classe", action="append", default=[], help="« domaine=classe » pour compléter sources_fr.json")
    ap.add_argument("--verifier", action="store_true", help="ouvrir les pages tierces citées et y chercher la marque")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        mesure = json.loads(Path(a.mesure).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"Mesure illisible ({e}) : lance visibilite.py mesurer … --json > mesure.json", file=sys.stderr)
        return 1
    noms = [c.split("=")[0].strip() for c in a.concurrent]
    doms = [d.strip().lower() for c in a.concurrent if "=" in c for d in c.split("=", 1)[1].split(",") if "." in d]
    extra = dict(x.lower().split("=", 1) for x in a.classe if "=" in x)
    r = analyser(mesure, [d.lower() for d in a.domaine], doms, extra)
    if a.verifier:
        if not (a.reponses and a.marque):
            print("--verifier demande --reponses et --marque.", file=sys.stderr)
            return 1
        verifier(r["lignes"], urls_citees(a.reponses), a.marque, noms)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r, a.marque))
    return 0


if __name__ == "__main__":
    sys.exit(main())
