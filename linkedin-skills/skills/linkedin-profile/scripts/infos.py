#!/usr/bin/env python3
"""infos.py : contrôle la section Infos (About) d'un profil LinkedIn.

LinkedIn replie la section Infos après les premiers caractères et cache la
suite derrière « … voir plus ». La position exacte n'est pas publiée : on
l'observe entre ~200 et ~265 caractères selon l'appareil. Ce qui est au-dessus
du pli est toute la section pour la plupart des lecteurs.

Ce script ne rédige rien. Il mesure et refuse :
  BLOQUANT  plus de 2 600 caractères ; aucune phrase terminée avant le pli ;
            ni audience ni preuve avant le pli ; aucun appel à l'action ;
            pseudo-gras Unicode
  ATTENTION moins de 400 caractères ; ouverture usée (« Passionné », « Fort de
            X ans », « Bienvenue ») ; troisième personne ; mots creux ; aucune
            preuve chiffrée ; pavé sans saut de ligne ; mot-clé absent du texte

Codes de sortie : 0 PASSE · 2 À REVOIR (avertissements) · 3 BLOQUÉ · 1 erreur

Adapté de about_section_builder.py (alirezarezvani/claude-skills, MIT), réécrit
pour le français. Sans dépendance, sans réseau.

Exemples :
  python3 infos.py --fichier infos.txt --mots-cles "acquisition,assurance"
  python3 infos.py --texte "…" --objectif emploi --json
  python3 infos.py --exemple
"""

import argparse
import json
import re
import sys
import unicodedata

LIMITE = 2600
PLI_COURT = 200      # pli prudent (mobile)
PLI_LONG = 265       # pli observé le plus souvent cité
MIN_PHRASE = 80      # une phrase doit finir entre 80 et le pli

MOTS_CREUX = [
    "passionne", "passionnee", "dynamique", "oriente resultats", "orientee resultats",
    "rigoureux", "rigoureuse", "motive", "motivee", "force de proposition", "esprit d'equipe",
    "touche-a-tout", "couteau suisse", "proactif", "proactive", "en quete de nouveaux defis",
    "sortir des sentiers battus", "valeur ajoutee", "expertise pointue", "a forte valeur ajoutee",
    "solutions innovantes", "accompagnement sur mesure", "leader d'opinion", "visionnaire",
]
OUVERTURES_USEES = [
    (r"^(bonjour|bienvenue|hello|salut)\b", "salutation : le lecteur n'apprend rien"),
    (r"^(passionne|passionnee)\b", "« Passionné(e) » : une attitude, pas une information"),
    (r"^(forte?|dote|dotee) d['e ]", "« Fort(e) de X ans d'expérience » : la formule de CV la plus courante"),
    (r"^(je suis|je m'appelle)\b", "« Je suis… » : commence par le lecteur, pas par toi"),
    (r"^(depuis (plus de )?\d+ ans)\b", "« Depuis X ans » : l'ancienneté n'est pas une preuve de résultat"),
    (r"^(mon parcours|ma mission|mon objectif)\b", "méta-annonce : dis-le directement"),
]
AUDIENCE = re.compile(
    r"\b(pour les|pour des|j'aide|j aide|j'accompagne|je travaille avec|mes clients|nos clients|"
    r"dirigeants?|fondateurs?|startups?|pme|eti|tpe|equipes|b2b|b2c|saas|assureurs|cabinets|"
    r"agences|independants|freelances|recruteurs|marketeurs|commerciaux|daf|drh|cmo|cto|ceo|"
    r"e-commer\w*|industriels|marques|entrepreneurs|createurs|collectivites|associations)\b")
PREUVE = re.compile(
    r"\d+\s*(%|x\b|×)|[x×]\s?\d|\d\s?(k€|m€|€|millions?)|\b\d[\d\s.]*\s*(clients?|projets?|"
    r"entreprises|marques|personnes|contrats?|leads?|abonnes|utilisateurs|missions|pays|"
    r"mois|semaines|jours)\b|(^|\s)ex-?\s?[a-z]")
CTA = re.compile(
    r"(\b(ecris-moi|ecrivez-moi|contacte-moi|contactez-moi|envoie-moi|envoyez-moi|message prive|"
    r"en message|par message|mp|dm|reserve|reservez|prenons|prends rendez-vous|prenez rendez-vous|"
    r"rendez-vous|calendly|lien|liens|appel de \d+|parlons|echangeons|discutons|abonne-toi|"
    r"abonnez-vous|newsletter|telecharge|telechargez)\b|cal\.com|@|https?://|www\.)")
