#!/usr/bin/env python3
"""
citability.py - un moteur génératif peut-il citer vos passages ?

Découpe une page (URL, HTML, Markdown ou texte) en sections et note chacune
sur 100, en français, selon cinq critères :

  RÉPONSE DIRECTE  30%  la première phrase répond (définition, chiffre, fait)
  AUTONOMIE        25%  le passage se comprend seul (sujet nommé, 50-200 mots,
                        pas de « Il », « Cela », « Mais » en tête)
  STRUCTURE        20%  titre (question si informationnel), paragraphes
                        courts, listes ou tableaux
  DONNÉES          15%  chiffres, dates, unités, sources citées
  ORIGINALITÉ      10%  données propres, cas réel, expérience, citation attribuée

    python3 citability.py https://www.site.fr/guide/
    python3 citability.py article.md --top 5
    python3 citability.py page.html --json

Heuristiques locales : elles repèrent la forme d'un passage citable, pas sa
vérité. Rubrique adaptée de geo-citability (geo-seo-claude, MIT), réécrite pour
le français.
"""

import argparse
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; JoinMedicis-citabilite/1.0; +https://joinmedicis.com)"
WEIGHTS = {"reponse": 0.30, "autonomie": 0.25, "structure": 0.20, "donnees": 0.15, "originalite": 0.10}
DEF = re.compile(r"\b(?:est|sont|désigne(?:nt)?|correspond(?:ent)? à|consiste(?:nt)? à|signifie(?:nt)?|se définit|"
                 r"représente(?:nt)?|coûte(?:nt)?|dure(?:nt)?|permet(?:tent)? de|couvre(?:nt)?|rembourse(?:nt)?|"
                 r"dépend(?:ent)? d[eu]|varie(?:nt)?|s'élève(?:nt)? à|se calcule(?:nt)?|inclu(?:t|ent)|comprend|"
                 r"comprennent|prévoi(?:t|ent)|oblige(?:nt)?|interdi(?:t|sent))\b", re.I)
WEAK_START = re.compile(r"^(?:il|elle|ils|elles|cela|ceci|ça|ce|cette|ces|celui|celle|on|mais|et|donc|cependant|"
                        r"toutefois|ainsi|pourtant|en effet|de plus|par ailleurs|en outre|néanmoins|c'est|ce qui)\b", re.I)
NUM = re.compile(r"\d+(?:[ .,]\d+)*\s?(?:%|€|\$|euros?|ans?|mois|jours?|heures?|h|km|m²|k€|M€|millions?|milliards?)?", re.I)
SOURCE = re.compile(r"\b(?:selon|d'après|source\s*:|étude|rapport|INSEE|Eurostat|OMS|CNIL|service-public|légifrance|"
                    r"décret|article L|loi n°)\b|https?://", re.I)
OWN = re.compile(r"\b(?:nous avons|notre (?:étude|enquête|analyse|équipe|expérience)|nos (?:clients|données|chiffres|"
                 r"dossiers)|chez nos|dans notre|nous constatons|nous observons|j'ai|mon expérience|nos experts)\b", re.I)
CASE = re.compile(r"\b(?:par exemple|exemple concret|cas (?:réel|client|concret)|prenons|imaginons)\b|«[^»]{10,}»\s*,?\s*(?:explique|précise|indique|selon)", re.I)


