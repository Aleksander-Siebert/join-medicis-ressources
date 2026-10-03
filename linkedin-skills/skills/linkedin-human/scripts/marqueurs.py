#!/usr/bin/env python3
"""marqueurs.py : repérage des marques d'écriture IA qui demandent du jugement.

Module partagé par humanize.py (rapport « à réécrire ») et detect.py (notes).
Rien n'est réécrit ici : on repère, on compte, on conseille.

Doctrine (version 2 du pack, octobre 2026) :
  - L'unité de jugement est le PARAGRAPHE, pas le mot. 3 marqueurs ou plus dans
    un paragraphe : réécrire le paragraphe. 2 : remplacer le plus faible.
    1 marqueur faible : laisser. Un marqueur « fort » (révélation, parallélisme,
    annonce de sincérité, appât, fuite de modèle) se corrige dès la 1re fois.
  - Le RYTHME ne récompense plus la variation. On signale le paragraphe plat
    (4 phrases ou plus de même longueur, sans subordonnée) et la variation
    fabriquée (staccato, fragments en série, alternance long/court mécanique).
    Les paragraphes d'une phrase séparés par des lignes vides sont la mise en
    page normale de LinkedIn : on ne les touche pas.
  - Une triade passe. Une triade creuse (éléments interchangeables, abstraits,
    sans chiffre ni nom) ou une 3e triade dans le post se corrige.

Sources : Serge Bulaev, linkedin-humanizer V3 (MIT) ; blader/humanizer v3.1
(MIT) ; Boileau (MIT) ; Wikipédia EN et FR. Réécrit pour le français.
"""

import json
import os
import re
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "tics-ia.json")

NIVEAUX = ("forensique", "strict", "esthetique")
SUBORDONNEES = re.compile(
    r"\b(qui|que|qu'|dont|où|parce que|parce qu'|quand|lorsque|lorsqu'|car|puisque|puisqu'|"
    r"si|s'il|bien que|alors que|pendant que|tandis que|après avoir|avant de|afin que|pour que|"
    r"même si|sans que|dès que|comme)\b", re.I)
MOT = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿœŒ0-9]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿœŒ]+)?")


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _ligne(text, idx):
    return text.count("\n", 0, idx) + 1


def paragraphes(text):
    """Liste de (index de début, texte) des paragraphes séparés par une ligne vide."""
    out = []
    for m in re.finditer(r"(?:[^\n]|\n(?!\s*\n))+", text):
        bloc = m.group(0)
        if bloc.strip():
            decalage = len(bloc) - len(bloc.lstrip())
            out.append((m.start() + decalage, bloc.strip()))
    return out


def phrases(text):
    morceaux = re.split(r"(?<=[.!?…])\s+|\n+", text)
    return [p.strip() for p in morceaux if p.strip() and MOT.search(p)]


def _paragraphe_de(starts, idx):
    n = 0
    for i, s in enumerate(starts):
        if s <= idx:
            n = i
    return n


def _ajouter(flags, text, m, famille, conseil, force, niveau="strict", extra=None):
    debut = m.start() + len(m.group(0)) - len(m.group(0).lstrip())
    f = {"ligne": _ligne(text, debut), "debut": debut, "extrait": m.group(0).strip()[:70],
         "famille": famille, "conseil": conseil, "force": force, "niveau": niveau}
    if extra:
        f.update(extra)
    flags.append(f)


def formulations_retirees(chemin):
    """Lit la table « Formulations retirées » d'un contexte.md (1re colonne)."""
    if not chemin or not os.path.exists(chemin):
        return []
    retirees, dedans = [], False
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            if ligne.startswith("## "):
                dedans = "formulations retir" in ligne.lower()
                continue
            if dedans and ligne.strip().startswith("|"):
                cellule = ligne.strip().strip("|").split("|")[0].strip()
                if cellule and not set(cellule) <= set("-: ") and "ancienne formulation" not in cellule.lower():
                    retirees.append(cellule.strip("«» \""))
    return retirees


def triades(text, lex):
    """Énumérations « A, B et C » ; marque les triades creuses."""
    creux = lex.get("triade_creux", {})
    abstraits = {m.lower() for m in creux.get("adjectifs", []) + creux.get("noms", [])}
    motif = re.compile(r"\b([\w'-]+(?: [\w'-]+){0,2}), ([\w'-]+(?: [\w'-]+){0,2}),? et ([\w'-]+(?: [\w'-]+){0,2})\b")
    out = []
    for m in motif.finditer(text):
        items = [g.strip() for g in m.groups()]
        recu = False
        for g_i, item in enumerate(items):
            debut = m.start(g_i + 1)
            if re.search(r"\d|[%€$]", item):
                recu = True
            avant = text[:debut]
            ouvre_phrase = re.search(r"(?:^|[.!?\n])\s*$", avant) is not None
            if item[:1].isupper() and not ouvre_phrase:
                recu = True
        dernier = [i.lower().split()[-1] for i in items]
        creuse = (not recu) and all(w in abstraits for w in dernier)
        out.append({"match": m, "creuse": creuse})
    # triade sans « et » : « Rapidité, transparence, proximité : »
    vus = {o["match"].start() for o in out}
    for m in re.finditer(r"(?<![\w,] )\b([\w'-]+), ([\w'-]+), ([\w'-]+)\s*(?=[:.!]|$)", text, re.M):
        if m.start() in vus:
            continue
        items = [g.lower() for g in m.groups()]
        if all(i in abstraits for i in items):
            out.append({"match": m, "creuse": True})
    return out


