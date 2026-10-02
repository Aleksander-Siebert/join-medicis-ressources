#!/usr/bin/env python3
"""
humanize.py - nettoie un brouillon en français de ses marques d'écriture IA.

Quatre passes, dans cet ordre :

  1. INVISIBLES   supprime les caractères qu'un clavier ne produit pas :
                  espaces sans chasse, joints, traits d'union conditionnels,
                  BOM, caractères d'étiquette Unicode, marques de direction.
                  Les espaces insécables (fines ou non) deviennent des espaces
                  normales, SANS supprimer l'espace : en français, l'espace
                  avant ; : ! ? reste.
  2. TYPOGRAPHIE  tiret cadratin supprimé (début ou fin de phrase) ou remplacé
                  par une virgule, jamais par un point-virgule ;
                  « 15 % » -> « 15% » ; demi-cadratin en incise -> virgule ;
                  guillemets anglais “ ” -> « » ; apostrophes harmonisées ;
                  espace ajoutée avant ; : ! ? quand elle manque ;
                  majuscules accentuées (Etat -> État, A propos -> À propos) ;
                  gras Markdown (**...**) retiré, LinkedIn ne l'affiche pas.
  3. LEXIQUE      remplace les formules sûres de tics-ia.json (« afin de »
                  -> « pour », « il est important de noter que » supprimé...),
                  en gardant la majuscule et sans toucher aux URL.
  4. SIGNALEMENTS tout ce qui demande du jugement (parallélismes, triades,
                  « Le résultat ? », verbes vides, connecteurs en pluie...)
                  est SIGNALÉ avec la ligne et une piste, jamais réécrit
                  par une regex.

Usage
  python3 humanize.py brouillon.txt                 # texte nettoyé sur la sortie
  python3 humanize.py brouillon.txt --rapport       # + le détail des changements
  python3 humanize.py brouillon.txt -o propre.txt --rapport
  python3 humanize.py brouillon.txt --insecables    # garde des insécables avant ; : ! ?
  python3 humanize.py brouillon.txt --json
  pbpaste | python3 humanize.py - --rapport

Adapté de humanize.py de Jake Schincariol (MIT), réécrit pour le français.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "tics-ia.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
NBSP = " "
# Espaces « exotiques » ramenées à une espace normale.
SPACES = {" ", " ", " ", " ", " ", " ", " ",
          " ", " ", " ", " ", " ", "　"}
ZWJ = "‍"


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def protect_urls(text):
    """Remplace les URL par des jetons pour qu'aucune passe ne les modifie."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    return re.sub(r"\x00(\d+)\x00", lambda m: found[int(m.group(1))], text)


def _is_pictograph(ch):
    return bool(ch) and (ord(ch) >= 0x1F000 or 0x2600 <= ord(ch) <= 0x27BF)


# ------------------------------------------------------------------ passe 1
def pass_invisible(text, keep_nbsp=False):
    log = Counter()
    out = []
    for i, ch in enumerate(text):
        if ch in SPACES:
            if keep_nbsp and ch in (" ", " "):
                out.append(NBSP)
                if ch == " ":
                    log["U+202F espace fine insécable -> insécable"] += 1
            else:
                out.append(" ")
                log[f"U+{ord(ch):04X} espace spéciale -> espace"] += 1
            continue
        # Sélecteurs de variante : légitimes après un émoji, un chiffre (1️⃣) ou un symbole (©️).
        # Isolés, ou dans le bloc supplémentaire U+E0100-E01EF, ils servent à cacher du texte.
        if 0xFE00 <= ord(ch) <= 0xFE0F or 0xE0100 <= ord(ch) <= 0xE01EF:
            prev = text[i - 1] if i else ""
            if ord(ch) <= 0xFE0F and prev and (_is_pictograph(prev) or prev in "0123456789#*"
                                               or unicodedata.category(prev) == "So" or prev in "©®™"):
                out.append(ch)
            else:
                log["sélecteur de variante isolé supprimé (texte caché possible)"] += 1
            continue
        if 0xE0000 <= ord(ch) <= 0xE007F:
            log["caractère de balise Unicode supprimé (texte caché possible)"] += 1
            continue
        if unicodedata.category(ch) == "Cf":
            # Le ZWJ entre deux pictogrammes construit un émoji (👨‍💻) : on le garde.
            if ch == ZWJ and i > 0 and i + 1 < len(text):
                prev = text[i - 1] if text[i - 1] != "️" else text[i - 2] if i > 1 else ""
                if _is_pictograph(prev) and _is_pictograph(text[i + 1]):
                    out.append(ch)
                    continue
            name = unicodedata.name(ch, "FORMAT")
            log[f"U+{ord(ch):04X} {name.lower()} supprimé"] += 1
            continue
        out.append(ch)
    return "".join(out), log


