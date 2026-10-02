"""Tests des scripts de skills/linkedin-profile (titre, infos, audit_profil)."""
import json
import sys
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
SKILL = PACK / "skills" / "linkedin-profile"
sys.path.insert(0, str(SKILL / "scripts"))
import audit_profil as a  # noqa: E402
import infos as i  # noqa: E402
import titre as t  # noqa: E402


class Titre(unittest.TestCase):
    def test_exemples(self):
        self.assertEqual(t.noter(t.EXEMPLE_FORT)["verdict"], "PRÊT")
        faible = t.noter(t.EXEMPLE_FAIBLE)
        self.assertEqual(faible["verdict"], "À RÉÉCRIRE")
        self.assertTrue(any(c["dimension"] == "clarté" and "passionnee" in c["constat"] for c in faible["constats"]))

    def test_intitule_seul(self):
        r = t.noter("Responsable marketing chez Assurly")
        self.assertEqual(r["dimensions"]["audience"], 0)
        self.assertEqual(r["verdict"], "À RÉÉCRIRE")

    def test_trop_long_bloque(self):
        r = t.noter("Consultante SEO pour les PME | " + "x" * 220)
        self.assertGreater(r["longueur"]["depasse"], 0)
        self.assertLessEqual(r["note"], 49)

    def test_pseudo_gras_bloque(self):
        r = t.noter("𝗖𝗼𝗻𝘀𝘂𝗹𝘁𝗮𝗻𝘁𝗲 SEO pour les PME industrielles | +180% de trafic pour 14 clients")
        self.assertEqual(r["verdict"], "À RÉÉCRIRE")
        self.assertTrue(any(c["dimension"] == "accessibilité" for c in r["constats"]))

    def test_pas_de_doublon_de_mot_creux(self):
        r = t.noter("Marketing Manager passionnée")
        constat = next(c for c in r["constats"] if "Mots creux" in c["constat"])
        self.assertNotIn("passionne,", constat["constat"])

    def test_exemples_de_la_reference(self):
        texte = (SKILL / "references" / "exemple.md").read_text(encoding="utf-8")
        self.assertIn("85 (PRÊT)", texte)
        titre = json.loads((SKILL / "exemples" / "profil-apres.json").read_text(encoding="utf-8"))["titre"]
        self.assertEqual(t.noter(titre)["note"], 85)


class Infos(unittest.TestCase):
    def test_exemple_passe(self):
        self.assertEqual(i.controler(i.EXEMPLE)["verdict"], "PASSE")

    def test_pli_coupe_et_cta(self):
        texte = ("Fort de 15 ans d'expérience dans le marketing digital je suis un professionnel passionné "
                 "et dynamique qui aime relever de nouveaux défis et accompagner les entreprises dans leur "
                 "transformation digitale grâce à une expertise pointue et une approche qui fait la différence "
                 "au quotidien pour tous mes interlocuteurs et partenaires")
        r = i.controler(texte)
        ids = {c["controle"] for c in r["constats"] if c["gravite"] == "bloquant"}
        self.assertIn("pli", ids)
        self.assertIn("appel à l'action", ids)

    def test_cta_facultatif_en_autorite(self):
        texte = i.EXEMPLE.rsplit("\n\n", 1)[0]
        clients = {c["controle"]: c["gravite"] for c in i.controler(texte, "clients")["constats"]}
        autorite = {c["controle"]: c["gravite"] for c in i.controler(texte, "autorite")["constats"]}
        self.assertEqual(clients.get("appel à l'action"), "bloquant")
        self.assertEqual(autorite.get("appel à l'action"), "attention")

    def test_trop_long(self):
        r = i.controler(i.EXEMPLE + ("\n\nUne phrase de plus pour allonger." * 80))
        self.assertTrue(any(c["controle"] == "longueur" and c["gravite"] == "bloquant" for c in r["constats"]))

    def test_mots_cles(self):
        r = i.controler(i.EXEMPLE, mots_cles=["acquisition", "growth hacking"])
        c = next(c for c in r["constats"] if c["controle"] == "mots-clés")
        self.assertIn("growth hacking", c["constat"])
        self.assertNotIn("acquisition", c["constat"])


class Audit(unittest.TestCase):
    def test_grille_100(self):
        g = json.loads((SKILL / "grille.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(c["points"] for c in g["criteres"]), 100)
        self.assertEqual(set(a.POURQUOI), {c["id"] for c in g["criteres"]})

    def test_section_non_montree_non_notee(self):
        r = a.auditer({"titre": "Responsable marketing chez Assurly"})
        self.assertEqual(r["sur"], 14)  # seul le titre a été montré
        r2 = a.auditer({"objectif": "autorite", "titre": "x"})
        self.assertIn("Recommandations", r2["non_notes"])

    def test_avant_apres(self):
        avant = a.auditer(json.loads((SKILL / "exemples" / "profil-avant.json").read_text(encoding="utf-8")))
        apres = a.auditer(json.loads((SKILL / "exemples" / "profil-apres.json").read_text(encoding="utf-8")))
        self.assertEqual(avant["verdict"], "FAIBLE")
        self.assertEqual(apres["verdict"], "SOLIDE")
        self.assertEqual((avant["note"], avant["sur"]), (27, 93))
        self.assertEqual((apres["note"], apres["sur"]), (78, 93))
        self.assertEqual(avant["fourchette_sur_100"], [27, 34])

    def test_plan_premiere_heure_tient_en_une_heure(self):
        r = a.auditer(a.EXEMPLE)
        effort = sum(c["effort_heures"] for c in r["corrections"] if c["nom"] in r["plan_premiere_heure"])
        self.assertLessEqual(effort, 1.0 + 1e-9)
        pph = [c["points_par_heure"] for c in r["corrections"]]
        self.assertEqual(pph, sorted(pph, reverse=True))

    def test_hors_reecriture(self):
        r = a.auditer(a.EXEMPLE)
        self.assertIn("Bannière", r["hors_reecriture"])
        self.assertNotIn("Titre", r["hors_reecriture"])


if __name__ == "__main__":
    unittest.main()
