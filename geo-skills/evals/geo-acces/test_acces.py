"""Tests de acces.py (/geo-acces) et de commun/robots_rfc.py, hors ligne."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
SCRIPT = PACK / "skills" / "geo-acces" / "scripts" / "acces.py"
sys.path.insert(0, str(PACK / "commun"))
sys.path.insert(0, str(SCRIPT.parent))
import acces  # noqa: E402
import robots_rfc  # noqa: E402

PIEGE = ICI / "robots-piege.txt"
PAGE = ICI / "page-nosnippet.html"


def lancer(*args):
    p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def jouer(robots, chemin="/", statut=200, html=None, erreur=None):
    return acces.analyser(robots, statut, erreur, html, {}, f"https://assurly.example{chemin}", 200)


class RFC9309(unittest.TestCase):
    def test_regle_la_plus_longue(self):
        g = robots_rfc.lire_groupes("User-agent: *\nDisallow: /\nAllow: /blog/\n")
        self.assertTrue(robots_rfc.decision(robots_rfc.groupe_pour(g, "GPTBot")[0], "/blog/a")[0])
        self.assertFalse(robots_rfc.decision(robots_rfc.groupe_pour(g, "GPTBot")[0], "/devis/")[0])

    def test_egalite_allow_gagne_et_jokers(self):
        g = robots_rfc.lire_groupes("User-agent: *\nDisallow: /a\nAllow: /a\nDisallow: /*.pdf$\n")
        r = robots_rfc.groupe_pour(g, "x")[0]
        self.assertTrue(robots_rfc.decision(r, "/a")[0])
        self.assertFalse(robots_rfc.decision(r, "/doc/f.pdf")[0])
        self.assertTrue(robots_rfc.decision(r, "/doc/f.pdf?v=1")[0])

    def test_groupe_propre_remplace_etoile(self):
        g = robots_rfc.lire_groupes("User-agent: *\nDisallow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n")
        self.assertTrue(robots_rfc.decision(robots_rfc.groupe_pour(g, "oai-searchbot")[0], "/x")[0])


class Statuts(unittest.TestCase):
    def test_5xx_tout_interdit(self):
        r = jouer(None, statut=503)
        self.assertFalse(any(b["autorise"] for b in r["robots"]))
        self.assertIn("erreur serveur", r["robots_txt"])

    def test_erreur_reseau_jamais_absent(self):
        r = jouer(None, statut=None, erreur="URLError: proxy")
        self.assertIn("NON LU", r["robots_txt"])
        self.assertNotIn("absent", r["robots_txt"])
        self.assertFalse(any(b["autorise"] for b in r["robots"]))

    def test_404_tout_permis(self):
        r = jouer(None, statut=404)
        self.assertTrue(all(b["autorise"] for b in r["robots"]))


class Affirmations(unittest.TestCase):
    def test_gptbot_bloque_ne_retire_pas_de_chatgpt(self):
        r = jouer("User-agent: GPTBot\nDisallow: /\n")
        a = {x["affirmation"]: x["verdict"] for x in r["affirmations"]}
        self.assertEqual(a["citable dans la recherche de ChatGPT"], "oui")
        self.assertIn("GPTBot", r["entrainement"])
        self.assertFalse(r["entrainement"]["GPTBot"])

    def test_oai_searchbot_bloque(self):
        r = jouer("User-agent: OAI-SearchBot\nDisallow: /\n")
        a = {x["affirmation"]: x["verdict"] for x in r["affirmations"]}
        self.assertEqual(a["citable dans la recherche de ChatGPT"], "non")

    def test_google_extended_sans_effet_sur_les_apercus(self):
        r = jouer("User-agent: Google-Extended\nDisallow: /\n", html="<html><body><p>texte</p></body></html>")
        a = {x["affirmation"]: x["verdict"] for x in r["affirmations"]}
        self.assertTrue(a["éligible aux Aperçus IA et au Mode IA de Google"].startswith("oui"))

    def test_nosnippet_exclut_des_apercus(self):
        r = jouer(PIEGE.read_text(), chemin="/blog/expat/", html=PAGE.read_text())
        a = {x["affirmation"]: x["verdict"] for x in r["affirmations"]}
        self.assertEqual(a["éligible aux Aperçus IA et au Mode IA de Google"], "non")
        self.assertEqual(r["page"]["data_nosnippet"], 1)

    def test_mistral_trois_robots(self):
        jetons = {x["jeton"] for x in acces.ROBOTS}
        self.assertTrue({"MistralAI-Index", "MistralAI-User", "MistralAI-Training"} <= jetons)

    def test_xrobots_tag(self):
        r = acces.analyser("", 200, None, "<html><body>x</body></html>", {"x-robots-tag": "googlebot: noindex"},
                           "https://assurly.example/", 200)
        self.assertEqual(r["page"]["noindex"], ["en-tête X-Robots-Tag"])


class Piege(unittest.TestCase):
    def test_fichier_piege(self):
        code, out, _ = lancer("https://assurly.example/blog/expat/", "--robots", PIEGE, "--html", PAGE, "--json")
        r = json.loads(out)
        self.assertEqual(code, 0)
        self.assertTrue(r["cloudflare"])
        cs = r["content_signal"][0]
        self.assertEqual(cs["valeurs"]["ai-train"], "no")
        self.assertEqual(len(cs["alertes"]), 2)
        roles = {b["jeton"]: b["autorise"] for b in r["robots"]}
        self.assertFalse(roles["GPTBot"])
        self.assertTrue(roles["OAI-SearchBot"])
        self.assertTrue(roles["Googlebot"])

    def test_racine_bloquee_pour_googlebot(self):
        r = jouer(PIEGE.read_text(), chemin="/")
        a = {x["affirmation"]: x["verdict"] for x in r["affirmations"]}
        self.assertEqual(a["éligible aux Aperçus IA et au Mode IA de Google"], "non")


class Propositions(unittest.TestCase):
    def test_equilibre(self):
        code, out, _ = lancer("--proposer", "equilibre")
        self.assertEqual(code, 0)
        bloc = out.split("User-agent: GPTBot")[1].split("\n")[1]
        self.assertEqual(bloc, "Disallow: /")
        self.assertIn("User-agent: OAI-SearchBot\nAllow: /", out)
        self.assertIn("User-agent: Google-Extended\nAllow: /", out)

    def test_refus_entrainement(self):
        out = lancer("--proposer", "refus-entrainement")[1]
        self.assertIn("User-agent: Google-Extended\nDisallow: /", out)
        self.assertIn("User-agent: MistralAI-Index\nAllow: /", out)

    def test_sans_entree(self):
        code, _, err = lancer()
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
