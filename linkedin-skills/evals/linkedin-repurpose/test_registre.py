"""Tests de registre.py (linkedin-repurpose). Lancer : python3 -m unittest discover -s evals/linkedin-repurpose"""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ICI = Path(__file__).parent
SCRIPT = ICI.parents[1] / "skills" / "linkedin-repurpose" / "scripts" / "registre.py"
spec = importlib.util.spec_from_file_location("registre", SCRIPT)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
SOURCE = (ICI / "source-exemple.md").read_text(encoding="utf-8")
REG = r.lire_registre(ICI / "journal-exemple.md")


class Decouper(unittest.TestCase):
    def setUp(self):
        self.res = r.decouper(SOURCE, "video", REG, "webinaire")
        self.u = {u["titre"]: u for u in self.res["unites"]}

    def test_unites(self):
        self.assertEqual(len(self.res["unites"]), 4)
        self.assertEqual(self.res["code"], 0)
        self.assertEqual(self.u["Le chiffre que personne ne croyait"]["score"], 100)

    def test_renvoi_pendant(self):
        u = self.u["Ce qui a changé"]
        self.assertTrue(u["disqualifiee"])
        self.assertIn("Donc", " ".join(u["manques"]))

    def test_deja_publiee(self):
        self.assertTrue(self.u["Les 60 appels"]["deja_publiee"])
        self.assertFalse(self.u["Le script"]["deja_publiee"])

    def test_traces(self):
        self.assertIn("renvoi au format d'origine (« dans cette vidéo »)", self.u["Le script"]["traces"])
        self.assertIn("tics d'oral de transcription", self.u["Les 60 appels"]["traces"])
        self.assertIn("appel à s'abonner d'une autre plateforme", self.u["Ce qui a changé"]["traces"])

    def test_format_et_accroche(self):
        self.assertTrue(self.u["Le script"]["format"].startswith("carrousel"))
        self.assertFalse(self.u["Le script"]["accroche_possible"].endswith("?"))

    def test_trouve(self):
        self.assertGreaterEqual(self.res["trouve"]["chiffres"], 5)
        self.assertEqual(self.res["trouve"]["erreurs"], 1)
        self.assertFalse(self.res["mince"])

    def test_rien_ne_tient(self):
        res = r.decouper("Donc voilà. Merci à tous.")
        self.assertEqual(res["code"], 3)
        self.assertTrue(res["mince"])

    def test_traces_instagram(self):
        u = r.noter_unite("", "Nouveau post ! Lien en bio. " + "#marketing " * 5 + "On a testé 3 formats en 2025. Le carrousel a gagné. Voici pourquoi, en détail, sur 6 mois de données. " * 3)
        self.assertIn("« lien en bio » (Instagram, TikTok)", u["traces"])
        self.assertIn("mur de hashtags", u["traces"])


class Registre(unittest.TestCase):
    def test_deja_publiee_recemment(self):
        v = r.verifier("La moitié des 60 clients rappelés citait le délai de remboursement, pas le prix", REG, date(2026, 10, 2))
        self.assertEqual(v["code"], 3)

    def test_reprise_apres_90_jours(self):
        v = r.verifier("La moitié des 60 clients rappelés citait le délai de remboursement, pas le prix", REG, date(2027, 1, 15))
        self.assertEqual(v["code"], 2)

    def test_deux_fois_en_8_mois(self):
        reg = REG + [dict(REG[0], date=date(2026, 5, 2))]
        v = r.verifier("La moitié des 60 clients rappelés citait le délai de remboursement, pas le prix", reg, date(2026, 12, 20))
        self.assertEqual(v["code"], 3)

    def test_nouvelle(self):
        self.assertEqual(r.verifier("Le script de 5 questions pour appeler un client parti", REG, date(2026, 10, 2))["code"], 0)

    def test_noter(self):
        with tempfile.TemporaryDirectory() as d:
            j = Path(d) / "journal.md"
            shutil.copy(ICI.parents[1] / "templates" / "journal.md", j)
            r.noter(j, "Le script de 5 questions", "webinaire", "carrousel", jour="2026-10-06")
            reg = r.lire_registre(j)
            self.assertEqual(len(reg), 1)
            self.assertEqual(reg[0]["date"], date(2026, 10, 6))
            self.assertIn("## Candidatures", j.read_text(encoding="utf-8"))

    def test_cli(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "decouper", "--fichier", str(ICI / "source-exemple.md")],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertIn("TROUVÉ", p.stdout)


if __name__ == "__main__":
    unittest.main()
