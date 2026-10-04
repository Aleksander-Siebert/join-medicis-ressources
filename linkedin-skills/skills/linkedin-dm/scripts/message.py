#!/usr/bin/env python3
"""message.py : contrôle une note d'invitation, un message ou une relance LinkedIn.

  verifier --type note|message|relance --texte "…" [--premium] [--prospection]
           [--relance-n 1] [--nouveau "ce qui a changé"] [--ligne "la ligne propre à la personne"]
      BLOQUANT
        - aucune ligne propre à la personne (un post, un commentaire, une
          décision, une intervention : ce qu'on n'aurait pas pu envoyer à un autre)
        - note au-delà de 200 caractères (compte gratuit, aide LinkedIn a563153)
        - demande, pitch ou lien dans une note d'invitation
        - lien d'agenda (Calendly…) dans un premier message
        - relance sans élément nouveau, ou 3e relance
        - tiret cadratin
      ATTENTION
        - phrases qui sentent l'envoi en masse (« Je me permets », « J'espère
          que vous allez bien », « Je suis tombé sur votre profil »,
          « Petite relance »…)
        - « vous accorder 15 minutes » ou « échanger » sans question précise
        - message de plus de 600 caractères (illisible sur un téléphone)
        - message de prospection sans moyen simple de dire non (CNIL)
        - plusieurs demandes dans le même message

  lot --fichier messages.txt
      Compare des messages destinés à des personnes différentes (séparés par
      une ligne « --- ») : au-delà de 60% de texte commun une fois les noms
      retirés, c'est un envoi en masse (Professional Community Policies).

Codes de sortie : 0 OK, 2 attention, 3 bloquant, 1 erreur.

D'après outreach_message_builder.py (alirezarezvani, claude-skills, MIT),
réécrit en français et complété (relances, CNIL, lot). Rien n'est envoyé :
l'utilisateur copie chaque message, une personne à la fois. Sans dépendance.
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

PLAFOND_NOTE = 200          # aide LinkedIn a563153, compte gratuit
PLAFOND_NOTE_PREMIUM = 300  # sources tierces, [à vérifier]
CONFORT_MESSAGE = 600

PHRASES = [
    ("je me permets", "formule de courrier type : commence par la ligne propre à la personne"),
    ("j'espere que vous allez bien", "remplissage : supprime"),
    ("j'espere que tu vas bien", "remplissage : supprime"),
    ("j'espere que ce message vous trouve", "calque de l'anglais : supprime"),
    ("je suis tombe sur votre profil", "ne dit rien : dis ce que tu lisais quand tu l'as trouvée"),
    ("je suis tombee sur votre profil", "ne dit rien : dis ce que tu lisais quand tu l'as trouvée"),
    ("en parcourant votre profil", "ne dit rien : dis ce que tu as lu d'elle"),
    ("votre profil a retenu mon attention", "ne dit rien : dis ce qui a retenu ton attention"),
    ("votre parcours est inspirant", "compliment sans contenu : nomme ce qui t'a servi"),
    ("votre parcours m'inspire", "compliment sans contenu : nomme ce qui t'a servi"),
    ("elargir mon reseau", "une raison qui vaut pour tout le monde n'en est pas une"),
    ("agrandir mon reseau", "une raison qui vaut pour tout le monde n'en est pas une"),
    ("vous avoir dans mon reseau", "une raison qui vaut pour tout le monde n'en est pas une"),
    ("rejoindre votre reseau", "une raison qui vaut pour tout le monde n'en est pas une"),
    ("en tant que", "l'appartenance à une catégorie n'est pas une raison (vérifie la phrase)"),
    ("nous avons beaucoup en commun", "dis quoi, précisément"),
    ("petite question", "elle n'est jamais petite : pose-la"),
    ("rapide question", "elle n'est jamais rapide : pose-la"),
    ("je reviens vers vous", "dis ce qui a changé depuis, ou ne relance pas"),
    ("je reviens vers toi", "dis ce qui a changé depuis, ou ne relance pas"),
    ("petite relance", "dis ce qui a changé depuis, ou ne relance pas"),
    ("je me permets de relancer", "dis ce qui a changé depuis, ou ne relance pas"),
    ("sans nouvelle de votre part", "reproche implicite : supprime"),
    ("sans reponse de votre part", "reproche implicite : supprime"),
    ("je remonte mon message", "dis ce qui a changé depuis, ou ne relance pas"),
    ("synergie", "personne n'a jamais répondu à ce mot"),
    ("faire un point", "dit pas ce que tu veux"),
    ("prendre un cafe virtuel", "demande du temps sans question précise"),
    ("vous piquer quelques idees", "demande du temps sans question précise"),
    ("vous solliciter", "dis la demande, simplement"),
    ("je serais ravi d'echanger", "échanger sur quoi ? une question précise"),
    ("je serais ravie d'echanger", "échanger sur quoi ? une question précise"),
    ("n'hesitez pas a me contacter", "formule de fin vide : supprime"),
    ("au plaisir d'echanger", "formule de fin vide : supprime"),
    ("je ne vous prendrai que", "tu annonces la durée au lieu de poser la question"),
]
PITCH = re.compile(r"\b(?:notre (?:solution|plateforme|offre|outil|logiciel|service|agence|cabinet)|nous aidons les|"
                   r"on aide les|j'aide les|nous accompagnons les|demo|demonstration|essai gratuit|tarifs?|devis|"
                   r"proposition commerciale|prendre rendez-vous|reserver un creneau|etes-vous la bonne personne|"
                   r"decideur)\b")
DEMANDE = re.compile(r"\b(?:appel|visio|rendez-vous|reunion|15 minutes|20 minutes|30 minutes|un cafe|zoom|teams|"
                     r"un echange|echanger|vous appeler|t'appeler|disponible|disponibilites|creneau)\b")
AGENDA = re.compile(r"calendly|cal\.com|zcal|meetings\.hubspot|calendar\.app|tidycal|youcanbook|"
                    r"\bprenez? (?:un )?creneau\b|\breservez?\b.{0,20}\bcreneau")
LIEN = re.compile(r"https?://|www\.|\b\w+\.(?:com|fr|io|co|example)\b(?:/\S*)?")
SPECIFIQUE = re.compile(r"\b(?:votre|ton|ta|vos|tes) (?:post|article|commentaire|intervention|conference|talk|podcast|"
                        r"episode|newsletter|livre|etude|rapport|carrousel|video|fil|analyse|retour|message|question|"
                        r"remarque|reponse|refonte|decision|annonce|recrutement|levee|lancement|nomination|projet|equipe|these|chiffre|"
                        r"table ronde|atelier|webinaire)\b|"
                        r"\b(?:vous avez|tu as) (?:ecrit|publie|dit|explique|partage|montre|annonce|lance|recrute|"
                        r"commente|presente|raconte|teste|choisi|decide|repondu|mene|conduit|pilote|rejoint|quitte|cree|fonde)\b|"
                        r"\b(?:vous|tu) (?:ecriviez|ecrivais|disiez|disais|parliez|parlais|expliquiez|expliquais|evoquiez|evoquais)\b|"
                        r"\b(?:sous|dans|a) (?:votre|ton|ta) |«")
OPPOSITION = re.compile(r"\b(?:si (?:ce n'est|ca n'est) pas (?:le bon moment|un sujet|pour (?:vous|toi))|"
                        r"(?:un|d'un) (?:mot|non) (?:suffit|et)|je n'insisterai pas|je n'insiste pas|je ne vous (?:re)?relancerai pas|"
                        r"je ne te (?:re)?relancerai pas|dites-le-moi|dis-le-moi|pas de reponse attendue|"
                        r"pas besoin de repondre|aucune obligation|je ne vous ecrirai plus|je ne t'ecrirai plus|stop)\b")
NOUVEAU = re.compile(r"\b(?:depuis|nouveau|nouvelle|nouveaux|vient de|viens de|venons de|cette semaine|ce matin|"
                     r"hier|publie|sorti|resultat|chiffre|etude|cas|exemple|a change|ont change)\b|\d")


def norme(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'")


def verifier(type_, texte, premium=False, prospection=False, relance_n=1, nouveau="", ligne=""):
    t, tn = texte.strip(), norme(texte)
    bloquants, attentions = [], []
    n = len(t)
    plafond = PLAFOND_NOTE_PREMIUM if premium else PLAFOND_NOTE
    lien = LIEN.search(tn)

    # la ligne propre à la personne
    ln = norme(ligne)
    if ligne:
        if len(ligne.split()) < 6:
            attentions.append(f"La ligne propre à la personne fait {len(ligne.split())} mots : trop courte pour prouver que tu l'as lue. Nomme ce qu'elle a fait et ce qui t'a servi.")
        if ln.strip() and ln.strip()[:30] not in tn:
            attentions.append("La ligne propre à la personne n'apparaît pas dans le texte.")
    elif type_ != "relance" and not SPECIFIQUE.search(tn):
        bloquants.append("Aucune ligne propre à la personne (son post, son commentaire, sa décision, son intervention). "
                         "Test : ce message aurait-il pu partir à quelqu'un d'autre ? Si oui, c'est un modèle, et c'est lui qu'on ignore.")

    if type_ == "note":
        if n > plafond:
            bloquants.append(f"{n} caractères : la note est limitée à {plafond}" +
                             (" (Premium, longueur [à vérifier] dans ton compte)." if premium else " en compte gratuit (aide LinkedIn a563153)."))
        elif premium and n > PLAFOND_NOTE:
            attentions.append(f"{n} caractères : au-delà de 200, la limite Premium de 300 vient de sources tierces [à vérifier].")
        if DEMANDE.search(tn) or "?" in t and re.search(r"\b(?:pourrions|pourrait|serait|seriez|accepteriez|auriez)\b", tn):
            bloquants.append("Une demande dans la note : la note ouvre la conversation, la demande vient après l'acceptation. "
                             "(Étude La Growth Machine : la note change peu l'acceptation, elle double à peu près la réponse ensuite.)")
        if PITCH.search(tn):
            bloquants.append("Argumentaire dans une note d'invitation : personne n'achète sur une invitation, et c'est la seule impression que tu donnes.")
        if lien:
            bloquants.append("Lien dans une note d'invitation : retire-le.")
    else:
        if n > CONFORT_MESSAGE:
            attentions.append(f"{n} caractères : au-delà de {CONFORT_MESSAGE}, un message est un mur sur un téléphone. Une ligne propre, une raison, une demande.")
        if type_ == "message" and AGENDA.search(tn):
            bloquants.append("Lien d'agenda dans un premier message : ça sent l'entonnoir, parce que c'en est un. Demande d'abord si le sujet l'intéresse.")
        demandes = len(re.findall(r"\?", t))
        if demandes >= 3:
            attentions.append(f"{demandes} questions : une seule demande par message, la plus petite possible.")
        temps = re.compile(r"\b(?:echanger|un echange|15 minutes|20 minutes|30 minutes|un appel|un cafe|disponible|disponibilites|creneau|en parler)\b")
        questions = re.findall(r"[^.!?:;]*\?", tn)
        if temps.search(tn) and (not questions or all(temps.search(q) for q in questions)):
            attentions.append("Une demande de temps sans question précise : pose une question à laquelle on peut répondre en deux phrases.")
        if type_ == "message" and PITCH.search(tn):
            attentions.append("Argumentaire dès le premier message : donne d'abord (un chiffre, un retour, une réponse), l'offre viendra si on te la demande.")
        if prospection and not OPPOSITION.search(tn):
            attentions.append("Prospection sans moyen simple de dire non : ajoute par exemple « Si ce n'est pas le sujet, un mot suffit et je n'insiste pas. » "
                              "(CNIL : la personne doit pouvoir s'opposer simplement.)")

    if type_ == "relance":
        if relance_n >= 3:
            bloquants.append("3e relance : la séquence s'arrête après une relance, deux au plus s'il y a du nouveau.")
        if not (nouveau.strip() or NOUVEAU.search(tn)):
            bloquants.append("Relance sans élément nouveau : dis ce qui a changé (un résultat, une ressource, une actualité de la personne), sinon ne relance pas.")
        elif relance_n == 2 and not nouveau.strip():
            attentions.append("2e relance : seulement avec un élément vraiment nouveau. Précise-le avec --nouveau.")

    for p, pourquoi in PHRASES:
        if p in tn:
            attentions.append(f"« {p} » : {pourquoi}.")
    if "—" in t or re.search(r"\s–\s", t):
        bloquants.append("Tiret cadratin : supprime-le ou mets une virgule.")

    verdict, code = ("BLOQUÉ", 3) if bloquants else ("À REVOIR", 2) if attentions else ("OK", 0)
    return {"verdict": verdict, "code": code, "type": type_, "caracteres": n,
            "plafond": plafond if type_ == "note" else None, "bloquants": bloquants, "attentions": attentions}


def _mots(t, noms):
    tn = norme(t)
    for nom in noms:
        tn = tn.replace(nom, " ")
    return [w for w in re.findall(r"[a-z0-9']+", tn) if len(w) > 2]


def _bigrammes(mots):
    return {(a, b) for a, b in zip(mots, mots[1:])}


def lot(texte):
    messages = [m.strip() for m in re.split(r"^\s*---\s*$", texte, flags=re.M) if m.strip()]
    # les noms propres (mots capitalisés hors début de phrase) sont retirés avant comparaison
    noms = set()
    for m in messages:
        for x in re.findall(r"(?<![.!?]\s)(?<!^)\b([A-ZÉ][a-zéèëïî-]{2,})", m):
            noms.add(norme(x))
    paires = []
    for i in range(len(messages)):
        for j in range(i + 1, len(messages)):
            a, b = _bigrammes(_mots(messages[i], noms)), _bigrammes(_mots(messages[j], noms))
            if not a or not b:
                continue
            commun = len(a & b) / min(len(a), len(b))
            if commun > 0.6:
                paires.append({"messages": [i + 1, j + 1], "commun": round(commun * 100)})
    code = 3 if paires else 0
    return {"messages": len(messages), "trop_proches": paires, "code": code,
            "verdict": "ENVOI EN MASSE" if paires else "OK"}


def main():
    a = argparse.ArgumentParser(description="Contrôle une note d'invitation, un message, une relance, ou un lot.")
    sous = a.add_subparsers(dest="cmd", required=True)
    v = sous.add_parser("verifier")
    v.add_argument("--type", choices=["note", "message", "relance"], required=True)
    v.add_argument("--texte", required=True)
    v.add_argument("--premium", action="store_true")
    v.add_argument("--prospection", action="store_true", help="message à visée commerciale (contrôle CNIL)")
    v.add_argument("--relance-n", type=int, default=1)
    v.add_argument("--nouveau", default="")
    v.add_argument("--ligne", default="", help="la ligne propre à la personne")
    v.add_argument("--json", action="store_true")
    lo = sous.add_parser("lot")
    lo.add_argument("--fichier", required=True)
    lo.add_argument("--json", action="store_true")
    x = a.parse_args()
    try:
        if x.cmd == "lot":
            r = lot(Path(x.fichier).read_text(encoding="utf-8"))
            if x.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                print(f"LOT  {r['verdict']}  ·  {r['messages']} messages")
                for p in r["trop_proches"]:
                    print(f"  ✖ messages {p['messages'][0]} et {p['messages'][1]} : {p['commun']}% de texte commun, noms retirés. "
                          "Un message copié à l'identique est un envoi en masse : réécris chacun à partir de sa ligne propre.")
            return r["code"]
        r = verifier(x.type, x.texte, x.premium, x.prospection, x.relance_n, x.nouveau, x.ligne)
    except OSError as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    if x.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        cap = f"/{r['plafond']}" if r["plafond"] else ""
        print(f"{x.type.upper()}  {r['verdict']}  ·  {r['caracteres']}{cap} caractères")
        for b in r["bloquants"]:
            print(f"  ✖ {b}")
        for t in r["attentions"]:
            print(f"  ! {t}")
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
