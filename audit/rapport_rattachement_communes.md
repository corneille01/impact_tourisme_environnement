# Rapport de rattachement spatial aux communes — Lot (D046)

Date de traitement : 2026-11-25T06:38:32+01:00

## Source administrative vérifiée

Source : couche WFS officielle IGN/Geoplateforme
`ADMINEXPRESS-COG.2025:commune`, interrogée sur
`code_insee_du_departement = '46'` avec `srsName=EPSG:2154`.
Endpoint : [`https://data.geopf.fr/wfs`](https://data.geopf.fr/wfs). Le produit ADMIN EXPRESS COG est déclaré
par l'IGN sur
[data.gouv.fr](https://www.data.gouv.fr/datasets/admin-express-admin-express-cog-admin-express-cog-carto-admin-express-cog-carto-pe-admin-express-cog-carto-plus-pe/),
avec la licence `lov2` (Licence Ouverte 2.0).

Résultat contrôlé : **312 communes**, 312 codes INSEE distincts au format
`46xxx`, tous rattachés au département 46; champs `code_insee`,
`nom_officiel`, `code_insee_du_departement`; géométries MultiPolygon non
nulles, non vides et valides; CRS WFS et couche enregistrée EPSG:2154. Le
millésime est 2025, cohérent avec les couches OCS GE étudiées. La réponse WFS
annonce `numberMatched=312`. La source est enregistrée dans
`data/processed/ocsge/communes_adminexpress_2025_D046.gpkg`.

## Méthodes et résultats

- **Centroïdes** : le centroïde géométrique de chaque objet est testé contre
  les communes. `commune_insee_centroid` n'est renseigné que si exactement une
  commune couvre le point; zéro ou plusieurs candidats restent non attribués.
  Cette méthode fournit un code ponctuel pratique, mais ne décrit pas la
  surface dominante ni les franchissements de limites.
- **Intersection de surface** : un index spatial identifie les communes
  intersectées; les intersections surfaciques strictement positives sont
  mesurées. Chaque relation est dans `ocsge_commune_intersections.csv`, avec
  aire et part de l'objet. Un objet traversant plusieurs communes apparaît
  dans plusieurs lignes.
- **Aucun découpage géométrique** : aucune géométrie source n'est coupée ou
  remplacée; les intersections sont calculées uniquement pour mesurer la
  relation spatiale.

| Couche | Entités | Sans intersection de surface | Dans plusieurs communes | Max. communes/entité | Centroïde sans attribution unique | Centroïde dans plusieurs communes | Relations surfaciques | Écart max couverture (m²) | Écart > 1 m² |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `OCCUPATION_SOL` | 299,787 | 0 | 10824 | 16 | 32 | 0 | 311,969 | 1602.242602 | 251 |
| `ZONE_CONSTRUITE` | 26,599 | 0 | 1310 | 5 | 0 | 0 | 27,973 | 7.296791 | 6 |
| `artif_2025_46` | 299,787 | 0 | 10824 | 16 | 32 | 0 | 311,969 | 1602.242602 | 251 |

Les 10,824 entités multicommunales d'`OCCUPATION_SOL` et
`artif_2025_46` sont les mêmes identifiants : les géométries de ces deux
couches sont identiques. Les relations sont retenues pour une aire
d'intersection strictement positive; de très petits recouvrements comptent
donc comme des relations. Aucun découpage n'a été appliqué.

### Écarts entre l'aire des objets et la couverture communale

L'écart est défini comme `aire géométrique source - somme des intersections
surfaciques avec les communes`. Un écart positif signifie qu'une partie de
l'aire source n'est pas couverte par la somme des intersections mesurées; un
écart négatif signifie que cette somme dépasse l'aire source. Ces écarts sont
rapportés, non corrigés.

| Couche | Écarts > 0,01 m² | Écarts > 1 m² | Maximum positif (m²) | Écarts < -0,01 m² |
|---|---:|---:|---:|---:|
| `OCCUPATION_SOL` | 1,200 | 251 | 1,602.242602 | 0 |
| `artif_2025_46` | 1,200 | 251 | 1,602.242602 | 0 |
| `ZONE_CONSTRUITE` | 98 | 6 | 7.296791 | 0 |

Les écarts OCS GE et artificialisation sont identiques puisque leurs géométries
sont identiques. La liste complémentaire
`audit/anomalies_rattachement_communes.csv` contient les 251 identifiants
distincts OCS/artificialisation dont l'écart dépasse 1 m², les six entités
`ZONE_CONSTRUITE` dépassant ce seuil et les 32 cas de centroïde hors des
polygones communaux. Elle ne liste pas les 949 autres écarts OCS et les 92
autres écarts `ZONE_CONSTRUITE` compris entre 0,01 et 1 m².

Les écarts positifs peuvent être liés aux limites, à leur précision ou à la
topologie des couches, mais leur cause n'est pas établie. Ils ne constituent
pas à eux seuls une preuve d'erreur dans les données OCS GE ni dans les
limites communales. Aucun écart négatif supérieur à 0,01 m² n'a été observé.

### Centroïdes sans attribution communale

Les 32 centroïdes OCS/artificialisation non attribués sont hors des 312
polygones communaux retenus, alors que chaque entité a au moins une
intersection surfacique positive avec une commune. La distance au polygone
communal le plus proche varie de 0,79 à 562,78 m. Le centroïde d'un objet
peut être extérieur à sa géométrie; les cas ne démontrent donc pas à eux seuls
un défaut de couverture administrative. Leur cause reste à examiner avec les
géométries adjacentes et les limites sources. Les identifiants, coordonnées,
communes intersectées et distances sont consignés dans le CSV complémentaire.

Les franchissements de communes sont déterminés par des intersections de
surface strictement positives, et non par un simple contact de frontière.
`ZONE_CONSTRUITE` présente 1,310 objets multicommunaux (jusqu'à cinq communes);
aucun centroïde de cette couche n'est resté sans attribution unique.

## Recommandation d'exploitation

Pour une future agrégation de surfaces, utiliser la table de relations et les
parts surfaciques, en documentant le traitement des écarts de couverture.
Utiliser le centroïde seulement lorsqu'une convention ponctuelle est souhaitée,
et conserver les 32 cas non attribués sans affectation arbitraire. Il faudra
examiner les écarts de couverture avant toute agrégation communale; ne pas
renormaliser les parts ni répartir les résidus sans règle explicite.
`ZONE_CONSTRUITE` est gardée à part : la métadonnée de livraison précise
qu'elle est calculée à partir de `OCCUPATION_SOL`; ne pas additionner ses
surfaces à celles de l'occupation du sol.
