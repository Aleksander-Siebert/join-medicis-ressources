#!/usr/bin/env python3
"""Tests des ajouts v2 de maillage.py (classes, ancres) : python3 -m unittest discover evals/seo-maillage"""
import importlib.util
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("maillage", ICI.parents[1] / "skills" / "seo-maillage" / "scripts" / "maillage.py")
ml = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ml)
CRAWL = ICI.parent / "scripts" / "crawl.csv"


class Classes(unittest.TestCase):
    def test_quatre_classes_et_mentions_legales_au_loin(self):
        r = ml.analyse(ml.load_crawl_csv(CRAWL), {})
        self.assertEqual(set(r["resume_classes"]), {"cœur", "proche", "médian", "lointain"})
        self.assertEqual(sum(v["pages"] for v in r["resume_classes"].values()), r["pages"])
        self.assertEqual(r["classes"]["https://assurly.example/mentions-legales/"]["classe"], "lointain")


class Ancres(unittest.TestCase):
    def page(self, url, ancres):
        return {"url": url, "title": url, "h1": "", "description": "", "texte": "mutuelle indépendant santé",
                "liens": [a for a, _ in ancres], "ancres": ancres}

    def test_ancre_repetee_au_dela_de_40_pourcent(self):
        cible = "https://assurly.example/mutuelle-independant"
        pages = [self.page(f"https://assurly.example/p{i}", [(cible, t)])
                 for i, t in enumerate(["cliquez ici", "cliquez ici", "cliquez ici", "mutuelle pour indépendant"])]
        pages.append(self.page(cible, []))
        r = ml.analyse(pages, {})
        self.assertEqual(len(r["ancres_repetees"]), 1)
        self.assertEqual(r["ancres_repetees"][0]["part"], 0.75)

    def test_ancres_variees_rien_a_signaler(self):
        cible = "https://assurly.example/mutuelle-independant"
        pages = [self.page(f"https://assurly.example/p{i}", [(cible, t)])
                 for i, t in enumerate(["mutuelle indépendant", "choisir sa mutuelle", "mutuelle freelance"])]
        self.assertEqual(ml.analyse(pages, {})["ancres_repetees"], [])

    def test_parseur_lit_le_texte_des_ancres(self):
        p = ml.PageParser("https://assurly.example/")
        p.feed('<p>Voir la <a href="/mutuelle-independant/">mutuelle <b>indépendant</b></a>.</p>')
        self.assertEqual(p.ancres, [("https://assurly.example/mutuelle-independant", "mutuelle indépendant")])


if __name__ == "__main__":
    unittest.main()
