# Lancer la veille

Colle ce texte dans la conversation, ou dans le champ « instructions » de la
tâche planifiée :

---

Lance la veille concurrentielle de ce dossier en suivant `AGENT.md` de bout
en bout : collecte, tri, `sortie/resume.json`, contrôle par
`scripts/mail.py`, envoi à l'adresse de `veille.md`, puis
`scripts/collecte.py --valider` seulement si le mail est parti. N'envoie
rien à une autre adresse. Termine par le bilan en 3 lignes.

---

Pour un essai sans envoi, ajoute : « Essai à blanc : montre-moi le mail dans
la conversation, n'envoie rien et ne lance pas --valider. »
