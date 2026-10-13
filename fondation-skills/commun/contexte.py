#!/usr/bin/env python3
"""État et export des fichiers de la Fondation (Python 3, sans dépendance).

Deux commandes :

  etat FICHIER [FICHIER…]
      Compte ce qui est vraiment rempli dans entreprise.md, clients.md,
      voix.md ou preuves.md : lignes étiquetées LIVE / À CONFIRMER / RETIRÉ,
      lignes sans étiquette, sans date, sans source, dates trop anciennes,
      trous {{à compléter}}. Un modèle vide n'a jamais de bonne note : seules
      les lignes LIVE datées et sourcées comptent comme utilisables.

  exporter --vers seo|linkedin entreprise.md
      Prépare, à partir d'entreprise.md, les sections à coller dans
      site-context.md (packs SEO et GEO) ou contexte.md (pack LinkedIn).
      N'écrit aucun fichier : affiche un brouillon à relire. Les faits
      À CONFIRMER sortent en {{à confirmer : …}}, les RETIRÉ ne sortent que
      dans « Formulations retirées », les vides en {{à compléter}}.

Codes de sortie : 0 rien à revoir · 2 à revoir · 3 fichier vide ou absent ·
1 erreur d'usage.

Exemples :
  python3 contexte.py etat ~/.claude/fondation/entreprise.md
  python3 contexte.py etat entreprise.md --aujourdhui 2026-10-13 --json
  python3 contexte.py exporter --vers seo ~/.claude/fondation/entreprise.md
"""
import argparse
import datetime as dt
import json
import re
import sys
import unicodedata
from pathlib import Path

ETIQUETTES = {"LIVE": "LIVE", "A CONFIRMER": "À CONFIRMER", "RETIRE": "RETIRÉ"}
MOIS = {"janvier": 1, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7,
        "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11, "decembre": 12,
        "janv": 1, "fevr": 2, "avr": 4, "juil": 7, "sept": 9, "oct": 10, "nov": 11, "dec": 12}
TYPES_ALTERNATIVE = {"statu quo", "directe", "secondaire", "indirecte"}


def plier(s):
    """Minuscules sans accents, pour comparer des libellés."""
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()


def etiquette(cellule):
    """« LIVE », « À CONFIRMER », « RETIRÉ » ou None."""
    c = plier(cellule).upper().replace("*", "").strip()
    return ETIQUETTES.get(c)


def lire_date(texte):
    """Lit 13/10/2026, 2026-10-13, 13 octobre 2026, 13 oct. 2026 ou octobre 2026."""
    t = plier(texte)
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", t)
    if m:
        j, mo, a = map(int, m.groups())
        return _date(a, mo, j)
    m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", t)
    if m:
        a, mo, j = map(int, m.groups())
        return _date(a, mo, j)
    m = re.search(r"\b(?:(\d{1,2})(?:er)?\s+)?([a-z]+)\.?\s+(\d{4})\b", t)
    if m and m.group(2) in MOIS:
        return _date(int(m.group(3)), MOIS[m.group(2)], int(m.group(1) or 1))
    return None


def _date(a, mo, j):
    try:
        return dt.date(a, mo, j)
    except ValueError:
        return None


# --- Lecture du Markdown -------------------------------------------------------

def cellules(ligne):
    ligne = ligne.strip()
    if not (ligne.startswith("|") and ligne.endswith("|")):
        return None
    return [c.strip() for c in ligne[1:-1].split("|")]


def tableaux(texte):
    """Liste de (titre de section, en-têtes, lignes) pour chaque tableau."""
    res, section, lignes = [], "", texte.splitlines()
    i = 0
    while i < len(lignes):
        l = lignes[i]
        if l.startswith("#"):
            section = l.lstrip("#").strip()
        c = cellules(l)
        if c and i + 1 < len(lignes) and re.match(r"^\|(\s*:?-+:?\s*\|)+\s*$", lignes[i + 1].strip()):
            entetes, corps = c, []
            i += 2
            while i < len(lignes) and cellules(lignes[i]) is not None:
                corps.append(cellules(lignes[i]))
                i += 1
            res.append((section, entetes, corps))
            continue
        i += 1
    return res


