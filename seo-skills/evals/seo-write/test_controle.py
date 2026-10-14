"""Tests de controle.py (/seo-write) sur le brouillon IA et l'article propre."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
SCRIPT = ICI.parents[1] / "skills" / "seo-write" / "scripts" / "controle.py"
sys.path.insert(0, str(SCRIPT.parent))
import controle  # noqa: E402

IA = (ICI / "article-ia.md").read_text(encoding="utf-8")
PROPRE = (ICI / "article-propre.md").read_text(encoding="utf-8")
OPTIONS = dict(affirmatif=True, remplacer=["chez Assurly=à Assurly"], interdire=["cash"], longueur=(1000, 1500),
               mot_cle="mutuelle indépendant", marque="Assurly", pref_title=(55, 60), pref_desc=(150, 160))


def constats(texte, **kw):
    opts = dict(OPTIONS, **kw)
    return controle.controler(texte, **opts)


class ArticleIA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = constats(IA)
        cls.texte = " | ".join(c["constat"] for c in cls.r["constats"])

    def test_verdict(self):
        self.assertEqual(self.r["verdict"], "À REVOIR")

    def test_structure(self):
        for attendu in ("résumé en tête absent", "section interdite : « Défis et perspectives »",
                        "section interdite : « Conclusion »", "s'ouvre sans réponse directe"):
            self.assertIn(attendu, self.texte)

    def test_style(self):
        for attendu in ("annonce de plan", "participe présent déductif", "transition toute faite",
                        "verbe d'état gonflé", "verbe modal d'hésitation", "voix passive"):
            self.assertIn(attendu, self.texte)

    def test_maison_et_forme(self):
        for attendu in ("« Chez Assurly » au lieu de « à Assurly »", "phrase entière en gras", "lien annoncé",
                        "ancre vide", "tiret cadratin"):
            self.assertIn(attendu, self.texte)

    def test_bloc_meta(self):
        for attendu in ("année dépassée", "liste de mots-clés", "marque répétée", "probablement coupé"):
            self.assertIn(attendu, self.texte)


class ArticlePropre(unittest.TestCase):
    def test_pret(self):
        r = constats(PROPRE)
        self.assertEqual(r["verdict"], "PRÊT", [c["constat"] for c in r["constats"] if c["gravite"] != "info"])
        self.assertEqual(r["liens_internes"], 4)
        self.assertEqual(len(r["trous"]), 4)

    def test_longueur_seulement_en_info(self):
        r = constats(PROPRE)
        lg = [c for c in r["constats"] if "préférence 1000-1500" in c["constat"]]
        self.assertEqual([c["gravite"] for c in lg], ["info"])

    def test_resume_trop_long(self):
        texte = PROPRE.replace("> Il se termine sur l'erreur que nous voyons le plus souvent en rendez-vous.",
                               "> Il se termine sur l'erreur fréquente. Il cite des cas. Il donne une méthode.")
        r = constats(texte)
        self.assertTrue(any("résumé trop long" in c["constat"] for c in r["constats"]))

    def test_sans_resume_si_le_site_n_en_veut_pas(self):
        texte = "\n".join(l for l in PROPRE.splitlines() if not l.startswith(">"))
        self.assertTrue(any("résumé" in c["constat"] for c in constats(texte)["constats"]))
        self.assertFalse(any("résumé" in c["constat"] for c in constats(texte, resume=False)["constats"]))

    def test_modal_seulement_si_affirmatif(self):
        texte = PROPRE.replace("Vous ajoutez votre conjoint", "Vous pourriez ajouter votre conjoint")
        self.assertTrue(any("modal" in c["constat"] for c in constats(texte)["constats"]))
        self.assertFalse(any("modal" in c["constat"] for c in constats(texte, affirmatif=False)["constats"]))

    def test_bloc_meta_absent(self):
        corps = PROPRE.split("BLOC MÉTA")[0]
        self.assertTrue(any("bloc méta absent" in c["constat"] for c in constats(corps)["constats"]))


class Ligne(unittest.TestCase):
    def test_codes_de_sortie(self):
        args = [sys.executable, str(SCRIPT)]
        self.assertEqual(subprocess.run(args + [str(ICI / "article-ia.md")], capture_output=True).returncode, 2)
        p = subprocess.run(args + [str(ICI / "article-propre.md"), "--remplacer", "chez Assurly=à Assurly", "--json"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertEqual(json.loads(p.stdout)["verdict"], "PRÊT")
        self.assertEqual(subprocess.run(args + ["absent.md"], capture_output=True).returncode, 1)


if __name__ == "__main__":
    unittest.main()
