#!/usr/bin/env python3
"""robots.py : ce que robots.txt autorise vraiment, robot par robot (RFC 9309).

Le module robotparser de Python applique la première règle qui correspond et
ignore les jokers : sur « Disallow: / » suivi de « Allow: /blog/ », il bloque
/blog/ alors que Google l'autorise. Ce script suit la RFC 9309 (septembre
2022), que Google applique :

- groupe choisi par robot : celui dont la ligne user-agent correspond à son
  jeton (sans tenir compte de la casse), sinon le groupe « * », sinon tout
  est permis ; plusieurs groupes pour le même robot sont fusionnés ;
- règle la plus longue qui correspond (en caractères) ; à égalité, Allow
  l'emporte ;
- jokers « * » et ancre de fin « $ » ;
- robots.txt absent (4xx) : tout est permis ; erreur serveur (5xx) ou
  injoignable : tout est interdit, par prudence (RFC 9309 §2.3.1.4).

    python3 robots.py https://www.site.fr --chemin / --chemin /blog/ --chemin /devis/
    python3 robots.py robots.txt --chemin /blog/guide/ --robot Googlebot --robot GPTBot
    python3 robots.py robots.txt --json

Chaque conclusion porte sur un robot et un chemin nommés. La liste des robots
d'IA vient du pack GEO (geo-acces) : vérifiez la documentation de chaque
éditeur avant de modifier un robots.txt en production.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlsplit

UA = "Mozilla/5.0 (compatible; JoinMedicis-robots/1.0; +https://joinmedicis.com)"

# jeton, éditeur, rôle (recherche = réponses en direct ; utilisateur = lecture à la demande ;
# entraînement = collecte pour entraîner les modèles ; moteur = index de recherche classique).
ROBOTS = [
    ("Googlebot", "Google", "moteur"),
    ("Bingbot", "Microsoft", "moteur"),
    ("OAI-SearchBot", "OpenAI", "recherche"),
    ("ChatGPT-User", "OpenAI", "utilisateur"),
    ("GPTBot", "OpenAI", "entraînement"),
    ("Claude-SearchBot", "Anthropic", "recherche"),
    ("Claude-User", "Anthropic", "utilisateur"),
    ("ClaudeBot", "Anthropic", "entraînement"),
    ("PerplexityBot", "Perplexity", "recherche"),
    ("Perplexity-User", "Perplexity", "utilisateur"),
    ("Google-Extended", "Google (Gemini)", "entraînement"),
    ("Applebot-Extended", "Apple", "entraînement"),
    ("MistralAI-User", "Mistral", "utilisateur"),
    ("CCBot", "Common Crawl", "entraînement"),
]


class Erreur(Exception):
    pass


def lire_groupes(texte: str) -> list[dict]:
    """Groupes du fichier : {agents: [...], regles: [(allow, motif, ligne)]}."""
    groupes, courant, dernier_agent = [], None, False
    for n, brute in enumerate(texte.splitlines(), 1):
        ligne = brute.split("#", 1)[0].strip()
        if ":" not in ligne:
            continue
        cle, val = (x.strip() for x in ligne.split(":", 1))
        cle = cle.lower()
        if cle == "user-agent":
            # Des lignes user-agent consécutives ouvrent un même groupe.
            if courant is None or not dernier_agent:
                courant = {"agents": [], "regles": []}
                groupes.append(courant)
            courant["agents"].append(val.lower())
            dernier_agent = True
        elif cle in ("allow", "disallow"):
            dernier_agent = False
            if courant is None:
                continue  # règle hors groupe : ignorée (RFC 9309 §2.1)
            if cle == "disallow" and val == "":
                continue  # « Disallow: » vide n'interdit rien
            courant["regles"].append((cle == "allow", val, n))
        else:
            dernier_agent = False  # sitemap, crawl-delay… : ne ferment pas le groupe pour la RFC, mais séparent les agents
    return groupes


def groupe_pour(groupes: list[dict], robot: str) -> tuple[list, str]:
    """Règles qui s'appliquent au robot, et le groupe retenu ('jeton', '*' ou 'aucun')."""
    r = robot.lower()
    propres = [g for g in groupes if r in g["agents"]]
    if propres:
        return [x for g in propres for x in g["regles"]], robot
    etoile = [g for g in groupes if "*" in g["agents"]]
    if etoile:
        return [x for g in etoile for x in g["regles"]], "*"
    return [], "aucun"


