#!/usr/bin/env python3
"""fidelite.py : vérifie qu'une réécriture n'a ajouté ni perdu aucun fait.

Un humaniseur change la forme, jamais les faits. Après chaque réécriture, ce
script compare l'avant et l'après sur ce qui se vérifie :

  chiffres      nombres, pourcentages, montants, durées (« 1 400 » = « 1400 »)
  dates         années, mois, trimestres
  noms          mots à majuscule hors début de phrase, sigles
  citations     texte entre « » ou " "
  liens         URL, adresses, @mentions, #hashtags
  à compléter   champs {{…}} (un champ perdu = un trou comblé, à vérifier)

  AJOUTÉ  : un fait absent de l'original est apparu → BLOQUANT (invention
            possible). Sauf s'il vient de l'utilisateur ou de reserve.md : à
            confirmer explicitement.
  PERDU   : un fait de l'original a disparu → ATTENTION. Une perte est une
            erreur, sauf si une règle l'exige (doublon, chiffre interdit).

Codes de sortie : 0 FIDÈLE · 2 PERTES · 3 AJOUTS · 1 erreur.

D'après la vérification de fidélité de blader/humanizer v3.1 (MIT),
automatisée et adaptée au français. Sans dépendance.

Exemples :
  python3 fidelite.py avant.txt apres.txt
  python3 fidelite.py avant.txt apres.txt --json
"""

import argparse
import json
import re
import sys
import unicodedata

MOIS = ("janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|"
        "decembre")
RE_NOMBRE = re.compile(r"(?<![\w])[-+−]?\d+(?:[   .]\d{3})*(?:[.,]\d+)?\s?(?:%|‰|k€|m€|M€|€|\$|k\b|K\b|M\b|x\b|×)?")
RE_DATE = re.compile(rf"\b(?:(?:19|20)\d\d|(?:{MOIS})(?:\s(?:19|20)\d\d)?|T[1-4](?:\s(?:19|20)\d\d)?|[1-4](?:er|e|ème) trimestre)\b", re.I)
RE_CITATION = re.compile(r"«\s*([^»]{3,200}?)\s*»|\"([^\"]{3,200}?)\"|“([^”]{3,200}?)”")
RE_LIEN = re.compile(r"https?://\S+|www\.\S+|[\w.+-]+@[\w-]+\.[\w.]+|(?<![\w])[@#][\wÀ-ÿ-]+")
RE_CHAMP = re.compile(r"\{\{[^}]+\}\}")
RE_NOM = re.compile(r"\b(?:[A-ZÀÂÉÈÊÎÔÛÇ][\wÀ-ÿ'’-]+|[A-Z]{2,}[\w-]*)\b")
MOTS_OUTILS = {"le", "la", "les", "un", "une", "des", "de", "du", "et", "ou", "mais", "donc", "car", "je", "tu",
               "il", "elle", "on", "nous", "vous", "ils", "elles", "ce", "cette", "ces", "mon", "ma", "mes",
               "ton", "ta", "tes", "notre", "nos", "votre", "vos", "leur", "leurs", "en", "au", "aux", "à",
               "pour", "par", "sur", "dans", "avec", "sans", "si", "quand", "comme", "qui", "que", "quoi",
               "c'est", "j'ai", "il", "voici", "alors", "puis", "ensuite", "aujourd'hui", "hier", "demain"}


def norme_nombre(s: str) -> str:
    s = s.replace("−", "-").replace(" ", " ").replace(" ", " ").strip()
    s = re.sub(r"(?<=\d)[ .](?=\d{3}\b)", "", s)
    s = s.replace(" ", "").replace(",", ".").lower()
    return s


def sans_accents(t: str) -> str:
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c))


def noms(texte: str) -> set:
    out = set()
    for m in RE_NOM.finditer(texte):
        avant = texte[:m.start()]
        ouvre = re.search(r"(?:^|[.!?…:\n«\"]\s*|^\s*[-•·*]\s*)$", avant) is not None
        if not re.search(r"\w", avant.rsplit("\n", 1)[-1]):
            ouvre = True  # premier mot de la ligne après une puce, un émoji ou du gras
        mot = m.group(0)
        if mot.lower() in MOTS_OUTILS:
            continue
        if ouvre and not mot.isupper():
            continue
        out.add(mot)
    return out


