#!/usr/bin/env python3
"""lint_post.py : contrôle un post LinkedIn avant publication. Note sur 100.

Cinq familles de contrôles :

  MÉCANIQUE      3 000 caractères (officiel), liens dans le corps, hashtags,
                 longueur par rapport à la médiane personnelle (--mediane)
  ACCROCHE       phrase complète avant ~140 caractères (le « voir plus »
                 mobile, observé), question en ligne 1, ouverture usée
  INTÉGRITÉ      appâts (« commente OUI »), champs {{…}} restants,
                 superlatifs invérifiables, tiret cadratin (règle de l'utilisateur)
  DENSITÉ        1 contraste et 1 triade au plus, 0 pont de révélation,
                 0 question avant la fin, 1 appel à l'action au plus
  ACCESSIBILITÉ  pseudo-gras Unicode (bloquant), émojis, capitales, pavés

Bloquant = ne pas publier en l'état : plus de 3 000 caractères, appât,
pseudo-gras Unicode, champ {{…}} restant, tiret cadratin.

Codes de sortie :
  0  PRÊT          (75 et plus, aucun bloquant)
  2  À REVOIR      (50 à 74, ou un bloquant)
  3  À RÉÉCRIRE    (moins de 50)
  1  erreur d'utilisation

Adapté de post_linter.py (alirezarezvani/claude-skills, MIT), réécrit pour le
français et la règle de densité de Serge Bulaev (MIT). Sans dépendance.

Exemples :
  python3 lint_post.py --fichier post.txt
  python3 lint_post.py --fichier post.txt --mediane 1100 --image
  python3 lint_post.py --exemple --json
"""

import argparse
import json
import re
import sys
import unicodedata

LIMITE = 3000
PLI_MOBILE = 140
PLI_ORDI = 210

APPATS = [
    (r"\bcommente[sz]?\b.{0,20}[«\"']\s*\w{1,20}\s*[»\"']", "« commente MOT »"),
    (r"\b(?:commente[sz]?|ecris|ecrivez|tape[sz]?)\b.{0,40}\b(?:pour recevoir|pour avoir|et je (?:t'|vous )?envoie)\b", "commentaire contre ressource"),
    (r"\b(?:like|likez|aime|aimez|repost\w*|partage[sz]?)\b.{0,15}\bsi (?:tu|vous|t')", "« like si »"),
    (r"\b(?:identifie|tague|taguez|mentionne[sz]?)\b.{0,12}\b(?:quelqu'un|3|trois|un ami|une amie|une personne)\b", "« tague quelqu'un »"),
    (r"\bqui d'autre (?:est|pense|a)\b", "« qui d'autre ? »"),
    (r"\b(?:d'accord|vous etes d'accord|t'es d'accord) ?\?\s*$", "« d'accord ? » en fin"),
    (r"\b(?:qu'en pensez-vous|vous en pensez quoi|tu en penses quoi)\s*\?", "question réflexe"),
    (r"♻️|\brepost(?:ez|e)? pour\b", "demande de repartage"),
    (r"\b(?:en|par) mp\b.{0,20}\b(?:le mot|ecris)\b", "« MP-moi le mot »"),
]
OUVERTURES = [
    "je suis ravi", "je suis ravie", "je suis heureux", "je suis heureuse", "j'ai le plaisir",
    "heureux de vous annoncer", "heureuse de vous annoncer", "fier de vous annoncer", "fiere de vous annoncer",
    "petite reflexion", "petite pensee", "et si je vous disais", "et si je te disais", "dans un monde",
    "aujourd'hui je voulais", "aujourd'hui, je voulais", "je voulais partager", "je souhaitais partager",
    "a l'heure ou", "a l'ere de", "on ne va pas se mentir", "spoiler", "thread",
]
SUPERLATIFS = [
    "le meilleur", "la meilleure", "le seul", "la seule", "garanti", "garantie", "100% efficace",
    "ca marche a tous les coups", "personne n'en parle", "personne ne parle de", "tout le monde sait",
    "revolutionnaire", "sans precedent", "numero 1", "n°1", "incontournable",
]
CONTRASTES = [
    r"\b(?:ce n'est pas|c'est pas|il ne s'agit pas)\b[^.!?\n]{1,80}[,.;:]\s*(?:c'est|il s'agit)\b",
    r"\bpas [^.!?\n,]{1,40}, mais\b",
    r"\bnon pas [^.!?\n]{1,40}, mais\b",
    r"\b(?:les bons|un bon|une bonne)\b[^.\n]{1,60}\.\s*(?:les excellents|les meilleurs|un excellent|une excellente)\b",
    r"\b(?:le vrai sujet|la vraie question|le vrai probleme)\b",
    r"\b(?:arrete[sz]?|stop) [^.\n]{1,40}[.,] (?:commence[sz]?|fais|faites)\b",
]
PONTS = [
    r"(?im)^\s*(?:le |la |les |mon |ma )?(?:resultat|secret|probleme|lecon|raison|verite|solution|suite|twist|piege|chute)\s*\?",
    r"(?im)^\s*(?:rebondissement|spoiler|plot twist|attention)\s*:",
    r"(?im)^\s*voici (?:pourquoi|comment|ce que)\b[^\n]{0,40}(?:👇|⬇️|:)\s*$",
    r"\bc'est la que (?:tout|ca) (?:change|devient)\b",
    r"\bce que personne ne (?:vous|te) dit\b",
]
CTA = re.compile(
    r"\b(?:ecris-moi|ecrivez-moi|contacte-moi|contactez-moi|reserve[sz]?|prends rendez-vous|prenez rendez-vous|"
    r"abonne-toi|abonnez-vous|inscris-toi|inscrivez-vous|telecharge[sz]?|lien en (?:premier )?commentaire|"
    r"lien dans (?:le|les) commentaires?|envoie-moi|envoyez-moi|rejoins|rejoignez)\b")
