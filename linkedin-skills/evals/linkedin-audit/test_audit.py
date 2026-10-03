"""Tests de audit.py (linkedin-audit). Lancer : python3 -m unittest discover -s evals/linkedin-audit"""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ICI = Path(__file__).parent
SCRIPT = ICI.parents[1] / "skills" / "linkedin-audit" / "scripts" / "audit.py"
spec = importlib.util.spec_from_file_location("audit", SCRIPT)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def posts(fichier=ICI / "posts-exemple.csv", **kw):
    lignes, _ = a.normaliser(a.lire(fichier))
    return a.preparer(lignes, **kw)[0]


def xlsx(chemin, lignes):
    """Construit un .xlsx minimal : une ligne de titre, puis l'en-tête et les données."""
    partages, idx = [], {}

    def s(v):
        if v not in idx:
            idx[v] = len(partages)
            partages.append(v)
        return idx[v]
    rows = []
    for r, ligne in enumerate(lignes, 1):
        cel = []
        for c, v in enumerate(ligne):
            ref = chr(65 + c) + str(r)
            if isinstance(v, (int, float)):
                cel.append(f'<c r="{ref}"><v>{v}</v></c>')
            else:
                cel.append(f'<c r="{ref}" t="s"><v>{s(v)}</v></c>')
        rows.append(f'<row r="{r}">{"".join(cel)}</row>')
    ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    with zipfile.ZipFile(chemin, "w") as z:
        z.writestr("xl/sharedStrings.xml", f'<sst xmlns="{ns}">' + "".join(f"<si><t>{p}</t></si>" for p in partages) + "</sst>")
        z.writestr("xl/worksheets/sheet1.xml", f'<worksheet xmlns="{ns}"><sheetData>{"".join(rows)}</sheetData></worksheet>')