def extraire(texte: str) -> dict:
    liens = {m.group(0).rstrip(".,;:!?)") for m in RE_LIEN.finditer(texte)}
    # le contenu d'un champ {{…}} n'est pas un fait : on ne l'extrait pas
    sans_liens = RE_CHAMP.sub(" ", RE_LIEN.sub(" ", texte))
    return {
        "chiffres": {norme_nombre(m.group(0)) for m in RE_NOMBRE.finditer(sans_liens)
                     if not RE_DATE.fullmatch(m.group(0).strip())},
        "dates": {sans_accents(m.group(0).lower()) for m in RE_DATE.finditer(sans_liens)},
        "noms": noms(sans_liens),
        "citations": {next(g for g in m.groups() if g).strip() for m in RE_CITATION.finditer(texte)},
        "liens": liens,
        "a_completer": set(RE_CHAMP.findall(texte)),
    }


def comparer(avant: str, apres: str) -> dict:
    a, b = extraire(avant), extraire(apres)
    ajouts, pertes = {}, {}
    for cle in a:
        plus = sorted(b[cle] - a[cle])
        moins = sorted(a[cle] - b[cle])
        if cle == "noms":
            # un nom passé en début de phrase n'est plus repérable : on vérifie sa présence brute
            moins = [n for n in moins if not re.search(rf"(?<!\w){re.escape(n)}(?!\w)", apres)]
            plus = [n for n in plus if not re.search(rf"(?<!\w){re.escape(n)}(?!\w)", avant)]
        if cle == "chiffres":
            plus = [x for x in plus if x not in {norme_nombre(y) for y in b["dates"]}]
        if plus:
            ajouts[cle] = plus
        if moins:
            pertes[cle] = moins
    # Un champ {{…}} qui disparaît a été « rempli » : c'est un ajout de fait à confirmer.
    if "a_completer" in pertes:
        ajouts.setdefault("champs_remplis", pertes.pop("a_completer"))
    # un champ {{…}} nouveau est un trou honnête, pas un fait inventé : signalé, jamais bloquant
    trous = ajouts.pop("a_completer", [])
    if ajouts:
        verdict, code = "AJOUTS", 3
    elif pertes:
        verdict, code = "PERTES", 2
    elif trous:
        verdict, code = "FIDÈLE, AVEC TROUS", 2
    else:
        verdict, code = "FIDÈLE", 0
    return {"verdict": verdict, "code": code, "ajouts": ajouts, "pertes": pertes, "trous": trous}


NOMS = {"chiffres": "chiffres", "dates": "dates", "noms": "noms", "citations": "citations",
        "liens": "liens et mentions", "a_completer": "champs à compléter", "champs_remplis": "champs {{…}} remplis"}


def afficher(r: dict) -> str:
    L = [f"FIDÉLITÉ : {r['verdict']}"]
    if r["ajouts"]:
        L.append("\n✖ Ajouté (absent de l'original, à justifier ou retirer) :")
        for k, v in r["ajouts"].items():
            L.append(f"  {NOMS[k]} : " + ", ".join(v))
    if r["pertes"]:
        L.append("\n! Perdu (présent dans l'original) :")
        for k, v in r["pertes"].items():
            L.append(f"  {NOMS[k]} : " + ", ".join(v))
    if r.get("trous"):
        L.append("\n! Champs à compléter ajoutés (à remplir par l'utilisateur, aucun fait inventé) :")
        L.append("  " + ", ".join(r["trous"]))
    if not r["ajouts"] and not r["pertes"]:
        L.append("Aucun chiffre, date, nom, citation ou lien ajouté ou perdu.")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser(description="Compare deux versions : faits ajoutés (3) ou perdus (2).")
    p.add_argument("avant")
    p.add_argument("apres")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    try:
        avant = open(a.avant, encoding="utf-8").read()
        apres = open(a.apres, encoding="utf-8").read()
    except OSError as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    r = comparer(avant, apres)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
