#!/usr/bin/env python3
"""profil.py : contrôle un tone-of-voice.md et en fait un Skill « ma-voix ».

Deux commandes :

  verifier tone-of-voice.md [--aujourdhui AAAA-MM-JJ]
      Le fichier est-il complet et utilisable ? Sections présentes, 3 à 5
      traits avec un exemple cité, au moins 3 « jamais », bloc de mesures
      lisible, trous {{…}} restants, date de mise à jour (plus de 6 mois :
      à refaire), typographie française (tiret cadratin, « 15 % »,
      guillemets droits), journal tenu.

  ma-voix tone-of-voice.md --nom "Camille" [--exemples a.txt b.txt …]
          [--sortie DOSSIER] [--zip]
      Construit le dossier d'un Skill autonome qui écrit dans cette voix :
        ma-voix-<nom>/SKILL.md                  consignes et déclenchement
        ma-voix-<nom>/references/tone-of-voice.md
        ma-voix-<nom>/exemples/exemple-01.md …  vrais textes, coordonnées retirées
        ma-voix-<nom>/scripts/ecart.py, texte.py (contrôle chiffré, facultatif)
      Avec --zip, écrit aussi ma-voix-<nom>.zip, importable sur claude.ai
      (Personnaliser → Skills). Le nom suit la spécification Agent Skills :
      64 caractères au plus, minuscules, chiffres et tirets, égal au dossier ;
      description de 1 024 caractères au plus ; un seul SKILL.md.

Codes de sortie : 0 rien à revoir · 2 à revoir · 3 fichier inutilisable ·
1 erreur d'usage.

Idée du Skill généré qui « apprend par l'exemple » (lire de vrais textes
avant d'écrire) : houtini-ai/voice-analyser-mcp (Apache 2.0). Réécrit.
"""

import argparse
import datetime as dt
import os
import re
import shutil
import sys
import unicodedata
import zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import texte as tx  # noqa: E402

SECTIONS = [
    ("1", "en une phrase"), ("2", "ce que je suis"), ("3", "curseurs"), ("4", "regles"),
    ("5", "mes mots"), ("6", "jamais"), ("7", "tranche"), ("8", "canal"), ("9", "avant"),
    ("10", "extraits"), ("11", "questions"), ("12", "mesures"), ("13", "journal"),
]
PEREMPTION_JOURS = 183
NOM_SKILL = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


# ---------------------------------------------------------------------------
# Lecture du fichier
# ---------------------------------------------------------------------------

def sections(md):
    """{numéro: (titre, corps)} pour les titres « ## n. Titre »."""
    out, cle, titre, corps = {}, None, None, []
    for ligne in md.splitlines():
        m = re.match(r"^##\s+(\d+)\.?\s+(.*)$", ligne)
        if m:
            if cle:
                out[cle] = (titre, "\n".join(corps))
            cle, titre, corps = m.group(1), m.group(2).strip(), []
        elif cle:
            corps.append(ligne)
    if cle:
        out[cle] = (titre, "\n".join(corps))
    return out


def lignes_tableau(corps):
    lignes = [l for l in corps.splitlines() if l.strip().startswith("|")]
    donnees = []
    for l in lignes[2:]:  # en-tête et séparateur
        cellules = [c.strip() for c in l.strip().strip("|").split("|")]
        if any(c and not re.fullmatch(r"-+", c) for c in cellules):
            donnees.append(cellules)
    return donnees


def hors_code(md):
    return re.sub(r"```.*?```", "", md, flags=re.S)


