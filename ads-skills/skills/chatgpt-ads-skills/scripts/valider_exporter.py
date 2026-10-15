#!/usr/bin/env python3
"""Valide une campagne ChatGPT Ads et écrit le fichier d'import XLSX (Python 3, sans dépendance).

Les LLM comptent mal : tout ce qui se compte ou se vérifie passe par ce script.

Commandes :

  modele [MODELE.xlsx]
      Relit le modèle d'import : onglets, colonnes, champs obligatoires,
      limites de caractères (lues dans le modèle, ligne 2). Par défaut, le
      modèle du pack (assets/modele-import.xlsx) ; le modèle téléchargé dans
      Ads Manager se lit de la même façon.

  valider SOURCE [--modele M] [--aujourdhui AAAA-MM-JJ] [--json] [--allegations CAMPAGNE.json]
      SOURCE : la campagne en JSON (format ci-dessous) ou un XLSX déjà rempli.
      Un XLSX ne contient pas la liste des allégations : --allegations la
      reprend d'un JSON de campagne ; sans elle, chaque chiffre ou promesse
      est à vérifier à la main.
      Contrôle longueurs, JSON des context hints, noms identiques et uniques
      entre onglets, champs obligatoires, doublons, URL, nombre d'annonces
      par groupe, termes vagues, lieux et chevauchements des hints,
      allégations non étayées, éligibilité de la catégorie selon les pays
      (règles publicitaires d'OpenAI v1.6), imitation de ChatGPT.

  exporter SOURCE -o SORTIE.xlsx [--modele M]
      Valide, puis écrit le XLSX au format exact du modèle : 3 onglets, en-têtes,
      mise en forme et contrôles de saisie conservés, ligne d'exemple retirée
      s'il y en a une, texte normal (pas d'italique). Refuse d'écrire s'il
      reste un point BLOQUANT.

  tableaux SOURCE
      Repli sans fichier : les 3 onglets en tableaux à coller (tabulations).

  relecture SOURCE
      Tableau de relecture humaine (Markdown) : intentions, hints, idée de
      visuel, annonces avec leurs longueurs, l'allégation utilisée.

Codes de sortie : 0 rien à revoir · 2 points d'attention · 3 bloquant · 1 erreur d'usage.

Format JSON de la campagne (champs facultatifs entre crochets) :

  {"annonceur": {"marque": "Vélora", "concurrents": ["…"], "domaines": ["velora.example"],
                 "categorie": "consommation"},
   "mode": "standard" | "grande-echelle",
   "allegations": [{"texte": "Garantie 12 mois", "source": "https://…", "statut": "approuvée"}],
   "campaigns": [{"campaign_name", "budget_max", [budget_type, launch_date, end_date,
                  objective, conversion_event_setting_ids, target_countries]}],
   "adgroups": [{"campaign_name", "adgroup_name", [max_bid], "context_hints": [...],
                 [intention, prompts_test, idee_visuel]}],
   "ads": [{"adgroup_name", "title", "copy", "link", "image_link", [angle, allegation]}]}

Exemple complet : assets/exemple-campagne.json.
"""
import argparse
import datetime as dt
import json
import re
import sys
import unicodedata
import urllib.parse
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ICI = Path(__file__).resolve().parent
MODELE_DEFAUT = ICI.parent / "assets" / "modele-import.xlsx"
ONGLETS = ("campaigns", "adgroups", "ads")
BLOQUANT, ATTENTION, INFO = "BLOQUANT", "ATTENTION", "INFO"

# Rôles de style : traduits en index de style du modèle par _styles_donnees (jamais d'italique).
STYLE_TEXTE, STYLE_DATE = "texte", "date"

# Codes ISO 3166-1 alpha-2 attribués.
ISO = set("""AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ
BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE
EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR
HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS
LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL
NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI
SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY
UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW""".split())
FAUX_CODES = {"UK": "GB", "EL": "GR", "EN": "GB"}

# Hints trop vagues pour décrire une situation (brief et Help Center : thème large, pas étiquette).
VAGUES = {"logiciel", "logiciels", "application", "applications", "appli", "app", "shopping", "achat",
          "achats", "voyage", "voyages", "ia", "ai", "intelligence artificielle", "software", "travel",
          "assurance", "assurances", "banque", "mode", "sante", "finance", "marketing", "business",
          "produit", "produits", "service", "services", "solution", "solutions", "outil", "outils",
          "offre", "offres", "promo", "promotion", "deal", "cadeau", "cadeaux", "technologie", "tech",
          "saas", "b2b", "b2c", "ecommerce", "e-commerce"}
MOTS_VIDES = set("""a au aux avec ce ces cet cette d de des du en et l la le les leur leurs mon ma mes
notre nos ou par pour sa se ses son sur ta te tes ton un une vos votre à the a an and of for to in on
with your my qu que qui dans est sont plus pas ne n s y il elle on nous vous je j""".split())

# Ce qui, dans une annonce, est une allégation à étayer.
SUPERLATIFS = re.compile(r"\b(meilleur(?:e|s|es)?|n\s?°\s?1|numéro\s?1|leader|le plus|la plus|les plus|moins cher(?:e|s|es)?|"
                         r"unique|premier(?:e|s|es)?|imbattable|garanti(?:e|s|es)?|garantie|100\s?%|sans risque|"
                         r"gratuit(?:e|s|es)?|offert(?:e|s|es)?|rembours(?:é|ée|és|ées|ement)|sans engagement|"
                         r"certifi(?:é|ée|és|ées)|agré(?:é|ée|és|ées)|best|cheapest|free|guaranteed?)\b", re.I)
