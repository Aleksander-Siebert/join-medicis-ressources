"""Tests du mail (python3 -m unittest discover -s tests)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import mail as m  # noqa: E402

A_TRAITER = {"sujets": [{"sources": [{"nom": "Le Média Un", "url": "https://news.google.com/rss/articles/abc", "domaine": "media-un.example"}]}], "pages_modifiees": [{"url": "https://concurrent-a.example/tarifs"}]}
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

    def test_article_d_origine_du_meme_media_accepte(self):
        info = {"titre": "Info", "texte": "t", "pourquoi": "p", "sources": [{"nom": "Le Média Un", "url": "https://www.media-un.example/2026/11/article-complet"}]}
        err, _ = m.verifier({**RESUME, "sections": [{"titre": "X", "infos": [info]}]}, A_TRAITER)
        self.assertEqual(err, [])

    def test_google_ne_couvre_pas_tout_le_web(self):
        info = {"titre": "Info", "texte": "t", "pourquoi": "p", "sources": [{"nom": "?", "url": "https://news.google.com/autre"}]}
        err, _ = m.verifier({**RESUME, "sections": [{"titre": "X", "infos": [info]}]}, A_TRAITER)
        self.assertTrue(err)

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

    def test_modele_par_defaut(self):
        h = m.rendre_html(RESUME)
        self.assertIn("À retenir", h)
        self.assertIn("Offre Essentiel à 9 €", h)
        self.assertIn('href="https://concurrent-a.example/tarifs"', h)
        self.assertNotIn("DEBUT:", h)
        self.assertNotIn("{{", h)
        self.assertNotIn("À surveiller", h)  # bloc vide retiré

    def test_modele_personnalise(self):
        modele = "<h1>{{objet}}</h1><!-- DEBUT:section --><h2>{{section}}</h2><!-- DEBUT:info --><p>{{titre}}<!-- DEBUT:source --> [{{nom}}]<!-- FIN:source --></p><!-- FIN:info --><!-- FIN:section -->"
        h = m.rendre_html(RESUME, modele)
        self.assertEqual(h, "<h1>Concurrent A baisse son offre d&#x27;entrée à 9 €</h1><h2>Prix et offres</h2><p>Offre Essentiel à 9 € [Page tarifs]</p>")

    def test_rendu_echappe_le_html(self):
        r = {**RESUME, "objet": "<script>alert(1)</script>"}
        self.assertNotIn("<script>alert", m.rendre_html(r))
        self.assertIn("Pour toi : Ton offre", m.rendre_texte(r))



class ModelesEtReglages(unittest.TestCase):
    RACINE = Path(__file__).resolve().parent.parent

    def _modele(self, nom):
        return (self.RACINE / "modeles" / f"{nom}.html").read_text("utf-8")

    def test_les_trois_modeles_se_remplissent_sans_reste(self):
        for nom in m.MODELES:
            h = m.rendre_html(RESUME, self._modele(nom), {"modele": nom})
            self.assertNotIn("{{", h, nom)
            self.assertNotIn("DEBUT:", h, nom)
            self.assertIn("https://concurrent-a.example/tarifs", h, nom)

    def test_reglages_appliques(self):
        h = m.rendre_html(RESUME, self._modele("recap"), {"titre": "Veille Assurly", "couleur": "#112233", "logo": "https://assurly.example/logo.png", "signature": "Équipe marketing"})
        for attendu in ("Veille Assurly", "#112233", "https://assurly.example/logo.png", "Équipe marketing"):
            self.assertIn(attendu, h)

    def test_sans_logo_pas_d_image(self):
        self.assertNotIn("<img", m.rendre_html(RESUME, self._modele("themes"), {}))

    def test_reglages_invalides_remplaces_et_signales(self):
        import json, shutil, tempfile
        d = Path(tempfile.mkdtemp())
        (d / "mail.json").write_text(json.dumps({"couleur": "rouge\"><script>", "logo": "javascript:alert(1)", "canaux": ["mail", "fax"], "modele": "recap"}), "utf-8")
        r, avert = m.lire_reglages(d)
        self.assertEqual((r["couleur"], r["logo"], r["canaux"], r["modele"]), (m.REGLAGES["couleur"], "", ["mail"], "recap"))
        self.assertEqual(len(avert), 3)
        shutil.rmtree(d)

    def test_points_cles_selon_le_modele(self):
        r = {**RESUME, "a_retenir": ["a", "b", "c", "d", "e"]}
        self.assertTrue(m.verifier(r, A_TRAITER, m.MODELES["themes"])[0])
        self.assertEqual(m.verifier(r, A_TRAITER, m.MODELES["recap"])[0], [])

    def test_appel_d_offres_et_offre_d_emploi_sont_des_sources_connues(self):
        at = {"sujets": [], "appels_offres": [{"url": "https://www.boamp.fr/pages/avis/?q=idweb:26-1"}], "emplois": [{"url": "https://jobs.lever.co/a", "nouvelles": [{"url": "https://jobs.lever.co/a/3"}]}]}
        infos = [{"titre": "Marché", "texte": "t", "pourquoi": "p", "sources": [{"nom": "BOAMP", "url": "https://www.boamp.fr/pages/avis/?q=idweb:26-1"}]},
                 {"titre": "Recrutement", "texte": "t", "pourquoi": "p", "sources": [{"nom": "Offre", "url": "https://jobs.lever.co/a/3"}]}]
        self.assertEqual(m.verifier({**RESUME, "sections": [{"titre": "X", "infos": infos}]}, at)[0], [])

    def test_markdown_et_slack(self):
        md = m.rendre_markdown(RESUME, {"modele": "recap"})
        self.assertIn("1. [Offre Essentiel à 9 €](https://concurrent-a.example/tarifs)", md)
        sl = m.rendre_slack({**RESUME, "objet": "A < B & C"}, {})
        self.assertIn("*A &lt; B &amp; C*", sl)
        self.assertIn("<https://concurrent-a.example/tarifs|Offre Essentiel à 9 €>", sl)

    def test_veille_deja_envoyee_bloquee(self):
        import json, shutil, tempfile
        d = Path(tempfile.mkdtemp())
        (d / "memoire").mkdir()
        (d / "memoire" / "dernier-envoi.json").write_text(json.dumps({"genere_le": "G1", "valide_le": "2026-11-09T08:00:00"}), "utf-8")
        self.assertEqual(m.deja_envoye(d, {"genere_le": "G1"}), "2026-11-09")
        self.assertIsNone(m.deja_envoye(d, {"genere_le": "G2"}))
        shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
