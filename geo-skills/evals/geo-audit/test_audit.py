"""Tests de audit.py (/geo-audit), hors ligne, sur les pages fictives des autres Skills."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
EVALS = ICI.parent
PACK = ICI.parents[1]
SCRIPT = PACK / "skills" / "geo-audit" / "scripts" / "audit.py"
sys.path.insert(0, str(SCRIPT.parent))
import audit as au  # noqa: E402

PAGE = (EVALS / "geo-contenu" / "page-assurly.html").read_text(encoding="utf-8")
PIEGE = (EVALS / "geo-acces" / "robots-piege.txt").read_text(encoding="utf-8")
DEVIS = (EVALS / "geo-agentic" / "devis-piege.html").read_text(encoding="utf-8")
ACCUEIL = (EVALS / "geo-entite" / "accueil-assurly.html").read_text(encoding="utf-8")
URL = "https://assurly.example/mutuelle-independant/"


def auditer(html=PAGE, robots="User-agent: *\nAllow: /\n", statut=200, **k):
    return au.auditer(html, {}, URL, robots, statut, None, "Assurly", **k)


def etats(r):
    return {c["id"]: c["etat"] for c in r["controles"]}


class Note(unittest.TestCase):
    def test_non_mesure_hors_calcul(self):
        r = auditer()
        n = r["note"]
        self.assertEqual(n["possibles"] + n["hors_calcul"], 100)
        self.assertEqual(n["note"], round(100 * n["obtenus"] / n["possibles"]))
        self.assertEqual(etats(r)["A9"], "non mesuré")

    def test_toutes_les_couches_presentes(self):
        self.assertEqual({c["couche"] for c in auditer()["controles"]}, set(au.COUCHES))

    def test_visibilite_jamais_dans_la_note(self):
        mesure = json.loads((EVALS / "geo-mentions" / "mesure-septembre.json").read_text(encoding="utf-8"))
        self.assertEqual(auditer()["note"], auditer(mesure=mesure)["note"])

    def test_chaque_controle_a_preuve_et_source(self):
        for c in auditer()["controles"]:
            self.assertTrue(c["preuve"] and c["source"], c["id"])


class Couches(unittest.TestCase):
    def test_robots_piege(self):
        e = etats(auditer(robots=PIEGE))
        self.assertEqual(e["A2"], "manqué")       # Googlebot sous « * » Disallow: /
        self.assertEqual(e["A5"], "ok")           # OAI-SearchBot a son propre groupe
        self.assertEqual(auditer(robots=PIEGE)["premiere"], "ACCÈS")

    def test_robots_5xx(self):
        e = etats(au.auditer(PAGE, {}, URL, None, 503, None, "Assurly"))
        self.assertEqual(e["A1"], "manqué")
        self.assertEqual(e["A2"], "manqué")

    def test_robots_non_lu(self):
        e = etats(au.auditer(PAGE, {}, URL, None, None, "URLError", "Assurly"))
        self.assertEqual(e["A1"], "non mesuré")
        self.assertEqual(e["A2"], "non mesuré")

    def test_nosnippet(self):
        html = PAGE.replace("<head>", '<head><meta name="robots" content="nosnippet">')
        self.assertEqual(etats(auditer(html))["A4"], "manqué")

    def test_canonical_ailleurs(self):
        html = PAGE.replace("<head>", '<head><link rel="canonical" href="https://assurly.example/autre/">')
        self.assertEqual(etats(auditer(html))["P2"], "manqué")

    def test_h1_double_et_contenu(self):
        e = etats(auditer())
        self.assertEqual(e["P3"], "manqué")
        self.assertEqual(e["C2"], "manqué")
        self.assertEqual(e["C3"], "manqué")
        self.assertEqual(e["C4"], "ok")

    def test_entite(self):
        e = etats(auditer(ACCUEIL))
        self.assertEqual(e["E1"], "manqué")
        self.assertEqual(e["E2"], "manqué")
        self.assertEqual(e["E4"], "manqué")

    def test_consigne_cachee(self):
        e = etats(auditer(DEVIS))
        self.assertEqual(e["G3"], "manqué")
        self.assertEqual(e["G1"], "manqué")

    def test_sonde_refus_a_verifier(self):
        r = au.auditer(PAGE, {}, URL, "User-agent: *\nAllow: /\n", 200, None, "Assurly",
                       sondes={"_navigateur": {"statut": 200}, "OAI-SearchBot": {"statut": 403, "refuse": True}})
        e = etats(r)
        self.assertEqual(e["A9"], "à vérifier")
        self.assertEqual(e["A5"], "ok")   # robots.txt l'autorise : le refus se vérifie à part

    def test_premiere_couche(self):
        # P3 (2 points) manqué ne suffit pas : la première couche avec un manque important est CONTENU (C2, 5 points)
        self.assertEqual(auditer()["premiere"], "CONTENU")


class Ligne(unittest.TestCase):
    def test_sortie(self):
        p = subprocess.run([sys.executable, str(SCRIPT), str(EVALS / "geo-contenu" / "page-assurly.html"), "--url", URL,
                            "--robots", str(EVALS / "geo-acces" / "robots-piege.txt"), "--marque", "Assurly"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        for x in ("PRÉPARATION", "hors calcul", "VISIBILITÉ (mesurée à part", "À VÉRIFIER HORS DU SITE", "Search Console"):
            self.assertIn(x, p.stdout)

    def test_journal(self):
        with tempfile.TemporaryDirectory() as d:
            j = Path(d) / "journal.csv"
            for _ in range(2):
                subprocess.run([sys.executable, str(SCRIPT), str(EVALS / "geo-contenu" / "page-assurly.html"), "--url", URL,
                                "--robots", str(EVALS / "geo-acces" / "robots-piege.txt"), "--journal", str(j)],
                               capture_output=True, text=True)
            lignes = j.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lignes), 3)
            self.assertIn("{{à compléter}}", lignes[1])


if __name__ == "__main__":
    unittest.main()
