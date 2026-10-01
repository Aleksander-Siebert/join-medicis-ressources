<!-- aucun Skill équivalent dans ce pack : réponse d'assistant sans Skill -->

Voici une recherche prête à l'emploi. Je ne peux pas consulter LinkedIn en direct, donc je ne peux pas te lister les offres elles-mêmes, mais ces liens ouvrent directement la recherche filtrée et triée par date.

**Requête booléenne** (à coller dans le champ de recherche Emplois)

```
("Growth Manager" OR "Head of Growth" OR "Growth Marketing Manager" OR "Responsable acquisition" OR "Responsable growth" OR "Acquisition Manager") AND (SaaS OR B2B) NOT (stage OR stagiaire OR alternance OR alternant OR apprentissage OR internship)
```

- Les opérateurs AND, OR, NOT doivent être en majuscules.
- Les guillemets droits forcent l'expression exacte.
- Le NOT exclut les stages et alternances, et le filtre « Temps plein » (f_JT=F) fait le reste.

**Liens**

1. Paris, publiées dans les dernières 24 h, plus récentes d'abord :
https://www.linkedin.com/jobs/search/?keywords=%28%22Growth%20Manager%22%20OR%20%22Head%20of%20Growth%22%20OR%20%22Growth%20Marketing%20Manager%22%20OR%20%22Responsable%20acquisition%22%20OR%20%22Responsable%20growth%22%20OR%20%22Acquisition%20Manager%22%29%20AND%20%28SaaS%20OR%20B2B%29%20NOT%20%28stage%20OR%20stagiaire%20OR%20alternance%20OR%20alternant%20OR%20apprentissage%20OR%20internship%29&location=Paris%2C%20%C3%8Ele-de-France%2C%20France&f_TPR=r86400&f_JT=F&sortBy=DD

2. Télétravail en France, dernières 24 h :
https://www.linkedin.com/jobs/search/?keywords=%28%22Growth%20Manager%22%20OR%20%22Head%20of%20Growth%22%20OR%20%22Growth%20Marketing%20Manager%22%20OR%20%22Responsable%20acquisition%22%20OR%20%22Responsable%20growth%22%20OR%20%22Acquisition%20Manager%22%29%20AND%20%28SaaS%20OR%20B2B%29%20NOT%20%28stage%20OR%20stagiaire%20OR%20alternance%20OR%20alternant%20OR%20apprentissage%20OR%20internship%29&location=France&f_WT=2&f_TPR=r86400&f_JT=F&sortBy=DD

3. Paris, dernière semaine (si les 24 h donnent trop peu de résultats) :
https://www.linkedin.com/jobs/search/?keywords=%28%22Growth%20Manager%22%20OR%20%22Head%20of%20Growth%22%20OR%20%22Growth%20Marketing%20Manager%22%20OR%20%22Responsable%20acquisition%22%20OR%20%22Responsable%20growth%22%20OR%20%22Acquisition%20Manager%22%29%20AND%20%28SaaS%20OR%20B2B%29%20NOT%20%28stage%20OR%20stagiaire%20OR%20alternance%20OR%20alternant%20OR%20apprentissage%20OR%20internship%29&location=Paris%2C%20%C3%8Ele-de-France%2C%20France&f_TPR=r604800&f_JT=F&sortBy=DD

4. Paris, dernière heure (astuce non officielle) :
https://www.linkedin.com/jobs/search/?keywords=%28%22Growth%20Manager%22%20OR%20%22Head%20of%20Growth%22%20OR%20%22Growth%20Marketing%20Manager%22%20OR%20%22Responsable%20acquisition%22%20OR%20%22Responsable%20growth%22%20OR%20%22Acquisition%20Manager%22%29%20AND%20%28SaaS%20OR%20B2B%29%20NOT%20%28stage%20OR%20stagiaire%20OR%20alternance%20OR%20alternant%20OR%20apprentissage%20OR%20internship%29&location=Paris%2C%20%C3%8Ele-de-France%2C%20France&f_TPR=r3600&f_JT=F&sortBy=DD

**Ce que font les paramètres**

- `f_TPR=r86400` : publiées dans les dernières 24 h (86 400 secondes). `r604800` = 7 jours.
- `f_TPR=r3600` : dernière heure. Ce n'est pas un filtre proposé dans l'interface : LinkedIn accepte la valeur dans l'URL aujourd'hui, mais rien ne garantit que ça dure, et sur une recherche aussi ciblée tu auras souvent zéro résultat.
- `sortBy=DD` : tri par date, plus récentes en premier.
- `f_WT=2` : télétravail (1 = sur site, 3 = hybride).
- `f_JT=F` : temps plein, ce qui écarte les offres classées « Stage ».

**Conseils**

- Crée une alerte depuis le lien 1 (bouton « Créer une alerte ») : tu recevras les nouvelles offres chaque jour sans refaire la recherche.
- Si tu veux aussi l'hybride à Paris, ajoute `&f_WT=1%2C2%2C3` ou retire simplement le paramètre f_WT.
- Le terme « SaaS » n'apparaît pas toujours dans l'offre. Si la liste te semble trop courte, enlève `AND (SaaS OR B2B)` et trie à la main.
