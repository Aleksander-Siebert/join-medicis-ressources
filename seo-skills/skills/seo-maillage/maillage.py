#!/usr/bin/env python3
"""
maillage.py - lit un sitemap, regroupe les pages en clusters et propose des
liens internes. Sans dépendance, sans clé d'API.

Étapes :
  1. INVENTAIRE   URL depuis un sitemap (index et .gz compris), une liste,
                  ou un export de crawl (Screaming Frog, Sitebulb, CSV maison).
  2. CONTENU      avec --lire : titre, H1, meta description, début du texte et
                  liens internes existants de chaque page (cache local).
  3. PROXIMITÉ    TF-IDF sur titre, H1, slug, description et texte, mots vides
                  français retirés, puis similarité cosinus entre pages.
  4. CLUSTERS     pages reliées au-dessus d'un seuil ; pilier = la page la plus
                  centrale (et la plus visitée si le trafic est fourni).
  5. DIAGNOSTIC   pages orphelines, cannibalisation probable, pages isolées.
  6. LIENS        pour chaque page cible, les pages hôtes qui devraient lui
                  faire un lien : 0,7 × similarité + 0,3 × trafic de l'hôte
                  (normalisé, log), liens déjà présents exclus.

Le script propose. Claude relit chaque paire (sens réel, ancre, paragraphe
d'insertion) et l'utilisateur valide. Ne publiez jamais un lien sans relecture.

Usage
  python3 maillage.py --sitemap https://www.site.fr/sitemap.xml --lire --max 300
  python3 maillage.py --crawl export.csv --trafic gsc-pages.csv
  python3 maillage.py --sitemap sitemap.xml --cible brouillon.md     # hôtes pour un nouvel article
  python3 maillage.py ... --json > maillage.json

Inspiré de l'Internal Linker d'Ahrefs (Agent A) et de seo-cluster
(claude-seo, MIT), réécrit sans embeddings ni API.
"""

import argparse
import csv
import gzip
import html
import io
import json
import math
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

UA = "Mozilla/5.0 (compatible; JoinMedicis-maillage/1.0; +https://joinmedicis.com)"
STOP = set("""
a à afin ai aie aient aies ait alors après as au aucun aucune aujourd auprès aussi autre autres aux avaient avais avait
avant avec avez aviez avions avoir avons ayant b bon c ça car ce ceci cela celle celles celui cependant certain certaines
certains ces cet cette ceux chaque chez ci comme comment contre d dans de des deux devrait dire dit doit donc dont du
durant e elle elles en encore entre es est et étaient était étant été être eu eux f faire fait faut g h i ici il ils
j je jusqu l la là le les leur leurs lors lui m ma mais me même mes moi moins mon n ne ni non nos notre nous o on ont
ou où p par parce pas pendant peu peut plus plusieurs pour pourquoi qu quand que quel quelle quelles quels qui quoi
r s sa sans se selon ses si sien soit son sont sous suis sur t ta tandis te tes toi ton tous tout toute toutes très tu
u un une unes uns v vers voici voilà vos votre vous vu w x y z
the and for with your you are how what why www http https html php fr com page pages accueil article articles blog
guide tout savoir
""".split())
WORD = re.compile(r"[a-zàâäçéèêëîïôöùûüÿœæ0-9]+", re.I)


# ------------------------------------------------------------------ texte
def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def stem(w):
    """Racinisation légère du français : pluriels et quelques suffixes."""
    for suf in ("issements", "issement", "ations", "ation", "ements", "ement", "ments", "ment", "euses", "euse",
                "eurs", "eur", "ables", "able", "iques", "ique", "ites", "ite", "aux", "s", "x", "e"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)] + ("al" if suf == "aux" else "")
    return w


def tokens(text):
    out = []
    for w in WORD.findall(fold(text)):
        if w in STOP or len(w) < 3 or w.isdigit():
            continue
        out.append(stem(w))
    return out


