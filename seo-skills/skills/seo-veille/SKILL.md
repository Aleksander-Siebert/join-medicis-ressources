---
name: seo-veille
description: >-
  Deux veilles SEO : les nouvelles pages publiées par les concurrents (en
  comparant leurs sitemaps d'une fois sur l'autre), et le rapport mensuel
  Search Console (gagnants, perdants, pages qui ne reçoivent plus de clics),
  avec 6 à 10 pistes d'analyse à valider. Utilise-le pour « veille
  concurrentielle », « qu'ont publié mes concurrents », « rapport SEO
  mensuel », « bilan Search Console ».
---

# seo-veille

Deux routines qui prennent une journée à la main et cinq minutes ici.
Inspiré du flux concurrents et du rapport mensuel d'Ahrefs (Agent A).

## 1. Veille concurrents

`concurrents.txt` : une ligne par concurrent, `Nom ; URL du sitemap`
(les concurrents de `site-context.md`).

```bash
python3 veille.py concurrents concurrents.txt --etat veille-etat.json --titres --filtre /blog/
```

Le premier passage enregistre l'état. Les suivants listent les nouvelles
pages (date et titre). Pour chaque nouvelle page intéressante :

- son sujet principal en 2 à 4 mots et l'intention ;
- est-ce que le site couvre déjà ce sujet (`/seo-maillage`) ?
- action proposée : ignorer, surveiller, ou créer/renforcer une page
  (`/seo-keywords` puis `/seo-brief`).

Ne propose pas de copier : on cherche les sujets, pas les textes.

## 2. Rapport mensuel Search Console

Deux exports « Pages » (Performances → Pages → Exporter), mois en cours et
mois précédent, à lancer le 2 ou 3 du mois (données complètes) :

```bash
python3 veille.py rapport pages-octobre.csv pages-septembre.csv --top 25
```

Sortie : clics totaux et variation, 25 gagnants, 25 perdants, pages qui
n'ont plus de clic. Ensuite, le Skill :

1. propose **6 à 10 pistes d'analyse** (ex. « 4 des 5 perdants sont des
   guides de 2024 : contenus datés ? », « la page X a perdu 6 places : SERP
   changée ? »), et l'utilisateur choisit celles à creuser ;
2. pour chaque piste retenue, l'action : `/seo-refresh`, `/seo-serp`,
   `/seo-maillage`.

Ne conclus jamais sur une cause sans preuve : « baisse de 30% » est un fait,
« à cause de la mise à jour de mars » est une hypothèse à vérifier.

## Récurrence

- **Claude Code** : tâche planifiée (ex. veille chaque lundi, rapport le 2 du
  mois).
- **claude.ai et autres** : à lancer à la main avec les exports ; sans
  exécution de code, colle les deux exports et fais la comparaison à la
  lecture.

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
- Zéro invention : chiffres tirés des exports uniquement, causes présentées
  comme hypothèses.
- Texte simple dans la conversation, sans créer de document.
- Respecte les sites lus : une requête toutes les 0,3 s, pas d'extraction
  massive de contenu.
