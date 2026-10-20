#!/usr/bin/env python3
"""Tests de valider_exporter.py : python3 -m unittest discover evals/chatgpt-ads-skills

Lecture du modèle, contrôles (un test par règle bloquante ou d'attention),
export XLSX (aller-retour, en-têtes conservés, ligne d'exemple retirée,
texte normal), commandes en ligne. Sans dépendance ; si openpyxl est
installé, un test de plus ouvre le fichier comme le ferait un tableur.
"""
import copy
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
import unicodedata
import zipfile
from datetime import date
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / "skills" / "chatgpt-ads-skills"
SCRIPT = SKILL / "scripts" / "valider_exporter.py"
MODELE = SKILL / "assets" / "modele-import.xlsx"
EXEMPLE = SKILL / "assets" / "exemple-campagne.json"
AUJ = date(2026, 10, 15)

spec = importlib.util.spec_from_file_location("valider_exporter", SCRIPT)
ve = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ve)
MOD = ve.lire_modele(MODELE)

# Un modèle « à la manière d'Ads Manager » (préfixe XML x:, ligne d'exemple en italique, lien hypertexte,
# libellés anglais), construit par le pack : le fichier d'OpenAI n'est pas redistribué.
spec_c = importlib.util.spec_from_file_location("construire_modele", SKILL.parents[1] / "outils" / "construire_modele.py")
cm = importlib.util.module_from_spec(spec_c)
spec_c.loader.exec_module(cm)
_TMP = tempfile.TemporaryDirectory()
MODELE_AM = Path(_TMP.name) / "modele-ads-manager.xlsx"
cm.construire(MODELE_AM, prefixe="x:", exemple=True, langue="en")


def exemple():
    return json.loads(EXEMPLE.read_text(encoding="utf-8"))


def points(camp, niveau=None, mode=None):
    r, _ = ve.valider(camp, MOD, AUJ, mode)
    return [p for p in r.points if niveau is None or p["niveau"] == niveau]


def messages(camp, niveau):
    return " | ".join(p["message"] for p in points(camp, niveau))


def lancer(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)


class Modele(unittest.TestCase):
    def test_trois_onglets_dans_l_ordre(self):
        self.assertEqual(MOD["onglets"], ["campaigns", "adgroups", "ads"])

    def test_limites_lues_dans_le_modele(self):
        self.assertEqual(MOD["limites"], {"title": 24, "copy": 48})

    def test_colonnes_attendues(self):
        noms = {o: [n for _, n in c] for o, c in MOD["colonnes"].items()}
        self.assertEqual(noms["ads"], ["adgroup_name", "title", "copy", "link", "image_link"])
        self.assertIn("Context Hints", noms["adgroups"])
        self.assertIn("conversion_event_setting_ids", noms["campaigns"])

    def test_limites_suivent_un_modele_modifie(self):
        with tempfile.TemporaryDirectory() as d:
            autre = Path(d) / "m.xlsx"
            with zipfile.ZipFile(MODELE_AM) as z, zipfile.ZipFile(autre, "w") as w:
                for n in z.namelist():
                    c = z.read(n)
                    if n == "xl/worksheets/sheet3.xml":
                        c = c.replace(b"max 24 chars", b"max 30 chars")
                    w.writestr(n, c)
            self.assertEqual(ve.lire_modele(autre)["limites"]["title"], 30)
            camp = exemple()
            camp["ads"][0]["title"] = "Un titre de vingt-huit car."
            self.assertEqual(ve.longueur(camp["ads"][0]["title"]), 27)
            r, _ = ve.valider(camp, ve.lire_modele(autre), AUJ)
            self.assertFalse([p for p in r.points if p["niveau"] == "BLOQUANT"])

    def test_limites_en_francais_et_en_anglais(self):
        self.assertEqual(ve.lire_modele(MODELE_AM)["limites"], {"title": 24, "copy": 48})

    def test_modele_maison_a_jour_et_different_d_un_fichier_ads_manager(self):
        self.assertEqual(MODELE.read_bytes(), cm.construire(None))
        with zipfile.ZipFile(MODELE) as z:
            tout = "".join(z.read(n).decode("utf-8") for n in z.namelist())
        self.assertNotIn("oaitest", tout)
        self.assertIn("Join Médicis", tout)
        self.assertIn("dataValidation", tout)

    def test_commande_modele(self):
        p = lancer("modele")
        self.assertEqual(p.returncode, 0)
        self.assertIn("titre 24 caractères, copie 48", p.stdout)


class Exemple(unittest.TestCase):
    def test_exemple_pret(self):
        self.assertEqual(points(exemple(), "BLOQUANT"), [])
        self.assertEqual(points(exemple(), "ATTENTION"), [])

    def test_exemple_volume_et_structure(self):
        camp = exemple()
        self.assertGreaterEqual(len(camp["adgroups"]), 5)
        self.assertTrue(40 <= len(camp["ads"]) <= 50)
        for g in camp["adgroups"]:
            self.assertEqual(len(g["context_hints"]), 3, g["adgroup_name"])
            self.assertEqual(len(g["prompts_test"]), 3, g["adgroup_name"])
            self.assertTrue(g["idee_visuel"] and g["intention"])

    def test_exemple_fictif(self):
        t = EXEMPLE.read_text(encoding="utf-8")
        self.assertIn("fictif", t)
        self.assertTrue(all(".example" in a["link"] for a in exemple()["ads"]))

    def test_typographie_des_annonces(self):
        for a in exemple()["ads"]:
            for champ in ("title", "copy"):
                self.assertNotIn("—", a[champ])
                self.assertNotRegex(a[champ], r"\S[?!:;]", a[champ])