class Blocks(HTMLParser):
    """Sections d'une page HTML : titre (h1-h3) + texte des p, li, td jusqu'au titre suivant."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections, self.cur, self.stack, self.skip = [], {"titre": "", "niveau": 0, "texte": [], "listes": 0}, [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "nav", "footer", "header", "aside", "form"):
            self.skip += 1
        if tag in ("h1", "h2", "h3") and not self.skip:
            self._flush()
            self.cur = {"titre": "", "niveau": int(tag[1]), "texte": [], "listes": 0}
        if tag in ("li", "tr") and not self.skip:
            self.cur["listes"] += 1
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "nav", "footer", "header", "aside", "form") and self.skip:
            self.skip -= 1
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if self.skip or not data.strip():
            return
        cur = self.stack[-1] if self.stack else ""
        if cur in ("h1", "h2", "h3"):
            self.cur["titre"] += data.strip() + " "
        elif cur in ("p", "li", "td", "th", "blockquote", "dd", "span", "strong", "em", "a", "b"):
            self.cur["texte"].append(data.strip())

    def _flush(self):
        if self.cur["texte"] or self.cur["titre"]:
            self.sections.append(self.cur)

    def close(self):
        super().close()
        self._flush()


def from_markdown(text):
    sections, cur = [], {"titre": "", "niveau": 0, "texte": [], "listes": 0}
    for line in text.splitlines():
        m = re.match(r"^(#{1,3})\s+(.*)", line)
        if m:
            if cur["texte"] or cur["titre"]:
                sections.append(cur)
            cur = {"titre": m.group(2), "niveau": len(m.group(1)), "texte": [], "listes": 0}
        elif line.strip():
            if re.match(r"^\s*(?:[-*•]|\d+\.|\|)", line):
                cur["listes"] += 1
            cur["texte"].append(re.sub(r"^\s*(?:[-*•]|\d+\.)\s*", "", line).strip("| "))
    if cur["texte"] or cur["titre"]:
        sections.append(cur)
    return sections


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if len(s.split()) >= 3]


def score_block(sec):
    text = " ".join(sec["texte"]).strip()
    words = re.findall(r"\w+", text)
    n = len(words)
    sents = sentences(text)
    first = sents[0] if sents else text
    titre = sec["titre"].strip()
    notes, conseils = {}, []

    # 1. Réponse directe
    r = 0
    first_words = first.split()[:25]
    if DEF.search(" ".join(first_words)):
        r += 45
    if NUM.search(first):
        r += 20
    if 8 <= len(first.split()) <= 35:
        r += 20
    if titre.endswith("?") and r >= 45:
        r += 15
    notes["reponse"] = min(r, 100)
    if notes["reponse"] < 50:
        conseils.append("Ouvre la section par la réponse en une phrase (« X est… », « X coûte… », « X couvre… »).")

    # 2. Autonomie
    a = 0
    if first and not WEAK_START.match(first):
        a += 40
    else:
        conseils.append("La section commence par un pronom ou un connecteur : nomme le sujet dès la première phrase.")
    if 50 <= n <= 200:
        a += 35
    elif 30 <= n < 50 or 200 < n <= 300:
        a += 20
    else:
        conseils.append(f"{n} mots : vise des passages de 50 à 200 mots, chacun complet.")
    title_terms = {w.lower() for w in re.findall(r"\w{5,}", titre)}
    if title_terms and title_terms & {w.lower() for w in re.findall(r"\w{5,}", " ".join(first_words))}:
        a += 25
    elif re.search(r"(?<![.!?]\s)\b[A-ZÉ][a-zé]{2,}", text[1:]):
        a += 15
    notes["autonomie"] = min(a, 100)

    # 3. Structure
    s = 0
    if titre:
        s += 35
        if titre.endswith("?") or re.match(r"(?i)(?:comment|pourquoi|quel|quelle|quels|quelles|combien|qu'est-ce|que|quand|où)\b", titre):
            s += 20
    avg = n / max(len(sec["texte"]), 1)
    if avg <= 90:
        s += 25
    else:
        conseils.append("Paragraphes longs : découpe en blocs de 2 à 4 phrases.")
    if sec["listes"]:
        s += 20
    notes["structure"] = min(s, 100)

    # 4. Données
    nums = len(NUM.findall(text))
    srcs = len(SOURCE.findall(text))
    d = min(nums * 15, 60) + min(srcs * 20, 40)
    notes["donnees"] = min(d, 100)
    if nums == 0:
        conseils.append("Aucun chiffre : ajoute un fait vérifiable (montant, délai, date, pourcentage) avec sa source.")
    elif srcs == 0:
        conseils.append("Des chiffres sans source : cite l'organisme ou le texte d'origine.")

    # 5. Originalité
    o = min(len(OWN.findall(text)) * 40, 70) + min(len(CASE.findall(text)) * 30, 30)
    notes["originalite"] = min(o, 100)
    if o == 0:
        conseils.append("Rien de propre au site : ajoute un cas réel, une donnée maison ou une expérience de terrain.")

    total = sum(notes[k] * w for k, w in WEIGHTS.items())
    return {"titre": titre or "(sans titre)", "mots": n, "score": round(total), "notes": notes,
            "conseils": conseils[:3], "debut": first[:140]}


def load(source):
    if re.match(r"https?://", source):
        req = urllib.request.Request(source, headers={"User-Agent": UA, "Accept-Language": "fr-FR,fr;q=0.9"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode(r.headers.get_content_charset() or "utf-8", errors="replace"), "html"
    raw = open(source, encoding="utf-8", errors="replace").read()
    return raw, "html" if source.endswith((".html", ".htm")) or raw.lstrip().startswith("<") else "md"


def analyse(raw, kind):
    if kind == "html":
        p = Blocks()
        p.feed(raw)
        p.close()
        sections = p.sections
    else:
        sections = from_markdown(raw)
    blocks = [score_block(s) for s in sections if len(re.findall(r"\w+", " ".join(s["texte"]))) >= 15]
    total_words = sum(b["mots"] for b in blocks) or 1
    page = round(sum(b["score"] * b["mots"] for b in blocks) / total_words) if blocks else 0
    return {"score_page": page, "sections": blocks}


def main():
    ap = argparse.ArgumentParser(description="Score de citabilité par les moteurs génératifs (français).")
    ap.add_argument("source", help="URL, fichier HTML, Markdown ou texte")
    ap.add_argument("--top", type=int, default=3, help="nombre de sections fortes et faibles à montrer")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    raw, kind = load(args.source)
    r = analyse(raw, kind)
    if args.json:
        json.dump(r, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    secs = r["sections"]
    print(f"CITABILITÉ · {args.source} · {r['score_page']}/100 · {len(secs)} sections notées")
    if not secs:
        print("Aucune section lisible (contenu rendu en JavaScript ?).")
        return
    print("\nSECTIONS")
    for b in secs:
        n = b["notes"]
        print(f"  {b['score']:>3}  {b['titre'][:60]:<60} R{n['reponse']:>3} A{n['autonomie']:>3} S{n['structure']:>3} D{n['donnees']:>3} O{n['originalite']:>3}")
    print("\nÀ RÉÉCRIRE EN PRIORITÉ")
    for b in sorted(secs, key=lambda b: b["score"])[: args.top]:
        print(f"  {b['score']:>3}  {b['titre'][:70]}\n       début : « {b['debut']} »")
        for c in b["conseils"]:
            print(f"       -> {c}")
    print("\nR = réponse directe, A = autonomie, S = structure, D = données, O = originalité")


if __name__ == "__main__":
    main()
