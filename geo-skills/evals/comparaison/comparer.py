#!/usr/bin/env python3
"""
Compare deux scoreurs de citabilité sur 8 passages français (4 bons, 4 faibles) :
citability_scorer.py de geo-seo-claude (référence) et citability.py (ce pack).

    git clone https://github.com/zubair-trabzada/geo-seo-claude /tmp/geo-seo-claude
    python3 comparer.py /tmp/geo-seo-claude/scripts

Un bon scoreur donne des notes nettement plus hautes aux bons passages.
"""
import json
import os
import statistics as st
import sys
import types

ICI = os.path.dirname(os.path.abspath(__file__))
REF = sys.argv[1] if len(sys.argv) > 1 else "."
# La référence importe requests et bs4 pour lire des URL : inutiles ici.
sys.modules.setdefault("requests", types.ModuleType("requests"))
bs4 = types.ModuleType("bs4"); bs4.BeautifulSoup = None; sys.modules.setdefault("bs4", bs4)
sys.path[:0] = [REF, os.path.join(ICI, "..", "..", "skills", "geo-citability")]
import citability_scorer as ref  # noqa: E402
import citability as v1  # noqa: E402

data = json.load(open(os.path.join(ICI, "passages.json"), encoding="utf-8"))
notes = {}
for groupe in ("bons", "faibles"):
    for titre, texte in data[groupe]:
        r = ref.score_passage(texte, titre)
        r = r.get("total_score", r.get("score"))
        m = v1.score_block({"titre": titre, "niveau": 2, "texte": [texte], "listes": 0})["score"]
        notes.setdefault(groupe, []).append((r, m))
        print(f"{groupe:8} {titre[:45]:45} référence {r:>5}   v1 {m:>3}")
for nom, i in (("référence", 0), ("v1", 1)):
    b = st.mean(x[i] for x in notes["bons"])
    f = st.mean(x[i] for x in notes["faibles"])
    print(f"{nom:10} bons {b:5.1f} · faibles {f:5.1f} · écart {b - f:5.1f}")