def motif_regex(motif: str) -> re.Pattern:
    fin = motif.endswith("$")
    corps = motif[:-1] if fin else motif
    rx = "".join(".*" if c == "*" else re.escape(c) for c in corps)
    return re.compile("^" + rx + ("$" if fin else ""))


def decision(regles: list, chemin: str) -> tuple[bool, tuple | None]:
    """(autorisé, règle retenue). Règle la plus longue ; à égalité, Allow."""
    meilleure = None
    for allow, motif, ligne in regles:
        if motif_regex(motif).match(chemin):
            cle = (len(motif), allow)
            if meilleure is None or cle > meilleure[0]:
                meilleure = (cle, (allow, motif, ligne))
    if meilleure is None:
        return True, None
    return meilleure[1][0], meilleure[1]


def analyser(texte: str | None, chemins: list[str], robots: list[tuple], statut: int | None = 200) -> dict:
    if statut is None or statut >= 500:
        mode = "tout interdit (robots.txt en erreur serveur ou injoignable)"
        groupes = None
    elif statut >= 400:
        mode = "tout permis (robots.txt absent)"
        groupes = []
    else:
        mode = "lu"
        groupes = lire_groupes(texte or "")
    res = []
    for jeton, editeur, role in robots:
        ligne = {"robot": jeton, "editeur": editeur, "role": role, "acces": {}}
        if groupes is None:
            ligne["groupe"] = "aucun"
            ligne["acces"] = {c: {"autorise": False, "regle": "robots.txt indisponible"} for c in chemins}
        else:
            regles, g = groupe_pour(groupes, jeton)
            ligne["groupe"] = g
            for c in chemins:
                ok, r = decision(regles, c)
                ligne["acces"][c] = {"autorise": ok,
                                     "regle": f"{'Allow' if r[0] else 'Disallow'}: {r[1]} (ligne {r[2]})" if r else "aucune règle"}
        res.append(ligne)
    return {"mode": mode, "chemins": chemins, "robots": res}


def lire_source(source: str) -> tuple[str | None, int | None, str]:
    if re.match(r"https?://", source):
        p = urlsplit(source)
        url = source if p.path.endswith("robots.txt") else urljoin(f"{p.scheme}://{p.netloc}/", "/robots.txt")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode("utf-8", errors="replace"), r.status, url
        except urllib.error.HTTPError as e:
            return None, e.code, url
        except Exception:  # noqa: BLE001
            return None, None, url
    try:
        with open(source, encoding="utf-8") as f:
            return f.read(), 200, source
    except OSError as exc:
        raise Erreur(f"fichier illisible : {source} ({exc})") from exc


def afficher(r: dict, source: str) -> str:
    lignes = [f"ROBOTS.TXT · {source} · {r['mode']}"]
    largeur = max(len(c) for c in r["chemins"])
    for b in r["robots"]:
        tete = f"  {b['robot']:<18} {b['role']:<12} groupe {b['groupe']:<18}"
        for i, c in enumerate(r["chemins"]):
            a = b["acces"][c]
            etat = "autorisé" if a["autorise"] else "BLOQUÉ"
            prefixe = tete if i == 0 else " " * len(tete)
            lignes.append(f"{prefixe} {c:<{largeur}}  {etat:<9} {a['regle']}")
    bloques = [b["robot"] for b in r["robots"] if b["role"] == "moteur" and not all(a["autorise"] for a in b["acces"].values())]
    if bloques:
        lignes.append(f"ALERTE · moteur de recherche bloqué sur au moins un chemin : {', '.join(bloques)}")
    return "\n".join(lignes)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Accès par robot selon robots.txt, règles de la RFC 9309.")
    ap.add_argument("source", help="URL du site (ou de son robots.txt) ou fichier robots.txt")
    ap.add_argument("--chemin", action="append", help="chemin à tester (répéter) ; défaut : /")
    ap.add_argument("--robot", action="append", help="jeton de robot à tester (répéter) ; défaut : la liste connue")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    chemins = a.chemin or ["/"]
    for c in chemins:
        if not c.startswith("/"):
            print(f"Erreur : un chemin commence par « / » ({c})", file=sys.stderr)
            return 1
    robots = ROBOTS if not a.robot else [next((x for x in ROBOTS if x[0].lower() == j.lower()), (j, "?", "?")) for j in a.robot]
    try:
        texte, statut, source = lire_source(a.source)
    except Erreur as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    r = analyser(texte, chemins, robots, statut)
    r["source"] = source
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r, source))
    return 0


if __name__ == "__main__":
    sys.exit(main())
