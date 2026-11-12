"""Tests des ajouts de la v2 : robots.txt, garde-fous réseau, modes, veille stratégique, emplois, mémoire."""
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

MOTS = "Assurance Banque Crédit Démarchage Énergie Franchise Garantie Hébergement Immobilier Jouets Kiosques Livraison Mutuelle Notaires Optique Pharmacie Quincaillerie Restauration Syndic Téléphonie Urbanisme Voyages Wagons Xylophones Yaourts Zinc Abonnements Bijouterie Covoiturage Déménagement".split()

RSS = """<rss version="2.0"><channel><title>Flux</title>{}</channel></rss>"""


def article(titre, lien, date="Fri, 06 Nov 2026 08:00:00 GMT", extrait=""):
    return f"<item><title>{titre}</title><link>{lien}</link><pubDate>{date}</pubDate><description>{extrait}</description></item>"


def web(reponses):
    """Faux web : {motif d'adresse: texte}. Garde la trace des adresses demandées."""
    vues = []

    def telecharge(url, corps=None):
        vues.append(url)
        for motif, texte in reponses.items():
            if motif in url:
                return texte
        raise OSError(f"injoignable : {url}")

    telecharge.vues = vues
    return telecharge


def config(**plus):
    base = {"jours": 7, "mode": "standard", "concurrents": [{"nom": "Concurrent A"}]}
    base.update(plus)
    d = Path(tempfile.mkdtemp())
    (d / "sources.json").write_text(json.dumps(base), "utf-8")
    try:
        return c.lire_config(d), d
    except SystemExit:
        shutil.rmtree(d)
        raise


class GardeFousReseau(unittest.TestCase):
    def test_refuse_fichiers_et_reseau_local(self):
        for url in ("file:///etc/passwd", "ftp://site.example/x", "http://localhost:8080/", "http://127.0.0.1/", "http://192.168.1.10/admin", "http://10.0.0.5/", "http://imprimante.local/", "http://[::1]/"):
            with self.assertRaises(c.AdresseRefusee, msg=url):
                c.verifier_adresse(url)

    def test_accepte_une_adresse_publique(self):
        c.verifier_adresse("https://93.184.216.34/page")


class RobotsTxt(unittest.TestCase):
    def test_page_interdite_non_lue_et_signalee(self):
        w = web({"/robots.txt": "User-agent: *\nDisallow: /tarifs\n", "/tarifs": "<p>Offre à 9 euros</p>"})
        cfg, d = config(concurrents=[{"nom": "Concurrent A", "pages": ["https://a.example/tarifs"]}])
        s = c.collecter(cfg, {"urls": {}, "titres": {}}, d, MAINTENANT, w)["sortie"]
        self.assertEqual(s["stats"]["refus_robots"], 1)
        self.assertIn("robots.txt", s["erreurs"][0]["erreur"])
        self.assertNotIn("https://a.example/tarifs", w.vues)
        shutil.rmtree(d)

    def test_page_permise_lue(self):
        w = web({"/robots.txt": "User-agent: *\nDisallow: /prive\n", "/tarifs": "<p>Offre à 9 euros par mois</p>"})
        cfg, d = config(concurrents=[{"nom": "Concurrent A", "pages": ["https://a.example/tarifs"]}])
        s = c.collecter(cfg, {"urls": {}, "titres": {}}, d, MAINTENANT, w)["sortie"]
        self.assertTrue(s["pages_modifiees"][0]["premiere_visite"])
        shutil.rmtree(d)

    def test_sans_robots_txt_la_page_est_lue(self):
        self.assertTrue(c.Robots(web({})).permet("https://a.example/tarifs"))

    def test_regle_propre_a_notre_robot(self):
        r = c.Robots(web({"/robots.txt": "User-agent: JoinMedicisVeille\nDisallow: /\n\nUser-agent: *\nAllow: /\n"}))
        self.assertFalse(r.permet("https://a.example/"))

    def test_desactivable(self):
        r = c.Robots(web({"/robots.txt": "User-agent: *\nDisallow: /\n"}), actif=False)
        self.assertTrue(r.permet("https://a.example/x"))


