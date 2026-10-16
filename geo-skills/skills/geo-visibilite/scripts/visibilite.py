#!/usr/bin/env python3
"""visibilite.py : mesurer la place d'une marque dans les réponses des IA.

Une réponse d'IA est un tirage : on pose chaque question plusieurs fois, on
colle les réponses, et le script en tire des taux avec leur marge d'erreur,
moteur par moteur. Il n'appelle aucune IA (sauf la commande `tavily`, en
option, avec l'accord explicite de l'utilisateur).

Commandes :

  portefeuille FICHIER.csv --marque M [--alias A]
      contrôle la liste de questions : part sans la marque (70 à 85% visés
      dans le cœur), témoins présents, doublons, questions orientées ;
      donne la version du cœur (empreinte), pour ne comparer que des mesures
      faites avec le même cœur.

  grille FICHIER.csv --moteur ChatGPT --moteur Perplexity [--passages 5]
      écrit le fichier à remplir : un en-tête par passage
      « === Moteur | id | question », la réponse se colle dessous.

  mesurer REPONSES.txt --marque M [--alias A] [--domaine m.fr]
          [--concurrent "Nom=alias1,alias2"]… [--portefeuille FICHIER.csv]
      taux de mention, de citation (lien vers le site), de recommandation et
      de mise en garde, avec intervalle à 95%, par moteur ; part de voix face
      aux concurrents nommés ; témoins ; questions perdues ; sources citées
      par classe.

  comparer AVANT.txt APRES.txt --marque M … [--portefeuille FICHIER.csv]
      compare deux périodes sur les seules questions communes :
      « hausse », « baisse » ou « pas de changement détectable ».

  tavily FICHIER.csv --accepte-tiers [--passages 1]
      option : pose les questions au moteur de réponse de Tavily (sans clé,
      débit limité) et écrit un fichier de réponses étiqueté
      « Tavily (approximation) ». Les questions partent chez un tiers ; ce
      n'est ni ChatGPT, ni Perplexity, ni Google.

Format des réponses collées (compatible v1) :

  === ChatGPT | P01 | Quel smartphone reconditionné acheter ?
  (réponse collée)
  === ChatGPT | P01 | Quel smartphone reconditionné acheter ?
  (deuxième passage, nouvelle conversation)

L'identifiant est facultatif (« === ChatGPT | question » marche aussi).
Les lignes avant le premier « === » sont ignorées.

Python 3 sans dépendance. Code de sortie 0, 1 en cas d'erreur d'entrée.
"""

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

ICI = Path(__file__).resolve().parent
for cand in (ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (cand / "stats.py").exists():
        COMMUN = cand
        break
else:  # pragma: no cover
    sys.exit("commun/stats.py introuvable : lance outils/propager.py")
sys.path.insert(0, str(COMMUN))
import stats  # noqa: E402

COHORTES = ("coeur", "exploratoire", "temoin")
PASSAGES_MIN = 5  # en dessous, résultat exploratoire (repère : 5 explorer, 10 confirmer, 15 affirmer)


# ── texte ────────────────────────────────────────────────────────────────────

def norm(texte):
    """Minuscules, sans accents, apostrophes droites, espaces simples."""
    t = unicodedata.normalize("NFD", texte or "")
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.replace("’", "'").replace("‘", "'").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", t.lower()).strip()


def motif_nom(nom):
    """Regex qui trouve un nom entier (pas « Fnac » dans « Fnacarde »)."""
    n = re.escape(norm(nom))
    return re.compile(rf"(?<![\w]){n}(?![\w])")


def phrases(texte):
    morceaux = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý0-9«\"(*-])|\n+", texte or "")
    return [m.strip() for m in morceaux if m and m.strip()]


TLD = r"(?:fr|com|org|net|eu|be|ch|ca|io|co|info|app|ai|de|es|it|uk|gouv\.fr)"
RE_URL = re.compile(r"https?://[^\s)\]>\"'<]+", re.I)
RE_NU = re.compile(rf"(?<![@\w.-])((?:[a-z0-9-]+\.)+{TLD})(?![\w-])", re.I)


