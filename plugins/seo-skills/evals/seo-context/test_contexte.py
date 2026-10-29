#!/usr/bin/env python3
"""Tests du contexte partagé : python3 -m unittest discover evals/seo-context

/seo-context n'a pas de script : ces tests vérifient que les modèles qu'il
remplit tiennent les promesses que les autres Skills supposent.
"""
import importlib.util
import re
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
RACINE = next(d for d in PACK.parents if (d / ".claude-plugin" / "marketplace.json").exists())  # racine du dépôt
MODELES = PACK / "templates"
SKILL = (PACK / "skills" / "seo-context" / "SKILL.md").read_text(encoding="utf-8")


class Modeles(unittest.TestCase):
    def test_sections_du_modele(self):
        t = (MODELES / "site-context.md").read_text(encoding="utf-8")
        for s in ("Le secteur", "Les lecteurs", "Les pages à pousser", "Le ton", "Les règles maison",
                  "Les données produit", "Les auteurs", "Les preuves de l'entreprise", "Les concurrents", "Les outils connectés"):
            self.assertIn(s, t, s)

    def test_etiquettes_documentees(self):
        t = (MODELES / "site-context.md").read_text(encoding="utf-8")
        for e in ("`LIVE`", "`À CONFIRMER`", "`RETIRÉ`"):
            self.assertIn(e, t)
            self.assertIn(e, SKILL)

    def test_exemple_fictif_et_ymyl(self):
        t = (MODELES / "exemple-site-context.md").read_text(encoding="utf-8")
        self.assertIn("Exemple fictif", t)
        self.assertIn("Assurly", t)
        self.assertTrue(re.search(r"\| LIVE \|", t), "l'exemple montre au moins une donnée LIVE")

    def test_reserve_partagee_avec_linkedin(self):
        li = RACINE / "linkedin-skills" / "templates" / "reserve.md"
        if li.exists():
            self.assertEqual((MODELES / "reserve.md").read_text(encoding="utf-8"), li.read_text(encoding="utf-8"))

    def test_affirmations_compte_le_contexte_comme_fourni(self):
        spec = importlib.util.spec_from_file_location("affirmations", PACK / "commun" / "affirmations.py")
        af = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(af)
        src = (PACK / "commun" / "affirmations.py").read_text(encoding="utf-8")
        self.assertIn("--contexte", src)


if __name__ == "__main__":
    unittest.main()
