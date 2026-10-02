"""Tests de skills/linkedin-interview/scripts/reserve.py."""
import subprocess
import sys
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
SCRIPT = PACK / "skills" / "linkedin-interview" / "scripts" / "reserve.py"
sys.path.insert(0, str(SCRIPT.parent))
import reserve as r  # noqa: E402


class Reserve(unittest.TestCase):
    def test_modele_vide(self):
        texte = (PACK / "templates" / "reserve.md").read_text(encoding="utf-8")
        e = r.etat_banque(texte)
        self.assertEqual(e["rempli"], "non")
        self.assertTrue(all(s["statut"] == "vide" for s in e["sections"]))
        self.assertEqual(e["reussites_a_preciser"], [])
        self.assertFalse(e["complet"])

    def test_exemple(self):
        e = r.etat_banque(r.EXEMPLE)
        statuts = {s["section"]: s["statut"] for s in e["sections"]}
        self.assertEqual(statuts[2], "ok")
        self.assertEqual(statuts[4], "vide")
        self.assertEqual(statuts[3], "mince")
        self.assertEqual(len(e["reussites_a_preciser"]), 1)
        self.assertIn("significativement", " ".join(e["reussites_a_preciser"][0]["problemes"]))
        self.assertEqual(e["prochaine_seance"][0], "Tournants")

    def test_priorites_par_objectif(self):
        e = r.etat_banque(r.EXEMPLE, "autorite")
        self.assertEqual(e["prochaine_seance"][0], "Positions")

    def test_verifier(self):
        ok = r.verifier_reussite("Vendu 340 abonnements annuels en 9 semaines : 210 k€ signés")
        self.assertTrue(ok["utilisable"], ok)
        ko = r.verifier_reussite("Participé au lancement du produit")
        self.assertFalse(ko["utilisable"])
        self.assertTrue(any("verbe faible" in p for p in ko["problemes"]))
        date_col = r.verifier_reussite("Doublé les leads entrants : 120 par mois", quand="T3 2024")
        self.assertTrue(date_col["utilisable"], date_col)

    def test_experiences_par_poste(self):
        x = r.experiences(r.EXEMPLE, "acquisition")
        self.assertEqual(list(x["postes"]), ["Responsable acquisition"])
        self.assertEqual(len(x["postes"]["Responsable acquisition"]), 3)

    def test_codes(self):
        self.assertEqual(subprocess.run([sys.executable, str(SCRIPT), "etat", "--exemple"],
                                        capture_output=True).returncode, 2)
        self.assertEqual(subprocess.run([sys.executable, str(SCRIPT), "verifier",
                                         "Signé 12 contrats en 3 mois : 80 k€"], capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run([sys.executable, str(SCRIPT), "etat", "/inexistant.md"],
                                        capture_output=True).returncode, 1)


if __name__ == "__main__":
    unittest.main()
