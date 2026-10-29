#!/usr/bin/env python3
"""Tests des scripts de /tone-of-voice : python3 -m unittest (ou evals/tout_tester.py)."""
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
SCRIPTS = PACK / "skills" / "tone-of-voice" / "scripts"
EXEMPLE = PACK / "skills" / "tone-of-voice" / "exemples" / "assurly"
FIX = PACK / "evals" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

import ecart  # noqa: E402
import profil  # noqa: E402
import texte as tx  # noqa: E402
import voix  # noqa: E402

TEXTES = sorted((FIX / "assurly").glob("*.txt"))


def lancer(script, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], capture_output=True, text=True)


def corpus(*chemins):
    return voix.analyser(voix.lire_textes([str(c) for c in chemins]))


class Texte(unittest.TestCase):
    def test_phrases_et_paragraphes(self):
        t = "Mardi, 7 h 40. Un client appelle.\n\nOn décroche ! Et après ?\nLa suite."
        self.assertEqual(len(tx.phrases(t)), 5)
        self.assertEqual(len(tx.paragraphes(t)), 2)

    def test_mesure_sans_objet_vaut_none(self):
        m = tx.mesurer("Une phrase. Deux phrases.")
        self.assertIsNone(m["phrase_ecart_type"])          # moins de 4 phrases
        self.assertIsNone(m["part_paragraphes_une_phrase"])  # moins de 3 paragraphes

    def test_adresse(self):
        self.assertEqual(tx.adresse(3, 0), "tutoiement")
        self.assertEqual(tx.adresse(0, 2), "vouvoiement")
        self.assertEqual(tx.adresse(2, 2), "mixte")
        self.assertEqual(tx.adresse(0, 0), "aucune")
        m = tx.mesurer("Tu sais, t'as raison. Ton équipe et toi.")
        self.assertEqual(tx.adresse(m["tu"], m["vous"]), "tutoiement")

    def test_negation_sans_ne(self):
        self.assertEqual(tx.negations_sans_ne("C'est pas encore assez bien."), 1)
        self.assertEqual(tx.negations_sans_ne("Ce n'est pas assez bien."), 0)
        self.assertEqual(tx.negations_sans_ne("Pas mal du tout."), 0)

    def test_classe_ponctuation(self):
        self.assertEqual(tx.classe(0), "jamais")
        self.assertEqual(tx.classe(0.1), "rare")
        self.assertEqual(tx.classe(0.15), "habituelle")
        self.assertIsNone(tx.classe(None))

    def test_liens_et_emails_ignores(self):
        m = tx.mesurer("Écris à camille@assurly.example ou va sur https://assurly.example/contact : merci.")
        self.assertEqual(m["liens"], 1)
        self.assertEqual(m["ponctuation"]["deux_points"], 1)

    def test_emojis_et_hashtags(self):
        m = tx.mesurer("Bravo l'équipe 🎉🚀 #assurance #artisans")
        self.assertEqual(m["emojis"], 2)
        self.assertEqual(m["hashtags"], 2)

    def test_marques_ia(self):
        ids = {x["id"] for x in tx.marques_ia((FIX / "assurly-ia.txt").read_text(encoding="utf-8"))}
        self.assertTrue({"ouverture-creuse", "ce-n-est-pas-c-est", "revelation", "fuite-assistant"} <= ids, ids)
        self.assertEqual(tx.marques_ia((FIX / "assurly" / "04-post-erreur.txt").read_text(encoding="utf-8")), [])

    def test_bloc_aller_retour(self):
        b = tx.ecrire_bloc({"version_mesures": 1, "phrase_mediane": 8.0, "adresse": "tutoiement", "vide": None})
        self.assertEqual(tx.lire_bloc(b), {"version_mesures": 1, "phrase_mediane": 8.0,
                                           "adresse": "tutoiement", "vide": None})
        self.assertIsNone(tx.lire_bloc("pas de bloc"))


