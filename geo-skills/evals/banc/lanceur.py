"""lanceur.py : lance un outil de référence en neutralisant sa seule garde anti-SSRF.

Les outils de référence refusent les adresses locales (127.0.0.1), ce qui
est une bonne protection en usage normal. Pour le banc, tous les outils
doivent lire le même site de test local : ce lanceur remplace la fonction
de garde par une fonction qui accepte l'URL, puis appelle la ligne de
commande de l'outil, sans rien changer d'autre.

  python3 lanceur.py geo-optimizer <racine du dépôt> -- <arguments de « geo »>
  python3 lanceur.py ultimate <racine du dépôt> <script.py> -- <arguments>
"""
import runpy
import sys
from pathlib import Path


def geo_optimizer(racine, args):
    sys.path.insert(0, str(Path(racine) / "src"))
    import geo_optimizer.utils.validators as v
    v.validate_public_url = lambda url, *a, **k: (True, None)
    v.resolve_and_validate_url = lambda url, *a, **k: (True, None, ["127.0.0.1"])
    v._check_ip_blocked = lambda ip, *a, **k: (False, None)
    from geo_optimizer.cli.main import cli  # noqa: E402
    for nom, mod in list(sys.modules.items()):
        if nom.startswith("geo_optimizer") and hasattr(mod, "validate_public_url"):
            mod.validate_public_url = v.validate_public_url
    sys.argv = ["geo"] + args
    cli()


def ultimate(racine, script, args):
    dossier = Path(racine) / "scripts"
    sys.path.insert(0, str(dossier))
    import url_safety as u
    vraie = u.validate_url

    def accepte(url, *a, **k):
        r = vraie(url, resolve_dns=False)
        r.ok, r.reason = True, ""
        r.normalized_url = r.normalized_url or url
        return r
    u.validate_url = accepte
    if hasattr(u, "validate_redirect_chain"):
        u.validate_redirect_chain = lambda urls, *a, **k: accepte(list(urls)[-1])
    sys.argv = [script] + args
    runpy.run_path(str(dossier / script), run_name="__main__")


if __name__ == "__main__":
    outil, racine = sys.argv[1], sys.argv[2]
    i = sys.argv.index("--")
    if outil == "geo-optimizer":
        geo_optimizer(racine, sys.argv[i + 1:])
    elif outil == "ultimate":
        ultimate(racine, sys.argv[3], sys.argv[i + 1:])
