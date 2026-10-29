#!/usr/bin/env python3
"""carrousel.py : construit un carrousel LinkedIn (PDF) à partir des textes validés.

Étapes :
  1. CONTRÔLE des textes (rien n'est fabriqué tant que c'est bloquant) :
     - 5 à 14 slides ; la couverture tient en 8 mots au plus ;
     - 25 mots au plus sous le titre d'une slide ;
     - le nombre promis en couverture (« 7 vérifications ») = nombre d'étapes ;
     - un seul appel à l'action ; aucun appât (« commente PDF ») ;
     - ni tiret cadratin, ni pseudo-gras Unicode, ni champ {{…}} restant ;
     - une signature (auteur) sur chaque slide.
  2. HTML : une <section> par slide, à partir de assets/gabarit.html (styles).
  3. PDF : Chromium sans interface s'il est installé ; sinon le HTML est rendu
     et l'utilisateur l'imprime depuis son navigateur (marges « aucune »).
  4. Vérification du PDF : nombre de pages, poids (100 Mo et 300 pages au plus,
     limites officielles de LinkedIn pour les documents).

Le PDF garde du texte sélectionnable (accessible et lisible au zoom), pas des
images de texte.

Entrée JSON :
  {
    "auteur": "Camille D. · Assurly",
    "format": "portrait" | "carre",
    "couleurs": {"accent": "#1f6f50", "fond": "#fbfaf7", "texte": "#16201b"},
    "slides": [
      {"type": "couverture", "titre": "…", "texte": "promesse en une ligne"},
      {"type": "enjeu", "titre": "…", "texte": "…"},
      {"type": "etape", "etiquette": "Vérification 1", "titre": "…", "texte": "…"},
      {"type": "recap", "titre": "En résumé", "points": ["…", "…"]},
      {"type": "preuve", "titre": "…", "texte": "…"},
      {"type": "appel", "titre": "…", "texte": "…"}
    ]
  }

Codes de sortie : 0 PDF produit · 2 HTML seul (pas de Chromium) ou
avertissements · 3 bloquant (rien n'est produit) · 1 erreur d'utilisation.

Sans dépendance. Chromium : trouvé dans le PATH (chromium, chromium-browser,
google-chrome) ou dans /opt/pw-browsers, ou passé par --chromium.

Exemples :
  python3 carrousel.py --fichier carrousel.json --sortie carrousel.pdf
  python3 carrousel.py --exemple --sortie /tmp/exemple.pdf
  python3 carrousel.py --fichier carrousel.json --verifier
"""

import argparse
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
GABARIT = ICI.parent / "assets" / "gabarit.html"
TYPES = {"couverture", "enjeu", "etape", "recap", "preuve", "appel", "texte"}
FORMATS = {"portrait": (1080, 1350), "carre": (1080, 1080), "banniere": (1584, 396)}
APPAT = re.compile(r"(?i)\bcommente[sz]?\b.{0,20}(?:«|\"|')\s*\w+|\b(?:like|likez)\b.{0,10}\bsi\b|\btague[sz]?\b")
CTA = re.compile(r"(?i)\b(?:abonne-toi|abonnez-vous|suis-moi|suivez-moi|écris-moi|écrivez-moi|réserve|réservez|"
                 r"télécharge|téléchargez|lien en commentaire|commente[sz]?|partage[sz]?|enregistre[sz]?|sauvegarde[sz]?)\b")
MOTS = re.compile(r"[\wÀ-ÿœ'’-]+")
NOMBRE_PROMIS = re.compile(r"\b(\d{1,2})\s+(?:[\wÀ-ÿ'’-]+\s+){0,2}?(?:étapes?|vérifications?|questions?|erreurs?|outils?|"
                           r"méthodes?|leçons?|règles?|astuces?|conseils?|façons?|points?|signaux|signes?|techniques?|"
                           r"choses?|raisons?|chiffres?|modèles?|prompts?)\b", re.I)

