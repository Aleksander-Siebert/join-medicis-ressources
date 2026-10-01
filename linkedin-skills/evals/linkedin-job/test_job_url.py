#!/usr/bin/env python3
"""Tests de job_url.py. Lancer : python3 test_job_url.py"""
import os
import sys
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "linkedin-job"))
from job_url import build_query, build_url, check_query, rewrite_url  # noqa: E402


def qs(url):
    return {k: v[0] for k, v in parse_qs(urlsplit(url).query).items()}


def test_requete_booleenne():
    q = build_query(["head of growth", "growth manager"], ["saas"], ["stage"])
    assert q == '("head of growth" OR "growth manager") AND saas NOT stage', q
    assert check_query(q) == []


def test_url_derniere_heure():
    p = qs(build_url("growth", lieu="Lyon", teletravail=["hybride"], experience=["confirme"]))
    assert p["f_TPR"] == "r3600" and p["sortBy"] == "DD" and p["f_WT"] == "3" and p["f_E"] == "4"
    assert p["location"] == "Lyon" and p["keywords"] == "growth"


def test_espaces_encodes_en_pourcent():
    assert "%20" in build_url('"head of growth"') and "+" not in build_url('"head of growth"')


def test_reecriture_garde_les_filtres_et_retire_le_pistage():
    url, _ = rewrite_url("https://fr.linkedin.com/jobs/search/?currentJobId=1&keywords=growth&f_WT=2&f_TPR=r86400&sortBy=R&trk=x")
    p = qs(url)
    assert p == {"keywords": "growth", "f_WT": "2", "f_TPR": "r3600", "sortBy": "DD"}, p
    assert url.startswith("https://www.linkedin.com/jobs/search/")


def test_reecriture_autre_duree():
    url, _ = rewrite_url("https://www.linkedin.com/jobs/search/?keywords=cmo", depuis=7200)
    assert qs(url)["f_TPR"] == "r7200"


def test_refuse_une_url_hors_linkedin():
    try:
        rewrite_url("https://www.welcometothejungle.com/fr/jobs?query=growth")
    except ValueError:
        return
    raise AssertionError("aurait dû refuser")


def test_verification():
    assert any("MAJUSCULES" in p for p in check_query("growth or acquisition"))
    assert any("Guillemets non fermés" in p for p in check_query('"head of growth'))
    assert any("Parenthèses" in p for p in check_query("(growth OR acquisition"))
    assert check_query('"chargé d\'acquisition" OR "traffic manager"') == []


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
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
