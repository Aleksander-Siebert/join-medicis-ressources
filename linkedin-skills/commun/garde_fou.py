#!/usr/bin/env python3
"""garde_fou.py : refuse les tactiques LinkedIn qui mettent le compte en danger.

Chaque Skill du pack LinkedIn passe une demande « à risque » (prospection,
volumes, outils, engagement, preuves) par ce script avant de rédiger. Il
classe la demande selon les Conditions d'utilisation de LinkedIn (§8.2),
la page d'aide sur les logiciels interdits, les Professional Community
Policies et le cadre CNIL de la prospection, puis rend un verdict :

  AUTORISÉ  (code 0) : rien ne bloque, continuer.
  ENCADRÉ   (code 2) : continuer, en appliquant les contraintes affichées.
  REFUSÉ    (code 3) : ne pas rédiger la tactique ; proposer l'alternative.
  (code 1 : erreur d'utilisation)

Un refus nomme toujours la règle et donne une alternative conforme.
Déterministe, sans dépendance, sans réseau : rien n'est envoyé nulle part.

Adapté de linkedin_policy_gate.py (alirezarezvani/claude-skills, MIT),
réécrit pour le français, la CNIL et les règles du pack Join Médicis.

Exemples :
  python3 garde_fou.py --texte "envoyer 300 invitations par jour avec Waalaxy"
  python3 garde_fou.py --fichier plan.md --json
  python3 garde_fou.py --exemple
"""

import argparse
import json
import re
import sys
import unicodedata

# Une négation proche du mot déclencheur (« sans bot », « pas de pod ») évite
# de refuser quelqu'un qui dit justement ne pas vouloir de la tactique.
NEGATION = re.compile(
    r"\b(sans|pas d[e']|pas un|pas une|aucun|aucune|jamais|ni|"
    r"no|not|never|without|interdit|interdits|eviter|refuse|"
    r"ne (?:veux|veut|voulons|souhaite|souhaitons) pas|pas question)\b"
)
FENETRE_NEGATION = 25  # caractères avant le déclencheur