def slug_words(url):
    path = urlsplit(url).path
    return " ".join(re.split(r"[/\-_.]+", path))


# ------------------------------------------------------------------ réseau
def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr-FR,fr;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
        if url.endswith(".gz") or r.headers.get("Content-Encoding") == "gzip":
            try:
                data = gzip.decompress(data)
            except OSError:
                pass
        charset = r.headers.get_content_charset() or "utf-8"
        return data.decode(charset, errors="replace"), r.geturl()


def read_source(src):
    if re.match(r"https?://", src):
        return fetch(src)[0]
    with open(src, "rb") as fh:
        data = fh.read()
    if src.endswith(".gz"):
        data = gzip.decompress(data)
    return data.decode("utf-8", errors="replace")


def sitemap_urls(src, depth=0, limit=5000):
    """URL d'un sitemap ; suit les index de sitemaps (3 niveaux maximum)."""
    xml = read_source(src)
    locs = [html.unescape(x.strip()) for x in re.findall(r"<loc>\s*(.*?)\s*</loc>", xml, re.S)]
    if "<sitemapindex" in xml and depth < 3:
        urls = []
        for sub in locs:
            try:
                urls += sitemap_urls(sub, depth + 1, limit)
            except Exception as e:  # noqa: BLE001
                print(f"  sitemap ignoré ({sub}) : {e}", file=sys.stderr)
            if len(urls) >= limit:
                break
        return urls[:limit]
    return locs[:limit]


class PageParser(HTMLParser):
    """Titre, H1, meta description, texte des paragraphes et liens."""

    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base, self.title, self.h1, self.desc = base, "", "", ""
        self.text, self.links, self._stack, self._skip = [], set(), [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript", "nav", "footer", "header", "aside"):
            self._skip += 1
        if tag == "meta" and (a.get("name") or "").lower() == "description":
            self.desc = a.get("content") or ""
        if tag == "a" and a.get("href"):
            href = urljoin(self.base, a["href"]).split("#")[0]
            if urlsplit(href).netloc == urlsplit(self.base).netloc and not self._skip:
                self.links.add(href.rstrip("/"))
        self._stack.append(tag)

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "nav", "footer", "header", "aside") and self._skip:
            self._skip -= 1
        if self._stack:
            self._stack.pop()

    def handle_data(self, data):
        cur = self._stack[-1] if self._stack else ""
        if cur == "title" and not self.title:
            self.title = data.strip()
        elif cur == "h1" and not self.h1:
            self.h1 = data.strip()
        elif cur in ("p", "li", "h2", "h3") and not self._skip and sum(len(t) for t in self.text) < 4000:
            if data.strip():
                self.text.append(data.strip())


def read_page(url, essais=2):
    for k in range(essais):
        try:
            body, final = fetch(url)
            break
        except urllib.error.HTTPError:
            raise  # 404, 410… : inutile de réessayer
        except Exception:  # noqa: BLE001  (coupure réseau passagère)
            if k == essais - 1:
                raise
            time.sleep(1.5)
    p = PageParser(final)
    p.feed(body)
    return {"url": url, "title": p.title, "h1": p.h1, "description": p.desc,
            "texte": " ".join(p.text)[:4000], "liens": sorted(p.links)}


# ------------------------------------------------------------------ entrées
def norm_url(u):
    return u.strip().rstrip("/")


def load_crawl_csv(path):
    """Export de crawl : colonnes reconnues en français ou en anglais."""
    pages = []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        for row in csv.DictReader(fh, dialect=dialect):
            low = {k.lower().strip(): (v or "") for k, v in row.items() if k}

            def pick(*names):
                for n in names:
                    if low.get(n):
                        return low[n]
                return ""
            url = pick("address", "url", "adresse", "page")
            if not url:
                continue
            pages.append({"url": url, "title": pick("title 1", "title", "titre"), "h1": pick("h1-1", "h1"),
                          "description": pick("meta description 1", "meta description", "description"),
                          "texte": pick("texte", "content", "contenu"), "liens": []})
    return pages


