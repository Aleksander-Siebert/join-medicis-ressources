#!/usr/bin/env python3
"""reserve.py : état de la banque d'histoires (reserve.md) et contrôle des réussites.

Commandes :
  etat FICHIER [--objectif clients|emploi|autorite]
      Sections vides ou minces, réussites inutilisables, ordre conseillé
      pour la prochaine séance d'interview.
  experiences FICHIER [--poste TEXTE]
      Réussites chiffrées regroupées par poste, prêtes pour /linkedin-profile.
  verifier "TEXTE"
      Contrôle une réussite au format « verbe + X, en Y : Z ».

Options communes : --json (sortie JSON), --exemple (travaille sur une banque
d'exemple au lieu d'un fichier).

Codes de sortie :
  0  banque complète / réussite utilisable
  2  sections à creuser / réussite à préciser
  1  erreur d'utilisation ou fichier illisible

Python 3.8+, sans dépendance. Ne lit que le fichier indiqué, n'envoie rien.
"""

import argparse
import json
import re
import sys
import unicodedata

SECTIONS = {
    1: "Parcours daté",
    2: "Réussites chiffrées",
    3: "Réalisations",
    4: "Tournants",
    5: "Erreurs et cicatrices",
    6: "Positions",
    7: "Histoires que tu racontes déjà",
    8: "Noms",
    9: "Hors limites",
}
# Nombre d'entrées à partir duquel une section n'est plus « mince ».
SEUIL_OK = {1: 2, 2: 3, 3: 2, 4: 2, 5: 1, 6: 2, 7: 2, 8: 1, 9: 1}

PRIORITES = {
    "clients": [2, 6, 7, 4, 5, 3, 1, 8, 9],
    "emploi": [1, 2, 3, 7, 4, 5, 6, 8, 9],
    "autorite": [6, 4, 5, 7, 2, 3, 1, 8, 9],
    "defaut": [2, 4, 5, 6, 7, 1, 3, 8, 9],
}

MOTS_VAGUES = [
    "significativement", "considerablement", "nettement", "fortement", "beaucoup",
    "enormement", "de nombreux", "de nombreuses", "plusieurs", "quelques",
    "recemment", "il y a quelque temps", "un gros client", "un grand compte",
    "ameliore", "optimise", "accompagne", "participe a", "contribue a",
    "en charge de", "responsable de", "aide a", "travaille sur",
]
VERBES_FAIBLES = ["participe", "contribue", "accompagne", "aide", "travaille",
                  "gere", "suivi", "assiste", "soutenu", "ete"]

MOIS = ("janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|"
        "novembre|decembre|janv|fevr|sept|oct|nov|dec")
RE_DATE = re.compile(rf"\b((19|20)\d\d|{MOIS}|t[1-4]|[1-4](er|e|eme)? trimestre|"
                     r"[12](er|e|eme)? semestre)\b")
RE_DELAI = re.compile(r"\b(en|sur|pendant)\s+(\d+|un|une|deux|trois|quatre|cinq|six|"
                      r"huit|dix|douze|quelques)\s*(jours?|semaines?|mois|ans?|annees?|"
                      r"trimestres?|semestres?|heures?)\b")
RE_CHIFFRE = re.compile(r"\d")
RE_RESULTAT = re.compile(r"(:|→|->|=>|\bsoit\b|\bce qui a\b|\bresultat\b|\bpour\b.{0,40}\d)")

EXEMPLE = """# reserve.md
## État
- rempli : oui
- mis à jour le : 2026-09-14
- séances d'interview : 1

## 1. Parcours daté
| Poste | Entreprise (ou description anonyme) | De | À | Ce dont tu étais vraiment responsable |
|---|---|---|---|---|
| Responsable acquisition | Assurly (assurance en ligne, 120 salariés) | 2023-03 | | leads B2C, budget payant, SEO |
| Chargée de marketing | agence conseil, 15 personnes | 2020-09 | 2023-02 | campagnes emailing de 6 clients |

## 2. Réussites chiffrées
| Réussite (format X / Y / Z) | Ce que le chiffre mesure | Quand | Poste | Confidentiel ? |
|---|---|---|---|---|
| Relancé 1 400 clients dormants en 6 semaines : 212 contrats réactivés | contrats réactivés | T2 2025 | Responsable acquisition | non |
| Amélioré significativement le taux de conversion du site | | | Responsable acquisition | non |
| Réduit le coût par lead de 41 € à 23 € en 4 mois : budget constant, 78% de leads en plus | coût par lead | 2024 | Responsable acquisition | ordre de grandeur seulement |

## 3. Réalisations
| Quoi | Ta part exacte | Ce que ça a coûté ou rapporté |
|---|---|---|
| Comparateur de garanties | brief, tests, lancement | {{à compléter}} |

## 4. Tournants
| Ce qui s'est passé (date) | Ce que tu croyais avant | Ce que tu crois maintenant |
|---|---|---|

## 5. Erreurs et cicatrices
| Ce qui a cassé (date) | Ce que ça a coûté, vraiment | Ce que tu fais autrement |
|---|---|---|

## 6. Positions
| Position | Qui n'est pas d'accord | Pourquoi tu la tiens quand même |
|---|---|---|
| Le SEO de marque compte plus que le SEO générique en assurance | les agences SEO | nos chiffres 2024 |

## 7. Histoires que tu racontes déjà
| L'histoire en deux lignes | Ce qu'elle montre | Déjà publiée ? (date) |
|---|---|---|

## 8. Noms
- **Citables librement :** Assurly
- **À demander d'abord :**
- **Jamais :** nos partenaires assureurs

## 9. Hors limites
- la levée de fonds en cours
"""


