#!/usr/bin/env python3
"""contenu.py : une page répond-elle clairement, avec des faits sourcés ?

Lit une page (URL, HTML ou Markdown), la découpe par titres (H1 à H3) et
contrôle chaque section, en français :

  réponse en tête   la première phrase répond (définition, chiffre, verbe
                    d'état), sans préambule (« dans cet article… »)
  autonome          ne commence ni par un pronom ni par un connecteur, ne
                    renvoie pas « plus haut »
  faits sourcés     chaque phrase chiffrée a une source dans la section
  première main     cas réel, donnée propre, expérience attribuée
  promesses         superlatifs et garanties à prouver (« n°1 », « le moins cher »)

Puis, pour la page : un seul H1, texte présent dans le HTML serveur, date
visible ou dans le JSON-LD, et la couverture des familles de faits qu'un
moteur va chercher pour la question visée (--question). Les familles sont
déduites du type de question : elles disent ce qui manque probablement,
pas ce qui fera citer la page.

Aucune note globale : une liste de contrôles réussis ou manqués, chacun
avec la phrase lue. Aucun de ces contrôles n'est un signal de classement
documenté ; ce sont des règles de clarté pour le lecteur.

  python3 contenu.py https://www.site.fr/guide/ --question "Combien coûte une mutuelle pour indépendant ?"
  python3 contenu.py article.md --json

Python 3 sans dépendance. Code 0 ; 1 si la page est illisible.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

ICI = Path(__file__).resolve().parent
for cand in (ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (cand / "page.py").exists():
        sys.path.insert(0, str(cand))
        break
import page as pg  # noqa: E402

# ---------------------------------------------------------------- lexiques

REPONSE = re.compile(
    r"\b(?:est|sont|designe(?:nt)?|correspond(?:ent)? a|consiste(?:nt)? a|signifie(?:nt)?|se definit|"
    r"represente(?:nt)?|coute(?:nt)?|vaut|valent|dure(?:nt)?|permet(?:tent)? de|couvre(?:nt)?|rembourse(?:nt)?|"
    r"depend(?:ent)? d[eu]|varie(?:nt)?|s'eleve(?:nt)? a|se calcule(?:nt)?|inclu(?:t|ent)|comprend|comprennent|"
    r"prevoi(?:t|ent)|oblige(?:nt)?|interdi(?:t|sent)|faut|suffit|fau(?:t|dra)|choisi(?:r|ssez)|compte(?:z|nt)?)\b")
PREAMBULE = re.compile(
    r"^(?:dans (?:cet|ce) (?:article|guide|billet|post)|nous allons|on va voir|vous allez decouvrir|"
    r"il est (?:important|essentiel|crucial|primordial) de|de nos jours|a l'heure (?:actuelle|ou)|"
    r"aujourd'hui,? (?:plus que jamais|de plus en plus)|vous vous demandez|vous etes nombreux|"
    r"bienvenue|avant de (?:repondre|commencer)|bonne question|tout d'abord, (?:il faut|rappelons))")
DEBUT_FAIBLE = re.compile(
    r"^(?:il|elle|ils|elles|cela|ceci|ca|celui-ci|celle-ci|on|mais|et|donc|cependant|toutefois|ainsi|"
    r"pourtant|en effet|de plus|par ailleurs|en outre|neanmoins|c'est|ce qui|ce dernier|cette derniere)\b")
RENVOI = re.compile(r"\b(?:(?:vu|indique|mentionne|explique|evoque|dit) (?:plus haut|precedemment|ci-dessus)|"
                    r"ci-dessus|plus haut|comme (?:nous l'avons|on l'a) vu|voir (?:plus haut|ci-dessous)|"
                    r"la section precedente|le paragraphe precedent)\b")
CHIFFRE = re.compile(r"(?<![\w])\d+(?:[  .,]\d+)*\s?(?:%|€|\$|euros?\b|ans?\b|mois\b|jours?\b|heures?\b|h\b|km\b|"
                     r"m²|k€|m€|millions?\b|milliards?\b)")
SOURCE = re.compile(r"\b(?:source ?:|sources ?:|etude|enquete|rapport|barometre|insee|eurostat|dares|"
                    r"drees|urssaf|acpr|amf|cnil|arcom|oms|service-public|legifrance|journal officiel|decret|"
                    r"article [lrd] ?\d|loi n|code (?:de la|des|du)|bofip)\b|https?://|\[\d+\]")
SELON = re.compile(r"\b(?:[Ss]elon|[Dd]'apr[eè]s) (?:l'|la |le |les |une |un |notre |nos )?(?:[A-ZÉ]|[ée]tude|enqu[êe]te|rapport|barom[èe]tre|donn[ée]es|chiffres)")
MOIS = r"(?:janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre)"
DATEE = re.compile(r"\b(?:au|en|depuis|le|du|mis a jour le|mise a jour le) (?:\d{1,2}(?:er)? )?" + MOIS + r" 20\d\d\b|\b20\d\d-\d\d-\d\d\b")
PROPRE = re.compile(r"\b(?:nous avons (?:mesure|analyse|compte|interroge|teste|constate|observe)|notre (?:etude|enquete|"
                    r"analyse|test|barometre)|nos (?:clients|donnees|chiffres|dossiers|mesures)|sur nos \d|"
                    r"dans notre (?:cabinet|agence|base)|nous constatons|nous observons|j'ai (?:teste|vu|accompagne)|"
                    r"(?:cas|exemple) (?:reel|client|concret)|temoignage)\b")
CITATION = re.compile(r"«[^»]{10,}»\s*,?\s*(?:explique|precise|indique|souligne|rappelle|selon)", re.I)
PROMESSE = re.compile(r"\b(?:n ?°\s?1|numero un|leader (?:du marche|francais|europeen)|le moins cher|la moins chere|"
                      r"les moins chers|le meilleur(?! moyen)|la meilleure(?! facon)|meilleur prix|prix le plus bas|"
                      r"garanti(?:e|s)? a vie|100 ?% (?:garanti|gratuit|satisfait|securise)|sans aucun risque|"
                      r"imbattable|incomparable|unique en france|recommande par (?:les|des) (?:experts|medecins))\b")
# Chiffres qui appellent une source : statistiques, pas les prix ni les délais de l'offre (/geo-exactitude)
STAT = re.compile(r"(?<![\w])\d+(?:[  .,]\d+)*\s?(?:%|pour ?cent\b|millions?\b|milliards?\b|m€)|"
                  r"\b\d+ (?:[a-z']+ ){0,2}sur \d+\b|\ben moyenne\b|\b\d+(?:,\d+)? fois plus\b")
QUESTION_TITRE = re.compile(r"^(?:comment|pourquoi|quel|quelle|quels|quelles|combien|qu'est-ce|que|quand|ou|faut-il|"
                            r"peut-on|est-ce)\b")

# Familles de faits par type de question (déduites, à confirmer par les sources citées dans /geo-visibilite)
FAMILLES = {
    "prix": [
        ("montant chiffré", r"\d[\d  .,]*\s?(?:€|euros?)"),
        ("période (par mois, par an)", r"par (?:mois|an|annee|jour|semaine)|mensuel|annuel|/ ?mois|/ ?an\b"),
        ("ce qui fait varier le prix", r"\b(?:depend|varie|selon (?:l'age|le profil|la formule|la region)|en fonction)"),
        ("ce qui est inclus ou exclu", r"\b(?:inclu|compris|exclu|hors|ne couvre pas|en option|supplement)"),
        ("date du tarif", r"\b(?:tarif|prix|grille)s? (?:au|en vigueur|de|du) .{0,20}20\d\d|\b(?:janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre) 20\d\d"),
    ],
    "comparaison": [
        ("critères nommés", r"\b(?:critere|prix|garantie|delai|frais|service|qualite)s?\b"),
        ("tableau ou liste comparative", r"__TABLEAU__"),
        ("verdict par profil (« pour qui »)", r"\b(?:pour (?:les|un|une|qui|vous)|si vous|ideal pour|adapte a|convient)"),
        ("limites de chaque option", r"\b(?:limite|inconvenient|defaut|moins|en revanche|mais)\b"),
    ],
    "procedure": [
        ("étapes numérotées", r"__LISTE__"),
        ("prérequis ou documents", r"\b(?:prerequis|document|piece|justificatif|avant de|il faut (?:avoir|disposer))"),
        ("durée ou délai", r"\d+\s?(?:minutes?|heures?|h\b|jours?|semaines?|mois)"),
        ("coût", r"\d[\d  .,]*\s?(?:€|euros?)|gratuit"),
        ("erreurs fréquentes", r"\b(?:erreur|piege|attention|eviter|oubli)"),
    ],
    "definition": [
        ("définition en une phrase", r"__DEFINITION__"),
        ("exemple", r"\b(?:par exemple|exemple|prenons|imaginons|cas)\b"),
        ("différence avec un terme voisin", r"\b(?:difference|a ne pas confondre|contrairement|alors que|tandis que)"),
        ("cadre légal ou source", SOURCE.pattern),
    ],
    "choix": [
        ("options nommées (marques, offres)", r"__NOMS__"),
        ("critères de choix", r"\b(?:critere|choisir|comparer|regarder|verifier)"),
        ("pour qui chaque option", r"\b(?:pour (?:les|un|une|qui)|si vous|ideal pour|adapte a|convient)"),
        ("prix ou fourchette", r"\d[\d  .,]*\s?(?:€|euros?)"),
        ("limites ou avis négatifs", r"\b(?:limite|inconvenient|defaut|en revanche|avis negatif|plainte)"),
    ],
}


def type_question(q: str) -> str:
    n = norm(q)
    brut = re.sub(r"\s+", " ", (q or "").lower())
    if re.search(r"\b(?:combien|prix|tarif|cout|coute|cher)\b", n):
        return "prix"
    if re.search(r"(?<![\wù])(?:ou|vs|versus|entre|difference|comparatif|comparer)(?![\wù])", brut.replace("différence", "difference")):
        return "comparaison"
    if re.search(r"^(?:comment|etapes?|demarche)|\b(?:comment|procedure|demarche|etapes?)\b", n):
        return "procedure"
    if re.search(r"^(?:qu'est-ce|c'est quoi|que (?:veut dire|signifie))|\b(?:definition|signifie)\b", n):
        return "definition"
    return "choix"


def norm(t: str) -> str:
    t = unicodedata.normalize("NFD", t or "")
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.replace("’", "'").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", t.lower()).strip()


def phrases(t: str) -> list[str]:
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý0-9«\"(])", t or "") if len(p.split()) >= 3]


# ---------------------------------------------------------------- découpage

BLOCS = {"p", "li", "td", "th", "div", "blockquote", "dd", "dt", "section", "article", "br", "tr", "main",
         "figcaption", "summary", "details"}
SAUTER = {"script", "style", "noscript", "nav", "footer", "header", "aside", "form", "template", "svg", "button"}


class Sections(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections = []
        self.cur = self._neuve("", 0)
        self.saut = 0
        self.titre = None
        self.para = []
        self.dans = 0           # profondeur li / td / th
        self.cache = 0          # profondeur sous un élément aria-hidden ou hidden (texte en double, animations)

    @staticmethod
    def _neuve(titre, niveau):
        return {"titre": titre, "niveau": niveau, "paras": [], "listes": 0, "tableaux": 0, "ol": 0, "premier": None}

    def _fin_para(self):
        t = " ".join(" ".join(self.para).split())
        if t:
            if self.cur["premier"] is None:
                self.cur["premier"] = "liste ou tableau" if self.dans else "texte"
            self.cur["paras"].append(t)
        self.para = []

    def handle_starttag(self, tag, attrs):
        if tag in SAUTER:
            self.saut += 1
            return
        if self.saut:
            return
        if tag in pg.VIDES:
            if tag == "br" and not self.cache:
                self._fin_para()
            return
        a = {k.lower(): (v or "") for k, v in attrs}
        if self.cache or a.get("aria-hidden") == "true" or "hidden" in a:
            self.cache += 1
            return
        if re.fullmatch(r"h[1-3]", tag):
            self._fin_para()
            self.sections.append(self.cur)
            self.cur = self._neuve("", int(tag[1]))
            self.titre = []
        elif tag in BLOCS:
            self._fin_para()
        if tag in ("li", "td", "th"):
            self.dans += 1
        if tag == "li":
            self.cur["listes"] += 1
        elif tag == "table":
            self.cur["tableaux"] += 1
        elif tag == "ol":
            self.cur["ol"] += 1

    def handle_endtag(self, tag):
        if tag in SAUTER:
            self.saut = max(0, self.saut - 1)
            return
        if self.saut:
            return
        if tag in pg.VIDES:
            return
        if self.cache:
            self.cache -= 1
            return
        if re.fullmatch(r"h[1-3]", tag) and self.titre is not None:
            self.cur["titre"] = " ".join(" ".join(self.titre).split())
            self.titre = None
        elif tag in BLOCS:
            self._fin_para()
        if tag in ("li", "td", "th"):
            self.dans = max(0, self.dans - 1)

    def handle_data(self, data):
        if self.saut or self.cache:
            return
        (self.titre if self.titre is not None else self.para).append(data)

    def fin(self):
        self._fin_para()
        self.sections.append(self.cur)
        return [s for s in self.sections if s["titre"] or s["paras"]]


def sections_markdown(texte: str) -> list[dict]:
    secs, cur, para, ol = [], Sections._neuve("", 0), [], False
    def fin():
        if para:
            cur["premier"] = cur["premier"] or "texte"
            cur["paras"].append(" ".join(para))
            para.clear()
    for ligne in texte.splitlines():
        m = re.match(r"^(#{1,3})\s+(.*)", ligne)
        if m:
            fin()
            secs.append(cur)
            cur = Sections._neuve(m.group(2).strip(), len(m.group(1)))
            continue
        if not ligne.strip():
            fin()
            continue
        if re.match(r"^\s*\|", ligne):
            fin()
            if re.match(r"^\s*\|[\s:|-]+\|?\s*$", ligne):
                continue
            cur["tableaux"] = 1
            cur["premier"] = cur["premier"] or "liste ou tableau"
            cur["paras"].append(" ".join(c.strip() for c in ligne.strip().strip("|").split("|")))
        elif re.match(r"^\s*(?:[-*•]|\d+[.)])\s+", ligne):
            fin()
            cur["listes"] += 1
            cur["premier"] = cur["premier"] or "liste ou tableau"
            if re.match(r"^\s*\d+[.)]", ligne):
                cur["ol"] = 1
            cur["paras"].append(re.sub(r"^\s*(?:[-*•]|\d+[.)])\s+", "", ligne).strip())
        else:
            para.append(ligne.strip())
    fin()
    secs.append(cur)
    return [s for s in secs if s["titre"] or s["paras"]]


# ---------------------------------------------------------------- contrôles

def controler(sec: dict) -> dict:
    texte = " ".join(sec["paras"])
    mots = len(re.findall(r"\w+", texte))
    ph = [x for para in sec["paras"] for x in phrases(para)] or ([texte] if texte else [])
    premiere = ph[0] if ph else ""
    p1 = norm(premiere)
    c = {}
    # réponse en tête
    if sec.get("premier") == "liste ou tableau":
        c["reponse"] = (True, "réponse en liste ou en tableau", "")
    elif PREAMBULE.search(p1):
        c["reponse"] = (False, "préambule avant la réponse", premiere)
    elif REPONSE.search(" ".join(p1.split()[:25])) or CHIFFRE.search(p1):
        c["reponse"] = (len(premiere.split()) <= 40, "réponse en tête" if len(premiere.split()) <= 40
                        else f"première phrase de {len(premiere.split())} mots", premiere)
    else:
        c["reponse"] = (False, "la première phrase ne répond pas (ni définition, ni fait)", premiere)
    # autonomie
    renvois = [p for p in ph if RENVOI.search(norm(p))]
    if DEBUT_FAIBLE.match(p1):
        c["autonome"] = (False, "commence par un pronom ou un connecteur", premiere)
    elif renvois:
        c["autonome"] = (False, "renvoie à une autre partie de la page", renvois[0])
    else:
        c["autonome"] = (True, "se lit seule", "")
    # faits sourcés
    chiffrees = [p for p in ph if STAT.search(norm(p))]
    a_source = bool(SOURCE.search(norm(texte)) or SELON.search(texte))
    datee = bool(DATEE.search(norm(texte)))
    if not chiffrees:
        c["sources"] = (None, "aucune statistique", "")
    elif a_source or datee:
        c["sources"] = (True, f"{len(chiffrees)} statistique(s), " + ("source citée" if a_source else "donnée datée"), "")
    else:
        c["sources"] = (False, f"{len(chiffrees)} statistique(s) sans source", chiffrees[0])
    propre = next((p for p in ph if PROPRE.search(norm(p)) or CITATION.search(p)), None)
    # promesses
    pr = [(p, PROMESSE.search(norm(p)).group(0)) for p in ph if PROMESSE.search(norm(p))]
    c["promesses"] = (not pr, f"à prouver : « {pr[0][1]} »" if pr else "aucune", pr[0][0] if pr else "")
    return {"titre": sec["titre"] or "(début de page)", "niveau": sec["niveau"], "mots": mots,
            "titre_question": bool(QUESTION_TITRE.match(norm(sec["titre"]))) or sec["titre"].strip().endswith("?"),
            "controles": c, "premiere_main": propre, "listes": sec["listes"], "tableaux": sec["tableaux"], "ol": sec["ol"]}


def couverture(question: str, secs: list[dict], texte: str) -> dict:
    t = type_question(question)
    n = norm(texte)
    out = []
    for nom, motif in FAMILLES[t]:
        if motif == "__TABLEAU__":
            ok = any(s["tableaux"] for s in secs) or sum(s["listes"] for s in secs) >= 3
        elif motif == "__LISTE__":
            ok = any(s["ol"] for s in secs)
        elif motif == "__DEFINITION__":
            ok = any(s["controles"]["reponse"][0] for s in secs)
        elif motif == "__NOMS__":
            ok = len(set(re.findall(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-zA-Z]{2,}(?:\s[A-Z][a-zA-Z]+)?", texte))) >= 3
        else:
            ok = bool(re.search(motif, n))
        out.append({"famille": nom, "presente": ok})
    return {"question": question, "type": t, "familles": out}


def analyser(source: str, html: str | None, md: str | None, entetes=None, question: str | None = None) -> dict:
    alertes = []
    if html is not None:
        p = Sections()
        try:
            p.feed(html)
            p.close()
        except Exception:  # noqa: BLE001
            pass
        brutes = p.fin()
        page = pg.analyser(html)
        h1 = [t for n, t in page["titres"] if n == 1]
        if len(h1) == 0:
            alertes.append("aucun H1")
        elif len(h1) > 1:
            dup = len(set(norm(x) for x in h1)) < len(h1)
            alertes.append(f"{len(h1)} H1" + (" dont un doublon exact (souvent un gabarit qui l'insère deux fois)" if dup else ""))
        if page["mots"] < 150:
            alertes.append(f"{page['mots']} mots dans le HTML serveur : contenu rendu en JavaScript ou page trop mince")
        dates = [o.get(k) for o in page["jsonld"] for k in ("dateModified", "datePublished") if o.get(k)]
        visible = re.search(r"(?i)(mis à jour|mise à jour|publié|actualisé)[^.]{0,30}\d{1,2}[ /.-]\w+[ /.-]20\d\d|20\d\d-\d\d-\d\d",
                            page["texte"])
        if not dates and not visible:
            alertes.append("aucune date de publication ou de mise à jour (visible ou JSON-LD)")
        titre_page = page["title"]
    else:
        brutes = sections_markdown(md or "")
        titre_page = next((s["titre"] for s in brutes if s["niveau"] == 1), "")
    secs = [controler(s) for s in brutes if len(re.findall(r"\w+", " ".join(s["paras"]))) >= 15]
    texte = " ".join(" ".join(s["paras"]) for s in brutes)
    r = {"source": source, "titre": titre_page, "sections": secs, "alertes": alertes}
    if question:
        r["couverture"] = couverture(question, secs, texte)
        mots_q = {w for w in re.findall(r"[a-z]{5,}", norm(question))}
        r["titre_repond"] = bool(mots_q & set(re.findall(r"[a-z]{5,}", norm(titre_page)))) if mots_q else None
    tot = {k: [0, 0] for k in ("reponse", "autonome", "sources", "promesses")}
    for s in secs:
        for k, (ok, _, _) in s["controles"].items():
            if ok is None:
                continue
            tot[k][1] += 1
            tot[k][0] += bool(ok)
    r["bilan"] = tot
    r["premiere_main"] = [{"section": s["titre"], "indice": s["premiere_main"]} for s in secs if s["premiere_main"]]
    if secs and not r["premiere_main"]:
        alertes.append("rien de propre au site (cas réel, donnée maison, expérience, citation attribuée) : "
                       "la page dit ce que disent les autres")
    return r


LIBELLES = {"reponse": "réponse en tête", "autonome": "autonome", "sources": "statistiques sourcées",
            "promesses": "sans promesse à prouver"}


def afficher(r: dict) -> str:
    L = [f"CONTENU · {r['source']} · {len(r['sections'])} sections de 15 mots ou plus", ""]
    if not r["sections"]:
        L.append("Aucune section lisible : contenu rendu en JavaScript, page vide ou bloquée.")
        return "\n".join(L)
    L.append("BILAN (sections qui passent le contrôle / sections concernées)")
    for k, (ok, n) in r["bilan"].items():
        L.append(f"  {LIBELLES[k]:<26}" + (f"{ok}/{n}" if n else "sans objet"))
    if r["premiere_main"]:
        L.append(f"  première main             {len(r['premiere_main'])} section(s), dont « {r['premiere_main'][0]['section'][:40]} » : « {r['premiere_main'][0]['indice'][:100]} »")
    if r["alertes"]:
        L += ["", "PAGE"] + [f"  ! {a}" for a in r["alertes"]]
    if "couverture" in r:
        c = r["couverture"]
        L += ["", f"FAMILLES DE FAITS · « {c['question']} » · type {c['type']} (déduit, pas observé)"]
        if r.get("titre_repond") is False:
            L.append("  ! le title ne reprend aucun mot de la question")
        for f in c["familles"]:
            L.append(f"  {'présente' if f['presente'] else 'ABSENTE ':<10}{f['famille']}")
    L += ["", "SECTIONS"]
    for s in r["sections"]:
        manque = [(k, v) for k, v in s["controles"].items() if v[0] is False]
        etat = "ok" if not manque else f"{len(manque)} à revoir"
        L.append(f"  {'#' * max(s['niveau'], 1)} {s['titre'][:70]} · {s['mots']} mots · {etat}")
        for k, (ok, motif, preuve) in manque:
            L.append(f"      ✗ {LIBELLES[k]} : {motif}" + (f"\n          « {preuve[:160]} »" if preuve else ""))
    L += ["", "Contrôles de clarté pour le lecteur, pas des signaux de classement documentés."]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Contrôles de clarté d'une page, section par section (français).")
    ap.add_argument("source", help="URL, fichier HTML ou Markdown")
    ap.add_argument("--question", help="question visée par la page, pour la couverture des familles de faits")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    html = md = None
    entetes = {}
    if re.match(r"https?://", a.source):
        lu = pg.lire(a.source)
        if lu["statut"] is None:
            print(f"Page non lue ({lu['erreur']}). Enregistre le HTML et relance sur le fichier.", file=sys.stderr)
            return 1
        if lu["statut"] >= 400:
            print(f"Page en {lu['statut']} pour le script (pare-feu ?). Enregistre le HTML depuis le navigateur.", file=sys.stderr)
            return 1
        html, entetes = lu["texte"], lu["entetes"]
    else:
        try:
            brut = pg.lire_fichier(a.source)
        except OSError as e:
            print(f"Erreur : {e}", file=sys.stderr)
            return 1
        if a.source.endswith((".html", ".htm")) or brut.lstrip().startswith("<"):
            html = brut
        else:
            md = brut
    r = analyser(a.source, html, md, entetes, a.question)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
