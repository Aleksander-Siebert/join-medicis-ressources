#!/usr/bin/env python3
"""titre.py : note un titre de profil LinkedIn (headline) sur 100.

Le titre est la seule phrase de LinkedIn qui voyage : elle accompagne chaque
commentaire, chaque résultat de recherche et chaque invitation. La plupart des
titres sont un intitulé de poste, c'est-à-dire la seule chose qu'un lecteur
aurait pu deviner.

Cinq dimensions, 20 points chacune :
  AUDIENCE         nomme-t-il pour qui ?
  RÉSULTAT         dit-il ce qui change pour eux ?
  PREUVE           porte-t-il un signal vérifiable (chiffre, ex-entreprise, titre) ?
  RECHERCHE        contient-il un terme de métier qu'un recruteur ou un client tape ?
  CLARTÉ           lisible, sans mots creux, dans les limites

Limites : 220 caractères (consensus de sources tierces, à vérifier dans le
compteur de l'éditeur) ; les ~60 premiers caractères sont ceux qu'on voit dans
la recherche, les invitations et à côté d'un commentaire (observation).

Codes de sortie :
  0  PRÊT          (75 et plus)
  2  À AFFÛTER     (50 à 74)
  3  À RÉÉCRIRE    (moins de 50, ou bloquant)
  1  erreur d'utilisation

Adapté de headline_scorer.py (alirezarezvani/claude-skills, MIT), réécrit pour
le français. Sans dépendance, sans réseau, déterministe.

Exemples :
  python3 titre.py --titre "Responsable marketing chez Assurly"
  python3 titre.py --titre "…" --titre "…"     (compare plusieurs options)
  python3 titre.py --exemple --json
"""

import argparse
import json
import re
import sys
import unicodedata

LIMITE = 220
AVANT = 60  # caractères visibles dans la recherche et les invitations (observation)

MOTS_CREUX = [
    "passionne", "passionnee", "dynamique", "oriente resultats", "orientee resultats",
    "oriente client", "orientee client", "motive", "motivee", "rigoureux", "rigoureuse",
    "creatif", "creative", "curieux", "curieuse", "touche-a-tout", "couteau suisse",
    "multi-casquettes", "expert reconnu", "experte reconnue", "visionnaire", "ninja",
    "guru", "gourou", "rockstar", "serial entrepreneur", "thought leader",
    "leader d'opinion", "en quete de nouveaux defis", "ouvert aux opportunites",
    "ouverte aux opportunites", "a l'ecoute des opportunites", "polyvalent", "polyvalente",
    "force de proposition", "esprit d'equipe", "proactif", "proactive", "innovant",
    "innovante", "results-driven", "passionate", "team player", "evangeliste",
]

AUDIENCE = [
    "pour les", "pour des", "pour ", "j'aide", "j aide", "nous aidons", "aide les", "aide des",
    "dirigeants", "dirigeant", "fondateurs", "fondatrices", "startups", "start-up", "pme", "eti",
    "tpe", "grands comptes", "daf", "drh", "cmo", "cto", "ceo", "marketeurs", "marketeuses",
    "equipes", "b2b", "b2c", "saas", "e-commerce", "ecommerce", "e-commercants", "assureurs",
    "cabinets", "agences", "independants", "freelances", "artisans", "recruteurs", "commerciaux",
    "avocats", "medecins", "collectivites", "associations", "ecoles", "etudiants", "restaurateurs",
    "industriels", "editeurs", "marques", "retailers", "franchises", "acheteurs", "investisseurs",
    "notaires", "experts-comptables", "therapeutes", "coachs", "createurs", "entrepreneurs",
]

RESULTAT = [
    "reduire", "reduis", "reduit", "augmenter", "augmente", "doubler", "double", "tripler",
    "signer", "signe", "vendre", "vends", "recruter", "recrute", "lancer", "lance",
    "automatiser", "automatise", "migrer", "transformer", "transforme", "convertir", "fideliser",
    "retenir", "gagner", "gagne", "economiser", "accelerer", "accelere", "trouver", "obtenir",
    "obtiennent", "decrocher", "remplir", "generer", "genere", "developper", "structurer",
    "passer de", "sans ", "→", "->", "en moins de", "plus de clients", "clients",
    "rendez-vous", "leads", "chiffre d'affaires", "rentabilite", "croissance", "visibilite",
    "baisser", "baisse", "diminuer", "diviser", "divise", "multiplier", "multiplie", "ameliorer",
    "cout par lead", "cout d'acquisition", "taux de conversion", "ventes", "pipeline", "marge",
    "delai", "delais", "recrutements", "abonnes", "trafic", "conversion", "retention",
]