def load_traffic(path):
    """Export Search Console (Pages) ou CSV url,clics."""
    out = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        for row in csv.DictReader(fh, dialect=dialect):
            low = {k.lower().strip(): (v or "") for k, v in row.items() if k}
            url = low.get("pages les plus populaires") or low.get("top pages") or low.get("page") or low.get("url") or ""
            val = low.get("clics") or low.get("clicks") or low.get("trafic") or low.get("traffic") or "0"
            try:
                out[norm_url(url)] = float(str(val).replace(" ", "").replace(" ", "").replace(",", "."))
            except ValueError:
                continue
    return out


# ------------------------------------------------------------------ calcul
def tfidf(docs):
    df = Counter()
    tfs = []
    for d in docs:
        tf = Counter(d)
        tfs.append(tf)
        df.update(tf.keys())
    n = len(docs)
    vecs = []
    for tf in tfs:
        v = {t: (1 + math.log(c)) * math.log((1 + n) / (1 + df[t])) for t, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({t: x / norm for t, x in v.items()})
    return vecs


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(t, 0.0) for t, x in a.items())


def page_doc(p):
    return tokens(" ".join([p.get("title", "")] * 3 + [p.get("h1", "")] * 2 +
                           [slug_words(p["url"])] * 2 + [p.get("description", ""), p.get("texte", "")]))


def label_of(p):
    t = p.get("h1") or p.get("title") or slug_words(p["url"]).strip()
    return re.split(r"\s[|\-–—]\s", t)[0].strip()


def analyse(pages, traffic, seuil_cluster=0.25, seuil_canni=0.6, top=3, cible=None):
    docs = [page_doc(p) for p in pages]
    if cible:
        docs.append(tokens(" ".join([cible["title"]] * 3 + [cible["texte"]])))
    vecs = tfidf(docs)
    n = len(pages)
    sims = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = cosine(vecs[i], vecs[j])
            sims[i][j] = sims[j][i] = s

    # Clusters : composantes connexes au-dessus du seuil.
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i in range(n):
        for j in range(i + 1, n):
            if sims[i][j] >= seuil_cluster:
                parent[find(i)] = find(j)
    groups = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)

    traf = [traffic.get(norm_url(p["url"]), 0.0) for p in pages]
    tmax = math.log1p(max(traf)) if traf and max(traf) > 0 else 1.0
    tnorm = [math.log1p(t) / tmax for t in traf]

    clusters = []
    for members in sorted(groups.values(), key=len, reverse=True):
        if len(members) < 2:
            continue
        central = {i: sum(sims[i][j] for j in members if j != i) / (len(members) - 1) for i in members}
        pillar = max(members, key=lambda i: (central[i] + 0.5 * tnorm[i], -len(urlsplit(pages[i]["url"]).path)))
        clusters.append({"pilier": pages[pillar]["url"], "sujet": label_of(pages[pillar]),
                         "pages": [pages[i]["url"] for i in sorted(members, key=lambda i: -central[i])]})
    isolees = [pages[i]["url"] for g in groups.values() if len(g) == 1 for i in g]

    # Liens existants (si les pages ont été lues).
    existing = {norm_url(p["url"]): {norm_url(x) for x in p.get("liens", [])} for p in pages}
    known_links = any(existing.values())
    inbound = Counter()
    for src, outs in existing.items():
        for dst in outs:
            if dst != src:
                inbound[dst] += 1
    orphelines = [p["url"] for p in pages if known_links and inbound[norm_url(p["url"])] == 0]

    # Cannibalisation : contenus très proches, ou titres/H1 qui se recouvrent
    # (« assurance santé expatrié » contenu dans « prix assurance santé expatrié »).
    heads = [set(tokens(p.get("h1") or p.get("title") or slug_words(p["url"]))) for p in pages]
    canni = []
    for i in range(n):
        for j in range(i + 1, n):
            inter = heads[i] & heads[j]
            recouvre = len(inter) / max(min(len(heads[i]), len(heads[j])), 1) if len(inter) >= 3 else 0.0
            if sims[i][j] >= seuil_canni or recouvre >= 0.75:
                raison = "contenus proches" if sims[i][j] >= seuil_canni else "titres qui se recouvrent"
                canni.append({"a": pages[i]["url"], "b": pages[j]["url"], "similarite": round(sims[i][j], 2),
                              "raison": raison})
    canni.sort(key=lambda c: -c["similarite"])

    # Liens proposés : pour chaque cible, les meilleures pages hôtes.
    def hosts_for(target_vec, target_url, exclude_idx=None):
        cand = []
        for h in range(n):
            if h == exclude_idx:
                continue
            if target_url and norm_url(target_url) in existing.get(norm_url(pages[h]["url"]), set()):
                continue  # le lien existe déjà
            s = cosine(vecs[h], target_vec)
            if s < 0.08:
                continue
            cand.append((0.7 * s + 0.3 * tnorm[h], s, h))
        cand.sort(reverse=True)
        return cand[:top]

    liens = []
    if cible:
        for score, s, h in hosts_for(vecs[n], None):
            liens.append({"hote": pages[h]["url"], "cible": "(nouvel article)", "ancre": cible["title"][:60],
                          "similarite": round(s, 2), "score": round(score, 2)})
    else:
        for t in range(n):
            for score, s, h in hosts_for(vecs[t], pages[t]["url"], exclude_idx=t):
                liens.append({"hote": pages[h]["url"], "cible": pages[t]["url"], "ancre": label_of(pages[t])[:60],
                              "similarite": round(s, 2), "score": round(score, 2)})
        liens.sort(key=lambda x: -x["score"])

    return {"pages": n, "clusters": clusters, "isolees": isolees, "orphelines": orphelines,
            "cannibalisation": canni[:30], "liens": liens, "liens_existants_connus": known_links,
            "trafic_fourni": bool(traffic)}


