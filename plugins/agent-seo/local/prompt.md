Lance l'agent SEO de ce dossier en suivant `AGENTS.md` de bout en bout, en
mode autonome : personne ne répondra pendant ce passage.

1. Récupère les données Search Console : avec le connecteur s'il est
   disponible, sinon avec le dernier export posé dans `donnees/`. Si aucune
   donnée n'est disponible, dis-le et arrête-toi là.
2. Propose les sujets, écris le premier sujet gardé en brouillon,
   contrôle-le, livre-le en `.md` et `.docx` dans `articles/`. Si aucun
   sujet ne passe le jugement (`AGENTS.md`, étape 3), n'écris pas d'article :
   dis « Rien à écrire cette semaine » et pourquoi.
3. Ne publie rien, n'envoie rien, ne contacte personne. Aucun chiffre, prix,
   délai ou source inventé : ce qui manque devient `{{à compléter}}`.
4. Enregistre le dossier de l'article, `sujets.md` et `memoire/` : commit
   sur la branche principale. Si le dossier a un dépôt distant, push ; si le
   push est refusé, écris-le clairement dans le bilan.
5. Le premier lundi du mois, ajoute le bilan des articles livrés
   (`AGENTS.md`, étape 8).

Termine par le bilan en 5 lignes : sujet choisi, article livré (chemin),
hypothèses à confirmer, trous `{{à compléter}}`, ce qui a bloqué. Si une
règle mériterait d'entrer dans `apprentissages.md`, propose-la ici sans
l'écrire : personne ne peut la valider pendant ce passage.
