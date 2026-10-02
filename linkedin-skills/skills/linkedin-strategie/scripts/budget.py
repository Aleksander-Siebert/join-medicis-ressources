#!/usr/bin/env python3
"""budget.py : dimensionne une semaine LinkedIn sur le temps qui existe vraiment.

Les plans LinkedIn échouent rarement faute d'idées. Ils échouent la 5e
semaine, quand le plan supposait six heures et qu'il en reste une et demie. Ce
script chiffre chaque activité en minutes, répartit le budget selon l'étape du
compte, refuse un objectif qu'il ne peut pas payer et rend la semaine minimale
à tenir quand tout déraille.

Étapes :
  depart        moins d'environ 1 000 abonnés, ou reprise après une longue pause
                → 60% du temps en commentaires sous les posts des autres
  reconstruction une audience existe mais s'est endormie → 45%
  etabli        les posts touchent régulièrement des non-relations → 30%

Sous 90 minutes par semaine : pas de plan de publication, une semaine
« commentaires seulement » (un rythme abandonné en 5e semaine se voit sur le
profil, c'est pire que de ne pas commencer).

Codes de sortie :
  0  le plan tient dans le budget
  2  budget sous le plancher : semaine « commentaires seulement »
  3  l'objectif demandé ne tient pas : le dépassement est chiffré
  1  erreur d'utilisation

Coûts en minutes repris de cadence_planner.py (alirezarezvani/claude-skills,
MIT) : ce sont des ordres de grandeur de praticien, à remplacer par les
temps mesurés de l'utilisateur (--cout format=minutes). Sans dépendance.

Exemples :
  python3 budget.py --minutes 240 --etape depart --posts 2
  python3 budget.py --minutes 300 --etape etabli --posts 3 --formats texte,carrousel,texte
  python3 budget.py --minutes 60
  python3 budget.py --minutes 300 --posts 3 --cout texte=40 --json
"""

import argparse
import json
import sys

COUT = {
    "texte": 25,
    "image": 30,
    "carrousel": 90,
    "video": 120,
    "sondage": 20,
    "article": 180,
    "newsletter": 150,
    "commentaire": 6,
    "message": 5,
    "reponses": 20,  # répondre sous son propre post, par post publié
}
PLANCHER = 90

ETAPES = {
    "depart": {"libelle": "moins d'environ 1 000 abonnés, ou reprise après une longue pause",
               "part_engagement": 0.60, "commentaires_par_jour": 5,
               "pourquoi": "Tes posts n'ont presque pas de diffusion. Un commentaire utile sous un post qui a déjà une audience est le seul levier qui marche à partir de zéro."},
    "reconstruction": {"libelle": "une audience existe mais ne réagit plus",
                       "part_engagement": 0.45, "commentaires_par_jour": 3,
                       "pourquoi": "La portée revient avec la régularité, pas avec un gros coup. Partage le temps pendant que le rythme se réinstalle."},
    "etabli": {"libelle": "les posts touchent régulièrement des personnes hors de ton réseau",
               "part_engagement": 0.30, "commentaires_par_jour": 2,
               "pourquoi": "La diffusion fonctionne : la contrainte devient la qualité et la régularité de ce que tu publies."},
}


