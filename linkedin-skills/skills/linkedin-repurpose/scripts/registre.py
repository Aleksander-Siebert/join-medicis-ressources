#!/usr/bin/env python3
"""registre.py : découper une source en posts qui tiennent seuls, sans republier la même idée.

  decouper --fichier source.txt [--type video|podcast|article|newsletter|tweet|fil|instagram|conference|appel]
           [--journal journal.md] [--source "nom de la source"]
      Coupe la source en unités et note chacune sur 100 (4 × 25) :
        longueur entre 240 et 2 400 caractères ; pas de renvoi pendant
        (« Cela », « Comme vu plus haut », « Donc »…) ; une preuve (chiffre,
        durée, montant) ; au moins 3 phrases. Un renvoi pendant ou moins de
        3 phrases disqualifient l'unité.
      Compte ce que la source contient (affirmations, chiffres, histoires,
      mécanismes, erreurs, phrases citables), propose un format, signale les
      traces de la plateforme d'origine et les idées déjà publiées
      (registre de journal.md). Code 0 unités utilisables, 2 toutes faibles,
      3 rien ne tient seul (« c'est un post, pas une série »).

  verifier --idee "l'idée en une phrase" --journal journal.md
      L'idée a-t-elle déjà été publiée ? Moins de 90 jours, ou déjà 2 fois en
      8 mois : bloquant (code 3) ; entre 90 jours et 8 mois : attention
      (code 2), seulement avec un angle neuf.

  noter --idee "…" --source "…" --format texte [--lien "…"] [--date 2026-10-06] --journal journal.md
      Ajoute la ligne au registre de journal.md (« Idées déjà utilisées »),
      après le « oui » de l'utilisateur.

D'après repurpose_splitter.py et repurposing_discipline.md (alirezarezvani,
claude-skills, MIT) et linkedin-repurposer (Serge Bulaev, MIT), réécrits en
français ; le registre vit dans journal.md, pas dans un fichier à part.
Sans dépendance.
"""

import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

MIN_UNITE, MAX_UNITE = 240, 2400
PENDANT = re.compile(r"^(?:cela|ceci|ca|ce|ces|cette|cet|celui-ci|celle-ci|ceux-ci|il|elle|ils|elles|donc|mais|et|"
                     r"ainsi|en effet|par ailleurs|ensuite|enfin|de plus|en outre|du coup|bref|pour conclure|"
                     r"comme (?:vu|dit|evoque|mentionne|explique) (?:plus haut|precedemment|avant)|"
                     r"comme je (?:le )?disais|on l'a vu|nous l'avons vu|le premier|le second|la premiere|la seconde|"
                     r"au passage|d'ailleurs|resultat|la suite|voila pourquoi)\b")
PREUVE = re.compile(r"\d+(?:[,.]\d+)?\s*(?:%|€|k€|m€|euros?|x\b|×|min\b|minutes?|h\b|heures?|jours?|semaines?|mois|ans?|"
                    r"clients?|personnes?|appels?|leads?|posts?|abonnes?|salaries?|commandes?|devis)|\b(?:19|20)\d{2}\b|\d{2,}")
HISTOIRE = re.compile(r"\b(?:j'ai|nous avons|on a|je me suis|ce jour-la|le jour ou|l'an dernier|en (?:janvier|fevrier|mars|avril|"
                      r"mai|juin|juillet|aout|septembre|octobre|novembre|decembre)|quand j'|quand on|je pensais|on pensait|"
                      r"il m'a dit|elle m'a dit|m'a repondu)\b")
ETAPES = re.compile(r"(?m)^\s*(?:\d+[.)]|[-*•]|etape \d)|\b(?:premiere etape|deuxieme etape|d'abord|ensuite|puis|enfin)\b")
AVIS = re.compile(r"\b(?:il faut|il ne faut pas|faux|surcote|sous-estime|mythe|arretez|arrete de|personne ne|la plupart|"
                  r"la vraie raison|je ne crois pas|on se trompe|contrairement a|a tort)\b")
ERREUR = re.compile(r"\b(?:erreur|rate|on s'est trompe|je me suis trompee?|echec|echoue|perdu|j'aurais du|on aurait du|"
                    r"regrette|mauvaise decision|on a coupe le mauvais)\b")
