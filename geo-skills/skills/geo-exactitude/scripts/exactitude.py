#!/usr/bin/env python3
"""exactitude.py : ce que les IA disent de la marque, comparé à ses vraies données.

Lit les réponses collées (même format que /geo-visibilite :
« === Moteur | id | question », la réponse dessous) et les données de la
marque, puis dresse le registre des affirmations : pour chaque phrase qui
nomme la marque et touche une donnée connue (prix, garantie, délai, année…),
un verdict.

Données acceptées :
  --contexte site-context.md   le tableau « Les données produit »
                               (| Fait | Valeur | Source | Étiquette |)
  --faits faits.csv            id;mots;valeur;unite;statut;source;gravite
                               mots : mots-clés séparés par « | » ;
                               statut : LIVE, À CONFIRMER, RETIRÉ ou FAUX
                               (FAUX : « valeur » contient une phrase fausse connue).

Verdicts du script (les 7 verdicts du Skill se complètent à la lecture) :
  exact            la valeur LIVE est dans la phrase
  périmé           la valeur d'une donnée RETIRÉE est dans la phrase
  devise           un prix dans une autre monnaie que la donnée
  différent        même unité, autre valeur : faux ou périmé, à vérifier
  faux             une phrase fausse connue (statut FAUX)
  à confirmer      la donnée de référence n'est pas encore vérifiée
  invérifiable     un chiffre sur la marque sans donnée de référence
  cadrage négatif  une mise en garde (« à éviter », « nombreuses plaintes »)

  python3 exactitude.py reponses.txt --marque "Assurly" --contexte site-context.md
  python3 exactitude.py reponses.txt --marque "Assurly" --faits faits.csv --json

Python 3 sans dépendance. Code 0, 1 en cas d'erreur d'entrée.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ICI = Path(__file__).resolve().parent
for cand in (ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (cand / "lexiques_fr.json").exists():
        COMMUN = cand
        break
else:  # pragma: no cover
    sys.exit("commun/ introuvable : lance outils/propager.py")

STATUTS = {"live": "LIVE", "a confirmer": "À CONFIRMER", "retire": "RETIRÉ", "faux": "FAUX"}
MOTS_VIDES = set("le la les de des du un une et ou en au aux a pour par sur avec sans dans son sa ses leur leurs "
                 "est sont qui que quoi dont plus moins tout tous toute toutes votre vos notre nos ce cette ces "
                 "delai prix offre formule".split())
UNITES = [
    (r"€|eur(?:o|os)?\b", "€"), (r"\$|usd\b|dollars?\b", "$"), (r"£|gbp\b|livres?\b", "£"),
    (r"%|pour ?cent\b", "%"), (r"mois\b", "mois"), (r"ans?\b|annees?\b", "an"), (r"jours?\b", "jour"),
    (r"semaines?\b", "semaine"), (r"heures?\b|h\b", "h"), (r"go\b", "Go"), (r"to\b", "To"),
]
MONNAIES = {"€", "$", "£"}
GRAVES = re.compile(r"prix|tarif|cout|garantie|delai|retractation|remboursement|condition|plafond|franchise|carence|frais")
REPRISE = re.compile(r"^(il|elle|ils|elles|son|sa|ses|leur|leurs|ce site|la plateforme|l'entreprise|la marque|cette offre)\b")


def norm(t: str) -> str:
    t = unicodedata.normalize("NFD", t or "")
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.replace("’", "'").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", t.lower()).strip()


def nombre(txt: str) -> float | None:
    txt = txt.replace(" ", "").replace(" ", "").replace(" ", "")
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", txt):
        txt = txt.replace(".", "")
    txt = txt.replace(",", ".")
    try:
        return float(txt)
    except ValueError:
        return None


RE_QTE = re.compile(r"(?<![\w.,])(\d[\d\s  .,]*\d|\d)\s*(" + "|".join(u for u, _ in UNITES) + r")?", re.I)


def quantites(phrase_n: str) -> list[tuple[float, str | None]]:
    out = []
    for m in RE_QTE.finditer(phrase_n):
        v = nombre(m.group(1))
        if v is None:
            continue
        unite = None
        if m.group(2):
            for motif, u in UNITES:
                if re.fullmatch(motif, m.group(2), re.I):
                    unite = u
                    break
        # « $ 296 » : symbole avant le nombre
        avant = phrase_n[max(0, m.start() - 2):m.start()]
        if unite is None and "$" in avant:
            unite = "$"
        if unite is None and "€" in avant:
            unite = "€"
        out.append((v, unite))
    return out


def lire_valeur(valeur: str) -> tuple[float | None, str | None]:
    q = quantites(norm(valeur))
    return q[0] if q else (None, None)


def mots_de(fait: str) -> list[str]:
    mots = [re.sub(r"^[a-z]'", "", w) for w in re.findall(r"[a-z0-9']+", norm(fait))]
    return [w for w in mots if len(w) >= 4 and w not in MOTS_VIDES][:4]


def touche(fait: dict, pn: str) -> bool:
    """CSV : un des mots-clés suffit. Contexte : deux mots du libellé (un seul s'il n'en a qu'un)."""
    presents = sum(1 for m in fait["mots"] if re.search(rf"(?<![\w]){re.escape(m)}", pn))
    return presents >= (1 if fait.get("un_mot") else min(2, len(fait["mots"])))


def statut_de(s: str) -> str:
    return STATUTS.get(norm(s).replace("é", "e"), s.strip().upper() or "LIVE")


def lire_contexte(chemin: str) -> list[dict]:
    texte = Path(chemin).read_text(encoding="utf-8")
    m = re.search(r"(?ims)^#+\s*\d*\.?\s*les donn[ée]es produit.*?\n(.*?)(?=^#|\Z)", texte)
    if not m:
        raise ValueError("pas de section « Les données produit » dans le contexte")
    faits = []
    for ligne in m.group(1).splitlines():
        cols = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cols) < 4 or set(cols[0]) <= set("-: ") or norm(cols[0]) == "fait":
            continue
        v, u = lire_valeur(cols[1])
        faits.append({"id": f"C{len(faits) + 1}", "fait": cols[0], "mots": mots_de(cols[0]), "valeur_txt": cols[1],
                      "valeur": v, "unite": u, "statut": statut_de(cols[3]), "source": cols[2],
                      "gravite": "critique" if GRAVES.search(norm(cols[0])) else "haute"})
    return faits


