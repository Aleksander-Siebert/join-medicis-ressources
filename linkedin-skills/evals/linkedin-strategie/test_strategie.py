"""Tests de skills/linkedin-strategie/scripts (budget.py, brief.py)."""
import copy
import sys
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACK / "skills" / "linkedin-strategie" / "scripts"))
import brief as b  # noqa: E402
import budget as bu  # noqa: E402


class Budget(unittest.TestCase):
    def test_sous_le_plancher(self):
        r = bu.planifier(60)
        self.assertEqual((r["verdict"], r["code"]), ("SOUS LE PLANCHER", 2))
        self.assertEqual(r["plan"]["posts"], 0)

    def test_exemple_tient(self):
        r = bu.planifier(240, "depart", 2)
        self.assertEqual(r["code"], 0)
        self.assertEqual(r["plan"]["minutes_posts"], 90)
        self.assertLessEqual(r["plan"]["minutes_utilisees"], 240)

    def test_ne_tient_pas_chiffre(self):
        r = bu.planifier(240, "depart", 4)
        self.assertEqual(r["code"], 3)
        self.assertEqual(r["besoin"], 324)
        self.assertEqual(r["depassement"], 84)

    def test_petit_budget_garde_un_post(self):
        # 120 min en étape « départ » : 1 post et 12 commentaires, pas « 0 post »
        r = bu.planifier(120, "depart")
        self.assertEqual(r["code"], 0)
        self.assertEqual(len(r["plan"]["posts"]), 1)

    def test_couts_personnalises(self):
        r = bu.planifier(320, "depart", 2, cout={"texte": 60})
        self.assertEqual(r["plan"]["minutes_posts"], 160)

    def test_format_inconnu(self):
        with self.assertRaises(ValueError):
            bu.planifier(300, "etabli", formats="podcast")

    def test_semaine_minimale_toujours_la(self):
        for m in (60, 240, 1000):
            self.assertIn("semaine_minimale", bu.planifier(m, "depart", 2))


class Brief(unittest.TestCase):
    def test_exemple_valide(self):
        r = b.verifier(b.EXEMPLE)
        self.assertEqual(r["verdict"], "VALIDE", r)
        self.assertTrue(r["criteres_90_jours"])
        self.assertTrue(all("abonn" not in c for c in r["criteres_90_jours"]))
        self.assertIn("grâce aux", r["phrase_de_positionnement"])

    def test_refus(self):
        cas = {
            "objectif": ("objectif", "notoriete"),
            "vanite": ("objectif_90_jours", "atteindre 10 000 abonnés"),
            "audience": ("audience", "les entrepreneurs"),
            "exclusions": ("exclusions", ["la politique"]),
        }
        for nom, (cle, valeur) in cas.items():
            with self.subTest(nom=nom):
                x = copy.deepcopy(b.EXEMPLE)
                x[cle] = valeur
                self.assertEqual(b.verifier(x)["code"], 3)

    def test_parts_pas_100(self):
        x = copy.deepcopy(b.EXEMPLE)
        x["piliers"][0]["part"] = 50
        self.assertEqual(b.verifier(x)["code"], 3)

    def test_a_reprendre(self):
        x = copy.deepcopy(b.EXEMPLE)
        for p in x["piliers"]:
            p["preuve"] = ""
        r = b.verifier(x)
        self.assertEqual(r["code"], 2)
        self.assertTrue(any("processus" in m for m in r["a_reprendre"]))
        y = copy.deepcopy(b.EXEMPLE)
        y["piliers"][2]["etape"] = "conversion"
        self.assertTrue(any("Conversion à 30%" in m for m in b.verifier(y)["a_reprendre"]))

    def test_vanite_acceptee_si_resultat(self):
        x = copy.deepcopy(b.EXEMPLE)
        x["objectif_90_jours"] = "6 rendez-vous clients, peu importe les vues"
        self.assertEqual(b.verifier(x)["code"], 0)


if __name__ == "__main__":
    unittest.main()
