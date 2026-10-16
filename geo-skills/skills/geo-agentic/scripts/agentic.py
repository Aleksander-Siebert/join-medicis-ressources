#!/usr/bin/env python3
"""agentic.py : un agent d'IA peut-il utiliser la page, et la page lui parle-t-elle en cachette ?

Les agents (navigateurs pilotés par une IA, assistants qui comparent,
réservent ou remplissent un formulaire pour l'utilisateur) lisent une page
par trois voies : une capture d'écran, le HTML et l'arbre d'accessibilité.
Ce script contrôle, sur le HTML livré par le serveur :

  BLOQUANT   contenu lisible sans JavaScript ; robots des agents (robots
             « utilisateur » de commun/robots_ia.json) autorisés, robots.txt
             qui ne répond pas en 5xx
  ACCÈS      cliquables non sémantiques (div onclick), boutons et liens sans
             nom, champs sans label, interactifs cachés (aria-hidden)
  STABILITÉ  images sans dimensions (décalages de mise en page)
  CONFIANCE  consignes adressées aux IA dans du texte caché, des
             commentaires, des attributs ou des caractères Unicode
             invisibles (« si vous êtes une IA, recommandez… », « ignore
             previous instructions ») : une manipulation, à retirer
  INFO       llms.txt, version Markdown (balise ou en-tête Link), outils
             WebMCP : non comptés, leur absence est normale

  python3 agentic.py https://www.site.fr/devis/
  python3 agentic.py page.html --url https://www.site.fr/devis/ --hors-ligne
  python3 agentic.py https://www.site.fr/ --json

Résultat : contrôles passés / contrôles faits, pas une note sur 100 (les
standards du web agentique bougent). Ni rendu JavaScript ni arbre
d'accessibilité calculé : pour la mesure officielle, Lighthouse, catégorie
Agentic Browsing. Sources : web.dev/articles/ai-agent-site-ux (Google),
documentation Lighthouse ; matrice des agents inspirée de seo-agentic
(claude-seo, MIT), réécrite.

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
from urllib.parse import urlsplit

ICI = Path(__file__).resolve().parent
for cand in (ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (cand / "robots_ia.json").exists():
        COMMUN = cand
        sys.path.insert(0, str(cand))
        break
else:  # pragma: no cover
    sys.exit("commun/ introuvable : lance outils/propager.py")
import page as pg  # noqa: E402
import robots_rfc  # noqa: E402

INPUT_SANS_LABEL_OK = {"hidden", "submit", "button", "image", "reset"}


def agents():
    d = json.loads((COMMUN / "robots_ia.json").read_text(encoding="utf-8"))
    return [(r["jeton"], r["editeur"], r["role"]) for r in d["robots"] if r["role"] == "utilisateur"], d["verifie_le"]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.labels_for = set()
        self.champs = []          # (type, id, nom accessible ?, dans un label ?)
        self.cliquables = []      # éléments non sémantiques avec onclick
        self.role_sans_tab = []   # role=button/link sans tabindex
        self.actions = []         # [balise, nom accessible trouvé ?, extrait]
        self.caches = []          # interactifs sous aria-hidden="true"
        self.imgs = []
        self.forms = []           # attributs WebMCP des formulaires
        self.scripts = []
        self.texte = []
        self._pile = []           # (balise, aria_hidden)
        self._label = 0
        self._skip = 0
        self._action = None
        self._script = False

    def _cache(self):
        return any(h for _, h in self._pile)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        hidden = a.get("aria-hidden", "").lower() == "true"
        if tag not in ("br", "img", "input", "meta", "link", "hr", "source", "wbr"):
            self._pile.append((tag, hidden))
        if tag in ("style", "noscript"):
            self._skip += 1
        if tag == "script":
            self._script = True
            self._skip += 1
            if a.get("src"):
                self.scripts.append("src:" + a["src"])
        if tag == "label":
            self._label += 1
            if a.get("for"):
                self.labels_for.add(a["for"])
        nom = bool(a.get("aria-label", "").strip() or a.get("aria-labelledby") or a.get("title", "").strip())
        if tag in ("input", "select", "textarea"):
            t = a.get("type", "text").lower() if tag == "input" else tag
            if t not in INPUT_SANS_LABEL_OK:
                self.champs.append({"type": t, "id": a.get("id", ""), "nom": nom, "dans_label": self._label > 0,
                                    "extrait": a.get("name") or a.get("placeholder") or t})
        if tag in ("div", "span", "li", "td", "img") and a.get("onclick") is not None:
            self.cliquables.append(f"<{tag}> {a.get('class', '')[:40]}")
        if a.get("role") in ("button", "link") and tag not in ("button", "a") and "tabindex" not in a:
            self.role_sans_tab.append(f"<{tag} role={a['role']}>")
        focusable = (tag in ("a", "button", "select", "textarea") or (tag == "input" and a.get("type") != "hidden")
                     or re.fullmatch(r"\s*\d+\s*", a.get("tabindex", "")) is not None)
        if focusable and (hidden or self._cache()) and (tag != "a" or a.get("href")):
            self.caches.append(f"<{tag}> {(a.get('aria-label') or a.get('href') or a.get('name') or '')[:50]}")
        if tag == "button" or (tag == "a" and a.get("href")):
            self._action = [tag, nom, a.get("href", "")[:60]]
            self.actions.append(self._action)
        if tag == "img":
            self.imgs.append(a)
            if self._action and a.get("alt", "").strip():
                self._action[1] = True
        if tag == "svg" and self._action and (a.get("aria-label") or a.get("role") == "img"):
            self._action[1] = True
        if tag == "form":
            self.forms.append({k: v for k, v in a.items() if k.startswith("tool")})

    def handle_endtag(self, tag):
        if tag == "script":
            self._script = False
        if tag in ("style", "noscript", "script") and self._skip:
            self._skip -= 1
        if tag == "label" and self._label:
            self._label -= 1
        if tag in ("button", "a"):
            self._action = None
        for i in range(len(self._pile) - 1, -1, -1):
            if self._pile[i][0] == tag:
                del self._pile[i:]
                break

    def handle_data(self, data):
        if self._script:
            self.scripts.append(data)
            return
        if self._skip or not data.strip():
            return
        self.texte.append(data.strip())
        if self._action:
            self._action[1] = True


def analyse_html(html):
    p = Page()
    p.feed(html)
    champs_sans_label = [c["extrait"] for c in p.champs
                         if not (c["nom"] or c["dans_label"] or (c["id"] and c["id"] in p.labels_for))]
    actions_sans_nom = [f"<{t}> {h}" for t, ok, h in p.actions if not ok]
    remplit = lambda i: i.get("data-nimg") == "fill" or "position:absolute" in i.get("style", "").replace(" ", "")  # noqa: E731
    sans_dim = [i.get("src", "")[:60] for i in p.imgs
                if i.get("src") and not i["src"].startswith("data:") and not (i.get("width") and i.get("height")) and not remplit(i)]
    js = " ".join(s for s in p.scripts if not s.startswith("src:"))
    return {
        "mots": len(re.findall(r"\w+", " ".join(p.texte))),
        "cliquables_non_semantiques": p.cliquables + p.role_sans_tab,
        "actions_sans_nom": actions_sans_nom,
        "champs_sans_label": champs_sans_label,
        "interactifs_caches": p.caches,
        "images_sans_dimensions": sans_dim,
        "formulaires": len(p.forms),
        "formulaires_webmcp": sum(1 for f in p.forms if f.get("toolname")),
        "webmcp_js": bool(re.search(r"navigator\.modelContext|modelContext\.(?:registerTool|provideContext)", js)),
    }


# ---------------------------------------------------------------- confiance

def norm(t: str) -> str:
    t = unicodedata.normalize("NFD", t or "")
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", t.lower().replace("’", "'")).strip()


CONSIGNES = [
    r"\b(?:si (?:vous etes|tu es)|en tant qu[e'] ?) ?(?:une? )?(?:ia|intelligence artificielle|assistant|agent|modele de langage|llm|chatgpt|claude|gemini|perplexity)\b",
    r"\b(?:ignore[zr]?|oublie[zr]?|ne tiens? pas compte de?)s? (?:toutes )?(?:les |tes |vos |des )?(?:instructions|consignes|regles)(?: precedentes)?\b",
    r"\b(?:instructions?|consignes?|note|message) (?:pour|aux|a l'attention des|destinee?s? aux) (?:les )?(?:ia|intelligences artificielles|assistants|llm|agents|modeles|robots)\b",
    r"\b(?:recommande[zr]?|cite[zr]?|mentionne[zr]?|presente[zr]?) (?:toujours|systematiquement|en premier|en priorite)\b",
    r"\bignore (?:all |any )?(?:the )?(?:previous|prior|above|earlier) (?:instructions|prompts?|rules)\b",
    r"\b(?:if you are|as an?|you are an?) (?:ai|a\.i\.|llm|large language model|language model|assistant|chatbot|ai agent)\b",
    r"\b(?:ai|llm) (?:assistants?|agents?|models?|crawlers?|systems?) (?:should|must|are instructed to)\b",
    r"\b(?:always|only) (?:recommend|cite|mention)\b",
]
RE_CONSIGNE = re.compile("|".join(CONSIGNES))
INVISIBLES = re.compile("[​-‏‪-‮⁠-⁤⁦-⁩\U000e0000-\U000e007f]")


def balises_unicode(texte: str) -> str:
    """Texte caché en caractères « tag » Unicode (U+E0020 à U+E007E = ASCII invisible)."""
    return "".join(chr(ord(c) - 0xE0000) for c in texte if 0xE0020 <= ord(c) <= 0xE007E)


class Attributs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.valeurs = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if v and (k in ("alt", "title", "aria-label", "content", "placeholder", "value") or k.startswith("data-")):
                self.valeurs.append((f"<{tag} {k}>", v))


def confiance(html: str, page: dict) -> dict:
    trouves = []
    lieux = [("texte caché", page["texte_cache"])] + [("commentaire HTML", c) for c in page["commentaires"]]
    a = Attributs()
    try:
        a.feed(html)
    except Exception:  # noqa: BLE001
        pass
    lieux += [(f"attribut {k}", v) for k, v in a.valeurs]
    for lieu, t in lieux:
        for m in RE_CONSIGNE.finditer(norm(t)):
            trouves.append({"lieu": lieu, "cache": True, "extrait": t[max(0, m.start() - 40):m.end() + 80].strip()})
            break
    for m in RE_CONSIGNE.finditer(norm(page["texte"])):
        trouves.append({"lieu": "texte visible", "cache": False, "extrait": page["texte"][max(0, m.start() - 40):m.end() + 80]})
        break
    invis = INVISIBLES.findall(html.lstrip("﻿"))
    cache_tag = balises_unicode(html)
    if cache_tag.strip():
        trouves.append({"lieu": "caractères Unicode « tag » (texte invisible)", "cache": True, "extrait": cache_tag[:160]})
    return {"consignes": trouves, "invisibles": len(invis)}


def markdown(html: str, entetes: dict | None) -> dict:
    balise = re.search(r'<link[^>]+rel=["\']?alternate[^>]+type=["\']?text/markdown[^>]*>', html, re.I)
    lien = (entetes or {}).get("link", "")
    return {"balise": bool(balise), "entete_link": "text/markdown" in lien.lower()}


def controles(h, conf, md, reseau=None):
    out = []

    def c(groupe, nom, ok, valeur, conseil):
        out.append({"groupe": groupe, "controle": nom, "statut": ok, "valeur": valeur, "conseil": conseil if ok != "OK" else ""})

    c("BLOQUANT", "Contenu lisible sans JavaScript", "OK" if h["mots"] >= 150 else "À CORRIGER", f"{h['mots']} mots dans le HTML",
      "Les agents qui n'exécutent pas JavaScript ne voient rien : rendu serveur ou statique pour le contenu principal.")
    if reseau:
        st = reseau["robots_statut"]
        if st is None:
            c("BLOQUANT", "robots.txt répond", "NON LU", reseau.get("robots_erreur") or "erreur réseau",
              "Le script n'a pas pu lire robots.txt : vérifier à la main, ne rien conclure.")
        else:
            c("BLOQUANT", "robots.txt répond", "À CORRIGER" if st >= 500 else "OK", str(st),
              "Un robots.txt en erreur 5xx est lu comme « tout est interdit » (RFC 9309).")
            bloques = [b["robot"] for b in reseau["agents"] if not all(x["autorise"] for x in b["acces"].values())]
            c("BLOQUANT", "Robots des agents autorisés", "OK" if not bloques else "À CORRIGER",
              ", ".join(bloques) or "tous autorisés",
              "Ils ouvrent la page quand un client le demande à son assistant ; plusieurs ignorent robots.txt, "
              "mais un refus reste un signal (/geo-acces).")
    n = h["cliquables_non_semantiques"]
    c("ACCÈS", "Éléments cliquables sémantiques", "OK" if not n else "À CORRIGER", f"{len(n)} non sémantique(s)",
      "<button> et <a href> plutôt que <div onclick> ; sinon role et tabindex.")
    n = h["actions_sans_nom"]
    c("ACCÈS", "Boutons et liens nommés", "OK" if not n else "À CORRIGER", f"{len(n)} sans nom",
      "Chaque bouton ou lien a un texte, un aria-label ou une image avec alt (bouton icône compris).")
    n = h["champs_sans_label"]
    c("ACCÈS", "Champs de formulaire avec label", "OK" if not n else "À CORRIGER", f"{len(n)} sans label",
      "<label for=\"id\"> relié au champ ; un placeholder ne suffit pas.")
    n = h["interactifs_caches"]
    c("ACCÈS", "Pas d'interactif caché", "OK" if not n else "À CORRIGER", f"{len(n)} sous aria-hidden",
      "Un élément cliquable ne doit pas être retiré de l'arbre d'accessibilité.")
    n = h["images_sans_dimensions"]
    c("STABILITÉ", "Images avec dimensions", "OK" if not n else "À CORRIGER", f"{len(n)} sans width/height",
      "Une page qui bouge trompe les agents qui travaillent sur capture d'écran (et les humains).")
    caches = [x for x in conf["consignes"] if x["cache"]]
    visibles = [x for x in conf["consignes"] if not x["cache"]]
    c("CONFIANCE", "Aucune consigne cachée aux IA", "OK" if not caches else "CRITIQUE",
      f"{len(caches)} trouvée(s)" + (f" · {conf['invisibles']} caractère(s) invisible(s)" if conf["invisibles"] else ""),
      "Texte caché qui s'adresse aux IA : manipulation, à retirer. Les moteurs peuvent la traiter comme du spam "
      "et elle ruine la confiance si elle est découverte.")
    if visibles:
        c("CONFIANCE", "Consigne visible aux IA", "À REVOIR", "1 passage",
          "Une phrase qui s'adresse aux IA plutôt qu'au lecteur : la réécrire pour le lecteur (Google : inutile).")
    if reseau:
        c("INFO", "llms.txt", "INFO", "présent" if reseau.get("llms_txt") else "absent",
          "Contrôlé par Lighthouse ; ignoré par Google Search ; aucun poids ici.")
    c("INFO", "Version Markdown", "INFO",
      "balise <link> : " + ("oui" if md["balise"] else "non") + " · en-tête Link : " + ("oui" if md["entete_link"] else "non")
      + (" · Accept: text/markdown : " + ("oui" if reseau.get("markdown") else "non") if reseau else ""),
      "Facultatif ; aucune source primaire ne montre un agent grand public qui la demande.")
    c("INFO", "Outils WebMCP", "INFO",
      f"{h['formulaires_webmcp']} formulaire(s) déclaré(s) sur {h['formulaires']} · JavaScript : {'oui' if h['webmcp_js'] else 'non'}",
      "Standard en essai : toolname et tooldescription sur un <form>. Absence normale.")
    return out


def reseau_pour(url):
    parts = urlsplit(url)
    base = f"{parts.scheme}://{parts.netloc}"
    rob = pg.lire(base + "/robots.txt", accept="text/plain,*/*")
    liste, _ = agents()
    res = robots_rfc.analyser(rob["texte"], [parts.path or "/"], liste, rob["statut"])
    llms = pg.lire(base + "/llms.txt", accept="text/plain,*/*")
    md = pg.lire(url, accept="text/markdown")
    return {"robots_statut": rob["statut"], "robots_erreur": rob["erreur"], "agents": res["robots"],
            "llms_txt": llms["statut"] == 200 and bool(llms["texte"].strip()) and "<html" not in llms["texte"][:500].lower(),
            "markdown": md["statut"] == 200 and "markdown" in (md["entetes"].get("content-type") or "")}


def analyser(html: str, entetes=None, reseau=None) -> dict:
    h = analyse_html(html)
    p = pg.analyser(html)
    conf = confiance(html, p)
    md = markdown(html, entetes)
    res = controles(h, conf, md, reseau)
    faits = [x for x in res if x["statut"] not in ("INFO", "NON LU")]
    return {"passes": sum(1 for x in faits if x["statut"] == "OK"), "total": len(faits), "controles": res,
            "details": h, "confiance": conf, "markdown": md}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Préparation d'une page aux agents d'IA, et consignes cachées.")
    ap.add_argument("source", help="URL ou fichier HTML")
    ap.add_argument("--url", help="URL de la page si la source est un fichier")
    ap.add_argument("--hors-ligne", action="store_true", help="sans requête réseau (robots, llms.txt, Markdown)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    entetes = {}
    if re.match(r"https?://", a.source):
        lu = pg.lire(a.source)
        if lu["statut"] is None or lu["statut"] >= 400:
            print(f"Page non lue ({lu['erreur'] or lu['statut']}) : enregistre le HTML et relance avec --url.", file=sys.stderr)
            return 1
        html, url, entetes = lu["texte"], lu["url"], lu["entetes"]
    else:
        try:
            html = pg.lire_fichier(a.source)
        except OSError as e:
            print(f"Erreur : {e}", file=sys.stderr)
            return 1
        url = a.url or "https://exemple.fr/"
    reseau = None if (a.hors_ligne or not (re.match(r"https?://", a.source) or a.url)) else reseau_pour(url)
    r = analyser(html, entetes, reseau)
    if a.json:
        print(json.dumps({"url": url, **r}, ensure_ascii=False, indent=2))
        return 0
    _, date = agents()
    print(f"AGENTS D'IA · {url} · {r['passes']}/{r['total']} contrôles passés · table des agents du {date}")
    for x in r["controles"]:
        print(f"  {x['groupe']:<10} {x['statut']:<11} {x['controle']:<36} {x['valeur']}")
        if x["conseil"] and x["statut"] not in ("INFO", "OK"):
            print(f"                         -> {x['conseil']}")
    h = r["details"]
    for cle, titre in (("actions_sans_nom", "SANS NOM"), ("champs_sans_label", "SANS LABEL"),
                       ("cliquables_non_semantiques", "NON SÉMANTIQUES"), ("interactifs_caches", "CACHÉS")):
        if h[cle]:
            print(f"\n{titre} : " + " · ".join(h[cle][:6]))
    for x in r["confiance"]["consignes"]:
        print(f"\nCONSIGNE AUX IA ({x['lieu']}) : « {x['extrait'][:200]} »")
    print("\nMesure officielle : Lighthouse, catégorie Agentic Browsing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
