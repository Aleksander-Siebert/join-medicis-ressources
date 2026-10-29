# Le Skill « ma-voix »

Un Skill autonome qui écrit dans la voix de la personne, partout, sans qu'elle
ait à joindre son fichier. Idée reprise de houtini-ai/voice-analyser-mcp
(Apache 2.0) : le Skill apprend par l'exemple, il contient de vrais textes et
demande d'en lire avant d'écrire.

## 1. Construire

```
python3 scripts/profil.py ma-voix tone-of-voice.md --nom "Camille" \
  --exemples textes/01.txt textes/02.txt textes/03.txt --zip --sortie .
```

Le script :

- nomme le Skill `ma-voix-<nom>` (spécification Agent Skills : 64 caractères
  au plus, minuscules, chiffres et tirets, égal au nom du dossier) ;
- écrit une description de 1 024 caractères au plus, qui dit quand
  l'utiliser et quand ne pas l'utiliser ;
- recopie les « jamais » de la section 6 dans le SKILL.md, parce que c'est ce
  qu'une IA respecte le mieux ;
- embarque le fichier de voix et les exemples, après retrait des emails, des
  téléphones et des noms précédés d'une civilité ;
- embarque `ecart.py` pour les outils qui exécutent du Python ;
- vérifie qu'il n'y a qu'un SKILL.md dans le ZIP.

**Avant de livrer**, relis les exemples : le script ne repère pas un prénom
seul (« Bravo à Inès et Théo »). Demande à la personne si ces prénoms peuvent
rester, sinon remplace-les.

**Choisir les exemples** : 3 à 6 textes, de canaux différents, écrits à la
main, ceux que la personne trouve les plus « elle ». Moins de 3 : le script
prévient.

## 2. Installer

| Outil | Comment | État |
|---|---|---|
| claude.ai | Personnaliser → Skills → importer le ZIP | chemin utilisé par les autres packs Join Médicis ; [à vérifier] à chaque changement d'interface |
| Claude Code | copier le dossier `ma-voix-<nom>/` dans `~/.claude/skills/` | format de dossier standard |
| Gemini | Personnaliser → Compétences → Importer le ZIP | testé avec le ZIP LinkedIn le 16 octobre 2026 |
| ChatGPT | chatgpt.com/skills (bêta) | [à vérifier] |
| Mistral | coller le contenu du SKILL.md et du fichier de voix dans les instructions de l'agent | l'import de Skills n'accepte ni dossier ni ZIP au 16 octobre 2026 |

## 3. Sans exécution de code

Pas de script, pas de ZIP. Donne à la personne, dans la conversation :

1. le contenu du `SKILL.md` (frontmatter compris), à enregistrer sous ce nom
   dans un dossier `ma-voix-<nom>` ;
2. le fichier de voix, à enregistrer sous le nom tone-of-voice.md dans un
   sous-dossier references ;
3. la marche à suivre pour zipper le dossier, ou, plus simple, le Projet
   claude.ai ou ChatGPT avec le fichier dans ses connaissances.

## 4. Mettre à jour

Le Skill « ma-voix » ne se modifie pas lui-même. Quand la voix change
(mode « Mettre à jour » de `/tone-of-voice`), reconstruis-le avec la même
commande et réimporte le ZIP : l'ancien est remplacé s'il porte le même nom.
