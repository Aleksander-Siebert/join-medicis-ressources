#!/usr/bin/env python3
"""
onpage.py - contrôle on-page d'une page HTML, sans dépendance.

Vérifie : title, meta description, H1 et plan des titres, nombre de mots,
images (alt, dimensions, chargement différé, priorité, format, poids avec
--poids-images), canonical, meta robots (noindex, nosnippet), lang, viewport,
hreflang, Open Graph, données structurées JSON-LD, liens internes et externes,
mot-clé principal (title, H1, URL, description, début du texte), et les Core
Web Vitals réels avec --cwv (API PageSpeed Insights, clé gratuite).

    python3 onpage.py https://www.site.fr/page/ --mot-cle "assurance expatrié"
    python3 onpage.py page.html --url https://www.site.fr/page/
    python3 onpage.py https://www.site.fr/ --json
    python3 onpage.py https://www.site.fr/ --poids-images --cwv   # PSI_API_KEY dans l'environnement

Le script mesure ; l'interprétation (priorités, contenu, E-E-A-T) reste dans
le Skill. Les longueurs de title et description sont des repères, pas des
règles de Google : la troncature se fait en pixels.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlencode, urljoin, urlsplit

UA = "Mozilla/5.0 (compatible; JoinMedicis-onpage/1.0; +https://joinmedicis.com)"


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


class P(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.title = ""
        self.meta = {}
        self.links_rel = []
        self.headings = []
        self.imgs = []
        self.anchors = []
        self.jsonld = []
        self.lang = ""
        self.text = []
        self._stack = []
        self._skip = 0
        self._cur_heading = None
        self._in_jsonld = False
        self._buf = []
        self._picture_moderne = False

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        if tag == "link":
            self.links_rel.append(a)
        if tag == "img":
            a["_picture_moderne"] = self._picture_moderne
            self.imgs.append(a)
        if tag == "picture":
            self._picture_moderne = False
        if tag == "source" and "picture" in self._stack and re.search(r"image/(?:webp|avif)", a.get("type", "")):
            self._picture_moderne = True
        if tag == "a" and a.get("href"):
            self.anchors.append({"href": urljoin(self.base, a["href"]), "rel": a.get("rel", ""), "texte": ""})
        if tag == "script" and "ld+json" in a.get("type", ""):
            self._in_jsonld, self._buf = True, []
        elif tag in ("script", "style", "noscript"):
            self._skip += 1
        if re.fullmatch(r"h[1-6]", tag):
            self._cur_heading = [int(tag[1]), ""]
        if tag == "br" and self._cur_heading is not None:
            self._cur_heading[1] += " "
        self._stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "picture":
            self._picture_moderne = False
        if tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.jsonld.append("".join(self._buf))
        elif tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1
        if re.fullmatch(r"h[1-6]", tag) and self._cur_heading:
            self.headings.append((self._cur_heading[0], re.sub(r"\s+", " ", self._cur_heading[1]).strip()))
            self._cur_heading = None
        if self._stack:
            self._stack.pop()

    def handle_data(self, data):
        if self._in_jsonld:
            self._buf.append(data)
            return
        if self._skip:
            return
        cur = self._stack[-1] if self._stack else ""
        if cur == "title" and not self.title:
            self.title = data.strip()
        if self._cur_heading is not None:
            self._cur_heading[1] += data
        if self.anchors and cur == "a":
            self.anchors[-1]["texte"] += data.strip()
        if cur not in ("title",) and data.strip():
            self.text.append(data.strip())


def schema_types(blocks):
    types = []
    for b in blocks:
        try:
            data = json.loads(b)
        except ValueError:
            types.append("JSON-LD invalide")
            continue
        stack = [data]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                t = x.get("@type")
                if t:
                    types += t if isinstance(t, list) else [t]
                stack += list(x.values())
            elif isinstance(x, list):
                stack += x
    return sorted(set(types))


MODERNE = re.compile(r"\.(?:webp|avif|svg)(?:[?#]|$)", re.I)
ANCIEN = re.compile(r"\.(?:jpe?g|png|gif|bmp)(?:[?#]|$)", re.I)


def controle_images(imgs, base):
    """Contrôles sur le HTML seul. La 1re image est traitée comme l'image principale probable (LCP)."""
    vraies = [i for i in imgs if i.get("src") and not i["src"].startswith("data:")]
    # Une image qui remplit un bloc positionné (data-nimg="fill", position:absolute) ne décale pas la page.
    remplit = lambda i: i.get("data-nimg") == "fill" or "position:absolute" in i.get("style", "").replace(" ", "")  # noqa: E731
    sans_dim = [i["src"] for i in vraies if not (i.get("width") and i.get("height")) and not remplit(i)]
    anciens = [i["src"] for i in vraies if ANCIEN.search(i["src"]) and not i.get("_picture_moderne")
               and not re.search(r"/_next/image|[?&](?:fm|format)=(?:webp|avif)", i["src"])]
    premiere = vraies[0] if vraies else None
    lcp_lazy = bool(premiere and premiere.get("loading", "").lower() == "lazy")
    lazy = sum(1 for i in vraies[1:] if i.get("loading", "").lower() == "lazy")
    return {"total": len(vraies), "sans_dimensions": sans_dim, "formats_anciens": anciens,
            "lcp_lazy": lcp_lazy, "lcp_priorite": bool(premiere and premiere.get("fetchpriority", "").lower() == "high"),
            "lazy_hors_premiere": lazy, "premiere": premiere["src"] if premiere else "",
            "urls": [urljoin(base, i["src"]) for i in vraies]}