def lire_faits(chemin: str) -> list[dict]:
    brut = Path(chemin).read_text(encoding="utf-8-sig")
    lignes = list(csv.DictReader(io.StringIO(brut), delimiter=";" if ";" in brut.splitlines()[0] else ","))
    faits = []
    for i, l in enumerate(lignes, 1):
        l = {k.strip().lower(): (v or "").strip() for k, v in l.items() if k}
        statut = statut_de(l.get("statut", "LIVE"))
        v, u = (None, None) if statut == "FAUX" else lire_valeur(f"{l.get('valeur', '')} {l.get('unite', '')}")
        mots = [norm(x) for x in l.get("mots", "").split("|") if x.strip()]
        faits.append({"id": l.get("id") or f"F{i}", "fait": l.get("mots", ""), "mots": mots, "un_mot": True, "valeur_txt": l.get("valeur", ""),
                      "valeur": v, "unite": u, "statut": statut, "source": l.get("source", ""),
                      "gravite": l.get("gravite") or ("critique" if GRAVES.search(" ".join(mots)) else "haute")})
    return faits


RE_TETE = re.compile(r"(?m)^===\s*(.+?)\s*$")


def lire_reponses(chemin: str) -> list[dict]:
    brut = Path(chemin).read_text(encoding="utf-8-sig")
    tetes = list(RE_TETE.finditer(brut))
    out = []
    for i, m in enumerate(tetes):
        fin = tetes[i + 1].start() if i + 1 < len(tetes) else len(brut)
        champs = [c.strip() for c in m.group(1).split("|")]
        if len(champs) < 2:
            continue
        ident = champs[1] if len(champs) >= 3 and re.fullmatch(r"[A-Za-z]{0,3}\d{1,4}", champs[1]) else None
        out.append({"moteur": champs[0], "id": ident, "prompt": champs[-1], "reponse": brut[m.end():fin].strip()})
    return out


def phrases(texte: str) -> list[str]:
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý0-9«\"(*-])|\n+", texte or "") if p.strip()]


def phrases_marque(texte, motifs, question=""):
    """Phrases qui nomment la marque, plus la suivante si elle la reprend (« Elle propose… »).
    Si la question nomme la marque, toute la réponse porte sur elle."""
    if any(m.search(norm(question)) for m in motifs):
        return [(ph, "nommée" if any(m.search(norm(ph)) for m in motifs) else "question sur la marque")
                for ph in phrases(texte)]
    out, prec = [], False
    for ph in phrases(texte):
        pn = norm(ph)
        if any(m.search(pn) for m in motifs):
            out.append((ph, "nommée"))
            prec = True
        elif prec and REPRISE.match(pn):
            out.append((ph, "reprise"))
        else:
            prec = False
    return out


