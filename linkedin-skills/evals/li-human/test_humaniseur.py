#!/usr/bin/env python3
"""Tests de non-régression de l'humaniseur FR. Lancer : python3 test_humaniseur.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "skills", "li-human"))

from humanize import humanize, load_lexicon  # noqa: E402
from detect import run  # noqa: E402

LEX = load_lexicon()


def clean(text, **kw):
    return humanize(text, LEX, **kw)[0]


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read()


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


@case
def garde_l_espace_avant_la_ponctuation_double():
    assert clean("En 6 mois ! Pourquoi ? Le secret : rien.") == "En 6 mois ! Pourquoi ? Le secret : rien."


@case
def ajoute_l_espace_manquante():
    assert clean("Résultat: 212 rendez-vous!") == "Résultat : 212 rendez-vous !"


@case
def ne_touche_ni_aux_heures_ni_aux_urls():
    t = "Rendez-vous à 14:30 sur https://joinmedicis.com/ressources?x=1!"
    assert clean(t) == t


@case
def tiret_cadratin_en_virgule():
    assert clean("Elle n'est pas morte — elle a changé.") == "Elle n'est pas morte, elle a changé."


@case
def plages_de_nombres():
    assert clean("Entre 10–20 messages par jour.") == "Entre 10-20 messages par jour."


@case
def guillemets_anglais_en_francais():
    assert clean("Il a dit “on signe”.") == "Il a dit « on signe »."


@case
def insecables_sur_demande():
    assert clean("Pourquoi? Parce que.", keep_nbsp=True) == "Pourquoi ? Parce que."


@case
def majuscules_accentuees():
    assert clean("Etat des lieux. A propos de nous.") == "État des lieux. À propos de nous."


@case
def suppression_en_debut_de_phrase_remet_la_majuscule():
    assert clean("Il est important de noter que les chiffres montent.") == "Les chiffres montent."


@case
def remplacements_surs():
    assert clean("Afin de gagner du temps, au sein de l'équipe.") == "Pour gagner du temps, dans l'équipe."


@case
def emoji_compose_intact():
    assert clean("Dev 👨‍💻 au calme.") == "Dev 👨‍💻 au calme."


@case
def supprime_les_invisibles():
    assert clean("Pro​spection­ B2B﻿") == "Prospection B2B"


@case
def markdown_retire():
    assert clean("**Important** : lire.") == "Important : lire."


@case
def signale_les_structures():
    _, _, flags = humanize(read("brouillon-ia.txt"), LEX)
    familles = {f["famille"] for f in flags}
    for attendu in ("parallelisme", "revelation", "appat", "conclusion", "connecteurs-en-pluie", "mise-en-forme"):
        assert attendu in familles, attendu


@case
def le_post_humain_passe_et_le_post_ia_non():
    _, score_ia, verdict_ia = run(read("brouillon-ia.txt"), LEX)
    _, score_h, verdict_h = run(read("post-humain.txt"), LEX)
    assert verdict_ia == "SIGNALÉ", (score_ia, verdict_ia)
    assert verdict_h == "OK", (score_h, verdict_h)


@case
def la_reecriture_manuelle_passe():
    _, score, verdict = run(read("brouillon-ia-reecrit.txt"), LEX)
    assert verdict == "OK", (score, verdict)


if __name__ == "__main__":
    failed = 0
    for fn in CASES:
        try:
            fn()
            print(f"ok      {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"ÉCHEC   {fn.__name__}  {e}")
    print(f"\n{len(CASES) - failed}/{len(CASES)} tests passés")
    sys.exit(1 if failed else 0)
