#!/usr/bin/env python3
"""Tests de non-régression de l'humaniseur FR. Lancer : python3 test_humaniseur.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "skills", "linkedin-human", "scripts"))

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
def tiret_cadratin_jamais_en_point_virgule():
    out = clean("— Premier point\nOn a testé — et ça a marché — en mars.\nUne idée —\nFin.")
    assert "—" not in out and ";" not in out, out
    assert out == "Premier point\nOn a testé, et ça a marché, en mars.\nUne idée\nFin.", out


@case
def pourcentage_colle_au_nombre():
    assert clean("Plus 15 % de réponses, puis 23\u00a0% et 4\u202f%.") == "Plus 15% de réponses, puis 23% et 4%."


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
    _, score_ia, verdict_ia, _ = run(read("brouillon-ia.txt"), LEX)
    _, score_h, verdict_h, _ = run(read("post-humain.txt"), LEX)
    assert verdict_ia == "SIGNALÉ", (score_ia, verdict_ia)
    assert verdict_h == "OK", (score_h, verdict_h)


@case
def les_formes_elidees_comptent_comme_pronoms():
    from detect import PRONOUNS, ORAL
    assert len(PRONOUNS.findall("J'ai vu, t'as raison, m'a dit")) == 3
    assert len(ORAL.findall("J'ai vu ça")) == 2


@case
def un_texte_court_n_est_pas_bloque_par_rythme_et_voix():
    results, score, verdict, _ = run("Votre post sur les délais parle de mon quotidien : je prépare des devis pour des PME.", LEX)
    assert results["RYTHME"][0] is None and results["VOIX"][0] is None
    assert verdict == "OK", (score, verdict)


@case
def la_reecriture_manuelle_passe():
    _, score, verdict, _ = run(read("brouillon-ia-reecrit.txt"), LEX)
    assert verdict == "OK", (score, verdict)


# ---------------------------------------------------------------- version 2 (doctrine V3)
from marqueurs import densite, find_flags, rythme, formulations_retirees  # noqa: E402
from fidelite import comparer  # noqa: E402
from detect import garde_sur_correction, resume  # noqa: E402


def familles(texte, niveau="strict"):
    return {f["famille"] for f in find_flags(texte, LEX, niveau)}


@case
def paragraphe_plat_signale_mais_variation_non_recompensee():
    plat = ("Nous avons lancé la campagne en mars dernier. Les premiers résultats sont arrivés très vite. "
            "L'équipe a suivi les chiffres chaque matin. Le budget est resté stable tout le trimestre.")
    r = rythme(plat)
    assert any(p["type"] == "paragraphe plat" for p in r["problemes"]), r
    vivant = ("On a lancé la campagne en mars, quand le budget a enfin été validé. Résultats rapides. "
              "L'équipe suivait les chiffres chaque matin, parce que personne ne croyait au canal. Le budget n'a pas bougé.")
    assert not rythme(vivant)["problemes"], rythme(vivant)


@case
def mise_en_page_linkedin_non_penalisee():
    texte = "J'ai envoyé 412 messages en 2025.\n\n9 réponses.\n\nPuis j'ai commenté avant d'écrire.\n\n14 réponses sur 60."
    assert not [p for p in rythme(texte)["problemes"] if p["type"] == "paragraphe plat"]


@case
def staccato_et_fragments():
    t = "Pas de réunion. Pas de slides. Juste du terrain.\n\nSimple. Rapide. Efficace.\n\nVraiment."
    ids = {f.get("id") for f in find_flags(t, LEX) if f["famille"] == "staccato"}
    assert {"pas-x-pas-y-juste-z", "adjectifs-en-rafale", "paragraphe-un-mot"} <= ids, ids
    assert any(p["type"] == "fragments" for p in rythme(t)["problemes"])


@case
def hashtag_seul_n_est_pas_un_fragment_mis_en_scene():
    assert "staccato" not in familles("J'ai signé 12 contrats en mars.\n\n#B2B")


@case
def annonce_de_sincerite():
    assert "sincerite" in familles("Honnêtement, je ne pensais pas que ça marcherait.")
    assert "sincerite" in familles("Je vais être cash : on a perdu le client.")
    assert "sincerite" not in familles("On a perdu le client Assurly le 14 février.")


@case
def fuites_forensiques_et_niveau():
    t = "Voici une version révisée de votre post. En tant qu'IA, je ne peux pas vérifier. [Votre nom]"
    f = find_flags(t, LEX, "forensique")
    assert f and all(x["famille"] == "forensique" for x in f), f
    _, _, verdict, _ = run(t + " " + read("post-humain.txt"), LEX)
    assert verdict == "SIGNALÉ"


@case
def champ_a_completer_n_est_pas_une_fuite():
    assert "forensique" not in familles("On a réduit le délai de {{à compléter : chiffre}} jours.")


@case
def densite_par_paragraphe():
    t = ("Cette approche stratégique constitue un levier crucial et holistique.\n\n"
         "On a signé 12 contrats en mars, un chiffre significatif pour nous.")
    d = densite(t, find_flags(t, LEX))
    assert d[0]["action"] == "RÉÉCRIRE LE PARAGRAPHE", d
    assert d[1]["action"] == "LAISSER", d


@case
def copule_seulement_en_esthetique():
    t = "Ce projet représente notre priorité."
    assert "copule" not in familles(t, "strict")
    assert "copule" in familles(t, "esthetique")


@case
def triade_creuse_contre_triade_concrete():
    creuse = [f for f in find_flags("Notre offre est simple, rapide et efficace.", LEX) if f["famille"] == "triade"]
    assert creuse, "triade creuse non repérée"
    concrete = [f for f in find_flags("On utilise Stripe, Qonto et Pennylane chaque jour.", LEX) if f["famille"] == "triade"]
    assert not concrete, concrete


@case
def epoques_datees():
    f = [x for x in find_flags("Plongeons dans le sujet.", LEX) if x.get("epoque")]
    assert f and f[0]["equivalent_en"] == "delve", f


@case
def formulations_retirees_du_contexte():
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
        fh.write("## Formulations retirées\n\n| Ancienne formulation | Retirée le | Remplacée par |\n|---|---|---|\n"
                 "| leader de l'assurance en ligne | 2026-03 | assurance habitation en ligne |\n")
    ret = formulations_retirees(fh.name)
    assert ret == ["leader de l'assurance en ligne"], ret
    f = find_flags("Assurly, leader de l'assurance en ligne, recrute.", LEX, "strict", ret)
    assert any(x["famille"] == "formulation-retiree" for x in f)


@case
def fidelite_ajout_et_perte():
    avant = "On a relancé 1 400 clients en 6 semaines chez Assurly : 212 contrats réactivés en mars 2025."
    assert comparer(avant, "Chez Assurly, 1400 clients relancés en 6 semaines : 212 contrats réactivés en mars 2025.")["verdict"] == "FIDÈLE"
    r = comparer(avant, "On a relancé 1 400 clients en 6 semaines chez Assurly : 212 contrats et 38 k€ en mars 2025.")
    assert r["verdict"] == "AJOUTS" and "38k€" in r["ajouts"]["chiffres"], r
    r = comparer(avant, "On a relancé nos clients dormants : beaucoup de contrats réactivés.")
    assert r["verdict"] == "PERTES" and "Assurly" in r["pertes"]["noms"], r


@case
def fidelite_champ_rempli():
    r = comparer("Délai réduit de {{à compléter}} jours.", "Délai réduit de 12 jours.")
    assert r["verdict"] == "AJOUTS" and "champs_remplis" in r["ajouts"], r


@case
def garde_anti_sur_correction():
    avant = "J'ai lancé la campagne en mars et les leads ont doublé en 6 semaines chez Assurly."
    apres = "Campagne lancée en mars. Leads doublés.\n\nSimple. Rapide. Efficace.\n\nHonnêtement, ça a marché."
    ra = run(avant, LEX)[3]
    rb = run(apres, LEX)[3]
    alertes = garde_sur_correction(resume(avant, ra), resume(apres, rb))
    texte = " ".join(alertes)
    assert "staccato" in texte and "sincérité" in texte and "je" in texte, alertes


@case
def evaluation_v2_cas_7_tous_les_tics():
    # cas 7 de l'éval à l'aveugle (octobre 2026) : 7 tics, dont 3 que la v2.0 ratait
    from marqueurs import find_flags
    t = ("Dans un monde en constante évolution, la fidélisation est un enjeu crucial, véritable pilier de la "
         "croissance. Nos équipes ont rappelé 60 clients. Le résultat ? Le délai. Rapidité, transparence, "
         "proximité : voilà les clés du succès.")
    familles = {f["famille"] for f in find_flags(t, LEX)}
    for attendu in ("veritable", "revelation", "triade", "cliche-succes"):
        assert attendu in familles, (attendu, familles)


@case
def fidelite_trou_ajoute_non_bloquant():
    from fidelite import comparer
    r = comparer("On a rappelé 60 clients.", "On a rappelé 60 clients en {{à compléter : durée}}.")
    assert r["code"] == 2 and r["trous"] and not r["ajouts"], r


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
