#!/usr/bin/env python3
"""lire_exports.py : analyse des exports Google Ads, Meta Ads et Microsoft Ads pour ChatGPT Ads (Python 3, sans dépendance).

Lit l'export en entier (CSV UTF-8 ou UTF-16, virgule, point-virgule ou
tabulation ; XLSX), repère la plateforme et les colonnes par leurs en-têtes
(anglais ou français), puis en tire ce qu'il faut pour réécrire les annonces
au format de ChatGPT Ads : banque de titres et de textes avec leurs longueurs,
allégations à vérifier avec leur ligne source, pages de destination, angles,
meilleures annonces si des statistiques sont présentes, termes de recherche
transformables en situations, signaux de catégories restreintes.

Commandes :

  colonnes EXPORT
      Montre les colonnes reconnues et celles ignorées (vérifier avant d'analyser).

  analyser EXPORT [EXPORT …] [-o analyse.json] [--md rapport.md] [--min-impressions N]
      Analyse un ou plusieurs exports (annonces, termes de recherche, mots-clés).
      --min-impressions : seuil sous lequel une performance n'est pas classée
      (défaut 100, choix du pack, réglable).

  amorcer analyse.json -o campagne.json [--marque M] [--categorie C] [--pays FR]
      Squelette de campagne pour /chatgpt-ads-skills : annonceur et domaines,
      allégations (toutes « à vérifier », avec leur source), un ad group par
      groupe source avec ses pages, sans annonce : la réécriture se fait
      ensuite, puis valider_exporter.py la contrôle.

  --colonne CHAMP=EN-TÊTE (répétable) force une correspondance que le script
  ne reconnaît pas, par exemple --colonne titre="Titre court 1".

Codes de sortie : 0 ok · 2 analyse partielle (colonnes manquantes) · 1 usage.
"""
import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

ICI = Path(__file__).resolve()
for base in (ICI.parents[1] / "commun", ICI.parents[2] / "commun"):   # Skill seul, ou ZIP claude.ai
    if (base / "classeur.py").exists():
        sys.path.insert(0, str(base))
        break
import classeur as cl  # noqa: E402
import signaux as sg  # noqa: E402

LIM_TITRE, LIM_COPIE = cl.LIMITES["import"]["title"], cl.LIMITES["import"]["copy"]

# En-têtes reconnus (pliés : minuscules, sans accents). Exports UI et éditeurs, anglais et français.
# Liste construite à partir des intitulés usuels ; un export qui en diffère se règle avec --colonne.
SYNONYMES = {
    "campagne": ["campaign", "campaign name", "campagne", "nom de la campagne"],
    "groupe": ["ad group", "ad group name", "adgroup", "groupe d'annonces", "nom du groupe d'annonces",
               "ad set name", "ad set", "nom de l'ensemble de publicites", "ensemble de publicites"],
    "annonce_nom": ["ad name", "nom de la publicite", "nom de l'annonce"],
    "titre": [r"headline \d+", r"titre \d+", "headline", "title", "titre", r"title part \d+", "long headline",
              "titre long", r"short title \d+"],
    "texte": [r"description \d+", "description", "body", "corps du texte", "texte principal", "primary text",
              "text", r"text part \d+", "link description", "description du lien", "ad text", "texte de l'annonce"],
    "url": ["final url", "final urls", "url finale", "url finales", "link", "lien", "website url", "url du site web",
            "destination url", "url de destination", "landing page", "page de destination"],
    "chemin": [r"path \d+", r"chemin \d+"],
    "statut": ["status", "ad status", "etat", "statut", "statut de l'annonce", "ad delivery", "diffusion de la publicite"],
    "type": ["ad type", "type d'annonce", "type"],
    "impressions": ["impr.", "impressions", "impr"],
    "clics": ["clicks", "clics", "link clicks", "clics sur un lien"],
    "conversions": ["conversions", "conv.", "results", "resultats", "all conv.", "toutes les conv."],
    "cout": ["cost", "cout", "amount spent", "montant depense", "spend", "depenses"],
    "terme": ["search term", "terme de recherche", "search query", "requete de recherche"],
    "mot_cle": ["keyword", "mot cle", "mot-cle", "search keyword"],
}
EXCLUS = {"titre": [r"^headline \d+ position$", r"^titre \d+ position$"]}
QUESTIONS = re.compile(r"^(comment|pourquoi|quel|quelle|quels|quelles|combien|ou|quand|est-ce|peut-on|faut-il|"
                       r"how|why|what|which|where|when|can|should|is|are|do|does)\b", re.I)
