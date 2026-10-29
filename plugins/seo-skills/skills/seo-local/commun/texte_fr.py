#!/usr/bin/env python3
"""texte_fr.py : outils de texte français partagés par les scripts du pack SEO.

Module importé, pas lancé. Sans dépendance. Fonctions :

  fold(s)            minuscules sans accents
  racine(mot)        racinisation légère : « assurance », « assurances »,
                     « assurer », « assuré » donnent la même racine
  termes(texte)      mots utiles racinisés (sans mots vides)
  mots(texte)        nombre de mots (Markdown retiré)
  phrases(texte)     découpage en phrases (abréviations françaises tenues)
  plan(markdown)     titres H1 à H4 avec le texte de chaque section
  vecteurs(docs)     TF-IDF sur des listes de termes ; cosinus(a, b)

Chaque script du pack l'importe ainsi, qu'il soit dans un Skill seul
(skills/<nom>/scripts/ → skills/<nom>/commun/) ou dans le ZIP claude.ai
(modules/<nom>/scripts/ → commun/ à la racine) :

    ICI = Path(__file__).resolve().parent
    for c in (ICI.parent / "commun", ICI.parents[2] / "commun"):
        if (c / "texte_fr.py").exists():
            sys.path.insert(0, str(c)); break
    import texte_fr
"""

import math
import re
import unicodedata
from collections import Counter

MOTS_VIDES = set("""
a ah ai aie aient aies ait alors apres as au aucun aucune aujourd aupres aussi autre autres aux avaient avais avait
avant avec avez aviez avions avoir avons ayant bon c ca car ce ceci cela celle celles celui cependant certain
certaines certains ces cet cette ceux chaque chez ci comme comment contre d dans de des deux dire dit doit donc dont du
durant e elle elles en encore entre es est et etaient etait etant ete etre eu eux faire fait faut il ils j je jusqu l
la la le les leur leurs lors lui m ma mais me meme mes moi moins mon n ne ni non nos notre nous o on ont ou ou par parce
pas pendant peu peut plus plusieurs pour pourquoi qu quand que quel quelle quelles quels qui quoi s sa sans se selon
ses si sien soit son sont sous suis sur t ta tandis te tes toi ton tous tout toute toutes tres tu un une unes uns vers
voici voila vos votre vous vu y quoi faut cas ainsi etc afin lequel laquelle lesquels lesquelles celle-ci
the and for with your you are how what why www http https html php com
""".split())

MOT = re.compile(r"[a-zàâäçéèêëîïôöùûüÿœæ0-9]+(?:['’][a-zàâäçéèêëîïôöùûüÿœæ]+)?", re.I)

# Suffixes retirés après le pluriel, du plus long au plus court.
_SUFFIXES = ("issements", "issement", "ements", "ement", "ations", "ation", "itions", "ition", "atrices", "atrice",
             "ateurs", "ateur", "euses", "euse", "eurs", "eur", "ables", "able", "ibles", "ible", "iques", "ique",
             "ismes", "isme", "istes", "iste", "ites", "ite", "ances", "ance", "ences", "ence", "ments", "ment",
             "ions", "ion",
             "ees", "ee", "er", "ez", "es", "e")


# Équivalences génériques du vocabulaire commercial (après racinisation).
# Volontairement courtes : pas de synonymes métier, que le Skill juge à la lecture.
EQUIVALENCES = {
    "tarif": "prix", "cout": "prix", "coute": "prix",
    "deduction": "deduct", "deduir": "deduct", "deductibl": "deduct",
    "comparatif": "compar", "comparaison": "compar", "comparais": "compar",
    "gratuit": "gratuit", "offert": "gratuit",
}


def fold(s):
    """Minuscules sans accents, œ et æ dépliés."""
    s = s.lower().replace("œ", "oe").replace("æ", "ae").replace("’", "'")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def racine(mot):
    """Racinisation légère et stable du français (pas un lemmatiseur).

    Objectif : que le singulier, le pluriel, le nom et le verbe d'une même
    famille se rapprochent (« remboursement », « rembourser »,
    « remboursé »). Une racine fait au moins 4 lettres.
    """
    w = fold(mot)
    if "'" in w:
        w = w.split("'", 1)[1] or w
    if len(w) > 4 and w[-1] in "sx" and not w.endswith(("ss", "ux")):
        w = w[:-1]
    elif len(w) > 5 and w.endswith("aux"):
        w = w[:-3] + "al"
    for suf in _SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            w = w[: -len(suf)]
            break
    return EQUIVALENCES.get(w, w)


