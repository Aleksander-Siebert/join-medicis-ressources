#!/usr/bin/env python3
"""audit_profil.py : note un profil LinkedIn sur 100 et classe les corrections.

Entrée : un JSON qui décrit le profil, rempli à partir de ce que l'utilisateur
a collé (jamais lu sur LinkedIn par un robot). Une clé absente ou à null =
section non montrée : elle n'est PAS notée, et la note est donnée sur les
points notés avec la fourchette possible. On ne note jamais ce qu'on n'a pas vu.

Sortie : tableau des 15 critères de grille.json, corrections classées par
POINTS GAGNÉS PAR HEURE, plan de la première heure, et ce qu'une réécriture ne
peut pas créer (recommandations, activité, photo, bannière).

Format d'entrée (toutes les clés sont facultatives) :
  {
    "objectif": "clients" | "emploi" | "autorite",
    "titre": "…",
    "infos": "…",
    "poste_actuel": {"intitule": "…", "lignes": ["…", "…"]},
    "experiences": [{"intitule": "…", "lignes": ["…"]}, …],
    "selection": {"elements": 2, "mise_a_jour_jours": 400},
    "banniere": "personnalisee" | "defaut",
    "photo": {"presente": true, "age_ans": 2},
    "competences": {"nombre": 12, "epinglees_alignees": false},
    "recommandations": {"recentes_2_ans": 1},
    "activite_jours": 40,
    "open_to": true,
    "url_personnalisee": false,
    "coordonnees": true,
    "formation": true
  }

Codes de sortie : 0 SOLIDE (80+) · 2 INCOMPLET (50-79) · 3 FAIBLE (<50) ·
1 erreur. Le verdict porte sur les points notés.

Inspiré de profile_completeness_auditor.py (alirezarezvani/claude-skills, MIT).
Sans dépendance, sans réseau.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import infos as mod_infos  # noqa: E402
import titre as mod_titre  # noqa: E402

GRILLE = ICI.parent / "grille.json"

VERBES_FAIBLES = re.compile(
    r"^\s*(responsable de|en charge d|charge d|participation|participe|contribue|contribution|"
    r"accompagne|aide|assiste|travaille|gestion d|suivi d|soutien|support)", re.I)
CHIFFRE = re.compile(r"\d")

EXEMPLE = {
    "objectif": "clients",
    "titre": "Responsable marketing chez Assurly",
    "infos": "Passionnée par le marketing digital depuis plus de 10 ans, j'aime relever de nouveaux défis.",
    "poste_actuel": {"intitule": "Responsable acquisition",
                     "lignes": ["En charge de l'acquisition payante et du SEO",
                                "Relancé 1 400 clients dormants en 6 semaines : 212 contrats réactivés"]},
    "experiences": [{"intitule": "Chargée de marketing", "lignes": ["Gestion des campagnes emailing"]}],
    "selection": {"elements": 0},
    "banniere": "defaut",
    "photo": {"presente": True, "age_ans": 4},
    "competences": {"nombre": 18, "epinglees_alignees": False},
    "recommandations": None,
    "activite_jours": 45,
    "open_to": False,
    "url_personnalisee": False,
    "coordonnees": True,
    "formation": True,
}

POURQUOI = {
    "titre": "Il accompagne chaque commentaire, résultat de recherche et invitation. Un intitulé seul ne dit rien qu'on ne devine.",
    "infos_ouverture": "Ce qui est avant « voir plus » est toute la section pour la plupart des lecteurs.",
    "infos_corps": "Le lecteur intéressé cherche une preuve et une prochaine étape.",
    "poste_actuel": "Une liste de missions est la même pour tous ceux qui ont eu ce poste. Les résultats sont à toi seul.",
    "experiences": "Le lecteur qui décide lit tout. Des expériences sans chiffres le laissent deviner.",
    "selection": "Le seul endroit où tu choisis ce qu'un visiteur voit en premier. Vide, il voit ton dernier repartage.",
    "banniere": "1 584 × 396 px laissés au dégradé par défaut : la place la moins chère pour dire ce que tu fais.",
    "photo": "Le premier jugement se fait avant la lecture d'un seul mot.",
    "competences": "La recherche et les filtres des recruteurs s'appuient dessus.",
    "recommandations": "Le seul texte du profil que tu n'as pas écrit toi-même.",
    "activite": "Un profil sans activité récente ne transforme pas une visite en conversation.",
    "open_to": "Dit aux visiteurs et à la recherche ce que tu proposes ou cherches.",
    "url": "Deux minutes, et l'adresse se dit à voix haute.",
    "coordonnees": "Un profil qui convertit a besoin d'un moyen de démarrer la conversation.",
    "formation": "Signal faible seul, mais filtre fréquent chez les recruteurs.",
}


def lignes_chiffrees(lignes: list) -> tuple:
    bonnes = [l for l in lignes if CHIFFRE.search(l) and not VERBES_FAIBLES.search(l)]
    return len(bonnes), len(lignes)


def evaluer(cle: str, p: dict):
    """Renvoie (fraction 0..1, détail) ou None si la section n'a pas été montrée."""
    obj = p.get("objectif") or "clients"
    if cle == "titre":
        t = p.get("titre")
        if t is None:
            return None
        if not t.strip():
            return 0.0, "vide"
        r = mod_titre.noter(t)
        return r["note"] / 100, f"{r['note']}/100 ({r['verdict']}), lance titre.py pour le détail"
    if cle in ("infos_ouverture", "infos_corps"):
        t = p.get("infos")
        if t is None:
            return None
        if not t.strip():
            return 0.0, "vide"
        r = mod_infos.controler(t, obj)
        ids = {c["controle"] for c in r["constats"]}
        if cle == "infos_ouverture":
            # une ouverture usée (« Bienvenue sur mon profil ») gâche les caractères les plus lus
            perdus = {"pli": 0.5, "contenu du pli": 0.5, "ouverture": 0.6}
            frac = max(0.0, 1 - sum(v for k, v in perdus.items() if k in ids))
            detail = "pli correct" if frac == 1 else "à revoir : " + ", ".join(k for k in perdus if k in ids)
            return frac, detail
        perdus = {"appel à l'action": 0.4, "preuve": 0.3, "voix": 0.2, "longueur": 0.2,
                  "mots creux": 0.1, "mise en page": 0.1}
        frac = max(0.0, 1 - sum(v for k, v in perdus.items() if k in ids))
        detail = f"{r['caracteres']} caractères" + ("" if frac == 1 else " ; à revoir : " + ", ".join(k for k in perdus if k in ids))
        return frac, detail
    if cle == "poste_actuel":
        pa = p.get("poste_actuel")
        if pa is None:
            return None
        if not pa.get("intitule"):
            return 0.0, "aucun poste actuel"
        bon, total = lignes_chiffrees(pa.get("lignes") or [])
        if total == 0:
            return 0.2, "intitulé sans description"
        frac = 0.3 + 0.7 * min(1.0, bon / 2) * (bon / total)
        return min(1.0, frac), f"{bon}/{total} lignes chiffrées (2 au moins attendues)"
    if cle == "experiences":
        ex = p.get("experiences")
        if ex is None:
            return None
        if not ex:
            return 1.0, "aucun poste précédent : sans objet"
        notes = []
        for e in ex[:2]:
            bon, total = lignes_chiffrees(e.get("lignes") or [])
            notes.append(min(1.0, bon / 2))
        return sum(notes) / len(notes), f"{len(ex[:2])} poste(s) lus, moyenne {round(100 * sum(notes) / len(notes))}% des lignes chiffrées attendues"
    if cle == "selection":
        s = p.get("selection")
        if s is None:
            return None
        n = s.get("elements") or 0
        if n == 0:
            return 0.0, "vide"
        age = s.get("mise_a_jour_jours")
        frac = 1.0 if n >= 3 else 0.6
        if age is not None and age > 365:
            frac -= 0.4
            return max(0.0, frac), f"{n} élément(s), mis à jour il y a {age} jours"
        return frac, f"{n} élément(s)"
    if cle == "banniere":
        b = p.get("banniere")
        if b is None:
            return None
        return (1.0, "personnalisée") if b == "personnalisee" else (0.0, "dégradé par défaut")
    if cle == "photo":
        ph = p.get("photo")
        if ph is None:
            return None
        if not ph.get("presente"):
            return 0.0, "absente"
        age = ph.get("age_ans")
        if age is not None and age > 3:
            return 0.6, f"présente, {age} ans"
        return 1.0, "présente"
    if cle == "competences":
        c = p.get("competences")
        if c is None:
            return None
        n = c.get("nombre") or 0
        frac = min(1.0, n / 5) * (1.0 if c.get("epinglees_alignees") else 0.6)
        return frac, f"{n} listées, 3 premières {'alignées' if c.get('epinglees_alignees') else 'non alignées'} sur l'objectif"
    if cle == "recommandations":
        r = p.get("recommandations")
        if r is None:
            return None
        n = r.get("recentes_2_ans") or 0
        return min(1.0, n / 3), f"{n} reçue(s) ces 2 dernières années"
    if cle == "activite":
        d = p.get("activite_jours")
        if d is None:
            return None
        if d <= 7:
            return 1.0, f"dernière activité il y a {d} jours"
        if d <= 30:
            return 0.6, f"il y a {d} jours"
        if d <= 90:
            return 0.3, f"il y a {d} jours : profil qui paraît en sommeil"
        return 0.0, f"il y a {d} jours : inactif"
    if cle == "open_to":
        if obj == "autorite":
            return 1.0, "sans objet pour un objectif d'autorité"
        v = p.get("open_to")
        if v is None:
            return None
        label = "« Services »" if obj == "clients" else "« Open to work »"
        return (1.0, f"{label} activé") if v else (0.0, f"{label} non activé")
    if cle in ("url", "coordonnees", "formation"):
        k = {"url": "url_personnalisee", "coordonnees": "coordonnees", "formation": "formation"}[cle]
        v = p.get(k)
        if v is None:
            return None
        return (1.0, "oui") if v else (0.0, "non")
    return None