RECHERCHE = [
    "responsable", "directeur", "directrice", "head of", "chef de projet", "cheffe de projet",
    "consultant", "consultante", "freelance", "fondateur", "fondatrice", "cofondateur",
    "cofondatrice", "dirigeant", "dirigeante", "gerant", "gerante", "cmo", "cto", "ceo", "coo",
    "daf", "drh", "growth", "marketing", "seo", "sea", "sem", "content", "contenu", "acquisition",
    "crm", "data", "product", "produit", "developpeur", "developpeuse", "ingenieur", "ingenieure",
    "commercial", "commerciale", "sales", "business developer", "rh", "recruteur", "recruteuse",
    "talent", "juriste", "avocat", "avocate", "comptable", "coach", "formateur", "formatrice",
    "designer", "ux", "ui", "social media", "community manager", "communication", "brand",
    "marque", "relations presse", "copywriter", "redacteur", "redactrice", "e-commerce",
    "paid", "ads", "analytics", "ia", "ai", "no-code", "automatisation", "hubspot", "salesforce",
    "account manager", "manager", "directeur marketing", "office manager", "customer success", "product manager", "product owner", "pmo", "achats",
    "supply chain", "finance", "controleur de gestion", "levee de fonds",
]

EXEMPLE_FORT = ("Responsable acquisition chez Assurly | J'aide les assureurs en ligne à "
                "réduire leur coût par lead | −44% de coût par lead en 4 mois | ex-agence conseil")
EXEMPLE_FAIBLE = "Marketing Manager passionnée | Dynamique et orientée résultats 🚀🔥"


