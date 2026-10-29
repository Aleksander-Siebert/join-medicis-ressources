#!/usr/bin/env python3
"""video.py : la couche texte d'une vidéo YouTube, contrôlée avant publication.

Une vidéo est trouvée (sur YouTube, dans Google, dans les réponses d'IA) par
son texte : titre, description, chapitres, transcription. Ce script contrôle
ce qui se mesure :

- chapitres de la description, selon l'aide YouTube « Ajouter des chapitres
  à vos vidéos » (relue le 16 octobre 2026) : premier code temporel 00:00,
  au moins trois codes, dans l'ordre chronologique, 10 secondes au moins
  par chapitre (le dernier se mesure avec --duree) ;
- chapitres formulés comme des sous-questions ou des étapes, pas « Partie 2 » ;
- mot-clé : dans le titre, dans les premières lignes de la description
  (celles qui s'affichent avant « Plus »), dans la transcription ;
- transcription : fournie ou non ; des sous-titres corrigés valent mieux que
  la transcription automatique, qui écorche les noms propres.

    python3 video.py --description description.txt --titre "Mutuelle indépendant : comment choisir ?" \\
        --mot-cle "mutuelle indépendant" --duree 12:40 --transcription sous-titres.srt
    python3 video.py --description description.txt --json

Le jugement (l'angle, la miniature, le commentaire épinglé) reste au Skill.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata

CODE = re.compile(r"^\s*(?:[-•*]\s*)?\(?((?:\d{1,2}:)?\d{1,2}:\d{2})\)?\s*[-–:|]?\s*(.+?)\s*$")
VAGUES = re.compile(r"(?i)^(partie|chapitre|section|part)\s*\d+$|^(intro|introduction|conclusion|outro|fin)$")
PREMIERES_LIGNES = 2


def plier(s: str) -> str:
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def secondes(code: str) -> int:
    parts = [int(x) for x in code.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return h * 3600 + m * 60 + s


def chapitres(description: str) -> list[dict]:
    out = []
    for n, ligne in enumerate(description.splitlines(), 1):
        m = CODE.match(ligne)
        if m:
            out.append({"ligne": n, "code": m.group(1), "secondes": secondes(m.group(1)), "titre": m.group(2)})
    return out


def controler(description: str, titre: str = "", mot_cle: str = "", duree: str | None = None,
              transcription: str | None = None) -> dict:
    constats = []

    def c(gravite, quoi, conseil=""):
        constats.append({"gravite": gravite, "constat": quoi, "conseil": conseil})

    ch = chapitres(description)
    if not ch:
        c("moyenne", "aucun chapitre dans la description",
          "Ajouter des chapitres : 00:00 puis une ligne par sous-question ou étape.")
    else:
        if ch[0]["secondes"] != 0:
            c("haute", f"le premier code est {ch[0]['code']}, pas 00:00 : YouTube n'affiche pas les chapitres",
              "Commencer la liste par 00:00.")
        if len(ch) < 3:
            c("haute", f"{len(ch)} code(s) temporel(s) : il en faut au moins 3", "Découper en 3 chapitres au moins.")
        for a, b in zip(ch, ch[1:]):
            if b["secondes"] <= a["secondes"]:
                c("haute", f"ligne {b['ligne']} : {b['code']} n'est pas après {a['code']} (ordre chronologique)",
                  "Classer les codes dans l'ordre.")
            elif b["secondes"] - a["secondes"] < 10:
                c("haute", f"chapitre « {a['titre']} » ({a['code']}) : {b['secondes'] - a['secondes']} s, moins de 10 s",
                  "Fusionner avec le suivant.")
        if duree:
            fin = secondes(duree)
            if fin - ch[-1]["secondes"] < 10:
                c("haute", f"dernier chapitre « {ch[-1]['titre']} » : {max(0, fin - ch[-1]['secondes'])} s, moins de 10 s",
                  "Le fusionner avec le précédent.")
        else:
            c("info", "durée de la vidéo non fournie : la longueur du dernier chapitre n'est pas vérifiée", "--duree mm:ss")
        vagues = [x["titre"] for x in ch if VAGUES.match(x["titre"].strip())]
        if vagues:
            c("basse", f"chapitres sans contenu : {', '.join(vagues)}",
              "Nommer chaque chapitre par la question qu'il traite ou l'étape qu'il montre.")

    k = plier(mot_cle)
    lignes = [l for l in description.splitlines() if l.strip()]
    if k:
        if titre and k not in plier(titre):
            c("moyenne", "mot-clé absent du titre", "Le mettre dans le titre, tel que les gens le cherchent.")
        if k not in plier(" ".join(lignes[:PREMIERES_LIGNES])):
            c("moyenne", f"mot-clé absent des {PREMIERES_LIGNES} premières lignes de la description",
              "Ces lignes s'affichent avant « Plus » : y dire de quoi parle la vidéo.")
    if titre and len(titre) > 70:
        c("info", f"titre de {len(titre)} caractères : la fin risque d'être coupée (repère de praticien, [à vérifier])",
          "Mettre l'essentiel au début.")
    if transcription is None:
        c("moyenne", "transcription non fournie",
          "Ajouter des sous-titres corrigés (fichier .srt ou .vtt) : la transcription automatique écorche les noms propres.")
    else:
        texte = re.sub(r"(?m)^\d+\s*$|^\d{2}:\d{2}:\d{2}[,.]\d{3} --> .*$|^WEBVTT.*$", " ", transcription)
        if k and k not in plier(texte):
            c("moyenne", "mot-clé jamais prononcé dans la transcription",
              "Le dire à l'oral, au début : c'est le texte que lisent les moteurs et les assistants.")
    verdict = "À CORRIGER" if any(x["gravite"] == "haute" for x in constats) else (
        "À AMÉLIORER" if any(x["gravite"] == "moyenne" for x in constats) else "PRÊT")
    return {"chapitres": ch, "constats": constats, "verdict": verdict}


def afficher(r: dict) -> str:
    out = [f"VIDÉO · {len(r['chapitres'])} chapitre(s)"]
    for x in r["chapitres"]:
        out.append(f"  {x['code']:>8}  {x['titre']}")
    for x in r["constats"]:
        out.append(f"  [{x['gravite']}] {x['constat']}")
        if x["conseil"]:
            out.append(f"         → {x['conseil']}")
    out.append(f"VERDICT · {r['verdict']}")
    return "\n".join(out)


def lire(chemin: str | None) -> str | None:
    if chemin is None:
        return None
    with open(chemin, encoding="utf-8-sig") as f:
        return f.read()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Contrôle titre, description, chapitres et transcription d'une vidéo YouTube.")
    ap.add_argument("--description", required=True, help="fichier texte de la description")
    ap.add_argument("--titre", default="")
    ap.add_argument("--mot-cle", default="")
    ap.add_argument("--duree", help="durée de la vidéo, mm:ss ou h:mm:ss")
    ap.add_argument("--transcription", help="sous-titres .srt/.vtt ou texte")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.duree and not re.fullmatch(r"(?:\d{1,2}:)?\d{1,2}:\d{2}", a.duree):
            raise ValueError(f"durée illisible : {a.duree} (mm:ss ou h:mm:ss)")
        r = controler(lire(a.description), a.titre, a.mot_cle, a.duree, lire(a.transcription))
    except (OSError, ValueError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return {"PRÊT": 0, "À AMÉLIORER": 2, "À CORRIGER": 3}[r["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
