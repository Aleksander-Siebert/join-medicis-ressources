#!/usr/bin/env python3
"""entite.py : la marque est-elle une seule entité, nommée pareil partout ?

Lit une page (URL ou HTML, la page d'accueil de préférence) et contrôle :

  noms        title, og:site_name, og:title, application-name, H1, JSON-LD
              (Organization et tous ses sous-types, LocalBusiness compris,
              @type en liste, @graph déplié), WebSite, mention « © » :
              chaque source nomme-t-elle la marque de la même façon ?
              Le title se coupe au premier séparateur du texte (| – — - · :).
  organisation un seul bloc Organization, avec @id, url, logo, sameAs
  sameAs      profils déclarés, classés (LinkedIn, Wikidata, Wikipédia…),
              doublons, liens non https ; --verifier les appelle
  visible     chaque valeur du JSON-LD qui se vérifie (téléphone, e-mail,
              adresse, prix, note, nombre d'avis) est-elle visible sur la
              page ? Une note ou un prix balisé mais invisible est contraire
              aux règles de Google.
  wikidata    --wikidata cherche la marque sur Wikidata (API publique, sans
              clé) : candidats à confirmer par l'utilisateur, jamais
              rattachés d'office.

  python3 entite.py https://www.site.fr/ --marque "Assurly"
  python3 entite.py accueil.html --marque "Assurly" --verifier --wikidata
  python3 entite.py accueil.html --marque "Assurly" --bloc     # JSON-LD à coller

Python 3 sans dépendance. Code 0 ; 1 si la page est illisible.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.parse
from pathlib import Path

ICI = Path(__file__).resolve().parent
for cand in (ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (cand / "page.py").exists():
        sys.path.insert(0, str(cand))
        break
import page as pg  # noqa: E402

ORGS = {
    "Organization", "Corporation", "LocalBusiness", "OnlineBusiness", "OnlineStore", "NGO", "NewsMediaOrganization",
    "EducationalOrganization", "GovernmentOrganization", "MedicalOrganization", "SportsOrganization", "Airline",
    "Consortium", "FundingScheme", "LibrarySystem", "PerformingGroup", "ResearchOrganization", "WorkersUnion",
    "Restaurant", "Store", "Dentist", "Physician", "LegalService", "Attorney", "Notary", "InsuranceAgency",
    "FinancialService", "AccountingService", "BankOrCreditUnion", "RealEstateAgent", "AutoDealer", "AutoRepair",
    "HealthAndBeautyBusiness", "ProfessionalService", "HomeAndConstructionBusiness", "Plumber", "Electrician",
    "Hotel", "LodgingBusiness", "FoodEstablishment", "Bakery", "CafeOrCoffeeShop", "TravelAgency", "Pharmacy",
    "MedicalBusiness", "MedicalClinic", "Optician", "SportsActivityLocation", "EntertainmentBusiness",
    "EmploymentAgency", "ChildCare", "DryCleaningOrLaundry", "Library", "RadioStation", "TelevisionStation",
}
SEPARATEURS = [" | ", " – ", " — ", " - ", " · ", " : ", " :: ", " » ", " / "]
PLATEFORMES = [
    ("wikidata", r"wikidata\.org/(?:wiki|entity)/Q\d+"), ("wikipedia", r"\.wikipedia\.org/wiki/"),
    ("linkedin", r"linkedin\.com/(?:company|school|showcase)/"), ("linkedin (profil personnel)", r"linkedin\.com/in/"),
    ("youtube", r"youtube\.com/"), ("x", r"(?:twitter|x)\.com/"), ("facebook", r"facebook\.com/"),
    ("instagram", r"instagram\.com/"), ("tiktok", r"tiktok\.com/"), ("github", r"github\.com/"),
    ("crunchbase", r"crunchbase\.com/organization/"), ("annuaire des entreprises", r"annuaire-entreprises\.data\.gouv\.fr/"),
    ("pappers", r"pappers\.fr/"), ("societe.com", r"societe\.com/"), ("google maps", r"(?:maps\.google\.|google\.[a-z.]+/maps|g\.page/|maps\.app\.goo\.gl)"),
    ("trustpilot", r"trustpilot\.com/"), ("avis vérifiés", r"avis-verifies\.com/"), ("pages jaunes", r"pagesjaunes\.fr/"),
]
UA = "Mozilla/5.0 (compatible; JoinMedicis-geo/2.0; +https://joinmedicis.com)"


def norm(t: str) -> str:
    t = unicodedata.normalize("NFD", str(t or ""))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.replace("’", "'").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", t.lower()).strip()


def cle(t: str) -> str:
    """Forme de comparaison d'un nom : sans accent, casse, ponctuation ni forme juridique."""
    n = norm(t)
    n = re.sub(r"\b(?:sas|sasu|sarl|eurl|sa|sca|snc|sci|inc|ltd|llc|gmbh|scop)\b\.?", " ", n)
    return re.sub(r"[^a-z0-9]+", "", n)


