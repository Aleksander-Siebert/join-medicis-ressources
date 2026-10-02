#!/usr/bin/env python3
"""boite.py : trie la messagerie LinkedIn collée par l'utilisateur.

  trier --fichier messages.txt [--categories "prospect,recruteur,pair,demande,partenaire,spam"]
        [--offre "mots de l'offre, séparés par des virgules"] [--json]
      1. Repère les séquences automatisées et dit quels indices les trahissent
         (message quelques minutes après l'acceptation, variable oubliée,
         « petite question » sans question, lien d'agenda au premier message,
         relance sans élément nouveau, même modèle chez plusieurs expéditeurs,
         offre de leads ou de visibilité…). 2 indices ou plus : SPAM.
      2. Range le reste en 6 catégories au plus (configurables dans
         contexte.md) : prospect, recruteur, candidat, partenaire, demande,
         pair, spam. Comptes d'abord, puis délai de réponse par catégorie.

  crm --fichier messages.txt [--offre "…"] [--format csv|tsv]
      Prépare les prospects pour le CRM (HubSpot, Pipedrive, tableur) : une
      ligne par personne avec la source, la date et la base légale à valider.
      Rien n'est envoyé au CRM : l'utilisateur importe ou colle.

Format du fichier : un fil par bloc, blocs séparés par une ligne « --- ».

  De : Paul Martin (CEO · Agence Leadz)
  Accepté : 2026-09-30 10:02          (facultatif : acceptation de l'invitation)
  Reçu : 2026-09-30 10:05
  Bonjour Paul, petite question…
  Reçu : 2026-10-04 10:05             (un 2e message du même expéditeur)
  Je me permets de relancer…
  Moi : …                              (facultatif : une réponse de l'utilisateur)

Un JSON [{"de", "titre", "accepte", "messages": [{"recu", "texte", "moi"}]}]
est aussi accepté.

Codes de sortie : 0, ou 1 en cas d'erreur.

D'après li-inbox (Jake Schincariol, MIT) et di-li-inbox (Joshua, Design
Industries, MIT) : 6 catégories, comptes d'abord, indices de séquence,
signalement CRM le jour même. Sans dépendance. Rien n'est lu sur LinkedIn.
"""

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

TOUTES = ["prospect", "recruteur", "candidat", "partenaire", "demande", "pair", "spam"]
DEFAUT = ["prospect", "recruteur", "pair", "demande", "partenaire", "spam"]
DELAIS = {"prospect": "aujourd'hui, réponse complète", "partenaire": "cette semaine",
          "recruteur": "sous 48 h si le poste t'intéresse, une ligne sinon", "candidat": "cette semaine",
          "demande": "cette semaine si c'est précis et rapide, refus net sinon", "pair": "cette semaine",
          "spam": "archiver, aucune réponse"}

VARIABLE = re.compile(r"\{\{?\s*\w+\s*\}?\}|\[(?:prenom|nom|entreprise|societe|first_?name|company)\]|%\w+%|<prenom>", re.I)
PETITE_QUESTION = re.compile(r"\b(?:petite|rapide|courte) question\b|\bquick question\b")
FLATTERIE = re.compile(r"\b(?:votre|ton) profil (?:a retenu|m'a interpelle|est (?:tres )?(?:interessant|impressionnant))|"
                       r"\bj'ai (?:vu|remarque) que (?:vous|tu) (?:etes|etiez|es|travaillez|travailles) (?:dans|chez)\b|"
                       r"\ben parcourant (?:votre|ton) profil\b|\bvotre parcours (?:est|m'a)\b")
AGENDA = re.compile(r"calendly|cal\.com|zcal|meetings\.hubspot|tidycal|youcanbook|\breservez?\b.{0,20}\bcreneau|\bprenez? un creneau\b")
RELANCE_VIDE = re.compile(r"\b(?:je me permets de (?:relancer|revenir)|petite relance|je remonte (?:mon|ce) message|"
                          r"suite a mon (?:precedent|dernier) message|je reviens vers (?:vous|toi)|"
                          r"avez-vous (?:eu le temps|pu) (?:de )?(?:lire|regarder|voir)|sans (?:nouvelle|reponse) de votre part)\b")
