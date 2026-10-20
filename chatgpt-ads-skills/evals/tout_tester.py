#!/usr/bin/env python3
"""Lance tous les tests du pack ChatGPT Ads : python3 evals/tout_tester.py

Deux familles : les suites unittest (evals/<dossier>/test_*.py) et les tests
d'intégrité. Code 0 si tout passe.
"""
import re
import subprocess
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
AUTONOMES = [ICI / "test_integrite.py"]


def main():
    ok, total, lignes = True, 0, []
    for d in sorted(p for p in ICI.iterdir() if p.is_dir() and not p.name.startswith(("__", "fixtures"))):
        suite = unittest.defaultTestLoader.discover(str(d), pattern="test_*.py", top_level_dir=str(d))
        n = suite.countTestCases()
        if not n:
            continue
        with open(__import__("os").devnull, "w") as nul:
            res = unittest.TextTestRunner(stream=nul, verbosity=0).run(suite)
        echecs = len(res.failures) + len(res.errors)
        ok &= echecs == 0
        total += n
        lignes.append(f"  {d.name:<24} {n - echecs}/{n}" + ("" if not echecs else "  ✖"))
        for t, trace in res.failures + res.errors:
            lignes.append(f"      ✖ {t.id()}\n{trace}")
    for f in AUTONOMES:
        p = subprocess.run([sys.executable, str(f)], capture_output=True, text=True)
        m = re.search(r"(\d+)/(\d+) tests passés", p.stdout)
        n = int(m.group(2)) if m else 0
        bon = p.returncode == 0 and m and m.group(1) == m.group(2)
        ok &= bool(bon)
        total += n
        lignes.append(f"  {f.name:<24} {m.group(0) if m else 'échec'}"
                      + ("" if bon else "  ✖\n" + p.stdout[-1500:] + p.stderr[-1500:]))
    print("\n".join(lignes))
    print(f"{'TOUT PASSE' if ok else 'ÉCHECS'} · {total} tests")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