REFUS = [
    {
        "id": "R1-AUTOMATISATION",
        "titre": "Activité automatisée sur LinkedIn",
        "regle": "Conditions d'utilisation LinkedIn §8.2 (robots et méthodes automatisées "
                 "pour ajouter des contacts, envoyer des messages, publier, commenter, aimer, "
                 "partager) ; Aide LinkedIn a1341387",
        "motifs": [
            r"\bauto[- ]?(connect|invit|dm|messag|like|comment|follow|publi|post|apply|postul)\w*",
            r"\b(publier|poster|commenter|liker|inviter|envoyer|relancer|postuler)\b.{0,40}"
            r"\b(automatiquement|en automatique|tout seul|a ma place)\b",
            r"\b(automatis\w+|automate[ds]?|automation)\b.{0,40}"
            r"\b(linkedin|invitations?|messages?|commentaires?|likes?|connexions?|posts?|relances?)\b",
            r"\b(linkedin|invitations?|messages?|commentaires?|likes?|connexions?|relances?)\b.{0,40}"
            r"\b(automatis\w+|automation)\b",
            r"\bbots?\b", r"\brobots?\b.{0,30}\b(linkedin|messages?|invitations?)\b",
            r"\b(selenium|puppeteer|playwright|headless)\b",
            r"\b(extension|plugin|plug-in)\b.{0,40}\b(linkedin|invitations?|messages?|connexions?)\b",
            r"\bsequence\b.{0,30}\b(linkedin|invitations?|messages? prives?)\b.{0,30}\bautomati",
        ],
        "alternative": "Faire le même travail à la main, sur un rythme plafonné. "
                       "/linkedin-dm (script volume.py) calcule un rythme tenable ; "
                       "le pack rédige, tu envoies. Pour publier à heure fixe : le "
                       "planificateur intégré à LinkedIn.",
    },
    {
        "id": "R2-EXTRACTION",
        "titre": "Extraction de profils ou de données de membres",
        "regle": "Conditions d'utilisation LinkedIn §8.2 (extraction, copie de profils) ; "
                 "Aide LinkedIn a1341387 ; RGPD (collecte sans information des personnes)",
        "motifs": [
            r"\bscrap\w*", r"\bcrawl\w*", r"\baspir\w+\b.{0,30}\b(profils?|contacts?|linkedin|donnees)\b",
            r"\b(extraire|recuperer|collecter|exporter|harvest|extract)\b.{0,40}"
            r"\b(emails?|e-mails?|adresses?|profils?|contacts?|leads?|membres?|numeros?)\b.{0,40}"
            r"\b(linkedin|profils?|en masse|automatiquement|tous)\b",
            r"\b(trouver|chercher|deviner)\b.{0,15}\b(son|leur|leurs|ses)\b.{0,15}\b(email|e-mail|adresse mail|numero)\b",
            r"\bemail finder\b",
            r"\b(fichier|base|liste)\b.{0,25}\b(de )?(leads?|prospects?|contacts?)\b.{0,30}"
            r"\b(depuis|a partir de|from)\b.{0,10}\blinkedin\b",
        ],
        "alternative": "Travailler sur TES données : l'export officiel (Préférences → "
                       "Confidentialité des données → Obtenir une copie de vos données) "
                       "et la recherche LinkedIn faite à la main. Pour un prospect précis, "
                       "noter source, date et base légale (CNIL).",
    },
    {
        "id": "R3-ENGAGEMENT-ARTIFICIEL",
        "titre": "Engagement artificiel (pods, échanges, achats)",
        "regle": "Professional Community Policies : « Don't do things to artificially increase "
                 "engagement » ; « don't agree with others ahead of time to like or re-share "
                 "each other's content » ; §8.2 (engagement inauthentique)",
        "motifs": [
            r"\bpods?\b", r"\bgroupes? d'engagement\b",
            r"\b(echange|echanger|swap)\w*\b.{0,20}\b(likes?|commentaires?|partages?|reposts?)\b",
            r"\blike[- ]?(pour|for)[- ]?like\b", r"\bcomment[- ]?(pour|for)[- ]?comment\w*\b",
            r"\b(acheter|achat|buy|payer)\b.{0,20}\b(abonnes|followers?|likes?|commentaires?|vues|impressions|relations?)\b",
            r"\b(faux|fausses|fake)\b.{0,15}\b(abonnes|followers?|likes?|commentaires?|engagement)\b",
            r"\b(se mettre d'accord|s'organiser|coordonner)\b.{0,40}\b(liker|commenter|partager)\b",
            r"\b(seeding|commentaires? de lancement)\b",
            r"\bcommenter\b.{0,30}\b(mes propres posts?|mon propre post)\b.{0,30}\b(autres? comptes?|faux)\b",
        ],
        "alternative": "Une vraie liste de réciprocité : /linkedin-comment choisit les posts "
                       "où ton commentaire apporte quelque chose, chaque jour, sans accord "
                       "préalable. Plus lent, et ça résiste à un contrôle.",
    },
    {
        "id": "R4-IDENTITE",
        "titre": "Fausse identité, double compte, usurpation",
        "regle": "Conditions d'utilisation LinkedIn §8.2 (fausse identité, compte d'autrui) ; "
                 "Professional Community Policies",
        "motifs": [
            r"\b(faux|fausse|fake)\b.{0,10}\b(profil|compte|persona|identite)\b",
            r"\b(deuxieme|second|double|autre|plusieurs)\b.{0,10}\bcomptes?\b.{0,20}\blinkedin\b",
            r"\busurp\w+", r"\bse faire passer pour\b", r"\bpretend(re|ing)? to be\b",
            r"\b(au nom de|a la place de|comme si c'etait)\b.{0,30}\b(sans|a son insu|sans qu'il|sans qu'elle)\b",
            r"\bsans (qu'il|qu'elle|qu'ils) (le )?sache\w*\b",
        ],
        "alternative": "Un seul profil, ton vrai nom. Écrire pour un dirigeant est normal "
                       "quand il relit et valide chaque post : il reste l'auteur.",
    },
    {
        "id": "R5-MESSAGES-EN-MASSE",
        "titre": "Messages ou invitations en masse",
        "regle": "Professional Community Policies (« untargeted… gratuitously repetitive "
                 "messages ») ; §8.2 ; CNIL (prospection non ciblée)",
        "motifs": [
            r"\b(en masse|massif|massivement|blast|bulk|mass)\b.{0,30}\b(messages?|dm|invitations?|inmails?)\b",
            r"\b(messages?|dm|invitations?|inmails?)\b.{0,30}\b(en masse|massivement|a tout le monde|a tous mes contacts|a toute la liste)\b",
            r"\b(meme|identique)\b.{0,15}\bmessage\b.{0,30}\b(a tous|a tout le monde|a \d{2,} personnes)\b",
            r"\b(meme|identique)\b.{0,15}\b(message|invitation|note)\b.{0,40}\b(ma liste|toute la liste|mes prospects|mon fichier|\d{2,} (?:personnes|prospects|contacts))\b",
            r"\b(copier[- ]coller|copy[- ]paste)\b.{0,30}\b(message|dm|invitation)\b.{0,30}\b(tous|tout le monde|centaines)\b",
            r"\b(\d{3,})\s*(invitations?|messages?|dm|demandes de connexion)\b.{0,20}\b(par jour|/jour|par semaine|/semaine|par mois)\b",
        ],
        "alternative": "Des messages un par un, chacun avec une ligne qui ne pourrait être "
                       "envoyée qu'à cette personne, sous un plafond hebdomadaire. "
                       "/linkedin-dm (message.py) refuse un message sans cette ligne. "
                       "Si c'est le nombre de contacts qui compte, la publicité LinkedIn "
                       "est le bon outil.",
    },
    {
        "id": "R6-PREUVE-INVENTEE",
        "titre": "Preuve, chiffre, client ou témoignage inventé",
        "regle": "Professional Community Policies (« false, misleading, or intended to "
                 "deceive ») ; §8.2 (informations inexactes) ; Code de la consommation, "
                 "pratiques commerciales trompeuses (art. L121-2)",
        "motifs": [
            r"\b(inventer|invente|inventes|imaginer|fabriquer|bidonner|make up|fabricate)\b.{0,40}"
            r"\b(chiffres?|stats?|statistiques?|resultats?|cas client|etude de cas|temoignages?|avis|clients?|"
            r"references?|diplomes?|certifications?|logos?|ca|chiffre d'affaires)\b",
            r"\b(faux|fausse|faux-|fake)\b.{0,10}\b(temoignages?|avis|chiffres?|cas client|resultats?|recommandations?)\b",
            r"\b(gonfler|exagerer|arrondir a la hausse|inflate|exaggerate)\b.{0,30}\b(chiffres?|resultats?|ca|clients?|nombres?)\b",
            r"\bfaire comme si\b.{0,40}\b(on avait|j'avais|nous avions)\b",
        ],
        "alternative": "Un vrai chiffre, une fourchette honnête (« plus de 200 »), un "
                       "ordre de grandeur ou un constat qualitatif. Sans preuve encore, le "
                       "post parle du processus, pas du résultat : /linkedin-interview "
                       "aide à retrouver les vrais chiffres.",
    },
    {
        "id": "R7-OUTILS-INTERDITS",
        "titre": "Outil tiers d'automatisation ou d'extraction nommé",
        "regle": "Aide LinkedIn a1341387 (logiciels et extensions interdits)",
        "motifs": [
            r"\b(waalaxy|prospectin|la growth machine|lagrowthmachine|lgm|dux[- ]?soup|phantom ?buster|"
            r"expandi|linked ?helper|meet ?alfred|octopus ?crm|lempod|zopto|we[- ]?connect|"
            r"salesflow|closely|texau|captain ?data|lemlist linkedin|podawaa|kaspr|lusha|"
            r"evaboot|apify|taplio autopilot)\b",
        ],
        "alternative": "Le planificateur intégré à LinkedIn et les partenaires officiels de "
                       "son API sont le chemin autorisé. Le pack ne se connecte jamais à ton "
                       "compte : il te donne du texte.",
    },
]

