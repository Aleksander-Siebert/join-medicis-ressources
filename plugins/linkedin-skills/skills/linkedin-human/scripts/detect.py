#!/usr/bin/env python3
"""
detect.py : note un texte en français sur six signaux d'écriture IA (version 2).

Chaque contrôle va de 0 à 100 : plus c'est haut, plus le texte se lit humain.

  FORENSIQUE  fuites de modèle qu'aucun humain ne produit (oaicite, « En tant
              qu'IA », gabarit non rempli, « Voici une version… »). Une seule
              suffit : verdict SIGNALÉ.
  DENSITÉ     marqueurs PAR PARAGRAPHE (lexique, verbes vides, faux soutenu,
              calques, révélations, parallélismes, sincérité annoncée…).
              3 ou plus = réécrire le paragraphe ; un marqueur « fort » = le
              corriger ; un marqueur faible isolé = rien.
  RYTHME      ne récompense PAS la variation. Signale le paragraphe plat
              (4 phrases ou plus de même longueur, sans subordonnée) et la
              variation fabriquée (staccato, plus de 2 fragments, alternance
              long/court mécanique).
  CONCRET     chiffres, noms propres, montants pour 100 mots.
  EMPREINTE   invisibles, tirets cadratins, guillemets anglais, gras, pour
              1 000 caractères.
  VOIX        pronoms, marques d'oral, structures types.

Verdict : moyenne à 60% et contrôle le plus faible à 40%. OK = 70 et plus sans
contrôle sous 55 ; À REVOIR = 50 et plus ; SIGNALÉ sinon, ou dès une fuite
forensique.

Avec deux fichiers (avant, après), le script ajoute la GARDE ANTI-SUR-CORRECTION :
la réécriture a-t-elle ajouté du staccato, une annonce de sincérité, perdu tous
les « je », perdu des éléments concrets ? (La vérification des faits ajoutés
ou perdus est faite par fidelite.py.)

Usage
  python3 detect.py brouillon.txt
  python3 detect.py avant.txt apres.txt
  python3 detect.py brouillon.txt --niveau esthetique --contexte ~/.claude/linkedin/contexte.md
  python3 detect.py brouillon.txt --json

Codes de sortie : 0 OK · 2 À REVOIR · 3 SIGNALÉ (sur le dernier fichier) · 1 erreur.

Ce sont des heuristiques locales, pas GPTZero, Pangram ou Compilatio. Elles
ne promettent aucun verdict de ces outils. Rien n'est envoyé nulle part.

Adapté de detect.py de Jake Schincariol (MIT) ; doctrine de densité et de
rythme d'après Serge Bulaev (linkedin-humanizer V3, MIT).
"""

import argparse
import json
import re
import statistics
import sys
import unicodedata

from humanize import LEX, load_lexicon, protect_urls
from marqueurs import densite, find_flags, formulations_retirees, rythme

WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿœŒ0-9]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿœŒ]+)?")
NUMBERS = re.compile(r"\d+(?:[ \u00a0\u202f.,]\d+)*\s?(?:%|€|k€|M€|K|k|h|min|j|ans?|mois|semaines?|jours?|x)?")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)(?<!\n)\b[A-ZÀÂÉÈÊÎÔÛÇ][a-zà-ÿœ]{2,}\b|\b[A-Z]{2,}[a-z]*\b", re.M)
PRONOUNS = re.compile(r"\b(?:(?:je|me|moi|mon|ma|mes|on|tu|te|toi|ton|ta|tes|vous|votre|vos|nous|notre|nos)\b|[jmt]['’])",
                      re.IGNORECASE)
ORAL = re.compile(r"\b(?:(?:ça|on|bref|du coup|perso|franchement)\b|j['’])", re.IGNORECASE)
STRUCTURES = {"parallelisme", "revelation", "appat", "tic-linkedin", "meta-annonce", "auto-validation",
              "conclusion", "anaphore", "connecteurs-en-pluie", "artefact", "flatterie", "posture-didactique",
              "sincerite", "staccato", "linkedin-2026"}
CHECKS = ["FORENSIQUE", "DENSITÉ", "RYTHME", "CONCRET", "EMPREINTE", "VOIX"]


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def words(text):
    return WORD_RE.findall(text)


def check_forensique(text, flags, dens, ryt):
    fuites = [f for f in flags if f["famille"] == "forensique"]
    if not fuites:
        return 100.0, "aucune fuite de modèle"
    return 0.0, f"{len(fuites)} fuite(s) : " + ", ".join(f["extrait"] for f in fuites[:3])


def check_densite(text, flags, dens, ryt):
    reecrire = [d for d in dens if d["action"] == "RÉÉCRIRE LE PARAGRAPHE"]
    remplacer = [d for d in dens if d["action"] == "REMPLACER"]
    plus_faible = [d for d in dens if d["action"] == "REMPLACER LE PLUS FAIBLE"]
    score = 100 - 30 * len(reecrire) - 15 * len(remplacer) - 8 * len(plus_faible)
    total = sum(d["marqueurs"] for d in dens)
    detail = (f"{total} marqueur(s) sur {len(dens)} paragraphe(s) : {len(reecrire)} à réécrire, "
              f"{len(remplacer)} avec un marqueur fort, {len(plus_faible)} à 2 marqueurs")
    return clamp(score), detail