class Modes(unittest.TestCase):
    def test_standard_ne_touche_aucun_agregateur(self):
        w = web({})
        cfg, d = config(concurrents=[{"nom": "Concurrent A", "mots_cles": ["assurance"]}])
        s = c.collecter(cfg, {"urls": {}, "titres": {}}, d, MAINTENANT, w)["sortie"]
        self.assertFalse([u for u in w.vues if "google" in u or "bing" in u])
        self.assertEqual(s["a_chercher"], [{"axe": "concurrents", "requete": '"Concurrent A" assurance', "pour": "Concurrent A"}])
        shutil.rmtree(d)

    def test_etendu_lit_les_agregateurs_choisis(self):
        w = web({"news.google.com": RSS.format(article("Concurrent A lève 10 millions - Média Un", "https://news.google.com/rss/articles/x")),
                 "bing.com": RSS.format(article("Concurrent A ouvre à Lyon", "http://www.bing.com/news/apiclick.aspx?ref=FexRss&amp;url=https%3a%2f%2fmedia-deux.example%2flyon&amp;c=1"))})
        cfg, d = config(mode="etendu", agregateurs=["google", "bing"], retrouver_articles=False)
        s = c.collecter(cfg, {"urls": {}, "titres": {}}, d, MAINTENANT, w)["sortie"]
        self.assertEqual(s["a_chercher"], [])
        liens = {src["url"] for x in s["sujets"] for src in x["sources"]}
        self.assertIn("https://media-deux.example/lyon", liens)
        self.assertEqual(len(s["sujets"]), 2)
        shutil.rmtree(d)

    def test_ancienne_configuration_reste_en_etendu(self):
        d = Path(tempfile.mkdtemp())
        (d / "sources.json").write_text(json.dumps({"actualites_google": True, "concurrents": [{"nom": "A"}]}), "utf-8")
        self.assertEqual(c.lire_config(d)["mode"], "etendu")
        shutil.rmtree(d)

    def test_mode_inconnu_refuse(self):
        with self.assertRaises(SystemExit):
            config(mode="furtif")

    def test_veille_par_sujet_sans_concurrent(self):
        cfg, d = config(concurrents=[], strategique={"tendances": {"mots_cles": ["néobanque"]}})
        s = c.collecter(cfg, {"urls": {}, "titres": {}}, d, MAINTENANT, web({}))["sortie"]
        self.assertEqual(s["a_chercher"][0]["axe"], "tendances")
        shutil.rmtree(d)

    def test_rien_a_suivre_refuse(self):
        with self.assertRaises(SystemExit):
            config(concurrents=[])


