"""Tests de entite.py (/geo-entite), hors ligne, sur une page d'accueil fictive."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
SCRIPT = PACK / "skills" / "geo-entite" / "scripts" / "entite.py"
sys.path.insert(0, str(SCRIPT.parent))
import entite as en  # noqa: E402

ACCUEIL = (ICI / "accueil-assurly.html").read_text(encoding="utf-8")


def lancer(*args):
    p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def page(tete="", corps="", jsonld=None):
    js = "".join(f'<script type="application/ld+json">{json.dumps(j)}</script>' for j in (jsonld or []))
    return f"<html><head>{tete}{js}</head><body>{corps}</body></html>"


class Separateurs(unittest.TestCase):
    """Cas du CHANGELOG de geo-optimizer (#550) : tiret demi-cadratin, premier séparateur du texte."""

    def test_tiret_demi_cadratin(self):
        self.assertEqual(en.couper("Assurly – Mutuelle des indépendants"), ["Assurly", "Mutuelle des indépendants"])

    def test_premier_separateur_du_texte(self):
        self.assertEqual(en.couper("Acme – Outils | Blog")[0], "Acme")

    def test_marque_en_fin_de_title(self):
        r = en.analyser(page("<title>Guide de la mutuelle | Assurly</title>"), "Assurly")
        self.assertEqual(r["noms"]["lignes"][0]["etat"], "marque")

    def test_trait_d_union_dans_le_nom_garde(self):
        self.assertEqual(en.couper("Coca-Cola - Accueil")[0], "Coca-Cola")


class Noms(unittest.TestCase):
    def setUp(self):
        self.r = en.analyser(ACCUEIL, "Assurly")
        self.etat = {x["source"]: x["etat"] for x in self.r["noms"]["lignes"]}

    def test_variante_d_ecriture(self):
        self.assertEqual(self.etat["og:title"], "variante")

    def test_nom_declare_different(self):
        self.assertEqual(self.etat["JSON-LD Organization.name"], "variante")

    def test_forme_juridique_ignoree(self):
        self.assertEqual(self.etat["mention ©"], "marque")

    def test_sous_type_et_liste_de_types(self):
        # cas #579 de geo-optimizer : InsuranceAgency et @type en liste comptent comme Organization
        self.assertEqual(self.etat["JSON-LD InsuranceAgency/LocalBusiness.name"], "marque")

    def test_marque_devinee(self):
        r = en.analyser(page('<title>Accueil | Assurly</title><meta property="og:site_name" content="Assurly">'), None)
        self.assertEqual(r["noms"]["marque"], "Assurly")


class Organisation(unittest.TestCase):
    def setUp(self):
        self.o = en.analyser(ACCUEIL, "Assurly")["organisation"]

    def test_deux_blocs_aux_noms_differents(self):
        self.assertTrue(any("noms différents" in a for a in self.o["alertes"]))

    def test_profil_personnel_et_doublon(self):
        self.assertTrue(any("profil LinkedIn personnel" in a for a in self.o["alertes"]))
        self.assertTrue(any("en double" in a for a in self.o["alertes"]))

    def test_pas_https(self):
        self.assertFalse(next(p for p in self.o["profils"] if p["plateforme"] == "facebook")["https"])

    def test_faq_signalee(self):
        self.assertTrue(any("7 mai 2026" in a for a in self.o["alertes"]))

    def test_aucune_organisation(self):
        o = en.analyser(page("<title>X</title>"), "X")["organisation"]
        self.assertTrue(any("aucun bloc Organization" in a for a in o["alertes"]))

    def test_graph_deplie(self):
        self.assertIn("WebSite", self.o["types"])


class Visible(unittest.TestCase):
    def setUp(self):
        self.v = {x["libelle"]: x["visible"] for x in en.analyser(ACCUEIL, "Assurly")["visible"]}

    def test_telephone_international_retrouve(self):
        self.assertTrue(self.v["téléphone"])

    def test_adresse_retrouvee(self):
        self.assertTrue(self.v["rue"] and self.v["code postal"])

    def test_note_balisee_invisible(self):
        self.assertFalse(self.v["note"])
        self.assertFalse(self.v["nombre d'avis"])

    def test_note_visible(self):
        j = [{"@context": "https://schema.org", "@type": "Product", "name": "Formule Essentielle",
              "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "1200"},
              "offers": {"@type": "Offer", "price": "39.00", "priceCurrency": "EUR"}}]
        r = en.analyser(page(corps="<p>Note 4,6 sur 5 (1 200 avis). 39 € par mois.</p>", jsonld=j), "Assurly")
        self.assertTrue(all(x["visible"] for x in r["visible"]), r["visible"])


class Bloc(unittest.TestCase):
    def test_bloc_nettoye(self):
        r = en.analyser(ACCUEIL, "Assurly")
        b = en.bloc(r["organisation"]["org"], "Assurly", r["page"], "https://assurly.example/")
        self.assertEqual(b["sameAs"], ["http://www.facebook.com/assurly-fictif"])
        self.assertIn("{{", b["logo"])
        self.assertEqual(b["@id"], "https://assurly.example/#organization")

    def test_sortie_texte(self):
        code, out, _ = lancer(ICI / "accueil-assurly.html", "--marque", "Assurly")
        self.assertEqual(code, 0)
        for x in ("NOMS", "ORGANISATION", "SAMEAS", "JSON-LD VISIBLE", "CRITIQUE"):
            self.assertIn(x, out)

    def test_bloc_en_ligne_de_commande(self):
        code, out, _ = lancer(ICI / "accueil-assurly.html", "--marque", "Assurly", "--bloc")
        self.assertEqual(code, 0)
        json.loads(out.split("\n", 1)[1].rsplit("</script>", 1)[0])


if __name__ == "__main__":
    unittest.main()