def sans_accents(texte: str) -> str:
    texte = unicodedata.normalize("NFKD", texte.lower())
    return "".join(c for c in texte if not unicodedata.combining(c)).replace("’", "'")


def _cellules(ligne: str) -> list:
    return [c.strip() for c in ligne.strip().strip("|").split("|")]


def analyser(texte: str) -> dict:
    """Découpe reserve.md en sections numérotées ; compte les entrées non vides."""
    sections = {n: {"titre": t, "entrees": [], "tableau": []} for n, t in SECTIONS.items()}
    etat = {}
    courante = None
    entete = None
    for ligne in texte.splitlines():
        m = re.match(r"^##\s+(\d)\.\s", ligne)
        if m:
            courante = int(m.group(1)) if int(m.group(1)) in sections else None
            entete = None
            continue
        if re.match(r"^##\s", ligne):
            courante = "etat" if "etat" in sans_accents(ligne) else None
            continue
        if courante == "etat":
            m = re.match(r"^\s*-\s*([^:]+):\s*(.*)$", ligne)
            if m:
                etat[sans_accents(m.group(1)).strip()] = m.group(2).strip()
            continue
        if courante is None:
            continue
        brut = ligne.strip()
        if brut.startswith("|"):
            cellules = _cellules(brut)
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cellules if c):
                continue
            if entete is None:
                entete = cellules
                continue
            if cellules and cellules[0] and not cellules[0].startswith("{{"):
                sections[courante]["tableau"].append(dict(zip(entete, cellules)))
                sections[courante]["entrees"].append(cellules[0])
        elif brut.startswith("-"):
            contenu = brut.lstrip("- ").strip()
            contenu = re.sub(r"^\*\*[^*]+\*\*\s*", "", contenu)  # retire « **Libellé :** »
            contenu = re.sub(r"^\([^)]*\)$", "", contenu).strip()
            if contenu and contenu not in {"…", "..."}:
                sections[courante]["entrees"].append(contenu)
    return {"etat": etat, "sections": sections}


def verifier_reussite(texte: str, quand: str = "") -> dict:
    t = sans_accents(texte)
    probleme = []
    premier = re.findall(r"[a-z']+", t)[:1]
    verbe = premier[0] if premier else ""
    if not RE_CHIFFRE.search(t):
        probleme.append("aucun chiffre (X)")
    if not (RE_DELAI.search(t) or RE_DATE.search(t) or RE_DATE.search(sans_accents(quand))):
        probleme.append("ni délai ni date (Y)")
    if not RE_RESULTAT.search(t):
        probleme.append("résultat non séparé (Z) : ajoute « : ce que ça a rapporté »")
    if verbe in VERBES_FAIBLES:
        probleme.append(f"verbe faible « {verbe} » : dis ce que tu as fait, pas que tu y étais")
    vagues = [m for m in MOTS_VAGUES if re.search(rf"\b{re.escape(m)}\b", t)]
    if vagues:
        probleme.append("mots vagues : " + ", ".join(vagues))
    if "{{" in texte:
        probleme.append("contient un champ à compléter")
    return {"texte": texte, "utilisable": not probleme, "problemes": probleme}


def etat_banque(texte: str, objectif: str = "defaut") -> dict:
    a = analyser(texte)
    lignes = []
    for n, s in a["sections"].items():
        nb = len(s["entrees"])
        statut = "vide" if nb == 0 else ("mince" if nb < SEUIL_OK[n] else "ok")
        lignes.append({"section": n, "titre": s["titre"], "entrees": nb, "statut": statut})
    faibles = []
    for ligne in a["sections"][2]["tableau"]:
        valeurs = list(ligne.values())
        quand = next((v for k, v in ligne.items() if sans_accents(k).startswith("quand")), "")
        res = verifier_reussite(valeurs[0], quand)
        if not res["utilisable"]:
            faibles.append(res)
    ordre = PRIORITES.get(objectif, PRIORITES["defaut"])
    a_creuser = [n for n in ordre if lignes[n - 1]["statut"] != "ok"]
    return {
        "rempli": a["etat"].get("rempli", "?"),
        "mis_a_jour": a["etat"].get("mis a jour le", ""),
        "sections": lignes,
        "reussites_a_preciser": faibles,
        "prochaine_seance": [SECTIONS[n] for n in a_creuser],
        "complet": not a_creuser and not faibles,
    }


