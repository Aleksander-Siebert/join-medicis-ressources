#!/usr/bin/env python3
"""banc_pages.py : 6 pages pièges servies en local, lues par chaque outil ; sorties brutes gardées.

Les verdicts sont relevés à la main dans les sorties brutes (sorties/pages/)
et cités dans RESULTATS.md : les formats des outils sont trop différents
pour un adaptateur juste, et la citation montre ce que chaque outil a
affiché.

  python3 banc_pages.py --depots <dossier des clones> --venv <bin d'un venv avec requests et bs4>
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
sys.path.insert(0, str(ICI))
from serveur import Sites  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--depots", required=True)
    ap.add_argument("--venv", required=True)
    a = ap.parse_args(argv)
    d = json.loads((ICI / "cas_pages.json").read_text(encoding="utf-8"))
    cas = [{"id": c["id"], "robots": {"statut": 200, "texte": "User-agent: *\nAllow: /\n"}, "pages": {"/": {"html": c["html"]}}}
           for c in d["cas"]]
    sites = Sites(cas)
    sortie = ICI / "sorties" / "pages"
    sortie.mkdir(parents=True, exist_ok=True)
    py, dep = f"{a.venv}/python", a.depots
    for c in d["cas"]:
        url = sites.url(c["id"]) + "/"
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(c["html"])
        cmds = {
            "join-medicis-audit": [sys.executable, str(PACK / "skills/geo-audit/scripts/audit.py"), url, "--marque", "Assurly", "--json"],
            "join-medicis-entite": [sys.executable, str(PACK / "skills/geo-entite/scripts/entite.py"), url, "--marque", "Assurly", "--json"],
            "join-medicis-agentic": [sys.executable, str(PACK / "skills/geo-agentic/scripts/agentic.py"), f.name, "--hors-ligne", "--json"],
            "geo-optimizer": [py, str(ICI / "lanceur.py"), "geo-optimizer", f"{dep}/geo-optimizer-skill", "--", "audit", "--url", url, "--format", "json"],
            "geo-score": [sys.executable, f"{dep}/geo-score/cli/geo_score.py", "--json", url],
            "ultimate-hidden": [py, f"{dep}/ultimate-seo-geo/scripts/hidden_instructions.py", f.name, "--json"],
            "claude-seo-agentic": [py, f"{dep}/claude-seo/scripts/agentic_check.py", url, "--json"],
        }
        for nom, cmd in cmds.items():
            try:
                p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                txt = p.stdout + "\n--- stderr ---\n" + p.stderr[-2000:]
            except subprocess.TimeoutExpired:
                txt = "délai dépassé"
            (sortie / f"{c['id']}-{nom}.txt").write_text(re.sub(r"127\.0\.0\.1:\d+", "site-de-test", txt), encoding="utf-8")
        print(f"{c['id']} fait", file=sys.stderr)
    sites.arreter()


if __name__ == "__main__":
    main()