class Longueurs(unittest.TestCase):
    def test_titre_trop_long_bloque(self):
        camp = exemple()
        camp["ads"][0]["title"] = "x" * 25
        self.assertIn("title de 25 caractères (max 24)", messages(camp, "BLOQUANT"))

    def test_copie_trop_longue_bloque(self):
        camp = exemple()
        camp["ads"][0]["copy"] = "y" * 49
        self.assertIn("copy de 49 caractères (max 48)", messages(camp, "BLOQUANT"))

    def test_limite_exacte_passe(self):
        camp = exemple()
        camp["ads"][0]["title"], camp["ads"][0]["copy"] = "a" * 24, "b" * 48
        self.assertNotIn("caractères (max", messages(camp, "BLOQUANT"))

    def test_accent_decompose_compte_pour_un(self):
        nfd = unicodedata.normalize("NFD", "Vélo révisé")
        self.assertEqual(len(nfd), 14)
        self.assertEqual(ve.longueur(nfd), 11)

    def test_espace_avant_point_d_interrogation_compte(self):
        self.assertEqual(ve.longueur("Neuf ou reconditionné ?"), 23)

    def test_titre_vide_bloque(self):
        camp = exemple()
        camp["ads"][0]["title"] = " "
        self.assertIn("case vide : title", messages(camp, "ATTENTION"))

    def test_sous_la_cible_en_information(self):
        camp = exemple()
        camp["ads"][0]["title"] = "Vélo"
        self.assertIn("sous la cible", messages(camp, "INFO"))


class Noms(unittest.TestCase):
    def test_caractere_special_bloque(self):
        camp = exemple()
        camp["campaigns"][0]["campaign_name"] = "velora/lancement"
        self.assertIn("caractères spéciaux", messages(camp, "BLOQUANT"))

    def test_accent_et_espace_en_attention(self):
        camp = exemple()
        camp["adgroups"][0]["adgroup_name"] = "trajet été"
        for a in camp["ads"]:
            if a["adgroup_name"] == "trajet_travail_sans_voiture":
                a["adgroup_name"] = "trajet été"
        self.assertIn("lettres accentuées", messages(camp, "ATTENTION"))

    def test_groupe_inconnu_dans_ads_bloque(self):
        camp = exemple()
        camp["ads"][0]["adgroup_name"] = "trajet_travail"
        self.assertIn("absent de l'onglet adgroups", messages(camp, "BLOQUANT"))

    def test_campagne_inconnue_dans_adgroups_bloque(self):
        camp = exemple()
        camp["adgroups"][0]["campaign_name"] = "velora_lancement"
        self.assertIn("absent de l'onglet campaigns", messages(camp, "BLOQUANT"))

    def test_groupe_en_double_bloque(self):
        camp = exemple()
        camp["adgroups"].append(copy.deepcopy(camp["adgroups"][0]))
        self.assertIn("en double", messages(camp, "BLOQUANT"))

    def test_ligne_d_exemple_bloque(self):
        camp = exemple()
        camp["campaigns"][0]["campaign_name"] = "oaitestcmp1234567"
        self.assertIn("ligne d'exemple", messages(camp, "BLOQUANT"))


class Campagne(unittest.TestCase):
    def test_budget_manquant_bloque(self):
        camp = exemple()
        del camp["campaigns"][0]["budget_max"]
        self.assertIn("budget_max manquant", messages(camp, "BLOQUANT"))

    def test_budget_total_en_attention(self):
        camp = exemple()
        camp["campaigns"][0]["budget_type"] = "Lifetime"
        self.assertIn("Lifetime", messages(camp, "ATTENTION"))

    def test_objectif_inconnu_bloque(self):
        camp = exemple()
        camp["campaigns"][0]["objective"] = "Reach"
        self.assertIn("Views, Clicks ou Conversions", messages(camp, "BLOQUANT"))

    def test_conversions_sans_identifiant_bloque(self):
        camp = exemple()
        camp["campaigns"][0]["objective"] = "Conversions"
        self.assertIn("exactement un conversion_event_setting_id", messages(camp, "BLOQUANT"))

    def test_conversions_avec_un_identifiant_passe(self):
        camp = exemple()
        camp["campaigns"][0]["objective"] = "Conversions"
        camp["campaigns"][0]["conversion_event_setting_ids"] = ["evt_123"]
        self.assertEqual(points(camp, "BLOQUANT"), [])

    def test_dates_inversees_bloquent(self):
        camp = exemple()
        camp["campaigns"][0]["end_date"] = "2026-11-01"
        self.assertIn("end_date avant launch_date", messages(camp, "BLOQUANT"))

    def test_lancement_passe_en_attention(self):
        camp = exemple()
        camp["campaigns"][0]["launch_date"] = "2026-10-01"
        self.assertIn("déjà passée", messages(camp, "ATTENTION"))

    def test_code_pays_uk_corrige(self):
        camp = exemple()
        camp["campaigns"][0]["target_countries"] = ["UK"]
        self.assertIn("le code ISO est GB", messages(camp, "BLOQUANT"))

    def test_pays_europeen_hors_liste_du_modele_accepte(self):
        camp = exemple()
        camp["campaigns"][0]["target_countries"] = ["FR", "BE", "LU"]
        self.assertEqual(points(camp, "BLOQUANT"), [])
        self.assertIn("vérifier dans Ads Manager", " ".join(p["conseil"] for p in points(camp, "INFO")))

    def test_pays_json_invalide_bloque(self):
        camp = exemple()
        camp["campaigns"][0]["target_countries"] = "[FR, BE]"
        self.assertIn("JSON invalide", messages(camp, "BLOQUANT"))

    def test_enchere_obligatoire_au_clic(self):
        camp = exemple()
        del camp["adgroups"][0]["max_bid"]
        self.assertIn("max_bid obligatoire pour une campagne Clicks", messages(camp, "BLOQUANT"))

    def test_enchere_superieure_au_budget(self):
        camp = exemple()
        camp["adgroups"][0]["max_bid"] = 200
        self.assertIn("supérieur au budget_max", messages(camp, "ATTENTION"))


