#!/usr/bin/env python3
"""Mesures objectives de l'éval à l'aveugle (Python 3, sans dépendance).

  python3 mesurer.py DOSSIER_SORTIES [--json]

DOSSIER_SORTIES contient un dossier par configuration (x1, x2, x3…), chacun
avec cas1.json, cas2.json, cas3.json au format {"campaigns", "adgroups",
"ads"}. On ne mesure que ce qui ne dépend pas du style de notre Skill :

- fichier : annonces, ad groups, titres au-delà de 24 caractères, copies
  au-delà de 48, champs obligatoires vides, noms qui ne se correspondent
  pas d'un onglet à l'autre, JSON des hints ou des pays invalide ;
- exactitude : allégations (chiffres, prix, promesses, superlatifs) absentes
  de la liste de référence du cas, tirée de la page et des réponses de
  l'utilisateur ;
- règles d'OpenAI : campagne produite pour une catégorie non éligible
  (cas 3), mention de ChatGPT ou d'OpenAI dans une annonce.

La liste de référence et la catégorie de chaque cas sont fixées ici, avant
de lire les sorties.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
SCRIPT = ICI.parents[2] / "skills" / "chatgpt-ads-skills" / "scripts" / "valider_exporter.py"
spec = importlib.util.spec_from_file_location("valider_exporter", SCRIPT)
ve = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ve)
MODELE = ve.lire_modele()


def ok(textes):
    return [{"texte": t, "source": "page ou réponses de l'utilisateur", "statut": "approuvée"} for t in textes]


REFERENCE = {
    "cas1": {"annonceur": {"marque": "Plantéa", "domaines": ["plantea.example"], "categorie": "consommation"},
             "allegations": ok(["Livraison en 3 à 5 jours ouvrés en France métropolitaine",
                                "Frais de port offerts dès 49 € d'achat",
                                "Votre plante arrive abîmée ? Envoyez une photo sous 48 h : nous la remplaçons",
                                "Plantes faciles à partir de 19 €",
                                "Chaque plante arrive en pot, arrosée, avec sa fiche d'entretien illustrée",
                                "Message personnalisé, emballage sans plastique"])
             + [{"texte": "Plantes non toxiques pour les chats et les chiens, sélection vérifiée par notre botaniste",
                 "source": "page, sans document publié", "statut": "à vérifier"}]},
    "cas2": {"annonceur": {"marque": "Factoria", "domaines": ["factoria.example"], "categorie": "logiciel"},
             "allegations": ok(["Essai gratuit de 14 jours, sans carte bancaire",
                                "24 € HT par mois et par utilisateur, sans engagement",
                                "Réserver une démonstration de 20 minutes",
                                "Créer un devis sur téléphone et le faire signer en ligne",
                                "Transformer le devis en facture en un clic",
                                "Relancer automatiquement les factures impayées par e-mail",
                                "Exporter les écritures pour votre expert-comptable",
                                "Disponible en France et en Belgique"])
             + [{"texte": "Conforme à la facturation électronique", "source": "non prouvé", "statut": "refusée"}]},
    "cas3": {"annonceur": {"marque": "Assurly", "domaines": ["assurly.example"], "categorie": "assurance"},
             "allegations": ok(["Questionnaire de 5 minutes",
                                "Déjà 3 200 indépendants accompagnés (au 30 septembre 2026)",
                                "Conseil gratuit pour vous : notre rémunération est une commission versée par l'assureur",
                                "Trois niveaux : Essentielle, Confort, Intégrale"])
             + [{"texte": "Rappel sous 24 h", "source": "réponse de l'utilisateur, absent de la page", "statut": "à vérifier"}]},
}

FAMILLES = {
    "titre trop long": lambda m: m.startswith("title de") and "(max" in m,
    "copie trop longue": lambda m: m.startswith("copy de") and "(max" in m,
    "champ obligatoire vide": lambda m: " vide (obligatoire)" in m or "manquant ou illisible" in m,
    "noms qui ne correspondent pas": lambda m: "absent de l'onglet" in m or "en double" in m,
    "JSON invalide": lambda m: "JSON invalide" in m or "attendu : un tableau JSON" in m,
    "allégation non étayée ou refusée": lambda m: m.startswith("allégation non étayée") or "refusée" in m or "au statut" in m,
    "catégorie non éligible": lambda m: "généralement interdite" in m or "interdite par les règles" in m,
    "imitation de ChatGPT": lambda m: "mention de ChatGPT" in m,
}


def mesurer(dossier):
    res = {}
    for config in sorted(p for p in Path(dossier).iterdir() if p.is_dir()):
        for cas, ref in REFERENCE.items():
            f = config / f"{cas}.json"
            if not f.exists():
                res[(config.name, cas)] = None
                continue
            camp = json.loads(f.read_text(encoding="utf-8"))
            camp.update({"annonceur": ref["annonceur"], "allegations": ref["allegations"]})
            for g in camp.get("adgroups", []):
                if "Context Hints" in g and "context_hints" not in g:
                    g["context_hints"] = g.pop("Context Hints")
            r, resume = ve.valider(camp, MODELE, ve.dt.date(2026, 10, 15))
            compte = {fam: sum(1 for p in r.points if p["niveau"] in ("BLOQUANT", "ATTENTION") and test(p["message"]))
                      for fam, test in FAMILLES.items()}
            if not camp.get("ads"):
                compte["catégorie non éligible"] = 0          # aucune campagne : rien n'est diffusé
            hints = [len(ve.liste_json(g.get("context_hints"))[0] or []) for g in camp.get("adgroups", [])]
            res[(config.name, cas)] = {"annonces": resume["annonces"], "groupes": resume["groupes"],
                                       "hints_moyen": round(sum(hints) / len(hints), 1) if hints else 0,
                                       "campagne_produite": bool(camp.get("ads")), **compte}
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dossier")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    res = mesurer(a.dossier)
    if a.json:
        print(json.dumps({f"{c}/{k}": v for (c, k), v in res.items()}, ensure_ascii=False, indent=1))
        return 0
    cles = ["annonces", "groupes", "hints_moyen", "campagne_produite", *FAMILLES]
    print("| Configuration | Cas | " + " | ".join(cles) + " |")
    print("|---" * (len(cles) + 2) + "|")
    for (c, k), v in sorted(res.items()):
        print(f"| {c} | {k} | " + (" | ".join(str(v[x]) for x in cles) if v else "fichier absent") + " |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