def couper(titre: str) -> list[str]:
    """Segments d'un title, coupés à chaque séparateur, dans l'ordre du texte."""
    t = " " + (titre or "").strip() + " "
    motif = "|".join(re.escape(s) for s in sorted(SEPARATEURS, key=len, reverse=True))
    return [x.strip() for x in re.split(motif, t) if x.strip()]


def types_de(o: dict) -> list[str]:
    t = o.get("@type", [])
    return [str(x).split("/")[-1] for x in (t if isinstance(t, list) else [t])]


def est_org(o: dict) -> bool:
    return any(t in ORGS or re.search(r"(?:Business|Store|Organization|Agency|Service)$", t) for t in types_de(o))


def texte_de(v) -> str:
    if isinstance(v, dict):
        return " ".join(texte_de(x) for k, x in v.items() if not k.startswith("@"))
    if isinstance(v, list):
        return " ".join(texte_de(x) for x in v)
    return str(v)


def liste(v) -> list:
    return v if isinstance(v, list) else ([] if v is None else [v])


# ---------------------------------------------------------------- noms

def sources_de_nom(page: dict) -> list[dict]:
    out = []
    m = page["metas"]
    if page["title"]:
        out.append({"source": "title", "brut": page["title"], "segments": couper(page["title"])})
    for k, lib in (("og:site_name", "og:site_name"), ("application-name", "application-name"),
                   ("og:title", "og:title"), ("twitter:title", "twitter:title")):
        if m.get(k):
            out.append({"source": lib, "brut": m[k], "segments": couper(m[k]) if "title" in k else [m[k].strip()]})
    for n, t in page["titres"]:
        if n == 1 and t:
            out.append({"source": "H1", "brut": t, "segments": couper(t)})
    for o in page["jsonld"]:
        ts = types_de(o)
        if est_org(o) or "WebSite" in ts:
            for k in ("name", "legalName", "alternateName"):
                for v in liste(o.get(k)):
                    if isinstance(v, str) and v.strip():
                        out.append({"source": f"JSON-LD {'/'.join(ts)}.{k}", "brut": v, "segments": [v.strip()]})
    for c in re.findall(r"(?:©|\(c\)|copyright)\s*(?:\d{4}\s*(?:[-–]\s*\d{4})?)?\s*([A-Z][\w&'’.\- ]{1,40}?)(?=[.,|]|\s+(?:tous|all|-|–)|$)",
                        page["texte"], re.I):
        out.append({"source": "mention ©", "brut": c.strip(), "segments": [c.strip()]})
        break
    return out


def coherence(sources: list[dict], marque: str | None) -> dict:
    if not marque:
        # la marque la plus fréquente parmi les segments courts (moins de 5 mots)
        compte = {}
        for s in sources:
            for seg in s["segments"]:
                if len(seg.split()) <= 4 and cle(seg):
                    compte.setdefault(cle(seg), [0, seg])[0] += 1
        marque = max(compte.values(), key=lambda x: x[0])[1] if compte else ""
    k = cle(marque)
    lignes, variantes = [], set()
    for s in sources:
        trouve = next((seg for seg in s["segments"] if k and k in cle(seg)), None)
        if trouve:
            # un nom déclaré (JSON-LD, og:site_name, ©) doit être la marque, forme juridique mise à part ;
            # un title ou un H1 peut la contenir dans une phrase
            nom_seul = s["source"].startswith(("JSON-LD", "og:site_name", "application-name", "mention"))
            exacte = (cle(trouve) == k) if nom_seul else re.search(rf"(?<![\w.]){re.escape(norm(marque))}(?![\w.])", norm(trouve))
            if not exacte:
                variantes.add(trouve)
            lignes.append({**s, "etat": "marque" if exacte else "variante", "lu": trouve})
        else:
            lignes.append({**s, "etat": "absente", "lu": s["brut"]})
    return {"marque": marque, "lignes": lignes, "variantes": sorted(variantes)}


