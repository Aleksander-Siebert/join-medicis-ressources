"""Tests du script de collecte (python3 -m unittest discover -s tests)."""
import json
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent / "scripts"))
import collecte as c  # noqa: E402

FX = ICI / "fixtures"
MAINTENANT = datetime(2026, 11, 9, 7, 0, tzinfo=timezone.utc)


def faux_web(pages):
    def telecharge(url):
        for motif, fichier in pages.items():
            if motif in url:
                return (FX / fichier).read_text("utf-8")
        raise OSError(f"injoignable : {url}")
    return telecharge


CONFIG = {
    "jours": 7, "langue": "fr", "pays": "FR", "actualites_google": True, "max_sujets": 40, "mots_exclus": [], "flux_secteur": [],
    "concurrents": [{"nom": "Concurrent A", "site": "https://concurrent-a.example", "flux": ["https://concurrent-a.example/feed"], "pages": ["https://concurrent-a.example/tarifs"]}],
}


class Outils(unittest.TestCase):
    def test_url_canonique_retire_le_pistage(self):
        self.assertEqual(c.url_canonique("http://www.Site.example/a/?utm_source=x&id=3#haut"), "https://site.example/a?id=3")

    def test_titres_proches(self):
        a = c.cle_titre("Concurrent A lance une offre santé à 9 euros")
        b = c.cle_titre("Concurrent A lance une nouvelle offre santé à 9 euros")
        z = c.cle_titre("Concurrent A recrute 50 personnes à Lyon")
        self.assertTrue(c.titres_proches(a, b))
        self.assertFalse(c.titres_proches(a, z))

    def test_dates(self):
        self.assertEqual(c.lire_date("Fri, 06 Nov 2026 08:00:00 GMT").day, 6)
        self.assertEqual(c.lire_date("2026-11-05T12:00:00Z").hour, 12)
        self.assertEqual(c.lire_date("2026-11-05").month, 11)
        self.assertIsNone(c.lire_date("hier"))

    def test_mention_insensible_aux_accents_et_mots_entiers(self):
        self.assertTrue(c.mentionne("Le géant ÉTOILE annonce", ["Etoile"]))
        self.assertFalse(c.mentionne("Alanis Morissette en concert", ["Alan"]))

    def test_titre_google(self):
        self.assertEqual(c.decouper_titre_google("Titre de l'info - Les Échos", "Google Actualités"), ("Titre de l'info", "Les Échos"))

    def test_flux_atom_et_rss(self):
        atom = c.lire_flux((FX / "blog.atom").read_text("utf-8"), "blog")
        self.assertEqual(atom[0]["lien"], "https://concurrent-a.example/blog/app")
        self.assertIsNone(atom[1]["date"])
        with self.assertRaises(ValueError):
            c.lire_flux("<html><body>pas un flux</body></html>", "x")
        rss = c.lire_flux((FX / "google.xml").read_text("utf-8"), "g")
        self.assertEqual(rss[0]["extrait"], "Concurrent A annonce une offre santé.")
        self.assertEqual(rss[0]["domaine"], "media-un.example")
        self.assertEqual(atom[0]["extrait"], "Nous lançons l'application.")

    def test_texte_de_page_ignore_scripts_et_trouve_le_flux(self):
        lignes, flux = c.texte_de_page((FX / "tarifs-v1.html").read_text("utf-8"))
        self.assertIn("12 € par mois", lignes)
        self.assertFalse(any("var x" in l for l in lignes))
        self.assertEqual(flux, ["/feed.xml"])

    def test_liens_utiles(self):
        page = '<a href="/fr/tarifs">Nos tarifs</a><a href="https://ailleurs.example/prix">x</a><a href="/blog/">Blog</a><a href="/contact">Contact</a>'
        self.assertEqual(c.liens_utiles(page, "https://www.site.example/fr"), ["https://www.site.example/blog/", "https://www.site.example/fr/tarifs"])

    def test_changements_ignorent_l_heure(self):
        v1, _ = c.texte_de_page((FX / "tarifs-v1.html").read_text("utf-8"))
        v2, _ = c.texte_de_page((FX / "tarifs-v2.html").read_text("utf-8"))
        ajouts, retraits = c.changements(v1, v2)
        self.assertIn("9 € par mois", ajouts)
        self.assertIn("Premium", ajouts)
        self.assertIn("12 € par mois", retraits)
        self.assertNotIn("09:42", ajouts)


