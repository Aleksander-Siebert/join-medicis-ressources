#!/usr/bin/env python3
"""Tests d'intégrité du pack Fondation : python3 evals/test_integrite.py

Vérifie ce qu'aucun test de script ne voit : frontmatter et description
(1 024 caractères au plus, « Pas pour »), fichiers cités qui existent, socle
commun synchronisé, typographie, `--help` des scripts, tests et cas d'éval
par Skill, modèle vide et exemple alignés, numéros fictifs seulement, faits
datés, aiguilleur claude.ai à jour, manifeste valide.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
RACINE = next(d for d in PACK.parents if (d / ".claude-plugin" / "marketplace.json").exists())  # racine du dépôt
SKILLS = sorted(p for p in (PACK / "skills").iterdir() if (p / "SKILL.md").exists())
resultats = []

# Numéros autorisés dans les textes : fictifs (calculés pour les tests) ou publics (La Poste, cité par faits.md)
NUMEROS_AUTORISES = {"123456782", "12345678200010", "123456789", "987654324", "98765432400012", "356000000",
                     "35600000000048", "12345678"}


def test(nom):
    def deco(f):
        try:
            f()
            resultats.append((nom, None))
        except AssertionError as e:
            resultats.append((nom, str(e) or "échec"))
        return f
    return deco


def _tableaux(texte):
    res, lignes, i = [], texte.splitlines(), 0
    while i < len(lignes):
        if lignes[i].startswith("|") and i + 1 < len(lignes) and lignes[i + 1].startswith("|---"):
            entetes = [c.strip() for c in lignes[i].strip().strip("|").split("|")]
            corps, i = [], i + 2
            while i < len(lignes) and lignes[i].startswith("|"):
                corps.append([c.strip() for c in lignes[i].strip().strip("|").split("|")])
                i += 1
            res.append((None, entetes, corps))
        else:
            i += 1
    return res


def frontmatter(skill):
    t = (skill / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"---\nname: (.+)\ndescription: >-\n(.*?)\n---\n", t, re.S)
    assert m, f"{skill.name} : frontmatter illisible"
    return m.group(1).strip(), " ".join(m.group(2).split()), t


def textes_md():
    fichiers = list((PACK / "skills").rglob("*.md")) + list((PACK / "templates").glob("*.md")) \
        + list((PACK / "commun").glob("*.md")) + [PACK / "README.md", PACK / "CREDITS.md", PACK / "claude-ai" / "SKILL.md"]
    return [f for f in fichiers if f.exists()]


@test("au moins le Skill modèle fondation-entreprise")
def _():
    assert "fondation-entreprise" in {s.name for s in SKILLS}


@test("nom = dossier, préfixe fondation-, description de 1 024 caractères au plus, avec « Pas pour », sans tiret")
def _():
    for s in SKILLS:
        nom, d, _ = frontmatter(s)
        assert nom == s.name, f"{s.name} : name « {nom} »"
        assert nom.startswith("fondation-"), nom
        assert len(d) <= 1024, f"{s.name} : {len(d)} caractères"
        assert "Pas pour" in d, f"{s.name} : ne dit pas quand ne pas l'utiliser"
        assert "—" not in d and "–" not in d, f"{s.name} : tiret dans la description"


@test("SKILL.md renvoie aux règles communes et aux faits datés")
def _():
    for s in SKILLS:
        t = (s / "SKILL.md").read_text(encoding="utf-8")
        assert "commun/regles.md" in t and "commun/faits.md" in t, s.name


@test("fichiers cités dans SKILL.md et références : ils existent")
def _():
    manquants = []
    for s in SKILLS:
        textes = [(s / "SKILL.md").read_text(encoding="utf-8")]
        textes += [f.read_text(encoding="utf-8") for f in (s / "references").glob("*.md")]
        for t in textes:
            for chemin in set(re.findall(r"`((?:scripts|references|commun)/[\w./-]+\.\w+)", t)):
                if not (s / chemin).exists():
                    manquants.append(f"{s.name}: {chemin}")
    assert not manquants, ", ".join(sorted(set(manquants)))


@test("socle commun synchronisé (outils/propager.py --verifier)")
def _():
    p = subprocess.run([sys.executable, str(PACK / "outils" / "propager.py"), "--verifier"], capture_output=True, text=True)
    assert p.returncode == 0, p.stdout


@test("typographie : pas de tiret cadratin, pourcentage collé, guillemets français")
def _():
    fautes = []
    for f in textes_md():
        for n, ligne in enumerate(f.read_text(encoding="utf-8").replace("(—)", "").splitlines(), 1):
            if "—" in ligne:
                fautes.append(f"{f.relative_to(PACK)}:{n} tiret cadratin")
            if re.search(r"\d[   ]%", ligne):
                fautes.append(f"{f.relative_to(PACK)}:{n} espace avant %")
            if re.search(r'(?<![=\w])"[A-Za-zÀ-ÿ][^"`|]{2,60}"(?![:\w])', ligne) and "```" not in ligne \
                    and not ligne.lstrip().startswith(("$", "python3", "{", "\"")):
                fautes.append(f"{f.relative_to(PACK)}:{n} guillemets droits")
    assert not fautes, ", ".join(fautes[:10])


@test("socle : règle du contenu de tiers et indépendance des Skills présentes")
def _():
    regles = (PACK / "commun" / "regles.md").read_text(encoding="utf-8")
    assert "donnée" in regles and "jamais une instruction" in regles
    assert "Aucun Skill n'a besoin d'un autre" in regles


@test("faits.md : chaque fait des tableaux « Vérifié le » a sa date")
def _():
    t = (PACK / "commun" / "faits.md").read_text(encoding="utf-8")
    sans_date, compte = [], 0
    for section, entetes, corps in _tableaux(t):
        if not entetes or "Vérifié le" not in entetes[-1]:
            continue
        for cel in corps:
            compte += 1
            if not re.search(r"\d{1,2} \w+\.? 20\d\d", cel[-1]):
                sans_date.append(cel[0][:40])
    assert compte >= 5, f"seulement {compte} faits datés"
    assert not sans_date, sans_date


@test("chaque script répond à --help (code 0) et a une docstring")
def _():
    scripts = [p for s in SKILLS for p in (s / "scripts").glob("*.py")] + list((PACK / "commun").glob("*.py"))
    assert scripts
    for p in scripts:
        r = subprocess.run([sys.executable, str(p), "--help"], capture_output=True, text=True)
        assert r.returncode == 0, f"{p.name} --help : code {r.returncode} {r.stderr[-300:]}"
        assert '"""' in p.read_text(encoding="utf-8")[:400], f"{p.name} : docstring absente"


