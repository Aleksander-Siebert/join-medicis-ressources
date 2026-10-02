#!/usr/bin/env python3
"""
onpage.py - contrôle on-page d'une page HTML, sans dépendance.

Vérifie : title, meta description, H1 et plan des titres, nombre de mots,
images sans alt, canonical, meta robots, lang, viewport, hreflang, Open Graph,
données structurées JSON-LD, liens internes et externes, mot-clé principal
(title, H1, URL, description, début du texte).

    python3 onpage.py https://www.site.fr/page/ --mot-cle "assurance expatrié"
    python3 onpage.py page.html --url https://www.site.fr/page/
    python3 onpage.py https://www.site.fr/ --json

Le script mesure ; l'interprétation (priorités, contenu, E-E-A-T) reste dans
le Skill. Les longueurs de title et description sont des repères, pas des
règles de Google : la troncature se fait en pixels.
"""

import argparse
import json
import re
import sys
import unicodedata
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

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
            self.imgs.append(a)
        if tag == "a" and a.get("href"):
            self.anchors.append({"href": urljoin(self.base, a["href"]), "rel": a.get("rel", ""), "texte": ""})
        if tag == "script" and "ld+json" in a.get("type", ""):
            self._in_jsonld, self._buf = True, []
        elif tag in ("script", "style", "noscript"):
            self._skip += 1
        if re.fullmatch(r"h[1-6]", tag):
            self._cur_heading = [int(tag[1]), ""]
        self._stack.append(tag)

    def handle_endtag(self, tag):
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
    sans_alt = [i.get("src", "")[:80] for i in p.imgs if not i.get("alt", "").strip()]
    robots = p.meta.get("robots", "")
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
    c("Canonical", "OK" if canon else "MANQUANT", canon or "absente", "Ajouter une canonical auto-référente.")
    c("Meta robots", "BLOQUANT" if "noindex" in robots.lower() else "OK", robots or "index par défaut",
      "noindex présent : la page ne sera pas indexée.")
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
    return {"url": url, "controles": checks, "titres": p.headings[:40]}


def main():
    ap = argparse.ArgumentParser(description="Contrôle on-page d'une page HTML.")
    ap.add_argument("source", help="URL ou fichier HTML")
    ap.add_argument("--url", help="URL de la page si la source est un fichier")
    ap.add_argument("--mot-cle")
    ap.add_argument("--json", action="store_true")
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