class Hints(unittest.TestCase):
    def test_json_invalide_bloque(self):
        camp = exemple()
        camp["adgroups"][0]["context_hints"] = '["un", "deux"'
        self.assertIn("Context Hints : JSON invalide", messages(camp, "BLOQUANT"))

    def test_hint_vague_bloque(self):
        camp = exemple()
        camp["adgroups"][0]["context_hints"][0] = "logiciel"
        self.assertIn("hint vague", messages(camp, "BLOQUANT"))

    def test_hint_vague_en_deux_mots_bloque(self):
        camp = exemple()
        camp["adgroups"][0]["context_hints"][0] = "voyage pas cher"
        self.assertIn("hint vague", messages(camp, "BLOQUANT"))

    def test_hint_de_marque_seule_bloque(self):
        camp = exemple()
        camp["annonceur"]["concurrents"] = ["Rivalo"]
        camp["adgroups"][0]["context_hints"][0] = "Vélora Rivalo"
        self.assertIn("seulement de marques", messages(camp, "BLOQUANT"))

    def test_hint_court_en_attention(self):
        camp = exemple()
        camp["adgroups"][0]["context_hints"][0] = "vélo urbain"
        self.assertIn("hint très court", messages(camp, "ATTENTION"))

    def test_plus_de_5_hints_en_attention(self):
        camp = exemple()
        camp["adgroups"][0]["context_hints"] += ["rouler en ville sous la pluie", "garer un vélo au bureau",
                                                 "porter un casque pour aller travailler"]
        self.assertIn("6 context hints", messages(camp, "ATTENTION"))

    def test_4_hints_en_information(self):
        camp = exemple()
        camp["adgroups"][0]["context_hints"].append("garer son vélo électrique au bureau")
        self.assertIn("4 context hints", messages(camp, "INFO"))

    def test_variante_mineure_en_attention(self):
        camp = exemple()
        camp["adgroups"][0]["context_hints"][2] = "remplacer sa voiture pour ses trajets quotidiens"
        self.assertIn("presque identiques", messages(camp, "ATTENTION"))

    def test_chevauchement_entre_groupes(self):
        camp = exemple()
        camp["adgroups"][1]["context_hints"][0] = camp["adgroups"][0]["context_hints"][0]
        self.assertIn("chevauchement", messages(camp, "ATTENTION"))

    def test_sans_intention_en_attention(self):
        camp = exemple()
        camp["adgroups"][0]["intention"] = ""
        self.assertIn("intention utilisateur envisagée absente", messages(camp, "ATTENTION"))

    def test_moins_de_3_prompts_en_information(self):
        camp = exemple()
        camp["adgroups"][0]["prompts_test"] = ["un seul"]
        self.assertIn("1 prompt(s) simulé(s) sur 3", messages(camp, "INFO"))

    def test_moins_de_5_groupes_en_attention(self):
        camp = exemple()
        garde = {g["adgroup_name"] for g in camp["adgroups"][:4]}
        camp["adgroups"] = camp["adgroups"][:4]
        camp["ads"] = [a for a in camp["ads"] if a["adgroup_name"] in garde]
        self.assertIn("5 au moins", messages(camp, "ATTENTION"))


