#!/usr/bin/env python3
"""controle.py : le contrôle avant livraison d'un article (règles de rédaction du pack).

Vérifie ce que la relecture rate le plus souvent, dans un article en
Markdown rédigé par /seo-write :

  structure   un seul H1 ; résumé en tête (citation « > » juste après
              l'introduction, 3 phrases et 60 mots au plus) ; pas de section
              « Conclusion », « En conclusion », « Défis », « Perspectives » ;
              chaque H2 s'ouvre sur une réponse, pas sur une annonce
  style       voix passive avec complément d'agent ; verbes modaux
              d'hésitation (--affirmatif) ; verbes d'état gonflés
              (« se positionne comme », « sert de ») ; participes présents
              déductifs en fin de phrase (« …, renforçant ainsi … ») ;
              annonces (« Dans cet article, nous allons voir »)
  maison      règles d'entité et remplacements (--remplacer « chez X=à X ») ;
              mots interdits (--interdire)
  forme       gras réservé aux notions (pas de phrase entière en gras) ;
              liens annoncés ou ancres vides (« cliquez ici ») ; nombre de liens
              internes ; longueur face à la préférence (--longueur 1000-1500)
  typographie tiret cadratin, espace avant « : ; ! ? », guillemets, « 15% »
  bloc méta   title et description (via commun/meta.py, en pixels)
  trous       chaque {{à compléter}} est compté et listé

Les tics d'écriture IA (lexique, triades, rythme) relèvent de /seo-human :
ce script ne les double pas.

Codes de sortie : 0 PRÊT · 2 À REVOIR · 1 erreur d'utilisation.

Exemples :
  python3 controle.py article.md
  python3 controle.py article.md --affirmatif --remplacer "chez Assurly=à Assurly" \\
          --interdire cash --longueur 1000-1500 --mot-cle "mutuelle indépendant" --marque Assurly
"""

import argparse
import json
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
for _c in (ICI.parent / "commun", ICI.parents[2] / "commun"):
    if (_c / "texte_fr.py").exists():
        sys.path.insert(0, str(_c))
        break
import meta  # noqa: E402
import texte_fr as tf  # noqa: E402

SECTIONS_INTERDITES = re.compile(r"^(?:en )?conclusions?\b|^pour conclure|^le mot de la fin|^d[ée]fis\b|^les d[ée]fis"
                                 r"|^perspectives\b|^d[ée]fis et perspectives|^perspectives d'avenir|^en r[ée]sum[ée]\b"
                                 r"|^le futur de|^et demain", re.I)
ANNONCES = re.compile(r"\b(?:dans cet article|dans ce guide|dans cette partie|dans cette section|nous allons (?:voir|"
                      r"d[ée]couvrir|aborder|expliquer)|voyons (?:ensemble|maintenant|comment)|découvrons|"
                      r"vous allez d[ée]couvrir|on fait le point|tour d'horizon)\b", re.I)
MODAUX = re.compile(r"\b(?:peut-[êe]tre|pourr(?:ais|ait|aient|iez|ions)|devr(?:ais|ait|aient|iez|ions)|il semblerai?t|semble(?:rai)?(?:t|nt)?|"
                    r"il se peut|[ée]ventuellement|potentiellement|probablement|sans doute)\b", re.I)
PASSIF_AGENT = re.compile(r"\b(?:est|sont|sera|seront|serait|seraient|était|étaient|a été|ont été|sera)\s+"
                          r"(?:\w+\s+)?\w+(?:é|ée|és|ées|i|ie|is|ies|u|ue|us|ues|it|ite|its|ites)\s+par\s", re.I)
ETAT_GONFLE = re.compile(r"\b(?:se positionne(?:nt)? comme|se pr[ée]sente(?:nt)? comme|s'impose(?:nt)? comme|sert de|servent de|"
                         r"fait office de|offre(?:nt)? une approche|repr[ée]sente(?:nt)? un v[ée]ritable|constitue(?:nt)? un v[ée]ritable|"
                         r"joue(?:nt)? un r[ôo]le (?:cl[ée]|crucial|essentiel|majeur|central))\b", re.I)
