"""Tests de skills/linkedin-comment/scripts/commentaire.py."""
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
sys.path.insert(0, str(PACK / "skills" / "linkedin-comment" / "scripts"))
import commentaire as c  # noqa: E402

POST = (ICI / "post-courtier.txt").read_text(encoding="utf-8")
BON = ("On a eu le même mur chez Assurly : coût par lead de 41 € en 2024. Avant de couper, on a rappelé 60 clients "
       "partis ; la moitié parlait du délai de remboursement. Vous avez regardé ce que disent vos résiliés ?")


class Verifier(unittest.TestCase):
    def test_bon(self):
        r = c.verifier(POST, BON)
        self.assertEqual(r["verdict"], "OK", r)
        self.assertIn("41", r["mots_nouveaux"])

    def test_eloge(self):
        r = c.verifier(POST, "Super post, tellement vrai !")
        self.assertEqual(r["code"], 3)

    def test_produit_lien_tiret(self):
        self.assertEqual(c.verifier(POST, BON + " Notre Diagnostic Acquisition aide.", produits=["Diagnostic Acquisition"])["code"], 3)
        self.assertEqual(c.verifier(POST, BON + " https://assurly.example")["code"], 3)
        self.assertEqual(c.verifier(POST, BON.replace(" : coût", " — coût"))["code"], 3)

    def test_pas_d_angle_nouveau(self):
        r = c.verifier(POST, "Le coût par lead a doublé en un an, et couper le budget payant ce trimestre, c'est ce que vous faites.")
        self.assertTrue(any("angle nouveau" in a or "résumé" in a for a in r["attentions"]), r)

    def test_doublon(self):
        r = c.verifier(POST, BON, existants=BON.replace("Assurly", "chez nous"))
        self.assertTrue(any("déjà publié" in a for a in r["attentions"]), r)


class Priorite(unittest.TestCase):
    def test_classement_et_exclusions(self):
        d = {"deja_commentes": {"Paul": 3}, "posts": [
            {"auteur": "A", "cible": 9, "intention": 8, "opportunite": 8, "portee": 5, "age_heures": 2, "commentaires": 10},
            {"auteur": "B", "cible": 4, "intention": 2, "opportunite": 6, "portee": 9, "age_heures": 6, "commentaires": 30},
            {"auteur": "C", "cible": 9, "intention": 9, "opportunite": 9, "portee": 9, "age_heures": 30, "commentaires": 80},
            {"auteur": "Paul", "cible": 9, "intention": 9, "opportunite": 9, "portee": 9, "age_heures": 1, "commentaires": 2},
            {"auteur": "D", "cible": 9, "intention": 9, "opportunite": 1, "portee": 9, "age_heures": 1, "commentaires": 2}]}
        r = c.priorite(d)
        self.assertEqual([p["auteur"] for p in r["a_commenter"]], ["A", "B"])
        self.assertEqual(len(r["exclus"]), 3)
        self.assertTrue(r["a_commenter"][0]["niveau"].startswith("relation"))
        self.assertTrue(r["a_commenter"][1]["niveau"].startswith("visibilité"))


if __name__ == "__main__":
    unittest.main()
