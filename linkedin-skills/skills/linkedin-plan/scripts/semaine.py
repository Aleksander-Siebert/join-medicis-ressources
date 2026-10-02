#!/usr/bin/env python3
"""semaine.py : contrôle et exporte le plan LinkedIn d'une semaine.

  python3 semaine.py --plan plan.json [--journal journal.md] [--apprentissages apprentissages.md]
                     [--minutes 240] [--export csv|json] [--json]
  python3 semaine.py --exemple

Contrôles :
  BLOQUANT
    - une formule notée « ne marche pas » dans apprentissages.md, reprogrammée
    - la même formule deux fois en 7 jours (plan + posts récents du journal)
    - un pilier au-delà de 60% des posts (semaine + 3 semaines précédentes)
    - formule inconnue de linkedin-post/formules.json
    - temps nécessaire au-delà du budget de la semaine (--minutes)
  ATTENTION
    - objectifs trop peu variés (3 posts ou plus : au moins 3 objectifs)
    - objectif absent de ceux que sert la formule
    - deux posts le même jour, ou le même objectif deux jours de suite
    - angle absent ou trop vague (« un angle, pas un sujet »)
    - jour férié ou pont en France, mois d'août, fin décembre
    - liste d'engagement hors 10 personnes ou sans acheteur

Le temps se compte avec les coûts de /linkedin-strategie (budget.py) : par
post, sa rédaction + 20 min de réponses ; 15 min de routine par jour ouvré.

Format de plan.json :
  {"semaine": "2026-10-05",
   "creneaux": [{"jour": "2026-10-06", "heure": "08:15", "formule": "chiffre-d-abord",
                 "objectif": "sauvegardes", "pilier": "Rétention", "format": "texte",
                 "angle": "les 60 appels aux résiliés"}],
   "personnes": [{"nom": "…", "groupe": "pair|portee|acheteur"}]}

Codes de sortie : 0 OK, 2 attention, 3 bloquant, 1 erreur.

Règles d'après Serge Bulaev (linkedin-skills, planning, MIT) : mélange des
objectifs, pas de formule répétée en 7 jours, aucun pilier au-delà de 60% ;
Joshua (di-li-plan, MIT) : ne pas reprogrammer ce que l'audit a écarté.
Sans dépendance.
"""

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from datetime import date, timedelta
from pathlib import Path

ICI = Path(__file__).resolve().parent
FORMULES = ICI.parents[1] / "linkedin-post" / "formules.json"
COUT = {"texte": 25, "image": 30, "carrousel": 90, "video": 120, "sondage": 20, "article": 180, "newsletter": 150}
REPONSES = 20
ROUTINE = 15
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

EXEMPLE = {
    "semaine": "2026-10-05",
    "creneaux": [
        {"jour": "2026-10-06", "heure": "08:15", "formule": "chiffre-d-abord", "objectif": "sauvegardes",
         "pilier": "Rétention", "format": "texte", "angle": "les 60 appels aux résiliés : la moitié parlait du délai"},
        {"jour": "2026-10-08", "heure": "08:00", "formule": "chiffre-d-abord", "objectif": "commentaires",
         "pilier": "Rétention", "format": "carrousel", "angle": "les 5 questions du script d'appel"},
        {"jour": "2026-10-09", "heure": "08:30", "formule": "contre-pied", "objectif": "commentaires",
         "pilier": "Rétention", "format": "texte", "angle": "l'IA"},
    ],
    "personnes": [{"nom": f"Pair {i}", "groupe": "pair"} for i in range(1, 7)] +
                 [{"nom": "Portée 1", "groupe": "portee"}, {"nom": "Portée 2", "groupe": "portee"}],
}


