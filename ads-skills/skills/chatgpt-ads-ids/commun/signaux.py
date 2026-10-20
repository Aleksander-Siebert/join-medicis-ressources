#!/usr/bin/env python3
"""signaux.py : repérage, dans un texte d'annonce, de ce qui demande une vérification (Python 3, sans dépendance).

Socle commun du pack (modifier ici, puis outils/propager.py). Repris de
valider_exporter.py (/chatgpt-ads-skills) ; un test d'intégrité vérifie que
les deux listes restent identiques.

  - allégations à étayer : chiffres, prix, pourcentages, superlatifs, promesses ;
  - catégories restreintes ou interdites par les règles d'OpenAI (v1.6) ;
  - points de droit français : allégations vertes génériques, crédit.
"""
import re

SUPERLATIFS = re.compile(r"\b(meilleur(?:e|s|es)?|n\s?°\s?1|numéro\s?1|leader|le plus|la plus|les plus|moins cher(?:e|s|es)?|"
                         r"unique|premier(?:e|s|es)?|imbattable|garanti(?:e|s|es)?|garantie|100\s?%|sans risque|"
                         r"gratuit(?:e|s|es)?|offert(?:e|s|es)?|rembours(?:é|ée|és|ées|ement)|sans engagement|"
                         r"certifi(?:é|ée|és|ées)|agré(?:é|ée|és|ées)|best|cheapest|free|guaranteed?)\b", re.I)
NOMBRES = re.compile(r"\d+(?:[.,   ]\d+)*\s?(?:%|€|\$|£|h\b|min\b|jours?\b|mois\b|ans?\b|k€|x\b)?", re.I)
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
VERT = re.compile(r"\b(?:écologiques?|éco-?responsables?|respectueu(?:x|se|ses) de l'environnement|verts?|durables?|"
                  r"neutres? en carbone|zéro carbone|green|eco-friendly|carbon neutral)\b", re.I)
IMITATION = re.compile(r"\b(?:chat\s?gpt|openai|gpt-?\d\w*)\b|^\s*(?:réponse|answer)\s*:", re.I)


def sensibles(texte):
    """Éléments d'un texte qui doivent être étayés : chiffres, prix, superlatifs, promesses."""
    sup = list(SUPERLATIFS.finditer(texte))
    trouves = [m.group(0).strip() for m in sup]
    trouves += [m.group(0).strip() for m in NOMBRES.finditer(texte) if re.search(r"\d", m.group(0))
                and not any(x.start() <= m.start() < x.end() for x in sup)]
    return [t for t in trouves if t]


def categories(texte):
    """Catégories restreintes ou interdites signalées par un mot du texte : {catégorie: mot}."""
    res = {}
    for cat, motif in SIGNAUX.items():
        m = re.search(motif, texte, re.I)
        if m:
            res[cat] = m.group(0)
    return res