# ------------------------------------------------------------------ passe 2
def pass_typography(text, lex, keep_nbsp=False):
    log = Counter()
    space = NBSP if keep_nbsp else " "

    def sub(pattern, repl, label, flags=0):
        nonlocal text
        text, n = re.subn(pattern, repl, text, flags=flags)
        if n:
            log[label] += n

    # Tiret cadratin (—) : supprimé, ou remplacé par une virgule. Jamais par un
    # point-virgule, un point ou un trait d'union.
    sub(r"(?m)^([ \t]*)—[ \t]*", r"\1", "tiret cadratin en début de ligne supprimé")
    sub(r"[ \t]*—[ \t]*(?=[.!?…:;,)»\n]|$)", "", "tiret cadratin en fin de phrase supprimé", flags=re.M)
    sub(r"[ \t]*—[ \t]*", ", ", "tiret cadratin -> virgule")
    # Tiret demi-cadratin (–) : plage de nombres -> trait d'union ; incise -> virgule.
    sub(r"(?<=\d)\s?–\s?(?=\d)", "-", "tiret entre nombres -> trait d'union")
    sub(r"(?m)^([ \t]*)–[ \t]*", r"\1", "tiret demi-cadratin en début de ligne supprimé")
    sub(r"\s+–\s+", ", ", "tiret demi-cadratin -> virgule")
    # Ponctuation doublée laissée par les remplacements de tirets.
    sub(r",\s*([,.;:!?)])", r"\1", "ponctuation doublée nettoyée")
    sub(r"\(\s*,\s*", "(", "ponctuation doublée nettoyée")

    # Pourcentage collé au nombre : « 15 % » -> « 15% ».
    sub(r"(?<=\d)[ \u00a0\u202f]+%", "%", "pourcentage collé au nombre (15%)")

    # Guillemets anglais courbes -> guillemets français.
    sub(r"“\s*([^”\n]*?)\s*”", "«" + space + r"\1" + space + "»", "guillemets anglais -> « »")
    # Espaces à l'intérieur des « » quand elles manquent.
    sub(r"«(?=\S)", "«" + space, "espace ajoutée après «")
    sub(r"(?<=\S)»", space + "»", "espace ajoutée avant »")

    # Apostrophes : on harmonise sur la forme majoritaire du texte.
    straight, curly = text.count("'"), text.count("’")
    if straight and curly:
        if curly > straight:
            sub(r"(?<=\w)'(?=\w)", "’", "apostrophes harmonisées (courbes)")
        else:
            sub(r"(?<=\w)’(?=\w)", "'", "apostrophes harmonisées (droites)")

    # Espace avant ; ! ? (et : suivi d'une espace ou d'une fin de ligne).
    sub(r"(?<=[\w»)\"'%€$])(?<!\d)([;!?]+)", space + r"\1", "espace ajoutée avant ; ! ?")
    sub(r"(?<=\d)([!?]+)(?=\s|$)", space + r"\1", "espace ajoutée avant ; ! ?", flags=re.M)
    sub(r"(?<=[A-Za-zÀ-ÿ»)\"'%€])(:)(?=\s|$)", space + r"\1", "espace ajoutée avant :", flags=re.M)
    if keep_nbsp:
        sub(r" ([;:!?»])", NBSP + r"\1", "espace -> insécable avant ponctuation")
        sub(r"« ", "«" + NBSP, "espace -> insécable après «")

    # Majuscules non accentuées en début de phrase ou de ligne.
    for wrong, right in lex.get("accents_majuscules", {}).items():
        pattern = r"(?:(?<=^)|(?<=[.!?…]\s)|(?<=\n)|(?<=[«\"]\s)|(?<=[«\"]))" + re.escape(wrong) + (r"\b" if not wrong.endswith(" ") else "")
        sub(pattern, right, f"majuscule accentuée : {wrong.strip()} -> {right.strip()}", flags=re.M)

    # Markdown que LinkedIn n'affiche pas.
    sub(r"\*\*([^*\n]+)\*\*", r"\1", "gras Markdown retiré (non affiché par LinkedIn)")
    sub(r"(?m)^#{1,6} (?=\S)", "", "titre Markdown retiré")

    # Espaces multiples créées par les passes précédentes.
    sub(r"(?<=\S)[ ]{2,}(?=\S)", " ", "espaces doublées")
    return text, log


# ------------------------------------------------------------------ passe 3
def _match_case(found, repl):
    if not repl:
        return repl
    if found[:1].isupper():
        return repl[:1].upper() + repl[1:]
    return repl


CAP = "\x01"  # marque « remettre une majuscule ici » après une suppression


