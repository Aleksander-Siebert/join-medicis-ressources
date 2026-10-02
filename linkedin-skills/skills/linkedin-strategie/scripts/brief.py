#!/usr/bin/env python3
"""brief.py : vérifie un brief de positionnement LinkedIn avant de planifier quoi que ce soit.

Un plan sans objectif, sans audience précise ni exclusions produit un fil de
remarques sans lien, abandonné la 5e semaine. Ce script refuse ce qui rend la
suite impossible et rend des critères à 90 jours vérifiables par un tiers.

Entrée JSON :
  {
    "objectif": "clients" | "emploi" | "reconversion" | "autorite" | "recrutement" | "levee" | "communaute",
    "objectif_90_jours": "6 rendez-vous qualifiés avec des DAF de PME industrielles",
    "audience": "DAF de PME industrielles de 50 à 250 salariés qui changent d'ERP cette année",
    "probleme": "…", "angle": "…",
    "exclusions": ["…", "…"],
    "piliers": [{"nom": "…", "part": 40, "pourquoi_moi": "…", "preuve": "…", "etape": "education"}, …],
    "minutes_semaine": 240
  }

Refus (code 3) : objectif hors liste ; objectif à 90 jours mesuré en abonnés,
vues ou likes ; audience trop large pour exclure quelqu'un ; moins de 2
exclusions ; piliers hors 2-4 ou parts dont la somme n'est pas 100.
À reprendre (code 2) : aucun pilier avec une preuve existante ; aucun pilier
expérimental (10 à 20%) ; un pilier au-delà de 60% ; conversion au-delà de
20% ; pilier sans « pourquoi moi » ; exclusions de façade ; moins de 90 min.
Valide (code 0) sinon. Code 1 : erreur d'utilisation.

Adapté de positioning_brief.py (alirezarezvani/claude-skills, MIT), avec la
grille de niche de Taplio (MIT) et l'entonnoir de Marian Kamenistak (MIT).
Sans dépendance, sans réseau.
"""

import argparse
import json
import re
import sys
import unicodedata

OBJECTIFS = {
    "clients": ["{n} conversations entrantes de {audience}, dont au moins une qui cite un post précis",
                "{n} rendez-vous qualifiés obtenus après un échange sur LinkedIn",
                "une personne de la cible sait dire en une phrase ce que tu fais (test de la phrase)"],
    "emploi": ["{n} échanges avec des recruteurs ou des managers du métier visé",
               "{n} candidatures appuyées par une personne rencontrée sur LinkedIn",
               "le titre et la Sélection reprennent les mots de 5 offres visées"],
    "reconversion": ["{n} échanges avec des praticiens du métier visé",
                     "{n} preuves publiques du nouveau métier (projet, post, étude) visibles sur le profil",
                     "une personne du métier visé te recommande ou te présente"],
    "autorite": ["{n} invitations (podcast, conférence, article invité, panel)",
                 "{n} reprises ou citations d'un de tes posts par des pairs",
                 "test de la phrase : une idée que les gens associent à ton nom"],
    "recrutement": ["{n} candidatures qui citent un post ou la page",
                    "{n} candidats de la cible contactés qui répondent",
                    "les salariés reprennent les formulations de la page dans leur profil"],
    "levee": ["{n} conversations avec des investisseurs du secteur",
              "une thèse publique datée, reprise par au moins un investisseur",
              "le profil du fondateur et la page racontent la même histoire"],
    "communaute": ["{n} personnes qui reviennent commenter au moins 3 fois",
                   "{n} échanges entre membres sans toi",
                   "un format récurrent que des gens attendent (série numérotée)"],
}
VANITE = re.compile(r"\b(abonnes|abonnees|followers?|vues|impressions|likes?|reactions|portee|viral)\b")
AUDIENCE_LARGE = [
    "tout le monde", "les entreprises", "les professionnels", "les entrepreneurs", "les dirigeants",
    "les pme", "les marketeurs", "les decideurs", "les business leaders", "les managers",
    "les independants", "les freelances", "les startups", "les gens", "toute personne",
]
QUALIFICATIF = re.compile(
    r"\d|\b(de|du|des|en|qui|dont|chez|dans|sur|pour|b2b|b2c|saas|industriel\w*|secteur|taille|"
    r"salaries|ca|arr|stade|serie [a-c]|levee|cette annee|ce trimestre)\b")