def section_num(texte, numero):
    """Texte de la section « ## numero. … » jusqu'à la suivante."""
    m = re.search(rf"^## {numero}\. .*?$(.*?)(?=^## |\Z)", texte, re.M | re.S)
    return m.group(1) if m else ""


def ligne_libre(texte, libelle):
    """Valeur d'une ligne « **Libellé :** valeur »."""
    m = re.search(rf"\*\*{re.escape(libelle)}\s*:\*\*\s*(.*)", texte)
    return m.group(1).strip() if m else ""


def est_contenu(cellule, entete):
    c = cellule.strip()
    if not c or c.endswith(":"):
        return False
    if plier(entete) == "type" and plier(c) in TYPES_ALTERNATIVE:
        return False
    return True


# --- etat --------------------------------------------------------------------

def analyser(texte, aujourdhui, jours):
    lignes, problemes = [], []
    for section, entetes, corps in tableaux(texte):
        noms = [plier(e) for e in entetes]
        if "etiquette" not in noms or "sens" in noms:
            continue  # tableau sans étiquette, ou légende des étiquettes
        i_et = noms.index("etiquette")
        i_au = noms.index("au") if "au" in noms else None
        i_src = noms.index("source") if "source" in noms else None
        exclus = {i_et, i_au, i_src}
        if noms[0] == "fait":
            exclus.add(0)
        for cel in corps:
            cel = cel + [""] * (len(entetes) - len(cel))
            libelle = cel[0].rstrip(" :") or entetes[0]
            contenu = [cel[k] for k in range(len(entetes)) if k not in exclus and est_contenu(cel[k], entetes[k])]
            et = etiquette(cel[i_et])
            if not contenu and not et:
                lignes.append({"section": section, "fait": libelle, "statut": "vide"})
                continue
            d = lire_date(cel[i_au]) if i_au is not None else None
            l = {"section": section, "fait": libelle, "etiquette": et,
                 "date": d.isoformat() if d else None,
                 "source": bool(i_src is not None and cel[i_src].strip()),
                 "trou": any("{{" in c for c in contenu)}
            defauts = []
            if not et:
                defauts.append("sans étiquette")
            if i_au is not None and not d:
                defauts.append("sans date")
            if i_src is not None and not l["source"] and et != "RETIRÉ":
                defauts.append("sans source")
            if d and et == "LIVE" and (aujourdhui - d).days > jours:
                defauts.append(f"daté de plus de {jours} jours")
            if l["trou"]:
                defauts.append("trou à compléter")
            if et == "À CONFIRMER":
                defauts.append("à confirmer")
            l["defauts"] = defauts
            l["statut"] = "utilisable" if et == "LIVE" and not defauts else (
                "retiré" if et == "RETIRÉ" else "à revoir")
            lignes.append(l)

    trous = len(re.findall(r"\{\{\s*à compléter", texte))
    relecture = lire_date(re.search(r"prochaine relecture\s*:\s*(.*)", texte).group(1)) \
        if re.search(r"prochaine relecture\s*:\s*(.*)", texte) else None
    if relecture and relecture < aujourdhui:
        problemes.append(f"relecture prévue le {relecture.isoformat()} : dépassée")
    remplies = [l for l in lignes if l["statut"] != "vide"]
    return {
        "lignes": len(lignes),
        "remplies": len(remplies),
        "utilisables": sum(1 for l in lignes if l["statut"] == "utilisable"),
        "a_revoir": sum(1 for l in lignes if l["statut"] == "à revoir"),
        "retirees": sum(1 for l in lignes if l["statut"] == "retiré"),
        "vides": len(lignes) - len(remplies),
        "trous": trous,
        "problemes": problemes,
        "details": [l for l in remplies if l.get("defauts")],
        "vides_liste": [f'{l["section"]} : {l["fait"]}' for l in lignes if l["statut"] == "vide"],
    }


def verdict(r):
    if r["remplies"] == 0:
        return "vide", 3
    if r["a_revoir"] or r["problemes"] or r["vides"] or r["trous"]:
        return "à revoir", 2
    return "à jour", 0


