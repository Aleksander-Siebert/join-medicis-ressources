#!/usr/bin/env python3
"""texte.py : découpage et mesures d'un texte français (module partagé).

Utilisé par voix.py (mesurer des textes), ecart.py (comparer un texte à une
voix) et profil.py (lire le bloc de mesures d'un tone-of-voice.md).
Python 3.8+, bibliothèque standard seulement. Rien n'est envoyé nulle part.

Toutes les mesures sont des heuristiques : elles décrivent des habitudes
d'écriture, elles ne prouvent rien sur l'auteur.
"""

import re
import statistics
import unicodedata

VERSION_MESURES = 1

MOT = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿœŒæÆ0-9]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿœŒæÆ]+)*")
NOMBRE = re.compile(r"\d+(?:[   .,]\d+)*")
URL = re.compile(r"https?://\S+|www\.\S+")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
TELEPHONE = re.compile(r"(?<!\d)(?:\+33\s?|0)[1-9](?:[ .-]?\d{2}){4}(?!\d)")
HASHTAG = re.compile(r"(?<!\w)#[\wÀ-ÿ]+")
MENTION = re.compile(r"(?<![\w.])@[\wÀ-ÿ.-]+")
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\U00002B50\U00002B55"
    "\U0000231A-\U0000231B\U000023E9-\U000023FA\U00002190-\U000021FF\U00002934\U00002935]"
)

# Mots vides français : exclus des mots fréquents et des expressions.
MOTS_VIDES = set("""
a à au aux avec ce ces cet cette c ça cela celui celle ceux comme dans de des du d elle elles en
et est été être eu il ils je j l la le les leur leurs lui m ma mais me mes moi mon même n ne
ni nos notre nous on ou où par pas plus pour qu que qui s sa se ses si son sur t ta te tes
toi ton tu un une vos votre vous y sont ai as avons avez ont était étaient fait faire
très tout tous toute toutes aussi alors donc car bien encore déjà là ici quand comment
entre sans sous chez vers après avant puis cette dont aux leurs mes tes ses quel quelle
c'est j'ai qu'il qu'on n'est l'on s'il d'un d'une l'a depuis peu moins trop fait faut
""".split())

# Marques d'oral et de registre familier relevées telles quelles.
MARQUES_ORAL = [
    "du coup", "en fait", "bref", "genre", "franchement", "carrément", "perso", "clairement",
    "honnêtement", "bon,", "bah", "ben", "voilà", "quoi.", "en vrai", "tranquille", "trop bien",
    "concrètement", "en gros", "à fond", "top",
]

# Formules de registre soutenu ou administratif.
SOUTENU = re.compile(
    r"(?i)\bnous vous prions\b|\bveuillez\b|\bnous vous saurions gré\b|\bconformément\b|\brelatif à\b|"
    r"\bdans les meilleurs délais\b|\bsalutations distinguées\b|\bnous accusons réception\b|\bje me permets\b|"
    r"\bci-joint\b|\bpar la présente\b|\bil apparaît que\b|\ben vue de\b|\bafin de\b")

# Anglicismes courants en marketing (relevés, jamais jugés).
ANGLICISMES = [
    "lead", "leads", "growth", "churn", "pipeline", "deal", "deals", "call", "calls", "process",
    "feedback", "feedbacks", "insight", "insights", "best practice", "best practices", "business",
    "marketing", "brief", "briefs", "meeting", "workshop", "deadline", "kpi", "kpis", "roi",
    "b2b", "b2c", "saas", "onboarding", "boost", "booster", "challenge", "challenger", "mindset",
    "storytelling", "content", "newsletter", "funnel", "scale", "scaler", "startup", "start-up",
    "freelance", "side project", "side business", "community", "network", "networking", "hack",
    "growth hacking", "inbound", "outbound", "cold email", "follow-up", "feature", "features",
    "use case", "rebranding", "teasing", "live", "replay", "webinar", "hook", "post", "posts",
]

