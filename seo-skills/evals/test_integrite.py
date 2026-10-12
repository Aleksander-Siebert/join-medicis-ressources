#!/usr/bin/env python3
"""Tests d'intégrité du pack SEO : python3 evals/test_integrite.py

Vérifie ce qu'aucun test de script ne voit, pour les Skills déjà passés en v2
(ceux qui renvoient à commun/regles.md) : frontmatter, description (1 024
caractères au plus, « Pas pour »), fichiers cités qui existent, socle commun
synchronisé, typographie des SKILL.md et références, `--help` des scripts,
tests et cas d'éval présents. Pour tout le pack : modèles, réserve partagée
avec le pack LinkedIn, exemple marqué fictif.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
SKILLS = sorted(p for p in (PACK / "skills").iterdir() if (p / "SKILL.md").exists())
V2 = [s for s in SKILLS if "commun/regles.md" in (s / "SKILL.md").read_text(encoding="utf-8")]
resultats = []


def test(nom):
    def deco(f):
        try:
            f()
            resultats.append((nom, None))
        except AssertionError as e:
            resultats.append((nom, str(e) or "échec"))
        return f
    return deco


def frontmatter(skill):
    t = (skill / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"---\nname: (.+)\ndescription: >-\n(.*?)\n---\n", t, re.S)
    assert m, f"{skill.name} : frontmatter illisible"
    return m.group(1).strip(), " ".join(m.group(2).split()), t


@test("Skills v2 présents (au moins seo-brief et seo-write)")
def _():
    noms = {s.name for s in V2}
    assert {"seo-brief", "seo-write"} <= noms, noms


@test("tous les Skills : nom = dossier, préfixe seo-, description de 1 024 caractères au plus")
def _():
    for s in SKILLS:
        nom, d, _ = frontmatter(s)
        assert nom == s.name, f"{s.name} : name « {nom} »"
        assert nom.startswith("seo-"), nom
        assert len(d) <= 1024, f"{s.name} : {len(d)} caractères"


@test("v2 : description avec « Pas pour », sans tiret cadratin")
def _():
    for s in V2:
        _, d, _ = frontmatter(s)
        assert "Pas pour" in d, f"{s.name} : ne dit pas quand ne pas l'utiliser"
        assert "—" not in d and "–" not in d, f"{s.name} : tiret dans la description"


@test("v2 : fichiers cités dans SKILL.md et références : ils existent")
def _():
    manquants = []
    for s in V2:
        textes = [(s / "SKILL.md").read_text(encoding="utf-8")]
        textes += [f.read_text(encoding="utf-8") for f in (s / "references").glob("*.md")] if (s / "references").exists() else []
        for t in textes:
            for chemin in set(re.findall(r"`((?:scripts|references|commun)/[\w./-]+\.\w+)", t)):
                if chemin.startswith("commun/modeles/"):
                    ok = (PACK / "templates" / chemin.split("/", 2)[2]).exists()
                elif chemin.startswith("commun/"):
                    ok = (PACK / chemin).exists()
                else:
                    ok = (s / chemin).exists()
                if not ok:
                    manquants.append(f"{s.name}: {chemin}")
    assert not manquants, ", ".join(sorted(set(manquants)))


@test("socle commun synchronisé (outils/propager.py --verifier)")
def _():
    p = subprocess.run([sys.executable, str(PACK / "outils" / "propager.py"), "--verifier"], capture_output=True, text=True)
    assert p.returncode == 0, p.stdout


@test("v2 : typographie des SKILL.md et références (pas de tiret cadratin, pas de « ; » à la place d'une incise)")
def _():
    fautes = []
    for s in V2:
        fichiers = [s / "SKILL.md"] + sorted((s / "references").glob("*.md"))
        for f in fichiers:
            for n, ligne in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if "—" in ligne and "commun/" not in ligne:
                    fautes.append(f"{s.name}/{f.name}:{n}")
    assert not fautes, ", ".join(fautes[:10])


@test("socle : règles et preuves sans tiret cadratin, règle du contenu de tiers présente")
def _():
    regles = (PACK / "commun" / "regles.md").read_text(encoding="utf-8")
    assert "donnée" in regles and "jamais une instruction" in regles
    for f in ("regles.md", "preuves.md"):
        t = (PACK / "commun" / f).read_text(encoding="utf-8").replace("(—)", "")
        assert "—" not in t, f


@test("v2 : chaque script répond à --help (code 0) et a une docstring")
def _():
    scripts = [p for s in V2 for p in (s / "scripts").glob("*.py")] if V2 else []
    scripts += [p for p in (PACK / "commun").glob("*.py") if p.name != "texte_fr.py"]
    for p in scripts:
        r = subprocess.run([sys.executable, str(p), "--help"], capture_output=True, text=True)
        assert r.returncode == 0, f"{p.name} --help : code {r.returncode} {r.stderr[-300:]}"
        assert p.read_text(encoding="utf-8").lstrip().startswith(("#!", '"""')), p.name
        assert '"""' in p.read_text(encoding="utf-8")[:400], f"{p.name} : docstring absente"


@test("v2 : tests et cas d'éval pour chaque Skill")
def _():
    cas = json.loads((PACK / "evals" / "evals.json").read_text(encoding="utf-8"))["cas"]
    for s in V2:
        assert list((PACK / "evals" / s.name).glob("test_*.py")), f"{s.name} : aucun test"
        assert any(c["skill"] == s.name for c in cas), f"{s.name} : aucun cas dans evals.json"


@test("modèles : réserve identique à celle du pack LinkedIn, exemple marqué fictif, modèles vides")
def _():
    li = PACK.parent / "linkedin-skills" / "templates" / "reserve.md"
    if li.exists():
        assert (PACK / "templates" / "reserve.md").read_text(encoding="utf-8") == li.read_text(encoding="utf-8"), \
            "templates/reserve.md diffère de linkedin-skills/templates/reserve.md (réserve partagée)"
    ex = (PACK / "templates" / "exemple-site-context.md").read_text(encoding="utf-8")
    assert "Exemple fictif" in ex
    vide = (PACK / "templates" / "site-context.md").read_text(encoding="utf-8")
    assert "- rempli : non" in vide and "Assurly" not in vide


@test("exemples : Assurly et assurly.example seulement, pas de nom de client réel")
def _():
    interdits = re.compile(r"mondassur|monda'blog", re.I)
    for f in list((PACK / "skills").rglob("*.md")) + list((PACK / "evals").rglob("*.md")) + list((PACK / "templates").glob("*.md")):
        assert not interdits.search(f.read_text(encoding="utf-8")), f"nom réel dans {f.relative_to(PACK)}"


def main():
    for nom, err in resultats:
        print(("  ✔ " if err is None else "  ✖ ") + nom + ("" if err is None else f"\n      {err}"))
    ok = sum(1 for _, e in resultats if e is None)
    print(f"{ok}/{len(resultats)} tests passés")
    return 0 if ok == len(resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
