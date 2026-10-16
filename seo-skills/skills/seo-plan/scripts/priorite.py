#!/usr/bin/env python3
"""priorite.py : quelles idées produire d'abord, et un lot de pages en série tient-il ?

Deux commandes, sans dépendance :

  idees IDEES.csv [--poids 40,30,20,10] [--json]
      Note chaque idée de contenu de 1 à 10 sur quatre critères, pondérés :
        impact       le problème revient souvent chez les clients, il pèse ;
        adequation   l'offre le résout, on a une preuve ou un cas à montrer ;
        recherche    on le cherche (volume mesuré, ou requêtes réelles du site) ;
        ressources   facile à produire avec ce qu'on a (10 = peu d'effort).
      Poids par défaut 40/30/20/10, repris de la grille de content-strategy
      (marketingskills, Corey Haines, MIT) ; modifiables. Une note absente
      n'est pas inventée : l'idée sort « à compléter » et n'est pas classée.

  lot PAGES.csv --modele "Mutuelle {metier} à {ville}" [--colonnes metier,ville] [--json]
      Pages en série (SEO programmatique) : chaque ligne est une page. Contrôle
      ce qui rend une page « publiable seule » : des données propres à la page
      au-delà des variables du titre, pas de doublon, pas de champ vide. Un
      lot de plus de 100 pages est signalé : publier par lots de 50 à 100 et
      regarder l'indexation avant de continuer.

IDEES.csv : colonnes idee, impact, adequation, recherche, ressources (en-têtes
français, ordre libre, séparateur , ou ;). PAGES.csv : une ligne par page, une
colonne par donnée.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

CRITERES = ("impact", "adequation", "recherche", "ressources")
LOT_MAX = 100


class Erreur(Exception):
    pass


def plier(s: str) -> str:
    s = unicodedata.normalize("NFD", (s or "").strip().lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def lire_csv(chemin: str) -> list[dict]:
    try:
        brut = Path(chemin).read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise Erreur(f"fichier illisible : {chemin} ({exc})") from exc
    tete = brut.split("\n", 1)[0]
    sep = ";" if tete.count(";") > tete.count(",") else ","
    lignes = list(csv.DictReader(io.StringIO(brut), delimiter=sep))
    if not lignes:
        raise Erreur(f"{chemin} : aucune ligne")
    return [{plier(k): (v or "").strip() for k, v in l.items() if k} for l in lignes]


def note(v: str) -> float | None:
    v = v.replace(",", ".").strip()
    if not v:
        return None
    try:
        x = float(v)
    except ValueError:
        return None
    return x if 1 <= x <= 10 else None


def idees(lignes: list[dict], poids: tuple[float, ...]) -> dict:
    if "idee" not in lignes[0]:
        raise Erreur("colonne « idee » introuvable")
    manquantes = [c for c in CRITERES if c not in lignes[0]]
    if manquantes:
        raise Erreur(f"colonnes introuvables : {', '.join(manquantes)}")
    total_poids = sum(poids)
    classees, a_completer = [], []
    for l in lignes:
        notes = {c: note(l.get(c, "")) for c in CRITERES}
        vides = [c for c, v in notes.items() if v is None]
        if vides:
            a_completer.append({"idee": l["idee"], "manque": vides})
            continue
        score = sum(notes[c] * p for c, p in zip(CRITERES, poids)) / total_poids
        classees.append({"idee": l["idee"], **notes, "score": round(score, 2)})
    classees.sort(key=lambda x: -x["score"])
    return {"poids": dict(zip(CRITERES, poids)), "classees": classees, "a_completer": a_completer}


def afficher_idees(r: dict) -> str:
    p = r["poids"]
    out = [f"PRIORITÉS · impact {p['impact']:g} · adéquation {p['adequation']:g} · recherche {p['recherche']:g} · ressources {p['ressources']:g}"]
    for i, x in enumerate(r["classees"], 1):
        out.append(f"  {i:>2}. {str(x['score']).replace('.', ','):>5}  {x['idee']}  "
                   f"({x['impact']:g} · {x['adequation']:g} · {x['recherche']:g} · {x['ressources']:g})")
    for x in r["a_completer"]:
        out.append(f"   à compléter : {x['idee']} (note manquante ou hors 1-10 : {', '.join(x['manque'])})")
    out.append("Une note est un jugement : dis d'où vient chacune (entretiens, Search Console, volume mesuré).")
    return "\n".join(out)


def rempli(v: str) -> bool:
    """Un trou « {{à compléter}} » n'est pas une donnée."""
    return bool(v) and not re.fullmatch(r"\{\{[^}]*\}\}", v.strip())


