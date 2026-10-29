#!/usr/bin/env python3
"""audit_page.py : note une page entreprise LinkedIn sur 100 (12 critères).

Chaque critère de grille-page.json dit sa source (page, statistiques,
humaniseur, contexte). Si la source n'a pas été fournie, ou si la donnée
manque, le critère est « n/a » : il n'est pas compté, et la note est donnée
sur les POINTS NOTABLES (ex. « 41/66 notables »). On ne note jamais ce qu'on
n'a pas vu.

Entrée JSON (toutes les clés facultatives) :
  {
    "sources": ["page", "statistiques", "contexte", "humaniseur"],
    "date": "2026-10-02",
    "nom": "Assurly", "nom_avec_categorie": false,
    "slogan": "…", "presentation": "…",
    "informations": {"site": true, "secteur": true, "taille": true, "siege": true,
                     "creation": true, "specialites_actuelles": false},
    "logo_net": true, "couverture": "personnalisee" | "defaut" | "banque",
    "bouton": {"present": true, "page_utile": true, "utm": false},
    "epingle": {"present": true, "age_jours": 40, "promeut_retire": false},
    "vitrines_a_jour": true,
    "posts": [{"date": "2026-09-30", "engagement": 0.031, "original": true,
               "hashtags": 2, "humaniseur": "OK"}, …],
    "engagement_historique_median": 0.025,
    "reponses_sous_2h": true,
    "equipe": {"salaries": 40, "relies_a_la_page": 31, "titres_alignes": 12},
    "formulations_retirees_trouvees": 0
  }

Codes de sortie : 0 SOLIDE (80% des points notables et plus) · 2 À
RENFORCER (50 à 79%) · 3 FAIBLE (moins de 50%) · 1 erreur.

Généralisé de page_rubric.json (JoshuaDIWork/Linkedin_SKILL, MIT). Sans
dépendance, sans réseau : rien n'est lu sur LinkedIn.
"""

import argparse
import datetime as dt
import json
import re
import statistics
import sys
import unicodedata
from pathlib import Path

GRILLE = Path(__file__).resolve().parent.parent / "grille-page.json"
AUDIENCE = re.compile(r"\b(pour les|pour des|pour vos|aux|j'aide|nous aidons|aide les|aidons les|pme|eti|"
                      r"locataires|proprietaires|independants|entreprises|particuliers|familles|equipes|b2b|saas)\b")
CTA = re.compile(r"\b(contact|contactez|ecrivez|ecris|devis|rendez-vous|essai|demo|demonstration|"
                 r"souscri\w*|decouvr\w*|site|www\.|https?://|@)\b")

EXEMPLE = {
    "sources": ["page", "statistiques", "contexte"],
    "date": "2026-10-02",
    "nom": "Assurly", "nom_avec_categorie": False,
    "slogan": "L'assurance habitation en ligne pour les locataires",
    "presentation": ("Assurly est une société fondée en 2019 qui propose des solutions d'assurance innovantes et "
                     "adaptées à vos besoins grâce à une approche centrée sur le client et une équipe passionnée."),
    "informations": {"site": True, "secteur": True, "taille": True, "siege": True, "creation": True,
                     "specialites_actuelles": False},
    "logo_net": True, "couverture": "banque",
    "bouton": {"present": True, "page_utile": False, "utm": False},
    "epingle": {"present": True, "age_jours": 210, "promeut_retire": True},
    "vitrines_a_jour": None,
    "posts": [{"date": "2026-09-29", "engagement": 0.012, "original": False, "hashtags": 6},
              {"date": "2026-09-15", "engagement": 0.018, "original": True, "hashtags": 5},
              {"date": "2026-09-02", "engagement": 0.009, "original": False, "hashtags": 4}],
    "engagement_historique_median": 0.016,
    "reponses_sous_2h": False,
    "equipe": {"salaries": 120, "relies_a_la_page": 74, "titres_alignes": 5},
    "formulations_retirees_trouvees": 1,
}


def pct(x):
    return f"{x:.1%}".replace(".", ",")


