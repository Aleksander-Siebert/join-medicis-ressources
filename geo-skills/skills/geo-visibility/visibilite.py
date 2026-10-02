#!/usr/bin/env python3
"""
visibilite.py - part de voix de votre marque dans les réponses des IA.

Vous posez les prompts (générés par le Skill) dans ChatGPT, Perplexity,
Gemini, Mistral, Claude ou Google AI Mode, et collez les réponses dans un
fichier texte, chacune précédée d'une ligne d'en-tête :

    === ChatGPT | Quelle assurance santé choisir pour s'expatrier en famille ?
    (réponse collée)
    === Perplexity | Quelle assurance santé choisir pour s'expatrier en famille ?
    (réponse collée)

Puis :

    python3 visibilite.py reponses.txt --marque "Assurly" --alias "assurly.example" \\
        --concurrent "April International" --concurrent "Allianz Care" --concurrent "Cigna"

Mesure, par plateforme et au total : taux de présence de la marque, rang de
première mention parmi les marques suivies, part de voix (mentions de la
marque / mentions de toutes les marques suivies), domaines cités comme
sources. Comparez deux mois avec --avant reponses-septembre.txt.
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlsplit


def parse(path):
    raw = open(path, encoding="utf-8").read()
    items = []
    for m in re.finditer(r"(?ms)^===\s*([^|\n]+?)\s*\|\s*(.+?)\s*\n(.*?)(?=^===|\Z)", raw):
        items.append({"plateforme": m.group(1).strip(), "prompt": m.group(2).strip(), "reponse": m.group(3).strip()})
    return items


def mentions(text, names):
    """Positions de la première mention de chaque marque (insensible à la casse et aux accents simples)."""
    low = text.lower()
    out = {}
    for label, variants in names.items():
        pos = [low.find(v.lower()) for v in variants if v and low.find(v.lower()) >= 0]
        if pos:
            out[label] = (min(pos), sum(low.count(v.lower()) for v in variants if v))
    return out


def domains(text):
    urls = re.findall(r"https?://[^\s)\]>\"']+", text)
    bare = re.findall(r"\b(?:[a-z0-9-]+\.)+(?:fr|com|org|net|eu|be|ch|ca|io|gouv\.fr)\b", text.lower())
    ds = [urlsplit(u).netloc.lower().removeprefix("www.") for u in urls] + [b.removeprefix("www.") for b in bare]
    return [d for d in ds if d]


def analyse(items, marque, alias, concurrents):
    names = {marque: [marque] + alias}
    for c in concurrents:
        names[c] = [c]
    per = defaultdict(lambda: {"prompts": 0, "presence": 0, "rangs": [], "mentions": Counter(), "domaines": Counter()})
    for it in items:
        for key in (it["plateforme"], "TOTAL"):
            p = per[key]
            p["prompts"] += 1
            found = mentions(it["reponse"], names)
            for lab, (_, cnt) in found.items():
                p["mentions"][lab] += cnt
            if marque in found:
                p["presence"] += 1
                order = sorted(found, key=lambda k: found[k][0])
                p["rangs"].append(order.index(marque) + 1)
            p["domaines"].update(set(domains(it["reponse"])))
    out = {}
    for k, p in per.items():
        total_m = sum(p["mentions"].values())
        out[k] = {
            "prompts": p["prompts"],
            "presence": round(100 * p["presence"] / p["prompts"]) if p["prompts"] else 0,
            "rang_moyen": round(sum(p["rangs"]) / len(p["rangs"]), 1) if p["rangs"] else None,
            "part_de_voix": round(100 * p["mentions"][marque] / total_m) if total_m else 0,
            "marques": dict(p["mentions"].most_common()),
            "domaines": dict(p["domaines"].most_common(10)),
        }
    return out


def render(r, avant=None):
    order = sorted([k for k in r if k != "TOTAL"]) + ["TOTAL"]
    print(f"{'PLATEFORME':<14}{'PROMPTS':>8}{'PRÉSENCE':>10}{'RANG':>6}{'PART DE VOIX':>14}")
    for k in order:
        v = r[k]
        delta = ""
        if avant and k in avant:
            delta = f"  ({v['part_de_voix'] - avant[k]['part_de_voix']:+d} pts)"
        rang = f"{v['rang_moyen']}" if v["rang_moyen"] else "-"
        print(f"{k:<14}{v['prompts']:>8}{v['presence']:>9}%{rang:>6}{v['part_de_voix']:>13}%{delta}")
    t = r["TOTAL"]
    print("\nMARQUES CITÉES (mentions) : " + ", ".join(f"{m} {n}" for m, n in t["marques"].items()))
    if t["domaines"]:
        print("SOURCES CITÉES (nombre de réponses) : " + ", ".join(f"{d} {n}" for d, n in t["domaines"].items()))


def main():
    ap = argparse.ArgumentParser(description="Part de voix d'une marque dans des réponses d'IA collées.")
    ap.add_argument("reponses")
    ap.add_argument("--marque", required=True)
    ap.add_argument("--alias", action="append", default=[], help="autre nom ou domaine de la marque (répétable)")
    ap.add_argument("--concurrent", action="append", default=[])
    ap.add_argument("--avant", help="fichier de réponses du mois précédent, pour l'écart")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    items = parse(args.reponses)
    if not items:
        sys.exit("Aucune réponse trouvée : chaque réponse doit commencer par « === Plateforme | prompt ».")
    r = analyse(items, args.marque, args.alias, args.concurrent)
    avant = analyse(parse(args.avant), args.marque, args.alias, args.concurrent) if args.avant else None
    if args.json:
        json.dump({"actuel": r, "avant": avant}, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        render(r, avant)


if __name__ == "__main__":
    main()