def domaines(texte):
    """Domaines cités dans une réponse (liens et noms de domaine nus), sans « www. »."""
    vus = []
    for u in RE_URL.findall(texte or ""):
        d = urlsplit(u.rstrip(".,;:")).netloc.lower()
        if d:
            vus.append(d)
    sans_urls = RE_URL.sub(" ", texte or "")
    vus += [m.lower() for m in RE_NU.findall(sans_urls)]
    out = []
    for d in vus:
        d = d.split(":")[0].removeprefix("www.")
        if d and d not in out:
            out.append(d)
    return out


def racine(domaine, connus):
    """fr.wikipedia.org → wikipedia.org si connu ; sinon le domaine lui-même."""
    parties = domaine.split(".")
    for i in range(len(parties) - 1):
        cand = ".".join(parties[i:])
        if cand in connus:
            return cand
    return domaine


# ── lecture des fichiers ─────────────────────────────────────────────────────

def lire_portefeuille(chemin):
    brut = Path(chemin).read_text(encoding="utf-8-sig")
    try:
        dialecte = csv.Sniffer().sniff(brut.splitlines()[0], delimiters=";,\t")
    except (csv.Error, IndexError):
        dialecte = csv.excel
    lignes = list(csv.DictReader(io.StringIO(brut), dialect=dialecte))
    if not lignes or "prompt" not in {k.strip().lower() for k in lignes[0]}:
        raise ValueError("le portefeuille doit avoir les colonnes id, cohorte, intention, prompt (et attendu pour les témoins)")
    out = []
    for i, l in enumerate(lignes, 1):
        l = {k.strip().lower(): (v or "").strip() for k, v in l.items() if k}
        coh = norm(l.get("cohorte", "coeur")) or "coeur"
        if coh not in COHORTES:
            raise ValueError(f"ligne {i} : cohorte « {l.get('cohorte')} » inconnue (coeur, exploratoire, temoin)")
        out.append({"id": l.get("id") or f"P{i:02d}", "cohorte": coh, "intention": norm(l.get("intention", "")) or "non precisee",
                    "prompt": l.get("prompt", ""), "attendu": norm(l.get("attendu", ""))})
    return out


RE_TETE = re.compile(r"(?m)^===\s*(.+?)\s*$")


def lire_reponses(chemin):
    brut = Path(chemin).read_text(encoding="utf-8-sig")
    tetes = list(RE_TETE.finditer(brut))
    items = []
    for i, m in enumerate(tetes):
        fin = tetes[i + 1].start() if i + 1 < len(tetes) else len(brut)
        corps = brut[m.end():fin].strip()
        champs = [c.strip() for c in m.group(1).split("|")]
        if len(champs) < 2:
            continue
        moteur = champs[0]
        if len(champs) >= 3 and re.fullmatch(r"[A-Za-z]{0,3}\d{1,4}", champs[1]):
            ident, prompt = champs[1], " | ".join(champs[2:])
        else:
            ident, prompt = None, " | ".join(champs[1:])
        items.append({"moteur": moteur, "id": ident, "prompt": prompt, "reponse": corps})
    return items


def parse_concurrents(valeurs):
    out = {}
    for v in valeurs:
        nom, _, alias = v.partition("=")
        noms = [nom.strip()] + [a.strip() for a in alias.split(",") if a.strip()]
        out[nom.strip()] = noms
    return out


def charger_classes(extra):
    data = json.loads((COMMUN / "sources_fr.json").read_text(encoding="utf-8"))
    dom = dict(data["domaines"])
    for e in extra or []:
        d, _, c = e.partition("=")
        if d and c:
            dom[d.strip().lower().removeprefix("www.")] = c.strip()
    return dom, data["classes"]


def charger_lexiques():
    data = json.loads((COMMUN / "lexiques_fr.json").read_text(encoding="utf-8"))
    return {k: [norm(x) for x in v] for k, v in data.items() if not k.startswith("_")}


# ── analyse d'une réponse ────────────────────────────────────────────────────

_MOTIFS = {}


def motif_marqueur(mk):
    """Marqueur lu comme mot ou expression entière (« évite » ne trouve pas « éviter »)."""
    if mk not in _MOTIFS:
        _MOTIFS[mk] = re.compile(rf"(?<![\w']){re.escape(mk.strip())}(?![\w])")
    return _MOTIFS[mk]


