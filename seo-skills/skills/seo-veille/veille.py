#!/usr/bin/env python3
"""
veille.py - deux outils de veille SEO, sans dépendance.

1. CONCURRENTS : compare les sitemaps de vos concurrents à leur état précédent
   et liste les nouvelles pages (avec date et titre si demandé).

     python3 veille.py concurrents concurrents.txt --etat veille-etat.json
     python3 veille.py concurrents concurrents.txt --etat veille-etat.json --titres --filtre /blog/

   concurrents.txt : une ligne par concurrent, « nom ; URL du sitemap »
   (ou juste l'URL du sitemap). Le premier passage enregistre l'état de départ.

2. RAPPORT : compare deux exports Search Console « Pages » (période actuelle et
   période précédente) et sort les gagnants, les perdants et les totaux.

     python3 veille.py rapport pages-octobre.csv pages-septembre.csv --top 25

Inspiré du Competitor Feed et du rapport mensuel d'Agent A (Ahrefs).
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "seo-maillage"))
try:
    from maillage import fetch, sitemap_urls  # même logique de lecture des sitemaps
except ImportError:  # Skill installé seul : copie minimale
    import gzip
    import html
    import urllib.request

    def fetch(url, timeout=20):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; JoinMedicis-veille/1.0)"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            if url.endswith(".gz"):
                data = gzip.decompress(data)
            return data.decode(r.headers.get_content_charset() or "utf-8", errors="replace"), r.geturl()

    def sitemap_urls(src, depth=0, limit=5000):
        xml = fetch(src)[0] if src.startswith("http") else open(src, encoding="utf-8").read()
        locs = [html.unescape(x.strip()) for x in re.findall(r"<loc>\s*(.*?)\s*</loc>", xml, re.S)]
        if "<sitemapindex" in xml and depth < 3:
            out = []
            for sub in locs:
                try:
                    out += sitemap_urls(sub, depth + 1, limit)
                except Exception:  # noqa: BLE001
                    continue
            return out[:limit]
        return locs[:limit]


def lastmods(src):
    """URL -> lastmod quand le sitemap le donne (sitemap simple uniquement)."""
    try:
        xml = fetch(src)[0] if src.startswith("http") else open(src, encoding="utf-8").read()
    except Exception:  # noqa: BLE001
        return {}
    out = {}
    for block in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>\s*(.*?)\s*</loc>", block, re.S)
        mod = re.search(r"<lastmod>\s*(.*?)\s*</lastmod>", block, re.S)
        if loc:
            out[loc.group(1).strip()] = mod.group(1).strip()[:10] if mod else ""
    return out


def page_title(url):
    try:
        body = fetch(url)[0]
    except Exception:  # noqa: BLE001
        return ""
    m = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def cmd_concurrents(args):
    etat = json.load(open(args.etat, encoding="utf-8")) if os.path.exists(args.etat) else {}
    premier = not etat
    lignes = [l.strip() for l in open(args.liste, encoding="utf-8") if l.strip() and not l.startswith("#")]
    rapport = []
    for ligne in lignes:
        nom, _, src = ligne.partition(";") if ";" in ligne else (ligne, "", ligne)
        nom, src = nom.strip(), (src or nom).strip()
        try:
            urls = sitemap_urls(src)
        except Exception as e:  # noqa: BLE001
            rapport.append({"concurrent": nom, "erreur": str(e), "nouvelles": []})
            continue
        if args.filtre:
            urls = [u for u in urls if args.filtre in u]
        connues = set(etat.get(src, {}).get("urls", []))
        nouvelles = [u for u in urls if u not in connues] if connues else []
        mods = lastmods(src) if nouvelles else {}
        items = []
        for u in nouvelles[: args.max]:
            item = {"url": u, "lastmod": mods.get(u, "")}
            if args.titres:
                item["titre"] = page_title(u)
                time.sleep(0.3)
            items.append(item)
        rapport.append({"concurrent": nom, "pages": len(urls), "nouvelles": items, "nb_nouvelles": len(nouvelles)})
        etat[src] = {"nom": nom, "urls": sorted(set(urls) | connues), "vu_le": date.today().isoformat()}
    json.dump(etat, open(args.etat, "w", encoding="utf-8"), ensure_ascii=False)

    if args.json:
        json.dump({"premier_passage": premier, "concurrents": rapport}, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    print(f"VEILLE CONCURRENTS · {date.today().isoformat()}")
    if premier:
        print("Premier passage : état de départ enregistré. Les nouvelles pages apparaîtront au prochain passage.")
    for r in rapport:
        if r.get("erreur"):
            print(f"\n{r['concurrent']} : sitemap illisible ({r['erreur']})")
            continue
        print(f"\n{r['concurrent']} · {r['pages']} pages · {r['nb_nouvelles']} nouvelle(s)")
        for it in r["nouvelles"]:
            extra = f"  « {it['titre']} »" if it.get("titre") else ""
            print(f"  + {it['lastmod'] or '?':<10} {it['url']}{extra}")


def read_gsc(path):
    """Export Search Console « Pages » : page, clics, impressions, CTR, position."""
    out = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        for row in csv.DictReader(fh, dialect=dialect):
            low = {k.lower().strip(): (v or "").strip() for k, v in row.items() if k}
            url = low.get("pages les plus populaires") or low.get("top pages") or low.get("page") or low.get("url")
            if not url:
                continue

            def num(*keys):
                for k in keys:
                    if low.get(k):
                        v = low[k].replace("%", "").replace(" ", "").replace(" ", "").replace(",", ".")
                        try:
                            return float(v)
                        except ValueError:
                            return 0.0
                return 0.0
            out[url.rstrip("/")] = {"clics": num("clics", "clicks"), "impressions": num("impressions"),
                                    "position": num("position")}
    return out


def cmd_rapport(args):
    cur, prev = read_gsc(args.actuel), read_gsc(args.precedent)
    urls = set(cur) | set(prev)
    rows = []
    for u in urls:
        c, p = cur.get(u, {"clics": 0, "impressions": 0, "position": 0}), prev.get(u, {"clics": 0, "impressions": 0, "position": 0})
        rows.append({"url": u, "clics": c["clics"], "avant": p["clics"], "delta": c["clics"] - p["clics"],
                     "impressions": c["impressions"], "position": c["position"], "position_avant": p["position"]})
    tot_c, tot_p = sum(r["clics"] for r in rows), sum(r["avant"] for r in rows)
    gagnants = sorted([r for r in rows if r["delta"] > 0], key=lambda r: -r["delta"])[: args.top]
    perdants = sorted([r for r in rows if r["delta"] < 0], key=lambda r: r["delta"])[: args.top]
    disparues = [r for r in rows if r["avant"] > 0 and r["clics"] == 0]
    if args.json:
        json.dump({"clics": tot_c, "clics_avant": tot_p, "gagnants": gagnants, "perdants": perdants,
                   "disparues": disparues}, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    var = (tot_c - tot_p) / tot_p * 100 if tot_p else 0
    print(f"RAPPORT SEARCH CONSOLE · {int(tot_c)} clics contre {int(tot_p)} ({var:+.1f}%) · {len(rows)} pages")
    for titre, lst in (("GAGNANTS", gagnants), ("PERDANTS", perdants)):
        print(f"\n{titre}")
        for r in lst:
            pos = f"pos. {r['position_avant']:.1f} -> {r['position']:.1f}" if r["position"] else ""
            print(f"  {r['delta']:+6.0f}  {int(r['avant']):>5} -> {int(r['clics']):<5} {pos:<18} {r['url']}")
    if disparues:
        print(f"\nPAGES SANS CLIC CE MOIS (en avaient avant) : {len(disparues)}")
        for r in disparues[:10]:
            print(f"  {r['url']}  ({int(r['avant'])} clics avant)")


def main():
    ap = argparse.ArgumentParser(description="Veille concurrents (sitemaps) et rapport Search Console.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("concurrents")
    c.add_argument("liste")
    c.add_argument("--etat", default="veille-etat.json")
    c.add_argument("--titres", action="store_true", help="récupère le titre des nouvelles pages")
    c.add_argument("--filtre", help="ne garder que les URL qui contiennent ce texte (ex. /blog/)")
    c.add_argument("--max", type=int, default=30)
    c.add_argument("--json", action="store_true")
    r = sub.add_parser("rapport")
    r.add_argument("actuel")
    r.add_argument("precedent")
    r.add_argument("--top", type=int, default=25)
    r.add_argument("--json", action="store_true")
    args = ap.parse_args()
    cmd_concurrents(args) if args.cmd == "concurrents" else cmd_rapport(args)


if __name__ == "__main__":
    main()