EXEMPLE = {
    "auteur": "Camille D. · conseil en acquisition",
    "format": "portrait",
    "slides": [
        {"type": "couverture", "titre": "6 vérifications avant de baisser vos prix",
         "texte": "Ce que j'ai appris en rappelant 60 clients partis."},
        {"type": "enjeu", "titre": "La moitié parlait du délai, pas du prix",
         "texte": "60 appels de résiliation en janvier 2026, chez un assureur en ligne."},
        {"type": "etape", "etiquette": "Vérification 1", "titre": "Rappelez les partants",
         "texte": "10 appels de 10 minutes. Une seule question : qu'est-ce qui vous a fait partir ?"},
        {"type": "etape", "etiquette": "Vérification 2", "titre": "Comptez les mots, pas les avis",
         "texte": "Notez les mots exacts. « Délai », « attente », « relance » : comptez-les."},
        {"type": "etape", "etiquette": "Vérification 3", "titre": "Mesurez le délai réel",
         "texte": "Du dossier complet au virement. Chez nous : 21 jours."},
        {"type": "etape", "etiquette": "Vérification 4", "titre": "Comparez avec vos concurrents",
         "texte": "Demandez à 3 clients récents combien de temps ils attendaient avant."},
        {"type": "etape", "etiquette": "Vérification 5", "titre": "Testez sur un segment",
         "texte": "Un seul produit, un trimestre. Ne touchez pas aux tarifs pendant le test."},
        {"type": "etape", "etiquette": "Vérification 6", "titre": "Décidez avec les chiffres",
         "texte": "Délai passé de 21 à 9 jours en 3 mois. Les tarifs n'ont pas bougé."},
        {"type": "recap", "titre": "En résumé",
         "points": ["Rappeler les partants", "Compter les mots", "Mesurer le délai réel",
                    "Comparer", "Tester sur un segment", "Décider avec les chiffres"]},
        {"type": "appel", "titre": "La grille des 6 questions",
         "texte": "Lien en commentaire, pour tout le monde."},
    ],
}


def mots(t):
    return MOTS.findall(t or "")


def texte_slide(s):
    return " ".join([s.get("etiquette", ""), s.get("titre", ""), s.get("texte", "")] + list(s.get("points", [])))


def controler(c):
    bloquants, attentions = [], []
    slides = c.get("slides") or []
    banniere = c.get("format") == "banniere"
    if banniere and len(slides) != 1:
        bloquants.append("Format bannière : une seule slide (1 584 × 396 px).")
    if not banniere and not 5 <= len(slides) <= 14:
        bloquants.append(f"{len(slides)} slides : il en faut 5 à 14 (en dessous, c'est un post texte ; au-delà, peu de lecteurs vont au bout).")
    if not c.get("auteur"):
        bloquants.append("Pas d'auteur : la signature doit être sur chaque slide (les captures voyagent sans le post).")
    if c.get("format", "portrait") not in FORMATS:
        bloquants.append(f"Format « {c.get('format')} » inconnu : portrait (1080 × 1350) ou carre (1080 × 1080).")
    for i, s in enumerate(slides, 1):
        if s.get("type") not in TYPES:
            bloquants.append(f"Slide {i} : type « {s.get('type')} » inconnu ({', '.join(sorted(TYPES))}).")
        t = texte_slide(s)
        if "—" in t or re.search(r"\s–\s", t):
            bloquants.append(f"Slide {i} : tiret cadratin (règle de l'utilisateur : supprimé ou virgule).")
        if any(0x1D400 <= ord(ch) <= 0x1D7FF for ch in t):
            bloquants.append(f"Slide {i} : pseudo-gras Unicode (illisible pour les lecteurs d'écran).")
        if "{{" in t:
            bloquants.append(f"Slide {i} : champ {{{{…}}}} restant.")
        if APPAT.search(t):
            bloquants.append(f"Slide {i} : appât d'engagement (« commente MOT »). Ressource en lien, pour tous.")
        n_texte = len(mots(s.get("texte", ""))) + sum(len(mots(p)) for p in s.get("points", []))
        if s.get("type") != "recap" and n_texte > 25:
            attentions.append(f"Slide {i} : {n_texte} mots sous le titre (25 au plus) : coupe en deux slides.")
        if len(mots(s.get("titre", ""))) > 9 and s.get("type") != "couverture":
            attentions.append(f"Slide {i} : titre de {len(mots(s['titre']))} mots (3 à 7 conseillés).")
    if slides and not banniere:
        cov = slides[0]
        if cov.get("type") != "couverture":
            attentions.append("La slide 1 n'est pas une couverture : c'est la vignette qui se bat seule dans le fil.")
        if len(mots(cov.get("titre", ""))) > 8:
            attentions.append(f"Couverture de {len(mots(cov.get('titre', '')))} mots : 8 au plus, elle se lit en vignette.")
        m = NOMBRE_PROMIS.search(cov.get("titre", "") + " " + cov.get("texte", ""))
        etapes = sum(1 for s in slides if s.get("type") == "etape")
        if m and etapes and int(m.group(1)) != etapes:
            bloquants.append(f"La couverture promet {m.group(1)} éléments, le carrousel en contient {etapes} : la promesse doit être tenue exactement.")
        appels = [i for i, s in enumerate(slides, 1) if s.get("type") == "appel"]
        if len(appels) > 1:
            bloquants.append(f"{len(appels)} slides d'appel à l'action : une seule.")
        if appels:
            n_cta = len(CTA.findall(texte_slide(slides[appels[0] - 1])))
            if n_cta > 1:
                attentions.append(f"La slide d'appel contient {n_cta} actions : une seule (s'abonner, OU le lien, OU une question).")
        if not any(s.get("type") == "recap" for s in slides) and etapes >= 4:
            attentions.append("Pas de slide de récapitulatif : c'est celle qu'on capture et qu'on garde.")
    return bloquants, attentions