class Annonces(unittest.TestCase):
    def test_allegation_non_etayee_bloque(self):
        camp = exemple()
        camp["ads"][0]["copy"] = "Livraison sous 48 h partout en France."
        self.assertIn("allégation non étayée : « 48 h »", messages(camp, "BLOQUANT"))

    def test_superlatif_refuse_bloque(self):
        camp = exemple()
        camp["ads"][0]["copy"] = "Le vélo reconditionné le moins cher de France."
        self.assertIn("moins cher", messages(camp, "BLOQUANT"))

    def test_gratuit_non_etaye_bloque(self):
        camp = exemple()
        camp["ads"][0]["copy"] = "Livraison gratuite pour tout achat en ligne."
        self.assertIn("gratuite", messages(camp, "BLOQUANT"))

    def test_allegation_approuvee_passe(self):
        camp = exemple()
        camp["ads"][0]["copy"] = "Garantie 12 mois sur chaque vélo révisé."
        self.assertNotIn("allégation", messages(camp, "BLOQUANT"))

    def test_allegation_a_verifier_en_attention(self):
        camp = exemple()
        camp["allegations"].append({"texte": "Retour possible sous 30 jours", "source": "utilisateur", "statut": "à vérifier"})
        camp["ads"][0]["copy"] = "Retour possible sous 30 jours."
        self.assertIn("au statut à vérifier", messages(camp, "ATTENTION"))

    def test_champ_allegation_refusee_bloque(self):
        camp = exemple()
        camp["ads"][0]["allegation"] = "Le vélo électrique reconditionné le moins cher de France"
        self.assertIn("allégation refusée utilisée", messages(camp, "BLOQUANT"))

    def test_doublon_exact_bloque(self):
        camp = exemple()
        camp["ads"].append(copy.deepcopy(camp["ads"][0]))
        self.assertIn("annonce en double", messages(camp, "BLOQUANT"))

    def test_titre_et_copie_qui_se_repetent(self):
        camp = exemple()
        camp["ads"][0]["title"], camp["ads"][0]["copy"] = "Vélo électrique révisé", "Un vélo électrique révisé pour vous."
        self.assertIn("se répètent", messages(camp, "ATTENTION"))

    def test_titre_qui_commence_par_la_marque(self):
        camp = exemple()
        camp["ads"][0]["title"] = "Vélora, VAE révisés"
        self.assertIn("commence par la marque", messages(camp, "ATTENTION"))

    def test_tiret_cadratin_emoji_capitales(self):
        camp = exemple()
        camp["ads"][0]["copy"] = "Un VAE révisé — PROMO 🚲 pour vos trajets."
        m = messages(camp, "ATTENTION")
        self.assertIn("tiret cadratin", m)
        self.assertIn("emoji", m)
        self.assertIn("capitales", m)

    def test_espace_manquante_avant_ponctuation(self):
        camp = exemple()
        camp["ads"][0]["title"] = "Neuf ou reconditionné?"
        self.assertIn("pas d'espace avant", messages(camp, "INFO"))

    def test_lien_hors_domaine_bloque(self):
        camp = exemple()
        camp["ads"][0]["link"] = "https://www.autre-site.example/velos/"
        self.assertIn("hors des domaines approuvés", messages(camp, "BLOQUANT"))

    def test_lien_mal_forme_bloque(self):
        camp = exemple()
        camp["ads"][0]["link"] = "www.velora.example/velos"
        self.assertIn("link invalide", messages(camp, "BLOQUANT"))

    def test_lien_page_d_accueil_en_information(self):
        camp = exemple()
        camp["ads"][0]["link"] = "https://www.velora.example/"
        self.assertIn("page d'accueil", messages(camp, "INFO"))

    def test_image_vide_bloque(self):
        camp = exemple()
        camp["ads"][0]["image_link"] = ""
        self.assertIn("case vide : image_url", messages(camp, "ATTENTION"))

    def test_image_sans_extension_en_attention(self):
        camp = exemple()
        camp["ads"][0]["image_link"] = "https://cdn.velora.example/i/abc123"
        self.assertIn("sans extension", messages(camp, "ATTENTION"))


class Volume(unittest.TestCase):
    def test_moins_de_40_en_attention(self):
        camp = exemple()
        camp["ads"] = [a for i, a in enumerate(camp["ads"]) if i % 8 < 7]
        self.assertIn("35 annonce(s) : cible 40 à 50", messages(camp, "ATTENTION"))

    def test_grande_echelle_demande_100(self):
        self.assertIn("cible 100", messages(exemple(), "ATTENTION") or
                      " | ".join(p["message"] for p in points(exemple(), "ATTENTION", "grande-echelle")))

    def test_groupe_de_2_annonces(self):
        camp = exemple()
        g = camp["adgroups"][0]["adgroup_name"]
        n = 0
        garde = []
        for a in camp["ads"]:
            if a["adgroup_name"] == g:
                n += 1
                if n > 2:
                    continue
            garde.append(a)
        camp["ads"] = garde
        m = messages(camp, "ATTENTION")
        self.assertIn("2 annonce(s) dans le groupe", m)
        self.assertIn("répartition déséquilibrée", m)

    def test_reformulation_minimale(self):
        camp = exemple()
        camp["ads"][1]["title"] = camp["ads"][0]["title"] + "!"
        camp["ads"][1]["copy"] = camp["ads"][0]["copy"]
        self.assertIn("reformulation minimale", messages(camp, "ATTENTION"))