def verifier(md, aujourdhui):
    erreurs, attention, infos = [], [], []
    if not md.strip():
        return {"verdict": "VIDE", "erreurs": ["fichier vide"], "attention": [], "infos": []}
    if not re.search(r"(?m)^#\s+Voix de\s+\S", md):
        attention.append("titre « # Voix de … » absent")
    secs = sections(md)
    for num, cle in SECTIONS:
        if num not in secs or cle not in tx.plier(secs[num][0]):
            erreurs.append(f"section {num} (« {cle} ») absente ou mal titrée")

    m = re.search(r"mise à jour le\s+(\d{4}-\d{2}-\d{2})", md)
    if not m:
        attention.append("date « mise à jour le AAAA-MM-JJ » absente")
    else:
        try:
            jours = (aujourdhui - dt.date.fromisoformat(m.group(1))).days
            if jours > PEREMPTION_JOURS:
                attention.append(f"voix mise à jour il y a {jours} jours : la refaire avec des textes récents")
            infos.append(f"mise à jour il y a {jours} jour(s)")
        except ValueError:
            attention.append(f"date illisible : {m.group(1)}")
    if not re.search(r"Version\s+\d+", md):
        attention.append("numéro de version absent")

    if "2" in secs:
        traits = [c for c in lignes_tableau(secs["2"][1]) if not all("{{" in x or not x for x in c)]
        traits = [c for c in traits if c and "{{" not in c[0]]
        if not 3 <= len(traits) <= 5:
            attention.append(f"{len(traits)} trait(s) en section 2 : il en faut 3 à 5")
        for c in traits:
            if not any("«" in x for x in c[3:] or c[-1:]):
                attention.append(f"trait « {c[0]} » sans exemple cité entre « »")
            if len(c) < 2 or not c[1] or "{{" in c[1]:
                attention.append(f"trait « {c[0]} » sans son « pas »")
    if "6" in secs:
        items = [l for l in secs["6"][1].splitlines() if l.strip().startswith(("-", "*")) and "{{" not in l]
        if len(items) < 3:
            attention.append(f"{len(items)} entrée(s) dans « Ce que je n'écris jamais » : au moins 3")
    if "13" in secs and not [c for c in lignes_tableau(secs["13"][1]) if c and "{{" not in c[0]]:
        attention.append("journal vide")

    bloc = tx.lire_bloc(md)
    if bloc is None:
        erreurs.append("bloc ```mesures``` absent : lance voix.py --bloc et colle-le en section 12")
    elif "version_mesures" not in bloc:
        erreurs.append("bloc de mesures incomplet (version_mesures absente)")
    else:
        infos.append(f"mesures : {bloc.get('textes')} textes, {bloc.get('mots')} mots, confiance {bloc.get('confiance')}")
        if bloc.get("confiance") == "faible":
            attention.append("confiance faible : redemander des textes écrits à la main")

    trous = re.findall(r"\{\{[^}]*\}\}", hors_code(md))
    if trous:
        attention.append(f"{len(trous)} trou(s) {{{{…}}}} à remplir ou à transformer en question ouverte")

    prose = hors_code(md)
    if "—" in prose:
        erreurs.append(f"{prose.count('—')} tiret(s) cadratin(s) : remplace par une virgule ou supprime")
    if re.search(r"\d[   ]%", prose):
        attention.append("pourcentage espacé (« 15 % ») : écris « 15% »")
    droits = len(re.findall(r'"', prose))
    if droits:
        attention.append(f"{droits} guillemet(s) droit(s) : utilise « »")

    verdict = "À REVOIR" if erreurs or attention else "OK"
    if len(erreurs) >= 5:
        verdict = "INUTILISABLE"
    return {"verdict": verdict, "erreurs": erreurs, "attention": attention, "infos": infos}


# ---------------------------------------------------------------------------
# Skill « ma-voix »
# ---------------------------------------------------------------------------

def slug(nom):
    s = unicodedata.normalize("NFD", nom)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s


def nom_skill(nom):
    if not slug(nom):
        raise ValueError(f"nom inutilisable pour un Skill : « {nom} »")
    n = "ma-voix-" + slug(nom)
    n = n[:64].rstrip("-")
    if not NOM_SKILL.match(n):
        raise ValueError(f"nom de Skill invalide : {n}")
    return n


CIVILITE = re.compile(r"\b(Monsieur|Madame|Mademoiselle|M\.|Mme|Mlle)\s+[A-ZÀ-Ý][a-zà-ÿ-]+")


def anonymiser(texte):
    """Retire coordonnées et noms de tiers précédés d'une civilité. Renvoie (texte, nombre)."""
    n = 0
    for motif, rempl in ((tx.EMAIL, "{{email retiré}}"), (tx.TELEPHONE, "{{téléphone retiré}}")):
        texte, k = motif.subn(rempl, texte)
        n += k
    texte, k = CIVILITE.subn(lambda m: f"{m.group(1)} X", texte)
    return texte, n + k


def premiere_phrase(secs):
    corps = secs.get("1", ("", ""))[1]
    lignes = [l.strip() for l in corps.splitlines() if l.strip() and "{{" not in l]
    return lignes[0] if lignes else ""


