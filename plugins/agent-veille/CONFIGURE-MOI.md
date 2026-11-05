# Configure-moi

Ouvre ce dossier dans Claude (Cowork ou Claude Code), puis colle le texte
ci-dessous. Compte une dizaine de minutes.

---

Tu vas configurer l'agent de veille concurrentielle de ce dossier. Lis
d'abord `AGENT.md`, `veille.md` et `sources.json`.

**1. Pose-moi ces questions une par une**, en attendant chaque réponse.
Propose un exemple à chaque fois et accepte une réponse courte.

1. Ton entreprise et ce que tu vends, en une phrase. Ton prix d'entrée ou
   ton offre principale, si tu veux que je compare.
2. Tes concurrents : 3 à 10, avec leur site si tu l'as.
3. Ce qui t'intéresse le plus chez eux : prix et offres, produit,
   marketing et campagnes, clients et partenariats, financement et
   recrutement, presse. Plusieurs choix possibles.
4. Ce que tu veux ignorer (exemples : offres d'emploi, sponsoring sportif,
   articles « top 10 »).
5. L'adresse qui reçoit la veille, et le jour et l'heure d'envoi
   (par défaut : le lundi à 8 h).
6. Des pages précises à surveiller chez eux (page tarifs, nouveautés,
   salle de presse) ? Sinon, je te propose les miennes.

**2. Prépare les sources.**

- Trouve le site officiel de chaque concurrent s'il manque. En cas de doute
  (homonymes), demande-moi.
- Ajoute les alias utiles (ancien nom, nom de marque) et, pour un nom
  courant (« Alan », « Orange »), un ou deux `mots_cles` du secteur pour
  éviter les homonymes dans les actualités.
- Écris `sources.json` avec les concurrents, puis lance :
  `python3 scripts/collecte.py --test-sources`
- Le test liste les flux RSS trouvés et les pages à surveiller possibles.
  Garde au plus 3 pages par concurrent : tarifs ou offres d'abord, puis
  nouveautés ou salle de presse. Montre-moi la liste et demande mon accord.
- Retire ou remplace chaque source en erreur, puis relance le test jusqu'à
  ce qu'il n'y ait plus d'erreur.

**3. Remplis `veille.md`** avec mes réponses, sans laisser de `{{à compléter}}`.

**4. Fais un essai à blanc** en suivant `AGENT.md` : collecte, tri,
`sortie/resume.json`, `python3 scripts/mail.py`, puis montre-moi le mail
dans la conversation. N'envoie rien et ne lance pas `--valider`. Demande-moi
ce qu'il faut ajuster (sujets à écarter, ton, longueur) et reporte mes
retours dans `veille.md`.

**5. Envoie-moi un premier mail de test** à mon adresse, après mon accord.
Ensuite seulement, lance `python3 scripts/collecte.py --valider`.

**6. Programme la veille** : propose-moi de créer une tâche planifiée au
rythme choisi, avec le texte de `LANCER.md` comme instructions. Si tu ne
peux pas la créer toi-même, donne-moi les étapes.

Termine par un récapitulatif : concurrents suivis, pages surveillées,
adresse, rythme, et comment modifier tout ça plus tard (« dis-moi “ajoute
tel concurrent” ou modifie `veille.md` »).

---
