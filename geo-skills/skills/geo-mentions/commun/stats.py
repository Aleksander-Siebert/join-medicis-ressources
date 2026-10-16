#!/usr/bin/env python3
"""stats.py : taux, intervalles et comparaisons pour des réponses d'IA.

Une réponse d'IA est un tirage : la même question ne donne pas deux fois la
même réponse. On rapporte donc un taux (« mentionnée dans 7 réponses sur
20 ») avec son intervalle de confiance à 95%, et on ne parle de hausse ou de
baisse que si la différence dépasse la marge d'erreur.

Méthodes :
  - intervalle de Wilson (fiable même avec peu de passages ou un taux de 0
    ou 100%) ;
  - différence de deux taux par la méthode de Newcombe (combine les deux
    intervalles de Wilson) : « hausse » si tout l'intervalle de la
    différence est au-dessus de 0, « baisse » s'il est en dessous, sinon
    « pas de changement détectable ».

Python 3 sans dépendance. Utilisable comme module ou en ligne de commande :

  python3 stats.py taux 7 20                  taux, intervalle, marge
  python3 stats.py comparer 4 20 11 20        avant 4/20, après 11/20
  python3 stats.py echantillon --marge 10     passages pour ±10 points (p = 0,5 par défaut)
  python3 stats.py ... --json
"""

import argparse
import json
import math
import sys

Z95 = 1.959963984540054


def wilson(k, n, z=Z95):
    """Intervalle de Wilson à 95% pour k succès sur n, ou None si n = 0."""
    if n <= 0:
        return None
    if not 0 <= k <= n:
        raise ValueError(f"succès hors limites : {k} sur {n}")
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    demi = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, centre - demi), min(1.0, centre + demi)


def taux(k, n):
    """Dictionnaire complet pour k sur n : taux, intervalle, marge (en points)."""
    if n <= 0:
        return {"k": k, "n": n, "taux": None, "ic": None, "marge": None}
    bas, haut = wilson(k, n)
    return {"k": k, "n": n, "taux": k / n, "ic": [bas, haut], "marge": (haut - bas) / 2}


def comparer(k1, n1, k2, n2):
    """Compare deux taux (avant k1/n1, après k2/n2) par Newcombe.

    Renvoie l'écart (après moins avant), son intervalle et un verdict :
    « hausse », « baisse » ou « pas de changement détectable ».
    """
    if n1 <= 0 or n2 <= 0:
        return {"ecart": None, "ic": None, "verdict": "non mesurable (aucun passage sur une période)"}
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    d = p2 - p1
    bas = d - math.sqrt((p2 - l2) ** 2 + (u1 - p1) ** 2)
    haut = d + math.sqrt((u2 - p2) ** 2 + (p1 - l1) ** 2)
    if bas > 0:
        verdict = "hausse"
    elif haut < 0:
        verdict = "baisse"
    else:
        verdict = "pas de changement détectable"
    return {"avant": taux(k1, n1), "apres": taux(k2, n2), "ecart": d, "ic": [bas, haut], "verdict": verdict}


def echantillon(marge, p=0.5):
    """Passages nécessaires pour une marge de ± `marge` (en points, ex. 10) au taux p."""
    m = marge / 100
    if m <= 0:
        raise ValueError("la marge doit être positive")
    return math.ceil(Z95 * Z95 * p * (1 - p) / (m * m))


def pct(x, decimales=0):
    """0.345 → « 35% » (typographie du pack : pourcentage collé)."""
    if x is None:
        return "n.d."
    f = 10 ** decimales
    v = math.floor(100 * x * f + 0.5) / f  # arrondi au plus proche, 12,5 → 13
    s = f"{v:.{decimales}f}".replace(".", ",")
    return f"{s}%"


def phrase_taux(t):
    """« 35% (7/20, IC 95% : 18-57%) »."""
    if t["n"] == 0:
        return "aucun passage"
    bas, haut = t["ic"]
    return f"{pct(t['taux'])} ({t['k']}/{t['n']}, IC 95% : {pct(bas)[:-1]}-{pct(haut)})"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Taux, intervalles de confiance et comparaisons pour des réponses d'IA.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("taux", help="taux et intervalle pour k succès sur n passages")
    a.add_argument("k", type=int)
    a.add_argument("n", type=int)
    b = sub.add_parser("comparer", help="comparer deux périodes : k1 n1 (avant) k2 n2 (après)")
    for nom in ("k1", "n1", "k2", "n2"):
        b.add_argument(nom, type=int)
    c = sub.add_parser("echantillon", help="nombre de passages pour une marge donnée")
    c.add_argument("--marge", type=float, required=True, help="marge voulue, en points (ex. 10)")
    c.add_argument("--p", type=float, default=0.5, help="taux attendu (0 à 1), défaut 0,5 (cas le plus exigeant)")
    for s in (a, b, c):
        s.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    try:
        if args.cmd == "taux":
            r = taux(args.k, args.n)
            texte = phrase_taux(r) + (f" · marge ±{round(100 * r['marge'])} points" if r["marge"] is not None else "")
        elif args.cmd == "comparer":
            r = comparer(args.k1, args.n1, args.k2, args.n2)
            if r["ecart"] is None:
                texte = r["verdict"]
            else:
                bas, haut = r["ic"]
                texte = (f"avant {phrase_taux(r['avant'])} · après {phrase_taux(r['apres'])}\n"
                         f"écart {round(100 * r['ecart']):+d} points (IC 95% : {round(100 * bas):+d} à "
                         f"{round(100 * haut):+d}) · {r['verdict'].upper()}")
        else:
            n = echantillon(args.marge, args.p)
            r = {"marge": args.marge, "p": args.p, "passages": n}
            texte = f"{n} passages pour une marge de ±{args.marge:g} points au taux de {pct(args.p)}"
    except ValueError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    if args.json:
        json.dump(r, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        print(texte)
    return 0


if __name__ == "__main__":
    sys.exit(main())