def norme(texte: str) -> str:
    t = unicodedata.normalize("NFKD", texte.lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'")


def _trouve(t: str, liste: list) -> list:
    vus = []
    for mot in liste:
        motif = re.escape(mot)
        if mot[0].isalnum():
            motif = rf"(?<![\w-]){motif}"
        if mot[-1].isalnum():
            motif = rf"{motif}(?![\w])"
        if re.search(motif, t) and mot.strip() not in vus:
            vus.append(mot.strip())
    return vus


def pseudo_gras(texte: str) -> bool:
    """Caractères du bloc Mathematical Alphanumeric Symbols (U+1D400–U+1D7FF)."""
    return any(0x1D400 <= ord(c) <= 0x1D7FF for c in texte)


def preuves(texte: str) -> list:
    signaux = []
    t = norme(texte)
    if re.search(r"\d+\s*(%|x\b|×)|[x×]\s?\d", t):
        signaux.append("pourcentage ou multiple")
    if re.search(r"\d\s?(k€|m€|€|k\b|m\b|millions?|milliards?)|€\s?\d", t):
        signaux.append("montant ou ordre de grandeur")
    if re.search(r"(^|[\s|·(])ex-?\s?[a-z0-9]", t):
        signaux.append("ancienne entreprise (ex-)")
    if re.search(r"\b\d[\d\s.]*\s*(clients?|projets?|entreprises|marques|startups|pme|eleves|"
                 r"personnes|abonnes|lecteurs|utilisateurs|missions|recrutements|ans|appels|resilies|leads|"
                 r"commandes|dossiers|contrats|devis|candidats|salaries|collaborateurs|equipes|pays|magasins)\b", t):
        signaux.append("volume")
    if re.search(r"\b(?:de|from)\s+\d[\d\s,.]*\s*(?:a|à|to)\s+\d[\d\s,.]*\s*(?:jours?|semaines?|mois|heures?|h|min|minutes?|ans?)?\b|"
                 r"\b\d+\s*(?:jours?|semaines?|mois|heures?|h|min|minutes?)\b.{0,15}\b(?:au lieu de|contre)\b|"
                 r"\b(?:divise|multiplie|double|triple)e?s?\s+par\s+\d|\b(?:divise|double|triple)", t):
        signaux.append("avant et après")
    if re.search(r"\b(auteur|autrice|conferencier|conferenciere|laureat|laureate|prix|"
                 r"certifie|certifiee|expert-comptable|docteur|phd|mba|google partner|"
                 r"top voice|podcast|chroniqueur|chroniqueuse|enseignant|enseignante)\b", t):
        signaux.append("preuve tierce")
    return signaux


def noter(texte: str) -> dict:
    brut = " ".join(texte.split())
    t = norme(brut)
    constats, dims = [], {}

    aud = _trouve(t, AUDIENCE)
    dims["audience"] = 20 if len(aud) >= 2 else (12 if aud else 0)
    if not aud:
        constats.append(("bloquant", "audience", "Aucune audience nommée : le lecteur ne sait pas si c'est pour lui.",
                         "Nomme le groupe en mots simples : « pour les assureurs en ligne », « pour les PME industrielles »."))

    res = _trouve(t, RESULTAT)
    dims["resultat"] = 20 if len(res) >= 2 else (12 if res else 0)
    if not res:
        constats.append(("bloquant", "résultat", "Un rôle, pas un résultat. Les intitulés sont interchangeables, les résultats non.",
                         "Ajoute ce qui change grâce à toi : « réduire le coût par lead », « signer plus vite »."))

    pr = preuves(brut)
    dims["preuve"] = 20 if len(pr) >= 2 else (12 if pr else 0)
    if not pr:
        constats.append(("majeur", "preuve", "Aucun signal vérifiable : tout est auto-déclaré.",
                         "Un chiffre, une ancienne entreprise ou un titre. Vrai, ou rien (voir reserve.md)."))

    rech = _trouve(t, RECHERCHE)
    dims["recherche"] = 20 if len(rech) >= 3 else (13 if len(rech) == 2 else (7 if rech else 0))
    if len(rech) < 2:
        constats.append(("majeur", "recherche", f"{len(rech)} terme(s) de métier reconnaissable(s). La recherche LinkedIn lit le titre ; un intitulé inventé ne remonte pas.",
                         "Garde au moins un intitulé ou une compétence que les gens tapent vraiment, à côté de la formule personnelle."))

    clarte = 20
    creux = _trouve(t, MOTS_CREUX)
    if creux:
        clarte -= min(10, 4 * len(creux))
        constats.append(("majeur", "clarté", "Mots creux : " + ", ".join(creux) + ". Ils décrivent une attitude, pas une compétence.",
                         "Supprime-les. La place gagnée paie un vrai chiffre ou une vraie audience."))
    seps = brut.count("|") + brut.count("•") + brut.count("·")
    if seps > 3:
        clarte -= 5
        constats.append(("mineur", "clarté", f"{seps} séparateurs : au-delà de trois, ça se lit comme une liste de mots-clés.",
                         "Trois segments : pour qui / ce qui change / une preuve."))
    emojis = len(re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", brut))
    if emojis > 1:
        clarte -= 4
        constats.append(("mineur", "clarté", f"{emojis} émojis : ils prennent la place de mots qui portent du sens.",
                         "Un au plus, et seulement comme séparateur."))
    majuscules = [m for m in brut.split() if len(m) > 3 and m.isupper() and m.isalpha()
                  and norme(m) not in {"saas", "ceo", "cmo", "cto", "daf", "drh", "b2b"}]
    if len(majuscules) > 1:
        clarte -= 3
        constats.append(("mineur", "clarté", "Plusieurs mots en capitales : ça crie et ça se lit mal.",
                         "Casse normale. L'insistance vient de la précision."))
    if re.match(r"^\s*j'?\s?aide (les|des)\b", t):
        constats.append(("mineur", "clarté", "Ouverture « J'aide les… » : la formule est devenue très courante.",
                         "Possible, mais essaie aussi une version qui commence par le métier ou par la preuve."))
    if re.search(r"\b(open to work|en recherche d'emploi|a l'ecoute du marche)\b", t):
        constats.append(("mineur", "clarté", "La recherche d'emploi dans le titre prend la place d'une preuve.",
                         "Utilise le badge « Open to work » et mets dans le titre le poste visé."))
    dims["clarte"] = max(0, clarte)

    if pseudo_gras(brut):
        constats.append(("bloquant", "accessibilité", "Pseudo-gras ou pseudo-italique Unicode : illisible pour les lecteurs d'écran, introuvable par la recherche.",
                         "Texte normal. La mise en valeur vient de l'ordre des mots."))

    longueur = len(brut)
    depasse = max(0, longueur - LIMITE)
    if depasse:
        constats.append(("bloquant", "longueur", f"{longueur} caractères, {depasse} de trop : LinkedIn refusera.",
                         f"Coupe {depasse} caractères, en commençant par le segment qui porte le moins de preuve."))
    elif longueur < 70:
        constats.append(("mineur", "longueur", f"{longueur} caractères sur {LIMITE} : l'espace n'est pas utilisé.",
                         "Ajoute l'audience ou la preuve qui manque."))
    debut = brut[:AVANT]
    td = norme(debut)
    if not (preuves(debut) or _trouve(td, AUDIENCE) or _trouve(td, RECHERCHE)):
        constats.append(("majeur", "début", f"Les {AVANT} premiers caractères (ceux qu'on voit dans la recherche et les invitations) ne portent ni métier, ni audience, ni preuve : « {debut} »",
                         "Mets le segment le plus fort en premier. Le reste est un bonus."))

    total = sum(dims.values())
    bloquant = any(c[0] == "bloquant" for c in constats)
    if depasse or pseudo_gras(brut):
        total = min(total, 49)
    verdict, code = (("PRÊT", 0) if total >= 75 and not bloquant else
                     ("À AFFÛTER", 2) if total >= 50 and not (depasse or pseudo_gras(brut)) else
                     ("À RÉÉCRIRE", 3))
    ordre = {"bloquant": 0, "majeur": 1, "mineur": 2}
    return {
        "titre": brut,
        "note": total,
        "verdict": verdict,
        "code": code,
        "dimensions": dims,
        "longueur": {"caracteres": longueur, "limite": LIMITE, "depasse": depasse, "debut_visible": debut},
        "signaux": {"audience": aud, "resultat": res, "preuve": pr, "recherche": rech},
        "constats": [{"gravite": g, "dimension": d, "constat": c, "correction": f}
                     for g, d, c, f in sorted(constats, key=lambda x: ordre[x[0]])],
    }


def afficher(r: dict) -> str:
    L = [f"TITRE  {r['note']}/100  {r['verdict']}",
         f"« {r['titre']} »",
         f"{r['longueur']['caracteres']}/{r['longueur']['limite']} caractères"
         + (f"  ({r['longueur']['depasse']} DE TROP)" if r["longueur"]["depasse"] else ""),
         f"Visible dans la recherche : « {r['longueur']['debut_visible']} »", ""]
    noms = {"audience": "audience", "resultat": "résultat", "preuve": "preuve",
            "recherche": "recherche", "clarte": "clarté"}
    for k, v in r["dimensions"].items():
        L.append(f"  {noms[k]:<10} {v:>2}/20  [{'#' * (v // 2)}{'.' * (10 - v // 2)}]")
    if r["constats"]:
        L.append("")
        for c in r["constats"]:
            L.append(f"  [{c['gravite'].upper()}] {c['dimension']} : {c['constat']}")
            L.append(f"      → {c['correction']}")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser(description="Note un titre LinkedIn sur 100 (PRÊT 0 / À AFFÛTER 2 / À RÉÉCRIRE 3).")
    p.add_argument("--titre", action="append", help="titre à noter (répétable pour comparer)")
    p.add_argument("--fichier", help="un titre par ligne")
    p.add_argument("--exemple", action="store_true", help="noter deux exemples (fort et faible)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    titres = []
    if a.exemple:
        titres = [EXEMPLE_FORT, EXEMPLE_FAIBLE]
    if a.titre:
        titres += a.titre
    if a.fichier:
        try:
            with open(a.fichier, encoding="utf-8") as f:
                titres += [l.strip() for l in f if l.strip()]
        except OSError as err:
            print(f"Erreur : {err}", file=sys.stderr)
            return 1
    if not titres:
        p.print_help(sys.stderr)
        return 1

    resultats = [noter(t) for t in titres]
    if a.json:
        print(json.dumps(resultats if len(resultats) > 1 else resultats[0], ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(afficher(r) for r in resultats))
        if len(resultats) > 1:
            meilleur = max(resultats, key=lambda r: r["note"])
            print(f"\nMeilleure note : {meilleur['note']}/100 · « {meilleur['titre']} »")
    return max(r["code"] for r in resultats) if len(resultats) == 1 else min(r["code"] for r in resultats)


if __name__ == "__main__":
    sys.exit(main())
