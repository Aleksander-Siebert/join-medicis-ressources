#!/usr/bin/env python3
"""volume.py : dimensionne une semaine de prospection pour qu'elle reste manuelle.

  python3 volume.py --invitations 30 --en-attente 45 --messages 10 --minutes 180 \
      [--jours 5] [--acceptation 0.31 | --journal journal.md] [--notes 8] [--premium]

Contrôles (seuils de prudence de praticien, LinkedIn ne publie pas les siens) :
  - plus de 40 invitations par jour : REFUSÉ, c'est un plan d'automatisation ;
  - plus de 25 par jour : attention, ce n'est plus écrit à la main ;
  - invitations prévues + en attente au-delà d'environ 100 par semaine (limite
    observée, invitations en attente comprises) : BLOQUANT ; au-delà de 80 :
    attention ;
  - taux d'acceptation sous 20% : STOP, revoir le ciblage avant d'envoyer plus ;
  - temps nécessaire (5 min par invitation, 8 par message) au-delà du budget ;
  - plus de 3 notes personnalisées par mois en compte gratuit (aide LinkedIn
    a563153) : garder les notes pour les invitations qui comptent.

Le taux d'acceptation se lit dans la section « Invitations envoyées » de
journal.md (4 dernières semaines) si --journal est donné.

Codes de sortie : 0 OK, 2 attention, 3 bloquant ou refusé, 1 erreur.

D'après outreach_volume_guard.py (alirezarezvani, claude-skills, MIT), réécrit
en français. Rien n'est envoyé. Sans dépendance.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

LIMITE_HEBDO = 100
PLAFOND_JOUR = 25
REFUS_JOUR = 40
ACCEPTATION_MIN = 0.20
MIN_INVITATION = 5
MIN_MESSAGE = 8
NOTES_GRATUIT_MOIS = 3


def acceptation_journal(chemin):
    """Taux d'acceptation des 4 dernières lignes du tableau « Invitations envoyées »."""
    texte = Path(chemin).read_text(encoding="utf-8")
    m = re.search(r"## Invitations envoyées[^\n]*\n(?:[^|\n][^\n]*\n|\n)*((?:\|.*\n?)+)", texte)
    if not m:
        return None, 0
    lignes = []
    for l in m.group(1).splitlines()[2:]:
        cel = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cel) >= 3 and cel[1].isdigit() and cel[2].isdigit():
            lignes.append((int(cel[1]), int(cel[2])))
    lignes = lignes[-4:]
    envoyees = sum(e for e, _ in lignes)
    if not envoyees:
        return None, 0
    return sum(a for _, a in lignes) / envoyees, envoyees