TIRET = re.compile("[—–]")


def plier_entete(h):
    return re.sub(r"\s+", " ", cl.plier(h).replace("’", "'")).strip()


def reconnaitre(entetes, forcees=None):
    """{index de colonne: champ}. Une colonne de titre ou de texte peut être multiple."""
    res, forcees = {}, forcees or {}
    for j, h in entetes.items():
        p = plier_entete(h)
        for champ, en_tete in forcees.items():
            if plier_entete(en_tete) == p:
                res[j] = champ
                break
        else:
            for champ, motifs in SYNONYMES.items():
                if any(re.fullmatch(m, p) for m in EXCLUS.get(champ, [])):
                    continue
                if any(re.fullmatch(m, p) for m in motifs):
                    res[j] = champ
                    break
    return res


def ligne_entete(onglet):
    """Le numéro de la ligne d'en-têtes : la première qui contient au moins 2 en-têtes connus (les rapports
    Google Ads ont 1 ou 2 lignes de titre et de période avant les en-têtes)."""
    for num in sorted(onglet["lignes"])[:15]:
        tete = {j: cl.texte(c["valeur"]) for j, c in onglet["lignes"][num].items()}
        if len(set(reconnaitre(tete).values())) >= 2:
            return num
    return None


def plateforme(entetes):
    t = " | ".join(plier_entete(h) for h in entetes)
    if re.search(r"ad set|ensemble de publicites|body|corps du texte|texte principal|link clicks|clics sur un lien", t):
        return "meta"
    if re.search(r"title part|text part|format version|parent id", t):
        return "microsoft"
    if re.search(r"headline \d|titre \d|url finale|final url|impr\.|search term|terme de recherche|mot cle|keyword", t):
        return "google ou microsoft"
    return "inconnue"


def nombre(v):
    if v in (None, ""):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace(" ", "").replace(" ", "").replace("%", "").replace("€", "").replace("$", "")
    if re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", s):
        s = s.replace(",", "")
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def lire_export(chemin, forcees=None):
    """Lignes normalisées {champ: valeur ou liste} d'un export."""
    classeur = cl.lire(chemin)
    res = {"fichier": Path(chemin).name, "lignes": [], "colonnes": {}, "ignorees": [], "plateforme": "inconnue"}
    for o in classeur["onglets"]:
        num = ligne_entete(o) if not forcees else (ligne_entete(o) or 1)
        if not num:
            continue
        entetes = {j: cl.texte(c["valeur"]).strip() for j, c in o["lignes"][num].items()}
        cols = reconnaitre(entetes, forcees)
        res["colonnes"].update({entetes[j]: c for j, c in cols.items()})
        res["ignorees"] += [h for j, h in entetes.items() if j not in cols and h]
        res["plateforme"] = plateforme(entetes.values())
        for n in sorted(x for x in o["lignes"] if x > num):
            cel = o["lignes"][n]
            ligne = {"_source": f"{res['fichier']} ligne {n}", "titres": [], "textes": [], "chemins": []}
            for j, champ in cols.items():
                if j not in cel:
                    continue
                v = cl.texte(cel[j]["valeur"]).strip()
                if not v or v in ("--", " --"):
                    continue
                if champ == "titre":
                    ligne["titres"].append(v)
                elif champ == "texte":
                    ligne["textes"].append(v)
                elif champ == "chemin":
                    ligne["chemins"].append(v)
                elif champ in ("impressions", "clics", "conversions", "cout"):
                    ligne[champ] = nombre(v)
                elif champ == "url" and v.startswith("["):     # Google : ["https://…"]
                    try:
                        ligne[champ] = (json.loads(v) or [""])[0]
                    except ValueError:
                        ligne[champ] = v
                else:
                    ligne[champ] = v
            if re.match(r"^(total|totaux|totals?)\b", cl.plier(ligne.get("campagne", "")) + cl.plier(ligne.get("groupe", ""))):
                continue
            if cl.plier(ligne.get("type", "")) in ("format version", "campaign", "ad group", "campagne", "groupe d'annonces"):
                continue   # lignes de structure d'un fichier en masse (Microsoft Ads, Google Ads Editor)
            if len(ligne) > 4 or ligne["titres"] or ligne["textes"]:
                res["lignes"].append(ligne)
    return res


