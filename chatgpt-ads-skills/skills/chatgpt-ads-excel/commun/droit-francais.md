# Annonces en France : les règles de droit à garder en tête

Les règles d'OpenAI (`commun/politiques-openai.md`) disent ce que la
plateforme accepte. Le droit français dit ce que l'annonceur a le droit
d'écrire. Les deux s'ajoutent : une annonce acceptée par OpenAI peut rester
illégale en France.

Ce fichier n'est pas un avis juridique. Il sert à repérer ce qui demande une
vérification par l'annonceur ou son juriste. Références relevées le 20 oct.
2026 ; vérifier le texte en vigueur sur Légifrance avant de s'y fier.

| Sujet | Règle (référence) | Conséquence pour une annonce de 24 + 48 caractères |
|---|---|---|
| Langue | Usage obligatoire du français dans la publicité ; un terme étranger doit être traduit (loi n° 94-665 du 4 août 1994, art. 2) | annonce en français pour le public français ; un anglicisme de marque passe, un slogan anglais non traduit pose problème |
| Pratiques trompeuses | Interdites : fausses allégations ou présentations sur les caractéristiques, le prix, les résultats, l'identité de l'annonceur (Code de la consommation, art. L121-2 et L121-3 pour les omissions) | même règle que la liste d'allégations du pack : rien qui ne soit étayé ; « gratuit », « offert », « sans engagement » doivent être vrais sans condition cachée |
| Publicité comparative | Licite seulement si elle compare objectivement des biens qui répondent aux mêmes besoins, sans dénigrer (art. L122-1 et suivants) | pas de concurrent nommé dans le pack par défaut ; une comparaison demande une source datée |
| Annonce de réduction | Le prix de référence d'une réduction est le prix le plus bas des 30 jours qui précèdent (art. L112-1-1) | « -30% » ou « prix barré » seulement avec le prix de référence vérifié |
| Crédit à la consommation | Toute publicité porte la mention « Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager. » (art. L312-5) | impossible à faire tenir dans 48 caractères : une annonce de crédit en France n'est pas réalisable dans ce format, en plus de la règle d'OpenAI |
| Médicaments | Publicité auprès du public encadrée (visa de l'ANSM) et interdite pour les médicaments sur prescription (Code de la santé publique, art. L5122-1 et suivants) | à exclure ; la règle d'OpenAI l'exclut aussi |
| Allégations nutritionnelles et de santé (aliments, compléments) | Seules les allégations autorisées par l'Union européenne, dans leurs conditions d'emploi (règlement (CE) n° 1924/2006) | « renforce l'immunité », « brûle les graisses » : interdits sauf allégation autorisée mot pour mot |
| Alcool | Contenu et supports encadrés (loi Évin, Code de la santé publique, art. L3323-2 et suivants) | catégorie interdite par OpenAI de toute façon |
| Allégations environnementales | Allégations génériques (« écologique », « respectueux de l'environnement ») non démontrées interdites dans l'Union européenne (directive (UE) 2024/825, applicable à partir du 27 sept. 2026) **[à vérifier : texte de transposition français]** ; « neutre en carbone » encadré par la loi Climat et résilience de 2021 **[à vérifier : article]** | une allégation verte demande une preuve précise, sinon on la retire |
| Traceurs et pixel | Le dépôt de traceurs non nécessaires demande le consentement préalable (loi Informatique et Libertés, art. 82 ; lignes directrices de la CNIL) | le pixel d'OpenAI doit démarrer en `consent: false` et suivre le bandeau de consentement (`commun/faits.md` § 2 bis) |

## Ce que le pack contrôle par script

- Les chiffres, prix, pourcentages, « gratuit », « garanti », superlatifs :
  bloqués s'ils ne sont pas dans la liste d'allégations approuvées.
- Les termes de crédit, de santé et d'assurance : signalés avec la règle
  d'OpenAI et la règle française correspondante.
- Les allégations vertes génériques : signalées.

Le reste relève du jugement de l'annonceur : le pack le dit, il ne tranche
pas.
