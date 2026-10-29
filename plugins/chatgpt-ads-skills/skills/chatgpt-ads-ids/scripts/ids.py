#!/usr/bin/env python3
"""ids.py : retrouve les identifiants ChatGPT Ads (campagnes, ad groups, annonces, images, conversions).

Python 3, sans dépendance. Deux voies, au choix :

  A. Par l'API officielle d'OpenAI Ads, en LECTURE SEULE (clé dans la variable
     d'environnement OPENAI_ADS_API_KEY, créée dans Ads Manager > Settings ;
     une clé = un compte publicitaire). La clé n'est jamais affichée ni écrite.
  B. Sans API : depuis un fichier exporté (Ads Manager, classeur déjà rempli),
     les identifiants sont repérés par leur préfixe (cmpn_, adgrp_, ad_, file_, ces_).

Commandes :

  compte                         nom, devise, fuseau, statut et revue du compte
  lister [--campagne ID] [--annonces] [-o ids.csv]
                                 campagnes et ad groups (et annonces avec --annonces) ;
                                 sans -o, tableau Markdown
  chercher NOM [--niveau campagne|groupe] [--campagne ID]
                                 recherche exacte, sans casse (API)
  evenements                     événements de conversion (conversion_event_setting_ids, ces_…)
  depuis-fichier FICHIER [-o ids.csv]
                                 voie B : identifiants repérés dans un CSV ou un XLSX
  fusionner CIBLE --ids ids.csv -o SORTIE [--ad-id]
                                 reporte les ad_group_id (et, avec --ad-id, les ad_id)
                                 dans un fichier au schéma d'annonces (CSV ou XLSX) ou un JSON de campagne,
                                 par nom de groupe (et d'annonce) ; signale les noms ambigus
  utm                            modèle de paramètres de suivi avec les macros documentées
  televerser SOURCE --confirmer  ÉCRITURE : téléverse une image (URL ou fichier) et rend son
                                 image_file_id ; ne crée ni ne modifie aucune annonce

Codes de sortie : 0 ok · 2 à revoir (noms ambigus, identifiants manquants) · 3 erreur d'API · 1 usage.
"""
import argparse
import csv
import io
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ICI = Path(__file__).resolve()
for base in (ICI.parents[1] / "commun", ICI.parents[2] / "commun"):   # Skill seul, ou ZIP claude.ai
    if (base / "classeur.py").exists():
        sys.path.insert(0, str(base))
        break
import classeur as cl  # noqa: E402

API = "https://api.ads.openai.com/v1"
PREFIXES = {"cmpn_": "campaign_id", "adgrp_": "ad_group_id", "ad_": "ad_id", "file_": "image_file_id",
            "ces_": "conversion_event_setting_id"}
COLONNES_IDS = ["niveau", "campaign_id", "campaign_name", "ad_group_id", "adgroup_name", "ad_id", "ad_name",
                "status", "review_status", "image_file_id", "title"]
# Macros de suivi citées par la documentation (landing_page_configuration.query_string_template), relue le 20 oct. 2026.
MACROS = {"{campaign_id}": "identifiant de la campagne", "{ad_id}": "identifiant de l'annonce",
          "{oppref}": "référence du clic (exemple de la documentation : click_id)"}