def a_marqueur(phrase_n, marqueurs, negations):
    """Vrai si un marqueur est présent sans négation juste avant (environ 3 mots)."""
    for mk in marqueurs:
        for t in motif_marqueur(mk).finditer(phrase_n):
            avant = phrase_n[max(0, t.start() - 25):t.start()]
            if not any(ng in avant for ng in negations):
                return True
    return False


def opposee(phrase_n, marque_motifs, lex):
    """Vrai si la marque est dans la partie écartée d'une opposition
    (« je recommande Cigna plutôt qu'Assurly », « au lieu de Assurly »)."""
    for m in marque_motifs:
        for trouve in m.finditer(phrase_n):
            avant = phrase_n[:trouve.start()]
            if any(o in avant for o in lex["opposition"]):
                return True
    return False


def analyser_reponse(texte, marque_motifs, domaines_marque, conc_motifs, lex):
    tn = norm(texte)
    mentionnee = any(m.search(tn) for m in marque_motifs)
    doms = domaines(texte)
    citee = any(d == dm or d.endswith("." + dm) for d in doms for dm in domaines_marque)
    recommandee = deconseillee = False
    if mentionnee:
        for ph in phrases(texte):
            pn = norm(ph)
            if not any(m.search(pn) for m in marque_motifs):
                continue
            if a_marqueur(pn, lex["mise_en_garde"], []):
                deconseillee = True
            elif a_marqueur(pn, lex["recommandation"], lex["negation"]) and not opposee(pn, marque_motifs, lex):
                recommandee = True
    concurrents = sorted(n for n, ms in conc_motifs.items() if any(m.search(tn) for m in ms))
    return {"mentionnee": mentionnee, "citee": citee, "recommandee": recommandee,
            "deconseillee": deconseillee, "concurrents": concurrents, "domaines": doms}


def cle_question(it, index_texte):
    if it["id"]:
        return it["id"]
    return index_texte.get(norm(it["prompt"]), norm(it["prompt"]))


# ── mesurer ──────────────────────────────────────────────────────────────────

