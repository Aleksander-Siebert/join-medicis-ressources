#!/usr/bin/env python3
"""ambassadeurs.py : programme d'ambassadeurs salariés (plan, relecture).

  plan --fichier equipe.json [--semaine N]
      Rythme par personne selon le rôle et l'ancienneté, montée en charge sur
      8 semaines, temps total de l'équipe, alertes (plancher, plafond).
  relecture --texte "brouillon" [--clients "A,B"] [--concurrents "X,Y"]
      Classe un brouillon de salarié :
        A  sans relecture (opinion, histoire, leçon personnelle) ;
        B  relecture des faits par le marketing, objectif 4 h ouvrées,
           accord tacite à 24 h (client nommé, chiffre interne, concurrent,
           annonce) ;
        C  accord explicite sous 48 h (sujet réglementé, prévision financière,
           litige, données personnelles).
      Le marketing relit les FAITS, jamais la voix.

Codes de sortie : plan 0 (2 si alertes) ; relecture 0 = A, 2 = B, 3 = C ;
1 erreur.

Rythmes d'après team-cadence-matrix.md et la gouvernance de
linkedin-employee-advocacy (Serge Bulaev, MIT) : ce sont des repères de
praticien, à ajuster avec les données de /linkedin-audit. Sans dépendance.

Format de equipe.json :
  {"membres": [{"nom": "Inès", "role": "marketing", "seniorite": "confirme"}, …]}
  rôles : dirigeant, directeur, marketing, commercial, produit, service-client
  séniorité : senior, confirme, junior (ignorée pour dirigeant et directeur)
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# (posts/semaine, commentaires/semaine, repartages/semaine, minutes/semaine) : valeurs basses de la fourchette.
MATRICE = {
    ("dirigeant", None): (3, 30, 2, 180),
    ("directeur", None): (1, 15, 1, 90),
    ("marketing", "senior"): (2, 15, 1, 120),
    ("marketing", "confirme"): (1, 10, 1, 60),
    ("marketing", "junior"): (1, 5, 1, 60),
    ("commercial", "senior"): (1, 25, 1, 90),
    ("commercial", "confirme"): (1, 15, 1, 60),
    ("commercial", "junior"): (0, 10, 0, 30),
    ("produit", "senior"): (1, 5, 1, 60),
    ("produit", "confirme"): (0, 3, 0, 30),
    ("produit", "junior"): (0, 3, 0, 30),
    ("service-client", "senior"): (1, 10, 1, 60),
    ("service-client", "confirme"): (0, 5, 0, 30),
    ("service-client", "junior"): (0, 5, 0, 30),
}
PALIERS = [((1, 2), "écouter", 0.0, None), ((3, 4), "premier post", None, 1), ((5, 8), "mi-régime", 0.5, None),
           ((9, 99), "régime", 1.0, None)]

EXEMPLE_EQUIPE = {"membres": [
    {"nom": "Directrice générale", "role": "dirigeant"},
    {"nom": "Camille", "role": "marketing", "seniorite": "senior"},
    {"nom": "Inès", "role": "marketing", "seniorite": "confirme"},
    {"nom": "Karim", "role": "commercial", "seniorite": "senior"},
    {"nom": "Léa", "role": "service-client", "seniorite": "confirme"},
]}

REGLEMENTE = r"\b(sante|patient\w*|medic\w*|diagnostic|conseil en investissement|placement|rendement garanti|bourse|amf|acpr|credit|pret|fiscal\w*|defiscalis\w*)\b"
PREVISION = r"\b(levee de fonds|on leve|rachat|acquisition de|fusion|introduction en bourse|resultats? (?:financiers|annuels)|chiffre d'affaires (?:previsionnel|attendu)|objectif de croissance|guidance|on va doubler)\b"
LITIGE = r"\b(proces|litige|plainte|tribunal|prud'?hom\w*|mise en demeure|contentieux|incident|fuite de donnees|panne)\b"
DONNEES = r"\b(donnees personnelles|nom du client|adresse|numero de|dossier medical|salaire de)\b"
CHIFFRE_INTERNE = r"\b(chiffre d'affaires|\bca\b|arr|mrr|marge|churn|attrition|taux de (?:retention|conversion|resiliation|transformation)|panier moyen|nombre de clients|budget)\b[^.\n]{0,40}\d|\d[^.\n]{0,20}\b(?:clients|contrats|assures|abonnes payants)\b"
ANNONCE = r"\b(on lance|nous lancons|bientot disponible|en avant-premiere|nouvelle offre|annonce|sortie prevue|a partir du \d)\b"


def norme(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'")


def cadence(role, seniorite):
    cle = (role, None) if role in ("dirigeant", "directeur") else (role, seniorite or "confirme")
    if cle not in MATRICE:
        raise ValueError(f"rôle ou séniorité inconnus : {role} / {seniorite}")
    return MATRICE[cle]


def palier(semaine):
    for (a, b), nom, part, posts_fixes in PALIERS:
        if a <= semaine <= b:
            return nom, part, posts_fixes
    return "régime", 1.0, None


def plan(equipe, semaine=None):
    lignes, alertes = [], []
    total = {"posts": 0, "commentaires": 0, "repartages": 0, "minutes": 0}
    for m in equipe.get("membres", []):
        p, c, r, mn = cadence(m.get("role"), m.get("seniorite"))
        if m.get("role") not in ("dirigeant",) and p >= 5:
            alertes.append(f"{m['nom']} : 5 posts ou plus par semaine, c'est un métier de créateur, pas d'ambassadeur.")
        ligne = {"nom": m["nom"], "role": m["role"], "cible": {"posts": p, "commentaires": c, "repartages": r, "minutes": mn}}
        if semaine:
            nom, part, fixes = palier(semaine)
            if fixes is not None:
                ps, cs = fixes if p else 0, round(c * 0.4)
            elif part == 0:
                ps, cs = 0, 5
            else:
                ps, cs = round(p * part), round(c * (0.75 if part < 1 else 1))
            ligne["semaine"] = {"palier": nom, "posts": ps, "commentaires": cs}
        if p < 1 or c < 5:
            ligne["hors_programme"] = True
            alertes.append(f"{m['nom']} : sous le plancher (1 post et 5 commentaires par semaine) ; à associer à un collègue, ou hors programme.")
        lignes.append(ligne)
        for k, v in (("posts", p), ("commentaires", c), ("repartages", r), ("minutes", mn)):
            total[k] += v
    return {"membres": lignes, "total_regime": total, "alertes": alertes,
            "rappel": "Chaque personne écrit dans sa voix ; jamais le même texte copié sur plusieurs comptes."}


def relecture(texte, clients=(), concurrents=()):
    t = norme(texte)
    c_raisons, b_raisons = [], []
    for motif, raison in ((REGLEMENTE, "sujet réglementé (santé, finance, crédit, fiscalité)"),
                          (PREVISION, "information financière ou prévision (levée, rachat, résultats)"),
                          (LITIGE, "litige, incident ou contentieux"),
                          (DONNEES, "données personnelles")):
        m = re.search(motif, t)
        if m:
            c_raisons.append(f"{raison} : « {m.group(0)} »")
    for nom in clients:
        if nom.strip() and re.search(rf"(?<!\w){re.escape(norme(nom.strip()))}(?!\w)", t):
            b_raisons.append(f"client nommé : {nom.strip()} (accord pour ce post ?)")
    for nom in concurrents:
        if nom.strip() and re.search(rf"(?<!\w){re.escape(norme(nom.strip()))}(?!\w)", t):
            b_raisons.append(f"concurrent nommé : {nom.strip()}")
    m = re.search(CHIFFRE_INTERNE, t)
    if m:
        b_raisons.append(f"chiffre interne possible : « {m.group(0).strip()} » (publiable ?)")
    m = re.search(ANNONCE, t)
    if m:
        b_raisons.append(f"annonce : « {m.group(0)} » (déjà annoncée officiellement ?)")
    if c_raisons:
        niveau, code, delai = "C", 3, "accord explicite sous 48 h (juridique ou direction)"
    elif b_raisons:
        niveau, code, delai = "B", 2, "relecture des faits par le marketing, objectif 4 h ouvrées, accord tacite à 24 h"
    else:
        niveau, code, delai = "A", 0, "aucune relecture : publier"
    return {"niveau": niveau, "code": code, "delai": delai, "raisons": c_raisons + b_raisons,
            "rappel": "Relire les faits, la confidentialité et la conformité. Ne jamais toucher à la voix, au ton, à l'accroche, aux opinions."}


def main():
    p = argparse.ArgumentParser(description="Programme d'ambassadeurs : plan de l'équipe, niveau de relecture d'un brouillon.")
    sous = p.add_subparsers(dest="cmd", required=True)
    pl = sous.add_parser("plan")
    pl.add_argument("--fichier")
    pl.add_argument("--exemple", action="store_true")
    pl.add_argument("--semaine", type=int, help="semaine du programme (montée en charge)")
    pl.add_argument("--json", action="store_true")
    rl = sous.add_parser("relecture")
    rl.add_argument("--texte", required=True)
    rl.add_argument("--clients", default="")
    rl.add_argument("--concurrents", default="")
    rl.add_argument("--json", action="store_true")
    a = p.parse_args()
    try:
        if a.cmd == "plan":
            eq = EXEMPLE_EQUIPE if a.exemple or not a.fichier else json.loads(Path(a.fichier).read_text(encoding="utf-8"))
            r = plan(eq, a.semaine)
            if a.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                print("PROGRAMME D'AMBASSADEURS" + (f" · semaine {a.semaine}" if a.semaine else ""))
                for l in r["membres"]:
                    c = l["cible"]
                    s = f"  {l['nom']:<20} régime : {c['posts']} post(s), {c['commentaires']} commentaires, {c['repartages']} repartage(s), ~{c['minutes']} min"
                    if "semaine" in l:
                        s += f" · cette semaine ({l['semaine']['palier']}) : {l['semaine']['posts']} post(s), {l['semaine']['commentaires']} commentaires"
                    print(s + ("  [hors programme]" if l.get("hors_programme") else ""))
                t = r["total_regime"]
                print(f"\n  Équipe au régime : {t['posts']} posts, {t['commentaires']} commentaires, {t['repartages']} repartages, ~{str(round(t['minutes'] / 60, 1)).replace('.', ',')} h par semaine")
                for x in r["alertes"]:
                    print(f"  ! {x}")
                print(f"  {r['rappel']}")
            return 2 if r["alertes"] else 0
        r = relecture(a.texte, a.clients.split(","), a.concurrents.split(","))
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print(f"RELECTURE  niveau {r['niveau']} : {r['delai']}")
            for x in r["raisons"]:
                print(f"  · {x}")
            print(f"  {r['rappel']}")
        return r["code"]
    except (OSError, ValueError, json.JSONDecodeError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