def pass_lexical(text, lex):
    log = Counter()
    entries = sorted(lex["remplacements"], key=lambda e: -len(e["trouver"]))
    for e in entries:
        find, repl = e["trouver"], e["remplacer"]
        pat = re.compile(r"(?<![\w])" + re.escape(find).replace(r"\ ", r"\s+")
                         + (r"(?!\w)" if find[-1:].isalnum() else ""), re.IGNORECASE)
        source = text

        def do(m):
            if repl == "":
                before = source[:m.start()]
                at_start = before == "" or re.search(r"(?:[.!?…]\s+|\n\s*|[«\"]\s*)$", before) is not None
                return CAP if at_start else ""
            return _match_case(m.group(0), repl)

        text, n = pat.subn(do, text)
        if n:
            log[f"« {find.strip()} » -> « {repl.strip() or '∅'} »"] += n
    # Après une suppression en début de phrase, la phrase reprend avec une majuscule.
    text = re.sub(CAP + r"(\s*)(\w)", lambda m: m.group(1) + m.group(2).upper(), text)
    return text.replace(CAP, ""), log


# ------------------------------------------------------------------ passe 4
# Le repérage de ce qui demande du jugement vit dans marqueurs.py (partagé
# avec detect.py) : densité par paragraphe, rythme, triades, sincérité...
from marqueurs import find_flags, formulations_retirees  # noqa: E402


# ------------------------------------------------------------------ pipeline
def humanize(text, lex, keep_nbsp=False, niveau="strict", retirees=None):
    text, urls = protect_urls(text)
    text, log1 = pass_invisible(text, keep_nbsp)
    text, log2 = pass_typography(text, lex, keep_nbsp)
    text, log3 = pass_lexical(text, lex)
    text = restore_urls(text, urls)
    # Les signalements portent sur le texte nettoyé : ce qui reste à réécrire.
    flags = find_flags(text, lex, niveau, retirees)
    return text, {"invisibles": log1, "typographie": log2, "lexique": log3}, flags


def render_report(logs, flags, out):
    total = sum(sum(c.values()) for c in logs.values())
    out.write("\nRAPPORT D'HUMANISATION\n----------------------\n")
    out.write(f"{total} corrections automatiques, {len(flags)} passage(s) à réécrire à la main\n")
    titles = {"invisibles": "1. CARACTÈRES INVISIBLES", "typographie": "2. TYPOGRAPHIE", "lexique": "3. LEXIQUE"}
    for key, title in titles.items():
        if logs[key]:
            out.write(f"\n{title}\n{'-' * len(title)}\n")
            for label, n in logs[key].most_common():
                out.write(f"  {n:>3}x  {label}\n")
    if flags:
        title = "4. À RÉÉCRIRE (jugement humain)"
        out.write(f"\n{title}\n{'-' * len(title)}\n")
        for f in flags:
            force = " (fort)" if f.get("force") in ("fort", "forensique") else ""
            out.write(f"  l.{f['ligne']:<3} [{f['famille']}{force}] « {f['extrait']} »\n        -> {f['conseil']}\n")


def main():
    ap = argparse.ArgumentParser(description="Nettoie un brouillon français de ses marques d'écriture IA.")
    ap.add_argument("fichier", help="fichier texte, ou - pour l'entrée standard")
    ap.add_argument("-o", "--sortie", help="écrit le texte nettoyé dans ce fichier")
    ap.add_argument("--rapport", action="store_true", help="affiche le détail des changements et des signalements")
    ap.add_argument("--insecables", action="store_true",
                    help="garde des espaces insécables avant ; : ! ? et dans « » (typographie soignée)")
    ap.add_argument("--json", action="store_true", help="sortie JSON (texte, corrections, signalements)")
    ap.add_argument("--lexique", default=LEX, help="chemin vers tics-ia.json")
    ap.add_argument("--niveau", choices=["forensique", "strict", "esthetique"], default="strict",
                    help="forensique : fuites de modèle seulement ; strict (défaut) ; esthétique : tout")
    ap.add_argument("--contexte", help="contexte.md de l'utilisateur : signale ses formulations retirées")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.fichier == "-" else open(args.fichier, encoding="utf-8").read()
    lex = load_lexicon(args.lexique)
    clean, logs, flags = humanize(raw, lex, args.insecables, args.niveau, formulations_retirees(args.contexte))

    if args.json:
        json.dump({"texte": clean, "corrections": {k: dict(v) for k, v in logs.items()}, "signalements": flags},
                  sys.stdout, ensure_ascii=False, indent=2, default=str)
        sys.stdout.write("\n")
        return
    if args.sortie:
        with open(args.sortie, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"écrit : {args.sortie}")
    else:
        sys.stdout.write(clean)
        if not clean.endswith("\n"):
            sys.stdout.write("\n")
    if args.rapport:
        render_report(logs, flags, sys.stdout)


if __name__ == "__main__":
    main()
