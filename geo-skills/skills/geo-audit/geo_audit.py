#!/usr/bin/env python3
"""
geo_audit.py - score GEO d'une page, mesuré là où c'est mesurable.

Six catégories, pondération reprise de geo-seo-claude (MIT) :

  Citabilité        25%  mesurée (citability.py)
  Marque / mentions 20%  à évaluer par le Skill (geo-mentions, geo-visibility)
  E-E-A-T           20%  à évaluer par le Skill (auteur, sources, expérience)
  Technique         15%  mesurée (robots d'IA, directives, contenu sans JS, llms.txt)
  Données structurées 10% mesurée (types JSON-LD présents)
  Plateformes       10%  à évaluer par le Skill (geo-visibility)

Le script calcule les trois catégories mesurables et un score partiel ; les
trois autres se passent en option quand le Skill les a évaluées :

    python3 geo_audit.py https://www.site.fr/guide/
    python3 geo_audit.py https://www.site.fr/guide/ --marque 40 --eeat 65 --plateformes 30

Sans ces options, le score affiché est partiel et le dit.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for d in ("geo-citability", "geo-crawlers"):
    sys.path.insert(0, os.path.join(HERE, "..", d))
try:
    import citability
    import crawlers
except ImportError:
    sys.exit("geo_audit.py a besoin de geo-citability/citability.py et geo-crawlers/crawlers.py (installez le pack complet).")

WEIGHTS = {"citabilite": 0.25, "marque": 0.20, "eeat": 0.20, "technique": 0.15, "schema": 0.10, "plateformes": 0.10}
USEFUL_TYPES = {"Organization", "LocalBusiness", "Person", "Article", "BlogPosting", "NewsArticle", "FAQPage",
                "HowTo", "Product", "Offer", "BreadcrumbList", "WebSite", "Service", "Review", "AggregateRating"}


def schema_types(html):
    types = set()
    for block in re.findall(r'(?is)<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        stack = [data]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                t = x.get("@type")
                types.update(t if isinstance(t, list) else [t] if t else [])
                stack += list(x.values())
            elif isinstance(x, list):
                stack += x
    return types


def score_technique(cr):
    s, notes = 0, []
    search_ok = [b for b in cr["robots_ia"] if b["role"] in ("recherche", "utilisateur")]
    allowed = sum(1 for b in search_ok if all(b["acces"].values()))
    s += round(45 * allowed / max(len(search_ok), 1))
    if allowed < len(search_ok):
        notes.append(f"{len(search_ok) - allowed} robot(s) de recherche ou d'utilisateur bloqué(s)")
    if all(all(e["acces"].values()) for e in cr["moteurs"]):
        s += 20
    else:
        notes.append("Googlebot ou Bingbot bloqué")
    page = cr["page"]
    if not page.get("erreur"):
        if not (page["noindex"] or page["noai"]):
            s += 15
        else:
            notes.append("directive noindex ou noai sur la page")
        if page["mots_dans_html"] >= 150:
            s += 15
        else:
            notes.append("contenu peu lisible sans JavaScript")
    if cr["llms_txt"] and not cr["llms_txt"]["problemes"]:
        s += 5
    return min(s, 100), notes


def score_schema(types):
    useful = types & USEFUL_TYPES
    s = min(len(useful) * 20, 80)
    if {"Person"} & useful and {"Article", "BlogPosting", "NewsArticle"} & useful:
        s += 20  # article attribué à un auteur
    return min(s, 100), sorted(useful)


def main():
    ap = argparse.ArgumentParser(description="Score GEO d'une page (partiel si tout n'est pas évalué).")
    ap.add_argument("url")
    ap.add_argument("--marque", type=int, help="score marque / mentions (0-100), évalué par le Skill")
    ap.add_argument("--eeat", type=int, help="score E-E-A-T (0-100), évalué par le Skill")
    ap.add_argument("--plateformes", type=int, help="score plateformes (0-100), évalué par le Skill")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    html, _ = citability.load(args.url)
    cit = citability.analyse(html, "html")
    cr = crawlers.analyse(args.url, [])
    tech, tech_notes = score_technique(cr)
    sch, sch_types = score_schema(schema_types(html))
    scores = {"citabilite": cit["score_page"], "technique": tech, "schema": sch,
              "marque": args.marque, "eeat": args.eeat, "plateformes": args.plateformes}
    known = {k: v for k, v in scores.items() if v is not None}
    wsum = sum(WEIGHTS[k] for k in known)
    total = round(sum(WEIGHTS[k] * v for k, v in known.items()) / wsum) if wsum else 0
    partiel = len(known) < len(WEIGHTS)
    res = {"url": args.url, "score": total, "partiel": partiel, "categories": scores,
           "technique": tech_notes, "schema_types": sch_types,
           "sections_faibles": sorted(cit["sections"], key=lambda b: b["score"])[:3]}
    if args.json:
        json.dump(res, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    label = f"score partiel sur {len(known)} catégories sur 6" if partiel else "score complet"
    print(f"AUDIT GEO · {args.url} · {total}/100 ({label})")
    noms = {"citabilite": "Citabilité", "marque": "Marque / mentions", "eeat": "E-E-A-T", "technique": "Technique",
            "schema": "Données structurées", "plateformes": "Plateformes"}
    for k, w in WEIGHTS.items():
        v = scores[k]
        print(f"  {noms[k]:<22} {int(w * 100):>3}%  {('%d/100' % v) if v is not None else 'à évaluer'}")
    for n in tech_notes:
        print(f"    technique : {n}")
    print(f"    schema : {', '.join(sch_types) or 'aucun type utile'}")
    print("  Sections les moins citables :")
    for b in res["sections_faibles"]:
        print(f"    {b['score']:>3}  {b['titre'][:70]}")


if __name__ == "__main__":
    main()