class _Export:
    """Mêmes contrôles d'export pour le modèle maison et pour un modèle à la manière d'Ads Manager."""
    MODELE_TEST = MODELE

    @classmethod
    def setUpClass(cls):
        cls.dossier = tempfile.TemporaryDirectory()
        cls.sortie = Path(cls.dossier.name) / "import.xlsx"
        cls.p = lancer("exporter", EXEMPLE, "-o", cls.sortie, "--modele", cls.MODELE_TEST, "--aujourdhui", "2026-10-15",
                       "--format", "trois-onglets")
        cls.z = zipfile.ZipFile(cls.sortie)
        cls.px = "x:" if "<x:worksheet" in cls.z.read("xl/worksheets/sheet1.xml").decode() else ""

    @classmethod
    def tearDownClass(cls):
        cls.z.close()
        cls.dossier.cleanup()

    def feuille(self, n):
        return self.z.read(f"xl/worksheets/sheet{n}.xml").decode("utf-8")

    def test_export_ecrit(self):
        self.assertEqual(self.p.returncode, 0, self.p.stdout + self.p.stderr)
        self.assertIn("Fichier écrit", self.p.stdout)

    def test_memes_fichiers_que_le_modele(self):
        with zipfile.ZipFile(self.MODELE_TEST) as m:
            self.assertEqual(sorted(m.namelist()), sorted(self.z.namelist()))
            for n in m.namelist():
                if "worksheets/sheet" not in n and not n.endswith(".rels"):
                    self.assertEqual(m.read(n), self.z.read(n), n)

    def test_en_tetes_et_controles_de_saisie_conserves(self):
        px = self.px
        with zipfile.ZipFile(self.MODELE_TEST) as m:
            for n in (1, 2, 3):
                avant = m.read(f"xl/worksheets/sheet{n}.xml").decode("utf-8")
                for num in (1, 2, 3):
                    self.assertEqual(ve._cellules_ligne(avant, num), ve._cellules_ligne(self.feuille(n), num))
                    ligne = re.search(rf'<{px}row r="{num}".*?</{px}row>', avant, re.S).group(0)
                    self.assertIn(ligne, self.feuille(n))
                dv = re.search(rf"<{px}dataValidations.*?</{px}dataValidations>", avant, re.S)
                if dv:
                    self.assertIn(dv.group(0), self.feuille(n))

    def test_ligne_d_exemple_retiree(self):
        for n in (1, 2, 3):
            self.assertNotIn("oaitest", self.feuille(n))

    def test_texte_normal_pas_d_italique(self):
        styles = self.z.read("xl/styles.xml").decode("utf-8")
        polices = re.findall(r"<(?:x:)?font>(.*?)</(?:x:)?font>", re.search(r"<(?:x:)?fonts[^>]*>(.*?)</(?:x:)?fonts>", styles, re.S).group(1), re.S)
        xfs = re.findall(r"<(?:x:)?xf [^>]*>", re.search(r"<(?:x:)?cellXfs[^>]*>(.*?)</(?:x:)?cellXfs>", styles, re.S).group(1))
        italiques = {str(i) for i, x in enumerate(xfs)
                     if re.search(r"<(?:x:)?i\s*/>", polices[int(re.search(r'fontId="(\d+)"', x).group(1))])}
        self.assertTrue(italiques, "les deux modèles de test contiennent un style italique")
        for n in (1, 2, 3):
            donnees = self.feuille(n).split(f'<{self.px}row r="4"', 1)[1]
            utilises = set(re.findall(r' s="(\d+)"', donnees))
            self.assertTrue(utilises)
            self.assertFalse(utilises & italiques, f"onglet {n} : styles italiques {utilises & italiques}")

    def test_dates_au_format_date(self):
        self.assertRegex(self.feuille(1), rf'<{self.px}c r="D4" s="\d+" t="n"><{self.px}v>46328</{self.px}v>')
        self.assertEqual(ve.lire_date(46328), date(2026, 11, 2))

    def test_json_compact_et_accents_lisibles(self):
        self.assertIn('["aller au travail à vélo sans arriver en sueur","', self.feuille(2))
        self.assertIn('["FR"]', self.feuille(1))

    def test_esperluettes_echappees(self):
        self.assertIn("utm_source=chatgpt&amp;utm_medium=ads", self.feuille(3))

    def test_liens_hypertexte_du_modele_retires(self):
        self.assertNotIn("hyperlink", self.feuille(3))
        if "xl/worksheets/_rels/sheet3.xml.rels" in self.z.namelist():
            self.assertNotIn("hyperlink", self.z.read("xl/worksheets/_rels/sheet3.xml.rels").decode("utf-8"))

    def test_aller_retour(self):
        relu = ve.lire_xlsx(self.sortie)
        ex = exemple()
        self.assertEqual([(a["adgroup_name"], a["title"], a["copy"], a["link"], a["image_link"]) for a in relu["ads"]],
                         [(a["adgroup_name"], a["title"], a["copy"], a["link"], a["image_link"]) for a in ex["ads"]])
        self.assertEqual(json.loads(relu["adgroups"][0]["context_hints_brut"]), ex["adgroups"][0]["context_hints"])
        self.assertEqual(relu["campaigns"][0]["budget_max"], 150.0)

    def test_fichier_exporte_revalide_avec_les_allegations(self):
        p = lancer("valider", self.sortie, "--allegations", EXEMPLE, "--modele", self.MODELE_TEST, "--aujourdhui", "2026-10-15")
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("PRÊT", p.stdout)

    def test_fichier_exporte_sans_liste_d_allegations(self):
        p = lancer("valider", self.sortie, "--modele", self.MODELE_TEST, "--aujourdhui", "2026-10-15")
        self.assertEqual(p.returncode, 2, p.stdout)
        self.assertIn("aucune liste d'allégations", p.stdout)

    def test_ouvert_par_openpyxl_si_disponible(self):
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl absent")
        wb = openpyxl.load_workbook(self.sortie)
        self.assertEqual(wb.sheetnames, ["campaigns", "adgroups", "ads"])
        ws = wb["ads"]
        self.assertEqual(ws.max_row, 3 + len(exemple()["ads"]))
        self.assertFalse(ws.cell(4, 2).font.i)
        self.assertEqual(wb["campaigns"].cell(4, 4).value.date(), date(2026, 11, 2))


