#!/usr/bin/env python3
"""Tests de lire_exports.py : python3 -m unittest discover evals/chatgpt-ads-exports

Exports fictifs (Assurly) : rapport Google Ads en français avec lignes de
titre et ligne de total, export Meta en anglais, fichier en masse Microsoft
Ads, rapport des termes de recherche ; UTF-16 avec tabulations ; XLSX ;
colonne forcée ; amorçage de la campagne.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
SKILL = PACK / "skills" / "chatgpt-ads-exports"
SCRIPT = SKILL / "scripts" / "lire_exports.py"
FIX = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(SKILL / "commun"))
import lire_exports as le  # noqa: E402
import classeur as cl  # noqa: E402


def lancer(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)


class TestLecture(unittest.TestCase):
    def test_google_preambule_et_total(self):
        e = le.lire_export(FIX / "google-annonces.csv")
        self.assertEqual(len(e["lignes"]), 4)
        self.assertEqual(e["lignes"][0]["titres"][:2], ["Assurance expatrié", "Devis en 2 minutes"])
        self.assertEqual(e["lignes"][0]["impressions"], 1250)
        self.assertEqual(e["lignes"][0]["url"], "https://www.assurly.example/expatriation")
        self.assertIn("CTR", e["ignorees"])

    def test_meta(self):
        e = le.lire_export(FIX / "meta-annonces.csv")
        self.assertEqual(e["plateforme"], "meta")
        self.assertEqual(e["lignes"][0]["groupe"], "Familles expatriées")
        self.assertEqual(len(e["lignes"][0]["textes"]), 2)

    def test_microsoft_lignes_de_structure_ignorees(self):
        e = le.lire_export(FIX / "microsoft-bulk.csv")
        self.assertEqual(e["plateforme"], "microsoft")
        self.assertEqual(len(e["lignes"]), 1)
        self.assertEqual(e["lignes"][0]["titres"], ["Assurance expatrié", "Devis immédiat"])

    def test_utf16_tabulations(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "editor.csv"
            f.write_text("Campaign\tAd Group\tHeadline 1\tDescription 1\tFinal URL\n"
                         "C1\tG1\tPartir vivre à Lisbonne\tDémarches pas à pas.\thttps://assurly.example/x\n", encoding="utf-16")
            e = le.lire_export(f)
        self.assertEqual(e["lignes"][0]["titres"], ["Partir vivre à Lisbonne"])

    def test_xlsx(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "e.xlsx"
            cl.ecrire_xlsx(f, [{"adgroup_name": "G1", "title": "Partir vivre à Lisbonne", "copy": "Démarches pas à pas.",
                                "link": "https://assurly.example/x"}])
            e = le.lire_export(f)
        self.assertEqual(e["lignes"][0]["titres"], ["Partir vivre à Lisbonne"])
        self.assertEqual(e["lignes"][0]["url"], "https://assurly.example/x")

    def test_colonne_forcee(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "e.csv"
            f.write_text("Campagne,Accroche courte,URL finale\nC1,Partir vivre à Lisbonne,https://assurly.example/x\n",
                         encoding="utf-8")
            self.assertEqual(le.lire_export(f)["lignes"][0]["titres"], [])
            e = le.lire_export(f, {"titre": "Accroche courte"})
        self.assertEqual(e["lignes"][0]["titres"], ["Partir vivre à Lisbonne"])

    def test_nombres_francais(self):
        self.assertEqual(le.nombre("1 250"), 1250)
        self.assertEqual(le.nombre("3,84 %"), 3.84)
        self.assertEqual(le.nombre("1,234.5"), 1234.5)
        self.assertIsNone(le.nombre("--"))


class TestAnalyse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = le.analyser([le.lire_export(f) for f in sorted(FIX.glob("*.csv"))])

    def test_inventaire(self):
        self.assertEqual(self.a["inventaire"]["annonces"], 7)
        self.assertEqual(self.a["inventaire"]["termes"], 5)

    def test_banque_longueurs(self):
        t = {x["texte"]: x for x in self.a["titres"]}
        self.assertTrue(t["Assurance étudiant monde"]["reutilisable"])
        self.assertFalse(t["Partir vivre à l'étranger"]["reutilisable"])
        self.assertEqual(t["Assurance expatrié"]["occurrences"], 2)
        self.assertIn("paramètre dynamique à retirer", t["{KeyWord:Assurance Expat}"]["a_corriger"])
        self.assertIn("capitales", t["VISA ÉTUDIANT OK"]["a_corriger"])

    def test_allegations_avec_source(self):
        el = {x["element"]: x for x in self.a["allegations"]}
        for e in ("n°1", "29 €", "gratuit", "sans engagement"):
            self.assertIn(e, el)
        self.assertTrue(el["n°1"]["sources"][0].startswith("google-annonces.csv ligne"))

    def test_pages(self):
        p = {x["url"]: x for x in self.a["pages"]}
        self.assertTrue(p["https://www.assurly.example/"]["accueil"])
        self.assertEqual(self.a["domaines"], ["assurly.example"])

    def test_performances_seuil(self):
        perf = self.a["performances"]
        self.assertEqual(perf["mesurees"], 4)
        self.assertEqual(perf["meilleures"][0]["titres"][0], "Assurance expatrié")
        self.assertEqual(perf["sous_le_seuil"], 2)

    def test_situations(self):
        termes = [x["terme"] for x in self.a["situations"]]
        self.assertIn("quelle assurance pour partir vivre au canada", termes)
        self.assertNotIn("assurly", termes)
        self.assertNotIn("assurance expatrié", termes)

    def test_alertes(self):
        self.assertIn("assurance", self.a["categories"])
        self.assertIn("Best student insurance", self.a["langue_anglaise"])


class TestCommandes(unittest.TestCase):
    def test_colonnes(self):
        p = lancer("colonnes", FIX / "google-annonces.csv")
        self.assertEqual(p.returncode, 0)
        self.assertIn("Titre 1", p.stdout)

    def test_colonnes_manquantes(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.csv"
            f.write_text("Campagne,Groupe d'annonces,Clics\nC,G,3\n", encoding="utf-8")
            self.assertEqual(lancer("colonnes", f).returncode, 2)

    def test_analyser_puis_amorcer(self):
        with tempfile.TemporaryDirectory() as d:
            a, md, c = Path(d) / "a.json", Path(d) / "a.md", Path(d) / "c.json"
            p = lancer("analyser", *sorted(FIX.glob("*.csv")), "-o", a, "--md", md)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("## Allégations à vérifier", md.read_text(encoding="utf-8"))
            p = lancer("amorcer", a, "-o", c, "--marque", "Assurly", "--categorie", "assurance")
            camp = json.loads(c.read_text(encoding="utf-8"))
        self.assertEqual(camp["campaigns"][0]["target_countries"], ["FR"])
        self.assertTrue(all(x["statut"] == "à vérifier" for x in camp["allegations"]))
        self.assertEqual(camp["ads"], [])
        self.assertIn("expatriation", [g["adgroup_name"] for g in camp["adgroups"]])

    def test_fichier_absent(self):
        self.assertEqual(lancer("analyser", "absent.csv").returncode, 1)

    def test_colonne_invalide(self):
        self.assertEqual(lancer("--colonne", "inconnu=X", "colonnes", FIX / "meta-annonces.csv").returncode, 1)


if __name__ == "__main__":
    unittest.main()
