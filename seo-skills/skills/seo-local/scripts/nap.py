#!/usr/bin/env python3
"""nap.py : nom, adresse et téléphone sont-ils les mêmes partout ?

Compare le NAP (nom, adresse, téléphone) d'un établissement entre plusieurs
sources : la page du site (texte visible et JSON-LD LocalBusiness), la fiche
Google Business Profile, les annuaires. Normalise à la française avant de
comparer, pour ne pas confondre une abréviation et un conflit :

- téléphone : +33 6 12 34 56 78, 06.12.34.56.78 et 0612345678 sont le même ;
- adresse : « bd » = « boulevard », « av. » = « avenue », « r. » = « rue »,
  accents, virgules et casse ignorés ; code postal à 5 chiffres comparé à part ;
- nom : forme juridique (SAS, SARL, EURL…) ignorée.

Verdict par champ : IDENTIQUE, ÉCRITURE DIFFÉRENTE (même valeur une fois
normalisée : pas un conflit), CONFLIT (valeurs réellement différentes),
ABSENT (une source ne donne pas le champ).

    python3 nap.py --source site=page-agence.html --source fiche=fiche-google.txt --source pagesjaunes=pj.txt
    python3 nap.py --source site=https://www.site.fr/agence-lyon/ --source fiche=fiche.txt --json

Une source texte : « Nom : … », « Adresse : … », « Téléphone : … », une par
ligne (copie de la fiche ou de l'annuaire). Une source HTML : JSON-LD
(LocalBusiness et ses sous-types, ou Organization avec adresse) d'abord,
sinon les numéros de téléphone visibles.

Ne jamais publier une adresse personnelle, ni dans la page ni dans le JSON-LD
(entreprise à domicile, zone de chalandise) : c'est au Skill de le vérifier.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.request

UA = "Mozilla/5.0 (compatible; JoinMedicis-nap/1.0; +https://joinmedicis.com)"

ABREVIATIONS = {
    "bd": "boulevard", "bld": "boulevard", "boul": "boulevard", "av": "avenue", "ave": "avenue",
    "r": "rue", "pl": "place", "chem": "chemin", "ch": "chemin", "imp": "impasse", "all": "allee",
    "rte": "route", "fg": "faubourg", "fbg": "faubourg", "qu": "quai", "crs": "cours", "sq": "square",
    "st": "saint", "ste": "sainte", "bis": "bis", "ter": "ter", "res": "residence", "bat": "batiment",
    "zi": "zone industrielle", "za": "zone artisanale", "zac": "zone d amenagement concerte",
}
FORMES = {"sas", "sasu", "sarl", "eurl", "sa", "sci", "snc", "scop", "selarl", "sel", "ei", "eirl", "micro"}


def plier(s: str) -> str:
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def mots(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", plier(s))


def norm_tel(t: str) -> str:
    d = re.sub(r"\D", "", re.sub(r"\(0\)", "", t or ""))  # +33 (0)4… : le (0) ne se compose pas
    if d.startswith("0033"):
        d = d[4:]
    elif d.startswith("33") and len(d) == 11:
        d = d[2:]
    if len(d) == 9:
        d = "0" + d
    return d


def norm_nom(n: str) -> str:
    return " ".join(m for m in mots(n) if m not in FORMES)


def norm_adresse(a: str) -> tuple[str, str]:
    """(voie et ville normalisées sans code postal, code postal)."""
    cp = re.search(r"\b(\d{5})\b", a or "")
    sans_cp = re.sub(r"\b\d{5}\b", " ", a or "")
    sortie = []
    for m in mots(sans_cp):
        sortie.extend(ABREVIATIONS.get(m, m).split())
    if sortie and sortie[-1] in ("france", "fr"):
        sortie = sortie[:-1]
    return " ".join(sortie), (cp.group(1) if cp else "")


# ---------------------------------------------------------------- lecture

TYPES_LOCAUX = re.compile(r"(LocalBusiness|Store|Restaurant|Office|Agency|Dentist|Physician|Attorney|Notary|"
                          r"InsuranceAgency|RealEstateAgent|AutoRepair|HomeAndConstructionBusiness|"
                          r"ProfessionalService|MedicalBusiness|FinancialService|Organization)$")


def _objets(d):
    if isinstance(d, list):
        for x in d:
            yield from _objets(x)
    elif isinstance(d, dict):
        yield d
        for v in d.values():
            if isinstance(v, (list, dict)):
                yield from _objets(v)


def lire_html(html: str) -> dict:
    res = {"nom": "", "adresse": "", "telephone": "", "origine": "html"}
    for bloc in re.findall(r'(?is)<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html):
        try:
            data = json.loads(bloc)
        except json.JSONDecodeError:
            continue
        for o in _objets(data):
            types = o.get("@type", [])
            types = types if isinstance(types, list) else [types]
            if not any(TYPES_LOCAUX.search(str(t)) for t in types):
                continue
            adr = o.get("address")
            if isinstance(adr, dict):
                adr = " ".join(str(adr.get(k, "")) for k in ("streetAddress", "postalCode", "addressLocality"))
            if adr or o.get("telephone"):
                res.update(nom=str(o.get("name", "")), adresse=str(adr or ""), telephone=str(o.get("telephone", "")),
                           origine="JSON-LD")
                return res
    texte = re.sub(r"(?s)<[^>]+>", " ", re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html))
    tels = re.findall(r"(?:\+33\s?|0)[1-9](?:[\s.-]?\d{2}){4}", texte)
    if tels:
        res["telephone"] = tels[0]
        res["origine"] = "texte visible (pas de JSON-LD local)"
    titre = re.search(r"(?is)<title>(.*?)</title>", html)
    if titre:
        res["nom_titre"] = re.sub(r"\s+", " ", titre.group(1)).strip()
    return res


def lire_texte(t: str) -> dict:
    res = {"nom": "", "adresse": "", "telephone": "", "origine": "texte"}
    for ligne in t.splitlines():
        if ":" not in ligne:
            continue
        cle, val = (x.strip() for x in ligne.split(":", 1))
        c = plier(cle)
        if c.startswith(("nom", "name", "raison")):
            res["nom"] = val
        elif c.startswith(("adresse", "address")):
            res["adresse"] = val
        elif c.startswith(("tel", "phone")):
            res["telephone"] = val
    return res


def lire_source(spec: str) -> tuple[str, dict]:
    if "=" not in spec:
        raise ValueError(f"source sans nom : « {spec} » (forme attendue : nom=fichier_ou_url)")
    nom, chemin = spec.split("=", 1)
    if re.match(r"https?://", chemin):
        req = urllib.request.Request(chemin, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            contenu = r.read().decode("utf-8", errors="replace")
    else:
        with open(chemin, encoding="utf-8") as f:
            contenu = f.read()
    est_html = bool(re.search(r"(?i)<html|<body|<script", contenu))
    return nom.strip(), (lire_html(contenu) if est_html else lire_texte(contenu))


# ---------------------------------------------------------------- comparaison

def comparer(sources: dict[str, dict]) -> dict:
    champs = {}
    for champ, norm in (("nom", norm_nom), ("telephone", norm_tel), ("adresse", None)):
        valeurs = {n: s.get(champ, "") for n, s in sources.items()}
        presentes = {n: v for n, v in valeurs.items() if v}
        absentes = [n for n, v in valeurs.items() if not v]
        if champ == "adresse":
            normes = {n: norm_adresse(v) for n, v in presentes.items()}
            voies = {v[0] for v in normes.values()}
            cps = {v[1] for v in normes.values() if v[1]}
            if len(voies) <= 1 and len(cps) <= 1:
                verdict = "IDENTIQUE" if len(set(presentes.values())) <= 1 else "ÉCRITURE DIFFÉRENTE"
            else:
                verdict = "CONFLIT"
            detail = {"codes_postaux": sorted(cps)} if len(cps) > 1 else {}
        else:
            normes = {n: norm(v) for n, v in presentes.items()}
            if len(set(normes.values())) <= 1:
                verdict = "IDENTIQUE" if len(set(presentes.values())) <= 1 else "ÉCRITURE DIFFÉRENTE"
            else:
                verdict = "CONFLIT"
            detail = {}
            if champ == "telephone":
                courts = [n for n, v in normes.items() if len(v) != 10]
                if courts:
                    detail["numeros_incomplets"] = courts
        if not presentes:
            verdict = "ABSENT"
        champs[champ] = {"verdict": verdict, "valeurs": valeurs, "absent_de": absentes, **detail}
    conflits = [c for c, v in champs.items() if v["verdict"] == "CONFLIT"]
    return {"sources": {n: s.get("origine") for n, s in sources.items()}, "champs": champs,
            "verdict": "CONFLIT" if conflits else ("INCOMPLET" if any(v["absent_de"] for v in champs.values()) else "COHÉRENT")}


def afficher(r: dict) -> str:
    noms_champs = {"nom": "Nom", "adresse": "Adresse", "telephone": "Téléphone"}
    out = ["NAP · " + " · ".join(f"{n} ({o})" for n, o in r["sources"].items())]
    for champ, v in r["champs"].items():
        out.append(f"  {noms_champs[champ]:<10} {v['verdict']}")
        for n, val in v["valeurs"].items():
            out.append(f"    {n:<14} {val or '(absent)'}")
        if v.get("codes_postaux"):
            out.append(f"    codes postaux différents : {', '.join(v['codes_postaux'])}")
        if v.get("numeros_incomplets"):
            out.append(f"    numéro incomplet dans : {', '.join(v['numeros_incomplets'])}")
    suite = {"CONFLIT": "Une seule version de référence (celle des documents officiels de l'entreprise), puis corriger chaque source en conflit, la fiche Google d'abord.",
             "INCOMPLET": "Compléter les champs absents ; une écriture différente n'est pas une erreur.",
             "COHÉRENT": "Rien à corriger sur le NAP."}[r["verdict"]]
    out.append(f"VERDICT · {r['verdict']} · {suite}")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Compare nom, adresse et téléphone entre plusieurs sources.")
    ap.add_argument("--source", action="append", required=True, help="nom=fichier ou nom=URL (répéter, 2 au moins)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if len(a.source) < 2:
        print("Erreur : il faut au moins deux sources à comparer", file=sys.stderr)
        return 1
    try:
        sources = dict(lire_source(s) for s in a.source)
    except (OSError, ValueError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    r = comparer(sources)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return {"COHÉRENT": 0, "INCOMPLET": 2, "CONFLIT": 3}[r["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
