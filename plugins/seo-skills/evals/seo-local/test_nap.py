#!/usr/bin/env python3
"""Tests de nap.py : python3 -m unittest discover evals/seo-local"""
import importlib.util
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("nap", ICI.parents[1] / "skills" / "seo-local" / "scripts" / "nap.py")
nap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nap)


def sources(*noms):
    return dict(nap.lire_source(f"{n}={ICI / f}") for n, f in noms)


class Normalisation(unittest.TestCase):
    def test_telephones_francais(self):
        for t in ("+33 4 78 00 00 00", "04.78.00.00.00", "0478000000", "+33 (0)4 78 00 00 00", "0033478000000"):
            self.assertEqual(nap.norm_tel(t), "0478000000", t)

    def test_abreviations_d_adresse(self):
        self.assertEqual(nap.norm_adresse("12 bd des Belges, 69006 Lyon"), nap.norm_adresse("12 Boulevard des Belges 69006 LYON, France"))
        self.assertEqual(nap.norm_adresse("3 av. St-Exupéry 31000 Toulouse")[0], "3 avenue saint exupery toulouse")

    def test_forme_juridique_ignoree(self):
        self.assertEqual(nap.norm_nom("Assurly SAS"), nap.norm_nom("assurly"))


class Comparaison(unittest.TestCase):
    def test_site_et_fiche_coherents(self):
        r = nap.comparer(sources(("site", "agence-lyon.html"), ("fiche", "fiche-google.txt")))
        self.assertEqual(r["verdict"], "COHÉRENT")
        self.assertEqual(r["sources"]["site"], "JSON-LD")
        self.assertEqual(r["champs"]["adresse"]["verdict"], "ÉCRITURE DIFFÉRENTE")

    def test_annuaire_en_conflit(self):
        r = nap.comparer(sources(("site", "agence-lyon.html"), ("fiche", "fiche-google.txt"), ("annuaire", "annuaire.txt")))
        self.assertEqual(r["verdict"], "CONFLIT")
        self.assertEqual({c for c, v in r["champs"].items() if v["verdict"] == "CONFLIT"}, {"nom", "adresse", "telephone"})

    def test_champ_absent(self):
        r = nap.comparer({"a": {"nom": "Assurly", "adresse": "", "telephone": "0478000000"},
                          "b": {"nom": "Assurly", "adresse": "", "telephone": "04 78 00 00 00"}})
        self.assertEqual(r["champs"]["adresse"]["verdict"], "ABSENT")
        self.assertEqual(r["verdict"], "INCOMPLET")

    def test_code_postal_different(self):
        r = nap.comparer({"a": {"nom": "x", "adresse": "12 rue de la Paix 75002 Paris", "telephone": "0100000000"},
                          "b": {"nom": "x", "adresse": "12 rue de la Paix 75001 Paris", "telephone": "0100000000"}})
        self.assertEqual(r["champs"]["adresse"]["codes_postaux"], ["75001", "75002"])

    def test_html_sans_jsonld_lit_le_telephone_visible(self):
        r = nap.lire_html("<html><body><p>Tél. 04 78 00 00 00</p></body></html>")
        self.assertEqual(nap.norm_tel(r["telephone"]), "0478000000")
        self.assertIn("pas de JSON-LD", r["origine"])


if __name__ == "__main__":
    unittest.main()
