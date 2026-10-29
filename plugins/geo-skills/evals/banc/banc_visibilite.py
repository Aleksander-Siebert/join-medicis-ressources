#!/usr/bin/env python3
"""banc_visibilite.py : lire une réponse d'IA, en français et en anglais.

La marque est-elle mentionnée, recommandée, déconseillée ? Join Médicis
(visibilite.py, analyser_reponse) contre geo-optimizer (brand_matches et
_classify_strength, les fonctions de sa commande « citations ») et
ultimate-seo-geo (réponses qui nomment la marque, dans citation_sampling.py
--facts ; il ne lit ni la recommandation ni la mise en garde : son tableur
les fait noter à la main). Les autres dépôts n'ont pas de lecture
automatique des réponses.

  python3 banc_visibilite.py --depots <dossier des clones>
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
sys.path.insert(0, str(PACK / "skills/geo-visibilite/scripts"))
import visibilite as vis  # noqa: E402


def nous(texte, d):
    lex = vis.charger_lexiques()
    conc = {c: [vis.motif_nom(c)] for c in d["concurrents"]}
    r = vis.analyser_reponse(texte, [vis.motif_nom(d["marque"])], [d["domaine"]], conc, lex)
    return {"m": r["mentionnee"], "r": r["recommandee"], "d": r["deconseillee"]}


def geo_optimizer(texte, d, depots):
    code = (f"import sys, json; sys.path.insert(0, {repr(depots + '/geo-optimizer-skill/src')}); "
            "from geo_optimizer.utils.brand_match import brand_matches; "
            "from geo_optimizer.core.audit_sentiment import _classify_strength; "
            f"t = {texte!r}; s = _classify_strength(t.lower()); "
            f"print(json.dumps({{'m': brand_matches(t, {d['marque']!r}), 'force': s}}))")
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    r = json.loads(p.stdout)
    # sa propre échelle : strongly_recommended et mentioned (déclenché par « recommend », « suggest », « worth »)
    # valent recommandation ; warned_against vaut mise en garde ; lue sur toute la réponse, pas par marque
    return {"m": r["m"], "r": r["force"] in ("strongly_recommended", "mentioned"),
            "d": r["force"] == "warned_against", "brut": r["force"]}


def ultimate(texte, d, depots):
    faits = {"brand": d["marque"], "aliases": [], "others": d["concurrents"],
             "facts": [{"field": "founding year", "type": "year", "value": 2019, "source": "x"}], "false_claims": []}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(faits, f)
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8", newline="") as g:
        w = csv.writer(g)
        w.writerow(["date", "engine", "prompt", "run", "cited", "mentioned", "cited_domains", "answer"])
        w.writerow(["2026-10-16", "chatgpt", "q", "1", "no", "", "", texte])
    p = subprocess.run([sys.executable, f"{depots}/ultimate-seo-geo/scripts/citation_sampling.py", g.name,
                        "--domain", d["domaine"], "--facts", f.name, "--json"], capture_output=True, text=True)
    r = json.loads(p.stdout)
    return {"m": r["brand_facts"]["answers_naming_brand"] > 0}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--depots", required=True)
    a = ap.parse_args(argv)
    d = json.loads((ICI / "cas_visibilite.json").read_text(encoding="utf-8"))
    outils = ["Join Médicis", "geo-optimizer", "ultimate-seo-geo"]
    bilan = {(o, l): [0, 0] for o in outils for l in ("fr", "en")}
    L = ["| Cas | Langue | Vérité (mentionnée · recommandée · déconseillée) | " + " | ".join(outils) + " |",
         "|---|---|---|" + "---|" * len(outils)]
    lettre = lambda b: "oui" if b else "non"  # noqa: E731
    for c in d["cas"]:
        for langue in ("fr", "en"):
            t = c[langue]
            res = {"Join Médicis": nous(t, d), "geo-optimizer": geo_optimizer(t, d, a.depots),
                   "ultimate-seo-geo": ultimate(t, d, a.depots)}
            cells = []
            for o in outils:
                r = res[o]
                parts = []
                for k in ("m", "r", "d"):
                    if k not in r:
                        parts.append("—")
                        continue
                    ok = r[k] == c[k]
                    bilan[(o, langue)][0] += ok
                    bilan[(o, langue)][1] += 1
                    parts.append(("✅ " if ok else "❌ ") + lettre(r[k]))
                cells.append(" · ".join(parts))
            L.append(f"| {c['id']} {c['titre']} | {langue} | {lettre(c['m'])} · {lettre(c['r'])} · {lettre(c['d'])} | "
                     + " | ".join(cells) + " |")
    tete = ["| Outil | Français | Anglais | Ce qu'il lit |", "|---|---|---|---|"]
    lit = {"Join Médicis": "mention, recommandation, mise en garde", "geo-optimizer": "mention, recommandation, mise en garde",
           "ultimate-seo-geo": "mention seulement (le reste est noté à la main)"}
    for o in outils:
        f, e = bilan[(o, "fr")], bilan[(o, "en")]
        tete.append(f"| {o} | {f[0]}/{f[1]} | {e[0]}/{e[1]} | {lit[o]} |")
    print("\n".join(tete + [""] + L))


if __name__ == "__main__":
    main()
