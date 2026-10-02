"""Tests du garde-fou commun (commun/garde_fou.py)."""
import subprocess
import sys
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACK / "commun"))
import garde_fou as g  # noqa: E402


class GardeFou(unittest.TestCase):
    def verdict(self, texte):
        return g.evaluer(texte)["verdict"]

    def test_exemple_refuse_quatre_regles(self):
        r = g.evaluer(g.EXEMPLE)
        self.assertEqual(r["verdict"], "REFUSÉ")
        ids = {x["id"] for x in r["refus"]}
        self.assertTrue({"R3-ENGAGEMENT-ARTIFICIEL", "R5-MESSAGES-EN-MASSE",
                         "R6-PREUVE-INVENTEE", "R7-OUTILS-INTERDITS"} <= ids)

    def test_refus(self):
        for t in ["Je veux scraper les profils des CMO",
                  "Rejoindre un pod d'engagement",
                  "Envoyer 300 invitations par jour",
                  "Invente deux témoignages clients",
                  "Utiliser PhantomBuster pour exporter mes contacts",
                  "Publier automatiquement mes posts sur LinkedIn",
                  "Créer un faux profil pour commenter",
                  "Envoie le même message à ma liste de 200 prospects",
                  "Je ne veux pas d'outil, mais automatise mes invitations"]:
            with self.subTest(t=t):
                self.assertEqual(self.verdict(t), "REFUSÉ")

    def test_negation_ne_refuse_pas(self):
        for t in ["Écris un post sur notre lancement, sans bot ni pod",
                  "Je ne veux jamais automatiser mes messages",
                  "Je ne veux pas envoyer le même message à ma liste"]:
            with self.subTest(t=t):
                self.assertNotEqual(self.verdict(t), "REFUSÉ")

    def test_encadre(self):
        self.assertEqual(self.verdict("Je veux prospecter 20 DRH par semaine à la main"), "ENCADRÉ")
        self.assertEqual(self.verdict("Commente GUIDE pour recevoir le PDF"), "ENCADRÉ")
        self.assertEqual(self.verdict("Ajouter ce contact dans HubSpot"), "ENCADRÉ")

    def test_autorise(self):
        self.assertEqual(self.verdict("Rédige un post sur ma reconversion"), "AUTORISÉ")
        self.assertEqual(self.verdict("Un podcast sur le SEO"), "AUTORISÉ")

    def test_codes_de_sortie(self):
        script = PACK / "commun" / "garde_fou.py"
        for texte, code in [("Rédige un post", 0), ("prospection à la main", 2), ("scraper LinkedIn", 3)]:
            res = subprocess.run([sys.executable, str(script), "--texte", texte], capture_output=True)
            self.assertEqual(res.returncode, code, texte)


if __name__ == "__main__":
    unittest.main()