# ---------------------------------------------------------------- organisation et sameAs

def organisation(page: dict) -> dict:
    orgs = [o for o in page["jsonld"] if est_org(o)]
    noms = sorted({cle(o.get("name", "")) for o in orgs if o.get("name")})
    alertes = []
    if not orgs:
        alertes.append("aucun bloc Organization (ni sous-type) : l'entité n'est pas décrite")
    elif len(noms) > 1:
        alertes.append(f"{len(orgs)} blocs Organization aux noms différents (thème et extension qui balisent chacun ?)")
    elif len(orgs) > 1 and not all(o.get("@id") for o in orgs):
        alertes.append(f"{len(orgs)} blocs Organization sans @id commun : à fusionner")
    o = orgs[0] if orgs else {}
    manque = [k for k in ("@id", "url", "logo", "sameAs") if not o.get(k)] if orgs else []
    sameas = []
    for x in orgs:
        sameas += [str(u) for u in liste(x.get("sameAs"))]
    vus, doublons = set(), []
    for u in sameas:
        c = u.rstrip("/").lower()
        if c in vus:
            doublons.append(u)
        vus.add(c)
    profils = []
    for u in dict.fromkeys(sameas):
        plat = next((n for n, m in PLATEFORMES if re.search(m, u, re.I)), "autre")
        profils.append({"url": u, "plateforme": plat, "https": u.lower().startswith("https://")})
    if any(p["plateforme"] == "linkedin (profil personnel)" for p in profils):
        alertes.append("sameAs vers un profil LinkedIn personnel : l'organisation pointe vers sa page entreprise")
    if doublons:
        alertes.append(f"sameAs en double : {', '.join(doublons)}")
    types = [t for x in page["jsonld"] for t in types_de(x)]
    if "FAQPage" in types:
        alertes.append("FAQPage : plus de résultat enrichi FAQ sur Google depuis le 7 mai 2026 ; à garder seulement si les questions sont visibles et utiles")
    if "HowTo" in types:
        alertes.append("HowTo : plus de résultat enrichi sur Google ; aucun balisage n'est propre à l'IA")
    return {"orgs": len(orgs), "types": sorted(set(types)), "manque": manque, "profils": profils,
            "alertes": alertes, "org": o}


# ---------------------------------------------------------------- JSON-LD visible

CHAMPS = {"telephone": "téléphone", "email": "e-mail", "streetAddress": "rue", "postalCode": "code postal",
          "addressLocality": "ville", "price": "prix", "lowPrice": "prix bas", "highPrice": "prix haut",
          "ratingValue": "note", "reviewCount": "nombre d'avis", "ratingCount": "nombre de notes",
          "foundingDate": "date de création", "vatID": "TVA", "taxID": "SIREN/SIRET"}