def auditer(profil: dict) -> dict:
    grille = json.loads(GRILLE.read_text(encoding="utf-8"))
    lignes, corrections = [], []
    gagnes = notes = 0.0
    for c in grille["criteres"]:
        res = evaluer(c["id"], profil)
        if res is None:
            lignes.append({"id": c["id"], "nom": c["nom"], "points": c["points"], "obtenus": None,
                           "detail": "non montré : non noté"})
            continue
        frac, detail = res
        obtenus = round(c["points"] * frac, 1)
        gagnes += obtenus
        notes += c["points"]
        lignes.append({"id": c["id"], "nom": c["nom"], "points": c["points"], "obtenus": obtenus, "detail": detail})
        perdus = round(c["points"] - obtenus, 1)
        if perdus >= 0.5:
            corrections.append({
                "id": c["id"], "nom": c["nom"], "points_a_gagner": perdus,
                "effort_heures": c["effort_heures"],
                "points_par_heure": round(perdus / c["effort_heures"], 1),
                "reecriture": c["reecriture"], "actuel": detail, "pourquoi": POURQUOI[c["id"]],
                "objectif": c["note_maximale"],
            })
    corrections.sort(key=lambda f: (-f["points_par_heure"], -f["points_a_gagner"]))
    plan, budget = [], 1.0
    for f in corrections:
        if f["effort_heures"] <= budget + 1e-9:
            plan.append(f["nom"])
            budget -= f["effort_heures"]
    non_notes = [l["nom"] for l in lignes if l["obtenus"] is None]
    manquants = sum(l["points"] for l in lignes if l["obtenus"] is None)
    note = round(gagnes)
    ratio = (gagnes / notes) if notes else 0
    verdict, code = (("SOLIDE", 0) if ratio >= 0.8 else ("INCOMPLET", 2) if ratio >= 0.5 else ("FAIBLE", 3))
    return {
        "objectif": profil.get("objectif") or "clients",
        "note": note,
        "sur": int(notes),
        "fourchette_sur_100": [note, note + manquants] if non_notes else [note, note],
        "verdict": verdict,
        "code": code,
        "criteres": lignes,
        "non_notes": non_notes,
        "corrections": corrections,
        "plan_premiere_heure": plan,
        "points_premiere_heure": round(sum(f["points_a_gagner"] for f in corrections if f["nom"] in plan), 1),
        "hors_reecriture": [f["nom"] for f in corrections if not f["reecriture"]],
    }