class Lecture(unittest.TestCase):
    def test_csv_francais(self):
        p = posts()
        self.assertEqual(len(p), 14)
        self.assertEqual(p[0]["reactions"], 41)
        self.assertEqual(p[0]["longueur"], "moyen (800-1500)")
        self.assertEqual(p[0]["reponse"], "oui")

    def test_xlsx(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "export.xlsx"
            lignes = [["Statistiques du contenu"], ["Date de publication", "Impressions", "Réactions", "Commentaires", "Republications"]]
            lignes += [[t[0], t[1], t[2], t[3], t[4]] for t in a.EXEMPLE]
            xlsx(f, lignes)
            p = posts(f)
            self.assertEqual(len(p), 14)
            self.assertEqual(p[2]["impressions"], 2900)

    def test_nombres_francais(self):
        self.assertEqual(a.nombre("1 234"), 1234)
        self.assertEqual(a.nombre("2,5%"), 2.5)
        self.assertEqual(a.nombre("1.234,5"), 1234.5)

    def test_journal_complete_les_formules(self):
        with tempfile.TemporaryDirectory() as d:
            csvf = Path(d) / "p.csv"
            csvf.write_text("date;impressions;reactions;commentaires;republications\n2026-05-05;2100;41;12;2\n", encoding="utf-8")
            j = Path(d) / "j.md"
            j.write_text("## Posts\n\n| date | formule | objectif | format | pilier | longueur | appel à l'action | première ligne |\n"
                         "|---|---|---|---|---|---|---|---|\n| 2026-05-05 | chiffre-d-abord | sauvegardes | texte | Rétention | 1250 | question | x |\n",
                         encoding="utf-8")
            lignes, _ = a.normaliser(a.lire(csvf))
            self.assertEqual(a.joindre_journal(lignes, j), 1)
            p = a.preparer(lignes)[0][0]
            self.assertEqual((p["formule"], p["pilier"], p["format"]), ("chiffre-d-abord", "Rétention", "texte"))


class Decrire(unittest.TestCase):
    def test_mediane_et_bandes(self):
        r = a.decrire(posts())
        self.assertEqual(r["verdict"], "ANALYSÉ")
        self.assertAlmostEqual(r["cv"], 0.447, places=3)
        self.assertEqual(r["top"][0]["date"], "2026-06-02")
        self.assertEqual(sum(r["bandes"].values()), 14)

    def test_moins_de_10(self):
        r = a.decrire(posts()[:8])
        self.assertEqual(r["code"], 2)
        self.assertEqual(r["flop"], [])

    def test_portee_sans_abonnes(self):
        self.assertEqual(a.decrire(posts(), "portee")["code"], 3)
        self.assertEqual(a.decrire(posts(abonnes=2000), "portee")["code"], 0)

    def test_voix_separees(self):
        lignes = [{"date": "2026-05-0%d" % i, "impressions": 100, "reactions": 1, "commentaires": 0, "republications": 0,
                   "voix": "page" if i % 2 else "profil"} for i in range(1, 9)]
        self.assertEqual(len(a.preparer(lignes, voix="page")[0]), 4)

    def test_contacts(self):
        from datetime import date
        c = a.contacts_journal(ICI / "journal-exemple.md", date(2026, 5, 1), date(2026, 6, 30))
        self.assertEqual(c["total"], 3)


class Motifs(unittest.TestCase):
    def test_refus_sous_10(self):
        self.assertEqual(a.motifs(posts()[:9], ["format"])["code"], 3)

    def test_soutenus_et_confondus(self):
        r = a.motifs(posts(), ["formule", "format", "pilier", "longueur", "reponse", "jour"])
        soutenus = {(c["attribut"], c["valeur"]) for c in r["soutenus"]}
        self.assertIn(("format", "texte"), soutenus)
        self.assertTrue(any("format = texte" in g and "jour = jeudi" in g for g in r["confondus"]))
        self.assertLess(r["signaux_distincts"], len(r["soutenus"]))
        # longueur courte (tous des jeudis) : regroupée elle aussi (bug trouvé par l'éval à l'aveugle)
        self.assertTrue(any("longueur = court (<800)" in g for g in r["confondus"]))

    def test_formules_non_testees(self):
        r = a.motifs(posts(), ["formule"])
        self.assertTrue(all(c["verdict"] == "NON TESTÉ" for c in r["candidats"]))
        self.assertEqual(r["code"], 2)

    def test_jour_en_dernier(self):
        r = a.motifs(posts(), ["jour", "format"])
        self.assertEqual(r["candidats"][-1]["attribut"], "jour")

    def test_bruit_ne_survit_pas(self):
        import random
        rng = random.Random(1)
        lignes = [{"date": f"2026-0{1 + i // 28}-{1 + i % 28:02d}", "impressions": 1000, "reactions": rng.randint(15, 25),
                   "commentaires": 3, "republications": 0, "format": rng.choice(["texte", "carrousel"])} for i in range(30)]
        p = a.preparer(a.normaliser(lignes)[0])[0]
        self.assertEqual(a.motifs(p, ["format"])["verdict"], "RIEN N'A SURVÉCU")

    def test_deterministe(self):
        self.assertEqual(a.motifs(posts(), ["format", "pilier"]), a.motifs(posts(), ["format", "pilier"]))


class Experience(unittest.TestCase):
    def test_taille(self):
        r = a.experience("h", "format", 0.45, 0.3, 2)
        self.assertEqual(r["posts_par_variante"], 28)
        self.assertEqual(r["verdict"], "TROP LONG")

    def test_faisable(self):
        r = a.experience("h", "format", 0.447, 0.5, 3, 12)
        self.assertEqual((r["posts_par_variante"], r["semaines"], r["code"]), (10, 7, 0))
        self.assertTrue(r["ligne_apprentissages"].startswith("| "))

    def test_refus(self):
        self.assertEqual(a.experience("", "x", 0.4, 0.3, 2)["code"], 3)
        self.assertEqual(a.experience("h", "x", 0.4, 0.3, 2, alpha=0.01)["code"], 3)


class Cli(unittest.TestCase):
    def test_exemple(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "decrire", "--exemple"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertIn("médiane 2,3%", p.stdout)


if __name__ == "__main__":
    unittest.main()
