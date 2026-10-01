#!/usr/bin/env python3
"""
job_url.py - construit ou réécrit une URL de recherche d'offres LinkedIn.

Deux usages :

  1. CONSTRUIRE une recherche booléenne à partir de mots-clés :
       python3 job_url.py construire \\
         --titres "growth marketing manager" "head of growth" "responsable acquisition" \\
         --mots-cles saas b2b --exclure stagiaire internship alternance \\
         --lieu "Paris" --teletravail hybride distanciel --experience confirme

  2. RÉÉCRIRE une URL copiée depuis LinkedIn pour n'afficher que les offres
     publiées dans la dernière heure (f_TPR=r3600), triées par date :
       python3 job_url.py reecrire "https://www.linkedin.com/jobs/search/?keywords=growth&f_TPR=r86400"
       python3 job_url.py reecrire "<url>" --depuis 7200     # 2 heures

  Vérifier une requête booléenne sans construire d'URL :
       python3 job_url.py verifier '("growth" OR "acquisition") NOT stagiaire'

Paramètres LinkedIn utilisés (constatés dans les URL de recherche, non
documentés officiellement : LinkedIn peut les changer sans prévenir) :
  keywords  requête, opérateurs AND OR NOT, "guillemets", (parenthèses)
  location  lieu en texte libre ; geoId si tu le copies d'une vraie recherche
  f_TPR     ancienneté max en secondes : r86400 = 24 h (menu LinkedIn),
            r604800 = 7 jours ; r3600 = 1 h (valeur hors menu, acceptée)
  sortBy    DD = plus récentes d'abord, R = pertinence
  f_WT      1 sur site, 2 à distance, 3 hybride
  f_E       1 stage, 2 premier emploi, 3 junior/confirmé, 4 confirmé/senior,
            5 directeur, 6 cadre dirigeant
  f_JT      F temps plein, P temps partiel, C contrat, T intérim, I stage,
            V bénévolat
  f_AL      true = candidature simplifiée
  distance  rayon en miles (5, 10, 25, 50, 100)
"""

import argparse
import json
import re
import sys
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit

BASE = "https://www.linkedin.com/jobs/search/"
TRACKING = {"currentJobId", "refId", "trackingId", "position", "pageNum", "lipi", "eBP", "originalSubdomain",
            "midToken", "midSig", "trk", "trkEmail", "otpToken"}
TELETRAVAIL = {"sur-site": "1", "distanciel": "2", "hybride": "3"}
EXPERIENCE = {"stage": "1", "debutant": "2", "junior": "3", "confirme": "4", "directeur": "5", "dirigeant": "6"}
CONTRAT = {"temps-plein": "F", "temps-partiel": "P", "contrat": "C", "interim": "T", "stage": "I", "benevolat": "V"}
DEFAULT_SINCE = 3600


def quote_term(term):
    term = term.strip().strip('"«»“”').strip()
    return f'"{term}"' if " " in term or "-" in term else term


def group(terms, op="OR"):
    terms = [quote_term(t) for t in terms if t.strip()]
    if not terms:
        return ""
    return terms[0] if len(terms) == 1 else "(" + f" {op} ".join(terms) + ")"


def build_query(titres=(), mots_cles=(), exclure=(), brut=None):
    if brut:
        return brut.strip()
    parts = [p for p in (group(titres), group(mots_cles)) if p]
    query = " AND ".join(parts)
    for e in exclure:
        query += f" NOT {quote_term(e)}"
    return query.strip()


def check_query(q):
    """Renvoie la liste des problèmes d'une requête booléenne LinkedIn."""
    problems = []
    if q.count('"') % 2:
        problems.append("Guillemets non fermés : la recherche exacte ne marchera pas.")
    depth = 0
    for ch in q:
        depth += ch == "("
        depth -= ch == ")"
        if depth < 0:
            break
    if depth != 0:
        problems.append("Parenthèses déséquilibrées.")
    outside = re.sub(r'"[^"]*"', "", q)
    for low in re.findall(r"\b(and|or|not|et|ou|sauf)\b", outside):
        problems.append(f"« {low} » en minuscules est lu comme un mot, pas comme un opérateur : écris-le en MAJUSCULES (AND, OR, NOT).")
    if re.search(r"(?:^|\s)[+-]\w", outside):
        problems.append("Les opérateurs + et - ne sont pas pris en charge : utilise AND et NOT.")
    if re.search(r'[“”«»]', q):
        problems.append("Guillemets typographiques : utilise des guillemets droits \" \".")
    if len(q) > 1000:
        problems.append("Requête très longue : LinkedIn peut la tronquer. Fais deux recherches.")
    return problems


