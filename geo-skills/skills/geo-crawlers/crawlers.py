#!/usr/bin/env python3
"""
crawlers.py - les robots d'IA peuvent-ils lire votre site ?

Vérifie :
  - robots.txt : chaque robot d'IA connu est-il autorisé ou bloqué sur la page
    d'accueil et sur les chemins demandés (--chemin /blog/) ;
  - les directives noai / noimageai / noindex (meta robots et en-tête
    X-Robots-Tag) de la page ;
  - llms.txt : présent ? bien formé (titre, résumé, sections de liens) ?
  - le contenu est-il dans le HTML (lisible sans JavaScript) ?

Génère sur demande un bloc robots.txt selon la stratégie choisie et un
brouillon de llms.txt à partir du sitemap.

    python3 crawlers.py https://www.site.fr
    python3 crawlers.py https://www.site.fr --chemin /blog/ --chemin /produits/
    python3 crawlers.py https://www.site.fr --robots-propose visibilite
    python3 crawlers.py https://www.site.fr --llms-propose --nom "Assurly" --resume "Courtier en assurance santé internationale."

La liste des robots évolue vite : vérifiez la documentation de chaque éditeur
avant de modifier un robots.txt en production. Inspiré de geo-crawlers et
geo-llmstxt (geo-seo-claude, MIT).
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser

UA = "Mozilla/5.0 (compatible; JoinMedicis-crawlers/1.0; +https://joinmedicis.com)"

# nom, éditeur, rôle ; rôle : recherche (réponses en direct), utilisateur (lecture à la demande),
# entraînement (collecte pour entraîner les modèles).
BOTS = [
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
    ("meta-externalagent", "Meta", "entraînement"),
    ("Amazonbot", "Amazon", "recherche"),
    ("DuckAssistBot", "DuckDuckGo", "recherche"),
    ("CCBot", "Common Crawl", "entraînement"),
    ("Bytespider", "ByteDance", "entraînement"),
]
SEARCH_ENGINES = [("Googlebot", "Google (recherche et AI Overviews)"), ("Bingbot", "Bing (Copilot, et ChatGPT en partie)")]


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr-FR,fr;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read().decode(r.headers.get_content_charset() or "utf-8", errors="replace")
        return r.status, dict(r.headers), body, r.geturl()


def try_fetch(url):
    try:
        return fetch(url)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), "", url
    except Exception as e:  # noqa: BLE001
        return None, {}, str(e), url


def robots_rules(base, robots_txt, chemins):
    rp = RobotFileParser()
    rp.parse(robots_txt.splitlines())
    groups = {m.lower() for m in re.findall(r"(?im)^\s*user-agent\s*:\s*(\S+)", robots_txt)}
    out = []
    for name, owner, role in BOTS:
        res = {"robot": name, "editeur": owner, "role": role,
               "cite": name.lower() in groups, "acces": {}}
        for c in chemins:
            res["acces"][c] = rp.can_fetch(name, urljoin(base, c))
        out.append(res)
    se = [{"robot": n, "editeur": o, "acces": {c: rp.can_fetch(n, urljoin(base, c)) for c in chemins}}
          for n, o in SEARCH_ENGINES]
    return out, se


def check_llms(text):
    """Contrôle le format llms.txt : # Titre, > résumé, sections ## avec des liens Markdown."""
    issues = []
    if not re.search(r"(?m)^# \S", text):
        issues.append("pas de titre « # Nom du site » en première ligne")
    if not re.search(r"(?m)^> \S", text):
        issues.append("pas de résumé en citation « > … »")
    sections = re.findall(r"(?m)^## (.+)$", text)
    links = re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", text)
    if not sections:
        issues.append("aucune section « ## »")
    if not links:
        issues.append("aucun lien Markdown [titre](url)")
    return {"sections": sections, "liens": len(links), "problemes": issues}


def page_signals(headers, body):
    meta = re.findall(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']+)', body, re.I)
    xrt = headers.get("X-Robots-Tag") or headers.get("x-robots-tag") or ""
    directives = ",".join(meta + [xrt]).lower()
    text = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", body)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    words = len(re.findall(r"\w+", text))
    return {"noindex": "noindex" in directives, "noai": "noai" in directives, "noimageai": "noimageai" in directives,
            "directives": directives.strip(","), "mots_dans_html": words}


def propose_robots(strategie):
    lines = ["# --- Robots d'IA (stratégie : %s) ---" % strategie]
    for name, owner, role in BOTS:
        bloque = strategie == "blocage" or (strategie == "equilibre" and role == "entraînement")
        lines += [f"User-agent: {name}", "Disallow: /" if bloque else "Allow: /", ""]
    return "\n".join(lines)


