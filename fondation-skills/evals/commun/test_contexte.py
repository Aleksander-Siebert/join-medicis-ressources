#!/usr/bin/env python3
"""Tests de commun/contexte.py : python3 -m unittest evals/commun/test_contexte.py"""
import datetime as dt
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
SCRIPT = PACK / "commun" / "contexte.py"
sys.path.insert(0, str(PACK / "commun"))
import contexte as cx  # noqa: E402

VIDE = PACK / "templates" / "entreprise.md"
EXEMPLE = PACK / "templates" / "exemple-entreprise.md"
JOUR = dt.date(2026, 10, 13)


def lancer(*args):
    p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def fichier(texte):
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    f.write(texte)
    f.close()
    return f.name


PROPRE = """# entreprise.md
- prochaine relecture : 13 janvier 2027

## 1. Identité

| Fait | Valeur | Étiquette | Au | Source |
|---|---|---|---|---|
| Nom commercial | Assurly | LIVE | 01/10/2026 | page d'accueil |
| Ce que nous faisons, en une phrase | Courtier santé | **LIVE** | 2026-10-01 | entretien |
"""


class Etat(unittest.TestCase):
    def test_modele_vide_n_a_jamais_de_bonne_note(self):
        r = cx.analyser(VIDE.read_text(encoding="utf-8"), JOUR, 90)
        self.assertEqual(r["utilisables"], 0)
        self.assertEqual(r["remplies"], 0)
        self.assertEqual(cx.verdict(r), ("vide", 3))
        code, out, _ = lancer("etat", VIDE, "--aujourdhui", "2026-10-13")
        self.assertEqual(code, 3)
        self.assertIn("VIDE", out)

    def test_le_statu_quo_pre_rempli_du_modele_ne_compte_pas(self):
        r = cx.analyser(VIDE.read_text(encoding="utf-8"), JOUR, 90)
        self.assertFalse(r["details"], "une ligne du modèle vide est signalée comme remplie")

    def test_exemple_assurly(self):
        r = cx.analyser(EXEMPLE.read_text(encoding="utf-8"), JOUR, 90)
        self.assertEqual((r["utilisables"], r["a_revoir"], r["retirees"], r["vides"]), (27, 6, 2, 0))
        self.assertEqual(r["trous"], 4)
        self.assertEqual(cx.verdict(r), ("à revoir", 2))
        faits = {l["fait"] for l in r["details"]}
        self.assertIn("Date de création", faits)

    def test_fichier_propre_est_a_jour(self):
        code, out, _ = lancer("etat", fichier(PROPRE), "--aujourdhui", "2026-10-13")
        self.assertEqual(code, 0, out)
        self.assertIn("2 faits utilisables", out)

    def test_fait_trop_ancien(self):
        r = cx.analyser(PROPRE, dt.date(2027, 3, 1), 90)
        self.assertEqual(r["utilisables"], 0)
        self.assertTrue(all("daté de plus de 90 jours" in l["defauts"] for l in r["details"]))
        self.assertTrue(any("relecture" in p for p in r["problemes"]))

    def test_valeur_sans_etiquette_ni_date(self):
        t = PROPRE + "| Site | https://www.assurly.example | | | |\n"
        r = cx.analyser(t, JOUR, 90)
        site = [l for l in r["details"] if l["fait"] == "Site"][0]
        self.assertIn("sans étiquette", site["defauts"])
        self.assertIn("sans date", site["defauts"])
        self.assertIn("sans source", site["defauts"])

    def test_retire_sans_source_n_est_pas_un_defaut(self):
        t = PROPRE + "| Site | ancien-site.example | RETIRÉ | 01/09/2026 | |\n"
        r = cx.analyser(t, JOUR, 90)
        self.assertEqual(r["retirees"], 1)
        self.assertEqual(cx.verdict(r)[1], 0)

    def test_etiquettes_tolerantes(self):
        for brut, attendu in (("À CONFIRMER", "À CONFIRMER"), ("à confirmer", "À CONFIRMER"), ("**LIVE**", "LIVE"),
                              ("Retiré", "RETIRÉ"), ("A CONFIRMER", "À CONFIRMER"), ("peut-être", None), ("", None)):
            self.assertEqual(cx.etiquette(brut), attendu, brut)

    def test_legende_ignoree(self):
        r = cx.analyser(EXEMPLE.read_text(encoding="utf-8"), JOUR, 90)
        self.assertFalse([l for l in r["details"] if l["fait"] in ("**LIVE**", "LIVE")])

    def test_dates(self):
        for texte, attendu in (("13/10/2026", (2026, 10, 13)), ("2026-10-13", (2026, 10, 13)),
                               ("13 octobre 2026", (2026, 10, 13)), ("1er juin 2026", (2026, 6, 1)),
                               ("13 oct. 2026", (2026, 10, 13)), ("septembre 2026", (2026, 9, 1)),
                               ("30 février 2026", None), ("bientôt", None), ("", None)):
            d = cx.lire_date(texte)
            self.assertEqual(d and (d.year, d.month, d.day), attendu, texte)

    def test_fichier_absent(self):
        code, out, _ = lancer("etat", "/nexiste/pas.md")
        self.assertEqual(code, 3)
        self.assertIn("introuvable", out)

    def test_json(self):
        code, out, _ = lancer("etat", EXEMPLE, "--aujourdhui", "2026-10-13", "--json")
        d = json.loads(out)
        self.assertEqual(d[0]["verdict"], "à revoir")
        self.assertEqual(code, 2)

    def test_plusieurs_fichiers_le_pire_code_gagne(self):
        code, _, _ = lancer("etat", fichier(PROPRE), VIDE, "--aujourdhui", "2026-10-13")
        self.assertEqual(code, 3)