def afficher(r: dict) -> str:
    L = [f"PROFIL  {r['note']}/{r['sur']} points notés  ·  {r['verdict']}  ·  objectif : {r['objectif']}"]
    if r["non_notes"]:
        L.append(f"Fourchette sur 100 : entre {r['fourchette_sur_100'][0]} et {r['fourchette_sur_100'][1]} "
                 f"(non montré : {', '.join(r['non_notes'])})")
    L.append("")
    for l in r["criteres"]:
        ob = "  ?" if l["obtenus"] is None else f"{l['obtenus']:>4g}"
        L.append(f"  {l['nom']:<36} {ob}/{l['points']:<3} {l['detail']}")
    if r["corrections"]:
        L += ["", "Corrections classées par points gagnés par heure :"]
        for f in r["corrections"]:
            marque = "" if f["reecriture"] else "  (hors réécriture)"
            L.append(f"  +{f['points_a_gagner']:<4g} pts  ~{f['effort_heures']:g} h  ({f['points_par_heure']:g} pts/h)  {f['nom']}{marque}")
            L.append(f"        actuel : {f['actuel']}")
    if r["plan_premiere_heure"]:
        L += ["", f"Première heure : {', '.join(r['plan_premiere_heure'])} (+{r['points_premiere_heure']:g} points)"]
    if r["hors_reecriture"]:
        L.append(f"Une réécriture ne crée pas : {', '.join(r['hors_reecriture'])}.")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser(description="Note un profil LinkedIn sur 100 (SOLIDE 0 / INCOMPLET 2 / FAIBLE 3).")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--fichier", help="JSON du profil")
    src.add_argument("--exemple", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    try:
        if a.exemple:
            profil = EXEMPLE
        elif a.fichier:
            profil = json.loads(Path(a.fichier).read_text(encoding="utf-8"))
        elif not sys.stdin.isatty():
            profil = json.loads(sys.stdin.read())
        else:
            p.print_help(sys.stderr)
            return 1
    except (OSError, json.JSONDecodeError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    r = auditer(profil)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
