"""Tests de candidatures.py (linkedin-job). Lancer : python3 -m unittest discover -s evals/linkedin-job"""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ICI = Path(__file__).parent
SCRIPT = ICI.parents[1] / "skills" / "linkedin-job" / "scripts" / "candidatures.py"
spec = importlib.util.spec_from_file_location("candidatures", SCRIPT)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
OFFRES = (ICI / "offres-exemple.txt").read_text(encoding="utf-8")
PROFIL = (ICI / "profil-exemple.txt").read_text(encoding="utf-8")


class Mots(unittest.TestCase):
    def setUp(self):
        self.r = c.mots(OFFRES, PROFIL)
        self.absents = dict(self.r["absents_du_profil"])

    def test_intitules(self):
        self.assertEqual(self.r["intitules"][0], ("Head of Growth", 2))
        self.assertEqual(self.r["offres"], 4)

    def test_absents(self):
        self.assertEqual(self.absents["ga4"], 3)
        self.assertIn("sql", self.absents)
        self.assertIn("lifecycle marketing", self.absents)

    def test_pas_de_bruit(self):
        for bruit in ("personnes", "pilotez", "vous", "equipe"):
            self.assertNotIn(bruit, self.absents)

    def test_deja_present(self):
        presents = dict(self.r["deja_dans_le_profil"])
        self.assertIn("hubspot", presents)
        self.assertNotIn("hubspot", self.absents)

    def test_competences_jamais_demandees(self):
        self.assertIn("prise de parole", self.r["jamais_dans_les_offres"])
        self.assertNotIn("HubSpot", self.r["jamais_dans_les_offres"])


class Suivi(unittest.TestCase):
    def test_etat(self):
        r = c.etat(c.lire_candidatures(ICI / "journal-exemple.md"), date(2026, 10, 3))
        self.assertEqual(r["total"], 4)
        self.assertEqual(r["taux_reponse"], 0.5)
        self.assertEqual(len(r["relances_dues"]), 1)
        self.assertIn("Mutuelle C", r["relances_dues"][0])
        self.assertIn("Néo-assurance A", r["a_classer"][0])
        self.assertEqual(r["par_source"]["réseau"]["taux"], 1.0)

    def test_ajouter_dans_le_modele(self):
        with tempfile.TemporaryDirectory() as d:
            j = Path(d) / "journal.md"
            shutil.copy(ICI.parents[1] / "templates" / "journal.md", j)
            c.ajouter(j, "Courtier B", "Responsable acquisition", source="reseau", contact="Hélène B.", jour="2026-10-02")
            cands = c.lire_candidatures(j)
            self.assertEqual(len(cands), 1)
            self.assertEqual(cands[0]["entreprise"], "Courtier B")
            self.assertEqual(cands[0]["_date"], date(2026, 10, 2))

    def test_cli_code_relance(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "etat", "--journal", str(ICI / "journal-exemple.md"), "--aujourdhui", "2026-10-03"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("relance due", p.stdout)


if __name__ == "__main__":
    unittest.main()
