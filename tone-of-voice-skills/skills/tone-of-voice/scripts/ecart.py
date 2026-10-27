#!/usr/bin/env python3
"""ecart.py : un texte est-il écrit dans la voix décrite par tone-of-voice.md ?

Compare un brouillon aux mesures du bloc ```mesures``` et à la section « Ce
que je n'écris jamais » du fichier de voix. Sort la liste des écarts, chacun
avec sa gravité et une piste de correction, puis une note sur 100.

Ce que le script contrôle (chiffrable) :
  - adresse : tutoiement ou vouvoiement contraire à la voix ;
  - longueur des phrases hors de la bande de la voix (médiane entre 0,67 et
    1,5 fois celle de la voix ; écart-type entre 0,5 et 1,5 fois) ;
  - ponctuation classée « jamais » dans la voix et présente dans le texte,
    ou classée « rare » et employée à chaque phrase ;
  - « cela » quand la voix dit « ça » ;
  - paragraphes d'une phrase très différents de la voix ;
  - expressions interdites : dans « Ce que je n'écris jamais », l'expression
    entre « » placée en tête de chaque ligne ;
  - marques d'écriture IA (antithèse « ce n'est pas X, c'est Y », ouvertures
    creuses, annonces de sincérité, fuites d'assistant…).

Ce qu'il ne contrôle pas : les traits (« direct, pas brutal »), l'humour, la
justesse du propos. Ça reste du jugement, fait par le Skill.

Usage
  python3 ecart.py tone-of-voice.md brouillon.txt
  python3 ecart.py tone-of-voice.md brouillon.txt --adresse tutoiement   # réglage d'un canal
  python3 ecart.py tone-of-voice.md brouillon.txt --json

Codes de sortie : 0 dans la voix · 2 à retoucher · 3 hors voix · 1 erreur.

Bande de l'écart-type d'après notque/claude-code-toolkit, voice-stylometry
(MIT). Réécrit pour le français.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import texte as tx  # noqa: E402

POIDS = {"fort": 15, "moyen": 7, "faible": 3}
NOMS = {
    "emojis": "émoji", "exclamation": "point d'exclamation", "question": "question",
    "points_suspension": "points de suspension", "parentheses": "parenthèse", "deux_points": "deux-points",
    "point_virgule": "point-virgule", "cadratin": "tiret cadratin (—)",
}


def interdits(markdown):
    """Expressions entre « » de la section dont le titre contient « jamais »."""
    sortie, dedans = [], False
    for ligne in markdown.splitlines():
        if re.match(r"^#{1,4}\s", ligne):
            dedans = "jamais" in tx.plier(ligne)
            continue
        # Seule l'expression entre « » placée en tête de la ligne est contrôlée ;
        # les citations qui suivent sont des explications.
        m = re.match(r"^\s*(?:[-*]|\|)\s*«\s*([^»]+?)\s*»", ligne) if dedans else None
        if m:
            expr = m.group(1).strip().rstrip(".…")
            if expr and "{{" not in expr:
                sortie.append(expr)
    return list(dict.fromkeys(sortie))


def chercher(expr, texte):
    motif = r"(?i)(?<![\wÀ-ÿ])" + re.escape(expr).replace("\\ ", r"\s+").replace("'", "['’]") + r"(?![\wÀ-ÿ])"
    return len(re.findall(motif, texte))


def comparer(profil_md, brouillon, adresse_canal=None):
    voix = tx.lire_bloc(profil_md)
    if voix is None:
        raise ValueError("aucun bloc ```mesures``` dans le fichier de voix : lance voix.py --bloc et colle-le")
    t = tx.normaliser(brouillon)
    m = tx.mesurer(t)
    ecarts = []

    def ajouter(gravite, quoi, piste):
        ecarts.append({"gravite": gravite, "ecart": quoi, "piste": piste})

    # Adresse
    attendue = adresse_canal or voix.get("adresse")
    trouvee = tx.adresse(m["tu"], m["vous"])
    if attendue in ("tutoiement", "vouvoiement") and trouvee in ("tutoiement", "vouvoiement", "mixte") \
            and trouvee != attendue:
        g = "moyen" if trouvee == "mixte" else "fort"
        piste = "passe au " + attendue
        if trouvee == "vouvoiement" or (trouvee == "mixte" and attendue == "tutoiement"):
            piste += " (si « vous » s'adresse à plusieurs personnes, c'est voulu : ignore cet écart)"
        ajouter(g, f"{trouvee} alors que la voix est au {attendue}", piste)

    # Rythme
    med_v, et_v = voix.get("phrase_mediane"), voix.get("phrase_ecart_type")
    if m["phrases"] >= 4 and isinstance(med_v, (int, float)) and m["phrase_mediane"] is not None:
        bas, haut = 0.67 * med_v, 1.5 * med_v
        if m["phrase_mediane"] > haut:
            ajouter("moyen", f"phrases de {m['phrase_mediane']:g} mots en médiane, la voix en fait {med_v:g}",
                    "coupe les phrases longues ; une idée par phrase")
        elif m["phrase_mediane"] < bas:
            ajouter("moyen", f"phrases de {m['phrase_mediane']:g} mots en médiane, la voix en fait {med_v:g}",
                    "relie les phrases trop hachées")
    if m["phrase_ecart_type"] is not None and isinstance(et_v, (int, float)) and et_v > 0:
        if m["phrase_ecart_type"] < 0.5 * et_v:
            ajouter("faible", f"rythme plat (écart-type {m['phrase_ecart_type']:g} contre {et_v:g})",
                    "mêle des phrases courtes et longues comme dans les textes d'origine")
        elif m["phrase_ecart_type"] > 1.5 * et_v:
            ajouter("faible", f"rythme heurté (écart-type {m['phrase_ecart_type']:g} contre {et_v:g})",
                    "évite d'alterner phrases très courtes et très longues")

    # Ponctuation
    n_ph = max(m["phrases"], 1)
    for cle, nom in NOMS.items():
        classe = voix.get(cle)
        nb = m["emojis"] if cle == "emojis" else m["ponctuation"].get(cle, 0)
        if classe == "jamais" and nb:
            g = "fort" if cle == "cadratin" else "moyen"
            ajouter(g, f"{nb} {nom}{'s' if nb > 1 and not nom.endswith('s') else ''} alors que la voix n'en met jamais",
                    ("retire-le" if nb == 1 else "retire-les") + (" (remplace le cadratin par une virgule)" if cle == "cadratin" else ""))
        elif classe == "rare" and nb / n_ph >= 0.5 and nb >= 3:
            ajouter("faible", f"{nb} {nom}s pour {m['phrases']} phrases alors que la voix en met rarement",
                    "garde-en un ou deux")

    # Registre
    if voix.get("ca_cela") == "ça" and m["cela"] and not m["ca"]:
        ajouter("faible", f"« cela » ({m['cela']} fois) alors que la voix dit « ça »", "remplace par « ça »")
    if voix.get("ca_cela") == "cela" and m["ca"] and not m["cela"]:
        ajouter("faible", f"« ça » ({m['ca']} fois) alors que la voix dit « cela »", "remplace par « cela »")
    if m["soutenu"] >= 2:
        ajouter("moyen", f"{m['soutenu']} formules administratives (« veuillez », « conformément »…)",
                "écris comme tu parles à ce lecteur")

    # Mise en page
    pv = voix.get("part_paragraphes_une_phrase")
    if isinstance(pv, (int, float)) and m["part_paragraphes_une_phrase"] is not None:
        if abs(m["part_paragraphes_une_phrase"] - pv) > 40:
            ajouter("faible", f"{m['part_paragraphes_une_phrase']:g}% de paragraphes d'une phrase, "
                              f"la voix en a {pv:g}%", "regroupe ou aère les paragraphes comme d'habitude")

    # Interdits du fichier
    for expr in interdits(profil_md):
        n = chercher(expr, t)
        if n:
            ajouter("fort", f"« {expr} » ({n} fois) figure dans « Ce que je n'écris jamais »", "retire ou reformule")

    # Marques IA
    for x in m["marques_ia"]:
        ajouter("fort" if x["force"] == "fort" else "faible", f"marque d'écriture IA ({x['id']}) : « {x['extrait']} »",
                "dis la chose directement")

    perte = sum(POIDS[e["gravite"]] for e in ecarts)
    note = max(0, 100 - perte)
    forts = sum(e["gravite"] == "fort" for e in ecarts)
    if note >= 80 and not forts:
        verdict = "DANS LA VOIX"
    elif note >= 55:
        verdict = "À RETOUCHER"
    else:
        verdict = "HORS VOIX"
    ordre = {"fort": 0, "moyen": 1, "faible": 2}
    ecarts.sort(key=lambda e: ordre[e["gravite"]])
    return {"note": note, "verdict": verdict, "ecarts": ecarts, "mots": m["mots"], "phrases": m["phrases"],
            "confiance_voix": voix.get("confiance"), "adresse_attendue": attendue}


def rendu(r, out=sys.stdout):
    print(f"{r['verdict']} · {r['note']}/100 · {r['mots']} mots, {r['phrases']} phrases", file=out)
    if r["confiance_voix"] == "faible":
        print("(voix construite sur peu de textes : écarts de rythme indicatifs)", file=out)
    if not r["ecarts"]:
        print("Aucun écart chiffrable. Reste à juger les traits et le propos.", file=out)
        return
    for e in r["ecarts"]:
        print(f"  [{e['gravite']}] {e['ecart']} → {e['piste']}", file=out)
    print("Ces écarts sont mesurés ; les traits (« direct, pas brutal ») se jugent à la relecture.", file=out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compare un texte à la voix décrite dans tone-of-voice.md.")
    ap.add_argument("voix", help="tone-of-voice.md (avec son bloc ```mesures```)")
    ap.add_argument("texte", help="brouillon à vérifier (.txt ou .md)")
    ap.add_argument("--adresse", choices=["tutoiement", "vouvoiement"],
                    help="adresse du canal visé, si elle diffère de la voix générale")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        with open(a.voix, encoding="utf-8") as fh:
            profil = fh.read()
        with open(a.texte, encoding="utf-8") as fh:
            brouillon = fh.read()
        r = comparer(profil, brouillon, a.adresse)
    except (OSError, ValueError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    if not tx.MOT.search(brouillon):
        print("Erreur : texte vide.", file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        rendu(r)
    return {"DANS LA VOIX": 0, "À RETOUCHER": 2, "HORS VOIX": 3}[r["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
