"""Tests de sources.py (/geo-mentions), hors ligne."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
SCRIPT = PACK / "skills" / "geo-mentions" / "scripts" / "sources.py"
sys.path.insert(0, str(SCRIPT.parent))
import sources as so  # noqa: E402

MESURE = json.loads((ICI / "mesure-septembre.json").read_text(encoding="utf-8"))
REPONSES = ICI / "reponses-septembre-liens.txt"


def lancer(*args):
    p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


class Classement(unittest.TestCase):
    def setUp(self):
        self.r = so.analyser(MESURE, ["assurly.example"], ["april.fr"])
        self.par = {l["domaine"]: l for l in self.r["lignes"]}

    def test_propre_site_exclu(self):
        self.assertNotIn("assurly.example", self.par)

    def test_classe_et_action(self):
        self.assertEqual(self.par["lelynx.fr"]["classe"], "comparateur")
        self.assertIn("évalué", self.par["lelynx.fr"]["action"])
        self.assertEqual(self.par["fr.wikipedia.org"]["classe"], "reference")

    def test_sources_des_questions_perdues_d_abord(self):
        perdues = [l["domaine"] for l in self.r["lignes"] if l["perdues"]]
        self.assertEqual(self.r["lignes"][:len(perdues)], [self.par[d] for d in perdues])
        self.assertIn("P01", self.par["lelynx.fr"]["questions"])

    def test_concurrents_nommes_sur_la_question(self):
        self.assertIn("April", self.par["lelynx.fr"]["concurrents"])

    def test_cite_seulement_ailleurs(self):
        self.assertEqual(self.par["service-public.fr"]["perdues"], 0)

    def test_domaine_concurrent(self):
        m = json.loads(json.dumps(MESURE))
        m["perdues"][0]["sources"]["april.fr"] = 1
        r = so.analyser(m, ["assurly.example"], ["april.fr"])
        self.assertEqual(next(l for l in r["lignes"] if l["domaine"] == "april.fr")["classe"], "concurrent")


class Verification(unittest.TestCase):
    def setUp(self):
        self.r = so.analyser(MESURE, ["assurly.example"], [])
        self.urls = so.urls_citees(str(REPONSES))
        pages = {"https://www.lelynx.fr/expat": "<p>Nos choix : April International, Allianz Care.</p>",
                 "https://www.reddit.com/r/expat/comments/abc": "<p>Assurly a bien remboursé ma fille.</p>"}
        self.ancien = so.pg.lire
        so.pg.lire = lambda u, **k: ({"statut": 200, "texte": pages[u], "erreur": None} if u in pages
                                     else {"statut": None, "texte": "", "erreur": "réseau"})
        so.verifier(self.r["lignes"], self.urls, "Assurly", ["April International", "Allianz Care"])
        self.par = {l["domaine"]: l for l in self.r["lignes"]}

    def tearDown(self):
        so.pg.lire = self.ancien

    def test_url_rattachee_a_sa_question(self):
        self.assertEqual(self.urls[("P01", "lelynx.fr")], ["https://www.lelynx.fr/expat"])
        self.assertEqual(self.urls[("P02", "lelynx.fr")], ["https://www.lelynx.fr/autre-page"])

    def test_marque_absente_et_concurrents_presents(self):
        p = self.par["lelynx.fr"]["pages"][0]
        self.assertEqual(p["etat"], "marque absente")
        self.assertEqual(p["concurrents"], ["April International", "Allianz Care"])

    def test_seules_les_url_des_questions_perdues(self):
        self.assertEqual([p["url"] for p in self.par["lelynx.fr"]["pages"]], ["https://www.lelynx.fr/expat"])

    def test_marque_presente(self):
        self.assertEqual(self.par["reddit.com"]["pages"][0]["etat"], "marque présente")

    def test_domaine_sans_lien_complet(self):
        self.assertEqual(self.par["quechoisir.org"]["pages"][0]["etat"], "URL exacte inconnue")


class Ligne(unittest.TestCase):
    def test_sortie(self):
        code, out, _ = lancer(ICI / "mesure-septembre.json", "--marque", "Assurly", "--domaine", "assurly.example")
        self.assertEqual(code, 0)
        self.assertIn("À TRAVAILLER", out)
        self.assertIn("pas une cause prouvée", out)
        self.assertNotIn("/100", out)

    def test_verifier_sans_reponses(self):
        code, _, err = lancer(ICI / "mesure-septembre.json", "--verifier")
        self.assertEqual(code, 1)

    def test_mesure_illisible(self):
        code, _, err = lancer(REPONSES)
        self.assertEqual(code, 1)
        self.assertIn("visibilite.py", err)


if __name__ == "__main__":
    unittest.main()
