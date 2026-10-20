# Réécrire une annonce de recherche ou de réseau social pour ChatGPT Ads

Une annonce ChatGPT s'affiche sous une réponse, dans une conversation. La
personne n'a pas tapé un mot-clé : elle a décrit une situation. L'annonce
complète la réponse, elle ne crie pas plus fort qu'elle.

## Les écarts de format

| | Google Ads (annonce responsive) | Meta Ads | Microsoft Ads | ChatGPT Ads (modèle d'import) |
|---|---|---|---|---|
| Titre | 30 caractères, jusqu'à 15 | titre court, souvent coupé | 30 caractères | **24 caractères**, un seul |
| Texte | 90 caractères, jusqu'à 4 | texte principal long | 90 caractères | **48 caractères**, un seul |
| Ciblage | mots-clés | audiences | mots-clés | **context hints** (situations), pays, plateformes |
| Image | non (recherche) | oui | non (recherche) | **oui**, carrée |

Les limites de Google et Microsoft sont données comme repères ; seules
celles de ChatGPT Ads comptent pour l'import (`commun/faits.md`).

## Méthode en 5 gestes

1. **Garder l'angle, pas la phrase.** « Devis en 2 minutes » dit
   *rapidité* ; si « 2 minutes » est validé, il peut rester, sinon l'angle
   devient « Votre devis en ligne ».
2. **Couper ce que ChatGPT a déjà dit.** La réponse a expliqué le sujet :
   l'annonce apporte le **prochain pas** (un devis, un guide, un essai).
3. **Écrire pour la situation, pas pour le mot-clé.** Terme « quelle
   assurance pour partir vivre au canada » → hint « préparer une
   installation au Canada » → titre « Partir vivre au Canada ».
4. **Titre et texte complémentaires.** Le titre nomme la situation ou le
   bénéfice ; le texte dit ce qu'on obtient en cliquant.
5. **Une preuve au plus, validée.** Chiffre, prix, « gratuit », « n°1 » :
   seulement avec la source de la liste d'allégations.

## Exemples (fictifs, Assurly)

| Source | Problème | Réécriture ChatGPT Ads |
|---|---|---|
| Google, titre « {KeyWord:Assurance Expat} » | paramètre dynamique, 25 caractères | « Assurance expatrié » (18) |
| Google, description « Le n°1 de l'assurance expatrié [tiret cadratin] conseillers à Paris. » | « n°1 » non étayé, tiret cadratin, 53 caractères | « Des conseillers à Paris pour votre départ. » (42), si l'allégation « conseillers à Paris » est validée |
| Meta, texte principal de 120 caractères sur la famille | trop long | titre « Partir en famille » (17) + texte « Santé, scolarité, rapatriement : on prépare tout. » (49 : trop long d'un caractère, à resserrer) → « Santé, scolarité, rapatriement réunis. » (38) |
| Google, titre « Best student insurance » | anglais, superlatif | « Assurance étudiant monde » (24), sans superlatif |
| Terme « assurance expatrié » (2 mots) | mot-clé, pas une situation | ne devient pas un hint ; « comparer les couvertures avant une expatriation » si le besoin est confirmé |

## Secteur restreint

L'exemple Assurly relève de l'assurance : les règles d'OpenAI (v1.6) la
disent « généralement interdite » hors des États-Unis. Le Skill alerte,
propose les pistes de `commun/politiques-openai.md` § 6 (offres non
restreintes, contenu pédagogique, situations voisines, demande d'examen),
puis réécrit. Les annonces restent **véridiques** : une annonce d'assurance
dit qu'elle parle d'assurance.

## Ce qui ne se transpose jamais

- Les paramètres dynamiques (insertion de mot-clé, compte à rebours, lieu).
- Les extensions (lieu, appel, liens annexes) : ChatGPT Ads n'en a pas.
- « Site officiel », « Cliquez ici », le ton d'urgence.
- Les mentions de prix ou de promotion périmées (vérifier la date).
