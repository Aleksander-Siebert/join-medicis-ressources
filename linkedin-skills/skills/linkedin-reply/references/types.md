# Répondre sous ses propres posts : modèles et cas difficiles

Modèles d'après `reply-templates.md` (Serge Bulaev, `linkedin-reply-handler`,
MIT), réécrits en français. Exemples fictifs : Camille, acquisition chez
Assurly (assurly.example). Les chiffres viennent de son `reserve.md`.

## 1. Les 5 modèles

### R1 · Répondre

**Quand :** le commentaire pose une question directe.

```
{{Prénom}}, {{la réponse en une phrase}}.
{{un fait, un chiffre ou un vécu qui l'appuie}}.
```

> Sarah, à deux, en 3 semaines, avec un script de 5 questions.
> Le plus long a été de retrouver des numéros à jour. Vous gardez les
> coordonnées après résiliation ?

Ne renvoie pas en message privé une réponse qui tient ici.

### R2 · Concéder puis préciser

**Quand :** le commentaire conteste.

```
{{ce qui est juste, avec ses mots}}. Là où je tiens, c'est {{point précis}} :
{{un cas ou un chiffre}}.
```

> Marc, le prix compte, et chez certains de nos clients c'était la première
> raison. Là où je tiens, c'est l'ordre : sur nos 60 appels, la moitié citait
> le délai de remboursement avant le prix.

Une seule réponse. S'il revient une troisième fois avec le même argument, une
réaction suffit, ou « On ne sera pas d'accord sur ce point, et c'est très
bien. »

### R3 · Prolonger

**Quand :** le commentaire approuve avec une idée, ou ajoute un cas.

```
{{Prénom}}, ce que ton exemple rend possible : {{l'étape d'après}}.
{{où ça se voit déjà}}.
```

> Julie, et 60 appels suffisent quand les réponses se répètent vite. Chez
> nous, les derniers appels n'apprenaient plus rien de nouveau.

### R4 · Vécu

**Quand :** le fil reste théorique et l'utilisateur a un vrai cas.

```
On a vécu ça {{quand}}. {{ce qui a cassé, une ligne}}.
{{ce qui a marché, ou ce qu'on essaie encore}}. {{une réserve honnête}}.
```

> On a vécu ça en 2024 : le coût par lead montait chaque mois. Raccourcir le
> délai de remboursement l'a fait baisser en 4 mois. Je ne sais pas si ça
> tient sur un marché plus cher que le nôtre.

### R5 · Question en retour

**Quand :** le commentaire est flou, et sa réponse aiderait les deux.

```
{{Prénom}}, ça dépend de {{la pièce qui manque}}. Si {{cas A}}, je dirais
{{X}} ; si {{cas B}}, plutôt {{Y}}. Tu es dans lequel ?
```

> Thomas, ça dépend de qui résilie. Si ce sont des clients de moins d'un an,
> je regarderais l'accueil ; s'ils ont plus de trois ans, plutôt le prix. Tu
> es dans quel cas ?

## 2. Cas difficiles

| Cas | Ce qu'on fait | Exemple |
|---|---|---|
| **Critique juste, ton sec** | R2 ; concéder sans s'excuser trois fois | « Juste, le chiffre manquait de contexte : 60 appels sur {{n}} résiliations. » |
| **Critique de mauvaise foi, troll** | une réaction ou rien ; ne jamais répondre deux fois | (rien) |
| **Insulte, harcèlement** | ne pas répondre ; masquer ou signaler avec les outils de LinkedIn ; c'est l'utilisateur qui le fait | (rien) |
| **Erreur de l'utilisateur relevée** | reconnaître, corriger, remercier pour ce service précis | « Bien vu, c'est 41 € et pas 14 €. Merci, je corrige le post. » |
| **Question sans réponse connue** | le dire, donner ce qu'on sait, ou demander | « Je n'ai pas le chiffre sur les néo-assurances. Sur notre portefeuille, {{…}}. » |
| **Demande de prix en public** | pas de tarif dans le fil ; une ligne, puis message | « Ça dépend de la taille du portefeuille, je t'envoie le détail en message. » |
| **Concurrent qui se fait de la publicité** | rien, ou une réponse sur le fond s'il apporte quelque chose | (rien) |
| **Tag d'un tiers** (« @Marie regarde ») | une ligne pour accueillir Marie, si elle répond | « Marie, si ton équipe a fait l'exercice, je suis preneuse du résultat. » |
| **Demande « envoie-moi le modèle »** | seulement si l'utilisateur a vraiment ce modèle ; ne jamais le promettre à sa place | « Je te l'envoie en message. » + `/linkedin-dm` |
| **Commentaire très long et juste** | R3 ou R4, et le signaler à l'utilisateur comme idée de post (`journal.md`, registre des idées) | |

## 3. Réactions

| Commentaire | Réaction |
|---|---|
| idée, donnée, désaccord argumenté | Intéressant |
| félicitations, soutien | J'aime ou Bravo |
| vécu difficile | Soutien |

Pas de « J'aime » sur un commentaire avec lequel l'utilisateur n'est pas
d'accord : une réponse R2 ou rien.

## 4. Anti-modèles

- « Merci ! », « 100% », « Top », « Bonne remarque, je vais y réfléchir ».
- « Je t'écris en MP » en réponse à une question qui tenait dans le fil.
- Copier la même réponse sous dix commentaires.
- Le prénom suivi d'un point d'exclamation, la réponse plus longue que le
  commentaire sans raison.
- Le lien vers l'offre, le tarif, le Calendly.
- Tiret cadratin, triade d'adjectifs, « ce n'est pas X, c'est Y ».

## 5. Sources

- Serge Bulaev, `linkedin-reply-handler` (MIT) : modèles R1 à R5, règles de
  filtrage, rapport chiffré, 150 à 300 caractères. Ses « .. » pour les pauses
  et son plafond d'un tiret cadratin ne sont pas repris : la règle de
  l'utilisateur supprime le tiret.
- Taplio, `linkedin-warm-lead-finder` (MIT) : notation des leads, adaptée ici
  aux commentaires (4 dimensions, 10 points).
- Pack Join Médicis v1, `linkedin-reply` : catégories, règle du public
  d'abord.