TRACES = [
    (r"lien (?:en|dans (?:la|ma)) bio", "« lien en bio » (Instagram, TikTok)"),
    (r"abonnez-vous|abonne-toi|activez la cloche|like et partage|likez", "appel à s'abonner d'une autre plateforme"),
    (r"(?<![\w.])@\w{2,}", "pseudo @ d'une autre plateforme"),
    (r"(?:#\w+\s*){4,}", "mur de hashtags"),
    (r"\b(?:dans (?:cette|ma derniere|la) video|dans cet episode|dans ce podcast|dans ma newsletter|comme je le disais (?:en|dans)|"
     r"j'ai tweete|sur x|sur twitter|en story)\b", "renvoi au format d'origine (« dans cette vidéo »)"),
    (r"\b\d+/\d*\s*$|🧵|\bthread\b", "numérotation ou marqueur de fil (« 1/ », 🧵)"),
    (r"\b\d{1,2}:\d{2}(?::\d{2})?\b", "horodatage de transcription"),
    (r"\[(?:musique|rires|applaudissements|inaudible)\]|\b(?:euh|bah|hein|du coup du coup)\b", "tics d'oral de transcription"),
]
RENDEMENT = {"conference": "4 à 8", "video": "3 à 6", "webinaire": "3 à 6", "podcast": "3 à 6", "article": "3 à 6", "newsletter": "2 à 5",
             "fil": "1 à 3", "tweet": "1", "instagram": "1 à 2", "appel": "1 à 3"}
STOP = set("""a au aux avec ce ces cet cette c'est dans de des du elle en et eux il ils je j'ai la le les leur leurs lui ma mais me
meme mes moi mon ne nos notre nous on ou par pas pour qu que qui sa se ses si son sur ta te tes toi ton tu un une vos votre vous y
est sont etait ete etre avoir ai as avons avez ont fait faire plus tres tout tous toute toutes bien aussi comme quand alors donc
car ni cela ca ici sans sous chez entre vers apres avant pendant depuis encore deja jamais toujours rien peu beaucoup""".split())


