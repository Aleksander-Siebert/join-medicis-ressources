"""serveur.py : un site de test par cas, chacun sur son port local (http://127.0.0.1:PORT).

Chaque cas décrit : le statut et le texte de /robots.txt, le HTML et les
en-têtes des pages, le statut de /llms.txt. Sert au banc de comparaison :
tous les outils lisent exactement le même site.
"""
from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def fabrique(cas: dict):
    class Gestion(BaseHTTPRequestHandler):
        def log_message(self, *a):  # silencieux
            pass

        def _repondre(self, statut, corps="", entetes=None, type_="text/html; charset=utf-8", tete=False):
            data = corps.encode("utf-8")
            self.send_response(statut)
            self.send_header("Content-Type", type_)
            self.send_header("Content-Length", str(len(data)))
            for k, v in (entetes or {}).items():
                self.send_header(k, v)
            self.end_headers()
            if not tete:
                self.wfile.write(data)

        def _servir(self, tete=False):
            chemin = self.path.split("?")[0]
            if chemin == "/robots.txt":
                r = cas.get("robots", {"statut": 404, "texte": ""})
                if r.get("couper"):
                    self.connection.close()  # erreur réseau simulée
                    return
                return self._repondre(r["statut"], r.get("texte", ""), type_="text/plain; charset=utf-8", tete=tete)
            if chemin in cas.get("pages", {}):
                p = cas["pages"][chemin]
                return self._repondre(p.get("statut", 200), p.get("html", ""), p.get("entetes"), tete=tete)
            return self._repondre(404, "<h1>404</h1>", tete=tete)

        def do_GET(self):
            self._servir()

        def do_HEAD(self):
            self._servir(tete=True)

    return Gestion


class Sites:
    """Démarre un serveur par cas ; .url(id) donne l'adresse de base."""

    def __init__(self, cas: list[dict]):
        self.serveurs = {}
        for c in cas:
            s = ThreadingHTTPServer(("127.0.0.1", 0), fabrique(c))
            threading.Thread(target=s.serve_forever, daemon=True).start()
            self.serveurs[c["id"]] = s

    def url(self, ident: str) -> str:
        return f"http://127.0.0.1:{self.serveurs[ident].server_address[1]}"

    def arreter(self):
        for s in self.serveurs.values():
            s.shutdown()
