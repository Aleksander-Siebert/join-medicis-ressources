#!/usr/bin/env python3
"""Tests de motscles.py : python3 -m unittest discover evals/seo-keywords"""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
SCRIPT = ICI.parents[1] / "skills" / "seo-keywords" / "scripts" / "motscles.py"
spec = importlib.util.spec_from_file_location("motscles", SCRIPT)
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
SERP = ICI / "serp-mutuelle.txt"
GSC = ICI / "gsc-requetes-pages.csv"


def lancer(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)


class Url(unittest.TestCase):
    def test_normalisation(self):
        self.assertEqual(mc.normaliser_url("https://www.Exemple.fr/guide/?utm_source=x#ancre")[0], "exemple.fr/guide")
        self.assertEqual(mc.normaliser_url("exemple.fr/guide")[0], "exemple.fr/guide")
        self.assertEqual(mc.normaliser_url("http://exemple.fr")[0], "exemple.fr/")


class Recouvrement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res = mc.recouvrement(mc.lire_serp(SERP))

    def paire(self, a, b):
        return next(p for p in self.res["paires"] if {p["a"], p["b"]} == {a, b})

    def test_meme_page(self):
        p = self.paire("mutuelle indépendant", "mutuelle pour indépendant")
        self.assertEqual(p["communes"], 8)
        self.assertEqual(p["verdict"], "même page")
        self.assertIn(["mutuelle indépendant", "mutuelle pour indépendant"], [sorted(x) for x in self.res["pages"]])

    def test_meme_cluster_a_trancher(self):
        p = self.paire("mutuelle indépendant", "mutuelle freelance prix")
        self.assertEqual((p["communes"], p["verdict"], p["a_trancher"]), (5, "même cluster", True))

    def test_sujets_separes(self):
        self.assertEqual(self.paire("mutuelle indépendant", "créer sa micro-entreprise")["verdict"], "sujets séparés")

    def test_plateformes_generalistes_retirees_concurrents_gardes(self):
        self.assertEqual(self.res["omnipresents"], ["fr.wikipedia.org", "youtube.com"])

    def test_meme_url_avec_parametres_comptee_une_fois(self):
        # La SERP 2 cite Wikipédia avec ?utm_source : sans le retrait, elle compterait comme la même URL.
        res = mc.recouvrement(mc.lire_serp(SERP), garder_omnipresents=True)
        p = next(p for p in res["paires"] if {p["a"], p["b"]} == {"mutuelle indépendant", "mutuelle pour indépendant"})
        self.assertEqual(p["communes"], 10)

    def test_echantillon_court_signale(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "s.json"
            f.write_text(json.dumps({"a": ["a.example/1", "b.example/2"], "b": ["a.example/1"]}), encoding="utf-8")
            res = mc.recouvrement(mc.lire_serp(f))
            self.assertTrue(any("échantillon court" in x for x in res["alertes"]))

    def test_commande_et_code(self):
        p = lancer("recouvrement", SERP)
        self.assertEqual(p.returncode, 2)
        self.assertIn("Aucun volume", p.stdout)

    def test_moins_de_deux_requetes(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "s.txt"
            f.write_text("# seule\nhttps://a.example/\n", encoding="utf-8")
            self.assertEqual(lancer("recouvrement", f).returncode, 1)


class SearchConsole(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lignes = mc.lire_export(GSC)

    def test_lecture_et_virgule_dans_la_requete(self):
        self.assertEqual(len(self.lignes), 9)
        self.assertIn("changer de mutuelle en cours d'année", {l["requete"] for l in self.lignes})

    def test_cannibalisation(self):
        cas = mc.cannibalisation(self.lignes, ["assurly"])
        self.assertEqual([c["requete"] for c in cas], ["mutuelle indépendant"])
        self.assertIn("fusionner ou différencier", cas[0]["piste"])

    def test_page_secondaire_marginale_ignoree(self):
        cas = mc.cannibalisation(self.lignes, ["assurly"])
        self.assertNotIn("mutuelle freelance", [c["requete"] for c in cas])
        self.assertNotIn("changer de mutuelle en cours d'année", [c["requete"] for c in cas])

    def test_marque_ignoree(self):
        self.assertIn("assurly avis", [c["requete"] for c in mc.cannibalisation(self.lignes)])
        self.assertNotIn("assurly avis", [c["requete"] for c in mc.cannibalisation(self.lignes, ["Assurly"])])

    def test_groupes_par_page(self):
        g = mc.groupes(self.lignes)
        self.assertEqual(g[0]["page"], "https://www.assurly.example/mutuelle-independant/")
        self.assertEqual([r["requete"] for r in g[0]["requetes"]], ["mutuelle indépendant", "mutuelle freelance"])

    def test_export_anglais_point_virgule(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "e.csv"
            f.write_text("Query;Landing Page;Clicks;Impressions;Average position\n"
                         "a b;https://x.example/1;1;100;5,5\na b;https://x.example/2;1;90;7\n", encoding="utf-8")
            cas = mc.cannibalisation(mc.lire_export(f))
            self.assertEqual(cas[0]["pages"][0]["position"], 5.5)

    def test_export_sans_croisement_refuse(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "q.csv"
            f.write_text("Requêtes les plus fréquentes,Clics,Impressions,CTR,Position\na,1,10,10%,3\n", encoding="utf-8")
            p = lancer("cannibalisation", f)
            self.assertEqual(p.returncode, 1)
            self.assertIn("croise requête et page", p.stderr)

    def test_commandes(self):
        self.assertEqual(lancer("cannibalisation", GSC, "--marque", "assurly").returncode, 2)
        self.assertEqual(lancer("groupes", GSC).returncode, 0)
        self.assertEqual(json.loads(lancer("groupes", GSC, "--json").stdout)[0]["impressions"], 1800)


if __name__ == "__main__":
    unittest.main()
