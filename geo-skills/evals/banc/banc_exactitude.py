#!/usr/bin/env python3
"""banc_exactitude.py : 10 réponses pièges, en français et en anglais, deux vérificateurs de faits.

Join Médicis (exactitude.py) contre ultimate-seo-geo (citation_sampling.py
--facts), le seul dépôt étudié qui vérifie les faits de la marque dans les
réponses par script. Mêmes réponses, mêmes données de référence, chacune
dans le format de l'outil (faits-banc.csv, faits-banc-ultimate.json).
Question posée : l'outil signale-t-il une erreur sur la marque ?

  python3 banc_exactitude.py --depots <dossier des clones>
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
ERREURS = {"différent", "devise", "périmé", "faux"}


def nous(texte, marque, concurrents):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(f"=== ChatGPT | P1 | Quelle mutuelle pour un indépendant ?\n{texte}\n")
    cmd = [sys.executable, str(PACK / "skills/geo-exactitude/scripts/exactitude.py"), f.name, "--marque", marque,
           "--faits", str(ICI / "faits-banc.csv"), "--json"] + sum((["--concurrent", c] for c in concurrents), [])
    p = subprocess.run(cmd, capture_output=True, text=True)
    r = json.loads(p.stdout)
    signale = [x for x in r["registre"] if x["verdict"] in ERREURS]
    return bool(signale), ", ".join(sorted({x["verdict"] for x in signale})) or "rien", p.stdout


def ultimate(texte, depots):
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "engine", "prompt", "run", "cited", "mentioned", "cited_domains", "answer"])
        w.writerow(["2026-10-16", "chatgpt", "Which health insurance for a freelancer?", "1", "no", "yes", "", texte])
    p = subprocess.run([sys.executable, f"{depots}/ultimate-seo-geo/scripts/citation_sampling.py", f.name,
                        "--domain", "assurly.example", "--facts", str(ICI / "faits-banc-ultimate.json"), "--json"],
                       capture_output=True, text=True)
    r = json.loads(p.stdout)
    faux = [x["field"] for x in r["brand_facts"]["facts"] if x["wrong"]]
    return bool(faux), ", ".join(faux) or "rien", p.stdout


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--depots", required=True)
    a = ap.parse_args(argv)
    d = json.loads((ICI / "cas_exactitude.json").read_text(encoding="utf-8"))
    sorties = ICI / "sorties" / "exactitude"
    sorties.mkdir(parents=True, exist_ok=True)
    bilan = {(o, l): [0, 0] for o in ("Join Médicis", "ultimate-seo-geo") for l in ("fr", "en")}
    L = ["| Cas | Langue | Vérité | Join Médicis | ultimate-seo-geo |", "|---|---|---|---|---|"]
    for c in d["cas"]:
        for langue in ("fr", "en"):
            t = c[langue]
            n_ok, n_txt, n_brut = nous(t, d["marque"], d["concurrents"])
            u_ok, u_txt, u_brut = ultimate(t, a.depots)
            (sorties / f"{c['id']}-{langue}-join-medicis.json").write_text(n_brut, encoding="utf-8")
            (sorties / f"{c['id']}-{langue}-ultimate.json").write_text(u_brut, encoding="utf-8")
            cells = []
            for o, ok, txt in (("Join Médicis", n_ok, n_txt), ("ultimate-seo-geo", u_ok, u_txt)):
                juste = ok == c["erreur"]
                bilan[(o, langue)][0] += juste
                bilan[(o, langue)][1] += 1
                cells.append(f"{'✅' if juste else '❌'} {'signale' if ok else 'ne signale rien'} ({txt})" if ok
                             else f"{'✅' if juste else '❌'} ne signale rien")
            L.append(f"| {c['id']} {c['titre']} | {langue} | {'erreur à signaler' if c['erreur'] else 'rien à signaler'} | "
                     + " | ".join(cells) + " |")
    tete = ["| Outil | Français | Anglais |", "|---|---|---|"]
    for o in ("Join Médicis", "ultimate-seo-geo"):
        tete.append(f"| {o} | {bilan[(o, 'fr')][0]}/{bilan[(o, 'fr')][1]} | {bilan[(o, 'en')][0]}/{bilan[(o, 'en')][1]} |")
    print("\n".join(tete + [""] + L))


if __name__ == "__main__":
    main()