class Exporter(unittest.TestCase):
    def test_vers_seo(self):
        code, out, _ = lancer("exporter", "--vers", "seo", EXEMPLE)
        self.assertEqual(code, 0)
        self.assertIn("- **Nom de l'entreprise :** Assurly", out)
        self.assertIn("| Premier mois offert |", out)
        self.assertIn("| RETIRÉ |", out)
        self.assertIn("« Les meilleurs prix du marché »", out)
        self.assertNotIn("{{à confirmer : assurance et intermédiation ; {{", out, "trous emboîtés")
        self.assertIn("Brouillon", out)

    def test_vers_linkedin(self):
        code, out, _ = lancer("exporter", "--vers", "linkedin", EXEMPLE)
        self.assertEqual(code, 0)
        self.assertIn("| Nom | Assurly | LIVE |", out)
        self.assertIn("| Page LinkedIn | {{à compléter}} |", out)
        self.assertIn("## Formulations retirées", out)

    def test_a_confirmer_et_retire(self):
        t = """## 1. Identité

| Fait | Valeur | Étiquette | Au | Source |
|---|---|---|---|---|
| Nom commercial | Assurly | LIVE | 01/10/2026 | accueil |
| Ce que nous faisons, en une phrase | courtier en ligne | À CONFIRMER | 01/10/2026 | déduit |
| Site | https://ancien.example | RETIRÉ | 01/09/2026 | |
"""
        code, out, _ = lancer("exporter", "--vers", "seo", fichier(t))
        self.assertEqual(code, 0)
        self.assertIn("{{à confirmer : courtier en ligne}}", out)
        self.assertIn("- **URL :** {{à compléter}}", out)
        self.assertNotIn("ancien.example", out)

    def test_rien_a_exporter(self):
        code, _, err = lancer("exporter", "--vers", "seo", VIDE)
        self.assertEqual(code, 3)
        self.assertIn("vide", err)

    def test_n_ecrit_aucun_fichier(self):
        avant = sorted(p.name for p in PACK.rglob("*") if p.is_file())
        lancer("exporter", "--vers", "linkedin", EXEMPLE)
        self.assertEqual(avant, sorted(p.name for p in PACK.rglob("*") if p.is_file()))


class Usage(unittest.TestCase):
    def test_help(self):
        code, out, _ = lancer("--help")
        self.assertEqual(code, 0)
        self.assertIn("etat", out)

    def test_commande_inconnue(self):
        code, _, _ = lancer("supprimer")
        self.assertNotEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