# Marques d'écriture IA (version courte du lexique du pack LinkedIn, même auteur).
MARQUES_IA = [
    # (identifiant, motif, force)
    ("fuite-assistant", r"(?im)^(?:bien sûr|avec plaisir|absolument|certainement)\s?! voici\b|"
     r"^voici (?:une|un|la|le) (?:version|proposition|exemple|brouillon|post)\b|"
     r"\bn'hésite[sz]? pas à me (?:dire|demander) si\b|\bj'espère que (?:cela|ça) (?:vous|t')aide\b|"
     r"\b(?:en tant qu'|comme )(?:IA|intelligence artificielle|assistant|modèle de langage)\b", "fort"),
    ("gabarit-non-rempli", r"\[(?:Votre|Ton|Ta|Vos|Insérer|Nom|Prénom|Entreprise|Date|Chiffre|Lien)[^\]\n]{0,40}\]", "fort"),
    ("ce-n-est-pas-c-est", r"(?i)\b(?:ce n['’]est pas|c['’]est pas|il ne s['’]agit pas)\b[^.!?\n]{1,80}[,.;:]\s*(?:c['’]est|il s['’]agit)\b", "fort"),
    ("non-seulement-mais", r"(?i)\bnon seulement\b[^.!?\n]{1,80}\bmais\b", "fort"),
    ("revelation", r"(?im)(?:^|(?<=[.!?] ))(?:le |la |les )?(?:résultat|secret|leçon|vérité|twist|verdict|moralité)\s*[?:]\s", "fort"),
    ("annonce-sincerite", r"(?i)\bpour être (?:honnête|transparent|franc)\b|\bsoyons honnêtes\b|\bje vais être (?:honnête|franc|franche|transparent|transparente|vulnérable)\b|\bparlons vrai\b", "fort"),
    ("ouverture-creuse", r"(?i)^\s*(?:dans un monde où|à l['’]ère d[eu]|dans le paysage (?:actuel|numérique)|de nos jours,|aujourd['’]hui plus que jamais)", "fort"),
    ("delayage", r"(?i)\bil (?:est|convient d['’]être) (?:important|essentiel|crucial) de (?:noter|souligner|comprendre)\b|\bforce est de constater\b|\bil convient de noter\b", "faible"),
    ("lexique-ia", r"(?i)\b(?:crucia(?:l|le|les|ux)|incontournables?|captivant(?:e|es|s)?|fascinant(?:e|es|s)?|révolutionnaires?|disruptif|disruptive|plonger au cœur|véritable levier|levier puissant|en constante évolution|tirer parti)\b", "faible"),
    ("connecteur-scolaire", r"(?m)^(?:Par ailleurs|De plus|En outre|De surcroît|En conclusion|En somme|Pour conclure),", "faible"),
    ("staccato", r"(?m)^\s*(?:[A-Za-zÀ-ÿ'’-]+\. ){2,}[A-Za-zÀ-ÿ'’-]+\.\s*$", "faible"),
]
MARQUES_IA = [(i, re.compile(m), f) for i, m, f in MARQUES_IA]

TU = re.compile(r"(?i)\b(?:tu|te|toi|ton|ta|tes|tien|tienne)\b|\bt['’](?=[aeiouyhéèêàâîôû])")
VOUS = re.compile(r"(?i)\b(?:vous|votre|vos|vôtre)\b")
JE = re.compile(r"(?i)\b(?:je|me|moi|mon|ma|mes)\b|\b[jm]['’]")
ON = re.compile(r"(?i)\bon\b")
NOUS = re.compile(r"(?i)\b(?:nous|notre|nos)\b")
CA = re.compile(r"(?i)\bça\b")
CELA = re.compile(r"(?i)\bcela\b")
NEGATION = re.compile(r"(?i)\b(?:pas|jamais|plus rien|personne)\b")
NE = re.compile(r"(?i)\bne\b|\bn['’]")
PAS_FIGES = re.compile(r"(?i)\bpas (?:mal|à pas|de souci|de problème|du tout)\b|\bpas\s*\?")