CONTRASTE = re.compile(r"^(?:contrairement a|a la difference de|compare a|comparee? aux?|par rapport a|face a|alors que|tandis que)\b")
NEGATION = re.compile(r"(?:\bne\b|\bn')[^,.;]{0,25}$|\b(?:pas|jamais|aucune?|plus|sans) (?:de |d')?$")


def retirer_autres(phrase_n: str, motifs, concurrents) -> str:
    """Retire ce qui parle d'un autre : concurrent dont le nom contient la marque, parenthèse qui suit
    un concurrent (« Mixpanel (fondée en 2009) »), proposition de contraste (« contrairement à X, qui… »)
    et proposition qui nomme un concurrent sans la marque."""
    t = phrase_n
    for c in concurrents:
        if any(m.search(c.pattern.replace("\\", "")) for m in motifs):
            t = c.sub(" ", t)
    for c in concurrents:
        t = re.sub(c.pattern + r"\s*\([^)]*\)", " ", t)
    morceaux = re.split(r"\s*[,;:]\s*", t)
    garde, sauter = [], False
    for m in morceaux:
        marque = any(x.search(m) for x in motifs)
        autre = any(c.search(m) for c in concurrents)
        if sauter and re.match(r"^(?:qui|dont|lequel|laquelle)\b", m) and not marque:
            continue
        sauter = False
        if CONTRASTE.match(m) and not marque:
            sauter = True
            continue
        if autre and not marque:
            continue
        garde.append(m)
    return ", ".join(garde)


def egal(a: float, b: float) -> bool:
    """Égalité au centime près (39 = 39,00) ; jamais de tolérance relative (2017 ≠ 2019)."""
    return abs(a - b) <= 0.01


def juger(phrase: str, faits: list[dict], lex_garde: list[str], motifs=(), concurrents=()) -> list[dict]:
    pn = retirer_autres(norm(phrase), motifs, concurrents)
    qs = quantites(pn)
    res = []
    for f in faits:
        if not f["mots"] or not touche(f, pn):
            continue
        if f["statut"] == "FAUX":
            v = norm(f["valeur_txt"])
            i = pn.find(v) if v else -1
            if i >= 0:
                nie = NEGATION.search(pn[:i])
                res.append({"verdict": "exact" if nie else "faux", "fait": f})  # « n'a pas de formule gratuite »
            continue
        if f["statut"] == "RETIRÉ":
            res.append({"verdict": "périmé", "fait": f})  # l'offre ou la donnée n'existe plus, chiffre ou non
            continue
        if f["valeur"] is None:
            continue
        annee = f["unite"] == "an" and 1800 <= f["valeur"] <= 2100
        if annee:
            annees = [float(a) for a in re.findall(r"(?<!\d)(1[89]\d\d|20\d\d)(?!\d)", pn)]
            if annees:
                ok = any(egal(a, f["valeur"]) for a in annees)
                res.append({"verdict": ("exact" if f["statut"] == "LIVE" else "à confirmer") if ok else
                            ("différent" if f["statut"] == "LIVE" else "à confirmer"), "fait": f})
            continue
        memes = [q for q in qs if egal(q[0], f["valeur"]) and (q[1] == f["unite"] or q[1] is None or f["unite"] is None)]
        if memes:
            res.append({"verdict": {"LIVE": "exact", "RETIRÉ": "périmé", "À CONFIRMER": "à confirmer"}.get(f["statut"], "exact"),
                        "fait": f})
            continue
        if f["statut"] != "LIVE":
            continue
        if f["unite"] in MONNAIES and any(q[1] in MONNAIES and q[1] != f["unite"] for q in qs):
            res.append({"verdict": "devise", "fait": f})
        elif any(q[1] == f["unite"] for q in qs if q[1]):
            res.append({"verdict": "différent", "fait": f})
    if not res and any(q[1] or q[0] >= 10 for q in qs if not (1800 <= q[0] <= 2100 and q[1] is None)):
        res.append({"verdict": "invérifiable", "fait": None})
    if any(re.search(rf"(?<![\w']){re.escape(g)}(?![\w])", pn) for g in lex_garde):
        res.append({"verdict": "cadrage négatif", "fait": None})
    return res


