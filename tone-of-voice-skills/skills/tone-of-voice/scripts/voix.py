#!/usr/bin/env python3
"""voix.py : mesure la façon d'écrire d'une personne à partir de ses textes.

Lit 1 à 30 textes (fichiers .txt ou .md, un texte par fichier, ou un seul
fichier où les textes sont séparés par une ligne « --- »). Sort :

  - le volume et la confiance (faible, moyenne, bonne) ;
  - les mesures : longueur des phrases, paragraphes, ponctuation classée
    jamais / rare / habituelle, tutoiement ou vouvoiement, « je », « on »,
    « nous », « ça » ou « cela », négation sans « ne », chiffres, émojis,
    hashtags, typographie (espace avant « : ; ! ? », « 15 % » ou « 15% ») ;
  - les mots et les expressions qui reviennent d'un texte à l'autre ;
  - les ouvertures et les fins ;
  - les alertes : textes probablement écrits par IA, textes à part (autre
    auteur ou autre registre), textes presque identiques ;
  - les règles que le corpus justifie (« jamais d'émoji » seulement si aucun
    texte n'en a).

Ce qui relève du jugement (traits, consignes, curseurs) n'est pas ici : le
Skill le fait à partir de ces mesures.

Usage
  python3 voix.py textes/*.txt
  python3 voix.py corpus.md                 # textes séparés par ---
  python3 voix.py textes/*.txt --json
  python3 voix.py textes/*.txt --bloc       # bloc à coller dans tone-of-voice.md
  python3 voix.py textes/*.txt --bloc --date 2026-10-27

Codes de sortie : 0 rien à signaler · 2 alertes à lire · 1 erreur d'usage.

Méthode : mesures inspirées de rhuss/cc-prose (MIT), du seuil « rare » de
notque/claude-code-toolkit (MIT) et des règles justifiées par le corpus de
houtini-ai/voice-analyser-mcp (Apache 2.0). Réécrit pour le français.
"""

import argparse
import datetime as dt
import itertools
import json
import os
import re
import statistics
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import texte as tx  # noqa: E402

CONFIANCE = ((500, "faible"), (1500, "moyenne"))  # heuristique maison, en mots
MAX_TEXTES = 30


def lire_textes(chemins):
    textes = []
    for chemin in chemins:
        with open(chemin, encoding="utf-8", errors="replace") as fh:
            contenu = tx.normaliser(fh.read())
        morceaux = re.split(r"(?m)^\s*-{3,}\s*$", contenu)
        etiquette = os.path.basename(chemin)
        morceaux = [m.strip() for m in morceaux if tx.MOT.search(m or "")]
        for i, m in enumerate(morceaux, 1):
            nom = etiquette if len(morceaux) == 1 else f"{etiquette}#{i}"
            textes.append((nom, m))
    return textes


def niveau_confiance(n_mots, n_textes):
    niveau = "bonne"
    for seuil, nom in CONFIANCE:
        if n_mots < seuil:
            niveau = nom
            break
    if n_textes < 3 and niveau == "bonne":
        niveau = "moyenne"
    if n_textes < 2:
        niveau = "faible"
    return niveau


def mots_frequents(textes, n=15):
    total, docs = Counter(), Counter()
    for _, t in textes:
        ms = [m.lower().replace("’", "'") for m in tx.mots(t)]
        ms = [m for m in ms if len(m) >= 3 and m not in tx.MOTS_VIDES and not m.isdigit()]
        total.update(ms)
        docs.update(set(ms))
    seuil_docs = 2 if len(textes) >= 2 else 1
    garde = [(m, c, docs[m]) for m, c in total.items() if c >= 2 and docs[m] >= seuil_docs]
    garde.sort(key=lambda x: (-x[2], -x[1], x[0]))
    return [{"mot": m, "occurrences": c, "textes": d} for m, c, d in garde[:n]]