def check_rythme(text, flags, dens, ryt):
    if ryt["phrases"] < 4:
        return None, "trop court pour juger (non compté)"
    pen = 0
    for p in ryt["problemes"]:
        pen += {"paragraphe plat": 25, "staccato": 15, "fragments": 15, "alternance fabriquée": 20}.get(p["type"], 10)
    if not ryt["problemes"]:
        return 100.0, f"{ryt['phrases']} phrases, ni paragraphe plat ni variation fabriquée"
    types = sorted({p["type"] for p in ryt["problemes"]})
    return clamp(100 - pen), f"{len(ryt['problemes'])} problème(s) : " + ", ".join(types)


def check_concret(text, flags, dens, ryt):
    w = words(text)
    if len(w) < 25:
        return None, "trop court pour juger (non compté)"
    body = re.sub(r"#[\wÀ-ÿ]+", "", text)
    hits = len(NUMBERS.findall(body)) + len(set(PROPER.findall(body)))
    density = hits * 100 / len(w)
    return scale(density, human=6.0, machine=0.5), f"{hits} éléments concrets, {density:.1f} pour 100 mots (viser 4+)"


def check_empreinte(text, flags, dens, ryt):
    body, _ = protect_urls(text)
    invisible = sum(1 for c in body if unicodedata.category(c) == "Cf" and c != "‍")
    em = body.count("—")
    en = len(re.findall(r"\s–\s", body))
    curly = body.count("“") + body.count("”")
    fine = body.count("\u202f")
    md = len(re.findall(r"\*\*[^*\n]+\*\*", body))
    ubold = len(re.findall(r"[\U0001D400-\U0001D7FF]{3,}", body))
    apos_mix = 1 if ("'" in body and "’" in body) else 0
    nospace = len(re.findall(r"(?<=[A-Za-zÀ-ÿ])[!?;]", body))
    total = invisible * 4 + em * 2 + en + curly + fine + md * 2 + ubold * 2 + apos_mix * 2 + nospace * 0.5
    per1k = total * 1000 / max(len(body), 1)
    detail = (f"{invisible} invisible(s), {em} tiret(s) cadratin(s), {curly} guillemet(s) anglais, "
              f"{fine} espace(s) fine(s), {md + ubold} gras, {nospace} ponctuation collée")
    return scale(per1k, human=0.0, machine=12.0), detail


def check_voix(text, flags, dens, ryt):
    w = words(text)
    if len(w) < 25:
        return None, "trop court pour juger (non compté)"
    per100 = 100 / len(w)
    person = len(PRONOUNS.findall(text)) * per100
    oral = len(ORAL.findall(text)) * per100
    tells = [f for f in flags if f["famille"] in STRUCTURES]
    score = (scale(person, human=8.0, machine=1.0) * 0.35
             + scale(oral, human=2.5, machine=0.0) * 0.25
             + clamp(100 - len(tells) * 22) * 0.40)
    detail = f"{person:.1f} pronoms et {oral:.1f} marques d'oral pour 100 mots, {len(tells)} structure(s) type"
    if tells:
        detail += " [" + ", ".join(sorted({t['famille'] for t in tells})[:4]) + "]"
    return clamp(score), detail


def run(text, lex, niveau="strict", retirees=None):
    flags = find_flags(text, lex, niveau, retirees)
    dens = densite(text, flags)
    ryt = rythme(text, flags)
    fns = [check_forensique, check_densite, check_rythme, check_concret, check_empreinte, check_voix]
    results = {name: fn(text, flags, dens, ryt) for name, fn in zip(CHECKS, fns)}
    scores = [results[c][0] for c in CHECKS if results[c][0] is not None]
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    if results["FORENSIQUE"][0] == 0:
        verdict = "SIGNALÉ"
    else:
        verdict = "OK" if overall >= 70 and min(scores) >= 55 else ("À REVOIR" if overall >= 50 else "SIGNALÉ")
    return results, overall, verdict, {"flags": flags, "densite": dens, "rythme": ryt}


LECTURE = {"OK": "se lit humain", "À REVOIR": "mitigé", "SIGNALÉ": "se lit IA"}


