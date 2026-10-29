#!/usr/bin/env python3
"""Tests d'intégrité du pack Tone of Voice : python3 evals/test_integrite.py

Vérifie ce qu'aucun test de script ne voit : frontmatter et description
(1 024 caractères au plus, « Pas pour »), fichiers cités qui existent,
typographie, `--help` des scripts, modèle et exemple alignés (mêmes
sections), copies de templates/ à jour, exemples fictifs seulement,
manifeste valide, ZIP claude.ai avec un seul SKILL.md.
"""
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
RACINE = next(d for d in PACK.parents if (d / ".claude-plugin" / "marketplace.json").exists())  # racine du dépôt
SKILL = PACK / "skills" / "tone-of-voice"
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


def textes_md():
    fichiers = list(SKILL.rglob("*.md")) + list((PACK / "templates").glob("*.md")) \
        + [PACK / "README.md", PACK / "CREDITS.md"]
    return [f for f in fichiers if f.exists()]


@test("nom = dossier, description de 1 024 caractères au plus, avec « Pas pour », sans tiret")
def _():
    t = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"---\nname: (.+)\ndescription: >-\n(.*?)\n---\n", t, re.S)
    assert m, "frontmatter illisible"
    nom, d = m.group(1).strip(), " ".join(m.group(2).split())
    assert nom == SKILL.name == "tone-of-voice", nom
    assert len(d) <= 1024, f"{len(d)} caractères"
    assert "Pas pour" in d
    assert "—" not in d and "–" not in d


@test("SKILL.md de 250 lignes au plus, références lues à la demande")
def _():
    n = len((SKILL / "SKILL.md").read_text(encoding="utf-8").splitlines())
    assert n <= 250, f"{n} lignes"


@test("fichiers cités dans SKILL.md et références : ils existent")
def _():
    manquants = []
    textes = [(SKILL / "SKILL.md").read_text(encoding="utf-8")]
    textes += [f.read_text(encoding="utf-8") for f in (SKILL / "references").glob("*.md")]
    for t in textes:
        for chemin in set(re.findall(r"`((?:scripts|references|modeles|exemples)/[\w./-]+\.\w+)", t)):
            if not (SKILL / chemin).exists():
                manquants.append(chemin)
    assert not manquants, ", ".join(sorted(set(manquants)))


@test("chaque référence est citée par SKILL.md")
def _():
    t = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    absentes = [f.name for f in (SKILL / "references").glob("*.md") if f"references/{f.name}" not in t]
    assert not absentes, absentes


@test("typographie : pas de tiret cadratin, pourcentage collé, guillemets français")
def _():
    fautes = []
    for f in textes_md():
        texte = re.sub(r"```.*?```", "", f.read_text(encoding="utf-8"), flags=re.S)
        for n, ligne in enumerate(texte.replace("(—)", "").splitlines(), 1):
            if "—" in ligne:
                fautes.append(f"{f.relative_to(PACK)}:{n} tiret cadratin")
            if re.search(r"\d[   ]%", ligne):
                fautes.append(f"{f.relative_to(PACK)}:{n} espace avant %")
            if re.search(r'(?<![=\w`])"[A-Za-zÀ-ÿ][^"`|]{2,60}"(?![:\w])', ligne):
                fautes.append(f"{f.relative_to(PACK)}:{n} guillemets droits")
    assert not fautes, ", ".join(fautes[:10])


@test("chaque script répond à --help (code 0), a une docstring, n'importe que la bibliothèque standard")
def _():
    scripts = sorted((SKILL / "scripts").glob("*.py"))
    assert len(scripts) == 4, [p.name for p in scripts]
    locaux = {p.stem for p in scripts}
    for p in scripts:
        src = p.read_text(encoding="utf-8")
        assert '"""' in src[:300], f"{p.name} : docstring absente"
        for mod in re.findall(r"^(?:import|from) (\w+)", src, re.M):
            assert mod in sys.stdlib_module_names or mod in locaux, f"{p.name} importe {mod}"
        if p.stem == "texte":
            continue
        r = subprocess.run([sys.executable, str(p), "--help"], capture_output=True, text=True)
        assert r.returncode == 0, f"{p.name} --help : code {r.returncode} {r.stderr[-300:]}"