def expressions(textes, n=10):
    """Suites de 2 à 4 mots présentes dans au moins 2 textes (phrases signatures possibles)."""
    docs = Counter()
    for _, t in textes:
        vues = set()
        for p in tx.phrases(t):
            ms = [m.lower().replace("’", "'") for m in tx.MOT.findall(p)]
            for k in (4, 3, 2):
                for i in range(len(ms) - k + 1):
                    g = ms[i:i + k]
                    if all(x in tx.MOTS_VIDES for x in g) or g[0] in ("et", "de", "à") or g[-1] in tx.MOTS_VIDES:
                        continue
                    vues.add(" ".join(g))
        docs.update(vues)
    candidats = [(e, d) for e, d in docs.items() if d >= 2]
    candidats.sort(key=lambda x: (-x[1], -len(x[0].split()), x[0]))
    retenus = []
    for e, d in candidats:
        if any(e in r["expression"] for r in retenus):
            continue
        retenus.append({"expression": e, "textes": d})
        if len(retenus) == n:
            break
    return retenus


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 0.0


def textes_a_part(par_texte):
    """Repère les textes qui s'écartent des autres (autre auteur, autre registre)."""
    if len(par_texte) < 3:
        return []
    sortie = []
    for i, (nom, m) in enumerate(par_texte):
        autres = [x for j, (_, x) in enumerate(par_texte) if j != i]
        raisons = []
        med_autres = [x["phrase_mediane"] for x in autres if x["phrase_mediane"] is not None]
        if m["phrase_mediane"] is not None and med_autres:
            ref = statistics.median(med_autres)
            if abs(m["phrase_mediane"] - ref) > 6:
                raisons.append(f"phrases de {m['phrase_mediane']:g} mots contre {ref:g} ailleurs")
        adr = tx.adresse(m["tu"], m["vous"])
        adr_autres = Counter(tx.adresse(x["tu"], x["vous"]) for x in autres)
        dominante, nb = adr_autres.most_common(1)[0]
        if {adr, dominante} == {"tutoiement", "vouvoiement"} and nb >= 2:
            raisons.append(f"{adr} alors que les autres textes sont au {dominante}")
        if m["emojis"] and not any(x["emojis"] for x in autres):
            raisons.append("seul texte avec des émojis")
        excl = m["ponctuation"]["exclamation"] / max(m["phrases"], 1)
        excl_autres = statistics.median(x["ponctuation"]["exclamation"] / max(x["phrases"], 1) for x in autres)
        if excl - excl_autres > 0.3:
            raisons.append("beaucoup plus d'exclamations que les autres")
        ca, cela = m["ca"], m["cela"]
        ca_autres = sum(x["ca"] for x in autres)
        cela_autres = sum(x["cela"] for x in autres)
        if cela and not ca and ca_autres and not cela_autres:
            raisons.append("« cela » alors que les autres textes disent « ça »")
        soutenu_autres = statistics.median(x["soutenu"] / max(x["mots"], 1) for x in autres)
        if m["soutenu"] >= 2 and m["soutenu"] / max(m["mots"], 1) > 3 * soutenu_autres + 0.005:
            raisons.append(f"{m['soutenu']} formules administratives (« veuillez », « conformément »…)")
        on_autres = sum(x["on"] for x in autres)
        nous_autres = sum(x["nous"] for x in autres)
        if m["nous"] >= 2 and m["on"] == 0 and on_autres > 2 * max(nous_autres, 1):
            raisons.append("« nous » partout alors que les autres textes disent « on »")
        if raisons:
            sortie.append({"texte": nom, "niveau": "à part" if len(raisons) >= 2 else "léger écart",
                           "raisons": raisons})
    return sortie


def presque_identiques(textes):
    sortie = []
    sacs = [(nom, [w.lower() for w in tx.mots(t)]) for nom, t in textes]
    for (n1, a), (n2, b) in itertools.combinations(sacs, 2):
        if len(a) >= 20 and len(b) >= 20 and jaccard(a, b) >= 0.6:
            sortie.append({"textes": [n1, n2], "vocabulaire_commun": round(100 * jaccard(a, b))})
    return sortie


