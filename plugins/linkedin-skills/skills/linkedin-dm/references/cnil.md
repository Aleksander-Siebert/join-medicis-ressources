# Prospection B2B sur LinkedIn : le cadre français

Ce n'est pas un avis juridique. C'est ce que disent les sources primaires,
avec leur date, et la façon prudente dont le pack les applique.

## 1. Ce que dit la CNIL

Source : CNIL, « La prospection commerciale par courrier électronique »
(cnil.fr, page mise à jour le 10 juin 2026, consultée le 2 octobre 2026).

| Règle | Citation |
|---|---|
| Base légale | la prospection de professionnels peut reposer sur « l'intérêt légitime » quand « l'objet de la sollicitation est en rapport avec la profession de la personne démarchée » |
| Exemple donné par la CNIL | « un appel présentant les mérites d'un logiciel au directeur informatique d'une entreprise » |
| Information et opposition | la personne « a été informée de la possible utilisation de son adresse électronique ou son numéro de téléphone […] pour de la prospection et est en mesure de s'y opposer » |
| Identification | chaque sollicitation « doit obligatoirement permettre à la personne concernée de prendre connaissance de l'identité de l'organisation qui l'émet » |

## 2. Ce que dit le RGPD

Règlement (UE) 2016/679, article 14 (données qui ne sont pas collectées
auprès de la personne, par exemple recopiées depuis son profil) :

- la personne est informée de l'identité du responsable, des finalités, de
  la base légale, de la source des données et de son droit d'opposition ;
- au plus tard **un mois** après l'obtention des données, ou **lors de la
  première communication** si les données servent à communiquer avec elle
  (article 14, paragraphe 3).

## 3. L'application prudente retenue par le pack

| Situation | Ce que fait le Skill |
|---|---|
| Message de prospection | en rapport avec le métier de la personne ; l'utilisateur est identifiable (son profil dit qui il est et pour qui il travaille) ; une phrase permet de dire non simplement |
| La personne dit non, ou ne répond pas après la relance | la séquence s'arrête ; `journal.md` : prochaine étape « aucune » |
| Le contact part dans un CRM | `/linkedin-inbox` prépare la ligne avec source, date et base légale ; l'utilisateur informe la personne au premier message (une phrase suffit : « J'ai noté vos coordonnées professionnelles pour ce suivi ; dites-le-moi si vous préférez que je les retire. ») |
| Extraction de profils, export de listes | refusé (garde-fou R2 ; aide LinkedIn a1341387) |
| Un message privé LinkedIn relève-t-il des règles du courrier électronique ? | **[à vérifier]** : pas de position CNIL trouvée sur la messagerie LinkedIn en particulier. Le pack applique les mêmes règles par prudence |

## 4. Phrases pour dire non simplement

À adapter au registre, une seule par message :

- « Si ce n'est pas le sujet, un mot suffit et je n'insiste pas. »
- « Pas besoin de répondre si vous êtes pris. »
- « Si ce n'est pas pour vous, dites-le-moi et je ne vous écrirai plus. »

## 5. Hors du champ de ce Skill

Particuliers (prospection B2C : consentement préalable pour le courrier
électronique), démarchage téléphonique, achat de fichiers. Le Skill le dit et
renvoie à la page de la CNIL.
