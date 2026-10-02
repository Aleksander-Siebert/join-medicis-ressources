#!/usr/bin/env python3
"""Tests hors ligne des scripts du pack GEO. Lancer : python3 test_geo.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..", "..", "skills")
for d in ("geo-citability", "geo-crawlers", "geo-visibility"):
    sys.path.insert(0, os.path.join(SK, d))

import citability  # noqa: E402
import crawlers  # noqa: E402
import visibilite  # noqa: E402


def f(n):
    return os.path.join(HERE, n)


def test_citabilite_distingue_bon_et_mauvais_passage():
    r = citability.analyse(open(f("page.md"), encoding="utf-8").read(), "md")
    bon = next(b for b in r["sections"] if b["titre"].startswith("Qu'est-ce"))
    assert bon["score"] >= 70, bon
    assert bon["notes"]["originalite"] > 0 and bon["notes"]["donnees"] > 0


def test_citabilite_ignore_les_sections_trop_courtes():
    r = citability.analyse(open(f("page.md"), encoding="utf-8").read(), "md")
    assert all(b["titre"] != "Ensuite" for b in r["sections"])


def test_citabilite_html():
    html = "<html><body><h2>Combien coûte la CFE ?</h2><p>La cotisation CFE dépend de l'âge et des revenus, selon le barème publié sur cfe.fr chaque année en janvier. Pour un adulte de 40 ans, elle se calcule par trimestre et couvre les soins remboursés sur la base des tarifs français, hors dépassements.</p></body></html>"
    r = citability.analyse(html, "html")
    assert r["sections"] and r["sections"][0]["notes"]["reponse"] >= 45, r


def test_robots_strategies():
    txt = "User-agent: GPTBot\nDisallow: /\n\nUser-agent: *\nAllow: /\n"
    bots, se = crawlers.robots_rules("https://a.fr", txt, ["/"])
    etat = {b["robot"]: b["acces"]["/"] for b in bots}
    assert etat["GPTBot"] is False and etat["OAI-SearchBot"] is True and etat["ClaudeBot"] is True
    assert all(s["acces"]["/"] for s in se)
    eq = crawlers.propose_robots("equilibre")
    assert "User-agent: GPTBot\nDisallow: /" in eq and "User-agent: OAI-SearchBot\nAllow: /" in eq


def test_llms_txt():
    ok = crawlers.check_llms("# Assurly\n\n> Courtier en assurance santé internationale.\n\n## Guides\n- [CFE](https://a.fr/cfe): la CFE en bref\n")
    assert ok["problemes"] == [] and ok["liens"] == 1
    ko = crawlers.check_llms("Bienvenue sur notre site")
    assert len(ko["problemes"]) == 4


def test_part_de_voix():
    items = visibilite.parse(f("reponses.txt"))
    assert len(items) == 3
    r = visibilite.analyse(items, "Assurly", ["assurly.example"], ["April International", "Allianz Care"])
    t = r["TOTAL"]
    assert t["presence"] == 67 and r["Perplexity"]["presence"] == 100 and r["ChatGPT"]["rang_moyen"] == 3.0
    assert "service-public.fr" in t["domaines"] and "cfe.fr" in t["domaines"]
    assert t["marques"]["Assurly"] >= 3


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok      {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"ÉCHEC   {t.__name__}  {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} tests passés")
    sys.exit(1 if failed else 0)