def mesurer(items, marque, alias, domaines_marque, concurrents, portefeuille=None, classes_extra=None):
    lex = charger_lexiques()
    dom_classes, noms_classes = charger_classes(classes_extra)
    marque_motifs = [motif_nom(n) for n in [marque] + alias]
    conc_motifs = {n: [motif_nom(a) for a in noms] for n, noms in concurrents.items()}
    dom_conc = {norm(a): n for n, noms in concurrents.items() for a in noms if "." in a}
    infos = {}
    index_texte = {}
    if portefeuille:
        for q in portefeuille:
            infos[q["id"]] = q
            index_texte[norm(q["prompt"])] = q["id"]

    par_moteur = defaultdict(lambda: defaultdict(int))
    par_intention = defaultdict(lambda: defaultdict(int))
    par_question = defaultdict(lambda: {"n": 0, "marque": 0, "concurrents": Counter(), "domaines": Counter(),
                                        "prompt": "", "moteurs": Counter()})
    par_qm = defaultdict(lambda: {"n": 0, "marque": 0, "concurrents": Counter(), "domaines": Counter()})
    sources = Counter()
    classes = Counter()
    for it in items:
        r = analyser_reponse(it["reponse"], marque_motifs, domaines_marque, conc_motifs, lex)
        q = cle_question(it, index_texte)
        info = infos.get(q, {})
        for cle in (it["moteur"], "TOTAL"):
            m = par_moteur[cle]
            m["n"] += 1
            for k in ("mentionnee", "citee", "recommandee", "deconseillee"):
                m[k] += r[k]
            m["voix_marque"] += r["mentionnee"]
            m["voix_total"] += r["mentionnee"] + len(r["concurrents"])
        if info:
            pi = par_intention[(info["cohorte"], info["intention"])]
            pi["n"] += 1
            pi["mentionnee"] += r["mentionnee"]
        pq = par_question[q]
        pq["n"] += 1
        pq["marque"] += r["mentionnee"]
        pq["concurrents"].update(r["concurrents"])
        pq["prompt"] = info.get("prompt") or it["prompt"]
        pq["moteurs"][it["moteur"]] += 1
        pm = par_qm[(q, it["moteur"])]
        pm["n"] += 1
        pm["marque"] += r["mentionnee"]
        pm["concurrents"].update(r["concurrents"])
        pm["domaines"].update(r["domaines"])
        for d in r["domaines"]:
            pq["domaines"][d] += 1
            sources[d] += 1
            if any(d == dm or d.endswith("." + dm) for dm in domaines_marque):
                classes["propre site"] += 1
            elif racine(d, dom_conc) in dom_conc:
                classes["concurrent"] += 1
            else:
                classes[dom_classes.get(racine(d, dom_classes), "autre")] += 1

    def resume(m):
        out = {"n": m["n"]}
        for k in ("mentionnee", "citee", "recommandee", "deconseillee"):
            out[k] = stats.taux(m[k], m["n"])
        out["part_de_voix"] = stats.taux(m["voix_marque"], m["voix_total"]) if m["voix_total"] else stats.taux(0, 0)
        return out

    moteurs = {k: resume(v) for k, v in par_moteur.items()}
    passages = Counter((it["moteur"], cle_question(it, index_texte)) for it in items)
    min_passages = {}
    for (mot, _), c in passages.items():
        min_passages[mot] = min(min_passages.get(mot, c), c)

    temoins = []
    perdues = []
    for q, pq in par_question.items():
        info = infos.get(q, {})
        if info.get("cohorte") == "temoin":
            attendu = info.get("attendu") or "present"
            ok = pq["marque"] > 0 if attendu.startswith("pres") else pq["marque"] == 0
            temoins.append({"id": q, "prompt": pq["prompt"], "attendu": attendu, "mentions": pq["marque"], "n": pq["n"], "ok": ok})
            continue
    for (q, mot), pm in par_qm.items():
        info = infos.get(q, {})
        prompt = par_question[q]["prompt"]
        if info.get("cohorte") == "temoin" or info.get("intention") == "marque" \
                or any(m.search(norm(prompt)) for m in marque_motifs):
            continue
        if pm["marque"] == 0 and pm["concurrents"]:
            perdues.append({"id": q, "moteur": mot, "prompt": prompt, "n": pm["n"],
                            "concurrents": dict(pm["concurrents"].most_common()),
                            "sources": dict(pm["domaines"].most_common(6))})
    perdues.sort(key=lambda x: (-sum(x["concurrents"].values()), x["id"], x["moteur"]))

    intentions = {f"{c} · {i}": {"n": v["n"], "mentionnee": stats.taux(v["mentionnee"], v["n"])}
                  for (c, i), v in sorted(par_intention.items())}
    return {"moteurs": moteurs, "passages_min": min_passages, "intentions": intentions, "temoins": temoins,
            "perdues": perdues, "sources": dict(sources.most_common(15)), "classes": dict(classes.most_common()),
            "questions": len(par_question)}


# ── portefeuille ─────────────────────────────────────────────────────────────

ORIENTEES = [r"pourquoi .{0,40} (est|sont) (le|la|les) meilleur", r"(le|la) meilleur.{0,30} (est|c'est)-?(il|elle)? ?.{0,20}\?$"]


def controler_portefeuille(qs, marque, alias):
    motifs = [motif_nom(n) for n in [marque] + alias]
    coeur = [q for q in qs if q["cohorte"] == "coeur"]
    avec = [q for q in coeur if any(m.search(norm(q["prompt"])) for m in motifs)]
    alertes = []
    if coeur:
        part = 1 - len(avec) / len(coeur)
        if part < 0.70:
            alertes.append(f"cœur : {stats.pct(part)} de questions sans la marque, sous les 70% visés (on mesure surtout ce que la marque sait déjà)")
        elif part > 0.85:
            alertes.append(f"cœur : {stats.pct(part)} de questions sans la marque, au-dessus des 85% visés (peu de questions pour vérifier ce que les IA disent de la marque)")
    else:
        part = None
        alertes.append("aucune question dans le cœur : rien de comparable d'une période à l'autre")
    tem = [q for q in qs if q["cohorte"] == "temoin"]
    if not any(q["attendu"].startswith("pres") for q in tem):
        alertes.append("pas de témoin où la marque doit apparaître (ex. « Que vend <marque> ? »)")
    if not any(q["attendu"].startswith("abs") for q in tem):
        alertes.append("pas de témoin où la marque ne doit pas apparaître (une catégorie sans rapport)")
    vus = {}
    for q in qs:
        k = norm(q["prompt"])
        if not k:
            alertes.append(f"{q['id']} : question vide")
        elif k in vus:
            alertes.append(f"{q['id']} : doublon de {vus[k]}")
        else:
            vus[k] = q["id"]
        if any(re.search(p, k) for p in ORIENTEES) and any(m.search(k) for m in motifs):
            alertes.append(f"{q['id']} : question orientée (elle contient déjà la réponse)")
    ids = Counter(q["id"] for q in qs)
    alertes += [f"identifiant {i} utilisé {c} fois" for i, c in ids.items() if c > 1]
    empreinte = hashlib.sha1("\n".join(sorted(norm(q["prompt"]) for q in coeur)).encode()).hexdigest()[:8]
    return {"questions": len(qs), "par_cohorte": dict(Counter(q["cohorte"] for q in qs)),
            "par_intention": dict(Counter(q["intention"] for q in coeur)),
            "coeur_sans_marque": part, "version_coeur": empreinte, "alertes": alertes}