ENCADREMENTS = [
    {
        "id": "E1-PROSPECTION",
        "titre": "Prospection à la main",
        "motifs": [
            r"\b(prospect\w*|demandes? de connexion|invitations?|inmails?|messages? a froid|cold (dm|message|outreach)|outreach)\b",
        ],
        "contrainte": "Envoi à la main, une personne à la fois, chaque message avec une "
                      "ligne écrite pour elle. Passer volume.py avant une campagne : la "
                      "limite observée tourne autour de 100 invitations par semaine, "
                      "invitations en attente comprises. Message en rapport avec le métier "
                      "de la personne, expéditeur identifié, possibilité de dire non (CNIL).",
    },
    {
        "id": "E2-APPAT",
        "titre": "Appât d'engagement",
        "motifs": [
            r"\bcommente\w*\b.{0,15}[«\"']?\s*\w{1,15}\s*[»\"']?.{0,25}\b(pour recevoir|pour avoir|et je t'envoie|je vous envoie|je t'envoie)\b",
            r"\b(like|aime|likez|repost\w*|partage\w*)\b.{0,10}\bsi (tu es|vous etes|t'es)\b.{0,15}\bd'accord\b",
            r"\b(identifie|tague|taguez|mentionne)\b.{0,15}\b(quelqu'un|3|trois|un ami|une personne)\b",
            r"\bcomment (yes|oui|\w+) (below|pour)\b",
            r"\b(ecris|ecrivez|tape|tapez)\b.{0,10}[«\"']\s*\w{1,15}\s*[»\"'].{0,20}\b(en commentaire|en com)\b",
        ],
        "contrainte": "Les Professional Community Policies visent l'engagement artificiel. "
                      "Remplacer par une vraie question que le post a méritée, ou mettre la "
                      "ressource en lien dans le premier commentaire, accessible à tous.",
    },
    {
        "id": "E3-TIERS-ET-CONFIDENTIEL",
        "titre": "Employeur, client, tiers nommé ou sujet réglementé",
        "motifs": [
            r"\b(mon employeur|ma boite|notre client|mon client|nos clients|confidentiel\w*|nda|"
            r"accord de confidentialite|donnees clients?|patients?|sante|conseil financier|"
            r"conseil en investissement|licenciement\w*|plan social|levee de fonds|rachat|resultats financiers)\b",
        ],
        "contrainte": "Vérifier le contrat de travail, l'accord de confidentialité et les "
                      "règles du secteur (santé, finance, AMF). Un client ou une personne "
                      "nommée donne son accord pour ce post précis : un logo sur le site "
                      "n'est pas une autorisation. Dans le doute, décrire la situation sans "
                      "détail qui identifie.",
    },
    {
        "id": "E4-DONNEES-CRM",
        "titre": "Données de contacts LinkedIn stockées ailleurs",
        "motifs": [
            r"\b(crm|hubspot|pipedrive|salesforce|tableur|google sheets?|excel|notion|airtable)\b",
        ],
        "contrainte": "Ne reporter que ce qui sert la relation (nom, poste, source, date, "
                      "prochaine étape). Noter la base légale (intérêt légitime) et "
                      "informer la personne au premier échange utile (RGPD art. 14). "
                      "Supprimer ce qui ne sert plus.",
    },
    {
        "id": "E5-PARTENARIAT",
        "titre": "Contenu sponsorisé ou partenariat rémunéré",
        "motifs": [
            r"\b(sponsoris\w+|partenariat remunere|collaboration commerciale|placement de produit|"
            r"code promo|lien affilie|affiliation|paid partnership)\b",
        ],
        "contrainte": "Signaler le partenariat clairement dans le post (mention "
                      "« Collaboration commerciale » ou l'outil de LinkedIn prévu à cet "
                      "effet) : loi du 9 juin 2023 sur l'influence commerciale.",
    },
]