class Voix(unittest.TestCase):
    def test_corpus_assurly(self):
        r = corpus(*TEXTES)
        self.assertEqual(r["textes"], 5)
        self.assertEqual(r["adresse"], "vouvoiement")
        self.assertEqual(r["ca_cela"], "ça")
        self.assertEqual(r["confiance"], "faible")
        self.assertEqual(r["ponctuation"]["exclamation"]["classe"], "jamais")
        self.assertEqual(r["ponctuation"]["emojis"]["classe"], "jamais")
        self.assertEqual(r["textes_ia_probables"], [])
        self.assertEqual(r["textes_a_part"], [])

    def test_regles_justifiees_seulement_par_le_corpus(self):
        r = corpus(*TEXTES)
        regles = " ".join(r["regles_justifiees"])
        self.assertIn("Jamais d’émojis", regles)
        self.assertIn("Vouvoiement (5 textes sur 5)", regles)
        self.assertNotIn("question", regles.lower().split("jamais")[0])  # questions rares, pas « jamais »

    def test_alerte_texte_ia(self):
        r = corpus(*TEXTES, FIX / "assurly-ia.txt")
        self.assertEqual([x["texte"] for x in r["textes_ia_probables"]], ["assurly-ia.txt"])
        self.assertTrue(any("assurly-ia.txt" in a and "IA" in a for a in r["alertes"]))

    def test_alerte_autre_auteur(self):
        r = corpus(*TEXTES, FIX / "assurly-autre-auteur.txt")
        a_part = {x["texte"]: x for x in r["textes_a_part"]}
        self.assertIn("assurly-autre-auteur.txt", a_part)
        self.assertEqual(a_part["assurly-autre-auteur.txt"]["niveau"], "à part")

    def test_presque_identiques(self):
        with tempfile.TemporaryDirectory() as d:
            t = (FIX / "assurly" / "02-post-chiffres.txt").read_text(encoding="utf-8")
            Path(d, "copie.txt").write_text(t.replace("novembre", "décembre"), encoding="utf-8")
            r = corpus(*TEXTES, Path(d, "copie.txt"))
        self.assertTrue(r["presque_identiques"])

    def test_fichier_unique_separe_par_tirets(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "corpus.md")
            p.write_text("\n---\n".join(t.read_text(encoding="utf-8") for t in TEXTES), encoding="utf-8")
            self.assertEqual(len(voix.lire_textes([str(p)])), 5)

    def test_confiance(self):
        self.assertEqual(voix.niveau_confiance(300, 5), "faible")
        self.assertEqual(voix.niveau_confiance(900, 5), "moyenne")
        self.assertEqual(voix.niveau_confiance(3000, 8), "bonne")
        self.assertEqual(voix.niveau_confiance(3000, 2), "moyenne")
        self.assertEqual(voix.niveau_confiance(3000, 1), "faible")

    def test_cli(self):
        p = lancer("voix.py", *TEXTES)
        self.assertEqual(p.returncode, 2)  # alerte : corpus court
        self.assertIn("RÈGLES JUSTIFIÉES", p.stdout)
        p = lancer("voix.py", *TEXTES, "--json")
        self.assertEqual(json.loads(p.stdout)["textes"], 5)
        p = lancer("voix.py", *TEXTES, "--bloc", "--date", "2026-10-27")
        self.assertEqual(tx.lire_bloc(p.stdout)["date"], "2026-10-27")
        with tempfile.TemporaryDirectory() as d:
            Path(d, "vide.txt").write_text("   \n", encoding="utf-8")
            self.assertEqual(lancer("voix.py", Path(d, "vide.txt")).returncode, 1)
        self.assertEqual(lancer("voix.py", "/inexistant.txt").returncode, 1)

    def test_bloc_de_l_exemple_a_jour(self):
        """Le bloc de l'exemple Assurly est celui que voix.py produit sur ses textes."""
        p = lancer("voix.py", *sorted((EXEMPLE / "textes").glob("*.txt")), "--bloc", "--date", "2026-10-27")
        attendu = tx.lire_bloc(p.stdout)
        self.assertEqual(tx.lire_bloc((EXEMPLE / "tone-of-voice.md").read_text(encoding="utf-8")), attendu)