class VeilleStrategique(unittest.TestCase):
    def test_reglementation_filtree_par_mots_cles(self):
        flux = RSS.format(article("Sanction de 2 millions pour un assureur", "https://regulateur.example/1") + article("Bilan de la journée portes ouvertes", "https://regulateur.example/2"))
        cfg, d = config(strategique={"reglementation": {"mots_cles": ["assureur"], "flux": ["https://regulateur.example/rss"]}})
        s = c.collecter(cfg, {"urls": {}, "titres": {}}, d, MAINTENANT, web({"regulateur.example/rss": flux}))["sortie"]
        self.assertEqual([(x["axe"], x["titre"]) for x in s["sujets"]], [("reglementation", "Sanction de 2 millions pour un assureur")])
        self.assertEqual(s["a_chercher"][0]["axe"], "concurrents")  # pas de recherche d'actualités pour la réglementation
        self.assertEqual(len(s["a_chercher"]), 1)
        shutil.rmtree(d)

    def test_un_article_qui_cite_un_concurrent_passe_dans_son_axe(self):
        flux = RSS.format(article("Le régulateur sanctionne Concurrent A", "https://regulateur.example/1"))
        cfg, d = config(strategique={"reglementation": {"flux": ["https://regulateur.example/rss"]}})
        s = c.collecter(cfg, {"urls": {}, "titres": {}}, d, MAINTENANT, web({"regulateur.example/rss": flux}))["sortie"]
        self.assertEqual((s["sujets"][0]["axe"], s["sujets"][0]["concurrents"]), ("concurrents", ["Concurrent A"]))
        shutil.rmtree(d)

    def test_plafond_par_axe_protege_les_concurrents(self):
        bavard = RSS.format("".join(article(f"{mot} {MOTS[-1 - i]} {MOTS[(i * 7 + 3) % 30]}", f"https://regulateur.example/{i}") for i, mot in enumerate(MOTS)))
        propre = RSS.format(article("Concurrent A change ses prix", "https://a.example/prix", date="Mon, 02 Nov 2026 08:00:00 GMT"))
        cfg, d = config(concurrents=[{"nom": "Concurrent A", "flux": ["https://a.example/feed"]}], strategique={"reglementation": {"flux": ["https://regulateur.example/rss"]}}, max_par_axe=5)
        s = c.collecter(cfg, {"urls": {}, "titres": {}}, d, MAINTENANT, web({"regulateur.example/rss": bavard, "a.example/feed": propre}))["sortie"]
        axes = [x["axe"] for x in s["sujets"]]
        self.assertEqual((axes.count("concurrents"), axes.count("reglementation")), (1, 5))
        self.assertEqual(s["stats"]["coupes_au_dela_du_max"], 25)
        shutil.rmtree(d)

    def test_boamp(self):
        url = c.url_boamp(["assurance", 'mutu"elle'], MAINTENANT, ["75"])
        self.assertIn("dateparution", url)
        self.assertNotIn("%22elle", url)
        rep = json.dumps({"results": [{"idweb": "26-1", "objet": "March&#233; d&#039;assurance", "nomacheteur": "Ville d&#039;Assurville", "dateparution": "2026-11-06", "datelimitereponse": "2026-12-01T11:00:00+00:00", "nature_libelle": "Avis de marché", "titulaire": ["Concurrent A", "Autre"], "code_departement": ["75"], "url_avis": "https://www.boamp.fr/pages/avis/?q=idweb:26-1"}]})
        a = c.lire_boamp(rep)[0]
        self.assertEqual((a["titre"], a["acheteur"], a["date_limite"], a["titulaire"]), ("Marché d'assurance", "Ville d'Assurville", "2026-12-01", "Concurrent A, Autre"))

    def test_ted(self):
        corps = json.loads(c.corps_ted(["assurance"], MAINTENANT, "FR"))
        self.assertIn('buyer-country = "FRA"', corps["query"])
        self.assertIn("publication-date >= 20261109", corps["query"])
        rep = json.dumps({"notices": [{"publication-number": "1-2026", "publication-date": "2026-11-06+01:00", "notice-title": {"eng": "Insurance", "fra": "Services d'assurance"}, "buyer-name": {"fra": ["Ville d'Assurville"]}, "deadline-receipt-tender-date-lot": ["2026-12-01+01:00"]}]})
        a = c.lire_ted(rep)[0]
        self.assertEqual((a["titre"], a["acheteur"], a["date"], a["date_limite"]), ("Services d'assurance", "Ville d'Assurville", "2026-11-06", "2026-12-01"))
        self.assertTrue(a["url"].endswith("/1-2026"))

    def test_appels_offres_dans_la_collecte_et_marche_gagne_par_un_concurrent(self):
        boamp = json.dumps({"results": [{"idweb": "26-1", "objet": "Assurance flotte automobile", "nomacheteur": "Ville d'Assurville", "dateparution": "2026-11-06", "titulaire": "CONCURRENT A", "url_avis": "https://www.boamp.fr/pages/avis/?q=idweb:26-1"}]})
        cfg, d = config(strategique={"appels_offres": {"mots_cles": ["assurance"], "sources": ["boamp"]}})
        w = web({"boamp-datadila": boamp})
        s = c.collecter(cfg, {"urls": {}, "titres": {}}, d, MAINTENANT, w)["sortie"]
        self.assertEqual(s["appels_offres"][0]["concurrents"], ["Concurrent A"])
        (d / "sortie").mkdir()
        (d / "sortie" / "a-traiter.json").write_text(json.dumps(s), "utf-8")
        c.valider(d, MAINTENANT)
        s2 = c.collecter(cfg, c.charger_memoire(d), d, MAINTENANT, w)["sortie"]
        self.assertEqual(s2["appels_offres"], [])  # déjà envoyé : il ne revient pas
        shutil.rmtree(d)


