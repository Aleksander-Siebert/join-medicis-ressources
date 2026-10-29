#!/usr/bin/env python3
"""format.py : choisit le format LinkedIn que la matière permet vraiment.

On choisit souvent un format par mode (« les carrousels marchent en ce
moment ») plutôt que par ce qu'on a à dire. Ce script note 9 formats selon
trois entrées que l'utilisateur maîtrise : l'objectif, la matière disponible
et les minutes. Il rend une courte liste classée, avec la contrainte de chaque
format.

Deux refus nets :
  - un sondage sans vraie décision derrière (une astuce de portée sans suite) ;
  - une vidéo sans caméra ni images (du travail qui ne sera pas fait).

Codes de sortie :
  0  un format est recommandé
  2  les deux premiers sont à moins d'un point : demander, ne pas deviner
  3  aucun format ne tient avec la matière déclarée : aller chercher la matière
  1  erreur d'utilisation

Adapté de format_picker.py (alirezarezvani/claude-skills, MIT). Coûts en
minutes : ordres de grandeur de praticien. Sans dépendance.

Exemples :
  python3 format.py --objectif clients --matiere histoire,chiffres --minutes 60
  python3 format.py --objectif autorite --matiere tutoriel,visuel --minutes 120
  python3 format.py --objectif communaute --matiere question --decision "choisir le thème du webinaire de novembre"
"""

import argparse
import json
import sys

OBJECTIFS = ["portee", "autorite", "clients", "recrutement", "communaute", "emploi"]
MATIERES = ["histoire", "chiffres", "opinion", "tutoriel", "annonce", "transcription", "visuel", "question", "selection"]

FORMATS = {
    "texte": {"nom": "Post texte", "minutes": 25,
              "objectif": {"portee": 3, "autorite": 3, "clients": 2, "recrutement": 2, "communaute": 3, "emploi": 3},
              "matiere": {"histoire": 3, "chiffres": 2, "opinion": 3, "tutoriel": 2, "annonce": 2, "transcription": 1, "visuel": 0, "question": 3, "selection": 1},
              "contrainte": "Une idée. Si elle en demande deux, c'est deux posts."},
    "carrousel": {"nom": "Carrousel (document PDF)", "minutes": 90,
                  "objectif": {"portee": 3, "autorite": 3, "clients": 2, "recrutement": 1, "communaute": 2, "emploi": 2},
                  "matiere": {"histoire": 1, "chiffres": 3, "opinion": 1, "tutoriel": 3, "annonce": 0, "transcription": 1, "visuel": 3, "question": 0, "selection": 3},
                  "contrainte": "Chaque slide tient seule ; PDF avec texte sélectionnable. Test : la slide 1 + le texte du post suffisent-ils ? Si oui, c'est un post texte. → /linkedin-carrousel"},
    "video": {"nom": "Vidéo native", "minutes": 120,
              "objectif": {"portee": 3, "autorite": 2, "clients": 2, "recrutement": 3, "communaute": 2, "emploi": 2},
              "matiere": {"histoire": 3, "chiffres": 1, "opinion": 2, "tutoriel": 3, "annonce": 2, "transcription": 3, "visuel": 3, "question": 1, "selection": 0},
              "contrainte": "Sous-titres obligatoires (la plupart des vidéos sont vues sans le son, et c'est le plancher d'accessibilité). L'essentiel dans les 5 premières secondes."},
    "image": {"nom": "Image et texte", "minutes": 30,
              "objectif": {"portee": 2, "autorite": 2, "clients": 1, "recrutement": 2, "communaute": 2, "emploi": 2},
              "matiere": {"histoire": 2, "chiffres": 3, "opinion": 1, "tutoriel": 1, "annonce": 3, "transcription": 0, "visuel": 3, "question": 1, "selection": 1},
              "contrainte": "Texte alternatif obligatoire : LinkedIn le permet et ne l'écrit pas pour toi."},
    "sondage": {"nom": "Sondage", "minutes": 20,
                "objectif": {"portee": 2, "autorite": 1, "clients": 1, "recrutement": 1, "communaute": 3, "emploi": 1},
                "matiere": {"histoire": 0, "chiffres": 1, "opinion": 1, "tutoriel": 0, "annonce": 0, "transcription": 0, "visuel": 0, "question": 3, "selection": 0},
                "contrainte": "Seulement si tu publies ensuite ce que les réponses ont changé. Le post de suivi est le vrai contenu."},
    "article": {"nom": "Article", "minutes": 180,
                "objectif": {"portee": 1, "autorite": 3, "clients": 2, "recrutement": 1, "communaute": 1, "emploi": 2},
                "matiere": {"histoire": 2, "chiffres": 3, "opinion": 3, "tutoriel": 3, "annonce": 0, "transcription": 2, "visuel": 1, "question": 0, "selection": 3},
                "contrainte": "Touche bien moins de monde qu'un post [praticien]. Pour un texte de référence durable ; à découper ensuite en posts."},
    "newsletter": {"nom": "Numéro de newsletter", "minutes": 150,
                   "objectif": {"portee": 2, "autorite": 3, "clients": 3, "recrutement": 1, "communaute": 3, "emploi": 1},
                   "matiere": {"histoire": 2, "chiffres": 3, "opinion": 3, "tutoriel": 3, "annonce": 1, "transcription": 2, "visuel": 1, "question": 0, "selection": 3},
                   "contrainte": "Promesse de régularité sur 6 mois ; éligibilité au-delà de 150 abonnés ou relations (officiel). → /linkedin-strategie"},
    "commentaire": {"nom": "Commentaire de fond sous le post d'un autre", "minutes": 6,
                    "objectif": {"portee": 3, "autorite": 3, "clients": 2, "recrutement": 2, "communaute": 3, "emploi": 3},
                    "matiere": {"histoire": 2, "chiffres": 3, "opinion": 3, "tutoriel": 1, "annonce": 0, "transcription": 0, "visuel": 0, "question": 2, "selection": 1},
                    "contrainte": "Il doit apporter ce que le post n'a pas. Être d'accord n'est pas un commentaire. → /linkedin-comment"},
    "repartage": {"nom": "Repartage avec ton avis", "minutes": 15,
                  "objectif": {"portee": 1, "autorite": 2, "clients": 1, "recrutement": 1, "communaute": 2, "emploi": 1},
                  "matiere": {"histoire": 0, "chiffres": 2, "opinion": 3, "tutoriel": 0, "annonce": 1, "transcription": 0, "visuel": 1, "question": 1, "selection": 3},
                  "contrainte": "Ton avis doit dire plus que « à lire ». Un repartage nu dépense ta crédibilité sur l'idée d'un autre."},
}