def cmd_etat(args):
    aujourdhui = dt.date.fromisoformat(args.aujourdhui) if args.aujourdhui else dt.date.today()
    sortie, code = [], 0
    for f in args.fichiers:
        p = Path(f).expanduser()
        if not p.exists():
            sortie.append({"fichier": f, "verdict": "absent"})
            code = max(code, 3)
            continue
        r = analyser(p.read_text(encoding="utf-8"), aujourdhui, args.jours)
        v, c = verdict(r)
        r.update({"fichier": f, "verdict": v})
        sortie.append(r)
        code = max(code, c)
    if args.json:
        print(json.dumps(sortie, ensure_ascii=False, indent=2))
        return code
    for r in sortie:
        print(f"{r['fichier']} : {r['verdict'].upper()}")
        if r["verdict"] == "absent":
            print("  fichier introuvable")
            continue
        print(f"  {r['utilisables']} faits utilisables (LIVE, datés, sourcés) sur {r['lignes']} lignes")
        print(f"  {r['a_revoir']} à revoir · {r['retirees']} retirés · {r['vides']} vides · {r['trous']} trous {{{{à compléter}}}}")
        for p in r["problemes"]:
            print(f"  ! {p}")
        for l in r["details"]:
            print(f"  - {l['section']} › {l['fait']} : {', '.join(l['defauts'])}")
        if r["vides_liste"] and r["remplies"]:
            print("  vides : " + " ; ".join(r["vides_liste"][:12]) + (" ; …" if len(r["vides_liste"]) > 12 else ""))
    return code


# --- exporter ------------------------------------------------------------------

def faits(texte, numero):
    """{libellé plié : (valeur, étiquette, au, source)} pour un tableau Fait/Valeur."""
    res = {}
    for _, entetes, corps in tableaux(section_num(texte, numero)):
        noms = [plier(e) for e in entetes]
        if noms[:2] != ["fait", "valeur"]:
            continue
        for cel in corps:
            cel = cel + [""] * (len(entetes) - len(cel))
            get = lambda n: cel[noms.index(n)] if n in noms else ""
            res[plier(cel[0])] = (cel[1], etiquette(get("etiquette")), get("au"), get("source"))
    return res


def rendre(fait):
    """Valeur prête à coller selon son étiquette."""
    if not fait:
        return "{{à compléter}}"
    valeur, et = fait[0], fait[1]
    if not valeur or et == "RETIRÉ":
        return "{{à compléter}}"
    if et != "LIVE":
        if "{{" in valeur:  # déjà un trou : on ne l'emboîte pas
            return valeur + " {{à confirmer}}"
        return "{{à confirmer : " + valeur + "}}"
    return valeur


def chercher(table, debut):
    for k, v in table.items():
        if k.startswith(plier(debut)):
            return v
    return None


def offres(texte):
    res = []
    for _, entetes, corps in tableaux(section_num(texte, 2)):
        noms = [plier(e) for e in entetes]
        if "offre" not in noms:
            continue
        for cel in corps:
            cel = cel + [""] * (len(entetes) - len(cel))
            d = {n: cel[i] for i, n in enumerate(noms)}
            if d.get("offre"):
                d["etiquette"] = etiquette(d.get("etiquette", ""))
                res.append(d)
    return res


def retirees(texte):
    res = []
    for _, entetes, corps in tableaux(section_num(texte, 10)):
        noms = [plier(e) for e in entetes]
        for cel in corps:
            cel = cel + [""] * (len(entetes) - len(cel))
            d = {n: cel[i] for i, n in enumerate(noms)}
            if d.get("ancienne formulation"):
                res.append(d)
    return res


