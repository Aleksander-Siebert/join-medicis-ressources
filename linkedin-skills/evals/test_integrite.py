#!/usr/bin/env python3
"""Tests d'intégrité du pack LinkedIn : python3 evals/test_integrite.py

Vérifie ce qu'aucun test de script ne voit : frontmatter, descriptions,
fichiers cités qui existent, Skills cités qui existent, socle commun
synchronisé, modèles livrés vides, grilles qui totalisent 100, règle du
contenu de tiers, typographie des SKILL.md, manifeste, aiguilleur claude.ai,
présence des tests et des évals par Skill.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
SKILLS = sorted(p for p in (PACK / "skills").iterdir() if p.is_dir())
NOMS = {p.name for p in SKILLS}
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


@test("15 Skills, nom = dossier, préfixe linkedin-")
def _():
    assert len(SKILLS) == 15, f"{len(SKILLS)} Skills"
    for s in SKILLS:
        nom, _, _ = frontmatter(s)
        assert nom == s.name, f"{s.name} : name « {nom} »"
        assert nom.startswith("linkedin-"), nom


@test("descriptions : 1 024 caractères au plus, « Pas pour », sans tiret cadratin")
def _():
    for s in SKILLS:
        _, d, _ = frontmatter(s)
        assert len(d) <= 1024, f"{s.name} : {len(d)} caractères"
        assert "Pas pour" in d or "Pas de" in d, f"{s.name} : la description ne dit pas quand ne pas l'utiliser"
        assert "—" not in d and "–" not in d, f"{s.name} : tiret dans la description"


@test("chaque SKILL.md renvoie au socle commun (règles, contenu de tiers)")
def _():
    regles = (PACK / "commun" / "regles.md").read_text(encoding="utf-8")
    assert re.search(r"donnée", regles) and re.search(r"jamais (?:une|des) instructions?", regles), "règle du contenu de tiers absente de regles.md"
    for s in SKILLS:
        assert "commun/regles.md" in frontmatter(s)[2], f"{s.name} : ne cite pas commun/regles.md"


@test("fichiers cités dans les SKILL.md : ils existent")
def _():
    manquants = []
    for s in SKILLS:
        t = frontmatter(s)[2]
        for chemin in set(re.findall(r"`((?:scripts|references|assets|commun)/[\w./-]+\.\w+)", t)):
            base = PACK if chemin.startswith("commun/") and not chemin.startswith("commun/modeles") else s
            if chemin.startswith("commun/modeles/"):
                base, chemin = PACK / "templates", chemin.split("/", 2)[2]
            if not (base / chemin).exists():
                manquants.append(f"{s.name}: {chemin}")
        for chemin in set(re.findall(r"`((?:formules|grille|grille-page)\.json)`", t)):
            if not (s / chemin).exists() and not any((PACK / "skills" / n / chemin).exists() for n in NOMS):
                manquants.append(f"{s.name}: {chemin}")
    assert not manquants, ", ".join(sorted(manquants))


@test("Skills cités (/linkedin-…) : ils existent tous")
def _():
    cites = set()
    for f in list((PACK / "skills").rglob("*.md")) + [PACK / "README.md", PACK / "claude-ai" / "SKILL.md"]:
        if "/commun/" in str(f):
            continue
        cites |= set(re.findall(r"/(linkedin-[a-z]+)\b", f.read_text(encoding="utf-8")))
    inconnus = cites - NOMS - {"linkedin-skills"}  # nom du pack, dans les URL
    assert not inconnus, f"inconnus : {sorted(inconnus)}"


@test("aucune trace de la v1 (linkedin-carousel, accroches.json, voix.md hors compatibilité)")
def _():
    fautes = []
    for f in list((PACK / "skills").rglob("*.md")) + list((PACK / "skills").rglob("*.py")) + [PACK / "README.md"]:
        if "/commun/" in str(f):
            continue
        # une mention explicite de la v1 (compatibilité) est permise
        t = "\n".join(l for l in f.read_text(encoding="utf-8").splitlines() if "v1" not in l)
        for motif in ("linkedin-carousel", "accroches.json", "voix.md"):
            if re.search(rf"(?<![\w-]){re.escape(motif)}", t):
                fautes.append(f"{f.relative_to(PACK)}: {motif}")
    assert not fautes, ", ".join(fautes)


@test("socle commun identique dans chaque Skill (outils/propager.py --verifier)")
def _():
    p = subprocess.run([sys.executable, str(PACK / "outils" / "propager.py"), "--verifier"], capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr


@test("modèles livrés vides (aucune ligne de tableau remplie)")
def _():
    for f in (PACK / "templates").glob("*.md"):
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.startswith("|") and not re.fullmatch(r"\|[\s|:-]*\|?", l.strip()):
                cel = [c.strip() for c in l.strip().strip("|").split("|")]
                # en-tête : la ligne suivante est un séparateur ; on accepte les en-têtes
                if all(cel) and not any(re.search(r"\d{4}-\d{2}-\d{2}|\d+ ?%|€", c) for c in cel):
                    continue
                assert not any(re.search(r"\d{4}-\d{2}-\d{2}", c) for c in cel), f"{f.name} : ligne remplie « {l[:60]} »"


@test("grilles notées sur 100")
def _():
    for f in [PACK / "skills" / "linkedin-profile" / "grille.json", PACK / "skills" / "linkedin-entreprise" / "grille-page.json"]:
        d = json.loads(f.read_text(encoding="utf-8"))
        somme = sum(c["points"] for c in d["criteres"])
        assert somme == d["total"] == 100, f"{f.name} : {somme} / {d['total']}"


@test("formules.json : identifiants uniques, objectifs connus")
def _():
    d = json.loads((PACK / "skills" / "linkedin-post" / "formules.json").read_text(encoding="utf-8"))
    ids = [f["id"] for f in d["accroches"] + d["structurelles"]]
    assert len(ids) == len(set(ids)), "identifiants en double"
    objectifs = set(d["objectifs"])
    for f in d["accroches"] + d["structurelles"]:
        assert set(f["objectif"]) <= objectifs, f["id"]


@test("SKILL.md : pas de tiret cadratin hors exemples, pas de gras Unicode")
def _():
    for s in SKILLS:
        t = frontmatter(s)[2]
        hors_code = re.sub(r"```.*?```|`[^`]*`|« [^»]*»", "", t, flags=re.S)
        if s.name != "linkedin-human":
            assert "—" not in hors_code, f"{s.name} : tiret cadratin"
        assert not re.search(r"[\U0001D400-\U0001D7FF]", t), f"{s.name} : gras Unicode"


@test("chaque Skill a ses tests et son evals.json")
def _():
    for s in SKILLS:
        d = PACK / "evals" / s.name
        assert d.is_dir() and list(d.glob("test_*.py")), f"{s.name} : pas de test"
        e = d / "evals.json"
        assert e.exists(), f"{s.name} : pas d'evals.json"
        j = json.loads(e.read_text(encoding="utf-8"))
        assert j.get("skill_name") == s.name and len(j.get("evals", [])) >= 3, f"{s.name} : evals.json incomplet"
        for ev in j["evals"]:
            assert ev.get("prompt") and ev.get("expectations"), f"{s.name} : éval {ev.get('id')} sans prompt ou attentes"


@test("manifeste 2.0.0 et aiguilleur claude.ai à 15 modules")
def _():
    m = json.loads((PACK / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert m["version"] == "2.0.0", m["version"]
    routeur = (PACK / "claude-ai" / "SKILL.md").read_text(encoding="utf-8")
    absents = [n for n in NOMS if f"`{n}`" not in routeur]
    assert not absents, f"absents de l'aiguilleur : {absents}"
    d = " ".join(re.search(r"description: >-\n(.*?)\n---", routeur, re.S).group(1).split())
    assert len(d) <= 1024, f"aiguilleur : {len(d)} caractères"


@test("scripts : --help répond sans erreur, sous-commandes comprises")
def _():
    for f in sorted((PACK / "skills").glob("*/scripts/*.py")):
        p = subprocess.run([sys.executable, str(f), "--help"], capture_output=True, text=True)
        assert p.returncode == 0, f"{f.relative_to(PACK)} : {p.stderr[-300:]}"
        m = re.search(r"\{([\w,-]+)\}", p.stdout)
        for sous in (m.group(1).split(",") if m else []):
            q = subprocess.run([sys.executable, str(f), sous, "--help"], capture_output=True, text=True)
            assert q.returncode == 0, f"{f.relative_to(PACK)} {sous} --help : {q.stderr[-300:]}"


@test("aucun caractère de contrôle dans les fichiers du pack")
def _():
    fautes = []
    for f in list(PACK.rglob("*.py")) + list(PACK.rglob("*.md")) + list(PACK.rglob("*.json")):
        if "__pycache__" in str(f):
            continue
        if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", f.read_text(encoding="utf-8")):
            fautes.append(str(f.relative_to(PACK)))
    assert not fautes, ", ".join(fautes)


if __name__ == "__main__":
    for nom, err in resultats:
        print(("  ok  " if err is None else "  ✖   ") + nom + ("" if err is None else f"\n        {err}"))
    n_ok = sum(1 for _, e in resultats if e is None)
    print(f"{n_ok}/{len(resultats)} tests passés")
    sys.exit(0 if n_ok == len(resultats) else 1)