PARTICIPE_DEDUCTIF = re.compile(r",\s*(?:renfor[çc]ant|soulignant|illustrant|t[ée]moignant|mettant en (?:lumi[èe]re|avant|[ée]vidence)|"
                                r"refl[ée]tant|confirmant|d[ée]montrant|t[ée]moignant|marquant|ouvrant la voie)\b[^.!?]*[.!?]", re.I)
TRANSITIONS = re.compile(r"\b(?:dans ce contexte|il convient de (?:noter|souligner|rappeler)|il est (?:important|essentiel|"
                         r"crucial|primordial) de (?:noter|souligner|rappeler|comprendre)|force est de constater|"
                         r"en d[ée]finitive|in fine|au final)\b", re.I)
LIENS_ANNONCES = re.compile(r"\b(?:comme (?:expliqu[ée]|vu|d[ée]taill[ée]|indiqu[ée]) dans (?:notre|cet|cet autre|l')\s*(?:article|guide)|"
                            r"(?:consultez|lisez|retrouvez|d[ée]couvrez) (?:notre|nos|cet) (?:article|guide|page)|"
                            r"nous en parlons dans|voir notre article|lire aussi)\b", re.I)
ANCRE_VIDE = re.compile(r"\[(?:ici|cliquez ici|ce lien|cet article|en savoir plus|lire la suite|plus d'infos?)\]\(", re.I)
LIEN = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
TROU = re.compile(r"\{\{[^}]*\}\}")


def separer_meta(texte):
    """(corps, bloc méta) : le bloc commence à « BLOC MÉTA » ou à une ligne « Title : »."""
    m = re.search(r"^\s*(?:#+\s*)?(?:BLOC M[ÉE]TA|Bloc m[ée]ta)\b.*$", texte, re.M)
    if not m:
        m = re.search(r"^\s*(?:Title|Balise title)\s*:", texte, re.M | re.I)
    if not m:
        return texte, ""
    return texte[:m.start()], texte[m.start():]


def lire_meta(bloc):
    def champ(*noms):
        for n in noms:
            m = re.search(r"^\s*[-*]?\s*" + n + r"\s*(?:\(.*?\))?\s*:\s*(.+)$", bloc, re.M | re.I)
            if m:
                return m.group(1).strip().strip("«»\" ")
        return ""
    return {"title": champ("title", "balise title"), "description": champ("meta description", "description"),
            "mot_cle": champ("mot-cl[ée] principal", "mot-cl[ée]"), "slug": champ("slug")}


def blocs(corps):
    """Paragraphes avec leur numéro de ligne, titres à part."""
    out, buf, debut = [], [], 0
    for n, ligne in enumerate(corps.splitlines() + [""], 1):
        if not ligne.strip() or re.match(r"^#{1,6}\s", ligne):
            if buf:
                out.append({"ligne": debut, "texte": "\n".join(buf)})
                buf = []
            if ligne.strip():
                out.append({"ligne": n, "titre": ligne.strip()})
            continue
        if not buf:
            debut = n
        buf.append(ligne)
    return out


def ligne_de(corps, idx):
    return corps.count("\n", 0, idx) + 1


