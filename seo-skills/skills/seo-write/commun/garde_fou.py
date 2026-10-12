#!/usr/bin/env python3
"""garde_fou.py : refuse les tactiques SEO qui mettent le site en danger.

Chaque Skill du pack SEO passe une demande « à risque » (volume de pages,
liens, avis, auteurs, texte d'un concurrent, manière de tromper un moteur)
par ce script avant de rédiger. Il la classe selon les politiques anti-spam
de Google Search (mise à jour du 28 août 2026), le guide « contenu utile »
et le droit français de la consommation, puis rend un verdict :

  AUTORISÉ  (code 0) : rien ne bloque, continuer.
  ENCADRÉ   (code 2) : continuer, en appliquant les contraintes affichées.
  REFUSÉ    (code 3) : ne pas rédiger la tactique ; proposer l'alternative.
  (code 1 : erreur d'utilisation)

Un refus nomme toujours la règle et donne une alternative. Déterministe,
sans dépendance, sans réseau.

Exemples :
  python3 garde_fou.py --texte "réécris l'article du concurrent pour qu'il ne soit pas détecté"
  python3 garde_fou.py --fichier plan.md --json
  python3 garde_fou.py --exemple
"""

import argparse
import json
import re
import sys
import unicodedata

NEGATION = re.compile(
    r"\b(sans|pas d[e']|pas un|pas une|pas les?|aucun|aucune|jamais|ni|"
    r"no|not|never|without|interdit|interdits|eviter|evite|refuse|"
    r"ne (?:veux|veut|voulons|souhaite|souhaitons) pas|pas question)\b"
)
FENETRE_NEGATION = 25

SPAM = "Politiques anti-spam de Google Search (developers.google.com/search/docs/essentials/spam-policies, maj 28 août 2026)"

