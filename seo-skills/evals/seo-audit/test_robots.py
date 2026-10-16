#!/usr/bin/env python3
"""Tests de robots.py et des corrections v2 d'onpage.py : python3 -m unittest discover evals/seo-audit"""
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
SCRIPTS = ICI.parents[1] / "skills" / "seo-audit" / "scripts"


def charger(nom):
    spec = importlib.util.spec_from_file_location(nom, SCRIPTS / f"{nom}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


rb = charger("robots")
op = charger("onpage")

ROBOTS = """User-agent: *
Disallow: /
Allow: /blog/

User-agent: GPTBot
Disallow: /blog/

User-agent: googlebot
User-agent: Bingbot
Disallow: /*.pdf$
Allow: /
"""


def acces(robot, chemin, texte=ROBOTS, statut=200):
    r = rb.analyser(texte, [chemin], [(robot, "?", "?")], statut)
    return r["robots"][0]["acces"][chemin]["autorise"], r["robots"][0]["groupe"]


class Rfc9309(unittest.TestCase):
    def test_regle_la_plus_longue_l_emporte(self):
        # robotparser de Python dit « bloqué » : première règle, pas la plus longue.
        self.assertEqual(acces("ClaudeBot", "/blog/guide/"), (True, "*"))
        self.assertEqual(acces("ClaudeBot", "/devis/"), (False, "*"))

    def test_groupe_propre_au_robot_remplace_l_etoile(self):
        self.assertEqual(acces("GPTBot", "/"), (True, "GPTBot"))
        self.assertEqual(acces("GPTBot", "/blog/x"), (False, "GPTBot"))

    def test_casse_ignoree_et_agents_groupes(self):
        self.assertEqual(acces("Googlebot", "/blog/x")[0], True)
        self.assertEqual(acces("bingbot", "/doc.pdf")[0], False)

    def test_joker_et_ancre_de_fin(self):
        self.assertFalse(acces("Googlebot", "/fichiers/guide.pdf")[0])
        self.assertTrue(acces("Googlebot", "/fichiers/guide.pdf?v=2")[0])

    def test_egalite_allow_gagne(self):
        t = "User-agent: *\nDisallow: /page\nAllow: /page\n"
        self.assertTrue(acces("X", "/page", t)[0])

    def test_disallow_vide_n_interdit_rien(self):
        self.assertTrue(acces("X", "/", "User-agent: *\nDisallow:\n")[0])

    def test_absent_tout_permis_erreur_tout_interdit(self):
        self.assertTrue(acces("X", "/", None, 404)[0])
        self.assertFalse(acces("X", "/", None, 503)[0])
        self.assertFalse(acces("X", "/", None, None)[0])

    def test_cli_chemin_sans_barre(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "robots.py"), "x.txt", "--chemin", "blog"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)


class OnpageV2(unittest.TestCase):
    def controles(self, html):
        return {c["controle"]: c for c in op.audit(html, "https://assurly.example/x/")["controles"]}

    def test_jsonld_absent_du_html_brut_est_a_verifier(self):
        c = self.controles("<html lang='fr'><head><title>Mutuelle indépendant | Assurly</title></head><body><h1>x</h1></body></html>")
        self.assertEqual(c["Données structurées"]["statut"], "À VÉRIFIER")

    def test_title_mesure_en_pixels(self):
        long = "Mutuelle indépendant : le guide complet pour bien choisir sa couverture santé en 2026 | Assurly"
        c = self.controles(f"<html><head><title>{long}</title></head><body></body></html>")
        self.assertEqual(c["Title"]["statut"], "À REVOIR")
        self.assertIn("px", c["Title"]["valeur"])
        court = self.controles("<html><head><title>Mutuelle indépendant | Assurly</title></head></html>")
        self.assertEqual(court["Title"]["statut"], "OK", "un title court n'est pas une faute")

    def test_nombre_de_mots_n_est_plus_une_faute(self):
        c = self.controles("<html><head><title>x</title></head><body><p>court</p></body></html>")
        self.assertEqual(c["Nombre de mots"]["statut"], "INFO")


if __name__ == "__main__":
    unittest.main()