def planifier(minutes, etape="depart", posts=None, formats=None, messages=0, cout=None):
    cout = {**COUT, **(cout or {})}
    e = ETAPES[etape]
    jours = 5
    minimale = {
        "posts": 1,
        "commentaires_par_jour_ouvre": 1,
        "minutes": cout["texte"] + cout["reponses"] + 5 * cout["commentaire"],
        "regle": "1 post texte le même jour chaque semaine, 1 commentaire utile par jour ouvré, réponse à chaque commentaire sous 24 h.",
    }
    if minutes < PLANCHER:
        n = max(1, minutes // cout["commentaire"])
        return {
            "verdict": "SOUS LE PLANCHER", "code": 2, "minutes": minutes, "plancher": PLANCHER,
            "plan": {"posts": 0, "commentaires": n, "minutes_utilisees": n * cout["commentaire"]},
            "constat": f"{minutes} min/semaine : pas assez pour publier ET répondre sans abandonner en route. "
                       f"Semaine « commentaires seulement » : {n} commentaires utiles, sous des posts de ta cible.",
            "semaine_minimale": minimale,
        }

    engagement = round(minutes * e["part_engagement"])
    publication = minutes - engagement
    if formats:
        liste = [f.strip() for f in formats.split(",") if f.strip()]
    else:
        liste = ["texte"] * (posts if posts else max(1, publication // (cout["texte"] + cout["reponses"])))
    inconnus = [f for f in liste if f not in cout]
    if inconnus:
        raise ValueError(f"format inconnu : {', '.join(inconnus)} (connus : {', '.join(k for k in cout if k not in ('commentaire', 'message', 'reponses'))})")
    cout_posts = sum(cout[f] + cout["reponses"] for f in liste)
    cout_messages = messages * cout["message"]
    comm_mini = e["commentaires_par_jour"] * jours
    cout_comm_mini = comm_mini * cout["commentaire"]
    besoin = cout_posts + cout_messages + cout_comm_mini
    constats = []

    if besoin > minutes:
        depasse = besoin - minutes
        tient = 0
        reste = minutes - cout_comm_mini - cout_messages
        for f in liste:
            if reste >= cout[f] + cout["reponses"]:
                tient += 1
                reste -= cout[f] + cout["reponses"]
        return {
            "verdict": "NE TIENT PAS", "code": 3, "minutes": minutes, "etape": etape,
            "besoin": besoin, "depassement": depasse,
            "constat": f"Le plan demande {besoin} min pour {minutes} disponibles ({depasse} de trop). "
                       f"À ce budget : {tient} post(s) de ce type, plus {comm_mini} commentaires.",
            "detail": {"posts": cout_posts, "commentaires_minimum": cout_comm_mini, "messages": cout_messages},
            "semaine_minimale": minimale,
        }

    reste = minutes - besoin
    comm_total = comm_mini + reste // cout["commentaire"] if reste > 0 else comm_mini
    part_reelle = round(100 * (minutes - cout_posts) / minutes)
    if part_reelle < e["part_engagement"] * 100 - 10:
        constats.append(f"Seulement {part_reelle}% du temps hors publication, pour {round(e['part_engagement'] * 100)}% conseillés à cette étape : "
                        "un post de moins et plus de commentaires rapporteraient davantage.")
    if any(f == "video" for f in liste):
        constats.append("Vidéo : seulement si tu as la caméra, le lieu et l'envie de le refaire chaque semaine.")
    if any(f == "newsletter" for f in liste):
        constats.append("Newsletter : vérifie l'éligibilité (plus de 150 abonnés ou relations, critère officiel) et tiens 6 mois (voir references/rythme-newsletter.md).")
    return {
        "verdict": "TIENT", "code": 0, "minutes": minutes, "etape": etape,
        "etape_libelle": e["libelle"], "pourquoi": e["pourquoi"],
        "plan": {
            "posts": liste,
            "minutes_posts": cout_posts,
            "commentaires": comm_total,
            "commentaires_par_jour": round(comm_total / jours, 1),
            "messages": messages,
            "minutes_utilisees": cout_posts + cout_messages + comm_total * cout["commentaire"],
        },
        "constats": constats,
        "semaine_minimale": minimale,
        "couts_utilises": {k: cout[k] for k in set(liste) | {"commentaire", "reponses"}},
    }


def afficher(r):
    L = [f"BUDGET LINKEDIN  {r['verdict']}  ·  {r['minutes']} min/semaine"]
    if r["code"] == 2:
        L += ["", r["constat"]]
    elif r["code"] == 3:
        L += ["", r["constat"],
              f"  posts : {r['detail']['posts']} min · commentaires minimum : {r['detail']['commentaires_minimum']} min"
              f" · messages : {r['detail']['messages']} min"]
    else:
        p = r["plan"]
        L += [f"Étape : {r['etape']} ({r['etape_libelle']})", f"  {r['pourquoi']}", "",
              f"Posts : {len(p['posts'])} ({', '.join(p['posts'])}), {p['minutes_posts']} min réponses comprises",
              f"Commentaires : {p['commentaires']} ({p['commentaires_par_jour']} par jour ouvré)",
              f"Messages : {p['messages']}",
              f"Total : {p['minutes_utilisees']} min sur {r['minutes']}"]
        for c in r["constats"]:
            L.append(f"  ! {c}")
    m = r["semaine_minimale"]
    L += ["", f"Semaine minimale (quand tout déraille, ~{m['minutes']} min) : {m['regle']}",
          "Coûts = ordres de grandeur de praticien. Remplace-les par tes temps mesurés : --cout texte=40."]
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser(description="Dimensionne une semaine LinkedIn en minutes (TIENT 0 / PLANCHER 2 / NE TIENT PAS 3).")
    p.add_argument("--minutes", type=int, help="minutes disponibles par semaine, mesurées sur une MAUVAISE semaine")
    p.add_argument("--etape", choices=list(ETAPES), default="depart")
    p.add_argument("--posts", type=int, help="nombre de posts texte voulus")
    p.add_argument("--formats", help="liste de formats, ex. texte,carrousel,texte")
    p.add_argument("--messages", type=int, default=0, help="messages de prospection à la main par semaine")
    p.add_argument("--cout", action="append", default=[], help="format=minutes mesurées (répétable)")
    p.add_argument("--exemple", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.exemple:
        a.minutes, a.etape, a.posts = 240, "depart", 2
    if a.minutes is None:
        p.print_help(sys.stderr)
        return 1
    try:
        cout = {}
        for c in a.cout:
            k, v = c.split("=")
            cout[k.strip()] = int(v)
        r = planifier(a.minutes, a.etape, a.posts, a.formats, a.messages, cout)
    except ValueError as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
