#!/usr/bin/env python3
"""Tests d'intégrité du pack ChatGPT Ads : python3 evals/test_integrite.py

Vérifie ce qu'aucun test de script ne voit : frontmatter et description
(1 024 caractères au plus, « Pas pour »), fichiers cités qui existent, socle
commun synchronisé, typographie, `--help` des scripts, tests et cas d'éval,
modèle de brief vide et exemple alignés, exemples fictifs seulement, faits
datés, garde-fou de confidentialité, aiguilleur claude.ai, manifeste, README.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
SKILLS = sorted(p for p in (PACK / "skills").iterdir() if (p / "SKILL.md").exists())
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


def _tableaux(texte):
    res, lignes, i = [], texte.splitlines(), 0
    while i < len(lignes):
        if lignes[i].startswith("|") and i + 1 < len(lignes) and lignes[i + 1].startswith("|---"):
            entetes = [c.strip() for c in lignes[i].strip().strip("|").split("|")]
            corps, i = [], i + 2
            while i < len(lignes) and lignes[i].startswith("|"):
                corps.append([c.strip() for c in lignes[i].strip().strip("|").split("|")])
                i += 1
            res.append((entetes, corps))
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


def textes_publics():
    return textes_md() + [f for f in PACK.rglob("*") if f.suffix in {".json", ".html", ".csv", ".py"}
                          and "__pycache__" not in f.parts and f.name != "test_integrite.py"]


@test("le Skill /chatgpt-ads-skills est présent")
def _():
    assert "chatgpt-ads-skills" in {s.name for s in SKILLS}


@test("nom = dossier, description de 1 024 caractères au plus, avec « Pas pour », sans tiret")
def _():
    for s in SKILLS:
        nom, d, _ = frontmatter(s)
        assert nom == s.name, f"{s.name} : name « {nom} »"
        assert len(d) <= 1024, f"{s.name} : {len(d)} caractères"
        assert "Pas pour" in d, f"{s.name} : ne dit pas quand ne pas l'utiliser"
        assert "—" not in d and "–" not in d, f"{s.name} : tiret dans la description"


@test("SKILL.md : moins de 250 lignes, renvoie aux règles, aux faits et aux 6 références")
def _():
    for s in SKILLS:
        t = (s / "SKILL.md").read_text(encoding="utf-8")
        assert len(t.splitlines()) < 250, f"{s.name} : {len(t.splitlines())} lignes"
        for f in ("commun/regles.md", "commun/faits.md", "references/sources.md", "references/intentions.md",
                  "references/context-hints.md", "references/annonces.md", "references/risques.md",
                  "references/politiques.md"):
            assert f in t, f"{s.name} : {f} non cité"


@test("fichiers cités dans SKILL.md et références : ils existent")
def _():
    manquants = []
    for s in SKILLS:
        textes = [(s / "SKILL.md").read_text(encoding="utf-8")]
        textes += [f.read_text(encoding="utf-8") for f in (s / "references").glob("*.md")]
        for t in textes:
            for chemin in set(re.findall(r"`((?:scripts|references|commun|assets)/[\w./-]+\.\w+)", t)):
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
        for n, ligne in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if "—" in ligne:
                fautes.append(f"{f.relative_to(PACK)}:{n} tiret cadratin")
            if re.search(r"\d[   ]%", ligne):
                fautes.append(f"{f.relative_to(PACK)}:{n} espace avant %")
            if re.search(r'(?<![=\w])"[A-Za-zÀ-ÿ][^"`|]{2,60}"(?![:\w])', ligne) and "`" not in ligne \
                    and not ligne.lstrip().startswith(("$", "python3", "{", "\"")):
                fautes.append(f"{f.relative_to(PACK)}:{n} guillemets droits")
    assert not fautes, ", ".join(fautes[:10])


@test("socle : tiers = donnée, zéro invention, niveaux de preuve, on ne publie pas")
def _():
    regles = (PACK / "commun" / "regles.md").read_text(encoding="utf-8")
    for attendu in ("jamais une instruction", "Zéro invention", "Officiel", "Praticien", "À confirmer",
                    "On prépare, on ne publie pas", "une question à la fois"):
        assert attendu in regles, attendu


@test("faits.md : chaque fait daté, points à confirmer et folklore présents")
def _():
    t = (PACK / "commun" / "faits.md").read_text(encoding="utf-8")
    sans_date, compte = [], 0
    for entetes, corps in _tableaux(t):
        if "Vérifié le" not in entetes[-1]:
            continue
        for cel in corps:
            compte += 1
            if not re.search(r"\d{1,2} \w+\.? 20\d\d", cel[-1]):
                sans_date.append(cel[0][:40])
    assert compte >= 25, f"seulement {compte} faits datés"
    assert not sans_date, sans_date
    assert "## 4. Points à confirmer" in t and "## 5. Folklore" in t
    for url in ("help.openai.com/en/articles/20001207", "openai.com/fr-FR/policies/ad-policies", "developers.openai.com/ads"):
        assert url in t, f"source officielle absente : {url}"
    assert "version 1.6" in t, "version des règles publicitaires absente"


@test("limites du modèle : SKILL.md et faits.md disent 24 et 48, comme le modèle")
def _():
    sys.path.insert(0, str(PACK / "skills" / "chatgpt-ads-skills" / "scripts"))
    import valider_exporter as ve
    lim = ve.lire_modele()["limites"]
    assert lim == {"title": 24, "copy": 48}, lim
    skill = (PACK / "skills" / "chatgpt-ads-skills" / "SKILL.md").read_text(encoding="utf-8")
    assert "titre 24, copie 48" in skill
    for f in textes_md():
        assert not re.search(r"\b(35|67) caractères\b(?![^\n]*(folklore|ne valent pas|sans source|écartées))",
                             f.read_text(encoding="utf-8")), f"limite 35/67 présentée comme règle dans {f.name}"


@test("chaque script répond à --help (code 0) et a une docstring")
def _():
    scripts = [p for s in SKILLS for p in (s / "scripts").glob("*.py")]
    assert scripts
    for p in scripts:
        r = subprocess.run([sys.executable, str(p), "--help"], capture_output=True, text=True)
        assert r.returncode == 0, f"{p.name} --help : code {r.returncode} {r.stderr[-300:]}"
        assert '"""' in p.read_text(encoding="utf-8")[:400], f"{p.name} : docstring absente"