class Collecte(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        (self.d / "sources.json").write_text(json.dumps(CONFIG), "utf-8")
        self.web = faux_web({"news.google.com": "google.xml", "/feed": "blog.atom", "/tarifs": "tarifs-v1.html"})

    def tearDown(self):
        shutil.rmtree(self.d)

    def run_collecte(self, web=None):
        cfg = c.lire_config(self.d)
        res = c.collecter(cfg, c.charger_memoire(self.d), self.d, MAINTENANT, telecharge=web or self.web)
        (self.d / "sortie").mkdir(exist_ok=True)
        (self.d / "sortie" / "a-traiter.json").write_text(json.dumps(res["sortie"], default=c._json_defaut), "utf-8")
        (self.d / "sortie" / ".pages.json").write_text(json.dumps(res["snapshots"], default=c._json_defaut), "utf-8")
        return res["sortie"]

    def test_premiere_collecte(self):
        s = self.run_collecte()
        titres = [x["titre"] for x in s["sujets"]]
        # l'offre santé reprise par deux médias = un seul sujet avec deux sources
        offre = [x for x in s["sujets"] if "offre santé" in x["titre"]]
        self.assertEqual(len(offre), 1)
        self.assertEqual(len(offre[0]["sources"]), 2)
        self.assertNotIn("Concurrent A lève 20 millions", titres)  # trop vieux
        self.assertNotIn("Un autre sujet sans rapport", titres)  # ne cite pas le concurrent
        self.assertIn("Notre nouvelle application mobile", titres)  # flux du concurrent
        sans_date = [x for x in s["sujets"] if x["titre"] == "Sans date"]
        self.assertTrue(sans_date and sans_date[0]["date_inconnue"])
        self.assertEqual(s["stats"]["trop_vieux"], 1)
        self.assertEqual(s["stats"]["hors_sujet"], 1)
        self.assertTrue(s["pages_modifiees"][0]["premiere_visite"])
        self.assertEqual(s["erreurs"], [])

    def test_rien_n_est_renvoye_apres_validation(self):
        self.run_collecte()
        c.valider(self.d, MAINTENANT)
        s = self.run_collecte()
        self.assertEqual(s["sujets"], [])
        self.assertGreaterEqual(s["stats"]["deja_envoyes"], 4)
        self.assertEqual(s["pages_modifiees"], [])  # page identique

    def test_sans_validation_rien_n_est_perdu(self):
        self.run_collecte()
        s = self.run_collecte()  # mail pas envoyé : on retrouve les mêmes sujets
        self.assertGreater(len(s["sujets"]), 0)

    def test_page_modifiee_detectee(self):
        self.run_collecte()
        c.valider(self.d, MAINTENANT)
        web2 = faux_web({"news.google.com": "google.xml", "/feed": "blog.atom", "/tarifs": "tarifs-v2.html"})
        s = self.run_collecte(web2)
        self.assertEqual(len(s["pages_modifiees"]), 1)
        self.assertIn("9 € par mois", s["pages_modifiees"][0]["ajouts"])

    def test_article_d_origine_retrouve_dans_le_flux_du_media(self):
        web = faux_web({"media-un.example/feed": "media-un.xml", "news.google.com": "google.xml", "concurrent-a.example/feed": "blog.atom", "/tarifs": "tarifs-v1.html"})
        web_ordre = lambda url: web(url) if "media-un.example" not in url or url.endswith("/feed") else (_ for _ in ()).throw(OSError("pas d'accueil"))
        s = self.run_collecte(web_ordre)
        offre = [x for x in s["sujets"] if "offre santé" in x["titre"]][0]
        urls = [src["url"] for src in offre["sources"]]
        self.assertIn("https://media-un.example/2026/11/offre-sante", urls)
        self.assertIn("contre 12 euros", offre["extrait"])
        self.assertGreaterEqual(s["stats"]["articles_retrouves"], 1)

    def test_source_en_panne_n_arrete_pas_la_veille(self):
        web = faux_web({"news.google.com": "google.xml"})
        s = self.run_collecte(web)
        self.assertEqual(len(s["erreurs"]), 2)
        self.assertGreater(len(s["sujets"]), 0)

    def test_mots_exclus(self):
        cfg = json.loads((self.d / "sources.json").read_text("utf-8"))
        cfg["mots_exclus"] = ["recrute"]
        (self.d / "sources.json").write_text(json.dumps(cfg), "utf-8")
        s = self.run_collecte()
        self.assertFalse(any("recrute" in x["titre"] for x in s["sujets"]))
        self.assertEqual(s["stats"]["exclus"], 1)

    def test_modele_non_rempli_refuse(self):
        modele = json.loads((ICI.parent / "sources.json").read_text("utf-8"))
        (self.d / "sources.json").write_text(json.dumps(modele), "utf-8")
        with self.assertRaises(SystemExit):
            c.lire_config(self.d)

    def test_config_absente(self):
        (self.d / "sources.json").unlink()
        with self.assertRaises(SystemExit):
            c.lire_config(self.d)


if __name__ == "__main__":
    unittest.main()
