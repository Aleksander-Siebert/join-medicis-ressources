# site-context.md

Le contexte de ton site. Les Skills des packs SEO et GEO le lisent avant de
travailler : sans lui, ils écrivent pour « un site en général » ; avec lui,
ils écrivent pour toi.

Copie ce fichier dans `~/.claude/seo/site-context.md` (Claude Code) ou mets-le
dans les connaissances de ton Projet (claude.ai, ChatGPT, Gemini, Mistral).
Pas envie de le remplir ? Lance `/seo-context` avec l'URL de ton site : il
pose les questions et le remplit avec toi.

Un exemple rempli est dans `exemple-site-context.md`.

> **Ne le mets jamais dans un dépôt public** : il contient des informations
> internes (offres, règles, données produit).

## État

- rempli : non
- mis à jour le :

## Comment lire les étiquettes

Chaque donnée produit porte une étiquette :

- `LIVE` : vraie aujourd'hui, avec sa source ; les Skills l'affirment.
- `À CONFIRMER` : probable mais non vérifiée ; elle sort en
  `{{à confirmer : …}}`, jamais affirmée.
- `RETIRÉ` : n'est plus vraie ; elle ne sort jamais (on la garde pour qu'elle
  ne revienne pas).

---

## 1. Le site

- **Nom de l'entreprise :**
- **URL :**
- **Ce qu'elle vend, en une phrase :**
- **Chiffres publics vérifiables :** (avec la page qui les publie)
- **Langue(s) et pays visés :**
- **CMS :** (WordPress, Webflow, Shopify, Next.js…)

## 2. Le secteur

- **YMYL ?** (oui / non) : santé, finances, assurance, juridique, sécurité.
  Si oui, la règle « zéro invention » est stricte : aucun prix, délai,
  plafond, condition ou chiffre médical sans source fournie.
- **Termes techniques, juridiques ou médicaux à employer correctement :**
- **Ce qu'il ne faut jamais affirmer :** (promesses de résultat, comparaisons interdites, obligations réglementaires)
- **Mentions obligatoires :** (ex. numéro d'immatriculation professionnelle, avertissement)

## 3. Les lecteurs

Pour chaque persona : qui, où, quel problème, quel niveau de connaissance,
quels mots il emploie.

1.
2.
3.

## 4. Les pages à pousser

Pages produit ou service vers lesquelles les articles doivent mener, avec leur
URL. C'est la base du maillage.

| Page | URL | Pour quel persona |
|---|---|---|
| | | |

## 5. Le ton

- **Registre :** (corporate accessible, expert, chaleureux, direct…)
- **Tutoiement ou vouvoiement :**
- **Style affirmatif :** (oui / non) Si oui : voix active obligatoire, aucun
  verbe modal d'hésitation (« peut-être », « pourrait », « devrait »,
  « il semblerait »).
- **Exemples de phrases qui nous ressemblent :**
- **Exemples de phrases qui ne nous ressemblent pas :**

## 6. Les règles maison

- **Règles d'entité :** comment nommer l'entreprise (ex. « à Marque », jamais « chez Marque »)
- **Remplacements obligatoires :**
- **Mots interdits en plus de la liste anti-IA :**
- **Références à éviter :** (ex. ne pas présenter un système national comme la norme si l'audience est internationale)
- **Longueur par défaut d'un article :** (défaut du pack : 1 000 à 1 500 mots ; c'est une préférence, Google n'a pas de nombre de mots préféré)
- **Résumé en tête d'article :** (défaut : oui, 3 lignes maximum)
- **Cadre par défaut si le type de page est clair :** (PAS, AIDA, MECE, pyramide inversée)
- **Title et description :** (défaut : title de 55 à 60 caractères, description de 150 à 160 ; la largeur en pixels décide)

## 7. Les données produit

Les faits que les articles ont le droit d'affirmer. Une ligne par fait, avec
sa source. Ce qui n'est pas ici sort en `{{à compléter}}`.

| Fait | Valeur | Source (page, document, date) | Étiquette |
|---|---|---|---|
| | | | LIVE / À CONFIRMER / RETIRÉ |

## 8. Les auteurs

Qui signe, et ce qui prouve son expertise (lien vérifiable : registre
professionnel, page auteur, profil public).

| Auteur | Rôle, expertise | Preuve vérifiable (lien) | Sujets |
|---|---|---|---|
| | | | |

## 9. Les preuves de l'entreprise

Cas clients, données propres, méthodes, ce que l'entreprise a vu sur le
terrain (anonymisé si besoin). L'expérience vécue d'une personne va dans
`reserve.md`, partagé avec le pack LinkedIn.

| Preuve | Chiffre ou fait | Date | Publiable ? |
|---|---|---|---|
| | | | oui / anonymisé / non |

## 10. Les concurrents

Les 3 à 5 sites qui te prennent les positions que tu veux, avec leur URL et
leur sitemap si tu le connais (pour `/seo-veille`).

-
-
-

## 11. Les outils connectés

Ce qui est disponible (les Skills s'en servent s'ils sont connectés, et
marchent sans) : Search Console, Semrush, Ahrefs, Google Analytics, HubSpot.

-
