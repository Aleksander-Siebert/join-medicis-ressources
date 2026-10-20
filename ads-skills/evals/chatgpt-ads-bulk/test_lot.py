#!/usr/bin/env python3
"""Tests de analyser_lot.py : python3 -m unittest discover evals/chatgpt-ads-bulk

Sur la campagne d'exemple du pack (Vélora, 40 annonces) : plan de lot
(groupes les moins garnis d'abord, 50 au plus, cible), structures et
facettes, mots répétés, quasi-doublons ; ajout d'un lot (chaque refus a sa
raison) ; notes et propositions ; lecture d'un classeur au schéma.
"""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
SKILL = PACK / "skills" / "chatgpt-ads-bulk"
SCRIPT = SKILL / "scripts" / "analyser_lot.py"
EXEMPLE = PACK / "skills" / "chatgpt-ads-skills" / "assets" / "exemple-campagne.json"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(SKILL / "commun"))
import analyser_lot as al  # noqa: E402
import classeur as cl  # noqa: E402


def exemple():
    return json.loads(EXEMPLE.read_text(encoding="utf-8"))


def lancer(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)


class TestOutils(unittest.TestCase):
    def test_structures(self):
        self.assertEqual(al.structure("Neuf ou reconditionné ?"), "question")
        self.assertEqual(al.structure("Découvrez nos vélos"), "impératif")
        self.assertEqual(al.structure("3 ans de garantie"), "chiffre")
        self.assertEqual(al.structure("Pour la rentrée"), "situation")
        self.assertEqual(al.structure("Un vélo livré monté"), "groupe nominal")

    def test_facettes(self):
        self.assertIn("budget", al.facettes("Reconditionné dès 900 €"))
        self.assertIn("occasion", al.facettes("Un vélo pour la rentrée"))
        self.assertIn("comparaison", al.facettes("Neuf ou reconditionné ?"))
        self.assertIn("question", al.facettes("Neuf ou reconditionné ?"))

    def test_similarite(self):
        sm, st = al.similarite("Votre vélo livré monté", "Votre vélo livré déjà monté")
        self.assertGreaterEqual(max(sm, st), al.SEUIL_MOTS)
        sm, st = al.similarite("Rentrer de l'école en vélo", "Batterie testée avant envoi")
        self.assertLess(max(sm, st), 0.3)