EXCLUSIONS_FACADE = ["la politique", "politique", "la negativite", "negativite", "le negatif", "les polemiques",
                     "polemiques", "la religion"]
ETAPES = {"notoriete", "education", "conversion"}


def norme(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'").strip()


def verifier(b):
    refus, reprendre, notes = [], [], []

    obj = norme(b.get("objectif"))
    if obj not in OBJECTIFS:
        refus.append(f"Objectif « {b.get('objectif')} » : choisis-en UN parmi {', '.join(OBJECTIFS)}. "
                     "Deux objectifs servent mal deux audiences qui se recoupent moins qu'on ne croit.")

    o90 = norme(b.get("objectif_90_jours"))
    if not o90:
        refus.append("Pas d'objectif à 90 jours. Que doit-il s'être passé dans 90 jours pour que ça ait valu le coup ?")
    elif VANITE.search(o90) and not re.search(r"\b(conversation|rendez-vous|rdv|client|candidat|offre|entretien|invitation|recrut)", o90):
        refus.append("L'objectif à 90 jours se mesure en abonnés, vues ou likes. Ce chiffre bouge pour des raisons "
                     "sans rapport avec l'objectif : choisis un résultat qu'un tiers peut vérifier.")
    elif not re.search(r"\d", o90):
        reprendre.append("L'objectif à 90 jours n'a pas de nombre : combien de conversations, de rendez-vous, d'invitations ?")

    aud = norme(b.get("audience"))
    mots = re.findall(r"[a-z0-9']+", aud)
    if not aud:
        refus.append("Pas d'audience.")
    elif aud in AUDIENCE_LARGE or len(mots) < 4 or not QUALIFICATIF.search(aud.split(" ", 2)[-1] if len(mots) > 2 else ""):
        refus.append(f"Audience « {b.get('audience')} » trop large : elle n'exclut personne. "
                     "Précise le rôle, la taille ou le stade de l'entreprise, et le problème qu'ils ont ce trimestre.")

    exc = [e for e in (b.get("exclusions") or []) if norme(e)]
    if len(exc) < 2:
        refus.append("Moins de 2 exclusions. Un positionnement qui n'exclut rien est une disponibilité. "
                     "Nomme 2 sujets dont tu ne parleras pas, dont le sujet tendance sur lequel tu n'as aucun avantage.")
    facade = [e for e in exc if norme(e) in EXCLUSIONS_FACADE]
    if facade:
        reprendre.append(f"Exclusions de façade : {', '.join(facade)}. Personne n'allait en parler. "
                         "Choisis une exclusion qui te coûte (un sujet qui marcherait mais qui t'éloigne de ta cible).")

    piliers = b.get("piliers") or []
    if not 2 <= len(piliers) <= 4:
        refus.append(f"{len(piliers)} pilier(s) : il en faut 2 à 4. En dessous c'est un monologue, au-delà un magazine auquel personne ne s'est abonné.")
    else:
        total = sum(p.get("part", 0) for p in piliers)
        if total != 100:
            refus.append(f"Les parts des piliers font {total}%, pas 100% : sans budget, ce sont des préférences.")
        if not any(norme(p.get("preuve")) for p in piliers):
            reprendre.append("Aucun pilier ne s'appuie sur une preuve qui existe déjà. Le premier pilier parlera du "
                             "processus, pas des résultats (sinon il faudrait inventer des preuves).")
        if not any(10 <= p.get("part", 0) <= 20 for p in piliers):
            reprendre.append("Aucun pilier expérimental (10 à 20%) : le pilier principal du trimestre prochain vient de là.")
        trop = [p["nom"] for p in piliers if p.get("part", 0) > 60]
        if trop:
            reprendre.append(f"Pilier au-delà de 60% : {', '.join(trop)}. Le fil devient monocorde.")
        sans = [p.get("nom", "?") for p in piliers if not norme(p.get("pourquoi_moi"))]
        if sans:
            reprendre.append(f"Pilier sans « pourquoi moi » : {', '.join(sans)}. Si n'importe qui peut en parler, coupe-le.")
        conv = sum(p.get("part", 0) for p in piliers if norme(p.get("etape")) == "conversion")
        if conv > 20:
            reprendre.append(f"Conversion à {conv}% : au-delà d'un post sur cinq, la confiance s'use.")
        if not any(norme(p.get("etape")) in ETAPES for p in piliers):
            notes.append("Aucune étape (notoriété, éducation, conversion) indiquée : l'équilibre de l'entonnoir n'est pas vérifiable.")

    minutes = b.get("minutes_semaine")
    if minutes is not None and minutes < 90:
        reprendre.append(f"{minutes} min par semaine : sous 90, le plan démarre par des semaines « commentaires seulement » (budget.py).")

    criteres = []
    if obj in OBJECTIFS:
        criteres = [c.replace("{audience}", b.get("audience") or "la cible").replace("{n}", "{{n}}") for c in OBJECTIFS[obj]]

    phrase = None
    if b.get("audience") and b.get("probleme") and b.get("angle"):
        aud = b["audience"].strip()
        if not re.match(r"(?i)(les|des|l'|la|le|mes|nos|ces)\b", aud):
            aud = "les " + aud
        phrase = f"J'aide {aud} à {b['probleme'].strip()} grâce à {b['angle'].strip()}."
        for faux, juste in ((" à les ", " aux "), (" à le ", " au "), ("grâce à les ", "grâce aux "), ("grâce à le ", "grâce au ")):
            phrase = phrase.replace(faux, juste)

    verdict, code = (("REFUSÉ", 3) if refus else ("À REPRENDRE", 2) if reprendre else ("VALIDE", 0))
    return {"verdict": verdict, "code": code, "refus": refus, "a_reprendre": reprendre, "notes": notes,
            "criteres_90_jours": criteres, "phrase_de_positionnement": phrase}


EXEMPLE = {
    "objectif": "clients",
    "objectif_90_jours": "6 rendez-vous qualifiés avec des responsables marketing d'assureurs ou de courtiers en ligne",
    "audience": "responsables marketing d'assureurs et de courtiers en ligne de 50 à 300 salariés dont le coût par lead monte",
    "probleme": "faire baisser leur coût par lead sans augmenter le budget",
    "angle": "les appels clients avant les campagnes",
    "exclusions": ["l'actualité de l'IA générale, sur laquelle je n'ai aucun avantage", "les comparatifs d'assureurs nommés (confidentialité)"],
    "piliers": [
        {"nom": "Acquisition en assurance, chiffres à l'appui", "part": 45, "pourquoi_moi": "3 ans à la tête de l'acquisition d'Assurly",
         "preuve": "coût par lead de 41 € à 23 € en 4 mois", "etape": "education"},
        {"nom": "Ce que disent les clients qui partent", "part": 25, "pourquoi_moi": "60 appels de résiliation écoutés",
         "preuve": "", "etape": "notoriete"},
        {"nom": "Coulisses de l'activité de conseil", "part": 15, "pourquoi_moi": "je la lance", "preuve": "", "etape": "notoriete"},
        {"nom": "Offre de diagnostic", "part": 15, "pourquoi_moi": "c'est mon offre", "preuve": "", "etape": "conversion"},
    ],
    "minutes_semaine": 240,
}


def afficher(r):
    L = [f"BRIEF  {r['verdict']}"]
    if r["phrase_de_positionnement"]:
        L.append(f"Brouillon de phrase (à raccourcir avec l'utilisateur) : « {r['phrase_de_positionnement']} »")
    for t, liste, m in (("Refusé", r["refus"], "✖"), ("À reprendre", r["a_reprendre"], "!"), ("Notes", r["notes"], "·")):
        if liste:
            L += ["", f"{t} :"] + [f"  {m} {x}" for x in liste]
    if r["criteres_90_jours"]:
        L += ["", "Critères à 90 jours (vérifiables par un tiers, à chiffrer) :"]
        L += [f"  · {c}" for c in r["criteres_90_jours"]]
        L.append("  Le nombre d'abonnés n'en fait pas partie : il bouge pour d'autres raisons que l'objectif.")
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser(description="Vérifie un brief de positionnement (VALIDE 0 / À REPRENDRE 2 / REFUSÉ 3).")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--fichier")
    src.add_argument("--exemple", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    try:
        if a.exemple:
            b = EXEMPLE
        elif a.fichier:
            with open(a.fichier, encoding="utf-8") as f:
                b = json.load(f)
        elif not sys.stdin.isatty():
            b = json.loads(sys.stdin.read())
        else:
            p.print_help(sys.stderr)
            return 1
    except (OSError, json.JSONDecodeError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    r = verifier(b)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
