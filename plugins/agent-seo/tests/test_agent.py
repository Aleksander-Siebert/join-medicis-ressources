"""Tests des scripts de l'agent SEO (python3 -m unittest discover -s tests)."""
import filecmp
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
import xml.dom.minidom
from pathlib import Path
from unittest import mock

ICI = Path(__file__).resolve().parent
AGENT = ICI.parent
sys.path.insert(0, str(AGENT / "scripts"))
import exporter  # noqa: E402
import sujets  # noqa: E402
import verite  # noqa: E402

FX = ICI / "fixtures"


def racine_depot():
    for p in [AGENT, *AGENT.parents]:
        if (p / ".claude-plugin" / "marketplace.json").exists():
            return p
    return None


class Sujets(unittest.TestCase):
    def setUp(self):
        self.lignes = sujets.lire_export(str(FX / "gsc.csv"))

    def proposer(self, **k):
        return sujets.proposer(self.lignes, [], marques=["assurly"], exclus=["emploi"], **k)

    def test_lecture_csv_francais(self):
        self.assertEqual(len(self.lignes), 12)
        self.assertEqual(self.lignes[1], {"requete": "rc pro auto entrepreneur", "page": "https://www.assurly.example/rc-pro/", "clics": 40.0, "impressions": 1200.0, "position": 6.2})

    def test_lecture_json_api_search_console(self):
        d = Path(tempfile.mkdtemp())
        (d / "gsc.json").write_text(json.dumps({"rows": [{"keys": ["prévoyance freelance", "https://a.example/p"], "clicks": 1, "impressions": 300, "position": 27.5}]}), "utf-8")
        self.assertEqual(sujets.lire_export(str(d / "gsc.json"))[0]["requete"], "prévoyance freelance")
        shutil.rmtree(d)

    def test_proposition(self):
        r = self.proposer()
        self.assertEqual([s["requete"] for s in r["sujets"]], ["assurance décennale micro entreprise", "prévoyance freelance"])
        self.assertEqual(r["sujets"][0]["requetes"], ["assurance décennale micro entreprise", "décennale micro-entreprise prix"])
        self.assertEqual(r["sujets"][0]["impressions"], 860)

    def test_ecartes(self):
        e = self.proposer()["ecartes"]
        self.assertEqual((e["marque"], e["exclus"], e["peu_vue"], e["deja_bien_placee"], e["trop_loin"]), (1, 1, 1, 1, 1))
        requetes = {p["requete"] for p in e["page_existante"]}
        self.assertIn("attestation rc pro freelance", requetes)  # l'adresse de la page reprend la requête
        self.assertIn("assurance rc pro auto-entrepreneur prix", requetes)  # variante d'une requête déjà bien placée

    def test_un_sujet_deja_ecrit_ne_revient_pas(self):
        m = {"sujets": {sujets.cle_sujet("décennale micro entreprise"): {"requete": "décennale micro entreprise", "etat": "livré"}}}
        r = sujets.proposer(self.lignes, [], ["assurly"], ["emploi"], memoire=m)
        self.assertEqual([s["requete"] for s in r["sujets"]], ["prévoyance freelance"])
        self.assertEqual(r["ecartes"]["deja_traite"], 2)

    def test_potentiel(self):
        self.assertGreater(sujets.potentiel(11), sujets.potentiel(25))
        self.assertGreater(sujets.potentiel(25), sujets.potentiel(38))

    def test_suivi_et_bilan(self):
        d = Path(tempfile.mkdtemp())
        with mock.patch.object(sujets, "RACINE", d):
            with mock.patch.object(sujets, "maintenant", return_value=sujets.date(2026, 10, 1)):
                sujets.marquer("prévoyance freelance", "livré", fichier="articles/x/article.md")
            with mock.patch.object(sujets, "maintenant", return_value=sujets.date(2026, 11, 16)):
                b = sujets.bilan(self.lignes, 28)
        self.assertEqual((b[0]["requete"], b[0]["jours"], b[0]["impressions"]), ("prévoyance freelance", 46, 300))
        shutil.rmtree(d)

    def test_commande(self):
        d = Path(tempfile.mkdtemp())
        with mock.patch.object(sujets, "RACINE", d):
            code = sujets.main(["proposer", str(FX / "gsc.csv"), "--marque", "assurly"])
            self.assertEqual(code, 0)
            self.assertIn("assurance décennale micro entreprise", (d / "sujets.md").read_text("utf-8"))
            self.assertEqual(json.loads((d / "memoire" / "sujets.json").read_text("utf-8"))["sujets"][sujets.cle_sujet("assurance décennale micro entreprise")]["etat"], "proposé")
        shutil.rmtree(d)


