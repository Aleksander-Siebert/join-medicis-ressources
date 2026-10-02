#!/usr/bin/env python3
"""
agentic.py - un agent d'IA peut-il utiliser votre page ?

Les agents (navigateurs pilotés par une IA, assistants qui réservent,
comparent ou remplissent un formulaire pour l'utilisateur) lisent une page
par trois voies : une capture d'écran, le HTML et l'arbre d'accessibilité.
Ce script contrôle, sur le HTML livré par le serveur :

  BLOQUANT  contenu lisible sans JavaScript, robots.txt qui ne répond pas en 5xx,
            robots des agents (ChatGPT-User, Claude-User…) autorisés
  ACCÈS     éléments cliquables non sémantiques (div onclick), boutons et liens
            sans nom, champs sans label, éléments interactifs cachés (aria-hidden)
  STABILITÉ images sans dimensions (décalages de mise en page)
  INFO      llms.txt, outils WebMCP (déclaratifs et en JavaScript), version
            Markdown de la page

    python3 agentic.py https://www.site.fr/devis/
    python3 agentic.py page.html --url https://www.site.fr/devis/ --hors-ligne
    python3 agentic.py https://www.site.fr/ --json

Le résultat est une fraction (contrôles passés / contrôles faits), comme la
catégorie « Agentic Browsing » de Lighthouse, et pas une note sur 100 : les
standards du web agentique sont encore en construction. Ce n'est pas
Lighthouse : il ne voit ni le rendu JavaScript ni l'arbre d'accessibilité
calculé par le navigateur. Pour la mesure officielle : Lighthouse, catégorie
Agentic Browsing (Chrome 150 ou plus).

Sources : web.dev/articles/ai-agent-site-ux (Google), documentation
Lighthouse Agentic Browsing. Inspiré de seo-agentic (claude-seo, MIT).
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

ICI = os.path.dirname(os.path.abspath(__file__))
for d in (os.path.join(ICI, "..", "geo-crawlers"),):
    sys.path.insert(0, d)
import crawlers  # noqa: E402

AGENTS = {"ChatGPT-User", "Claude-User", "Perplexity-User", "MistralAI-User"}
INPUT_SANS_LABEL_OK = {"hidden", "submit", "button", "image", "reset"}


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


def controles(h, reseau=None):
    """Transforme les mesures en contrôles OK / À CORRIGER / INFO."""
    out = []

    def c(groupe, nom, ok, valeur, conseil):
        out.append({"groupe": groupe, "controle": nom, "statut": ok, "valeur": valeur, "conseil": conseil if ok != "OK" else ""})

    c("BLOQUANT", "Contenu lisible sans JavaScript", "OK" if h["mots"] >= 150 else "À CORRIGER", f"{h['mots']} mots dans le HTML",
      "Les agents qui n'exécutent pas JavaScript ne voient rien : rendu serveur ou statique pour le contenu principal.")
    if reseau:
        st = reseau.get("robots_statut")
        c("BLOQUANT", "robots.txt répond", "À CORRIGER" if st and st >= 500 else "OK", str(st),
          "Un robots.txt en erreur 5xx est lu comme « tout est interdit » par les robots qui respectent la norme.")
        bloques = [b["robot"] for b in reseau.get("robots_ia", []) if b["robot"] in AGENTS and not all(b["acces"].values())]
        c("BLOQUANT", "Robots des agents autorisés", "OK" if not bloques else "À CORRIGER", ", ".join(bloques) or "tous autorisés",
          "Ces robots lisent la page quand un utilisateur le demande à son assistant : voir /geo-crawlers.")
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
    if reseau:
        llms = reseau.get("llms_txt")
        c("INFO", "llms.txt", "INFO", "présent" if llms else "absent",
          "Contrôlé par Lighthouse ; ignoré par Google Search. Facultatif.")
        md = reseau.get("markdown")
        c("INFO", "Version Markdown (Accept: text/markdown)", "INFO", "oui" if md else "non",
          "Facultatif : certains agents préfèrent une version Markdown de la page.")
    c("INFO", "Outils WebMCP", "INFO",
      f"{h['formulaires_webmcp']} formulaire(s) sur {h['formulaires']} déclaré(s) · JavaScript : {'oui' if h['webmcp_js'] else 'non'}",
      "Standard en essai (origin trial Chrome) : toolname et tooldescription sur un <form> pour le déclarer aux agents.")
    return out


def reseau_pour(url, html_headers=None):
    parts = urlsplit(url)
    base = f"{parts.scheme}://{parts.netloc}"
    st_r, _, robots_txt, _ = crawlers.try_fetch(base + "/robots.txt")
    bots, _ = crawlers.robots_rules(base, robots_txt if st_r == 200 else "", [parts.path or "/"])
    st_l, _, llms, _ = crawlers.try_fetch(base + "/llms.txt")
    md = False
    try:
        req = urllib.request.Request(url, headers={"User-Agent": crawlers.UA, "Accept": "text/markdown"})
        with urllib.request.urlopen(req, timeout=15) as r:
            md = "markdown" in (r.headers.get("Content-Type") or "")
    except Exception:  # noqa: BLE001
        pass
    return {"robots_statut": st_r, "robots_ia": bots, "llms_txt": st_l == 200 and bool(llms.strip()), "markdown": md}


def main():
    ap = argparse.ArgumentParser(description="Préparation d'une page aux agents d'IA.")
    ap.add_argument("source", help="URL ou fichier HTML")
    ap.add_argument("--url", help="URL de la page si la source est un fichier")
    ap.add_argument("--hors-ligne", action="store_true", help="sans requête réseau (robots, llms.txt, Markdown)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if re.match(r"https?://", args.source):
        st, _, html, url = crawlers.try_fetch(args.source)
        if st != 200:
            sys.exit(f"Page illisible ({st})")
    else:
        html, url = open(args.source, encoding="utf-8", errors="replace").read(), args.url or "https://exemple.fr/"
    h = analyse_html(html)
    res = controles(h, None if args.hors_ligne else reseau_pour(url))
    faits = [x for x in res if x["statut"] != "INFO"]
    ok = sum(1 for x in faits if x["statut"] == "OK")
    if args.json:
        json.dump({"url": url, "passes": ok, "total": len(faits), "controles": res, "details": h}, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    print(f"AGENTS D'IA · {url} · {ok}/{len(faits)} contrôles passés")
    for x in res:
        print(f"  {x['groupe']:<9} {x['statut']:<10} {x['controle']:<38} {x['valeur']}")
        if x["conseil"] and x["statut"] != "INFO":
            print(f"                       -> {x['conseil']}")
    for cle, titre in (("actions_sans_nom", "SANS NOM"), ("champs_sans_label", "SANS LABEL"),
                       ("cliquables_non_semantiques", "NON SÉMANTIQUES"), ("interactifs_caches", "CACHÉS")):
        if h[cle]:
            print(f"\n{titre} : " + " · ".join(h[cle][:6]))
    print("\nMesure officielle : Lighthouse, catégorie Agentic Browsing (Chrome 150+).")


if __name__ == "__main__":
    main()
