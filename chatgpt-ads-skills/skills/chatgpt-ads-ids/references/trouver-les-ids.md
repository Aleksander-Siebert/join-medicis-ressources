# Trouver les identifiants ChatGPT Ads, pas à pas

Sources : documentation développeur d'OpenAI Ads (relue le 20 oct. 2026).
L'interface d'Ads Manager change souvent et n'est pas documentée écran par
écran : les chemins dans l'interface sont marqués **[à vérifier]** et se
complètent avec des captures du compte de l'utilisateur.

## Voie A : l'API, en lecture seule

1. **Créer une clé** : Ads Manager > Settings > clé d'API (documentation :
   « Settings tab in Ads Manager »). Une clé ne donne accès qu'à **un**
   compte publicitaire.
2. **La définir dans son terminal**, jamais dans la conversation :
   - macOS, Linux : `export OPENAI_ADS_API_KEY="…"`
   - Windows PowerShell : `$env:OPENAI_ADS_API_KEY="…"`
3. **Vérifier le compte** : `python3 scripts/ids.py compte` (nom, devise,
   fuseau, statut).
4. **Lister** : `python3 scripts/ids.py lister -o ids.csv`, puis
   `--annonces` pour les annonces et leurs images.

Ce que fait le script, et seulement cela : `GET /ad_account`,
`GET /campaigns`, `GET /ad_groups?campaign_id=…`, `GET /ads?ad_group_id=…`,
`GET /conversions/event_settings`, avec pagination (500 par page) et
nouvel essai en cas de limite de débit (600 requêtes par minute et par
point d'accès, documentation). La commande `televerser` est la seule qui
écrit (`POST /upload`), et seulement avec `--confirmer`.

## Voie B : un export

1. Dans Ads Manager, ouvrir la liste des ad groups (ou des annonces) de la
   campagne **[à vérifier : nom du menu]**.
2. Afficher la colonne d'identifiant si elle est masquée **[à vérifier]**.
3. Exporter en CSV ou XLSX **[à vérifier : bouton d'export]**.
4. `python3 scripts/ids.py depuis-fichier export.csv -o ids.csv` repère les
   identifiants par préfixe, où qu'ils soient dans le fichier, et les noms
   par en-tête (« Ad group name », « Nom du groupe d'annonces »…).

## Voie C : recopie guidée (sans terminal)

1. Créer les ad groups dans Ads Manager à partir de la fiche de
   paramétrage.
2. Pour chaque ad group, copier son identifiant **[à vérifier : où il
   s'affiche]** dans une table à deux colonnes : `adgroup_name`,
   `ad_group_id`.
3. Coller cette table dans la conversation : l'assistant reporte les
   identifiants dans les lignes du classeur et signale tout nom introuvable
   ou en double.
4. Mettre les colonnes d'identifiants au format Texte dans le tableur avant
   de coller (sinon Excel peut les abîmer, `/chatgpt-ads-excel`).

## Les identifiants dans l'analyse d'audience

Avec ce modèle de paramètres de suivi (commande `utm`), chaque visite issue
d'une annonce porte l'identifiant de sa campagne et de son annonce :

```
utm_source=chatgpt&utm_medium=paid&utm_campaign={campaign_id}&utm_content={ad_id}&click_id={oppref}
```

Les paramètres se règlent au niveau du compte, de la campagne, de l'ad
group ou de l'annonce ; le niveau le plus fin l'emporte sur une même clé
(documentation). Pour la France, ces paramètres ne déposent rien sur
l'appareil : ce n'est pas un traceur, mais l'outil d'analyse qui les lit
doit respecter le consentement.

## Erreurs fréquentes

| Erreur | Conséquence | Prévention |
|---|---|---|
| `ad_id` rempli sur une nouvelle annonce | l'import modifie une annonce existante **[à vérifier]** | laisser `ad_id` vide pour une création |
| identifiant d'un autre compte | annonce refusée ou introuvable | une clé et un export par compte |
| identifiant tapé à la main | ligne rejetée | toujours copier-coller, puis `/chatgpt-ads-excel` |
| identifiant devenu `1,23E+15` | perdu | colonnes au format Texte avant de coller |
