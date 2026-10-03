# Exemple : une session de commentaires

> Les faits de cet exemple sont fictifs (Assurly, Camille et leurs chiffres) : ils
> montrent la méthode. Ne les reprends jamais dans une réponse à l'utilisateur.

Utilisatrice fictive : Camille (acquisition, assurance en ligne). Elle colle
3 posts et le fichier de priorité qu'elle a noté avec l'aide du Skill
(`assets` non requis : le JSON tient dans la conversation).

## Priorité

```
python3 scripts/commentaire.py priorite --fichier posts.json
POSTS À COMMENTER
  1. [66/80] Directeur marketing d'un courtier · « Notre coût par lead a doublé en un an. On coupe le budget… »
     niveau relation : 2 à 4 phrases, ton vécu chiffré, une vraie question, aucun lien
  2. [51/80] Créatrice B2B · « On a arrêté les CV pour recruter nos commerciaux… »
     niveau visibilité : 1 à 2 phrases, une idée nette
  · écarté : Influenceur marketing (plus de 24 h et plus de 50 commentaires : un commentaire de plus serait enterré)
```

## Commentaire n°1 (relation)

Post : « Notre coût par lead a doublé en un an. On coupe le budget payant de
30% ce trimestre. Quelqu'un a trouvé mieux ? »

```
[Répondre à la question]
On a eu le même mur chez Assurly : coût par lead de 41 € en 2024. Avant de
couper, on a rappelé 60 clients partis ; la moitié parlait du délai de
remboursement, pas du prix. On a raccourci ce délai et le coût par lead est
redescendu à 23 € en 4 mois, à budget constant. Vous avez regardé ce que
disent vos résiliés ?
(contrôle : OK · apporte : 2024, 23, 4, 41, 60, assurl, cli, consta, delai, dis…)

[La pièce manquante]
Couper le budget traite le symptôme. La pièce qui manque souvent : le coût par
lead monte aussi quand les clients partent plus vite, parce qu'on rachète les
mêmes. Vous suivez le coût par lead et le taux de renouvellement ensemble ?

À publier : le 1, parce qu'il répond à sa question avec des chiffres vrais
(reserve.md) et finit sur une question qu'il peut vérifier chez lui.
Réaction suggérée : Intéressant.
```

Chaque chiffre vient de `reserve.md`. « Assurly » est citable (`contexte.md`).
Le produit de conseil de Camille n'est pas mentionné.

## Ce que le Skill a refusé

- « Super post, très inspirant ! 👏 » (bloqué : ouverture vide, rien de
  nouveau).
- « Je propose un audit gratuit, écris-moi en MP » (bloqué : autopromotion
  sous le post d'un autre).
- Demander à deux collègues de commenter le post de Camille dans la première
  heure (refusé : engagement artificiel ; alternative : qu'ils commentent s'ils
  ont quelque chose à ajouter).