def feuilles(o, chemin=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.startswith("@"):
                continue
            yield from feuilles(v, f"{chemin}.{k}" if chemin else k)
    elif isinstance(o, list):
        for v in o:
            yield from feuilles(v, chemin)
    elif o is not None and str(o).strip():
        yield chemin, str(o).strip()


def visible(valeur: str, champ: str, texte_n: str, chiffres: str) -> bool:
    if champ in ("telephone", "vatID", "taxID"):
        d = re.sub(r"\D", "", valeur)
        d = re.sub(r"^33", "0", d)
        return len(d) >= 6 and (d in chiffres or d[-9:] in chiffres)
    if champ in ("price", "lowPrice", "highPrice", "ratingValue"):
        try:
            x = float(valeur.replace(",", "."))
        except ValueError:
            return norm(valeur) in texte_n
        formes = {f"{x:g}", f"{x:.2f}", f"{x:.1f}"}
        formes |= {f.replace(".", ",") for f in formes}
        return any(re.search(rf"(?<![\d,.]){re.escape(f)}(?![\d])", texte_n) for f in formes)
    if champ in ("reviewCount", "ratingCount"):
        d = re.sub(r"\D", "", valeur)
        return bool(d) and bool(re.search(rf"(?<!\d){d}(?!\d)", chiffres_espaces(texte_n)))
    if champ == "foundingDate":
        return valeur[:4] in texte_n
    return norm(valeur) in texte_n


def chiffres_espaces(t: str) -> str:
    return re.sub(r"(?<=\d)[  .](?=\d{3}\b)", "", t)


def jsonld_visible(page: dict) -> list[dict]:
    texte_n = norm(page["texte"])
    chiffres = re.sub(r"\D", "", page["texte"])
    out = []
    for o in page["jsonld"]:
        t = "/".join(types_de(o))
        for chemin, v in feuilles(o):
            champ = chemin.split(".")[-1]
            if champ in CHAMPS:
                out.append({"type": t, "champ": chemin, "libelle": CHAMPS[champ], "valeur": v,
                            "visible": visible(v, champ, texte_n, chiffres)})
    return out


# ---------------------------------------------------------------- réseau (options)

def verifier(profils: list[dict]) -> None:
    for p in profils:
        r = pg.lire(p["url"], ua=pg.UA_NAVIGATEUR, timeout=15)
        p["statut"] = r["statut"]
        p["erreur"] = r["erreur"]


def wikidata(marque: str) -> dict:
    url = ("https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=fr&uselang=fr&limit=5&search="
           + urllib.parse.quote(marque))
    r = pg.lire(url, ua=UA, accept="application/json")
    if r["statut"] == 429:  # limite de débit de Wikimedia : un seul nouvel essai
        import time
        time.sleep(3)
        r = pg.lire(url, ua=UA, accept="application/json")
    if r["statut"] != 200:
        return {"erreur": r["erreur"] or f"statut {r['statut']}", "candidats": []}
    try:
        d = json.loads(r["texte"])
    except ValueError:
        return {"erreur": "réponse illisible", "candidats": []}
    return {"erreur": None, "candidats": [{"id": x.get("id"), "label": x.get("label"),
                                           "description": x.get("description", "")} for x in d.get("search", [])]}


# ---------------------------------------------------------------- bloc à coller

def bloc(org: dict, marque: str, page: dict, url: str | None) -> dict:
    base = (url or "").split("#")[0]
    racine = re.match(r"https?://[^/]+", base).group(0) + "/" if re.match(r"https?://", base) else "{{https://www.site.fr/}}"
    def ou(v, defaut="{{à compléter}}"):
        return v if v else defaut
    garde = []
    for u in liste(org.get("sameAs")):
        u = str(u)
        if re.search(r"linkedin\.com/in/", u, re.I) or u.rstrip("/").lower() in [g.rstrip("/").lower() for g in garde]:
            continue  # profil personnel ou doublon : retiré du bloc
        garde.append(u)
    sameas = garde or ["{{https://www.linkedin.com/company/…}}",
                                                             "{{https://www.wikidata.org/wiki/Q… (si l'entité existe)}}"]
    out = {"@context": "https://schema.org", "@type": org.get("@type", "Organization"),
           "@id": ou(org.get("@id"), racine + "#organization"), "name": marque,
           "url": ou(org.get("url"), racine), "logo": ou(org.get("logo"), "{{URL du logo, 112 px minimum}}"),
           "sameAs": sameas}
    for k in ("legalName", "description", "telephone", "email", "address", "foundingDate", "vatID"):
        if org.get(k):
            out[k] = org[k]
    out.setdefault("legalName", "{{raison sociale exacte, ou supprimer la ligne}}")
    return out


# ---------------------------------------------------------------- sortie

def analyser(html: str, marque: str | None) -> dict:
    page = pg.analyser(html)
    noms = coherence(sources_de_nom(page), marque)
    org = organisation(page)
    for e in page["jsonld_erreurs"]:
        org["alertes"].insert(0, f"bloc JSON-LD illisible, ignoré : {e}")
    vis = jsonld_visible(page)
    return {"page": page, "noms": noms, "organisation": org, "visible": vis}


def afficher(r: dict, source: str, wd: dict | None) -> str:
    n, o = r["noms"], r["organisation"]
    L = [f"ENTITÉ · {source} · marque lue : « {n['marque']} »", "",
         "NOMS (JSON-LD, og:site_name et © doivent être la marque ; title et H1 peuvent la contenir)"]
    for x in n["lignes"]:
        etat = {"marque": "ok      ", "variante": "VARIANTE", "absente": "absente "}[x["etat"]]
        L.append(f"  {etat} {x['source']:<44} « {x['lu'][:70]} »")
    if n["variantes"]:
        L.append(f"  → variantes à aligner : {', '.join('« ' + v + ' »' for v in n['variantes'])}")
    L += ["", f"ORGANISATION · {o['orgs']} bloc(s) · types JSON-LD : {', '.join(o['types']) or 'aucun'}"]
    if o["manque"]:
        L.append(f"  manque : {', '.join(o['manque'])}")
    for a in o["alertes"]:
        L.append(f"  ! {a}")
    L += ["", f"SAMEAS · {len(o['profils'])} profil(s)"]
    for p in o["profils"]:
        st = ""
        if "statut" in p:
            st = f" · {p['statut']}" if p["statut"] else f" · NON LU ({(p['erreur'] or '')[:40]})"
        L.append(f"  {p['plateforme']:<26}{p['url']}{'' if p['https'] else ' · pas https'}{st}")
    if not any(p["plateforme"] == "wikidata" for p in o["profils"]):
        L.append("  pas de Wikidata dans sameAs")
    invis = [v for v in r["visible"] if not v["visible"]]
    L += ["", f"JSON-LD VISIBLE · {len(r['visible']) - len(invis)}/{len(r['visible'])} valeurs vérifiables retrouvées sur la page"]
    graves = ("note", "nombre d'avis", "nombre de notes", "prix", "prix bas", "prix haut")
    for v in invis:
        if v["libelle"] in graves:
            L.append(f"  CRITIQUE {v['type']}.{v['champ']} = {v['valeur']} : {v['libelle']} balisé mais absent du texte visible")
    autres = [v for v in invis if v["libelle"] not in graves]
    if autres:
        L.append(f"  info     absents de cette page : {', '.join(sorted({v['libelle'] for v in autres}))} "
                 "(normal s'ils figurent sur la page contact ou mentions légales)")
    if wd is not None:
        L += ["", "WIKIDATA (candidats, à confirmer : jamais rattachés d'office)"]
        if wd["erreur"]:
            L.append(f"  NON LU : {wd['erreur']}")
        elif not wd["candidats"]:
            L.append("  aucun élément à ce nom")
        for c in wd["candidats"]:
            L.append(f"  {c['id']:<12}{c['label']} · {c['description'][:70]}")
    L += ["", "Données structurées : utiles pour décrire l'entité et les résultats enrichis encore actifs ;",
          "Google : aucune n'est requise pour les Aperçus IA, aucune n'est propre à l'IA."]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Cohérence de l'entité de marque : noms, JSON-LD, sameAs, Wikidata.")
    ap.add_argument("source", help="URL ou fichier HTML (page d'accueil de préférence)")
    ap.add_argument("--marque", help="nom de la marque (sinon le plus fréquent)")
    ap.add_argument("--verifier", action="store_true", help="appeler chaque lien sameAs")
    ap.add_argument("--wikidata", action="store_true", help="chercher la marque sur Wikidata (API publique)")
    ap.add_argument("--bloc", action="store_true", help="écrire le bloc Organization à coller")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if re.match(r"https?://", a.source):
        lu = pg.lire(a.source)
        if lu["statut"] is None or lu["statut"] >= 400:
            print(f"Page non lue ({lu['erreur'] or lu['statut']}). Enregistre le HTML et relance sur le fichier.",
                  file=sys.stderr)
            return 1
        html, url = lu["texte"], lu["url"]
    else:
        try:
            html, url = pg.lire_fichier(a.source), None
        except OSError as e:
            print(f"Erreur : {e}", file=sys.stderr)
            return 1
    r = analyser(html, a.marque)
    if a.verifier:
        verifier(r["organisation"]["profils"])
    wd = wikidata(r["noms"]["marque"]) if a.wikidata else None
    if a.bloc:
        b = bloc(r["organisation"]["org"], r["noms"]["marque"], r["page"], url)
        print('<script type="application/ld+json">\n' + json.dumps(b, ensure_ascii=False, indent=2) + "\n</script>")
        return 0
    if a.json:
        sortie = {k: v for k, v in r.items() if k != "page"}
        sortie["organisation"] = {k: v for k, v in r["organisation"].items() if k != "org"}
        sortie["wikidata"] = wd
        print(json.dumps(sortie, ensure_ascii=False, indent=2))
    else:
        print(afficher(r, a.source, wd))
    return 0


if __name__ == "__main__":
    sys.exit(main())
