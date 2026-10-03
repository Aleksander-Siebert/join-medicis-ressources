"""Tests de semaine.py (linkedin-plan). Lancer : python3 -m unittest discover -s evals/linkedin-plan"""
import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path

ICI = Path(__file__).parent
SKILL = ICI.parents[1] / "skills" / "linkedin-plan"
spec = importlib.util.spec_from_file_location("semaine", SKILL / "scripts" / "semaine.py")
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)
PLAN = json.loads((SKILL / "assets" / "plan-exemple.json").read_text(encoding="utf-8"))
HIST = s.posts_journal(ICI / "journal-exemple.md")
ECARTEES = s.formules_ecartees(ICI / "apprentissages-exemple.md")


def controle(plan, minutes=300):
    return s.controler(copy.deepcopy(plan), HIST, ECARTEES, minutes)


class Plan(unittest.TestCase):
    def test_plan_exemple_pret(self):
        r = controle(PLAN)
        self.assertEqual(r["verdict"], "PRÊT", r)
        self.assertEqual(r["minutes_necessaires"], 215)

    def test_exemple_bloque(self):
        r = s.controler(copy.deepcopy(s.EXEMPLE), minutes=200)
        self.assertEqual(r["code"], 3)
        self.assertEqual(len(r["bloquants"]), 3)

    def test_formule_en_7_jours_avec_journal(self):
        p = copy.deepcopy(PLAN)
        p["creneaux"][0]["formule"] = "erreur-datee"
        p["creneaux"][0]["jour"] = "2026-09-28"  # erreur-datee publiée le 2026-09-22 : 6 jours
        r = controle(p)
        self.assertIn("pas deux fois la même formule", " ".join(r["bloquants"]))

    def test_7_jours_pile_permis(self):
        self.assertFalse([b for b in controle(PLAN)["bloquants"] if "cas-a-trancher" in b])

    def test_formule_ecartee(self):
        p = copy.deepcopy(PLAN)
        p["creneaux"][1]["formule"] = "interpellation"
        self.assertIn("Ce qui ne marche pas", " ".join(controle(p)["bloquants"]))

    def test_formule_inconnue(self):
        p = copy.deepcopy(PLAN)
        p["creneaux"][1]["formule"] = "question-piege"
        self.assertIn("inconnue", " ".join(controle(p)["bloquants"]))

    def test_pilier_60_sur_4_semaines(self):
        p = copy.deepcopy(PLAN)
        for c in p["creneaux"]:
            c["pilier"] = "Acquisition"
        r = controle(p)
        self.assertIn("Acquisition", " ".join(r["bloquants"]))

    def test_budget(self):
        self.assertIn("minutes", " ".join(controle(PLAN, 150)["bloquants"]))

    def test_objectif_hors_formule(self):
        p = copy.deepcopy(PLAN)
        p["creneaux"][2]["objectif"] = "sauvegardes"
        self.assertIn("sert plutôt", " ".join(controle(p)["attentions"]))


class Calendrier(unittest.TestCase):
    def test_paques(self):
        self.assertEqual(s.paques(2026), date(2026, 4, 5))
        self.assertEqual(s.paques(2027), date(2027, 3, 28))

    def test_feries_et_ponts(self):
        f, ponts = s.feries(2026)
        self.assertEqual(f[date(2026, 5, 14)], "Ascension")
        self.assertIn(date(2026, 5, 15), ponts)
        self.assertIn(date(2027, 11, 12), s.feries(2027)[1])

    def test_signalement(self):
        p = copy.deepcopy(PLAN)
        p["creneaux"][0]["jour"] = "2026-05-14"
        p["creneaux"][1]["jour"] = "2026-08-18"
        att = " ".join(controle(p)["attentions"])
        self.assertIn("Ascension", att)
        self.assertIn("août", att)


class Export(unittest.TestCase):
    def test_csv(self):
        lignes = s.exporter(PLAN, "csv").strip().splitlines()
        self.assertEqual(len(lignes), 4)
        self.assertTrue(lignes[1].startswith("2026-10-06;mardi;08:15;chiffre-d-abord"))

    def test_json(self):
        self.assertEqual(json.loads(s.exporter(PLAN, "json"))[2]["Jour"], "vendredi")

    def test_cli(self):
        p = subprocess.run([sys.executable, str(SKILL / "scripts" / "semaine.py"), "--exemple"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 3)
        self.assertIn("PLAN  BLOQUÉ", p.stdout)


if __name__ == "__main__":
    unittest.main()
