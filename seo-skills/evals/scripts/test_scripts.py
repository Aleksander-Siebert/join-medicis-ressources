#!/usr/bin/env python3
"""Tests hors ligne des scripts du pack SEO. Lancer : python3 test_scripts.py"""
import io
import os
import sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..", "..", "skills")
for d in ("seo-maillage", "seo-veille", "seo-audit", "seo-drift"):
    sys.path.insert(0, os.path.join(SK, d))

import maillage  # noqa: E402
import onpage  # noqa: E402
import veille  # noqa: E402
import drift  # noqa: E402


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


def test_onpage_images_et_nosnippet():
    html = ('<html lang="fr"><head><meta name="robots" content="max-snippet:0"></head><body><h1>Titre<br>suite</h1>'
            '<img src="/hero.jpg" loading="lazy"><picture><source type="image/avif" srcset="/b.avif"><img src="/b.jpg" width="10" height="10"></picture>'
            '<img src="/c.png" width="5" height="5" alt=""><img src="/d.webp" data-nimg="fill"></body></html>')
    r = onpage.audit(html, "https://exemple.fr/")
    st = {c["controle"]: c for c in r["controles"]}
    assert st["Meta robots"]["statut"] == "BLOQUANT"
    assert st["Image principale"]["statut"] == "À REVOIR"
    assert r["images"]["sans_dimensions"] == ["/hero.jpg"], r["images"]
    assert r["images"]["formats_anciens"] == ["/hero.jpg", "/c.png"], r["images"]
    assert r["titres"][0] == (1, "Titre suite")


def test_onpage_lit_pagespeed():
    d = {"loadingExperience": {"metrics": {"LARGEST_CONTENTFUL_PAINT_MS": {"percentile": 3100},
                                           "INTERACTION_TO_NEXT_PAINT": {"percentile": 150},
                                           "CUMULATIVE_LAYOUT_SHIFT_SCORE": {"percentile": 5}}},
         "lighthouseResult": {"audits": {"largest-contentful-paint": {"numericValue": 2900.4}}}}
    v = onpage.lire_psi(d)
    assert v["terrain"] == {"LCP": 3100, "INP": 150, "CLS": 0.05} and v["labo"]["LCP"] == 2900
    assert onpage.note_cwv("LCP", 3100) == "à améliorer" and onpage.note_cwv("CLS", 0.05) == "bon"


def test_drift_detecte_les_regressions():
    html = open(f("page.html"), encoding="utf-8").read()
    url = "https://assurly.example/assurance-sante-expatrie/"
    avant = drift.photo(url, 200, url, {}, html)
    assert avant["title"].startswith("Assurance santé expatrié") and avant["h1"] == ["Assurance santé expatrié"]
    casse = (html.replace("<head>", '<head><meta name="robots" content="noindex">')
             .replace("https://assurly.example/assurance-sante-expatrie/\"", "https://assurly.example/\"")
             .replace("<h1>Assurance santé expatrié</h1>", ""))
    res = drift.comparer(avant, drift.photo(url, 200, url, {}, casse))
    critiques = {x["regle"] for x in res if x["gravite"] == "CRITIQUE"}
    assert {"noindex ajouté", "Canonical modifié", "H1 supprimé"} <= critiques, res
    assert drift.comparer(avant, drift.photo(url, 200, url, {}, html)) == []
    erreur = drift.photo(url, 404, url, {}, "")
    assert any(x["regle"] == "La page répond en erreur" for x in drift.comparer(avant, erreur))


def test_drift_normalise_les_url():
    assert drift.normaliser("HTTPS://Site.fr:443/page/?utm_source=x&b=2&a=1") == "https://site.fr/page?a=1&b=2"


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
