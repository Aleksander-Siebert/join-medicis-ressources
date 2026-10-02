#!/usr/bin/env python3
"""Tests hors ligne des scripts du pack SEO. Lancer : python3 test_scripts.py"""
import io
import os
import sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..", "..", "skills")
for d in ("seo-maillage", "seo-veille", "seo-audit"):
    sys.path.insert(0, os.path.join(SK, d))

import maillage  # noqa: E402
import onpage  # noqa: E402
import veille  # noqa: E402


def f(name):
    return os.path.join(HERE, name)


def test_maillage_clusters_et_pilier():
    pages = maillage.load_crawl_csv(f("crawl.csv"))
    r = maillage.analyse(pages, maillage.load_traffic(f("gsc-actuel.csv")))
    piliers = {c["pilier"] for c in r["clusters"]}
    assert "https://assurly.example/assurance-sante-expatrie/" in piliers, r["clusters"]
    exp = next(c for c in r["clusters"] if c["pilier"].endswith("/assurance-sante-expatrie/"))
    assert any("choisir-assurance-sante-expatrie" in u for u in exp["pages"])
    assert not any("assurance-etudiant-erasmus" in u for u in exp["pages"]), "étudiant mélangé à expatrié"
    assert "https://assurly.example/mentions-legales/" in r["isolees"]


def test_maillage_cannibalisation():
    pages = maillage.load_crawl_csv(f("crawl.csv"))
    r = maillage.analyse(pages, {})
    paires = {(c["a"], c["b"]) for c in r["cannibalisation"]}
    assert any("assurance-sante-expatrie" in a and "assurance-sante-expatrie" in b for a, b in paires), paires


def test_maillage_le_trafic_favorise_les_hotes_visites():
    pages = maillage.load_crawl_csv(f("crawl.csv"))
    r = maillage.analyse(pages, maillage.load_traffic(f("gsc-actuel.csv")))
    vers_prix = [l for l in r["liens"] if l["cible"].endswith("assurance-sante-expatrie-prix/")]
    assert vers_prix and vers_prix[0]["hote"].endswith("/assurance-sante-expatrie/"), vers_prix[:2]


def test_maillage_hotes_pour_un_nouvel_article():
    pages = maillage.load_crawl_csv(f("crawl.csv"))
    cible = {"title": "Assurance santé pour un PVT au Canada", "texte": "étudiant visa Canada assurance santé PVT"}
    r = maillage.analyse(pages, {}, cible=cible)
    assert r["liens"] and "canada" in r["liens"][0]["hote"], r["liens"]


def test_sitemap_index_local(tmp="sitemap-test.xml"):
    path = f(tmp)
    open(path, "w").write('<?xml version="1.0"?><urlset><url><loc>https://a.fr/x</loc></url><url><loc>https://a.fr/y</loc></url></urlset>')
    try:
        assert maillage.sitemap_urls(path) == ["https://a.fr/x", "https://a.fr/y"]
    finally:
        os.remove(path)


def test_rapport_search_console():
    class A:
        actuel, precedent, top, json = f("gsc-actuel.csv"), f("gsc-precedent.csv"), 5, False
    out = io.StringIO()
    with redirect_stdout(out):
        veille.cmd_rapport(A)
    txt = out.getvalue()
    assert "640 clics contre 585" in txt, txt
    assert txt.index("+120") < txt.index("PERDANTS") < txt.index("-40")
    assert "assurance-etudiant-erasmus" in txt.split("PAGES SANS CLIC")[1]


def test_onpage():
    html = open(f("page.html"), encoding="utf-8").read()
    r = onpage.audit(html, "https://assurly.example/assurance-sante-expatrie/", "assurance santé expatrié")
    st = {c["controle"]: c["statut"] for c in r["controles"]}
    assert st["Title"] == "OK" and st["Meta description"] == "OK" and st["H1"] == "OK"
    assert st["Hiérarchie des titres"] == "À REVOIR" and st["Images sans alt"] == "À REVOIR"
    assert st["Données structurées"] == "OK"
    assert st["Mot-clé « assurance santé expatrié »"] == "OK"
    liens = next(c for c in r["controles"] if c["controle"] == "Liens internes")
    assert "1 ancre(s)" in liens["valeur"], liens


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