# ------------------------------------------------------------------ sortie
def render(r, out=sys.stdout, max_liens=40):
    w = out.write
    w(f"MAILLAGE · {r['pages']} pages · {len(r['clusters'])} clusters · {len(r['isolees'])} pages isolées")
    w(f" · trafic {'pris en compte' if r['trafic_fourni'] else 'non fourni'}\n")
    if r.get("erreurs"):
        w(f"\nURL DU SITEMAP EN ERREUR (à corriger ou retirer du sitemap) : {len(r['erreurs'])}\n")
        for e in r["erreurs"][:20]:
            w(f"  - {e['url']}  ({e['erreur']})\n")
    for k, c in enumerate(r["clusters"], 1):
        w(f"\nCLUSTER {k} · {c['sujet']} · {len(c['pages'])} pages\n  pilier : {c['pilier']}\n")
        for u in c["pages"]:
            if u != c["pilier"]:
                w(f"    - {u}\n")
    if r["isolees"]:
        w(f"\nPAGES ISOLÉES (aucune page proche, à rattacher ou à assumer) : {len(r['isolees'])}\n")
        for u in r["isolees"][:20]:
            w(f"  - {u}\n")
    if r["liens_existants_connus"]:
        w(f"\nPAGES ORPHELINES (aucun lien interne dans le contenu) : {len(r['orphelines'])}\n")
        for u in r["orphelines"][:20]:
            w(f"  - {u}\n")
    if r["cannibalisation"]:
        w("\nCANNIBALISATION PROBABLE (à vérifier dans la SERP ou la Search Console)\n")
        for c in r["cannibalisation"][:10]:
            w(f"  {c['similarite']:.2f}  {c['a']}\n        {c['b']}  ({c['raison']})\n")
    w(f"\nLIENS PROPOSÉS ({min(len(r['liens']), max_liens)} sur {len(r['liens'])}) : hôte -> cible [ancre de départ]\n")
    for l in r["liens"][:max_liens]:
        w(f"  {l['score']:.2f}  {l['hote']}\n        -> {l['cible']}  [{l['ancre']}]\n")
    w("\nÀ relire : sens réel du lien, ancre naturelle, paragraphe d'insertion. Rien n'est publié.\n")


