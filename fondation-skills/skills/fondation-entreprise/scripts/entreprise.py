#!/usr/bin/env python3
"""Contrôles d'identité d'une entreprise française (Python 3, sans dépendance).

Trois commandes :

  siren NUMERO
      SIREN (9 chiffres) ou SIRET (14) : format et clé de Luhn (règle propre
      aux établissements de La Poste), numéro de TVA calculé, lien vers
      l'Annuaire des entreprises pour vérifier qu'il est attribué.

  tva NUMERO
      Numéro de TVA français (FR + clé + SIREN) : format et clé. Seul le
      service européen VIES dit si le numéro est actif.

  mentions SOURCE
      Lit une page de mentions légales (fichier HTML ou texte, URL, ou « - »
      pour l'entrée standard) et en extrait ce qui y est écrit : raison
      sociale, forme, capital, SIREN, SIRET, RCS, TVA, siège, ORIAS,
      directeur de la publication, hébergeur. Chaque valeur sort avec
      l'extrait d'où elle vient. Les numéros sont contrôlés et recoupés
      (SIRET et TVA contre SIREN).

Un numéro bien formé n'est pas un numéro attribué : le script contrôle la
forme, l'Annuaire des entreprises et VIES contrôlent l'existence.

Codes de sortie : 0 rien à revoir · 2 à revoir (clé fausse, incohérence,
mention introuvable) · 3 bloqué (page inaccessible ou vide) · 1 erreur
d'usage.

Exemples :
  python3 entreprise.py siren "123 456 782"        (numéro fictif)
  python3 entreprise.py tva FR11123456782
  python3 entreprise.py mentions mentions-legales.html --json
  python3 entreprise.py mentions https://www.exemple.fr/mentions-legales
"""
import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

LA_POSTE = "356000000"
SIEGE_LA_POSTE = "35600000000048"
ANNUAIRE = "https://annuaire-entreprises.data.gouv.fr/entreprise/{}"
VIES = "https://ec.europa.eu/taxation_customs/vies/"
ORDRE = ["raison_sociale", "forme", "capital", "siren", "siret", "rcs", "tva", "siege", "orias",
         "directeur_publication", "hebergeur"]
LIBELLES = {"raison_sociale": "raison sociale", "siege": "siège", "rcs": "RCS", "siren": "SIREN",
            "siret": "SIRET", "tva": "TVA", "orias": "ORIAS", "hebergeur": "hébergeur",
            "directeur_publication": "directeur de la publication"}
FORMES = ["SASU", "SAS", "SARL", "EURL", "SA", "SNC", "SCI", "SCOP", "SCA", "SELARL", "SELAS",
          "EIRL", "EI", "micro-entreprise", "auto-entrepreneur", "association", "GIE"]


def chiffres(s):
    return re.sub(r"[\s.\-  ]", "", s or "")


def luhn(n):
    total = 0
    for i, c in enumerate(reversed(n)):
        d = int(c)
        if i % 2:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
    return total % 10 == 0


def cle_tva(siren):
    """Clé de TVA française : (12 + 3 × (SIREN mod 97)) mod 97, sur 2 chiffres."""
    return f"{(12 + 3 * (int(siren) % 97)) % 97:02d}"


def grouper(n):
    if len(n) == 9:
        return f"{n[:3]} {n[3:6]} {n[6:]}"
    if len(n) == 14:
        return f"{n[:3]} {n[3:6]} {n[6:9]} {n[9:]}"
    return n


def controler_siren(numero):
    """Dictionnaire de résultat pour un SIREN ou un SIRET."""
    n = chiffres(numero)
    r = {"saisi": numero, "numero": n, "type": None, "forme_ok": False, "cle_ok": False, "notes": []}
    if not n.isdigit() or len(n) not in (9, 14):
        r["notes"].append("ni 9 chiffres (SIREN) ni 14 chiffres (SIRET)")
        return r
    r["type"] = "SIREN" if len(n) == 9 else "SIRET"
    r["forme_ok"] = True
    r["affiche"] = grouper(n)
    siren = n[:9]
    if r["type"] == "SIRET" and siren == LA_POSTE and n != SIEGE_LA_POSTE:
        r["cle_ok"] = sum(map(int, n)) % 5 == 0
        r["notes"].append("établissement de La Poste : la somme des chiffres doit être un multiple de 5 (pas de clé de Luhn)")
    else:
        r["cle_ok"] = luhn(n)
    if r["type"] == "SIRET":
        r["siren"] = siren
        if not luhn(siren):
            r["cle_ok"] = False
            r["notes"].append("le SIREN contenu dans ce SIRET a une clé fausse")
    if not r["cle_ok"]:
        r["notes"].append("clé de contrôle fausse : faute de frappe probable, relis le numéro à la source")
    else:
        r["tva_calculee"] = f"FR{cle_tva(siren)}{siren}"
        r["annuaire"] = ANNUAIRE.format(siren)
        r["notes"].append("forme correcte ; l'existence se vérifie sur l'Annuaire des entreprises")
    return r