def cmd_exporter(args):
    p = Path(args.fichier).expanduser()
    if not p.exists():
        print(f"{args.fichier} : fichier introuvable", file=sys.stderr)
        return 3
    t = p.read_text(encoding="utf-8")
    ident, contraintes = faits(t, 1), faits(t, 8)
    if not any(v[0] for v in ident.values()):
        print("entreprise.md est vide : rien à exporter. Lance d'abord /fondation-entreprise.", file=sys.stderr)
        return 3
    o, r = offres(t), retirees(t)
    nom = rendre(chercher(ident, "nom commercial"))
    phrase = rendre(chercher(ident, "ce que nous faisons"))
    site = rendre(chercher(ident, "site"))
    entete = (f"<!-- Pré-remplissage depuis la Fondation (entreprise.md), le {dt.date.today().isoformat()}. "
              "Brouillon : relis-le, complète les {{…}}, puis colle-le toi-même. -->")
    out = [entete, ""]

    if args.vers == "seo":
        out += ["## 1. Le site", "",
                f"- **Nom de l'entreprise :** {nom}",
                f"- **URL :** {site}",
                f"- **Ce qu'elle vend, en une phrase :** {phrase}",
                f"- **Langue(s) et pays visés :** {rendre(chercher(ident, 'pays et langues'))}", "",
                "## 2. Le secteur", "",
                "- **YMYL ?** {{à compléter : oui / non}} (secteur réglementé déclaré dans la Fondation : "
                f"{rendre(chercher(contraintes, 'secteur reglemente'))})",
                f"- **Ce qu'il ne faut jamais affirmer :** {rendre(chercher(contraintes, 'ce qu'))}",
                f"- **Mentions obligatoires :** {rendre(chercher(contraintes, 'mentions obligatoires'))}", "",
                "## 6. Les règles maison (extrait)", "",
                "- **Mots interdits en plus de la liste anti-IA :** "
                + (" ; ".join(x["ancienne formulation"] for x in r) or "{{à compléter}}"), "",
                "## 7. Les données produit", "",
                "| Fait | Valeur | Source (page, document, date) | Étiquette |",
                "|---|---|---|---|"]
        for x in o:
            valeur = " ; ".join(v for v in (x.get("ce que c'est", ""), x.get("pour qui", ""), x.get("format et prix", "")) if v)
            source = ", ".join(v for v in (x.get("source", ""), x.get("au", "")) if v)
            out.append(f"| {x['offre']} | {valeur} | {source} | {x['etiquette'] or 'À CONFIRMER'} |")
    else:
        out += ["## Qui nous sommes", "",
                "| Fait | Valeur | Étiquette | Au | Source |",
                "|---|---|---|---|---|"]
        for libelle, cle in (("Nom", "nom commercial"), ("Ce que nous faisons, en une phrase", "ce que nous faisons"),
                             ("Site", "site")):
            f = chercher(ident, cle)
            if f and f[0]:
                out.append(f"| {libelle} | {f[0]} | {f[1] or 'À CONFIRMER'} | {f[2]} | entreprise.md, {f[3]} |")
            else:
                out.append(f"| {libelle} | {{{{à compléter}}}} | | | |")
        out.append("| Page LinkedIn | {{à compléter}} | | | |")
        out += ["", "## Offres", "",
                "| Offre | Ce que c'est | Format et prix | Étiquette | Au | Page |",
                "|---|---|---|---|---|---|"]
        for x in o:
            quoi = x.get("ce que c'est", "")
            out.append(f"| {x['offre']} | {quoi} | {x.get('format et prix', '')} "
                       f"| {x['etiquette'] or 'À CONFIRMER'} | {x.get('au', '')} | {x.get('source', '')} |")
        out += ["", "## Hors limites (extrait)", "",
                f"- **Ce qu'on n'affirme jamais :** {rendre(chercher(contraintes, 'ce qu'))}",
                f"- **Mentions obligatoires :** {rendre(chercher(contraintes, 'mentions obligatoires'))}"]
    out += ["", "## Formulations retirées", "",
            "| Ancienne formulation | Retirée le | Remplacée par |", "|---|---|---|"]
    for x in r:
        out.append(f"| {x['ancienne formulation']} | {x.get('retiree le', '')} | {x.get('remplacee par', '')} |")
    print("\n".join(out))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("etat", help="compter ce qui est vraiment rempli")
    e.add_argument("fichiers", nargs="+")
    e.add_argument("--aujourdhui", help="date du jour (AAAA-MM-JJ), pour les tests")
    e.add_argument("--jours", type=int, default=90, help="âge maximal d'un fait LIVE (défaut : 90)")
    e.add_argument("--json", action="store_true")
    x = sub.add_parser("exporter", help="préparer un brouillon pour le pack SEO ou LinkedIn")
    x.add_argument("--vers", choices=["seo", "linkedin"], required=True)
    x.add_argument("fichier")
    a = ap.parse_args(argv)
    return cmd_etat(a) if a.cmd == "etat" else cmd_exporter(a)


if __name__ == "__main__":
    sys.exit(main())
