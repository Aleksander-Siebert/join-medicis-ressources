"""Tests de visibilite.py (/geo-visibilite) et de commun/stats.py, sur les fixtures fictives Assurly."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
SCRIPT = PACK / "skills" / "geo-visibilite" / "scripts" / "visibilite.py"
sys.path.insert(0, str(PACK / "commun"))
sys.path.insert(0, str(SCRIPT.parent))
import stats  # noqa: E402
import visibilite as vis  # noqa: E402

PORTEFEUILLE = ICI / "portefeuille-assurly.csv"
SEPT = ICI / "reponses-septembre.txt"
OCT = ICI / "reponses-octobre.txt"
MARQUE = ["--marque", "Assurly", "--domaine", "assurly.example"]
CONC = ["--concurrent", "April International", "--concurrent", "Allianz Care", "--concurrent", "Cigna"]


def lancer(*args):
    p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def fichier(texte, suffixe=".txt"):
    f = tempfile.NamedTemporaryFile("w", suffix=suffixe, delete=False, encoding="utf-8")
    f.write(texte)
    f.close()
    return f.name


class Stats(unittest.TestCase):
    def test_wilson_valeurs_connues(self):
        bas, haut = stats.wilson(7, 20)
        self.assertAlmostEqual(bas, 0.1812, places=3)
        self.assertAlmostEqual(haut, 0.5671, places=3)

    def test_wilson_zero_et_cent_pour_cent(self):
        self.assertEqual(stats.wilson(0, 5)[0], 0.0)
        self.assertGreater(stats.wilson(0, 5)[1], 0.4)
        self.assertEqual(stats.wilson(5, 5)[1], 1.0)
        self.assertIsNone(stats.wilson(0, 0))

    def test_comparer_bruit_et_vraie_hausse(self):
        self.assertEqual(stats.comparer(4, 5, 3, 5)["verdict"], "pas de changement détectable")
        self.assertEqual(stats.comparer(2, 50, 20, 50)["verdict"], "hausse")
        self.assertEqual(stats.comparer(20, 50, 2, 50)["verdict"], "baisse")

    def test_echantillon(self):
        self.assertEqual(stats.echantillon(10), 97)
        self.assertLess(stats.echantillon(10, 0.3), stats.echantillon(10))

    def test_pourcentage_typographie_et_arrondi(self):
        self.assertEqual(stats.pct(0.125), "13%")
        self.assertEqual(stats.pct(0.3456, 1), "34,6%")


class Texte(unittest.TestCase):
    def test_nom_entier_sans_accent_ni_casse(self):
        m = vis.motif_nom("Fnac")
        self.assertTrue(m.search(vis.norm("Achetez à la FNAC.")))
        self.assertFalse(m.search(vis.norm("La Fnacarde n'existe pas")))
        self.assertTrue(vis.motif_nom("Électro Dépôt").search(vis.norm("chez electro depot")))

    def test_domaines(self):
        d = vis.domaines("Voir https://www.lelynx.fr/x, fr.wikipedia.org et reddit.com/r/expatfr. Mail : a@b.fr")
        self.assertEqual(d, ["lelynx.fr", "fr.wikipedia.org", "reddit.com"])

    def test_recommandation_et_negation(self):
        lex = vis.charger_lexiques()
        m = [vis.motif_nom("Assurly")]
        r = vis.analyser_reponse("Je vous recommande Assurly.", m, [], {}, lex)
        self.assertTrue(r["recommandee"])
        r = vis.analyser_reponse("Je ne recommande pas Assurly pour ce cas.", m, [], {}, lex)
        self.assertFalse(r["recommandee"])
        self.assertTrue(r["deconseillee"])
        r = vis.analyser_reponse("Assurly est une option parmi d'autres.", m, [], {}, lex)
        self.assertTrue(r["mentionnee"])
        self.assertFalse(r["recommandee"] or r["deconseillee"])

    def test_eviter_n_est_pas_une_mise_en_garde(self):
        lex = vis.charger_lexiques()
        r = vis.analyser_reponse("Pour éviter les risques, choisissez Assurly ou un courtier agréé.",
                                 [vis.motif_nom("Assurly")], [], {}, lex)
        self.assertFalse(r["deconseillee"])
        self.assertTrue(r["recommandee"])

    def test_liste_courte_recommandee(self):
        lex = vis.charger_lexiques()
        conc = {"Cigna": [vis.motif_nom("Cigna")], "April": [vis.motif_nom("April")]}
        r = vis.analyser_reponse("Choisissez un courtier sérieux : Cigna, Assurly ou April.", [vis.motif_nom("Assurly")], [], conc, lex)
        self.assertTrue(r["recommandee"])

    def test_recommandation_d_un_concurrent_ne_compte_pas(self):
        lex = vis.charger_lexiques()
        conc = {"Cigna": [vis.motif_nom("Cigna")]}
        r = vis.analyser_reponse("Je recommande Cigna plutôt qu'Assurly.", [vis.motif_nom("Assurly")], [], conc, lex)
        self.assertTrue(r["mentionnee"])
        self.assertFalse(r["recommandee"])


class Portefeuille(unittest.TestCase):
    def test_portefeuille_correct(self):
        code, out, _ = lancer("portefeuille", PORTEFEUILLE, "--marque", "Assurly", "--json")
        r = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(r["alertes"], [])
        self.assertEqual(r["par_cohorte"], {"coeur": 6, "exploratoire": 1, "temoin": 2})
        self.assertEqual(len(r["version_coeur"]), 8)

    def test_alertes(self):
        f = fichier("id;cohorte;intention;prompt\nP1;coeur;marque;Pourquoi Assurly est le meilleur courtier ?\n"
                    "P2;coeur;marque;Assurly est-il fiable ?\nP3;coeur;decouverte;assurance expat\n"
                    "P4;coeur;decouverte;Assurance expat\n", ".csv")
        r = json.loads(lancer("portefeuille", f, "--marque", "Assurly", "--json")[1])
        texte = " ".join(r["alertes"])
        self.assertIn("sous les 70%", texte)
        self.assertIn("pas de témoin où la marque doit apparaître", texte)
        self.assertIn("doublon de P3", texte)
        self.assertIn("question orientée", texte)

    def test_cohorte_inconnue(self):
        f = fichier("id;cohorte;intention;prompt\nP1;principal;x;question\n", ".csv")
        code, _, err = lancer("portefeuille", f, "--marque", "Assurly")
        self.assertEqual(code, 1)
        self.assertIn("cohorte", err)

    def test_version_du_coeur_stable(self):
        a = vis.controler_portefeuille(vis.lire_portefeuille(PORTEFEUILLE), "Assurly", [])
        b = vis.controler_portefeuille(list(reversed(vis.lire_portefeuille(PORTEFEUILLE))), "Assurly", [])
        self.assertEqual(a["version_coeur"], b["version_coeur"])


class Mesurer(unittest.TestCase):
    def setUp(self):
        code, out, _ = lancer("mesurer", SEPT, *MARQUE, *CONC, "--portefeuille", PORTEFEUILLE, "--json")
        self.assertEqual(code, 0)
        self.r = json.loads(out)

    def test_taux_par_moteur(self):
        c = self.r["moteurs"]["ChatGPT"]
        self.assertEqual((c["mentionnee"]["k"], c["mentionnee"]["n"]), (4, 8))
        self.assertEqual(c["citee"]["k"], 1)
        self.assertEqual(c["recommandee"]["k"], 1)
        self.assertEqual(c["deconseillee"]["k"], 1)
        self.assertEqual(self.r["moteurs"]["TOTAL"]["n"], 12)

    def test_temoins(self):
        t = {x["id"]: x for x in self.r["temoins"]}
        self.assertTrue(t["T01"]["ok"])
        self.assertTrue(t["T02"]["ok"])

    def test_questions_perdues_par_moteur(self):
        perdues = {(p["id"], p["moteur"]) for p in self.r["perdues"]}
        self.assertIn(("P01", "ChatGPT"), perdues)
        self.assertNotIn(("P01", "Perplexity"), perdues)
        self.assertNotIn(("T02", "ChatGPT"), perdues)

    def test_classes_de_sources(self):
        cl = self.r["classes"]
        self.assertEqual(cl.get("propre site"), 1)
        self.assertEqual(cl.get("reference"), 1)
        self.assertEqual(cl.get("communaute"), 1)
        self.assertEqual(cl.get("institution"), 1)

    def test_exploratoire_et_etiquette(self):
        self.assertTrue(all(v < vis.PASSAGES_MIN for v in self.r["passages_min"].values()))
        self.assertEqual(self.r["etiquette"], "mesuré (réponses collées)")

    def test_temoin_en_derive(self):
        f = fichier("=== ChatGPT | T02 | Quelle tondeuse robot acheter pour un petit jardin ?\nAssurly vend aussi des tondeuses.\n")
        r = json.loads(lancer("mesurer", f, *MARQUE, "--portefeuille", PORTEFEUILLE, "--json")[1])
        self.assertFalse(r["temoins"][0]["ok"])

    def test_approximation_tavily_etiquetee(self):
        f = fichier("=== Tavily (approximation) | P01 | question\nAssurly.\n")
        r = json.loads(lancer("mesurer", f, *MARQUE, "--json")[1])
        self.assertIn("approximation", r["etiquette"])

    def test_fichier_sans_reponse(self):
        code, _, err = lancer("mesurer", fichier("rien ici"), *MARQUE)
        self.assertEqual(code, 1)
        self.assertIn("Aucune réponse", err)

    def test_format_v1_sans_identifiant(self):
        f = fichier("=== ChatGPT | Quelle assurance pour Dubaï ?\nAssurly et Cigna.\n")
        r = json.loads(lancer("mesurer", f, *MARQUE, "--json")[1])
        self.assertEqual(r["moteurs"]["ChatGPT"]["mentionnee"]["k"], 1)


class Comparer(unittest.TestCase):
    def test_paires_communes_seulement(self):
        code, out, _ = lancer("comparer", SEPT, OCT, *MARQUE, "--portefeuille", PORTEFEUILLE, "--json")
        c = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(c["questions_communes"], 2)
        self.assertNotIn("Perplexity", c["moteurs"])
        m = c["moteurs"]["ChatGPT"]["mentionnee"]
        self.assertEqual((m["avant"]["k"], m["avant"]["n"], m["apres"]["k"], m["apres"]["n"]), (2, 4, 4, 4))
        self.assertEqual(m["verdict"], "pas de changement détectable")


class Grille(unittest.TestCase):
    def test_grille(self):
        code, out, _ = lancer("grille", PORTEFEUILLE, "--moteur", "ChatGPT", "--moteur", "Perplexity", "--passages", "3")
        self.assertEqual(code, 0)
        self.assertEqual(out.count("=== "), 2 * 9 * 3)
        self.assertEqual(len(vis.lire_reponses(fichier(out))), 54)

    def test_tavily_refuse_sans_accord(self):
        code, _, err = lancer("tavily", PORTEFEUILLE)
        self.assertEqual(code, 1)
        self.assertIn("tiers", err)


class Aide(unittest.TestCase):
    def test_aide(self):
        for script in (SCRIPT, PACK / "commun" / "stats.py"):
            p = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0)


class Homonymes(unittest.TestCase):
    """Cas tirés des CHANGELOG de ultimate-seo-geo (1.22.0) et geo-optimizer (#294)."""

    def setUp(self):
        self.lex = vis.charger_lexiques()

    def lire(self, texte, marque, domaines=(), concurrents=None):
        conc = {n: [vis.motif_nom(n)] for n in (concurrents or [])}
        return vis.analyser_reponse(texte, [vis.motif_nom(marque)], list(domaines), conc, self.lex)

    def test_concurrent_dont_le_nom_contient_la_marque(self):
        r = self.lire("Bloom Party Co Bay Area a une note de 4,8.", "Party Co", concurrents=["Bloom Party Co"])
        self.assertFalse(r["mentionnee"])
        self.assertEqual(r["concurrents"], ["Bloom Party Co"])

    def test_marque_et_concurrent_homonyme(self):
        r = self.lire("Je recommande Party Co plutôt que Bloom Party Co.", "Party Co", concurrents=["Bloom Party Co"])
        self.assertTrue(r["mentionnee"])

    def test_domaine_homonyme_n_est_pas_la_marque(self):
        self.assertFalse(self.lire("Essayez geoready.app.", "GeoReady", ["geoready.dev"])["mentionnee"])

    def test_domaine_de_la_marque_compte(self):
        r = self.lire("Essayez geoready.dev.", "GeoReady", ["geoready.dev"])
        self.assertTrue(r["mentionnee"])


if __name__ == "__main__":
    unittest.main()