# ---------------------------------------------------------------- analyse

def _banque(lignes, cle, limite):
    banque = {}
    for l in lignes:
        for t in l[cle]:
            k = cl.plier(t)
            x = banque.setdefault(k, {"texte": t, "longueur": cl.longueur(t), "occurrences": 0, "sources": [],
                                      "groupes": set()})
            x["occurrences"] += 1
            if len(x["sources"]) < 3:
                x["sources"].append(l["_source"])
            if l.get("groupe"):
                x["groupes"].add(l["groupe"])
    res = sorted(banque.values(), key=lambda x: (-x["occurrences"], x["longueur"]))
    for x in res:
        x["groupes"] = sorted(x["groupes"])
        x["reutilisable"] = x["longueur"] <= limite
        x["a_corriger"] = [p for p, m in (("paramètre dynamique à retirer", re.search(r"\{[^}]*\}", x["texte"])),
                                          ("tiret cadratin", TIRET.search(x["texte"])),
                                          ("capitales", re.search(r"\b[A-ZÀ-Ý]{4,}\b", x["texte"])),
                                          ("pas d'espace avant ? ! : ;", re.search(r"\S[?!:;]", x["texte"])))
                           if m]
    return res


def analyser(exports, min_impressions=100):
    lignes = [l for e in exports for l in e["lignes"]]
    annonces = [l for l in lignes if l["titres"] or l["textes"]]
    termes = [l for l in lignes if l.get("terme") or l.get("mot_cle")]
    res = {"fichiers": [{"fichier": e["fichier"], "plateforme": e["plateforme"], "lignes": len(e["lignes"]),
                         "colonnes": e["colonnes"], "ignorees": e["ignorees"]} for e in exports]}
    statuts = {}
    for l in annonces:
        statuts[cl.plier(l.get("statut", "inconnu")) or "inconnu"] = statuts.get(cl.plier(l.get("statut", "inconnu")) or "inconnu", 0) + 1
    res["inventaire"] = {
        "annonces": len(annonces),
        "campagnes": sorted({l["campagne"] for l in annonces if l.get("campagne")}),
        "groupes": sorted({l["groupe"] for l in annonces if l.get("groupe")}),
        "statuts": statuts,
        "termes": len(termes),
    }
    res["titres"] = _banque(annonces, "titres", LIM_TITRE)
    res["textes"] = _banque(annonces, "textes", LIM_COPIE)
    # allégations : chaque élément à étayer, avec ses sources
    alleg = {}
    for l in annonces:
        for t in l["titres"] + l["textes"]:
            for s in sg.sensibles(t):
                x = alleg.setdefault(cl.plier(s), {"element": s, "exemples": [], "sources": [], "occurrences": 0})
                x["occurrences"] += 1
                if t not in x["exemples"] and len(x["exemples"]) < 3:
                    x["exemples"].append(t)
                if len(x["sources"]) < 3:
                    x["sources"].append(l["_source"])
    res["allegations"] = sorted(alleg.values(), key=lambda x: -x["occurrences"])
    # pages
    pages = {}
    for l in annonces:
        u = l.get("url", "")
        if not u:
            continue
        x = pages.setdefault(u, {"url": u, "annonces": 0, "groupes": set()})
        x["annonces"] += 1
        if l.get("groupe"):
            x["groupes"].add(l["groupe"])
    for x in pages.values():
        p = urllib.parse.urlsplit(x["url"])
        x["groupes"] = sorted(x["groupes"])
        x["accueil"] = p.path in ("", "/") and not p.query
        x["valide"] = cl._url_ok(x["url"])
    res["pages"] = sorted(pages.values(), key=lambda x: -x["annonces"])
    res["domaines"] = sorted({urllib.parse.urlsplit(u).hostname.removeprefix("www.") for u in pages
                              if urllib.parse.urlsplit(u).hostname})
    # performances
    mesurees = [l for l in annonces if (l.get("impressions") or 0) >= min_impressions]
    for l in mesurees:
        l["ctr"] = (l.get("clics") or 0) / l["impressions"] if l.get("impressions") else None
    cle = (lambda l: (l.get("conversions") or 0, l.get("ctr") or 0))
    res["performances"] = {
        "seuil_impressions": min_impressions,
        "mesurees": len(mesurees),
        "sous_le_seuil": sum(1 for l in annonces if l.get("impressions") is not None) - len(mesurees),
        "meilleures": [_resume(l) for l in sorted(mesurees, key=cle, reverse=True)[:10]],
        "faibles": [_resume(l) for l in sorted(mesurees, key=cle)[:5]],
    } if any(l.get("impressions") is not None for l in annonces) else None
    # termes de recherche → situations
    situations = {}
    for l in termes:
        t = l.get("terme") or l.get("mot_cle")
        t = re.sub(r"^[\[\"+]|[\]\"]$", "", t).strip()
        mots = t.split()
        if len(mots) >= 4 or QUESTIONS.match(t):
            x = situations.setdefault(cl.plier(t), {"terme": t, "clics": 0, "conversions": 0, "question": bool(QUESTIONS.match(t))})
            x["clics"] += l.get("clics") or 0
            x["conversions"] += l.get("conversions") or 0
    res["situations"] = sorted(situations.values(), key=lambda x: (-x["conversions"], -x["clics"]))[:60]
    res["termes_courts"] = len(termes) - len(situations)
    # catégories et droit français
    cats, vert = {}, []
    for l in annonces:
        for t in l["titres"] + l["textes"]:
            for c, mot in sg.categories(t).items():
                cats.setdefault(c, {"mot": mot, "source": l["_source"], "occurrences": 0})["occurrences"] += 1
            m = sg.VERT.search(t)
            if m and len(vert) < 5:
                vert.append({"mot": m.group(0), "texte": t, "source": l["_source"]})
    res["categories"] = cats
    res["allegations_vertes"] = vert
    res["langue_anglaise"] = [t["texte"] for t in res["titres"][:200] if _anglais(t["texte"])][:10]
    return res