def propose_llms(base, nom, resume, urls):
    groups = {}
    for u in urls:
        seg = (urlsplit(u).path.strip("/").split("/") or [""])[0] or "Accueil"
        groups.setdefault(seg, []).append(u)
    out = [f"# {nom}", "", f"> {resume}", ""]
    for seg, us in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:8]:
        out.append(f"## {seg.replace('-', ' ').capitalize()}")
        for u in us[:10]:
            slug = urlsplit(u).path.strip("/").split("/")[-1] or nom
            out.append(f"- [{slug.replace('-', ' ').capitalize()}]({u}): {{{{description en une phrase}}}}")
        out.append("")
    return "\n".join(out)


def sitemap_urls(base):
    status, _, xml, _ = try_fetch(urljoin(base, "/sitemap.xml"))
    if status != 200:
        return []
    locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", xml, re.S)
    if "<sitemapindex" in xml and locs:
        st, _, sub, _ = try_fetch(locs[0])
        locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", sub, re.S) if st == 200 else []
    return locs[:200]


def analyse(url, chemins):
    parts = urlsplit(url if "://" in url else "https://" + url)
    base = f"{parts.scheme}://{parts.netloc}"
    chemins = chemins or ["/"]
    if parts.path not in ("", "/") and parts.path not in chemins:
        chemins.append(parts.path)
    st_r, _, robots_txt, _ = try_fetch(base + "/robots.txt")
    bots, se = robots_rules(base, robots_txt if st_r == 200 else "", chemins)
    st_l, _, llms_txt, _ = try_fetch(base + "/llms.txt")
    st_p, headers, body, final = try_fetch(url if "://" in url else base + "/")
    return {
        "site": base,
        "robots_txt": "présent" if st_r == 200 else f"absent ({st_r})",
        "robots_ia": bots,
        "moteurs": se,
        "llms_txt": check_llms(llms_txt) if st_l == 200 and llms_txt.strip() else None,
        "page": page_signals(headers, body) if st_p == 200 else {"erreur": str(st_p)},
    }


def render(r):
    print(f"ROBOTS D'IA · {r['site']} · robots.txt {r['robots_txt']}")
    for s in r["moteurs"]:
        ok = all(s["acces"].values())
        print(f"  {'OK ' if ok else 'BLOQUÉ'} {s['robot']:<20} {s['editeur']}")
    print()
    for b in r["robots_ia"]:
        acc = b["acces"]
        etat = "autorisé" if all(acc.values()) else ("bloqué" if not any(acc.values()) else "partiel")
        detail = " ".join(f"{c}:{'oui' if v else 'non'}" for c, v in acc.items()) if etat == "partiel" else ""
        cite = "" if b["cite"] else " (non cité, règle * appliquée)"
        print(f"  {etat:<9} {b['robot']:<20} {b['editeur']:<16} {b['role']:<12}{cite} {detail}")
    print()
    if r["llms_txt"] is None:
        print("llms.txt : absent (facultatif ; utile pour guider les assistants vers vos pages clés)")
    else:
        l = r["llms_txt"]
        print(f"llms.txt : présent · {len(l['sections'])} section(s) · {l['liens']} lien(s)")
        for p in l["problemes"]:
            print(f"  - {p}")
    p = r["page"]
    if "erreur" in p:
        print(f"Page : illisible ({p['erreur']})")
    else:
        flags = [k for k in ("noindex", "noai", "noimageai") if p[k]]
        print(f"Page : directives {', '.join(flags) or 'aucune restriction'} · {p['mots_dans_html']} mots lisibles sans JavaScript")
        if p["mots_dans_html"] < 150:
            print("  -> Peu de texte dans le HTML : le contenu est peut-être rendu en JavaScript, que la plupart des robots d'IA n'exécutent pas.")


def main():
    ap = argparse.ArgumentParser(description="Accès des robots d'IA, llms.txt et directives d'une page.")
    ap.add_argument("url")
    ap.add_argument("--chemin", action="append", default=[], help="chemin à tester (répétable), défaut /")
    ap.add_argument("--robots-propose", choices=["visibilite", "equilibre", "blocage"],
                    help="visibilité : tout autoriser ; équilibre : bloquer l'entraînement, autoriser recherche et utilisateurs ; blocage : tout bloquer")
    ap.add_argument("--llms-propose", action="store_true", help="brouillon de llms.txt depuis le sitemap")
    ap.add_argument("--nom", default="Nom du site")
    ap.add_argument("--resume", default="{{résumé du site en une phrase}}")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    r = analyse(args.url, args.chemin)
    if args.json:
        json.dump(r, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        render(r)
    if args.robots_propose:
        print("\n" + propose_robots(args.robots_propose))
    if args.llms_propose:
        print("\n" + propose_llms(r["site"], args.nom, args.resume, sitemap_urls(r["site"])))


if __name__ == "__main__":
    main()
