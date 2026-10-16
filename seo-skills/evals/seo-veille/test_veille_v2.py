#!/usr/bin/env python3
"""Tests des événements datés de veille.py : python3 -m unittest discover evals/seo-veille"""
import importlib.util
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ICI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("veille", ICI.parents[1] / "skills" / "seo-veille" / "scripts" / "veille.py")
vl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vl)


class Evenements(unittest.TestCase):
    def test_periode_filtre(self):
        ev = vl.lire_evenements(str(ICI / "evenements.txt"), "2026-10-01:2026-10-31")
        self.assertEqual([e["date"] for e in ev], ["2026-10-08"])

    def test_sans_periode_tout_le_fichier(self):
        self.assertEqual(len(vl.lire_evenements(str(ICI / "evenements.txt"))), 3)

    def test_rapport_les_presente_comme_hypotheses(self):
        class A:
            actuel = str(ICI.parent / "scripts" / "gsc-actuel.csv")
            precedent = str(ICI.parent / "scripts" / "gsc-precedent.csv")
            top, json = 5, False
            evenements = str(ICI / "evenements.txt")
            periode = "2026-10-01:2026-10-31"
        f = io.StringIO()
        with redirect_stdout(f):
            vl.cmd_rapport(A)
        self.assertIn("hypothèses à vérifier, jamais des causes", f.getvalue())

    def test_json(self):
        class A:
            actuel = str(ICI.parent / "scripts" / "gsc-actuel.csv")
            precedent = str(ICI.parent / "scripts" / "gsc-precedent.csv")
            top, json = 5, True
            evenements = str(ICI / "evenements.txt")
            periode = None
        f = io.StringIO()
        with redirect_stdout(f):
            vl.cmd_rapport(A)
        self.assertEqual(len(json.loads(f.getvalue())["evenements"]), 3)


if __name__ == "__main__":
    unittest.main()