URL_RE = re.compile(r"https?://[^\s)]+|\bwww\.[^\s)]+")
HASHTAG_RE = re.compile(r"(?<!\w)#[\wÀ-ÿ][\wÀ-ÿ_]{1,49}")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿⬀-⯿]")
PSEUDO_RE = re.compile("[\U0001D400-\U0001D7FF\U0001F130-\U0001F189Ａ-ｚ]")
TRIADE = re.compile(r"\b[\w'-]+(?: [\w'-]+){0,2}, [\w'-]+(?: [\w'-]+){0,2},? et [\w'-]+(?: [\w'-]+){0,2}\b")

EXEMPLE = """412 messages de prospection au premier trimestre. 9 réponses.

Le trimestre suivant, on a changé une seule chose : on ne contacte plus personne sans avoir commenté un de ses posts avant.

60 messages. 14 réponses.

Ça nous coûte 20 minutes par jour. Et ça a tué notre plus vieux réflexe, celui du volume.

Ce que je n'avais pas prévu : les commentaires eux-mêmes ont amené 3 rendez-vous, sans aucun message.

Vous commentez avant d'écrire, ou vous écrivez à froid ?"""


def norme(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'")


def phrases(texte):
    return [p.strip() for p in re.split(r"(?<=[.!?…])\s+|\n+", texte) if p.strip()]


def controler(texte, mediane=None, image=False):
    brut = texte.rstrip("\n")
    t = norme(brut)
    n = len(brut)
    constats = []

    def add(gravite, famille, constat, correction):
        constats.append({"gravite": gravite, "famille": famille, "constat": constat, "correction": correction})

    # MÉCANIQUE
    if n > LIMITE:
        add("bloquant", "mécanique", f"{n} caractères, {n - LIMITE} de plus que la limite de {LIMITE} (officiel).",
            "Une seule idée. La partie à laquelle tu tiens le plus est souvent celle à couper.")
    elif n < 300:
        add("info", "mécanique", f"{n} caractères : la place manque souvent pour une affirmation et sa preuve.",
            "Ajoute l'exemple précis, ou fais-en un commentaire plutôt qu'un post.")
    if mediane:
        if n > 2 * mediane or n < 0.5 * mediane:
            add("info", "mécanique", f"{n} caractères pour une médiane personnelle de {mediane} : très loin de tes habitudes.",
                "Pas un défaut. Note-le dans le journal pour que /linkedin-audit puisse comparer.")
    urls = URL_RE.findall(brut)
    if urls:
        add("attention", "mécanique", f"{len(urls)} lien(s) externe(s) dans le corps. Une étude tierce (1,3 M posts) observe environ 19% de portée médiane en moins ; LinkedIn n'a jamais confirmé de pénalité.",
            "Mets le lien en premier commentaire et dis-le dans le post. Garde-le dans le corps seulement si le clic EST l'objectif.")
    tags = HASHTAG_RE.findall(brut)
    if len(tags) > 3:
        add("attention", "mécanique", f"{len(tags)} hashtags : au-delà de 3, ils se lisent comme une course à la portée.",
            "Garde les 2 ou 3 qui décrivent vraiment le sujet, en fin de post.")

    # ACCROCHE
    premiere = next((l.strip() for l in brut.split("\n") if l.strip()), "")
    debut = brut[:PLI_MOBILE]
    if n > PLI_MOBILE:
        fins = [m.end() for m in re.finditer(r"[.!?…](?:\s|$)|\n", debut)]
        if not fins or fins[-1] < 40:
            add("majeur", "accroche", f"Aucune phrase ne se termine avant le caractère {PLI_MOBILE} (le « voir plus » mobile, position observée).",
                f"Termine une phrase avant le caractère {PLI_MOBILE}. Sur ordinateur, le pli est vers {PLI_ORDI} : le mobile est la contrainte.")
    if premiere.rstrip().endswith("?"):
        add("attention", "accroche", "Question en première ligne. Une étude tierce (vendeur) observe environ −34% de likes ; règle du pack : pas de question en ouverture par défaut.",
            "Remplace la question par le chiffre ou le fait qui y répond. Si ton audit montre l'inverse pour ton compte, garde-la.")
    tp = norme(premiere)
    usees = [o for o in OUVERTURES if tp.startswith(o) or o in norme(debut)[:80]]
    if usees:
        add("majeur", "accroche", f"Ouverture usée : « {usees[0]} ».",
            "Ouvre sur la chose précise : le chiffre, l'erreur, la phrase que quelqu'un t'a dite.")
    if not re.search(r"\d", premiere):
        add("info", "accroche", "Pas de chiffre en première ligne.",
            "Un chiffre précis est l'ouverture la plus solide [étude tierce, vendeur]. Pas obligatoire si la phrase tient seule.")

    # INTÉGRITÉ
    appats = sorted({label for motif, label in APPATS if re.search(motif, t, re.I | re.M)})
    if appats:
        add("bloquant", "intégrité", "Appât d'engagement : " + ", ".join(appats) + ". LinkedIn en réduit la diffusion (annonce du 12 mars 2026) et ses règles l'interdisent.",
            "Pose la question que le post a méritée, ou donne la ressource sans condition.")
    if "{{" in brut:
        add("bloquant", "intégrité", "Champ {{…}} encore présent : le post n'est pas prêt.",
            "Remplace-le par le vrai fait (reserve.md, utilisateur) ou supprime la phrase.")
    if "—" in brut or re.search(r"\s–\s", brut):
        add("bloquant", "intégrité", "Tiret cadratin ou demi-cadratin en incise : règle de l'utilisateur.",
            "Supprime-le, ou remplace-le par une virgule (jamais un point-virgule). humanize.py le fait.")
    sup = [s for s in SUPERLATIFS if s in t]
    if sup:
        add("attention", "intégrité", "Superlatifs invérifiables : " + ", ".join(sup) + ".",
            "Remplace par ce que tu as mesuré, sur quelle période, dans quel contexte.")

    # DENSITÉ
    nb_contrastes = sum(len(re.findall(m, t, re.I)) for m in CONTRASTES)
    if nb_contrastes > 1:
        add("majeur", "densité", f"{nb_contrastes} contrastes (« ce n'est pas X, c'est Y », « pas X, mais Y »…) : 1 au plus par post.",
            "Garde le plus fort. Écris les autres en affirmations.")
    triades = TRIADE.findall(brut)
    if len(triades) > 1:
        add("majeur", "densité", f"{len(triades)} énumérations en trois : 1 au plus, faite de faits (noms, chiffres), pas d'adjectifs.",
            "Garde la plus concrète, casse les autres en 2 ou 4 éléments.")
    ponts = [m.group(0).strip() for p in PONTS for m in re.finditer(p, t, re.I)]
    if ponts:
        add("majeur", "densité", "Pont de révélation : " + ", ".join(f"« {p} »" for p in ponts[:3]) + " (environ −4,8%, étude tierce, vendeur).",
            "Supprime le pont et écris la révélation à plat, avec un chiffre.")
    ph = phrases(brut)
    questions_avant = [p for p in ph[:-2] if p.endswith("?")] if len(ph) > 2 else []
    if questions_avant:
        add("attention", "densité", f"{len(questions_avant)} question(s) avant la fin : « {questions_avant[0][:60]} ».",
            "Une seule question, à la fin. Les questions rhétoriques au milieu se lisent comme de la mise en scène.")
    ctas = CTA.findall(t)
    if len(ctas) > 1:
        add("attention", "densité", f"{len(ctas)} appels à l'action ({', '.join(sorted(set(ctas)))}) : un seul par post, en une phrase.",
            "Garde celui que contexte.md associe à ce sujet. Beaucoup de posts n'en méritent aucun.")

    # ACCESSIBILITÉ
    pseudo = PSEUDO_RE.findall(brut)
    if pseudo:
        add("bloquant", "accessibilité", f"{len(pseudo)} caractères en pseudo-gras ou pseudo-italique Unicode : lus comme des symboles mathématiques par les lecteurs d'écran, non trouvés par la recherche.",
            "Texte normal. L'insistance vient des retours à la ligne et de l'ordre des mots.")
    emojis = EMOJI_RE.findall(brut)
    if len(emojis) > 6:
        add("attention", "accessibilité", f"{len(emojis)} émojis : chacun est lu à voix haute par les lecteurs d'écran.",
            "Garde ceux qui structurent, coupe les décoratifs.")
    if re.match(r"\s*[\U0001F300-\U0001FAFF☀-➿]", brut):
        add("info", "accessibilité", "Le post commence par un émoji.", "Commence par un mot : c'est lui qu'on lit dans l'aperçu.")
    caps = [l for l in brut.split("\n") if len(l) > 20 and l.isupper()]
    if caps:
        add("attention", "accessibilité", f"{len(caps)} ligne(s) en capitales : certains lecteurs d'écran les épellent.",
            "Casse normale.")
    paras = [p for p in re.split(r"\n\s*\n", brut) if p.strip()]
    plus_long = max((len(p) for p in paras), default=0)
    if plus_long > 600:
        add("attention", "accessibilité", f"Paragraphe de {plus_long} caractères : un mur sur téléphone.",
            "Coupe aux changements d'idée : 1 à 3 lignes par bloc.")
    if image:
        add("info", "accessibilité", "Image ou document joint : LinkedIn permet un texte alternatif et ne l'écrit pas pour toi.",
            "Une phrase qui dit ce que montre l'image, pas « graphique ».")

    # FIN
    fin = t[-300:]
    if "?" not in fin and not CTA.search(fin):
        add("info", "fin", "Le post se termine sans question ni prochaine étape.",
            "Une question que seul ce post peut poser, ou rien. Jamais « Qu'en pensez-vous ? ».")

    poids = {"bloquant": 22, "majeur": 11, "attention": 6, "info": 1}
    note = max(0, 100 - sum(poids[c["gravite"]] for c in constats))
    bloquant = any(c["gravite"] == "bloquant" for c in constats)
    if bloquant:
        note = min(note, 60)
        verdict, code = ("À RÉÉCRIRE", 3) if note < 50 else ("À REVOIR", 2)
    elif note >= 75:
        verdict, code = "PRÊT", 0
    elif note >= 50:
        verdict, code = "À REVOIR", 2
    else:
        verdict, code = "À RÉÉCRIRE", 3
    ordre = {"bloquant": 0, "majeur": 1, "attention": 2, "info": 3}
    return {
        "note": note, "verdict": verdict, "code": code,
        "stats": {"caracteres": n, "limite": LIMITE, "hashtags": len(tags), "liens": len(urls),
                  "emojis": len(emojis), "paragraphes": len(paras), "contrastes": nb_contrastes,
                  "triades": len(triades), "appels_action": len(ctas),
                  "visible_mobile": debut, "visible_ordinateur": brut[:PLI_ORDI]},
        "constats": sorted(constats, key=lambda c: ordre[c["gravite"]]),
    }


def afficher(r):
    s = r["stats"]
    L = [f"POST  {r['note']}/100  {r['verdict']}",
         f"{s['caracteres']}/{s['limite']} caractères · {s['hashtags']} hashtag(s) · {s['liens']} lien(s) · "
         f"{s['contrastes']} contraste(s) · {s['triades']} triade(s) · {s['appels_action']} appel(s) à l'action", "",
         "Visible avant « voir plus » (mobile, ~140) :", f"  « {s['visible_mobile'].replace(chr(10), ' / ')} »", ""]
    if not r["constats"]:
        L.append("Aucun constat. Relis-le à voix haute avant de le publier.")
    for c in r["constats"]:
        L.append(f"  [{c['gravite'].upper()}] {c['famille']} : {c['constat']}")
        L.append(f"      → {c['correction']}")
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser(description="Contrôle un post LinkedIn (PRÊT 0 / À REVOIR 2 / À RÉÉCRIRE 3).")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--texte")
    src.add_argument("--fichier")
    src.add_argument("--exemple", action="store_true")
    p.add_argument("--mediane", type=int, help="longueur médiane de tes posts (rendue par /linkedin-audit)")
    p.add_argument("--image", action="store_true", help="le post a une image ou un document")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.exemple:
        texte = EXEMPLE
    elif a.fichier:
        try:
            texte = open(a.fichier, encoding="utf-8").read()
        except OSError as err:
            print(f"Erreur : {err}", file=sys.stderr)
            return 1
    elif a.texte:
        texte = a.texte
    elif not sys.stdin.isatty():
        texte = sys.stdin.read()
    else:
        p.print_help(sys.stderr)
        return 1
    r = controler(texte, a.mediane, a.image)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