def norme(t):
    t = unicodedata.normalize("NFKD", str(t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'")


def racines(t):
    out = set()
    for m in re.findall(r"[a-z0-9']+", norme(t)):
        m = m.split("'")[-1]
        if m in STOP or len(m) < 4 and not m.isdigit():
            continue
        r = re.sub(r"(?:s|x)$", "", m)
        r = re.sub(r"(?:ements?|ation|aient|ions|ent|ait|er|ee|es|e)$", "", r)
        out.add(r[:6])
    return out


def proximite(a, b):
    ra, rb = racines(a), racines(b)
    if not ra or not rb:
        return 0.0
    return len(ra & rb) / min(len(ra), len(rb))


def phrases(t):
    return [p for p in re.split(r"(?<=[.!?…])\s+", t.strip()) if len(p.split()) >= 3]


def couper(texte):
    """Coupe aux titres, puis regroupe les paragraphes jusqu'à une taille de post."""
    blocs, titre, courant = [], "", []
    for para in re.split(r"\n\s*\n", texte.strip()):
        p = para.strip()
        if not p:
            continue
        if re.match(r"^#{1,6}\s", p) or (len(p) < 90 and "\n" not in p and not p.endswith((".", "?", "!", ":"))):
            if courant:
                blocs.append((titre, "\n\n".join(courant)))
            titre, courant = re.sub(r"^#{1,6}\s*", "", p), []
            continue
        courant.append(p)
        if sum(len(c) for c in courant) >= 900:
            blocs.append((titre, "\n\n".join(courant)))
            courant = []
    if courant:
        blocs.append((titre, "\n\n".join(courant)))
    return blocs


def noter_unite(titre, texte):
    tn = norme(texte)
    n = len(texte)
    ph = phrases(texte)
    debut = norme(texte.lstrip("-*• \t"))[:60]
    pendant = bool(PENDANT.match(debut))
    preuve = bool(PREUVE.search(tn))
    score = 25 * (MIN_UNITE <= n <= MAX_UNITE) + 25 * (not pendant) + 25 * preuve + 25 * (len(ph) >= 3)
    manques = []
    if n < MIN_UNITE:
        manques.append(f"{n} caractères : trop court pour une affirmation et sa preuve")
    elif n > MAX_UNITE:
        manques.append(f"{n} caractères : à couper encore")
    if pendant:
        manques.append(f"commence par un renvoi (« {re.split(r'[,.;:]', texte.strip())[0][:25]} ») à ce que le lecteur n'a pas lu : "
                       "le retirer et réécrire l'ouverture")
    if not preuve:
        manques.append("aucune preuve chiffrée : un post d'avis, pas un post de preuve")
    if len(ph) < 3:
        manques.append(f"{len(ph)} phrase(s) : une note, pas un post")
    if ETAPES.search(tn) and len(re.findall(r"(?m)^\s*(?:\d+[.)]|[-*•])", texte)) >= 3:
        fmt = "carrousel (étapes) : /linkedin-carrousel"
    elif HISTOIRE.search(tn):
        fmt = "texte, récit (formules scene, erreur-datee)"
    elif preuve:
        fmt = "texte, chiffre d'abord (chiffre-d-abord, avant-apres)"
    elif AVIS.search(tn):
        fmt = "texte, avis (contre-pied, regle-impopulaire)"
    else:
        fmt = "texte"
    traces = [lib for motif, lib in TRACES if re.search(motif, tn if "@" not in motif and "#" not in motif else texte, re.M)]
    citables = [p for p in ph if 6 <= len(p.split()) <= 18 and not PENDANT.match(norme(p)[:40])]
    # pas de question en première ligne par défaut (règle du pack)
    citables.sort(key=lambda p: (p.rstrip().endswith("?"), not PREUVE.search(norme(p))))
    return {"titre": titre, "texte": texte, "caracteres": n, "score": score,
            "disqualifiee": pendant or len(ph) < 3, "manques": manques, "format": fmt, "traces": traces,
            "elements": {"affirmations": len(AVIS.findall(tn)), "chiffres": len(PREUVE.findall(tn)),
                         "histoires": len(HISTOIRE.findall(tn)), "mecanismes": 1 if ETAPES.search(tn) else 0,
                         "erreurs": len(ERREUR.findall(tn)), "phrases_citables": len(citables)},
            "accroche_possible": citables[0] if citables else (ph[0] if ph else "")}


def lire_registre(chemin):
    if not chemin or not Path(chemin).exists():
        return []
    texte = Path(chemin).read_text(encoding="utf-8")
    m = re.search(r"## Idées déjà utilisées[^\n]*\n(?:[^|\n][^\n]*\n|\n)*((?:\|.*\n?)+)", texte)
    if not m:
        return []
    out = []
    for l in m.group(1).splitlines()[2:]:
        cel = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cel) >= 2 and cel[1]:
            try:
                d = date.fromisoformat(cel[0][:10])
            except ValueError:
                d = None
            out.append({"date": d, "idee": cel[1], "source": cel[2] if len(cel) > 2 else "",
                        "format": cel[3] if len(cel) > 3 else ""})
    return out


def verifier(idee, registre, aujourd_hui=None, seuil=0.5):
    auj = aujourd_hui or date.today()
    proches = [dict(r, proximite=round(proximite(idee, r["idee"]), 2)) for r in registre]
    proches = [r for r in proches if r["proximite"] >= seuil]
    recents = [r for r in proches if r["date"] and (auj - r["date"]).days < 90]
    huit_mois = [r for r in proches if r["date"] and (auj - r["date"]).days < 243]
    if recents or len(huit_mois) >= 2:
        verdict, code = "DÉJÀ PUBLIÉE", 3
        raison = ("publiée il y a moins de 90 jours" if recents else f"déjà publiée {len(huit_mois)} fois en 8 mois") + \
                 " : l'audience s'en souviendra avant toi."
    elif proches:
        verdict, code = "REPRISE POSSIBLE", 2
        raison = "publiée il y a plus de 90 jours : seulement avec un angle neuf (un chiffre nouveau, un cas, ce qui a changé)."
    else:
        verdict, code, raison = "NOUVELLE", 0, "aucune idée proche dans le registre."
    return {"verdict": verdict, "code": code, "raison": raison,
            "proches": [{"date": r["date"].isoformat() if r["date"] else "", "idee": r["idee"], "proximite": r["proximite"]} for r in proches]}


def decouper(texte, type_=None, registre=(), source=""):
    unites = [noter_unite(t, x) for t, x in couper(texte)]
    for u in unites:
        deja = [r for r in registre if proximite(r["idee"], u["texte"]) >= 0.5]
        u["deja_publiee"] = [f"{r['date']} : {r['idee']}" for r in deja]
    total = {k: sum(u["elements"][k] for u in unites) for k in
             ("affirmations", "chiffres", "histoires", "mecanismes", "erreurs", "phrases_citables")}
    utilisables = [u for u in unites if not u["disqualifiee"] and u["score"] >= 75 and not u["deja_publiee"]]
    faibles = [u for u in unites if not u["disqualifiee"] and u["score"] < 75]
    utilisees_source = [r for r in registre if source and norme(source) in norme(r["source"])]
    if utilisables:
        verdict, code = "UNITÉS UTILISABLES", 0
    elif faibles:
        verdict, code = "UNITÉS FAIBLES", 2
    else:
        verdict, code = "RIEN NE TIENT SEUL", 3
    elements = sum(1 for k in ("affirmations", "chiffres", "histoires", "erreurs") if total[k]) + (1 if total["mecanismes"] else 0)
    return {"verdict": verdict, "code": code, "unites": unites, "utilisables": len(utilisables), "trouve": total,
            "mince": sum(total.values()) < 4 or elements < 2,
            "rendement_attendu": RENDEMENT.get(type_ or "", None),
            "source_deja_utilisee": len(utilisees_source),
            "rappel": "Chaque unité est une matière, pas un post. Il manque toujours la phrase que seul l'auteur peut écrire : "
                      "ce que ça a coûté, ce qu'il croyait, ce qu'il ferait autrement."}


def noter(chemin, idee, source, fmt, lien="", jour=None):
    p = Path(chemin)
    texte = p.read_text(encoding="utf-8") if p.exists() else "# journal.md\n"
    ligne = f"| {jour or date.today().isoformat()} | {idee.replace('|', '/')} | {source.replace('|', '/')} | {fmt} | {lien.replace('|', '/')} |"
    m = re.search(r"(## Idées déjà utilisées[^\n]*\n(?:[^|\n][^\n]*\n|\n)*)((?:\|.*\n?)+)", texte)
    if m:
        bloc = m.group(2)
        if not bloc.endswith("\n"):
            bloc += "\n"
        texte = texte[:m.start(2)] + bloc + ligne + "\n" + texte[m.end(2):]
    else:
        texte = texte.rstrip("\n") + "\n\n## Idées déjà utilisées (registre de réutilisation)\n\n" \
                "| date | idée (une phrase) | source | format | lien ou première ligne |\n|---|---|---|---|---|\n" + ligne + "\n"
    p.write_text(texte, encoding="utf-8")
    return ligne


def main():
    a = argparse.ArgumentParser(description="Découpe une source en posts, tient le registre des idées publiées.")
    sous = a.add_subparsers(dest="cmd", required=True)
    d = sous.add_parser("decouper")
    d.add_argument("--fichier", required=True)
    d.add_argument("--type", choices=sorted(RENDEMENT))
    d.add_argument("--journal")
    d.add_argument("--source", default="")
    d.add_argument("--json", action="store_true")
    v = sous.add_parser("verifier")
    v.add_argument("--idee", required=True)
    v.add_argument("--journal", required=True)
    v.add_argument("--json", action="store_true")
    n = sous.add_parser("noter")
    n.add_argument("--idee", required=True)
    n.add_argument("--source", required=True)
    n.add_argument("--format", required=True)
    n.add_argument("--lien", default="")
    n.add_argument("--date")
    n.add_argument("--journal", required=True)
    x = a.parse_args()
    try:
        if x.cmd == "noter":
            print("Ajouté au registre : " + noter(x.journal, x.idee, x.source, x.format, x.lien, x.date))
            return 0
        registre = lire_registre(x.journal)
        if x.cmd == "verifier":
            r = verifier(x.idee, registre)
            if x.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                print(f"IDÉE  {r['verdict']} · {r['raison']}")
                for p in r["proches"]:
                    print(f"  · {p['date']} : « {p['idee']} » (proximité {str(p['proximite']).replace('.', ',')})")
            return r["code"]
        r = decouper(Path(x.fichier).read_text(encoding="utf-8"), x.type, registre, x.source)
    except OSError as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    if x.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return r["code"]
    t = r["trouve"]
    print(f"SOURCE  {r['verdict']} · {len(r['unites'])} unités, {r['utilisables']} utilisable(s)"
          + (f" · rendement habituel pour ce type : {r['rendement_attendu']}" if r["rendement_attendu"] else ""))
    print(f"  TROUVÉ  {t['affirmations']} affirmation(s), {t['chiffres']} chiffre(s), {t['histoires']} histoire(s), "
          f"{t['mecanismes']} mécanisme(s), {t['erreurs']} erreur(s), {t['phrases_citables']} phrase(s) citable(s)")
    if r["mince"]:
        print("  ! Source mince : moins de 4 éléments. Les posts qu'on en tirera le seront aussi.")
    if r["source_deja_utilisee"] >= 4:
        print(f"  ! Source déjà utilisée {r['source_deja_utilisee']} fois : une source porte un mois, pas un trimestre.")
    for i, u in enumerate(r["unites"], 1):
        etat = "écartée" if u["disqualifiee"] else "déjà publiée" if u["deja_publiee"] else f"{u['score']}/100"
        print(f"\n  [{i}] {u['titre'] or '(sans titre)'} · {etat} · {u['caracteres']} car. · {u['format']}")
        print(f"      accroche possible : « {u['accroche_possible'][:100]} »")
        for m in u["manques"]:
            print(f"      - {m}")
        for tr in u["traces"]:
            print(f"      ! trace à retirer : {tr}")
        for dp in u["deja_publiee"]:
            print(f"      ! déjà publiée : {dp}")
    print(f"\n  {r['rappel']}")
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
