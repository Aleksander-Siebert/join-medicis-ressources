#!/usr/bin/env python3
"""
noter.py - vérifie les attentes [auto] de evals.json sur deux dossiers de sorties.

  python3 noter.py <dossier_reference> <dossier_v1>

Chaque dossier contient case-N.md (réponse complète) et, pour les textes à
coller sur LinkedIn, case-N-final.txt. Les attentes non automatiques se
relisent à la main.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "skills", "linkedin-human"))
from detect import run  # noqa: E402
from humanize import load_lexicon  # noqa: E402

LEX = load_lexicon()
OPENERS = re.compile(r"^\s*(?:\[[^\]]*\]\s*)?(?:Super post|J'adore|Tellement vrai|Merci pour ce partage|Great post|Love this)", re.I | re.M)


def read(folder, name):
    p = os.path.join(folder, name)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def score(text):
    if not text.strip():
        return None
    _, overall, verdict = run(text, LEX)
    return f"{overall:.1f} {verdict}"


def typo_fr(text):
    """Ponctuation double collée à un mot : « mois! », « Résultat: »."""
    return len(re.findall(r"(?<=[A-Za-zÀ-ÿ])[!?;]|(?<=[A-Za-zÀ-ÿ]):(?=\s)", text))


def checks(folder):
    out = {}
    f1 = read(folder, "case-1-final.txt")
    out["1 · score detect.py"] = score(f1)
    out["1 · tirets cadratins"] = f1.count("—") if f1 else None
    out["1 · ponctuation collée"] = typo_fr(f1) if f1 else None
    out["1 · hashtags"] = len(re.findall(r"#\w", f1)) if f1 else None
    f3 = read(folder, "case-3-final.txt")
    src = read(os.path.join(HERE, "linkedin-human"), "brouillon-ia.txt")
    out["3 · score brouillon -> final"] = f"{score(src)} -> {score(f3)}" if f3 else None
    out["3 · ponctuation collée"] = typo_fr(f3) if f3 else None
    out["3 · guillemets anglais"] = (f3.count("“") + f3.count("”") + f3.count('"')) if f3 else None
    c4 = read(folder, "case-4.md") + read(folder, "case-4-final.txt")
    out["4 · ouverture interdite"] = len(OPENERS.findall(c4)) if c4 else None
    f6 = read(folder, "case-6-final.txt") or read(folder, "case-6.md")
    note = f6.strip().split("\n\n")[0] if f6 else ""
    out["6 · longueur de la note"] = len(note) if note else None
    c7 = read(folder, "case-7.md")
    out["7 · URL avec f_TPR=r3600"] = bool(re.search(r"f_TPR=r3600", c7))
    out["7 · URL avec sortBy=DD"] = bool(re.search(r"sortBy=DD", c7))
    out["7 · opérateurs en minuscules"] = len(re.findall(r'(?<!")\b(?:or|and|not)\b(?!")', re.sub(r'"[^"]*"', "", c7))) if c7 else None
    c8 = read(folder, "case-8.md")
    out["8 · mentionne août"] = bool(re.search(r"août", c8, re.I))
    return out


def main():
    ref, v1 = sys.argv[1], sys.argv[2]
    a, b = checks(ref), checks(v1)
    width = max(len(k) for k in a)
    print(f"{'contrôle':<{width}}  {'référence':>22}  {'v1':>22}")
    for k in a:
        print(f"{k:<{width}}  {str(a[k]):>22}  {str(b[k]):>22}")


if __name__ == "__main__":
    main()