class Verite(unittest.TestCase):
    def test_article_piege(self):
        faits = verite.lire_faits(FX / "site-context.md")
        b = verite.controler((FX / "article-faux.md").read_text("utf-8"), faits, "Assurly")
        texte = "\n".join(b)
        self.assertEqual(len(b), 4)
        self.assertIn("29 absent des données produit LIVE", texte)
        self.assertIn("48 est RETIRÉ", texte)
        self.assertIn("« garanti »", texte)
        self.assertIn("blog/inconnu", texte)
        self.assertNotIn("Insee", texte)  # phrase qui ne parle pas de la marque : hors champ
        self.assertNotIn("{{", texte.replace("{{à compléter}}", ""))

    def test_valeurs_normalisees(self):
        self.assertEqual(verite.valeurs("1 200,50 € et 1200.5"), {"1200,5"})
        self.assertEqual(verite.valeurs("11 € par mois"), {"11"})

    def test_article_propre(self):
        faits = verite.lire_faits(FX / "site-context.md")
        self.assertEqual(faits["interdits"], ["garanti", "le moins cher du marché"])
        self.assertEqual(verite.controler("Chez Assurly, l'offre Solo coûte 11 € par mois. [Devis](https://www.assurly.example/devis/)", faits, "Assurly"), [])


class Exporter(unittest.TestCase):
    def test_docx_valide(self):
        d = Path(tempfile.mkdtemp())
        sortie = exporter.convertir((FX / "article.md").read_text("utf-8"), d / "a.docx")
        with zipfile.ZipFile(sortie) as z:  # fermé avant la suppression : Windows refuse d'effacer un fichier ouvert
            for n in z.namelist():
                xml.dom.minidom.parseString(z.read(n))
            doc = z.read("word/document.xml").decode("utf-8")
            rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
            core = z.read("docProps/core.xml").decode("utf-8")
        self.assertIn("Assurance décennale en micro-entreprise", doc)
        self.assertIn('w:pStyle w:val="Titre"', doc)
        self.assertIn('w:pStyle w:val="Titre1"', doc)
        self.assertIn("<w:tbl>", doc)
        self.assertIn('w:numId w:val="2"', doc)  # liste numérotée
        self.assertIn("&lt;tout&gt;", doc)
        self.assertIn("https://assurly.example/?a=1&amp;b=2", rels)
        self.assertNotIn("title: test", doc)  # en-tête YAML retiré
        self.assertIn("Assurance décennale", core)
        shutil.rmtree(d)


class Copies(unittest.TestCase):
    def test_skills_copies_a_jour(self):
        racine = racine_depot()
        if racine is None:  # dépôt modèle publié seul : la source n'est pas là
            self.skipTest("pack SEO absent (dépôt modèle)")
        pack = racine / "plugins" / "seo-skills" / "skills"
        copies = AGENT / ".claude" / "skills"
        for s in sorted(p.name for p in copies.iterdir()):
            cmp = filecmp.dircmp(pack / s, copies / s, ignore=["__pycache__"])
            pile = [cmp]
            while pile:
                c = pile.pop()
                self.assertFalse(c.left_only or c.right_only or c.diff_files, f"{s} : copie pas à jour, lance outils/copier-skills.sh ({c.left_only or c.right_only or c.diff_files})")
                pile.extend(c.subdirs.values())


if __name__ == "__main__":
    unittest.main()