def main():
    ap = argparse.ArgumentParser(description="Clusters et liens internes à partir d'un sitemap.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--sitemap", help="URL ou fichier du sitemap (index accepté)")
    src.add_argument("--urls", help="fichier texte, une URL par ligne")
    src.add_argument("--crawl", help="export CSV de crawl (Address/URL, Title, H1, Meta Description)")
    ap.add_argument("--lire", action="store_true", help="lit chaque page (titre, H1, texte, liens existants)")
    ap.add_argument("--max", type=int, default=300, help="nombre maximum de pages (défaut 300)")
    ap.add_argument("--filtre", help="ne garder que les URL qui contiennent ce texte (ex. /blog/)")
    ap.add_argument("--trafic", help="export Search Console « Pages » ou CSV url,clics")
    ap.add_argument("--cible", help="brouillon .md/.txt d'un nouvel article : trouve ses pages hôtes")
    ap.add_argument("--seuil", type=float, default=0.25, help="similarité minimale pour un même cluster")
    ap.add_argument("--liens-par-page", type=int, default=3)
    ap.add_argument("--cache", default="maillage-cache.json", help="cache des pages lues")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.crawl:
        pages = load_crawl_csv(args.crawl)
    else:
        urls = sitemap_urls(args.sitemap) if args.sitemap else [l.strip() for l in open(args.urls, encoding="utf-8") if l.strip()]
        pages = [{"url": u, "title": "", "h1": "", "description": "", "texte": "", "liens": []} for u in urls]
    if args.filtre:
        pages = [p for p in pages if args.filtre in p["url"]]
    pages = [p for p in pages if not re.search(r"\.(?:jpg|jpeg|png|gif|webp|svg|pdf|zip|xml)$", p["url"], re.I)]
    pages = pages[: args.max]

    if args.lire:
        cache = {}
        if os.path.exists(args.cache):
            cache = json.load(open(args.cache, encoding="utf-8"))
        for k, p in enumerate(pages):
            if p["url"] in cache:
                p.update(cache[p["url"]])
                continue
            try:
                p.update(read_page(p["url"]))
                cache[p["url"]] = {k2: p[k2] for k2 in ("title", "h1", "description", "texte", "liens")}
            except Exception as e:  # noqa: BLE001
                p["erreur"] = str(e)
                print(f"  page illisible ({p['url']}) : {e}", file=sys.stderr)
            if k % 20 == 19:
                json.dump(cache, open(args.cache, "w", encoding="utf-8"), ensure_ascii=False)
            time.sleep(0.3)  # politesse envers le serveur
        json.dump(cache, open(args.cache, "w", encoding="utf-8"), ensure_ascii=False)

    erreurs = [{"url": p["url"], "erreur": p["erreur"]} for p in pages if p.get("erreur")]
    pages = [p for p in pages if not p.get("erreur")]
    traffic = load_traffic(args.trafic) if args.trafic else {}
    cible = None
    if args.cible:
        raw = open(args.cible, encoding="utf-8").read()
        title = (re.search(r"^#\s+(.+)$", raw, re.M) or re.search(r"^(.+)$", raw, re.M)).group(1)
        cible = {"title": title.strip(), "texte": raw[:6000]}

    if len(pages) < 2:
        sys.exit("Pas assez de pages pour analyser le maillage.")
    r = analyse(pages, traffic, args.seuil, top=args.liens_par_page, cible=cible)
    r["erreurs"] = erreurs
    if args.json:
        json.dump(r, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        render(r)


if __name__ == "__main__":
    main()
