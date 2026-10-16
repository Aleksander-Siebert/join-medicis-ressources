#!/usr/bin/env python3
"""Tests de pipeline.py : python3 -m unittest discover evals/seo-article"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
PACK = ICI.parents[1]
SCRIPT = PACK / "skills" / "seo-article" / "scripts" / "pipeline.py"
CONTEXTE = PACK / "skills" / "seo-write" / "commun" / "modeles" / "exemple-site-context.md"
ARTICLE_IA = PACK / "evals" / "seo-write" / "article-ia.md"
spec = importlib.util.spec_from_file_location("pipeline", SCRIPT)
pl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pl)

OPTS_SITE = ["--contexte", str(CONTEXTE), "--affirmatif", "--remplacer", "chez Assurly=à Assurly",
             "--longueur", "1000-1500", "--mot-cle", "mutuelle indépendant", "--marque", "Assurly"]


def lancer(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)


def etat_neuf(autonome=False):
    return pl.nouvel_etat("mutuelle indépendant", ymyl=True, autonome=autonome, max_tours=2)


def jusqu_a(etat, cle):
    """Fait et valide toutes les étapes avant `cle`."""
    for k in pl.CLES[:pl.CLES.index(cle)]:
        pl.fait(etat, k, None, None)
        if etat["etapes"][k]["statut"] == "à valider":
            pl.valider(etat, k)


class Ordre(unittest.TestCase):
    def test_pas_de_redaction_sans_plan_valide(self):
        e = etat_neuf()
        jusqu_a(e, "plan")
        with self.assertRaises(pl.Usage) as cm:
            pl.fait(e, "redaction", "article.md", None)
        self.assertIn("plan", str(cm.exception))

    def test_plan_fait_mais_pas_valide_bloque_aussi(self):
        e = etat_neuf()
        jusqu_a(e, "plan")
        pl.fait(e, "plan", "plan.md", None)
        with self.assertRaises(pl.Usage):
            pl.fait(e, "redaction", "article.md", None)

    def test_ordre_respecte(self):
        e = etat_neuf()
        jusqu_a(e, "livraison")
        pl.fait(e, "livraison", None, None)
        pl.valider(e, "livraison")
        self.assertIsNone(pl.prochaine(e))

    def test_valider_une_etape_pas_faite(self):
        e = etat_neuf()
        with self.assertRaises(pl.Usage):
            pl.valider(e, "cadrage")

    def test_etape_inconnue(self):
        with self.assertRaises(pl.Usage):
            pl.fait(etat_neuf(), "redaction-finale", None, None)


class Rejouer(unittest.TestCase):
    def test_refaire_renvoie_les_suivantes_en_revue(self):
        e = etat_neuf()
        jusqu_a(e, "maillage")
        touchees = pl.refaire(e, "plan", "ajouter une section prix")
        self.assertEqual(touchees, ["redaction", "controles"])
        self.assertEqual(e["etapes"]["plan"]["statut"], "à refaire")
        self.assertEqual(e["etapes"]["redaction"]["statut"], "à revoir")
        self.assertEqual(e["etapes"]["serp"]["statut"], "validé")
        self.assertEqual(e["etapes"]["cadrage"]["statut"], "validé")

    def test_refaire_ne_touche_jamais_les_precedentes(self):
        e = etat_neuf()
        jusqu_a(e, "livraison")
        pl.refaire(e, "maillage", "un autre hôte")
        for k in pl.CLES[:pl.CLES.index("maillage")]:
            self.assertEqual(e["etapes"][k]["statut"], "validé", k)

    def test_refaire_demande_un_retour(self):
        e = etat_neuf()
        jusqu_a(e, "serp")
        with self.assertRaises(pl.Usage):
            pl.refaire(e, "cadrage", "  ")

    def test_refaire_une_etape_pas_faite(self):
        with self.assertRaises(pl.Usage):
            pl.refaire(etat_neuf(), "plan", "x")

    def test_refaire_puis_fait_redemande_validation(self):
        e = etat_neuf()
        jusqu_a(e, "redaction")
        pl.refaire(e, "plan", "section prix")
        self.assertEqual(pl.fait(e, "plan", "plan-v2.md", None), "à valider")
        self.assertEqual(e["etapes"]["plan"]["fichier"], "plan-v2.md")

    def test_fait_d_une_etape_deja_faite_invalide_les_suivantes(self):
        e = etat_neuf()
        jusqu_a(e, "controles")
        pl.fait(e, "plan", "plan-v2.md", None)
        self.assertEqual(e["etapes"]["redaction"]["statut"], "à revoir")

    def test_passer(self):
        e = etat_neuf()
        jusqu_a(e, "mots-cles")
        pl.passer(e, "mots-cles", "mot-clé donné")
        self.assertEqual(pl.prochaine(e), "serp")

    def test_on_ne_passe_ni_le_plan_ni_la_redaction(self):
        e = etat_neuf()
        for k in ("cadrage", "plan", "redaction", "controles", "livraison"):
            with self.assertRaises(pl.Usage, msg=k):
                pl.passer(e, k, "pressé")

    def test_passer_demande_une_raison(self):
        with self.assertRaises(pl.Usage):
            pl.passer(etat_neuf(), "serp", "")


class Autonome(unittest.TestCase):
    def test_fait_valide_d_office(self):
        e = etat_neuf(autonome=True)
        self.assertEqual(pl.fait(e, "cadrage", None, None), "validé")
        self.assertEqual(pl.prochaine(e), "mots-cles")

    def test_hypotheses_au_rapport(self):
        e = etat_neuf(autonome=True)
        pl.hypothese(e, "cadrage", "persona : indépendant qui se lance, 25-40 ans (site-context.md §3, lecteur 1)")
        pl.hypothese(e, "plan", "guide MECE, consensus fort")
        r = pl.afficher_rapport(e)
        self.assertIn("HYPOTHÈSES À CONFIRMER", r)
        self.assertIn("Cadrage · persona", r)
        self.assertIn("Plan · guide MECE", r)
        self.assertIn("HYPOTHÈSES · 2", pl.afficher_etat(e))

    def test_ordre_tient_aussi_en_autonome(self):
        e = etat_neuf(autonome=True)
        with self.assertRaises(pl.Usage):
            pl.fait(e, "redaction", None, None)

    def test_hypothese_vide(self):
        with self.assertRaises(pl.Usage):
            pl.hypothese(etat_neuf(), "plan", " ")


def porte(nom, etat):
    return {"porte": nom, "etat": etat, "resume": "", "a_corriger": [], "avis": []}


class Verdict(unittest.TestCase):
    def test_bloque_l_emporte(self):
        self.assertEqual(pl.verdict_global([porte("Rédaction", "OK"), porte("Affirmations", "BLOQUÉ"), porte("Humaniseur", "À CORRIGER")]), "BLOQUÉ")

    def test_pas_de_moyenne(self):
        # Deux portes parfaites ne rachètent pas une affirmation bloquante.
        self.assertEqual(pl.verdict_global([porte("Rédaction", "OK"), porte("Affirmations", "BLOQUÉ"), porte("Humaniseur", "OK")]), "BLOQUÉ")

    def test_non_lance_n_est_jamais_livrable(self):
        self.assertEqual(pl.verdict_global([porte("Rédaction", "OK"), porte("Affirmations", "OK"), porte("Humaniseur", "NON LANCÉ")]), "CONTRÔLES INCOMPLETS")

    def test_avis_ne_bloque_pas(self):
        self.assertEqual(pl.verdict_global([porte("Rédaction", "OK"), porte("Affirmations", "OK"), porte("Humaniseur", "AVIS")]), "LIVRABLE")

    def test_humaniseur_note_basse_sans_paragraphe_est_un_avis(self):
        script = Path(tempfile.mkdtemp()) / "faux.py"
        script.write_text("import json;print(json.dumps({'niveau':'strict','resultats':[{'score':61.0,'verdict':'À REVOIR','controles':{'CONCRET':{'score':40,'detail':'2 pour 100 mots'}},'densite':[{'paragraphe':1,'action':'LAISSER'}]}]}))")
        r = pl.porte_humaniseur(script, [], 70)
        self.assertEqual(r["etat"], "AVIS")
        self.assertEqual(r["a_corriger"], [])
        self.assertTrue(r["avis"][0].startswith("CONCRET 40"))

    def test_humaniseur_fuite_de_modele_bloque(self):
        script = Path(tempfile.mkdtemp()) / "faux.py"
        script.write_text("import json;print(json.dumps({'niveau':'strict','resultats':[{'score':20.0,'verdict':'SIGNALÉ','controles':{},'densite':[]}]}))")
        self.assertEqual(pl.porte_humaniseur(script, [], 70)["etat"], "BLOQUÉ")

    def test_sortie_illisible_devient_non_lance(self):
        script = Path(tempfile.mkdtemp()) / "faux.py"
        script.write_text("import sys;print('Traceback');sys.exit(1)")
        self.assertEqual(pl.porte_redaction(script, [])["etat"], "NON LANCÉ")


class Portail(unittest.TestCase):
    """Le portail sur les vrais scripts du pack."""

    def setUp(self):
        self.dossier = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dossier)
        self.assertEqual(lancer("init", "mutuelle indépendant", "--dossier", self.dossier, "--ymyl").returncode, 0)

    def controler(self, article, *extra):
        p = lancer("controler", article, "--dossier", self.dossier, *OPTS_SITE, *extra, "--json")
        return p.returncode, json.loads(p.stdout)

    def test_article_ia_bloque(self):
        code, r = self.controler(ARTICLE_IA)
        self.assertEqual(code, 3)
        self.assertEqual(r["verdict"], "BLOQUÉ")
        portes = {p["porte"]: p for p in r["portes"]}
        self.assertEqual(portes["Affirmations"]["etat"], "BLOQUÉ")
        self.assertTrue(any("73%" in c for c in portes["Affirmations"]["a_corriger"]))

    def test_tour_1_a_corriger_puis_tour_2_livrable(self):
        code, r = self.controler(ICI / "article-tour1.md")
        self.assertEqual((code, r["verdict"], r["tour"]), (2, "À CORRIGER", 1))
        hum = next(p for p in r["portes"] if p["porte"] == "Humaniseur")
        self.assertEqual(len(hum["a_corriger"]), 2)
        self.assertEqual(len(r["trous"]), 4)
        code, r = self.controler(ICI / "article-tour2.md")
        self.assertEqual((code, r["verdict"], r["tour"]), (0, "LIVRABLE", 2))
        self.assertEqual(len(r["trous"]), 4, "les trous restent listés quand l'article est livrable")

    def test_relecture_humaine_au_dernier_tour(self):
        self.controler(ICI / "article-tour1.md")
        code, r = self.controler(ICI / "article-tour1.md")
        self.assertEqual((code, r["verdict"]), (2, "RELECTURE HUMAINE"))

    def test_bloque_ne_devient_jamais_relecture_humaine(self):
        self.controler(ARTICLE_IA)
        code, r = self.controler(ARTICLE_IA)
        self.assertEqual((code, r["verdict"]), (3, "BLOQUÉ"))

    def test_nouvelle_version_repart_au_tour_1(self):
        etat = pl.charger(str(self.dossier))
        jusqu_a(etat, "controles")
        pl.sauver(str(self.dossier), etat)
        self.controler(ICI / "article-tour1.md")
        self.controler(ICI / "article-tour1.md")
        etat = pl.charger(str(self.dossier))
        pl.refaire(etat, "plan", "section prévoyance")
        pl.sauver(str(self.dossier), etat)
        code, r = self.controler(ICI / "article-tour1.md")
        self.assertEqual((r["tour"], r["verdict"]), (1, "À CORRIGER"))
        self.assertIn("plan", r["avertissement"])
        rapport = lancer("rapport", "--dossier", self.dossier).stdout
        self.assertIn("version 1 · 2 tour(s) : À CORRIGER → RELECTURE HUMAINE", rapport)
        self.assertIn("version 2 · 1 tour(s) : À CORRIGER", rapport)

    def test_corriger_l_article_ne_remet_pas_le_compteur_a_zero(self):
        etat = pl.charger(str(self.dossier))
        jusqu_a(etat, "controles")
        pl.sauver(str(self.dossier), etat)
        self.controler(ICI / "article-tour1.md")
        etat = pl.charger(str(self.dossier))
        pl.fait(etat, "redaction", "article.md", "passages corrigés")
        pl.sauver(str(self.dossier), etat)
        code, r = self.controler(ICI / "article-tour1.md")
        self.assertEqual(r["tour"], 2)

    def test_statut_des_controles_suit_le_verdict(self):
        etat = pl.charger(str(self.dossier))
        jusqu_a(etat, "controles")
        pl.sauver(str(self.dossier), etat)
        self.controler(ICI / "article-tour1.md")
        self.assertEqual(pl.charger(str(self.dossier))["etapes"]["controles"]["statut"], "à refaire")
        self.controler(ICI / "article-tour2.md")
        self.assertEqual(pl.charger(str(self.dossier))["etapes"]["controles"]["statut"], "à valider")

    def test_skill_installe_seul_controles_incomplets(self):
        vide = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, vide)
        seul = vide / "seo-article"
        shutil.copytree(PACK / "skills" / "seo-article", seul, ignore=shutil.ignore_patterns("__pycache__"))
        p = subprocess.run([sys.executable, str(seul / "scripts" / "pipeline.py"), "controler", str(ICI / "article-tour2.md"),
                            "--ymyl", *OPTS_SITE, "--json"], capture_output=True, text=True)
        r = json.loads(p.stdout)
        etats = {x["porte"]: x["etat"] for x in r["portes"]}
        self.assertEqual(etats["Rédaction"], "NON LANCÉ")
        self.assertEqual(etats["Humaniseur"], "NON LANCÉ")
        self.assertEqual(etats["Affirmations"], "OK", "affirmations.py vient du commun/ du Skill")
        self.assertEqual(r["verdict"], "CONTRÔLES INCOMPLETS")
        self.assertEqual(p.returncode, 2)

    def test_option_outils(self):
        vide = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, vide)
        seul = vide / "seo-article"
        shutil.copytree(PACK / "skills" / "seo-article", seul, ignore=shutil.ignore_patterns("__pycache__"))
        p = subprocess.run([sys.executable, str(seul / "scripts" / "pipeline.py"), "controler", str(ICI / "article-tour2.md"),
                            "--ymyl", "--outils", str(PACK / "skills"), *OPTS_SITE, "--json"], capture_output=True, text=True)
        self.assertEqual(json.loads(p.stdout)["verdict"], "LIVRABLE")

    def test_article_absent(self):
        p = lancer("controler", self.dossier / "absent.md")
        self.assertEqual(p.returncode, 1)


class Cli(unittest.TestCase):
    def setUp(self):
        self.dossier = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dossier)

    def test_sans_init(self):
        p = lancer("etat", "--dossier", self.dossier)
        self.assertEqual(p.returncode, 1)
        self.assertIn("init", p.stderr)

    def test_init_refuse_d_ecraser(self):
        lancer("init", "x", "--dossier", self.dossier)
        self.assertEqual(lancer("init", "y", "--dossier", self.dossier).returncode, 1)
        self.assertEqual(lancer("init", "y", "--dossier", self.dossier, "--forcer").returncode, 0)

    def test_parcours_complet(self):
        d = self.dossier
        lancer("init", "mutuelle indépendant", "--dossier", d, "--ymyl")
        p = lancer("fait", "redaction", "--dossier", d)
        self.assertEqual(p.returncode, 1)
        self.assertIn("On ne rédige pas sans plan validé", p.stderr)
        for k in ("cadrage", "serp", "plan", "redaction"):
            if k == "serp":
                lancer("passer", "mots-cles", "--dossier", d, "--raison", "donné")
            self.assertEqual(lancer("fait", k, "--dossier", d).returncode, 0, k)
            self.assertEqual(lancer("valider", k, "--dossier", d).returncode, 0, k)
        out = lancer("etat", "--dossier", d).stdout
        self.assertIn("SUITE · Contrôles", out)
        etat = json.loads(lancer("etat", "--dossier", d, "--json").stdout)
        self.assertEqual(etat["etapes"]["mots-cles"]["statut"], "passée")


if __name__ == "__main__":
    unittest.main()
