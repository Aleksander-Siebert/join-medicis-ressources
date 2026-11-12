#!/usr/bin/env python3
"""
Collecte de l'agent de veille (Join Médicis) : concurrents, tendances,
réglementation, appels d'offres.

Fait la partie mécanique, celle qu'une IA fait mal : lire les sources, garder
ce qui est récent d'après la vraie date, écarter ce qui a déjà été envoyé,
regrouper la même info reprise par plusieurs médias, repérer ce qui a changé
sur les pages surveillées. Le jugement (pertinence, résumé) revient à l'agent.

Python 3.9+ sans dépendance.

Utilisation :
  python3 scripts/collecte.py                 # collecte -> sortie/a-traiter.json
  python3 scripts/collecte.py --test-sources  # vérifie chaque source, cherche les flux RSS des sites
  python3 scripts/collecte.py --valider       # après l'envoi du mail : mémorise ce qui a été envoyé
  python3 scripts/collecte.py --diagnostic    # vérifie l'installation, étape par étape
  python3 scripts/collecte.py --integrer      # ajoute les articles trouvés par recherche web (sortie/trouvailles.json)
  python3 scripts/collecte.py --dossier CHEMIN --maintenant 2026-11-09T08:00:00+01:00
"""

from __future__ import annotations

import argparse
import difflib
import email.utils
import hashlib
import html
import ipaddress
import json
import re
import socket
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

# Un robot qui se présente comme tel : pas de faux navigateur.
USER_AGENT = "Mozilla/5.0 (compatible; JoinMedicisVeille/2.0; +https://joinmedicis.com)"
NOM_ROBOT = "JoinMedicisVeille"
TIMEOUT = 15
SEUIL_TITRE = 0.82  # deux titres plus proches que ça parlent de la même info
MEMOIRE_JOURS = 90  # durée pendant laquelle une info envoyée n'est plus renvoyée
MAX_LIGNES_DIFF = 25
PAUSE_PAR_SITE = 1.0  # secondes entre deux lectures du même site
PAUSE_MAX = 10.0  # plafond appliqué au « Crawl-delay » demandé par un site
TAILLE_MAX = 3_000_000  # octets lus par page, au plus

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


class AdresseRefusee(Exception):
    pass


