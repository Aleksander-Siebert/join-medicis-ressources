#!/usr/bin/env python3
"""commentaire.py : quels posts commenter, et ce commentaire apporte-t-il quelque chose ?

  priorite --fichier posts.json [--max 10]
      Classe les posts à commenter (grille sur 80) : adéquation à la cible ×2,
      signal d'intention ×2, possibilité d'un commentaire utile ×2, portée ×1,
      fraîcheur ×1. Exclut : plus de 24 h ET plus de 50 commentaires ; rien
      d'utile à ajouter ; auteur commenté 3 fois ou plus cette semaine.
      Suggère un niveau : relation, visibilité ou entretien.

  verifier --post post.txt --commentaire "…" [--existants commentaires.txt] [--produits "A,B"]
      Contrôle un commentaire :
        BLOQUANT  ouverture vide (« Super post »), éloge seul, appât, produit
                  de l'utilisateur nommé, tiret cadratin, lien
        ATTENTION aucun mot ou chiffre absent du post (pas d'angle nouveau),
                  doublon d'un commentaire existant, résumé du post, longueur
                  hors 12 mots / 500 caractères, émoji en tête, hashtags
      Rend la liste des mots nouveaux apportés.

Codes de sortie : verifier 0 OK · 2 attention · 3 bloquant ; priorite 0 ;
1 erreur.

Grille d'après listening.md (Corey Haines, marketingskills, MIT) ; contrôle
« angle nouveau » d'après la structure en 4 temps de Serge Bulaev (MIT). Sans
dépendance. Rien n'est lu sur LinkedIn : l'utilisateur colle les posts.

Format de posts.json :
  {"deja_commentes": {"Nom Auteur": 2},
   "posts": [{"auteur": "…", "extrait": "…", "cible": 0-10, "intention": 0-10,
              "opportunite": 0-10, "portee": 0-10, "age_heures": 3, "commentaires": 12}]}
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

OUVERTURES = ["super post", "excellent post", "tres bon post", "top post", "j'adore", "tellement vrai", "tellement juste",
              "je ne peux qu'approuver", "entierement d'accord", "totalement d'accord", "ca resonne", "100%", "merci pour ce post",
              "merci pour ce partage", "bravo", "felicitations", "great post", "so true", "this", "exactement", "pepite",
              "tres inspirant", "inspirant", "quel beau post", "post tres interessant", "tres interessant"]
APPAT = re.compile(r"\b(?:dm|mp|ecris-moi|contacte-moi)\b.{0,30}\b(?:pour|si)\b|\bvoir mon profil\b|\blien dans ma bio\b")
STOP = set("""a au aux avec ce ces cet cette c'est dans de des du elle en et eux il ils je j'ai la le les leur leurs lui ma mais me meme mes
moi mon ne nos notre nous on ou par pas pour qu que qui sa se ses si son sur ta te tes toi ton tu un une vos votre vous y est sont
etait ete etre avoir ai as avons avez ont fait faire plus tres tout tous toute toutes bien aussi comme quand alors donc car ni
cela ca ici la-bas oui non sans sous chez entre vers apres avant pendant depuis encore deja jamais toujours rien peu beaucoup
quoi dont ou cette celui celle ceux celles chaque autre autres meme memes peut peuvent faut fois
super tellement merci bravo vraiment genial excellent interessant inspirant partage""".split())


def norme(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("’", "'")


def mots_pleins(t):
    out = set()
    for m in re.findall(r"[a-z0-9][a-z0-9'%-]*", norme(t)):
        m = m.split("'")[-1]
        if m in STOP:
            continue
        if re.search(r"\d", m):
            out.add(m)
        elif len(m) >= 5:
            # racine grossière : « coupe », « couper », « coupons » se rapprochent
            r = re.sub(r"(?:s|x)$", "", m)
            r = re.sub(r"(?:ements?|ement|ations?|ation|aient|ions|ons|ent|ait|ais|ez|er|ee|es|e)$", "", r)
            out.add(r[:6])
    return out


def chevauchement(a, b):
    ma, mb = mots_pleins(a), mots_pleins(b)
    if not ma:
        return 0.0
    return len(ma & mb) / len(ma)


def priorite(donnees, maxi=10):
    deja = {norme(k): v for k, v in (donnees.get("deja_commentes") or {}).items()}
    classes, exclus = [], []
    for p in donnees.get("posts", []):
        raison = None
        if (p.get("age_heures") or 0) > 24 and (p.get("commentaires") or 0) > 50:
            raison = "plus de 24 h et plus de 50 commentaires : un commentaire de plus serait enterré"
        elif (p.get("opportunite") or 0) <= 2:
            raison = "rien d'utile à ajouter"
        elif deja.get(norme(p.get("auteur")), 0) >= 3:
            raison = "auteur déjà commenté 3 fois cette semaine : ça se voit"
        if raison:
            exclus.append({"auteur": p.get("auteur"), "raison": raison})
            continue
        age = p.get("age_heures") or 0
        fraicheur = 10 if age <= 4 else 7 if age <= 12 else 4 if age <= 24 else 1
        score = 2 * p.get("cible", 0) + 2 * p.get("intention", 0) + 2 * p.get("opportunite", 0) + p.get("portee", 0) + fraicheur
        if p.get("cible", 0) >= 7 and p.get("intention", 0) >= 5:
            niveau = "relation : 2 à 4 phrases, ton vécu chiffré, une vraie question, aucun lien"
        elif p.get("portee", 0) >= 7:
            niveau = "visibilité : 1 à 2 phrases, une idée nette"
        else:
            niveau = "entretien : 1 phrase qui cite une ligne précise du post"
        classes.append({"auteur": p.get("auteur"), "extrait": (p.get("extrait") or "")[:90], "score": score, "sur": 80, "niveau": niveau})
    classes.sort(key=lambda x: -x["score"])
    return {"a_commenter": classes[:maxi], "exclus": exclus}


def verifier(post, commentaire, existants="", produits=()):
    c = commentaire.strip()
    cn = norme(c)
    bloquants, attentions = [], []
    debut = cn[:40]
    ouv = [o for o in OUVERTURES if debut.startswith(o) or re.match(rf"^[\w-]+\s*[!,]\s*{re.escape(o)}", debut)]
    if ouv:
        bloquants.append(f"Ouverture vide : « {ouv[0]} ». Commence par le point précis du post que tu prolonges.")
    nb_mots = len(re.findall(r"\w+", c))
    if nb_mots < 12:
        if not mots_pleins(c) - mots_pleins(post):
            bloquants.append(f"{nb_mots} mots sans rien de nouveau : c'est un éloge, pas un commentaire.")
        else:
            attentions.append(f"{nb_mots} mots : un commentaire de moins de 12 mots pèse peu (une ligne citable peut suffire, en niveau « entretien »).")
    if len(c) > 500:
        attentions.append(f"{len(c)} caractères : au-delà de 500, ça se lit comme un détournement du fil. 200 à 350 visés.")
    if APPAT.search(cn):
        bloquants.append("Appel à te contacter sous le post d'un autre : pas d'auto-promotion en commentaire.")
    for p in produits:
        if p.strip() and re.search(rf"(?<!\w){re.escape(norme(p.strip()))}(?!\w)", cn):
            bloquants.append(f"Ton produit « {p.strip()} » est nommé : décris ce que tu fais, sans le nommer.")
    if "—" in c or re.search(r"\s–\s", c):
        bloquants.append("Tiret cadratin : supprime-le ou mets une virgule.")
    if re.search(r"https?://|www\.", c):
        bloquants.append("Lien dans un commentaire sous le post d'un autre : retire-le.")
    if re.match(r"\s*[\U0001F300-\U0001FAFF☀-➿]", c):
        attentions.append("Émoji en premier caractère : commence par un mot.")
    if re.search(r"(?<!\w)#\w", c):
        attentions.append("Hashtag dans un commentaire : inutile.")
    nouveaux = sorted(mots_pleins(c) - mots_pleins(post) - mots_pleins(existants))
    if len(nouveaux) <= 1:
        attentions.append("Presque aucun mot, chiffre ou nom absent du post : le commentaire n'apporte pas d'angle nouveau.")
    elif chevauchement(c, post) > 0.75 and len(mots_pleins(c)) >= 4:
        attentions.append("Le commentaire reprend surtout les mots du post : ça ressemble à un résumé.")
    for ligne in [l for l in (existants or "").split("\n\n") if l.strip()]:
        if chevauchement(c, ligne) > 0.6 and len(mots_pleins(c)) >= 4:
            attentions.append(f"Proche d'un commentaire déjà publié : « {ligne.strip()[:70]}… ». Trouve un autre angle.")
            break
    verdict, code = ("BLOQUÉ", 3) if bloquants else ("À REVOIR", 2) if attentions else ("OK", 0)
    return {"verdict": verdict, "code": code, "caracteres": len(c), "mots": nb_mots,
            "mots_nouveaux": nouveaux[:12], "bloquants": bloquants, "attentions": attentions}


def lire(chemin):
    return Path(chemin).read_text(encoding="utf-8") if chemin else ""


def main():
    a = argparse.ArgumentParser(description="Priorité des posts à commenter, contrôle d'un commentaire.")
    sous = a.add_subparsers(dest="cmd", required=True)
    pr = sous.add_parser("priorite")
    pr.add_argument("--fichier", required=True)
    pr.add_argument("--max", type=int, default=10)
    pr.add_argument("--json", action="store_true")
    ve = sous.add_parser("verifier")
    ve.add_argument("--post", required=True, help="fichier contenant le texte du post")
    ve.add_argument("--commentaire", required=True)
    ve.add_argument("--existants", help="fichier des meilleurs commentaires déjà publiés (séparés par une ligne vide)")
    ve.add_argument("--produits", default="", help="noms de produits de l'utilisateur, séparés par des virgules")
    ve.add_argument("--json", action="store_true")
    x = a.parse_args()
    try:
        if x.cmd == "priorite":
            r = priorite(json.loads(lire(x.fichier)), x.max)
            if x.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                print("POSTS À COMMENTER")
                for i, p in enumerate(r["a_commenter"], 1):
                    print(f"  {i}. [{p['score']}/80] {p['auteur']} · « {p['extrait']} »\n     niveau {p['niveau']}")
                for e in r["exclus"]:
                    print(f"  · écarté : {e['auteur']} ({e['raison']})")
            return 0
        r = verifier(lire(x.post), x.commentaire, lire(x.existants), x.produits.split(","))
    except (OSError, json.JSONDecodeError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1
    if x.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"COMMENTAIRE  {r['verdict']}  ·  {r['caracteres']} caractères, {r['mots']} mots")
        print("  Apporte : " + (", ".join(r["mots_nouveaux"]) if r["mots_nouveaux"] else "rien de nouveau"))
        for b in r["bloquants"]:
            print(f"  ✖ {b}")
        for t in r["attentions"]:
            print(f"  ! {t}")
    return r["code"]


if __name__ == "__main__":
    sys.exit(main())