class ErreurAPI(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def transport_http(methode, url, entetes, corps):
    req = urllib.request.Request(url, data=corps, method=methode, headers=entetes)
    try:
        with urllib.request.urlopen(req, timeout=30) as rep:
            return rep.status, dict(rep.headers), rep.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read() if e.fp else b""


class Client:
    """Client minimal ; `transport(methode, url, entetes, corps)` → (code, entêtes, octets), remplaçable en test."""

    def __init__(self, cle, transport=None, pause=time.sleep):
        if not cle:
            raise ErreurAPI(0, "clé absente : définir OPENAI_ADS_API_KEY dans le terminal (Ads Manager > Settings), "
                               "jamais dans la conversation")
        self.cle, self.transport, self.pause = cle, transport or transport_http, pause

    def requete(self, methode, chemin, params=None, json_corps=None, brut=None, type_contenu=None):
        url = API + chemin + ("?" + urllib.parse.urlencode(params) if params else "")
        entetes = {"Authorization": f"Bearer {self.cle}", "Accept": "application/json"}
        corps = None
        if json_corps is not None:
            corps, entetes["Content-Type"] = json.dumps(json_corps).encode(), "application/json"
        elif brut is not None:
            corps, entetes["Content-Type"] = brut, type_contenu
        for essai in range(4):
            code, h, octets = self.transport(methode, url, entetes, corps)
            if code == 429 and essai < 3:
                attente = h.get("Retry-After") or h.get("retry-after")
                self.pause(float(attente) if attente and str(attente).replace(".", "").isdigit() else 2 ** (essai + 1))
                continue
            break
        try:
            donnees = json.loads(octets.decode() or "{}")
        except (ValueError, UnicodeDecodeError):
            donnees = {}
        if code >= 400:
            msg = (donnees.get("error") or {}).get("message") if isinstance(donnees, dict) else None
            conseil = {401: "clé refusée : vérifier OPENAI_ADS_API_KEY (Ads Manager > Settings)",
                       403: "accès refusé : la clé appartient-elle à ce compte ? fonction ouverte au compte ?",
                       404: "introuvable : identifiant exact, bon compte, bon type de ressource",
                       429: "trop de requêtes : réessayer dans une minute"}.get(code, "")
            raise ErreurAPI(code, f"HTTP {code}" + (f" : {msg}" if msg else "") + (f" ({conseil})" if conseil else ""))
        return donnees

    def tout(self, chemin, params=None):
        """Toutes les pages d'une liste (curseur after = last_id)."""
        params = dict(params or {}, limit=500)
        res = []
        while True:
            page = self.requete("GET", chemin, params)
            res += page.get("data", [])
            if not page.get("has_more") or not page.get("last_id"):
                return res
            params["after"] = page["last_id"]


# ---------------------------------------------------------------- voie A : API

def inventaire(client, campagne=None, annonces=False):
    lignes = []
    campagnes = [client.requete("GET", f"/campaigns/{campagne}")] if campagne else client.tout("/campaigns")
    for c in campagnes:
        lignes.append({"niveau": "campagne", "campaign_id": c.get("id", ""), "campaign_name": c.get("name", ""),
                       "status": c.get("status", "")})
        for g in client.tout("/ad_groups", {"campaign_id": c.get("id")}):
            lignes.append({"niveau": "groupe", "campaign_id": c.get("id", ""), "campaign_name": c.get("name", ""),
                           "ad_group_id": g.get("id", ""), "adgroup_name": g.get("name", ""), "status": g.get("status", "")})
            if annonces:
                for a in client.tout("/ads", {"ad_group_id": g.get("id")}):
                    cr = a.get("creative") or {}
                    lignes.append({"niveau": "annonce", "campaign_id": c.get("id", ""), "campaign_name": c.get("name", ""),
                                   "ad_group_id": g.get("id", ""), "adgroup_name": g.get("name", ""),
                                   "ad_id": a.get("id", ""), "ad_name": a.get("name", ""), "status": a.get("status", ""),
                                   "review_status": a.get("review_status", ""), "image_file_id": cr.get("file_id", ""),
                                   "title": cr.get("title", "")})
    return lignes


def televerser(client, source):
    if re.match(r"https?://", source):
        return client.requete("POST", "/upload", json_corps={"image_url": source})
    p = Path(source)
    contenu = p.read_bytes()
    limite = uuid.uuid4().hex
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    corps = (f"--{limite}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{p.name}\"\r\n"
             f"Content-Type: {mime}\r\n\r\n").encode() + contenu + f"\r\n--{limite}--\r\n".encode()
    return client.requete("POST", "/upload", brut=corps, type_contenu=f"multipart/form-data; boundary={limite}")


# ---------------------------------------------------------------- voie B : fichier

def ids_depuis_fichier(chemin):
    """Repère les identifiants par préfixe et les noms par en-tête, ligne par ligne."""
    classeur = cl.lire(chemin)
    lignes = []
    noms_entetes = {
        "campaign_name": r"^(campaign(_| )?name|campaign|nom de (la )?campagne|campagne)$",
        "adgroup_name": r"^(ad ?_?group(_| )?name|adgroup_name|ad group|nom du groupe( d'annonces)?|groupe d'annonces)$",
        "ad_name": r"^(ad(_| )?name|nom de l'annonce|annonce)$",
        "title": r"^(title|titre)$",
    }
    for o in classeur["onglets"]:
        tete = {j: cl.plier(cl.texte(c["valeur"])) for j, c in o["lignes"].get(1, {}).items()}
        cols_noms = {champ: j for champ, motif in noms_entetes.items() for j, t in tete.items() if re.match(motif, t)}
        for num in sorted(n for n in o["lignes"] if n > 1):
            cel = o["lignes"][num]
            ligne = {}
            for j, c in cel.items():
                v = cl.texte(c["valeur"]).strip()
                for pref, champ in sorted(PREFIXES.items(), key=lambda x: -len(x[0])):
                    if re.fullmatch(re.escape(pref) + r"[A-Za-z0-9_-]+", v):
                        if champ == "ad_id" and v.startswith("adgrp_"):
                            continue
                        ligne.setdefault(champ, v)
                        break
            if not ligne:
                continue
            for champ, j in cols_noms.items():
                if j in cel:
                    ligne[champ] = cl.texte(cel[j]["valeur"]).strip()
            ligne["niveau"] = "annonce" if ligne.get("ad_id") else "groupe" if ligne.get("ad_group_id") else \
                "campagne" if ligne.get("campaign_id") else "autre"
            ligne["_source"] = f"{o['nom']} ligne {num}"
            lignes.append(ligne)
    return lignes


# ---------------------------------------------------------------- fusion

def lire_ids(chemin):
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def table_groupes(ids):
    """nom plié → {identifiants} ; plusieurs identifiants = nom ambigu."""
    t = {}
    for x in ids:
        if x.get("ad_group_id") and x.get("adgroup_name"):
            t.setdefault(cl.plier(x["adgroup_name"]), set()).add(x["ad_group_id"])
    return t


def table_annonces(ids):
    t = {}
    for x in ids:
        if x.get("ad_id") and x.get("ad_name"):
            t.setdefault((cl.plier(x.get("adgroup_name", "")), cl.plier(x["ad_name"])), set()).add(x["ad_id"])
    return t


def fusionner(lignes, ids, avec_ad_id=False, cle_groupe="adgroup_name"):
    """Complète ad_group_id (et ad_id) sans jamais écraser une valeur existante différente sans le dire."""
    tg, ta = table_groupes(ids), table_annonces(ids)
    journal, a_revoir = [], 0
    for i, x in enumerate(lignes):
        ou = f"ligne {x['_ligne']}" if "_ligne" in x else f"{i + 1}"
        nom = cl.plier(x.get(cle_groupe, ""))
        trouves = tg.get(nom, set())
        actuel = cl.texte(x.get("ad_group_id", "")).strip()
        if len(trouves) > 1:
            journal.append(f"{ou} : groupe « {x.get(cle_groupe)} » ambigu ({', '.join(sorted(trouves))}) : non rempli")
            a_revoir += 1
        elif len(trouves) == 1:
            (gid,) = trouves
            if actuel and actuel != gid:
                journal.append(f"{ou} : ad_group_id {actuel} ≠ {gid} trouvé pour « {x.get(cle_groupe)} » : gardé, à vérifier")
                a_revoir += 1
            elif not actuel:
                x["ad_group_id"] = gid
                journal.append(f"{ou} : ad_group_id ← {gid}")
        elif not actuel:
            journal.append(f"{ou} : aucun ad group « {x.get(cle_groupe)} » dans les identifiants")
            a_revoir += 1
        if avec_ad_id and "ad_name" in x:
            t = ta.get((nom, cl.plier(x.get("ad_name", ""))), set())
            if len(t) == 1 and not cl.texte(x.get("ad_id", "")).strip():
                (aid,) = t
                x["ad_id"] = aid
                journal.append(f"{ou} : ad_id ← {aid} (la ligne MODIFIERA cette annonce existante)")
    return journal, a_revoir


# ---------------------------------------------------------------- sorties

def ecrire_csv(chemin, lignes):
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLONNES_IDS, extrasaction="ignore")
        w.writeheader()
        for x in lignes:
            w.writerow({c: x.get(c, "") for c in COLONNES_IDS})