def controler_tva(numero):
    n = chiffres(numero).upper()
    r = {"saisi": numero, "numero": n, "forme_ok": False, "cle_ok": False, "notes": []}
    m = re.fullmatch(r"FR([0-9A-Z]{2})(\d{9})", n)
    if not m:
        r["notes"].append("format attendu : FR + 2 caractères + 9 chiffres (ex. FR 12 345678901)")
        return r
    r["forme_ok"] = True
    cle, siren = m.groups()
    r["siren"] = siren
    if not cle.isdigit():
        r["notes"].append("clé alphanumérique (ancien format ou entité sans SIREN) : contrôle par VIES uniquement")
        r["cle_ok"] = None
    elif siren.startswith("000"):
        r["notes"].append("numéro sans SIREN (ex. Monaco) : contrôle par VIES uniquement")
        r["cle_ok"] = cle == cle_tva(siren)
    else:
        r["cle_ok"] = cle == cle_tva(siren) and luhn(siren)
        if cle != cle_tva(siren):
            r["notes"].append(f"clé fausse : pour ce SIREN, la clé est {cle_tva(siren)}")
        if not luhn(siren):
            r["notes"].append("le SIREN contenu a une clé de Luhn fausse")
    r["notes"].append(f"forme contrôlée ; activité du numéro : VIES ({VIES})")
    return r


# --- mentions légales ------------------------------------------------------------

def lire_source(source, delai=20):
    """Texte brut de la source. Lève RuntimeError si inaccessible."""
    if source == "-":
        brut = sys.stdin.read()
    elif re.match(r"https?://", source):
        req = urllib.request.Request(source, headers={
            "User-Agent": "Mozilla/5.0 (compatible; fondation-entreprise/1.0; lecture des mentions legales)",
            "Accept-Language": "fr-FR,fr;q=0.9"})
        try:
            with urllib.request.urlopen(req, timeout=delai) as rep:
                brut = rep.read(3_000_000).decode(rep.headers.get_content_charset() or "utf-8", "replace")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"la page répond {e.code}")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise RuntimeError(f"page inaccessible ({getattr(e, 'reason', e)})")
    else:
        p = Path(source).expanduser()
        if not p.exists():
            raise RuntimeError("fichier introuvable")
        brut = p.read_text(encoding="utf-8", errors="replace")
    return texte_de(brut)


def texte_de(brut):
    """HTML → texte, une ligne par bloc. Un texte simple passe tel quel."""
    if "<" not in brut:
        return brut
    t = re.sub(r"(?is)<(script|style|noscript|svg|template)\b.*?</\1>", " ", brut)
    t = re.sub(r"(?is)<!--.*?-->", " ", t)
    t = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr|section|article|footer|header|address)>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t).replace(" ", " ").replace(" ", " ")
    lignes = [re.sub(r"[ \t]+", " ", l).strip() for l in t.splitlines()]
    return "\n".join(l for l in lignes if l)


