"""Tests de exactitude.py (/geo-exactitude), hors ligne, sur des réponses fictives."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
SCRIPT = PACK / "skills" / "geo-exactitude" / "scripts" / "exactitude.py"
sys.path.insert(0, str(SCRIPT.parent))
import exactitude as ex  # noqa: E402

FAITS = ICI / "faits-assurly.csv"
REPONSES = ICI / "reponses-assurly.txt"
CONTEXTE = PACK / "templates" / "exemple-site-context.md"


def lancer(*args):
    p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def registre(texte, question="Que vaut Assurly ?", faits=FAITS, moteur="ChatGPT"):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(f"=== {moteur} | P01 | {question}\n{texte}\n")
    r = ex.analyser(ex.lire_reponses(f.name), "Assurly", [], ex.lire_faits(str(faits)))
    return [(x["verdict"], x["gravite"]) for x in r["registre"]]


def verdicts(texte, **k):
    return [v for v, _ in registre(texte, **k)]


class Verdicts(unittest.TestCase):
    def test_exact(self):
        self.assertEqual(verdicts("Assurly propose la formule Essentielle à 39 € par mois."), ["exact"])

    def test_exact_avec_centimes(self):
        self.assertEqual(verdicts("Assurly : formule Essentielle à 39,00 €."), ["exact"])

    def test_devise_critique(self):
        self.assertEqual(registre("Assurly vend la formule Essentielle 42 $."), [("devise", "critique")])

    def test_different(self):
        self.assertEqual(registre("Assurly vend la formule Essentielle 45 € par mois."), [("différent", "critique")])

    def test_perime_sans_chiffre(self):
        self.assertIn("périmé", verdicts("Assurly offre le premier mois offert aux nouveaux clients."))

    def test_faux_connu(self):
        self.assertIn("faux", verdicts("Assurly assure aussi les animaux."))

    def test_annee_jamais_par_tolerance(self):
        self.assertEqual(verdicts("Assurly a été fondée en 2017."), ["différent"])
        self.assertEqual(verdicts("Assurly a été fondée en 2019."), ["exact"])

    def test_a_confirmer(self):
        self.assertEqual(verdicts("Assurly : aucune carence, 0 jour."), ["à confirmer"])

    def test_inverifiable(self):
        self.assertEqual(verdicts("Assurly compte 15 000 clients."), ["invérifiable"])

    def test_petit_nombre_sans_unite_ignore(self):
        self.assertEqual(verdicts("Assurly propose 3 formules."), [])

    def test_cadrage_negatif(self):
        self.assertEqual(verdicts("Attention à Assurly, nombreuses plaintes."), ["cadrage négatif"])


class Lecture(unittest.TestCase):
    def test_phrase_qui_reprend_la_marque(self):
        r = verdicts("Les assureurs varient. Assurly est en ligne. Elle assure aussi les animaux.",
                     question="Quelle assurance choisir ?")
        self.assertIn("faux", r)

    def test_phrase_sans_marque_ignoree(self):
        r = verdicts("Assurly est en ligne. Un concurrent vend sa formule Essentielle 45 €.",
                     question="Quelle assurance choisir ?")
        self.assertEqual(r, [])

    def test_question_sur_la_marque_lit_toute_la_reponse(self):
        r = verdicts("Courtier en ligne. La formule Essentielle coûte 45 €.", question="Assurly est-il fiable ?")
        self.assertEqual(r, ["différent"])

    def test_mot_cle_en_mot_entier(self):
        # « depuis » est un mot-clé de F4, « 2019 » ne doit pas être jugé hors du mot
        self.assertEqual(verdicts("Assurly répond en 48 h, attestation comprise."), ["exact"])

    def test_alias(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("=== ChatGPT | P01 | Quel courtier ?\nAssurly.example vend la formule Essentielle 45 €.\n")
        r = ex.analyser(ex.lire_reponses(f.name), "Assurly SAS", ["assurly.example"], ex.lire_faits(str(FAITS)))
        self.assertEqual([x["verdict"] for x in r["registre"]], ["différent"])


class Contexte(unittest.TestCase):
    def test_lit_le_tableau_du_site_context(self):
        faits = ex.lire_contexte(str(CONTEXTE))
        self.assertEqual(len(faits), 4)
        self.assertEqual({f["statut"] for f in faits}, {"LIVE", "À CONFIRMER", "RETIRÉ"})
        att = faits[0]
        self.assertEqual((att["valeur"], att["unite"]), (48.0, "h"))
        self.assertIn("attestation", att["mots"])

    def test_un_seul_mot_commun_ne_suffit_pas(self):
        # « mois » seul ne doit pas relier « 39 € par mois » à l'offre retirée « premier mois offert »
        r = ex.analyser([{"moteur": "X", "id": "P1", "prompt": "Prix ?", "reponse": "Assurly coûte 39 € par mois."}],
                        "Assurly", [], ex.lire_contexte(str(CONTEXTE)))
        self.assertNotIn("périmé", [x["verdict"] for x in r["registre"]])

    def test_offre_retiree_reconnue(self):
        r = ex.analyser([{"moteur": "X", "id": "P1", "prompt": "Prix ?",
                          "reponse": "Assurly propose le premier mois offert."}],
                        "Assurly", [], ex.lire_contexte(str(CONTEXTE)))
        self.assertIn("périmé", [x["verdict"] for x in r["registre"]])


class Ligne(unittest.TestCase):
    def test_jeu_complet(self):
        code, out, _ = lancer(REPONSES, "--marque", "Assurly", "--faits", FAITS)
        self.assertEqual(code, 0)
        for v in ("DEVISE", "FAUX", "DIFFÉRENT", "PÉRIMÉ", "CADRAGE NÉGATIF", "À CONFIRMER", "INVÉRIFIABLE"):
            self.assertIn(v, out)
        self.assertIn("EXACT · 3 affirmation(s)", out)

    def test_ordre_par_gravite(self):
        _, out, _ = lancer(REPONSES, "--marque", "Assurly", "--faits", FAITS, "--json")
        r = json.loads(out)
        ordre = [ex.GRAVITE[x["verdict"]] for x in r["registre"]]
        self.assertEqual(ordre, sorted(ordre))

    def test_sans_reponse_lisible(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("du texte sans en-tête\n")
        code, _, err = lancer(f.name, "--marque", "Assurly", "--faits", FAITS)
        self.assertEqual(code, 1)
        self.assertIn("===", err)

    def test_contexte_sans_section(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("# Contexte\nrien\n")
        code, _, err = lancer(REPONSES, "--marque", "Assurly", "--contexte", f.name)
        self.assertEqual(code, 1)
        self.assertIn("données produit", err)


if __name__ == "__main__":
    unittest.main()