CONTRAINTES_PERMANENTES = [
    "L'utilisateur est l'auteur : il relit chaque ligne avant de publier.",
    "Rien n'est envoyé ni publié par le pack : il rend du texte à copier.",
    "Aucune affirmation sans preuve : vrai chiffre, fourchette honnête ou constat qualitatif.",
]

EXEMPLE = ("Je veux 20 000 abonnés en six mois. Plan : utiliser Waalaxy pour envoyer "
           "300 invitations par jour, rejoindre un pod pour les 90 premières minutes, "
           "envoyer le même message à tous ceux qui acceptent et inventer deux témoignages "
           "clients pour la page.")


def normaliser(texte: str) -> str:
    """Minuscules sans accents : les motifs restent simples."""
    texte = unicodedata.normalize("NFKD", texte.lower())
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return texte.replace("’", "'")


def _nie(texte: str, debut: int) -> bool:
    avant = texte[max(0, debut - FENETRE_NEGATION):debut]
    # la négation s'arrête à la proposition : « pas d'outil, mais automatise… » n'est pas nié
    avant = re.split(r"[.;!?]|,?\s\b(?:mais|puis|ensuite|par contre|en revanche)\b", avant)[-1]
    return bool(NEGATION.search(avant))


def _scanner(texte: str, regles: list, cle: str) -> list:
    touches = []
    for regle in regles:
        trouves = []
        for motif in regle["motifs"]:
            for m in re.finditer(motif, texte):
                extrait = m.group(0).strip()
                if not extrait or _nie(texte, m.start()):
                    continue
                if extrait not in trouves:
                    trouves.append(extrait)
        if trouves:
            touche = {"id": regle["id"], "titre": regle["titre"], "declencheurs": trouves[:5],
                      cle: regle[cle]}
            if "regle" in regle:
                touche["regle"] = regle["regle"]
            touches.append(touche)
    return touches


