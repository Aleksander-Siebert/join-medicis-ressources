#!/usr/bin/env python3
"""affirmations.py : chaque affirmation vérifiable d'un texte, et sa source.

Relève dans un article (Markdown ou texte) les phrases qui affirment un fait
vérifiable : pourcentage, montant, délai, chiffre, texte de loi, étude,
promesse (« garanti », « 100% remboursé », « le moins cher »). Pour chacune,
il dit si elle a une source :

  sourcée      lien, « (source : …) », « selon l'Insee », note [^1]
  fournie      ses chiffres viennent de site-context.md ou reserve.md
  vague        « une étude », « des experts », « selon les spécialistes » :
               ce n'est pas une source
  sans source  rien
  trou         {{à compléter}} : assumé, listé pour l'utilisateur

En mode --ymyl (santé, argent, assurance, droit), une affirmation chiffrée,
légale ou une promesse sans source bloque la publication.

Codes de sortie : 0 rien à vérifier · 2 à vérifier · 3 bloqué (YMYL) ·
1 erreur d'utilisation.

Le script lit, il ne juge pas la vérité d'un fait : une affirmation
« sourcée » peut citer une mauvaise source. Le Skill vérifie les sources.

Exemples :
  python3 affirmations.py article.md
  python3 affirmations.py article.md --ymyl --contexte site-context.md --reserve reserve.md
  python3 affirmations.py --texte "Selon une étude, 73% des Français…" --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
for _c in (ICI, ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (_c / "texte_fr.py").exists():
        sys.path.insert(0, str(_c))
        break
import texte_fr as tf  # noqa: E402

NB = r"\d[\d   ]*(?:[.,]\d+)?"
MOIS = r"(?:janvier|f[ée]vrier|mars|avril|mai|juin|juillet|ao[ûu]t|septembre|octobre|novembre|d[ée]cembre)"

TYPES = [
    ("pourcentage", re.compile(NB + r"\s?(?:%|pour ?cent)", re.I)),
    ("montant", re.compile(r"(?:" + NB + r"\s?(?:€|euros?\b|eur\b|k€|m€|millions? d'euros|milliards? d'euros)|€\s?" + NB + ")", re.I)),
    ("délai", re.compile(r"\b" + NB + r"\s?(?:jours?|j\b|mois|ans?\b|ann[ée]es?|semaines?|heures?|h\b|minutes?|min\b)", re.I)),
    ("loi", re.compile(r"\b(?:art(?:icle|\.)\s*[LRD]?\.?\s*\d[\d\-]*|loi (?:n°\s*)?\d[\d\-]*|loi du \d|d[ée]cret|ordonnance n°|"
                       r"code (?:de la|du|des|civil|p[ée]nal|g[ée]n[ée]ral)|directive (?:\(ue\)|ue|europ[ée]enne)|r[èe]glement \(ue\))", re.I)),
    ("étude", re.compile(r"\b(?:[ée]tudes?|enqu[êe]tes?|sondages?|barom[èe]tres?|rapports?|statistiques?|chiffres? officiels?)\b", re.I)),
    ("promesse", re.compile(r"\b(?:(?:est|sont|c'est|reste|restent) garanti(?:e|s|es)?|garanti(?:e|s|es)? (?:à vie|à 100|sans|pendant|quoi qu'il)|"
                            r"satisfait ou rembours\w+|100\s?% rembours\w*|rembours\w* (?:int[ée]gralement|à 100)|sans (?:aucun )?risque|aucun risque|"
                            r"(?:le|la|les) (?:moins ch[èe]re?s?|meilleure?s?|seule?s?) (?:du march[ée]|de france|offre|mutuelle|assurance|solution|prix)|"
                            r"n°\s?1\b|num[ée]ro 1\b|leader (?:du|de|en)|imbattable|z[ée]ro reste à charge)", re.I)),
    ("chiffre", re.compile(r"\b\d{1,3}(?:[\u202f\u00a0 ]\d{3})+\b|\b\d{5,}\b|\b\d{2,}\s+(?:clients?|personnes|patients|assur[ée]s|entreprises|salari[ée]s|"
                           r"utilisateurs|ind[ée]pendants|dossiers|sinistres|contrats|adh[ée]rents|fois)\b", re.I)),
    ("date", re.compile(r"\b(?:depuis|en|au|du|le|à partir du)\s+(?:(?:1er|\d{1,2})\s+" + MOIS + r"\s+)?(?:19|20)\d{2}\b", re.I)),
]

VAGUE = re.compile(r"\b(?:selon|d'apr[èe]s)\s+(?:une|des|certaines?|plusieurs|de nombreuses|r[ée]centes?)\s+(?:[ée]tudes?|enqu[êe]tes?|sources?|experts?|sp[ée]cialistes?|recherches?)"
                   r"|\b(?:une|des|plusieurs|de nombreuses|certaines?) (?:[ée]tudes?|recherches?|enqu[êe]tes?)\s+(?:r[ée]centes?\s+)?(?:montrent|r[ée]v[èe]lent|indiquent|prouvent|sugg[èe]rent|ont montr[ée])"
                   r"|\b(?:les|des|nos|certains) (?:experts?|sp[ée]cialistes?|professionnels?|scientifiques)\s+(?:estiment|affirment|recommandent|s'accordent|disent)"
                   r"|\bon (?:estime|sait|dit) que\b|\bil est (?:prouv[ée]|d[ée]montr[ée]|bien connu) que\b|\bselon (?:certains|les sp[ée]cialistes|les experts)\b"
                   r"|\b(?:la plupart|la majorit[ée]) des (?:fran[çc]ais|gens|personnes|entreprises|ind[ée]pendants)\b", re.I)

SOURCE = re.compile(r"\]\(https?://|https?://\S+|\[\^\w+\]|\[\d+\]|\(\s*sources?\s*:|\bsources?\s*:\s*\S"
                    r"|\b[a-z0-9\-]+\.(?:gouv\.fr|fr|org|com|eu|int)\b"
                    r"|\b(?:service-public|legifrance|ameli|insee|drees|urssaf|cnil|has-sante|ansm|acpr|amf|dgccrf|eurostat|oms)\b", re.I)
# Un nom propre après « selon », « d'après »… (sensible à la casse : « selon une étude » n'en est pas un)
NOMME = re.compile(r"\b(?:[Ss]elon|[Dd]'apr[èe]s|[Dd]’apr[èe]s|[Ss]ource|[Pp]ubli[ée]e? par|[Cc]hiffres? de|[Dd]onn[ée]es? de)\s+"
                   r"(?:l'|l’|la |le |les )?[A-ZÉÈÀ][\w\-’']+")


def a_source(p):
    return bool(SOURCE.search(p) or NOMME.search(p))


TROU = re.compile(r"\{\{[^}]*\}\}")
SENSIBLES = {"pourcentage", "montant", "délai", "loi", "promesse", "chiffre"}


def nombres(texte):
    """Nombres normalisés d'un texte (« 3 200 » → 3200, « 1,5 » → 1.5)."""
    out = set()
    for m in re.finditer(NB, texte):
        n = re.sub(r"[\s  ]", "", m.group(0)).replace(",", ".").rstrip(".")
        if n and re.fullmatch(r"\d+(\.\d+)?", n):
            out.add(n.rstrip("0").rstrip(".") if "." in n else n)
    return out


