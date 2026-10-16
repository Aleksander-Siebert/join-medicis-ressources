#!/usr/bin/env python3
"""Pipeline d'un article SEO : étapes nommées, validées une à une, rejouables.

Deux rôles, sans dépendance :

1. L'état du pipeline (fichier etat-article.json dans le dossier de l'article) :
   chaque étape est « à faire », « à valider », « validé », « passée »,
   « à refaire » (avec le retour de l'utilisateur) ou « à revoir » (une étape
   d'avant a changé). Refaire une étape renvoie les suivantes en revue, jamais
   celles d'avant. Une étape ne se termine pas tant que les précédentes ne
   sont pas validées (pas de rédaction sans plan validé).

2. Le portail qualité (`controler`) : lance les contrôles des Skills voisins
   (controle.py de /seo-write, affirmations.py, detect.py de /seo-human) et
   rend un verdict par portes, pas par moyenne : une affirmation sans source
   en YMYL bloque, quelle que soit la qualité du reste. Après N tours sans
   passer, le verdict devient RELECTURE HUMAINE au lieu de boucler.

Usage :
  pipeline.py init "mutuelle indépendant" --dossier art/ [--ymyl] [--autonome] [--max-tours 2]
  pipeline.py etat --dossier art/ [--json]
  pipeline.py fait plan --dossier art/ --fichier plan.md [--note "…"]
  pipeline.py valider plan --dossier art/
  pipeline.py refaire plan --dossier art/ --retour "ajouter une section prix"
  pipeline.py passer mots-cles --dossier art/ --raison "mot-clé donné par l'utilisateur"
  pipeline.py hypothese cadrage --dossier art/ "persona tiré de site-context.md"
  pipeline.py controler art/article.md --dossier art/ [options des contrôles]
  pipeline.py rapport --dossier art/

Codes de sortie : 0 OK ou LIVRABLE · 2 À CORRIGER, CONTRÔLES INCOMPLETS ou
RELECTURE HUMAINE · 3 BLOQUÉ · 1 erreur d'usage.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ETAPES = [
    ("cadrage", "Cadrage", "les réponses aux questions, ou les hypothèses écrites"),
    ("mots-cles", "Mots-clés", "mot-clé principal, secondaires, intention (/seo-keywords)"),
    ("serp", "SERP", "type de page qui gagne, manques, gain d'information (/seo-serp)"),
    ("plan", "Plan", "title, H1, H2/H3 commentés, cadre, liens (/seo-brief)"),
    ("redaction", "Rédaction", "l'article dans la voix du site (/seo-write)"),
    ("controles", "Contrôles", "portail qualité : rédaction, affirmations, humaniseur"),
    ("maillage", "Maillage", "liens entrants depuis les pages existantes (/seo-maillage)"),
    ("livraison", "Livraison", "article, bloc méta, trous et hypothèses listés"),
]
CLES = [e[0] for e in ETAPES]
FICHIER_ETAT = "etat-article.json"
TERMINES = {"validé", "passée"}
# Une étape passable : l'utilisateur fournit déjà le résultat.
PASSABLES = {"mots-cles", "serp", "maillage"}

SKILL = Path(__file__).resolve().parent.parent
TROU = re.compile(r"\{\{\s*à (?:compléter|confirmer)[^}]*\}\}")


class Usage(Exception):
    pass


# ---------------------------------------------------------------- état

def chemin_etat(dossier: str) -> Path:
    return Path(dossier) / FICHIER_ETAT


def charger(dossier: str) -> dict:
    p = chemin_etat(dossier)
    if not p.exists():
        raise Usage(f"pas de pipeline dans {dossier} : lance d'abord « pipeline.py init »")
    return json.loads(p.read_text(encoding="utf-8"))


def sauver(dossier: str, etat: dict) -> None:
    p = chemin_etat(dossier)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(etat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def aujourd_hui() -> str:
    return date.today().isoformat()


def nouvel_etat(sujet: str, ymyl: bool, autonome: bool, max_tours: int) -> dict:
    return {
        "sujet": sujet,
        "cree_le": aujourd_hui(),
        "ymyl": ymyl,
        "autonome": autonome,
        "max_tours": max_tours,
        "etapes": {k: {"statut": "à faire", "fichier": None, "notes": [], "hypotheses": [], "retours": []} for k in CLES},
        "tours": [],
        # Le compteur de tours repart à chaque nouvelle version de l'article
        # (rédaction refaite, ou étape d'avant changée) : un cycle par version.
        "cycle": 1,
    }


def verifier_cle(cle: str) -> None:
    if cle not in CLES:
        raise Usage(f"étape inconnue « {cle} » ; étapes : {', '.join(CLES)}")


def bloquantes_avant(etat: dict, cle: str) -> list[str]:
    """Étapes précédentes qui ne sont ni validées ni passées."""
    i = CLES.index(cle)
    return [k for k in CLES[:i] if etat["etapes"][k]["statut"] not in TERMINES]


def invalider_suivantes(etat: dict, cle: str, motif: str) -> list[str]:
    """Une étape change : les suivantes déjà produites passent « à revoir »."""
    touchees = []
    for k in CLES[CLES.index(cle) + 1:]:
        e = etat["etapes"][k]
        if e["statut"] in {"validé", "à valider"}:
            e["statut"] = "à revoir"
            e["notes"].append(f"{aujourd_hui()} · à revoir : {motif}")
            touchees.append(k)
    return touchees


def prochaine(etat: dict) -> str | None:
    for k in CLES:
        if etat["etapes"][k]["statut"] not in TERMINES:
            return k
    return None


def fait(etat: dict, cle: str, fichier: str | None, note: str | None) -> str:
    verifier_cle(cle)
    avant = bloquantes_avant(etat, cle)
    if avant:
        raise Usage(
            f"« {cle} » attend la validation de : {', '.join(avant)}. "
            "On ne rédige pas sans plan validé, on ne contrôle pas sans article."
        )
    e = etat["etapes"][cle]
    deja = e["statut"] in {"validé", "à valider", "à revoir", "à refaire"}
    e["fichier"] = fichier or e["fichier"]
    if note:
        e["notes"].append(f"{aujourd_hui()} · {note}")
    if etat["autonome"]:
        e["statut"] = "validé"
        e["notes"].append(f"{aujourd_hui()} · validé en mode autonome (hypothèses listées au rapport)")
    else:
        e["statut"] = "à valider"
    if deja:
        invalider_suivantes(etat, cle, f"« {cle} » a été refait")
    return e["statut"]


def valider(etat: dict, cle: str) -> None:
    verifier_cle(cle)
    e = etat["etapes"][cle]
    if e["statut"] != "à valider":
        raise Usage(f"« {cle} » est « {e['statut']} » : seule une étape « à valider » se valide")
    avant = bloquantes_avant(etat, cle)
    if avant:
        raise Usage(f"valide d'abord : {', '.join(avant)}")
    e["statut"] = "validé"
    e["notes"].append(f"{aujourd_hui()} · validé")


def refaire(etat: dict, cle: str, retour: str) -> list[str]:
    verifier_cle(cle)
    if not retour.strip():
        raise Usage("« refaire » demande le retour de l'utilisateur (--retour)")
    e = etat["etapes"][cle]
    if e["statut"] == "à faire":
        raise Usage(f"« {cle} » n'a pas encore été faite")
    e["statut"] = "à refaire"
    e["retours"].append(f"{aujourd_hui()} · {retour}")
    # Un retour de l'utilisateur sur une étape d'avant les contrôles donne une
    # nouvelle version de l'article : ses tours repartent de 1. Corriger
    # l'article après un verdict n'en est pas une (sinon la limite ne tiendrait pas).
    if CLES.index(cle) < CLES.index("controles") and etat["tours"]:
        etat["cycle"] = max(t.get("cycle", 1) for t in etat["tours"]) + 1
    return invalider_suivantes(etat, cle, f"« {cle} » à refaire : {retour}")


def passer(etat: dict, cle: str, raison: str) -> None:
    verifier_cle(cle)
    if cle not in PASSABLES:
        raise Usage(f"« {cle} » ne se passe pas (étapes passables : {', '.join(sorted(PASSABLES))})")
    if not raison.strip():
        raise Usage("« passer » demande une raison (--raison)")
    e = etat["etapes"][cle]
    e["statut"] = "passée"
    e["notes"].append(f"{aujourd_hui()} · passée : {raison}")


def hypothese(etat: dict, cle: str, texte: str) -> None:
    verifier_cle(cle)
    if not texte.strip():
        raise Usage("hypothèse vide")
    etat["etapes"][cle]["hypotheses"].append(texte.strip())


# ---------------------------------------------------------------- portail qualité

def trouver_script(outils: Path | None, skill: str, relatif: str) -> Path | None:
    """Script d'un Skill voisin : skills/<skill>/… (plugin, copie) ou modules/<skill>/… (claude.ai)."""
    bases = [outils] if outils else []
    bases.append(SKILL.parent)
    for base in bases:
        p = base / skill / relatif
        if p.exists():
            return p
    if relatif.startswith("commun/"):
        p = SKILL / relatif
        if p.exists():
            return p
    return None