class Ecart(unittest.TestCase):
    PROFIL = (EXEMPLE / "tone-of-voice.md").read_text(encoding="utf-8")

    def test_interdits_lus_dans_la_section_jamais(self):
        self.assertEqual(ecart.interdits(self.PROFIL)[:3], ["n'hésitez pas", "solution", "au cœur de"])
        self.assertEqual(ecart.interdits("## 5. Mes mots\n- « dossier »\n"), [])

    def test_texte_hors_voix(self):
        b = ("Dans un monde où tout change, nous plaçons nos clients au cœur de notre démarche — "
             "et ce n'est pas qu'une promesse, c'est un engagement !\n\nN'hésitez pas à nous écrire 🚀")
        r = ecart.comparer(self.PROFIL, b)
        self.assertEqual(r["verdict"], "HORS VOIX")
        textes = " ".join(e["ecart"] for e in r["ecarts"])
        for attendu in ("cadratin", "« n'hésitez pas »", "« au cœur de »", "émoji", "point d'exclamation",
                        "ouverture-creuse", "ce-n-est-pas-c-est"):
            self.assertIn(attendu, textes)

    def test_texte_dans_la_voix(self):
        b = ("Jeudi, 16 h 20. Une boulangère nous appelle : son four a lâché, la livraison du soir est compromise.\n\n"
             "On a ouvert le dossier pendant l'appel. L'expert est passé le lendemain matin.\n\n"
             "Ce genre de journée, on en a deux ou trois par mois. On ne fait rien d'héroïque. "
             "On décroche, et on tient les délais qu'on a annoncés.\n\n"
             "Vous êtes commerçant et votre assureur vous fait attendre ? On en parle.")
        r = ecart.comparer(self.PROFIL, b)
        self.assertEqual(r["verdict"], "DANS LA VOIX", r["ecarts"])

    def test_adresse_et_reglage_de_canal(self):
        b = "Tu sais quoi ? Ton dossier est complet. Je te rappelle demain à 9 h. Tu peux dormir tranquille."
        r = ecart.comparer(self.PROFIL, b)
        self.assertTrue(any("tutoiement" in e["ecart"] and e["gravite"] == "fort" for e in r["ecarts"]))
        r = ecart.comparer(self.PROFIL, b, adresse_canal="tutoiement")
        self.assertFalse(any("tutoiement" in e["ecart"] for e in r["ecarts"]))

    def test_vous_signale_ambigu(self):
        b = "Vous avez été nombreux à répondre. Merci à vous. On lit tout. On répond à chacun."
        r = ecart.comparer(self.PROFIL.replace("adresse: vouvoiement", "adresse: tutoiement"), b)
        piste = [e["piste"] for e in r["ecarts"] if "vouvoiement" in e["ecart"]][0]
        self.assertIn("plusieurs personnes", piste)

    def test_phrases_trop_longues(self):
        b = ". ".join(["Nous avons longuement étudié l'ensemble des dossiers transmis par nos clients artisans "
                       "au cours des derniers mois afin d'en tirer des enseignements utiles"] * 5) + "."
        r = ecart.comparer(self.PROFIL, b)
        self.assertTrue(any("médiane" in e["ecart"] for e in r["ecarts"]))

    def test_cela_contre_ca(self):
        r = ecart.comparer(self.PROFIL, "Cela marche. On le voit. On le mesure. Cela tient.")
        self.assertTrue(any("« cela »" in e["ecart"] for e in r["ecarts"]))

    def test_sans_bloc(self):
        with self.assertRaises(ValueError):
            ecart.comparer("# Voix de X\n", "Un texte.")

    def test_cli_codes(self):
        with tempfile.TemporaryDirectory() as d:
            bon = Path(d, "bon.txt")
            bon.write_text("On a ouvert le dossier. L'expert passe jeudi. On vous rappelle avant.", encoding="utf-8")
            mauvais = Path(d, "mauvais.txt")
            mauvais.write_text("Dans un monde où tout va vite — n'hésitez pas ! 🚀 Au cœur de tout.", encoding="utf-8")
            self.assertEqual(lancer("ecart.py", EXEMPLE / "tone-of-voice.md", bon).returncode, 0)
            self.assertEqual(lancer("ecart.py", EXEMPLE / "tone-of-voice.md", mauvais).returncode, 3)
            p = lancer("ecart.py", EXEMPLE / "tone-of-voice.md", mauvais, "--json")
            self.assertEqual(json.loads(p.stdout)["verdict"], "HORS VOIX")
            self.assertEqual(lancer("ecart.py", Path(d, "absent.md"), bon).returncode, 1)