def controler(texte, affirmatif=False, remplacer=None, interdire=None, longueur=None, mot_cle="", marque="",
              domaine="", pref_title=None, pref_desc=None, resume=True, h1_gabarit=False):
    corps, bloc_meta = separer_meta(texte)
    constats = []

    def c(gravite, famille, quoi, ligne=None, conseil=""):
        constats.append({"gravite": gravite, "famille": famille, "constat": quoi, "ligne": ligne, "conseil": conseil})

    b = blocs(corps)
    titres = [x for x in b if "titre" in x]
    h1 = [x for x in titres if re.match(r"^#\s", x["titre"])]
    if h1_gabarit:
        # Texte placé dans une page dont le gabarit porte déjà le H1 (catégorie, fiche produit).
        if h1:
            c("haute", "structure", f"{len(h1)} H1 dans un texte de gabarit (le H1 est déjà dans la page)", h1[0]["ligne"])
    elif len(h1) != 1:
        c("haute", "structure", f"{len(h1)} H1 (un seul attendu)", h1[1]["ligne"] if len(h1) > 1 else None)

    # résumé : une citation « > » avant le premier H2
    premier_h2 = next((i for i, x in enumerate(b) if "titre" in x and re.match(r"^##\s", x["titre"])), len(b))
    avant = b[:premier_h2]
    resumes = [x for x in avant if "texte" in x and all(l.lstrip().startswith(">") for l in x["texte"].splitlines())]
    if resume:
        if not resumes:
            c("haute", "structure", "résumé en tête absent (citation « > » de 3 lignes juste après l'introduction)")
        else:
            r = re.sub(r"^\s*>\s?", "", resumes[0]["texte"], flags=re.M)
            nph, nmo = len(tf.phrases(r)), tf.mots(r)
            if nph > 3 or nmo > 60:
                c("moyenne", "structure", f"résumé trop long ({nph} phrases, {nmo} mots ; 3 lignes maximum)",
                  resumes[0]["ligne"], "Une phrase par idée : de quoi parle l'article, ce que le lecteur en retire.")
            if re.search(r"^\s*>\s*[-*]\s", resumes[0]["texte"], re.M):
                c("basse", "structure", "résumé en liste à puces", resumes[0]["ligne"], "Des phrases simples, pas une liste.")

    for i, x in enumerate(b):
        if "titre" not in x:
            continue
        nom = re.sub(r"^#+\s*", "", x["titre"]).strip()
        if re.match(r"^#{2,3}\s", x["titre"]) and SECTIONS_INTERDITES.search(nom):
            c("haute", "structure", f"section interdite : « {nom} »", x["ligne"],
              "Finir sur une réponse utile ou une action concrète, sans section de clôture.")
        if re.match(r"^##\s", x["titre"]):
            suite = next((y for y in b[i + 1:] if "texte" in y or "titre" in y), None)
            if suite is None or "titre" in suite:
                c("moyenne", "structure", f"« {nom} » ne s'ouvre pas sur un paragraphe de réponse", x["ligne"])
            else:
                premiere = (tf.phrases(suite["texte"]) or [""])[0]
                if ANNONCES.search(premiere) or premiere.rstrip().endswith("?") or len(premiere.split()) > 45:
                    c("moyenne", "structure", f"« {nom} » s'ouvre sans réponse directe : « {premiere[:80]} »",
                      suite["ligne"], "Répondre en 1 à 2 phrases, puis détailler.")

    lignes_corps = corps
    for rx, gravite, famille, quoi, conseil in (
        (ANNONCES, "moyenne", "style", "annonce de plan", "Entrer dans le sujet : la première phrase répond."),
        (PASSIF_AGENT, "basse", "style", "voix passive avec complément d'agent", "Le sujet fait l'action."),
        (ETAT_GONFLE, "moyenne", "style", "verbe d'état gonflé", "Écrire « est » ou « sont »."),
        (PARTICIPE_DEDUCTIF, "moyenne", "style", "participe présent déductif en fin de phrase",
         "Couper : une phrase pour le fait, une pour sa conséquence si elle est prouvée."),
        (TRANSITIONS, "moyenne", "style", "transition toute faite", "Supprimer : la phrase suivante suffit."),
        (LIENS_ANNONCES, "moyenne", "forme", "lien annoncé", "Intégrer le lien dans la phrase, sans l'annoncer."),
        (ANCRE_VIDE, "moyenne", "forme", "ancre vide", "L'ancre dit où mène le lien (2 à 6 mots descriptifs)."),
    ):
        for m in rx.finditer(lignes_corps):
            c(gravite, famille, f"{quoi} : « {m.group(0).strip()[:70]} »", ligne_de(lignes_corps, m.start()), conseil)
    if affirmatif:
        for m in MODAUX.finditer(lignes_corps):
            c("moyenne", "style", f"verbe modal d'hésitation : « {m.group(0)} »", ligne_de(lignes_corps, m.start()),
              "Style affirmatif : dire ce qui est, ou ce qui dépend du contrat.")
    for regle in remplacer or []:
        if "=" not in regle:
            continue
        avant_r, apres_r = [x.strip() for x in regle.split("=", 1)]
        for m in re.finditer(re.escape(avant_r), lignes_corps, re.I):
            c("haute", "maison", f"« {m.group(0)} » au lieu de « {apres_r} »", ligne_de(lignes_corps, m.start()))
    for mot in interdire or []:
        for m in re.finditer(r"\b" + re.escape(mot) + r"\b", lignes_corps, re.I):
            c("haute", "maison", f"mot interdit : « {m.group(0)} »", ligne_de(lignes_corps, m.start()))

    # gras
    gras = re.findall(r"\*\*([^*]+)\*\*|__([^_]+)__", corps)
    gras = [g[0] or g[1] for g in gras]
    nmots = tf.mots(corps)
    for g in gras:
        if len(g.split()) >= 8 or re.search(r"[.!?]\s*$", g):
            c("moyenne", "forme", f"phrase entière en gras : « {g[:60]} »", conseil="Le gras marque une notion, pas une phrase.")
    if nmots and len(gras) * 100 / nmots > 1.5:
        c("basse", "forme", f"{len(gras)} passages en gras pour {nmots} mots", conseil="Garder le gras pour les notions clés.")

    # liens internes
    liens = LIEN.findall(corps)
    internes = [u for _, u in liens if u.startswith("/") or (domaine and domaine in u)]
    if not internes:
        c("moyenne", "forme", "aucun lien interne", conseil="3 à 5 liens vers les pages à pousser, dans le texte.")

    # longueur
    if longueur and nmots:
        lo, hi = longueur
        if not lo * 0.85 <= nmots <= hi * 1.15:
            c("info", "forme", f"{nmots} mots, hors de la préférence {lo}-{hi}",
              conseil="Préférence de site-context.md, pas une règle de Google : couper le remplissage ou compléter un manque réel.")

    # typographie (hors liens et code)
    propre = re.sub(r"`[^`]*`|\]\([^)]*\)|https?://\S+", " ", corps)
    for rx, quoi in ((re.compile(r"—|\s–\s"), "tiret cadratin ou demi-cadratin (virgule ou reformulation)"),
                     (re.compile(r"[^\s(\[«|>*:]([:;!?])(?=\s|$)"), "espace manquante avant « : ; ! ? »"),
                     (re.compile(r'"[^"\n]{2,}"'), "guillemets droits (« »)"),
                     (re.compile(r"\d\s%"), "pourcentage détaché (« 15% »)")):
        for m in rx.finditer(propre):
            c("basse", "typographie", quoi, ligne_de(propre, m.start()))

    trous = [m.group(0) for m in TROU.finditer(texte)]

    meta_r = None
    if bloc_meta:
        mm = lire_meta(bloc_meta)
        meta_r = meta.analyser(mm["title"], mm["description"], mot_cle or mm["mot_cle"], marque,
                               pref_title=pref_title, pref_desc=pref_desc)
        for x in meta_r["constats"]:
            if x["gravite"] in ("haute", "moyenne"):
                c(x["gravite"], "bloc méta", x["constat"], conseil=x["conseil"])
        if h1 and mm["title"]:
            th1 = set(tf.termes(re.sub(r"^#\s*", "", h1[0]["titre"])))
            tt = set(tf.termes(mm["title"]))
            if th1 and len(th1 & tt) / len(th1) < 0.4:
                c("basse", "bloc méta", "title et H1 ne parlent pas du même sujet",
                  conseil="Google réécrit les titles qui ne correspondent pas au titre visible.")
    else:
        c("moyenne", "bloc méta", "bloc méta absent (Title, Meta description, Mot-clé principal, Slug)")

    ordre = {"haute": 0, "moyenne": 1, "basse": 2, "info": 3}
    constats.sort(key=lambda x: (ordre[x["gravite"]], x["ligne"] or 0))
    a_revoir = any(x["gravite"] in ("haute", "moyenne") for x in constats)
    return {"mots": nmots, "liens_internes": len(internes), "gras": len(gras), "trous": trous,
            "constats": constats, "meta": meta_r, "verdict": "À REVOIR" if a_revoir else "PRÊT"}


