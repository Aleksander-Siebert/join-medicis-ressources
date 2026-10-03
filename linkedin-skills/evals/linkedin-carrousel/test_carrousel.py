"""Tests de skills/linkedin-carrousel/scripts/carrousel.py."""
import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
SKILL = PACK / "skills" / "linkedin-carrousel"
sys.path.insert(0, str(SKILL / "scripts"))
import carrousel as c  # noqa: E402


class Controle(unittest.TestCase):
    def test_exemple_ok(self):
        b, a = c.controler(c.EXEMPLE)
        self.assertEqual((b, a), ([], []))

    def test_promesse_tenue(self):
        x = copy.deepcopy(c.EXEMPLE)
        x["slides"][0]["titre"] = "7 vérifications avant de baisser vos prix"
        b, _ = c.controler(x)
        self.assertTrue(any("promet 7" in m for m in b), b)

    def test_bloquants(self):
        for mod in (lambda x: x["slides"][3].update(texte="Commente « GRILLE » pour la recevoir"),
                    lambda x: x["slides"][3].update(texte="On a testé — et ça marche"),
                    lambda x: x["slides"][3].update(texte="Délai de {{à compléter}} jours"),
                    lambda x: x.pop("auteur"),
                    lambda x: x.update(slides=x["slides"][:3])):
            x = copy.deepcopy(c.EXEMPLE)
            mod(x)
            with self.subTest():
                self.assertTrue(c.controler(x)[0])

    def test_trop_de_mots(self):
        x = copy.deepcopy(c.EXEMPLE)
        x["slides"][3]["texte"] = " ".join(["mot"] * 30)
        _, a = c.controler(x)
        self.assertTrue(any("30 mots" in m for m in a))

    def test_banniere_une_slide(self):
        b = json.loads((SKILL / "assets" / "exemple-banniere.json").read_text(encoding="utf-8"))
        self.assertEqual(c.controler(b)[0], [])
        b["slides"].append(b["slides"][0])
        self.assertTrue(c.controler(b)[0])


class Html(unittest.TestCase):
    def test_sections_typo_et_echappement(self):
        x = copy.deepcopy(c.EXEMPLE)
        x["slides"][2]["texte"] = "Une question : <script>alert(1)</script> pourquoi ?"
        h = c.construire_html(x)
        self.assertEqual(h.count("<section"), len(x["slides"]))
        self.assertNotIn("<script>", h)
        self.assertIn(" ?", h)
        self.assertIn(" :", h)
        self.assertIn("10/10", h)

    def test_couleurs_validees(self):
        x = copy.deepcopy(c.EXEMPLE)
        x["couleurs"] = {"accent": "#ff0000", "fond": "red; background:url(x)"}
        h = c.construire_html(x)
        self.assertIn("--accent: #ff0000;", h)
        self.assertNotIn("url(x)", h)


@unittest.skipUnless(c.trouver_chromium(), "Chromium absent")
class Pdf(unittest.TestCase):
    def test_pdf_reel(self):
        d = Path(tempfile.mkdtemp())
        try:
            src = d / "c.json"
            src.write_text(json.dumps(c.EXEMPLE), encoding="utf-8")
            import subprocess
            r = subprocess.run([sys.executable, str(SKILL / "scripts" / "carrousel.py"), "--fichier", str(src),
                                "--sortie", str(d / "c.pdf")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual(c.pages_pdf(d / "c.pdf"), 10)
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
