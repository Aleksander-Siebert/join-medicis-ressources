#!/usr/bin/env python3
"""
Collecte de l'agent de veille concurrentielle (Join Médicis).

Fait la partie mécanique, celle qu'une IA fait mal : lire les sources, garder
ce qui est récent d'après la vraie date, écarter ce qui a déjà été envoyé,
regrouper la même info reprise par plusieurs médias, repérer ce qui a changé
sur les pages surveillées. Le jugement (pertinence, résumé) revient à l'agent.

Python 3.9+ sans dépendance.

Utilisation :
  python3 scripts/collecte.py                 # collecte -> sortie/a-traiter.json
  python3 scripts/collecte.py --test-sources  # vérifie chaque source, cherche les flux RSS des sites
  python3 scripts/collecte.py --valider       # après l'envoi du mail : mémorise ce qui a été envoyé
  python3 scripts/collecte.py --dossier CHEMIN --maintenant 2026-11-09T08:00:00+01:00
"""

from __future__ import annotations

import argparse
import difflib
import email.utils
import hashlib
import html
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (compatible; JoinMedicisVeille/1.0; +https://joinmedicis.com)"
TIMEOUT = 15
SEUIL_TITRE = 0.82  # deux titres plus proches que ça parlent de la même info
MEMOIRE_JOURS = 90  # durée pendant laquelle une info envoyée n'est plus renvoyée
MAX_LIGNES_DIFF = 25

# ------------------------------------------------------------------ outils


def maintenant_utc(valeur: str | None = None) -> datetime:
    if valeur:
        d = datetime.fromisoformat(valeur.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def sans_accents(texte: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texte) if unicodedata.category(c) != "Mn")


MOTS_VIDES = set(
    """le la les un une des du de d l au aux et ou en a à pour par sur dans avec sans ce cet cette ces son sa ses
    leur leurs qui que quoi est sont plus moins pas ne se s y il elle ils elles on nous vous the a an of to in on for
    and or with by at from is are be as its it this that new nouveau nouvelle""".split()
)


def cle_titre(titre: str) -> str:
    """Titre réduit à ses mots utiles, pour comparer deux titres."""
    t = sans_accents(titre.lower())
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    mots = [m for m in t.split() if m not in MOTS_VIDES and len(m) > 1]
    return " ".join(mots)


def titres_proches(a: str, b: str) -> bool:
    if not a or not b:
        return False
    if a == b:
        return True
    if difflib.SequenceMatcher(None, a, b).ratio() >= SEUIL_TITRE:
        return True
    ma, mb = set(a.split()), set(b.split())
    if min(len(ma), len(mb)) >= 4:
        return len(ma & mb) / len(ma | mb) >= 0.6
    return False


PARAMS_PISTAGE = re.compile(r"^(utm_|fbclid$|gclid$|mc_|igshid$|ref$|ref_src$|xtor$)")


def url_canonique(url: str) -> str:
    """URL sans pistage, sans fragment, sans « www. » ni barre finale : deux liens vers la même page se ressemblent."""
    try:
        p = urllib.parse.urlsplit(url.strip())
    except ValueError:
        return url.strip()
    hote = p.netloc.lower()
    if hote.startswith("www."):
        hote = hote[4:]
    params = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True) if not PARAMS_PISTAGE.match(k.lower())]
    chemin = p.path.rstrip("/") or "/"
    return urllib.parse.urlunsplit(("https", hote, chemin, urllib.parse.urlencode(params), ""))


def domaine(url: str) -> str:
    """« https://www.lesechos.fr/x » devient « lesechos.fr »."""
    hote = urllib.parse.urlsplit(url.strip()).netloc.lower().split(":")[0]
    return hote[4:] if hote.startswith("www.") else hote


def empreinte(texte: str) -> str:
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()[:16]


