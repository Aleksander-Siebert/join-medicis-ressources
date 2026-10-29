#!/usr/bin/env python3
"""candidatures.py : caler le profil sur les offres visées, suivre les candidatures.

  mots --offres offres.txt --profil profil.txt [--min 2]
      Compare 3 à 15 offres collées (séparées par une ligne « --- ») avec le
      texte du profil (titre, Infos, expériences, compétences) :
        - les intitulés des offres, par fréquence (pour le titre et la recherche) ;
        - les termes présents dans au moins --min offres (et au moins un tiers
          d'entre elles) et absents du profil : à ajouter SEULEMENT si c'est vrai ;
        - les termes du profil que les offres n'emploient jamais.

  ajouter --journal journal.md --entreprise "…" --poste "…" [--lien …] [--source offre|reseau|spontanee]
          [--contact "…"] [--etape envoyee] [--date 2026-10-02] [--prochaine "…"]
      Ajoute une ligne au tableau « Candidatures » de journal.md (après le
      « oui » de l'utilisateur).

  etat --journal journal.md [--aujourdhui 2026-10-20]
      Comptes par étape, taux de réponse par source (offre, réseau,
      spontanée), relances dues (7 jours sans réponse : une relance, avec un
      élément nouveau), candidatures à classer (21 jours sans réponse).

Codes de sortie : 0 ; etat : 2 s'il y a des relances dues ; 1 erreur.
Sans dépendance. Rien n'est lu sur LinkedIn : les offres sont collées.
"""

import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

STOP = set("""a au aux avec ce ces cet cette c'est dans de des du elle en et eux il ils je j'ai la le les leur leurs lui ma mais me
meme mes moi mon ne nos notre nous on ou par pas pour qu que qui sa se ses si son sur ta te tes toi ton tu un une vos votre vous y
est sont etre avoir ont fait faire plus tres tout tous toute toutes bien aussi comme alors donc car ni cela ca ici sans sous chez
entre vers apres avant pendant depuis encore deja jamais toujours rien peu the and of to in for with on at by an or as is are be
will you your our we this that from h/f f/h hf poste profil mission missions entreprise equipe equipes rejoindre rejoins recherche
recherchons cherchons candidat candidate experience experiences ans annee annees an niveau minimum idealement souhaite souhaitee
capacite capable bonne bonnes excellent excellente forte fort sens esprit maitrise connaissance connaissances environnement
cadre type contrat cdi cdd temps plein partiel paris lyon france remote teletravail hybride salaire remuneration avantages
offre offres description job role responsibilities requirements nice have plus etc via afin ainsi notamment dont leur
personnes personne pilotez pilotes piloter pilote travaillez travailles construisez construis animez animes encadrez encadres
suivez suis etes es serez seras appreciee apprecies appreciees appreciable attendue attendu attendus outils outil un plus
responsable responsables vous tu rejoignez""".split())
ETAPES = ["envoyee", "relancee", "entretien", "test", "offre", "refus", "abandon", "classee"]


