"""Tests de skills/linkedin-entreprise (audit_page.py, ambassadeurs.py)."""
import copy
import json
import sys
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
SKILL = PACK / "skills" / "linkedin-entreprise"
sys.path.insert(0, str(SKILL / "scripts"))
import ambassadeurs as am  # noqa: E402
import audit_page as ap  # noqa: E402


class Page(unittest.TestCase):
    def test_grille_100(self):
        g = json.loads((SKILL / "grille-page.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(c["points"] for c in g["criteres"]), 100)

    def test_exemple(self):
        r = ap.auditer(ap.EXEMPLE)
        self.assertEqual((r["note"], r["notables"], r["verdict"]), (48, 100, "FAIBLE"))

    def test_n_a_sans_statistiques(self):
        p = copy.deepcopy(ap.EXEMPLE)
        p["sources"] = ["page", "contexte"]
        r = ap.auditer(p)
        self.assertEqual(r["notables"], 74)
        self.assertIn("Rythme de publication", r["n_a"])

    def test_slogan(self):
        frac, d = ap.evaluer("nom_slogan", {"slogan": "L'assurance habitation pour les locataires, remboursée en 9 jours"})
        self.assertEqual(frac, 1.0, d)
        frac, d = ap.evaluer("nom_slogan", {"slogan": "x" * 130})
        self.assertIn("130 caractères", d)

    def test_ouverture_sur_entreprise(self):
        frac, d = ap.evaluer("presentation_debut", {"nom": "Assurly", "presentation": "Assurly est une société fondée en 2019."})
        self.assertIn("ouvre sur l'entreprise", d)


class Ambassadeurs(unittest.TestCase):
    def test_plan(self):
        r = am.plan(am.EXEMPLE_EQUIPE)
        self.assertEqual(r["total_regime"]["posts"], 7)
        self.assertTrue(any("Léa" in a for a in r["alertes"]))

    def test_montee_en_charge(self):
        r1 = am.plan(am.EXEMPLE_EQUIPE, 1)
        self.assertTrue(all(m["semaine"]["posts"] == 0 for m in r1["membres"]))
        r9 = am.plan(am.EXEMPLE_EQUIPE, 9)
        self.assertEqual(r9["membres"][0]["semaine"]["posts"], 3)

    def test_role_inconnu(self):
        with self.assertRaises(ValueError):
            am.plan({"membres": [{"nom": "X", "role": "astronaute"}]})

    def test_relecture(self):
        self.assertEqual(am.relecture("Ce que j'ai appris en 3 ans au service client.")["niveau"], "A")
        self.assertEqual(am.relecture("Maison Durand a réduit son churn de 12%.", ["Maison Durand"])["niveau"], "B")
        self.assertEqual(am.relecture("Notre levée de fonds arrive.")["niveau"], "C")
        self.assertEqual(am.relecture("On a résolu un litige client.")["niveau"], "C")


if __name__ == "__main__":
    unittest.main()