def telecharger(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        brut = r.read(3_000_000)
        enc = r.headers.get_content_charset() or "utf-8"
    try:
        return brut.decode(enc, errors="replace")
    except LookupError:
        return brut.decode("utf-8", errors="replace")


# ------------------------------------------------------------------ dates


def lire_date(texte: str | None) -> datetime | None:
    if not texte:
        return None
    texte = texte.strip()
    try:
        d = email.utils.parsedate_to_datetime(texte)
        if d is not None:
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError, IndexError):
        pass
    try:
        d = datetime.fromisoformat(texte.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", texte)
    if m:
        return datetime(int(m[1]), int(m[2]), int(m[3]), tzinfo=timezone.utc)
    return None


# ------------------------------------------------------------------ flux RSS et Atom


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _texte(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return "".join(el.itertext()).strip()


def nettoyer_html(texte: str) -> str:
    texte = re.sub(r"<[^>]+>", " ", texte or "")
    return re.sub(r"\s+", " ", html.unescape(texte)).strip()


def lire_flux(xml_texte: str, origine: str) -> list[dict]:
    """Articles d'un flux RSS 2.0, RSS 1.0 ou Atom. Lève ValueError si ce n'est pas un flux."""
    try:
        racine = ET.fromstring(xml_texte.encode("utf-8") if isinstance(xml_texte, str) else xml_texte)
    except ET.ParseError as e:
        raise ValueError(f"flux illisible ({e})") from e
    articles = []
    for el in racine.iter():
        nom = _local(el.tag)
        if nom not in ("item", "entry"):
            continue
        champs = {_local(c.tag): c for c in el}
        titre = nettoyer_html(_texte(champs.get("title")))
        lien = ""
        if "link" in champs:
            lien_el = champs["link"]
            lien = lien_el.get("href") or _texte(lien_el)
            # Atom : préférer le lien rel="alternate"
            for c in el:
                if _local(c.tag) == "link" and c.get("rel", "alternate") == "alternate" and c.get("href"):
                    lien = c.get("href")
                    break
        if not lien and "guid" in champs and _texte(champs["guid"]).startswith("http"):
            lien = _texte(champs["guid"])
        date = None
        for cle in ("pubdate", "published", "updated", "date", "issued", "created"):
            if cle in champs:
                date = lire_date(_texte(champs[cle]))
                if date:
                    break
        # attention : un élément XML sans enfant vaut « faux », d'où les tests explicites
        corps = next((champs[k] for k in ("description", "summary", "content", "encoded") if champs.get(k) is not None), None)
        resume = nettoyer_html(_texte(corps))
        source = _texte(champs.get("source")) or origine
        src_el = champs.get("source")
        src_url = (src_el.get("url") if src_el is not None else None) or lien
        if titre or lien:
            articles.append({"titre": titre, "lien": lien.strip(), "date": date, "extrait": resume[:600], "source": source, "domaine": domaine(src_url or "")})
    if not articles and _local(racine.tag) not in ("rss", "feed", "rdf"):
        raise ValueError("ce n'est pas un flux RSS ou Atom")
    return articles


def url_google_actualites(requete: str, langue: str = "fr", pays: str = "FR") -> str:
    q = urllib.parse.quote_plus(requete)
    return f"https://news.google.com/rss/search?q={q}&hl={langue}&gl={pays}&ceid={pays}:{langue}"


def decouper_titre_google(titre: str, source: str) -> tuple[str, str]:
    """Google Actualités ajoute « - Média » à la fin du titre : on le sépare."""
    if " - " in titre:
        debut, fin = titre.rsplit(" - ", 1)
        if len(fin) <= 60:
            return debut.strip(), (source if source and source != "Google Actualités" else fin.strip())
    return titre, source


# ------------------------------------------------------------------ pages web


class _Texte(HTMLParser):
    BLOCS = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "td", "th", "section", "article", "br", "dt", "dd", "span", "a", "button"}
    IGNORES = {"script", "style", "noscript", "svg", "template", "head"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lignes: list[str] = []
        self.courant: list[str] = []
        self.ignore = 0
        self.flux: list[str] = []
        self.liens: list[tuple[str, str]] = []
        self._lien: str | None = None
        self._texte_lien: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.IGNORES:
            self.ignore += 1
        if tag == "link":
            a = dict(attrs)
            if (a.get("rel") or "").lower() == "alternate" and re.search(r"rss|atom", a.get("type") or "") and a.get("href"):
                self.flux.append(a["href"])
        if tag == "a":
            self._lien = dict(attrs).get("href")
            self._texte_lien = []
        if tag in self.BLOCS:
            self._couper()

    def handle_endtag(self, tag):
        if tag == "a" and self._lien:
            self.liens.append((self._lien, re.sub(r"\s+", " ", "".join(self._texte_lien)).strip()))
            self._lien = None
        if tag in self.IGNORES and self.ignore:
            self.ignore -= 1
        if tag in self.BLOCS:
            self._couper()

    def handle_data(self, data):
        if not self.ignore:
            self.courant.append(data)
            if self._lien is not None:
                self._texte_lien.append(data)

    def _couper(self):
        ligne = re.sub(r"\s+", " ", "".join(self.courant)).strip()
        if ligne:
            self.lignes.append(ligne)
        self.courant = []


PAGES_UTILES = re.compile(r"tarif|prix|pricing|price|plans?\b|offres?\b|abonnement|nouveaut|changelog|release|presse|press|blog|actualit|news", re.I)


def liens_utiles(html_texte: str, base: str) -> list[str]:
    """Liens d'une page d'accueil qui méritent d'être surveillés (tarifs, offres, nouveautés, presse)."""
    p = _Texte()
    p.feed(html_texte)
    hote = urllib.parse.urlsplit(base).netloc.replace("www.", "")
    vus, out = set(), []
    for href, texte in p.liens:
        url = urllib.parse.urljoin(base, href)
        if urllib.parse.urlsplit(url).netloc.replace("www.", "") != hote:
            continue
        sans_params = url.split("#")[0].split("?")[0]
        if PAGES_UTILES.search(f"{href} {texte}") and url_canonique(sans_params) not in vus:
            vus.add(url_canonique(sans_params))
            out.append(sans_params)
    # les pages courtes d'abord (« /tarifs » plutôt qu'un article de blog)
    out.sort(key=lambda u: len(urllib.parse.urlsplit(u).path.strip("/").split("/")))
    return out[:6]


def texte_de_page(html_texte: str) -> tuple[list[str], list[str]]:
    """Lignes de texte visibles d'une page, et flux RSS qu'elle annonce."""
    p = _Texte()
    p.feed(html_texte)
    p._couper()
    lignes = []
    for ligne in p.lignes:
        if len(ligne) < 2:
            continue
        if lignes and lignes[-1] == ligne:
            continue
        lignes.append(ligne)
    return lignes, p.flux


# Lignes qui changent à chaque visite sans rien signifier (horloges, compteurs, jetons).
BRUIT = re.compile(r"^(\d{1,2}[:h]\d{2}|il y a \d+|\d+ (min|minutes|secondes|s) ago|©.*\d{4}|copyright.*)$", re.I)


def changements(avant: list[str], apres: list[str]) -> tuple[list[str], list[str]]:
    av = [l for l in avant if not BRUIT.match(l)]
    ap = [l for l in apres if not BRUIT.match(l)]
    ajouts, retraits = [], []
    for op in difflib.ndiff(av, ap):
        if op.startswith("+ "):
            ajouts.append(op[2:])
        elif op.startswith("- "):
            retraits.append(op[2:])
    return ajouts[:MAX_LIGNES_DIFF], retraits[:MAX_LIGNES_DIFF]


# ------------------------------------------------------------------ mémoire


def charger_memoire(dossier: Path) -> dict:
    f = dossier / "memoire" / "deja-vu.json"
    if f.exists():
        try:
            m = json.loads(f.read_text("utf-8"))
            m.setdefault("urls", {})
            m.setdefault("titres", {})
            return m
        except json.JSONDecodeError:
            pass
    return {"urls": {}, "titres": {}}


def nettoyer_memoire(m: dict, maintenant: datetime) -> dict:
    limite = (maintenant - timedelta(days=MEMOIRE_JOURS)).isoformat()
    return {
        "urls": {k: v for k, v in m["urls"].items() if v >= limite},
        "titres": {k: v for k, v in m["titres"].items() if v >= limite},
    }


def deja_vu(article: dict, memoire: dict) -> bool:
    if empreinte(url_canonique(article["lien"])) in memoire["urls"]:
        return True
    cle = cle_titre(article["titre"])
    return any(titres_proches(cle, t) for t in memoire["titres"])


# ------------------------------------------------------------------ concurrents


def mentionne(texte: str, noms: list[str]) -> bool:
    t = " " + re.sub(r"[^a-z0-9]+", " ", sans_accents(texte.lower())) + " "
    for nom in noms:
        n = re.sub(r"[^a-z0-9]+", " ", sans_accents(nom.lower())).strip()
        if n and f" {n} " in t:
            return True
    return False


def contient_mot_exclu(texte: str, exclus: list[str]) -> bool:
    return bool(exclus) and mentionne(texte, exclus)


# ------------------------------------------------------------------ regroupement


def regrouper(articles: list[dict]) -> list[dict]:
    """Une info reprise par plusieurs médias devient un seul sujet avec toutes ses sources."""
    sujets: list[dict] = []
    for a in sorted(articles, key=lambda x: x["date"] or datetime.min.replace(tzinfo=timezone.utc)):
        cle = cle_titre(a["titre"])
        url = url_canonique(a["lien"]) if a["lien"] else ""
        cible = None
        for s in sujets:
            if (url and url in s["_urls"]) or titres_proches(cle, s["_cle"]):
                cible = s
                break
        source = {"nom": a["source"], "url": a["lien"], "domaine": a.get("domaine") or domaine(a["lien"])}
        if cible:
            if url and url in cible["_urls"]:
                continue
            cible["sources"].append(source)
            cible["_urls"].add(url)
            if len(a["extrait"]) > len(cible["extrait"]):
                cible["extrait"] = a["extrait"]
            continue
        sujets.append(
            {
                "titre": a["titre"],
                "date": a["date"],
                "date_inconnue": a["date"] is None,
                "concurrents": a.get("concurrents", []),
                "extrait": a["extrait"],
                "sources": [source],
                "_cle": cle,
                "_urls": {url} if url else set(),
            }
        )
    for s in sujets:
        s["doublons"] = len(s["sources"]) - 1
    return sujets


# ------------------------------------------------------------------ articles d'origine


def retrouver_originaux(sujets: list[dict], telecharge, max_medias: int = 15) -> int:
    """Pour les sujets connus seulement par Google Actualités, cherche l'article dans le flux RSS du média :
    vrai lien et chapeau à la place du seul titre. Renvoie le nombre d'articles retrouvés."""
    flux_par_media: dict[str, list[dict] | None] = {}
    trouves = 0
    for s in sujets:
        if s["extrait"] and len(s["extrait"]) > len(s["titre"]) + 40:
            continue
        for src in s["sources"]:
            dom = src.get("domaine")
            if not dom or dom == "news.google.com" or "news.google.com" not in src.get("url", ""):
                continue
            if dom not in flux_par_media:
                if len(flux_par_media) >= max_medias:
                    continue
                flux_par_media[dom] = None
                candidats = []
                try:
                    _, annonces = texte_de_page(telecharge(f"https://{dom}/"))
                    candidats += [urllib.parse.urljoin(f"https://{dom}/", f) for f in annonces[:2]]
                except Exception:
                    pass
                candidats += [f"https://{dom}/feed", f"https://{dom}/rss"]
                for url in candidats:
                    try:
                        flux_par_media[dom] = lire_flux(telecharge(url), dom)
                        break
                    except Exception:
                        continue
            articles = flux_par_media.get(dom) or []
            cle = cle_titre(s["titre"])
            for a in articles:
                if titres_proches(cle, cle_titre(a["titre"])):
                    src["url_google"] = src["url"]
                    src["url"] = a["lien"]
                    if len(a["extrait"]) > len(s["extrait"]):
                        s["extrait"] = a["extrait"]
                    trouves += 1
                    break
    return trouves


# ------------------------------------------------------------------ collecte


def lire_config(dossier: Path) -> dict:
    f = dossier / "sources.json"
    if not f.exists():
        raise SystemExit(f"Fichier introuvable : {f}. Lance d'abord CONFIGURE-MOI.md.")
    try:
        c = json.loads(f.read_text("utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"sources.json n'est pas un JSON valide (ligne {e.lineno}) : {e.msg}")
    c.setdefault("jours", 7)
    c.setdefault("langue", "fr")
    c.setdefault("pays", "FR")
    c.setdefault("concurrents", [])
    c.setdefault("flux_secteur", [])
    c.setdefault("mots_exclus", [])
    c.setdefault("actualites_google", True)
    c.setdefault("max_sujets", 40)
    if not any(x.get("nom") and "{{" not in x["nom"] for x in c["concurrents"]):
        raise SystemExit("Aucun concurrent dans sources.json : lance d'abord CONFIGURE-MOI.md.")
    return c


def collecter(config: dict, memoire: dict, dossier: Path, maintenant: datetime, telecharge=telecharger) -> dict:
    limite = maintenant - timedelta(days=int(config["jours"]))
    stats = {"lus": 0, "trop_vieux": 0, "deja_envoyes": 0, "hors_sujet": 0, "exclus": 0, "dans_le_futur": 0}
    erreurs: list[dict] = []
    gardes: list[dict] = []
    pages_modifiees: list[dict] = []
    snapshots: dict = {}
    noms_concurrents = [c["nom"] for c in config["concurrents"] if c.get("nom")]

    def traiter(articles: list[dict], concurrent: dict | None, exige_mention: bool):
        for a in articles:
            stats["lus"] += 1
            if concurrent and concurrent.get("source_google"):
                a["titre"], a["source"] = decouper_titre_google(a["titre"], a["source"])
            texte = f"{a['titre']} {a['extrait']}"
            if a["date"] and a["date"] < limite:
                stats["trop_vieux"] += 1
                continue
            if a["date"] and a["date"] > maintenant + timedelta(days=1):
                stats["dans_le_futur"] += 1
                a["date"] = None
            noms = [concurrent["nom"], *concurrent.get("alias", [])] if concurrent else noms_concurrents
            vises = [c for c in noms_concurrents if mentionne(texte, [c])]
            if exige_mention and not mentionne(texte, noms):
                stats["hors_sujet"] += 1
                continue
            if contient_mot_exclu(texte, config["mots_exclus"] + (concurrent.get("exclure", []) if concurrent else [])):
                stats["exclus"] += 1
                continue
            if deja_vu(a, memoire):
                stats["deja_envoyes"] += 1
                continue
            a["concurrents"] = sorted(set(vises + ([concurrent["nom"]] if concurrent else [])))
            gardes.append(a)

    for c in config["concurrents"]:
        nom = c.get("nom", "").strip()
        if not nom:
            continue
        # 1. Actualités qui citent le concurrent
        if config["actualites_google"]:
            requete = c.get("requete") or f'"{nom}"' + (" " + " ".join(c["mots_cles"]) if c.get("mots_cles") else "")
            # « when:7d » : sans lui, Google renvoie surtout des articles anciens triés par pertinence
            url = url_google_actualites(f"{requete} when:{int(config['jours'])}d", config["langue"], config["pays"])
            try:
                traiter(lire_flux(telecharge(url), "Google Actualités"), {**c, "source_google": True}, exige_mention=True)
            except Exception as e:  # une source en panne n'arrête pas la veille
                erreurs.append({"source": f"Actualités « {nom} »", "url": url, "erreur": str(e)[:200]})
        # 2. Flux du concurrent (blog, salle de presse)
        for url in c.get("flux", []):
            try:
                traiter(lire_flux(telecharge(url), nom), c, exige_mention=False)
            except Exception as e:
                erreurs.append({"source": f"Flux de {nom}", "url": url, "erreur": str(e)[:200]})
        # 3. Pages surveillées (prix, offres, produit)
        for url in c.get("pages", []):
            try:
                lignes, _ = texte_de_page(telecharge(url))
                cle = empreinte(url_canonique(url))
                ancien_f = dossier / "memoire" / "pages" / f"{cle}.json"
                snapshots[cle] = {"url": url, "concurrent": nom, "lignes": lignes, "vu_le": maintenant.isoformat()}
                if not ancien_f.exists():
                    pages_modifiees.append({"concurrent": nom, "url": url, "premiere_visite": True, "ajouts": [], "retraits": []})
                    continue
                ancien = json.loads(ancien_f.read_text("utf-8"))
                ajouts, retraits = changements(ancien.get("lignes", []), lignes)
                if ajouts or retraits:
                    pages_modifiees.append({"concurrent": nom, "url": url, "premiere_visite": False, "depuis": ancien.get("vu_le"), "ajouts": ajouts, "retraits": retraits})
            except Exception as e:
                erreurs.append({"source": f"Page de {nom}", "url": url, "erreur": str(e)[:200]})

    # 4. Flux du secteur (médias, blogs) : seuls les articles qui citent un concurrent ou un mot-clé suivi
    mots_secteur = [m for c in config["concurrents"] for m in [c.get("nom", "")] + c.get("alias", [])] + config.get("mots_cles_secteur", [])
    for url in config["flux_secteur"]:
        try:
            articles = lire_flux(telecharge(url), urllib.parse.urlsplit(url).netloc.replace("www.", ""))
            for a in articles:
                if not mentionne(f"{a['titre']} {a['extrait']}", mots_secteur):
                    stats["lus"] += 1
                    stats["hors_sujet"] += 1
                    continue
                traiter([a], None, exige_mention=False)
        except Exception as e:
            erreurs.append({"source": "Flux du secteur", "url": url, "erreur": str(e)[:200]})

    sujets = regrouper(gardes)
    stats["articles_retrouves"] = retrouver_originaux(sujets, telecharge) if config.get("retrouver_articles", True) else 0
    stats["doublons_regroupes"] = sum(s["doublons"] for s in sujets)
    sujets.sort(key=lambda s: (s["date"] is None, -(s["date"].timestamp() if s["date"] else 0)))
    coupes = max(0, len(sujets) - int(config["max_sujets"]))
    sujets = sujets[: int(config["max_sujets"])]
    stats["coupes_au_dela_du_max"] = coupes
    stats["sujets"] = len(sujets)
    stats["pages_modifiees"] = sum(1 for p in pages_modifiees if not p["premiere_visite"])

    sortie = {
        "genere_le": maintenant.isoformat(),
        "periode": {"du": limite.date().isoformat(), "au": maintenant.date().isoformat(), "jours": int(config["jours"])},
        "stats": stats,
        "sujets": [
            {
                "id": f"s{i + 1}",
                "titre": s["titre"],
                "date": s["date"].date().isoformat() if s["date"] else None,
                "date_inconnue": s["date_inconnue"],
                "concurrents": s["concurrents"],
                "extrait": s["extrait"],
                "sources": s["sources"],
            }
            for i, s in enumerate(sujets)
        ],
        "pages_modifiees": pages_modifiees,
        "erreurs": erreurs,
    }
    return {"sortie": sortie, "snapshots": snapshots}


def valider(dossier: Path, maintenant: datetime) -> str:
    """Après l'envoi : mémorise les sujets et l'état des pages pour ne pas les renvoyer."""
    f = dossier / "sortie" / "a-traiter.json"
    s = dossier / "sortie" / ".pages.json"
    if not f.exists():
        raise SystemExit("Rien à valider : lance d'abord la collecte.")
    data = json.loads(f.read_text("utf-8"))
    m = nettoyer_memoire(charger_memoire(dossier), maintenant)
    jour = maintenant.isoformat()
    n = 0
    for sujet in data["sujets"]:
        m["titres"][cle_titre(sujet["titre"])] = jour
        for src in sujet["sources"]:
            if src.get("url"):
                m["urls"][empreinte(url_canonique(src["url"]))] = jour
        n += 1
    (dossier / "memoire").mkdir(exist_ok=True)
    (dossier / "memoire" / "deja-vu.json").write_text(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True), "utf-8")
    p = 0
    if s.exists():
        snaps = json.loads(s.read_text("utf-8"))
        (dossier / "memoire" / "pages").mkdir(parents=True, exist_ok=True)
        for cle, snap in snaps.items():
            (dossier / "memoire" / "pages" / f"{cle}.json").write_text(json.dumps(snap, ensure_ascii=False, indent=1), "utf-8")
            p += 1
    return f"Mémoire mise à jour : {n} sujets et {p} pages enregistrés."


def tester_sources(config: dict, telecharge=telecharger) -> list[str]:
    """Vérifie chaque source et propose les flux RSS trouvés sur les sites des concurrents."""
    rapport = []
    for c in config["concurrents"]:
        nom = c.get("nom", "?")
        if c.get("site"):
            try:
                page = telecharge(c["site"])
                _, flux = texte_de_page(page)
                flux = [urllib.parse.urljoin(c["site"], f) for f in flux]
                if flux:
                    rapport.append(f"OK   {nom} : site lu, flux trouvés : {', '.join(flux[:3])}")
                else:
                    rapport.append(f"OK   {nom} : site lu, aucun flux RSS annoncé (on surveillera ses pages)")
                pistes = [u for u in liens_utiles(page, c["site"]) if u not in c.get("pages", [])]
                if pistes:
                    rapport.append(f"     {nom} : pages à surveiller possibles : {', '.join(pistes)}")
            except Exception as e:
                rapport.append(f"ERR  {nom} : site illisible ({str(e)[:80]})")
        for url in c.get("flux", []):
            try:
                n = len(lire_flux(telecharge(url), nom))
                rapport.append(f"OK   {nom} : flux {url} ({n} articles)")
            except Exception as e:
                rapport.append(f"ERR  {nom} : flux {url} ({str(e)[:80]})")
        for url in c.get("pages", []):
            try:
                lignes, _ = texte_de_page(telecharge(url))
                etat = "OK  " if len(lignes) >= 5 else "VIDE"
                rapport.append(f"{etat} {nom} : page {url} ({len(lignes)} lignes de texte)")
            except Exception as e:
                rapport.append(f"ERR  {nom} : page {url} ({str(e)[:80]})")
    for url in config["flux_secteur"]:
        try:
            n = len(lire_flux(telecharge(url), url))
            rapport.append(f"OK   secteur : {url} ({n} articles)")
        except Exception as e:
            rapport.append(f"ERR  secteur : {url} ({str(e)[:80]})")
    return rapport


def _json_defaut(o):
    if isinstance(o, datetime):
        return o.isoformat()
    if isinstance(o, set):
        return sorted(o)
    raise TypeError(type(o))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Collecte de l'agent de veille concurrentielle")
    ap.add_argument("--dossier", default=str(Path(__file__).resolve().parent.parent), help="dossier de l'agent")
    ap.add_argument("--valider", action="store_true", help="mémorise ce qui vient d'être envoyé")
    ap.add_argument("--test-sources", action="store_true", help="vérifie les sources sans rien collecter")
    ap.add_argument("--maintenant", help="date et heure de référence (ISO 8601), pour les tests")
    a = ap.parse_args(argv)
    dossier = Path(a.dossier)
    now = maintenant_utc(a.maintenant)

    if a.valider:
        print(valider(dossier, now))
        return 0
    config = lire_config(dossier)
    if a.test_sources:
        lignes = tester_sources(config)
        print("\n".join(lignes) or "Aucune source à tester.")
        return 1 if any(l.startswith("ERR") for l in lignes) else 0

    res = collecter(config, nettoyer_memoire(charger_memoire(dossier), now), dossier, now)
    (dossier / "sortie").mkdir(exist_ok=True)
    (dossier / "sortie" / "a-traiter.json").write_text(json.dumps(res["sortie"], ensure_ascii=False, indent=1, default=_json_defaut), "utf-8")
    (dossier / "sortie" / ".pages.json").write_text(json.dumps(res["snapshots"], ensure_ascii=False, default=_json_defaut), "utf-8")
    st = res["sortie"]["stats"]
    print(
        f"Collecte du {res['sortie']['periode']['du']} au {res['sortie']['periode']['au']} : "
        f"{st['lus']} articles lus, {st['sujets']} sujets gardés "
        f"({st['trop_vieux']} trop vieux, {st['deja_envoyes']} déjà envoyés, {st['hors_sujet']} hors sujet, "
        f"{st['exclus']} exclus, {st['doublons_regroupes']} doublons regroupés), "
        f"{st['pages_modifiees']} pages modifiées, {len(res['sortie']['erreurs'])} sources en erreur."
    )
    print("Résultat : sortie/a-traiter.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