def analyser(textes):
    if not textes:
        raise ValueError("aucun texte lisible")
    par_texte = [(nom, tx.mesurer(t)) for nom, t in textes]
    tout = "\n\n".join(t for _, t in textes)
    m_tout = tx.mesurer(tout)
    n_mots = sum(m["mots"] for _, m in par_texte)
    n_ph = sum(m["phrases"] for _, m in par_texte)
    longueurs = [len(tx.MOT.findall(p)) for _, t in textes for p in tx.phrases(t)]
    n_pars = [m for _, m in par_texte if m["part_paragraphes_une_phrase"] is not None]
    n = len(textes)

    ponct = {}
    for k in tx.PONCTUATION:
        nb = sum(m["ponctuation"][k] for _, m in par_texte)
        taux = nb / n_ph if n_ph else None
        ponct[k] = {"total": nb, "par_phrase": tx.arrondi(taux, 2), "classe": tx.classe(taux),
                    "textes": sum(1 for _, m in par_texte if m["ponctuation"][k])}
    em = sum(m["emojis"] for _, m in par_texte)
    ponct["emojis"] = {"total": em, "par_phrase": tx.arrondi(em / n_ph, 2) if n_ph else None,
                       "classe": tx.classe(em / n_ph) if n_ph else None,
                       "textes": sum(1 for _, m in par_texte if m["emojis"])}

    adresses = Counter(tx.adresse(m["tu"], m["vous"]) for _, m in par_texte)
    tu, vous = m_tout["tu"], m_tout["vous"]
    ca, cela = m_tout["ca"], m_tout["cela"]
    oral, angl = Counter(), Counter()
    for _, m in par_texte:
        oral.update({k: 1 for k in m["marques_oral"]})
        angl.update({k: 1 for k in m["anglicismes"]})

    ia = []
    for nom, m in par_texte:
        forts = [x for x in m["marques_ia"] if x["force"] == "fort"]
        if forts or len(m["marques_ia"]) >= 3:
            ia.append({"texte": nom, "marques": m["marques_ia"][:6]})

    typo = {
        "espace_avant_double": m_tout["espace_avant_double"],
        "sans_espace_avant_double": m_tout["sans_espace_avant_double"],
        "pourcent_espace": m_tout["pourcent_espace"],
        "pourcent_colle": m_tout["pourcent_colle"],
    }

    resultat = {
        "version_mesures": tx.VERSION_MESURES,
        "textes": n,
        "mots": n_mots,
        "phrases": n_ph,
        "confiance": niveau_confiance(n_mots, n),
        "phrase_mediane": tx.arrondi(statistics.median(longueurs)) if longueurs else None,
        "phrase_ecart_type": tx.arrondi(statistics.stdev(longueurs)) if len(longueurs) >= 4 else None,
        "part_phrases_courtes": m_tout["part_phrases_courtes"],
        "part_phrases_longues": m_tout["part_phrases_longues"],
        "part_paragraphes_une_phrase": (
            tx.arrondi(statistics.median(m["part_paragraphes_une_phrase"] for m in n_pars), 0) if n_pars else None),
        "adresse": tx.adresse(tu, vous),
        "adresse_par_texte": dict(adresses),
        "je_pour_1000": tx.pour_mille(m_tout["je"], n_mots),
        "on_pour_1000": tx.pour_mille(m_tout["on"], n_mots),
        "nous_pour_1000": tx.pour_mille(m_tout["nous"], n_mots),
        "ca_cela": "ça" if ca > cela else "cela" if cela > ca else ("les deux" if ca else "aucun"),
        "negation_sans_ne_pour_1000": tx.pour_mille(m_tout["negations_sans_ne"], n_mots),
        "chiffres_pour_100": tx.arrondi(100 * m_tout["chiffres"] / n_mots) if n_mots else None,
        "hashtags_par_texte": tx.arrondi(sum(m["hashtags"] for _, m in par_texte) / n),
        "ponctuation": ponct,
        "typographie": typo,
        "marques_oral": dict(oral.most_common()),
        "anglicismes": dict(angl.most_common()),
        "mots_frequents": mots_frequents(textes),
        "expressions": expressions(textes),
        "ouvertures": [{"texte": nom, "debut": m["ouverture"]} for nom, m in par_texte],
        "fins": dict(Counter(m["fin"] for _, m in par_texte if m["fin"])),
        "textes_ia_probables": ia,
        "textes_a_part": textes_a_part(par_texte),
        "presque_identiques": presque_identiques(textes),
        "par_texte": [{"texte": nom, "mots": m["mots"], "phrase_mediane": m["phrase_mediane"],
                       "adresse": tx.adresse(m["tu"], m["vous"]), "fin": m["fin"]} for nom, m in par_texte],
    }
    resultat["regles_justifiees"] = regles(resultat)
    resultat["alertes"] = alertes(resultat)
    return resultat