def jamais(secs):
    corps = secs.get("6", ("", ""))[1]
    return [l.strip() for l in corps.splitlines() if l.strip().startswith(("-", "*")) and "{{" not in l]


def canaux(secs):
    lignes = lignes_tableau(secs.get("8", ("", ""))[1])
    return [c[0] for c in lignes if c and c[0] and "{{" not in c[0]]


def description(nom, une_phrase, liste_canaux):
    can = ", ".join(liste_canaux) if liste_canaux else "posts, emails, messages, pages"
    d = (f"Écrit et réécrit les textes de {nom} dans sa voix ({can}). "
         f"Utilise-le dès que {nom} demande d'écrire, de rédiger, de réécrire ou de répondre, "
         f"ou dit « mets ça dans ma voix », « est-ce que ça sonne comme moi ? », « relis ce texte ». "
         f"Ne l'utilise pas pour écrire au nom d'une autre personne, ni pour du code ou des tableaux de chiffres. "
         f"Créé avec /tone-of-voice de Join Médicis.")
    if une_phrase and len(d) + len(une_phrase) + 8 <= 1024:
        une = une_phrase.rstrip(".")
        une = une[:1].lower() + une[1:] if une[:2] != une[:2].upper() else une
        d = d.replace(f"dans sa voix ({can}). ", f"dans sa voix ({can}) : {une}. ", 1)
    return d[:1024]


def skill_md(nom, nom_s, secs, nb_exemples):
    une = premiere_phrase(secs)
    desc = description(nom, une, canaux(secs)).replace('"', "'")
    liste_jamais = "\n".join(jamais(secs)) or "- (voir references/tone-of-voice.md, section 6)"
    lecture = (f"3 des {nb_exemples} textes de `exemples/`, choisis au hasard" if nb_exemples >= 3
               else "les textes de `exemples/`" if nb_exemples else "la section 10 du fichier de voix")
    return f"""---
name: {nom_s}
description: "{desc}"
license: MIT
metadata:
  cree-avec: "tone-of-voice (Join Médicis)"
---

# Ma voix : {nom}

{une}

## Avant d'écrire

1. Lis `references/tone-of-voice.md` en entier. Les sections 2 (traits) et 6
   (ce que {nom} n'écrit jamais) passent avant tout le reste.
2. Lis {lecture}. Imite leur rythme, leurs ouvertures, leurs fins. Ne recopie
   aucune phrase.
3. Repère le canal (section 8) et applique sa ligne : adresse, longueur,
   ouverture, fin, formule d'appel et signature.

## Ce que {nom} n'écrit jamais

{liste_jamais}

## Après avoir écrit

- Chaque trait de la section 2 est-il visible ? Aucune limite « Pas » n'est
  franchie ?
- Aucune expression de la liste ci-dessus, aucune tournure d'IA (« Dans un
  monde où », « ce n'est pas X, c'est Y », « n'hésitez pas »).
- Aucun fait, chiffre, nom ou délai inventé : ce qui manque s'écrit
  `{{{{à compléter}}}}`.
- Si tu peux exécuter du Python :
  `python3 scripts/ecart.py references/tone-of-voice.md brouillon.txt`
  (ajoute `--adresse tutoiement` ou `--adresse vouvoiement` si le canal le
  demande). Corrige les écarts « fort », juge les autres.

## Quand {nom} corrige

Si {nom} dit « ce n'est pas moi », corrige le texte, puis propose la règle
qui en découle en une phrase. Le fichier de voix se met à jour avec le
Skill `/tone-of-voice` (mode « mettre à jour »), pas à la main.

## Portée

S'applique à tout texte écrit au nom de {nom}. Ne s'applique pas au code,
aux tableaux de chiffres, aux citations d'autres personnes, ni aux textes
écrits au nom de quelqu'un d'autre.
"""


