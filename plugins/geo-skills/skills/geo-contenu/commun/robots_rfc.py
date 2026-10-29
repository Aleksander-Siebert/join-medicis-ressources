#!/usr/bin/env python3
"""robots_rfc.py : lecture de robots.txt selon la RFC 9309 (septembre 2022).

Module partagé du pack GEO (repris du pack SEO, testé). Le module robotparser
de Python applique la première règle qui correspond et ignore les jokers ;
ce module suit la RFC, que Google applique :

- groupe du robot (jeton, sans casse), sinon « * », sinon tout est permis ;
  plusieurs groupes pour le même robot sont fusionnés ;
- règle la plus longue ; à égalité, Allow l'emporte ; jokers « * » et « $ » ;
- robots.txt absent (4xx) : tout permis ; erreur serveur (5xx) ou non lu :
  tout interdit (RFC 9309 §2.3.1.4).

Sans ligne de commande : importé par les scripts du pack (acces.py).
"""
from __future__ import annotations

import re

class Erreur(Exception):
    pass


def lire_groupes(texte: str) -> list[dict]:
    """Groupes du fichier : {agents: [...], regles: [(allow, motif, ligne)]}."""
    groupes, courant, dernier_agent = [], None, False
    for n, brute in enumerate(texte.splitlines(), 1):
        ligne = brute.split("#", 1)[0].strip()
        if ":" not in ligne:
            continue
        cle, val = (x.strip() for x in ligne.split(":", 1))
        cle = cle.lower()
        if cle == "user-agent":
            # Des lignes user-agent consécutives ouvrent un même groupe.
            if courant is None or not dernier_agent:
                courant = {"agents": [], "regles": []}
                groupes.append(courant)
            courant["agents"].append(val.lower())
            dernier_agent = True
        elif cle in ("allow", "disallow"):
            dernier_agent = False
            if courant is None:
                continue  # règle hors groupe : ignorée (RFC 9309 §2.1)
            if cle == "disallow" and val == "":
                continue  # « Disallow: » vide n'interdit rien
            courant["regles"].append((cle == "allow", val, n))
        else:
            dernier_agent = False  # sitemap, crawl-delay… : ne ferment pas le groupe pour la RFC, mais séparent les agents
    return groupes


def groupe_pour(groupes: list[dict], robot: str) -> tuple[list, str]:
    """Règles qui s'appliquent au robot, et le groupe retenu ('jeton', '*' ou 'aucun')."""
    r = robot.lower()
    propres = [g for g in groupes if r in g["agents"]]
    if propres:
        return [x for g in propres for x in g["regles"]], robot
    etoile = [g for g in groupes if "*" in g["agents"]]
    if etoile:
        return [x for g in etoile for x in g["regles"]], "*"
    return [], "aucun"


def motif_regex(motif: str) -> re.Pattern:
    fin = motif.endswith("$")
    corps = motif[:-1] if fin else motif
    rx = "".join(".*" if c == "*" else re.escape(c) for c in corps)
    return re.compile("^" + rx + ("$" if fin else ""))


def decision(regles: list, chemin: str) -> tuple[bool, tuple | None]:
    """(autorisé, règle retenue). Règle la plus longue ; à égalité, Allow."""
    meilleure = None
    for allow, motif, ligne in regles:
        if motif_regex(motif).match(chemin):
            cle = (len(motif), allow)
            if meilleure is None or cle > meilleure[0]:
                meilleure = (cle, (allow, motif, ligne))
    if meilleure is None:
        return True, None
    return meilleure[1][0], meilleure[1]


def analyser(texte: str | None, chemins: list[str], robots: list[tuple], statut: int | None = 200) -> dict:
    if statut is None or statut >= 500:
        mode = "tout interdit (robots.txt en erreur serveur ou injoignable)"
        groupes = None
    elif statut >= 400:
        mode = "tout permis (robots.txt absent)"
        groupes = []
    else:
        mode = "lu"
        groupes = lire_groupes(texte or "")
    res = []
    for jeton, editeur, role in robots:
        ligne = {"robot": jeton, "editeur": editeur, "role": role, "acces": {}}
        if groupes is None:
            ligne["groupe"] = "aucun"
            ligne["acces"] = {c: {"autorise": False, "regle": "robots.txt indisponible"} for c in chemins}
        else:
            regles, g = groupe_pour(groupes, jeton)
            ligne["groupe"] = g
            for c in chemins:
                ok, r = decision(regles, c)
                ligne["acces"][c] = {"autorise": ok,
                                     "regle": f"{'Allow' if r[0] else 'Disallow'}: {r[1]} (ligne {r[2]})" if r else "aucune règle"}
        res.append(ligne)
    return {"mode": mode, "chemins": chemins, "robots": res}