def _resume(l):
    return {"titres": l["titres"][:3], "textes": l["textes"][:2], "groupe": l.get("groupe", ""), "url": l.get("url", ""),
            "impressions": l.get("impressions"), "clics": l.get("clics"), "conversions": l.get("conversions"),
            "ctr": round(l["ctr"] * 100, 2) if l.get("ctr") is not None else None, "source": l["_source"]}


MOTS_EN = {"the", "your", "with", "and", "for", "get", "shop", "now", "free", "best", "new", "buy", "our"}


def _anglais(t):
    """Heuristique : 2 mots anglais courants, ou 1 dans un texte de 4 mots au plus."""
    m = cl.plier(t).split()
    n = len(set(m) & MOTS_EN)
    return n >= 2 or (n >= 1 and len(m) <= 4)


# ---------------------------------------------------------------- rapport

def rapport_md(a):
    out = ["# Analyse des exports", ""]
    for f in a["fichiers"]:
        out.append(f"- **{f['fichier']}** : {f['lignes']} ligne(s), plateforme {f['plateforme']} ; colonnes "
                   f"reconnues : {', '.join(sorted(set(f['colonnes'].values()))) or 'aucune'}"
                   + (f" ; ignorées : {len(f['ignorees'])}" if f["ignorees"] else ""))
    inv = a["inventaire"]
    out += ["", "## Inventaire", "",
            f"{inv['annonces']} annonce(s), {len(inv['campagnes'])} campagne(s), {len(inv['groupes'])} groupe(s), "
            f"{inv['termes']} terme(s) ou mot(s)-clé(s). Statuts : "
            + ", ".join(f"{k} {v}" for k, v in sorted(inv["statuts"].items())), ""]
    for cle, nom, lim in (("titres", "Titres", LIM_TITRE), ("textes", "Textes", LIM_COPIE)):
        lst = a[cle]
        ok = sum(1 for x in lst if x["reutilisable"])
        out += [f"## {nom} ({len(lst)} uniques, {ok} tiennent en {lim} caractères)", "",
                "| Texte | Car. | Fois | À corriger |", "|---|---|---|---|"]
        for x in lst[:25]:
            out.append(f"| {x['texte']} | {x['longueur']}{'' if x['reutilisable'] else ' ✖'} | {x['occurrences']} | "
                       f"{', '.join(x['a_corriger'])} |")
        out.append("")
    out += ["## Allégations à vérifier (aucune n'est approuvée d'office)", "",
            "| Élément | Exemple | Fois | Source |", "|---|---|---|---|"]
    for x in a["allegations"][:30]:
        out.append(f"| {x['element']} | {x['exemples'][0]} | {x['occurrences']} | {x['sources'][0]} |")
    out += ["", "## Pages de destination", "", "| Page | Annonces | Groupes | Remarque |", "|---|---|---|---|"]
    for x in a["pages"][:20]:
        rem = "page d'accueil" if x["accueil"] else ("adresse invalide" if not x["valide"] else "")
        out.append(f"| {x['url']} | {x['annonces']} | {', '.join(x['groupes'][:3])} | {rem} |")
    p = a["performances"]
    if p:
        out += ["", f"## Performances (annonces à {p['seuil_impressions']} impressions ou plus : {p['mesurees']} ; "
                    f"sous le seuil : {p['sous_le_seuil']})", "",
                "| Titre | Groupe | Impr. | Clics | CTR | Conv. |", "|---|---|---|---|---|---|"]
        for x in p["meilleures"]:
            out.append(f"| {(x['titres'] or [''])[0]} | {x['groupe']} | {x['impressions']:g} | {x['clics'] or 0:g} | "
                       f"{str(x['ctr']).replace('.', ',')}% | {x['conversions'] or 0:g} |")
        out.append("\nUne performance de recherche ne se transpose pas telle quelle : elle désigne les angles à essayer.")
    if a["situations"]:
        out += ["", "## Termes de recherche à transformer en situations", "",
                "| Terme | Question | Clics | Conv. |", "|---|---|---|---|"]
        for x in a["situations"][:25]:
            out.append(f"| {x['terme']} | {'oui' if x['question'] else ''} | {x['clics']:g} | {x['conversions']:g} |")
        out.append(f"\n{a['termes_courts']} terme(s) court(s) écarté(s) : un mot-clé de 1 à 3 mots n'est pas une situation.")
    if a["categories"]:
        out += ["", "## Signaux de catégories restreintes ou interdites (règles d'OpenAI v1.6)", ""]
        for c, x in a["categories"].items():
            out.append(f"- **{c}** : « {x['mot']} » ({x['occurrences']} fois, ex. {x['source']})")
    if a["allegations_vertes"]:
        out += ["", "## Allégations environnementales à justifier", ""]
        out += [f"- « {x['mot']} » dans « {x['texte']} » ({x['source']})" for x in a["allegations_vertes"]]
    if a["langue_anglaise"]:
        out += ["", "## Textes en anglais (à traduire pour la France)", ""] + [f"- {t}" for t in a["langue_anglaise"]]
    return "\n".join(out) + "\n"


