#!/usr/bin/env python3
"""Tests de ids.py : python3 -m unittest discover evals/chatgpt-ads-ids

API simulée (aucun appel réseau) : pagination, lecture seule, erreurs et
nouvel essai, recherche par nom ; voie fichier (préfixes) ; fusion dans un
classeur au schéma et dans un JSON de campagne, noms ambigus ; clé jamais
affichée.
"""
import contextlib
import csv
import io
import json
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
SKILL = PACK / "skills" / "chatgpt-ads-ids"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(SKILL / "commun"))
import ids  # noqa: E402
import classeur as cl  # noqa: E402

CLE = "sk-test-NE-PAS-AFFICHER"


class FausseAPI:
    """Répond comme la documentation ; mémorise les appels."""

    def __init__(self, pages=2, echecs_429=0, code=None):
        self.appels, self.pages, self.echecs_429, self.code = [], pages, echecs_429, code

    def __call__(self, methode, url, entetes, corps):
        self.appels.append((methode, url))
        assert entetes["Authorization"] == f"Bearer {CLE}"
        if self.code:
            return self.code, {}, json.dumps({"error": {"message": "refusé"}}).encode()
        if self.echecs_429:
            self.echecs_429 -= 1
            return 429, {"Retry-After": "0"}, b"{}"
        u = urllib.parse.urlsplit(url)
        q = dict(urllib.parse.parse_qsl(u.query))
        chemin = u.path.replace("/v1", "", 1)
        if chemin == "/ad_account":
            return 200, {}, json.dumps({"id": "adacct_1", "name": "Assurly", "currency_code": "EUR",
                                        "timezone": "Europe/Paris", "status": "active"}).encode()
        if chemin == "/campaigns":
            if "after" not in q:
                return 200, {}, json.dumps({"data": [{"id": "cmpn_1", "name": "Expat FR", "status": "paused"}],
                                            "has_more": self.pages > 1, "last_id": "cmpn_1"}).encode()
            return 200, {}, json.dumps({"data": [{"id": "cmpn_2", "name": "Etudiants FR", "status": "paused"}],
                                        "has_more": False, "last_id": "cmpn_2"}).encode()
        if chemin == "/campaigns/cmpn_1":
            return 200, {}, json.dumps({"id": "cmpn_1", "name": "Expat FR"}).encode()
        if chemin == "/ad_groups":
            groupes = {"cmpn_1": [{"id": "adgrp_11", "name": "expat-preparer"}, {"id": "adgrp_12", "name": "expat-famille"}],
                       "cmpn_2": [{"id": "adgrp_21", "name": "etudiant-depart"}]}[q["campaign_id"]]
            if "name" in q:
                groupes = [g for g in groupes if g["name"].lower() == q["name"].lower()]
            return 200, {}, json.dumps({"data": groupes, "has_more": False}).encode()
        if chemin == "/ads":
            return 200, {}, json.dumps({"data": [{"id": f"ad_{q['ad_group_id'][-2:]}1", "name": "a-01", "status": "paused",
                                                  "review_status": "approved",
                                                  "creative": {"file_id": "file_9", "title": "Partir vivre à Lisbonne"}}],
                                        "has_more": False}).encode()
        if chemin == "/conversions/event_settings":
            return 200, {}, json.dumps({"data": [{"id": "ces_5", "name": "Devis", "event_type": "lead_created"}],
                                        "has_more": False}).encode()
        if chemin == "/upload":
            return 200, {}, json.dumps({"file_id": "file_77"}).encode()
        return 404, {}, b"{}"


def lancer(args, api=None, env_cle=CLE):
    import os
    ancien = os.environ.get("OPENAI_ADS_API_KEY")
    if env_cle is None:
        os.environ.pop("OPENAI_ADS_API_KEY", None)
    else:
        os.environ["OPENAI_ADS_API_KEY"] = env_cle
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = ids.main(args, transport=api)
    finally:
        if ancien is None:
            os.environ.pop("OPENAI_ADS_API_KEY", None)
        else:
            os.environ["OPENAI_ADS_API_KEY"] = ancien
    return code, out.getvalue(), err.getvalue()


class TestAPI(unittest.TestCase):
    def test_compte(self):
        code, out, _ = lancer(["compte"], FausseAPI())
        self.assertEqual(code, 0)
        self.assertIn("EUR", out)
        self.assertNotIn(CLE, out)

    def test_lister_pagine_et_lit_seulement(self):
        api = FausseAPI()
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "ids.csv"
            code, out, _ = lancer(["lister", "--annonces", "-o", str(f)], api)
            with open(f, encoding="utf-8") as h:
                lignes = list(csv.DictReader(h))
        self.assertEqual(code, 0)
        self.assertEqual({x["niveau"] for x in lignes}, {"campagne", "groupe", "annonce"})
        self.assertIn("adgrp_21", {x["ad_group_id"] for x in lignes})
        self.assertIn("file_9", {x["image_file_id"] for x in lignes})
        self.assertTrue(all(m == "GET" for m, _ in api.appels))
        self.assertTrue(any("after=cmpn_1" in u for _, u in api.appels))
        self.assertTrue(all("limit=500" in u for _, u in api.appels if "/ad_account" not in u))

    def test_lister_une_campagne(self):
        code, out, _ = lancer(["lister", "--campagne", "cmpn_1"], FausseAPI())
        self.assertIn("adgrp_12", out)
        self.assertNotIn("adgrp_21", out)

    def test_chercher(self):
        code, out, _ = lancer(["chercher", "EXPAT-preparer"], FausseAPI())
        self.assertEqual(code, 0)
        self.assertIn("adgrp_11", out)
        code, _, _ = lancer(["chercher", "inconnu"], FausseAPI())
        self.assertEqual(code, 2)

    def test_evenements(self):
        code, out, _ = lancer(["evenements"], FausseAPI())
        self.assertIn("ces_5", out)

    def test_cle_absente(self):
        code, _, err = lancer(["compte"], FausseAPI(), env_cle=None)
        self.assertEqual(code, 1)
        self.assertIn("jamais dans la conversation", err)

    def test_erreurs(self):
        code, _, err = lancer(["compte"], FausseAPI(code=401))
        self.assertEqual(code, 3)
        self.assertIn("HTTP 401", err)
        self.assertNotIn(CLE, err)

    def test_nouvel_essai_429(self):
        api = FausseAPI(echecs_429=2)
        client = ids.Client(CLE, api, pause=lambda s: None)
        self.assertEqual(client.requete("GET", "/ad_account")["currency_code"], "EUR")
        self.assertEqual(len(api.appels), 3)

    def test_televerser_demande_confirmation(self):
        api = FausseAPI()
        code, out, _ = lancer(["televerser", "https://assurly.example/img.png"], api)
        self.assertEqual(code, 1)
        self.assertEqual(api.appels, [])
        code, out, _ = lancer(["televerser", "https://assurly.example/img.png", "--confirmer"], api)
        self.assertIn("file_77", out)
        self.assertEqual(api.appels[0][0], "POST")