def lot(lignes: list[dict], modele: str, colonnes: list[str] | None) -> dict:
    variables = [plier(v) for v in re.findall(r"\{(\w+)\}", modele)]
    entetes = list(lignes[0].keys())
    absentes = [v for v in variables if v not in entetes]
    if absentes:
        raise Erreur(f"variables du modèle absentes du fichier : {', '.join(absentes)}")
    donnees = [plier(c) for c in colonnes] if colonnes else [h for h in entetes if h not in variables]
    titres, doublons, vides, pauvres = {}, [], [], []
    for i, l in enumerate(lignes, 2):
        titre = modele
        for v in re.findall(r"\{(\w+)\}", modele):
            titre = titre.replace("{" + v + "}", l.get(plier(v), ""))
        cle = plier(titre)
        if cle in titres:
            doublons.append({"ligne": i, "titre": titre, "meme_que": titres[cle]})
        else:
            titres[cle] = i
        manquent = [d for d in donnees if not rempli(l.get(d, ""))]
        if manquent:
            vides.append({"ligne": i, "titre": titre, "champs": manquent})
        if not [d for d in donnees if rempli(l.get(d, ""))]:
            pauvres.append({"ligne": i, "titre": titre})
    # Une donnée identique sur toutes les pages n'apporte rien de propre à chacune.
    constantes = [d for d in donnees if len({l.get(d, "") for l in lignes}) == 1]
    publiables = len(lignes) - len({x["ligne"] for x in doublons + vides + pauvres})
    alertes = []
    if not donnees or len(constantes) == len(donnees):
        alertes.append("aucune donnée ne varie d'une page à l'autre en dehors du titre : pages interchangeables, à ne pas publier")
    if len(lignes) > LOT_MAX:
        alertes.append(f"{len(lignes)} pages : publier par lots de 50 à {LOT_MAX} et suivre l'indexation avant le lot suivant")
    if alertes and alertes[0].startswith("aucune"):
        publiables = 0
    verdict = "À NE PAS PUBLIER" if alertes and alertes[0].startswith("aucune") else (
        "À REVOIR" if doublons or vides or pauvres or alertes else "PUBLIABLE")
    return {"pages": len(lignes), "variables": variables, "donnees": donnees, "constantes": constantes,
            "doublons": doublons, "champs_vides": vides, "sans_donnee": pauvres, "publiables": publiables,
            "alertes": alertes, "verdict": verdict}


def afficher_lot(r: dict) -> str:
    out = [f"LOT · {r['pages']} pages · variables du titre : {', '.join(r['variables'])} · données : {', '.join(r['donnees']) or 'aucune'}",
           f"  publiables seules : {r['publiables']} sur {r['pages']}"]
    if r["constantes"]:
        out.append(f"  identiques partout (n'apportent rien de propre) : {', '.join(r['constantes'])}")
    for d in r["doublons"][:10]:
        out.append(f"  doublon ligne {d['ligne']} : « {d['titre']} » (déjà ligne {d['meme_que']})")
    for d in r["champs_vides"][:10]:
        out.append(f"  ligne {d['ligne']} « {d['titre']} » : vide ({', '.join(d['champs'])})")
    out += [f"  ALERTE · {a}" for a in r["alertes"]]
    out.append(f"VERDICT · {r['verdict']}")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Priorité des idées de contenu, et contrôle d'un lot de pages en série.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("idees")
    p.add_argument("fichier")
    p.add_argument("--poids", default="40,30,20,10")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("lot")
    p.add_argument("fichier")
    p.add_argument("--modele", required=True, help="modèle de titre, ex. « Mutuelle {metier} à {ville} »")
    p.add_argument("--colonnes", help="colonnes de données propres à chaque page (défaut : toutes sauf les variables)")
    p.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        lignes = lire_csv(a.fichier)
        if a.cmd == "idees":
            try:
                poids = tuple(float(x) for x in a.poids.split(","))
            except ValueError as exc:
                raise Erreur(f"--poids illisible : {a.poids}") from exc
            if len(poids) != 4 or sum(poids) <= 0:
                raise Erreur("--poids attend 4 nombres, ex. 40,30,20,10")
            r = idees(lignes, poids)
            print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher_idees(r))
            return 0
        r = lot(lignes, a.modele, a.colonnes.split(",") if a.colonnes else None)
        print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher_lot(r))
        return {"PUBLIABLE": 0, "À REVOIR": 2, "À NE PAS PUBLIER": 3}[r["verdict"]]
    except Erreur as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