OFFRE_SPAM = re.compile(r"\b(?:generer|genere|garantir|garantis?)\b.{0,30}\b(?:leads?|rendez-vous|rdv|prospects?|clients?)\b|"
                        r"\b(?:\d+|des dizaines de) (?:leads?|rendez-vous|rdv) (?:qualifies )?(?:par|chaque) (?:mois|semaine)\b|"
                        r"\b(?:booster|doubler|tripler|multiplier) (?:votre|ta) (?:visibilite|portee|chiffre|ca|croissance)\b|"
                        r"\b(?:developpeurs?|equipe) (?:offshore|a madagascar|en inde|nearshore)\b|"
                        r"\b(?:crypto|bitcoin|forex|trading|investissement garanti|revenu passif)\b|"
                        r"\b(?:sans engagement|offre limitee|places limitees|derniere chance)\b")
PROSPECT = re.compile(r"\b(?:vos services|votre offre|vos offres|vos tarifs|votre tarif|un devis|combien (?:coute|couterait|ca coute)|"
                      r"vous accompagnez|tu accompagnes|vous proposez|tu proposes|on cherche (?:quelqu'un|un prestataire|une agence|un consultant)|"
                      r"nous cherchons (?:quelqu'un|un prestataire|une agence|un consultant)|travailler ensemble|"
                      r"on a un (?:besoin|projet)|nous avons un (?:besoin|projet)|(?:votre|ton) aide (?:pour|sur)|"
                      r"pourriez-vous nous aider|tu pourrais nous aider|un accompagnement)\b")
RECRUTEUR = re.compile(r"\b(?:poste|cdi|cdd|freelance mission|opportunite professionnelle|je recrute|nous recrutons|on recrute|"
                       r"cabinet de recrutement|chasseur|talent acquisition|remuneration|salaire|package|fourchette|"
                       r"votre candidature|profil correspond)\b")
CANDIDAT = re.compile(r"\b(?:je postule|ma candidature|candidature spontanee|mon cv|rejoindre votre equipe|"
                      r"recrutez-vous|vous recrutez|un stage|une alternance)\b")
PARTENAIRE = re.compile(r"\b(?:partenariat|partenaire|co-organiser|coorganiser|webinaire commun|evenement commun|"
                        r"intervenir (?:a|lors)|table ronde|podcast|interview croisee|co-ecrire|collaboration)\b")
DEMANDE = re.compile(r"\b(?:un conseil|ton avis|votre avis|ton retour|votre retour|quelques minutes|15 minutes|20 minutes|30 minutes|"
                     r"un cafe|echanger avec (?:vous|toi)|mise en relation|me presenter a|me mettre en relation|"
                     r"(?:vous|te) solliciter|(?:une|des) recommandations?|relire|pourrais-tu|pourriez-vous)\b")
INJECTION = re.compile(r"\b(?:ignore|oublie|ignorez|oubliez)\b.{0,40}\b(?:instructions?|consignes?|regles?)\b|"
                       r"\b(?:ia|chatgpt|claude|assistant|agent|modele)\b.{0,40}\b(?:reponds?|repondez|envoie|envoyez|clique|cliquez|accepte|transfere)\b|"
                       r"\bsystem prompt\b")
FOND = re.compile(r"\d|\?|\b(?:ton post|votre post|ton article|votre article|j'ai lu|on a teste|chez nous|de notre cote)\b")