def find_flags(text, lex, niveau="strict", retirees=None):
    """Tous les passages qui demandent un jugement humain."""
    if niveau not in NIVEAUX:
        niveau = "strict"
    flags = []

    for e in lex.get("forensique", []):
        for m in re.finditer(e["motif"], text, re.I | re.M):
            _ajouter(flags, text, m, "forensique", e["conseil"], "forensique", "forensique")

    for r in retirees or []:
        for m in re.finditer(r"(?<!\w)" + re.escape(r) + r"(?!\w)", text, re.I):
            _ajouter(flags, text, m, "formulation-retiree", "Formulation retirée (contexte.md) : ne plus l'employer.", "fort")

    if niveau == "forensique":
        flags.sort(key=lambda f: f["debut"])
        return flags

    for e in lex.get("sincerite", []):
        for m in re.finditer(e["motif"], text, re.I | re.M):
            _ajouter(flags, text, m, "sincerite", e["conseil"], e.get("force", "fort"))

    for e in lex["signaler"]:
        if e.get("niveau", "strict") == "esthetique" and niveau != "esthetique":
            continue
        for m in re.finditer(e["motif"], text, re.I | re.M):
            extra = {k: e[k] for k in ("epoque", "equivalent_en") if k in e}
            _ajouter(flags, text, m, e["famille"], e["conseil"], e.get("force", "faible"), e.get("niveau", "strict"), extra)

    for e in lex["structures"]:
        for m in re.finditer(e["motif"], text, re.I):
            _ajouter(flags, text, m, e["famille"], e["conseil"], e.get("force", "faible"), "strict", {"id": e["id"]})

    for e in lex.get("staccato", []):
        for m in re.finditer(e["motif"], text, re.I | re.M):
            if e["id"] == "paragraphe-un-mot" and re.fullmatch(r"\s*(?:#\S+|\d+[.)]?)\s*", m.group(0)):
                continue
            _ajouter(flags, text, m, "staccato", e["conseil"], "fort", "strict", {"id": e["id"]})

    # Listes « Titre : texte » : signature visuelle des LLM.
    entetes = list(re.finditer(
        r"^\s*(?:[-•*▪✅👉➡✔🔹▶]\S*\s*)(?:\*\*[^*\n]{1,40}\*\*\s*:|\*\*[^*\n]{1,40}:\s*\*\*|[^\s:][^:\n.!?]{0,30}\s?:\s)"
        r"|^\s*\*\*[^*\n]{1,40}(?:\*\*\s*:|:\s*\*\*)", text, re.M))
    if len(entetes) >= 2:
        for m in entetes:
            _ajouter(flags, text, m, "mise-en-forme", "Liste « Titre : texte » : signature visuelle d'IA. Écris des phrases.", "faible")

    # Anaphores : 3 phrases ou lignes de suite qui commencent par le même mot.
    unites = [(m.start(), m.group(0).strip()) for m in re.finditer(r"[^.!?\n]+[.!?…]*", text) if m.group(0).strip()]
    premiers = [re.sub(r"^[-•*\s]+", "", u).split(" ")[0].lower() for _, u in unites]
    i = 0
    while i < len(premiers) - 2:
        if premiers[i] and premiers[i] == premiers[i + 1] == premiers[i + 2] and len(premiers[i]) > 1:
            m = re.match(r".*", text[unites[i][0]:])
            flags.append({"ligne": _ligne(text, unites[i][0]), "debut": unites[i][0], "extrait": unites[i][1][:60],
                          "famille": "anaphore", "force": "fort", "niveau": "strict",
                          "conseil": f"Trois phrases de suite commencent par « {premiers[i]} » : effet slogan."})
            i += 3
        else:
            i += 1

    # Triades : une passe ; creuse ou 3e et suivantes, à corriger.
    tri = triades(text, lex)
    naturelle_vue = False
    for t in tri:
        m = t["match"]
        if t["creuse"]:
            _ajouter(flags, text, m, "triade", "Triade creuse (éléments interchangeables, sans chiffre ni nom) : garde 2 éléments précis, ou 4 dont un qui casse le moule.", "fort")
        elif len(tri) >= 3 and naturelle_vue:
            _ajouter(flags, text, m, "triade", "Trop de triades dans le post : garde la première, casse les autres.", "faible")
        else:
            naturelle_vue = True

    # Connecteurs en pluie : 2 débuts de phrase connecteurs ou plus.
    conn = lex.get("connecteurs_debut", [])
    if conn:
        hits = list(re.finditer(r"(?:^|(?<=[.!?]\s)|(?<=\n))(" + "|".join(map(re.escape, conn)) + r")\b", text))
        if len(hits) >= 2:
            flags.append({"ligne": _ligne(text, hits[0].start()), "debut": hits[0].start(),
                          "extrait": ", ".join(h.group(1) for h in hits[:4]), "famille": "connecteurs-en-pluie",
                          "force": "fort", "niveau": "strict",
                          "conseil": f"{len(hits)} phrases ouvertes par un connecteur. Supprime-en la plupart."})

    # Dédoublonnage : un même passage n'est compté qu'une fois par famille.
    vus, uniques = set(), []
    for f in sorted(flags, key=lambda f: f["debut"]):
        cle = (f["debut"], f["famille"])
        if cle not in vus:
            vus.add(cle)
            uniques.append(f)
    return uniques