REFUS = [
    {
        "id": "R1-CONTENU-COPIE",
        "titre": "Texte d'un autre site recopié, reformulé ou « spinné »",
        "regle": SPAM + " : scraping (reprise de contenu d'autres sites pour manipuler le "
                 "classement) ; droit d'auteur (Code de la propriété intellectuelle).",
        "motifs": [
            r"\b(reecri\w*|reformul\w*|paraphras\w*|spinn\w*|spin|rewrite|copi\w*|recopi\w*|reprend\w*|plagi\w*)\b"
            r".{0,50}\b(articles?|textes?|contenus?|pages?|sites?|blogs?)\b.{0,40}\b(concurrent\w*|d'un autre|des autres|"
            r"d'autres sites?|qui ranke|en tete|premier resultat|wikipedia)\b",
            r"\b(concurrent\w*)\b.{0,40}\b(reecri\w*|reformul\w*|copier|recopi\w*|spinn\w*|plagi\w*)\b",
            r"\bcontent spinn\w*|\bspinner\b|\barticle spinn\w*",
            r"\b(indetectable|non detectable|ne (?:soit|sera) pas detect\w*|passer (?:sous|inapercu)|eviter le plagiat|anti[- ]?plagiat)\b",
        ],
        "alternative": "Tirer de ces pages des sujets, des manques et des questions "
                       "(/seo-serp), puis écrire avec ce que le site sait et a vécu "
                       "(/seo-brief, /seo-write). Citer la source quand on reprend un fait.",
    },
    {
        "id": "R2-FAUSSE-PREUVE",
        "titre": "Faux avis, faux témoignages, faux auteur ou faux diplôme",
        "regle": "Code de la consommation (pratiques commerciales trompeuses, art. L. 121-2 et "
                 "L. 121-4 [à vérifier]) ; guide Google « contenu utile » (Qui a écrit) ; "
                 "règles Google sur les avis.",
        "motifs": [
            r"\b(faux|fausses?|fake|invent\w*|fictifs?|fictives?)\b.{0,25}\b(avis|temoignages?|reviews?|"
            r"etudes? de cas|cas clients?|clients?|auteurs?|experts?|medecins?|avocats?|diplomes?|"
            r"certifications?|labels?|notes?|etoiles|citations?)\b",
            r"\b(invente[rz]?|imagine[rz]?|fabrique[rz]?|creer?)\b.{0,30}\b(un |une |des )?(temoignages?|avis clients?|"
            r"auteur expert|bio d'expert|persona d'auteur|statistiques?|chiffres?|etudes?)\b",
            r"\b(achet\w*|achat|pay\w*)\b.{0,20}\b(avis|reviews?|etoiles|notes)\b",
            r"\b(avis|temoignages?|reviews?|etudes? de cas|cas clients?|auteurs?|experts?|citations?|statistiques?|chiffres?)\b"
            r".{0,20}\b(invente\w*|fictifs?|fictives?|faux|fausses?|bidons?)\b",
            r"\b(signer|signature|byline)\b.{0,40}\b(medecin|docteur|avocat|expert)\b.{0,30}\b(qui n'a pas|sans qu'il|fictif|invente)\b",
        ],
        "alternative": "Utiliser de vrais avis (avec leur date et leur source), de vrais cas "
                       "tirés de reserve.md, un auteur réel qui relit. Sans preuve : "
                       "{{à compléter}} ou une formulation qui n'affirme rien.",
    },
    {
        "id": "R3-TROMPER-LE-MOTEUR",
        "titre": "Texte caché, bourrage, cloaking, redirections trompeuses",
        "regle": SPAM + " : texte et liens cachés, bourrage de mots-clés, cloaking, "
                 "redirections trompeuses, détournement du bouton retour (pratiques malveillantes).",
        "motifs": [
            r"\b(texte|mots?[- ]cles?|liens?)\b.{0,20}\b(caches?|invisibles?|en blanc|blanc sur blanc|"
            r"hors ecran|display ?: ?none|font-size ?: ?0)\b",
            r"\bcloaking\b|\bcloak\w*",
            r"\b(bourr\w+|stuffing|stuff)\b.{0,20}\b(mots?[- ]cles?|keywords?)\b",
            r"\b(repeter|mettre|placer)\b.{0,30}\b(mot[- ]cle)\b.{0,30}\b(le plus (?:de fois )?possible|partout|"
            r"\d{2,} fois|un maximum)\b",
            r"\b(montrer|servir|afficher)\b.{0,30}\b(autre chose|un autre contenu|contenu different)\b.{0,30}\b(google|googlebot|robots?|moteurs?)\b",
            r"\b(bloquer|desactiver|detourner|pieger)\b.{0,20}\b(bouton )?retour\b",
            r"\bredirections? (trompeuses?|sournoises?|cachees?)\b",
        ],
        "alternative": "Écrire pour le lecteur : le mot-clé là où il aide (title, H1, première "
                       "phrase), le même contenu pour Google et pour les visiteurs.",
    },
    {
        "id": "R4-LIENS-ARTIFICIELS",
        "titre": "Achat, échange ou réseau de liens pour le classement",
        "regle": SPAM + " : spam de liens (achat ou vente de liens qui transmettent du "
                 "classement, échanges excessifs, réseaux de sites).",
        "motifs": [
            r"\b(achet\w*|achat|vend\w*|pay\w*|lou\w*)\b.{0,25}\b(liens?|backlinks?|articles? sponsoris\w+ dofollow)\b",
            r"\b(echang\w+|swap)\b.{0,20}\b(liens?|backlinks?)\b",
            r"\b(pbn|private blog network|reseau de (?:sites|blogs)|ferme de liens|link farm)\b",
            r"\b(microsites?|sites? satellites?|mini[- ]sites?)\b.{0,50}\b(lien|liens|renvoi\w*|pointer|vers le site|ia)\b",
            r"\b(domaines? expires?|expired domains?)\b.{0,40}\b(rediriger|lien|liens|recuperer le jus|autorite)\b",
        ],
        "alternative": "Gagner des liens et des mentions : données propres, outils utiles, "
                       "relations presse, partenaires réels (/seo-plan, option preuve sociale). "
                       "Un lien payé porte rel=\"sponsored\".",
    },
    {
        "id": "R5-PAGES-EN-MASSE",
        "titre": "Pages générées en masse ou satellites, sans valeur propre",
        "regle": SPAM + " : contenu à grande échelle pour manipuler le classement, pages "
                 "satellites (doorway).",
        "motifs": [
            r"\b(generer|creer|publier|produire|sortir)\b.{0,25}\b(\d{3,}|des centaines|des milliers|plusieurs centaines|"
            r"une page par ville|une page par commune)\b.{0,40}\b(pages?|articles?|contenus?|textes?)\b"
            r".{0,60}\b(sans (?:relecture|relire|verifier|valeur)|automatiquement|a la chaine|pour ranker|pour se positionner|"
            r"juste (?:changer|remplacer) (?:le nom de )?la ville)\b",
            r"\b(chang\w*|remplac\w*)\b.{0,15}\b(seulement |juste |uniquement )?(le nom de la ville|la ville|le nom de ville)\b",
            r"\bpages? satellites?\b|\bdoorway\b",
        ],
        "alternative": "Une page par vraie différence (lieu servi, offre, données propres), "
                       "par lots relus. Les portes de qualité sont dans /seo-plan (option "
                       "pages à grande échelle).",
    },
    {
        "id": "R6-FAUSSE-FRAICHEUR",
        "titre": "Date de mise à jour changée sans changement réel",
        "regle": "Guide Google « Créer des contenus utiles » : changer la date sans "
                 "changement significatif est un signal de contenu écrit pour les moteurs.",
        "motifs": [
            r"\b(chang\w*|modifi\w*|mettre a jour|actualis\w*|rafraich\w*)\b.{0,15}\b(la )?date\b.{0,40}"
            r"\b(sans (?:rien )?(?:changer|modifier|toucher)|pour (?:faire|paraitre) (?:recent|frais|a jour))\b",
            r"\b(faire croire|faire semblant)\b.{0,30}\b(a jour|recent|mis a jour)\b",
        ],
        "alternative": "Mettre à jour vraiment (/seo-refresh) : chiffres, sections, liens. La "
                       "date change ensuite, et elle dit ce qui a changé.",
    },
]

