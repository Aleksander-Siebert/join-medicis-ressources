#!/usr/bin/env python3
"""page.py : lire une page (URL ou fichier) et en extraire ce que lisent les moteurs.

Module partagé du pack GEO, sans dépendance. Fonctions :

- lire(url, ua) : statut, en-têtes, HTML, URL finale, erreur. Une erreur
  réseau n'est jamais confondue avec une page absente : `statut` vaut None
  et `erreur` dit ce qui a échoué.
- analyser(html) : title, méta (robots, description, og:*), canonical,
  titres H1 à H6 avec leur texte, blocs JSON-LD (avec `@graph` déplié),
  texte visible, liens, nombre d'éléments `data-nosnippet`, commentaires,
  éléments cachés (style, `hidden`, `aria-hidden`) et leur texte.

Utilisé par acces.py, contenu.py, entite.py, agentic.py et audit.py.
"""
from __future__ import annotations

import json
import re
import ssl
import urllib.error
import urllib.request
from html.parser import HTMLParser

UA_PACK = "Mozilla/5.0 (compatible; JoinMedicis-geo/2.0; +https://joinmedicis.com)"
UA_NAVIGATEUR = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/140.0.0.0 Safari/537.36")
TAILLE_MAX = 3_000_000
NON_VISIBLES = {"script", "style", "noscript", "template", "svg", "head", "title"}
VIDES = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def lire(url: str, ua: str = UA_PACK, timeout: int = 25, accept: str = "text/html,*/*;q=0.8") -> dict:
    """Lit une URL. Ne lève jamais : renvoie {'statut', 'entetes', 'texte', 'url', 'erreur'}."""
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": accept,
                                               "Accept-Language": "fr-FR,fr;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            brut = r.read(TAILLE_MAX)
            jeu = r.headers.get_content_charset() or "utf-8"
            return {"statut": r.status, "entetes": {k.lower(): v for k, v in r.headers.items()},
                    "texte": brut.decode(jeu, errors="replace"), "url": r.geturl(), "erreur": None}
    except urllib.error.HTTPError as e:
        corps = ""
        try:
            corps = e.read(200_000).decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass
        return {"statut": e.code, "entetes": {k.lower(): v for k, v in (e.headers or {}).items()},
                "texte": corps, "url": url, "erreur": None}
    except Exception as e:  # noqa: BLE001  (réseau, TLS, proxy, délai)
        return {"statut": None, "entetes": {}, "texte": "", "url": url, "erreur": f"{type(e).__name__}: {e}"}


def lire_fichier(chemin: str) -> str:
    with open(chemin, encoding="utf-8", errors="replace") as f:
        return f.read()


