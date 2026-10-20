#!/usr/bin/env python3
"""classeur_ads.py : contrôle et répare le classeur d'annonces ChatGPT Ads (Python 3, sans dépendance).

Le format attendu est le schéma d'annonces, en CSV (UTF-8, virgule) ; un XLSX à un onglet se lit aussi :
  ad_id | ad_group_id | adgroup_name | ad_name | status | title | copy | link | image_url | image_file_id

Commandes :

  schema [-o VIERGE.csv]
      Affiche les colonnes et, avec -o, écrit un fichier vierge au format (.csv, ou .xlsx).

  verifier FICHIER [--limites import|api] [--en-ligne] [--json]
      FICHIER : .csv ou .xlsx. Contrôle la structure (séparateur, encodage, BOM ;
      onglets, en-têtes, ordre, fusions), chaque cellule (formules, italique, nombres à la place de
      texte, espaces, retours à la ligne, invisibles) et chaque annonce
      (identifiants, groupe, nom, statut, longueurs, liens, image, doublons).
      Les cases vides (adgroup_name, title, copy, link, image_url) sont listées
      colonne par colonne avec leurs lignes, pour vérification.
      --en-ligne ouvre chaque lien et chaque image (taille, format carré).

  reparer FICHIER -o SORTIE.csv [--limites import|api]
      Réécrit un fichier propre (CSV UTF-8 sans BOM, virgule ; .xlsx si demandé) :
      colonnes dans l'ordre, valeurs en texte, espaces et invisibles retirés,
      status vide → active, ad_name vide → groupe-NN, doublons exacts retirés.
      N'ajoute jamais d'identifiant, ne raccourcit jamais un titre ni une copie.
      Puis contrôle le résultat.

  depuis-json CAMPAGNE.json -o SORTIE.csv
      Écrit le classeur à partir du JSON d'une campagne du pack
      (/chatgpt-ads-skills, /chatgpt-ads-bulk, /chatgpt-ads-exports).

  tableau FICHIER
      Repli sans fichier : en-têtes et lignes séparés par des tabulations,
      à coller dans la cellule A1 d'un classeur vierge.

Codes de sortie : 0 rien à revoir · 2 points d'attention · 3 bloquant · 1 erreur d'usage.
"""
import argparse
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve()
for base in (ICI.parents[1] / "commun", ICI.parents[2] / "commun"):   # Skill seul, ou ZIP claude.ai
    if (base / "classeur.py").exists():
        sys.path.insert(0, str(base))
        break
import classeur as cl  # noqa: E402


def lignes_depuis_json(camp):
    """Annonces du JSON de campagne → lignes du schéma (ad_group_id repris de l'ad group s'il est connu)."""
    ids = {g.get("adgroup_name"): g.get("ad_group_id", "") for g in camp.get("adgroups", [])}
    res = []
    for a in camp.get("ads", []):
        g = a.get("adgroup_name", "")
        res.append({
            "ad_id": a.get("ad_id", ""),
            "ad_group_id": a.get("ad_group_id") or ids.get(g, ""),
            "adgroup_name": g,
            "ad_name": a.get("ad_name", ""),
            "status": a.get("status") or cl.STATUT_DEFAUT,
            "title": a.get("title", ""),
            "copy": a.get("copy", ""),
            "link": a.get("link", ""),
            "image_url": a.get("image_url") or a.get("image_link", ""),
            "image_file_id": a.get("image_file_id", ""),
        })
    return res


def afficher(r, en_json, titre):
    if en_json:
        print(json.dumps({"bloquants": r.compte(cl.BLOQUANT), "attention": r.compte(cl.ATTENTION),
                          "points": r.points}, ensure_ascii=False, indent=2))
    else:
        print(r.texte(titre))
        print("Verdict : " + ("bloquant, à corriger avant import" if r.code() == 3 else
                              "importable après relecture des points d'attention" if r.code() == 2 else
                              "format conforme (import d'essai conseillé)"))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("schema")
    s.add_argument("-o", "--sortie", help="vierge.csv (ou .xlsx)")
    v = sp.add_parser("verifier")
    v.add_argument("fichier")
    v.add_argument("--limites", choices=("import", "api"), default="import")
    v.add_argument("--en-ligne", action="store_true")
    v.add_argument("--json", action="store_true")
    rp = sp.add_parser("reparer")
    rp.add_argument("fichier")
    rp.add_argument("-o", "--sortie", required=True)
    rp.add_argument("--limites", choices=("import", "api"), default="import")
    dj = sp.add_parser("depuis-json")
    dj.add_argument("campagne")
    dj.add_argument("-o", "--sortie", required=True)
    dj.add_argument("--limites", choices=("import", "api"), default="import")
    t = sp.add_parser("tableau")
    t.add_argument("fichier")
    a = p.parse_args(argv)

    if a.cmd == "schema":
        print(" | ".join(cl.COLONNES))
        if a.sortie:
            cl.ecrire(a.sortie, [])
            print(f"Fichier vierge écrit : {a.sortie}")
        return 0

    if a.cmd in ("verifier", "reparer", "tableau") and not Path(a.fichier).exists():
        print(f"Fichier introuvable : {a.fichier}", file=sys.stderr)
        return 1

    if a.cmd == "verifier":
        r, _, _ = cl.verifier(a.fichier, a.limites, cl.controle_en_ligne if a.en_ligne else None)
        afficher(r, a.json, f"Contrôle de {Path(a.fichier).name}")
        return r.code()

    if a.cmd == "tableau":
        _, lignes = cl.annonces(cl.lire(a.fichier))
        print(cl.tableau_a_coller(lignes))
        return 0

    if a.cmd == "reparer":
        avant, classeur, lignes = cl.verifier(a.fichier, a.limites)
        if classeur is None:
            afficher(avant, False, "Lecture impossible")
            return 3
        propres, journal = cl.reparer_lignes(lignes)
        cl.ecrire(a.sortie, propres)
        print(f"Avant : {avant.compte(cl.BLOQUANT)} bloquant(s), {avant.compte(cl.ATTENTION)} attention.")
        print(f"Corrections ({len(journal)}) :" if journal else "Aucune correction de cellule.")
        for j in journal:
            print(f"  - {j}")
        apres, _, _ = cl.verifier(a.sortie, a.limites)
        afficher(apres, False, f"Contrôle de {Path(a.sortie).name}")
        return apres.code()

    if a.cmd == "depuis-json":
        camp = json.loads(Path(a.campagne).read_text(encoding="utf-8"))
        lignes = lignes_depuis_json(camp)
        r = cl.Rapport()
        cl.verifier_annonces(lignes, r, a.limites)
        if r.compte(cl.BLOQUANT):
            afficher(r, False, "Contrôle avant écriture")
            print("Fichier non écrit : corriger les points bloquants.")
            return 3
        cl.ecrire(a.sortie, lignes)
        afficher(r, False, f"Contrôle de {Path(a.sortie).name}")
        return r.code()
    return 1


if __name__ == "__main__":
    sys.exit(main())