@test("modèle vide et exemple : mêmes sections dans le même ordre ; templates/ à jour")
def _():
    modele = (SKILL / "modeles" / "tone-of-voice.md").read_text(encoding="utf-8")
    exemple = (SKILL / "exemples" / "assurly" / "tone-of-voice.md").read_text(encoding="utf-8")
    titres = lambda t: re.findall(r"^## (.+)$", t, re.M)
    assert titres(modele) == titres(exemple), "sections différentes"
    assert len(titres(modele)) == 13
    assert "Assurly" not in modele
    assert (PACK / "templates" / "tone-of-voice.md").read_text(encoding="utf-8") == modele, "templates/tone-of-voice.md périmé"
    assert (PACK / "templates" / "exemple-tone-of-voice.md").read_text(encoding="utf-8") == exemple, \
        "templates/exemple-tone-of-voice.md périmé"


@test("exemples : Assurly fictif seulement, pas de nom de client réel")
def _():
    interdits = re.compile(r"mondassur|anna lou", re.I)
    fichiers = textes_md() + list((PACK / "evals").rglob("*.txt")) + list(SKILL.rglob("*.txt"))
    for f in fichiers:
        assert not interdits.search(f.read_text(encoding="utf-8")), f"nom réel dans {f.relative_to(PACK)}"
    assert "Exemple fictif" in (SKILL / "exemples" / "assurly" / "parcours.md").read_text(encoding="utf-8")


@test("cas d'éval : au moins 8, avec des attentes vérifiées par script")
def _():
    cas = json.loads((PACK / "evals" / "evals.json").read_text(encoding="utf-8"))["cas"]
    assert len(cas) >= 8
    assert sum(1 for c in cas for a in c["attentes"] if a.startswith("[auto]")) >= 8


@test("manifeste de plugin valide, version citée dans le README")
def _():
    m = json.loads((PACK / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert m["name"] == PACK.name and m["license"] == "MIT"
    assert f"version-{m['version']}" in (PACK / "README.md").read_text(encoding="utf-8")
    racine = json.loads((RACINE / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert any(p["name"] == PACK.name for p in racine["plugins"]), "absent du marketplace"


@test("ZIP claude.ai : un seul SKILL.md, licence, aucun manifeste")
def _():
    with tempfile.TemporaryDirectory() as d:
        z = Path(d) / "t.zip"
        r = subprocess.run(["bash", str(PACK / "claude-ai" / "build.sh"), str(z)], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        noms = zipfile.ZipFile(z).namelist()
    assert sum(n.endswith("SKILL.md") for n in noms) == 1
    assert "tone-of-voice/LICENSE" in noms
    assert not any(".claude-plugin" in n or "__pycache__" in n for n in noms)


@test("captures du README : à jour avec la sortie réelle des scripts")
def _():
    outil = RACINE / "outils" / "visuels" / "capture.py"
    r = subprocess.run([sys.executable, str(outil), "--manifeste", str(PACK / "docs" / "media" / "captures.json"),
                        "--verifier"], capture_output=True, text=True, cwd=RACINE)
    assert r.returncode == 0, r.stdout[-400:] + r.stderr[-400:]


if __name__ == "__main__":
    for nom, err in resultats:
        print(("  ok  " if err is None else "  ✖   ") + nom + ("" if err is None else f"\n        {err}"))
    ok = sum(1 for _, e in resultats if e is None)
    print(f"{ok}/{len(resultats)} tests passés")
    sys.exit(0 if ok == len(resultats) else 1)
