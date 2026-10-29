#!/usr/bin/env python3
"""Lance tous les tests du pack LinkedIn : python3 evals/tout_tester.py

Deux familles : les suites unittest (evals/<skill>/test_*.py) et les deux
scripts de test autonomes de la v1 (humaniseur, job_url), qui affichent
« n/n tests passés ». Code 0 si tout passe.
"""
import re
import subprocess
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
AUTONOMES = [ICI / "linkedin-human" / "test_humaniseur.py", ICI / "linkedin-job" / "test_job_url.py",
             ICI / "test_integrite.py"]


def main():
    ok, total, lignes = True, 0, []
    for d in sorted(p for p in ICI.iterdir() if p.is_dir() and not p.name.startswith(("resultats", "__"))):
        suite = unittest.defaultTestLoader.discover(str(d), pattern="test_*.py", top_level_dir=str(d))
        n = suite.countTestCases()
        if not n:
            continue
        res = unittest.TextTestRunner(stream=open("/dev/null", "w"), verbosity=0).run(suite)
        echecs = len(res.failures) + len(res.errors)
        ok &= echecs == 0
        total += n
        lignes.append(f"  {d.name:<22} {n - echecs}/{n}" + ("" if not echecs else "  ✖"))
        for t, trace in res.failures + res.errors:
            lignes.append(f"      ✖ {t.id()}\n{trace}")
    for f in AUTONOMES:
        if not f.exists():
            continue
        p = subprocess.run([sys.executable, str(f)], capture_output=True, text=True)
        m = re.search(r"(\d+)/(\d+) tests passés", p.stdout)
        n = int(m.group(2)) if m else 0
        bon = p.returncode == 0 and m and m.group(1) == m.group(2)
        ok &= bool(bon)
        total += n
        lignes.append(f"  {f.parent.name + '/' + f.name:<22} {m.group(0) if m else 'échec'}" + ("" if bon else "  ✖\n" + p.stdout[-1500:] + p.stderr[-1500:]))
    print("\n".join(lignes))
    print(f"{'TOUT PASSE' if ok else 'ÉCHECS'} · {total} tests")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