def densite(text, flags):
    """Marqueurs par paragraphe et action à mener (doctrine « 3 = réécrire »)."""
    paras = paragraphes(text)
    starts = [s for s, _ in paras]
    compte = [[] for _ in paras]
    vus = set()
    for f in flags:
        if f["famille"] in ("forensique",) or not paras or f["debut"] in vus:
            continue
        vus.add(f["debut"])  # un même passage pris par deux familles compte une fois
        compte[_paragraphe_de(starts, f["debut"])].append(f)
    out = []
    for i, (s, p) in enumerate(paras):
        fs = compte[i]
        forts = [f for f in fs if f["force"] == "fort"]
        n = len(fs)
        if n >= 3:
            action = "RÉÉCRIRE LE PARAGRAPHE"
        elif forts:
            action = "REMPLACER"
        elif n == 2:
            action = "REMPLACER LE PLUS FAIBLE"
        else:
            action = "LAISSER"
        out.append({"paragraphe": i + 1, "ligne": _ligne(text, s), "marqueurs": n, "forts": len(forts),
                    "action": action, "extraits": [f["extrait"] for f in fs][:5],
                    "debut_texte": p.strip()[:50]})
    return out


def rythme(text, flags=None):
    """Problèmes de rythme : plat mécanique, fragments, staccato, alternance fabriquée."""
    problemes = []
    toutes = []
    for s, p in paragraphes(text):
        ph = phrases(p)
        toutes += ph
        longueurs = [len(MOT.findall(x)) for x in ph]
        if len(ph) >= 4:
            moy = statistics.mean(longueurs)
            if all(abs(n - moy) <= 3 for n in longueurs) and not any(SUBORDONNEES.search(x) for x in ph):
                problemes.append({"type": "paragraphe plat", "ligne": _ligne(text, s),
                                  "detail": f"{len(ph)} phrases de ~{moy:.0f} mots, aucune subordonnée",
                                  "conseil": "Relie UNE phrase à sa voisine par une subordonnée qui travaille (parce que, quand, qui). Une seule fois."})
    longueurs = [len(MOT.findall(x)) for x in toutes]
    fragments = [x for x, n in zip(toutes, longueurs) if n < 4 and not x.startswith("#")]
    if len(fragments) > 2:
        problemes.append({"type": "fragments", "ligne": None,
                          "detail": f"{len(fragments)} fragments de moins de 4 mots (2 au plus par post) : " + " / ".join(fragments[:4]),
                          "conseil": "Rattache les fragments en trop à la phrase voisine (virgule ou deux-points)."})
    # Alternance mécanique long/court sur 6 phrases ou plus.
    serie = 0
    for a, b in zip(longueurs, longueurs[1:]):
        alterne = (a >= 15 and b <= 6) or (a <= 6 and b >= 15)
        serie = serie + 1 if alterne else 0
        if serie >= 5:
            problemes.append({"type": "alternance fabriquée", "ligne": None,
                              "detail": "long, court, long, court sur 6 phrases",
                              "conseil": "Cette bascule est l'empreinte des humaniseurs. Fusionne une phrase courte avec sa voisine."})
            break
    for f in flags or []:
        if f["famille"] == "staccato":
            problemes.append({"type": "staccato", "ligne": f["ligne"], "detail": f["extrait"], "conseil": f["conseil"]})
    return {"phrases": len(toutes), "longueurs": longueurs, "problemes": problemes}