NOMS_PONCT = {
    "question": "questions", "exclamation": "points d'exclamation", "points_suspension": "points de suspension",
    "parentheses": "parenthèses", "deux_points": "deux-points", "point_virgule": "points-virgules",
    "cadratin": "tirets cadratins (—)", "guillemets_droits": "guillemets droits (\")",
    "guillemets_francais": "guillemets « »", "emojis": "émojis",
}


def regles(r):
    """Règles que le corpus justifie. Rien n'est proposé sans preuve dans les textes."""
    out = []
    n = r["textes"]
    for k, v in r["ponctuation"].items():
        if v["classe"] == "jamais" and k not in ("guillemets_droits", "guillemets_francais"):
            nom = NOMS_PONCT[k]
            out.append(f"Jamais {'d’' if nom[0] in 'aeiouyéè' else 'de '}{nom} (0 sur {n} textes).")
        elif v["classe"] == "habituelle" and k in ("question", "exclamation", "emojis", "points_suspension", "parentheses"):
            out.append(f"{NOMS_PONCT[k].capitalize()} habituels : {v['par_phrase']} par phrase ({v['textes']} textes sur {n}).")
    adr = r["adresse_par_texte"]
    if r["adresse"] in ("tutoiement", "vouvoiement"):
        out.append(f"{r['adresse'].capitalize()} ({adr.get(r['adresse'], 0)} textes sur {n}).")
    if r["ca_cela"] in ("ça", "cela"):
        out.append(f"« {r['ca_cela']} » plutôt que « {'cela' if r['ca_cela'] == 'ça' else 'ça'} ».")
    if r["phrase_mediane"] is not None:
        out.append(f"Phrases de {r['phrase_mediane']:g} mots en médiane"
                   + (f", écart-type {r['phrase_ecart_type']:g}." if r["phrase_ecart_type"] is not None else "."))
    return out


def alertes(r):
    out = []
    if r["confiance"] == "faible":
        out.append(f"Corpus court ({r['mots']} mots, {r['textes']} texte(s)) : profil provisoire, "
                   "compléter avec des questions et redemander des textes.")
    for x in r["textes_ia_probables"]:
        ids = ", ".join(sorted({m["id"] for m in x["marques"]}))
        out.append(f"{x['texte']} : marques d'écriture IA ({ids}). Demander si ce texte a été écrit à la main.")
    for x in r["textes_a_part"]:
        out.append(f"{x['texte']} : {x['niveau']} ({' ; '.join(x['raisons'])}). Demander s'il faut le garder.")
    for x in r["presque_identiques"]:
        out.append(f"{x['textes'][0]} et {x['textes'][1]} se ressemblent ({x['vocabulaire_commun']}% de vocabulaire "
                   "commun) : un seul compte vraiment.")
    if r["textes"] >= 3:
        sujets = Counter()
        for m in r["mots_frequents"][:5]:
            if m["textes"] == r["textes"]:
                sujets[m["mot"]] += 1
        if len(sujets) >= 4:
            out.append("Tous les textes parlent du même sujet : demander un texte sur un autre sujet "
                       "pour séparer la voix du thème.")
    return out


def bloc(r, date):
    p = r["ponctuation"]
    valeurs = {
        "version_mesures": r["version_mesures"],
        "date": date,
        "textes": r["textes"],
        "mots": r["mots"],
        "confiance": r["confiance"],
        "phrase_mediane": r["phrase_mediane"],
        "phrase_ecart_type": r["phrase_ecart_type"],
        "part_paragraphes_une_phrase": r["part_paragraphes_une_phrase"],
        "adresse": r["adresse"],
        "ca_cela": r["ca_cela"],
        "je_pour_1000": r["je_pour_1000"],
        "on_pour_1000": r["on_pour_1000"],
        "nous_pour_1000": r["nous_pour_1000"],
        "negation_sans_ne_pour_1000": r["negation_sans_ne_pour_1000"],
        "chiffres_pour_100": r["chiffres_pour_100"],
    }
    for k in ("emojis", "exclamation", "question", "points_suspension", "parentheses", "deux_points",
              "point_virgule", "cadratin"):
        valeurs[k] = p[k]["classe"]
        valeurs[k + "_par_phrase"] = p[k]["par_phrase"]
    return tx.ecrire_bloc(valeurs)


def f(x):
    """Nombre lisible : 8.0 devient 8, None devient « n.d. »."""
    return "n.d." if x is None else f"{x:g}" if isinstance(x, (int, float)) else str(x)