def norme(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'")


def date(t):
    for f in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y"):
        try:
            return datetime.strptime(t.strip(), f)
        except (ValueError, AttributeError):
            pass
    return None


def lire(texte):
    texte = texte.strip()
    if texte.startswith("["):
        return json.loads(texte)
    fils = []
    for bloc in re.split(r"^\s*---\s*$", texte, flags=re.M):
        if not bloc.strip():
            continue
        fil = {"de": "?", "titre": "", "accepte": "", "messages": []}
        courant = None
        for ligne in bloc.strip().splitlines():
            m = re.match(r"^\s*(De|Accepté|Accepte|Reçu|Recu|Moi)\s*:\s*(.*)$", ligne)
            if m and m[1] == "De":
                d = re.match(r"^(.*?)\s*(?:\((.*)\))?\s*$", m[2])
                fil["de"], fil["titre"] = d[1].strip(), (d[2] or "").strip()
            elif m and m[1] in ("Accepté", "Accepte"):
                fil["accepte"] = m[2].strip()
            elif m and m[1] in ("Reçu", "Recu"):
                courant = {"recu": m[2].strip(), "texte": "", "moi": False}
                fil["messages"].append(courant)
            elif m and m[1] == "Moi":
                courant = {"recu": "", "texte": m[2].strip(), "moi": True}
                fil["messages"].append(courant)
            else:
                if courant is None:
                    courant = {"recu": "", "texte": "", "moi": False}
                    fil["messages"].append(courant)
                courant["texte"] = (courant["texte"] + " " + ligne.strip()).strip()
        fils.append(fil)
    return fils


def _sans_noms(t, noms):
    tn = norme(t)
    for n in noms:
        for p in norme(n).split():
            if len(p) > 2:
                tn = re.sub(rf"\b{re.escape(p)}\b", " ", tn)
    return set(zip(*(lambda w: (w, w[1:]))(re.findall(r"[a-z']{3,}", tn))))


def indices(fil, autres):
    """Indices d'une séquence automatisée dans un fil."""
    out = []
    recus = [m for m in fil["messages"] if not m.get("moi")]
    if not recus:
        return out
    premier = norme(recus[0]["texte"])
    acc, r0 = date(fil.get("accepte", "")), date(recus[0].get("recu", ""))
    if acc and r0 and 0 <= (r0 - acc).total_seconds() <= 15 * 60:
        out.append(f"premier message {int((r0 - acc).total_seconds() // 60)} min après l'acceptation")
    tout = " ".join(norme(m["texte"]) for m in recus)
    if VARIABLE.search(" ".join(m["texte"] for m in recus)):
        out.append("variable de modèle oubliée")
    if PETITE_QUESTION.search(tout):
        out.append("« petite question »" + ("" if "?" in " ".join(m["texte"] for m in recus) else " sans question"))
    if FLATTERIE.search(tout):
        out.append("accroche générique (« votre profil a retenu… », « j'ai vu que vous êtes dans… »)")
    if AGENDA.search(premier):
        out.append("lien d'agenda dès le premier message")
    if OFFRE_SPAM.search(tout):
        out.append("offre de leads, de visibilité ou promesse chiffrée")
    if len(recus) >= 2:
        rel = [m for m in recus[1:] if RELANCE_VIDE.search(norme(m["texte"]))]
        if rel:
            out.append("relance sans élément nouveau")
        dates = [date(m.get("recu", "")) for m in recus]
        ecarts = [round((b - a).total_seconds() / 86400, 2) for a, b in zip(dates, dates[1:]) if a and b]
        if ecarts and all(abs(e - round(e)) < 0.02 for e in ecarts) and not any(m.get("moi") for m in fil["messages"]):
            out.append("relances à intervalle exact (" + ", ".join(f"J+{int(round(e))}" for e in ecarts) + ")")
    noms = [fil["de"]] + [a["de"] for a in autres]
    moi_bi = _sans_noms(recus[0]["texte"], noms)
    for a in autres:
        ar = [m for m in a["messages"] if not m.get("moi")]
        if not ar or not moi_bi:
            continue
        lui = _sans_noms(ar[0]["texte"], noms)
        if lui and len(moi_bi & lui) / min(len(moi_bi), len(lui)) > 0.6:
            out.append(f"même modèle que le message de {a['de']}")
            break
    return out


def categoriser(fil, actives, offre=()):
    t = norme(" ".join(m["texte"] for m in fil["messages"] if not m.get("moi")))
    titre = norme(fil.get("titre"))
    offre = [norme(o) for o in offre if o.strip()]
    scores = {
        "prospect": 3 * bool(PROSPECT.search(t)) + sum(1 for o in offre if o in t),
        "recruteur": 2 * bool(RECRUTEUR.search(t)) + bool(re.search(r"\b(?:recrut|talent|rh\b|chasseur)", titre)),
        "candidat": 2 * bool(CANDIDAT.search(t)),
        "partenaire": 2 * bool(PARTENAIRE.search(t)),
        "demande": 2 * bool(DEMANDE.search(t)),
    }
    cat, s = max(scores.items(), key=lambda kv: kv[1])
    if s == 0:
        cat = "pair" if FOND.search(t) else "demande" if "?" in t else "pair"
    if cat not in actives:
        repli = {"candidat": "demande", "partenaire": "pair", "recruteur": "demande", "demande": "pair", "pair": "demande"}
        cat = repli.get(cat, cat)
        if cat not in actives:
            cat = next(c for c in actives if c != "spam")
    return cat


def trier(fils, actives=None, offre=()):
    actives = [c for c in (actives or DEFAUT) if c in TOUTES][:6]
    if "spam" not in actives:
        actives = actives[:5] + ["spam"]
    sortie = []
    for i, fil in enumerate(fils):
        ind = indices(fil, fils[:i] + fils[i + 1:])
        if INJECTION.search(norme(" ".join(m["texte"] for m in fil["messages"] if not m.get("moi")))):
            ind = ["consigne adressée à une IA (ignorée, à signaler à l'utilisateur)"] + ind
            cat = "spam"
        elif len(ind) >= 2:
            cat = "spam"
        else:
            cat = categoriser(fil, actives, offre)
        recus = [m for m in fil["messages"] if not m.get("moi")]
        sortie.append({"de": fil["de"], "titre": fil.get("titre", ""), "categorie": cat, "indices": ind,
                       "a_repondu": any(m.get("moi") for m in fil["messages"]),
                       "dernier": recus[-1].get("recu", "") if recus else "",
                       "extrait": (recus[0]["texte"] if recus else "")[:110], "delai": DELAIS[cat]})
    comptes = {c: sum(1 for s in sortie if s["categorie"] == c) for c in actives}
    ordre = {c: i for i, c in enumerate(["prospect", "partenaire", "recruteur", "candidat", "demande", "pair", "spam"])}
    sortie.sort(key=lambda s: ordre[s["categorie"]])
    familles = {}
    for s in sortie:
        if s["categorie"] == "spam":
            cle = s["indices"][0] if s["indices"] else "démarchage"
            familles[cle] = familles.get(cle, 0) + 1
    return {"total": len(fils), "comptes": comptes, "fils": sortie, "spam_par_indice": familles}


def crm(fils, offre=(), fmt="csv"):
    r = trier(fils, offre=offre)
    lignes = []
    aujourd_hui = datetime.now().strftime("%Y-%m-%d")
    for s in r["fils"]:
        if s["categorie"] != "prospect":
            continue
        parts = s["de"].split()
        prenom, nom = (parts[0], " ".join(parts[1:])) if parts else ("", "")
        poste, entreprise = (s["titre"].split("·", 1) + [""])[:2] if "·" in s["titre"] else (s["titre"], "")
        recu = (date(s["dernier"]) or datetime.now()).strftime("%Y-%m-%d")
        lignes.append({"Prénom": prenom, "Nom": nom, "Poste": poste.strip(), "Entreprise": entreprise.strip(),
                       "Source": f"LinkedIn, message reçu le {recu}", "Date d'entrée": aujourd_hui,
                       "Base légale": "contact entrant, mesures précontractuelles ou intérêt légitime [à valider]",
                       "Note": s["extrait"], "Prochaine étape": "répondre aujourd'hui", "Échéance": aujourd_hui})
    buf = io.StringIO()
    if lignes:
        w = csv.DictWriter(buf, fieldnames=list(lignes[0]), delimiter="\t" if fmt == "tsv" else ";")
        w.writeheader()
        w.writerows(lignes)
    return buf.getvalue(), len(lignes)


def main():
    a = argparse.ArgumentParser(description="Trie une messagerie LinkedIn collée, prépare les prospects pour le CRM.")
    sous = a.add_subparsers(dest="cmd", required=True)
    t = sous.add_parser("trier")
    t.add_argument("--fichier", required=True)
    t.add_argument("--categories", default=",".join(DEFAUT))
    t.add_argument("--offre", default="")
    t.add_argument("--json", action="store_true")
    c = sous.add_parser("crm")
    c.add_argument("--fichier", required=True)
    c.add_argument("--offre", default="")
    c.add_argument("--format", choices=["csv", "tsv"], default="csv")
    x = a.parse_args()
    try:
        fils = lire(Path(x.fichier).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    if x.cmd == "crm":
        texte, n = crm(fils, x.offre.split(","), x.format)
        print(texte if n else "Aucun prospect à reporter.", end="" if n else "\n")
        return 0
    r = trier(fils, [c.strip().lower() for c in x.categories.split(",")], x.offre.split(","))
    if x.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    comptes = ", ".join(f"{n} {c.upper()}" for c, n in r["comptes"].items() if n)
    print(f"MESSAGERIE · {r['total']} fils · {comptes}")
    courant = None
    for s in r["fils"]:
        if s["categorie"] == "spam":
            continue
        if s["categorie"] != courant:
            courant = s["categorie"]
            print(f"\n{courant.upper()} ({r['comptes'][courant]}) · {DELAIS[courant]}")
        rep = " · déjà répondu" if s["a_repondu"] else ""
        ind = f" · ! {s['indices'][0]}" if s["indices"] else ""
        print(f"  {s['de']} ({s['titre']}){rep}{ind}\n     « {s['extrait']} »")
    if r["comptes"].get("spam"):
        print(f"\nSPAM ({r['comptes']['spam']}) · à archiver")
        for s in r["fils"]:
            if s["categorie"] == "spam":
                print(f"  {s['de']} : " + ("; ".join(s["indices"]) if s["indices"] else "démarchage"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
