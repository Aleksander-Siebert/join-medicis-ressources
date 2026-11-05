"""Tests du mail (python3 -m unittest discover -s tests)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import mail as m  # noqa: E402

A_TRAITER = {"sujets": [{"sources": [{"nom": "Le Média Un", "url": "https://media-un.example/article-1"}]}], "pages_modifiees": [{"url": "https://concurrent-a.example/tarifs"}]}
RESUME = {
    "objet": "Concurrent A baisse son offre d'entrée à 9 €",
    "periode": "du 2 au 9 novembre 2026",
    "a_retenir": ["Concurrent A passe son offre Essentiel de 12 à 9 € par mois."],
    "sections": [{"titre": "Prix et offres", "infos": [{"titre": "Offre Essentiel à 9 €", "texte": "La page tarifs affiche 9 € au lieu de 12 €.", "pourquoi": "Ton offre d'entrée est à 11 €.", "date": "2026-11-06", "sources": [{"nom": "Page tarifs", "url": "https://concurrent-a.example/tarifs"}]}]}],
    "stats": {"lus": 12, "sujets": 4, "pages_modifiees": 1},
}


class Mail(unittest.TestCase):
    def test_resume_valide(self):
        err, _ = m.verifier(RESUME, A_TRAITER)
        self.assertEqual(err, [])

    def test_source_inventee_bloquee(self):
        r = {**RESUME, "sections": [{"titre": "X", "infos": [{"titre": "Info", "texte": "t", "pourquoi": "p", "sources": [{"nom": "?", "url": "https://ailleurs.example"}]}]}]}
        err, _ = m.verifier(r, A_TRAITER)
        self.assertTrue(any("ne vient pas de la collecte" in e for e in err))

    def test_info_sans_source_bloquee(self):
        r = {**RESUME, "sections": [{"titre": "X", "infos": [{"titre": "Info", "texte": "t", "pourquoi": "p", "sources": []}]}]}
        err, _ = m.verifier(r, A_TRAITER)
        self.assertTrue(any("aucune source" in e for e in err))

    def test_trop_de_points_a_retenir(self):
        err, _ = m.verifier({**RESUME, "a_retenir": ["a", "b", "c", "d"]}, A_TRAITER)
        self.assertTrue(err)

    def test_mail_vide_honnete(self):
        r = {"objet": "Rien de neuf cette semaine", "rien_de_neuf": "Aucun changement chez tes 5 concurrents.", "sections": [], "stats": {"lus": 30, "sujets": 0}}
        err, _ = m.verifier(r, A_TRAITER)
        self.assertEqual(err, [])
        self.assertIn("Aucun changement", m.rendre_html(r))

    def test_typographie(self):
        r = {**RESUME, "a_retenir": ["Hausse de 15 % — à suivre"]}
        _, av = m.verifier(r, A_TRAITER)
        self.assertEqual(len(av), 2)

    def test_dates_en_francais(self):
        self.assertEqual(m.date_fr("2026-10-30"), "30 octobre")
        self.assertEqual(m.date_fr("2026-11-01"), "1er novembre")
        self.assertEqual(m.date_fr(None), "")
        self.assertIn("6 novembre", m.rendre_html(RESUME))

    def test_rendu_echappe_le_html(self):
        r = {**RESUME, "objet": "<script>alert(1)</script>"}
        self.assertNotIn("<script>alert", m.rendre_html(r))
        self.assertIn("Pour toi : Ton offre", m.rendre_texte(r))


if __name__ == "__main__":
    unittest.main()
