#!/usr/bin/env python3
"""Contrôle du README d'un pack (Python 3, sans dépendance).

  python3 outils/visuels/readme.py linkedin-skills [seo-skills …]

Pour chaque pack : chaque image et chaque lien local du README existent (les
emplacements en commentaire HTML, comme les GIF à venir, sont ignorés) ; le
badge de version et le tableau des versions suivent .claude-plugin/plugin.json ;
chaque Skill a son icône ; aucun tiret cadratin ; captures et visuels
conformes aux scripts (capture.py et visuels.py --verifier).

Code 0 si tout va bien, 1 sinon (les écarts sont listés).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parents[1]


def controler(pack):
    """Liste des écarts pour un dossier de pack."""
    ecarts = []
    readme_brut = (pack / "README.md").read_text(encoding="utf-8")
    readme = re.sub(r"<!--.*?-->", "", readme_brut, flags=re.S)
    for cible in re.findall(r'(?:src|href)="(?!https?:|#|mailto:)([^"]+)"', readme) + \
            re.findall(r"\]\((?!https?:|#|mailto:)([^)]+)\)", readme):
        if not (pack / cible).exists():
            ecarts.append(f"lien ou image introuvable : {cible}")
    manifeste = pack / ".claude-plugin" / "plugin.json"
    if manifeste.exists():
        version = json.loads(manifeste.read_text(encoding="utf-8"))["version"]
        if f"version-{version}-" not in readme:
            ecarts.append(f"badge de version différent de {version}")
        if f"**{version}**" not in readme:
            ecarts.append(f"version {version} absente du tableau des versions")
    if "—" in readme_brut:
        ecarts.append("tiret cadratin dans le README")
    skills = pack / "skills"
    if skills.is_dir():
        for d in sorted(skills.iterdir()):
            if (d / "SKILL.md").exists() and f"docs/media/icones/{d.name}.svg" not in readme:
                ecarts.append(f"{d.name} : pas d'icône dans le README")
    media = pack / "docs" / "media"
    for outil, manifeste_media, options in (("capture.py", media / "captures.json", ["--manifeste"]),
                                            ("visuels.py", media / "visuels.json", [])):
        if not manifeste_media.exists():
            continue
        r = subprocess.run([sys.executable, str(ICI / outil), *options, str(manifeste_media), "--verifier"],
                           capture_output=True, text=True)
        if r.returncode:
            ecarts.append(f"{outil} : {(r.stdout + r.stderr).strip()[-300:]} (relancer sans --verifier)")
    return ecarts


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("packs", nargs="+", help="dossiers de packs (ex. linkedin-skills) ou « . » pour la racine")
    a = ap.parse_args(argv)
    total = 0
    for nom in a.packs:
        pack = (RACINE / nom).resolve() if not Path(nom).is_absolute() else Path(nom)
        ecarts = controler(pack)
        total += len(ecarts)
        print(f"{pack.name} : " + ("README conforme" if not ecarts else f"{len(ecarts)} écart(s)"))
        for e in ecarts:
            print(f"  - {e}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