class Emplois(unittest.TestCase):
    def test_reconnait_les_outils(self):
        self.assertEqual(c.api_emplois("https://boards.greenhouse.io/acme")[1], "https://boards-api.greenhouse.io/v1/boards/acme/jobs")
        self.assertEqual(c.api_emplois("https://jobs.lever.co/acme/")[0], "lever")
        self.assertEqual(c.api_emplois("https://jobs.ashbyhq.com/acme")[1], "https://api.ashbyhq.com/posting-api/job-board/acme")
        self.assertIsNone(c.api_emplois("https://acme.example/carrieres"))

    def test_nouvelles_offres_et_offres_retirees(self):
        def lever(titres):
            return json.dumps([{"text": t, "hostedUrl": f"https://jobs.lever.co/a/{i}", "categories": {"location": "Paris", "team": "Ventes"}} for i, t in titres])
        cfg, d = config(concurrents=[{"nom": "Concurrent A", "emplois": ["https://jobs.lever.co/a"]}])
        r = c.collecter(cfg, {"urls": {}, "titres": {}}, d, MAINTENANT, web({"api.lever.co": lever([(1, "Commercial"), (2, "Juriste")])}))
        self.assertTrue(r["sortie"]["emplois"][0]["premiere_visite"])
        (d / "sortie").mkdir()
        (d / "sortie" / "a-traiter.json").write_text(json.dumps(r["sortie"]), "utf-8")
        (d / "sortie" / ".pages.json").write_text(json.dumps(r["snapshots"]), "utf-8")
        c.valider(d, MAINTENANT)
        e = c.collecter(cfg, c.charger_memoire(d), d, MAINTENANT, web({"api.lever.co": lever([(1, "Commercial"), (3, "Directeur Italie")])}))["sortie"]["emplois"][0]
        self.assertEqual(([o["titre"] for o in e["nouvelles"]], e["retirees"]), (["Directeur Italie"], ["Juriste"]))
        shutil.rmtree(d)


class PagesSuivies(unittest.TestCase):
    def _deux_visites(self, page, v1, v2):
        cfg, d = config(concurrents=[{"nom": "Concurrent A", "pages": [page]}])
        r = c.collecter(cfg, {"urls": {}, "titres": {}}, d, MAINTENANT, web({"/tarifs": v1}))
        (d / "sortie").mkdir()
        (d / "sortie" / "a-traiter.json").write_text(json.dumps(r["sortie"]), "utf-8")
        (d / "sortie" / ".pages.json").write_text(json.dumps(r["snapshots"]), "utf-8")
        c.valider(d, MAINTENANT)
        s = c.collecter(cfg, c.charger_memoire(d), d, MAINTENANT, web({"/tarifs": v2}))["sortie"]
        shutil.rmtree(d)
        return s["pages_modifiees"]

    def test_ignorer(self):
        page = {"url": "https://a.example/tarifs", "ignorer": ["clients nous font confiance"]}
        m = self._deux_visites(page, "<p>Offre à 12 euros</p><p>4 000 clients nous font confiance</p>", "<p>Offre à 12 euros</p><p>4 200 clients nous font confiance</p>")
        self.assertEqual(m, [])

    def test_seulement_si(self):
        page = {"url": "https://a.example/tarifs", "seulement_si": ["€", "euros"], "intention": "préviens-moi si un prix change"}
        self.assertEqual(self._deux_visites(page, "<p>Offre à 12 euros</p><p>Nouveau logo</p>", "<p>Offre à 12 euros</p><p>Logo refait</p>"), [])
        m = self._deux_visites(page, "<p>Offre à 12 euros</p>", "<p>Offre à 9 euros</p>")
        self.assertEqual((m[0]["ajouts"], m[0]["intention"]), (["Offre à 9 euros"], "préviens-moi si un prix change"))

    def test_reponse_json_comparee_cle_par_cle(self):
        m = self._deux_visites("https://a.example/tarifs", '{"offres": [{"nom": "Solo", "prix": 12}]}', '{"offres": [{"nom": "Solo", "prix": 9}]}')
        self.assertEqual((m[0]["retraits"], m[0]["ajouts"]), (["offres[0].prix : 12"], ["offres[0].prix : 9"]))