UNITES = [("%", r"%|pour ?cent"), ("€", r"€|euros?\b|eur\b"), ("h", r"h\b|heures?"), ("jour", r"j\b|jours?"),
          ("semaine", r"semaines?"), ("mois", r"mois"), ("an", r"ans?\b|ann[ée]es?"), ("min", r"min\b|minutes?")]
_QTE = re.compile(r"(" + NB + r")\s?(" + "|".join(u for _, u in UNITES) + r")?", re.I)


def quantites(texte):
    """Couples (nombre normalisé, unité) : « 48 h » → ("48", "h"), « 3 200 clients » → ("3200", "")."""
    out = set()
    for m in _QTE.finditer(texte):
        n = re.sub(r"[\s\u202f\u00a0]", "", m.group(1)).replace(",", ".").rstrip(".")
        if not re.fullmatch(r"\d+(\.\d+)?", n):
            continue
        n = n.rstrip("0").rstrip(".") if "." in n else n
        unite = ""
        if m.group(2):
            for nom, rx in UNITES:
                if re.fullmatch(rx, m.group(2), re.I):
                    unite = nom
                    break
        out.add((n, unite))
    return out


def lignes_de(texte):
    """(numéro de ligne, phrase) pour le texte hors blocs de code et hors bloc méta."""
    out = []
    dans_code = False
    for n, ligne in enumerate(texte.splitlines(), 1):
        if ligne.strip().startswith("```"):
            dans_code = not dans_code
            continue
        if dans_code or not ligne.strip() or re.match(r"^\s{0,3}#{1,6}\s", ligne):
            continue  # un titre annonce, il n'affirme pas
        for p in tf.phrases(ligne):
            out.append((n, p))
    return out