class ExportModeleMaison(_Export, unittest.TestCase):
    MODELE_TEST = MODELE


class ExportModeleAdsManager(_Export, unittest.TestCase):
    MODELE_TEST = MODELE_AM


class Politiques(unittest.TestCase):
    """Règles publicitaires d'OpenAI (Ad Policies v1.6, sept. 2026) et docs développeur."""

    def test_categorie_autorisee_sans_remarque(self):
        self.assertNotIn("catégorie", messages(exemple(), "INFO") + messages(exemple(), "ATTENTION"))

    def test_categorie_non_declaree_en_information(self):
        camp = exemple()
        del camp["annonceur"]["categorie"]
        self.assertIn("catégorie de l'annonceur non déclarée", messages(camp, "INFO"))

    def test_categorie_interdite_alerte_sans_bloquer(self):
        camp = exemple()
        camp["annonceur"]["categorie"] = "alcool"
        self.assertIn("ALERTE : catégorie « alcool » interdite par les règles publicitaires", messages(camp, "ATTENTION"))
        self.assertNotIn("catégorie", messages(camp, "BLOQUANT"))

    def test_categorie_reservee_aux_etats_unis_alerte_en_france(self):
        camp = exemple()
        camp["annonceur"]["categorie"] = "assurance"
        self.assertIn("généralement interdite hors des États-Unis (FR)", messages(camp, "ATTENTION"))
        self.assertNotIn("catégorie", messages(camp, "BLOQUANT"))

    def test_categorie_reservee_aux_etats_unis_au_cas_par_cas(self):
        camp = exemple()
        camp["annonceur"]["categorie"] = "sante"
        camp["campaigns"][0]["target_countries"] = ["US"]
        self.assertEqual(points(camp, "BLOQUANT"), [])
        self.assertIn("approbation au cas par cas", messages(camp, "ATTENTION"))

    def test_categorie_inconnue(self):
        camp = exemple()
        camp["annonceur"]["categorie"] = "astrologie"
        self.assertIn("inconnue du pack", messages(camp, "ATTENTION"))

    def test_signal_de_categorie_dans_une_annonce(self):
        camp = exemple()
        camp["ads"][0]["copy"] = "Un vin offert pour tout vélo acheté en ligne."
        self.assertIn("« vin » : signal de la catégorie alcool", messages(camp, "ATTENTION"))

    def test_pret_a_rouler_n_est_pas_un_credit(self):
        self.assertNotIn("finance", messages(exemple(), "ATTENTION"))
        camp = exemple()
        camp["ads"][0]["copy"] = "Un prêt personnel pour financer votre vélo."
        self.assertIn("catégorie finance", messages(camp, "ATTENTION"))

    def test_imitation_de_chatgpt(self):
        camp = exemple()
        camp["ads"][0]["title"] = "ChatGPT vous conseille"
        self.assertIn("mention de ChatGPT ou d'OpenAI", messages(camp, "ATTENTION"))

    def test_hint_geographique(self):
        camp = exemple()
        camp["adgroups"][0]["context_hints"][0] = "aller au bureau à vélo à Lyon"
        self.assertIn("hint géographique", messages(camp, "ATTENTION"))

    def test_nom_trop_court(self):
        camp = exemple()
        camp["campaigns"][0]["campaign_name"] = "v1"
        for g in camp["adgroups"]:
            g["campaign_name"] = "v1"
        self.assertIn("de 3 à 1 000 attendus", messages(camp, "BLOQUANT"))

    def test_lien_trop_long(self):
        camp = exemple()
        camp["ads"][0]["link"] = "https://www.velora.example/?q=" + "a" * 2050
        self.assertIn("2 048 au plus", messages(camp, "BLOQUANT"))

    def test_image_webp(self):
        camp = exemple()
        camp["ads"][0]["image_link"] = "https://www.velora.example/images/ville.webp"
        self.assertIn("WebP", messages(camp, "ATTENTION"))

    def test_enchere_hors_recommandation_en_information(self):
        self.assertNotIn("max_bid au clic", messages(exemple(), "INFO"))
        camp = exemple()
        camp["adgroups"][0]["max_bid"] = 1.2
        self.assertIn("max_bid au clic hors de 3 à 5 : trajet_travail_sans_voiture (1.2)", messages(camp, "INFO"))


