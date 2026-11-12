# Lancer la veille

Colle l'un de ces textes dans la conversation, ou dans le champ
« instructions » de la tâche planifiée.

## Sur ton ordinateur

---

Lance la veille de ce dossier en suivant `AGENT.md` de bout en bout :
collecte, recherches web demandées, tri, `sortie/resume.json`, contrôle par
`scripts/mail.py`, envoi sur les canaux de `mail.json` aux destinations de
`veille.md`, puis `scripts/collecte.py --valider` seulement si l'envoi a
réussi. N'envoie rien ailleurs. Termine par le bilan en 3 lignes.

---

## Dans une tâche planifiée cloud

---

Lance la veille de ce dépôt en suivant `AGENT.md` de bout en bout.
N'envoie qu'aux destinations de `veille.md`, avec les connecteurs.

Si l'envoi a réussi : lance `python3 scripts/collecte.py --valider`, puis
enregistre la mémoire dans le dépôt : `git add memoire archives`, un commit
« Veille : mémoire du jour », et pousse sur la branche principale du dépôt
(pas sur une branche `claude/`). Si le push est refusé, dis-le clairement
dans ta réponse : la prochaine veille renverrait les mêmes infos.

Si l'envoi a échoué : ne lance pas `--valider`, ne pousse rien, et explique
pourquoi.

Termine par le bilan en 3 lignes.

---

## Essai sans envoi

Ajoute à l'un des deux textes : « Essai à blanc : montre-moi la veille dans
la conversation, n'envoie rien et ne lance pas --valider. »