def construire_html(c):
    gab = GABARIT.read_text(encoding="utf-8")
    style = re.search(r"<style>(.*?)</style>", gab, re.S).group(1)
    l, h = FORMATS.get(c.get("format", "portrait"), FORMATS["portrait"])
    style = (style.replace("1080px 1350px", f"{l}px {h}px").replace("height: 1350px", f"height: {h}px")
             .replace("width: 1080px", f"width: {l}px"))
    if c.get("format") == "banniere":
        # Texte dans les deux tiers droits : la photo de profil couvre la gauche.
        style += ("section { padding: 48px 72px 48px 560px; } h1 { font-size: 64px; } "
                  ".promesse { font-size: 32px; margin-top: 16px; } .num, .suite { display: none; } "
                  ".auteur { bottom: 32px; left: auto; right: 72px; font-size: 24px; }")
    for cle, var in (("accent", "--accent"), ("fond", "--fond"), ("texte", "--texte")):
        val = (c.get("couleurs") or {}).get(cle)
        if val and re.fullmatch(r"#[0-9a-fA-F]{3,8}", val):
            style = re.sub(rf"{var}: [^;]+;", f"{var}: {val};", style)
    slides = c["slides"]
    n = len(slides)
    def e(t):
        # Espace fine insécable avant ? ! : ; et à l'intérieur des guillemets français.
        t = html.escape(t or "", quote=False)
        t = re.sub(r"\s+([?!:;»])", "\u202f\\1", t)
        return re.sub(r"«\s+", "«\u202f", t)
    auteur = e(c.get("auteur", ""))
    sections = []
    for i, s in enumerate(slides, 1):
        t = s.get("type")
        cls = ' class="couverture"' if t in ("couverture", "appel") else ""
        corps = []
        if s.get("etiquette"):
            corps.append(f'<div class="etiquette">{e(s["etiquette"])}</div>')
        if t == "couverture":
            corps.append(f"<h1>{e(s.get('titre', ''))}</h1>")
            if s.get("texte"):
                corps.append(f'<p class="promesse">{e(s["texte"])}</p>')
        elif t == "recap":
            corps.append(f'<div class="etiquette">{e(s.get("titre", "En résumé"))}</div>')
            corps.append('<ul class="recap">' + "".join(f"<li><b>{k}</b>{e(p)}</li>" for k, p in enumerate(s.get("points", []), 1)) + "</ul>")
        else:
            corps.append(f"<h2>{e(s.get('titre', ''))}</h2>")
            if s.get("texte"):
                attr = ' class="promesse"' if t == "appel" else ""
                corps.append(f"<p{attr}>{e(s['texte'])}</p>")
        suite = '<span class="suite" aria-hidden="true">→</span>' if i < n else ""
        sections.append(f'<section{cls} aria-label="Slide {i} sur {n}">\n  <span class="num">{i}/{n}</span>\n  '
                        + "\n  ".join(corps) + f'\n  <span class="auteur">{auteur}</span>\n  {suite}\n</section>')
    titre = e(slides[0].get("titre", "Carrousel")) if slides else "Carrousel"
    return (f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<title>{titre}</title>\n'
            f"<style>{style}</style>\n</head>\n<body>\n" + "\n\n".join(sections) + "\n</body>\n</html>\n")


def trouver_chromium(explicite=None):
    if explicite:
        return explicite if os.path.exists(explicite) else None
    for nom in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        p = shutil.which(nom)
        if p:
            return p
    for p in sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"), reverse=True):
        return p
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    return mac if os.path.exists(mac) else None


def imprimer_pdf(chemin_html, chemin_pdf, chromium):
    cmd = [chromium, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
           f"--print-to-pdf={chemin_pdf}", Path(chemin_html).resolve().as_uri()]
    subprocess.run(cmd, check=True, capture_output=True, timeout=120)