class LeconsDeLEval(unittest.TestCase):
    """Défauts relevés par le juge de l'éval à l'aveugle du 15 oct. 2026."""

    def test_titre_repris_dans_deux_groupes(self):
        camp = exemple()
        autre = next(a for a in camp["ads"] if a["adgroup_name"] != camp["ads"][0]["adgroup_name"])
        autre["title"] = camp["ads"][0]["title"]
        self.assertIn(f"titre repris dans 2 groupes : « {camp['ads'][0]['title']} »", messages(camp, "ATTENTION"))

    def test_trop_d_annonces_pour_le_budget(self):
        camp = exemple()
        camp["campaigns"][0]["budget_max"] = 30
        self.assertIn("40 annonces pour 10 clics par jour au plus", messages(camp, "ATTENTION"))

    def test_volume_adapte_au_budget_sans_remarque(self):
        self.assertNotIn("clics par jour", messages(exemple(), "ATTENTION"))


class Fautive(unittest.TestCase):
    """La campagne fautive des fixtures (aussi capturée dans le README)."""
    FIX = Path(__file__).resolve().parent / "fixtures" / "campagne-a-corriger.json"

    def test_erreurs_attendues(self):
        camp = json.loads(self.FIX.read_text(encoding="utf-8"))
        b = messages(camp, "BLOQUANT")
        for attendu in ("le code ISO est GB", "« plantea-noël » absent de l'onglet campaigns", "title de 35 caractères",
                        "allégation non étayée : « n°1 »", "« gratuite »",
                        "« offrir_plante » absent de l'onglet adgroups", "« 24 h »"):
            self.assertIn(attendu, b)
        self.assertNotIn("allégation « 1 »", b)
        self.assertIn("hint très court : « plantes »", messages(camp, "ATTENTION"))

    def test_export_refuse(self):
        with tempfile.TemporaryDirectory() as d:
            p = lancer("exporter", self.FIX, "-o", Path(d) / "o.xlsx", "--aujourdhui", "2026-10-15")
            self.assertEqual(p.returncode, 3)


class Refus(unittest.TestCase):
    def test_export_refuse_si_bloquant(self):
        camp = exemple()
        camp["ads"][0]["title"] = "x" * 30
        with tempfile.TemporaryDirectory() as d:
            src, out = Path(d) / "c.json", Path(d) / "o.xlsx"
            src.write_text(json.dumps(camp, ensure_ascii=False), encoding="utf-8")
            p = lancer("exporter", src, "-o", out, "--aujourdhui", "2026-10-15")
            self.assertEqual(p.returncode, 3)
            self.assertIn("Fichier non écrit", p.stdout)
            self.assertFalse(out.exists())

    def test_modele_brut_bloque_a_cause_de_l_exemple(self):
        p = lancer("valider", MODELE_AM, "--modele", MODELE_AM, "--aujourdhui", "2026-10-15")
        self.assertEqual(p.returncode, 3)
        self.assertIn("ligne d'exemple du modèle encore présente", p.stdout)

    def test_modele_sans_prefixe_xml(self):
        """Une future version du modèle sans préfixe x: s'exporte aussi."""
        with tempfile.TemporaryDirectory() as d:
            sans = Path(d) / "sans.xlsx"
            with zipfile.ZipFile(MODELE_AM) as z, zipfile.ZipFile(sans, "w") as w:
                for n in z.namelist():
                    c = z.read(n)
                    if n.startswith("xl/worksheets/sheet") or n == "xl/workbook.xml":
                        t = c.decode("utf-8")
                        t = re.sub(r"<(/?)x:", r"<\1", t).replace("xmlns:x=", "xmlns=")
                        c = t.encode("utf-8")
                    w.writestr(n, c)
            self.assertEqual(ve.lire_modele(sans)["limites"], {"title": 24, "copy": 48})
            out = Path(d) / "o.xlsx"
            ve.exporter(exemple(), sans, out)
            relu = ve.lire_xlsx(out)
            self.assertEqual(len(relu["ads"]), 40)
            self.assertNotIn("oaitest", zipfile.ZipFile(out).read("xl/worksheets/sheet3.xml").decode())


class Commandes(unittest.TestCase):
    def test_help(self):
        self.assertEqual(lancer("--help").returncode, 0)

    def test_valider_json(self):
        p = lancer("valider", EXEMPLE, "--json", "--aujourdhui", "2026-10-15")
        d = json.loads(p.stdout)
        self.assertEqual(d["verdict"], 0)
        self.assertEqual(d["resume"]["annonces"], 40)

    def test_tableaux(self):
        p = lancer("tableaux", EXEMPLE, "--aujourdhui", "2026-10-15")
        self.assertEqual(p.returncode, 0)
        for o in ("### campaigns", "### adgroups", "### ads"):
            self.assertIn(o, p.stdout)
        self.assertIn("velora_lancement_fr\t150\tDaily\t2026-11-02", p.stdout)

    def test_relecture(self):
        p = lancer("relecture", EXEMPLE, "--aujourdhui", "2026-10-15")
        self.assertIn("| Neuf ou reconditionné ? | 23 |", p.stdout)
        self.assertIn("Idée de visuel", p.stdout)

    def test_fichier_absent(self):
        p = lancer("valider", "nexistepas.json")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("introuvable", p.stdout + p.stderr)


