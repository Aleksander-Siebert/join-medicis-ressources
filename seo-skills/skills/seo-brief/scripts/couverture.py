#!/usr/bin/env python3
"""couverture.py : le test MECE d'un plan, mesuré.

Deux commandes :

  couvrir  PLAN REQUETES   chaque requête du champ sémantique est-elle
                           rattachée à une section ? (« sans manque »)
                           deux sections se disputent-elles les mêmes
                           requêtes ? (« sans recouvrement »)
  grille   PLAN --concurrent F [--concurrent F …]
                           sous-thèmes des concurrents classés attendu,
                           courant, distinctif ; ce que notre plan couvre ;
                           nos angles propres (aucun concurrent ne les a)

PLAN : Markdown (# Titre, ## Section…) ou plan de /seo-brief
(« H2 Titre → description »). REQUETES : une requête par ligne, ou export
CSV de Search Console (première colonne). Concurrents : plans en Markdown,
ou pages HTML enregistrées (H2 et H3 lus).

Codes de sortie : 0 rien à corriger · 2 manques ou recouvrements à revoir ·
1 erreur d'utilisation.

La correspondance est lexicale (mots racinisés, mots vides et termes de tête
retirés) : elle repère les manques évidents, elle ne comprend pas les
synonymes. Le Skill relit chaque « non couverte » avant de créer une section.

Exemples :
  python3 couverture.py couvrir plan.md requetes.txt
  python3 couverture.py couvrir plan.md export-gsc.csv --json
  python3 couverture.py grille plan.md --concurrent a.md --concurrent b.html --concurrent c.md
"""