def experiences(texte: str, poste: str = "") -> dict:
    a = analyser(texte)
    par_poste = {}
    for ligne in a["sections"][2]["tableau"]:
        valeurs = list(ligne.values())
        p = next((v for k, v in ligne.items() if sans_accents(k).startswith("poste")), "") or "sans poste"
        if poste and sans_accents(poste) not in sans_accents(p):
            continue
        conf = next((v for k, v in ligne.items() if sans_accents(k).startswith("confidentiel")), "")
        quand = next((v for k, v in ligne.items() if sans_accents(k).startswith("quand")), "")
        res = verifier_reussite(valeurs[0], quand)
        par_poste.setdefault(p, []).append({
            "ligne": valeurs[0], "utilisable": res["utilisable"], "problemes": res["problemes"],
            "confidentiel": conf,
        })
    return {"postes": par_poste}


def afficher_etat(r: dict) -> str:
    out = [f"RÉSERVE · rempli : {r['rempli']} · mis à jour : {r['mis_a_jour'] or '?'}", ""]
    for s in r["sections"]:
        marque = {"ok": "✓", "mince": "~", "vide": "✖"}[s["statut"]]
        out.append(f"  {marque} {s['section']}. {s['titre']:<32} {s['entrees']:>2} entrée(s)  {s['statut']}")
    if r["reussites_a_preciser"]:
        out += ["", "Réussites à préciser :"]
        for f in r["reussites_a_preciser"]:
            out.append(f"  · « {f['texte']} »")
            out += [f"      - {p}" for p in f["problemes"]]
    out.append("")
    if r["prochaine_seance"]:
        out.append("Prochaine séance, dans l'ordre : " + " → ".join(r["prochaine_seance"]))
    else:
        out.append("Banque complète. Relis-la dans 3 mois ou après un changement de poste.")
    return "\n".join(out)


def afficher_experiences(r: dict) -> str:
    out = ["LIGNES D'EXPÉRIENCE (pour /linkedin-profile)", ""]
    if not r["postes"]:
        return "Aucune réussite chiffrée dans la banque. Lance /linkedin-interview."
    for poste, lignes in r["postes"].items():
        out.append(poste)
        for l in lignes:
            note = "" if l["utilisable"] else "   ← à préciser : " + "; ".join(l["problemes"])
            conf = f"   [{l['confidentiel']}]" if l["confidentiel"] and l["confidentiel"] != "non" else ""
            out.append(f"  · {l['ligne']}{conf}{note}")
        out.append("")
    return "\n".join(out).rstrip()


def lire(chemin: str, exemple: bool) -> str:
    if exemple:
        return EXEMPLE
    if not chemin:
        raise ValueError("indique un fichier reserve.md ou --exemple")
    with open(chemin, encoding="utf-8") as f:
        return f.read()


def main() -> int:
    p = argparse.ArgumentParser(description="État de reserve.md et contrôle des réussites chiffrées.")
    sous = p.add_subparsers(dest="cmd", required=True)
    for nom in ("etat", "experiences"):
        sp = sous.add_parser(nom)
        sp.add_argument("fichier", nargs="?")
        sp.add_argument("--exemple", action="store_true")
        sp.add_argument("--json", action="store_true")
    sous.choices["etat"].add_argument("--objectif", choices=["clients", "emploi", "autorite", "defaut"],
                                      default="defaut")
    sous.choices["experiences"].add_argument("--poste", default="")
    sv = sous.add_parser("verifier")
    sv.add_argument("texte")
    sv.add_argument("--json", action="store_true")
    a = p.parse_args()

    try:
        if a.cmd == "verifier":
            r = verifier_reussite(a.texte)
            if a.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                print("UTILISABLE" if r["utilisable"] else "À PRÉCISER")
                for pb in r["problemes"]:
                    print(f"  - {pb}")
            return 0 if r["utilisable"] else 2
        texte = lire(a.fichier, a.exemple)
    except (OSError, ValueError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1

    if a.cmd == "etat":
        r = etat_banque(texte, a.objectif)
        print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher_etat(r))
        return 0 if r["complet"] else 2
    r = experiences(texte, a.poste)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher_experiences(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
