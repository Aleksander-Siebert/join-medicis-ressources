#!/usr/bin/env python3
"""Tests du profil « article » de l'humaniseur. Lancer : python3 test_article.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "skills", "seo-human"))

from humanize import humanize, load_lexicon  # noqa: E402
from detect import run  # noqa: E402

LEX = load_lexicon()
SRC = open(os.path.join(HERE, "article-ia.md"), encoding="utf-8").read()
OPTS = dict(profil="article", affirmatif=True, remplacer=["chez Assurly=>à Assurly"], interdire=["cash"])
CLEAN, LOGS, FLAGS = humanize(SRC, LEX, **OPTS)
FAM = {f["famille"] for f in FLAGS}
IDS = {f.get("id") for f in FLAGS}


def test_garde_le_markdown_d_un_article():
    assert CLEAN.startswith("# Assurance santé expatrié") and "## Pourquoi" in CLEAN
    assert "**Important :**" in CLEAN


def test_le_profil_linkedin_retire_toujours_le_markdown():
    out = humanize(SRC, LEX)[0]
    assert "## " not in out and "**" not in out


def test_tiret_cadratin_et_pourcentage():
    assert "—" not in CLEAN and "10%" in CLEAN and ";" not in CLEAN.split("\n")[2]


def test_remplacement_de_site():
    assert "À Assurly, nous savons" in CLEAN and "Chez Assurly" not in CLEAN


def test_signalements_propres_aux_articles():
    for fid in ("section-conclusion", "intro-meta", "passif-agent", "passif-futur"):
        assert fid in IDS, fid
    assert "modal" in FAM and "regle-site" in FAM and "copule" in FAM


def test_gras_en_exces():
    assert any("passages en gras" in f["extrait"] for f in FLAGS)


def test_modaux_seulement_en_style_affirmatif():
    flags = humanize(SRC, LEX, profil="article")[2]
    assert "modal" not in {f["famille"] for f in flags}


def test_markdown_non_penalise_dans_l_empreinte():
    res_article = run(CLEAN, LEX, "article")[0]["EMPREINTE"][1]
    assert "0 gras" in res_article, res_article


def test_article_ia_signale():
    _, score, verdict = run(SRC, LEX, "article", True)
    assert verdict == "SIGNALÉ", (score, verdict)


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
