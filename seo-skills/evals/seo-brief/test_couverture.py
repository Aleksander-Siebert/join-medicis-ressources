"""Tests de couverture.py (/seo-brief) sur les fixtures Assurly du dossier."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
SCRIPT = ICI.parents[1] / "skills" / "seo-brief" / "scripts" / "couverture.py"
sys.path.insert(0, str(SCRIPT.parent))
import couverture  # noqa: E402

PLAN1 = ICI / "plan-mutuelle-independant.md"
PLAN2 = ICI / "plan-mutuelle-independant-v2.md"
REQ = ICI / "requetes-mutuelle-independant.txt"
CONC = [ICI / f"concurrent-{x}.md" for x in "abcd"]


def lancer(*args):
    p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


class Couvrir(unittest.TestCase):
    def test_premier_plan_a_des_manques(self):
        code, out, _ = lancer("couvrir", PLAN1, REQ, "--json")
        r = json.loads(out)
        self.assertEqual(code, 2)
        nc = {d["requete"] for d in r["detail"] if d["statut"] == "non couverte"}
        for attendu in ("mutuelle auto-entrepreneur", "mutuelle indépendant famille", "mutuelle indépendant senior"):
            self.assertIn(attendu, nc)
        self.assertEqual(set(r["termes_de_tete"]), {"independant", "mutuell"})

    def test_plan_corrige_est_mece(self):
        code, out, _ = lancer("couvrir", PLAN2, REQ)
        self.assertEqual(code, 0)
        self.assertIn("couvertes 24", out)
        self.assertIn("VERDICT : MECE OK", out)

    def test_requete_de_tete_rattachee_au_h1(self):
        r = couverture.couvrir(couverture.lire_plan(str(PLAN2)), couverture.lire_requetes(str(REQ)))
        d = next(x for x in r["detail"] if x["requete"] == "mutuelle indépendant")
        self.assertEqual(d["section"], "titre de la page (H1)")

    def test_synonymes_generiques(self):
        r = couverture.couvrir(couverture.lire_plan(str(PLAN2)), couverture.lire_requetes(str(REQ)))
        d = {x["requete"]: x for x in r["detail"]}
        self.assertEqual(d["mutuelle indépendant déductible impôts"]["section"], "Mutuelle Madelin : la déduction des cotisations")
        self.assertEqual(d["mutuelle indépendant prix"]["section"], "Combien coûte une mutuelle indépendant")

    def test_recouvrement_detecte(self):
        with tempfile.TemporaryDirectory() as t:
            plan = Path(t) / "plan.md"
            plan.write_text("# Mutuelle indépendant\n## Prix d'une mutuelle indépendant\nTarifs et coût.\n"
                            "## Combien coûte une mutuelle indépendant\nPrix et tarifs.\n## Madelin\nDéduction.\n",
                            encoding="utf-8")
            req = Path(t) / "req.txt"
            req.write_text("mutuelle indépendant\nmutuelle indépendant prix\nmutuelle indépendant tarif\n"
                           "mutuelle indépendant madelin\nmutuelle indépendant coût\n", encoding="utf-8")
            code, out, _ = lancer("couvrir", plan, req)
            self.assertEqual(code, 2)
            self.assertIn("RECOUVREMENTS", out)

    def test_export_search_console_csv(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "gsc.csv"
            f.write_text("Requêtes les plus fréquentes,Clics,Impressions,CTR,Position\n"
                         "mutuelle indépendant,12,840,1.4%,9.3\nmutuelle indépendant madelin,3,120,2.5%,11.2\n",
                         encoding="utf-8")
            self.assertEqual(couverture.lire_requetes(str(f)), ["mutuelle indépendant", "mutuelle indépendant madelin"])

    def test_format_brief_accepte(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "brief.md"
            f.write_text("H1 Mutuelle indépendant\nH2 Faut-il une mutuelle ? → obligatoire ou non\n"
                         "H2 Combien ça coûte → prix et tarifs\n", encoding="utf-8")
            s = couverture.lire_plan(str(f))
            self.assertEqual([x["niveau"] for x in s], [1, 2, 2])

    def test_erreurs(self):
        with tempfile.TemporaryDirectory() as t:
            vide = Path(t) / "vide.md"
            vide.write_text("pas de titre ici\n", encoding="utf-8")
            self.assertEqual(lancer("couvrir", vide, REQ)[0], 1)
            self.assertEqual(lancer("couvrir", PLAN1, Path(t) / "absent.txt")[0], 1)


class Grille(unittest.TestCase):
    def test_attendus_et_angles_propres(self):
        args = ["grille", PLAN1] + [x for c in CONC for x in ("--concurrent", c)] + ["--json"]
        code, out, _ = lancer(*args)
        r = json.loads(out)
        self.assertEqual(code, 0)
        attendus = [l for l in r["lignes"] if l["classe"] == "attendu"]
        self.assertEqual(len(attendus), 3)
        self.assertTrue(all(l["chez_nous"] for l in attendus))
        obligatoire = next(l for l in attendus if "obligatoire" in l["sous_theme"].lower())
        self.assertEqual(obligatoire["nombre"], 4)
        self.assertIn("Comment choisir sa mutuelle d'indépendant en 4 étapes", r["angles_propres"])

    def test_attendu_manquant_donne_code_2(self):
        with tempfile.TemporaryDirectory() as t:
            plan = Path(t) / "plan.md"
            plan.write_text("# Mutuelle indépendant\n## Ce que rembourse une mutuelle\nHospitalisation, optique.\n",
                            encoding="utf-8")
            args = ["grille", plan] + [x for c in CONC for x in ("--concurrent", c)]
            code, out, _ = lancer(*args)
            self.assertEqual(code, 2)
            self.assertIn("ATTENDUS ABSENTS DE NOTRE PLAN (à ajouter) : ", out)
            self.assertNotIn("(à ajouter) : aucun", out)

    def test_page_html_concurrente(self):
        with tempfile.TemporaryDirectory() as t:
            h = Path(t) / "page.html"
            h.write_text("<!doctype html><html><body><h1>Mutuelle indépendant</h1><h2>Est-ce obligatoire ?</h2>"
                         "<p>texte</p><h3>Le cas du micro-entrepreneur</h3></body></html>", encoding="utf-8")
            s = couverture.lire_plan(str(h))
            self.assertEqual([x["titre"] for x in s],
                             ["Mutuelle indépendant", "Est-ce obligatoire ?", "Le cas du micro-entrepreneur"])

    def test_moins_de_trois_concurrents(self):
        code, out, _ = lancer("grille", PLAN1, "--concurrent", CONC[0], "--concurrent", CONC[1])
        self.assertIn("Moins de 3 concurrents", out)
        self.assertFalse([l for l in out.splitlines() if l.startswith("courant")])


if __name__ == "__main__":
    unittest.main()
