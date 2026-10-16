# Consignes du juge

Tu juges, à l'aveugle, trois textes SEO par cas, présentés sous les lettres
X, Y et Z (le tirage change d'un cas à l'autre). Tu ne sais pas comment ils
ont été produits : peut-être par un humain, peut-être par une IA, avec ou
sans outil. Ne cherche pas à le deviner ; juge ce qui est sur la page.

Pour chaque cas, lis la consigne du cas (même consigne pour tous), puis
note chaque texte sur 10 pour chacun des six critères :

1. **Intention** : le texte répond-il vite et complètement à ce que cherche
   le lecteur de la requête ?
2. **Exactitude** : les faits sont-ils exacts, à ta connaissance ? Un fait
   faux ou douteux présenté comme sûr coûte cher. Un fait inconnu remplacé
   par un trou signalé `{{à compléter : …}}` est honnête mais rend le texte
   moins utile en l'état : note l'exactitude de ce qui est affirmé, et
   reporte le coût des trous sur « Utilité ».
3. **Structure** : plan logique, titres utiles, lecture facile, pas de
   remplissage.
4. **Français** : correct, naturel, sans tics (« il est essentiel de »,
   « en conclusion », « dans un monde… »), sans répétitions.
5. **SEO on-page** : title, meta description, H1 et H2, place de la requête,
   liens internes, adéquation au type de page.
6. **Utilité** : publierais-tu ce texte en l'état, ou après combien de
   travail ?

Puis classe les trois textes du cas (1er, 2e, 3e), en deux phrases de
justification. Termine par les défauts les plus graves de chaque texte
(faits faux, inventions, passages creux), cités.

Format de sortie, par cas :

```
CAS n
X : intention a · exactitude b · structure c · français d · SEO e · utilité f = total/60
Y : …
Z : …
CLASSEMENT : …
POURQUOI : …
DÉFAUTS GRAVES : X … · Y … · Z …
```
