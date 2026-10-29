#!/usr/bin/env python3
"""Tests de positions.py : python3 -m unittest discover evals/seo-refresh"""
import importlib.util
import json
import shutil
import tempfile
import unittest
from datetime import date
from pathlib import Path

ICI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("positions", ICI.parents[1] / "skills" / "seo-refresh" / "scripts" / "positions.py")
ps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ps)
EXPORT = str(ICI / "gsc-positions.csv")
AVANT = str(ICI / "gsc-positions-precedent.csv")


class Paniers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = ps.paniers(ps.lire_export(EXPORT), ps.lire_export(AVANT), 100, ("assurly",))

    def requetes(self, panier):
        return [x["requete"] for x in self.r[panier]]

    def test_a_portee(self):
        self.assertEqual(self.requetes("a_portee"), ["mutuelle entreprise obligatoire", "mutuelle tpe", "part employeur mutuelle"])

    def test_plancher_d_impressions(self):
        self.assertNotIn("mutuelle senior indépendant", self.requetes("a_portee"), "60 impressions, sous le plancher")

    def test_clic_faible_contre_le_site_lui_meme(self):
        self.assertEqual(set(self.requetes("clic_faible")), {"plafond madelin", "mutuelle freelance"})
        x = next(x for x in self.r["clic_faible"] if x["requete"] == "plafond madelin")
        self.assertAlmostEqual(x["ctr_attendu"], 0.1345, places=4)

    def test_pas_de_verdict_sans_reference(self):
        self.assertIn(1, self.r["tranches_sans_reference"])

    def test_cannibalisation_sortie_des_paniers(self):
        self.assertEqual(self.r["cannibalisation"], ["indemnités journalières indépendant"])
        tous = self.requetes("a_portee") + self.requetes("presque_en_tete") + self.requetes("clic_faible")
        self.assertNotIn("indemnités journalières indépendant", tous)

    def test_marque_exclue(self):
        self.assertNotIn("assurly avis", self.requetes("clic_faible"))

    def test_pic_signale(self):
        x = next(x for x in self.r["a_portee"] if x["requete"] == "mutuelle entreprise obligatoire")
        self.assertTrue(x["pic"])

    def test_export_sans_position(self):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d)
        (d / "x.csv").write_text("Requête,Page,Clics,Impressions\na,b,1,2\n", encoding="utf-8")
        with self.assertRaises(ps.Erreur):
            ps.lire_export(str(d / "x.csv"))


class Journal(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d)
        self.j = str(self.d / "journal.json")
        self.page = "https://www.assurly.example/mutuelle-entreprise/"

    def test_attendre_puis_sans_effet_puis_arreter(self):
        lignes = ps.lire_export(EXPORT)
        ps.noter(self.j, self.page, "mutuelle tpe", lignes, "section « part employeur » ajoutée", "2026-09-01")
        ps.noter(self.j, self.page, "mutuelle tpe", lignes, "liens depuis le blog", "2026-09-25")
        res = ps.bilan(ps.charger_journal(self.j), lignes, date(2026, 10, 5))
        self.assertEqual(res[0]["verdict"], "sans effet")
        self.assertTrue(res[1]["verdict"].startswith("attendre"))
        res = ps.bilan(ps.charger_journal(self.j), lignes, date(2026, 10, 20))
        self.assertIn("arrêter", res[1]["verdict"])

    def test_effet_mesure(self):
        ps.noter(self.j, self.page, "mutuelle tpe", ps.lire_export(EXPORT), "titre revu", "2026-09-01")
        mieux = [dict(l, position=9.5) if l["requete"] == "mutuelle tpe" else l for l in ps.lire_export(EXPORT)]
        self.assertEqual(ps.bilan(ps.charger_journal(self.j), mieux, date(2026, 10, 5))[0]["verdict"], "effet")

    def test_noter_sans_point_de_depart(self):
        with self.assertRaises(ps.Erreur):
            ps.noter(self.j, self.page, "requête inconnue", ps.lire_export(EXPORT), "x", "2026-09-01")
        self.assertEqual(json.loads((self.d / "journal.json").read_text()) if (self.d / "journal.json").exists() else [], [])


if __name__ == "__main__":
    unittest.main()
