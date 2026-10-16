#!/usr/bin/env python3
"""banc_robots.py : 9 robots.txt pièges, 7 outils, la même question à chacun.

Pour chaque cas, un site local (serveur.py) sert le robots.txt du cas ;
chaque outil lit la même URL et dit, robot par robot, si la page est
lisible. La vérité vient de la RFC 9309 et des pages des éditeurs
(cas_robots.json). Sorties brutes dans sorties/robots/, tableau en
Markdown sur la sortie standard.

  python3 banc_robots.py --depots <dossier des clones> [--venv <bin d'un venv avec requests>]

Outils : Join Médicis (acces.py), geo-optimizer (geo audit), ultimate-seo-geo
(robots_checker.py), elmo (check_ai_access.py), geo-score (geo_score.py),
geo-seo-claude (fetch_robots_txt), gtm-engineer-skills (aeo-audit.mjs).
claude-seo n'a pas de verdict par robot (son agentic_check.py contrôle
seulement que robots.txt répond) : il n'est pas dans ce banc.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
sys.path.insert(0, str(ICI))
from serveur import Sites  # noqa: E402

ROBOTS = ["OAI-SearchBot", "GPTBot", "PerplexityBot", "Claude-SearchBot"]
OUTILS = ["Join Médicis", "geo-optimizer", "ultimate-seo-geo", "elmo", "geo-score", "geo-seo-claude", "gtm-engineer-skills"]


def lancer(cmd, timeout=240):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired:
        return "", "délai dépassé", -1


def json_de(sortie):
    i = min([x for x in (sortie.find("{"), sortie.find("[")) if x >= 0], default=-1)
    if i < 0:
        return None
    try:
        return json.loads(sortie[i:])
    except ValueError:
        return None


# ---------------------------------------------------------------- adaptateurs : sortie -> {robot: verdict}

def ad_nous(d):
    if not d:
        return {}
    if d["robots_txt"].startswith("NON LU") or d["robots_txt"] == "non lu":
        return {r: "non lu" for r in ROBOTS}
    par = {r["jeton"]: r for r in d["robots"]}
    return {r: ("autorisé" if par[r]["autorise"] else "bloqué") for r in ROBOTS if r in par}


def ad_geo_optimizer(d):
    if not d or d.get("error"):
        return {}
    det = d["checks"]["robots_txt"]["details"]
    out = {}
    for r in ROBOTS:
        if r in det.get("bots_blocked", []):
            out[r] = "bloqué"
        elif r in det.get("bots_partial", []):
            out[r] = "partiel"
        elif r in det.get("bots_allowed", []):
            out[r] = "autorisé"
        elif r in det.get("bots_missing", []):
            out[r] = "autorisé" if not det.get("found") else "non mentionné"
    if not det.get("found"):  # « No robots.txt » : l'outil le lit comme absent, donc tout permis
        out = {r: out.get(r, "autorisé (lu comme absent)") for r in ROBOTS}
    return out


def ad_ultimate(d):
    if not d:
        return {}
    st = d.get("ai_crawler_status") or {}
    out = {}
    for r in ROBOTS:
        v = str(st.get(r, "")).lower()
        if not v:
            continue
        if "partial" in v:
            out[r] = "partiel"
        elif "inherits" in v:
            out[r] = "renvoie à *"
        elif "block" in v or "disallow" in v:
            out[r] = "bloqué"
        elif "allow" in v or "not mentioned" in v or "no robots" in v or "not found" in v:
            out[r] = "autorisé"
        else:
            out[r] = v[:30]
    return out


def ad_elmo(d):
    if not d:
        return {}
    page = d[0] if isinstance(d, list) else d
    out = {}
    for c in page.get("crawlers", []):
        if c["crawler"] in ROBOTS:
            out[c["crawler"]] = "autorisé" if c["robots"] else "bloqué"
    return out


def ad_geo_score(d):
    if not d:
        return {}
    rp = (d.get("access") or {}).get("robots_paths") or {}
    if rp.get("robots_txt") not in ("read", None) and not rp.get("pages"):
        etat = rp.get("robots_txt")
        v = "autorisé (absent)" if etat == "absent" else ("non lu" if etat == "unreadable" else f"robots.txt {etat}")
        return {r: v for r in ROBOTS if r not in ("GPTBot",)}
    bloques = {c for p in rp.get("pages", []) for rule in p.get("rules", []) for c in rule.get("crawlers", [])}
    # GPTBot n'est pas noté par geo-score (robot d'entraînement) : non évalué
    return {r: ("bloqué" if r in bloques else "autorisé") for r in ROBOTS if r != "GPTBot"}


def ad_geo_seo_claude(d):
    if not d:
        return {}
    st = d.get("ai_crawler_status", {})
    out = {}
    for r in ROBOTS:
        v = st.get(r)
        if v is None:
            continue
        out[r] = {"BLOCKED": "bloqué", "BLOCKED_BY_WILDCARD": "bloqué", "PARTIALLY_BLOCKED": "partiel",
                  "ALLOWED": "autorisé", "ALLOWED_BY_DEFAULT": "autorisé", "NOT_MENTIONED": "autorisé",
                  "NO_ROBOTS_TXT": "autorisé"}.get(v, v)
    if not st and d.get("errors"):  # statut inattendu ou erreur réseau : pas de verdict, l'erreur est dite
        out = {r: "non lu" for r in ROBOTS if r != "Claude-SearchBot"}
    return out


def ad_gtm(d):
    if not d:
        return {}
    rb = d.get("robots") or {}
    bloques = {b.lower() for b in rb.get("aiBotBlocked", [])}
    suivis = {"oai-searchbot", "gptbot", "perplexitybot"}  # sa liste ne contient pas Claude-SearchBot
    return {r: ("bloqué" if r.lower() in bloques else "autorisé") for r in ROBOTS if r.lower() in suivis}


def commandes(outil, url, depots, venv):
    py = f"{venv}/python" if venv else sys.executable
    if outil == "Join Médicis":
        return [sys.executable, str(PACK / "skills/geo-acces/scripts/acces.py"), url, "--json"]
    if outil == "geo-optimizer":
        return [py, str(ICI / "lanceur.py"), "geo-optimizer", f"{depots}/geo-optimizer-skill", "--", "audit", "--url", url, "--format", "json"]
    if outil == "ultimate-seo-geo":
        return [py, str(ICI / "lanceur.py"), "ultimate", f"{depots}/ultimate-seo-geo", "robots_checker.py", "--", "--json", url]
    if outil == "elmo":
        return [sys.executable, f"{depots}/elmo/skills/aeo/scripts/check_ai_access.py", "--json", url]
    if outil == "geo-score":
        return [sys.executable, f"{depots}/geo-score/cli/geo_score.py", "--json", url]
    if outil == "geo-seo-claude":
        code = (f"import sys, json; sys.path.insert(0, {repr(depots + '/geo-seo-claude/scripts')}); "
                f"from fetch_page import fetch_robots_txt; print(json.dumps(fetch_robots_txt({url!r})))")
        return [py, "-c", code]
    if outil == "gtm-engineer-skills":
        return ["node", f"{depots}/gtm-engineer-skills/audit-website-aeo/scripts/aeo-audit.mjs", url, "--json", "--max-pages=1"]


ADAPT = {"Join Médicis": ad_nous, "geo-optimizer": ad_geo_optimizer, "ultimate-seo-geo": ad_ultimate, "elmo": ad_elmo,
         "geo-score": ad_geo_score, "geo-seo-claude": ad_geo_seo_claude, "gtm-engineer-skills": ad_gtm}


SANS_VERDICT = ("partiel", "renvoie à *", "non mentionné")


def juste(verite, v):
    """True juste, False faux, None sans verdict (réponse partielle ou renvoi à une autre règle)."""
    if v is None or v in SANS_VERDICT:
        return None
    if verite is None:
        return v in ("non lu", "bloqué")
    return v.startswith("autorisé") if verite else (v == "bloqué")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--depots", required=True)
    ap.add_argument("--venv")
    ap.add_argument("--outils", default=",".join(OUTILS))
    a = ap.parse_args(argv)
    d = json.loads((ICI / "cas_robots.json").read_text(encoding="utf-8"))
    cas = d["cas"]
    for c in cas:
        c["pages"] = {"/": {"html": d["page_ok"]}, c["chemin"].split("?")[0]: {"html": d["page_ok"]}}
    sites = Sites(cas)
    sorties = ICI / "sorties" / "robots"
    sorties.mkdir(parents=True, exist_ok=True)
    res = {}
    for c in cas:
        url = sites.url(c["id"]) + c["chemin"]
        for o in a.outils.split(","):
            out, err, code = lancer(commandes(o, url, a.depots, a.venv))
            (sorties / f"{c['id']}-{re.sub(r'[^a-z0-9]+', '-', o.lower())}.txt").write_text(
                re.sub(r"127\.0\.0\.1:\d+", "site-de-test", out + "\n--- stderr ---\n" + err[-3000:]), encoding="utf-8")
            res[(c["id"], o)] = ADAPT[o](json_de(out))
        print(f"{c['id']} fait", file=sys.stderr)
    sites.arreter()
    outils = a.outils.split(",")
    L = []
    bilan = {o: [0, 0, 0] for o in outils}  # justes, répondus, total
    for c in cas:
        L += [f"#### {c['id']} · {c['titre']}", "", f"Piège : {c['piege']}. Page : `{c['chemin']}`.", "",
              "| Robot | Vérité | " + " | ".join(outils) + " |", "|---|---|" + "---|" * len(outils)]
        for r in ROBOTS:
            v = c["verite"][r]
            vt = "non lu ou bloqué" if v is None else ("autorisé" if v else "bloqué")
            cell = []
            for o in outils:
                x = res[(c["id"], o)].get(r)
                j = juste(v, x)
                bilan[o][2] += 1
                if j is not None:
                    bilan[o][1] += 1
                    bilan[o][0] += bool(j)
                cell.append("—" if not x else (f"· {x}" if j is None else (f"✅ {x}" if j else f"❌ {x}")))
            L.append(f"| {r} | {vt} | " + " | ".join(cell) + " |")
        L.append("")
    tete = ["| Outil | Justes | Faux | Sans verdict |", "|---|---|---|---|"]
    for o in outils:
        j, rep, tot = bilan[o]
        tete.append(f"| {o} | {j}/{tot} | {rep - j} | {tot - rep} |")
    print("\n".join(tete + [""] + L))
    (ICI / "sorties" / "robots.json").write_text(json.dumps(
        {f"{k[0]}|{k[1]}": v for k, v in res.items()}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