# ── comparer ─────────────────────────────────────────────────────────────────

def comparer_periodes(avant, apres, args, portefeuille):
    index = {norm(q["prompt"]): q["id"] for q in portefeuille} if portefeuille else {}
    qa = {(i["moteur"], cle_question(i, index)) for i in avant}
    qb = {(i["moteur"], cle_question(i, index)) for i in apres}
    communes = qa & qb
    fa = [i for i in avant if (i["moteur"], cle_question(i, index)) in communes]
    fb = [i for i in apres if (i["moteur"], cle_question(i, index)) in communes]
    conc = parse_concurrents(args.concurrent)
    ra = mesurer(fa, args.marque, args.alias, args.domaine, conc, portefeuille)
    rb = mesurer(fb, args.marque, args.alias, args.domaine, conc, portefeuille)
    out = {"questions_communes": len(communes), "ecartees": len((qa | qb) - communes), "moteurs": {}}
    for mot in sorted(set(ra["moteurs"]) & set(rb["moteurs"]), key=lambda x: (x == "TOTAL", x)):
        a, b = ra["moteurs"][mot], rb["moteurs"][mot]
        out["moteurs"][mot] = {k: stats.comparer(a[k]["k"], a[k]["n"], b[k]["k"], b[k]["n"])
                               for k in ("mentionnee", "citee", "recommandee")}
    return out


# ── Tavily (option) ──────────────────────────────────────────────────────────