def garde_sur_correction(avant, apres):
    """Pass 4 automatisée : ce que la réécriture a introduit ou perdu."""
    alertes = []
    fa = {f["famille"] for f in avant["flags"]}
    for fam, msg in (("staccato", "La réécriture a ajouté du staccato (fragments mis en scène)."),
                     ("sincerite", "La réécriture a ajouté une annonce de sincérité ou une précaution."),
                     ("revelation", "La réécriture a ajouté un « pont de révélation »."),
                     ("parallelisme", "La réécriture a ajouté un parallélisme « pas X, mais Y ».")):
        if fam not in fa and any(f["famille"] == fam for f in apres["flags"]):
            alertes.append(msg)
    if any(p["type"] == "alternance fabriquée" for p in apres["rythme"]["problemes"]) and \
            not any(p["type"] == "alternance fabriquée" for p in avant["rythme"]["problemes"]):
        alertes.append("La réécriture alterne long/court mécaniquement : empreinte des humaniseurs.")
    if avant["je"] > 0 and apres["je"] == 0:
        alertes.append("Tous les « je » ont disparu : la voix de l'auteur est aplatie.")
    if apres["concret"] < avant["concret"]:
        alertes.append(f"Éléments concrets en baisse ({avant['concret']} → {apres['concret']}) : vérifie avec fidelite.py.")
    return alertes


def bar(score, width=24):
    filled = int(round(score / 100 * width))
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, extra, label=None, out=sys.stdout):
    if label:
        out.write(f"\n{label}\n")
    for name in CHECKS:
        score, detail = results[name]
        shown = f"{bar(score)} {score:5.1f}" if score is not None else f"{'-' * 24}   n/a"
        out.write(f"  {name:<10} {shown}\n             {detail}\n")
    out.write("  " + "-" * 60 + "\n")
    out.write(f"  SCORE HUMAIN {bar(overall)} {overall:5.1f}   {verdict} ({LECTURE[verdict]})\n")
    actions = [d for d in extra["densite"] if d["action"] != "LAISSER"]
    if actions:
        out.write("\n  Paragraphes à reprendre :\n")
        for d in actions:
            out.write(f"    §{d['paragraphe']} (l.{d['ligne']}) {d['action']} · {d['marqueurs']} marqueur(s) : "
                      + ", ".join(f"« {e} »" for e in d["extraits"][:3]) + "\n")
    if extra["rythme"]["problemes"]:
        out.write("\n  Rythme :\n")
        for p in extra["rythme"]["problemes"]:
            ou = f"l.{p['ligne']} " if p["ligne"] else ""
            out.write(f"    {ou}{p['type']} : {p['detail']}\n      -> {p['conseil']}\n")
    if verdict != "OK":
        weakest = min((c for c in CHECKS if results[c][0] is not None), key=lambda c: results[c][0])
        out.write(f"\n  Signal le plus faible : {weakest}. Commence par lui.\n")


def resume(text, extra):
    return {"flags": extra["flags"], "rythme": extra["rythme"],
            "je": len(re.findall(r"\b(?:je|j['’]|moi|mon|ma|mes)\b", text, re.I)),
            "concret": len(NUMBERS.findall(text)) + len(set(PROPER.findall(text)))}


def main():
    ap = argparse.ArgumentParser(description="Note un texte français sur six signaux d'écriture IA.")
    ap.add_argument("fichiers", nargs="+", help="un fichier, ou deux (avant, après) pour voir l'écart")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexique", default=LEX)
    ap.add_argument("--niveau", choices=["forensique", "strict", "esthetique"], default="strict")
    ap.add_argument("--contexte", help="contexte.md : signale les formulations retirées")
    args = ap.parse_args()
    lex = load_lexicon(args.lexique)
    retirees = formulations_retirees(args.contexte)

    runs = []
    for path in args.fichiers[:2]:
        try:
            text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        except OSError as err:
            print(f"Erreur : {err}", file=sys.stderr)
            sys.exit(1)
        results, overall, verdict, extra = run(text, lex, args.niveau, retirees)
        runs.append((path, text, results, overall, verdict, extra))

    alertes = []
    if len(runs) == 2:
        alertes = garde_sur_correction(resume(runs[0][1], runs[0][5]), resume(runs[1][1], runs[1][5]))

    if args.json:
        json.dump({"niveau": args.niveau, "resultats": [
            {"fichier": p, "score": round(o, 1), "verdict": v, "lecture": LECTURE[v],
             "controles": {k: {"score": None if s is None else round(s, 1), "detail": d} for k, (s, d) in r.items()},
             "densite": e["densite"], "rythme": e["rythme"]["problemes"],
             "signalements": [{k: f[k] for k in f if k != "debut"} for f in e["flags"]]}
            for p, _, r, o, v, e in runs], "sur_correction": alertes},
            sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        for path, _, results, overall, verdict, extra in runs:
            render(results, overall, verdict, extra, label=path if len(runs) > 1 else None)
        if len(runs) == 2:
            delta = runs[1][3] - runs[0][3]
            print(f"\n  ÉCART  {delta:+.1f} points ({runs[0][4]} -> {runs[1][4]})")
            if alertes:
                print("\n  GARDE ANTI-SUR-CORRECTION :")
                for a in alertes:
                    print(f"    ! {a}")
            else:
                print("  Garde anti-sur-correction : rien à signaler.")
    sys.exit({"OK": 0, "À REVOIR": 2, "SIGNALÉ": 3}[runs[-1][4]])


if __name__ == "__main__":
    main()