def rendu(r, out=sys.stdout):
    w = lambda s="": print(s, file=out)  # noqa: E731
    w(f"VOIX : {r['textes']} texte(s), {r['mots']} mots, {r['phrases']} phrases · confiance {r['confiance']}")
    w()
    w("RYTHME")
    w(f"  phrases : médiane {f(r['phrase_mediane'])} mots, écart-type {f(r['phrase_ecart_type'])}, "
      f"{f(r['part_phrases_courtes'])}% de 8 mots ou moins, {f(r['part_phrases_longues'])}% de 25 mots ou plus")
    w(f"  paragraphes d'une seule phrase : {f(r['part_paragraphes_une_phrase'])}%")
    w()
    w("ADRESSE ET REGISTRE")
    w(f"  {r['adresse']} (par texte : {r['adresse_par_texte']})")
    w(f"  pour 1000 mots : je {f(r['je_pour_1000'])} · on {f(r['on_pour_1000'])} · nous {f(r['nous_pour_1000'])} · "
      f"négation sans « ne » {f(r['negation_sans_ne_pour_1000'])}")
    w(f"  « ça » ou « cela » : {r['ca_cela']} · chiffres pour 100 mots : {f(r['chiffres_pour_100'])}")
    if r["marques_oral"]:
        w("  marques d'oral (nombre de textes) : " + ", ".join(f"{k} ({v})" for k, v in r["marques_oral"].items()))
    if r["anglicismes"]:
        w("  anglicismes (nombre de textes) : " + ", ".join(f"{k} ({v})" for k, v in r["anglicismes"].items()))
    w()
    w("PONCTUATION (par phrase · classe · textes)")
    for k, v in r["ponctuation"].items():
        w(f"  {NOMS_PONCT[k]:<28} {f(v['par_phrase']):>5}  {v['classe'] or '-':<11} {v['textes']}/{r['textes']}")
    t = r["typographie"]
    w(f"  espace avant : ; ! ? → avec {t['espace_avant_double']}, sans {t['sans_espace_avant_double']} · "
      f"pourcentage → « 15 % » {t['pourcent_espace']}, « 15% » {t['pourcent_colle']}")
    w()
    if r["mots_frequents"]:
        w("MOTS QUI REVIENNENT (occurrences · textes)")
        w("  " + ", ".join(f"{m['mot']} ({m['occurrences']}·{m['textes']})" for m in r["mots_frequents"]))
    if r["expressions"]:
        w("EXPRESSIONS PRÉSENTES DANS PLUSIEURS TEXTES")
        for e in r["expressions"]:
            w(f"  « {e['expression']} » ({e['textes']} textes)")
    w("OUVERTURES")
    for o in r["ouvertures"]:
        w(f"  {o['texte']} : « {o['debut']}… »")
    w(f"FINS : {r['fins']}")
    w()
    if r["regles_justifiees"]:
        w("RÈGLES JUSTIFIÉES PAR LES TEXTES" + (" (provisoires : corpus court)" if r["confiance"] == "faible" else ""))
        for x in r["regles_justifiees"]:
            w(f"  - {x}")
        w()
    if r["alertes"]:
        w("ALERTES")
        for x in r["alertes"]:
            w(f"  ! {x}")
    else:
        w("ALERTES : aucune")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mesure la façon d'écrire d'une personne à partir de ses textes.")
    ap.add_argument("fichiers", nargs="+", help="textes (.txt, .md) ; un fichier peut contenir plusieurs textes séparés par ---")
    ap.add_argument("--json", action="store_true", help="sortie JSON complète")
    ap.add_argument("--bloc", action="store_true", help="bloc ```mesures``` à coller dans tone-of-voice.md")
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="date du bloc (AAAA-MM-JJ)")
    a = ap.parse_args(argv)
    try:
        textes = lire_textes(a.fichiers)
    except OSError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    if not textes:
        print("Erreur : aucun texte lisible (fichiers vides ?).", file=sys.stderr)
        return 1
    if len(textes) > MAX_TEXTES:
        print(f"Erreur : {len(textes)} textes, {MAX_TEXTES} au plus. Garde les plus représentatifs.", file=sys.stderr)
        return 1
    r = analyser(textes)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif a.bloc:
        print(bloc(r, a.date))
    else:
        rendu(r)
    return 2 if r["alertes"] else 0


if __name__ == "__main__":
    sys.exit(main())