def choisir(objectif, matieres, minutes, camera=False, decision=""):
    if objectif not in OBJECTIFS:
        raise ValueError(f"objectif inconnu : {objectif} (choisis parmi {', '.join(OBJECTIFS)})")
    inconnues = [m for m in matieres if m not in MATIERES]
    if inconnues:
        raise ValueError(f"matière inconnue : {', '.join(inconnues)} (choisis parmi {', '.join(MATIERES)})")
    classement, refus, alternatives = [], [], []
    for cle, f in FORMATS.items():
        if cle in ("commentaire", "repartage"):
            # Pas des posts : proposés à part, comme alternatives plus rapides.
            if max(f["matiere"][m] for m in matieres) >= 2:
                alternatives.append({"format": cle, "nom": f["nom"], "minutes": f["minutes"], "contrainte": f["contrainte"]})
            continue
        if cle == "sondage" and not decision.strip():
            refus.append({"format": f["nom"], "raison": "aucune décision déclarée derrière le sondage (--decision)"})
            continue
        if cle == "video" and not camera and "visuel" not in matieres and "transcription" not in matieres:
            refus.append({"format": f["nom"], "raison": "pas de caméra (--camera) ni d'images ou de vidéo existantes"})
            continue
        if f["minutes"] > minutes:
            refus.append({"format": f["nom"], "raison": f"demande ~{f['minutes']} min, {minutes} disponibles"})
            continue
        fit_matiere = max(f["matiere"][m] for m in matieres) if matieres else 0
        if fit_matiere == 0:
            continue
        note = f["objectif"][objectif] * 2 + fit_matiere * 3 + (1 if f["minutes"] <= minutes / 2 else 0)
        classement.append({"format": cle, "nom": f["nom"], "note": note, "minutes": f["minutes"], "contrainte": f["contrainte"]})
    classement.sort(key=lambda x: -x["note"])
    if not classement:
        verdict, code = "AUCUN", 3
    elif len(classement) > 1 and classement[0]["note"] - classement[1]["note"] <= 1:
        verdict, code = "À DÉPARTAGER", 2
    else:
        verdict, code = "RECOMMANDÉ", 0
    return {"verdict": verdict, "code": code, "objectif": objectif, "matieres": matieres, "minutes": minutes,
            "classement": classement[:4], "refus": refus, "alternatives": alternatives,
            "departage": "À égalité : celui que tu auras envie de refaire. Celui qu'on répète bat celui qui score plus une fois."}


def afficher(r):
    L = [f"FORMAT  {r['verdict']}  ·  objectif {r['objectif']} · matière {', '.join(r['matieres'])} · {r['minutes']} min", ""]
    if not r["classement"]:
        L.append("Aucun format ne tient avec cette matière. Va chercher la matière d'abord (/linkedin-interview).")
    for i, c in enumerate(r["classement"], 1):
        L.append(f"  {i}. {c['nom']} ({c['note']} pts, ~{c['minutes']} min)")
        L.append(f"     {c['contrainte']}")
    if r["code"] == 2:
        L += ["", r["departage"]]
    if r["alternatives"]:
        L += ["", "Plus rapide, sans publier :"] + [f"  · {x['nom']} (~{x['minutes']} min) : {x['contrainte']}" for x in r["alternatives"]]
    if r["refus"]:
        L += ["", "Écartés :"] + [f"  · {x['format']} : {x['raison']}" for x in r["refus"]]
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser(description="Choisit un format LinkedIn (RECOMMANDÉ 0 / À DÉPARTAGER 2 / AUCUN 3).")
    p.add_argument("--objectif", choices=OBJECTIFS)
    p.add_argument("--matiere", help="liste séparée par des virgules : " + ", ".join(MATIERES))
    p.add_argument("--minutes", type=int, default=60)
    p.add_argument("--camera", action="store_true", help="prêt à tourner une vidéo")
    p.add_argument("--decision", default="", help="la décision que le sondage va trancher")
    p.add_argument("--exemple", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.exemple:
        a.objectif, a.matiere, a.minutes = "clients", "histoire,chiffres", 60
    if not a.objectif or not a.matiere:
        p.print_help(sys.stderr)
        return 1
    try:
        r = choisir(a.objectif, [m.strip() for m in a.matiere.split(",") if m.strip()], a.minutes, a.camera, a.decision)
    except ValueError as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
