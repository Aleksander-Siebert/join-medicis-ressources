"""Tests de fil.py (linkedin-reply). Lancer : python3 -m unittest discover -s evals/linkedin-reply"""
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).parent
SCRIPT = ICI.parents[1] / "skills" / "linkedin-reply" / "scripts" / "fil.py"
spec = importlib.util.spec_from_file_location("fil", SCRIPT)
fil = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fil)

CIBLE = "marketing,assureur,courtier,acquisition".split(",")


def exemple():
    return fil.trier(fil.lire_commentaires((ICI / "fil-exemple.txt").read_text(encoding="utf-8")), "Camille D.", CIBLE,
                     ["agency", "agence"], fil.compter_journal(ICI / "journal-exemple.md"), 3)


class Tri(unittest.TestCase):
    def test_rapport_chiffre(self):
        r = exemple()
        self.assertTrue(r["rapport"].startswith("9 récupérés → 5 écartés"))
        self.assertIn("→ 4 à traiter", r["rapport"])

    def test_raisons(self):
        raisons = {e["nom"]: e["raison"] for e in exemple()["ecartes"]}
        self.assertEqual(raisons["Dan P."], "éloge vide")
        self.assertEqual(raisons["Kevin L."], "doublon")
        self.assertEqual(raisons["Agence Boost"], "spam")
        self.assertEqual(raisons["Bot test"], "instruction adressée à une IA")
        self.assertEqual(raisons["Camille D."], "propre commentaire")

    def test_relation_gardee_meme_courte(self):
        thomas = [g for g in exemple()["a_traiter"] if g["nom"] == "Thomas G."][0]
        self.assertTrue(thomas["relation"])
        self.assertEqual(thomas["categorie"], "SOUTIEN")

    def test_prospect_chaud_en_tete(self):
        premier = exemple()["a_traiter"][0]
        self.assertEqual((premier["nom"], premier["categorie"], premier["lead"]["niveau"]), ("Sarah M.", "PROSPECT", "chaud"))
        self.assertGreaterEqual(premier["lead"]["score"], 7)

    def test_desaccord_reste_fond(self):
        marc = [g for g in exemple()["a_traiter"] if g["nom"] == "Marc W."][0]
        self.assertEqual(marc["categorie"], "FOND")
        self.assertIn("désaccord", marc["garde_parce_que"])

    def test_question_courte_gardee(self):
        r = fil.trier([{"nom": "A", "titre": "", "texte": "Et en B2B ?"}])
        self.assertEqual(len(r["a_traiter"]), 1)

    def test_tags_seuls_et_pair(self):
        r = fil.trier([{"nom": "P", "titre": "CEO", "texte": "@Marie Durand @Jean"},
                       {"nom": "Q", "titre": "Fondateur · Agence Croissance", "texte": "On voit la même chose chez nos clients, surtout en mutuelle santé."}],
                      concurrents=["agence"])
        self.assertEqual(r["ecartes"][0]["raison"], "spam")
        self.assertEqual(r["a_traiter"][0]["categorie"], "PAIR")
        self.assertEqual(r["a_traiter"][0]["lead"]["score"], 0)

    def test_fil_ancien(self):
        r = fil.trier([{"nom": "A", "titre": "", "texte": "Comment vous faites ?"}], age_heures=80)
        self.assertTrue(r["fil_ancien"])

    def test_json_accepte(self):
        self.assertEqual(fil.lire_commentaires('[{"nom": "A", "titre": "", "texte": "x"}]')[0]["nom"], "A")


class Verifier(unittest.TestCase):
    C = "Comment vous avez fait pour rappeler 60 clients ?"

    def test_vides(self):
        for r in ["Merci !", "Sarah, 100%", "Julie, merci beaucoup !", "Bonne remarque, je vais y réfléchir.", "Sarah, bonne question ! Je t'écris en MP."]:
            self.assertEqual(fil.verifier(self.C, r)["code"], 3, r)

    def test_bonne_reponse(self):
        r = fil.verifier(self.C, "Sarah, à deux, en 3 semaines, avec un script de 5 questions. Le plus long a été de retrouver des numéros à jour. Vous gardez les coordonnées après résiliation ?")
        self.assertEqual(r["code"], 0, r)

    def test_tiret_et_lien(self):
        self.assertEqual(fil.verifier(self.C, "On a fait ça à deux — en trois semaines avec un script précis.")["code"], 3)
        self.assertEqual(fil.verifier(self.C, "Voici notre offre pour en parler https://assurly.example/tarif")["code"], 3)

    def test_merci_en_tete(self):
        r = fil.verifier(self.C, "Merci Sarah, on a rappelé les 60 clients en 3 semaines avec un script de 5 questions.")
        self.assertEqual(r["code"], 2)
        r = fil.verifier(self.C, "Merci pour le lien vers l'étude, je ne l'avais pas. Leur échantillon de 2025 confirme le nôtre.")
        self.assertEqual(r["code"], 0, r)

    def test_trop_long(self):
        r = fil.verifier(self.C, "Sarah, on a fait ça en 3 semaines. " * 14)
        self.assertIn("caractères", " ".join(r["attentions"]))

    def test_cli(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "trier", "--fichier", str(ICI / "fil-exemple.txt"), "--moi", "Camille D."],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertIn("FIL · 9 récupérés", p.stdout)


if __name__ == "__main__":
    unittest.main()
