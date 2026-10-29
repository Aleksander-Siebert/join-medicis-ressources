"""Tests de message.py et volume.py (linkedin-dm). Lancer : python3 -m unittest discover -s evals/linkedin-dm"""
import importlib.util
import re
import subprocess
import sys
import unittest
from pathlib import Path

ICI = Path(__file__).parent
SKILL = ICI.parents[1] / "skills" / "linkedin-dm"


def charger(nom):
    spec = importlib.util.spec_from_file_location(nom, SKILL / "scripts" / f"{nom}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


message, volume = charger("message"), charger("volume")
NOTE_OK = "Votre post sur les clients qui partent avant 6 mois m'a fait revoir nos chiffres : même courbe chez nous, même cause. Je suis l'acquisition chez Assurly."


class Note(unittest.TestCase):
    def test_bonne_note(self):
        self.assertEqual(message.verifier("note", NOTE_OK)["code"], 0)

    def test_note_generique(self):
        r = message.verifier("note", "Bonjour Paul, je me permets de vous inviter afin d'élargir mon réseau. Nous aidons les assureurs à réduire le churn, seriez-vous disponible pour un échange de 15 minutes ?")
        self.assertEqual(r["code"], 3)
        texte = " ".join(r["bloquants"])
        self.assertIn("ligne propre", texte)
        self.assertIn("demande dans la note", texte)
        self.assertIn("Argumentaire", texte)

    def test_plafonds(self):
        longue = NOTE_OK + " " + "Votre analyse du marché des courtiers en ligne était la plus claire que j'ai lue."
        self.assertGreater(len(longue), 200)
        self.assertEqual(message.verifier("note", longue)["code"], 3)
        self.assertEqual(message.verifier("note", longue, premium=True)["code"], 2)

    def test_lien_dans_note(self):
        self.assertEqual(message.verifier("note", NOTE_OK[:120] + " assurly.example/etude")["code"], 3)


class Message(unittest.TestCase):
    BON = ("Merci d'avoir accepté. Dans votre post de mardi, vous disiez que 1 client sur 3 part avant 6 mois. "
           "On a mesuré la même chose en 2024 et la cause était le délai de remboursement. Vous avez regardé ce point chez vous ?")

    def test_prospection_sans_opposition(self):
        self.assertEqual(message.verifier("message", self.BON, prospection=True)["code"], 2)
        self.assertEqual(message.verifier("message", self.BON + " Si ce n'est pas le sujet, un mot suffit et je n'insiste pas.", prospection=True)["code"], 0)

    def test_agenda(self):
        self.assertEqual(message.verifier("message", self.BON + " Mon agenda : calendly.com/camille")["code"], 3)

    def test_demande_de_temps_vague(self):
        r = message.verifier("message", "Vous écriviez que la rétention compte plus que l'acquisition. Seriez-vous disponible pour un échange de 15 minutes ?")
        self.assertIn("demande de temps", " ".join(r["attentions"]))

    def test_trop_long(self):
        self.assertIn("600", " ".join(message.verifier("message", self.BON * 3)["attentions"]))

    def test_tiret(self):
        self.assertEqual(message.verifier("message", self.BON.replace(". On", " — on"))["code"], 3)


class Relance(unittest.TestCase):
    def test_sans_nouveau(self):
        self.assertEqual(message.verifier("relance", "Petite relance concernant mon message précédent.")["code"], 3)

    def test_avec_nouveau(self):
        self.assertEqual(message.verifier("relance", "On a publié le script des 60 appels, les 5 questions. Je vous l'envoie s'il peut servir à votre équipe.")["code"], 0)

    def test_troisieme(self):
        self.assertEqual(message.verifier("relance", "On vient de publier une étude.", relance_n=3)["code"], 3)


class Lot(unittest.TestCase):
    def test_envoi_en_masse(self):
        r = message.lot((ICI / "lot-exemple.txt").read_text(encoding="utf-8"))
        self.assertEqual(r["code"], 3)
        self.assertEqual(r["trop_proches"][0]["messages"], [1, 2])
        self.assertEqual(len(r["trop_proches"]), 1)


class Volume(unittest.TestCase):
    def test_automatisation_refusee(self):
        r = volume.controler(250, 0, 0, 2000, jours=5)
        self.assertEqual(r["verdict"], "REFUSÉ")

    def test_limite_et_acceptation(self):
        r = volume.controler(150, 40, 20, 120, acceptation=0.14)
        self.assertEqual(r["code"], 3)
        self.assertEqual(r["invitations_conseillees"], 0)
        self.assertEqual(len(r["bloquants"]), 3)

    def test_semaine_saine(self):
        r = volume.controler(20, 30, 8, 200, acceptation=0.34)
        self.assertEqual(r["code"], 0)
        self.assertEqual(r["invitations_conseillees"], 27)

    def test_journal(self):
        taux, base = volume.acceptation_journal(ICI / "journal-exemple.md")
        self.assertEqual(base, 65)
        self.assertAlmostEqual(taux, 25 / 65)

    def test_journal_modele_vide(self):
        self.assertEqual(volume.acceptation_journal(ICI.parents[1] / "templates" / "journal.md"), (None, 0))

    def test_notes_gratuites(self):
        r = volume.controler(10, 0, 0, 200, acceptation=0.3, notes=5)
        self.assertIn("3 par mois", " ".join(r["attentions"]))


class References(unittest.TestCase):
    def test_modeles_passent_le_controle(self):
        s = (SKILL / "references" / "contextes.md").read_text(encoding="utf-8")
        for m in re.finditer(r"NOTE \((\d+)/200\)\n(.*?)(?=\n\n|\n```)", s, re.S):
            t = " ".join(m.group(2).split())
            with self.subTest(note=t[:40]):
                self.assertEqual(len(t), int(m.group(1)))
                self.assertEqual(message.verifier("note", t)["code"], 0)
        for m in re.finditer(r"(PREMIER MESSAGE|\nMESSAGE)\n(.*?)(?=\n\n|\n```)", s, re.S):
            t = " ".join(m.group(2).split())
            with self.subTest(message=t[:40]):
                self.assertEqual(message.verifier("message", t)["code"], 0)

    def test_cli(self):
        p = subprocess.run([sys.executable, str(SKILL / "scripts" / "volume.py"), "--invitations", "20", "--en-attente", "40",
                            "--messages", "8", "--minutes", "180", "--journal", str(ICI / "journal-exemple.md")], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertIn("38%", p.stdout)


if __name__ == "__main__":
    unittest.main()
