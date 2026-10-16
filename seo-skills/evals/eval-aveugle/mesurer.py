#!/usr/bin/env python3
"""Mesures objectives des textes de l'éval avec les scripts du pack (A et B publiés ; les références C restent hors du dépôt)."""
import json, re, subprocess, sys
from pathlib import Path
ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
CTRL = PACK / "skills/seo-write/scripts/controle.py"
AFF = PACK / "commun/affirmations.py"
DET = PACK / "skills/seo-human/scripts/detect.py"
CAS = {"ps5": ("PS5 verticale ou horizontale", False), "iphone16": ("iPhone 16", False), "expat": ("associations de Français à l'étranger", True)}
def js(cmd):
    r = subprocess.run([sys.executable, *map(str, cmd), "--json"], capture_output=True, text=True)
    try: return json.loads(r.stdout)
    except Exception: return {"erreur": (r.stderr or r.stdout)[-200:]}
lignes = []
for cas, (kw, ymyl) in CAS.items():
    for conf in ("A", "B", "C"):
        f = ICI / ("sorties" if conf != "C" else ".") / (f"{conf}-{cas}.md")
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        c = js([CTRL, f, "--mot-cle", kw])
        a = js([AFF, f] + (["--ymyl"] if ymyl else []))
        d = js([DET, f, "--profil", "article"])
        r = (d.get("resultats") or [{}])[-1]
        meta = c.get("meta") or {}
        lignes.append({"cas": cas, "conf": conf, "mots": c.get("mots"), "trous": len(re.findall(r"\{\{", t)),
                       "controle": c.get("verdict"), "constats_hauts": sum(1 for x in c.get("constats", []) if x.get("gravite") in ("haut", "moyen", "haute", "moyenne")),
                       "title_px": meta.get("title_px"), "desc_px": meta.get("description_px"),
                       "affirmations": a.get("verdict"), "sans_source": a.get("compte", {}).get("bloquant", 0) + a.get("compte", {}).get("à vérifier", 0),
                       "humaniseur": r.get("score"), "verdict_humain": r.get("verdict"),
                       "a_reecrire": sum(1 for p in r.get("densite", []) if p.get("action") not in (None, "LAISSER"))})
print("| Cas | Conf. | Mots | Trous | controle.py | Constats hauts/moyens | Title px | Affirmations | Sans source | Humaniseur | Paragraphes à réécrire |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for l in lignes:
    print(f"| {l['cas']} | {l['conf']} | {l['mots']} | {l['trous']} | {l['controle']} | {l['constats_hauts']} | {l['title_px']} | {l['affirmations']} | {l['sans_source']} | {l['humaniseur']} {l['verdict_humain']} | {l['a_reecrire']} |")