def evaluer(texte: str) -> dict:
    norme = normaliser(texte)
    refus = _scanner(norme, REFUS, "alternative")
    encadrements = _scanner(norme, ENCADREMENTS, "contrainte")
    if refus:
        verdict, code = "REFUSÉ", 3
    elif encadrements:
        verdict, code = "ENCADRÉ", 2
    else:
        verdict, code = "AUTORISÉ", 0
    return {
        "verdict": verdict,
        "code": code,
        "refus": refus,
        "encadrements": encadrements,
        "contraintes_permanentes": CONTRAINTES_PERMANENTES,
    }


def afficher(res: dict) -> str:
    lignes = [f"GARDE-FOU : {res['verdict']}", ""]
    for r in res["refus"]:
        lignes += [f"✖ {r['id']} · {r['titre']}",
                   f"  déclenché par : {', '.join(r['declencheurs'])}",
                   f"  règle : {r['regle']}",
                   f"  alternative : {r['alternative']}", ""]
    for e in res["encadrements"]:
        lignes += [f"! {e['id']} · {e['titre']}",
                   f"  déclenché par : {', '.join(e['declencheurs'])}",
                   f"  contrainte : {e['contrainte']}", ""]
    lignes.append("Toujours :")
    lignes += [f"  · {c}" for c in res["contraintes_permanentes"]]
    return "\n".join(lignes)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Classe une demande LinkedIn : AUTORISÉ (0), ENCADRÉ (2) ou REFUSÉ (3).")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--texte", help="la demande ou le plan à vérifier")
    src.add_argument("--fichier", help="fichier texte à vérifier")
    src.add_argument("--exemple", action="store_true", help="lancer sur un exemple")
    p.add_argument("--json", action="store_true", help="sortie JSON")
    a = p.parse_args()

    if a.exemple:
        texte = EXEMPLE
    elif a.fichier:
        try:
            with open(a.fichier, encoding="utf-8") as f:
                texte = f.read()
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

    res = evaluer(texte)
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else afficher(res))
    return res["code"]


if __name__ == "__main__":
    sys.exit(main())
