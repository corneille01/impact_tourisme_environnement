# Rapport de contre-expertise des anomalies OCS GE 2025 - D046

Date de verification : 25 novembre 2026. Aucune valeur source n a ete modifiee; les GeoPackages ont ete ouverts en lecture seule. Aucun indicateur territorial n a ete recalcule.

## Sources et methode

- GeoPackage d origine : [OCCUPATION_SOL.gpkg](../extracted/ocsge_2025_D046/OCS-GE_2-0__GPKG_LAMB93_D046_2025-01-01/OCS-GE/1_DONNEES_LIVRAISON_2026-10-00131/OCSGE_2-0_GPKG_LAMB93_D46-2025/OCCUPATION_SOL.gpkg).
- Controle de presence et d effectifs : [layers.csv](./layers.csv); types et contraintes SQLite declares : [fields.csv](./fields.csv); archives et empreintes : [downloads.csv](./downloads.csv).
- Comparaison auxiliaire avec [artif_2025_46.gpkg](../extracted/ocsge_artificialisation_2025_D046/OCS-GE_2-0_ARTIFICIALISATION_GPKG_LAMB93_D046_2025-01-01/artif_2025_46.gpkg). Les 299 787 ids correspondent exactement et les attributs communs controles sont identiques; les anomalies listees dans les deux CSV sont donc presentes dans les deux produits pour ces ids.
- Regles normatives : [DC_OCSGE_NG.pdf](https://data.geopf.fr/annexes/ressources/documentation/DC_OCSGE_NG.pdf), edition juin 2026, pp. 24-26. La nomenclature de livraison se trouve dans [NomenclatureOCSGE.csv](../extracted/ocsge_2025_D046/OCS-GE_2-0__GPKG_LAMB93_D046_2025-01-01/OCS-GE/3_SUPPLEMENTS_LIVRAISON_2026-10-00131/NomenclatureOCSGE.csv).

Les CSV d anomalies sont des extractions exhaustives, triees par `id`. Dans `anomalies_id_origine.csv` et `anomalies_code_or.csv`, `id_origine_is_sql_null=true` et une cellule brute vide signifient SQL NULL; ce n est pas une valeur `NC`. Toute valeur non nulle de `id_origine_value_raw` est conservee telle que lue, espaces compris. Les lignes sont sourcees par `OCCUPATION_SOL`, sans duplication par couche artificielle; `present_dans_artif_2025_46` indique l appariement par id.

## A. Regles IGN applicables

### `ID_ORIGINE` - descriptif IGN, section 4.1.2, p. 25; contraintes recapitulatives, section 4.1.3, p. 26

Le passage « Contrainte sur l’attribut » de la page 25 prescrit :

- si `OSSATURE=0` : `ID_ORIGINE=NC` ou une chaine de 24 caracteres;
- si `OSSATURE=1` et `SOURCE=BDTopo` : une chaine de 24 caracteres;
- si `OSSATURE=1` et `SOURCE=saisie` (cas exceptionnel) ou `calcul` : `ID_ORIGINE=NC`.

Le tableau « Attributs OCS GE » de la section 4.1.3, page 26, reprend les couples OSSATURE/CODE_OR/ID_ORIGINE/SOURCE : pour OSSATURE=1, OR1.1/OR1.2 associes a BDTopo et un id de 24 caracteres; les OR2.* associes a calcul et `NC`; OR3 associe a saisie et `NC`; pour OSSATURE=0, `CODE_OR=NC` et `ID_ORIGINE=NC ou Identifiant`, SOURCE etant liste sans contrainte specifique. Aucun des passages ne liste SQL NULL comme une valeur admissible. La colonne SQLite n est toutefois pas declaree `NOT NULL` dans [fields.csv](./fields.csv) : le schema physique autorise le NULL, mais cette permissivite ne l ajoute pas au domaine semantique IGN. Le retrait des espaces de remplissage est utilise uniquement pour verifier la longueur; la valeur brute est conservee dans le CSV.

### `CODE_OR` - descriptif IGN, section 4.1.2, p. 25; contraintes recapitulatives, section 4.1.3, p. 26

- si `OSSATURE=0` : `CODE_OR=NC`;
- si `OSSATURE=1`, `SOURCE=BDTopo` : `{OR1.1, OR1.2}`;
- si `OSSATURE=1`, `SOURCE=calcul` : `{OR2.1.1, OR2.1.2, OR2.2.1, OR2.2.2, OR2.2.3, OR2.2.4}`;
- si `OSSATURE=1`, `SOURCE=saisie` (cas exceptionnel) : `OR3`.

La p. 25 définit `CODE_OR` comme le type d’objet de l’Ossature dépendant de la méthode de création. La p. 26 résume ces correspondances sous « Contraintes entre attributs ». Le descriptif p. 24 précise que SOURCE est un type de données source et que, pour OSSATURE=1, ses valeurs possibles sont BDTopo, calcul ou saisie; OSSATURE=0 n’impose pas de domaine SOURCE. Les valeurs de `code_cs` et `code_us` sont fournies pour contexte dans les listes d’anomalies; aucun lien réglementaire de ces champs à la validité d’ID_ORIGINE/CODE_OR n’est invoqué ici.

## B. Anomalies confirmees

### 1. `id_origine` SQL NULL

Contre-expertise des 299 787 objets : **3 863 lignes** ont SQL NULL. Toutes violent le domaine conditionnel ci-dessus :

| OSSATURE | SOURCE | NULL observes | Regle applicable |
|---:|---|---:|---|
| 0 | saisie | 3 258 | `NC` ou chaine de 24 caracteres |
| 0 | calcul | 9 | `NC` ou chaine de 24 caracteres |
| 1 | calcul | 596 | `NC` |

Aucun SQL NULL n a ete trouve pour `OSSATURE=1, SOURCE=BDTopo`; aucun autre couple n est observe. Les autres valeurs non nulles controlees respectent le domaine de longueur/valeur de leur couple. Le fait que `id_origine` soit nullable dans SQLite est une propriete du schema, pas une exception a la contrainte de contenu IGN.

**Conclusion : non-conformite au domaine IGN confirmee, certitude elevee.** La cause (valeur manquante en production, livraison, conversion ou autre) est inconnue et ne peut pas etre determinee a partir des fichiers et documents consultes. Le CSV [anomalies_id_origine.csv](./anomalies_id_origine.csv) contient les 3 863 ids et les attributs contextuels. Les NULL ne sont ni remplis ni assimiles a `NC`.

### 2. `code_or` hors regle conditionnelle

**45 lignes** ne respectent pas la contrainte p. 25-26 :

| OSSATURE | SOURCE | CODE_OR observe | Valeur(s) prescrite(s) | Nombre |
|---:|---|---|---|---:|
| 0 | BDTopo | OR1.2 | NC | 2 |
| 0 | calcul | OR2.1.2 | NC | 1 |
| 1 | BDTopo | NC | OR1.1, OR1.2 | 38 |
| 1 | calcul | NC | OR2.1.1, OR2.1.2, OR2.2.1, OR2.2.2, OR2.2.3, OR2.2.4 | 4 |

Les quatre combinaisons sont explicitement couvertes par les règles; aucune exception de valeur `NC` pour OSSATURE=1/BDTopo ou OSSATURE=1/calcul n’est indiquée. Aucun objet OSSATURE=1/SOURCE=saisie n’est observé. **Non-conformité confirmée, certitude élevée** sur le constat; la cause des valeurs n’est pas vérifiable. La liste exhaustive et les champs utiles sont dans [anomalies_code_or.csv](./anomalies_code_or.csv).

Le recoupement entre populations trouve **3 ids** présentant à la fois SQL NULL sur `id_origine` et un `code_or` hors règle. Ce recoupement est indiqué par les colonnes booléennes des deux CSV; il ne change pas les effectifs de chaque anomalie.

## C. US235

La nomenclature de livraison associe à `US235` le libellé « Production secondaire, tertiaire et usage résidentiel ». Le PDF IGN de juin 2026, p. 6 et p. 21, emploie « Usage mixte » et définit explicitement ce groupe comme `US2` + `US3` + `US5`; il précise qu’une partie des usages non séparés demeure codée US235 en nouvelle génération. Dans les données D046, US235 apparaît 47 fois.

**Arbitrage :** les formulations sont semantiquement equivalentes, et les pieces ne demontrent pas une evolution du sens du code. Elles demontrent une variation de libelle entre le CSV fourni avec le paquet d octobre 2026 et le descriptif de juin 2026. Le CSV ne portant ni numero de version de nomenclature ni historique de changement, l origine precise de l ecart (libelle developpe, version ou incoherence editoriale) reste indeterminee. Les deux references sont conservees dans [analyse_divergence_US235.md](./analyse_divergence_US235.md); aucun code ni libelle source n a ete remplace.

## Limites

- L analyse etablit l ecart avec les contraintes textuelles IGN disponibles, pas la cause en amont ni l intention de production.
- Aucun contact ou erratum IGN n a ete consulte; aucune confirmation du producteur n est disponible.
- Le controle est attributaire : aucune geometrie n a ete modifiee, et aucun indicateur territorial ou surface n a ete recalcule.
- Les anomalies ont été extraites exhaustivement par SQL sur le GeoPackage d’origine; le CSV d’audit de champs confirme que les colonnes sont nullable au niveau SQLite. Cela ne vaut pas validation topologique des géométries.

## Resultat des controles de sortie

Les deux CSV d’anomalies contiennent respectivement 3 863 et 45 lignes de données, soit une ligne par entité, sans doublon d’id dans chaque fichier. Les documents Markdown conservent les citations de pages et les conclusions de certitude. Les quatre fichiers ont été relus après écriture; les totaux, les entêtes, le décodage UTF-8 et les identifiants sont vérifiés. Les GeoPackages originaux et les trois CSV d’audit existants n’ont pas été modifiés.
