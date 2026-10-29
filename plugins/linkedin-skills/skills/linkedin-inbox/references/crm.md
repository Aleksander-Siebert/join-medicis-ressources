# Les prospects dans le CRM

## Ce que produit `boite.py crm`

Une ligne par prospect, avec ces colonnes :

| Colonne | Contenu |
|---|---|
| Prénom, Nom | tels qu'ils signent |
| Poste, Entreprise | tirés du titre (« Directrice marketing · Mutuelle régionale ») |
| Source | « LinkedIn, message reçu le {{date}} » |
| Date d'entrée | le jour de l'import |
| Base légale | à valider par l'utilisateur (voir plus bas) |
| Note | l'extrait du message |
| Prochaine étape, Échéance | « répondre aujourd'hui », la date du jour |

`--format csv` : points-virgules (ouverture directe dans un tableur réglé en
français). `--format tsv` : tabulations, à coller dans Google Sheets ou Excel.

## Importer

- **HubSpot** : Contacts, Importer, un fichier, puis faire correspondre
  chaque colonne à une propriété. Créer avant l'import les propriétés qui
  n'existent pas (source LinkedIn, base légale) ou les ignorer.
- **Pipedrive** : Importer des données, un fichier, puis faire correspondre
  les colonnes aux champs de personne, d'organisation et d'affaire.
- **Tableur** : coller le bloc TSV.

Les intitulés exacts des menus changent : suivre l'assistant d'import du CRM.
Le Skill ne se connecte pas au CRM et n'y écrit rien (`commun/regles.md`,
règle 1), même avec un connecteur.

## Le cadre RGPD

| Situation | Ce qui s'applique | Source |
|---|---|---|
| Le prospect a écrit le premier | il a fourni lui-même ses informations : il est informé (identité, finalité, droits) au moment de la collecte, en pratique dans la réponse ou par la politique de confidentialité | RGPD, article 13 |
| L'utilisateur recopie un profil qu'il a cherché | information au plus tard lors de la première communication | RGPD, article 14, paragraphe 3 |
| Base légale | répondre à une demande de devis relève de mesures précontractuelles prises à la demande de la personne (article 6, paragraphe 1, point b) ; un suivi commercial B2B relève généralement de l'intérêt légitime (CNIL) | RGPD art. 6 ; CNIL, « La prospection commerciale par courrier électronique », mise à jour le 10 juin 2026 |
| Durée | ne garder un prospect sans suite que le temps utile ; la CNIL retient 3 ans après le dernier contact pour un prospect | CNIL, référentiel « gestion commerciale » **[à vérifier]** |

La colonne « Base légale » reste marquée **[à valider]** : c'est à
l'utilisateur, ou à son délégué à la protection des données, de la fixer.
