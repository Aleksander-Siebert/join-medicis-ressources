#!/usr/bin/env python3
"""
drift.py - surveiller les régressions SEO d'un site, page par page.

Prend une « photo » des éléments SEO critiques d'une page (code HTTP,
redirection, title, meta description, canonical, robots, H1, H2, données
structurées, hreflang, langue, Open Graph, nombre de mots, liens internes,
images sans alt, empreinte du texte), puis compare une nouvelle photo à la
précédente avec des règles classées CRITIQUE, À SURVEILLER et INFO.

    python3 drift.py photo https://www.site.fr/ https://www.site.fr/guide/
    python3 drift.py photo --sitemap https://www.site.fr/sitemap.xml --max 50
    python3 drift.py comparer https://www.site.fr/guide/
    python3 drift.py comparer --tout               # toutes les pages photographiées
    python3 drift.py historique https://www.site.fr/guide/

Les photos sont des fichiers JSON dans ~/.claude/seo/drift/ (--dossier pour
changer). Rien n'est envoyé ailleurs. Le cas d'usage : une photo avant une
mise en ligne ou une refonte, une comparaison juste après.

Adapté de seo-drift (claude-seo, MIT ; auteur d'origine Dan Colta), réécrit
sans base SQLite ni dépendance.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ICI = os.path.dirname(os.path.abspath(__file__))
for d in (os.path.join(ICI, "..", "seo-audit"), os.path.join(ICI, "..", "..", "seo-audit")):
    if os.path.exists(os.path.join(d, "onpage.py")):
        sys.path.insert(0, d)
import onpage  # noqa: E402

UA = "Mozilla/5.0 (compatible; JoinMedicis-drift/1.0; +https://joinmedicis.com)"
DOSSIER = os.path.expanduser("~/.claude/seo/drift")
GRAVITES = ("CRITIQUE", "À SURVEILLER", "INFO")


def normaliser(url):
    """Même page, même clé : hôte en minuscules, sans port par défaut, sans utm_*, sans / final."""
    s = urlsplit(url.strip())
    host = (s.hostname or "").lower()
    if s.port and s.port not in (80, 443):
        host += f":{s.port}"
    q = urlencode(sorted((k, v) for k, v in parse_qsl(s.query) if not k.lower().startswith("utm_")))
    path = s.path.rstrip("/") or "/"
    return urlunsplit((s.scheme.lower() or "https", host, path, q, ""))


def fichier(dossier, url):
    cle = re.sub(r"[^a-z0-9]+", "-", normaliser(url).split("://", 1)[-1].lower()).strip("-")[:120]
    return os.path.join(dossier, cle + ".json")


def telecharger(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr-FR,fr;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read().decode(r.headers.get_content_charset() or "utf-8", errors="replace")
            return r.status, r.geturl(), dict(r.headers), body
    except urllib.error.HTTPError as e:
        return e.code, url, dict(e.headers or {}), ""


def photo(url, status, url_finale, headers, html):
    p = onpage.P(url_finale or url)
    p.feed(html)
    meta = p.meta
    rel = lambda r: [l for l in p.links_rel if r in (l.get("rel") or "").lower().split()]  # noqa: E731
    canonical = (rel("canonical") or [{}])[0].get("href", "")
    robots = ",".join(x for x in (meta.get("robots", ""), headers.get("X-Robots-Tag") or headers.get("x-robots-tag") or "") if x).lower()
    texte = re.sub(r"\s+", " ", " ".join(p.text)).strip()
    hote = urlsplit(url_finale or url).hostname
    internes = [a for a in p.anchors if urlsplit(a["href"]).hostname == hote]
    types = onpage.schema_types(p.jsonld)
    return {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "url": url,
        "statut": status,
        "url_finale": normaliser(url_finale) if url_finale else normaliser(url),
        "title": p.title,
        "description": meta.get("description", ""),
        "canonical": canonical,
        "robots": robots,
        "h1": [t for n, t in p.headings if n == 1],
        "h2": [t for n, t in p.headings if n == 2],
        "schema": types,
        "hreflang": sorted(f"{l.get('hreflang')}={l.get('href')}" for l in rel("alternate") if l.get("hreflang")),
        "lang": p.lang,
        "og": {k: meta.get(k, "") for k in ("og:title", "og:description", "og:image")},
        "mots": len(re.findall(r"\w+", texte)),
        "liens_internes": len(internes),
        "images_sans_alt": sum(1 for i in p.imgs if "alt" not in i),
        "empreinte_texte": hashlib.sha256(texte.encode()).hexdigest()[:16],
        "empreinte_schema": hashlib.sha256("".join(p.jsonld).encode()).hexdigest()[:16],
    }


def comparer(avant, apres):
    """Applique les règles. Renvoie une liste de {gravite, regle, avant, apres, action}."""
    out = []

    def r(gravite, regle, a, b, action):
        out.append({"gravite": gravite, "regle": regle, "avant": a, "apres": b, "action": action})

    a, b = avant, apres
    # CRITIQUE
    if a["statut"] < 400 <= b["statut"]:
        r("CRITIQUE", "La page répond en erreur", a["statut"], b["statut"], "Rétablir la page ou rediriger en 301 vers son équivalent.")
    if a["url_finale"] != b["url_finale"] and b["statut"] < 400:
        r("CRITIQUE", "Nouvelle redirection", a["url_finale"], b["url_finale"], "Vérifier que la redirection est voulue et en 301.")
    if "noindex" in b["robots"] and "noindex" not in a["robots"]:
        r("CRITIQUE", "noindex ajouté", a["robots"] or "(aucun)", b["robots"], "Retirer le noindex si la page doit rester dans Google.")
    if re.search(r"nosnippet|max-snippet\s*:\s*0\b", b["robots"]) and not re.search(r"nosnippet|max-snippet\s*:\s*0\b", a["robots"]):
        r("CRITIQUE", "nosnippet ajouté", a["robots"] or "(aucun)", b["robots"], "Sans extrait, la page sort aussi d'AI Overviews et d'AI Mode.")
    if a["canonical"] and b["canonical"] and normaliser(a["canonical"]) != normaliser(b["canonical"]):
        r("CRITIQUE", "Canonical modifié", a["canonical"], b["canonical"], "Un canonical vers une autre URL retire cette page de l'index.")
    if a["title"] and not b["title"]:
        r("CRITIQUE", "Title supprimé", a["title"], "", "Remettre le title.")
    if a["h1"] and not b["h1"]:
        r("CRITIQUE", "H1 supprimé", " | ".join(a["h1"]), "", "Remettre un H1.")
    if a["mots"] >= 150 and b["mots"] < a["mots"] * 0.5:
        r("CRITIQUE", "Contenu divisé par deux ou plus", a["mots"], b["mots"], "Contenu supprimé ou rendu en JavaScript : vérifier le HTML livré.")
    # À SURVEILLER
    if a["canonical"] and not b["canonical"]:
        r("À SURVEILLER", "Canonical supprimé", a["canonical"], "", "Remettre un canonical auto-référent.")
    if a["title"] and b["title"] and a["title"] != b["title"]:
        r("À SURVEILLER", "Title modifié", a["title"], b["title"], "Changement voulu ? Suivre les clics de la page dans Search Console.")
    if a["description"] != b["description"]:
        r("À SURVEILLER", "Meta description " + ("supprimée" if not b["description"] else "modifiée"), a["description"], b["description"], "Changement voulu ?")
    if a["h1"] and b["h1"] and a["h1"] != b["h1"]:
        r("À SURVEILLER", "H1 modifié", " | ".join(a["h1"]), " | ".join(b["h1"]), "Changement voulu ? Le H1 doit garder l'intention de la page.")
    perdus = sorted(set(a["schema"]) - set(b["schema"]))
    if perdus:
        r("À SURVEILLER", "Données structurées retirées", ", ".join(perdus), ", ".join(b["schema"]) or "(aucune)", "Un plugin ou le thème a-t-il changé ?")
    if "JSON-LD invalide" in b["schema"] and "JSON-LD invalide" not in a["schema"]:
        r("À SURVEILLER", "JSON-LD devenu invalide", "", "JSON-LD invalide", "Tester la page avec validator.schema.org.")
    if a["mots"] >= 150 and a["mots"] * 0.5 <= b["mots"] < a["mots"] * 0.8:
        r("À SURVEILLER", "Contenu réduit de plus de 20%", a["mots"], b["mots"], "Vérifier qu'aucune section utile n'a disparu.")
    if a["liens_internes"] >= 10 and b["liens_internes"] < a["liens_internes"] * 0.7:
        r("À SURVEILLER", "Liens internes en baisse de plus de 30%", a["liens_internes"], b["liens_internes"], "Menu, pied de page ou liens du texte supprimés ?")
    if a["hreflang"] != b["hreflang"]:
        r("À SURVEILLER", "hreflang modifié", len(a["hreflang"]), len(b["hreflang"]), "Vérifier les versions de langue.")
    if a["lang"] != b["lang"]:
        r("À SURVEILLER", "Langue de la page modifiée", a["lang"], b["lang"], "L'attribut lang doit rester fr ou fr-FR.")
    # INFO
    if a["h2"] != b["h2"]:
        r("INFO", "Plan H2 modifié", len(a["h2"]), len(b["h2"]), "Relire le nouveau plan.")
    ajoutes = sorted(set(b["schema"]) - set(a["schema"]) - {"JSON-LD invalide"})
    if ajoutes:
        r("INFO", "Données structurées ajoutées", ", ".join(a["schema"]) or "(aucune)", ", ".join(ajoutes), "Valider le nouveau balisage.")
    if a["og"] != b["og"]:
        r("INFO", "Open Graph modifié", "", "", "Vérifier l'aperçu de partage.")
    if b["images_sans_alt"] > a["images_sans_alt"]:
        r("INFO", "Plus d'images sans alt", a["images_sans_alt"], b["images_sans_alt"], "Ajouter un alt (vide si l'image est décorative).")
    if a["empreinte_texte"] != b["empreinte_texte"] and not any(x["regle"].startswith("Contenu") for x in out):
        r("INFO", "Texte modifié", a["mots"], b["mots"], "Normal après une mise à jour ; sinon, chercher la cause.")
    return out


def charger(dossier, url):
    f = fichier(dossier, url)
    return json.load(open(f, encoding="utf-8")) if os.path.exists(f) else []


def sauver(dossier, url, photos, garder=20):
    os.makedirs(dossier, exist_ok=True)
    with open(fichier(dossier, url), "w", encoding="utf-8") as fh:
        json.dump(photos[-garder:], fh, ensure_ascii=False, indent=1)


def sitemap_urls(url, maxi):
    _, _, _, xml = telecharger(url)
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    pages = [l for l in locs if not l.endswith(".xml")]
    for sub in [l for l in locs if l.endswith(".xml")]:
        if len(pages) >= maxi:
            break
        _, _, _, x = telecharger(sub)
        pages += re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", x)
    return pages[:maxi]


def afficher(url, resultats):
    if not resultats:
        print(f"OK            {url} : aucun changement SEO")
        return
    print(f"\n{url}")
    for g in GRAVITES:
        for x in (x for x in resultats if x["gravite"] == g):
            av, ap = str(x["avant"])[:70], str(x["apres"])[:70]
            detail = f" : « {av} » → « {ap} »" if (av or ap) else ""
            print(f"  {g:<13} {x['regle']}{detail}\n                -> {x['action']}")


def main():
    ap = argparse.ArgumentParser(description="Photos SEO et détection des régressions.")
    ap.add_argument("commande", choices=["photo", "comparer", "historique"])
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--sitemap", help="photographier les pages d'un sitemap")
    ap.add_argument("--max", type=int, default=50)
    ap.add_argument("--tout", action="store_true", help="comparer toutes les pages déjà photographiées")
    ap.add_argument("--dossier", default=DOSSIER)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    urls = list(args.urls)
    if args.sitemap:
        urls += sitemap_urls(args.sitemap, args.max)
    if args.tout and os.path.isdir(args.dossier):
        for f in sorted(os.listdir(args.dossier)):
            if f.endswith(".json"):
                hist = json.load(open(os.path.join(args.dossier, f), encoding="utf-8"))
                if hist:
                    urls.append(hist[-1]["url"])
    if not urls:
        ap.error("donne au moins une URL, --sitemap ou --tout")

    if args.commande == "historique":
        for u in urls:
            hist = charger(args.dossier, u)
            print(f"{u} · {len(hist)} photo(s)")
            for s in hist:
                print(f"  {s['date']}  {s['statut']}  {s['mots']} mots  « {s['title'][:60]} »")
        return

    rapport, critiques = {}, 0
    for u in urls:
        hist = charger(args.dossier, u)
        try:
            nouvelle = photo(u, *telecharger(u))
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            print(f"ERREUR        {u} : {e}")
            continue
        if args.commande == "comparer":
            if not hist:
                print(f"PAS DE PHOTO  {u} : lance d'abord « drift.py photo {u} »")
            else:
                res = comparer(hist[-1], nouvelle)
                rapport[u] = res
                critiques += sum(1 for x in res if x["gravite"] == "CRITIQUE")
                if not args.json:
                    afficher(u, res)
        elif not args.json:
            print(f"PHOTO         {u} · {nouvelle['statut']} · {nouvelle['mots']} mots · « {nouvelle['title'][:50]} »")
        sauver(args.dossier, u, hist + [nouvelle])

    if args.json:
        json.dump(rapport, sys.stdout, ensure_ascii=False, indent=2)
        print()
    elif args.commande == "comparer":
        print(f"\n{len(rapport)} page(s) comparée(s) · {critiques} changement(s) CRITIQUE(S)")
    sys.exit(1 if critiques else 0)


if __name__ == "__main__":
    main()