def build_url(query, lieu=None, geo_id=None, teletravail=(), experience=(), contrat=(), simplifiee=False,
              depuis=DEFAULT_SINCE, distance=None, tri="DD"):
    params = [("keywords", query)]
    if lieu:
        params.append(("location", lieu))
    if geo_id:
        params.append(("geoId", str(geo_id)))
    if distance:
        params.append(("distance", str(distance)))
    if depuis:
        params.append(("f_TPR", f"r{int(depuis)}"))
    if teletravail:
        params.append(("f_WT", ",".join(TELETRAVAIL[t] for t in teletravail)))
    if experience:
        params.append(("f_E", ",".join(EXPERIENCE[e] for e in experience)))
    if contrat:
        params.append(("f_JT", ",".join(CONTRAT[c] for c in contrat)))
    if simplifiee:
        params.append(("f_AL", "true"))
    if tri:
        params.append(("sortBy", tri))
    return BASE + "?" + urlencode(params, safe=",", quote_via=quote)


def rewrite_url(url, depuis=DEFAULT_SINCE, tri="DD"):
    """Garde les filtres de l'URL, impose l'ancienneté et le tri, retire le pistage."""
    parts = urlsplit(url.strip())
    if "linkedin.com" not in parts.netloc:
        raise ValueError("Ce n'est pas une URL LinkedIn.")
    kept, notes = [], []
    for k, v in parse_qsl(parts.query, keep_blank_values=False):
        if k in TRACKING:
            notes.append(f"retiré : {k}")
            continue
        if k in ("f_TPR", "sortBy"):
            notes.append(f"remplacé : {k}={v}")
            continue
        kept.append((k, v))
    if depuis:
        kept.append(("f_TPR", f"r{int(depuis)}"))
    if tri:
        kept.append(("sortBy", tri))
    path = parts.path
    if not path.startswith("/jobs/search"):
        notes.append(f"chemin {path} remplacé par /jobs/search/ (les collections ne gèrent pas ces filtres)")
        path = "/jobs/search/"
    if not any(k == "keywords" for k, _ in kept):
        notes.append("aucun mot-clé dans l'URL : la recherche portera sur toutes les offres du lieu")
    new = urlunsplit(("https", "www.linkedin.com", path, urlencode(kept, safe=",", quote_via=quote), ""))
    return new, notes


def main():
    ap = argparse.ArgumentParser(description="Construit ou réécrit une URL de recherche d'offres LinkedIn.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("construire", help="construit une recherche booléenne et son URL")
    b.add_argument("--titres", nargs="*", default=[], help="intitulés de poste, reliés par OR")
    b.add_argument("--mots-cles", nargs="*", default=[], help="mots-clés reliés par OR, ajoutés avec AND")
    b.add_argument("--exclure", nargs="*", default=[], help="mots exclus avec NOT")
    b.add_argument("--requete", help="requête booléenne brute (remplace titres/mots-clés/exclure)")
    b.add_argument("--lieu")
    b.add_argument("--geo-id")
    b.add_argument("--distance", type=int, choices=[5, 10, 25, 50, 100])
    b.add_argument("--teletravail", nargs="*", default=[], choices=list(TELETRAVAIL))
    b.add_argument("--experience", nargs="*", default=[], choices=list(EXPERIENCE))
    b.add_argument("--contrat", nargs="*", default=[], choices=list(CONTRAT))
    b.add_argument("--candidature-simplifiee", action="store_true")
    b.add_argument("--depuis", type=int, default=DEFAULT_SINCE, help="ancienneté max en secondes (défaut 3600 = 1 h)")
    b.add_argument("--tri", choices=["DD", "R"], default="DD")
    b.add_argument("--json", action="store_true")

    r = sub.add_parser("reecrire", help="réécrit une URL LinkedIn existante (dernière heure, plus récentes)")
    r.add_argument("url")
    r.add_argument("--depuis", type=int, default=DEFAULT_SINCE)
    r.add_argument("--tri", choices=["DD", "R"], default="DD")
    r.add_argument("--json", action="store_true")

    v = sub.add_parser("verifier", help="vérifie une requête booléenne")
    v.add_argument("requete")

    args = ap.parse_args()

    if args.cmd == "verifier":
        problems = check_query(args.requete)
        print("\n".join(problems) if problems else "Requête valide.")
        sys.exit(1 if problems else 0)

    if args.cmd == "construire":
        q = build_query(args.titres, args.mots_cles, args.exclure, args.requete)
        if not q:
            ap.error("donne au moins --titres, --mots-cles ou --requete")
        url = build_url(q, args.lieu, args.geo_id, args.teletravail, args.experience, args.contrat,
                        args.candidature_simplifiee, args.depuis, args.distance, args.tri)
        problems = check_query(q)
        if args.json:
            json.dump({"requete": q, "url": url, "problemes": problems}, sys.stdout, ensure_ascii=False, indent=2)
            print()
            return
        print(f"REQUÊTE  {q}\nURL      {url}")
        for p in problems:
            print(f"ATTENTION {p}")
        return

    url, notes = rewrite_url(args.url, args.depuis, args.tri)
    if args.json:
        json.dump({"url": url, "notes": notes}, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    print(url)
    for n in notes:
        print(f"  - {n}")


if __name__ == "__main__":
    main()