class TestFichiers(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_depuis_fichier(self):
        f = self.d / "export.csv"
        f.write_text("Campaign name;Ad group name;Ad group ID;Status\nExpat FR;expat-preparer;adgrp_11;Paused\n"
                     "Expat FR;expat-famille;adgrp_12;Paused\n", encoding="utf-8")
        lignes = ids.ids_depuis_fichier(f)
        self.assertEqual([(x["adgroup_name"], x["ad_group_id"]) for x in lignes],
                         [("expat-preparer", "adgrp_11"), ("expat-famille", "adgrp_12")])

    def test_prefixe_ad_et_adgrp_distincts(self):
        f = self.d / "a.csv"
        f.write_text("ad_id,ad_group_id,ad_name\nad_5,adgrp_1,a-01\n", encoding="utf-8")
        x = ids.ids_depuis_fichier(f)[0]
        self.assertEqual((x["ad_id"], x["ad_group_id"], x["niveau"]), ("ad_5", "adgrp_1", "annonce"))

    def ecrire_ids(self, lignes):
        f = self.d / "ids.csv"
        ids.ecrire_csv(f, lignes)
        return f

    def test_fusionner_classeur(self):
        src, out = self.d / "c.xlsx", self.d / "o.xlsx"
        base = {"adgroup_name": "Expat-Préparer", "title": "Partir vivre à Lisbonne", "copy": "Démarches et calendrier.",
                "link": "https://assurly.example/x", "image_url": "https://assurly.example/i.png"}
        cl.ecrire_xlsx(src, [base, dict(base, adgroup_name="inconnu"), dict(base, adgroup_name="double")])
        f = self.ecrire_ids([{"ad_group_id": "adgrp_11", "adgroup_name": "expat-preparer"},
                             {"ad_group_id": "adgrp_31", "adgroup_name": "double"},
                             {"ad_group_id": "adgrp_32", "adgroup_name": "Double"}])
        code, out_txt, _ = lancer(["fusionner", str(src), "--ids", str(f), "-o", str(out), "--xlsx"])
        self.assertEqual(code, 2)
        self.assertIn("ambigu", out_txt)
        self.assertIn("aucun ad group « inconnu »", out_txt)
        _, l = cl.annonces(cl.lire(out))
        self.assertEqual([x.get("ad_group_id", "") for x in l], ["adgrp_11", "", ""])

    def test_fusionner_ne_remplace_pas(self):
        lignes = [{"adgroup_name": "expat-preparer", "ad_group_id": "adgrp_99"}]
        journal, n = ids.fusionner(lignes, [{"ad_group_id": "adgrp_11", "adgroup_name": "expat-preparer"}])
        self.assertEqual(lignes[0]["ad_group_id"], "adgrp_99")
        self.assertEqual(n, 1)

    def test_fusionner_ad_id_seulement_sur_demande(self):
        lignes = [{"adgroup_name": "g", "ad_name": "a-01"}]
        idsl = [{"ad_group_id": "adgrp_1", "adgroup_name": "g", "ad_id": "ad_5", "ad_name": "a-01"}]
        ids.fusionner(lignes, idsl)
        self.assertNotIn("ad_id", lignes[0])
        journal, _ = ids.fusionner(lignes, idsl, True)
        self.assertEqual(lignes[0]["ad_id"], "ad_5")
        self.assertTrue(any("MODIFIERA" in j for j in journal))

    def test_fusionner_json(self):
        src, out = self.d / "c.json", self.d / "o.json"
        src.write_text(json.dumps({"adgroups": [{"adgroup_name": "expat-preparer"}], "ads": []}), encoding="utf-8")
        f = self.ecrire_ids([{"ad_group_id": "adgrp_11", "adgroup_name": "expat-preparer"}])
        code, _, _ = lancer(["fusionner", str(src), "--ids", str(f), "-o", str(out)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out.read_text())["adgroups"][0]["ad_group_id"], "adgrp_11")

    def test_utm(self):
        code, out, _ = lancer(["utm"])
        self.assertIn("{campaign_id}", out)
        self.assertIn("{ad_id}", out)


if __name__ == "__main__":
    unittest.main()