def imprimer_png(chemin_html, chemin_png, chromium, l, h):
    """Bannière en PNG exact : PDF à la taille de la page, puis pdftoppm à 96 dpi.

    La capture d'écran de Chromium sans interface ne donne pas une hauteur de
    fenêtre fiable ; l'impression PDF respecte exactement @page.
    """
    pdf = Path(chemin_png).with_suffix(".tmp.pdf")
    imprimer_pdf(chemin_html, pdf, chromium)
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        os.replace(pdf, Path(chemin_png).with_suffix(".pdf"))
        raise FileNotFoundError("pdftoppm absent : PDF de la bannière produit, à convertir en PNG")
    base = str(Path(chemin_png).with_suffix(""))
    subprocess.run([pdftoppm, "-png", "-scale-to-x", str(l), "-scale-to-y", str(h), "-singlefile", str(pdf), base], check=True, capture_output=True, timeout=60)
    pdf.unlink(missing_ok=True)


def pages_pdf(chemin):
    data = Path(chemin).read_bytes()
    return len(re.findall(rb"/Type\s*/Page(?!s)", data))


def main():
    p = argparse.ArgumentParser(description="Construit un carrousel LinkedIn en PDF (0 PDF / 2 HTML seul ou avertissements / 3 bloquant).")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--fichier", help="JSON des slides")
    src.add_argument("--exemple", action="store_true")
    p.add_argument("--sortie", default="carrousel.pdf", help="chemin du PDF (le HTML est écrit à côté)")
    p.add_argument("--verifier", action="store_true", help="contrôler les textes seulement")
    p.add_argument("--chromium", help="chemin de Chromium ou Chrome")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    try:
        if a.exemple:
            c = EXEMPLE
        elif a.fichier:
            c = json.loads(Path(a.fichier).read_text(encoding="utf-8"))
        else:
            p.print_help(sys.stderr)
            return 1
    except (OSError, json.JSONDecodeError) as err:
        print(f"Erreur : {err}", file=sys.stderr)
        return 1

    bloquants, attentions = controler(c)
    res = {"slides": len(c.get("slides") or []), "bloquants": bloquants, "attentions": attentions,
           "html": None, "pdf": None, "pages": None, "poids_mo": None}
    if bloquants or a.verifier:
        res["verdict"] = "BLOQUÉ" if bloquants else ("À REVOIR" if attentions else "TEXTES OK")
        code = 3 if bloquants else (2 if attentions else 0)
    else:
        sortie = Path(a.sortie)
        chemin_html = sortie.with_suffix(".html")
        chemin_html.write_text(construire_html(c), encoding="utf-8")
        res["html"] = str(chemin_html)
        chromium = trouver_chromium(a.chromium)
        if chromium and c.get("format") == "banniere":
            try:
                png = sortie.with_suffix(".png")
                imprimer_png(chemin_html, png, chromium, *FORMATS["banniere"])
                res["pdf"] = str(png)
                res["pages"] = 1
                res["poids_mo"] = round(png.stat().st_size / 1e6, 2)
                if res["poids_mo"] > 8:
                    bloquants.append("Image au-delà de 8 Mo (limite officielle de la bannière).")
            except (subprocess.SubprocessError, OSError) as err:
                attentions.append(f"Chromium n'a pas produit l'image ({err.__class__.__name__}) : fais une capture du HTML à 1 584 × 396.")
        elif chromium:
            try:
                imprimer_pdf(chemin_html, sortie, chromium)
                res["pdf"] = str(sortie)
                res["pages"] = pages_pdf(sortie)
                res["poids_mo"] = round(sortie.stat().st_size / 1e6, 2)
                if res["pages"] != res["slides"]:
                    attentions.append(f"Le PDF a {res['pages']} pages pour {res['slides']} slides : vérifie l'impression.")
                if res["poids_mo"] > 100 or res["pages"] > 300:
                    bloquants.append("PDF au-delà des limites LinkedIn (100 Mo, 300 pages).")
            except (subprocess.SubprocessError, OSError) as err:
                attentions.append(f"Chromium n'a pas produit le PDF ({err.__class__.__name__}) : imprime le HTML depuis le navigateur.")
        else:
            attentions.append("Chromium introuvable : ouvre le HTML dans Chrome, Imprimer, « Enregistrer au format PDF », marges « Aucune ».")
        res["verdict"] = "BLOQUÉ" if bloquants else ("PDF PRÊT" if res["pdf"] and not attentions else "À REVOIR" if res["pdf"] else "HTML SEUL")
        code = 3 if bloquants else (0 if res["pdf"] and not attentions else 2)

    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"CARROUSEL  {res['verdict']}  ·  {res['slides']} slides")
        for b in bloquants:
            print(f"  ✖ {b}")
        for x in attentions:
            print(f"  ! {x}")
        if res["html"]:
            print(f"  HTML : {res['html']}")
        if res["pdf"]:
            print(f"  Fichier : {res['pdf']} · {res['pages']} pages · {res['poids_mo']} Mo")
    return code


if __name__ == "__main__":
    sys.exit(main())
