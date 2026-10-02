#!/usr/bin/env python3
"""propager.py : copie le socle commun du pack dans chaque Skill.

Chaque Skill doit fonctionner seul (ZIP claude.ai d'un seul Skill, dossier
copié dans ~/.claude/skills/). Le socle commun est donc copié dans
skills/<nom>/commun/ :

  commun/regles.md, commun/preuves.md, commun/garde_fou.py  → skills/<nom>/commun/
  templates/*.md                                            → skills/<nom>/commun/modeles/

On ne modifie jamais skills/<nom>/commun/ à la main : on modifie commun/ ou
templates/ à la racine du pack, puis on relance ce script.

  python3 outils/propager.py            copie
  python3 outils/propager.py --verifier vérifie que les copies sont identiques (code 1 sinon)
"""

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parent.parent
COMMUN = PACK / "commun"
MODELES = PACK / "templates"


def sources():
    """(chemin source, chemin relatif dans skills/<nom>/commun/)"""
    for f in sorted(COMMUN.iterdir()):
        if f.is_file() and f.suffix in {".md", ".py", ".json"}:
            yield f, Path(f.name)
    for f in sorted(MODELES.glob("*.md")):
        yield f, Path("modeles") / f.name


def skills():
    return sorted(d for d in (PACK / "skills").iterdir() if (d / "SKILL.md").exists())


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--verifier", action="store_true", help="vérifier sans copier")
    a = p.parse_args()

    attendus = list(sources())
    ecarts = []
    for skill in skills():
        cible = skill / "commun"
        noms_attendus = {str(rel) for _, rel in attendus}
        for src, rel in attendus:
            dst = cible / rel
            if a.verifier:
                if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
                    ecarts.append(f"{skill.name}/commun/{rel}")
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        # fichiers en trop (supprimés à la source)
        if cible.exists():
            for f in cible.rglob("*"):
                if f.is_file() and "__pycache__" not in f.parts:
                    rel = str(f.relative_to(cible))
                    if rel not in noms_attendus:
                        if a.verifier:
                            ecarts.append(f"{skill.name}/commun/{rel} (en trop)")
                        else:
                            f.unlink()

    if a.verifier:
        if ecarts:
            print("Socle commun désynchronisé, lance outils/propager.py :")
            for e in ecarts:
                print(f"  · {e}")
            return 1
        print(f"Socle commun identique dans {len(skills())} Skills.")
        return 0
    print(f"Socle commun copié dans {len(skills())} Skills ({len(attendus)} fichiers chacun).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