def afficher(r):
    out = [f"CONTRÔLE · {r['mots']} mots · {r['liens_internes']} lien(s) interne(s) · {r['gras']} gras · "
           f"{len(r['trous'])} trou(s)"]
    if r["meta"] and "title_px" in r["meta"]:
        m = r["meta"]
        out.append(f"  title {m['title_car']} car. / {m['title_px']} px"
                   + (f" · description {m['description_car']} car. / {m['description_px']} px" if "description_px" in m else ""))
    for g in ("haute", "moyenne", "basse", "info"):
        lot = [x for x in r["constats"] if x["gravite"] == g]
        if lot:
            out += ["", g.upper()]
            for x in lot:
                ou = f"l.{x['ligne']} " if x["ligne"] else ""
                out.append(f"  [{x['famille']}] {ou}{x['constat']}" + (f"\n      → {x['conseil']}" if x["conseil"] else ""))
    if r["trous"]:
        out += ["", "À COMPLÉTER PAR L'UTILISATEUR"] + [f"  {t}" for t in dict.fromkeys(r["trous"])]
    out += ["", f"VERDICT : {r['verdict']}"]
    return "\n".join(out)


def bornes(x, p):
    if not x:
        return None
    m = re.fullmatch(r"\s*(\d+)\s*[-–à]\s*(\d+)\s*", x)
    if not m:
        p.error(f"intervalle illisible : {x} (attendu : 1000-1500)")
    return int(m.group(1)), int(m.group(2))


