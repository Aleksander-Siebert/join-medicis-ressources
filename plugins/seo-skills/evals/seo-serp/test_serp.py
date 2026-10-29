#!/usr/bin/env python3
"""Tests de serp.py : python3 -m unittest discover evals/seo-serp"""
import datetime as dt
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
SCRIPT = ICI.parents[1] / "skills" / "seo-serp" / "scripts" / "serp.py"
spec = importlib.util.spec_from_file_location("serp", SCRIPT)
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)
AUJ = dt.date(2026, 10, 15)


def lancer(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)


class Mutuelle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        res, err = sp.lire(ICI / "releve-mutuelle.csv")
        assert not err
        cls.r = sp.analyser(res, "mutuelle indépendant", ai_overview=True, annonces=4, aujourdhui=AUJ)

    def test_consensus(self):
        self.assertEqual((self.r["dominant"], self.r["part"], self.r["consensus"]), ("comparatif", 0.4, "partagé"))

    def test_difficulte_directionnelle(self):
        self.assertEqual(self.r["difficulte"], "moyenne")
        self.assertIn("AI Overview affiché (moins de clics vers les résultats)", self.r["signaux"])
        self.assertEqual(len(self.r["signaux"]), 5)

    def test_rien_a_ne_pas_tenter(self):
        self.assertEqual(self.r["ne_pas_tenter"], [])

    def test_concurrents_sans_plateformes_ni_sites_publics(self):
        self.assertEqual(len(self.r["concurrents"]), 8)
        self.assertFalse(any("reddit" in u or "service-public" in u for u in self.r["concurrents"]))
        self.assertEqual(self.r["sources"], ["https://www.service-public.fr/particuliers/vosdroits/F000"])


class Reglementaire(unittest.TestCase):
    def test_ne_pas_tenter(self):
        p = lancer(ICI / "releve-reglementaire.csv", "--requete", "déclaration urssaf micro-entreprise obligatoire",
                   "--aujourdhui", "2026-10-15")
        self.assertEqual(p.returncode, 3)
        self.assertIn("question réglementaire", p.stdout)
        self.assertIn("Wikipédia en tête", p.stdout)

    def test_sans_requete_reglementaire_pas_d_arret_reglementaire(self):
        res, _ = sp.lire(ICI / "releve-reglementaire.csv")
        r = sp.analyser(res, "idées de nom pour une micro-entreprise", aujourdhui=AUJ)
        self.assertFalse(any("réglementaire" in s for s in r["ne_pas_tenter"]))


class Formats(unittest.TestCase):
    def ecrire(self, contenu):
        d = tempfile.mkdtemp()
        f = Path(d) / "r.csv"
        f.write_text(contenu, encoding="utf-8")
        return f

    def test_type_inconnu_refuse(self):
        f = self.ecrire("position,url,type\n" + "".join(f"{i},https://s{i}.example/,blog\n" for i in range(1, 7)))
        p = lancer(f)
        self.assertEqual(p.returncode, 1)
        self.assertIn("type « blog » inconnu", p.stderr)

    def test_trop_peu_de_resultats(self):
        f = self.ecrire("position,url,type\n1,https://a.example/,guide\n2,https://b.example/,guide\n")
        self.assertEqual(lancer(f).returncode, 1)

    def test_forums_dominants(self):
        lignes = "position;url;type\n" + "".join(f"{i};https://www.reddit.com/r/x/{i};forum\n" for i in range(1, 4)) + \
                 "".join(f"{i};https://g{i}.example/;guide\n" for i in range(4, 8))
        res, err = sp.lire(self.ecrire(lignes))
        self.assertFalse(err)
        self.assertTrue(any("forums dominants" in s for s in sp.analyser(res, aujourdhui=AUJ)["ne_pas_tenter"]))

    def test_actualite_chaude(self):
        lignes = "position,url,type\n" + "".join(f"{i},https://media{i}.example/a,actualite\n" for i in range(1, 6))
        res, _ = sp.lire(self.ecrire(lignes))
        self.assertTrue(any("actualité chaude" in s for s in sp.analyser(res, aujourdhui=AUJ)["ne_pas_tenter"]))

    def test_json(self):
        p = lancer(ICI / "releve-mutuelle.csv", "--json", "--aujourdhui", "2026-10-15")
        self.assertEqual(json.loads(p.stdout)["dominant"], "comparatif")


if __name__ == "__main__":
    unittest.main()