def termes(texte, garder_nombres=False):
    """Mots utiles racinisés, dans l'ordre du texte."""
    out = []
    for w in MOT.findall(texte):
        f = fold(w)
        if "'" in f:
            f = f.split("'", 1)[1]
        if f in MOTS_VIDES or len(f) < 3:
            continue
        if f.isdigit() and not garder_nombres:
            continue
        out.append(racine(f))
    return out


def sans_markdown(texte):
    """Texte brut : liens gardés en texte, marques Markdown retirées."""
    t = re.sub(r"```.*?```", " ", texte, flags=re.S)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"^\s{0,3}#{1,6}\s*", "", t, flags=re.M)
    t = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", t, flags=re.M)
    t = re.sub(r"^\s*>\s?", "", t, flags=re.M)
    t = re.sub(r"[*_`]{1,3}", "", t)
    t = re.sub(r"^\|.*\|$", lambda m: m.group(0).replace("|", " "), t, flags=re.M)
    return t


def mots(texte):
    """Nombre de mots d'un texte (Markdown retiré, « l'assurance » = 1 mot)."""
    return len(MOT.findall(sans_markdown(texte)))


_ABREV = ("M.", "MM.", "Mme.", "Dr.", "Pr.", "p.", "art.", "n°.", "etc.", "cf.", "ex.", "env.", "av.", "bd.", "St.")


def phrases(texte):
    """Découpe en phrases. Garde ensemble « M. Dupont », « art. L. 122-1 », « 2,5 % »."""
    t = sans_markdown(texte)
    t = re.sub(r"\s+", " ", t).strip()
    if not t:
        return []
    proteges = {}
    for i, a in enumerate(_ABREV):
        t = re.sub(r"(?<![A-Za-zÀ-ÿ])" + re.escape(a) + r"(?= )", a[:-1] + f"\x00{i}\x00", t)
    t = re.sub(r"\b([A-Z])\. (?=[A-Z0-9])", lambda m: m.group(1) + "\x01 ", t)  # initiales, « L. 122-1 »
    morceaux = re.split(r"(?<=[.!?…])\s+(?=[«\"A-ZÀ-Ý0-9{])", t)
    out = []
    for m in morceaux:
        for i, a in enumerate(_ABREV):
            m = m.replace(f"\x00{i}\x00", ".")
        out.append(m.replace("\x01", ".").strip())
    return [p for p in out if p]


TITRE = re.compile(r"^(#{1,4})\s+(.+?)\s*#*\s*$")


def plan(markdown):
    """Liste des sections : niveau, titre, texte propre, numéro de ligne.

    Accepte aussi un plan écrit « H2 : titre » ou « H2 Titre → description »
    (sortie de /seo-brief) : la description après « → » devient le texte.
    """
    sections = []
    courant = None
    for n, ligne in enumerate(markdown.splitlines(), 1):
        m = TITRE.match(ligne)
        if not m:
            m2 = re.match(r"^\s*(?:[-*]\s*)?H([1-4])\s*[:.\-]?\s+(.+)$", ligne)
            if m2:
                niveau, reste = int(m2.group(1)), m2.group(2)
                titre, _, desc = reste.partition("→")
                courant = {"niveau": niveau, "titre": titre.strip(), "texte": desc.strip(), "ligne": n}
                sections.append(courant)
                continue
        if m:
            courant = {"niveau": len(m.group(1)), "titre": m.group(2).strip(), "texte": "", "ligne": n}
            sections.append(courant)
        elif courant is not None:
            courant["texte"] += ligne + "\n"
        else:
            if ligne.strip():
                sections.append({"niveau": 0, "titre": "", "texte": ligne + "\n", "ligne": n})
                courant = sections[-1]
    return sections


def vecteurs(docs):
    """TF-IDF normalisé pour une liste de listes de termes."""
    df = Counter()
    tfs = []
    for d in docs:
        tf = Counter(d)
        tfs.append(tf)
        df.update(tf.keys())
    n = len(docs)
    out = []
    for tf in tfs:
        v = {t: (1 + math.log(c)) * math.log((1 + n) / (1 + df[t]) + 1) for t, c in tf.items()}
        norme = math.sqrt(sum(x * x for x in v.values())) or 1.0
        out.append({t: x / norme for t, x in v.items()})
    return out


def cosinus(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(t, 0.0) for t, x in a.items())


def recouvrement(petit, grand):
    """Part des termes de `petit` présents dans `grand` (0 à 1)."""
    p = set(petit)
    return len(p & set(grand)) / len(p) if p else 0.0