PREMIERE_PERSONNE = re.compile(r"\b(je|j'|mon|ma|mes|me|m'|moi)\b")
TROISIEME = re.compile(r"\b(il|elle) (est|a|accompagne|aide|travaille|dirige)\b")

EXEMPLE = (
    "Un tiers des clients d'une assurance en ligne ne renouvelle pas, et la plupart des équipes "
    "pensent que c'est une question de prix. Chez Assurly, j'ai appris que c'était souvent le délai "
    "de remboursement.\n\n"
    "Je dirige l'acquisition d'Assurly, une assurance en ligne de 120 salariés : publicité, SEO, "
    "emailing et fidélisation.\n\n"
    "Ce que j'ai fait, en chiffres :\n"
    "· Réduit le coût par lead de 41 € à 23 € en 4 mois, budget constant.\n"
    "· Relancé 1 400 clients dormants en 6 semaines : 212 contrats réactivés.\n\n"
    "Comment je travaille : je pars des appels clients avant de toucher aux campagnes. Les mots "
    "qu'ils emploient finissent dans nos annonces.\n\n"
    "Tu diriges le marketing d'un assureur ou d'un courtier en ligne et ton coût par lead monte ? "
    "Écris-moi en message privé : je te dis en 20 minutes où je chercherais en premier."
)


