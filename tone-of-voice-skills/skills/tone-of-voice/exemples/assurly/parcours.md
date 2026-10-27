# Parcours complet : Camille, fondatrice d'Assurly

Exemple fictif (Assurly, assurly.example, n'existe pas). Il montre le mode
« Créer » de bout en bout ; le résultat est `tone-of-voice.md` dans ce
dossier, les textes d'origine dans `textes/`.

## 1. Collecte

Camille colle 5 textes : 3 posts LinkedIn, un email à un client, un message
WhatsApp à l'équipe. Elle en avait un sixième, une lettre de réclamation
rédigée par le service juridique : écartée (relue par d'autres, registre
administratif).

## 2. Mesure

```
python3 scripts/voix.py textes/*.txt
```

Ce que le script sort (extrait) :

```
VOIX : 5 texte(s), 405 mots, 44 phrases · confiance faible
  phrases : médiane 8 mots, écart-type 5.9, 55% de 8 mots ou moins
  vouvoiement (par texte : {'vouvoiement': 5})
  pour 1000 mots : je 22.2 · on 39.5 · nous 4.9 · négation sans « ne » 9.9
  points d'exclamation   0  jamais
  émojis                 0  jamais
RÈGLES JUSTIFIÉES PAR LES TEXTES (provisoires : corpus court)
  - Jamais d’émojis (0 sur 5 textes).
  - Vouvoiement (5 textes sur 5).
  - « ça » plutôt que « cela ».
ALERTES
  ! Corpus court (405 mots, 5 texte(s)) : profil provisoire…
```

Le Skill le dit à Camille : « 405 mots, c'est court. On fait la voix
maintenant, avec un peu plus de questions, et on la recalcule quand tu as 5
nouveaux posts. »

## 3. Comparaison avec l'IA par défaut

Sujet du post 1 (« un sinistre traité vite »), version qu'une IA écrirait
sans consigne :

> Chez Assurly, la réactivité est au cœur de notre engagement. Lorsqu'un
> client fait face à un sinistre, notre équipe se mobilise pour l'accompagner
> à chaque étape !

Ce que Camille fait autrement :

- **structure** : elle commence par un moment précis (« Mardi, 7 h 40. »),
  jamais par l'entreprise ;
- **arguments** : une durée exacte (« Douze minutes. ») au lieu d'un
  adjectif (« réactive ») ;
- **engagement** : elle minimise (« Pas grand-chose d'extraordinaire, en
  fait. ») là où l'IA vante ;
- **phrase** : fragments assumés (« Photos, constat, dépanneuse. ») ;
- **négations** : aucune exclamation, aucun « au cœur de », aucune
  promesse.

Traits retenus : concrète (pas technique), franche (pas dure), proche (pas
familière), modeste sur les résultats (pas fausse modeste). Refusé au test
de spécificité : « authentique » (vaut pour tout le monde).

## 4. Questions (6 posées)

Les textes répondent déjà à « tu ou vous ? » et aux émojis : pas posées.

| Question | Réponse de Camille | Où ça va |
|---|---|---|
| Quels canaux couvrir ? | LinkedIn, emails clients, WhatsApp équipe | section 8 |
| L'humour ? | « Pas vraiment, on parle de gens qui ont eu un pépin. » | curseur sérieux à 2 |
| Trois mots jamais sous ton nom ? | « n'hésitez pas », « solution », « transparence » | section 6 |
| Je propose : pas de critique des autres assureurs nommés. D'accord ? | oui | section 6 |
| Où tu tranches, où tu nuances ? | « Je tranche sur nos délais. Sur ce qu'on teste, je dis qu'on teste. » | section 7 |
| Tu signes comment tes emails ? | « Bonne journée, Camille » | section 8 |

## 5. Calibrage (2 tours)

Message réel : un post sur le nouvel envoi des pièces par SMS. L'hésitation
porte sur « direct ou amené ».

- **A** : le fait en première phrase (« Depuis lundi, la liste des pièces part
  par SMS dès le premier appel. »)
- **B** : une phrase de contexte d'abord
- **C** : une anecdote d'abord (« Jeudi, un client a mis 9 jours à nous
  envoyer une photo… »)

Camille : « C, mais l'anecdote est trop longue. » Réglage : anecdote de 2
phrases au plus avant le fait (section 4, « Ouvertures »). Tour 2 : « Oui,
c'est moi. »

## 6. Test final

Deux versions du même post, ordre tiré au hasard. Camille choisit la bonne
sans hésiter. Contrôle de la version dans la voix :

```
python3 scripts/ecart.py tone-of-voice.md post-sms.txt
DANS LA VOIX · 100/100
```

## 7. Sortie

```
python3 scripts/profil.py verifier tone-of-voice.md
À REVOIR · tone-of-voice.md
  ! confiance faible : redemander des textes écrits à la main
```

Seule remarque : le corpus court, déjà noté en « Questions ouvertes ».
Camille dit « oui », le fichier est écrit. Elle demande ensuite le Skill :

```
python3 scripts/profil.py ma-voix tone-of-voice.md --nom "Camille" \
  --exemples textes/*.txt --zip
Skill « ma-voix-camille » écrit dans ./ma-voix-camille
  · 5 exemple(s), 2 coordonnée(s) ou nom(s) de tiers retiré(s)
```

Le Skill relève les prénoms « Inès » et « Théo » dans le message WhatsApp ;
Camille accepte qu'ils restent (collègues, d'accord).