class Memoire(unittest.TestCase):
    def test_un_envoi_ne_se_valide_pas_deux_fois(self):
        d = Path(tempfile.mkdtemp())
        (d / "sortie").mkdir()
        (d / "sortie" / "a-traiter.json").write_text(json.dumps({"genere_le": "2026-11-09T07:00:00+00:00", "sujets": []}), "utf-8")
        self.assertIn("Mémoire mise à jour", c.valider(d, MAINTENANT))
        self.assertIn("Déjà validé", c.valider(d, MAINTENANT))
        shutil.rmtree(d)

    def test_historique_par_concurrent_et_rubrique(self):
        d = Path(tempfile.mkdtemp())
        (d / "sortie").mkdir()
        sujets = [{"titre": "Concurrent A baisse ses prix", "concurrents": ["Concurrent A"], "sources": [{"url": "https://m.example/1"}]}]
        (d / "sortie" / "a-traiter.json").write_text(json.dumps({"genere_le": "x", "sujets": sujets}), "utf-8")
        resume = {"sections": [{"titre": "Prix et offres", "infos": [{"titre": "Offre à 9 €", "date": "2026-11-06", "sources": [{"url": "https://m.example/1"}]}]}]}
        (d / "sortie" / "resume.json").write_text(json.dumps(resume), "utf-8")
        c.valider(d, MAINTENANT)
        h = c.resume_historique(json.loads((d / "memoire" / "historique.json").read_text("utf-8"))["entrees"], MAINTENANT)
        self.assertEqual(h["Concurrent A"]["par_rubrique"], {"Prix et offres": 1})
        shutil.rmtree(d)

    def test_sujets_qui_montent(self):
        avant = [{"termes": {"facturation electronique": 1, "banque": 6}}, {"termes": {"banque": 5}}, {"termes": {"banque": 7}}]
        m = c.sujets_qui_montent({"facturation electronique": 6, "facturation": 6, "banque": 6, "rare": 1}, avant)
        self.assertEqual([t["terme"] for t in m], ["facturation electronique"])
        self.assertEqual(c.sujets_qui_montent({"x y": 9}, avant[:2]), [])  # pas assez de recul


class RechercheWeb(unittest.TestCase):
    def test_integrer_applique_les_memes_controles(self):
        d = Path(tempfile.mkdtemp())
        (d / "sortie").mkdir()
        (d / "memoire").mkdir()
        deja = {"urls": {c.empreinte(c.url_canonique("https://m.example/vu")): MAINTENANT.isoformat()}, "titres": {}}
        (d / "memoire" / "deja-vu.json").write_text(json.dumps(deja), "utf-8")
        collecte = {"genere_le": "x", "periode": {"jours": 7}, "stats": {}, "sujets": [
            {"id": "s1", "axe": "concurrents", "titre": "Concurrent A lève 10 millions d'euros", "extrait": "", "concurrents": ["Concurrent A"], "sources": [{"url": "https://m.example/levee"}]}]}
        (d / "sortie" / "a-traiter.json").write_text(json.dumps(collecte), "utf-8")
        trouvailles = [
            {"titre": "Concurrent A lève 10 millions d'euros en série A", "url": "https://autre.example/levee", "date": "2026-11-05", "media": "Autre Média"},
            {"titre": "Concurrent B ouvre un bureau à Lyon", "url": "https://m.example/lyon", "date": "2026-11-06", "concurrents": ["Concurrent B"]},
            {"titre": "Vieille histoire", "url": "https://m.example/vieux", "date": "2026-09-01"},
            {"titre": "Déjà envoyé la semaine dernière", "url": "https://m.example/vu", "date": "2026-11-06"},
            {"titre": "Sans lien", "url": ""},
            {"titre": "Lien local", "url": "http://localhost/admin"},
            {"titre": "Sans date", "url": "https://m.example/sans-date"},
        ]
        (d / "sortie" / "trouvailles.json").write_text(json.dumps(trouvailles), "utf-8")
        c.integrer(d, MAINTENANT)
        apres = json.loads((d / "sortie" / "a-traiter.json").read_text("utf-8"))
        self.assertEqual(apres["stats"]["trouvailles"], {"ajoutes": 2, "regroupes": 1, "trop_vieux": 1, "deja_envoyes": 1, "invalides": 2, "deja_la": 0})
        self.assertEqual(len(apres["sujets"][0]["sources"]), 2)
        self.assertEqual([(x["id"], x["axe"], x["date_inconnue"]) for x in apres["sujets"][1:]], [("t1", "concurrents", False), ("t2", "tendances", True)])
        shutil.rmtree(d)


class Diagnostic(unittest.TestCase):
    def test_dit_quoi_faire(self):
        d = Path(tempfile.mkdtemp())
        (d / "veille.md").write_text("Adresse : {{à compléter}}", "utf-8")
        lignes = c.diagnostic(d, web({}))
        self.assertTrue(lignes[0].startswith("OK   Python"))
        self.assertIn("CONFIGURE-MOI", lignes[1])
        self.assertTrue(lignes[-1].startswith("ERR"))
        shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
