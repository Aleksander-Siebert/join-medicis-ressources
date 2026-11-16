# Lancer l'agent

Colle l'un de ces textes dans une session claude.ai/code ouverte sur ton
dépôt, ou dans le champ « Instructions » de la tâche planifiée.

## Proposer des sujets

---

Propose-moi des sujets d'articles : suis `AGENT.md`, étapes 1 à 3, et
montre-moi les 5 premiers.

---

## Écrire le prochain article (à la demande)

---

Écris le prochain article : suis `AGENT.md` de bout en bout, en mode
autonome, sur le premier sujet gardé de `sujets.md` (ou sur « {{mot-clé}} »
si je le précise). Livre l'article en `.md` et `.docx`, enregistre tout dans
le dépôt, puis fais le bilan en 5 lignes.

---

## Tous les lundis (tâche planifiée)

---

Lance l'agent SEO de ce dépôt en suivant `AGENT.md` de bout en bout, en mode
autonome : récupère les données Search Console avec le connecteur, propose
les sujets, écris le premier sujet gardé en brouillon, contrôle-le, livre-le
en `.md` et `.docx` dans `articles/`. Ne publie rien et n'envoie rien.

Enregistre ensuite dans le dépôt le dossier de l'article, `sujets.md` et
`memoire/` : commit, puis push sur la branche principale du dépôt (`main`),
pas sur une branche `claude/` : la tâche suivante repart de la branche
principale et doit retrouver la mémoire. Si le push est refusé, dis-le
clairement dans ta réponse.

Le premier lundi du mois, ajoute le bilan des articles livrés (`AGENT.md`,
étape 8).

Termine par le bilan en 5 lignes.

---