ENCADREMENTS = [
    {
        "id": "E1-GRANDE-ECHELLE",
        "titre": "Pages ou articles produits à grande échelle",
        "motifs": [
            r"\b(\d{2,}|des dizaines|des centaines|plusieurs dizaines)\b.{0,15}\b(pages?|articles?|fiches?)\b",
            r"\b(programmati\w+|generation automatique|en masse|a grande echelle|par lots?)\b",
        ],
        "contrainte": "Chaque page doit pouvoir être publiée seule (test « publiable seule ? »), "
                      "avec des données propres. Publication par lots relus, suivi de "
                      "l'indexation avant d'étendre.",
    },
    {
        "id": "E2-AVIS-CLIENTS",
        "titre": "Demande ou affichage d'avis clients",
        "motifs": [r"\b(avis|reviews?|temoignages?|notes? clients?|etoiles)\b"],
        "contrainte": "Demander un avis à tous les clients, sans filtrage préalable ni "
                      "contrepartie. Afficher la date de l'avis et l'existence ou non d'une "
                      "vérification (art. L. 111-7-2 et D. 111-17 du Code de la consommation "
                      "[à vérifier]). Un témoignage nommé demande l'accord de la personne.",
    },
    {
        "id": "E3-COMPARATIF",
        "titre": "Page comparative ou « alternative à »",
        "motifs": [
            r"\b(comparatifs?|comparaisons?|versus|vs|alternatives? a|meilleur que|mieux que)\b",
            r"\bpublicite comparative\b",
        ],
        "contrainte": "Comparer des offres qui répondent au même besoin, sur des "
                      "caractéristiques vérifiables, datées (« au 12 oct. 2026 »), avec la "
                      "source de chaque donnée concurrente. « Non trouvé sur leur site » n'est "
                      "pas « n'existe pas ». Cadre : art. L. 122-1 et suivants du Code de la "
                      "consommation [à vérifier].",
    },
    {
        "id": "E4-YMYL",
        "titre": "Sujet YMYL (santé, argent, assurance, droit, sécurité)",
        "motifs": [
            r"\b(sante|medical|medicament|maladie|symptome|traitement|assurance|mutuelle|prevoyance|"
            r"credit|pret|placement|investissement|impots?|fiscal\w*|retraite|juridique|droit|avocat|"
            r"contrat|garanties?|remboursement|securite|grossesse|enfants?)\b",
        ],
        "contrainte": "Chaque chiffre, délai, plafond ou condition a une source nommée ou "
                      "sort en {{à compléter}}. Auteur réel et identifiable. Pas de promesse "
                      "(« garanti », « 100% remboursé ») sans le contrat qui la prouve. "
                      "Passer affirmations.py en mode --ymyl.",
    },
    {
        "id": "E5-IA",
        "titre": "Contenu écrit avec l'IA",
        "motifs": [r"\b(ia|intelligence artificielle|chatgpt|claude|genere par|generation de contenu|llm)\b"],
        "contrainte": "Un humain relit et signe. Dire comment le contenu a été produit là où "
                      "le lecteur peut se le demander (guide Google, « Comment »). L'IA ne "
                      "fournit aucun fait non vérifié.",
    },
    {
        "id": "E6-PARTENARIAT",
        "titre": "Contenu sponsorisé, affiliation ou lien payé",
        "motifs": [r"\b(sponsoris\w+|affili\w+|lien paye|article paye|partenariat remunere|code promo)\b"],
        "contrainte": "Lien en rel=\"sponsored\" ; partenariat signalé clairement au lecteur "
                      "(loi du 9 juin 2023 sur l'influence commerciale pour les contenus "
                      "d'influence [à vérifier selon le support]).",
    },
]

