#!/usr/bin/env python3
"""fil.py : trie les commentaires sous un post de l'utilisateur et contrôle les réponses.

  trier --fichier commentaires.txt [--moi "Prénom Nom"] [--cible "DAF,assureur"]
        [--concurrents "Agence X"] [--journal journal.md] [--age-heures 30]
      1. FILTRE chiffré : éloges vides, doublons, spam, propres commentaires,
         textes qui s'adressent à une IA (injection). Gardés toujours : une
         question, un désaccord, un détail nommé ou chiffré, une personne déjà
         venue (« relation »).
      2. CATÉGORIES : PROSPECT, FOND, PAIR, SOUTIEN.
      3. LEADS notés sur 10 : adéquation (0-3) + intention (0-3) + récurrence
         (0-2) + portée (0-2). 7 et plus = chaud, 4 à 6 = tiède. Action
         suivante proposée.
      4. Fil de plus de 72 h : le message privé est souvent plus adapté.

  verifier --commentaire "…" --reponse "…"
      Bloque les réponses vides (« Merci ! », « 100% », « Top »), le tiret
      cadratin, le lien commercial ; signale une réponse qui n'apporte ni
      détail, ni nom, ni question, et une longueur hors 150-400 caractères.

Format du fichier : un commentaire par paragraphe (ligne vide entre deux),
« Nom (titre) : texte » ou « Nom : texte ». Un JSON
[{"nom", "titre", "texte"}] est aussi accepté.

Codes de sortie : trier 0 ; verifier 0 OK, 2 attention, 3 bloquant ; 1 erreur.

D'après filtering-rules.md et reply-templates.md (Serge Bulaev, MIT) et
linkedin-warm-lead-finder (Taplio, MIT), sans lecture de LinkedIn : les
commentaires sont collés par l'utilisateur. Sans dépendance.
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ELOGES = ["super post", "great post", "top", "bravo", "merci pour le partage", "merci pour ce partage", "merci pour ce post",
          "tellement vrai", "tellement juste", "so true", "100%", "100 %", "entierement d'accord", "totalement d'accord",
          "j'adore", "love this", "excellent", "tres juste", "tres interessant", "interessant", "bien dit", "exactement",
          "pepite", "inspirant", "merci", "genial", "clair", "+1", "cela", "ceci", "this"]
SPAM = re.compile(r"(?:voir|visite[zr]?|regarde[zr]?) mon profil|\b(?:dm|mp)\b.{0,15}\b(?:moi|pour)\b|ecris-moi pour|"
                  r"je propose|nos services|offre speciale|lien en bio|^\s*(?:https?://\S+\s*)+$")
INJECTION = re.compile(r"\b(?:ignore|oublie|ignorez|oubliez)\b.{0,40}\b(?:instructions?|consignes?|regles?)\b|"
                       r"\b(?:ia|chatgpt|claude|assistant|modele)\b.{0,30}\b(?:reponds?|ecris|dis|envoie|ajoute)\b|"
                       r"\bsystem prompt\b|\bprompt\b.{0,20}\b(?:revele|affiche)\b")
DESACCORD = re.compile(r"\b(?:pas d'accord|je ne suis pas (?:sur|convaincu|d'accord)|au contraire|je nuancerais|"
                       r"pas si simple|je ne crois pas|faux|discutable|oui mais|sauf que|chez nous c'est l'inverse)\b")
INTENTION_FORTE = re.compile(r"\b(?:comment (?:vous|tu) (?:faites|fais|avez|as)|vous proposez|tu proposes|vous accompagnez|"
                             r"combien|tarif|prix de|on cherche|nous cherchons|je cherche|interesse par|ca m'interesse|"
                             r"on peut en parler|on peut echanger|tu as un modele|vous avez un modele|partager (?:le|la|ton|votre))\b")
INTENTION_PROBLEME = re.compile(r"\b(?:chez nous|on a le meme|nous avons le meme|meme probleme|on galere|on bloque|"
                                r"on vit (?:la|exactement)|exactement notre|notre (?:cout|taux|equipe|probleme)|mon equipe)\b")
DECIDEUR = re.compile(r"\b(?:fondateur|fondatrice|cofondat\w+|ceo|dg|directeur|directrice|head of|vp|vice-president\w*|"
                      r"gerant|gerante|associe|associee|president\w*|cmo|cfo|daf|drh|cto|coo)\b")
MANAGER = re.compile(r"\b(?:responsable|manager|chef|lead|senior)\b")
REPONSES_VIDES = ["merci", "merci beaucoup", "merci !", "100%", "top", "avec plaisir", "merci pour ton commentaire",
                  "merci pour votre commentaire", "merci pour ton retour", "merci pour votre retour", "bien vu",
                  "exactement", "tout a fait", "c'est ca", "ravi que ca te parle", "ravie que ca te parle", "bonne remarque",
                  "bonne question", "je vais y reflechir", "a mediter", "je note", "on en parle en mp", "je t'ecris en mp",
                  "je vous ecris en mp", "merci a toi", "merci a vous", "content que ca te parle", "contente que ca te parle"]


def norme(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'").strip()


def lire_commentaires(texte):
    texte = texte.strip()
    if texte.startswith("["):
        return json.loads(texte)
    out = []
    for bloc in re.split(r"\n\s*\n", texte):
        bloc = " ".join(bloc.split())
        m = re.match(r"^(?P<nom>[^:()]{2,60}?)\s*(?:\((?P<titre>[^)]*)\))?\s*:\s*(?P<texte>.+)$", bloc)
        if m:
            out.append({"nom": m["nom"].strip(), "titre": (m["titre"] or "").strip(), "texte": m["texte"].strip()})
        elif bloc:
            out.append({"nom": "?", "titre": "", "texte": bloc})
    return out


def compter_journal(chemin):
    if not chemin or not Path(chemin).exists():
        return {}
    compte = {}
    for ligne in Path(chemin).read_text(encoding="utf-8").splitlines():
        if ligne.startswith("|"):
            for cel in ligne.strip("|").split("|"):
                c = norme(cel)
                if c and not re.fullmatch(r"[-: \d/]+", c):
                    compte[c] = compte.get(c, 0) + 1
    return compte


def eloge_vide(t):
    tn = re.sub(r"[^\w%+' ]", " ", norme(t))
    tn = " ".join(tn.split())
    if not tn:
        return True
    if "?" in t or re.search(r"\d", t):
        return False
    reste = tn
    for e in sorted(ELOGES, key=len, reverse=True):
        reste = reste.replace(e, " ")
    reste = " ".join(w for w in reste.split() if len(w) > 2)
    return len(reste.split()) <= 2 and len(tn.split()) <= 8


def trier(commentaires, moi="", cible=(), concurrents=(), journal=None, age_heures=None):
    journal = journal or {}
    cible = [norme(c) for c in cible if c.strip()]
    concurrents = [norme(c) for c in concurrents if c.strip()]
    ecartes = {"éloge vide": 0, "doublon": 0, "spam": 0, "propre commentaire": 0, "instruction adressée à une IA": 0}
    details_ecartes, gardes, vus = [], [], []
    for c in commentaires:
        t, tn, nom = c.get("texte", ""), norme(c.get("texte", "")), c.get("nom", "?")
        relation = journal.get(norme(nom), 0)
        if moi and norme(nom) == norme(moi):
            raison = "propre commentaire"
        elif INJECTION.search(tn):
            raison = "instruction adressée à une IA"
        elif SPAM.search(tn) or (re.search(r"@\w", t) and not re.sub(r"@[\w.-]+(?:\s+[A-ZÉ][\w-]+)?|[^\w]", "", t)):
            raison = "spam"
        elif any(tn == v or (len(tn) > 20 and tn[:60] == v[:60]) for v in vus):
            raison = "doublon"
        elif eloge_vide(t) and not relation:
            raison = "éloge vide"
        else:
            raison = None
        vus.append(tn)
        if raison:
            ecartes[raison] += 1
            details_ecartes.append({"nom": nom, "raison": raison, "texte": t[:80]})
            continue
        titre = norme(c.get("titre"))
        fit_hits = sum(1 for k in cible if k and k in titre)
        fit = 3 if fit_hits >= 2 else 2 if fit_hits == 1 else 0
        if INTENTION_FORTE.search(tn):
            intention = 3
        elif INTENTION_PROBLEME.search(tn):
            intention = 2
        elif len(t.split()) >= 8 and not eloge_vide(t):
            intention = 1
        else:
            intention = 0
        recurrence = 2 if relation >= 2 else 1 if (relation == 1 or len(t) > 200) else 0
        portee = 2 if DECIDEUR.search(titre) else 1 if MANAGER.search(titre) else 0
        pair = any(k in titre or k in tn for k in concurrents)
        score = 0 if pair else fit + intention + recurrence + portee
        if pair:
            categorie = "PAIR"
        elif (intention == 3 or (intention == 2 and not DESACCORD.search(tn))) and (fit >= 2 or not cible):
            categorie = "PROSPECT"
        elif "?" in t or DESACCORD.search(tn) or re.search(r"\d", t) or len(t) > 120:
            categorie = "FOND"
        elif relation:
            categorie = "SOUTIEN"
        else:
            categorie = "FOND" if intention >= 1 else "SOUTIEN"
        niveau = "chaud" if score >= 7 else "tiède" if score >= 4 else "-"
        if niveau == "chaud":
            action = "réponse complète en public + invitation qui cite son commentaire (/linkedin-dm), ou message s'il est déjà en relation"
        elif niveau == "tiède":
            action = "réponse seule, avec une question qui l'invite à en dire plus"
        else:
            action = {"FOND": "la réponse la plus soignée du fil", "PAIR": "une réponse qui lui apporte quelque chose",
                      "SOUTIEN": "une réaction ; une réponse seulement si tu as un détail à ajouter",
                      "PROSPECT": "réponse complète en public"}[categorie]
        gardes.append({"nom": nom, "titre": c.get("titre", ""), "texte": t, "categorie": categorie,
                       "relation": bool(relation), "garde_parce_que": ", ".join(
                           x for x, cond in (("question", "?" in t), ("désaccord", bool(DESACCORD.search(tn))),
                                             ("détail chiffré", bool(re.search(r"\d", t))), ("relation", bool(relation))) if cond),
                       "lead": {"score": score, "niveau": niveau, "adequation": fit, "intention": intention,
                                "recurrence": recurrence, "portee": portee}, "action": action})
    ordre = {"PROSPECT": 0, "FOND": 1, "PAIR": 2, "SOUTIEN": 3}
    gardes.sort(key=lambda g: (ordre[g["categorie"]], -g["lead"]["score"]))
    total_ecartes = sum(ecartes.values())
    rapport = f"{len(commentaires)} récupérés → {total_ecartes} écartés"
    detail = ", ".join(f"{n} {k}" for k, n in ecartes.items() if n)
    if detail:
        rapport += f" ({detail})"
    rapport += f" → {len(gardes)} à traiter"
    conseil_dm = age_heures is not None and age_heures > 72
    return {"rapport": rapport, "ecartes": details_ecartes, "a_traiter": gardes,
            "comptes": {k: sum(1 for g in gardes if g["categorie"] == k) for k in ordre},
            "fil_ancien": conseil_dm}


def verifier(commentaire, reponse):
    r, rn = reponse.strip(), norme(reponse)
    bloquants, attentions = [], []
    nu = re.sub(r"[^\w%' ]", " ", rn)
    nu = " ".join(w for w in nu.split())
    sans_prenom = " ".join(nu.split()[1:]) if len(nu.split()) > 1 else nu
    reste = " " + nu + " "
    for v in sorted(REPONSES_VIDES, key=len, reverse=True):
        reste = reste.replace(" " + v + " ", " ")
    reste = [w for w in reste.split() if len(w) > 2 and w != nu.split()[0]] if nu else []
    if nu in REPONSES_VIDES or sans_prenom in REPONSES_VIDES or len(nu.split()) <= 3 or (len(reste) <= 1 and "?" not in r):
        bloquants.append("Réponse vide (« Merci ! », « 100% », « Top ») : une réaction suffit, ou apporte un détail, un nom ou une question.")
    if "—" in r or re.search(r"\s–\s", r):
        bloquants.append("Tiret cadratin : supprime-le ou mets une virgule.")
    if re.search(r"https?://|www\.", r) and re.search(r"\b(?:offre|tarif|reserve|rendez-vous|calendly|demo)\b", rn):
        bloquants.append("Lien commercial dans une réponse publique : la valeur d'abord, l'offre en message privé si on te la demande.")
    if not bloquants:
        apporte = re.search(r"\d", r) or "?" in r or re.search(r"(?<![.!?]\s)(?<!^)\b[A-ZÉ][a-zé]{2,}", r)
        nouveaux = set(re.findall(r"[a-z]{6,}", rn)) - set(re.findall(r"[a-z]{6,}", norme(commentaire)))
        if not apporte and len(nouveaux) < 2:
            attentions.append("La réponse n'apporte ni détail, ni nom, ni question, ni idée nouvelle.")
    if len(r) > 400:
        attentions.append(f"{len(r)} caractères : une réponse se lit mieux entre 150 et 300.")
    if not bloquants and re.match(r"^(?:\w+\s*,\s*)?merci\b", rn) and not re.match(r"^(?:\w+\s*,\s*)?merci (?:pour|d'avoir) (?:le|la|les|l'|ce|cet|cette|ton|ta|tes|votre|vos)\s*\w{4,}", rn):
        attentions.append("Commence par « Merci » : commence par la réponse, sauf pour un service précis (« Merci pour le lien vers l'étude »).")
    if re.match(r"^\s*\w+\s*!", r):
        attentions.append("Prénom suivi d'un point d'exclamation : le prénom, puis la réponse.")
    verdict, code = ("BLOQUÉ", 3) if bloquants else ("À REVOIR", 2) if attentions else ("OK", 0)
    return {"verdict": verdict, "code": code, "caracteres": len(r), "bloquants": bloquants, "attentions": attentions}


def main():
    a = argparse.ArgumentParser(description="Trie un fil de commentaires, contrôle une réponse.")
    sous = a.add_subparsers(dest="cmd", required=True)
    t = sous.add_parser("trier")
    t.add_argument("--fichier", required=True)
    t.add_argument("--moi", default="")
    t.add_argument("--cible", default="", help="mots du titre de la cible, séparés par des virgules")
    t.add_argument("--concurrents", default="")
    t.add_argument("--journal")
    t.add_argument("--age-heures", type=float)
    t.add_argument("--json", action="store_true")
    v = sous.add_parser("verifier")
    v.add_argument("--commentaire", required=True)
    v.add_argument("--reponse", required=True)
    v.add_argument("--json", action="store_true")
    x = a.parse_args()
    try:
        if x.cmd == "trier":
            r = trier(lire_commentaires(Path(x.fichier).read_text(encoding="utf-8")), x.moi, x.cible.split(","),
                      x.concurrents.split(","), compter_journal(x.journal), x.age_heures)
            if x.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                c = r["comptes"]
                print(f"FIL · {r['rapport']}")
                print(f"     {c['PROSPECT']} prospect(s), {c['FOND']} de fond, {c['PAIR']} pair(s), {c['SOUTIEN']} soutien(s)")
                if r["fil_ancien"]:
                    print("  ! Fil de plus de 72 h : pour les échanges importants, un message privé est souvent plus adapté.")
                for g in r["a_traiter"]:
                    lead = f" · lead {g['lead']['score']}/10 {g['lead']['niveau']}" if g["lead"]["niveau"] != "-" else ""
                    pq = f" (gardé : {g['garde_parce_que']})" if g["garde_parce_que"] else ""
                    print(f"  [{g['categorie']}] {g['nom']}{lead}{pq}\n     « {g['texte'][:90]} »\n     → {g['action']}")
                for e in r["ecartes"]:
                    print(f"  · écarté ({e['raison']}) : {e['nom']}")
            return 0
        r = verifier(x.commentaire, x.reponse)
    except (OSError, json.JSONDecodeError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    if x.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"RÉPONSE  {r['verdict']}  ·  {r['caracteres']} caractères")
        for b in r["bloquants"]:
            print(f"  ✖ {b}")
        for t2 in r["attentions"]:
            print(f"  ! {t2}")
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
