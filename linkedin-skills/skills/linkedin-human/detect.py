#!/usr/bin/env python3
"""
detect.py - note un texte en français sur cinq signaux d'écriture IA.

Chaque contrôle va de 0 à 100 : plus c'est haut, plus le texte sonne humain.

  RYTHME     variation de longueur des phrases. Les modèles écrivent égal.
  PRÉCISION  chiffres, noms propres, montants pour 100 mots. L'IA reste vague.
  TICS       densité du lexique tics-ia.json pour 100 mots.
  EMPREINTE  caractères invisibles, tirets cadratins, guillemets anglais,
             espaces fines générées, gras Unicode ou Markdown, apostrophes
             mélangées, pour 1 000 caractères.
  VOIX       pronoms personnels, marques d'oral (« on », « ça », « j' »)
             et structures types (« Ce n'est pas X, c'est Y », « Le résultat ? »...).

Le verdict pèse la moyenne à 60 % et le contrôle le plus faible à 40 % :
un détecteur n'a besoin que d'un signal pour se déclencher.
OK = 70+ sans contrôle sous 55 ; À REVOIR = 50+ ; SIGNALÉ en dessous.

Usage
  python3 detect.py brouillon.txt
  python3 detect.py avant.txt apres.txt      # montre l'écart
  python3 detect.py brouillon.txt --json

Ce sont des heuristiques locales, pas GPTZero, Originality ou Compilatio.
Elles ne promettent aucun verdict de ces outils. Rien n'est envoyé nulle part.

Adapté de detect.py de Jake Schincariol (MIT), réécrit pour le français.
"""

import argparse
import json
import re
import statistics
import sys
import unicodedata

from humanize import LEX, find_flags, load_lexicon, protect_urls

WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿœŒ0-9]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿœŒ]+)?")
SENT_RE = re.compile(r"[^.!?\n]+[.!?…]*")
NUMBERS = re.compile(r"\d+(?:[  .,]\d+)*\s?(?:%|€|k€|M€|K|k|h|min|j|ans?|mois|semaines?|jours?|x)?")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)(?<!\n)\b[A-ZÀÂÉÈÊÎÔÛÇ][a-zà-ÿœ]{2,}\b|\b[A-Z]{2,}[a-z]*\b", re.M)
# Les formes élidées (j', m', t') sont suivies d'une lettre : pas de limite de mot après l'apostrophe.
PRONOUNS = re.compile(r"\b(?:(?:je|me|moi|mon|ma|mes|on|tu|te|toi|ton|ta|tes|vous|votre|vos|nous|notre|nos)\b|[jmt]['’])",
                      re.IGNORECASE)
ORAL = re.compile(r"\b(?:(?:ça|on|bref|du coup|perso|franchement)\b|j['’])", re.IGNORECASE)
STRUCTURE_FAMILIES = {"parallelisme", "revelation", "appat", "tic-linkedin", "meta-annonce", "auto-validation",
                      "conclusion", "anaphore", "connecteurs-en-pluie", "artefact", "flatterie", "posture-didactique"}
