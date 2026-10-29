#!/usr/bin/env python3
"""Tests de priorite.py : python3 -m unittest discover evals/seo-plan"""
import importlib.util
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("priorite", ICI.parents[1] / "skills" / "seo-plan" / "scripts" / "priorite.py")
pr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pr)


class Idees(unittest.TestCase):
    def test_classement_et_poids(self):
        r = pr.idees(pr.lire_csv(str(ICI / "idees.csv")), (40, 30, 20, 10))
        self.assertEqual([x["idee"] for x in r["classees"]][:2],
                         ["Mutuelle et prévoyance : la différence", "Déduction Madelin pas à pas"])
        self.assertEqual(r["classees"][0]["score"], 8.3)

    def test_note_absente_non_inventee(self):
        r = pr.idees(pr.lire_csv(str(ICI / "idees.csv")), (40, 30, 20, 10))
        self.assertEqual(r["a_completer"], [{"idee": "Mutuelle senior indépendant", "manque": ["recherche"]}])

    def test_autres_poids(self):
        r = pr.idees(pr.lire_csv(str(ICI / "idees.csv")), (0, 0, 1, 0))
        self.assertEqual(r["classees"][0]["idee"], "Déduction Madelin pas à pas")


class Lot(unittest.TestCase):
    def test_doublons_vides_et_trous(self):
        r = pr.lot(pr.lire_csv(str(ICI / "pages-metiers.csv")), "Assurance {metier} à {ville}", None)
        self.assertEqual(len(r["doublons"]), 1)
        self.assertEqual(r["publiables"], 0)
        self.assertEqual(r["verdict"], "À REVOIR")
        electricien = next(x for x in r["champs_vides"] if "électricien" in x["titre"])
        self.assertEqual(electricien["champs"], ["tarif_indicatif"], "un {{à compléter}} n'est pas une donnée")

    def test_pages_interchangeables(self):
        r = pr.lot(pr.lire_csv(str(ICI / "pages-vides.csv")), "Mutuelle {metier} à {ville}", None)
        self.assertEqual(r["verdict"], "À NE PAS PUBLIER")
        self.assertEqual(r["publiables"], 0)

    def test_variable_absente(self):
        with self.assertRaises(pr.Erreur):
            pr.lot(pr.lire_csv(str(ICI / "pages-vides.csv")), "Mutuelle {profession}", None)

    def test_gros_lot_par_tranches(self):
        lignes = [{"metier": f"m{i}", "ville": "Lyon", "donnee": f"d{i}"} for i in range(120)]
        r = pr.lot(lignes, "Assurance {metier} à {ville}", None)
        self.assertTrue(any("lots de 50" in a for a in r["alertes"]))


if __name__ == "__main__":
    unittest.main()