@test("script sans dépendance hors bibliothèque standard")
def _():
    autorises = {"argparse", "datetime", "json", "re", "sys", "unicodedata", "urllib", "zipfile", "pathlib", "xml"}
    for s in SKILLS:
        for p in (s / "scripts").glob("*.py"):
            mods = re.findall(r"^(?:import|from) (\w+)", p.read_text(encoding="utf-8"), re.M)
            assert set(mods) <= autorises, f"{p.name} : {set(mods) - autorises}"


@test("exemple de campagne : prêt selon le script (0 bloquant, 0 attention)")
def _():
    s = PACK / "skills" / "chatgpt-ads-skills"
    p = subprocess.run([sys.executable, str(s / "scripts" / "valider_exporter.py"), "valider",
                        str(s / "assets" / "exemple-campagne.json"), "--aujourdhui", "2026-10-15"],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stdout[-800:]


@test("tests et cas d'éval : B2C, B2B, secteur sensible, et 5 cas au moins")
def _():
    d = json.loads((PACK / "evals" / "evals.json").read_text(encoding="utf-8"))
    cas = d["cas"]
    for s in SKILLS:
        assert list((PACK / "evals" / s.name).glob("test_*.py")), f"{s.name} : aucun test"
        assert sum(1 for c in cas if c["skill"] == s.name) >= 5, f"{s.name} : moins de 5 cas"
    types = {c.get("type") for c in cas}
    assert {"B2C", "B2B", "secteur sensible"} <= types, types
    for c in cas:
        for f in c.get("fichiers", []):
            assert (PACK / "evals" / f).exists(), f"cas {c['id']} : {f} manquant"


@test("modèle de brief : vide sans données, exemple marqué fictif, mêmes sections")
def _():
    for vide in (PACK / "templates").glob("*.md"):
        if vide.name.startswith("exemple-"):
            continue
        ex = PACK / "templates" / f"exemple-{vide.name}"
        assert ex.exists(), f"exemple-{vide.name} manquant"
        tv, te = vide.read_text(encoding="utf-8"), ex.read_text(encoding="utf-8")
        assert "- rempli : non" in tv and ".example" not in tv, vide.name
        assert "Exemple fictif" in te, ex.name
        titres = lambda t: re.findall(r"^## (.+)$", t, re.M)
        assert titres(tv) == titres(te), f"{vide.name} et {ex.name} n'ont pas les mêmes sections"


@test("exemples fictifs : domaines en .example, aucun nom de client réel")
def _():
    interdits = re.compile(r"mondassur|monda'blog", re.I)
    for f in textes_publics():
        t = f.read_text(encoding="utf-8", errors="ignore")
        assert not interdits.search(t), f"nom réel dans {f.relative_to(PACK)}"
    for f in [PACK / "skills" / "chatgpt-ads-skills" / "assets" / "exemple-campagne.json"] + \
            list((PACK / "evals" / "chatgpt-ads-skills" / "fixtures").glob("*")):
        for hote in re.findall(r"https?://([\w.-]+)", f.read_text(encoding="utf-8")):
            assert hote.endswith(".example"), f"{f.name} : domaine réel {hote}"


@test("confidentialité : aucun document d'onboarding repris (fichiers, titres, études de cas)")
def _():
    noms = [p.name.lower() for p in PACK.rglob("*")]
    for interdit in ("scaling_guide", "ads_deck", "chatgpt_ads_deck", "exemple_de_campagne"):
        assert not any(interdit in n for n in noms), interdit
    for f in textes_publics():
        t = f.read_text(encoding="utf-8", errors="ignore").lower()
        for marque in ("scaling guide", "guide de montée en charge", "case study", "étude de cas d'openai"):
            assert marque not in t, f"{marque} dans {f.relative_to(PACK)}"


@test("modèle d'import : celui du pack, à jour, sans le fichier d'OpenAI")
def _():
    noms = [p.name.lower() for p in PACK.rglob("*.xlsx")]
    assert not any("ad_schema" in n for n in noms), noms
    p = subprocess.run([sys.executable, str(PACK / "outils" / "construire_modele.py"), "--verifier"], capture_output=True, text=True)
    assert p.returncode == 0, p.stdout


@test("catégories : le script et references/politiques.md disent la même chose")
def _():
    sys.path.insert(0, str(PACK / "skills" / "chatgpt-ads-skills" / "scripts"))
    import valider_exporter as ve
    t = (PACK / "skills" / "chatgpt-ads-skills" / "references" / "politiques.md").read_text(encoding="utf-8")
    for cat, statut in ve.CATEGORIES.items():
        ligne = next((l for l in t.splitlines() if l.startswith("|") and f"`{cat}`" in l), None)
        assert ligne, f"catégorie {cat} absente de politiques.md"
        attendu = {"autorisee": "autorisée", "restreinte_us": "États-Unis seulement", "interdite": "interdite"}[statut]
        assert attendu in ligne, f"{cat} : « {attendu} » attendu dans politiques.md"


@test("aiguilleur claude.ai : chaque Skill présent y figure, frontmatter valide")
def _():
    t = (PACK / "claude-ai" / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"---\nname: ads-skills\ndescription: >-\n(.*?)\n---\n", t, re.S)
    assert m and len(" ".join(m.group(1).split())) <= 1024
    assert "Pas pour" in m.group(1)
    for s in SKILLS:
        assert f"`{s.name}`" in t, f"{s.name} absent de l'aiguilleur"


@test("manifeste de plugin valide et marketplace à jour")
def _():
    d = json.loads((PACK / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert d["name"] == "ads-skills" and d["license"] == "MIT"
    m = json.loads((PACK.parent / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert any(p["name"] == "ads-skills" and p["source"] == "./ads-skills" for p in m["plugins"])


@test("README : images, liens, version, icônes, captures et visuels conformes (outils/visuels/readme.py)")
def _():
    r = subprocess.run([sys.executable, str(PACK.parent / "outils" / "visuels" / "readme.py"), str(PACK)],
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
