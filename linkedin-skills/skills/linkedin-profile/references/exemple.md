# Exemple complet : avant et après

Personne fictive : Camille, responsable acquisition chez Assurly
(assurly.example). Objectif : clients (activité de conseil, avec l'accord de
son employeur). Fichiers : `exemples/profil-avant.json` et
`exemples/profil-apres.json`. Les sorties ci-dessous sont celles des scripts,
recopiées telles quelles.

## Ce que Camille a collé

- Titre : « Responsable marketing chez Assurly »
- Infos : « Passionnée par le marketing digital depuis plus de 10 ans, j'aime
  relever de nouveaux défis. »
- Poste actuel : « En charge de l'acquisition payante et du SEO » ; « Relancé
  1 400 clients dormants en 6 semaines : 212 contrats réactivés »
- Poste précédent : « Gestion des campagnes emailing »
- Sélection vide, bannière par défaut, photo de 4 ans, 18 compétences (les 3
  premières : « Créativité », « Communication », « Marketing »), dernier post
  il y a 45 jours, « Services » non activé, URL par défaut.
- Recommandations : non précisé → **non noté**.

## Note de départ

```
PROFIL  27/93 points notés  ·  FAIBLE  ·  objectif : clients
Fourchette sur 100 : entre 27 et 34 (non montré : Recommandations)

Première heure : « Open to work » ou « Services », URL personnalisée, Titre (+15.4 points)
Une réécriture ne crée pas : Bannière, Activité, Photo.
```

Ordre suivi : « Services » (10 min), URL (5 min), titre (30 min), puis Infos
et Sélection.

## Les chiffres

`reserve.md` contenait déjà « Relancé 1 400 clients dormants en 6 semaines :
212 contrats réactivés ». Questions posées une à une pour le reste :

- « Le coût par lead, il était de combien quand tu es arrivée ? Et
  maintenant ? » → 41 € puis 23 €, en 4 mois, budget constant.
- « Pour l'emailing en agence : combien de campagnes, pour combien de
  clients ? » → 48 campagnes, 6 clients, 2022 ; ouverture de 18% à 27%.
- « Le comparateur de garanties : quel résultat ? » → « je ne sais pas » →
  laissé `{{résultat à confirmer}}`, ligne retirée du profil en attendant.

## Titre : trois options comparées

```
python3 scripts/titre.py \
  --titre "Responsable acquisition chez Assurly | J'aide les assureurs en ligne à baisser leur coût par lead | −44% en 4 mois, budget constant" \
  --titre "Consultante acquisition pour les assureurs en ligne | Coût par lead de 41 € à 23 € en 4 mois | Responsable acquisition chez Assurly" \
  --titre "Acquisition B2C en assurance | 212 contrats réactivés en 6 semaines"
```

Notes : 85 (PRÊT), 84 (PRÊT), 39 (À RÉÉCRIRE : ni audience nommée, ni
terme de métier assez précis).

Recommandée : la première : métier et entreprise dans les
60 premiers caractères, audience, résultat, preuve. Camille l'a lue à voix
haute et l'a gardée.

## Infos

Texte complet dans `references/infos.md` (exemple « objectif clients »).
`infos.py` : PASSE.

## Expériences

```
Responsable acquisition · Assurly · depuis mars 2023
Acquisition B2C d'une assurance en ligne de 120 salariés : SEA, SEO, emailing.
· Réduit le coût par lead de 41 € à 23 € en 4 mois, à budget constant (SEA, SEO)
· Relancé 1 400 clients dormants en 6 semaines : 212 contrats réactivés

Chargée de marketing · agence conseil · sept. 2020 à fév. 2023
· Lancé 48 campagnes emailing pour 6 clients en 2022 : taux d'ouverture moyen passé de 18% à 27%
· Formé 3 clients à leur outil d'emailing en 2 mois : 0 campagne sous-traitée ensuite
```

## Après

```
PROFIL  78/93 points notés  ·  SOLIDE  ·  objectif : clients
Fourchette sur 100 : entre 78 et 85 (non montré : Recommandations)

Corrections restantes : Bannière (hors réécriture), Activité (hors réécriture), Photo (hors réécriture)
```

Dit honnêtement à Camille : « 78 sur les points notés. Ce qui manque ne
s'écrit pas : une bannière (je peux préparer le texte, `/linkedin-carrousel`
peut faire l'image), une photo plus récente, une activité régulière
(`/linkedin-plan`), et des recommandations (modèle de demande dans
`references/recommandations.md`). »

## À vérifier (liste rendue à Camille)

- « Un tiers des clients ne renouvelle pas » (Infos) : chiffre interne,
  publiable ?
- « 0 campagne sous-traitée ensuite » : confirmé pour les 3 clients ?
- Accord de l'employeur pour l'activité de conseil mentionnée dans l'appel à
  l'action.