def norme(texte: str) -> str:
    t = unicodedata.normalize("NFKD", texte.lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'")


def derniere_fin_de_phrase(texte: str, limite: int) -> int:
    zone = texte[:limite]
    fins = [m.end() for m in re.finditer(r"[.!?…](\s|$)|[.!?…]»|\n\n", zone)]
    return fins[-1] if fins else -1


def controler(texte: str, objectif: str = "clients", mots_cles=None, prenom: str = "") -> dict:
    mots_cles = [m.strip() for m in (mots_cles or []) if m.strip()]
    t = norme(texte)
    n = len(texte)
    constats = []

    def ajouter(gravite, controle, constat, correction):
        constats.append({"gravite": gravite, "controle": controle, "constat": constat, "correction": correction})

    if n > LIMITE:
        ajouter("bloquant", "longueur", f"{n} caractères, {n - LIMITE} de plus que la limite de {LIMITE}.",
                "Coupe d'abord le bloc « comment je travaille » : c'est celui que le lecteur devine.")
    elif n < 400:
        ajouter("attention", "longueur", f"{n} caractères : pas la place pour une promesse et sa preuve.",
                "Ajoute un résultat chiffré ou une phrase qui dit pour qui tu travailles.")
    elif n > 2000:
        ajouter("attention", "longueur", f"{n} caractères : au-delà d'environ 1 500, peu de lecteurs vont au bout.",
                "Garde ce qui sert la décision du lecteur, coupe le reste.")

    if any(0x1D400 <= ord(c) <= 0x1D7FF for c in texte):
        ajouter("bloquant", "accessibilité", "Pseudo-gras ou pseudo-italique Unicode : lu comme des symboles par les lecteurs d'écran.",
                "Texte normal, sauts de ligne pour structurer.")

    fin = derniere_fin_de_phrase(texte, PLI_LONG)
    if n > PLI_LONG and fin < MIN_PHRASE:
        ajouter("bloquant", "pli", f"Aucune phrase ne se termine entre le caractère {MIN_PHRASE} et le pli (~{PLI_LONG}). Le lecteur voit une pensée coupée et s'arrête.",
                f"Réécris l'ouverture pour qu'une phrase se termine avant le caractère {PLI_COURT} si possible, {PLI_LONG} au plus tard.")
    elif n > PLI_COURT and derniere_fin_de_phrase(texte, PLI_COURT) < MIN_PHRASE:
        ajouter("attention", "pli", f"Aucune phrase ne finit avant le caractère {PLI_COURT} : sur certains téléphones, le pli tombe au milieu.",
                "Raccourcis la première phrase.")

    visible = texte[:PLI_LONG]
    tv = norme(visible)
    if not AUDIENCE.search(tv) and not PREUVE.search(tv):
        ajouter("bloquant", "contenu du pli", "Avant le pli, ni audience ni preuve : c'est un échauffement, et c'est tout ce que la plupart des lecteurs verront.",
                "Remonte la phrase qui dit pour qui tu travailles, ou celle qui porte un chiffre, dans les deux premières phrases.")

    debut = t.lstrip()
    for motif, raison in OUVERTURES_USEES:
        if re.search(motif, debut):
            ajouter("attention", "ouverture", f"Ouverture usée : {raison}.",
                    "Commence par le problème du lecteur, dans ses mots, ou par un chiffre.")
            break
    if prenom and norme(prenom) in norme(texte[:60]):
        ajouter("attention", "ouverture", "L'ouverture commence par ton nom.", "Le nom est déjà au-dessus. Commence par le lecteur.")

    if not CTA.search(t):
        gravite = "attention" if objectif == "autorite" else "bloquant"
        ajouter(gravite, "appel à l'action", "Aucune prochaine étape : la section se termine et le lecteur n'a rien à faire.",
                "Une phrase : qui doit t'écrire, et ce qu'il obtient (« Écris-moi : je te dis en 20 minutes… »).")

    if len(PREMIERE_PERSONNE.findall(t)) < 2 or TROISIEME.search(t[:300]):
        ajouter("attention", "voix", "Écrit à la troisième personne ou sans « je » : ça se lit comme un communiqué écrit par quelqu'un d'autre.",
                "Écris comme tu le dirais : « Je dirige… », pas « Camille est… ».")

    creux = [m for m in MOTS_CREUX if re.search(rf"(?<![\w-]){re.escape(m)}(?![\w])", t)]
    if creux:
        ajouter("attention", "mots creux", "Mots creux : " + ", ".join(creux) + ".",
                "Supprime chacun. S'il manque du sens, remplace-le par la chose précise qu'il cachait.")

    if not PREUVE.search(t):
        ajouter("attention", "preuve", "Aucun chiffre, aucun volume, aucune ancienne entreprise dans toute la section.",
                "Un résultat réel et vérifiable (voir reserve.md). Une fourchette honnête vaut mieux qu'un chiffre inventé.")

    paragraphes = [p for p in re.split(r"\n\s*\n", texte) if p.strip()]
    if any(len(p) > 600 for p in paragraphes):
        ajouter("attention", "mise en page", "Un paragraphe de plus de 600 caractères : sur mobile, c'est un mur.",
                "Un saut de ligne toutes les 2 ou 3 phrases.")

    if mots_cles:
        absents = [m for m in mots_cles if norme(m) not in t]
        if absents:
            ajouter("attention", "mots-clés", "Absents du texte : " + ", ".join(absents) + ".",
                    "Place les plus importants dans de vraies phrases, pas dans une liste en bas.")

    bloquants = [c for c in constats if c["gravite"] == "bloquant"]
    verdict, code = (("BLOQUÉ", 3) if bloquants else ("À REVOIR", 2) if constats else ("PASSE", 0))
    return {
        "verdict": verdict,
        "code": code,
        "caracteres": n,
        "limite": LIMITE,
        "visible_200": texte[:PLI_COURT],
        "visible_265": visible,
        "fin_de_phrase_avant_pli": fin,
        "constats": sorted(constats, key=lambda c: c["gravite"] != "bloquant"),
    }


def afficher(r: dict) -> str:
    L = [f"INFOS  {r['verdict']}  ·  {r['caracteres']}/{r['limite']} caractères", "",
         "Visible avant « voir plus » (pli prudent, ~200) :",
         f"  « {r['visible_200'].replace(chr(10), ' / ')} »",
         "Visible au pli le plus cité (~265) :",
         f"  « {r['visible_265'].replace(chr(10), ' / ')} »", ""]
    if not r["constats"]:
        L.append("Aucun problème mesurable. Relis-la à voix haute avant de la coller.")
    for c in r["constats"]:
        L.append(f"  [{c['gravite'].upper()}] {c['controle']} : {c['constat']}")
        L.append(f"      → {c['correction']}")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser(description="Contrôle la section Infos (PASSE 0 / À REVOIR 2 / BLOQUÉ 3).")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--texte")
    src.add_argument("--fichier")
    src.add_argument("--exemple", action="store_true")
    p.add_argument("--objectif", choices=["clients", "emploi", "autorite"], default="clients")
    p.add_argument("--mots-cles", default="", help="liste séparée par des virgules")
    p.add_argument("--prenom", default="", help="pour repérer une ouverture par son propre nom")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if a.exemple:
        texte = EXEMPLE
    elif a.fichier:
        try:
            with open(a.fichier, encoding="utf-8") as f:
                texte = f.read().strip()
        except OSError as err:
            print(f"Erreur : {err}", file=sys.stderr)
            return 1
    elif a.texte:
        texte = a.texte.strip()
    elif not sys.stdin.isatty():
        texte = sys.stdin.read().strip()
    else:
        p.print_help(sys.stderr)
        return 1

    r = controler(texte, a.objectif, a.mots_cles.split(","), a.prenom)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