# Ponctuation suivie. Le taux est compté par phrase.
PONCTUATION = {
    "question": re.compile(r"\?"),
    "exclamation": re.compile(r"!"),
    "points_suspension": re.compile(r"…|\.\.\."),
    "parentheses": re.compile(r"\("),
    "deux_points": re.compile(r"(?<!\d):(?!\d|//)"),
    "point_virgule": re.compile(r";"),
    "cadratin": re.compile(r"—"),
    "guillemets_droits": re.compile(r"\""),
    "guillemets_francais": re.compile(r"«"),
}
SEUIL_RARE = 0.15  # marques par phrase ; repris de notque/voice-stylometry (MIT)


def normaliser(texte):
    """Unifie les retours à la ligne et retire les caractères invisibles."""
    texte = unicodedata.normalize("NFC", texte or "")
    texte = texte.replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"[​‌‍⁠﻿]", "", texte)


def sans_liens(texte):
    return URL.sub(" ", EMAIL.sub(" ", texte))


def mots(texte):
    return MOT.findall(sans_liens(texte))


def paragraphes(texte):
    return [p.strip() for p in re.split(r"\n\s*\n", normaliser(texte)) if p.strip() and MOT.search(p)]


def phrases(texte):
    """Phrases : coupe après . ! ? … et à chaque retour à la ligne (listes, posts)."""
    morceaux = re.split(r"(?<=[.!?…])[\"»”)]?\s+|\n+", sans_liens(normaliser(texte)))
    return [p.strip() for p in morceaux if p.strip() and MOT.search(p)]


def arrondi(x, n=1):
    return None if x is None else round(x, n)


def classe(taux):
    """jamais / rare / habituelle, selon le nombre de marques par phrase."""
    if taux is None:
        return None
    if taux == 0:
        return "jamais"
    return "rare" if taux < SEUIL_RARE else "habituelle"


def marques_ia(texte):
    sortie = []
    for ident, motif, force in MARQUES_IA:
        for m in motif.finditer(texte):
            sortie.append({"id": ident, "force": force, "extrait": m.group(0).strip()[:60]})
    return sortie


def negations_sans_ne(texte):
    n = 0
    for p in phrases(texte):
        if NEGATION.search(p) and not NE.search(p) and not PAS_FIGES.search(p):
            n += 1
    return n


def type_de_fin(derniere):
    d = derniere.strip()
    if d.endswith("?"):
        return "question"
    if d.endswith("!"):
        return "exclamation"
    if NOMBRE.search(d):
        return "chiffre"
    if re.match(r"(?i)^(?:écris|écrivez|dis|dites|contacte|contactez|réserve|réservez|inscris|inscrivez|"
                r"télécharge|téléchargez|découvre|découvrez|lis|lisez|clique|cliquez|rejoins|rejoignez|"
                r"viens|venez|essaie|essayez|teste|testez|partage|partagez|commente|commentez)\b", d):
        return "appel"
    return "affirmation"