def norme(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'")



def evaluer(cid, p):
    """(fraction, détail) ou None (n/a)."""
    if cid == "nom_slogan":
        s = p.get("slogan")
        if s is None and p.get("nom") is None:
            return None
        frac, notes = 1.0, []
        if p.get("nom_avec_categorie"):
            frac -= 0.2
            notes.append("nom suivi d'une catégorie")
        if not s:
            return max(0, frac - 0.8), "slogan vide"
        if len(s) > 120:
            frac -= 0.3
            notes.append(f"slogan de {len(s)} caractères (120 au plus)")
        if not AUDIENCE.search(norme(s)):
            frac -= 0.3
            notes.append("slogan sans audience nommée")
        if not re.search(r"\d", s):
            frac -= 0.2
            notes.append("slogan sans preuve chiffrée")
        return max(0.0, frac), ", ".join(notes) or f"{len(s)} caractères, audience et preuve"
    if cid in ("presentation_debut", "presentation_corps"):
        t = p.get("presentation")
        if t is None:
            return None
        if not t.strip():
            return 0.0, "vide"
        tn = norme(t)
        if cid == "presentation_debut":
            debut = tn[:200]
            frac, notes = 1.0, []
            nom = norme(p.get("nom") or "")
            if re.match(rf"\s*({re.escape(nom)} est|fondee? en|depuis \d|creee? en|nous sommes)", tn) if nom else re.match(r"\s*(fondee? en|depuis \d|nous sommes)", tn):
                frac -= 0.5
                notes.append("ouvre sur l'entreprise, pas sur le lecteur")
            if not re.search(r"[.!?](\s|$)", t[:200]):
                frac -= 0.3
                notes.append("aucune phrase finie avant ~200 caractères")
            if not (AUDIENCE.search(debut) or re.search(r"\d", debut)):
                frac -= 0.2
                notes.append("ni audience ni chiffre avant le pli")
            return max(0.0, frac), ", ".join(notes) or "ouvre sur le lecteur"
        frac, notes = 1.0, []
        if len(t) > 2000:
            frac -= 0.4
            notes.append(f"{len(t)} caractères (2 000 au plus)")
        if not re.search(r"\d", t):
            frac -= 0.3
            notes.append("aucun chiffre")
        if not CTA.search(tn):
            frac -= 0.3
            notes.append("pas de porte d'entrée")
        creux = [m for m in ("innovant", "passionne", "sur mesure", "centree sur le client", "adaptees a vos besoins",
                             "leader", "solutions") if m in tn]
        if creux:
            frac -= 0.2
            notes.append("mots creux : " + ", ".join(creux))
        return max(0.0, frac), ", ".join(notes) or f"{len(t)} caractères"
    if cid == "informations":
        i = p.get("informations")
        if not i:
            return None
        ok = sum(1 for v in i.values() if v)
        manquants = [k for k, v in i.items() if not v]
        return ok / len(i), ("complet" if not manquants else "à revoir : " + ", ".join(manquants))
    if cid == "logo_couverture":
        if p.get("couverture") is None and p.get("logo_net") is None:
            return None
        frac = (0.4 if p.get("logo_net") else 0.0) + (0.6 if p.get("couverture") == "personnalisee" else 0.0)
        return frac, f"logo {'net' if p.get('logo_net') else 'à refaire'}, couverture {p.get('couverture') or '?'}"
    if cid == "bouton":
        b = p.get("bouton")
        if b is None:
            return None
        if not b.get("present"):
            return 0.0, "aucun bouton"
        frac = 0.4 + (0.4 if b.get("page_utile") else 0) + (0.2 if b.get("utm") else 0)
        manque = [x for x, k in (("page utile", "page_utile"), ("UTM", "utm")) if not b.get(k)]
        return frac, "présent" + (" ; manque : " + ", ".join(manque) if manque else "")
    if cid == "epingle_vitrines":
        e = p.get("epingle")
        if e is None:
            return None
        if not e.get("present"):
            frac, d = 0.3, "aucun post épinglé"
        else:
            frac, d = 1.0, f"épinglé il y a {e.get('age_jours', '?')} jours"
            if (e.get("age_jours") or 0) > 90:
                frac -= 0.4
            if e.get("promeut_retire"):
                frac -= 0.6
                d += ", promeut une offre ou formulation retirée"
        if p.get("vitrines_a_jour") is False:
            frac -= 0.3
            d += ", pages vitrines à jour : non"
        return max(0.0, frac), d
    if cid in ("rythme", "qualite_posts", "engagement"):
        posts = p.get("posts")
        if not posts:
            return None
        if cid == "rythme":
            ref = dt.date.fromisoformat(p.get("date") or dt.date.today().isoformat())
            dates = sorted((dt.date.fromisoformat(x["date"]) for x in posts if x.get("date")), reverse=True)
            if not dates:
                return None
            recents = [d for d in dates if (ref - d).days <= 28]
            dernier = (ref - dates[0]).days
            frac = min(1.0, len(recents) / 4) * (1.0 if dernier <= 7 else 0.6)
            return frac, f"{len(recents)} post(s) sur 4 semaines, dernier il y a {dernier} jours"
        if cid == "qualite_posts":
            n = len(posts[:10])
            originaux = sum(1 for x in posts[:10] if x.get("original"))
            hashtags_ok = sum(1 for x in posts[:10] if (x.get("hashtags") or 0) <= 3)
            hum = [x.get("humaniseur") for x in posts[:10] if x.get("humaniseur")]
            frac = 0.4 * (originaux / n) + 0.3 * (hashtags_ok / n) + (0.3 * sum(1 for h in hum if h == "OK") / len(hum) if hum else 0.15)
            return frac, f"{originaux}/{n} originaux, {hashtags_ok}/{n} avec 0 à 3 hashtags" + ("" if hum else ", humaniseur non lancé")
        taux = [x["engagement"] for x in posts[:10] if x.get("engagement") is not None]
        if not taux:
            return None
        med = statistics.median(taux)
        hist = p.get("engagement_historique_median")
        frac = 0.6 if hist is None else (0.6 if med >= hist else 0.6 * med / hist)
        frac += 0.4 if p.get("reponses_sous_2h") else 0
        comp = f" (historique {pct(hist)})" if hist else " (pas d'historique : comparer au prochain audit)"
        return min(1.0, frac), f"médiane {pct(med)} sur {len(taux)} posts{comp}, réponses sous 2 h : {'oui' if p.get('reponses_sous_2h') else 'non'}"
    if cid == "alignement_equipe":
        e = p.get("equipe")
        if not e or not e.get("salaries"):
            return None
        r1 = e.get("relies_a_la_page", 0) / e["salaries"]
        r2 = e.get("titres_alignes", 0) / e["salaries"]
        return min(1.0, 0.6 * r1 + 0.4 * min(1.0, r2 * 2)), f"{r1:.0%} reliés à la page, {r2:.0%} avec les formulations maison"
    if cid == "coherence":
        n = p.get("formulations_retirees_trouvees")
        if n is None:
            return None
        return (1.0, "aucune formulation retirée") if n == 0 else (max(0.0, 1 - 0.5 * n), f"{n} formulation(s) retirée(s) encore visible(s)")
    return None


def auditer(p):
    g = json.loads(GRILLE.read_text(encoding="utf-8"))
    lignes, corrections = [], []
    obtenu = notables = 0.0
    for c in g["criteres"]:
        res = evaluer(c["id"], p) if all(s in (p.get("sources") or []) for s in c["source"] if s not in ("humaniseur",)) else None
        if res is None:
            lignes.append({"id": c["id"], "nom": c["nom"], "points": c["points"], "obtenus": None,
                           "detail": "n/a : source « " + "/".join(c["source"]) + " » non fournie ou donnée manquante"})
            continue
        frac, detail = res
        pts = round(c["points"] * frac, 1)
        obtenu += pts
        notables += c["points"]
        lignes.append({"id": c["id"], "nom": c["nom"], "points": c["points"], "obtenus": pts, "detail": detail})
        perdus = round(c["points"] - pts, 1)
        if perdus >= 0.5:
            corrections.append({"nom": c["nom"], "points_a_gagner": perdus, "effort_heures": c["effort_heures"],
                                "points_par_heure": round(perdus / c["effort_heures"], 1), "objectif": c["note_maximale"],
                                "actuel": detail})
    corrections.sort(key=lambda x: (-x["points_par_heure"], -x["points_a_gagner"]))
    ratio = obtenu / notables if notables else 0
    verdict, code = ("SOLIDE", 0) if ratio >= 0.8 else ("À RENFORCER", 2) if ratio >= 0.5 else ("FAIBLE", 3)
    return {"note": round(obtenu), "notables": int(notables), "pourcentage": round(100 * ratio),
            "verdict": verdict, "code": code, "criteres": lignes, "corrections": corrections,
            "n_a": [l["nom"] for l in lignes if l["obtenus"] is None]}


def afficher(r):
    L = [f"PAGE ENTREPRISE  {r['note']}/{r['notables']} points notables ({r['pourcentage']}%)  ·  {r['verdict']}", ""]
    for l in r["criteres"]:
        ob = " n/a" if l["obtenus"] is None else f"{l['obtenus']:>4g}"
        L.append(f"  {l['nom']:<38} {ob}/{l['points']:<3} {l['detail']}")
    if r["corrections"]:
        L += ["", "Corrections, par points gagnés par heure :"]
        for c in r["corrections"]:
            L.append(f"  +{c['points_a_gagner']:<4g} pts  ~{c['effort_heures']:g} h  {c['nom']} : {c['actuel']}")
    if r["n_a"]:
        L += ["", "Non noté (fournir la source pour un audit complet) : " + ", ".join(r["n_a"])]
    return "\n".join(L)


def main():
    a = argparse.ArgumentParser(description="Note une page entreprise LinkedIn (SOLIDE 0 / À RENFORCER 2 / FAIBLE 3).")
    s = a.add_mutually_exclusive_group()
    s.add_argument("--fichier")
    s.add_argument("--exemple", action="store_true")
    a.add_argument("--json", action="store_true")
    x = a.parse_args()
    try:
        if x.exemple:
            p = EXEMPLE
        elif x.fichier:
            p = json.loads(Path(x.fichier).read_text(encoding="utf-8"))
        else:
            a.print_help(sys.stderr)
            return 1
        r = auditer(p)
    except (OSError, ValueError, json.JSONDecodeError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    print(json.dumps(r, ensure_ascii=False, indent=2) if x.json else afficher(r))
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
