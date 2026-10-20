#!/usr/bin/env python3
"""analyser_lot.py : passer de 40 à 50 annonces ChatGPT Ads à 120 ou plus, sans doublons (Python 3, sans dépendance).

Commandes :

  analyser CAMPAGNE [--cible 120] [--lot 50] [--md plan.md]
      CAMPAGNE : le JSON de /chatgpt-ads-skills (ou un classeur au schéma
      d'annonces). Décrit comment les annonces sont construites : nombre par
      groupe, structures de titre (question, impératif, chiffre, situation,
      groupe nominal), facettes d'intention couvertes (problème, objectif,
      compromis, contrainte, comparaison, occasion, budget, question), angles
      déclarés, mots trop répétés, quasi-doublons, allégations utilisées ;
      puis le plan du prochain lot : combien par groupe (les moins garnis
      d'abord), quelles structures et facettes manquent, quels mots éviter.

  ajouter CAMPAGNE LOT.json -o CAMPAGNE-SUIVANTE.json [--limites import|api]
      LOT.json : {"ads": [...]} au format de la campagne. Chaque nouvelle
      annonce est contrôlée contre toutes les autres (doublon exact, quasi-
      doublon, titre déjà pris dans un autre groupe), contre les limites,
      les groupes existants et la liste d'allégations. Les annonces
      acceptées sont ajoutées ; les refusées sont listées avec la raison.

  noter CAMPAGNE [--md notes.md]
      Note chaque annonce de 1 à 5 sur ce qui se mesure (longueur, caractère
      distinct, allégations) et prépare les colonnes de jugement (page,
      intention, clarté) ; propose Conserver, Corriger ou Supprimer. Ne
      supprime rien.

Les seuils (similarité 0,6 sur les mots, 0,75 sur les trigrammes de
caractères, 30% de titres pour un mot « trop répété ») sont des choix du
pack, réglables dans le code, à tester.

Codes de sortie : 0 ok · 2 points à revoir · 3 lot refusé en entier · 1 usage.
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve()
for base in (ICI.parents[1] / "commun", ICI.parents[2] / "commun"):   # Skill seul, ou ZIP claude.ai
    if (base / "classeur.py").exists():
        sys.path.insert(0, str(base))
        break
import classeur as cl  # noqa: E402
import signaux as sg  # noqa: E402

SEUIL_MOTS, SEUIL_TRIGRAMMES, SEUIL_REPETITION = 0.6, 0.75, 0.30
CIBLES = {"title": (16, 24), "copy": (32, 48)}
MOTS_VIDES = set("""a au aux avec ce ces cet cette d de des du en et l la le les leur leurs mon ma mes notre nos ou
par pour sa se ses son sur ta te tes ton un une vos votre à y qu que qui dans est sont plus pas ne n s il elle on
nous vous je j tout tous toute toutes""".split())
IMPERATIFS = re.compile(r"^(?:\w+ez|découvre|essaie|compare|prépare|trouve|offre|passe|choisis|réserve|commande|"
                        r"profite|teste|obtiens|demande|lance|crée|simplifie|gagne|économise|pars)\b", re.I)
SITUATION = re.compile(r"^(?:pour|quand|si|avant|après|en|dès|sans|même|entre|chez|au|à)\b", re.I)
FACETTES = {
    "comparaison": r"\b(?:vs|ou bien|plutôt que|compar\w*|neuf ou|lequel|laquelle|entre)\b|\bou\b.*\?",
    "budget": r"(?:€|\bprix\b|\bbudget\b|\btarifs?\b|\bdès\b|\béconomi\w*|\bpas cher|\bmoins de\b)",
    "question": r"\?",
    "occasion": r"\b(?:cadeau|noël|rentrée|été|hiver|départ|anniversaire|mariage|déménag\w*|vacances|week-end|fête)\b",
    "contrainte": r"\b(?:sans|même si|petit espace|peu de temps|pas le temps|sans voiture|sans fenêtre|obligatoire)\b",
    "objectif": r"\b(?:pour (?:\w+er|\w+ir|\w+re)\b|objectif|réussir|atteindre|enfin)\b",
    "problème": r"\b(?:marre|problème|éviter|fini|trop|galère|stress|oubli\w*|perdu|panne)\b",
    "compromis": r"\b(?:sans renoncer|à la fois|tout en|sans sacrifier|équilibre|compromis)\b",
}


# ---------------------------------------------------------------- outils texte

def mots(t):
    return [m for m in re.findall(r"[a-z0-9]+", cl.plier(t)) if m not in MOTS_VIDES]


def racine(m):
    for suf in ("issements", "ements", "ations", "ation", "ement", "euses", "euse", "eurs", "eur", "ees", "es", "s", "e"):
        if len(m) > len(suf) + 3 and m.endswith(suf):
            return m[: -len(suf)]
    return m


def jaccard(a, b):
    x, y = {racine(m) for m in mots(a)}, {racine(m) for m in mots(b)}
    return len(x & y) / len(x | y) if x and y else 0.0


def trigrammes(t):
    s = f"  {cl.plier(t)} "
    return {s[i:i + 3] for i in range(len(s) - 2)}


def similarite(a, b):
    """(mots, trigrammes) entre deux annonces « titre + copie »."""
    ta, tb = trigrammes(a), trigrammes(b)
    return jaccard(a, b), (len(ta & tb) / len(ta | tb) if ta and tb else 0.0)


def structure(titre):
    t = titre.strip()
    if t.endswith("?"):
        return "question"
    if re.match(r"^\d", t):
        return "chiffre"
    if IMPERATIFS.match(t):
        return "impératif"
    if SITUATION.match(t):
        return "situation"
    return "groupe nominal"


def facettes(texte):
    return sorted(f for f, m in FACETTES.items() if re.search(m, texte, re.I))


# ---------------------------------------------------------------- chargement

def charger(source):
    p = Path(source)
    if p.suffix.lower() in (".xlsx", ".csv"):
        _, lignes = cl.annonces(cl.lire(p))
        ads = [{"adgroup_name": cl.texte(x.get("adgroup_name") or x.get("ad_group_id")), "title": cl.texte(x.get("title")),
                "copy": cl.texte(x.get("copy")), "link": cl.texte(x.get("link")),
                "image_url": cl.texte(x.get("image_url")), "image_file_id": cl.texte(x.get("image_file_id")),
                "ad_group_id": cl.texte(x.get("ad_group_id")), "status": cl.texte(x.get("status")),
                "ad_name": cl.texte(x.get("ad_name"))} for x in lignes]
        groupes = sorted({a["adgroup_name"] for a in ads})
        return {"adgroups": [{"adgroup_name": g} for g in groupes], "ads": ads, "_source_xlsx": True}
    return json.loads(p.read_text(encoding="utf-8"))


def texte_annonce(a):
    return f"{a.get('title', '')} {a.get('copy', '')}"


# ---------------------------------------------------------------- analyse

def quasi_doublons(ads):
    paires = []
    for i in range(len(ads)):
        for j in range(i + 1, len(ads)):
            sm, st = similarite(texte_annonce(ads[i]), texte_annonce(ads[j]))
            if sm >= SEUIL_MOTS or st >= SEUIL_TRIGRAMMES:
                paires.append((i, j, round(sm, 2), round(st, 2)))
    return paires


def analyser(camp, cible=120, lot=50):
    ads = camp.get("ads", [])
    groupes = [g.get("adgroup_name") for g in camp.get("adgroups", [])] or sorted({a.get("adgroup_name") for a in ads})
    par_groupe = {g: [a for a in ads if a.get("adgroup_name") == g] for g in groupes}
    res = {"annonces": len(ads), "groupes": len(groupes), "cible": cible, "par_groupe": {}}
    # vocabulaire
    titres_mots = [set(racine(m) for m in mots(a.get("title", ""))) for a in ads]
    compte = {}
    for s in titres_mots:
        for m in s:
            compte[m] = compte.get(m, 0) + 1
    repetes = sorted(((m, n) for m, n in compte.items() if ads and n / len(ads) >= SEUIL_REPETITION), key=lambda x: -x[1])
    res["mots_repetes"] = [{"mot": m, "titres": n, "part": round(100 * n / len(ads))} for m, n in repetes]
    # doublons
    paires = quasi_doublons(ads)
    res["quasi_doublons"] = [{"a": f"{ads[i].get('adgroup_name')} · {ads[i].get('title')}",
                              "b": f"{ads[j].get('adgroup_name')} · {ads[j].get('title')}", "mots": sm, "trigrammes": st}
                             for i, j, sm, st in paires]
    titres = {}
    for a in ads:
        titres.setdefault(cl.plier(a.get("title", "")), set()).add(a.get("adgroup_name"))
    res["titres_partages"] = [t for t, gs in titres.items() if len(gs) > 1 and t]
    # allégations
    approuvees = {cl.plier(x.get("texte", "")) for x in camp.get("allegations", []) if cl.plier(x.get("statut", "")) == "approuvee"}
    usage = {}
    for a in ads:
        for s in sg.sensibles(texte_annonce(a)):
            usage[s] = usage.get(s, 0) + 1
    res["allegations_utilisees"] = usage
    res["allegations_approuvees"] = len(approuvees)
    # par groupe et plan
    restant = max(0, cible - len(ads))
    besoin = {}
    if groupes:
        objectif = math.ceil(cible / len(groupes))
        for g in groupes:
            besoin[g] = max(0, objectif - len(par_groupe[g]))
    a_faire = min(lot, restant)
    plan = {g: 0 for g in groupes}
    while a_faire > 0:          # remplissage par le bas : toujours le groupe le moins garni
        ouverts = [g for g in groupes if plan[g] < besoin[g]]
        if not ouverts:
            break
        g = min(ouverts, key=lambda x: (len(par_groupe[x]) + plan[x], groupes.index(x)))
        plan[g] += 1
        a_faire -= 1
    for g in groupes:
        lst = par_groupe[g]
        structs, facs, angles = {}, {}, {}
        for a in lst:
            s = structure(a.get("title", ""))
            structs[s] = structs.get(s, 0) + 1
            for f in facettes(texte_annonce(a)):
                facs[f] = facs.get(f, 0) + 1
            if a.get("angle"):
                angles[a["angle"]] = angles.get(a["angle"], 0) + 1
        dominante = max(structs.items(), key=lambda x: x[1]) if structs else None
        res["par_groupe"][g] = {
            "annonces": len(lst),
            "a_ajouter": plan.get(g, 0),
            "structures": structs,
            "structure_dominante": dominante[0] if dominante and len(lst) >= 4 and dominante[1] / len(lst) > 0.5 else None,
            "structures_absentes": [s for s in ("question", "impératif", "chiffre", "situation", "groupe nominal") if s not in structs],
            "facettes": facs,
            "facettes_absentes": [f for f in FACETTES if f not in facs],
            "angles": angles,
        }
    res["lot_suivant"] = sum(plan.values())
    res["reste_apres_lot"] = max(0, restant - res["lot_suivant"])
    return res


def plan_md(a):
    out = [f"# Plan du prochain lot", "",
           f"{a['annonces']} annonces dans {a['groupes']} groupe(s) ; cible {a['cible']}. "
           f"Ce lot : **{a['lot_suivant']} annonces** ; il en restera {a['reste_apres_lot']} après.", "",
           "| Groupe | Actuelles | À ajouter | Structures absentes | Facettes absentes | Angles déclarés |",
           "|---|---|---|---|---|---|"]
    for g, x in a["par_groupe"].items():
        dom = f" (trop de « {x['structure_dominante']} »)" if x["structure_dominante"] else ""
        angles = ", ".join(f"{k} {v}" for k, v in x["angles"].items()) or "non déclarés"
        out.append(f"| {g} | {x['annonces']} | {x['a_ajouter']} | {', '.join(x['structures_absentes']) or '-'}{dom} | "
                   f"{', '.join(x['facettes_absentes'][:4]) or '-'} | {angles} |")
    if a["mots_repetes"]:
        out += ["", "**Mots à éviter dans ce lot** (présents dans 30% des titres ou plus) : "
                + ", ".join(f"{x['mot']} ({x['part']}%)" for x in a["mots_repetes"])]
    if a["quasi_doublons"]:
        out += ["", f"**Quasi-doublons déjà présents ({len(a['quasi_doublons'])})**, à corriger avant d'ajouter :", ""]
        out += [f"- {x['a']} / {x['b']} (mots {x['mots']}, trigrammes {x['trigrammes']})" for x in a["quasi_doublons"][:15]]
    if a["titres_partages"]:
        out += ["", "**Titres repris dans plusieurs groupes** : " + ", ".join(a["titres_partages"][:10])]
    out += ["", "Facettes repérées par mots indicateurs : une indication, pas un verdict. Les angles déclarés "
                "(champ `angle`) sont plus fiables."]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- ajout d'un lot

def ajouter(camp, lot, limites="import"):
    lim = cl.LIMITES[limites]
    ads = camp.get("ads", [])
    groupes = {g.get("adgroup_name") for g in camp.get("adgroups", [])} or {a.get("adgroup_name") for a in ads}
    approuvees = [cl.plier(x.get("texte", "")) for x in camp.get("allegations", []) if cl.plier(x.get("statut", "")) == "approuvee"]
    titres = {cl.plier(a.get("title", "")): a.get("adgroup_name") for a in ads}
    acceptees, refusees = [], []
    for n, a in enumerate(lot.get("ads", []), 1):
        raisons = []
        if a.get("adgroup_name") not in groupes:
            raisons.append(f"groupe « {a.get('adgroup_name')} » inconnu")
        for c in ("title", "copy"):
            L = cl.longueur(a.get(c, ""))
            if not a.get(c):
                raisons.append(f"{c} vide")
            elif L > lim[c]:
                raisons.append(f"{c} {L} caractères (max {lim[c]})")
        t = cl.plier(a.get("title", ""))
        if t in titres:
            raisons.append("titre déjà utilisé" + ("" if titres[t] == a.get("adgroup_name") else f" dans « {titres[t]} »"))
        for s in sg.sensibles(texte_annonce(a)):
            if not any(cl.plier(s) in x for x in approuvees):
                raisons.append(f"allégation non approuvée « {s} »")
        for b in ads + acceptees:
            sm, st = similarite(texte_annonce(a), texte_annonce(b))
            if sm >= SEUIL_MOTS or st >= SEUIL_TRIGRAMMES:
                raisons.append(f"quasi-doublon de « {b.get('title')} » (mots {sm:.2f}, trigrammes {st:.2f})")
                break
        if raisons:
            refusees.append({"n": n, "title": a.get("title"), "groupe": a.get("adgroup_name"), "raisons": raisons})
        else:
            acceptees.append(a)
            titres[t] = a.get("adgroup_name")
    return acceptees, refusees


# ---------------------------------------------------------------- notes

def noter(camp):
    ads = camp.get("ads", [])
    approuvees = [cl.plier(x.get("texte", "")) for x in camp.get("allegations", []) if cl.plier(x.get("statut", "")) == "approuvee"]
    sims = [0.0] * len(ads)
    jumeaux = [None] * len(ads)
    for i in range(len(ads)):
        for j in range(len(ads)):
            if i != j:
                s = max(similarite(texte_annonce(ads[i]), texte_annonce(ads[j])))
                if s > sims[i]:
                    sims[i], jumeaux[i] = s, j
    res = []
    for i, a in enumerate(ads):
        notes = {}
        L = [(c, cl.longueur(a.get(c, ""))) for c in ("title", "copy")]
        lim = cl.LIMITES["import"]
        if any(n > lim[c] for c, n in L):
            notes["longueur"] = 1
        else:
            notes["longueur"] = 5 if all(CIBLES[c][0] <= n for c, n in L) else 4
        s = sims[i]
        notes["distinct"] = 5 if s < 0.3 else 4 if s < 0.45 else 3 if s < SEUIL_MOTS else 2 if s < 0.8 else 1
        sens = sg.sensibles(texte_annonce(a))
        non_app = [x for x in sens if not any(cl.plier(x) in y for y in approuvees)]
        notes["sources"] = 1 if non_app else 5
        proposition, raison = "Conserver", ""
        if non_app:
            proposition, raison = "Supprimer", f"allégation non approuvée : {', '.join(non_app)}"
        elif notes["distinct"] <= 2 and jumeaux[i] is not None and i > jumeaux[i]:
            proposition, raison = "Supprimer", f"quasi-doublon de « {ads[jumeaux[i]].get('title')} »"
        elif notes["longueur"] == 1:
            proposition, raison = "Corriger", "trop long"
        elif notes["distinct"] == 3:
            proposition, raison = "Corriger", f"proche de « {ads[jumeaux[i]].get('title')} »"
        res.append({"groupe": a.get("adgroup_name"), "title": a.get("title"), "copy": a.get("copy"), **notes,
                    "page": None, "intention": None, "clarte": None, "proposition": proposition, "raison": raison})
    return res


def notes_md(notes):
    out = ["| Groupe | Titre | Longueur | Distinct | Sources | Page | Intention | Clarté | Proposition | Raison |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for x in notes:
        out.append(f"| {x['groupe']} | {x['title']} | {x['longueur']} | {x['distinct']} | {x['sources']} | ? | ? | ? | "
                   f"{x['proposition']} | {x['raison']} |")
    tot = {p: sum(1 for x in notes if x["proposition"] == p) for p in ("Conserver", "Corriger", "Supprimer")}
    out += ["", f"Conserver {tot['Conserver']} · Corriger {tot['Corriger']} · Supprimer {tot['Supprimer']}. "
                "Les colonnes « ? » se notent au jugement (1 à 5) : la page tient-elle la promesse, l'annonce "
                "répond-elle à l'intention du groupe, la valeur est-elle claire ?"]
    return "\n".join(out) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sp = p.add_subparsers(dest="cmd", required=True)
    an = sp.add_parser("analyser")
    an.add_argument("campagne")
    an.add_argument("--cible", type=int, default=120)
    an.add_argument("--lot", type=int, default=50)
    an.add_argument("--md")
    aj = sp.add_parser("ajouter")
    aj.add_argument("campagne")
    aj.add_argument("lot")
    aj.add_argument("-o", "--sortie", required=True)
    aj.add_argument("--limites", choices=("import", "api"), default="import")
    no = sp.add_parser("noter")
    no.add_argument("campagne")
    no.add_argument("--md")
    a = p.parse_args(argv)
    for f in [a.campagne] + ([a.lot] if a.cmd == "ajouter" else []):
        if not Path(f).exists():
            print(f"Fichier introuvable : {f}", file=sys.stderr)
            return 1
    camp = charger(a.campagne)

    if a.cmd == "analyser":
        if a.lot > 50:
            print("Un lot de plus de 50 annonces se relit mal : 50 au plus (choix du pack).", file=sys.stderr)
        res = analyser(camp, a.cible, min(a.lot, 50))
        md = plan_md(res)
        if a.md:
            Path(a.md).write_text(md, encoding="utf-8")
        print(md)
        return 2 if res["quasi_doublons"] or res["titres_partages"] else 0

    if a.cmd == "ajouter":
        lot = json.loads(Path(a.lot).read_text(encoding="utf-8"))
        acceptees, refusees = ajouter(camp, lot, a.limites)
        camp["ads"] = camp.get("ads", []) + acceptees
        Path(a.sortie).write_text(json.dumps(camp, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Lot : {len(acceptees)} acceptée(s), {len(refusees)} refusée(s). Total : {len(camp['ads'])} annonces → {a.sortie}")
        for r in refusees:
            print(f"  ✖ n°{r['n']} « {r['title']} » ({r['groupe']}) : {' ; '.join(r['raisons'])}")
        if not acceptees and refusees:
            return 3
        return 2 if refusees else 0

    if a.cmd == "noter":
        notes = noter(camp)
        md = notes_md(notes)
        if a.md:
            Path(a.md).write_text(md, encoding="utf-8")
        print(md)
        return 2 if any(x["proposition"] != "Conserver" for x in notes) else 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