def amorcer(a, marque="", categorie="", pays="FR"):
    """Squelette de campagne : le Skill réécrit ensuite les annonces dans ce JSON."""
    groupes = {}
    for x in a["pages"]:
        for g in x["groupes"] or ["{{à compléter}}"]:
            groupes.setdefault(g, []).append(x["url"])
    nom_camp = re.sub(r"[^a-z0-9_-]+", "_", cl.plier(marque or "campagne")).strip("_") + "_chatgpt_fr"
    return {
        "annonceur": {"marque": marque or "{{à compléter}}", "domaines": a["domaines"],
                      "categorie": categorie or "{{à compléter}}"},
        "allegations": [{"texte": x["exemples"][0], "element": x["element"], "source": x["sources"][0],
                         "statut": "à vérifier"} for x in a["allegations"]],
        "campaigns": [{"campaign_name": nom_camp, "budget_max": "{{à compléter}}", "budget_type": "Daily",
                       "objective": "Clicks", "target_countries": [pays]}],
        "adgroups": [{"campaign_name": nom_camp,
                      "adgroup_name": re.sub(r"[^a-z0-9_-]+", "_", cl.plier(g)).strip("_")[:60] or "groupe",
                      "groupe_source": g, "pages": urls[:3], "intention": "{{à compléter}}", "context_hints": []}
                     for g, urls in groupes.items()],
        "ads": [],
        "_origine": "amorcé depuis l'analyse d'exports : intentions, hints et annonces à écrire ; "
                    "allégations à faire valider avant usage",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--colonne", action="append", default=[], metavar="CHAMP=EN-TÊTE")
    sp = p.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("colonnes")
    c.add_argument("export")
    an = sp.add_parser("analyser")
    an.add_argument("exports", nargs="+")
    an.add_argument("-o", "--sortie")
    an.add_argument("--md")
    an.add_argument("--min-impressions", type=int, default=100)
    am = sp.add_parser("amorcer")
    am.add_argument("analyse")
    am.add_argument("-o", "--sortie", required=True)
    am.add_argument("--marque", default="")
    am.add_argument("--categorie", default="")
    am.add_argument("--pays", default="FR")
    a = p.parse_args(argv)
    forcees = {}
    for x in a.colonne:
        if "=" not in x or x.split("=", 1)[0] not in SYNONYMES:
            print(f"--colonne {x} : CHAMP parmi {', '.join(SYNONYMES)}", file=sys.stderr)
            return 1
        champ, entete = x.split("=", 1)
        forcees[champ] = entete

    if a.cmd == "amorcer":
        camp = amorcer(json.loads(Path(a.analyse).read_text(encoding="utf-8")), a.marque, a.categorie, a.pays)
        Path(a.sortie).write_text(json.dumps(camp, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Squelette écrit : {a.sortie} ({len(camp['adgroups'])} groupe(s), {len(camp['allegations'])} "
              "allégation(s) à vérifier, aucune annonce). Suite : /chatgpt-ads-skills, étapes 2 à 7.")
        return 0

    fichiers = [a.export] if a.cmd == "colonnes" else a.exports
    for f in fichiers:
        if not Path(f).exists():
            print(f"Fichier introuvable : {f}", file=sys.stderr)
            return 1
    try:
        exports = [lire_export(f, forcees) for f in fichiers]
    except Exception as e:  # fichier abîmé : message clair plutôt qu'une trace
        print(f"Lecture impossible : {e}. Réexporter en CSV ou XLSX.", file=sys.stderr)
        return 1

    if a.cmd == "colonnes":
        e = exports[0]
        print(f"{e['fichier']} · plateforme : {e['plateforme']} · {len(e['lignes'])} ligne(s)")
        for h, champ in e["colonnes"].items():
            print(f"  {h:<40} → {champ}")
        if e["ignorees"]:
            print("Ignorées : " + ", ".join(e["ignorees"]))
        manque = {"titre", "texte", "url"} - set(e["colonnes"].values())
        if manque and not (set(e["colonnes"].values()) & {"terme", "mot_cle"}):
            print(f"Colonnes attendues absentes : {', '.join(sorted(manque))} (--colonne CHAMP=EN-TÊTE pour forcer)")
            return 2
        return 0

    res = analyser(exports, a.min_impressions)
    if a.sortie:
        Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    md = rapport_md(res)
    if a.md:
        Path(a.md).write_text(md, encoding="utf-8")
    if not a.sortie and not a.md:
        print(md)
    else:
        inv = res["inventaire"]
        print(f"{inv['annonces']} annonce(s), {len(res['titres'])} titres et {len(res['textes'])} textes uniques, "
              f"{len(res['allegations'])} allégation(s) à vérifier, {len(res['pages'])} page(s), "
              f"{len(res['situations'])} situation(s) issues des termes.")
    partiel = not res["inventaire"]["annonces"] and not res["inventaire"]["termes"]
    return 2 if partiel else 0


if __name__ == "__main__":
    sys.exit(main())