def verifier_adresse(url: str) -> None:
    """Refuse tout ce qui n'est pas une page web publique : fichiers locaux, réseau interne, cette machine.
    Un flux ou une redirection ne peut donc pas faire lire l'intranet de l'utilisateur."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise AdresseRefusee(f"adresse refusée (seules les pages http et https sont lues) : {url[:80]}")
    hote = parts.hostname
    if hote == "localhost" or hote.endswith((".local", ".internal", ".lan")):
        raise AdresseRefusee(f"adresse du réseau local refusée : {hote}")
    try:
        ips = [ipaddress.ip_address(hote)]
    except ValueError:
        try:
            ips = [ipaddress.ip_address(i[4][0]) for i in socket.getaddrinfo(hote, None)]
        except (OSError, ValueError):
            return  # nom non résolu ici (proxy d'entreprise) : la lecture échouera d'elle-même si besoin
    for ip in ips:
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            raise AdresseRefusee(f"adresse du réseau local refusée : {hote}")


class _Redirections(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        verifier_adresse(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OUVREUR = urllib.request.build_opener(_Redirections)
_DERNIER_PASSAGE: dict[str, float] = {}
_PAUSES: dict[str, float] = {}


def _attendre(hote: str) -> None:
    pause = _PAUSES.get(hote, PAUSE_PAR_SITE)
    reste = _DERNIER_PASSAGE.get(hote, 0) + pause - time.monotonic()
    if reste > 0:
        time.sleep(reste)
    _DERNIER_PASSAGE[hote] = time.monotonic()


def telecharger(url: str, corps: bytes | None = None) -> str:
    """Lit une page publique. `corps` : envoi en JSON (API qui exigent une requête POST)."""
    verifier_adresse(url)
    _attendre(urllib.parse.urlsplit(url).hostname or "")
    entetes = {"User-Agent": USER_AGENT, "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"}
    if corps is not None:
        entetes["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=corps, headers=entetes)
    for essai in (1, 2):  # une coupure réseau passagère ne doit pas faire perdre une source
        try:
            with _OUVREUR.open(req, timeout=TIMEOUT) as r:
                brut = r.read(TAILLE_MAX)
                enc = r.headers.get_content_charset() or "utf-8"
            break
        except urllib.error.HTTPError:
            raise  # le site a répondu (403, 404…) : insister ne sert à rien
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            if essai == 2:
                raise
            time.sleep(2)
    try:
        return brut.decode(enc, errors="replace")
    except LookupError:
        return brut.decode("utf-8", errors="replace")


# ------------------------------------------------------------------ robots.txt


class Robots:
    """Respect du fichier robots.txt de chaque site, lu une fois par passage.
    Il s'applique aux pages que le script va chercher de lui-même. Les flux RSS et les API
    officielles sont publiés pour être lus par des programmes : ils ne sont pas concernés."""

    def __init__(self, telecharge, actif: bool = True):
        self.telecharge = telecharge
        self.actif = actif
        self._regles: dict[str, urllib.robotparser.RobotFileParser | None] = {}

    def _pour(self, url: str):
        parts = urllib.parse.urlsplit(url)
        racine = f"{parts.scheme}://{parts.netloc}"
        if racine not in self._regles:
            regles = None
            try:
                texte = self.telecharge(racine + "/robots.txt")
                if "<html" not in texte[:500].lower():
                    regles = urllib.robotparser.RobotFileParser()
                    regles.parse(texte.splitlines())
                    delai = regles.crawl_delay(NOM_ROBOT)
                    if delai:
                        _PAUSES[parts.hostname or ""] = min(float(delai), PAUSE_MAX)
            except Exception:
                regles = None  # pas de robots.txt lisible : le site ne pose pas de règle
            self._regles[racine] = regles
        return self._regles[racine]

    def permet(self, url: str) -> bool:
        if not self.actif:
            return True
        regles = self._pour(url)
        return True if regles is None else regles.can_fetch(NOM_ROBOT, url)


class RefusRobots(Exception):
    def __init__(self, url: str):
        super().__init__("le site demande aux robots de ne pas lire cette page (robots.txt)")
        self.url = url


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
            cible["concurrents"] = sorted(set(cible["concurrents"]) | set(a.get("concurrents", [])))
            if cible["concurrents"]:
                cible["axe"] = "concurrents"
            if len(a["extrait"]) > len(cible["extrait"]):
                cible["extrait"] = a["extrait"]
            continue
        sujets.append(
            {
                "titre": a["titre"],
                "date": a["date"],
                "date_inconnue": a["date"] is None,
                "axe": a.get("axe", "concurrents"),
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


# ------------------------------------------------------------------ agrégateurs (mode étendu)


def url_bing_actualites(requete: str, langue: str = "fr", pays: str = "FR") -> str:
    q = urllib.parse.quote_plus(requete)
    return f"https://www.bing.com/news/search?q={q}&format=rss&setlang={langue}&cc={pays}"


def lien_reel_bing(lien: str) -> str:
    """Bing Actualités enveloppe chaque lien : on retrouve l'adresse de l'article."""
    parts = urllib.parse.urlsplit(lien)
    if "bing.com" in parts.netloc:
        cible = urllib.parse.parse_qs(parts.query).get("url")
        if cible and cible[0].startswith("http"):
            return cible[0]
    return lien


AGREGATEURS = {"google": "Google Actualités", "bing": "Bing Actualités"}


def lire_agregateur(nom: str, requete: str, config: dict, telecharge) -> list[dict]:
    jours = int(config["jours"])
    if nom == "google":
        # « when:7d » : sans lui, Google renvoie surtout des articles anciens triés par pertinence
        articles = lire_flux(telecharge(url_google_actualites(f"{requete} when:{jours}d", config["langue"], config["pays"])), AGREGATEURS[nom])
        for a in articles:
            a["titre"], a["source"] = decouper_titre_google(a["titre"], a["source"])
        return articles
    if nom == "bing":
        articles = lire_flux(telecharge(url_bing_actualites(requete, config["langue"], config["pays"])), AGREGATEURS[nom])
        for a in articles:
            a["lien"] = lien_reel_bing(a["lien"])
            a["domaine"] = domaine(a["lien"])
            if a["source"] == AGREGATEURS[nom]:
                a["source"] = a["domaine"]
        return articles
    raise ValueError(f"agrégateur inconnu : {nom}")


# ------------------------------------------------------------------ pages suivies


def decrire_page(page) -> dict:
    """Une page suivie s'écrit comme une adresse seule, ou avec ses réglages :
    {"url": …, "intention": "préviens-moi seulement si le prix change", "ignorer": [...], "seulement_si": [...]}"""
    if isinstance(page, str):
        return {"url": page, "intention": "", "ignorer": [], "seulement_si": []}
    return {
        "url": page.get("url", ""),
        "intention": page.get("intention", ""),
        "ignorer": page.get("ignorer", []) or [],
        "seulement_si": page.get("seulement_si", []) or [],
    }


def _aplatir(valeur, chemin: str = "") -> list[str]:
    if isinstance(valeur, dict):
        return [l for k in sorted(valeur) for l in _aplatir(valeur[k], f"{chemin}.{k}" if chemin else str(k))]
    if isinstance(valeur, list):
        return [l for i, v in enumerate(valeur) for l in _aplatir(v, f"{chemin}[{i}]")]
    return [f"{chemin} : {valeur}"]


def lignes_de_contenu(texte: str) -> tuple[list[str], list[str]]:
    """Lignes comparables d'une page HTML ou d'une réponse JSON publique, et flux annoncés."""
    debut = texte.lstrip()[:1]
    if debut in "{[" and debut:
        try:
            return _aplatir(json.loads(texte))[:5000], []
        except json.JSONDecodeError:
            pass
    return texte_de_page(texte)


def filtrer_lignes(lignes: list[str], ignorer: list[str]) -> list[str]:
    if not ignorer:
        return lignes
    mots = [sans_accents(m.lower()) for m in ignorer if m.strip()]
    return [l for l in lignes if not any(m in sans_accents(l.lower()) for m in mots)]


def concerne(lignes: list[str], mots: list[str]) -> bool:
    if not mots:
        return True
    cibles = [sans_accents(m.lower()) for m in mots if m.strip()]
    return any(m in sans_accents(l.lower()) for l in lignes for m in cibles)


# ------------------------------------------------------------------ offres d'emploi


def api_emplois(url: str) -> tuple[str, str] | None:
    """Les outils de recrutement courants publient leurs offres par une API publique.
    Renvoie (outil, adresse de l'API) pour une page carrière reconnue."""
    parts = urllib.parse.urlsplit(url)
    chemin = [x for x in parts.path.split("/") if x]
    hote = parts.netloc.lower().replace("www.", "")
    if not chemin:
        return None
    if hote in ("boards.greenhouse.io", "job-boards.greenhouse.io", "job-boards.eu.greenhouse.io"):
        return "greenhouse", f"https://boards-api.greenhouse.io/v1/boards/{chemin[0]}/jobs"
    if hote in ("jobs.lever.co", "jobs.eu.lever.co"):
        base = "api.eu.lever.co" if ".eu." in hote else "api.lever.co"
        return "lever", f"https://{base}/v0/postings/{chemin[0]}?mode=json"
    if hote == "jobs.ashbyhq.com":
        return "ashby", f"https://api.ashbyhq.com/posting-api/job-board/{chemin[0]}"
    return None


def lire_emplois(outil: str, texte: str) -> list[dict]:
    data = json.loads(texte)
    offres = []
    if outil == "greenhouse":
        for j in data.get("jobs", []):
            offres.append({"titre": j.get("title", ""), "lieu": (j.get("location") or {}).get("name", ""), "url": j.get("absolute_url", "")})
    elif outil == "lever":
        for j in data if isinstance(data, list) else []:
            cat = j.get("categories") or {}
            offres.append({"titre": j.get("text", ""), "lieu": cat.get("location", ""), "equipe": cat.get("team", ""), "url": j.get("hostedUrl", "")})
    elif outil == "ashby":
        for j in data.get("jobs", []):
            offres.append({"titre": j.get("title", ""), "lieu": j.get("location", ""), "equipe": j.get("department", ""), "url": j.get("jobUrl", "")})
    return [o for o in offres if o["titre"]]


# ------------------------------------------------------------------ appels d'offres

BOAMP = "https://boamp-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/boamp/records"
TED = "https://api.ted.europa.eu/v3/notices/search"
PAYS_TED = {"FR": "FRA", "BE": "BEL", "CH": "CHE", "LU": "LUX", "DE": "DEU", "ES": "ESP", "IT": "ITA", "NL": "NLD", "PT": "PRT"}


def _sans_guillemets(mot: str) -> str:
    return re.sub(r'["\'\\\\]', " ", mot).strip()


def url_boamp(mots: list[str], depuis: datetime, departements: list[str], limite: int = 40) -> str:
    recherche = " or ".join(f'search(objet,"{_sans_guillemets(m)}")' for m in mots)
    where = f"({recherche}) and dateparution>=date'{depuis.date().isoformat()}'"
    if departements:
        where += " and (" + " or ".join(f'code_departement="{_sans_guillemets(d)}"' for d in departements) + ")"
    return f"{BOAMP}?" + urllib.parse.urlencode({"where": where, "order_by": "dateparution desc", "limit": limite})


def lire_boamp(texte: str) -> list[dict]:
    avis = []
    for r in json.loads(texte).get("results", []):
        avis.append(
            {
                "titre": html.unescape(r.get("objet") or "").strip(),
                "acheteur": html.unescape(r.get("nomacheteur") or ""),
                "date": r.get("dateparution"),
                "date_limite": (r.get("datelimitereponse") or "")[:10] or None,
                "type": r.get("nature_libelle") or "",
                "titulaire": ", ".join(r["titulaire"]) if isinstance(r.get("titulaire"), list) else (r.get("titulaire") or None),
                "departements": r.get("code_departement") or [],
                "source": "BOAMP",
                "url": r.get("url_avis") or f"https://www.boamp.fr/pages/avis/?q=idweb:{r.get('idweb', '')}",
            }
        )
    return [a for a in avis if a["titre"]]


def corps_ted(mots: list[str], depuis: datetime, pays: str, limite: int = 40) -> bytes:
    # recherche dans le titre de l'avis : le texte intégral ramène trop d'avis sans rapport
    recherche = " OR ".join(f'notice-title ~ "{_sans_guillemets(m)}"' for m in mots)
    requete = f"({recherche}) AND publication-date >= {depuis.strftime('%Y%m%d')}"
    if pays:
        requete += f' AND buyer-country = "{PAYS_TED.get(pays.upper(), pays.upper())}"'
    champs = ["notice-title", "publication-date", "buyer-name", "deadline-receipt-tender-date-lot", "notice-type"]
    return json.dumps({"query": requete + " SORT BY publication-date DESC", "fields": champs, "limit": limite}).encode("utf-8")


def _langue(valeur, langue: str = "fra") -> str:
    """Les champs de TED sont donnés par langue : le français d'abord, puis l'anglais, puis ce qui existe."""
    if isinstance(valeur, dict):
        for cle in (langue, "eng", *valeur.keys()):
            if valeur.get(cle):
                valeur = valeur[cle]
                break
    if isinstance(valeur, list):
        valeur = valeur[0] if valeur else ""
    return str(valeur or "").strip()


def lire_ted(texte: str) -> list[dict]:
    avis = []
    for r in json.loads(texte).get("notices", []):
        numero = r.get("publication-number", "")
        limites = r.get("deadline-receipt-tender-date-lot") or []
        avis.append(
            {
                "titre": _langue(r.get("notice-title")),
                "acheteur": _langue(r.get("buyer-name")),
                "date": (r.get("publication-date") or "")[:10] or None,
                "date_limite": (limites[0][:10] if limites else None),
                "type": r.get("notice-type") or "",
                "titulaire": None,
                "departements": [],
                "source": "TED (Europe)",
                "url": f"https://ted.europa.eu/fr/notice/-/detail/{numero}",
            }
        )
    return [a for a in avis if a["titre"]]


# ------------------------------------------------------------------ sujets qui montent


def termes_du_titre(titre: str) -> list[str]:
    mots = [m for m in cle_titre(titre).split() if len(m) > 3 and not m.isdigit()]
    return mots + [f"{a} {b}" for a, b in zip(mots, mots[1:])]


def sujets_qui_montent(compte: dict, passages: list[dict], minimum: int = 3, rapport: float = 2.5, maximum: int = 8) -> list[dict]:
    """Compare la fréquence d'un terme dans les titres lus à sa moyenne des passages précédents.
    Il faut au moins 3 passages en mémoire : avant, rien ne permet de dire ce qui est habituel."""
    if len(passages) < 3:
        return []
    montent = []
    for terme, n in compte.items():
        if n < minimum:
            continue
        moyenne = sum(p.get("termes", {}).get(terme, 0) for p in passages) / len(passages)
        if n / (moyenne + 1) >= rapport:
            montent.append({"terme": terme, "cette_fois": n, "moyenne_avant": round(moyenne, 1)})
    montent.sort(key=lambda t: (-t["cette_fois"] / (t["moyenne_avant"] + 1), t["terme"]))
    # un groupe de deux mots suffit : on retire les mots seuls qu'il contient déjà
    doubles = {m for t in montent if " " in t["terme"] for m in t["terme"].split()}
    return [t for t in montent if " " in t["terme"] or t["terme"] not in doubles][:maximum]


def charger_json(fichier: Path, defaut):
    if fichier.exists():
        try:
            return json.loads(fichier.read_text("utf-8"))
        except json.JSONDecodeError:
            pass
    return defaut


def resume_historique(entrees: list[dict], maintenant: datetime) -> dict:
    """Ce que la veille a déjà signalé par concurrent sur 90 jours, pour repérer ce qui se répète."""
    limite = (maintenant - timedelta(days=MEMOIRE_JOURS)).date().isoformat()
    par_concurrent: dict = {}
    for e_ in entrees:
        if (e_.get("date") or "") < limite:
            continue
        for nom in e_.get("concurrents", []) or ["(marché)"]:
            c = par_concurrent.setdefault(nom, {"par_rubrique": {}, "derniers": []})
            c["par_rubrique"][e_.get("rubrique", "Autre")] = c["par_rubrique"].get(e_.get("rubrique", "Autre"), 0) + 1
            c["derniers"].append({"date": e_.get("date"), "rubrique": e_.get("rubrique"), "titre": e_.get("titre")})
    for c in par_concurrent.values():
        c["derniers"] = sorted(c["derniers"], key=lambda x: x["date"] or "", reverse=True)[:5]
    return par_concurrent


# ------------------------------------------------------------------ collecte

FLUX_REGLEMENTATION = {
    "CNIL": "https://www.cnil.fr/fr/rss.xml",
    "DGCCRF": "https://www.economie.gouv.fr/dgccrf/rss",
    "EUR-Lex (législation européenne)": "https://eur-lex.europa.eu/EN/display-feed.rss?rssId=162",
}


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
    c.setdefault("mots_cles_secteur", [])
    c.setdefault("mots_exclus", [])
    c.setdefault("max_sujets", 40)
    c.setdefault("respecter_robots", True)
    # « standard » : flux, pages et sources officielles. « etendu » : en plus, les agrégateurs d'actualités.
    if "mode" not in c:
        c["mode"] = "etendu" if c.get("actualites_google") else "standard"
    if c["mode"] not in ("standard", "etendu"):
        raise SystemExit('sources.json : "mode" vaut "standard" ou "etendu".')
    c.setdefault("agregateurs", ["google"])
    inconnus = [a for a in c["agregateurs"] if a not in AGREGATEURS]
    if inconnus:
        raise SystemExit(f"sources.json : agrégateur inconnu ({', '.join(inconnus)}). Choix : {', '.join(AGREGATEURS)}.")
    s = c.setdefault("strategique", {})
    for axe in ("tendances", "reglementation", "appels_offres"):
        a = s.setdefault(axe, {})
        a.setdefault("mots_cles", [])
        a.setdefault("flux", [])
    s["appels_offres"].setdefault("departements", [])
    s["appels_offres"].setdefault("sources", ["boamp", "ted"])
    c["concurrents"] = [x for x in c["concurrents"] if x.get("nom") and "{{" not in x["nom"]]
    a_des_sujets = any(s[a]["mots_cles"] or s[a]["flux"] for a in s)
    if not c["concurrents"] and not a_des_sujets:
        raise SystemExit("Ni concurrent ni sujet à suivre dans sources.json : lance d'abord CONFIGURE-MOI.md.")
    return c


def collecter(config: dict, memoire: dict, dossier: Path, maintenant: datetime, telecharge=telecharger) -> dict:
    limite = maintenant - timedelta(days=int(config["jours"]))
    stats = {"lus": 0, "trop_vieux": 0, "deja_envoyes": 0, "hors_sujet": 0, "exclus": 0, "dans_le_futur": 0, "refus_robots": 0}
    erreurs: list[dict] = []
    gardes: list[dict] = []
    pages_modifiees: list[dict] = []
    emplois: list[dict] = []
    a_chercher: list[dict] = []
    snapshots: dict = {}
    compte_termes: dict = {}
    etendu = config.get("mode", "standard") == "etendu"
    strategique = config.get("strategique") or {}
    robots = Robots(telecharge, config.get("respecter_robots", True))
    noms_concurrents = [c["nom"] for c in config["concurrents"] if c.get("nom")]

    def erreur(source: str, url: str, e: Exception):
        if isinstance(e, RefusRobots):
            stats["refus_robots"] += 1
        erreurs.append({"source": source, "url": url, "erreur": str(e)[:200]})

    def lire_page(url: str) -> str:
        if not robots.permet(url):
            raise RefusRobots(url)
        return telecharge(url)

    def compter(titre: str):
        for t in set(termes_du_titre(titre)):
            compte_termes[t] = compte_termes.get(t, 0) + 1

    def traiter(articles: list[dict], concurrent: dict | None, exige_mention: bool, axe: str = "concurrents", mots: list[str] | None = None):
        for a in articles:
            stats["lus"] += 1
            compter(a["titre"])
            texte = f"{a['titre']} {a['extrait']}"
            if a["date"] and a["date"] < limite:
                stats["trop_vieux"] += 1
                continue
            if a["date"] and a["date"] > maintenant + timedelta(days=1):
                stats["dans_le_futur"] += 1
                a["date"] = None
            noms = [concurrent["nom"], *concurrent.get("alias", [])] if concurrent else (mots if mots is not None else noms_concurrents)
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
            a["axe"] = "concurrents" if a["concurrents"] else axe
            gardes.append(a)

    def chercher(requete: str, libelle: str, concurrent: dict | None, axe: str, mots: list[str] | None = None):
        """Mode étendu : les agrégateurs. Mode standard : la recherche est confiée à l'agent."""
        if not etendu:
            a_chercher.append({"axe": axe, "requete": requete, "pour": libelle})
            return
        for nom in config["agregateurs"]:
            try:
                traiter(lire_agregateur(nom, requete, config, telecharge), concurrent, exige_mention=True, axe=axe, mots=mots)
            except Exception as e:  # une source en panne n'arrête pas la veille
                erreur(f"{AGREGATEURS[nom]} « {libelle} »", "", e)

    for c in config["concurrents"]:
        nom = c["nom"].strip()
        # 1. Actualités qui citent le concurrent
        chercher(c.get("requete") or f'"{nom}"' + (" " + " ".join(c["mots_cles"]) if c.get("mots_cles") else ""), nom, c, "concurrents")
        # 2. Flux du concurrent (blog, salle de presse, notes de version)
        for url in c.get("flux", []):
            try:
                traiter(lire_flux(telecharge(url), nom), c, exige_mention=False)
            except Exception as e:
                erreur(f"Flux de {nom}", url, e)
        # 3. Pages surveillées (prix, offres, produit)
        for page in map(decrire_page, c.get("pages", [])):
            url = page["url"]
            try:
                lignes, _ = lignes_de_contenu(lire_page(url))
                lignes = filtrer_lignes(lignes, page["ignorer"])
                cle = empreinte(url_canonique(url))
                ancien_f = dossier / "memoire" / "pages" / f"{cle}.json"
                snapshots[cle] = {"url": url, "concurrent": nom, "lignes": lignes, "vu_le": maintenant.isoformat()}
                if not ancien_f.exists():
                    pages_modifiees.append({"concurrent": nom, "url": url, "premiere_visite": True, "ajouts": [], "retraits": []})
                    continue
                ancien = json.loads(ancien_f.read_text("utf-8"))
                ajouts, retraits = changements(filtrer_lignes(ancien.get("lignes", []), page["ignorer"]), lignes)
                if (ajouts or retraits) and concerne(ajouts + retraits, page["seulement_si"]):
                    pages_modifiees.append(
                        {"concurrent": nom, "url": url, "premiere_visite": False, "depuis": ancien.get("vu_le"), "intention": page["intention"], "ajouts": ajouts, "retraits": retraits}
                    )
            except Exception as e:
                erreur(f"Page de {nom}", url, e)
        # 4. Offres d'emploi, par l'API publique de l'outil de recrutement
        for url in c.get("emplois", []):
            try:
                api = api_emplois(url)
                if not api:
                    raise ValueError("page carrière non reconnue (Greenhouse, Lever et Ashby sont lus) : ajoute-la plutôt aux pages suivies")
                offres = lire_emplois(api[0], telecharge(api[1]))
                cle = "emplois-" + empreinte(url_canonique(url))
                ancien_f = dossier / "memoire" / "pages" / f"{cle}.json"
                snapshots[cle] = {"url": url, "concurrent": nom, "offres": offres, "vu_le": maintenant.isoformat()}
                if not ancien_f.exists():
                    emplois.append({"concurrent": nom, "url": url, "premiere_visite": True, "total": len(offres), "nouvelles": [], "retirees": []})
                    continue
                avant = {o["url"] or o["titre"]: o for o in json.loads(ancien_f.read_text("utf-8")).get("offres", [])}
                apres = {o["url"] or o["titre"]: o for o in offres}
                nouvelles = [o for k, o in apres.items() if k not in avant]
                retirees = [o["titre"] for k, o in avant.items() if k not in apres]
                if nouvelles or retirees:
                    emplois.append({"concurrent": nom, "url": url, "premiere_visite": False, "total": len(offres), "nouvelles": nouvelles[:30], "retirees": retirees[:30]})
            except Exception as e:
                erreur(f"Offres d'emploi de {nom}", url, e)

    # 5. Flux du secteur (médias, blogs) : seuls les articles qui citent un concurrent ou un mot-clé suivi
    mots_secteur = [m for c in config["concurrents"] for m in [c.get("nom", "")] + c.get("alias", [])] + config["mots_cles_secteur"]
    for url in config["flux_secteur"]:
        try:
            traiter(lire_flux(telecharge(url), domaine(url)), None, exige_mention=True, axe="tendances", mots=mots_secteur)
        except Exception as e:
            erreur("Flux du secteur", url, e)

    # 6. Veille stratégique : tendances du marché et réglementation
    for axe, libelle in (("tendances", "Tendances"), ("reglementation", "Réglementation")):
        reglage = strategique.get(axe) or {}
        mots = reglage.get("mots_cles", [])
        for url in reglage.get("flux", []):
            try:
                # sans mot-clé, tout le flux est gardé : c'est le cas d'un flux déjà très ciblé
                traiter(lire_flux(telecharge(url), domaine(url)), None, exige_mention=bool(mots), axe=axe, mots=mots)
            except Exception as e:
                erreur(f"{libelle} : flux", url, e)
        # La réglementation se suit aux sources officielles : une recherche d'actualités sur
        # « données » ou « IA » noierait la veille. Les tendances, elles, se cherchent.
        if axe == "tendances":
            for mot in mots:
                chercher(f'"{mot}"', mot, None, axe, mots=[mot])

    # 7. Appels d'offres : API officielles, sans clé
    appels: list[dict] = []
    ao = strategique.get("appels_offres") or {}
    if ao.get("mots_cles"):
        lecteurs = {
            "boamp": lambda: lire_boamp(telecharge(url_boamp(ao["mots_cles"], limite, ao.get("departements", [])))),
            "ted": lambda: lire_ted(telecharge(TED, corps_ted(ao["mots_cles"], limite, config["pays"]))),
        }
        for source in ao.get("sources", ["boamp", "ted"]):
            try:
                for avis in lecteurs[source]():
                    stats["lus"] += 1
                    if deja_vu({"lien": avis["url"], "titre": f"{avis['titre']} {avis['acheteur']}"}, memoire):
                        stats["deja_envoyes"] += 1
                        continue
                    if contient_mot_exclu(avis["titre"], config["mots_exclus"]):
                        stats["exclus"] += 1
                        continue
                    # un marché européen paraît au BOAMP et sur TED : on ne le garde qu'une fois
                    if any(titres_proches(cle_titre(avis["titre"]), cle_titre(x["titre"])) and x["acheteur"][:12].lower() == avis["acheteur"][:12].lower() for x in appels):
                        continue
                    avis["concurrents"] = [c for c in noms_concurrents if mentionne(avis.get("titulaire") or "", [c])]
                    appels.append(avis)
            except Exception as e:
                erreur(f"Appels d'offres ({source.upper()})", "", e)

    sujets = regrouper(gardes)
    stats["articles_retrouves"] = retrouver_originaux(sujets, telecharge) if config.get("retrouver_articles", True) else 0
    stats["doublons_regroupes"] = sum(s["doublons"] for s in sujets)
    sujets.sort(key=lambda s: (s["date"] is None, -(s["date"].timestamp() if s["date"] else 0)))
    # Les concurrents d'abord, jusqu'à max_sujets. Chaque autre axe a son propre plafond,
    # pour qu'un flux bavard ne chasse pas le reste.
    plafonds = {"concurrents": int(config["max_sujets"])}
    gardes_par_axe: dict = {}
    retenus = []
    for s in sujets:
        n = gardes_par_axe.get(s["axe"], 0)
        if n < plafonds.get(s["axe"], int(config.get("max_par_axe", 15))):
            gardes_par_axe[s["axe"]] = n + 1
            retenus.append(s)
    coupes = len(sujets) - len(retenus)
    sujets = retenus
    stats["coupes_au_dela_du_max"] = coupes
    stats["sujets"] = len(sujets)
    stats["pages_modifiees"] = sum(1 for p in pages_modifiees if not p["premiere_visite"])
    stats["appels_offres"] = len(appels)
    stats["emplois_modifies"] = sum(1 for x in emplois if not x["premiere_visite"])

    passages = charger_json(dossier / "memoire" / "termes.json", {"passages": []}).get("passages", [])
    historique = charger_json(dossier / "memoire" / "historique.json", {"entrees": []}).get("entrees", [])
    sortie = {
        "genere_le": maintenant.isoformat(),
        "mode": config.get("mode", "standard"),
        "periode": {"du": limite.date().isoformat(), "au": maintenant.date().isoformat(), "jours": int(config["jours"])},
        "stats": stats,
        "sujets": [
            {
                "id": f"s{i + 1}",
                "axe": s["axe"],
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
        "emplois": emplois,
        "appels_offres": appels[:40],
        "a_chercher": a_chercher,
        "sujets_qui_montent": sujets_qui_montent(compte_termes, passages),
        "historique": resume_historique(historique, maintenant),
        "erreurs": erreurs,
    }
    termes = dict(sorted(compte_termes.items(), key=lambda kv: -kv[1])[:400])
    return {"sortie": sortie, "snapshots": snapshots, "termes": termes}


def valider(dossier: Path, maintenant: datetime) -> str:
    """Après l'envoi : mémorise les sujets et l'état des pages pour ne pas les renvoyer."""
    f = dossier / "sortie" / "a-traiter.json"
    s = dossier / "sortie" / ".pages.json"
    if not f.exists():
        raise SystemExit("Rien à valider : lance d'abord la collecte.")
    data = json.loads(f.read_text("utf-8"))
    memoire = dossier / "memoire"
    memoire.mkdir(exist_ok=True)
    dernier = charger_json(memoire / "dernier-envoi.json", {})
    if dernier.get("genere_le") == data.get("genere_le"):
        return f"Déjà validé le {dernier.get('valide_le', '?')[:10]} : rien à refaire, et ce mail ne doit pas repartir."
    m = nettoyer_memoire(charger_memoire(dossier), maintenant)
    jour = maintenant.isoformat()
    n = 0
    for sujet in data["sujets"]:
        m["titres"][cle_titre(sujet["titre"])] = jour
        for src in sujet["sources"]:
            for url in (src.get("url"), src.get("url_google")):
                if url:
                    m["urls"][empreinte(url_canonique(url))] = jour
        n += 1
    for avis in data.get("appels_offres", []):
        m["urls"][empreinte(url_canonique(avis["url"]))] = jour
    (memoire / "deja-vu.json").write_text(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True), "utf-8")
    p = 0
    if s.exists():
        snaps = json.loads(s.read_text("utf-8"))
        (memoire / "pages").mkdir(parents=True, exist_ok=True)
        for cle, snap in snaps.items():
            (memoire / "pages" / f"{cle}.json").write_text(json.dumps(snap, ensure_ascii=False, indent=1), "utf-8")
            p += 1
    # termes lus à ce passage : la base de comparaison des « sujets qui montent »
    t = dossier / "sortie" / ".termes.json"
    if t.exists():
        passages = charger_json(memoire / "termes.json", {"passages": []}).get("passages", [])
        passages.append({"date": jour[:10], "termes": json.loads(t.read_text("utf-8"))})
        (memoire / "termes.json").write_text(json.dumps({"passages": passages[-12:]}, ensure_ascii=False), "utf-8")
    # ce qui a été envoyé, par concurrent et par rubrique : pour dire « c'est la 3e fois en 2 mois »
    r = dossier / "sortie" / "resume.json"
    if r.exists():
        resume = charger_json(r, {})
        par_url = {src.get("url"): sujet.get("concurrents", []) for sujet in data["sujets"] for src in sujet["sources"]}
        noms = sorted({c for sujet in data["sujets"] for c in sujet.get("concurrents", [])} | {x["concurrent"] for x in data.get("pages_modifiees", [])})
        entrees = charger_json(memoire / "historique.json", {"entrees": []}).get("entrees", [])
        limite = (maintenant - timedelta(days=2 * MEMOIRE_JOURS)).date().isoformat()
        for section in resume.get("sections", []):
            for info in section.get("infos", []):
                concurrents = sorted({c for src in info.get("sources", []) for c in par_url.get(src.get("url"), [])})
                if not concurrents:
                    concurrents = [c for c in noms if mentionne(f"{info.get('titre', '')} {info.get('texte', '')}", [c])]
                entrees.append({"date": info.get("date") or jour[:10], "rubrique": section.get("titre", "Autre"), "titre": info.get("titre", ""), "concurrents": concurrents})
        entrees = [x for x in entrees if (x.get("date") or "") >= limite]
        (memoire / "historique.json").write_text(json.dumps({"entrees": entrees}, ensure_ascii=False, indent=1), "utf-8")
    (memoire / "dernier-envoi.json").write_text(json.dumps({"genere_le": data.get("genere_le"), "valide_le": jour}), "utf-8")
    return f"Mémoire mise à jour : {n} sujets et {p} pages enregistrés."


AXES = ("concurrents", "tendances", "reglementation", "appels_offres")


def integrer(dossier: Path, maintenant: datetime) -> str:
    """Fait entrer dans a-traiter.json les articles que l'agent a trouvés par recherche web
    (sortie/trouvailles.json), avec les mêmes contrôles que le reste : vraie date dans la période,
    pas déjà envoyé, regroupé avec le sujet existant s'il s'agit de la même info."""
    f = dossier / "sortie" / "a-traiter.json"
    t = dossier / "sortie" / "trouvailles.json"
    if not f.exists():
        raise SystemExit("Lance d'abord la collecte : sortie/a-traiter.json n'existe pas.")
    if not t.exists():
        raise SystemExit("sortie/trouvailles.json introuvable : écris-y d'abord les articles trouvés.")
    try:
        trouvailles = json.loads(t.read_text("utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"trouvailles.json n'est pas un JSON valide (ligne {e.lineno}) : {e.msg}")
    if not isinstance(trouvailles, list):
        raise SystemExit("trouvailles.json doit être une liste d'articles.")
    data = json.loads(f.read_text("utf-8"))
    memoire = nettoyer_memoire(charger_memoire(dossier), maintenant)
    limite = maintenant - timedelta(days=int(data["periode"]["jours"]))
    bilan = {"ajoutes": 0, "regroupes": 0, "trop_vieux": 0, "deja_envoyes": 0, "invalides": 0, "deja_la": 0}
    sujets = data["sujets"]
    for a in trouvailles:
        titre, url = str(a.get("titre") or "").strip(), str(a.get("url") or "").strip()
        try:
            verifier_adresse(url)
        except AdresseRefusee:
            titre = ""
        if not titre:
            bilan["invalides"] += 1
            continue
        date = lire_date(a.get("date"))
        if date and date < limite:
            bilan["trop_vieux"] += 1
            continue
        if deja_vu({"lien": url, "titre": titre}, memoire):
            bilan["deja_envoyes"] += 1
            continue
        source = {"nom": a.get("media") or domaine(url), "url": url, "domaine": domaine(url), "origine": "recherche web"}
        cle, canon = cle_titre(titre), url_canonique(url)
        existant = next((x for x in sujets if any(url_canonique(src.get("url", "")) == canon for src in x["sources"])), None)
        if existant:
            bilan["deja_la"] += 1
            continue
        proche = next((x for x in sujets if titres_proches(cle, cle_titre(x["titre"]))), None)
        if proche:
            proche["sources"].append(source)
            if len(str(a.get("extrait") or "")) > len(proche.get("extrait") or ""):
                proche["extrait"] = str(a["extrait"])
            bilan["regroupes"] += 1
            continue
        concurrents = [c for c in (a.get("concurrents") or []) if isinstance(c, str)]
        sujets.append(
            {
                "id": f"t{sum(1 for x in sujets if x['id'].startswith('t')) + 1}",
                "axe": a.get("axe") if a.get("axe") in AXES else ("concurrents" if concurrents else "tendances"),
                "titre": titre,
                "date": date.date().isoformat() if date else None,
                "date_inconnue": date is None,
                "concurrents": concurrents,
                "extrait": str(a.get("extrait") or ""),
                "sources": [source],
            }
        )
        bilan["ajoutes"] += 1
    data["stats"]["sujets"] = len(sujets)
    data["stats"]["trouvailles"] = bilan
    f.write_text(json.dumps(data, ensure_ascii=False, indent=1), "utf-8")
    return (
        f"Recherche web intégrée : {bilan['ajoutes']} sujets ajoutés, {bilan['regroupes']} regroupés avec un sujet existant, "
        f"{bilan['trop_vieux']} trop vieux, {bilan['deja_envoyes']} déjà envoyés, {bilan['deja_la']} déjà présents, {bilan['invalides']} sans titre ou sans lien valide."
    )


def tester_sources(config: dict, telecharge=telecharger) -> list[str]:
    """Vérifie chaque source et propose les flux RSS trouvés sur les sites des concurrents."""
    rapport = []
    robots = Robots(telecharge, config.get("respecter_robots", True))

    def lire_page(url: str) -> str:
        if not robots.permet(url):
            raise RefusRobots(url)
        return telecharge(url)

    for c in config["concurrents"]:
        nom = c.get("nom", "?")
        suivies = [decrire_page(p)["url"] for p in c.get("pages", [])]
        if c.get("site"):
            try:
                page = lire_page(c["site"])
                _, flux = texte_de_page(page)
                flux = [urllib.parse.urljoin(c["site"], f) for f in flux]
                if flux:
                    rapport.append(f"OK   {nom} : site lu, flux trouvés : {', '.join(flux[:3])}")
                else:
                    rapport.append(f"OK   {nom} : site lu, aucun flux RSS annoncé (on surveillera ses pages)")
                pistes = [u for u in liens_utiles(page, c["site"]) if u not in suivies]
                if pistes:
                    rapport.append(f"     {nom} : pages à surveiller possibles : {', '.join(pistes)}")
            except RefusRobots:
                rapport.append(f"REFUS {nom} : le site demande aux robots de ne pas le lire (robots.txt). On suit ce concurrent par ses actualités.")
            except Exception as e:
                rapport.append(f"ERR  {nom} : site illisible ({str(e)[:80]})")
        for url in c.get("flux", []):
            try:
                n = len(lire_flux(telecharge(url), nom))
                rapport.append(f"OK   {nom} : flux {url} ({n} articles)")
            except Exception as e:
                rapport.append(f"ERR  {nom} : flux {url} ({str(e)[:80]})")
        for url in suivies:
            try:
                lignes, _ = lignes_de_contenu(lire_page(url))
                etat = "OK  " if len(lignes) >= 5 else "VIDE"
                rapport.append(f"{etat} {nom} : page {url} ({len(lignes)} lignes de texte)")
            except RefusRobots:
                rapport.append(f"REFUS {nom} : page {url} (interdite aux robots par le site : à retirer)")
            except Exception as e:
                rapport.append(f"ERR  {nom} : page {url} ({str(e)[:80]})")
        for url in c.get("emplois", []):
            try:
                api = api_emplois(url)
                if not api:
                    raise ValueError("page carrière non reconnue")
                n = len(lire_emplois(api[0], telecharge(api[1])))
                rapport.append(f"{'OK  ' if n else 'VIDE'} {nom} : {n} offres d'emploi lues ({api[0]})" + ("" if n else " : vérifie l'adresse de la page carrière"))
            except Exception as e:
                rapport.append(f"ERR  {nom} : offres d'emploi {url} ({str(e)[:80]})")
    strategique = config.get("strategique") or {}
    tous_les_flux = [("secteur", u) for u in config["flux_secteur"]]
    tous_les_flux += [(axe, u) for axe in ("tendances", "reglementation") for u in (strategique.get(axe) or {}).get("flux", [])]
    for axe, url in tous_les_flux:
        try:
            n = len(lire_flux(telecharge(url), url))
            rapport.append(f"OK   {axe} : {url} ({n} articles)")
        except Exception as e:
            rapport.append(f"ERR  {axe} : {url} ({str(e)[:80]})")
    ao = strategique.get("appels_offres") or {}
    if ao.get("mots_cles"):
        depuis = datetime.now(timezone.utc) - timedelta(days=30)
        essais = {
            "boamp": lambda: lire_boamp(telecharge(url_boamp(ao["mots_cles"], depuis, ao.get("departements", [])))),
            "ted": lambda: lire_ted(telecharge(TED, corps_ted(ao["mots_cles"], depuis, config["pays"]))),
        }
        for source in ao.get("sources", ["boamp", "ted"]):
            try:
                rapport.append(f"OK   appels d'offres {source.upper()} : {len(essais[source]())} avis sur 30 jours")
            except Exception as e:
                rapport.append(f"ERR  appels d'offres {source.upper()} ({str(e)[:80]})")
    return rapport


def diagnostic(dossier: Path, telecharge=telecharger) -> list[str]:
    """Vérifie l'installation étape par étape, avec quoi faire quand une étape échoue."""
    r = []
    v = sys.version_info
    r.append(f"OK   Python {v.major}.{v.minor}" if v >= (3, 9) else f"ERR  Python {v.major}.{v.minor} : il faut la version 3.9 ou plus récente")
    veille = dossier / "veille.md"
    if not veille.exists():
        r.append("ERR  veille.md introuvable : lance CONFIGURE-MOI.md")
    elif "{{" in veille.read_text("utf-8"):
        r.append("ERR  veille.md contient encore des {{à compléter}} : lance CONFIGURE-MOI.md")
    else:
        r.append("OK   veille.md rempli")
    try:
        config = lire_config(dossier)
        r.append(f"OK   sources.json lisible : {len(config['concurrents'])} concurrents, mode {config['mode']}")
    except SystemExit as e:
        return r + [f"ERR  {e}"]
    try:
        (dossier / "memoire").mkdir(exist_ok=True)
        essai = dossier / "memoire" / ".essai"
        essai.write_text("ok", "utf-8")
        essai.unlink()
        r.append("OK   dossier memoire/ accessible en écriture")
    except OSError as e:
        r.append(f"ERR  impossible d'écrire dans memoire/ ({e}) : vérifie les droits du dossier")
    if not any((dossier / n).exists() for n in ("modele-mail.html", "modeles")):
        r.append("ERR  modèle de mail introuvable : retélécharge le dossier de l'agent")
    try:
        telecharge("https://www.cnil.fr/fr/rss.xml")
        r.append("OK   accès à Internet")
    except Exception as e:
        return r + [f"ERR  pas d'accès à Internet depuis ce dossier ({str(e)[:80]}). Dans une tâche cloud : ouvre le réseau de l'environnement (accès « Full »)."]
    return r + tester_sources(config, telecharge)


def _json_defaut(o):
    if isinstance(o, datetime):
        return o.isoformat()
    if isinstance(o, set):
        return sorted(o)
    raise TypeError(type(o))


def main(argv: list[str] | None = None) -> int:
    for flux in (sys.stdout, sys.stderr):  # Windows : la console n'est pas en UTF-8 par défaut
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Collecte de l'agent de veille")
    ap.add_argument("--dossier", default=str(Path(__file__).resolve().parent.parent), help="dossier de l'agent")
    ap.add_argument("--valider", action="store_true", help="mémorise ce qui vient d'être envoyé")
    ap.add_argument("--test-sources", action="store_true", help="vérifie les sources sans rien collecter")
    ap.add_argument("--diagnostic", action="store_true", help="vérifie l'installation étape par étape")
    ap.add_argument("--integrer", action="store_true", help="ajoute à la collecte les articles de sortie/trouvailles.json")
    ap.add_argument("--maintenant", help="date et heure de référence (ISO 8601), pour les tests")
    a = ap.parse_args(argv)
    dossier = Path(a.dossier)
    now = maintenant_utc(a.maintenant)

    if a.valider:
        print(valider(dossier, now))
        return 0
    if a.integrer:
        print(integrer(dossier, now))
        return 0
    if a.diagnostic:
        lignes = diagnostic(dossier)
        print("\n".join(lignes))
        return 1 if any(l.startswith("ERR") for l in lignes) else 0
    config = lire_config(dossier)
    if a.test_sources:
        lignes = tester_sources(config)
        print("\n".join(lignes) or "Aucune source à tester.")
        return 1 if any(l.startswith("ERR") for l in lignes) else 0

    res = collecter(config, nettoyer_memoire(charger_memoire(dossier), now), dossier, now)
    (dossier / "sortie").mkdir(exist_ok=True)
    (dossier / "sortie" / "a-traiter.json").write_text(json.dumps(res["sortie"], ensure_ascii=False, indent=1, default=_json_defaut), "utf-8")
    (dossier / "sortie" / ".pages.json").write_text(json.dumps(res["snapshots"], ensure_ascii=False, default=_json_defaut), "utf-8")
    (dossier / "sortie" / ".termes.json").write_text(json.dumps(res["termes"], ensure_ascii=False), "utf-8")
    st = res["sortie"]["stats"]
    print(
        f"Collecte du {res['sortie']['periode']['du']} au {res['sortie']['periode']['au']} (mode {res['sortie']['mode']}) : "
        f"{st['lus']} articles lus, {st['sujets']} sujets gardés "
        f"({st['trop_vieux']} trop vieux, {st['deja_envoyes']} déjà envoyés, {st['hors_sujet']} hors sujet, "
        f"{st['exclus']} exclus, {st['doublons_regroupes']} doublons regroupés), "
        f"{st['pages_modifiees']} pages modifiées, {st['appels_offres']} appels d'offres, "
        f"{st['emplois_modifies']} pages emploi modifiées, {len(res['sortie']['erreurs'])} sources en erreur."
    )
    if res["sortie"]["a_chercher"]:
        print(f"{len(res['sortie']['a_chercher'])} recherches web à faire par l'agent (champ a_chercher).")
    print("Résultat : sortie/a-traiter.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
