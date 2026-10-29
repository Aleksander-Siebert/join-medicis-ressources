#!/usr/bin/env python3
"""audit.py : diagnostic GEO d'une page, couche par couche, avec une note de préparation.

Assemble les scripts des autres Skills du pack, dans l'ordre où un moteur
de réponse rencontre la page :

  1. ACCÈS     robots.txt (RFC 9309), Googlebot, robots de recherche des IA,
               indexable, extrait autorisé, pare-feu (--sonder)   /geo-acces
  2. PAGE      texte dans le HTML serveur, canonical, un H1, date  /geo-contenu
  3. CONTENU   réponse en tête, statistiques sourcées, promesses,
               première main                                       /geo-contenu
  4. ENTITÉ    nom cohérent, Organization, sameAs, balisage visible /geo-entite
  5. AGENTS    noms et labels, interactifs, consignes cachées aux IA /geo-agentic

Chaque contrôle vaut des points, a une preuve (ce que le script a lu) et une
source (page Google ou table datée du pack). La note de préparation est la
part des points obtenus **sur les contrôles mesurés** : un contrôle non
mesuré sort du calcul, avec sa raison. Elle dit si la page est prête à être
lue et citée, pas si elle le sera. La visibilité réelle (--mesure, sortie de
/geo-visibilite) s'affiche à part et ne s'additionne jamais à la note.

  python3 audit.py https://www.site.fr/page/ --marque "Assurly"
  python3 audit.py https://www.site.fr/page/ --marque "Assurly" --question "Combien coûte…" --mesure mesure.json --sonder
  python3 audit.py page.html --url https://www.site.fr/page/ --robots robots.txt --marque "Assurly"   # hors ligne
  … --journal journal-geo.csv     ajoute la note et les contrôles manqués au journal (avant / après)

Python 3 sans dépendance. Code 0 ; 1 si la page est illisible.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ICI = Path(__file__).resolve().parent
SKILLS = ICI.parents[1]


def charger(skill: str, module: str):
    """Charge le script d'un autre Skill du pack (dossier voisin), ou None s'il manque."""
    chemin = SKILLS / skill / "scripts" / f"{module}.py"
    if not chemin.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"geo_{module}", chemin)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(chemin.parent))
    spec.loader.exec_module(m)
    return m


acces = charger("geo-acces", "acces")
contenu = charger("geo-contenu", "contenu")
entite = charger("geo-entite", "entite")
agentic = charger("geo-agentic", "agentic")
for cand in (ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (cand / "page.py").exists():
        sys.path.insert(0, str(cand))
        break
import page as pg  # noqa: E402

G = "https://developers.google.com/search/docs/"
SRC = {
    "ia": G + "fundamentals/ai-optimization-guide?hl=fr",
    "robots": G + "crawling-indexing/robots/intro?hl=fr",
    "noindex": G + "crawling-indexing/block-indexing?hl=fr",
    "extrait": G + "appearance/snippet?hl=fr",
    "js": G + "crawling-indexing/javascript/javascript-seo-basics?hl=fr",
    "canonical": G + "crawling-indexing/consolidate-duplicate-urls?hl=fr",
    "utile": G + "fundamentals/creating-helpful-content?hl=fr",
    "sd": G + "appearance/structured-data/sd-policies?hl=fr",
    "table": "commun/preuves.md §1 (table datée des robots)",
    "agents": "https://web.dev/articles/ai-agent-site-ux",
    "pack": "règle du pack (commun/regles.md)",
}
COUCHES = ["ACCÈS", "PAGE", "CONTENU", "ENTITÉ", "AGENTS"]
CRITIQUES = {"A2", "A3", "A4", "P1", "G3"}


def controle(couche, ident, libelle, points, etat, preuve, source, skill):
    return {"couche": couche, "id": ident, "libelle": libelle, "points": points, "etat": etat,
            "preuve": preuve, "source": SRC.get(source, source), "skill": skill}


def absent(couche, ident, libelle, points, skill):
    return controle(couche, ident, libelle, points, "non mesuré", f"script de {skill} absent du pack installé", "pack", skill)


# ---------------------------------------------------------------- couches

def couche_acces(ra: dict | None, sondes_faites: bool) -> list[dict]:
    if ra is None:
        return [absent("ACCÈS", i, l, p, "/geo-acces") for i, l, p in
                (("A1", "robots.txt lisible", 3), ("A2", "Googlebot autorisé", 5), ("A3", "page indexable", 5),
                 ("A4", "extrait autorisé", 5))]
    out = []
    rob = ra["robots_txt"]
    if rob.startswith("NON LU") or rob == "non lu":
        out.append(controle("ACCÈS", "A1", "robots.txt lisible", 3, "non mesuré", rob[:120], "robots", "/geo-acces"))
    else:
        out.append(controle("ACCÈS", "A1", "robots.txt lisible", 3, "manqué" if rob.startswith("erreur serveur") else "ok",
                            rob, "robots", "/geo-acces"))
    par = {r["jeton"]: r for r in ra["robots"]}
    for ident, jeton, pts, src in (("A2", "Googlebot", 5, "robots"), ("A5", "OAI-SearchBot", 4, "table"),
                                   ("A6", "Bingbot", 3, "table"), ("A7", "PerplexityBot", 3, "table"),
                                   ("A8", "Claude-SearchBot", 3, "table")):
        r = par.get(jeton)
        if r is None:
            continue
        if rob.startswith("NON LU"):
            out.append(controle("ACCÈS", ident, f"{jeton} autorisé", pts, "non mesuré", "robots.txt non lu", src, "/geo-acces"))
            continue
        out.append(controle("ACCÈS", ident, f"{jeton} autorisé par robots.txt", pts, "ok" if r["autorise"] else "manqué",
                            f"groupe {r['groupe']} · {r['regle']}", src, "/geo-acces"))
    p = ra["page"]
    if p is None:
        out += [controle("ACCÈS", "A3", "page indexable", 5, "non mesuré", "page non lue", "noindex", "/geo-acces"),
                controle("ACCÈS", "A4", "extrait autorisé", 5, "non mesuré", "page non lue", "extrait", "/geo-acces")]
    else:
        out.append(controle("ACCÈS", "A3", "page indexable (pas de noindex)", 5, "manqué" if p["noindex"] else "ok",
                            ", ".join(p["noindex"]) or "aucun noindex", "noindex", "/geo-acces"))
        extrait = p["nosnippet"] or (p["max_snippet"] == 0)
        out.append(controle("ACCÈS", "A4", "extrait autorisé (condition des Aperçus IA)", 5, "manqué" if extrait else "ok",
                            ", ".join(p["nosnippet"]) or (f"max-snippet:{p['max_snippet']}" if p["max_snippet"] is not None else "aucune restriction"),
                            "ia", "/geo-acces"))
    if sondes_faites:
        refus = [r["jeton"] for r in ra["robots"] if r.get("sonde") and r["sonde"].get("refuse")]
        non_lus = [r["jeton"] for r in ra["robots"] if r.get("sonde") and r["sonde"].get("non_lu")]
        if refus:
            # un pare-feu peut refuser un faux user-agent et accepter le vrai robot (vérifié par son adresse IP)
            out.append(controle("ACCÈS", "A9", "pas de refus au user-agent des robots (pare-feu)", 4, "à vérifier",
                                f"refusé à : {', '.join(refus)} ; à confirmer dans les réglages du pare-feu ou les journaux",
                                "table", "/geo-acces"))
        elif non_lus and len(non_lus) == len([r for r in ra["robots"] if r.get("sonde")]):
            out.append(controle("ACCÈS", "A9", "pas de refus au user-agent des robots (pare-feu)", 4, "non mesuré",
                                "aucun appel n'a abouti (réseau)", "table", "/geo-acces"))
        else:
            out.append(controle("ACCÈS", "A9", "pas de refus au user-agent des robots (pare-feu)", 4, "ok",
                                "aucun refus constaté" + (f" ; non lus : {', '.join(non_lus)}" if non_lus else ""),
                                "table", "/geo-acces"))
    else:
        out.append(controle("ACCÈS", "A9", "pas de refus au user-agent des robots (pare-feu)", 4, "non mesuré",
                            "lancer avec --sonder", "table", "/geo-acces"))
    return out


def couche_page_contenu(rc: dict | None, html: str, url: str | None) -> list[dict]:
    if rc is None:
        return [absent("PAGE", "P1", "texte dans le HTML serveur", 8, "/geo-contenu"),
                absent("CONTENU", "C1", "réponse en tête", 8, "/geo-contenu")]
    p = pg.analyser(html)
    out = []
    out.append(controle("PAGE", "P1", "texte dans le HTML serveur (150 mots ou plus)", 8,
                        "ok" if p["mots"] >= 150 else "manqué", f"{p['mots']} mots", "js", "/geo-contenu"))
    can = p["canonical"]
    if url and can:
        cible = urljoin(url, can).split("#")[0].rstrip("/")
        etat = "ok" if cible == url.split("#")[0].rstrip("/") else "manqué"
        preuve = f"canonical → {cible}" + ("" if etat == "ok" else " (autre URL : c'est elle qui sera lue)")
    else:
        etat, preuve = ("ok", f"canonical {can}" if can else "pas de canonical (la page elle-même)")
    out.append(controle("PAGE", "P2", "canonical vers cette page", 3, etat, preuve, "canonical", "/geo-acces"))
    h1 = [a for a in rc["alertes"] if "H1" in a]
    out.append(controle("PAGE", "P3", "un seul H1", 2, "manqué" if h1 else "ok", h1[0] if h1 else "1 H1", "utile", "/geo-contenu"))
    d = [a for a in rc["alertes"] if "date" in a]
    out.append(controle("PAGE", "P4", "date de publication ou de mise à jour", 2, "manqué" if d else "ok",
                        d[0] if d else "date trouvée", "utile", "/geo-contenu"))
    b = rc["bilan"]
    ok, n = b["reponse"]
    if n:
        out.append(controle("CONTENU", "C1", "sections qui répondent en tête (60% ou plus)", 8,
                            "ok" if ok / n >= 0.6 else "manqué", f"{ok}/{n} sections", "utile", "/geo-contenu"))
    else:
        out.append(controle("CONTENU", "C1", "sections qui répondent en tête", 8, "non mesuré", "aucune section de 15 mots", "utile", "/geo-contenu"))
    ok, n = b["sources"]
    out.append(controle("CONTENU", "C2", "statistiques sourcées", 5, ("ok" if ok == n else "manqué") if n else "non mesuré",
                        f"{ok}/{n} sections" if n else "aucune statistique sur la page", "utile", "/geo-contenu"))
    ok, n = b["promesses"]
    out.append(controle("CONTENU", "C3", "aucune promesse à prouver (« n°1 », « le moins cher »)", 3,
                        ("ok" if ok == n else "manqué") if n else "non mesuré", f"{n - ok} section(s) concernée(s)", "pack", "/geo-contenu"))
    pm = rc.get("premiere_main") or []
    out.append(controle("CONTENU", "C4", "élément de première main (cas, donnée maison, expérience)", 4,
                        "ok" if pm else "manqué", f"« {pm[0]['indice'][:70]} »" if pm else "rien de propre au site",
                        "ia", "/geo-contenu"))
    return out


def couche_entite(re_: dict | None) -> list[dict]:
    if re_ is None:
        return [absent("ENTITÉ", "E1", "nom de la marque cohérent", 5, "/geo-entite")]
    n, o = re_["noms"], re_["organisation"]
    out = []
    declares = [x for x in n["lignes"] if x["source"].startswith(("JSON-LD", "og:site_name", "application-name", "mention"))]
    var = [x for x in n["lignes"] if x["etat"] == "variante"]
    trouve = [x for x in n["lignes"] if x["etat"] == "marque"]
    if declares or var or trouve:
        out.append(controle("ENTITÉ", "E1", "nom de la marque cohérent", 5, "manqué" if var else "ok",
                            ", ".join(f"{x['source']} « {x['lu'][:30]} »" for x in var[:2]) or f"« {n['marque']} » partout",
                            "pack", "/geo-entite"))
    else:
        out.append(controle("ENTITÉ", "E1", "nom de la marque cohérent", 5, "non mesuré", "aucun nom déclaré lu", "pack", "/geo-entite"))
    deux = [a for a in o["alertes"] if "noms différents" in a or "sans @id commun" in a]
    out.append(controle("ENTITÉ", "E2", "un bloc Organization (ou sous-type) par entité", 4,
                        "manqué" if (o["orgs"] == 0 or deux) else "ok",
                        "aucun bloc" if o["orgs"] == 0 else (deux[0][:80] if deux else f"{o['orgs']} bloc(s)"), "sd", "/geo-entite"))
    bons = [p for p in o["profils"] if p["plateforme"] != "linkedin (profil personnel)"]
    out.append(controle("ENTITÉ", "E3", "sameAs vers les profils de l'organisation", 3, "ok" if bons else "manqué",
                        f"{len(bons)} profil(s)" + (" ; profil personnel retiré du compte" if len(bons) < len(o["profils"]) else ""),
                        "pack", "/geo-entite"))
    graves = [v for v in re_["visible"] if v["libelle"] in ("note", "nombre d'avis", "nombre de notes", "prix", "prix bas", "prix haut")]
    if graves:
        inv = [v for v in graves if not v["visible"]]
        out.append(controle("ENTITÉ", "E4", "note et prix balisés visibles sur la page", 3, "manqué" if inv else "ok",
                            ", ".join(f"{v['libelle']} {v['valeur']}" for v in inv) or "tous visibles", "sd", "/geo-entite"))
    else:
        out.append(controle("ENTITÉ", "E4", "note et prix balisés visibles sur la page", 3, "non mesuré",
                            "ni note ni prix balisés", "sd", "/geo-entite"))
    return out


def couche_agents(rg: dict | None) -> list[dict]:
    if rg is None:
        return [absent("AGENTS", "G3", "aucune consigne cachée aux IA", 7, "/geo-agentic")]
    st = {c["controle"]: c for c in rg["controles"]}
    h = rg["details"]
    noms = len(h["actions_sans_nom"]) + len(h["champs_sans_label"])
    caches = len(h["interactifs_caches"]) + len(h["cliquables_non_semantiques"])
    conf = st["Aucune consigne cachée aux IA"]
    return [
        controle("AGENTS", "G1", "boutons, liens et champs nommés", 5, "ok" if not noms else "manqué",
                 f"{len(h['actions_sans_nom'])} sans nom, {len(h['champs_sans_label'])} champ(s) sans label", "agents", "/geo-agentic"),
        controle("AGENTS", "G2", "rien de cliquable caché ou non sémantique", 3, "ok" if not caches else "manqué",
                 f"{caches} élément(s)", "agents", "/geo-agentic"),
        controle("AGENTS", "G3", "aucune consigne cachée aux IA", 7, "ok" if conf["statut"] == "OK" else "manqué",
                 conf["valeur"], "ia", "/geo-agentic"),
    ]


# ---------------------------------------------------------------- synthèse

def note(ctrls: list[dict]) -> dict:
    mesures = [c for c in ctrls if c["etat"] in ("ok", "manqué")]
    obtenus = sum(c["points"] for c in mesures if c["etat"] == "ok")
    possibles = sum(c["points"] for c in mesures)
    par_couche = {}
    for k in COUCHES:
        m = [c for c in mesures if c["couche"] == k]
        par_couche[k] = (sum(c["points"] for c in m if c["etat"] == "ok"), sum(c["points"] for c in m))
    return {"note": round(100 * obtenus / possibles) if possibles else None, "obtenus": obtenus, "possibles": possibles,
            "hors_calcul": sum(c["points"] for c in ctrls if c["etat"] not in ("ok", "manqué")), "par_couche": par_couche}


def premiere_couche(ctrls: list[dict]) -> str | None:
    for k in COUCHES:
        if any(c["couche"] == k and c["etat"] == "manqué" and (c["id"] in CRITIQUES or c["points"] >= 4) for c in ctrls):
            return k
    for k in COUCHES:
        if any(c["couche"] == k and c["etat"] == "manqué" for c in ctrls):
            return k
    return None


def visibilite(mesure: dict) -> list[str]:
    L = []
    for mot, r in mesure.get("moteurs", {}).items():
        if mot == "TOTAL" and len(mesure["moteurs"]) > 2:
            continue
        def t(k):
            x = r[k]
            return f"{round(100 * x['taux'])}% ({x['k']}/{x['n']}, {round(100 * x['ic'][0])}-{round(100 * x['ic'][1])}%)"
        L.append(f"  {mot:<24} mentionnée {t('mentionnee')} · recommandée {t('recommandee')} · citée {t('citee')}")
    L.append(f"  {mesure.get('etiquette', '')} · {mesure.get('questions', '?')} questions · "
             f"{len(mesure.get('perdues', []))} paire(s) question × moteur perdue(s)")
    return L


HORS_SITE = [
    "réglage « Contrôle de l'IA générative dans la Recherche » de Search Console (inclure, exclure, hériter)",
    "indexation réelle : rapport « Pages » et inspection de l'URL dans Search Console",
    "ce que les IA disent de la marque : /geo-exactitude",
    "sites tiers cités là où la marque perd : /geo-mentions",
]


def afficher(r: dict) -> str:
    n = r["note"]
    L = [f"AUDIT GEO · {r['url']} · {r['date']}"]
    L.append(f"PRÉPARATION · {n['note']}/100 sur les contrôles mesurés ({n['obtenus']}/{n['possibles']} points ; "
             f"{n['hors_calcul']} points non mesurés ou à vérifier, hors calcul)" if n["note"] is not None else "PRÉPARATION · aucun contrôle mesuré")
    L.append("  Dit si la page est prête à être lue et citée, pas si elle le sera.")
    if r["premiere"]:
        L.append(f"  Couche à traiter d'abord : {r['premiere']} (corriger une couche plus basse ne compense pas celle-ci).")
    for k in COUCHES:
        ok, tot = n["par_couche"][k]
        cs = [c for c in r["controles"] if c["couche"] == k]
        if not cs:
            continue
        L += ["", f"{k} · {ok}/{tot} points" if tot else f"{k} · non mesuré"]
        for c in cs:
            marque = {"ok": "ok     ", "manqué": "MANQUÉ ", "non mesuré": "·      ", "à vérifier": "?      "}[c["etat"]]
            L.append(f"  {marque}{c['id']:<4}{c['libelle']:<56}{c['points']:>2} pt · {c['preuve'][:90]}")
            if c["etat"] in ("manqué", "à vérifier"):
                L.append(f"         → {c['skill']} · source : {c['source']}")
    if r.get("familles"):
        f = r["familles"]
        abs_ = [x["famille"] for x in f["familles"] if not x["presente"]]
        L += ["", f"FAMILLES DE FAITS · « {f['question']} » · type {f['type']} (déduit, sans points) · "
              + ("toutes présentes" if not abs_ else "absentes : " + ", ".join(abs_))]
    L += ["", "VISIBILITÉ (mesurée à part, jamais additionnée à la note)"]
    L += visibilite(r["mesure"]) if r.get("mesure") else ["  non mesurée : /geo-visibilite"]
    L += ["", "À VÉRIFIER HORS DU SITE"] + [f"  · {x}" for x in HORS_SITE]
    L += ["", "Ce que Google dit d'abord : les Aperçus IA et le Mode IA reposent sur la recherche classique ;",
          f"aucune optimisation spéciale n'est requise ({SRC['ia']})."]
    return "\n".join(L)


def journal(chemin: str, r: dict) -> None:
    nouveau = not Path(chemin).exists()
    with open(chemin, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        if nouveau:
            w.writerow(["date", "url", "note", "points", "manqués", "non mesurés", "action menée"])
        w.writerow([r["date"], r["url"], r["note"]["note"], f"{r['note']['obtenus']}/{r['note']['possibles']}",
                    " ".join(c["id"] for c in r["controles"] if c["etat"] == "manqué"),
                    " ".join(c["id"] for c in r["controles"] if c["etat"] == "non mesuré"), "{{à compléter}}"])


def auditer(html, entetes, url, robots_txt, statut_robots, erreur_robots, marque=None, question=None,
            sondes=None, mesure=None, statut_page=200, date=None) -> dict:
    ra = acces.analyser(robots_txt, statut_robots, erreur_robots, html, entetes, url or "https://exemple.fr/",
                        statut_page, sondes) if acces else None
    rc = contenu.analyser(url or "page", html, None, entetes, question) if contenu else None
    re_ = entite.analyser(html, marque) if entite else None
    rg = agentic.analyser(html, entetes, None) if agentic else None
    ctrls = couche_acces(ra, sondes is not None) + couche_page_contenu(rc, html, url) + couche_entite(re_) + couche_agents(rg)
    ctrls.sort(key=lambda c: (COUCHES.index(c["couche"]), c["id"]))
    return {"url": url or "(fichier)", "date": date or dt.date.today().isoformat(), "controles": ctrls, "note": note(ctrls),
            "premiere": premiere_couche(ctrls), "familles": (rc or {}).get("couverture"), "mesure": mesure}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Diagnostic GEO d'une page, couche par couche.")
    ap.add_argument("source", help="URL ou fichier HTML")
    ap.add_argument("--url", help="URL de la page si la source est un fichier")
    ap.add_argument("--robots", help="robots.txt enregistré (hors ligne)")
    ap.add_argument("--marque", help="nom de la marque")
    ap.add_argument("--question", help="question visée par la page (familles de faits)")
    ap.add_argument("--mesure", help="sortie JSON de /geo-visibilite, affichée à part")
    ap.add_argument("--sonder", action="store_true", help="appeler la page avec le user-agent des robots (pare-feu)")
    ap.add_argument("--journal", help="fichier CSV où ajouter cet audit")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--date", help="date de l'audit (AAAA-MM-JJ), par défaut aujourd'hui")
    a = ap.parse_args(argv)
    if acces is None and contenu is None and entite is None and agentic is None:
        print("Aucun script du pack trouvé à côté de geo-audit : installe le pack complet.", file=sys.stderr)
        return 1
    entetes, statut = {}, 200
    if re.match(r"https?://", a.source):
        lu = pg.lire(a.source)
        if lu["statut"] is None or lu["statut"] >= 400:
            print(f"Page non lue ({lu['erreur'] or lu['statut']}) : pare-feu ou erreur. Enregistre le HTML et relance "
                  "avec --url ; /geo-acces --sonder montre qui est refusé.", file=sys.stderr)
            return 1
        html, url, entetes, statut = lu["texte"], lu["url"], lu["entetes"], lu["statut"]
    else:
        try:
            html = pg.lire_fichier(a.source)
        except OSError as e:
            print(f"Erreur : {e}", file=sys.stderr)
            return 1
        url = a.url
    if a.robots:
        robots_txt, st_r, err_r = pg.lire_fichier(a.robots), 200, None
    elif url:
        rr = pg.lire(urljoin(url, "/robots.txt"), accept="text/plain,*/*")
        robots_txt = rr["texte"] if rr["statut"] and rr["statut"] < 400 else None
        st_r, err_r = rr["statut"], rr["erreur"]
    else:
        robots_txt, st_r, err_r = None, None, "ni URL ni --robots"
    sondes = acces.sonder(url) if (a.sonder and url and acces) else None
    mesure = None
    if a.mesure:
        try:
            mesure = json.loads(Path(a.mesure).read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"Mesure illisible ({e}) : ignorée.", file=sys.stderr)
    r = auditer(html, entetes, url, robots_txt, st_r, err_r, a.marque, a.question, sondes, mesure, statut, date=a.date)
    if a.journal:
        journal(a.journal, r)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