def construire(chemin_md, nom, exemples, sortie, faire_zip):
    with open(chemin_md, encoding="utf-8") as fh:
        md = fh.read()
    secs = sections(md)
    nom_s = nom_skill(nom)
    racine = os.path.join(sortie, nom_s)
    if os.path.exists(racine):
        shutil.rmtree(racine)
    os.makedirs(os.path.join(racine, "references"))
    os.makedirs(os.path.join(racine, "scripts"))
    rapport = {"skill": nom_s, "dossier": racine, "exemples": 0, "retraits": 0, "alertes": []}

    md_anonyme, k = anonymiser(md)
    rapport["retraits"] += k
    with open(os.path.join(racine, "references", "tone-of-voice.md"), "w", encoding="utf-8") as fh:
        fh.write(md_anonyme)

    if exemples:
        os.makedirs(os.path.join(racine, "exemples"))
    for i, ch in enumerate(exemples, 1):
        with open(ch, encoding="utf-8", errors="replace") as fh:
            t, k = anonymiser(tx.normaliser(fh.read()).strip())
        rapport["retraits"] += k
        with open(os.path.join(racine, "exemples", f"exemple-{i:02d}.md"), "w", encoding="utf-8") as fh:
            fh.write(t + "\n")
        rapport["exemples"] += 1
        if tx.marques_ia(t):
            rapport["alertes"].append(f"{os.path.basename(ch)} contient des marques d'écriture IA : est-ce un vrai texte ?")

    for f in ("ecart.py", "texte.py"):
        shutil.copy(os.path.join(ICI, f), os.path.join(racine, "scripts", f))

    contenu = skill_md(nom, nom_s, secs, rapport["exemples"])
    with open(os.path.join(racine, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(contenu)

    desc = re.search(r'^description: "(.*)"$', contenu, re.M).group(1)
    if len(desc) > 1024:
        raise ValueError("description de plus de 1 024 caractères")
    rapport["description"] = len(desc)
    if rapport["exemples"] < 3:
        rapport["alertes"].append("moins de 3 exemples : le Skill imitera moins bien le rythme (ajoute --exemples)")

    if faire_zip:
        chemin_zip = os.path.join(sortie, nom_s + ".zip")
        with zipfile.ZipFile(chemin_zip, "w", zipfile.ZIP_DEFLATED) as z:
            for dossier, _, fichiers in os.walk(racine):
                for f in sorted(fichiers):
                    if f.endswith(".pyc"):
                        continue
                    plein = os.path.join(dossier, f)
                    z.write(plein, os.path.relpath(plein, sortie))
        with zipfile.ZipFile(chemin_zip) as z:
            n_skill = sum(1 for n in z.namelist() if n.endswith("SKILL.md"))
        if n_skill != 1:
            raise ValueError(f"{n_skill} SKILL.md dans le ZIP (1 attendu)")
        rapport["zip"] = chemin_zip
    return rapport


# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="Contrôle un tone-of-voice.md et en fait un Skill « ma-voix ».")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verifier", help="contrôle un tone-of-voice.md")
    v.add_argument("fichier")
    v.add_argument("--aujourdhui", help="date du jour (AAAA-MM-JJ), pour les tests")
    s = sub.add_parser("ma-voix", help="construit le Skill « ma-voix »")
    s.add_argument("fichier")
    s.add_argument("--nom", required=True, help="prénom ou nom de la personne ou de la marque")
    s.add_argument("--exemples", nargs="*", default=[], help="3 à 6 vrais textes à embarquer")
    s.add_argument("--sortie", default=".", help="dossier où écrire le Skill")
    s.add_argument("--zip", action="store_true", help="écrit aussi le ZIP importable")
    a = ap.parse_args(argv)

    try:
        if a.cmd == "verifier":
            with open(a.fichier, encoding="utf-8") as fh:
                md = fh.read()
            jour = dt.date.fromisoformat(a.aujourdhui) if a.aujourdhui else dt.date.today()
            r = verifier(md, jour)
            print(f"{r['verdict']} · {a.fichier}")
            for x in r["infos"]:
                print(f"  · {x}")
            for x in r["erreurs"]:
                print(f"  ✗ {x}")
            for x in r["attention"]:
                print(f"  ! {x}")
            return {"OK": 0, "À REVOIR": 2}.get(r["verdict"], 3)
        r = construire(a.fichier, a.nom, a.exemples, a.sortie, a.zip)
    except (OSError, ValueError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    print(f"Skill « {r['skill']} » écrit dans {r['dossier']}")
    print(f"  · {r['exemples']} exemple(s), {r['retraits']} coordonnée(s) ou nom(s) de tiers retiré(s), "
          f"description {r['description']} caractères")
    if r.get("zip"):
        print(f"  · ZIP : {r['zip']} (claude.ai : Personnaliser → Skills → importer)")
    for x in r["alertes"]:
        print(f"  ! {x}")
    return 2 if r["alertes"] else 0


if __name__ == "__main__":
    sys.exit(main())