def controler(invitations, en_attente, messages, minutes, jours=5, acceptation=None, envoyees_base=0,
              notes=0, premium=False):
    bloquants, attentions = [], []
    refuse = False
    par_jour = invitations / max(1, jours)
    if par_jour > REFUS_JOUR:
        refuse = True
        bloquants.append(f"{invitations} invitations en {jours} jours, soit {par_jour:.0f} par jour : personne ne lit autant de profils "
                         "ni n'écrit autant de lignes propres. C'est un plan d'automatisation (interdit, aide LinkedIn a1341387). "
                         "Si c'est le nombre qui compte, la publicité est le bon outil.")
    elif par_jour > PLAFOND_JOUR:
        attentions.append(f"{par_jour:.0f} invitations par jour : au-delà de {PLAFOND_JOUR}, ce n'est plus écrit à la main. Étale sur plus de jours.")
    total = invitations + en_attente
    if total > LIMITE_HEBDO:
        bloquants.append(f"{invitations} prévues + {en_attente} en attente = {total} : au-delà de la limite observée d'environ {LIMITE_HEBDO} "
                         f"par semaine, invitations en attente comprises. Envoie au plus {max(0, LIMITE_HEBDO - en_attente)} cette semaine, "
                         "et retire les invitations en attente depuis plus de 3 semaines (une invitation retirée ne se renvoie pas "
                         "à la même personne avant environ 3 semaines [à vérifier]).")
    elif total > LIMITE_HEBDO * 0.8:
        attentions.append(f"{total} sur environ {LIMITE_HEBDO} : proche de la limite hebdomadaire observée, invitations en attente comprises.")
    if acceptation is not None:
        if acceptation < ACCEPTATION_MIN:
            bloquants.append(f"Taux d'acceptation de {acceptation:.0%}".replace(" %", "%") +
                             (f" sur {envoyees_base} invitations" if envoyees_base else "") +
                             f" : sous {ACCEPTATION_MIN:.0%}, arrête d'envoyer et revois le ciblage (qui, pourquoi maintenant, la ligne propre). "
                             "Un taux bas à volume élevé est le motif que LinkedIn examine.")
        elif acceptation < 0.30:
            attentions.append(f"Taux d'acceptation de {acceptation:.0%} : correct, à surveiller avant d'augmenter le volume.")
    else:
        attentions.append("Taux d'acceptation inconnu : note chaque semaine envoyées, acceptées, en attente dans journal.md.")
    besoin = invitations * MIN_INVITATION + messages * MIN_MESSAGE
    if besoin > minutes:
        possible = max(0, (minutes - messages * MIN_MESSAGE) // MIN_INVITATION)
        bloquants.append(f"Il faut environ {besoin} minutes ({invitations} × {MIN_INVITATION} + {messages} × {MIN_MESSAGE}) pour {minutes} disponibles : "
                         f"vise {possible} invitations, ou moins de messages. Une invitation bâclée coûte plus qu'une invitation pas envoyée.")
    if notes and not premium and notes > NOTES_GRATUIT_MOIS:
        attentions.append(f"{notes} notes personnalisées prévues : un compte gratuit en a {NOTES_GRATUIT_MOIS} par mois (aide LinkedIn a563153). "
                          "Garde-les pour les invitations qui comptent ; les autres partent sans note, et le premier message après "
                          "acceptation porte la ligne propre à la personne.")
    possibles = [LIMITE_HEBDO - en_attente, PLAFOND_JOUR * jours, max(0, (minutes - messages * MIN_MESSAGE) // MIN_INVITATION)]
    conseil = max(0, min(possibles))
    if acceptation is not None and acceptation < ACCEPTATION_MIN:
        conseil = 0
    if refuse:
        verdict, code = "REFUSÉ", 3
    else:
        verdict, code = ("BLOQUÉ", 3) if bloquants else ("À SURVEILLER", 2) if attentions else ("OK", 0)
    return {"verdict": verdict, "code": code, "par_jour": round(par_jour, 1), "pipeline": total,
            "minutes_necessaires": besoin, "invitations_conseillees": conseil,
            "acceptation": None if acceptation is None else round(acceptation, 3),
            "bloquants": bloquants, "attentions": attentions}


def main():
    a = argparse.ArgumentParser(description="Dimensionne une semaine de prospection manuelle.")
    a.add_argument("--invitations", type=int, required=True, help="invitations prévues cette semaine")
    a.add_argument("--en-attente", type=int, default=0)
    a.add_argument("--messages", type=int, default=0, help="messages prévus (premiers messages et relances)")
    a.add_argument("--minutes", type=int, required=True, help="minutes disponibles cette semaine")
    a.add_argument("--jours", type=int, default=5)
    a.add_argument("--acceptation", type=float, help="taux d'acceptation récent, entre 0 et 1")
    a.add_argument("--journal", help="journal.md, pour lire le taux d'acceptation")
    a.add_argument("--notes", type=int, default=0, help="notes personnalisées prévues ce mois")
    a.add_argument("--premium", action="store_true")
    a.add_argument("--json", action="store_true")
    x = a.parse_args()
    acc, base = x.acceptation, 0
    try:
        if acc is None and x.journal:
            acc, base = acceptation_journal(x.journal)
    except OSError as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    if acc is not None and not 0 <= acc <= 1:
        print("Erreur : --acceptation entre 0 et 1 (0.25 pour 25%).", file=sys.stderr)
        return 1
    r = controler(x.invitations, x.en_attente, x.messages, x.minutes, x.jours, acc, base, x.notes, x.premium)
    if x.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"VOLUME  {r['verdict']}  ·  {r['par_jour']} invitations par jour · {r['pipeline']} dans la semaine (en attente comprises) · "
              f"{r['minutes_necessaires']} min nécessaires")
        if r["acceptation"] is not None:
            print(f"  Taux d'acceptation récent : {round(r['acceptation'] * 100)}%" + (f" (sur {base} invitations, journal.md)" if base else ""))
        print(f"  Invitations conseillées cette semaine : {r['invitations_conseillees']}")
        for b in r["bloquants"]:
            print(f"  ✖ {b}")
        for t in r["attentions"]:
            print(f"  ! {t}")
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
