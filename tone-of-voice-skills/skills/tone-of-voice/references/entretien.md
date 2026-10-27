# Collecte et questions

## 1. Quels textes demander

Ordre de valeur, du plus révélateur au moins révélateur :

1. **Messages écrits vite** : WhatsApp, Slack, emails à des clients ou à
   l'équipe. Personne ne les a polis : la voix y est entière.
2. **Posts et commentaires** (LinkedIn, Instagram) écrits par la personne.
3. **Newsletters, articles**.
4. **Pages du site, plaquettes** : souvent relues par plusieurs personnes,
   donc moins personnelles. À garder pour la voix de marque.

À écarter, et à dire pourquoi :

- textes écrits ou retouchés par une IA (on copierait la voix de l'IA) ;
- textes juridiques, conditions générales, communiqués relus par d'autres ;
- textes co-écrits, sauf si l'on veut la voix de l'équipe ;
- citations d'autres personnes, partages, modèles d'emails non personnalisés.

**Combien.** 3 textes et 500 mots au minimum pour mesurer. 5 à 10 textes,
de 2 ou 3 contextes différents (un post, un email, un message), c'est mieux :
on voit ce qui reste constant quand le sujet change. Au-delà de 30 textes,
`voix.py` refuse : garder les plus représentatifs.

**Formats.** Collés dans la conversation, ou fichiers .txt / .md. Un .docx ou
un PDF : demander de copier le texte. Plusieurs textes dans un seul fichier :
les séparer par une ligne `---`.

**Message type** (à adapter) :

> Pour trouver ta voix, j'ai besoin de 5 à 10 textes que tu as écrits toi-même,
> sans IA : des messages ou des emails écrits vite, quelques posts, une page
> de ton site. Plus c'est spontané, mieux c'est. Colle-les ici, un par message
> ou séparés par une ligne « --- ».

## 2. Les trois entrées

| Entrée | Ce qu'on fait | Ce qu'on dit |
|---|---|---|
| **Ses textes** | parcours complet | rien de spécial |
| **Un style à émuler** | `voix.py` sur les textes admirés ; on en tire des traits, pas des phrases ; on demande aussi 2 textes de la personne pour voir l'écart | « On s'inspire de ce style, on ne le copie pas : ses tournures signatures restent les siennes. » |
| **Rien** | toutes les questions de la banque (12 au plus, en 3 blocs), puis calibrage à 3 tours | « Sans texte, la voix est une hypothèse : confiance faible, on la recalcule dès que tu as 5 textes. » |

Une personne peut combiner : ses textes plus un style qui l'inspire. Dans ce
cas, la section 2 du fichier garde la voix réelle, et une ligne « Vers où je
veux aller » note l'écart choisi (voir `references/format.md`).

**Personne ou marque.** Une personne écrit « je » ; une marque écrit « nous »
ou « on », et sa voix doit pouvoir être tenue par plusieurs personnes. Pour une
marque, prendre des textes de 2 auteurs au moins, et laisser `voix.py`
signaler l'auteur qui s'écarte.

## 3. Règles des questions

- **Seulement ce que les textes ne disent pas.** Si 5 textes sur 5 vouvoient,
  ne demande pas « tu ou vous ? » : écris « vouvoiement (5 textes sur 5) ».
- **5 à 7 questions**, par blocs de 2 ou 3, jamais d'interrogatoire de 15.
- **Questions fermées avec une proposition.** « Je propose : pas d'émoji sur
  LinkedIn, tu n'en mets dans aucun post. D'accord ? » plutôt que « Que
  penses-tu des émojis ? ».
- **Chaque réponse finit dans le fichier**, avec sa source : « (entretien) ».
- Une réponse floue (« ça dépend ») devient une question ouverte du fichier,
  avec une proposition.

## 4. Banque de questions

Choisir celles dont la réponse manque. L'ordre donné est l'ordre conseillé.

| # | Question | Sert à |
|---|---|---|
| 1 | À qui écris-tu le plus souvent ? (clients, prospects, équipe, communauté) | section 1, canaux |
| 2 | Quels canaux veux-tu couvrir ? (LinkedIn, email, site, WhatsApp, newsletter) | section 8 |
| 3 | Tu tutoies ou tu vouvoies, et est-ce que ça change selon le canal ? | section 4 et 8 |
| 4 | L'humour : jamais, de l'autodérision, des clins d'œil, franchement drôle ? | curseur sérieux / drôle |
| 5 | Trois mots que tu ne veux jamais voir sous ton nom ? | section 6 |
| 6 | Un texte (à toi ou pas) dont tu t'es dit « ça, c'est exactement moi » ? | traits, extraits |
| 7 | Un texte qui t'a fait dire « jamais je n'écrirais ça » ? | section 6, « Pas » des traits |
| 8 | Sur quels sujets tu tranches sans précaution ? Où tu préfères nuancer ? | section 7 |
| 9 | Tu parles de tes erreurs et de tes chiffres en public ? | traits, section 7 |
| 10 | Comment tu signes un email ? Comment tu commences un message ? | section 8 |
| 11 | Des mots de ton métier que tu assumes, ou que tu évites ? | section 5 et 6 |
| 12 | Si ta voix était une personne, ce serait qui pour tes clients ? (un voisin, un expert, un coach, un ami) | section 1 |

Pour une marque, remplacer « tu » par « la marque » et ajouter : « Qui écrit
aujourd'hui au nom de la marque ? », « Quelles règles existent déjà (charte,
guide) ? ». Une charte existante est une source : ses règles entrent dans le
fichier avec « (charte, date) », et on vérifie dans les textes si elle est
appliquée.