def norme(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'").strip()


def paques(annee):
    a, b, c = annee % 19, annee // 100, annee % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mois = (h + l - 7 * m + 114) // 31
    jour = (h + l - 7 * m + 114) % 31 + 1
    return date(annee, mois, jour)


def feries(annee):
    p = paques(annee)
    f = {date(annee, 1, 1): "Jour de l'an", p + timedelta(days=1): "lundi de Pâques", date(annee, 5, 1): "1er mai",
         date(annee, 5, 8): "8 mai", p + timedelta(days=39): "Ascension", p + timedelta(days=50): "lundi de Pentecôte",
         date(annee, 7, 14): "14 juillet", date(annee, 8, 15): "15 août", date(annee, 11, 1): "Toussaint",
         date(annee, 11, 11): "11 novembre", date(annee, 12, 25): "Noël"}
    ponts = {}
    for d, nom in f.items():
        if d.weekday() == 3:
            ponts[d + timedelta(days=1)] = f"pont ({nom})"
        elif d.weekday() == 1:
            ponts[d - timedelta(days=1)] = f"pont ({nom})"
    return f, ponts


def lire_jour(t):
    try:
        return date.fromisoformat(str(t)[:10])
    except ValueError:
        return None


def posts_journal(chemin):
    """Lignes du tableau « Posts » de journal.md : date, formule, objectif, format, pilier."""
    if not chemin or not Path(chemin).exists():
        return []
    texte = Path(chemin).read_text(encoding="utf-8")
    m = re.search(r"## Posts[^\n]*\n(?:[^|\n][^\n]*\n|\n)*((?:\|.*\n?)+)", texte)
    if not m:
        return []
    lignes = m.group(1).splitlines()
    entete = [norme(c) for c in lignes[0].strip().strip("|").split("|")]
    out = []
    for l in lignes[2:]:
        cel = [c.strip() for c in l.strip().strip("|").split("|")]
        ligne = dict(zip(entete, cel))
        d = lire_jour(ligne.get("date", ""))
        if d:
            out.append({"jour": d, "formule": ligne.get("formule", ""), "objectif": ligne.get("objectif", ""),
                        "pilier": ligne.get("pilier", ""), "format": ligne.get("format", "")})
    return out


def formules_ecartees(chemin):
    """Formules citées dans la section « Ce qui ne marche pas pour moi » d'apprentissages.md."""
    if not chemin or not Path(chemin).exists():
        return ""
    texte = Path(chemin).read_text(encoding="utf-8")
    m = re.search(r"## Ce qui ne marche pas[^\n]*\n(.*?)(?=\n## |\Z)", texte, re.S)
    return norme(m.group(1)) if m else ""


def charger_formules(chemin=FORMULES):
    try:
        d = json.loads(Path(chemin).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return {f["id"]: f for f in d.get("accroches", []) + d.get("structurelles", [])}


def controler(plan, historique=(), ecartees="", minutes=None, formules=None):
    bloquants, attentions = [], []
    cren = sorted(plan.get("creneaux", []), key=lambda c: (str(c.get("jour")), str(c.get("heure"))))
    for c in cren:
        c["_jour"] = lire_jour(c.get("jour"))
    if formules is None:
        formules = charger_formules()
    if formules is None:
        attentions.append("formules.json de /linkedin-post introuvable : les formules ne sont pas vérifiées.")

    for c in cren:
        fid = c.get("formule", "")
        if formules is not None and fid and fid not in formules:
            bloquants.append(f"{c.get('jour')} : formule « {fid} » inconnue de linkedin-post/formules.json.")
        elif formules is not None and fid and c.get("objectif") and c["objectif"] not in formules[fid].get("objectif", []):
            attentions.append(f"{c.get('jour')} : « {fid} » sert plutôt {', '.join(formules[fid].get('objectif', []))}, pas {c['objectif']}.")
        if fid and ecartees and re.search(rf"(?<![\w-]){re.escape(norme(fid))}(?![\w-])", ecartees):
            bloquants.append(f"{c.get('jour')} : « {fid} » figure dans « Ce qui ne marche pas pour moi » (apprentissages.md). Ne pas la reprogrammer sans nouvelle expérience.")
        angle = (c.get("angle") or "").strip()
        if len(angle.split()) < 4:
            attentions.append(f"{c.get('jour')} : angle « {angle or 'absent'} » : un angle, pas un sujet (ce qui s'est passé, le chiffre, la scène).")

    # même formule en 7 jours
    tous = [(h["jour"], h["formule"], "journal") for h in historique] + [(c["_jour"], c.get("formule", ""), "plan") for c in cren if c["_jour"]]
    tous.sort()
    signale = set()
    for i, (d1, f1, s1) in enumerate(tous):
        for d2, f2, s2 in tous[i + 1:]:
            if f1 and f1 == f2 and (d2 - d1).days < 7 and "plan" in (s1, s2) and (f1, d2) not in signale:
                signale.add((f1, d2))
                bloquants.append(f"« {f1} » le {d1.isoformat()} et le {d2.isoformat()} : pas deux fois la même formule en 7 jours.")

    # piliers sur 4 semaines
    debut = min([c["_jour"] for c in cren if c["_jour"]] or [date.today()])
    recents = [h for h in historique if 0 <= (debut - h["jour"]).days <= 21]
    noms = {norme(x): x for x in [h["pilier"] for h in recents] + [c.get("pilier", "") for c in cren] if x}
    piliers = [norme(h["pilier"]) for h in recents if h["pilier"]] + [norme(c.get("pilier")) for c in cren if c.get("pilier")]
    if len(piliers) >= 3:
        for p in set(piliers):
            part = piliers.count(p) / len(piliers)
            if part > 0.6:
                bloquants.append(f"Pilier « {noms[p]} » : {round(part * 100)}% des {len(piliers)} posts sur 4 semaines. Aucun pilier au-delà de 60%.")

    # objectifs
    objectifs = [c.get("objectif") for c in cren if c.get("objectif")]
    if len(cren) >= 3 and len(set(objectifs)) < 3:
        attentions.append(f"Objectifs de la semaine : {', '.join(sorted(set(objectifs))) or 'aucun'}. Avec {len(cren)} posts, vise au moins 3 objectifs différents (commentaires, partages, réactions, sauvegardes).")
    for a, b in zip(cren, cren[1:]):
        if a["_jour"] and b["_jour"]:
            if a["_jour"] == b["_jour"]:
                attentions.append(f"Deux posts le {a['_jour'].isoformat()} : le second coupe la diffusion du premier.")
            elif (b["_jour"] - a["_jour"]).days == 1 and a.get("objectif") == b.get("objectif"):
                attentions.append(f"{a['_jour'].isoformat()} et {b['_jour'].isoformat()} : même objectif deux jours de suite.")

    # calendrier français
    for c in cren:
        d = c["_jour"]
        if not d:
            continue
        f, ponts = feries(d.year)
        if d in f:
            attentions.append(f"{d.isoformat()} : {f[d]}, jour férié. Audience B2B absente : décale ou garde un post personnel.")
        elif d in ponts:
            attentions.append(f"{d.isoformat()} : {ponts[d]}. Beaucoup de lecteurs B2B absents.")
        elif d.month == 8:
            attentions.append(f"{d.isoformat()} : août, audience B2B réduite. Allège ou passe en semaine d'engagement. [praticien]")
        elif d.month == 12 and d.day >= 24 or d.month == 1 and d.day == 1:
            attentions.append(f"{d.isoformat()} : fêtes de fin d'année, audience B2B réduite. [praticien]")

    # temps
    besoin = sum(COUT.get(norme(c.get("format", "texte")), COUT["texte"]) + REPONSES for c in cren) + ROUTINE * 5
    if minutes is not None and besoin > minutes:
        bloquants.append(f"Il faut environ {besoin} minutes ({len(cren)} posts avec réponses + 15 min de routine par jour ouvré) pour {minutes} disponibles. "
                         "Retire un post ou passe un carrousel en texte : un post de moins vaut mieux qu'un post bâclé.")

    # liste d'engagement
    pers = plan.get("personnes") or []
    if pers:
        groupes = {g: sum(1 for p in pers if p.get("groupe") == g) for g in ("pair", "portee", "acheteur")}
        if len(pers) != 10:
            attentions.append(f"Liste d'engagement de {len(pers)} personnes : 10 se suivent sans tableur (6 pairs, 2 de portée, 2 acheteurs).")
        if not groupes["acheteur"]:
            attentions.append("Aucun acheteur dans la liste : ajoute 1 ou 2 personnes qui pourraient acheter, à commenter des semaines avant tout message.")
    else:
        attentions.append("Pas de liste d'engagement : 10 personnes (6 pairs, 2 de portée, 2 acheteurs).")

    verdict, code = ("BLOQUÉ", 3) if bloquants else ("À REVOIR", 2) if attentions else ("PRÊT", 0)
    return {"verdict": verdict, "code": code, "posts": len(cren), "minutes_necessaires": besoin,
            "bloquants": bloquants, "attentions": attentions}


def exporter(plan, fmt):
    lignes = []
    for c in sorted(plan.get("creneaux", []), key=lambda c: (str(c.get("jour")), str(c.get("heure")))):
        d = lire_jour(c.get("jour"))
        lignes.append({"Date": c.get("jour", ""), "Jour": JOURS[d.weekday()] if d else "", "Heure": c.get("heure", ""),
                       "Formule": c.get("formule", ""), "Objectif": c.get("objectif", ""), "Pilier": c.get("pilier", ""),
                       "Format": c.get("format", ""), "Angle": c.get("angle", ""), "Statut": "à écrire",
                       "Réponses": f"{c.get('heure', '')} + 30 min, bloquer le créneau"})
    if fmt == "json":
        return json.dumps(lignes, ensure_ascii=False, indent=2)
    buf = io.StringIO()
    if lignes:
        w = csv.DictWriter(buf, fieldnames=list(lignes[0]), delimiter=";")
        w.writeheader()
        w.writerows(lignes)
    return buf.getvalue()


def main():
    a = argparse.ArgumentParser(description="Contrôle et exporte le plan LinkedIn de la semaine.")
    a.add_argument("--plan")
    a.add_argument("--journal")
    a.add_argument("--apprentissages")
    a.add_argument("--minutes", type=int)
    a.add_argument("--export", choices=["csv", "json"])
    a.add_argument("--json", action="store_true")
    a.add_argument("--exemple", action="store_true")
    x = a.parse_args()
    try:
        if x.exemple:
            plan = json.loads(json.dumps(EXEMPLE))
        elif x.plan:
            plan = json.loads(Path(x.plan).read_text(encoding="utf-8"))
        else:
            a.error("--plan ou --exemple")
        if x.export:
            print(exporter(plan, x.export), end="")
            return 0
        r = controler(plan, posts_journal(x.journal), formules_ecartees(x.apprentissages), x.minutes)
    except (OSError, json.JSONDecodeError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    if x.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"PLAN  {r['verdict']}  ·  {r['posts']} posts · environ {r['minutes_necessaires']} min")
        for b in r["bloquants"]:
            print(f"  ✖ {b}")
        for t in r["attentions"]:
            print(f"  ! {t}")
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
