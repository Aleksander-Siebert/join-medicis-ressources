Réponse courte : ton brouillon faisait très IA (21,5/100, SIGNALÉ). Le script seul ne suffisait pas (32,2, toujours SIGNALÉ) : il retire le tiret cadratin et le gras, mais les tics de structure demandent une vraie réécriture. Après réécriture, le texte obtient 78,7, OK.

Voici le texte, prêt à copier :

```
La prospection LinkedIn n'est pas morte. Elle a changé, et nos chiffres le montrent.

En mars, on a envoyé 412 messages. 9 réponses.
En avril, 60 messages. 14 réponses.

Les décideurs reçoivent trop de messages pour lire ceux qui pourraient partir chez n'importe qui. Alors on a arrêté de compter les envois.

Chaque message est maintenant écrit pour une seule personne. Il part au moment où elle a une raison de le lire, sur le canal où elle répond. Et la relance apporte quelque chose de neuf, sinon on ne l'envoie pas.

Ça demande plus de travail par message. Mais 14 réponses sur 60, ça fait 23 %. En mars, on était à 2 %.

Ta dernière campagne, c'était combien de messages pour combien de réponses ?

#Prospection #B2B
```

LA NOTE (detect.py, cinq contrôles)

```
                   brouillon   script seul   réécrit
RYTHME               100,0        99,9         62,8
PRÉCISION             37,9        41,4        100,0
TICS                   0,0         0,0        100,0
EMPREINTE             16,2       100,0        100,0
VOIX                  25,2        27,4         83,8
SCORE HUMAIN          21,5        32,2         78,7
verdict             SIGNALÉ     SIGNALÉ        OK
```

Contrôle le plus faible maintenant : le rythme (62,8), au-dessus du seuil de 55. Si tu veux gagner encore, varie davantage la longueur des phrases du paragraphe « Chaque message… ».

CE QUI A ÉTÉ CORRIGÉ AUTOMATIQUEMENT (humanize.py, 7 corrections)
- 1 tiret cadratin remplacé par une virgule (après « n'est pas morte »)
- 3 gras Markdown retirés (LinkedIn affiche les ** tels quels)
- « il est important de noter que » supprimé, « une véritable » → « une », « afin de » → « pour »

CE QUE J'AI RÉÉCRIT À LA MAIN (26 passages signalés par le script)
- « 🚀 Et si je vous disais… » : ouverture usée et émoji décoratif. Le post commence par le fait.
- « Dans un monde en constante évolution » : supprimé.
- « Ce n'est pas une question de volume, c'est une question de pertinence » : remplacé par la preuve elle-même (412 messages → 9 réponses, 60 messages → 14 réponses).
- « Le résultat ? Une révolution dans notre approche » : pont de révélation. Le résultat est donné directement (23 % contre 2 %).
- « Par ailleurs… De plus… stratégie holistique… levier crucial… répondre aux besoins… témoignant de notre engagement » : paragraphe vide, supprimé.
- La liste « ✅ Personnalisation : / ✅ Timing : / ✅ Suivi : » : réécrite en phrases, sans émojis, en gardant les trois idées (message unique, bon moment et bon canal, relance utile).
- « En somme, l'avenir s'annonce prometteur. Qu'en pensez-vous ? » : conclusion vide et question réflexe, remplacées par une question que seul ce post peut poser.
- 6 hashtags ramenés à 2.

À VÉRIFIER AVANT DE PUBLIER
- J'ai changé le fond sur un point : le brouillon ne contenait aucun fait, alors j'ai repris les chiffres de ton voix.md (9 réponses sur 412 en mars, 14 sur 60 en avril). Je suppose qu'il s'agit de messages LinkedIn ; si ce sont des e-mails ou un mélange, dis-le et j'ajuste la première ligne. Si tu ne veux pas les citer, je reviens à ton texte avec {{ton chiffre}} à la place.
- Le brouillon vouvoyait (« Et si je vous disais ») ; je suis passé au tutoiement, comme dans tes autres posts.
- 23 % et 2 % sont des arrondis (14/60 = 23,3 % ; 9/412 = 2,2 %).

Pour être honnête sur la note : ce sont cinq heuristiques locales, construites sur les signaux qu'utilisent les détecteurs publics et les contributeurs de Wikipédia. Ce n'est ni GPTZero, ni Originality, ni Compilatio, et personne ne peut te garantir un texte « indétectable ». Corriger ce qu'elles mesurent fait en général bouger ces outils, parce qu'ils regardent la même chose. Et ces signes orientent, ils ne prouvent rien : ce qui trahissait ton brouillon, c'était l'accumulation de tics et l'absence de faits derrière.