class ExportSchema(unittest.TestCase):
    """Format de sortie v2 : le schéma d'annonces (un onglet, 10 colonnes) et la fiche de paramétrage."""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(SKILL / "commun"))
        import classeur
        cls.cl = classeur
        cls.tmp = tempfile.TemporaryDirectory()
        d = Path(cls.tmp.name)
        camp = exemple()
        camp["adgroups"][0]["ad_group_id"] = "adgrp_501"
        cls.src = d / "c.json"
        cls.src.write_text(json.dumps(camp, ensure_ascii=False), encoding="utf-8")
        cls.sortie = d / "import.xlsx"
        cls.p = lancer("exporter", cls.src, "-o", cls.sortie, "--aujourdhui", "2026-10-15")
        _, cls.lignes = classeur.annonces(classeur.lire(cls.sortie))
        cls.fiche = (d / "import-parametrage.md").read_text(encoding="utf-8")
        cls.camp = camp

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_ecrit(self):
        self.assertIn(self.p.returncode, (0, 2), self.p.stdout)
        self.assertIn("Fichier d'import écrit", self.p.stdout)

    def test_format_schema(self):
        cl = self.cl
        r, classeur, _ = cl.verifier(self.sortie)
        self.assertEqual([o["nom"] for o in classeur["onglets"]], [cl.ONGLET])
        self.assertEqual(r.compte(cl.BLOQUANT), 0, r.texte())
        self.assertEqual(len(self.lignes), len(self.camp["ads"]))

    def test_identifiant_de_groupe_repris(self):
        g = self.camp["adgroups"][0]["adgroup_name"]
        self.assertTrue(all(x["ad_group_id"] == "adgrp_501" for x in self.lignes if x["adgroup_name"] == g))
        self.assertIn("ad_group_id à compléter pour 4 groupe(s)", self.p.stdout)

    def test_valeurs_par_defaut(self):
        self.assertTrue(all(x["status"] == "active" for x in self.lignes))
        self.assertTrue(all(x.get("image_file_id", "") == "" for x in self.lignes))
        self.assertEqual(self.lignes[0]["ad_name"], self.lignes[0]["adgroup_name"] + "-01")
        self.assertEqual(self.lignes[0]["image_url"], self.camp["ads"][0]["image_link"])

    def test_fiche(self):
        self.assertIn("# Paramétrage dans Ads Manager", self.fiche)
        self.assertIn("| Pays | FR |", self.fiche)
        hints = self.camp["adgroups"][0]["context_hints"]
        self.assertIn(json.dumps(hints, ensure_ascii=False), self.fiche)
        self.assertIn("adgrp_501", self.fiche)

    def test_image_file_id_accepte(self):
        camp = exemple()
        for a in camp["ads"]:
            a.pop("image_link")
            a["image_file_id"] = "file_42"
        self.assertNotIn("image", messages(camp, "BLOQUANT"))

    def test_csv_par_defaut_et_cases_vides(self):
        camp = exemple()
        camp["ads"][0]["image_link"] = ""
        camp["ads"][1]["link"] = ""
        with tempfile.TemporaryDirectory() as d:
            src, out = Path(d) / "c.json", Path(d) / "import.csv"
            src.write_text(json.dumps(camp, ensure_ascii=False), encoding="utf-8")
            p = lancer("exporter", src, "-o", out, "--aujourdhui", "2026-10-15")
            self.assertTrue(out.exists(), p.stdout)
            self.assertTrue(out.read_text(encoding="utf-8").startswith("ad_id,ad_group_id,adgroup_name"))
        self.assertIn("Cases vides à vérifier, image_url : ligne(s) 2", p.stdout)
        self.assertIn("Cases vides à vérifier, link : ligne(s) 3", p.stdout)

    def test_bloquant_de_format_refuse(self):
        camp = exemple()
        camp["ads"][0]["status"] = "en pause"
        with tempfile.TemporaryDirectory() as d:
            src, out = Path(d) / "c.json", Path(d) / "o.xlsx"
            src.write_text(json.dumps(camp, ensure_ascii=False), encoding="utf-8")
            p = lancer("exporter", src, "-o", out, "--aujourdhui", "2026-10-15")
            self.assertEqual(p.returncode, 3)
            self.assertFalse(out.exists())
            self.assertIn("status « en pause »", p.stdout)


class DroitFrancais(unittest.TestCase):
    def test_allegation_verte(self):
        camp = exemple()
        camp["ads"][0]["copy"] = "Un vélo écologique pour la ville."
        self.assertIn("allégation environnementale", messages(camp, "ATTENTION"))

    def test_credit(self):
        camp = exemple()
        camp["ads"][0]["copy"] = "Payez en 3 fois avec notre crédit."
        self.assertIn("L312-5", messages(camp, "ATTENTION"))

    def test_credit_d_impot_ignore(self):
        camp = exemple()
        camp["ads"][0]["copy"] = "Éligible au crédit d'impôt."
        self.assertNotIn("L312-5", messages(camp, "ATTENTION"))

    def test_pays_vide(self):
        camp = exemple()
        camp["campaigns"][0]["target_countries"] = ""
        self.assertIn("aucun pays ciblé", messages(camp, "ATTENTION"))


if __name__ == "__main__":
    unittest.main()