NOMBRES = re.compile(r"\d+(?:[.,   ]\d+)*\s?(?:%|€|\$|£|h\b|min\b|jours?\b|mois\b|ans?\b|k€|x\b)?", re.I)
# Catégories d'annonceur (Ad Policies d'OpenAI, v1.6, septembre 2026 ; relu le 15 oct. 2026).
CATEGORIES = {
    **dict.fromkeys(["maison", "consommation", "style_de_vie", "services_locaux", "voyage", "divertissement",
                     "numerique", "logiciel", "education"], "autorisee"),
    **dict.fromkeys(["finance", "assurance", "sante", "juridique"], "restreinte_us"),
    **dict.fromkeys(["alcool", "tabac", "jeux_argent", "rencontres", "adulte", "politique", "substances", "armes",
                     "contrefacon", "bien_etre_allegations", "dette", "offre_emploi", "annonce_logement"], "interdite"),
}
# Termes qui signalent une catégorie restreinte ou interdite (contrôle lexical : à confirmer par une personne).
SIGNAUX = {
    "alcool": r"\b(?:vins?|bières?|whisky|spiritueux|alcools?|cocktails?|champagnes?|wines?|beers?|liquor)\b",
    "tabac": r"\b(?:cigarettes?|vapes?|vapoteuses?|e-liquides?|nicotine|tabac|tobacco)\b",
    "jeux_argent": r"\b(?:casinos?|paris sportifs|parier|poker|loteries?|betting|gambling)\b",
    "rencontres": r"\b(?:sites? de rencontres?|célibataires|dating)\b",
    "finance": r"\b(?:crédits?|prêts? (?:immobiliers?|personnels?|auto|étudiants?|à taux)|emprunts?|taux d'intérêt|investir|investissements?|placements?|bourse|crypto\w*|loans?|mortgages?)\b",
    "assurance": r"\b(?:assurances?|mutuelles?|prévoyance|insurance)\b",
    "sante": r"\b(?:médecins?|médical(?:e|es|aux)?|traitements?|guérir|soigner|thérapies?|symptômes?|diagnostics?|médicaments?|pharmacies?|dentaires?)\b",
    "juridique": r"\b(?:avocats?|conseil juridique|litiges?|divorces?|lawyers?)\b",
    "bien_etre_allegations": r"\b(?:détox|minceur|maigrir|perte de poids|brûle-graisses?|weight loss)\b",
    "substances": r"\b(?:cannabis|thc|cbd|psychédéliques?)\b",
    "armes": r"\b(?:armes? à feu|fusils?|pistolets?|munitions?|firearms?|guns?)\b",
    "politique": r"\b(?:élections?|référendum|candidats?|partis? politiques?|votez)\b",
    "offre_emploi": r"\b(?:offres? d'emploi|nous recrutons|on recrute|job offer)\b",
}
IMITATION = re.compile(r"\b(?:chat\s?gpt|openai|gpt-?\d\w*)\b|^\s*(?:réponse|answer)\s*:", re.I)
GEO_HINT = re.compile(r"\b(?:en|à|au|aux|in)\s+(?:France|Belgique|Suisse|Luxembourg|Canada|Québec|Europe|Paris|Lyon|Marseille|"
                      r"Toulouse|Bordeaux|Lille|Nantes|Bruxelles|Genève|Montréal)\b", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⬀-⯿]")


# ---------------------------------------------------------------- outils texte