class TestAnalyse(unittest.TestCase):
    def test_plan_equilibre(self):
        camp = exemple()
        camp["ads"] = [a for a in camp["ads"] if a["adgroup_name"] != camp["adgroups"][0]["adgroup_name"]][:30] + \
            [a for a in camp["ads"] if a["adgroup_name"] == camp["adgroups"][0]["adgroup_name"]][:2]
        r = al.analyser(camp, cible=120, lot=50)
        g0 = camp["adgroups"][0]["adgroup_name"]
        self.assertEqual(r["lot_suivant"], 50)
        self.assertEqual(max(r["par_groupe"].items(), key=lambda x: x[1]["a_ajouter"])[0], g0)
        niveaux = [x["annonces"] + x["a_ajouter"] for x in r["par_groupe"].values()]
        self.assertLessEqual(max(niveaux) - min(niveaux), 1)

    def test_cible_atteinte(self):
        r = al.analyser(exemple(), cible=40)
        self.assertEqual(r["lot_suivant"], 0)

    def test_mots_repetes_et_doublons(self):
        camp = exemple()
        g = camp["adgroups"][0]["adgroup_name"]
        base = dict(camp["ads"][0])
        camp["ads"] = [dict(base, title=f"Vélo électrique {x}", copy="Un vélo électrique pour vos trajets du matin.")
                       for x in ("urbain", "malin", "léger")] + camp["ads"][1:4]
        r = al.analyser(camp)
        self.assertTrue(any(x["mot"].startswith("velo") for x in r["mots_repetes"]))
        self.assertTrue(r["quasi_doublons"])

    def test_classeur_schema(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "c.xlsx"
            cl.ecrire_xlsx(f, [{"adgroup_name": a["adgroup_name"], "title": a["title"], "copy": a["copy"],
                                "link": a["link"], "image_url": a["image_link"]} for a in exemple()["ads"]])
            camp = al.charger(f)
        self.assertEqual(len(camp["ads"]), 40)
        self.assertEqual(len(camp["adgroups"]), 5)


class TestAjout(unittest.TestCase):
    def setUp(self):
        self.camp = exemple()
        self.g = self.camp["adgroups"][0]["adgroup_name"]
        self.lien = self.camp["ads"][0]["link"]

    def nouvelle(self, titre, copie, **kw):
        return dict({"adgroup_name": self.g, "title": titre, "copy": copie, "link": self.lien,
                     "image_link": self.camp["ads"][0]["image_link"], "angle": "situation"}, **kw)

    def test_refus_motives(self):
        existant = self.camp["ads"][0]
        lot = {"ads": [
            self.nouvelle("Le soir, rentrer à vélo", "Le trajet du soir devient une balade."),
            self.nouvelle(existant["title"], "Une copie différente pour ce titre."),
            self.nouvelle("Un titre beaucoup trop long pour ici", "Copie correcte."),
            self.nouvelle("Livré en 48 h chrono", "Commandez avant midi."),
            self.nouvelle("Groupe fantôme ici", "Copie correcte.", adgroup_name="inexistant"),
            self.nouvelle(existant["title"] + " ", existant["copy"]),
        ]}
        acc, ref = al.ajouter(self.camp, lot)
        self.assertEqual([a["title"] for a in acc], ["Le soir, rentrer à vélo"])
        raisons = {r["n"]: " ; ".join(r["raisons"]) for r in ref}
        self.assertIn("titre déjà utilisé", raisons[2])
        self.assertIn("title 36 caractères", raisons[3])
        self.assertIn("allégation non approuvée « 48 h »", raisons[4])
        self.assertIn("inconnu", raisons[5])
        self.assertIn("quasi-doublon", raisons[6])

    def test_doublon_dans_le_lot(self):
        lot = {"ads": [self.nouvelle("Le soir, rentrer à vélo", "Le trajet du soir devient une balade."),
                       self.nouvelle("Le soir, rentrez à vélo", "Le trajet du soir devient une balade.")]}
        acc, ref = al.ajouter(self.camp, lot)
        self.assertEqual(len(acc), 1)
        self.assertIn("quasi-doublon", ref[0]["raisons"][-1])

    def test_commande_ajouter(self):
        with tempfile.TemporaryDirectory() as d:
            c, l, o = Path(d) / "c.json", Path(d) / "l.json", Path(d) / "o.json"
            c.write_text(json.dumps(self.camp, ensure_ascii=False), encoding="utf-8")
            l.write_text(json.dumps({"ads": [self.nouvelle("Le soir, rentrer à vélo", "Le trajet du soir devient une balade.")]},
                                    ensure_ascii=False), encoding="utf-8")
            p = lancer("ajouter", c, l, "-o", o)
            self.assertEqual(p.returncode, 0, p.stdout)
            self.assertEqual(len(json.loads(o.read_text(encoding="utf-8"))["ads"]), 41)
            l.write_text(json.dumps({"ads": [self.camp["ads"][0]]}, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(lancer("ajouter", c, l, "-o", o).returncode, 3)


class TestNotes(unittest.TestCase):
    def test_propositions(self):
        camp = exemple()
        a0 = camp["ads"][0]
        camp["ads"].append(dict(a0, title=a0["title"] + " !"))
        camp["ads"].append(dict(a0, title="Livré en 48 h chrono", copy="Commandez avant midi pour recevoir."))
        camp["ads"].append(dict(a0, title="Un titre beaucoup trop long pour ici", copy="Une copie tout à fait correcte ici."))
        notes = al.noter(camp)
        par = {(x["title"], x["copy"]): x for x in notes}
        self.assertEqual(par[(a0["title"] + " !", a0["copy"])]["proposition"], "Supprimer")
        self.assertEqual(par[("Livré en 48 h chrono", "Commandez avant midi pour recevoir.")]["sources"], 1)
        self.assertEqual(par[("Un titre beaucoup trop long pour ici", "Une copie tout à fait correcte ici.")]["proposition"], "Corriger")
        self.assertEqual(par[(a0["title"], a0["copy"])]["proposition"], "Conserver")

    def test_commandes(self):
        p = lancer("analyser", EXEMPLE, "--cible", "120")
        self.assertIn("Ce lot : **50 annonces**", p.stdout)
        p = lancer("noter", EXEMPLE)
        self.assertIn("| Groupe | Titre | Longueur |", p.stdout)
        self.assertEqual(lancer("analyser", "absent.json").returncode, 1)


if __name__ == "__main__":
    unittest.main()
