---
name: seo-context
description: >-
  Crée ou met à jour le fichier site-context.md que lisent tous les Skills SEO
  et GEO : entreprise, secteur (YMYL ou non), personas, pages à pousser, ton,
  règles maison, concurrents, outils connectés. Utilise-le au premier usage du
  pack, quand l'utilisateur dit « configure mon site », « voici mon site »,
  donne une URL sans autre consigne, ou quand un autre Skill n'a pas de
  contexte.
---

# seo-context

Sans contexte, un Skill SEO écrit pour « un site en général ». Celui-ci
remplit `site-context.md` une fois, et tous les autres s'en servent.

## Déroulé

1. **Lis ce qui existe.** `~/.claude/seo/site-context.md` ou le contenu chargé
   dans le Projet. S'il est rempli, propose seulement de le mettre à jour.
2. **Lis le site.** Avec l'URL, consulte la page d'accueil, la page « à
   propos » et le sitemap (recherche web ou lecture directe). Déduis :
   ce que l'entreprise vend, ses pages produit ou service, sa langue, son ton.
   N'invente rien que le site ne dit pas.
3. **Pose les questions qui manquent**, groupées en une fois, dans cet ordre :
   - le secteur est-il YMYL (santé, finances, assurance, juridique) ?
   - les personas : qui, où, quel problème ;
   - les pages à pousser (avec URL) ;
   - tutoiement ou vouvoiement, style affirmatif (voix active, sans verbe
     modal) oui ou non ;
   - les règles maison : remplacements obligatoires, mots interdits,
     références à éviter ;
   - 3 à 5 concurrents ;
   - les outils connectés (Search Console, Semrush, Ahrefs).
4. **Rends le fichier rempli**, au format du modèle `templates/site-context.md`,
   en texte simple, prêt à copier. Marque `{{à compléter}}` ce qui manque.
5. **Indique où le ranger** : `~/.claude/seo/site-context.md` dans Claude Code,
   les connaissances du Projet ailleurs.

Un exemple rempli (secteur assurance, YMYL) est dans
`templates/exemple-site-context.md`.

## Ce que les autres Skills en tirent

| Section | Utilisée par |
|---|---|
| YMYL, termes, interdits | `seo-write`, `seo-brief`, `seo-refresh` : zéro invention |
| Personas | `seo-keywords`, `seo-brief`, `seo-write` |
| Pages à pousser | `seo-maillage`, `seo-brief`, `seo-write` |
| Ton, règles maison | `seo-write`, `seo-human` (`--affirmatif`, `--remplacer`, `--interdire`) |
| Concurrents | `seo-serp`, `seo-veille` |
| Outils | tous : données réelles si un connecteur est là |

## Règles du pack

- Lis `site-context.md` et `apprentissages.md` s'ils existent.
  `apprentissages.md` passe avant les règles générales.
- Zéro invention : aucun chiffre, prix, délai, condition ou source inventé.
  S'il manque, écris `{{à compléter}}`.
- Réponds en texte simple dans la conversation, sans créer de document, sauf
  demande. Markdown seulement pour un plan ou un tableau.
- Données : connecteur (Search Console, Semrush, Ahrefs) s'il est là, sinon
  recherche web ou export collé par l'utilisateur. Dis toujours d'où vient un
  chiffre.
- Rien n'est publié par le Skill.