class Profil(unittest.TestCase):
    def test_exemple_complet(self):
        r = profil.verifier((EXEMPLE / "tone-of-voice.md").read_text(encoding="utf-8"), dt.date(2026, 10, 27))
        self.assertEqual(r["erreurs"], [])
        self.assertEqual(r["attention"], ["confiance faible : redemander des textes écrits à la main"])

    def test_modele_vide_signale(self):
        md = (PACK / "skills" / "tone-of-voice" / "modeles" / "tone-of-voice.md").read_text(encoding="utf-8")
        r = profil.verifier(md, dt.date(2026, 10, 27))
        self.assertEqual(r["verdict"], "À REVOIR")
        self.assertTrue(any("trou" in a for a in r["attention"]))
        self.assertTrue(any("trait" in a for a in r["attention"]))

    def test_peremption_et_typo(self):
        md = (EXEMPLE / "tone-of-voice.md").read_text(encoding="utf-8")
        r = profil.verifier(md, dt.date(2027, 6, 1))
        self.assertTrue(any("jours" in a for a in r["attention"]))
        r = profil.verifier(md.replace("Concrète", "Concrète — vraiment").replace("40%", "40 %"), dt.date(2026, 10, 27))
        self.assertTrue(any("cadratin" in e for e in r["erreurs"]))
        self.assertTrue(any("15%" in a for a in r["attention"]))

    def test_section_manquante(self):
        md = (EXEMPLE / "tone-of-voice.md").read_text(encoding="utf-8")
        md = re.sub(r"## 6\. Ce que je n'écris jamais.*?## 7\.", "## 7.", md, flags=re.S)
        r = profil.verifier(md, dt.date(2026, 10, 27))
        self.assertTrue(any("section 6" in e for e in r["erreurs"]))

    def test_fichier_vide(self):
        self.assertEqual(profil.verifier("", dt.date(2026, 10, 27))["verdict"], "VIDE")

    def test_nom_skill(self):
        self.assertEqual(profil.nom_skill("Anna Lou"), "ma-voix-anna-lou")
        self.assertEqual(profil.nom_skill("Élodie & Co."), "ma-voix-elodie-co")
        self.assertLessEqual(len(profil.nom_skill("x" * 100)), 64)
        with self.assertRaises(ValueError):
            profil.nom_skill("!!!")

    def test_anonymiser(self):
        t, n = profil.anonymiser("Bonjour Monsieur Garnier, écrivez à g.garnier@exemple.fr ou au 06 12 34 56 78.")
        self.assertEqual(n, 3)
        self.assertIn("Monsieur X", t)
        self.assertNotIn("06 12", t)

    def test_ma_voix(self):
        with tempfile.TemporaryDirectory() as d:
            r = profil.construire(str(EXEMPLE / "tone-of-voice.md"), "Camille",
                                  [str(p) for p in sorted((EXEMPLE / "textes").glob("*.txt"))], d, True)
            racine = Path(d, "ma-voix-camille")
            skill = (racine / "SKILL.md").read_text(encoding="utf-8")
            m = re.match(r'---\nname: (.+)\ndescription: "(.*)"\n', skill)
            self.assertEqual(m.group(1), racine.name)
            self.assertLessEqual(len(m.group(2)), 1024)
            self.assertIn("Ne l'utilise pas", m.group(2))
            self.assertIn("« n'hésitez pas »", skill)          # les « jamais » sont recopiés
            self.assertEqual(r["exemples"], 5)
            self.assertNotIn("Garnier", (racine / "references" / "tone-of-voice.md").read_text(encoding="utf-8"))
            self.assertNotIn("Garnier", (racine / "exemples" / "exemple-03.md").read_text(encoding="utf-8"))
            with zipfile.ZipFile(r["zip"]) as z:
                noms = z.namelist()
            self.assertEqual(sum(n.endswith("SKILL.md") for n in noms), 1)
            self.assertTrue(all(n.startswith("ma-voix-camille/") for n in noms))
            # le Skill généré embarque un ecart.py qui marche
            p = subprocess.run([sys.executable, str(racine / "scripts" / "ecart.py"),
                                str(racine / "references" / "tone-of-voice.md"), str(FIX / "assurly-ia.txt")],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 3, p.stdout + p.stderr)

    def test_ma_voix_sans_exemples_alerte(self):
        with tempfile.TemporaryDirectory() as d:
            p = lancer("profil.py", "ma-voix", EXEMPLE / "tone-of-voice.md", "--nom", "Camille", "--sortie", d)
            self.assertEqual(p.returncode, 2)
            self.assertIn("moins de 3 exemples", p.stdout)

    def test_cli_verifier(self):
        p = lancer("profil.py", "verifier", EXEMPLE / "tone-of-voice.md", "--aujourdhui", "2026-10-27")
        self.assertEqual(p.returncode, 2)
        self.assertEqual(lancer("profil.py", "verifier", "/inexistant.md").returncode, 1)


if __name__ == "__main__":
    unittest.main()
