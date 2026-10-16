#!/usr/bin/env python3
"""Tests de video.py : python3 -m unittest discover evals/seo-social"""
import importlib.util
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("video", ICI.parents[1] / "skills" / "seo-social" / "scripts" / "video.py")
vd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vd)
OK = (ICI / "description-ok.txt").read_text(encoding="utf-8")
KO = (ICI / "description-ko.txt").read_text(encoding="utf-8")
SRT = (ICI / "sous-titres.srt").read_text(encoding="utf-8")


def constats(r):
    return " | ".join(c["constat"] for c in r["constats"])


class Chapitres(unittest.TestCase):
    def test_description_conforme(self):
        r = vd.controler(OK, "Mutuelle indépendant : comment bien la choisir ?", "mutuelle indépendant", "12:40", SRT)
        self.assertEqual(r["verdict"], "PRÊT")
        self.assertEqual(len(r["chapitres"]), 5)

    def test_regles_youtube(self):
        r = vd.controler(KO, "", "", "3:05", None)
        t = constats(r)
        self.assertIn("pas 00:00", t)
        self.assertIn("5 s, moins de 10 s", t)
        self.assertIn("dernier chapitre", t)
        self.assertEqual(r["verdict"], "À CORRIGER")

    def test_trois_codes_au_moins_et_ordre(self):
        r = vd.controler("00:00 Début\n02:00 Fin\n", "", "", None, None)
        self.assertIn("il en faut au moins 3", constats(r))
        r = vd.controler("00:00 A\n03:00 B\n02:00 C\n", "", "", None, None)
        self.assertIn("ordre chronologique", constats(r))

    def test_heures(self):
        self.assertEqual(vd.secondes("1:02:03"), 3723)

    def test_mot_cle_et_transcription(self):
        r = vd.controler(OK, "Notre vidéo", "mutuelle indépendant", "12:40", None)
        t = constats(r)
        self.assertIn("absent du titre", t)
        self.assertIn("transcription non fournie", t)
        r = vd.controler(OK, "Mutuelle indépendant", "prévoyance artisan", "12:40", SRT)
        self.assertIn("jamais prononcé", constats(r))


if __name__ == "__main__":
    unittest.main()
