"""Tests d'intégrité du pack GEO : frontmatter, affirmations interdites, typographie, anonymisation."""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

PACK = Path(__file__).resolve().parents[2]
RACINE = next(d for d in PACK.parents if (d / ".claude-plugin" / "marketplace.json").exists())  # racine du dépôt
SKILLS = sorted(d for d in (PACK / "skills").iterdir() if (d / "SKILL.md").exists())
NOMS = ["geo-audit", "geo-acces", "geo-visibilite", "geo-exactitude", "geo-contenu", "geo-mentions", "geo-entite", "geo-agentic"]


def textes():
    """Tous les .md du pack livrés à l'utilisateur, sauf les copies de commun/ (contrôlées à la source)."""
    for f in sorted(PACK.rglob("*.md")):
        if "/commun/" in str(f.relative_to(RACINE)) and f.parent.name in ("commun", "modeles") and "skills" in f.parts:
            continue
        if "evals" in f.parts:
            continue
        yield f


def lignes_sans_code(f):
    for n, l in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        yield n, re.sub(r"`[^`]*`", "", l)


def frontmatter(f):
    s = f.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", s, re.S)
    assert m, f
    nom = re.search(r"^name:\s*(\S+)", m.group(1), re.M).group(1)
    d = re.search(r"description:\s*>-\n(.*)", m.group(1), re.S)
    desc = " ".join(d.group(1).split()) if d else re.search(r"^description:\s*(.+)$", m.group(1), re.M).group(1)
    return nom, desc


class Frontmatter(unittest.TestCase):
    def test_huit_skills_valides(self):
        self.assertEqual(sorted(d.name for d in SKILLS), sorted(NOMS))

    def test_nom_description(self):
        for d in SKILLS:
            nom, desc = frontmatter(d / "SKILL.md")
            self.assertEqual(nom, d.name)
            self.assertLessEqual(len(desc), 1024, d.name)
            self.assertIn("Pas pour", desc, f"{d.name} : la description dit quand ne pas l'utiliser")
            self.assertIn("Utilise-le", desc, d.name)

    def test_fichiers_cites_existent(self):
        for d in SKILLS:
            s = (d / "SKILL.md").read_text(encoding="utf-8")
            for chemin in set(re.findall(r"`((?:scripts|references)/[\w./-]+\.(?:py|md))`", s)):
                self.assertTrue((d / chemin).exists(), f"{d.name} cite {chemin}")

    def test_scripts_aide(self):
        for f in sorted(PACK.glob("skills/*/scripts/*.py")):
            p = subprocess.run([sys.executable, str(f), "--help"], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, f"{f.name} : {p.stderr[-300:]}")


class Affirmations(unittest.TestCase):
    """Le folklore reste nommé pour être écarté, jamais affirmé (commun/preuves.md §7)."""

    INTERDITS = [
        (r"GPTBot[^.|\n]{0,50}(?:sert|utilis\w*|indexe|pour)[^.|\n]{0,20}(?:la )?recherche", "GPTBot présenté comme robot de recherche"),
        (r"bloquer GPTBot[^.\n]{0,60}(?:retire|sort|exclut)[^.\n]{0,40}(?:ChatGPT|recherche)", "bloquer GPTBot = sortir de ChatGPT"),
        (r"Google-Extended[^.\n]{0,60}(?:retire|exclut|sort)[^.\n]{0,40}(?:Aperçus IA|AI Overviews|Search|Recherche)", "Google-Extended et la Recherche"),
        (r"llms\.txt[^.\n]{0,40}(?:essentiel|indispensable|améliore|augmente|levier)", "llms.txt présenté comme un levier"),
        (r"(?:\+|jusqu'à )\d+ ?%[^.\n]{0,40}(?:citations?|visibilité)", "gain de visibilité chiffré"),
        (r"\b(?:134|40)\s*(?:à|-)\s*(?:167|60) mots", "longueur de passage idéale"),
    ]
    NEGATION = re.compile(r"\b(?:pas|jamais|aucun|aucune|ni|sans effet|écart\w*|folklore|inutile|n'|ne )\b|«|Jamais|Pas\b", re.I)

    def test_aucune_affirmation_interdite(self):
        fautes = []
        for f in textes():
            for n, l in lignes_sans_code(f):
                for motif, quoi in self.INTERDITS:
                    if re.search(motif, l, re.I) and not self.NEGATION.search(l):
                        fautes.append(f"{f.relative_to(PACK)}:{n} {quoi}")
        self.assertEqual(fautes, [])

    def test_table_des_robots(self):
        d = json.loads((PACK / "commun" / "robots_ia.json").read_text(encoding="utf-8"))
        role = {r["jeton"]: r["role"] for r in d["robots"]}
        self.assertEqual(role["GPTBot"], "entrainement")
        self.assertEqual(role["OAI-SearchBot"], "recherche")
        self.assertEqual(role["Google-Extended"], "jeton")
        self.assertEqual(role["Google-Agent"], "utilisateur")
        for r in d["robots"]:
            self.assertTrue(r["source"], r["jeton"])


class Typographie(unittest.TestCase):
    def test_pas_de_tiret_cadratin_en_prose(self):
        fautes = [f"{f.relative_to(PACK)}:{n}" for f in textes() for n, l in lignes_sans_code(f)
                  if "—" in l and "tiret cadratin" not in l]
        self.assertEqual(fautes, [])

    def test_pourcentage_colle(self):
        fautes = [f"{f.relative_to(PACK)}:{n}" for f in textes() for n, l in lignes_sans_code(f)
                  if re.search(r"\d [%]", l)]
        self.assertEqual(fautes, [])


class Anonymisation(unittest.TestCase):
    INTERDITS = re.compile(r"back ?market|backmarket|@gmail\.com|aleksiebert", re.I)

    def test_aucune_donnee_reelle(self):
        fautes = []
        for f in PACK.rglob("*"):
            if f.is_file() and f.suffix in (".md", ".py", ".json", ".txt", ".csv", ".html") and "__pycache__" not in f.parts:
                if self.INTERDITS.search(f.read_text(encoding="utf-8", errors="ignore")) and f.name != "test_integrite.py":
                    fautes.append(str(f.relative_to(PACK)))
        self.assertEqual(fautes, [])

    def test_exemples_fictifs_signales(self):
        for f in PACK.glob("evals/geo-*/*"):
            if f.suffix in (".txt", ".html", ".md") and f.stat().st_size > 200 and not f.name.startswith("robots"):
                self.assertRegex(f.read_text(encoding="utf-8").lower(), r"fictiv|fictif", f.name)


class Socle(unittest.TestCase):
    def test_copies_du_socle_a_jour(self):
        p = subprocess.run([sys.executable, str(PACK / "outils" / "propager.py"), "--verifier"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-500:])

    def test_readme(self):
        p = subprocess.run([sys.executable, str(RACINE / "outils" / "visuels" / "readme.py"), str(PACK)],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-600:])


if __name__ == "__main__":
    unittest.main()
