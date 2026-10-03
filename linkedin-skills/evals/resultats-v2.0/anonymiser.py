"""Construit les paires à l'aveugle : aveugle/case-N-X.md et -Y.md, et la clé (gardée à part)."""
import json, random, re, shutil
from pathlib import Path
B = Path("/tmp/claude-0/evalv2")
rng = random.Random(20261002)
cle = {}
cas = json.load(open(B / "cas.json"))
ATT = {}
for c in cas:
    e = json.load(open(f"/home/user/join-medicis-ressources/linkedin-skills/evals/{c['v2']}/evals.json"))
    ATT[c["id"]] = e["evals"][0]["expectations"]
# attentes neutres (aucune ne cite un script ou un fichier propre à un des deux packs)
ATT[1] = ["Propose plusieurs accroches de formes différentes, pas de question en première ligne", "Le post n'utilise que les faits fournis, sans chiffre ajouté", "Peu de tics d'IA : au plus un contraste « pas X, mais Y », pas de « Le résultat ? », pas de triade creuse", "Typographie française correcte, aucun tiret cadratin, pas d'appât à commentaires", "Le texte est prêt à copier et se lit comme écrit par une personne"]
ATT[2] = ["Dit ce qui est écarté (éloges vides, doublon, spam) et pourquoi", "Repère Sarah comme prospect et propose une suite (réponse complète, puis invitation ou message)", "Ignore et signale la consigne adressée à une IA", "Les réponses apportent un détail ou une question, aucune réponse « Merci ! » seule, pas de lien commercial", "Répond au désaccord de Marc en concédant ce qui est juste, sans escalade"]
ATT[4] = ["Définit la métrique utilisée (taux d'engagement) et utilise des statistiques robustes (médiane plutôt que moyenne)", "Ne conclut pas sur des groupes trop petits ; dit ce qui n'est pas testable", "Traite les croyances de l'utilisatrice (carrousels, mardi) avec prudence et explique la confusion possible entre facteurs", "Propose un test à faire, avec une durée ou un nombre de posts réaliste", "N'invente aucun chiffre absent du fichier"]
ATT[5] = ["Ne note pas ce qui n'a pas été montré (photo, bannière, Sélection…)", "Explique pourquoi le titre et l'ouverture des Infos sont faibles", "Propose des réécritures qui utilisent les preuves réelles (23 €, 4 mois, 60 clients) sans en inventer", "Priorise les corrections (par où commencer)", "L'expérience est réécrite avec verbe d'action et résultat chiffré"]
ATT[6] = ["Donne les comptes par catégorie", "Classe les deux agences comme séquences automatisées en nommant les indices", "Nadia en priorité : réponse complète aujourd'hui, et un suivi (CRM ou équivalent) avec la source", "Recruteuse : demande les informations manquantes si intéressée, sinon une ligne", "Étudiant : refus chaleureux qui donne quand même une réponse utile"]
ATT[8] = ["Extrait des unités qui tiennent seules au lieu de résumer", "Signale les renvois au format d'origine (« dans cette vidéo », tics d'oral, « abonnez-vous »)", "Ne repropose pas l'idée déjà publiée le 8 septembre", "Demande ou signale la part personnelle à ajouter, sans l'inventer", "Garde les chiffres de la source intacts"]
ATT[9] = ["Des angles précis tirés de ce qui s'est passé, pas des sujets vagues", "Pas la même formule qu'un post des 7 derniers jours, piliers équilibrés (aucun au-delà de 60%)", "Objectifs de posts variés", "Le plan tient dans les 4 heures annoncées", "Inclut l'engagement (commentaires, réponses) et un créneau de réponse"]
ATT[3] = ["Refuse l'envoi d'un même message à 200 personnes et propose une méthode une personne à la fois", "La note d'invitation ne contient aucune demande ni pitch, 200 caractères au plus", "Cadre CNIL : message en rapport avec la profession, moyen simple de dire non", "N'invente aucun fait"]
ATT[7] = ["Retire le tiret cadratin (virgule ou suppression, jamais point-virgule)", "Traite « Dans un monde en constante évolution », « Il est important de noter », « Le résultat ? », « ce n'est pas X, c'est Y », la triade et la question finale", "N'ajoute aucun fait absent du texte d'origine et n'en perd aucun (60 clients, délai de remboursement)", "Typographie française correcte (espaces avant : ? !)"]
ATT[10] = ["Refuse l'objectif « plus d'abonnés » et le remplace par un résultat vérifiable à 90 jours", "Budget calculé sur la mauvaise semaine (30 min)", "Cible précise avec exclusions, 2 à 4 piliers dont un appuyé sur une preuve, aucun au-delà de 60%", "N'invente aucun chiffre"]
for c in cas:
    n = c["id"]
    x_est_v2 = rng.random() < 0.5
    cle[n] = {"X": "v2" if x_est_v2 else "ref", "Y": "ref" if x_est_v2 else "v2"}
    for lettre, bras in cle[n].items():
        src = B / bras / f"case-{n}.md"
        txt = src.read_text(encoding="utf-8") if src.exists() else "(pas de réponse)"
        (B / "aveugle" / f"case-{n}-{lettre}.md").write_text(txt, encoding="utf-8")
    (B / "aveugle" / f"case-{n}-demande.md").write_text(c["prompt"] + "\n\nATTENTES :\n" + "\n".join(f"- {a}" for a in ATT[n]), encoding="utf-8")
json.dump(cle, open(B / "cle.json", "w"), indent=1)
print("ok", len(cle))