def tableau(lignes, colonnes):
    out = ["| " + " | ".join(colonnes) + " |", "|" + "---|" * len(colonnes)]
    for x in lignes:
        out.append("| " + " | ".join(str(x.get(c, "")).replace("|", "/") for c in colonnes) + " |")
    return "\n".join(out)


def client_depuis_env(transport=None):
    return Client(os.environ.get("OPENAI_ADS_API_KEY", ""), transport)


def main(argv=None, transport=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("compte")
    li = sp.add_parser("lister")
    li.add_argument("--campagne")
    li.add_argument("--annonces", action="store_true")
    li.add_argument("-o", "--sortie")
    ch = sp.add_parser("chercher")
    ch.add_argument("nom")
    ch.add_argument("--niveau", choices=("campagne", "groupe"), default="groupe")
    ch.add_argument("--campagne")
    sp.add_parser("evenements")
    df = sp.add_parser("depuis-fichier")
    df.add_argument("fichier")
    df.add_argument("-o", "--sortie")
    fu = sp.add_parser("fusionner")
    fu.add_argument("cible")
    fu.add_argument("--ids", required=True)
    fu.add_argument("-o", "--sortie", required=True)
    fu.add_argument("--ad-id", action="store_true", help="reporter aussi ad_id : la ligne modifiera l'annonce existante")
    fu.add_argument("--xlsx", action="store_true", help="écrire un .xlsx au lieu du CSV (seulement si l'utilisateur le demande)")
    sp.add_parser("utm")
    tv = sp.add_parser("televerser")
    tv.add_argument("source")
    tv.add_argument("--confirmer", action="store_true")
    a = p.parse_args(argv)

    if a.cmd == "utm":
        print("utm_source=chatgpt&utm_medium=paid&utm_campaign={campaign_id}&utm_content={ad_id}&click_id={oppref}")
        print("\nÀ coller dans Ads Manager, paramètres de suivi (compte, campagne, ad group ou annonce).")
        for m, sens in MACROS.items():
            print(f"  {m:<15} {sens}")
        print("Les visites arrivent dans l'outil d'analyse avec l'identifiant de campagne et d'annonce : "
              "une autre façon de les retrouver. Macro d'ad group : non documentée [à vérifier].")
        return 0

    if a.cmd == "depuis-fichier":
        if not Path(a.fichier).exists():
            print(f"Fichier introuvable : {a.fichier}", file=sys.stderr)
            return 1
        lignes = ids_depuis_fichier(a.fichier)
        if not lignes:
            print("Aucun identifiant reconnu (cmpn_, adgrp_, ad_, file_, ces_). Exporter depuis Ads Manager "
                  "avec les colonnes d'identifiants, ou passer par l'API.")
            return 2
        if a.sortie:
            ecrire_csv(a.sortie, lignes)
            print(f"{len(lignes)} ligne(s) d'identifiants écrites dans {a.sortie}")
        else:
            print(tableau(lignes, ["niveau", "campaign_id", "campaign_name", "ad_group_id", "adgroup_name", "ad_id",
                                   "ad_name", "image_file_id", "_source"]))
        return 0

    if a.cmd == "fusionner":
        ids = lire_ids(a.ids)
        if a.cible.lower().endswith(".json"):
            camp = json.loads(Path(a.cible).read_text(encoding="utf-8"))
            journal, n = fusionner(camp.get("adgroups", []), ids)
            if a.ad_id:
                j2, _ = fusionner(camp.get("ads", []), ids, True)
                journal += [x for x in j2 if "ad_id ←" in x]
            Path(a.sortie).write_text(json.dumps(camp, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            _, lignes = cl.annonces(cl.lire(a.cible))
            journal, n = fusionner(lignes, ids, a.ad_id)
            a.sortie = str(cl.ecrire(a.sortie, [{c: x.get(c, "") for c in cl.COLONNES} for x in lignes], a.xlsx))
        print("\n".join(journal) or "Rien à reporter.")
        print(f"\nÉcrit : {a.sortie} · {n} point(s) à revoir")
        return 2 if n else 0

    try:
        client = Client(os.environ.get("OPENAI_ADS_API_KEY", ""), transport)
        if a.cmd == "compte":
            c = client.requete("GET", "/ad_account")
            for k in ("name", "id", "currency_code", "timezone", "status"):
                if c.get(k) is not None:
                    print(f"{k:<14} {c[k]}")
            if c.get("review"):
                print(f"{'review':<14} {json.dumps(c['review'], ensure_ascii=False)}")
            return 0
        if a.cmd == "lister":
            lignes = inventaire(client, a.campagne, a.annonces)
            if a.sortie:
                ecrire_csv(a.sortie, lignes)
                print(f"{len(lignes)} ligne(s) écrites dans {a.sortie}")
            else:
                cols = COLONNES_IDS if a.annonces else ["niveau", "campaign_id", "campaign_name", "ad_group_id",
                                                        "adgroup_name", "status"]
                print(tableau(lignes, cols))
            return 0
        if a.cmd == "chercher":
            if a.niveau == "campagne":
                res = client.requete("GET", "/campaigns", {"name": a.nom}).get("data", [])
            else:
                camps = [a.campagne] if a.campagne else [c["id"] for c in client.tout("/campaigns")]
                res = [g for cid in camps for g in client.requete("GET", "/ad_groups", {"campaign_id": cid, "name": a.nom}).get("data", [])]
            res = [r for r in res if cl.plier(r.get("name", "")) == cl.plier(a.nom)]
            for r in res:
                print(f"{r.get('id')}  {r.get('name')}  ({r.get('status', '')})")
            if len(res) > 1:
                print("Plusieurs résultats : le nom n'est pas unique, choisir par identifiant.")
            return 0 if len(res) == 1 else 2
        if a.cmd == "evenements":
            for e in client.tout("/conversions/event_settings"):
                print(f"{e.get('id')}  {e.get('name')}  {e.get('event_type')}  {'archivé' if e.get('archived') else ''}")
            return 0
        if a.cmd == "televerser":
            if not a.confirmer:
                print("Téléverser écrit une image dans le compte publicitaire (aucune annonce créée). "
                      "Relancer avec --confirmer après accord de l'annonceur.")
                return 1
            r = televerser(client, a.source)
            print(f"image_file_id : {r.get('file_id')}")
            return 0
    except ErreurAPI as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 3 if e.code else 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
