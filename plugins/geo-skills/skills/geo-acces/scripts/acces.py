#!/usr/bin/env python3
"""acces.py : qui peut lire le site, et pour en faire quoi.

Pour chaque robot d'IA (table datée de commun/robots_ia.json) : ce que
robots.txt autorise selon la RFC 9309, et ce que ça veut dire pour chaque
moteur (« citable dans ChatGPT » se lit sur OAI-SearchBot, jamais sur
GPTBot). Puis la page : noindex, nosnippet, max-snippet, data-nosnippet
(condition des Aperçus IA de Google), texte présent dans le HTML serveur,
canonical ; le bloc robots.txt géré par Cloudflare ; la directive
Content-Signal ; llms.txt (rapporté, sans poids).

  python3 acces.py https://www.site.fr/guide/
  python3 acces.py https://www.site.fr/guide/ --sonder          appelle la page avec le user-agent de chaque robot de recherche
  python3 acces.py --robots robots.txt --html page.html --url https://www.site.fr/guide/   hors ligne
  python3 acces.py https://www.site.fr --proposer refus-entrainement   bloc robots.txt à proposer
  python3 acces.py … --json

Un robots.txt non lu à cause d'une erreur réseau n'est jamais présenté comme
« absent » : le script dit qu'il ne l'a pas lu. Rien n'est modifié sur le site.
Code 0, ou 1 en cas d'erreur d'entrée.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ICI = Path(__file__).resolve().parent
for cand in (ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (cand / "robots_rfc.py").exists():
        COMMUN = cand
        break
else:  # pragma: no cover
    sys.exit("commun/ introuvable : lance outils/propager.py")
sys.path.insert(0, str(COMMUN))
import page as pg  # noqa: E402
import robots_rfc  # noqa: E402

TABLE = json.loads((COMMUN / "robots_ia.json").read_text(encoding="utf-8"))
ROBOTS = TABLE["robots"]
VERIFIE_LE = TABLE["verifie_le"]
CLES_CS = {"search", "ai-input", "ai-train"}
CLES_CS_EXPERIMENTALES = {"use"}

STRATEGIES = {
    "visibilite": "tout autoriser, entraînement compris",
    "equilibre": "autoriser recherche et visites des utilisateurs, refuser l'entraînement",
    "refus-entrainement": "comme équilibre, en refusant aussi les jetons d'usage (Google-Extended, Applebot-Extended)",
}


# ── robots.txt ───────────────────────────────────────────────────────────────

def bloc_cloudflare(texte: str) -> bool:
    return bool(re.search(r"#\s*BEGIN Cloudflare Managed", texte or "", re.I))


def content_signals(texte: str) -> list[dict]:
    out = []
    for n, ligne in enumerate((texte or "").splitlines(), 1):
        m = re.match(r"\s*content-signal\s*:\s*(.+)", ligne, re.I)
        if not m:
            continue
        valeurs, alertes = {}, []
        for morceau in m.group(1).split("#")[0].split(","):
            if "=" not in morceau:
                continue
            k, v = (x.strip().lower() for x in morceau.split("=", 1))
            valeurs[k] = v
            if k not in CLES_CS | CLES_CS_EXPERIMENTALES:
                alertes.append(f"clé inconnue « {k} »")
            elif k in CLES_CS and v not in ("yes", "no"):
                alertes.append(f"valeur « {v} » pour {k} (yes ou no)")
        out.append({"ligne": n, "valeurs": valeurs, "alertes": alertes})
    return out


def lire_robots(base: str | None, fichier: str | None) -> tuple[str | None, int | None, str, str | None]:
    if fichier:
        return pg.lire_fichier(fichier), 200, fichier, None
    url = urljoin(base, "/robots.txt")
    r = pg.lire(url, accept="text/plain,*/*")
    return (r["texte"] if r["statut"] and r["statut"] < 400 else None), r["statut"], url, r["erreur"]


# ── analyse ──────────────────────────────────────────────────────────────────

def analyser(robots_txt, statut_robots, erreur_robots, html, entetes, url_page, statut_page=200, sondes=None):
    # le chemin avec sa requête : « Disallow: /*.pdf$ » bloque /guide.pdf mais pas /guide.pdf?v=2 (RFC 9309, Google)
    if url_page:
        u = urlsplit(url_page)
        chemin = (u.path or "/") + (f"?{u.query}" if u.query else "")
    else:
        chemin = "/"
    jetons = [(r["jeton"], r["editeur"], r["role"]) for r in ROBOTS]
    rr = robots_rfc.analyser(robots_txt, [chemin], jetons, statut_robots)
    acces = {b["robot"]: b["acces"][chemin] for b in rr["robots"]}
    groupe = {b["robot"]: b["groupe"] for b in rr["robots"]}

    if erreur_robots:
        etat_robots = f"NON LU (erreur réseau : {erreur_robots[:90]}) : la RFC 9309 dit « tout interdit » si les robots ont la même erreur ; à vérifier"
    elif statut_robots is None:
        etat_robots = "non lu"
    elif statut_robots >= 500:
        etat_robots = f"erreur serveur {statut_robots} : tout interdit pour les robots qui respectent la RFC 9309"
    elif statut_robots >= 400:
        etat_robots = f"absent ({statut_robots}) : tout permis"
    else:
        etat_robots = "lu"

    p = pg.analyser(html) if html is not None else None
    directives = pg.directives_robots(p, entetes) if p else None

    lignes = []
    for r in ROBOTS:
        a = acces[r["jeton"]]
        lignes.append({**r, "autorise": a["autorise"], "regle": a["regle"], "groupe": groupe[r["jeton"]],
                       "sonde": (sondes or {}).get(r["jeton"])})

    def ok(jeton):
        return acces[jeton]["autorise"]

    affirmations = []
    for a in TABLE["affirmations"]:
        robots_ok = all(ok(j) for j in a["robots"])
        verdict = "oui" if robots_ok else "non"
        detail = ", ".join(f"{j} {'autorisé' if ok(j) else 'BLOQUÉ'}" for j in a["robots"])
        if a["robots"] == ["Googlebot"] and p is not None:
            if directives["noindex"]:
                verdict, detail = "non", detail + f" ; noindex ({', '.join(directives['noindex'])})"
            elif directives["nosnippet"] or (directives["max_snippet"] is not None and directives["max_snippet"] == 0):
                verdict, detail = "non", detail + " ; extrait interdit (nosnippet ou max-snippet:0)"
            if verdict == "oui":
                verdict = "oui, si le site est inclus dans Search Console"
        sonde = [(sondes or {}).get(j) for j in a["robots"]]
        if any(s and s.get("refuse") for s in sonde):
            verdict, detail = "à vérifier", detail + " ; refusé à l'appel avec le user-agent du robot (pare-feu ?)"
        affirmations.append({"affirmation": a["affirmation"], "verdict": verdict, "detail": detail,
                             "pas": a.get("pas", "")})

    entrainement = {r["jeton"]: ok(r["jeton"]) for r in ROBOTS if r["role"] in ("entrainement", "jeton")
                    and r["jeton"] != "Applebot"}

    page = None
    if p is not None:
        page = {
            "statut": statut_page,
            "noindex": directives["noindex"], "nosnippet": directives["nosnippet"],
            "max_snippet": directives["max_snippet"], "data_nosnippet": p["data_nosnippet"],
            "mots_html": p["mots"], "canonical": p["canonical"], "title": p["title"],
        }
    return {
        "verifie_le": VERIFIE_LE, "url": url_page, "robots_txt": etat_robots, "chemin": chemin,
        "cloudflare": bloc_cloudflare(robots_txt or ""), "content_signal": content_signals(robots_txt or ""),
        "robots": lignes, "affirmations": affirmations, "entrainement": entrainement, "page": page,
    }


def sonder(url: str) -> dict:
    """Appelle la page avec un navigateur puis avec chaque robot de recherche ou utilisateur."""
    ref = pg.lire(url, ua=pg.UA_NAVIGATEUR)
    out = {"_navigateur": {"statut": ref["statut"], "erreur": ref["erreur"]}}
    for r in ROBOTS:
        if r["role"] not in ("recherche", "utilisateur", "moteur") or r["jeton"] in ("OAI-AdsBot",):
            continue
        ua = f"Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; {r['jeton']}/1.0)"
        x = pg.lire(url, ua=ua)
        if x["statut"] is None:  # erreur réseau : un second essai, puis « non lu », jamais « refusé »
            x = pg.lire(url, ua=ua)
        refuse = bool(ref["statut"] and ref["statut"] < 400 and x["statut"] is not None and x["statut"] >= 400)
        out[r["jeton"]] = {"statut": x["statut"], "erreur": x["erreur"], "refuse": refuse,
                           "non_lu": x["statut"] is None}
    return out


# ── propositions ─────────────────────────────────────────────────────────────

def proposer(strategie: str) -> str:
    lignes = [f"# Robots d'IA · stratégie « {strategie} » : {STRATEGIES[strategie]}",
              f"# Proposition Join Médicis du {VERIFIE_LE}. À relire avant de publier ; ne remplace pas les règles existantes.",
              "# Les robots de recherche et de visite restent autorisés : ils décident de la présence dans les réponses."]
    for r in ROBOTS:
        if r["role"] in ("moteur",):
            continue
        refuse = (strategie != "visibilite" and r["role"] == "entrainement") or \
                 (strategie == "refus-entrainement" and r["role"] == "jeton")
        lignes += ["", f"# {r['editeur']} · {r['produit']}", f"User-agent: {r['jeton']}",
                   "Disallow: /" if refuse else "Allow: /"]
    if strategie != "visibilite":
        lignes += ["", "# Préférence d'usage (Content Signals, respect volontaire, pas un contrôle d'accès)",
                   "Content-Signal: search=yes, ai-input=yes, ai-train=no"]
    return "\n".join(lignes)


# ── sortie ───────────────────────────────────────────────────────────────────

def afficher(r: dict) -> str:
    L = [f"ACCÈS DES IA · {r['url'] or 'fichiers locaux'} · robots.txt {r['robots_txt']} · table des robots du {r['verifie_le']}", ""]
    L.append("CE QUE ÇA VEUT DIRE")
    for a in r["affirmations"]:
        L.append(f"  {a['affirmation']:<48} {a['verdict'].upper():<10} {a['detail']}")
    if r["page"]:
        pgi = r["page"]
        L += ["", f"PAGE · statut {pgi['statut']} · {pgi['mots_html']} mots dans le HTML serveur · canonical {pgi['canonical'] or 'absent'}"]
        if pgi["noindex"]:
            L.append(f"  CRITIQUE  noindex : {', '.join(pgi['noindex'])}")
        if pgi["nosnippet"]:
            L.append(f"  CRITIQUE  nosnippet : {', '.join(pgi['nosnippet'])} (plus d'extrait, donc plus d'Aperçus IA ni de Mode IA)")
        if pgi["max_snippet"] is not None and 0 <= pgi["max_snippet"] < 50:
            L.append(f"  HAUTE     max-snippet:{pgi['max_snippet']} : extrait très court ou nul")
        if pgi["data_nosnippet"]:
            L.append(f"  INFO      {pgi['data_nosnippet']} élément(s) data-nosnippet exclus des extraits")
        if pgi["mots_html"] < 150:
            L.append("  HAUTE     peu de texte dans le HTML serveur : le contenu dépend peut-être de JavaScript")
    L += ["", f"{'ROBOT':<20}{'ÉDITEUR':<14}{'RÔLE':<14}{'ACCÈS':<10}{'RÈGLE':<36}SONDE"]
    for b in r["robots"]:
        s = b["sonde"]
        sonde = "" if not s else (f"{s['statut']}" + (" ! refusé au robot, pas au navigateur" if s["refuse"] else ""))
        L.append(f"{b['jeton']:<20}{b['editeur']:<14}{b['role']:<14}{'autorisé' if b['autorise'] else 'BLOQUÉ':<10}{b['regle'][:35]:<36}{sonde}")
    refuse = [j for j, v in r["entrainement"].items() if not v]
    L += ["", "ENTRAÎNEMENT · refusé pour : " + (", ".join(refuse) if refuse else "aucun (tout est autorisé)")]
    if r["cloudflare"]:
        L.append("CLOUDFLARE · bloc « Managed content » présent dans le robots.txt servi : il est ajouté par Cloudflare, "
                 "pas par le fichier du site. Vérifier le réglage dans Cloudflare (Security, Bots).")
    for cs in r["content_signal"]:
        val = ", ".join(f"{k}={v}" for k, v in cs["valeurs"].items())
        L.append(f"CONTENT-SIGNAL (ligne {cs['ligne']}) · {val}" + (f" · {'; '.join(cs['alertes'])}" if cs["alertes"] else "")
                 + " · préférence d'usage, respect volontaire")
    L += ["", "À VÉRIFIER HORS DU SITE · réglage « Contrôle de l'IA générative » de Search Console (Paramètres) : "
          "un site exclu n'apparaît pas dans les Aperçus IA ni le Mode IA, quoi que dise robots.txt."]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Accès des robots d'IA : robots.txt (RFC 9309), page, Cloudflare, Content-Signal.")
    ap.add_argument("url", nargs="?", help="URL de la page (le robots.txt est lu à la racine)")
    ap.add_argument("--robots", help="fichier robots.txt (hors ligne)")
    ap.add_argument("--html", help="fichier HTML de la page (hors ligne)")
    ap.add_argument("--entetes", help="fichier d'en-têtes HTTP « Nom: valeur » (hors ligne)")
    ap.add_argument("--sonder", action="store_true", help="appeler la page avec le user-agent de chaque robot")
    ap.add_argument("--proposer", choices=sorted(STRATEGIES), help="écrire un bloc robots.txt pour une stratégie")
    ap.add_argument("--llms", action="store_true", help="vérifier aussi /llms.txt (rapporté, sans poids)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.proposer and not a.url and not a.robots:
        print(proposer(a.proposer))
        return 0
    if not a.url and not (a.robots or a.html):
        ap.error("donne une URL, ou --robots / --html pour travailler hors ligne")
    url = a.url
    if url and not re.match(r"https?://", url):
        print("Erreur : l'URL commence par http:// ou https://", file=sys.stderr)
        return 1
    base = f"{urlsplit(url).scheme}://{urlsplit(url).netloc}/" if url else None

    robots_txt, statut_r, _, err_r = lire_robots(base, a.robots) if (a.robots or base) else (None, 404, "", None)
    html, entetes, statut_p = None, {}, None
    if a.html:
        html, statut_p = pg.lire_fichier(a.html), 200
    elif url:
        rp = pg.lire(url)
        if rp["erreur"]:
            print(f"Page non lue : {rp['erreur']}. Donne le HTML avec --html pour l'analyser hors ligne.", file=sys.stderr)
        else:
            html, entetes, statut_p = rp["texte"], rp["entetes"], rp["statut"]
    if a.entetes:
        for ligne in pg.lire_fichier(a.entetes).splitlines():
            if ":" in ligne:
                k, v = ligne.split(":", 1)
                entetes[k.strip().lower()] = v.strip()
    sondes = sonder(url) if (a.sonder and url) else None

    r = analyser(robots_txt, statut_r, err_r, html, entetes, url or "/", statut_p, sondes)
    if a.llms and base:
        l = pg.lire(urljoin(base, "/llms.txt"), accept="text/plain,*/*")
        r["llms_txt"] = {"statut": l["statut"], "erreur": l["erreur"],
                         "note": "rapporté sans poids : Google Search ne l'utilise pas (guide du 10 juil. 2026) ; "
                                 "utile surtout pour une documentation lue par des agents de code"}
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(afficher(r))
        if "llms_txt" in r:
            print(f"LLMS.TXT · statut {r['llms_txt']['statut']} · {r['llms_txt']['note']}")
        if a.proposer:
            print("\n" + proposer(a.proposer))
    return 0


if __name__ == "__main__":
    sys.exit(main())