import argparse
import csv
import io
import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ICI = Path(__file__).resolve().parent
for _c in (ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (_c / "texte_fr.py").exists():
        sys.path.insert(0, str(_c))
        break
import texte_fr as tf  # noqa: E402

SEUIL_COUVERTE = 0.75
SEUIL_PARTIELLE = 0.4
SEUIL_TETE = 0.6          # un terme présent dans 60% des requêtes est un terme de tête
SEUIL_SOUS_THEME = 0.5    # deux titres de concurrents parlent du même sous-thème
SEUIL_NOUS = 0.5          # un sous-thème est couvert par une de nos sections


# ------------------------------------------------------------------ lecture
def lire(chemin):
    try:
        return Path(chemin).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return Path(chemin).read_text(encoding="latin-1")


def lire_requetes(chemin):
    texte = lire(chemin)
    lignes = [l for l in texte.splitlines() if l.strip()]
    if not lignes:
        return []
    premiere = lignes[0]
    if premiere.count(",") >= 2 or premiere.count(";") >= 2 or "\t" in premiere:
        delim = "\t" if "\t" in premiere else (";" if premiere.count(";") > premiere.count(",") else ",")
        lecteur = csv.reader(io.StringIO(texte), delimiter=delim)
        rangs = [r for r in lecteur if r and r[0].strip()]
        entete = rangs[0][0].lower()
        if any(m in entete for m in ("requ", "query", "mot", "keyword")):
            rangs = rangs[1:]
        return list(dict.fromkeys(r[0].strip() for r in rangs if r[0].strip()))
    return list(dict.fromkeys(l.strip().lstrip("-*• ").strip() for l in lignes if not l.startswith("#")))


class _Titres(HTMLParser):
    def __init__(self):
        super().__init__()
        self.titres, self._niv, self._buf = [], None, []

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3"):
            self._niv, self._buf = int(tag[1]), []

    def handle_endtag(self, tag):
        if self._niv and tag == f"h{self._niv}":
            t = " ".join("".join(self._buf).split())
            if t:
                self.titres.append({"niveau": self._niv, "titre": t, "texte": "", "ligne": 0})
            self._niv = None

    def handle_data(self, data):
        if self._niv:
            self._buf.append(data)


def lire_plan(chemin):
    texte = lire(chemin)
    if chemin.lower().endswith((".html", ".htm")) or texte.lstrip().lower().startswith(("<!doctype", "<html")):
        p = _Titres()
        p.feed(texte)
        return p.titres
    return [s for s in tf.plan(texte) if s["niveau"] > 0]


# ------------------------------------------------------------------ calcul
def termes_de_tete(requetes):
    if len(requetes) < 4:
        return set()
    compte = Counter()
    for q in requetes:
        compte.update(set(tf.termes(q)))
    return {t for t, n in compte.items() if n / len(requetes) >= SEUIL_TETE}


def sections_cibles(sections):
    """Les H2 (avec leurs H3) sont les unités du plan ; à défaut, chaque titre."""
    h2 = [i for i, s in enumerate(sections) if s["niveau"] == 2]
    if not h2:
        return [{"titre": s["titre"], "niveau": s["niveau"], "ligne": s["ligne"],
                 "texte": s["titre"] + " " + s["titre"] + " " + s["texte"], "sous": []} for s in sections]
    cibles = []
    for k, i in enumerate(h2):
        fin = h2[k + 1] if k + 1 < len(h2) else len(sections)
        sous = [s for s in sections[i + 1:fin] if s["niveau"] > 2]
        s = sections[i]
        texte = " ".join([s["titre"]] * 2 + [s["texte"]] + [x["titre"] + " " + x["texte"] for x in sous])
        cibles.append({"titre": s["titre"], "niveau": 2, "ligne": s["ligne"], "texte": texte,
                       "sous": [x["titre"] for x in sous]})
    return cibles


def couvrir(sections, requetes):
    titre_page = " ".join(s["titre"] for s in sections if s["niveau"] == 1)
    tete = termes_de_tete(requetes)
    if titre_page:  # le sujet de la page, c'est ce que dit son H1
        tete &= set(tf.termes(titre_page))
    cibles = sections_cibles(sections)
    t_cibles = [[t for t in tf.termes(c["texte"]) if t not in tete] for c in cibles]
    resultats = []
    for q in requetes:
        tq_all = tf.termes(q)
        tq = [t for t in tq_all if t not in tete]
        if not tq:  # requête faite seulement des termes de tête : c'est le sujet de la page
            ok = tf.recouvrement(tq_all, tf.termes(titre_page)) >= SEUIL_COUVERTE if titre_page else True
            resultats.append({"requete": q, "statut": "couverte" if ok else "partielle",
                              "section": "titre de la page (H1)", "score": 1.0 if ok else 0.5, "aussi": []})
            continue
        scores = sorted(((tf.recouvrement(tq, t), i) for i, t in enumerate(t_cibles)), reverse=True)
        meilleur, i = scores[0] if scores else (0.0, None)
        statut = "couverte" if meilleur >= SEUIL_COUVERTE else ("partielle" if meilleur >= SEUIL_PARTIELLE else "non couverte")
        aussi = [cibles[j]["titre"] for sc, j in scores[1:] if sc >= SEUIL_COUVERTE]
        resultats.append({"requete": q, "statut": statut, "score": round(meilleur, 2),
                          "section": cibles[i]["titre"] if i is not None and meilleur >= SEUIL_PARTIELLE else None,
                          "aussi": aussi})
    # recouvrements : requêtes couvertes pleinement par deux sections ou plus
    paires = Counter()
    for r in resultats:
        if r["statut"] == "couverte" and r["aussi"]:
            for autre in r["aussi"]:
                paires[tuple(sorted((r["section"], autre)))] += 1
    vec = tf.vecteurs(t_cibles) if t_cibles else []
    proches = []
    for a in range(len(cibles)):
        for b in range(a + 1, len(cibles)):
            sim = tf.cosinus(vec[a], vec[b])
            if sim >= 0.5:
                proches.append({"a": cibles[a]["titre"], "b": cibles[b]["titre"], "similarite": round(sim, 2)})
    sans_requete = [c["titre"] for c in cibles
                    if not any(r["section"] == c["titre"] for r in resultats)]
    compte = Counter(r["statut"] for r in resultats)
    return {
        "requetes": len(requetes),
        "couvertes": compte["couverte"], "partielles": compte["partielle"], "non_couvertes": compte["non couverte"],
        "termes_de_tete": sorted(tete),
        "detail": resultats,
        "recouvrements": [{"a": a, "b": b, "requetes_partagees": n} for (a, b), n in paires.most_common()],
        "sections_proches": proches,
        "sections_sans_requete": sans_requete,
        "sections": len(cibles),
    }


def grille(sections, concurrents):
    """concurrents : liste de (nom, sections)."""
    tous_titres = [s["titre"] for _, secs in concurrents for s in secs if s["niveau"] in (2, 3)]
    tete = termes_de_tete(tous_titres + [s["titre"] for s in sections if s["niveau"] == 1])
    # les mots du sujet (H1 des pages) repris dans au moins un quart des titres sont aussi de tête
    h1 = [s["titre"] for s in sections if s["niveau"] == 1] + \
         [s["titre"] for _, secs in concurrents for s in secs if s["niveau"] == 1]
    compte = Counter(t for titre in tous_titres for t in set(tf.termes(titre)))
    sujet = Counter(t for titre in h1 for t in set(tf.termes(titre)))
    tete |= {t for t, n in sujet.items() if n >= max(2, len(h1) / 2) and compte[t] >= 0.25 * len(tous_titres)}
    groupes = []  # {"termes": [...], "titres": [(nom, titre)], "noms": set()}
    for nom, secs in concurrents:
        for s in secs:
            if s["niveau"] not in (2, 3):
                continue
            t = [x for x in tf.termes(s["titre"]) if x not in tete]
            if not t:
                continue
            meilleur, g_best = 0.0, None
            st = set(t)
            for g in groupes:
                for autre in g["ensembles"]:
                    inter = len(st & autre)
                    sc = inter / min(len(st), len(autre)) if inter else 0.0
                    if inter and min(len(st), len(autre)) == 1 and max(len(st), len(autre)) > 3:
                        sc *= 0.5  # un seul mot commun avec un long titre : prudence
                    if sc > meilleur:
                        meilleur, g_best = sc, g
            if g_best is not None and meilleur >= SEUIL_SOUS_THEME:
                g_best["titres"].append((nom, s["titre"]))
                g_best["noms"].add(nom)
                g_best["ensembles"].append(st)
                g_best["termes"] = list(dict.fromkeys(g_best["termes"] + t))
            else:
                groupes.append({"termes": t, "titres": [(nom, s["titre"])], "noms": {nom}, "ensembles": [st]})
    n = len(concurrents)
    cibles = sections_cibles(sections)
    t_nous = [[x for x in tf.termes(c["texte"]) if x not in tete] for c in cibles]
    lignes = []
    for g in groupes:
        part = len(g["noms"]) / n
        if n >= 3:
            classe = "attendu" if part >= 0.8 else ("courant" if part >= 0.4 else "distinctif")
        else:
            classe = "attendu" if len(g["noms"]) == n else "distinctif"
        sc, i = max(((max(tf.recouvrement(e, t) for e in g["ensembles"]), i) for i, t in enumerate(t_nous)),
                    default=(0.0, None))
        lignes.append({"sous_theme": g["titres"][0][1], "classe": classe, "concurrents": sorted(g["noms"]),
                       "nombre": len(g["noms"]), "variantes": [t for _, t in g["titres"]][:4],
                       "chez_nous": cibles[i]["titre"] if i is not None and sc >= SEUIL_NOUS else None})
    ordre = {"attendu": 0, "courant": 1, "distinctif": 2}
    lignes.sort(key=lambda l: (ordre[l["classe"]], -l["nombre"], l["sous_theme"]))
    termes_conc = [e for g in groupes for e in g["ensembles"]]
    propres = []
    for c, t in zip(cibles, t_nous):
        st = set(tf.termes(c["titre"])) - tete
        if st and not any(len(st & tc) / min(len(st), len(tc)) >= SEUIL_NOUS for tc in termes_conc if tc):
            propres.append(c["titre"])
    manques = [l for l in lignes if l["classe"] == "attendu" and not l["chez_nous"]]
    return {"concurrents": [nom for nom, _ in concurrents], "lignes": lignes,
            "manques_attendus": [l["sous_theme"] for l in manques], "angles_propres": propres}


# ------------------------------------------------------------------ affichage
def afficher_couvrir(r, plan_nom):
    out = [f"COUVERTURE · {plan_nom} · {r['requetes']} requêtes · {r['sections']} sections",
           f"  couvertes {r['couvertes']} · partielles {r['partielles']} · non couvertes {r['non_couvertes']}"]
    if r["termes_de_tete"]:
        out.append(f"  termes de tête (sujet de la page, ignorés pour le rattachement) : {', '.join(r['termes_de_tete'])}")
    nc = [d for d in r["detail"] if d["statut"] == "non couverte"]
    pa = [d for d in r["detail"] if d["statut"] == "partielle"]
    if nc:
        out += ["", "NON COUVERTES (section à créer ou à élargir, à relire : synonymes non vus)"]
        out += [f"  - {d['requete']}" for d in nc]
    if pa:
        out += ["", "PARTIELLES (la section en parle, sans répondre à toute la requête)"]
        out += [f"  - {d['requete']}  →  {d['section']} ({int(d['score'] * 100)}%)" for d in pa]
    if r["recouvrements"]:
        out += ["", "RECOUVREMENTS (deux sections répondent aux mêmes requêtes)"]
        out += [f"  - « {x['a']} » et « {x['b']} » : {x['requetes_partagees']} requête(s)" for x in r["recouvrements"]]
    if r["sections_proches"]:
        out += ["", "SECTIONS PROCHES (vocabulaire très semblable : test « si je supprime l'une, l'autre l'absorbe-t-elle ? »)"]
        out += [f"  - « {x['a']} » / « {x['b']} » ({int(x['similarite'] * 100)}%)" for x in r["sections_proches"]]
    if r["sections_sans_requete"]:
        out += ["", "SECTIONS SANS REQUÊTE (gain d'information possible, ou section à justifier)"]
        out += [f"  - {t}" for t in r["sections_sans_requete"]]
    out += ["", "COUVERTES"]
    for d in r["detail"]:
        if d["statut"] == "couverte":
            out.append(f"  - {d['requete']}  →  {d['section']}")
    verdict = "MECE OK" if not nc and not r["recouvrements"] else "À REVOIR"
    out += ["", f"VERDICT : {verdict}"]
    return "\n".join(out)


def afficher_grille(r, plan_nom):
    n = len(r["concurrents"])
    out = [f"GRILLE · {plan_nom} face à {n} concurrent(s) : {', '.join(r['concurrents'])}", "",
           f"{'classe':<11} {'chez eux':>8}  {'chez nous':<34} sous-thème"]
    for l in r["lignes"]:
        nous = l["chez_nous"] or "ABSENT"
        out.append(f"{l['classe']:<11} {l['nombre']:>3}/{n:<4}  {nous[:34]:<34} {l['sous_theme']}")
    out += ["", "ATTENDUS ABSENTS DE NOTRE PLAN (à ajouter) : " + (", ".join(r["manques_attendus"]) or "aucun"),
            "NOS ANGLES PROPRES (aucun concurrent ne les traite) : " + (", ".join(r["angles_propres"]) or "aucun")]
    if n < 3:
        out.append("Moins de 3 concurrents : la classe « courant » n'est pas calculée.")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Test MECE d'un plan : couverture des requêtes et grille des concurrents.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("couvrir", help="rattacher les requêtes aux sections du plan")
    c.add_argument("plan")
    c.add_argument("requetes")
    c.add_argument("--json", action="store_true")
    g = sub.add_parser("grille", help="sous-thèmes des concurrents : attendu, courant, distinctif")
    g.add_argument("plan")
    g.add_argument("--concurrent", action="append", required=True, help="plan Markdown ou page HTML (répéter)")
    g.add_argument("--json", action="store_true")
    a = p.parse_args()

    try:
        sections = lire_plan(a.plan)
    except OSError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    if not sections:
        print("Erreur : aucun titre trouvé dans le plan (# Titre, ## Section, ou « H2 Titre »).", file=sys.stderr)
        return 1

    if a.cmd == "couvrir":
        try:
            requetes = lire_requetes(a.requetes)
        except OSError as e:
            print(f"Erreur : {e}", file=sys.stderr)
            return 1
        if not requetes:
            print("Erreur : aucune requête lue.", file=sys.stderr)
            return 1
        r = couvrir(sections, requetes)
        print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher_couvrir(r, Path(a.plan).name))
        return 0 if not r["non_couvertes"] and not r["recouvrements"] else 2

    concurrents = []
    for f in a.concurrent:
        try:
            secs = lire_plan(f)
        except OSError as e:
            print(f"Erreur : {e}", file=sys.stderr)
            return 1
        if not secs:
            print(f"Attention : aucun titre lu dans {f} (ignoré).", file=sys.stderr)
            continue
        concurrents.append((Path(f).stem, secs))
    if not concurrents:
        print("Erreur : aucun plan concurrent lisible.", file=sys.stderr)
        return 1
    r = grille(sections, concurrents)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher_grille(r, Path(a.plan).name))
    return 2 if r["manques_attendus"] else 0


if __name__ == "__main__":
    sys.exit(main())