def tavily(question, profondeur="basic"):
    corps = json.dumps({"query": question, "include_answer": "advanced", "max_results": 8,
                        "search_depth": profondeur}).encode()
    req = urllib.request.Request("https://api.tavily.com/search", data=corps, method="POST",
                                 headers={"Content-Type": "application/json", "X-Tavily-Access-Mode": "keyless",
                                          "User-Agent": "JoinMedicis-geo-visibilite/2.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode("utf-8"))
    urls = [x.get("url") for x in data.get("results", []) if x.get("url")]
    return (data.get("answer") or "").strip(), urls


# ── sortie ───────────────────────────────────────────────────────────────────

def cell(t):
    if not t or t["n"] == 0:
        return "n.d."
    bas, haut = t["ic"]
    return f"{stats.pct(t['taux'])} ({t['k']}/{t['n']}, {stats.pct(bas)[:-1]}-{stats.pct(haut)})"


def afficher_mesure(r, marque, etiquette):
    tot = r["moteurs"].get("TOTAL", {"n": 0})
    nb_moteurs = len([k for k in r["moteurs"] if k != "TOTAL"])
    print(f"VISIBILITÉ IA · {marque} · {etiquette} · {tot['n']} réponses · {r['questions']} questions · {nb_moteurs} moteur(s)")
    print("Taux avec intervalle de confiance à 95% (k/n, bas-haut).\n")
    larg = max([24] + [len(k) + 2 for k in r["moteurs"]])
    print(f"{'MOTEUR':<{larg}}{'MENTIONNÉE':<26}{'CITÉE (lien)':<26}{'RECOMMANDÉE':<26}{'DÉCONSEILLÉE':<14}PART DE VOIX")
    for mot in sorted(r["moteurs"], key=lambda x: (x == "TOTAL", x)):
        v = r["moteurs"][mot]
        dec = f"{v['deconseillee']['k']}/{v['n']}"
        print(f"{mot:<{larg}}{cell(v['mentionnee']):<26}{cell(v['citee']):<26}{cell(v['recommandee']):<26}{dec:<14}{cell(v['part_de_voix'])}")
    faibles = sorted(m for m, c in r["passages_min"].items() if c < PASSAGES_MIN)
    if faibles:
        print(f"\nExploratoire : moins de {PASSAGES_MIN} passages par question pour {', '.join(faibles)} "
              f"(repère : 5 pour explorer, 10 pour confirmer, 15 pour affirmer).")
    if r["intentions"]:
        print("\nPAR COHORTE ET INTENTION (mentionnée, tous moteurs)")
        for k, v in r["intentions"].items():
            print(f"  {k:<34}{cell(v['mentionnee'])}")
    if r["temoins"]:
        print("\nTÉMOINS")
        for t in r["temoins"]:
            etat = "OK" if t["ok"] else "DÉRIVE : vérifie la saisie ou le moteur avant de lire les autres chiffres"
            print(f"  {t['id']:<6}attendu {t['attendu']:<8} mentionnée {t['mentions']}/{t['n']}  {etat}")
    if r["perdues"]:
        print("\nQUESTIONS PERDUES (un concurrent cité, la marque jamais)")
        for p in r["perdues"][:10]:
            conc = ", ".join(f"{c} {n}" for c, n in p["concurrents"].items())
            src = ", ".join(p["sources"]) or "aucune source citée"
            print(f"  {p['id']:<6}{p['moteur'] + ' ':<16}{p['prompt'][:64]}\n        concurrents : {conc} · sources : {src}")
    if r["classes"]:
        print("\nSOURCES CITÉES PAR CLASSE (nombre de citations)")
        print("  " + " · ".join(f"{c} {n}" for c, n in r["classes"].items()))
        print("  Domaines : " + ", ".join(f"{d} {n}" for d, n in r["sources"].items()))
    print("\nNon observable dans une réponse : les pages que le moteur a lues sans les citer (« récupéré »).")


def afficher_comparaison(c, marque):
    print(f"COMPARAISON · {marque} · {c['questions_communes']} paires moteur et question communes"
          + (f" ({c['ecartees']} écartées, absentes d'une période)" if c["ecartees"] else ""))
    for mot, v in c["moteurs"].items():
        print(f"\n{mot}")
        for k, lib in (("mentionnee", "mentionnée"), ("citee", "citée"), ("recommandee", "recommandée")):
            x = v[k]
            if x["ecart"] is None:
                print(f"  {lib:<12}{x['verdict']}")
                continue
            bas, haut = x["ic"]
            print(f"  {lib:<12}{cell(x['avant']):<26}→ {cell(x['apres']):<26}"
                  f"{round(100 * x['ecart']):+d} pts ({round(100 * bas):+d} à {round(100 * haut):+d}) · {x['verdict'].upper()}")


# ── ligne de commande ────────────────────────────────────────────────────────

def options_marque(p):
    p.add_argument("--marque", required=True)
    p.add_argument("--alias", action="append", default=[], help="autre nom de la marque (répétable)")
    p.add_argument("--domaine", action="append", default=[], help="domaine de la marque, pour la citation (répétable)")
    p.add_argument("--concurrent", action="append", default=[], help="« Nom=alias1,domaine.fr » (répétable)")
    p.add_argument("--portefeuille", help="portefeuille CSV (cohortes, intentions, témoins)")
    p.add_argument("--classe", action="append", default=[], help="« domaine=classe » pour compléter sources_fr.json")
    p.add_argument("--json", action="store_true")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mesurer la place d'une marque dans des réponses d'IA collées.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("portefeuille", help="contrôler la liste de questions")
    p.add_argument("fichier")
    p.add_argument("--marque", required=True)
    p.add_argument("--alias", action="append", default=[])
    p.add_argument("--json", action="store_true")
    g = sub.add_parser("grille", help="écrire le fichier de réponses à remplir")
    g.add_argument("fichier")
    g.add_argument("--moteur", action="append", required=True)
    g.add_argument("--passages", type=int, default=PASSAGES_MIN)
    g.add_argument("--cohorte", action="append", choices=COHORTES, help="cohortes à inclure (défaut : toutes)")
    m = sub.add_parser("mesurer", help="mesurer un fichier de réponses collées")
    m.add_argument("reponses")
    m.add_argument("--approximation", action="store_true", help="réponses d'un moteur de substitution (Tavily)")
    options_marque(m)
    c = sub.add_parser("comparer", help="comparer deux périodes")
    c.add_argument("avant")
    c.add_argument("apres")
    options_marque(c)
    t = sub.add_parser("tavily", help="option : poser les questions à Tavily (tiers, approximation)")
    t.add_argument("fichier")
    t.add_argument("--accepte-tiers", action="store_true", help="obligatoire : les questions sont envoyées à Tavily")
    t.add_argument("--passages", type=int, default=1)
    t.add_argument("--cohorte", action="append", choices=COHORTES)
    args = ap.parse_args(argv)

    try:
        if args.cmd == "portefeuille":
            r = controler_portefeuille(lire_portefeuille(args.fichier), args.marque, args.alias)
            if args.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                print(f"PORTEFEUILLE · {r['questions']} questions · cœur version {r['version_coeur']}")
                print("  cohortes : " + ", ".join(f"{k} {v}" for k, v in r["par_cohorte"].items()))
                if r["coeur_sans_marque"] is not None:
                    print(f"  cœur sans la marque : {stats.pct(r['coeur_sans_marque'])} (visé : 70 à 85%)")
                print("  intentions du cœur : " + ", ".join(f"{k} {v}" for k, v in r["par_intention"].items()))
                print("\n".join(f"  ! {a}" for a in r["alertes"]) or "  aucune alerte")
            return 0
        if args.cmd == "grille":
            qs = [q for q in lire_portefeuille(args.fichier) if not args.cohorte or q["cohorte"] in args.cohorte]
            print("# Une nouvelle conversation par passage, recherche web activée si le moteur la propose.")
            print("# Colle la réponse complète sous chaque en-tête, liens et sources compris.\n")
            for mot in args.moteur:
                for q in qs:
                    for _ in range(args.passages):
                        print(f"=== {mot} | {q['id']} | {q['prompt']}\n")
            return 0
        if args.cmd == "tavily":
            if not args.accepte_tiers:
                print("Refusé : chaque question serait envoyée à Tavily, un service tiers. Relance avec --accepte-tiers "
                      "si l'utilisateur l'a accepté. Ce moteur est une approximation, ni ChatGPT ni Perplexity.", file=sys.stderr)
                return 1
            qs = [q for q in lire_portefeuille(args.fichier) if not args.cohorte or q["cohorte"] in args.cohorte]
            print("# Réponses du moteur de Tavily : APPROXIMATION, ni ChatGPT, ni Perplexity, ni Google.")
            for q in qs:
                for _ in range(args.passages):
                    try:
                        rep, urls = tavily(q["prompt"])
                    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
                        print(f"# {q['id']} : échec ({e}), question non mesurée")
                        continue
                    print(f"=== Tavily (approximation) | {q['id']} | {q['prompt']}\n{rep}\nSources : {' '.join(urls)}\n")
            return 0
        portefeuille = lire_portefeuille(args.portefeuille) if args.portefeuille else None
        if args.cmd == "mesurer":
            items = lire_reponses(args.reponses)
            if not items:
                print("Aucune réponse lue : chaque réponse commence par « === Moteur | question ».", file=sys.stderr)
                return 1
            r = mesurer(items, args.marque, args.alias, args.domaine, parse_concurrents(args.concurrent),
                        portefeuille, args.classe)
            etiquette = "approximation (moteur de substitution)" if args.approximation or any(
                "approximation" in i["moteur"].lower() for i in items) else "mesuré (réponses collées)"
            r["etiquette"] = etiquette
            if args.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                afficher_mesure(r, args.marque, etiquette)
            return 0
        if args.cmd == "comparer":
            c = comparer_periodes(lire_reponses(args.avant), lire_reponses(args.apres), args, portefeuille)
            if args.json:
                print(json.dumps(c, ensure_ascii=False, indent=2))
            else:
                afficher_comparaison(c, args.marque)
            return 0
    except (OSError, ValueError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