class _Analyseur(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pile = []          # (balise, caché)
        self.titre = ""
        self.metas = []
        self.liens_tete = []
        self.titres = []        # [niveau, texte]
        self.jsonld_brut = []
        self.texte = []
        self.texte_cache = []
        self.liens = []
        self.data_nosnippet = 0
        self.commentaires = []
        self.interactifs = []   # (balise, attrs)
        self.images = []
        self._dans = None       # 'title', 'jsonld', ('h', n), None
        self._tampon = []

    def _cache(self):
        return any(c for _, c in self.pile)

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        style = a.get("style", "").replace(" ", "").lower()
        cache = ("hidden" in a or a.get("aria-hidden") == "true" or "display:none" in style
                 or "visibility:hidden" in style or "font-size:0" in style)
        if "data-nosnippet" in a:
            self.data_nosnippet += 1
        if tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.liens_tete.append(a)
        elif tag == "img":
            self.images.append(a)
        if tag == "a" and a.get("href"):
            self.liens.append(a["href"])
        if tag in ("a", "button", "input", "select", "textarea") or a.get("role") in ("button", "link"):
            self.interactifs.append((tag, a, cache or self._cache()))
        if tag in VIDES:
            if tag == "br" and self._dans is not None:
                self._tampon.append(" ")
            return
        if self._dans is not None and tag in ("div", "p", "br"):
            self._tampon.append(" ")
        self.pile.append((tag, cache))
        if tag == "title":
            self._dans, self._tampon = "title", []
        elif tag == "script" and "ld+json" in a.get("type", "").lower():
            self._dans, self._tampon = "jsonld", []
        elif re.fullmatch(r"h[1-6]", tag):
            self._dans, self._tampon = ("h", int(tag[1])), []

    def handle_endtag(self, tag):
        if tag in VIDES:
            return
        if self._dans == "title" and tag == "title":
            self.titre = " ".join("".join(self._tampon).split())
            self._dans = None
        elif self._dans == "jsonld" and tag == "script":
            self.jsonld_brut.append("".join(self._tampon))
            self._dans = None
        elif isinstance(self._dans, tuple) and tag == f"h{self._dans[1]}":
            self.titres.append([self._dans[1], " ".join("".join(self._tampon).split())])
            self._dans = None
        for i in range(len(self.pile) - 1, -1, -1):
            if self.pile[i][0] == tag:
                del self.pile[i:]
                break

    def handle_data(self, data):
        if self._dans is not None and not (isinstance(self._dans, tuple) and self._cache()):
            self._tampon.append(data)  # titre Hn : sans le texte aria-hidden (lettres animées en double)
        if any(t in NON_VISIBLES for t, _ in self.pile):
            return
        if data.strip():
            (self.texte_cache if self._cache() else self.texte).append(data)

    def handle_comment(self, data):
        if data.strip():
            self.commentaires.append(data.strip())


def _deplier(objet, out):
    if isinstance(objet, list):
        for x in objet:
            _deplier(x, out)
    elif isinstance(objet, dict):
        if "@graph" in objet:
            _deplier(objet["@graph"], out)
        if "@type" in objet:
            out.append(objet)


def analyser(html: str) -> dict:
    p = _Analyseur()
    try:
        p.feed(html or "")
        p.close()
    except Exception:  # noqa: BLE001  HTML très cassé : on garde ce qui a été lu
        pass
    metas = {}
    for m in p.metas:
        cle = (m.get("name") or m.get("property") or m.get("http-equiv") or "").lower()
        if cle:
            metas.setdefault(cle, m.get("content", ""))
    canonical = next((l.get("href") for l in p.liens_tete if "canonical" in l.get("rel", "").lower().split()), None)
    jsonld, erreurs = [], []
    for brut in p.jsonld_brut:
        try:
            _deplier(json.loads(brut), jsonld)
        except ValueError as e:
            erreurs.append(str(e)[:80])
    texte = " ".join(" ".join(p.texte).split())
    return {
        "title": p.titre, "metas": metas, "canonical": canonical,
        "lang": None, "titres": p.titres, "jsonld": jsonld, "jsonld_erreurs": erreurs,
        "texte": texte, "mots": len(re.findall(r"\w+", texte)),
        "texte_cache": " ".join(" ".join(p.texte_cache).split()),
        "liens": p.liens, "data_nosnippet": p.data_nosnippet, "commentaires": p.commentaires,
        "interactifs": p.interactifs, "images": p.images,
    }


def types_jsonld(page: dict) -> list[str]:
    out = []
    for o in page["jsonld"]:
        t = o.get("@type")
        out += t if isinstance(t, list) else [t]
    return [str(x) for x in out if x]


def directives_robots(page: dict, entetes: dict | None = None) -> dict:
    """noindex, nosnippet, max-snippet, none : balise robots, balise googlebot et en-tête X-Robots-Tag."""
    morceaux = []
    for cle in ("robots", "googlebot"):
        if page["metas"].get(cle):
            morceaux.append((f"meta {cle}", page["metas"][cle].lower()))
    xr = (entetes or {}).get("x-robots-tag")
    if xr:
        morceaux.append(("en-tête X-Robots-Tag", xr.lower()))
    out = {"noindex": [], "nosnippet": [], "max_snippet": None, "sources": morceaux}
    for src, val in morceaux:
        jetons = [x.strip() for x in val.split(",")]
        if any(j in ("noindex", "none") or j.endswith(": noindex") for j in jetons):
            out["noindex"].append(src)
        if any(j in ("nosnippet", "none") or j.endswith(": nosnippet") for j in jetons):
            out["nosnippet"].append(src)
        m = re.search(r"max-snippet\s*:\s*(-?\d+)", val)
        if m:
            v = int(m.group(1))
            out["max_snippet"] = v if out["max_snippet"] is None else min(out["max_snippet"], v)
    return out