def poids_images(urls, seuil_ko=200, maxi=30):
    """HEAD sur chaque image : celles au-dessus du seuil."""
    lourdes = []
    for u in urls[:maxi]:
        try:
            req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=15) as r:
                ko = int(r.headers.get("Content-Length") or 0) // 1024
        except Exception:  # noqa: BLE001 - une image illisible ne bloque pas l'audit
            continue
        if ko > seuil_ko:
            lourdes.append((u, ko))
    return lourdes


PSI = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
SEUILS = {"LCP": (2500, 4000), "INP": (200, 500), "CLS": (0.1, 0.25)}


def lire_psi(d):
    """Core Web Vitals d'une réponse PageSpeed Insights : terrain (CrUX, 28 jours) si dispo, sinon labo."""
    m = (d.get("loadingExperience") or {}).get("metrics") or {}
    terrain = {}
    if "LARGEST_CONTENTFUL_PAINT_MS" in m:
        terrain["LCP"] = m["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]
    if "INTERACTION_TO_NEXT_PAINT" in m:
        terrain["INP"] = m["INTERACTION_TO_NEXT_PAINT"]["percentile"]
    if "CUMULATIVE_LAYOUT_SHIFT_SCORE" in m:
        terrain["CLS"] = m["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"] / 100
    audits = (d.get("lighthouseResult") or {}).get("audits") or {}
    labo = {}
    if "largest-contentful-paint" in audits:
        labo["LCP"] = round(audits["largest-contentful-paint"].get("numericValue", 0))
    if "cumulative-layout-shift" in audits:
        labo["CLS"] = round(audits["cumulative-layout-shift"].get("numericValue", 0), 3)
    if "total-blocking-time" in audits:
        labo["TBT"] = round(audits["total-blocking-time"].get("numericValue", 0))
    return {"terrain": terrain, "labo": labo}


def note_cwv(nom, v):
    if nom not in SEUILS:
        return ""
    bon, mauvais = SEUILS[nom]
    return "bon" if v <= bon else ("à améliorer" if v <= mauvais else "mauvais")


def cwv(url, cle=None, strategie="mobile"):
    q = {"url": url, "strategy": strategie, "category": "performance"}
    if cle:
        q["key"] = cle
    req = urllib.request.Request(PSI + "?" + urlencode(q), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return lire_psi(json.loads(r.read().decode()))


def audit(html, url, mot_cle=None):
    p = P(url)
    p.feed(html)
    host = urlsplit(url).netloc
    words = re.findall(r"\w+", " ".join(p.text))
    texte = " ".join(p.text)
    h1 = [h for lvl, h in p.headings if lvl == 1]
    canon = next((l.get("href") for l in p.links_rel if "canonical" in l.get("rel", "").lower()), "")
    hreflang = [l.get("hreflang") for l in p.links_rel if l.get("hreflang")]
    internes = [a for a in p.anchors if urlsplit(a["href"]).netloc == host]
    externes = [a for a in p.anchors if urlsplit(a["href"]).netloc not in ("", host) and a["href"].startswith("http")]
    vides = [a for a in internes if not a["texte"] or fold(a["texte"]) in ("ici", "cliquez ici", "en savoir plus", "lire la suite")]
    # alt="" est correct pour une image décorative : seul l'attribut absent est signalé.
    sans_alt = [i.get("src", "")[:80] for i in p.imgs if "alt" not in i]
    robots = p.meta.get("robots", "")
    img = controle_images(p.imgs, url)
    desc = p.meta.get("description", "")
    sauts = [f"H{a}→H{b}" for (a, _), (b, _) in zip(p.headings, p.headings[1:]) if b > a + 1]

    checks = []

    def c(nom, ok, valeur, conseil=""):
        checks.append({"controle": nom, "statut": ok, "valeur": valeur, "conseil": conseil if ok != "OK" else ""})

    tl = len(p.title)
    c("Title", "OK" if 30 <= tl <= 60 else ("MANQUANT" if not tl else "À REVOIR"), f"{tl} car. « {p.title[:70]} »",
      "Viser 50-60 caractères, mot-clé au début, marque à la fin.")
    dl = len(desc)
    c("Meta description", "OK" if 120 <= dl <= 160 else ("MANQUANT" if not dl else "À REVOIR"), f"{dl} car.",
      "Viser 140-160 caractères, voix active, une promesse concrète.")
    c("H1", "OK" if len(h1) == 1 else ("MANQUANT" if not h1 else "À REVOIR"), f"{len(h1)} · {' | '.join(h1)[:80]}",
      "Un seul H1, proche du title, avec le mot-clé principal.")
    c("Hiérarchie des titres", "OK" if not sauts else "À REVOIR", ", ".join(sauts[:5]) or "sans saut",
      "Ne pas sauter de niveau (H2 puis H4).")
    c("Nombre de mots", "OK" if len(words) >= 300 else "À REVOIR", str(len(words)),
      "Moins de 300 mots : vérifier que la page répond vraiment à l'intention.")
    c("Images sans alt", "OK" if not sans_alt else "À REVOIR", f"{len(sans_alt)} sur {len(p.imgs)}",
      "Alt descriptif sur les images porteuses de sens, vide (alt=\"\") sur les décoratives.")
    c("Dimensions des images", "OK" if not img["sans_dimensions"] else "À REVOIR",
      f"{len(img['sans_dimensions'])} sur {img['total']} sans width/height",
      "width et height sur chaque image : évite les décalages de mise en page (CLS).")
    if img["total"]:
        c("Image principale", "À REVOIR" if img["lcp_lazy"] else "OK",
          ("loading=lazy sur la 1re image" if img["lcp_lazy"] else "chargée tout de suite")
          + (" · fetchpriority=high" if img["lcp_priorite"] else ""),
          "Pas de loading=lazy sur l'image principale ; fetchpriority=\"high\" l'affiche plus vite (LCP).")
        c("Format des images", "OK" if not img["formats_anciens"] else "À REVOIR",
          f"{len(img['formats_anciens'])} en JPEG/PNG/GIF sur {img['total']}",
          "WebP ou AVIF : souvent 25 à 50% plus légers à qualité égale.")
    c("Canonical", "OK" if canon else "MANQUANT", canon or "absente", "Ajouter une canonical auto-référente.")
    rl = robots.lower()
    snip = "nosnippet" in rl or bool(re.search(r"max-snippet\s*:\s*0\b", rl))
    c("Meta robots", "BLOQUANT" if "noindex" in rl or snip else "OK", robots or "index par défaut",
      "noindex : la page ne sera pas indexée. nosnippet ou max-snippet:0 : pas d'extrait, donc pas d'AI Overviews ni d'AI Mode.")
    c("Langue (html lang)", "OK" if p.lang else "MANQUANT", p.lang or "absente", "Déclarer lang=\"fr\" (ou fr-FR).")
    c("Viewport mobile", "OK" if p.meta.get("viewport") else "MANQUANT", p.meta.get("viewport", "absent"),
      "Ajouter <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">.")
    c("Open Graph", "OK" if p.meta.get("og:title") and p.meta.get("og:image") else "À REVOIR",
      f"og:title {'oui' if p.meta.get('og:title') else 'non'} · og:image {'oui' if p.meta.get('og:image') else 'non'}",
      "og:title, og:description et og:image pour les partages.")
    types = schema_types(p.jsonld)
    c("Données structurées", "OK" if types and "JSON-LD invalide" not in types else ("À REVOIR" if types else "MANQUANT"),
      ", ".join(types) or "aucune", "Ajouter le schema adapté (Organization, Article, Product, LocalBusiness, BreadcrumbList…).")
    c("Liens internes", "OK" if len(internes) >= 3 else "À REVOIR", f"{len(internes)} (dont {len(vides)} ancre(s) vide(s) ou générique(s))",
      "Au moins 3 liens internes contextuels, ancres descriptives.")
    c("Liens externes", "OK", f"{len(externes)}")
    if hreflang:
        c("Hreflang", "OK" if "x-default" in hreflang else "À REVOIR", ", ".join(hreflang),
          "Prévoir x-default et des liens réciproques.")
    if mot_cle:
        k = fold(mot_cle)
        debut = fold(" ".join(words[:100]))
        places = {"title": k in fold(p.title), "H1": k in fold(" ".join(h1)), "URL": k.replace(" ", "-") in fold(url),
                  "description": k in fold(desc), "100 premiers mots": k in debut}
        manque = [n for n, ok in places.items() if not ok]
        c(f"Mot-clé « {mot_cle} »", "OK" if not manque else "À REVOIR",
          "présent partout" if not manque else "absent de : " + ", ".join(manque),
          "Placer le mot-clé (ou une variante proche) là où il manque, sans forcer.")
    return {"url": url, "controles": checks, "titres": p.headings[:40], "images": img}


def main():
    ap = argparse.ArgumentParser(description="Contrôle on-page d'une page HTML.")
    ap.add_argument("source", help="URL ou fichier HTML")
    ap.add_argument("--url", help="URL de la page si la source est un fichier")
    ap.add_argument("--mot-cle")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--poids-images", action="store_true", help="mesurer le poids des images (requêtes HEAD)")
    ap.add_argument("--cwv", action="store_true", help="Core Web Vitals via PageSpeed Insights (mobile)")
    ap.add_argument("--cle", default=os.environ.get("PSI_API_KEY"), help="clé API PageSpeed (ou PSI_API_KEY)")
    args = ap.parse_args()
    if re.match(r"https?://", args.source):
        req = urllib.request.Request(args.source, headers={"User-Agent": UA, "Accept-Language": "fr-FR,fr;q=0.9"})
        with urllib.request.urlopen(req, timeout=25) as r:
            html = r.read().decode(r.headers.get_content_charset() or "utf-8", errors="replace")
            url = r.geturl()
    else:
        html = open(args.source, encoding="utf-8", errors="replace").read()
        url = args.url or "https://exemple.fr/"
    res = audit(html, url, args.mot_cle)
    if args.poids_images:
        lourdes = poids_images(res["images"]["urls"])
        res["controles"].append({"controle": "Poids des images", "statut": "OK" if not lourdes else "À REVOIR",
                                 "valeur": f"{len(lourdes)} au-dessus de 200 Ko" + "".join(f"\n              {k} Ko  {u[:80]}" for u, k in lourdes[:5]),
                                 "conseil": "" if not lourdes else "Compresser et redimensionner à la taille affichée."})
    if args.cwv:
        try:
            v = cwv(url, args.cle)
            res["cwv"] = v
            src, mes = ("terrain (28 jours, CrUX)", v["terrain"]) if v["terrain"] else ("labo (Lighthouse)", v["labo"])
            val = " · ".join(f"{k} {x}{' ms' if k in ('LCP', 'INP', 'TBT') else ''} ({note_cwv(k, x) or 'labo'})" for k, x in mes.items())
            mauvais = any(note_cwv(k, x) in ("mauvais", "à améliorer") for k, x in mes.items())
            res["controles"].append({"controle": "Core Web Vitals", "statut": "À REVOIR" if mauvais else "OK",
                                     "valeur": f"{src} : {val or 'aucune donnée'}",
                                     "conseil": "Seuils : LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1 (75e centile)." if mauvais else ""})
        except urllib.error.HTTPError as e:
            msg = "quota sans clé épuisé : crée une clé gratuite (Google Cloud → API PageSpeed Insights) et passe --cle ou PSI_API_KEY" if e.code == 429 else f"erreur {e.code}"
            res["controles"].append({"controle": "Core Web Vitals", "statut": "NON MESURÉ", "valeur": msg, "conseil": ""})
    if args.json:
        json.dump(res, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    print(f"ON-PAGE · {res['url']}")
    for ch in res["controles"]:
        print(f"  {ch['statut']:<9} {ch['controle']:<26} {ch['valeur']}")
        if ch["conseil"]:
            print(f"            -> {ch['conseil']}")
    print("\nPLAN DES TITRES")
    for lvl, t in res["titres"]:
        print(f"  {'  ' * (lvl - 1)}H{lvl} {t[:90]}")


if __name__ == "__main__":
    main()
