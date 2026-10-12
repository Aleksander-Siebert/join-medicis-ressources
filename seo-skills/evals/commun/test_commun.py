"""Tests du socle commun du pack SEO : texte_fr, garde_fou, meta, affirmations."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
COMMUN = PACK / "commun"
sys.path.insert(0, str(COMMUN))

import affirmations  # noqa: E402
import garde_fou  # noqa: E402
import meta  # noqa: E402
import texte_fr as tf  # noqa: E402

CONTEXTE = (PACK / "templates" / "exemple-site-context.md").read_text(encoding="utf-8")


def lancer(script, *args):
    p = subprocess.run([sys.executable, str(COMMUN / script), *args], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


class TexteFr(unittest.TestCase):
    def test_familles_de_mots(self):
        for famille in (["assurance", "assurances", "assurer", "assuré", "assurée"],
                        ["remboursement", "rembourser", "remboursé"],
                        ["garantie", "garanties"], ["expatrié", "expatriés", "expatriation"],
                        ["déduction", "déductible", "déduire"], ["tarif", "prix", "coût", "coûts"]):
            self.assertEqual(len({tf.racine(m) for m in famille}), 1, famille)

    def test_mots_differents_restent_differents(self):
        self.assertNotEqual(tf.racine("mutuelle"), tf.racine("prévoyance"))
        self.assertNotEqual(tf.racine("santé"), tf.racine("sanction"))

    def test_phrases_et_abreviations(self):
        p = tf.phrases("Selon M. Dupont, l'art. L. 122-1 encadre la publicité. Le délai est de 30 jours ! Vraiment ?")
        self.assertEqual(len(p), 3)
        self.assertIn("L. 122-1", p[0])

    def test_mots_ignore_le_markdown(self):
        self.assertEqual(tf.mots("**L'assurance** [santé](https://x.example) couvre 3 cas."), 5)

    def test_plan_markdown_et_format_brief(self):
        s = tf.plan("# Titre\nintro\n## A\ntexte\n### A1\nH2 : Coûts → combien ça coûte\n")
        self.assertEqual([x["niveau"] for x in s], [1, 2, 3, 2])
        self.assertEqual(s[-1]["texte"], "combien ça coûte")


class GardeFou(unittest.TestCase):
    def verdict(self, texte):
        r = garde_fou.evaluer(texte)
        return r["verdict"], {x["id"] for x in r["refus"]}, {x["id"] for x in r["encadrements"]}

    def test_exemple_refuse_quatre_regles(self):
        v, refus, _ = self.verdict(garde_fou.EXEMPLE)
        self.assertEqual(v, "REFUSÉ")
        self.assertTrue({"R1-CONTENU-COPIE", "R2-FAUSSE-PREUVE", "R4-LIENS-ARTIFICIELS", "R5-PAGES-EN-MASSE"} <= refus)

    def test_formes_conjuguees(self):
        self.assertIn("R1-CONTENU-COPIE", self.verdict("réécris les articles du concurrent")[1])
        self.assertIn("R2-FAUSSE-PREUVE", self.verdict("ajoute des témoignages clients inventés")[1])
        self.assertIn("R4-LIENS-ARTIFICIELS", self.verdict("on achète des backlinks")[1])
        self.assertIn("R6-FAUSSE-FRAICHEUR", self.verdict("change la date pour faire récent sans rien modifier")[1])
        self.assertIn("R3-TROMPER-LE-MOTEUR", self.verdict("mettre du texte caché en blanc sur blanc")[1])

    def test_negation(self):
        self.assertEqual(self.verdict("On veut éviter de copier les concurrents")[0], "AUTORISÉ")
        self.assertEqual(self.verdict("Écris un article sans texte caché ni bourrage")[0], "AUTORISÉ")

    def test_encadrements(self):
        self.assertIn("E3-COMPARATIF", self.verdict("Fais un comparatif Assurly vs un concurrent")[2])
        self.assertIn("E4-YMYL", self.verdict("article sur la mutuelle santé")[2])
        self.assertEqual(self.verdict("article sur le jardinage d'automne")[0], "AUTORISÉ")

    def test_codes_de_sortie(self):
        self.assertEqual(lancer("garde_fou.py", "--exemple")[0], 3)
        self.assertEqual(lancer("garde_fou.py", "--texte", "mutuelle santé")[0], 2)
        self.assertEqual(lancer("garde_fou.py", "--texte", "le jardinage")[0], 0)


class Meta(unittest.TestCase):
    def test_largeur_pixels(self):
        self.assertGreater(meta.largeur("WWWWW", 20), meta.largeur("iiiii", 20) * 3)
        self.assertEqual(meta.largeur("é", 20), meta.largeur("e", 20))

    def test_bon_title(self):
        r = meta.analyser("Mutuelle indépendant : bien la choisir en 2026 | Assurly", "", "mutuelle indépendant",
                          "Assurly", annee=2026)
        self.assertLessEqual(r["title_px"], 600)
        self.assertFalse([c for c in r["constats"] if c["gravite"] == "haute" and "title" in c["constat"]])

    def test_defauts_du_title(self):
        r = meta.analyser("Mutuelle indépendant 2025 : le guide de la mutuelle indépendant et de la mutuelle "
                          "indépendant pas chère — Assurly | Assurly", "", "mutuelle indépendant", "Assurly", annee=2026)
        constats = " ".join(c["constat"] for c in r["constats"])
        for attendu in ("probablement coupé", "bourrage", "marque répétée", "année dépassée", "tiret"):
            self.assertIn(attendu, constats)
        self.assertEqual(r["verdict"], "À REVOIR")

    def test_description_liste_et_echo(self):
        r = meta.analyser("Assurance habitation pas chère en ligne", "assurance, habitation, pas cher, devis, en ligne, gratuit")
        self.assertTrue(any("liste de mots-clés" in c["constat"] for c in r["constats"]))
        r = meta.analyser("Assurance habitation pas chère en ligne | Assurly",
                          "Assurance habitation pas chère en ligne : comparez nos formules et recevez un devis.")
        self.assertTrue(any("recopie le title" in c["constat"] for c in r["constats"]))

    def test_preferences(self):
        r = meta.analyser("Un title court", "", pref_title=(55, 60))
        self.assertTrue(any("préférence" in c["constat"] for c in r["constats"]))

    def test_lot(self):
        pages = [{"url": f"/p{i}", "title": f"Mutuelle {v} | Assurly",
                  "description": f"Mutuelle {v} pour indépendants : garanties et prix. Découvrez nos offres."}
                 for i, v in enumerate(["santé", "senior", "famille", "jeune"])]
        pages.append(dict(pages[0], url="/doublon"))
        r = meta.analyser_lot(pages)
        constats = " ".join(a["constat"] for a in r["alertes_lot"])
        self.assertIn("en double", constats)
        self.assertIn("même fin de description", constats)

    def test_typographie(self):
        self.assertTrue(meta.typographie("Votre devis: gratuit!"))
        self.assertFalse(meta.typographie("Votre devis : gratuit !"))


class Affirmations(unittest.TestCase):
    def statut(self, texte, ymyl=False, faits=""):
        return [(a["statut"], a["gravite"]) for a in affirmations.analyser(texte, ymyl, faits)["affirmations"]]

    def test_etude_vague_n_est_pas_une_source(self):
        self.assertEqual(self.statut("Selon une étude récente, 73% des indépendants n'ont pas de mutuelle.", True),
                         [("vague", "bloquant")])
        self.assertEqual(self.statut("Selon les experts, 30% des contrats sont mal choisis."), [("vague", "à vérifier")])

    def test_source_nommee_ou_lien(self):
        self.assertEqual(self.statut("Selon l'Insee, les indépendants représentent 12,8% de l'emploi.")[0][0], "sourcée")
        self.assertEqual(self.statut("Le plafond est de 10% du revenu ([impots.gouv.fr](https://www.impots.gouv.fr)).")[0][0],
                         "sourcée")

    def test_fait_fourni_par_le_contexte(self):
        self.assertEqual(self.statut("Vous recevez votre attestation sous 48 h ouvrées.", True, CONTEXTE),
                         [("fournie", "ok")])

    def test_promesse_et_loi_sans_source_bloquent_en_ymyl(self):
        r = affirmations.analyser("Notre mutuelle est la moins chère, remboursée à 100% sans aucun risque.\n\n"
                                  "L'article L. 911-1 du Code de la sécurité sociale encadre les contrats.", True)
        self.assertEqual(r["verdict"], "BLOQUÉ")
        self.assertEqual(r["compte"]["bloquant"], 2)

    def test_trou_assume(self):
        self.assertEqual(self.statut("Le plafond Madelin est de {{à compléter : plafond 2026}}.", True), [("trou", "trou")])

    def test_ce_qui_n_est_pas_une_affirmation(self):
        self.assertEqual(self.statut("Une étude de cas : la confusion entre mutuelle et prévoyance."), [])
        self.assertEqual(self.statut("Depuis 2024, le sujet revient souvent."), [])
        self.assertEqual(self.statut("Vous choisissez votre formule en ligne."), [])

    def test_codes_de_sortie(self):
        self.assertEqual(lancer("affirmations.py", "--texte", "Selon une étude, 73% des gens.", "--ymyl")[0], 3)
        self.assertEqual(lancer("affirmations.py", "--texte", "Selon une étude, 73% des gens.")[0], 2)
        self.assertEqual(lancer("affirmations.py", "--texte", "Vous choisissez votre formule.")[0], 0)
        r = json.loads(lancer("affirmations.py", "--texte", "Selon l'Insee, 12% des actifs.", "--json")[1])
        self.assertEqual(r["verdict"], "OK")


if __name__ == "__main__":
    unittest.main()
