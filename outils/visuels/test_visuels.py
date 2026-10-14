#!/usr/bin/env python3
"""Tests des générateurs de visuels : python3 -m unittest outils/visuels/test_visuels.py"""
import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import capture as cap  # noqa: E402
import visuels as vis  # noqa: E402

RACINE = ICI.parents[1]
SVG = "{http://www.w3.org/2000/svg}"


def textes(svg):
    racine = ET.fromstring(svg)
    return ["".join(t.itertext()) for t in racine.iter(f"{SVG}text")]


class Capture(unittest.TestCase):
    def test_svg_valide_et_texte_exact(self):
        sortie = "PLAN  BLOQUÉ  ·  3 posts\n  ✖ pas deux fois <la même> formule & co\n  ! angle « l'IA »"
        s = cap.svg(sortie, "titre « test »", "python3 x.py --exemple")
        lignes = textes(s)
        self.assertEqual(lignes[0], "titre « test »")
        self.assertEqual(lignes[1], "$ python3 x.py --exemple")
        self.assertEqual(lignes[2:], sortie.splitlines(), "le texte affiché doit être la sortie exacte")

    def test_espaces_conserves(self):
        s = cap.svg("  FORENSIQUE ###\n             suite", "t", "c")
        self.assertIn('xml:space="preserve"', s)
        self.assertIn("white-space:pre", s)
        self.assertEqual(textes(s)[3], "             suite")

    def test_couleurs_des_verdicts(self):
        seg = dict((t, c) for t, c in cap.segments("TITRE 93/100  PRÊT · SIGNALÉ · BLOQUANT"))
        self.assertEqual(seg["PRÊT"], cap.VERT)
        self.assertEqual(seg["SIGNALÉ"], cap.OR)
        self.assertEqual(seg["BLOQUANT"], cap.ROUGE)
        self.assertEqual(cap.segments("  ✖ x")[1], ("✖", cap.ROUGE))

    def test_coupe_les_lignes_longues_avec_retrait(self):
        ligne = "    " + " ".join(["mot"] * 60)
        morceaux = cap.couper(ligne, 50)
        self.assertTrue(all(len(m) <= 50 for m in morceaux))
        self.assertTrue(morceaux[1].startswith("      "))
        self.assertEqual(" ".join(" ".join(morceaux).split()), " ".join(ligne.split()))

    def test_commande_muette_refusee(self):
        with self.assertRaises(RuntimeError):
            cap.executer({"id": "x", "commande": "true"}, Path("."))

    def test_texte_vers_svg(self):
        with tempfile.TemporaryDirectory() as d:
            src, out = Path(d) / "s.txt", Path(d) / "s.svg"
            src.write_text("OK\n", encoding="utf-8")
            self.assertEqual(cap.main(["--texte", str(src), "--titre", "t", "--commande", "c", "-o", str(out)]), 0)
            ET.fromstring(out.read_text(encoding="utf-8"))


class Visuels(unittest.TestCase):
    def test_chaque_glyphe_donne_un_svg_valide(self):
        for nom in vis.GLYPHES:
            ET.fromstring(vis.tuile(nom, "#0E3F2D", titre=nom))

    def test_banniere_valide_et_complete(self):
        m = {"pack": "Test & Co", "surtitre": "Join Médicis", "accroche": ["Ligne « une »"], "puces": ["3 Skills"],
             "familles": {"A": "#123456"}, "icones": [{"nom": f"s{i}", "glyphe": g, "famille": "A"}
                                                      for i, g in enumerate(list(vis.GLYPHES)[:7])]}
        s = vis.banniere(m)
        racine = ET.fromstring(s)
        self.assertIn("Test & Co", textes(s))
        self.assertEqual(racine.get("width"), "1280")

    def test_glyphe_inconnu_refuse(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "visuels.json"
            p.write_text(json.dumps({"pack": "x", "surtitre": "x", "accroche": [], "puces": [], "familles": {"A": "#000"},
                                     "icones": [{"nom": "a", "glyphe": "licorne", "famille": "A"}]}), encoding="utf-8")
            self.assertEqual(vis.main([str(p)]), 1)

    def test_manifestes_des_packs(self):
        for manifeste in RACINE.glob("*-skills/docs/media/visuels.json"):
            m = json.loads(manifeste.read_text(encoding="utf-8"))
            for ic in m["icones"]:
                if ic.get("a_venir"):
                    continue
                self.assertIn(ic["glyphe"], vis.GLYPHES, f"{manifeste} : {ic['glyphe']}")
                self.assertIn(ic["famille"], m["familles"], f"{manifeste} : {ic['famille']}")
                self.assertTrue((RACINE / manifeste.parts[-4] / "skills" / ic["nom"]).is_dir(),
                                f"{manifeste} : aucun Skill « {ic['nom']} »")


if __name__ == "__main__":
    unittest.main()