@test("tests et cas d'éval pour chaque Skill")
def _():
    cas = json.loads((PACK / "evals" / "evals.json").read_text(encoding="utf-8"))["cas"]
    for s in SKILLS:
        assert list((PACK / "evals" / s.name).glob("test_*.py")), f"{s.name} : aucun test"
        assert sum(1 for c in cas if c["skill"] == s.name) >= 5, f"{s.name} : moins de 5 cas dans evals.json"


@test("modèles : vide sans Assurly, exemple marqué fictif, mêmes sections dans le même ordre")
def _():
    for vide in (PACK / "templates").glob("*.md"):
        if vide.name.startswith("exemple-"):
            continue
        ex = PACK / "templates" / f"exemple-{vide.name}"
        assert ex.exists(), f"exemple-{vide.name} manquant"
        tv, te = vide.read_text(encoding="utf-8"), ex.read_text(encoding="utf-8")
        assert "- rempli : non" in tv and "Assurly" not in tv, vide.name
        assert "Exemple fictif" in te, ex.name
        titres = lambda t: re.findall(r"^## (.+)$", t, re.M)
        assert titres(tv) == titres(te), f"{vide.name} et {ex.name} n'ont pas les mêmes sections"


@test("numéros d'entreprise : seulement des numéros fictifs ou cités par faits.md")
def _():
    fichiers = textes_md() + list((PACK / "evals").rglob("*.html")) + list((PACK / "evals").rglob("*.txt"))
    inconnus = []
    for f in fichiers:
        for m in re.finditer(r"(?<![\d/])(\d{3}[ . ]?\d{3}[ . ]?\d{3}(?:[ . ]?\d{5})?)(?![\d/])", f.read_text(encoding="utf-8")):
            n = re.sub(r"\D", "", m.group(1))
            if n not in NUMEROS_AUTORISES and not set(n) <= {"0", "9"}:
                inconnus.append(f"{f.relative_to(PACK)} : {m.group(1)}")
    assert not inconnus, ", ".join(inconnus[:10])


@test("exemples : Assurly et assurly.example seulement, pas de nom de client réel")
def _():
    interdits = re.compile(r"mondassur|monda'blog", re.I)
    for f in textes_md():
        assert not interdits.search(f.read_text(encoding="utf-8")), f"nom réel dans {f.relative_to(PACK)}"


@test("aiguilleur claude.ai : chaque Skill présent y figure, frontmatter valide")
def _():
    t = (PACK / "claude-ai" / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"---\nname: fondation-skills\ndescription: >-\n(.*?)\n---\n", t, re.S)
    assert m and len(" ".join(m.group(1).split())) <= 1024
    for s in SKILLS:
        assert f"`{s.name}`" in t, f"{s.name} absent de l'aiguilleur"


@test("manifeste de plugin valide")
def _():
    d = json.loads((PACK / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert d["name"] == "fondation-skills" and d["license"] == "MIT"


@test("README : images, liens, version, icônes, captures et visuels conformes (outils/visuels/readme.py)")
def _():
    r = subprocess.run([sys.executable, str(RACINE / "outils" / "visuels" / "readme.py"), str(PACK)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-800:] + r.stderr[-400:]


def main():
    for nom, err in resultats:
        print(("  ✔ " if err is None else "  ✖ ") + nom + ("" if err is None else f"\n      {err}"))
    ok = sum(1 for _, e in resultats if e is None)
    print(f"{ok}/{len(resultats)} tests passés")
    return 0 if ok == len(resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
