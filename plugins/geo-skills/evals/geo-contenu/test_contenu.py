"""Tests de contenu.py (/geo-contenu), hors ligne, sur des pages fictives."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
SCRIPT = PACK / "skills" / "geo-contenu" / "scripts" / "contenu.py"
sys.path.insert(0, str(SCRIPT.parent))
import contenu as ct  # noqa: E402

PAGE = (ICI / "page-assurly.html").read_text(encoding="utf-8")
ARTICLE = (ICI / "article-assurly.md").read_text(encoding="utf-8")
ANIME = (ICI / "titre-anime.html").read_text(encoding="utf-8")


def lancer(*args):
    p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def section(r, debut):
    return next(s for s in r["sections"] if s["titre"].startswith(debut))


def md(texte, question=None):
    return ct.analyser("t.md", None, texte, {}, question)


class Sections(unittest.TestCase):
    def setUp(self):
        self.r = ct.analyser("page", PAGE, None, {}, "Combien coûte une mutuelle pour indépendant ?")

    def test_reponse_en_tete(self):
        self.assertTrue(section(self.r, "Combien")["controles"]["reponse"][0])

    def test_preambule(self):
        ok, motif, _ = section(self.r, "Introduction")["controles"]["reponse"]
        self.assertFalse(ok)
        self.assertIn("préambule", motif)

    def test_pronom_en_tete(self):
        self.assertFalse(section(self.r, "Les garanties")["controles"]["autonome"][0])

    def test_statistique_sans_source(self):
        ok, motif, preuve = section(self.r, "Le marché")["controles"]["sources"]
        self.assertFalse(ok)
        self.assertIn("8%", preuve)

    def test_prix_de_l_offre_pas_une_statistique(self):
        self.assertIsNone(section(self.r, "Combien")["controles"]["sources"][0])

    def test_source_interne_nommee(self):
        self.assertTrue(section(self.r, "Notre avis")["controles"]["sources"][0])

    def test_promesse_a_prouver(self):
        ok, motif, _ = section(self.r, "Notre avis")["controles"]["promesses"]
        self.assertFalse(ok)
        self.assertIn("le meilleur", motif)

    def test_premiere_main(self):
        self.assertEqual([x["section"] for x in self.r["premiere_main"]], ["Notre avis"])

    def test_nav_et_pied_de_page_ignores(self):
        self.assertFalse(any("mentions légales" in s["titre"] for s in self.r["sections"]))


class Page(unittest.TestCase):
    def test_h1_en_double(self):
        r = ct.analyser("page", PAGE, None, {}, None)
        self.assertTrue(any("doublon exact" in a for a in r["alertes"]))

    def test_titre_anime_un_seul_h1(self):
        # texte pour lecteur d'écran + lettres aria-hidden : un seul H1, pas de doublon
        r = ct.analyser("page", ANIME, None, {}, None)
        self.assertFalse(any("H1" in a for a in r["alertes"]))
        self.assertNotIn("L e", json.dumps(r, ensure_ascii=False))

    def test_texte_cache_ignore(self):
        r = ct.analyser("page", ANIME, None, {}, None)
        self.assertNotIn("Texte caché", json.dumps(r, ensure_ascii=False))

    def test_date_json_ld_reconnue(self):
        r = ct.analyser("page", PAGE, None, {}, None)
        self.assertFalse(any("date" in a for a in r["alertes"]))

    def test_page_mince(self):
        r = ct.analyser("page", ANIME, None, {}, None)
        self.assertTrue(any("HTML serveur" in a for a in r["alertes"]))


class Markdown(unittest.TestCase):
    def test_tableau_et_etapes_repondent(self):
        r = md(ARTICLE)
        self.assertTrue(section(r, "CFE ou premier")["controles"]["reponse"][0])
        self.assertTrue(section(r, "Comment souscrire")["controles"]["reponse"][0])

    def test_renvoi(self):
        ok, motif, preuve = section(md(ARTICLE), "Comment souscrire")["controles"]["autonome"]
        self.assertFalse(ok)
        self.assertIn("ci-dessus", preuve)

    def test_selon_seul_n_est_pas_une_source(self):
        r = md("## Le marché\n\nLe tarif moyen a augmenté de 8% en un an selon la formule choisie et l'âge de l'assuré.")
        self.assertFalse(r["sections"][0]["controles"]["sources"][0])

    def test_source_nommee(self):
        r = md("## Le marché\n\nLe tarif moyen a augmenté de 8% en un an, selon la DREES, pour toutes les formules du marché.")
        self.assertTrue(r["sections"][0]["controles"]["sources"][0])


class Familles(unittest.TestCase):
    def test_types_de_question(self):
        self.assertEqual(ct.type_question("Combien coûte une mutuelle ?"), "prix")
        self.assertEqual(ct.type_question("CFE ou premier euro ?"), "comparaison")
        self.assertEqual(ct.type_question("Où acheter un iPhone reconditionné ?"), "choix")
        self.assertEqual(ct.type_question("Comment résilier sa mutuelle ?"), "procedure")
        self.assertEqual(ct.type_question("Qu'est-ce que la CFE ?"), "definition")

    def test_prix_couvert(self):
        r = ct.analyser("page", PAGE, None, {}, "Combien coûte une mutuelle pour indépendant ?")
        self.assertTrue(all(f["presente"] for f in r["couverture"]["familles"]))

    def test_famille_absente(self):
        r = md("## Prix\n\nAssurly propose trois formules simples pour les indépendants, avec un devis en ligne gratuit.",
               "Combien coûte Assurly ?")
        absentes = [f["famille"] for f in r["couverture"]["familles"] if not f["presente"]]
        self.assertIn("montant chiffré", absentes)


class Ligne(unittest.TestCase):
    def test_sortie_texte(self):
        code, out, _ = lancer(ICI / "page-assurly.html", "--question", "Combien coûte une mutuelle ?")
        self.assertEqual(code, 0)
        for x in ("BILAN", "FAMILLES DE FAITS", "SECTIONS", "pas des signaux de classement"):
            self.assertIn(x, out)
        self.assertNotIn("/100", out)

    def test_fichier_absent(self):
        code, _, err = lancer(ICI / "absent.html")
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