def analyser(texte, ymyl=False, faits=""):
    faits_q = quantites(faits)
    resultats = []
    toutes = lignes_de(texte)
    for i, (n, p) in enumerate(toutes):
        types = [nom for nom, rx in TYPES if rx.search(p)]
        vague = bool(VAGUE.search(p))
        if vague and "étude" not in types:
            types.append("étude")
        if TROU.search(p) and not types:
            types = ["à compléter"]
        if not types:
            continue
        if "promesse" in types and re.search(r"\b(?:n'existe pas|n'est pas|ne (?:sont|sont jamais|garantit) pas|aucune? (?:mutuelle|offre|contrat))\b", p, re.I):
            types.remove("promesse")
        if not types:
            continue
        if types == ["date"]:
            continue  # une date seule situe, elle n'affirme pas
        if types == ["étude"] and not vague and not re.search(r"\d", p):
            continue  # « une étude de cas », « l'étude de votre dossier »
        voisine = toutes[i + 1][1] if i + 1 < len(toutes) and toutes[i + 1][0] == n else ""
        q = {x for x in quantites(p) if not (x[1] == "" and x[0] in {"1", "2", "3", "4"})}
        q = {x for x in q if not (x[1] == "" and len(x[0]) == 4 and x[0].startswith(("19", "20")))}
        if TROU.search(p):
            statut = "trou"
        elif vague and not a_source(p):
            statut = "vague"
        elif a_source(p) or (voisine and re.match(r"^\(?\s*sources?\s*:", voisine, re.I)):
            statut = "sourcée"
        elif q and faits_q and q <= faits_q:
            statut = "fournie"
        else:
            statut = "sans source"
        sensible = bool(set(types) & SENSIBLES) or vague
        if statut in ("sans source", "vague") and ymyl and sensible:
            gravite = "bloquant"
        elif statut in ("sans source", "vague"):
            gravite = "à vérifier"
        elif statut == "trou":
            gravite = "trou"
        else:
            gravite = "ok"
        resultats.append({"ligne": n, "phrase": p, "types": types, "statut": statut, "gravite": gravite})
    compte = {k: sum(1 for r in resultats if r["gravite"] == k) for k in ("bloquant", "à vérifier", "trou", "ok")}
    if compte["bloquant"]:
        verdict, code = "BLOQUÉ", 3
    elif compte["à vérifier"]:
        verdict, code = "À VÉRIFIER", 2
    else:
        verdict, code = "OK", 0
    return {"affirmations": resultats, "compte": compte, "ymyl": ymyl, "verdict": verdict, "code": code}


CONSEILS = {
    "vague": "Nommer la source (organisme, date, lien) ou retirer l'affirmation. « Une étude » n'est pas une source.",
    "sans source": "Ajouter la source (lien ou « selon X, date »), ou la donnée dans site-context.md, "
                   "ou remplacer par une formulation sans chiffre, ou {{à compléter : source}}.",
}


def afficher(r):
    c = r["compte"]
    out = [f"AFFIRMATIONS · {len(r['affirmations'])} relevées · {c['ok']} sourcées ou fournies · "
           f"{c['à vérifier']} à vérifier · {c['bloquant']} bloquantes · {c['trou']} trous"
           + (" · mode YMYL" if r["ymyl"] else "")]
    for g, titre in (("bloquant", "BLOQUANTES (YMYL : pas de publication sans source)"),
                     ("à vérifier", "À VÉRIFIER"), ("trou", "TROUS ASSUMÉS (à fournir par l'utilisateur)")):
        lot = [x for x in r["affirmations"] if x["gravite"] == g]
        if not lot:
            continue
        out += ["", titre]
        for x in lot:
            phrase = x["phrase"] if len(x["phrase"]) <= 140 else x["phrase"][:137] + "…"
            out.append(f"  l.{x['ligne']:<4} [{', '.join(x['types'])} · {x['statut']}] {phrase}")
            if x["statut"] in CONSEILS:
                out.append(f"         → {CONSEILS[x['statut']]}")
    ok = [x for x in r["affirmations"] if x["gravite"] == "ok"]
    if ok:
        out += ["", "SOURCÉES OU FOURNIES"]
        out += [f"  l.{x['ligne']:<4} [{x['statut']}] {x['phrase'][:110]}" for x in ok]
    out += ["", f"VERDICT : {r['verdict']}"]
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Affirmations vérifiables d'un texte et leurs sources.")
    p.add_argument("fichier", nargs="?", help="article .md ou .txt (sinon --texte ou entrée standard)")
    p.add_argument("--texte")
    p.add_argument("--ymyl", action="store_true", help="santé, argent, assurance, droit : sans source = bloquant")
    p.add_argument("--contexte", help="site-context.md (ses chiffres comptent comme fournis)")
    p.add_argument("--reserve", help="reserve.md (ses chiffres comptent comme fournis)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    try:
        if a.texte:
            texte = a.texte
        elif a.fichier:
            texte = Path(a.fichier).read_text(encoding="utf-8")
        elif not sys.stdin.isatty():
            texte = sys.stdin.read()
        else:
            p.print_help(sys.stderr)
            return 1
        faits = ""
        for f in (a.contexte, a.reserve):
            if f:
                faits += Path(f).read_text(encoding="utf-8") + "\n"
    except OSError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    r = analyser(texte, a.ymyl, faits)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