GRAVITE = {"faux": 0, "devise": 0, "périmé": 1, "différent": 1, "cadrage négatif": 2, "à confirmer": 3, "invérifiable": 3, "exact": 4}


def analyser(reponses, marque, alias, faits, concurrents=()):
    lex = json.loads((COMMUN / "lexiques_fr.json").read_text(encoding="utf-8"))
    garde = [norm(x) for x in lex["mise_en_garde"]]
    motifs = [re.compile(rf"(?<![\w]){re.escape(norm(n))}(?![\w])") for n in [marque] + alias]
    conc = [re.compile(rf"(?<![\w]){re.escape(norm(n))}(?![\w])") for n in concurrents]
    registre = []
    for r in reponses:
        for ph, mode in phrases_marque(r["reponse"], motifs, r["prompt"]):
            if mode == "nommée" and not any(m.search(retirer_autres(norm(ph), motifs, conc)) for m in motifs):
                continue  # le nom lu était celui d'un concurrent homonyme
            for j in juger(ph, faits, garde, motifs, conc):
                f = j["fait"]
                grav = f["gravite"] if f and j["verdict"] in ("faux", "devise", "périmé", "différent") else (
                    "moyenne" if j["verdict"] == "cadrage négatif" else "basse")
                if j["verdict"] in ("faux", "devise") and f and f["gravite"] == "critique":
                    grav = "critique"
                registre.append({"moteur": r["moteur"], "question": r["id"] or r["prompt"][:60], "verdict": j["verdict"],
                                 "gravite": grav, "fait": f["fait"] if f else None,
                                 "reference": f"{f['valeur_txt'] or f['fait']} ({f['statut']}, {f['source']})" if f else None,
                                 "phrase": ph, "lecture": mode})
    registre.sort(key=lambda x: (GRAVITE.get(x["verdict"], 9), x["moteur"], str(x["question"])))
    compte = Counter((x["moteur"], x["verdict"]) for x in registre)
    return {"registre": registre, "compte": {f"{m} · {v}": n for (m, v), n in sorted(compte.items())},
            "reponses": len(reponses), "faits": len(faits)}


def afficher(r, marque):
    L = [f"EXACTITUDE · {marque} · {r['reponses']} réponses lues · {r['faits']} données de référence · {len(r['registre'])} affirmations", ""]
    if not r["registre"]:
        L.append("Aucune affirmation chiffrée ni mise en garde sur la marque dans ces réponses.")
    for x in r["registre"]:
        if x["verdict"] == "exact":
            continue
        ref = f" · référence : {x['reference']}" if x["reference"] else ""
        L.append(f"{x['verdict'].upper():<16}{x['gravite']:<10}{x['moteur']} · {x['question']}{ref}")
        L.append(f"    « {x['phrase'][:220]} »" + ({"reprise": " (phrase qui reprend la marque)", "question sur la marque": " (réponse à une question sur la marque)"}.get(x["lecture"], "")))
    exacts = sum(1 for x in r["registre"] if x["verdict"] == "exact")
    L += ["", f"EXACT · {exacts} affirmation(s) conforme(s) aux données LIVE.",
          "Verdicts à compléter à la lecture : incomplet, ambigu, opinion présentée comme un fait."]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Registre des affirmations des IA sur une marque, comparées à ses données.")
    ap.add_argument("reponses", help="réponses collées (=== Moteur | id | question)")
    ap.add_argument("--marque", required=True)
    ap.add_argument("--alias", action="append", default=[])
    ap.add_argument("--concurrent", action="append", default=[],
                    help="nom d'un concurrent (répétable) : ses faits ne sont pas lus comme ceux de la marque")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--contexte", help="site-context.md (tableau « Les données produit »)")
    src.add_argument("--faits", help="faits.csv (id;mots;valeur;unite;statut;source;gravite)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        faits = lire_contexte(a.contexte) if a.contexte else lire_faits(a.faits)
        reponses = lire_reponses(a.reponses)
    except (OSError, ValueError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    if not reponses:
        print("Aucune réponse lue : chaque réponse commence par « === Moteur | question ».", file=sys.stderr)
        return 1
    r = analyser(reponses, a.marque, a.alias, faits, a.concurrent)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r, a.marque))
    return 0


if __name__ == "__main__":
    sys.exit(main())