def plier(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()


def longueur(s):
    """Caractères affichés (forme NFC) : « é » compte pour 1."""
    return len(unicodedata.normalize("NFC", str(s or "")))


def racine(mot):
    m = plier(mot)
    for fin in ("ements", "ement", "ations", "ation", "euses", "euse", "eurs", "eur", "ees", "ee",
                "es", "s", "e"):
        if len(m) > len(fin) + 3 and m.endswith(fin):
            return m[: -len(fin)]
    return m


def mots(s):
    return [m for m in re.findall(r"[\w']+", plier(s)) if m not in MOTS_VIDES]


def termes(s):
    return {racine(m) for m in mots(s)}


def jaccard(a, b):
    a, b = termes(a), termes(b)
    return len(a & b) / len(a | b) if a and b else 0.0


def nombre(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    t = re.sub(r"[\s  €$]", "", str(v)).replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def lire_date(v):
    if v in (None, ""):
        return None
    if isinstance(v, (int, float)):
        return dt.date(1899, 12, 30) + dt.timedelta(days=int(v))
    t = str(v).strip()
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return dt.datetime.strptime(t, f).date()
        except ValueError:
            pass
    return None


def serie_excel(d):
    return (d - dt.date(1899, 12, 30)).days


def liste_json(v):
    """(liste, erreur) depuis une liste Python ou une chaîne JSON."""
    if v is None or v == "":
        return [], None
    if isinstance(v, list):
        return v, None
    try:
        x = json.loads(str(v))
    except json.JSONDecodeError as e:
        return None, f"JSON invalide ({e.msg})"
    if not isinstance(x, list):
        return None, "attendu : un tableau JSON, par exemple [\"un\", \"deux\"]"
    return x, None


# ---------------------------------------------------------------- modèle

def _cellules_ligne(xml, num):
    m = re.search(rf'<(?:\w+:)?row r="{num}"[^>]*>(.*?)</(?:\w+:)?row>', xml, re.S)
    if not m:
        return {}
    res = {}
    for ref, corps in re.findall(r'<(?:\w+:)?c r="([A-Z]+)\d+"[^>]*?(?:/>|>(.*?)</(?:\w+:)?c>)', m.group(1), re.S):
        t = re.search(r"<(?:\w+:)?t[^>]*>(.*?)</(?:\w+:)?t>|<(?:\w+:)?v>(.*?)</(?:\w+:)?v>", corps or "", re.S)
        res[ref] = _desechapper((t.group(1) or t.group(2)) if t else "")
    return res


def _desechapper(s):
    return (s or "").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'") \
        .replace("&amp;", "&")


def _chemins_onglets(z):
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8-sig")
    cibles = {}
    for rel in re.findall(r"<Relationship\b[^>]*>", rels):
        i, t = re.search(r'Id="([^"]+)"', rel), re.search(r'Target="([^"]+)"', rel)
        if i and t:
            cibles[i.group(1)] = t.group(1)
    res = {}
    for nom, rid in re.findall(r'<(?:\w+:)?sheet name="([^"]+)"[^>]*?\bid="([^"]+)"', wb):
        cible = cibles[rid].lstrip("/")
        res[nom] = cible if cible.startswith("xl/") else "xl/" + cible
    return res


def lire_modele(chemin=MODELE_DEFAUT):
    """Colonnes, obligations et limites lues dans le modèle."""
    with zipfile.ZipFile(chemin) as z:
        onglets = _chemins_onglets(z)
        res = {"onglets": list(onglets), "colonnes": {}, "statut": {}, "aide": {}}
        for nom, chemin_xml in onglets.items():
            xml = z.read(chemin_xml).decode("utf-8")
            l1, l2, l3 = (_cellules_ligne(xml, n) for n in (1, 2, 3))
            cols = sorted(l1, key=lambda c: (len(c), c))
            res["colonnes"][nom] = [(c, l1[c]) for c in cols]
            res["statut"][nom] = {l1[c]: l2.get(c, "") for c in cols}
            res["aide"][nom] = {l1[c]: l3.get(c, "") for c in cols}
    limites = {}
    for champ in ("title", "copy"):
        m = re.search(r"max\s+(\d+)\s+char|(\d+)\s*caract", res["statut"].get("ads", {}).get(champ, ""), re.I)
        limites[champ] = int(m.group(1) or m.group(2)) if m else {"title": 24, "copy": 48}[champ]
    res["limites"] = limites
    return res


def cle(entete):
    return re.sub(r"\s+", "_", entete.strip().lower())


# ---------------------------------------------------------------- lecture d'un XLSX rempli

def lire_xlsx(chemin):
    """Campagne depuis un XLSX au format du modèle (données à partir de la ligne 4)."""
    camp = {"campaigns": [], "adgroups": [], "ads": [], "_source_xlsx": True}
    with zipfile.ZipFile(chemin) as z:
        partages = []
        if "xl/sharedStrings.xml" in z.namelist():
            ss = z.read("xl/sharedStrings.xml").decode("utf-8")
            for si in re.findall(r"<(?:\w+:)?si>(.*?)</(?:\w+:)?si>", ss, re.S):
                partages.append(_desechapper("".join(re.findall(r"<(?:\w+:)?t[^>]*>(.*?)</(?:\w+:)?t>", si, re.S))))
        onglets = _chemins_onglets(z)
        camp["_onglets"] = list(onglets)
        for nom, chemin_xml in onglets.items():
            if nom not in ONGLETS:
                continue
            xml = z.read(chemin_xml).decode("utf-8")
            entetes = {c: cle(v) for c, v in _cellules_ligne(xml, 1).items()}
            for num, corps in re.findall(r'<(?:\w+:)?row r="(\d+)"[^>]*>(.*?)</(?:\w+:)?row>', xml, re.S):
                if int(num) < 4:
                    continue
                ligne = {}
                for ref, attrs, contenu in re.findall(r'<(?:\w+:)?c r="([A-Z]+)\d+"([^>]*?)(?:/>|>(.*?)</(?:\w+:)?c>)', corps, re.S):
                    if ref not in entetes or not contenu:
                        continue
                    t = re.search(r'<(?:\w+:)?t[^>]*>(.*?)</(?:\w+:)?t>|<(?:\w+:)?v>(.*?)</(?:\w+:)?v>', contenu, re.S)
                    if not t:
                        continue
                    val = _desechapper(t.group(1) if t.group(1) is not None else t.group(2))
                    if 't="s"' in attrs:
                        val = partages[int(val)]
                    elif 't="n"' in attrs or ('t="' not in attrs and t.group(2) is not None):
                        val = float(val) if re.fullmatch(r"-?\d+(\.\d+)?", val) else val
                    ligne[entetes[ref]] = val
                if any(str(v).strip() for v in ligne.values()):
                    ligne["_ligne"] = int(num)
                    camp[nom].append(ligne)
    for g in camp["adgroups"]:
        if "context_hints" in g:
            g["context_hints_brut"] = g.pop("context_hints")
    return camp


# ---------------------------------------------------------------- contrôles

class Rapport:
    def __init__(self):
        self.points = []

    def ajoute(self, niveau, onglet, ou, message, conseil=""):
        self.points.append({"niveau": niveau, "onglet": onglet, "ou": ou, "message": message, "conseil": conseil})

    def compte(self, niveau):
        return sum(1 for p in self.points if p["niveau"] == niveau)

    def code(self):
        return 3 if self.compte(BLOQUANT) else 2 if self.compte(ATTENTION) else 0


def _nom(r, onglet, ou, champ, valeur):
    if not str(valeur or "").strip():
        r.ajoute(BLOQUANT, onglet, ou, f"{champ} vide (obligatoire)")
        return
    v = str(valeur)
    if not 3 <= len(v) <= 1000:
        r.ajoute(BLOQUANT, onglet, ou, f"{champ} « {v} » : {len(v)} caractère(s), de 3 à 1 000 attendus (docs OpenAI)")
    if re.fullmatch(r"[A-Za-z0-9_-]+", v):
        return
    autres = set(re.sub(r"[A-Za-z0-9_\- ]", "", plier(v)))
    if autres:
        r.ajoute(BLOQUANT, onglet, ou, f"{champ} « {v} » : caractères spéciaux ({''.join(sorted(autres))})",
                 "le modèle demande « no special characters » : lettres, chiffres, _ et -")
    elif re.search(r"[^\x00-\x7f]", v):
        r.ajoute(ATTENTION, onglet, ou, f"{champ} « {v} » : lettres accentuées", "les remplacer (é → e), à confirmer")
    else:
        r.ajoute(ATTENTION, onglet, ou, f"{champ} « {v} » : contient des espaces", "préférer _ ou - (règle à confirmer)")


def _sensibles(texte):
    """Éléments d'une annonce qui doivent être étayés : chiffres, prix, superlatifs, promesses."""
    sup = list(SUPERLATIFS.finditer(texte))
    trouves = [m.group(0).strip() for m in sup]
    trouves += [m.group(0).strip() for m in NOMBRES.finditer(texte) if re.search(r"\d", m.group(0))
                and not any(x.start() <= m.start() < x.end() for x in sup)]   # « 1 » de « n°1 » : déjà compté
    return [t for t in trouves if t]


def valider(camp, modele, aujourdhui=None, mode=None):
    r = Rapport()
    aujourdhui = aujourdhui or dt.date.today()
    mode = mode or camp.get("mode") or "standard"
    lim = modele["limites"]
    annonceur = camp.get("annonceur") or {}
    marques = {plier(x) for x in [annonceur.get("marque", "")] + list(annonceur.get("concurrents", [])) if x}
    domaines = [plier(d).lstrip(".") for d in annonceur.get("domaines", []) if d]
    allegations = camp.get("allegations") or []

    if camp.get("_source_xlsx"):
        en_trop = [o for o in camp.get("_onglets", []) if o not in ONGLETS]
        manquants = [o for o in ONGLETS if o not in camp.get("_onglets", [])]
        if en_trop:
            r.ajoute(BLOQUANT, "classeur", "onglets", f"onglets en trop : {', '.join(en_trop)}",
                     "le fichier ne doit contenir que campaigns, adgroups et ads")
        if manquants:
            r.ajoute(BLOQUANT, "classeur", "onglets", f"onglets manquants : {', '.join(manquants)}")

    def ou(onglet, i, ligne):
        return f"ligne {ligne['_ligne']}" if "_ligne" in ligne else f"{onglet}[{i + 1}]"

    # campaigns
    noms_camp, objectifs = {}, {}
    if not camp.get("campaigns"):
        r.ajoute(BLOQUANT, "campaigns", "-", "aucune campagne")
    for i, c in enumerate(camp.get("campaigns", [])):
        o = ou("campaigns", i, c)
        nom = str(c.get("campaign_name", "")).strip()
        if nom.startswith("oaitest"):
            r.ajoute(BLOQUANT, "campaigns", o, "ligne d'exemple du modèle encore présente", "la supprimer")
        _nom(r, "campaigns", o, "campaign_name", nom)
        if nom in noms_camp:
            r.ajoute(BLOQUANT, "campaigns", o, f"campaign_name « {nom} » en double")
        noms_camp[nom] = c
        b = nombre(c.get("budget_max"))
        if b is None:
            r.ajoute(BLOQUANT, "campaigns", o, "budget_max manquant ou illisible (obligatoire)",
                     "montant dans la devise du compte, sans symbole")
        elif b <= 0:
            r.ajoute(BLOQUANT, "campaigns", o, "budget_max doit être positif")
        bt = plier(c.get("budget_type", ""))
        if bt and bt not in ("daily", "lifetime", "quotidien", "total"):
            r.ajoute(BLOQUANT, "campaigns", o, f"budget_type « {c.get('budget_type')} » : Daily ou Lifetime")
        elif bt in ("lifetime", "total"):
            r.ajoute(ATTENTION, "campaigns", o, "budget total (Lifetime) : le modèle indique qu'il n'a pas encore de lissage",
                     "préférer Daily pour une dépense régulière")
        obj = plier(c.get("objective", ""))
        norm = {"views": "Views", "vues": "Views", "clicks": "Clicks", "clics": "Clicks",
                "conversions": "Conversions", "conversion": "Conversions"}.get(obj)
        if obj and not norm:
            r.ajoute(BLOQUANT, "campaigns", o, f"objective « {c.get('objective')} » : Views, Clicks ou Conversions")
        objectifs[nom] = norm
        ids, err = liste_json(c.get("conversion_event_setting_ids"))
        if err:
            r.ajoute(BLOQUANT, "campaigns", o, f"conversion_event_setting_ids : {err}")
        elif norm == "Conversions" and len(ids) != 1:
            r.ajoute(BLOQUANT, "campaigns", o, "campagne de conversion : exactement un conversion_event_setting_id",
                     "créer l'événement dans Ads Manager (pixel ou API Conversions), puis coller son identifiant")
        elif norm != "Conversions" and ids:
            r.ajoute(ATTENTION, "campaigns", o, "conversion_event_setting_ids rempli alors que l'objectif n'est pas Conversions")
        d1, d2 = lire_date(c.get("launch_date")), lire_date(c.get("end_date"))
        for champ, val, d in (("launch_date", c.get("launch_date"), d1), ("end_date", c.get("end_date"), d2)):
            if val not in (None, "") and d is None:
                r.ajoute(BLOQUANT, "campaigns", o, f"{champ} « {val} » illisible", "format AAAA-MM-JJ")
        if d1 and d2 and d2 < d1:
            r.ajoute(BLOQUANT, "campaigns", o, "end_date avant launch_date")
        if d1 and d1 < aujourdhui:
            r.ajoute(ATTENTION, "campaigns", o, f"launch_date {d1.isoformat()} déjà passée")
        pays, err = liste_json(c.get("target_countries"))
        if err:
            r.ajoute(BLOQUANT, "campaigns", o, f"target_countries : {err}")
        elif not pays:
            r.ajoute(INFO, "campaigns", o, "aucun pays ciblé", "vérifier le comportement par défaut d'Ads Manager [à vérifier]")
        else:
            for p in pays:
                code = str(p).strip()
                if code.upper() in FAUX_CODES:
                    r.ajoute(BLOQUANT, "campaigns", o, f"pays « {code} » : le code ISO est {FAUX_CODES[code.upper()]}")
                elif code.upper() not in ISO or len(code) != 2:
                    r.ajoute(BLOQUANT, "campaigns", o, f"pays « {code} » : pas un code ISO à 2 lettres")
                elif code != code.upper():
                    r.ajoute(ATTENTION, "campaigns", o, f"pays « {code} » en minuscules", "écrire en majuscules")
            r.ajoute(INFO, "campaigns", o, f"pays ciblés : {', '.join(map(str, pays))}",
                     "un code ISO valide n'est pas forcément ouvert à la publicité (docs OpenAI) : vérifier dans Ads Manager")

    # éligibilité de l'annonceur (Ad Policies)
    pays_vises = {str(p).strip().upper() for c in camp.get("campaigns", []) for p in (liste_json(c.get("target_countries"))[0] or [])}
    categorie = plier(annonceur.get("categorie", "")).replace(" ", "_").replace("-", "_")
    statut_cat = CATEGORIES.get(categorie)
    if not categorie and not camp.get("_source_xlsx"):
        r.ajoute(INFO, "annonceur", "categorie", "catégorie de l'annonceur non déclarée",
                 "la déclarer (references/politiques.md) : certaines catégories sont interdites ou réservées aux États-Unis")
    elif categorie and not statut_cat:
        r.ajoute(ATTENTION, "annonceur", "categorie", f"catégorie « {annonceur.get('categorie')} » inconnue du pack",
                 "la rapprocher d'une catégorie de references/politiques.md")
    elif statut_cat == "interdite":
        r.ajoute(BLOQUANT, "annonceur", "categorie", f"catégorie « {categorie} » interdite par les règles publicitaires d'OpenAI",
                 "Ad Policies v1.6 (sept. 2026) : ne pas lancer ; relire la page si elle a changé")
    elif statut_cat == "restreinte_us":
        hors_us = sorted(pays_vises - {"US"}) or ["tous pays (aucun ciblage)"]
        if pays_vises != {"US"}:
            r.ajoute(BLOQUANT, "annonceur", "categorie",
                     f"catégorie « {categorie} » : hors des États-Unis, généralement interdite ({', '.join(hors_us)})",
                     "Ad Policies v1.6 (sept. 2026) : ne pas lancer hors US sans accord écrit d'OpenAI")
        else:
            r.ajoute(ATTENTION, "annonceur", "categorie", f"catégorie « {categorie} » : approbation au cas par cas aux États-Unis",
                     "justificatif d'autorisation d'exercer possible ; examen manuel")

    # adgroups
    noms_groupes, hints_par_groupe = {}, {}
    groupes = camp.get("adgroups", [])
    hors_reco = []
    if len(groupes) < 5:
        r.ajoute(ATTENTION, "adgroups", "-", f"{len(groupes)} ad group(s) : 5 au moins conseillés, une intention chacun")
    for i, g in enumerate(groupes):
        o = ou("adgroups", i, g)
        nom = str(g.get("adgroup_name", "")).strip()
        if nom.startswith("oaitest"):
            r.ajoute(BLOQUANT, "adgroups", o, "ligne d'exemple du modèle encore présente", "la supprimer")
        _nom(r, "adgroups", o, "adgroup_name", nom)
        if nom in noms_groupes:
            r.ajoute(BLOQUANT, "adgroups", o, f"adgroup_name « {nom} » en double (doit être unique)")
        noms_groupes[nom] = g
        cn = str(g.get("campaign_name", "")).strip()
        if cn not in noms_camp:
            r.ajoute(BLOQUANT, "adgroups", o, f"campaign_name « {cn} » absent de l'onglet campaigns",
                     "le nom doit être identique, caractère pour caractère")
        objectif = objectifs.get(cn)
        mb = nombre(g.get("max_bid"))
        if g.get("max_bid") not in (None, "") and mb is None:
            r.ajoute(BLOQUANT, "adgroups", o, f"max_bid « {g.get('max_bid')} » illisible")
        if mb is None and objectif in ("Clicks", "Conversions"):
            r.ajoute(BLOQUANT, "adgroups", o, f"max_bid obligatoire pour une campagne {objectif}",
                     "fixer un plafond prudent, à revoir après les premiers jours")
        elif mb is None and objectif is None:
            r.ajoute(ATTENTION, "adgroups", o, "max_bid vide et objectif de campagne non précisé")
        elif mb is not None and mb <= 0:
            r.ajoute(BLOQUANT, "adgroups", o, "max_bid doit être positif")
        if mb and objectif == "Clicks" and not 3 <= mb <= 5:
            hors_reco.append(f"{nom} ({mb:g})")
        budget = nombre((noms_camp.get(cn) or {}).get("budget_max"))
        if mb and budget and mb > budget:
            r.ajoute(ATTENTION, "adgroups", o, f"max_bid ({mb:g}) supérieur au budget_max de la campagne ({budget:g})")
        if not str(g.get("intention", "")).strip() and not camp.get("_source_xlsx"):
            r.ajoute(ATTENTION, "adgroups", o, "intention utilisateur envisagée absente",
                     "c'est le pivot du groupe : une phrase, une seule intention")
        brut = g.get("context_hints", g.get("context_hints_brut"))
        hints, err = liste_json(brut)
        if err:
            r.ajoute(BLOQUANT, "adgroups", o, f"Context Hints : {err}")
            hints = []
        elif any(not isinstance(h, str) or not h.strip() for h in hints):
            r.ajoute(BLOQUANT, "adgroups", o, "Context Hints : chaque hint doit être un texte non vide")
            hints = [h for h in hints if isinstance(h, str) and h.strip()]
        hints_par_groupe[nom] = hints
        n = len(hints)
        if n == 0:
            r.ajoute(ATTENTION, "adgroups", o, "aucun context hint", "3 par défaut (2 à 5)")
        elif n < 2:
            r.ajoute(ATTENTION, "adgroups", o, "1 seul context hint", "3 par défaut (2 à 5), à tester")
        elif n > 5:
            r.ajoute(ATTENTION, "adgroups", o, f"{n} context hints : au-delà de 5, le groupe risque de mélanger les intentions",
                     "garder les 3 qui décrivent le mieux la situation")
        elif n > 3:
            r.ajoute(INFO, "adgroups", o, f"{n} context hints : chaque hint en plus élargit les conversations visées",
                     "défaut du pack : 3 (hypothèse à tester)")
        for h in hints:
            nm = mots(h)
            if plier(h) in VAGUES or (len(nm) <= 2 and any(m in VAGUES for m in nm)):
                r.ajoute(BLOQUANT, "adgroups", o, f"hint vague : « {h} »", "décrire une situation ou un besoin réel")
            elif nm and all(any(m in plier(x).split() for x in marques) for m in nm):
                r.ajoute(BLOQUANT, "adgroups", o, f"hint fait seulement de marques : « {h} »",
                         "décrire le besoin, pas la marque ou un concurrent")
            elif len(h.split()) < 3:
                r.ajoute(ATTENTION, "adgroups", o, f"hint très court : « {h} »", "ressemble à un mot-clé ; viser 4 à 8 mots")
            elif GEO_HINT.search(h):
                r.ajoute(ATTENTION, "adgroups", o, f"hint géographique : « {h} »",
                         "la zone se règle dans le ciblage de la campagne, pas dans les hints (docs OpenAI)")
            elif len(h.split()) > 14:
                r.ajoute(ATTENTION, "adgroups", o, f"hint long ({len(h.split())} mots) : « {h[:60]}… »",
                         "une situation par hint ; longueur à confirmer")
        for a in range(n):
            for b in range(a + 1, n):
                if jaccard(hints[a], hints[b]) >= 0.6:
                    r.ajoute(ATTENTION, "adgroups", o, f"hints presque identiques : « {hints[a]} » / « {hints[b]} »",
                             "variante mineure d'une même idée : en garder un")
        if not camp.get("_source_xlsx"):
            if not str(g.get("idee_visuel", "") or "").strip():
                r.ajoute(INFO, "adgroups", o, "pas d'idée de visuel", "une image carrée, un sujet lisible en vignette")
            pt = g.get("prompts_test") or []
            if len(pt) < 3:
                r.ajoute(INFO, "adgroups", o, f"auto-test : {len(pt)} prompt(s) simulé(s) sur 3",
                         "simuler 3 conversations pour vérifier que le groupe tient une seule intention")
    if hors_reco:
        r.ajoute(INFO, "adgroups", "-", f"max_bid au clic hors de 3 à 5 : {', '.join(hors_reco)}",
                 "OpenAI conseille de commencer entre 3 et 5 USD par clic (Help Center, relu le 15 oct. 2026), "
                 "à convertir dans la devise du compte")
    noms_g = list(hints_par_groupe)
    for a in range(len(noms_g)):
        for b in range(a + 1, len(noms_g)):
            for ha in hints_par_groupe[noms_g[a]]:
                for hb in hints_par_groupe[noms_g[b]]:
                    if plier(ha) == plier(hb) or jaccard(ha, hb) >= 0.6:
                        r.ajoute(ATTENTION, "adgroups", f"{noms_g[a]} / {noms_g[b]}",
                                 f"chevauchement : « {ha} » / « {hb} »", "les deux groupes visent la même conversation")

    # ads
    annonces = camp.get("ads", [])
    par_groupe = {n: [] for n in noms_groupes}
    vus = {}
    for i, a in enumerate(annonces):
        o = ou("ads", i, a)
        gn = str(a.get("adgroup_name", "")).strip()
        if gn.startswith("oaitest"):
            r.ajoute(BLOQUANT, "ads", o, "ligne d'exemple du modèle encore présente", "la supprimer")
        if gn not in noms_groupes:
            r.ajoute(BLOQUANT, "ads", o, f"adgroup_name « {gn} » absent de l'onglet adgroups")
        else:
            par_groupe[gn].append(a)
        titre, copie = str(a.get("title", "") or ""), str(a.get("copy", "") or "")
        for champ, val, maxi, cible in (("title", titre, lim["title"], 16), ("copy", copie, lim["copy"], 32)):
            n = longueur(val)
            if not val.strip():
                r.ajoute(BLOQUANT, "ads", o, f"{champ} vide (obligatoire)")
            elif n > maxi:
                r.ajoute(BLOQUANT, "ads", o, f"{champ} de {n} caractères (max {maxi}) : « {val} »",
                         f"retirer {n - maxi} caractère(s)")
            elif n < cible:
                r.ajoute(INFO, "ads", o, f"{champ} de {n} caractères : sous la cible ({cible} à {maxi})")
            if "—" in val or "–" in val:
                r.ajoute(ATTENTION, "ads", o, f"{champ} : tiret cadratin", "le remplacer par une virgule")
            if IMITATION.search(val):
                r.ajoute(ATTENTION, "ads", o, f"{champ} : mention de ChatGPT ou d'OpenAI, ou ton de réponse",
                         "Ad Policies : l'annonce ne doit pas imiter l'interface ou la voix de ChatGPT ni suggérer une affiliation")
            if EMOJI.search(val):
                r.ajoute(ATTENTION, "ads", o, f"{champ} : emoji", "à éviter dans une annonce de 24 ou 48 caractères")
            if re.search(r"\b[A-ZÀ-Ý]{4,}\b", val) and not re.fullmatch(r"[A-Z0-9 ]+", val.strip()):
                r.ajoute(ATTENTION, "ads", o, f"{champ} : mot en capitales", "le ton crié nuit à la pertinence perçue")
            if re.search(r"\S[?!:;]", val):
                r.ajoute(INFO, "ads", o, f"{champ} : pas d'espace avant « ? ! : ; »",
                         "typographie française : l'espace compte dans la limite")
        if titre and copie:
            if plier(titre) in plier(copie) or jaccard(titre, copie) >= 0.5:
                r.ajoute(ATTENTION, "ads", o, "le titre et la copie se répètent", "la copie doit compléter le titre")
        marque = plier(annonceur.get("marque", ""))
        if marque and plier(titre).startswith(marque):
            r.ajoute(ATTENTION, "ads", o, "titre qui commence par la marque", "le nom de l'annonceur s'affiche déjà ; parler du bénéfice")
        cle_a = (plier(titre), plier(copie))
        if cle_a in vus:
            r.ajoute(BLOQUANT, "ads", o, f"annonce en double de {vus[cle_a]}")
        vus.setdefault(cle_a, o)
        # allégations
        declaree = str(a.get("allegation", "") or "").strip()
        if declaree:
            appui = [x for x in allegations if plier(x.get("texte", "")) == plier(declaree)]
            statut = plier(appui[0].get("statut", "")) if appui else ""
            if not appui:
                r.ajoute(ATTENTION, "ads", o, f"allégation déclarée absente de la liste : « {declaree} »",
                         "reprendre le texte exact d'une allégation approuvée")
            elif statut == "refusee":
                r.ajoute(BLOQUANT, "ads", o, f"allégation refusée utilisée : « {declaree} »")
            elif statut != "approuvee":
                r.ajoute(ATTENTION, "ads", o, f"allégation « {declaree} » au statut {statut or 'inconnu'}",
                         "la faire valider avant import")
        for s in _sensibles(f"{titre} {copie}"):
            appuis = [x for x in allegations if plier(s) in plier(x.get("texte", ""))]
            statuts = {plier(x.get("statut", "")) for x in appuis}
            libelles = sorted({str(x.get("statut", "")).strip() or "sans statut" for x in appuis})
            if not appuis and not allegations and camp.get("_source_xlsx"):
                r.ajoute(ATTENTION, "ads", o, f"allégation à vérifier : « {s} » (aucune liste d'allégations fournie)",
                         "relancer avec --allegations campagne.json, ou vérifier à la main")
            elif not appuis:
                r.ajoute(BLOQUANT, "ads", o, f"allégation non étayée : « {s} »",
                         "l'ajouter à la liste des allégations avec sa source, ou la retirer")
            elif "approuvee" not in statuts:
                niveau = BLOQUANT if "refusee" in statuts else ATTENTION
                r.ajoute(niveau, "ads", o, f"allégation « {s} » au statut {', '.join(libelles)}",
                         "la faire valider avant import")
        # liens
        lien = str(a.get("link", "") or "").strip()
        if len(lien) > 2048:
            r.ajoute(BLOQUANT, "ads", o, f"link de {len(lien)} caractères (2 048 au plus, docs OpenAI)")
        if not lien:
            r.ajoute(BLOQUANT, "ads", o, "link vide (obligatoire)")
        else:
            u = urllib.parse.urlsplit(lien)
            if " " in lien:
                r.ajoute(BLOQUANT, "ads", o, f"link avec une espace : « {lien} »")
            elif u.scheme in ("http", "https"):
                if not u.netloc or "." not in u.netloc:
                    r.ajoute(BLOQUANT, "ads", o, f"link mal formé : « {lien} »")
                else:
                    if u.scheme == "http":
                        r.ajoute(ATTENTION, "ads", o, "link en http", "préférer https")
                    hote = plier(u.hostname or "")
                    if domaines and not any(hote == d or hote.endswith("." + d) for d in domaines):
                        r.ajoute(BLOQUANT, "ads", o, f"link hors des domaines approuvés : {u.hostname}")
                    if (u.path in ("", "/")) and not u.query:
                        r.ajoute(INFO, "ads", o, "link vers la page d'accueil", "une page qui répond à l'intention du groupe convertit mieux [praticien]")
            elif u.scheme and u.scheme not in ("javascript", "data", "file"):
                r.ajoute(INFO, "ads", o, f"lien profond ou d'installation ({u.scheme}:)", "le modèle les accepte ; le tester sur mobile")
            else:
                r.ajoute(BLOQUANT, "ads", o, f"link invalide : « {lien} »")
        image = str(a.get("image_link", "") or "").strip()
        if not image:
            r.ajoute(BLOQUANT, "ads", o, "image_link vide (obligatoire)",
                     "image carrée 640 à 1200 px, PNG ou JPG, à une URL publique directe")
        else:
            u = urllib.parse.urlsplit(image)
            if u.scheme not in ("http", "https") or not u.netloc or " " in image:
                r.ajoute(BLOQUANT, "ads", o, f"image_link invalide : « {image} »")
            elif re.search(r"\.webp$", u.path, re.I):
                r.ajoute(ATTENTION, "ads", o, "image_link en WebP", "l'API l'accepte, le modèle d'import cite PNG ou JPG : préférer PNG ou JPG")
            elif not re.search(r"\.(png|jpe?g)$", u.path, re.I):
                r.ajoute(ATTENTION, "ads", o, "image_link sans extension .png ou .jpg",
                         "vérifier que l'URL ouvre directement l'image")

    # signaux de catégories restreintes ou interdites (textes des annonces et des hints)
    textes = [("ads", f"{x.get('title', '')} {x.get('copy', '')}") for x in annonces] + \
             [("adgroups", h) for hs in hints_par_groupe.values() for h in hs]
    vus_sig = set()
    for cat, motif in SIGNAUX.items():
        if cat == categorie:
            continue
        for onglet_t, t in textes:
            m = re.search(motif, t, re.I)
            if m and (cat, plier(m.group(0))) not in vus_sig:
                vus_sig.add((cat, plier(m.group(0))))
                r.ajoute(ATTENTION, onglet_t, "-", f"« {m.group(0)} » : signal de la catégorie {cat}",
                         "vérifier l'éligibilité (references/politiques.md) ; ignorer si l'usage est incident")

    # volume et équilibre
    for gn, lst in par_groupe.items():
        if not lst:
            r.ajoute(ATTENTION, "ads", gn, "ad group sans annonce")
        elif len(lst) < 3:
            r.ajoute(ATTENTION, "ads", gn, f"{len(lst)} annonce(s) dans le groupe", "3 au moins, d'angles différents")
        titres = [plier(x.get("title", "")) for x in lst]
        for t in {t for t in titres if titres.count(t) > 1 and t}:
            r.ajoute(ATTENTION, "ads", gn, f"titre répété dans le groupe : « {t} »")
        for x in range(len(lst)):
            for y in range(x + 1, len(lst)):
                a_, b_ = lst[x], lst[y]
                if (plier(a_.get("title")), plier(a_.get("copy"))) == (plier(b_.get("title")), plier(b_.get("copy"))):
                    continue
                if jaccard(f"{a_.get('title')} {a_.get('copy')}", f"{b_.get('title')} {b_.get('copy')}") >= 0.7:
                    r.ajoute(ATTENTION, "ads", gn, f"reformulation minimale : « {a_.get('title')} » / « {b_.get('title')} »",
                             "chercher un autre angle (bénéfice, situation, objection)")
    tailles = [len(v) for v in par_groupe.values() if v]
    if tailles and max(tailles) > 2 * min(tailles):
        r.ajoute(ATTENTION, "ads", "-", f"répartition déséquilibrée : de {min(tailles)} à {max(tailles)} annonces par groupe")
    titres_vus = {}
    for gn, lst in par_groupe.items():
        for x in lst:
            t = plier(x.get("title", ""))
            if t:
                titres_vus.setdefault(t, [x.get("title", "").strip(), set()])[1].add(gn)
    for t, (original, gs) in titres_vus.items():
        if len(gs) > 1:
            r.ajoute(ATTENTION, "ads", " / ".join(sorted(gs)), f"titre repris dans {len(gs)} groupes : « {original} »",
                     "un titre par intention : les groupes se font concurrence et les résultats se lisent mal")
    # Volume face au budget : une annonce doit recevoir assez de clics pour être départagée.
    for c in camp.get("campaigns", []):
        budget = nombre(c.get("budget_max"))
        cn = str(c.get("campaign_name", "")).strip()
        if objectifs.get(cn) != "Clicks" or not budget or plier(c.get("budget_type", "daily")) not in ("daily", "quotidien", ""):
            continue
        enchères = [nombre(g.get("max_bid")) for g in groupes if str(g.get("campaign_name", "")).strip() == cn]
        enchères = [e for e in enchères if e]
        nb = sum(len(par_groupe.get(str(g.get("adgroup_name", "")).strip(), [])) for g in groupes
                 if str(g.get("campaign_name", "")).strip() == cn)
        if enchères and nb:
            clics = budget / (sum(enchères) / len(enchères))
            if nb > 2 * clics:
                r.ajoute(ATTENTION, "ads", cn,
                         f"{nb} annonces pour {clics:.0f} clics par jour au plus (budget ÷ enchère moyenne)",
                         "chaque annonce recevra trop peu de clics pour être départagée : proposer un lancement à "
                         "2 ou 3 annonces par groupe, ou plus de budget ; volume à décider avec l'annonceur")
    total = len(annonces)
    cible = 100 if mode == "grande-echelle" else 40
    if total < cible:
        r.ajoute(ATTENTION, "ads", "-", f"{total} annonce(s) : cible {'100 (grande échelle)' if cible == 100 else '40 à 50'}",
                 "volume à confirmer : voir commun/faits.md")
    return r, {"campagnes": len(camp.get("campaigns", [])), "groupes": len(groupes), "annonces": total,
               "par_groupe": {k: len(v) for k, v in par_groupe.items()}, "limites": lim, "mode": mode}


# ---------------------------------------------------------------- écriture

def _cellule(ref, valeur, style="0", px="x:"):
    """Une cellule ; px est le préfixe d'espace de noms du modèle (« x: » ou vide)."""
    if isinstance(valeur, (int, float)) and not isinstance(valeur, bool):
        v = int(valeur) if float(valeur).is_integer() else valeur
        return f'<{px}c r="{ref}" s="{style}" t="n"><{px}v>{v}</{px}v></{px}c>'
    return (f'<{px}c r="{ref}" s="{style}" t="inlineStr"><{px}is><{px}t xml:space="preserve">'
            f'{escape(str(valeur))}</{px}t></{px}is></{px}c>')


def _valeur(onglet, champ, ligne):
    v = ligne.get(champ)
    if champ == "context_hints":
        v = ligne.get("context_hints", ligne.get("context_hints_brut"))
    if v in (None, ""):
        return None, STYLE_TEXTE
    if champ in ("launch_date", "end_date"):
        d = lire_date(v)
        return (serie_excel(d), STYLE_DATE) if d else (str(v), STYLE_TEXTE)
    if champ in ("budget_max", "max_bid"):
        n = nombre(v)
        return (n if n is not None else str(v)), STYLE_TEXTE
    if champ in ("target_countries", "conversion_event_setting_ids", "context_hints"):
        lst, err = liste_json(v)
        if err:
            return str(v), STYLE_TEXTE
        if champ == "target_countries":
            lst = [str(x).strip().upper() for x in lst]
        return json.dumps(lst, ensure_ascii=False, separators=(",", ":")), STYLE_TEXTE
    if champ == "budget_type":
        return {"daily": "Daily", "quotidien": "Daily", "lifetime": "Lifetime", "total": "Lifetime"}.get(plier(v), v), STYLE_TEXTE
    if champ == "objective":
        return {"views": "Views", "vues": "Views", "clicks": "Clicks", "clics": "Clicks",
                "conversions": "Conversions", "conversion": "Conversions"}.get(plier(v), v), STYLE_TEXTE
    return v, STYLE_TEXTE


def _styles_donnees(styles_xml):
    """Index des styles de cellule pour le texte et les dates : police non italique, non grasse,
    sans remplissage. Le modèle d'Ads Manager met sa ligne d'exemple en italique : on ne la copie pas."""
    def bloc(nom):
        m = re.search(rf"<(?:\w+:)?{nom}\b[^>]*>(.*?)</(?:\w+:)?{nom}>", styles_xml, re.S)
        return m.group(1) if m else ""
    polices = re.findall(r"<(?:\w+:)?font\b[^>]*?(?:/>|>(.*?)</(?:\w+:)?font>)", bloc("fonts"), re.S)
    formats = dict(re.findall(r'<(?:\w+:)?numFmt\b[^>]*numFmtId="(\d+)"[^>]*formatCode="([^"]*)"', bloc("numFmts")))
    texte = date = None
    for i, xf in enumerate(re.findall(r"<(?:\w+:)?xf\b[^>]*>", bloc("cellXfs"))):
        attr = dict(re.findall(r'(\w+)="([^"]*)"', xf))
        police = polices[int(attr.get("fontId", 0))] if int(attr.get("fontId", 0)) < len(polices) else ""
        if re.search(r"<(?:\w+:)?[ib]\s*/?>", police or "") or attr.get("fillId", "0") != "0":
            continue
        fmt = attr.get("numFmtId", "0")
        est_date = fmt in {str(n) for n in range(14, 23)} or ("y" in formats.get(fmt, "").lower() and "d" in formats.get(fmt, "").lower())
        if est_date and date is None:
            date = str(i)
        elif fmt == "0" and texte is None:
            texte = str(i)
    texte = texte or "0"
    return {STYLE_TEXTE: texte, STYLE_DATE: date or texte}


def exporter(camp, modele_chemin, sortie):
    with zipfile.ZipFile(modele_chemin) as z:
        onglets = _chemins_onglets(z)
        fichiers = {n: z.read(n) for n in z.namelist()}
    styles = _styles_donnees(fichiers.get("xl/styles.xml", b"").decode("utf-8-sig"))
    for onglet, chemin_xml in onglets.items():
        xml = fichiers[chemin_xml].decode("utf-8")
        entetes = _cellules_ligne(xml, 1)
        colonnes = sorted(entetes, key=lambda c: (len(c), c))
        m = re.search(r"<(\w+:)?sheetData\b", xml)
        if not m:
            raise ValueError(f"onglet {onglet} : pas de sheetData dans le modèle")
        px = m.group(1) or ""
        garde = "".join(re.findall(rf'<{px}row r="[123]"[^>]*>.*?</{px}row>', xml, re.S))
        lignes = []
        for i, ligne in enumerate(camp.get(onglet, []), start=4):
            cells = []
            for col in colonnes:
                val, style = _valeur(onglet, cle(entetes[col]), ligne)
                if val is not None:
                    if style == STYLE_DATE and styles[STYLE_DATE] == styles[STYLE_TEXTE]:
                        val, style = lire_date(ligne.get(cle(entetes[col]))).isoformat(), STYLE_TEXTE
                    cells.append(_cellule(f"{col}{i}", val, styles[style], px))
            lignes.append(f'<{px}row r="{i}">{"".join(cells)}</{px}row>')
        donnees = f"<{px}sheetData>{garde}{''.join(lignes)}</{px}sheetData>"
        xml, n = re.subn(rf"<{px}sheetData\b[^>]*?(?:/>|>.*?</{px}sheetData>)", lambda _: donnees, xml, count=1, flags=re.S)
        if n != 1:
            raise ValueError(f"onglet {onglet} : sheetData introuvable")
        xml = re.sub(rf"<{px}hyperlinks>.*?</{px}hyperlinks>", "", xml, flags=re.S)
        xml = re.sub(rf"<{px}dimension [^>]*/>", "", xml)
        fichiers[chemin_xml] = xml.encode("utf-8")
        rels = chemin_xml.replace("worksheets/", "worksheets/_rels/") + ".rels"
        if rels in fichiers:
            r = fichiers[rels].decode("utf-8-sig")
            r = re.sub(r"<Relationship [^>]*relationships/hyperlink[^>]*/>", "", r)
            fichiers[rels] = r.encode("utf-8")
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        for nom, contenu in fichiers.items():
            z.writestr(nom, contenu)


# ---------------------------------------------------------------- affichage

def afficher(r, resume):
    b, a, i = r.compte(BLOQUANT), r.compte(ATTENTION), r.compte(INFO)
    verdict = "BLOQUÉ" if b else "À REVOIR" if a else "PRÊT"
    print(f"CAMPAGNE · {verdict} · {resume['campagnes']} campagne(s), {resume['groupes']} ad group(s), "
          f"{resume['annonces']} annonce(s) · limites du modèle : titre {resume['limites']['title']}, "
          f"copie {resume['limites']['copy']}")
    print(f"  {b} bloquant(s) · {a} attention · {i} info")
    for niveau in (BLOQUANT, ATTENTION, INFO):
        pts = [p for p in r.points if p["niveau"] == niveau]
        if not pts:
            continue
        print(f"\n{niveau}")
        for p in pts:
            print(f"  [{p['onglet']} · {p['ou']}] {p['message']}")
            if p["conseil"]:
                print(f"      → {p['conseil']}")


def charger(source):
    p = Path(source)
    if not p.exists():
        raise SystemExit(f"{source} : fichier introuvable")
    if p.suffix.lower() == ".xlsx":
        return lire_xlsx(p)
    return json.loads(p.read_text(encoding="utf-8"))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("modele", help="relire le modèle d'import")
    m.add_argument("chemin", nargs="?", default=str(MODELE_DEFAUT))
    for nom, aide in (("valider", "contrôler une campagne (JSON ou XLSX)"), ("exporter", "écrire le XLSX d'import"),
                      ("tableaux", "tableaux à coller, sans fichier"), ("relecture", "tableau de relecture humaine")):
        s = sub.add_parser(nom, help=aide)
        s.add_argument("source")
        s.add_argument("--modele", default=str(MODELE_DEFAUT))
        s.add_argument("--aujourdhui", help="date du jour AAAA-MM-JJ (tests)")
        s.add_argument("--mode", choices=["standard", "grande-echelle"])
        if nom == "valider":
            s.add_argument("--json", action="store_true")
            s.add_argument("--allegations", metavar="CAMPAGNE.json",
                           help="pour un XLSX : reprendre annonceur et allégations d'un JSON de campagne")
        if nom == "exporter":
            s.add_argument("-o", "--sortie", required=True)
    a = ap.parse_args(argv)

    if a.cmd == "modele":
        mod = lire_modele(a.chemin)
        print(f"MODÈLE · {Path(a.chemin).name} · onglets : {', '.join(mod['onglets'])}")
        print(f"  limites : titre {mod['limites']['title']} caractères, copie {mod['limites']['copy']}")
        for onglet, cols in mod["colonnes"].items():
            print(f"\n{onglet}")
            for col, nom in cols:
                print(f"  {col}  {nom:<30} {mod['statut'][onglet].get(nom, '')}")
        return 0

    try:
        mod = lire_modele(a.modele)
    except (FileNotFoundError, zipfile.BadZipFile, KeyError) as e:
        print(f"modèle illisible ({a.modele}) : {e}", file=sys.stderr)
        return 1
    camp = charger(a.source)
    if getattr(a, "allegations", None):
        src = charger(a.allegations)
        camp["allegations"] = src.get("allegations", [])
        camp["annonceur"] = src.get("annonceur", camp.get("annonceur", {}))
    auj = dt.date.fromisoformat(a.aujourdhui) if a.aujourdhui else None
    r, resume = valider(camp, mod, auj, a.mode)

    if a.cmd == "valider":
        if a.json:
            print(json.dumps({"verdict": r.code(), "resume": resume, "points": r.points}, ensure_ascii=False, indent=2))
        else:
            afficher(r, resume)
        return r.code()

    if a.cmd == "exporter":
        if r.compte(BLOQUANT):
            afficher(r, resume)
            print("\nFichier non écrit : corriger les points bloquants d'abord.")
            return 3
        exporter(camp, a.modele, a.sortie)
        afficher(r, resume)
        print(f"\nFichier écrit : {a.sortie} (onglets {', '.join(ONGLETS)}). À relire par une personne qualifiée avant import.")
        return r.code()

    if a.cmd == "tableaux":
        for onglet in ONGLETS:
            cols = [cle(n) for _, n in mod["colonnes"].get(onglet, [])]
            print(f"### {onglet}")
            print("\t".join(n for _, n in mod["colonnes"].get(onglet, [])))
            for ligne in camp.get(onglet, []):
                vals = []
                for c in cols:
                    v, style = _valeur(onglet, c, ligne)
                    if style == STYLE_DATE and v is not None:
                        v = lire_date(ligne.get(c)).isoformat()
                    vals.append("" if v is None else (f"{v:g}" if isinstance(v, float) else str(v)))
                print("\t".join(vals))
            print()
        print("Repli sans fichier : colle chaque bloc dans l'onglet du même nom, ligne 4, à la place de la ligne d'exemple (oaitest…), sans la ligne d'en-tête.")
        return r.code()

    if a.cmd == "relecture":
        par_groupe = {}
        for x in camp.get("ads", []):
            par_groupe.setdefault(x.get("adgroup_name"), []).append(x)
        for g in camp.get("adgroups", []):
            print(f"### {g.get('adgroup_name')}")
            print(f"Intention : {g.get('intention', '{{à compléter}}')}")
            hints, _ = liste_json(g.get("context_hints", g.get("context_hints_brut")))
            print(f"Hints : {' · '.join(hints or [])}")
            if g.get("idee_visuel"):
                print(f"Idée de visuel : {g['idee_visuel']}")
            print("\n| Titre | Car. | Copie | Car. | Angle | Allégation | Page |\n|---|---|---|---|---|---|---|")
            for x in par_groupe.get(g.get("adgroup_name"), []):
                page = urllib.parse.urlsplit(str(x.get("link", ""))).path or str(x.get("link", ""))
                print(f"| {x.get('title', '')} | {longueur(x.get('title'))} | {x.get('copy', '')} | {longueur(x.get('copy'))} "
                      f"| {x.get('angle', '')} | {x.get('allegation', '')} | {page} |")
            print()
        return r.code()
    return 1


if __name__ == "__main__":
    sys.exit(main())