CONTRAINTES_PERMANENTES = [
    "Le contenu est écrit d'abord pour un lecteur réel du site.",
    "Rien n'est publié ni modifié par le pack : il rend du texte et des listes à faire.",
    "Aucun fait sans source : vrai chiffre sourcé, formulation prudente ou {{à compléter}}.",
]

EXEMPLE = ("Je veux ranker vite : réécris les 3 premiers articles du concurrent pour que ce ne soit "
           "pas détecté, ajoute deux témoignages clients inventés, crée 300 pages en changeant juste "
           "la ville et achète quelques backlinks.")


def normaliser(texte: str) -> str:
    texte = unicodedata.normalize("NFKD", texte.lower())
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return texte.replace("’", "'")


def _nie(texte: str, debut: int) -> bool:
    avant = texte[max(0, debut - FENETRE_NEGATION):debut]
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
            touche = {"id": regle["id"], "titre": regle["titre"], "declencheurs": trouves[:5], cle: regle[cle]}
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
    return {"verdict": verdict, "code": code, "refus": refus, "encadrements": encadrements,
            "contraintes_permanentes": CONTRAINTES_PERMANENTES}


def afficher(res: dict) -> str:
    lignes = [f"GARDE-FOU : {res['verdict']}", ""]
    for r in res["refus"]:
        lignes += [f"✖ {r['id']} · {r['titre']}", f"  déclenché par : {', '.join(r['declencheurs'])}",
                   f"  règle : {r['regle']}", f"  alternative : {r['alternative']}", ""]
    for e in res["encadrements"]:
        lignes += [f"! {e['id']} · {e['titre']}", f"  déclenché par : {', '.join(e['declencheurs'])}",
                   f"  contrainte : {e['contrainte']}", ""]
    lignes.append("Toujours :")
    lignes += [f"  · {c}" for c in res["contraintes_permanentes"]]
    return "\n".join(lignes)


def main() -> int:
    p = argparse.ArgumentParser(description="Classe une demande SEO : AUTORISÉ (0), ENCADRÉ (2) ou REFUSÉ (3).")
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