NUM9 = r"(\d{3}[ . ]?\d{3}[ . ]?\d{3})"
NUM14 = r"(\d{3}[ . ]?\d{3}[ . ]?\d{3}[ . ]?\d{5})"
MOTIFS = {
    "siret": rf"\bSIRET\b\s*(?:n°|no|numéro|num\.?)?\s*:?\s*{NUM14}",
    "siren": rf"\bSIREN\b\s*(?:n°|no|numéro|num\.?)?\s*:?\s*{NUM9}(?!\s?\d)",
    "rcs": r"(?i:\bR\.?C\.?S\.?)[ \t]+(?i:de[ \t]+|d')?([A-ZÉÈÎ][a-zéèêëîïôûüç'\-]+(?:[ \-][A-ZÉÈÎ][a-zéèêëîïôûüç'\-]+)*)",
    "tva": r"\b(FR\s?[0-9A-Z]{2}\s?\d{3}\s?\d{3}\s?\d{3})\b",
    "capital": r"capital\s+(?:social\s+)?(?:variable\s+)?(?:de\s+|:\s*)?((?:\d[\d  .]*)(?:,\d+)?\s*(?:€|euros?|EUR))",
    "orias": r"(?i:\bORIAS\b)[^\d\n]{0,60}(\d{2}[ .]?\d{3}[ .]?\d{3})",
    "siege": r"(?i:si[èe]ge(?:[ \t]+social)?)[ \t]*(?i:est[ \t]+situé[ \t]+)?(?i:au|à)?[ \t]*:?[ \t]*([^\n]{8,140})",
    "directeur_publication": r"(?i:direct(?:eur|rice)[ \t]+(?:de[ \t]+la[ \t]+)?publication)[ \t]*(?i:est)?[ \t]*:?[ \t]*([^\n]{3,90})",
    "hebergeur": r"(?i:h[ée]berg(?:eur|é[ \t]+par|ement))[ \t]*(?i:du[ \t]+site)?[ \t]*:?[ \t]*([^\n]{3,120})",
}


def extrait(texte, m, large=40):
    """Le passage autour de la valeur lue, coupé aux espaces (« … » si le texte continue)."""
    a, b = max(0, m.start() - large), min(len(texte), m.end() + large)
    if a > 0:
        espace = texte.find(" ", a, m.start())
        a = espace + 1 if espace != -1 else m.start()
    if b < len(texte):
        espace = texte.rfind(" ", m.end(), b)
        b = espace if espace != -1 else m.end()
    morceau = re.sub(r"\s+", " ", texte[a:b]).strip()
    return ("… " if a > 0 else "") + morceau + (" …" if b < len(texte) else "")


def trouver_forme(texte):
    for f in FORMES:
        m = re.search(rf"(?<![\w-]){re.escape(f)}(?![\w-])", texte, 0 if f.isupper() else re.I)
        if m:
            return f, m
    return None, None


def analyser_mentions(texte):
    trouve, alertes = {}, []
    for cle, motif in MOTIFS.items():
        m = re.search(motif, texte, re.I if cle in ("siret", "siren", "capital") else 0)
        if m:
            valeur = m.group(1).strip(" .;,")
            trouve[cle] = {"valeur": valeur, "extrait": extrait(texte, m)}
    if "rcs" in trouve and re.fullmatch(NUM9, trouve["rcs"]["valeur"]):
        del trouve["rcs"]
    # SIREN implicite : le numéro qui suit « RCS Ville »
    if "siren" not in trouve:
        m = re.search(rf"\bR\.?C\.?S\.?\s+(?:de\s+)?[A-ZÉÈ][\w'\-]+(?:[ \-][A-ZÉÈ][\w'\-]+)*\s*(?:[A-B]\s*)?(?:n°\s*)?{NUM9}", texte, re.I)
        if m:
            trouve["siren"] = {"valeur": m.group(1), "extrait": extrait(texte, m), "deduit": "lu après le RCS"}
    forme, m = trouver_forme(texte)
    if forme:
        trouve["forme"] = {"valeur": forme, "extrait": extrait(texte, m)}
        ra = re.search(rf"((?:[A-ZÉÈ0-9][\w&'.\-]*[ \t]+){{0,3}}[A-ZÉÈ0-9][\w&'.\-]*)[ \t]*,?[ \t]*\(?{re.escape(forme)}\b", texte)
        if ra:
            trouve["raison_sociale"] = {"valeur": f"{ra.group(1).strip()} {forme}", "extrait": extrait(texte, ra)}

    controles = {}
    siren = chiffres(trouve["siren"]["valeur"]) if "siren" in trouve else None
    if siren:
        controles["siren"] = controler_siren(siren)
        if not controles["siren"]["cle_ok"]:
            alertes.append("SIREN lu avec une clé fausse : relis la page ou demande le Kbis")
    if "siret" in trouve:
        s = chiffres(trouve["siret"]["valeur"])
        controles["siret"] = controler_siren(s)
        if not controles["siret"]["cle_ok"]:
            alertes.append("SIRET lu avec une clé fausse")
        if siren and s[:9] != siren:
            alertes.append(f"le SIRET ({grouper(s)}) ne commence pas par le SIREN ({grouper(siren)})")
        siren = siren or s[:9]
    if "tva" in trouve:
        controles["tva"] = controler_tva(trouve["tva"]["valeur"])
        if controles["tva"]["cle_ok"] is False:
            alertes.append("numéro de TVA lu avec une clé fausse")
        if siren and controles["tva"].get("siren") and controles["tva"]["siren"] != siren:
            alertes.append("le numéro de TVA ne contient pas le SIREN de la page")
    if not siren:
        alertes.append("aucun SIREN ni SIRET lu : demande-le ou cherche l'entreprise sur l'Annuaire des entreprises")
    manquants = [c for c in ("raison_sociale", "forme", "siege", "directeur_publication", "hebergeur") if c not in trouve]
    return {"trouve": trouve, "controles": controles, "alertes": alertes, "manquants": manquants,
            "annuaire": ANNUAIRE.format(siren) if siren and luhn(siren) else None}


