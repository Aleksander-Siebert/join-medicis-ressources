#!/usr/bin/env python3
"""
Mail de l'agent de veille concurrentielle (Join Médicis).

Lit sortie/resume.json (écrit par l'agent), contrôle que chaque info a une
source et que rien ne vient d'ailleurs que de sortie/a-traiter.json, puis
produit sortie/mail.html et sortie/mail.txt au format fixe. Avec --envoyer,
l'envoie par SMTP (mode GitHub Actions) à l'adresse MAIL_TO.

Python 3.9+ sans dépendance.

Utilisation :
  python3 scripts/mail.py                # contrôle + mail.html / mail.txt
  python3 scripts/mail.py --verifier     # contrôle seul (code 1 si une erreur bloque)
  python3 scripts/mail.py --envoyer      # + envoi SMTP (variables SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, MAIL_TO)
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import smtplib
import ssl
import sys
from email.message import EmailMessage
from pathlib import Path

MAX_A_RETENIR = 3
MAX_INFO_CARACTERES = 420

# ------------------------------------------------------------------ contrôle


def verifier(resume: dict, a_traiter: dict | None) -> tuple[list[str], list[str]]:
    """Renvoie (erreurs bloquantes, avertissements)."""
    erreurs: list[str] = []
    avert: list[str] = []
    urls_connues = set()
    domaines_connus = set()
    if a_traiter:
        for s in a_traiter.get("sujets", []):
            for src in s.get("sources", []):
                urls_connues.add(src.get("url", ""))
                if src.get("domaine") and src["domaine"] != "news.google.com":
                    domaines_connus.add(src["domaine"])
        for p in a_traiter.get("pages_modifiees", []):
            urls_connues.add(p.get("url", ""))

    if not resume.get("objet"):
        erreurs.append("Il manque l'objet du mail (« objet »).")
    retenir = resume.get("a_retenir", [])
    if len(retenir) > MAX_A_RETENIR:
        erreurs.append(f"« À retenir » contient {len(retenir)} points : {MAX_A_RETENIR} au plus.")

    infos = [i for sec in resume.get("sections", []) for i in sec.get("infos", [])]
    for n, info in enumerate(infos, 1):
        nom = info.get("titre") or f"info n° {n}"
        sources = info.get("sources", [])
        if not sources:
            erreurs.append(f"« {nom} » n'a aucune source : chaque info doit renvoyer à sa source.")
        for src in sources:
            url = src.get("url", "")
            if not url.startswith("http"):
                erreurs.append(f"« {nom} » : lien de source invalide ({url or 'vide'}).")
            elif a_traiter is not None and url not in urls_connues and domaine(url) not in domaines_connus:
                erreurs.append(
                    f"« {nom} » : la source {url} ne vient pas de la collecte (a-traiter.json), ni d'un média qu'elle a repéré. "
                    "Rien d'autre ne doit entrer dans le mail."
                )
        if len(info.get("texte", "")) > MAX_INFO_CARACTERES:
            avert.append(f"« {nom} » dépasse {MAX_INFO_CARACTERES} caractères : resserre en 2 ou 3 phrases.")
        if not info.get("pourquoi"):
            avert.append(f"« {nom} » n'a pas de « pourquoi c'est pour toi ».")

    tout = json.dumps(resume, ensure_ascii=False)
    if "—" in tout:
        avert.append("Tiret cadratin « — » trouvé : remplace-le par une virgule.")
    if re.search(r"\d \%", tout):
        avert.append("Pourcentage avec espace (« 15 % ») : écris « 15% ».")
    if re.search(r"\{\{[^}]*\}\}", tout):
        avert.append("Un {{à compléter}} est resté dans le mail.")
    if not infos and not resume.get("rien_de_neuf"):
        erreurs.append("Aucune info et « rien_de_neuf » absent : le mail ne dit rien.")
    return erreurs, avert


def domaine(url: str) -> str:
    from urllib.parse import urlsplit

    hote = urlsplit(url.strip()).netloc.lower().split(":")[0]
    return hote[4:] if hote.startswith("www.") else hote


# ------------------------------------------------------------------ rendu

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def date_fr(d: str | None) -> str:
    """« 2026-10-30 » devient « 30 octobre » ; le reste est gardé tel quel."""
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", d or "")
    if not m or not 1 <= int(m[2]) <= 12:
        return d or ""
    jour = int(m[3])
    return f"{'1er' if jour == 1 else jour} {MOIS[int(m[2]) - 1]}"


def nb_infos(r: dict) -> int:
    return sum(len(sec.get("infos", [])) for sec in r.get("sections", []))


def e(t: str) -> str:
    return html.escape(t or "", quote=True)


BLOC = re.compile(r"<!--\s*DEBUT:(\w+)\s*-->(.*?)<!--\s*FIN:\1\s*-->", re.S)
VARIABLE = re.compile(r"\{\{\s*(\w+)\s*\}\}")


def remplir(modele: str, ctx: dict) -> str:
    """Mini-gabarit : blocs <!-- DEBUT:x --> … <!-- FIN:x --> répétés ou retirés, puis {{x}} remplacés (texte protégé)."""

    def bloc(m: re.Match) -> str:
        nom, interieur = m.group(1), m.group(2)
        val = ctx.get(nom)
        if isinstance(val, list):
            return "".join(remplir(interieur, {**ctx, **(v if isinstance(v, dict) else {nom: v, "point": v})}) for v in val)
        return remplir(interieur, ctx) if val else ""

    texte = BLOC.sub(bloc, modele)
    return VARIABLE.sub(lambda m: e(str(ctx.get(m.group(1), "") or "")), texte)


def contexte(r: dict) -> dict:
    st = r.get("stats", {})
    pied = f'{st.get("lus", "?")} articles lus, {st.get("sujets", "?")} sujets trouvés, {nb_infos(r)} retenus dans ce mail, {st.get("pages_modifiees", 0)} pages modifiées.'
    if r.get("erreurs"):
        pied += " Sources injoignables : " + ", ".join(r["erreurs"]) + "."
    sections = []
    for sec in r.get("sections", []):
        infos = [
            {
                "titre": i.get("titre", ""),
                "date": f"· {date_fr(i['date'])}" if i.get("date") else "",
                "texte": i.get("texte", ""),
                "pourquoi": i.get("pourquoi", ""),
                "source": [{"nom": s.get("nom") or "source", "url": s.get("url", "")} for s in i.get("sources", [])],
            }
            for i in sec.get("infos", [])
        ]
        if infos:
            sections.append({"section": sec.get("titre", ""), "info": infos})
    return {
        "objet": r.get("objet", ""),
        "periode": r.get("periode", ""),
        "pied": pied,
        "rien_de_neuf": r.get("rien_de_neuf", ""),
        "a_retenir": bool(r.get("a_retenir")),
        "point": r.get("a_retenir", []),
        "section": sections,
        "a_surveiller": bool(r.get("a_surveiller")),
        "surveiller": r.get("a_surveiller", []),
    }


def rendre_html(r: dict, modele: str | None = None) -> str:
    """Remplit modele-mail.html (à la racine de l'agent) avec le résumé."""
    if modele is None:
        modele = (Path(__file__).resolve().parent.parent / "modele-mail.html").read_text("utf-8")
    modele = re.sub(r"<!--(?!\s*(DEBUT|FIN):).*?-->", "", modele, flags=re.S)  # retire les commentaires d'aide
    return remplir(modele, contexte(r))


def rendre_texte(r: dict) -> str:
    l = [r.get("objet", ""), f"Veille concurrentielle · {r.get('periode', '')}", ""]
    if r.get("rien_de_neuf"):
        l += [r["rien_de_neuf"], ""]
    if r.get("a_retenir"):
        l.append("À RETENIR")
        l += [f"{i}. {pt}" for i, pt in enumerate(r["a_retenir"], 1)]
        l.append("")
    for sec in r.get("sections", []):
        if not sec.get("infos"):
            continue
        l.append(sec.get("titre", "").upper())
        for info in sec["infos"]:
            l.append(f"- {info.get('titre')}" + (f" ({date_fr(info['date'])})" if info.get("date") else ""))
            l.append(f"  {info.get('texte')}")
            if info.get("pourquoi"):
                l.append(f"  Pour toi : {info['pourquoi']}")
            for s in info.get("sources", []):
                l.append(f"  Source : {s.get('nom')} {s.get('url')}")
        l.append("")
    if r.get("a_surveiller"):
        l.append("À SURVEILLER")
        l += [f"- {pt}" for pt in r["a_surveiller"]]
        l.append("")
    st = r.get("stats", {})
    l.append(f"{st.get('lus', '?')} articles lus, {st.get('sujets', '?')} sujets trouvés, {nb_infos(r)} retenus dans ce mail, {st.get('pages_modifiees', 0)} pages modifiées.")
    return "\n".join(l)


# ------------------------------------------------------------------ envoi


def envoyer(objet: str, texte: str, html_corps: str) -> str:
    manquantes = [v for v in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "MAIL_TO") if not os.environ.get(v)]
    if manquantes:
        raise SystemExit("Envoi impossible, variables manquantes : " + ", ".join(manquantes))
    msg = EmailMessage()
    msg["Subject"] = objet
    msg["From"] = os.environ.get("MAIL_FROM") or os.environ["SMTP_USER"]
    msg["To"] = os.environ["MAIL_TO"]
    msg.set_content(texte)
    msg.add_alternative(html_corps, subtype="html")
    port = int(os.environ.get("SMTP_PORT", "465"))
    if port == 465:
        with smtplib.SMTP_SSL(os.environ["SMTP_HOST"], port, context=ssl.create_default_context(), timeout=30) as s:
            s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            s.send_message(msg)
    else:
        with smtplib.SMTP(os.environ["SMTP_HOST"], port, timeout=30) as s:
            s.starttls(context=ssl.create_default_context())
            s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            s.send_message(msg)
    return f"Mail envoyé à {os.environ['MAIL_TO']}."


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Mail de l'agent de veille")
    ap.add_argument("--dossier", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--verifier", action="store_true", help="contrôle seul")
    ap.add_argument("--envoyer", action="store_true", help="envoi SMTP (mode GitHub Actions)")
    a = ap.parse_args(argv)
    d = Path(a.dossier) / "sortie"
    f = d / "resume.json"
    if not f.exists():
        print("sortie/resume.json introuvable : l'agent doit d'abord l'écrire.", file=sys.stderr)
        return 1
    try:
        resume = json.loads(f.read_text("utf-8"))
    except json.JSONDecodeError as ex:
        print(f"resume.json invalide (ligne {ex.lineno}) : {ex.msg}", file=sys.stderr)
        return 1
    at = d / "a-traiter.json"
    a_traiter = json.loads(at.read_text("utf-8")) if at.exists() else None
    erreurs, avert = verifier(resume, a_traiter)
    for x in avert:
        print(f"ATTENTION : {x}")
    for x in erreurs:
        print(f"BLOQUANT : {x}")
    if erreurs:
        return 1
    if a.verifier:
        print("Contrôle réussi.")
        return 0
    modele_f = Path(a.dossier) / "modele-mail.html"
    corps_html = rendre_html(resume, modele_f.read_text("utf-8") if modele_f.exists() else None)
    corps_txt = rendre_texte(resume)
    (d / "mail.html").write_text(corps_html, "utf-8")
    (d / "mail.txt").write_text(corps_txt, "utf-8")
    print("Mail prêt : sortie/mail.html et sortie/mail.txt")
    if a.envoyer:
        print(envoyer(resume["objet"], corps_txt, corps_html))
    return 0


if __name__ == "__main__":
    sys.exit(main())
