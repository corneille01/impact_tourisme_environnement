# Rapport de validation de la base analytique — OCS GE 2025, D046

Date : 2026-11-25T06:38:32+01:00

## Contrôles réussis

- Les trois GeoPackages sources ont été analysés intégralement en flux :
  299 787 objets `OCCUPATION_SOL`, 26 599 `ZONE_CONSTRUITE`, 299 787
  `artif_2025_46`, en EPSG:2154. Les types réels, la validité, les nulles,
  les vides et les multiparties sont détaillés dans `rapport_geometries.md`.
- Les GeoPackages dérivés ont été relus intégralement : nombres, CRS, valeurs
  de tous les attributs source et égalité exacte des géométries. Résultats :
  `{"OCCUPATION_SOL": {"features": 299787, "attribute_value_differences": {}, "geometry_exact_mismatches": 0, "crs": "EPSG:2154", "fields": ["id", "code_cs", "code_us", "millesime", "source", "ossature", "id_origine", "code_or", "aire_geometrie_m2", "commune_insee_centroid", "commune_intersection_count"]}, "ZONE_CONSTRUITE": {"features": 26599, "attribute_value_differences": {}, "geometry_exact_mismatches": 0, "crs": "EPSG:2154", "fields": ["id", "millesime", "aire_geometrie_m2", "commune_insee_centroid", "commune_intersection_count"]}, "artif_2025_46": {"features": 299787, "attribute_value_differences": {}, "geometry_exact_mismatches": 0, "crs": "EPSG:2154", "fields": ["id", "code_cs", "code_us", "millesime", "source", "ossature", "id_origine", "code_or", "aire", "artif", "crit_seuil", "aire_geometrie_m2", "commune_insee_centroid", "commune_intersection_count"]}}`.
- ADMINEXPRESS-COG 2025 : 312 communes, codes uniques `46xxx`, attributs
  officiels présents et géométries MultiPolygon valides en EPSG:2154.
- `aire` : 299,787 valeurs comparées; 299,787
  correspondent à `round(surface géométrique, 2)`; aucune valeur nulle ou
  non positive.
- Les trois sources brutes ont des empreintes SHA-256 identiques avant et
  après le traitement : **True**. Les archives originales
  n'ont pas été ouvertes en écriture.

## Anomalies confirmées et réserves

- `id_origine` SQL NULL : **3,863** entités;
  `code_or` hors règle conditionnelle IGN : **45**;
  chevauchement entre les deux listes : **3**.
  Aucune valeur n'a été remplacée ou normalisée. Les nombres géographiques
  figurent dans `synthese_anomalies_spatiales.csv`; un objet multicommunal
  est compté dans chaque commune intersectée.
- La divergence documentaire du libellé `US235` reste conservée sous ses
  deux formulations dans les audits antérieurs; aucun arbitrage n'a été
  appliqué aux données.
- Les causes des anomalies attributaires restent inconnues; elles ne sont
  pas interprétées comme erreurs géométriques ou d'artificialisation.
- Le rattachement a détecté 10,824 entités multicommunales dans chacune des
  couches `OCCUPATION_SOL` et `artif_2025_46` (jusqu'à 16 communes par
  entité), et 1,310 dans `ZONE_CONSTRUITE` (jusqu'à cinq communes). Aucun
  objet n'est sans intersection surfacique positive.
- Les écarts `aire géométrique - somme des intersections communales` sont
  supérieurs à 0,01 m² pour 1,200 entités OCS/artificialisation identiques
  (251 dépassent 1 m²; maximum 1,602.242602 m²) et pour 98 entités
  `ZONE_CONSTRUITE` (six dépassent 1 m²; maximum 7.296791 m²). Aucun écart
  négatif inférieur à -0,01 m² n'a été observé. Ces écarts ne sont pas
  corrigés et leur cause n'est pas établie.
- Pour 32 entités OCS/artificialisation, le centroïde est hors des 312
  polygones communaux, bien que l'objet ait une intersection surfacique
  positive avec au moins une commune. Ces cas ne sont pas affectés
  arbitrairement; les coordonnées et distances sont dans
  `anomalies_rattachement_communes.csv`.

## Opérations effectuées

- Création de trois GeoPackages dérivés distincts, sans suppression
  d'entités : `occupation_sol_controlee.gpkg`,
  `artificialisation_2025_46_controlee.gpkg`,
  `zone_construite_controlee.gpkg`. Les attributs source sont conservés;
  `aire_geometrie_m2`, `commune_insee_centroid` et
  `commune_intersection_count` sont ajoutés. Le champ original `aire`
  demeure inchangé.
- Enregistrement des 312 limites communales officielles dans
  `communes_adminexpress_2025_D046.gpkg`. Source : WFS IGN/Geoplateforme
  `ADMINEXPRESS-COG.2025:commune`; licence déclarée sur data.gouv.fr :
  Licence Ouverte 2.0 (`lov2`).
- Création de `ocsge_commune_intersections.csv`, table sans géométrie
  contenant 651,911 relations entre entités et communes, aires
  d'intersection et parts surfaciques.
- Création de `anomalies_rattachement_communes.csv`, qui détaille les cas
  avec un écart de couverture supérieur à 1 m² et les centroïdes non
  attribués. Les écarts compris entre 0,01 et 1 m² sont comptabilisés dans
  ce rapport, mais ne figurent pas dans cette liste.
- Création des six livrables d'audit demandés sous `audit/`, dont le
  manifeste SHA-256. Le manifeste répertorie les fichiers de données et
  tables dérivés; les rapports narratifs sont vérifiés séparément.

## Limites méthodologiques et données prêtes

La relation par intersection de surface est recommandée pour une agrégation
communale; elle peut être plusieurs-à-plusieurs. Le centroïde est une
convention ponctuelle distincte et n'attribue pas arbitrairement les objets
sans couverture unique. Aucun découpage n'a été appliqué. Les écarts d'aire
de couverture sont détaillés dans `rapport_rattachement_communes.md`; ils ne
sont pas corrigés. Avant une agrégation, il faudra choisir explicitement
comment traiter ces résidus et les cas multicommunaux; ne pas renormaliser
les parts ni traiter les centroïdes non attribués comme des erreurs de
géométrie établies.

Les couches d'occupation du sol et d'artificialisation sont prêtes pour les
analyses spatiales futures, sous réserve de préserver les anomalies
attributaires et les limites de rattachement. `ZONE_CONSTRUITE` est conservée
séparément car sa métadonnée indique qu'elle est calculée depuis
`OCCUPATION_SOL`; elle ne doit pas être additionnée directement. Aucun
indicateur touristique ni lien causal tourisme/artificialisation n'a été
calculé. Les GeoPackages source et leurs valeurs n'ont pas été modifiés.

Le manifeste `manifest_base_analytique.csv` donne, pour chaque fichier de
données dérivé, le chemin, la source, la date, le CRS, le nombre d'entités,
l'empreinte SHA-256 et les transformations.
