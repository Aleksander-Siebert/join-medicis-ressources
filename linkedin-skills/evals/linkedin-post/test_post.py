"""Tests de skills/linkedin-post (formules.json, lint_post.py, format.py)."""
import json
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
SKILL = PACK / "skills" / "linkedin-post"
sys.path.insert(0, str(SKILL / "scripts"))
import format as fmt  # noqa: E402
import lint_post as lp  # noqa: E402


class Formules(unittest.TestCase):
    def setUp(self):
        self.d = json.loads((SKILL / "formules.json").read_text(encoding="utf-8"))

    def test_completes_et_uniques(self):
        toutes = self.d["accroches"] + self.d["structurelles"]
        ids = [f["id"] for f in toutes]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(self.d["accroches"]), 25)
        for f in toutes:
            for cle in ("nom", "objectif", "squelette", "exemple", "pourquoi", "piege", "source"):
                self.assertTrue(f.get(cle), (f["id"], cle))
            self.assertTrue(set(f["objectif"]) <= {"commentaires", "partages", "reactions", "sauvegardes"}, f["id"])

    def test_pas_de_tiret_cadratin_ni_appat(self):
        brut = (SKILL / "formules.json").read_text(encoding="utf-8")
        self.assertNotIn("—", brut)
        for f in self.d["accroches"]:
            self.assertNotIn("commente", lp.norme(f["squelette"]), f["id"])

    def test_comment_gate_ecartee(self):
        self.assertTrue(any("Comment-Gate" in e["nom"] for e in self.d["ecartees"]))

    def test_tous_les_objectifs_couverts(self):
        couverts = {o for f in self.d["accroches"] for o in f["objectif"]}
        self.assertEqual(couverts, {"commentaires", "partages", "reactions", "sauvegardes"})


class Lint(unittest.TestCase):
    def test_exemples_propres(self):
        self.assertEqual(lp.controler(lp.EXEMPLE)["verdict"], "PRÊT")
        r = lp.controler((ICI / "post-exemple.txt").read_text(encoding="utf-8"), mediane=900)
        self.assertEqual(r["verdict"], "PRÊT", r["constats"])

    def test_brouillon_ia(self):
        r = lp.controler((PACK / "evals" / "linkedin-human" / "brouillon-ia.txt").read_text(encoding="utf-8"))
        self.assertEqual(r["code"], 3)
        familles = {(c["gravite"], c["famille"]) for c in r["constats"]}
        self.assertIn(("bloquant", "intégrité"), familles)
        self.assertIn(("majeur", "densité"), familles)

    def bloquants(self, texte):
        return [c["constat"] for c in lp.controler(texte)["constats"] if c["gravite"] == "bloquant"]

    def test_bloquants(self):
        self.assertTrue(any("3000" in b or "3 000" in b for b in self.bloquants("a" * 3100)))
        self.assertTrue(self.bloquants("Commente « GUIDE » pour recevoir le PDF."))
        self.assertTrue(self.bloquants("Notre méthode 𝗦𝗶𝗺𝗽𝗹𝗲 a marché en 2025."))
        self.assertTrue(self.bloquants("On a signé {{à compléter}} contrats."))
        self.assertTrue(self.bloquants("On a testé — et ça a marché."))

    def test_question_en_ouverture(self):
        r = lp.controler("Pourquoi vos clients partent-ils ?\n\nOn a rappelé 60 assurés en janvier.")
        self.assertTrue(any("Question en première ligne" in c["constat"] for c in r["constats"]))

    def test_densite(self):
        t = ("Ce n'est pas une question de prix, c'est une question de délai.\n\n"
             "Pas une affaire de budget, mais de méthode.\n\nLe résultat ?\n\n9 jours au lieu de 21.")
        r = lp.controler(t)
        self.assertGreaterEqual(r["stats"]["contrastes"], 2)
        self.assertTrue(any("Pont de révélation" in c["constat"] for c in r["constats"]))

    def test_pli_mobile(self):
        long = "On a rappelé soixante assurés qui venaient de résilier et la moitié parlait du délai de remboursement plutôt que du prix et ce constat a tout changé pour nous"
        r = lp.controler(long + ".\n\nSuite.")
        self.assertTrue(any(c["famille"] == "accroche" and "140" in c["constat"] for c in r["constats"]))

    def test_lien_et_hashtags(self):
        r = lp.controler("Notre guide est en ligne : https://assurly.example/guide\n\n#assurance #acquisition #marketing #b2b")
        constats = " ".join(c["constat"] for c in r["constats"])
        self.assertIn("19%", constats)
        self.assertIn("4 hashtags", constats)


class Format(unittest.TestCase):
    def test_exemple(self):
        r = fmt.choisir("clients", ["histoire", "chiffres"], 60)
        self.assertEqual(r["classement"][0]["format"], "texte")
        self.assertTrue(any(a["format"] == "commentaire" for a in r["alternatives"]))

    def test_refus(self):
        r = fmt.choisir("communaute", ["question"], 60)
        self.assertTrue(any("Sondage" in x["format"] for x in r["refus"]))
        r = fmt.choisir("recrutement", ["histoire"], 200)
        self.assertTrue(any("Vidéo" in x["format"] for x in r["refus"]))
        r = fmt.choisir("recrutement", ["histoire"], 200, camera=True)
        self.assertFalse(any("Vidéo" in x["format"] for x in r["refus"]))

    def test_aucun(self):
        self.assertEqual(fmt.choisir("emploi", ["visuel"], 10)["code"], 3)

    def test_inconnu(self):
        with self.assertRaises(ValueError):
            fmt.choisir("viral", ["histoire"], 60)


if __name__ == "__main__":
    unittest.main()