def mesurer(texte):
    """Mesures d'un seul texte. Une mesure sans objet vaut None (jamais 0 inventé)."""
    texte = normaliser(texte)
    ms = mots(texte)
    ps = phrases(texte)
    pars = paragraphes(texte)
    longueurs = [len(MOT.findall(p)) for p in ps]
    n_mots, n_ph = len(ms), len(ps)
    sortie = {
        "mots": n_mots,
        "phrases": n_ph,
        "paragraphes": len(pars),
        "phrase_mediane": arrondi(statistics.median(longueurs)) if longueurs else None,
        "phrase_moyenne": arrondi(statistics.mean(longueurs)) if longueurs else None,
        "phrase_ecart_type": arrondi(statistics.stdev(longueurs)) if len(longueurs) >= 4 else None,
        "part_phrases_courtes": arrondi(100 * sum(l <= 8 for l in longueurs) / n_ph, 0) if n_ph else None,
        "part_phrases_longues": arrondi(100 * sum(l >= 25 for l in longueurs) / n_ph, 0) if n_ph else None,
        "phrases_par_paragraphe": arrondi(n_ph / len(pars)) if pars else None,
        "part_paragraphes_une_phrase": (
            arrondi(100 * sum(len(phrases(p)) == 1 for p in pars) / len(pars), 0) if len(pars) >= 3 else None),
        "tu": len(TU.findall(texte)),
        "vous": len(VOUS.findall(texte)),
        "je": len(JE.findall(texte)),
        "on": len(ON.findall(texte)),
        "nous": len(NOUS.findall(texte)),
        "ca": len(CA.findall(texte)),
        "cela": len(CELA.findall(texte)),
        "negations_sans_ne": negations_sans_ne(texte),
        "soutenu": len(SOUTENU.findall(texte)),
        "chiffres": len(NOMBRE.findall(sans_liens(texte))),
        "emojis": len(EMOJI.findall(texte)),
        "hashtags": len(HASHTAG.findall(texte)),
        "mentions": len(MENTION.findall(EMAIL.sub(" ", texte))),
        "liens": len(URL.findall(texte)),
        "ponctuation": {k: len(r.findall(sans_liens(texte))) for k, r in PONCTUATION.items()},
        "espace_avant_double": len(re.findall(r"[   ][;:!?](?!//)", sans_liens(texte))),
        "sans_espace_avant_double": len(re.findall(r"[A-Za-zÀ-ÿ0-9»)][;:!?](?!//|\d)", sans_liens(texte))),
        "pourcent_espace": len(re.findall(r"\d[   ]%", texte)),
        "pourcent_colle": len(re.findall(r"\d%", texte)),
        "marques_oral": {m: n for m in MARQUES_ORAL
                         if (n := len(re.findall(r"(?i)(?<![\wÀ-ÿ])" + re.escape(m) + r"(?![\wÀ-ÿ])", texte)))},
        "anglicismes": {a: n for a in ANGLICISMES
                        if (n := len(re.findall(r"(?i)(?<![\wÀ-ÿ-])" + re.escape(a) + r"(?![\wÀ-ÿ-])", texte)))},
        "ouverture": " ".join(MOT.findall(ps[0])[:6]) if ps else "",
        "fin": type_de_fin(ps[-1]) if ps else None,
        "derniere_phrase": ps[-1][:120] if ps else "",
        "marques_ia": marques_ia(texte),
    }
    return sortie


def adresse(tu, vous):
    if tu == 0 and vous == 0:
        return "aucune"
    if tu >= 2 * max(vous, 1) or (vous == 0 and tu > 0):
        return "tutoiement"
    if vous >= 2 * max(tu, 1) or (tu == 0 and vous > 0):
        return "vouvoiement"
    return "mixte"


def pour_mille(n, total):
    return arrondi(1000 * n / total) if total else None


# ---------------------------------------------------------------------------
# Bloc de mesures dans tone-of-voice.md
# ---------------------------------------------------------------------------

BLOC = re.compile(r"```mesures\s*\n(.*?)```", re.S)


def lire_bloc(markdown):
    """Lit le bloc ```mesures``` d'un tone-of-voice.md. Renvoie un dict ou None."""
    m = BLOC.search(markdown or "")
    if not m:
        return None
    out = {}
    for ligne in m.group(1).splitlines():
        ligne = ligne.split("#", 1)[0].strip()
        if not ligne or ":" not in ligne:
            continue
        cle, val = (x.strip() for x in ligne.split(":", 1))
        if val == "":
            out[cle] = None
            continue
        try:
            out[cle] = float(val) if "." in val else int(val)
        except ValueError:
            out[cle] = val
    return out


def ecrire_bloc(valeurs):
    lignes = ["```mesures"]
    for cle, val in valeurs.items():
        lignes.append(f"{cle}: {'' if val is None else val}")
    lignes.append("```")
    return "\n".join(lignes)


def plier(s):
    """Minuscules sans accents, pour comparer des libellés."""
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()