CHECKS = ["RYTHME", "PRÉCISION", "TICS", "EMPREINTE", "VOIX"]


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Ramène `value` sur 0-100 : `human` -> 100, `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def check_rythme(text, lex, flags):
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return None, "trop court pour juger (non compté)"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    return scale(cv, human=0.55, machine=0.15), f"variation {cv:.2f} sur {len(lens)} phrases (viser 0,5+)"


def check_precision(text, lex, flags):
    w = words(text)
    if len(w) < 25:
        return None, "trop court pour juger (non compté)"
    body = re.sub(r"#[\wÀ-ÿ]+", "", text)  # les hashtags ne sont pas des faits
    hits = len(NUMBERS.findall(body)) + len(set(PROPER.findall(body)))
    density = hits * 100 / len(w)
    return scale(density, human=6.0, machine=0.5), f"{hits} éléments concrets, {density:.1f} pour 100 mots (viser 4+)"


def check_tics(text, lex, flags):
    w = words(text)
    if not w:
        return 50.0, "vide"
    hits, found = 0, []
    for e in lex["remplacements"]:
        n = len(re.findall(r"(?<![\w])" + re.escape(e["trouver"].strip()).replace(r"\ ", r"\s+"), text, re.IGNORECASE))
        if n:
            hits += n
            found.append(e["trouver"].strip())
    for f in flags:
        if f["famille"] not in STRUCTURE_FAMILIES and f["famille"] not in ("mise-en-forme", "typo-fr", "rythme", "triade"):
            hits += 1
            found.append(f["extrait"].lower().strip(" ,.;:"))
    density = hits * 100 / len(w)
    detail = f"{hits} tic(s), {density:.1f} pour 100 mots"
    if found:
        uniq = sorted(set(found))
        detail += " (" + ", ".join(uniq[:4]) + (", ..." if len(uniq) > 4 else "") + ")"
    return scale(density, human=0.0, machine=4.0), detail


def check_empreinte(text, lex, flags):
    body, _ = protect_urls(text)
    invisible = sum(1 for c in body if unicodedata.category(c) == "Cf" and c != "‍")
    em = body.count("—")
    en = len(re.findall(r"\s–\s", body))
    curly = body.count("“") + body.count("”")
    fine = body.count(" ")
    md = len(re.findall(r"\*\*[^*\n]+\*\*", body))
    ubold = len(re.findall(r"[\U0001D400-\U0001D7FF]{3,}", body))
    apos_mix = 1 if ("'" in body and "’" in body) else 0
    nospace = len(re.findall(r"(?<=[A-Za-zÀ-ÿ])[!?;]", body))
    total = invisible * 4 + em * 2 + en + curly + fine + md * 2 + ubold * 2 + apos_mix * 2 + nospace * 0.5
    per1k = total * 1000 / max(len(body), 1)
    detail = (f"{invisible} invisible(s), {em} tiret(s) cadratin(s), {curly} guillemet(s) anglais, "
              f"{fine} espace(s) fine(s), {md + ubold} gras, {nospace} ponctuation collée")
    return scale(per1k, human=0.0, machine=12.0), detail


def check_voix(text, lex, flags):
    w = words(text)
    if len(w) < 25:
        return None, "trop court pour juger (non compté)"
    per100 = 100 / len(w)
    person = len(PRONOUNS.findall(text)) * per100
    oral = len(ORAL.findall(text)) * per100
    tells = [f for f in flags if f["famille"] in STRUCTURE_FAMILIES]
    score = (scale(person, human=8.0, machine=1.0) * 0.35
             + scale(oral, human=2.5, machine=0.0) * 0.25
             + clamp(100 - len(tells) * 22) * 0.40)
    detail = f"{person:.1f} pronoms et {oral:.1f} marques d'oral pour 100 mots, {len(tells)} structure(s) type"
    if tells:
        detail += " [" + ", ".join(sorted({t['famille'] for t in tells})[:4]) + "]"
    return clamp(score), detail


def run(text, lex):
    flags = find_flags(text, lex)
    fns = [check_rythme, check_precision, check_tics, check_empreinte, check_voix]
    results = {name: fn(text, lex, flags) for name, fn in zip(CHECKS, fns)}
    # Un texte court (note d'invitation, commentaire) n'a pas assez de phrases pour
    # juger le rythme ou la voix : ces contrôles sont exclus du verdict, pas notés 50.
    scores = [results[c][0] for c in CHECKS if results[c][0] is not None]
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "OK" if overall >= 70 and min(scores) >= 55 else ("À REVOIR" if overall >= 50 else "SIGNALÉ")
    return results, overall, verdict


def bar(score, width=24):
    filled = int(round(score / 100 * width))
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    if label:
        out.write(f"\n{label}\n")
    for name in CHECKS:
        score, detail = results[name]
        shown = f"{bar(score)} {score:5.1f}" if score is not None else f"{'-' * 24}   n/a"
        out.write(f"  {name:<10} {shown}\n             {detail}\n")
    out.write("  " + "-" * 60 + "\n")
    out.write(f"  SCORE HUMAIN {bar(overall)} {overall:5.1f}   {verdict}\n")
    weakest = min((c for c in CHECKS if results[c][0] is not None), key=lambda c: results[c][0])
    if verdict != "OK":
        out.write(f"\n  Signal le plus faible : {weakest}. Commence par lui.\n")


def main():
    ap = argparse.ArgumentParser(description="Note un texte français sur cinq signaux d'écriture IA.")
    ap.add_argument("fichiers", nargs="+", help="un fichier, ou deux (avant, après) pour voir l'écart")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexique", default=LEX)
    args = ap.parse_args()
    lex = load_lexicon(args.lexique)

    runs = []
    for path in args.fichiers[:2]:
        text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        runs.append((path, *run(text, lex)))

    if args.json:
        json.dump([{"fichier": p, "score": round(o, 1), "verdict": v,
                    "controles": {k: {"score": None if s is None else round(s, 1), "detail": d} for k, (s, d) in r.items()}}
                   for p, r, o, v in runs], sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return
    for path, results, overall, verdict in runs:
        render(results, overall, verdict, label=path if len(runs) > 1 else None)
    if len(runs) == 2:
        delta = runs[1][2] - runs[0][2]
        print(f"\n  ÉCART  {delta:+.1f} points ({runs[0][3]} -> {runs[1][3]})")


if __name__ == "__main__":
    main()
