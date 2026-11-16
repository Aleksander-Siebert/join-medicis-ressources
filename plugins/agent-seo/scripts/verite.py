#!/usr/bin/env python3
"""
verite.py : l'article ne dit rien de ta marque qui ne soit dans site-context.md.

Python 3.9+ sans dépendance. Contrôle mécanique, avant toute relecture :

- chaque phrase qui parle de la marque (son nom, « notre », « nous ») et
  contient un chiffre, un prix ou un pourcentage doit retrouver ce chiffre
  dans les données produit LIVE de site-context.md (§7) ; un fait RETIRÉ ou
  À CONFIRMER ne s'affirme pas ;
- aucun mot interdit de site-context.md (§6) n'apparaît dans l'article ;
- les adresses du site citées dans l'article figurent dans site-context.md
  (§1 et §4) ou dans la liste des pages du site.

Ce qui manque ne s'invente pas : l'agent écrit {{à compléter}} ou retire la
phrase. Idée reprise de seo-agent-kit (facts.json, MIT).

Utilisation :
  python3 scripts/verite.py articles/2026-11-16-decennale/article.md --marque Assurly
Codes de sortie : 0 rien à signaler · 3 bloquant · 1 erreur d'utilisation.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

CHIFFRE = re.compile(r"(?<![\w.,])(\d{1,3}(?:[   .]\d{3})+|\d+)(?:[.,](\d+))?\s?(€|euros?|%|ht|ttc|mois|ans?|jours?|h\b)?", re.I)


def plier(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def valeurs(texte: str) -> set[str]:
    """Les nombres d'un texte, écrits d'une seule façon (« 1 200,50 » et « 1200.5 » sont égaux)."""
    sortie = set()
    for m in CHIFFRE.finditer(texte):
        entier = re.sub(r"[   .]", "", m.group(1))
        dec = (m.group(2) or "").rstrip("0")
        sortie.add(entier.lstrip("0") or "0" if not dec else f"{entier.lstrip('0') or '0'},{dec}")
    return sortie


def phrases(texte: str) -> list[str]:
    texte = re.sub(r"```.*?```", " ", texte, flags=re.S)  # blocs techniques (contrôles) hors champ
    texte = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", texte)
    morceaux = re.split(r"(?<=[.!?])\s+|\n+", texte)
    return [m.strip(" -*>#|") for m in morceaux if m.strip(" -*>#|")]


def _section(texte: str, numero: str) -> str:
    m = re.search(rf"^##\s*{numero}\..*?$(.*?)(?=^##\s|\Z)", texte, re.M | re.S)
    return m.group(1) if m else ""


def _lignes_tableau(bloc: str) -> list[list[str]]:
    rangs = []
    for l in bloc.splitlines():
        if l.strip().startswith("|") and not re.match(r"^\|\s*:?-{2,}", l.strip()):
            rangs.append([c.strip() for c in l.strip().strip("|").split("|")])
    return rangs[1:]  # sans l'en-tête


def lire_faits(chemin: Path) -> dict:
    """Les faits que l'article a le droit d'affirmer sur la marque, lus dans site-context.md :
    §7 données produit (lignes LIVE seulement), §4 pages à pousser et §1 site (adresses connues),
    §6 règles maison (mots interdits). Un fichier sans ces sections est lu en entier."""
    texte = chemin.read_text("utf-8")
    produit = _section(texte, "7")
    if produit:
        vrais = [r for r in _lignes_tableau(produit) if any(plier(c).startswith("live") for c in r)]
        source_valeurs = " ".join(" ".join(r[:2]) for r in vrais)
        retires = [r for r in _lignes_tableau(produit) if any(plier(c).startswith(("retire", "a confirmer")) for c in r)]
    else:
        source_valeurs, retires = texte, []
    interdits = []
    regles = _section(texte, "6") or texte
    for m in re.finditer(r"mots interdits[^:]*:\*{0,2}\s*(.+)", regles, re.I):
        interdits += [w.strip(" «»\"'.") for w in re.split(r"[,;]", m.group(1)) if w.strip(" «»\"'.") and "{{" not in w and "(" not in w]
    section = None
    for ligne in texte.splitlines():
        if ligne.startswith("#"):
            section = plier(ligne)
            continue
        if section and "interdit" in section and ligne.strip().startswith(("-", "*")):
            mot = ligne.strip()[1:].strip().strip("«»\"' ")
            if mot and "{{" not in mot:
                interdits.append(mot)
    urls = set(re.findall(r"https?://[^\s)>\]|]+", (_section(texte, "1") + _section(texte, "4")) if produit else texte))
    return {"texte": texte, "valeurs": valeurs(source_valeurs), "interdits": interdits, "urls": urls,
            "retires": valeurs(" ".join(" ".join(r[:2]) for r in retires)) - valeurs(source_valeurs)}


def controler(article: str, faits: dict, marque: str, pages: set[str] = frozenset()) -> list[str]:
    bloquants = []
    m_marque = re.compile(rf"\b({re.escape(plier(marque))}|nous|notre|nos)\b") if marque else re.compile(r"\b(nous|notre|nos)\b")
    for ph in phrases(article):
        if "{{" in ph:
            continue
        if not m_marque.search(plier(ph)):
            continue
        manquants = sorted(v for v in valeurs(ph) if v not in faits["valeurs"])
        for v in manquants:
            if v in faits.get("retires", set()):
                bloquants.append(f"« {ph[:140]} » : {v} est RETIRÉ ou À CONFIRMER dans site-context.md (§7) : ne l'affirme pas.")
            else:
                bloquants.append(f"« {ph[:140]} » : {v} absent des données produit LIVE de site-context.md (§7). Ajoute le fait avec sa source, ou écris {{{{à compléter}}}}.")
    art = plier(article)
    for mot in faits["interdits"]:
        if re.search(rf"\b{re.escape(plier(mot))}\b", art):
            bloquants.append(f"Mot interdit par site-context.md : « {mot} ».")
    domaine = None
    for u in faits["urls"]:
        d = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
        domaine = domaine or d
    if domaine:
        connues = {u.rstrip("/") for u in faits["urls"] | set(pages)}
        for u in re.findall(rf"https?://(?:www\.)?{re.escape(domaine)}[^\s)>\]]*", article):
            if u.rstrip("/.,") not in connues and not any(u.rstrip("/.,").startswith(c) and c.count("/") > 3 for c in connues):
                bloquants.append(f"Lien interne inconnu : {u}. Utilise une page qui existe (site-context.md ou liste des pages), ou retire le lien.")
    return bloquants


def main(argv: list[str] | None = None) -> int:
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Ce que l'article dit de la marque est-il dans site-context.md ?")
    ap.add_argument("article")
    ap.add_argument("--faits", default="site-context.md", help="site-context.md (par défaut)")
    ap.add_argument("--marque", default="")
    ap.add_argument("--pages", help="liste des adresses du site (une par ligne) ou sitemap XML")
    a = ap.parse_args(argv)
    art, f = Path(a.article), Path(a.faits)
    for p in (art, f):
        if not p.exists():
            print(f"Fichier introuvable : {p}", file=sys.stderr)
            return 1
    faits = lire_faits(f)
    if not faits["valeurs"]:
        print("ATTENTION : aucune donnée produit LIVE dans site-context.md (§7) : aucun chiffre sur la marque ne peut être écrit.")
    pages = set()
    if a.pages and Path(a.pages).exists():
        t = Path(a.pages).read_text("utf-8")
        pages = set(re.findall(r"<loc>\s*([^<\s]+)", t)) or {l.strip() for l in t.splitlines() if l.strip().startswith("http")}
    bloquants = controler(art.read_text("utf-8"), faits, a.marque, pages)
    if not bloquants:
        print("VÉRITÉ PRODUIT · OK : rien sur la marque qui ne soit dans site-context.md.")
        return 0
    print(f"VÉRITÉ PRODUIT · BLOQUÉ · {len(bloquants)} point(s) :")
    for b in bloquants:
        print(f"- {b}")
    return 3


if __name__ == "__main__":
    sys.exit(main())