# --- sortie ----------------------------------------------------------------------

def afficher_controle(r, titre):
    etat = "illisible" if not r["forme_ok"] else ("clé correcte" if r["cle_ok"] else
                                                   ("à contrôler sur VIES" if r["cle_ok"] is None else "clé fausse"))
    print(f"{titre} {r.get('affiche', r['numero'])} : {etat}")
    if r.get("tva_calculee"):
        print(f"  TVA calculée : {r['tva_calculee']}")
    if r.get("annuaire"):
        print(f"  Annuaire : {r['annuaire']}")
    for n in r["notes"]:
        print(f"  - {n}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nom, aide in (("siren", "contrôler un SIREN ou un SIRET"), ("tva", "contrôler un numéro de TVA français")):
        s = sub.add_parser(nom, help=aide)
        s.add_argument("numero")
        s.add_argument("--json", action="store_true")
    m = sub.add_parser("mentions", help="extraire les mentions légales d'une page")
    m.add_argument("source", help="fichier HTML ou texte, URL, ou - pour l'entrée standard")
    m.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd in ("siren", "tva"):
        r = controler_siren(a.numero) if a.cmd == "siren" else controler_tva(a.numero)
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            afficher_controle(r, r.get("type") or "TVA")
        return 0 if r["forme_ok"] and r["cle_ok"] is not False else 2

    try:
        texte = lire_source(a.source)
    except RuntimeError as e:
        msg = f"{a.source} : {e}. Colle le texte de la page, ou passe par l'Annuaire des entreprises."
        print(json.dumps({"erreur": msg}, ensure_ascii=False) if a.json else msg)
        return 3
    if len(texte.strip()) < 40:
        msg = f"{a.source} : page vide ou rendue en JavaScript. Colle le texte de la page."
        print(json.dumps({"erreur": msg}, ensure_ascii=False) if a.json else msg)
        return 3
    r = analyser_mentions(texte)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("Lu sur la page :")
        for cle in ORDRE:
            v = r["trouve"].get(cle)
            if not v:
                continue
            suffixe = f" ({v['deduit']})" if v.get("deduit") else ""
            print(f"  {LIBELLES.get(cle, cle):<28} {v['valeur']}{suffixe}")
            print(f"  {'':<28} « {v['extrait']} »")
        if r["controles"]:
            print("Contrôles :")
            for cle, c in r["controles"].items():
                etat = "clé correcte" if c["cle_ok"] else ("à contrôler sur VIES" if c["cle_ok"] is None else "clé fausse")
                print(f"  {cle.upper():<6} {c.get('affiche', c['numero'])} : {etat}")
            if r["annuaire"]:
                print(f"  Annuaire des entreprises : {r['annuaire']}")
            if "tva" in r["controles"]:
                print(f"  Activité du numéro de TVA : VIES ({VIES})")
        if r["manquants"]:
            print("Absent de la page : " + ", ".join(LIBELLES.get(x, x) for x in r["manquants"]))
        for al in r["alertes"]:
            print(f"! {al}")
    return 2 if r["alertes"] or r["manquants"] else 0


if __name__ == "__main__":
    sys.exit(main())