def lancer(script: Path, args: list[str]) -> tuple[dict | None, str]:
    try:
        r = subprocess.run(
            [sys.executable, str(script), *args, "--json"],
            capture_output=True, text=True, timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, f"échec du lancement : {exc}"
    try:
        return json.loads(r.stdout), ""
    except json.JSONDecodeError:
        err = (r.stderr or r.stdout).strip().splitlines()
        return None, f"sortie illisible (code {r.returncode}) : {err[-1] if err else 'vide'}"


def portes(article: Path, opts: argparse.Namespace, ymyl: bool) -> list[dict]:
    """Les trois contrôles, chacun avec son verdict propre."""
    outils = Path(opts.outils) if opts.outils else None
    res = []

    # 1. rédaction : structure, style, règles maison, liens, bloc méta
    s = trouver_script(outils, "seo-write", "scripts/controle.py")
    args = [str(article)]
    if opts.affirmatif:
        args.append("--affirmatif")
    for r_ in opts.remplacer or []:
        args += ["--remplacer", r_]
    for m in opts.interdire or []:
        args += ["--interdire", m]
    for opt, val in (("--longueur", opts.longueur), ("--mot-cle", opts.mot_cle), ("--marque", opts.marque), ("--domaine", opts.domaine)):
        if val:
            args += [opt, val]
    if opts.sans_resume:
        args.append("--sans-resume")
    if getattr(opts, "h1_gabarit", False):
        args.append("--h1-gabarit")
    res.append(porte_redaction(s, args))

    # 2. affirmations : chaque fait vérifiable a sa source (bloquant en YMYL)
    s = trouver_script(outils, "seo-write", "commun/affirmations.py")
    args = [str(article)] + (["--ymyl"] if ymyl else [])
    if opts.contexte:
        args += ["--contexte", opts.contexte]
    if opts.reserve:
        args += ["--reserve", opts.reserve]
    res.append(porte_affirmations(s, args))

    # 3. humaniseur : tics d'écriture IA, profil article
    s = trouver_script(outils, "seo-human", "scripts/detect.py")
    args = [str(article), "--profil", "article", "--niveau", opts.niveau]
    if opts.affirmatif:
        args.append("--affirmatif")
    for m in opts.interdire or []:
        args += ["--interdire", m]
    res.append(porte_humaniseur(s, args, opts.seuil_humain))
    return res


def non_lance(nom: str, pourquoi: str) -> dict:
    return {"porte": nom, "etat": "NON LANCÉ", "resume": pourquoi, "a_corriger": [], "avis": []}


def porte_redaction(script: Path | None, args: list[str]) -> dict:
    nom = "Rédaction"
    if not script:
        return non_lance(nom, "controle.py introuvable : installe /seo-write à côté de /seo-article (ou --outils)")
    d, err = lancer(script, args)
    if d is None:
        return non_lance(nom, err)
    meta = d.get("meta") or {}
    hauts = [c for c in d.get("constats", []) if c.get("gravite") in {"haut", "moyen"}]
    etat = "OK" if d.get("verdict") == "PRÊT" else "À CORRIGER"
    resume = f"{d.get('verdict')} · {d.get('mots')} mots · {d.get('liens_internes')} liens internes"
    if meta.get("title_px"):
        resume += f" · title {meta['title_px']} px"
    if meta.get("description_px"):
        resume += f" · description {meta['description_px']} px"
    return {
        "porte": nom, "etat": etat, "resume": resume,
        "a_corriger": [f"[{c.get('gravite')}] {c.get('constat')}" for c in hauts],
    }


def porte_affirmations(script: Path | None, args: list[str]) -> dict:
    nom = "Affirmations"
    if not script:
        return non_lance(nom, "affirmations.py introuvable (dossier commun/ du pack)")
    d, err = lancer(script, args)
    if d is None:
        return non_lance(nom, err)
    verdict = d.get("verdict")
    etat = {"OK": "OK", "À VÉRIFIER": "À CORRIGER", "BLOQUÉ": "BLOQUÉ"}.get(verdict, "À CORRIGER")
    c = d.get("compte", {})
    mode = "YMYL" if d.get("ymyl") else "standard"
    resume = f"{verdict} en mode {mode} · {c.get('bloquant', 0)} bloquante(s), {c.get('à vérifier', 0)} à vérifier, {c.get('trou', 0)} trou(s) assumé(s)"
    fautes = [a for a in d.get("affirmations", []) if a.get("gravite") in {"bloquant", "à vérifier"}]
    return {
        "porte": nom, "etat": etat, "resume": resume,
        "a_corriger": [f"[{a.get('gravite')}] ligne {a.get('ligne')} ({', '.join(a.get('types', []))}) : {a.get('phrase')}" for a in fautes],
    }


def porte_humaniseur(script: Path | None, args: list[str], seuil: float) -> dict:
    nom = "Humaniseur"
    if not script:
        return non_lance(nom, "detect.py introuvable : installe /seo-human à côté de /seo-article (ou --outils)")
    d, err = lancer(script, args)
    if d is None:
        return non_lance(nom, err)
    r = (d.get("resultats") or [{}])[-1]
    score = r.get("score")
    verdict = r.get("verdict")
    a_reecrire = [p for p in r.get("densite", []) if p.get("action") not in {None, "LAISSER"}]
    faibles = [(k, c) for k, c in (r.get("controles") or {}).items() if isinstance(c.get("score"), (int, float)) and c["score"] < seuil]
    # Une fuite de modèle bloque ; un paragraphe à réécrire se corrige ; une note
    # globale basse sans passage désigné n'est qu'un avis : elle ne dit pas quoi
    # réécrire, et la faire bloquer ferait tourner la boucle à vide.
    if verdict == "SIGNALÉ":
        etat = "BLOQUÉ"
    elif a_reecrire:
        etat = "À CORRIGER"
    elif score is not None and score < seuil:
        etat = "AVIS"
    else:
        etat = "OK"
    resume = f"{score} {verdict} (profil article, niveau {d.get('niveau')}, seuil {seuil:g})"
    return {
        "porte": nom, "etat": etat, "resume": resume,
        "a_corriger": [f"paragraphe {p.get('paragraphe')} (ligne {p.get('ligne')}) : {p.get('action')}, {', '.join(p.get('extraits', []))}" for p in a_reecrire],
        "avis": [f"{k} {c['score']:g} : {c.get('detail', '')}" for k, c in faibles],
    }


def verdict_global(res: list[dict]) -> str:
    etats = [r["etat"] for r in res]
    if "BLOQUÉ" in etats:
        return "BLOQUÉ"
    if "À CORRIGER" in etats:
        return "À CORRIGER"
    if "NON LANCÉ" in etats:
        return "CONTRÔLES INCOMPLETS"
    return "LIVRABLE"


CODES = {"LIVRABLE": 0, "À CORRIGER": 2, "CONTRÔLES INCOMPLETS": 2, "RELECTURE HUMAINE": 2, "BLOQUÉ": 3}


def controler(article: Path, opts: argparse.Namespace) -> dict:
    if not article.exists():
        raise Usage(f"article introuvable : {article}")
    etat = None
    if opts.dossier and chemin_etat(opts.dossier).exists():
        etat = charger(opts.dossier)
    ymyl = opts.ymyl or bool(etat and etat["ymyl"])
    res = portes(article, opts, ymyl)
    verdict = verdict_global(res)
    texte = article.read_text(encoding="utf-8")
    trous = sorted(set(TROU.findall(texte)), key=texte.index)
    tour = 1
    max_tours = opts.max_tours
    avertissement = ""
    if etat is not None:
        reprendre = [k for k in CLES[:CLES.index("controles")] if etat["etapes"][k]["statut"] in {"à refaire", "à revoir"}]
        if reprendre:
            avertissement = f"étapes à reprendre avant : {', '.join(reprendre)} ; ce contrôle porte sur une version qui va changer"
        max_tours = max_tours or etat["max_tours"]
        cycle = etat.get("cycle", 1)
        tour = sum(1 for t in etat["tours"] if t.get("cycle", 1) == cycle) + 1
    max_tours = max_tours or 2
    # BLOQUÉ reste BLOQUÉ : une affirmation sans source ne se « relit » pas, elle se source ou sort.
    if verdict in {"À CORRIGER", "CONTRÔLES INCOMPLETS"} and tour >= max_tours:
        verdict = "RELECTURE HUMAINE"
    if etat is not None:
        etat["tours"].append({"cycle": cycle, "tour": tour, "date": aujourd_hui(), "verdict": verdict, "portes": {r["porte"]: r["etat"] for r in res}})
        e = etat["etapes"]["controles"]
        e["fichier"] = str(article)
        if not bloquantes_avant(etat, "controles"):
            e["statut"] = ("validé" if etat["autonome"] else "à valider") if verdict == "LIVRABLE" else "à refaire"
        sauver(opts.dossier, etat)
    return {"article": str(article), "tour": tour, "max_tours": max_tours, "ymyl": ymyl,
            "verdict": verdict, "portes": res, "trous": trous, "avertissement": avertissement}


def afficher_controle(r: dict) -> str:
    lignes = [f"PORTAIL QUALITÉ · tour {r['tour']} sur {r['max_tours']} · {'YMYL' if r['ymyl'] else 'standard'}"]
    if r.get("avertissement"):
        lignes.append(f"ATTENTION · {r['avertissement']}")
    for p in r["portes"]:
        lignes.append(f"  {p['porte']:<13} {p['etat']:<11} {p['resume']}")
    lignes.append(f"VERDICT · {r['verdict']}")
    avis = [(p["porte"], c) for p in r["portes"] for c in p.get("avis", [])]
    corrections = [(p["porte"], c) for p in r["portes"] for c in p["a_corriger"]]
    if corrections:
        lignes.append("À CORRIGER (dans l'ordre : bloquants d'abord)")
        ordre = {"Affirmations": 0, "Rédaction": 1, "Humaniseur": 2}
        for porte, c in sorted(corrections, key=lambda x: ordre.get(x[0], 9)):
            lignes.append(f"  {porte} · {c}")
    if avis:
        lignes.append("AVIS (non bloquant : à améliorer si un passage s'y prête)")
        lignes += [f"  {porte} · {c}" for porte, c in avis]
    if r["trous"]:
        lignes.append(f"TROUS ASSUMÉS ({len(r['trous'])})")
        lignes += [f"  {t}" for t in r["trous"]]
    suite = {
        "LIVRABLE": "Montre l'article et le bloc « Contrôles » ; l'utilisateur valide l'étape.",
        "À CORRIGER": "Corrige seulement les passages listés, puis relance le contrôle.",
        "CONTRÔLES INCOMPLETS": "Un contrôle n'a pas tourné : installe le Skill manquant, ou fais ce contrôle à la lecture et dis-le.",
        "RELECTURE HUMAINE": "Plus de tour automatique : livre l'article avec cette liste, l'utilisateur tranche.",
        "BLOQUÉ": "Chaque affirmation bloquante se source, se reformule sans chiffre, ou devient un trou listé. On ne livre pas un article bloqué.",
    }[r["verdict"]]
    lignes.append(f"SUITE · {suite}")
    return "\n".join(lignes)


# ---------------------------------------------------------------- affichages

def afficher_etat(etat: dict) -> str:
    mode = "autonome" if etat["autonome"] else "validé étape par étape"
    lignes = [f"ARTICLE · {etat['sujet']} · {'YMYL · ' if etat['ymyl'] else ''}{mode}"]
    for k, nom, quoi in ETAPES:
        e = etat["etapes"][k]
        extra = f" · {e['fichier']}" if e["fichier"] else ""
        lignes.append(f"  {nom:<10} {e['statut']:<10}{extra}")
        if e["statut"] == "à refaire" and e["retours"]:
            lignes.append(f"             retour : {e['retours'][-1].split(' · ', 1)[-1]}")
    p = prochaine(etat)
    if p is None:
        lignes.append("SUITE · pipeline terminé")
    else:
        nom, quoi = next((n, q) for k, n, q in ETAPES if k == p)
        statut = etat["etapes"][p]["statut"]
        verbe = {"à valider": "faire valider", "à refaire": "refaire, avec le retour", "à revoir": "revoir (une étape d'avant a changé)"}.get(statut, "faire")
        lignes.append(f"SUITE · {nom} : {verbe} · {quoi}")
    nb = sum(len(etat["etapes"][k]["hypotheses"]) for k in CLES)
    if nb:
        lignes.append(f"HYPOTHÈSES · {nb} (listées au rapport)")
    return "\n".join(lignes)


def afficher_rapport(etat: dict) -> str:
    lignes = [f"RAPPORT · {etat['sujet']}"]
    for k, nom, _ in ETAPES:
        e = etat["etapes"][k]
        lignes.append(f"  {nom:<10} {e['statut']}")
    cycles = sorted({t.get("cycle", 1) for t in etat["tours"]})
    for c in cycles:
        tours = [t for t in etat["tours"] if t.get("cycle", 1) == c]
        histo = " → ".join(t["verdict"] for t in tours)
        version = f"version {c} · " if len(cycles) > 1 else ""
        lignes.append(f"CONTRÔLES · {version}{len(tours)} tour(s) : {histo}")
    hyps = [(nom, h) for k, nom, _ in ETAPES for h in etat["etapes"][k]["hypotheses"]]
    if hyps:
        lignes.append("HYPOTHÈSES À CONFIRMER")
        lignes += [f"  {nom} · {h}" for nom, h in hyps]
    restantes = [nom for k, nom, _ in ETAPES if etat["etapes"][k]["statut"] not in TERMINES]
    lignes.append("RESTE · " + (", ".join(restantes) if restantes else "rien : pipeline terminé"))
    return "\n".join(lignes)


# ---------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Pipeline d'un article SEO : étapes validées et portail qualité.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("sujet")
    p.add_argument("--dossier", default=".")
    p.add_argument("--ymyl", action="store_true", help="santé, argent, assurance, droit")
    p.add_argument("--autonome", action="store_true", help="avancer sans attendre, hypothèses écrites")
    p.add_argument("--max-tours", type=int, default=2)
    p.add_argument("--forcer", action="store_true", help="écraser un pipeline existant")

    p = sub.add_parser("etat")
    p.add_argument("--dossier", default=".")
    p.add_argument("--json", action="store_true")

    for nom in ("fait", "valider", "refaire", "passer"):
        p = sub.add_parser(nom)
        p.add_argument("etape")
        p.add_argument("--dossier", default=".")
        if nom == "fait":
            p.add_argument("--fichier")
            p.add_argument("--note")
        if nom == "refaire":
            p.add_argument("--retour", default="")
        if nom == "passer":
            p.add_argument("--raison", default="")

    p = sub.add_parser("hypothese")
    p.add_argument("etape")
    p.add_argument("texte")
    p.add_argument("--dossier", default=".")

    p = sub.add_parser("rapport")
    p.add_argument("--dossier", default=".")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("controler")
    p.add_argument("article")
    p.add_argument("--dossier", help="dossier du pipeline (compte les tours)")
    p.add_argument("--ymyl", action="store_true")
    p.add_argument("--max-tours", type=int, default=0)
    p.add_argument("--outils", help="dossier qui contient seo-write/ et seo-human/")
    p.add_argument("--affirmatif", action="store_true")
    p.add_argument("--remplacer", action="append")
    p.add_argument("--interdire", action="append")
    p.add_argument("--longueur")
    p.add_argument("--mot-cle")
    p.add_argument("--marque")
    p.add_argument("--domaine")
    p.add_argument("--sans-resume", action="store_true")
    p.add_argument("--h1-gabarit", action="store_true", help="texte de gabarit : le H1 est déjà dans la page")
    p.add_argument("--contexte", help="site-context.md")
    p.add_argument("--reserve", help="reserve.md")
    p.add_argument("--niveau", choices=["forensique", "strict", "esthetique"], default="strict")
    p.add_argument("--seuil-humain", type=float, default=70.0)
    p.add_argument("--json", action="store_true")

    a = ap.parse_args(argv)
    try:
        if a.cmd == "init":
            if chemin_etat(a.dossier).exists() and not a.forcer:
                raise Usage(f"un pipeline existe déjà dans {a.dossier} (--forcer pour l'écraser)")
            if a.max_tours < 1:
                raise Usage("--max-tours vaut 1 au moins")
            etat = nouvel_etat(a.sujet, a.ymyl, a.autonome, a.max_tours)
            sauver(a.dossier, etat)
            print(afficher_etat(etat))
            return 0
        if a.cmd == "controler":
            r = controler(Path(a.article), a)
            print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher_controle(r))
            return CODES[r["verdict"]]
        etat = charger(a.dossier)
        if a.cmd == "etat":
            print(json.dumps(etat, ensure_ascii=False, indent=2) if a.json else afficher_etat(etat))
            return 0
        if a.cmd == "rapport":
            print(json.dumps(etat, ensure_ascii=False, indent=2) if a.json else afficher_rapport(etat))
            return 0
        if a.cmd == "fait":
            fait(etat, a.etape, a.fichier, a.note)
        elif a.cmd == "valider":
            valider(etat, a.etape)
        elif a.cmd == "refaire":
            refaire(etat, a.etape, a.retour)
        elif a.cmd == "passer":
            passer(etat, a.etape, a.raison)
        elif a.cmd == "hypothese":
            hypothese(etat, a.etape, a.texte)
        sauver(a.dossier, etat)
        print(afficher_etat(etat))
        return 0
    except Usage as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