def norme(t):
    t = unicodedata.normalize("NFKD", str(t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'")


def termes(texte):
    """Mots pleins et groupes de 2 mots pleins consécutifs ; noms d'outils conservés tels quels."""
    tn = norme(texte)
    mots = re.findall(r"[a-z0-9][a-z0-9+#.\-]*[a-z0-9+#]|[a-z0-9]", tn)
    pleins = [m for m in mots if m not in STOP and (len(m) >= 3 or m in ("ga4", "ia", "ai", "bi", "ux", "ui", "c#", "go", "r"))]
    out = set(pleins)
    for a, b in zip(mots, mots[1:]):
        if a not in STOP and b not in STOP and len(a) >= 3 and len(b) >= 3:
            out.add(f"{a} {b}")
    return out


def intitule(offre):
    premiere = next((l.strip() for l in offre.strip().splitlines() if l.strip()), "")
    premiere = re.sub(r"\s*[-–(|].*$", "", premiere)
    premiere = re.sub(r"\b[hf]\s*/\s*[hf]\b|\(h/f\)", "", premiere, flags=re.I)
    return premiere.strip(" -:")


def mots(offres_txt, profil_txt, minimum=2):
    offres = [o for o in re.split(r"^\s*---\s*$", offres_txt, flags=re.M) if o.strip()]
    n = len(offres)
    profil = norme(profil_txt)
    intitules = {}
    for o in offres:
        t = intitule(o)
        if t:
            intitules[t] = intitules.get(t, 0) + 1
    compte = {}
    for o in offres:
        for t in termes(o):
            compte[t] = compte.get(t, 0) + 1
    seuil = max(minimum, -(-n // 3))
    frequents = {t: c for t, c in compte.items() if c >= seuil}
    # un groupe de deux mots fréquent absorbe ses mots seuls s'ils n'ont pas plus d'occurrences
    for t in [t for t in frequents if " " in t]:
        for m in t.split():
            if m in frequents and frequents[m] <= frequents[t]:
                del frequents[m]
    absents = sorted(((t, c) for t, c in frequents.items() if not re.search(rf"(?<![\w-]){re.escape(t)}(?![\w-])", profil)),
                     key=lambda x: (-x[1], x[0]))
    presents = sorted(((t, c) for t, c in frequents.items() if (t, c) not in absents), key=lambda x: (-x[1], x[0]))
    # les compétences listées dans le profil (ligne « Compétences : … ») que les offres n'emploient jamais
    m = re.search(r"comp[ée]tences?\s*:\s*(.+)", profil_txt, re.I)
    listees = [c.strip(" .") for c in re.split(r"[,;·]", m.group(1))] if m else []
    offres_n = norme(offres_txt)
    jamais = [c for c in listees if c and not re.search(rf"(?<![\w-]){re.escape(norme(c))}(?![\w-])", offres_n)]
    return {"offres": n, "seuil": seuil,
            "intitules": sorted(intitules.items(), key=lambda x: -x[1]),
            "absents_du_profil": absents[:25], "deja_dans_le_profil": presents[:25], "jamais_dans_les_offres": jamais,
            "rappel": "Un terme absent ne s'ajoute que s'il est vrai : jamais une compétence ou un outil que tu n'as pas pratiqué."}


def _table(texte):
    m = re.search(r"## Candidatures[^\n]*\n(?:[^|\n][^\n]*\n|\n)*((?:\|.*\n?)+)", texte)
    return m


def lire_candidatures(chemin):
    p = Path(chemin)
    if not p.exists():
        return []
    m = _table(p.read_text(encoding="utf-8"))
    if not m:
        return []
    lignes = m.group(1).splitlines()
    entete = [norme(c).split(" (")[0].strip() for c in lignes[0].strip().strip("|").split("|")]
    out = []
    for l in lignes[2:]:
        d = dict(zip(entete, [c.strip() for c in l.strip().strip("|").split("|")]))
        if not d.get("entreprise"):
            continue
        try:
            d["_date"] = date.fromisoformat(d.get("date", "")[:10])
        except ValueError:
            d["_date"] = None
        out.append(d)
    return out


def ajouter(chemin, entreprise, poste, lien="", source="offre", contact="", etape="envoyee", jour=None, prochaine=""):
    p = Path(chemin)
    texte = p.read_text(encoding="utf-8") if p.exists() else "# journal.md\n"
    cel = [jour or date.today().isoformat(), entreprise, poste, lien, source, contact, etape, prochaine]
    ligne = "| " + " | ".join(str(c).replace("|", "/") for c in cel) + " |"
    m = _table(texte)
    if m:
        bloc = m.group(1) if m.group(1).endswith("\n") else m.group(1) + "\n"
        texte = texte[:m.start(1)] + bloc + ligne + "\n" + texte[m.end(1):]
    else:
        texte = texte.rstrip("\n") + "\n\n## Candidatures (pour /linkedin-job)\n\n| date | entreprise | poste | lien | source (offre, réseau, " \
                "candidature spontanée) | contact | étape | prochaine action |\n|---|---|---|---|---|---|---|---|\n" + ligne + "\n"
    p.write_text(texte, encoding="utf-8")
    return ligne


def etat(cands, aujourd_hui=None):
    auj = aujourd_hui or date.today()
    par_etape, par_source = {}, {}
    relances, classer = [], []
    for c in cands:
        e = norme(c.get("etape")).split()[0] if c.get("etape") else "envoyee"
        par_etape[e] = par_etape.get(e, 0) + 1
        s = norme(c.get("source")).split()[0] if c.get("source") else "?"
        s = {"reseau": "réseau", "spontanee": "spontanée", "candidature": "spontanée"}.get(s, s)
        ps = par_source.setdefault(s, {"total": 0, "reponses": 0})
        ps["total"] += 1
        if e not in ("envoyee", "relancee", "classee", "abandon"):
            ps["reponses"] += 1
        jours = (auj - c["_date"]).days if c.get("_date") else None
        if e == "envoyee" and jours is not None and 7 <= jours < 21:
            relances.append(f"{c['entreprise']} ({c.get('poste', '')}) : envoyée il y a {jours} jours. Une relance, avec un élément nouveau "
                            "(un projet, un résultat, une question sur l'équipe), au recruteur ou à la personne qui a publié l'offre.")
        elif e in ("envoyee", "relancee") and jours is not None and jours >= 21:
            classer.append(f"{c['entreprise']} ({c.get('poste', '')}) : {jours} jours sans réponse. Classer et passer à la suite.")
    total = len(cands)
    reponses = sum(v["reponses"] for v in par_source.values())
    return {"total": total, "par_etape": par_etape,
            "taux_reponse": round(reponses / total, 2) if total else None,
            "par_source": {s: dict(v, taux=round(v["reponses"] / v["total"], 2)) for s, v in par_source.items()},
            "relances_dues": relances, "a_classer": classer,
            "note": "Sous 10 candidatures par source, les taux sont indicatifs." if total < 10 else ""}


def main():
    a = argparse.ArgumentParser(description="Offres contre profil, suivi des candidatures.")
    sous = a.add_subparsers(dest="cmd", required=True)
    m = sous.add_parser("mots")
    m.add_argument("--offres", required=True)
    m.add_argument("--profil", required=True)
    m.add_argument("--min", type=int, default=2)
    m.add_argument("--json", action="store_true")
    j = sous.add_parser("ajouter")
    j.add_argument("--journal", required=True)
    j.add_argument("--entreprise", required=True)
    j.add_argument("--poste", required=True)
    j.add_argument("--lien", default="")
    j.add_argument("--source", default="offre", choices=["offre", "reseau", "spontanee"])
    j.add_argument("--contact", default="")
    j.add_argument("--etape", default="envoyee", choices=ETAPES)
    j.add_argument("--date")
    j.add_argument("--prochaine", default="")
    e = sous.add_parser("etat")
    e.add_argument("--journal", required=True)
    e.add_argument("--aujourdhui")
    e.add_argument("--json", action="store_true")
    x = a.parse_args()
    try:
        if x.cmd == "ajouter":
            print("Ajouté : " + ajouter(x.journal, x.entreprise, x.poste, x.lien, x.source, x.contact, x.etape, x.date, x.prochaine))
            return 0
        if x.cmd == "mots":
            r = mots(Path(x.offres).read_text(encoding="utf-8"), Path(x.profil).read_text(encoding="utf-8"), x.min)
            if x.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
                return 0
            print(f"OFFRES · {r['offres']} offres · un terme compte s'il apparaît dans au moins {r['seuil']} offres")
            print("  INTITULÉS : " + ", ".join(f"{t} ({n})" for t, n in r["intitules"]))
            print("  ABSENTS DU PROFIL (à ajouter seulement si c'est vrai) :")
            for t, n in r["absents_du_profil"]:
                print(f"    {t} · {n} offres")
            print("  DÉJÀ DANS LE PROFIL : " + ", ".join(t for t, _ in r["deja_dans_le_profil"]))
            if r["jamais_dans_les_offres"]:
                print("  DANS LE PROFIL, JAMAIS DANS LES OFFRES : " + ", ".join(r["jamais_dans_les_offres"]))
            print(f"  {r['rappel']}")
            return 0
        auj = date.fromisoformat(x.aujourdhui) if x.aujourdhui else None
        r = etat(lire_candidatures(x.journal), auj)
    except (OSError, ValueError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    if x.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        taux = f" · taux de réponse {round(r['taux_reponse'] * 100)}%" if r["taux_reponse"] is not None else ""
        print(f"CANDIDATURES · {r['total']}{taux} · " + ", ".join(f"{n} {e}" for e, n in r["par_etape"].items()))
        for s, v in r["par_source"].items():
            print(f"  {s} : {v['reponses']} réponse(s) sur {v['total']} ({round(v['taux'] * 100)}%)")
        for l in r["relances_dues"]:
            print(f"  ! relance due : {l}")
        for l in r["a_classer"]:
            print(f"  · à classer : {l}")
        if r["note"]:
            print(f"  {r['note']}")
    return 2 if r["relances_dues"] else 0


if __name__ == "__main__":
    sys.exit(main())