def main():
    p = argparse.ArgumentParser(description="Contrôle avant livraison d'un article Markdown.")
    p.add_argument("fichier")
    p.add_argument("--affirmatif", action="store_true", help="signaler les verbes modaux d'hésitation")
    p.add_argument("--remplacer", action="append", help="règle maison « avant=après » (répéter)")
    p.add_argument("--interdire", action="append", help="mot interdit (répéter)")
    p.add_argument("--longueur", help="préférence de longueur, ex. 1000-1500")
    p.add_argument("--mot-cle", default="")
    p.add_argument("--marque", default="")
    p.add_argument("--domaine", default="", help="domaine du site, pour compter les liens internes absolus")
    p.add_argument("--pref-title", default="55-60")
    p.add_argument("--pref-description", default="150-160")
    p.add_argument("--sans-resume", action="store_true", help="le site ne veut pas de résumé en tête")
    p.add_argument("--h1-gabarit", action="store_true",
                   help="texte inséré dans une page dont le gabarit porte déjà le H1 (catégorie, fiche produit) : aucun H1 attendu")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    try:
        texte = Path(a.fichier).read_text(encoding="utf-8")
    except OSError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    r = controler(texte, a.affirmatif, a.remplacer, a.interdire, bornes(a.longueur, p), a.mot_cle, a.marque,
                  a.domaine, bornes(a.pref_title, p), bornes(a.pref_description, p), not a.sans_resume,
                  h1_gabarit=a.h1_gabarit)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else afficher(r))
    return 0 if r["verdict"] == "PRÊT" else 2


if __name__ == "__main__":
    sys.exit(main())
